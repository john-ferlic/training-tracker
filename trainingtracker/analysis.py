"""Turn fetched data + the plan into a structured daily assessment and a
rule-based verdict. The same structured output is what Claude reasons over for
the richer interactive briefing.
"""
from __future__ import annotations

import statistics
from datetime import date, timedelta
from typing import Any, Optional

from . import plan as plan_mod

HARD_TYPES = {"VO2max", "Threshold", "Anaerobic", "Race"}
MODERATE_TYPES = {"Tempo", "SweetSpot"}
EASY_TYPES = {"Endurance", "Recovery"}


def _median(values: list[float]) -> Optional[float]:
    vals = [v for v in values if v is not None]
    return statistics.median(vals) if vals else None


def _rides_by_date(rides: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    out: dict[str, list[dict[str, Any]]] = {}
    for r in rides:
        d = r.get("date")
        if d:
            out.setdefault(d, []).append(r)
    return out


def assess_recovery(
    oura_days: dict[str, Any], today: date, thresholds: dict[str, Any], athlete: dict[str, Any]
) -> dict[str, Any]:
    """Classify today's recovery as green/amber/red from Oura signals."""
    key = today.isoformat()
    today_data = oura_days.get(key, {})

    # Baselines from the trailing window (exclude today), falling back to config.
    prior = [v for k, v in oura_days.items() if k < key]
    rhr_baseline = _median([d.get("resting_hr") for d in prior]) or athlete.get("resting_hr")
    hrv_baseline = _median([d.get("average_hrv") for d in prior])

    readiness = today_data.get("readiness")
    sleep_score = today_data.get("sleep_score")
    resting_hr = today_data.get("resting_hr")
    hrv = today_data.get("average_hrv")
    total_sleep_h = today_data.get("total_sleep_h")

    flags: list[str] = []
    if readiness is not None and readiness < thresholds["readiness_low"]:
        flags.append(f"Oura readiness {readiness} (below {thresholds['readiness_low']})")
    if sleep_score is not None and sleep_score < thresholds["sleep_low"]:
        flags.append(f"sleep score {sleep_score} (below {thresholds['sleep_low']})")
    if (
        resting_hr is not None
        and rhr_baseline
        and resting_hr >= rhr_baseline + thresholds["resting_hr_elevated"]
    ):
        flags.append(f"resting HR {resting_hr} (+{round(resting_hr - rhr_baseline)} vs baseline)")
    if (
        hrv is not None
        and hrv_baseline
        and hrv <= hrv_baseline * (1 - thresholds["hrv_drop_pct"] / 100)
    ):
        flags.append(f"HRV {hrv} ({round((hrv/hrv_baseline-1)*100)}% vs baseline)")

    if readiness is None and sleep_score is None:
        status = "unknown"
    elif (readiness is not None and readiness < 60) or len(flags) >= 2:
        status = "red"
    elif len(flags) == 1:
        status = "amber"
    else:
        status = "green"

    return {
        "status": status,
        "flags": flags,
        "readiness": readiness,
        "sleep_score": sleep_score,
        "total_sleep_h": total_sleep_h,
        "resting_hr": resting_hr,
        "resting_hr_baseline": round(rhr_baseline) if rhr_baseline else None,
        "hrv": hrv,
        "hrv_baseline": round(hrv_baseline) if hrv_baseline else None,
    }


def assess_last_workout(
    rides: list[dict[str, Any]], plan: dict[str, Any], today: date, thresholds: dict[str, Any]
) -> Optional[dict[str, Any]]:
    """Find the most recent ride (today or before) and compare it to what was
    planned for that day. Detect 'harder than expected'."""
    by_date = _rides_by_date(rides)
    for offset in range(0, 8):
        d = today - timedelta(days=offset)
        day_rides = by_date.get(d.isoformat())
        if not day_rides:
            continue
        ride = max(day_rides, key=lambda r: r.get("tss") or 0)
        planned = plan_mod.workout_for(plan, d)

        notes: list[str] = []
        harder = False
        easier = False
        target_if = planned.get("target_if")
        if target_if and ride.get("intensity_factor"):
            delta = ride["intensity_factor"] - target_if
            if delta > thresholds["if_overshoot"]:
                harder = True
                notes.append(
                    f"IF {ride['intensity_factor']} vs target {target_if} (+{round(delta,2)})"
                )
            elif delta < -thresholds["if_overshoot"]:
                easier = True
                notes.append(f"IF {ride['intensity_factor']} below target {target_if}")
        if ride.get("decoupling_pct") is not None and ride["decoupling_pct"] > thresholds[
            "decoupling_high"
        ]:
            harder = True
            notes.append(
                f"aerobic decoupling {ride['decoupling_pct']}% "
                f"(>{thresholds['decoupling_high']}% = cardiac drift / fatigue)"
            )
        iv = ride.get("intervals")
        if iv and iv.get("fade_pct") is not None and iv["fade_pct"] >= 4:
            harder = True
            notes.append(
                f"faded {iv['fade_pct']}% across {iv['count']} intervals "
                f"(struggled on the later reps)"
            )
        target_tss = planned.get("target_tss")
        if target_tss and ride.get("tss"):
            ratio = ride["tss"] / target_tss
            if ratio < 0.6:
                notes.append(f"TSS {ride['tss']} well under planned {target_tss} (cut short?)")

        return {
            "days_ago": offset,
            "date": d.isoformat(),
            "ride": ride,
            "planned": planned,
            "harder_than_expected": harder,
            "easier_than_expected": easier and not harder,
            "notes": notes,
        }
    return None


def recent_load(rides: list[dict[str, Any]], today: date) -> dict[str, Any]:
    by_date = _rides_by_date(rides)
    def tss_window(days: int) -> int:
        total = 0.0
        for offset in range(days):
            d = (today - timedelta(days=offset)).isoformat()
            for r in by_date.get(d, []):
                total += r.get("tss") or 0
        return round(total)

    return {"tss_7d": tss_window(7), "tss_3d": tss_window(3), "rides_7d": sum(
        len(by_date.get((today - timedelta(days=o)).isoformat(), [])) for o in range(7)
    )}


def _intensity(workout_type: Optional[str]) -> str:
    if workout_type in HARD_TYPES:
        return "hard"
    if workout_type in MODERATE_TYPES:
        return "moderate"
    if workout_type in EASY_TYPES:
        return "easy"
    if workout_type == "Rest":
        return "rest"
    return "unknown"


def make_verdict(
    recovery: dict[str, Any],
    last_workout: Optional[dict[str, Any]],
    load: dict[str, Any],
    today_plan: dict[str, Any],
    thresholds: dict[str, Any],
) -> dict[str, Any]:
    """Rule-based recommendation. Returns one of PROCEED / MODIFY / PUSH / REST
    with reasons. This is the offline fallback; Claude can refine it."""
    today_type = today_plan.get("type")
    intensity = _intensity(today_type)
    reasons: list[str] = []

    rec = recovery["status"]
    harder = bool(last_workout and last_workout["harder_than_expected"])
    high_load = load["tss_7d"] > thresholds["tss_ramp_7d_high"]

    if intensity == "rest":
        return {
            "verdict": "REST",
            "headline": "Rest day — keep it a rest day.",
            "reasons": ["Plan calls for rest."]
            + (["Recovery markers are low, so this is well timed."] if rec in ("amber", "red") else []),
        }

    if rec == "red":
        if intensity in ("hard", "moderate"):
            verdict = "MODIFY"
            headline = f"Swap today's {today_type} for easy Z2 or rest."
            reasons.append("Recovery is red: " + "; ".join(recovery["flags"]))
            reasons.append("Training hard into poor recovery raises injury/illness risk for little gain.")
        else:
            verdict = "PROCEED"
            headline = f"Keep today's {today_type}, but truly easy."
            reasons.append("Recovery is red: " + "; ".join(recovery["flags"]))
            reasons.append("Easy day is fine — cap the intensity and stop if it feels off.")
    elif rec == "amber":
        if intensity == "hard" and (harder or high_load):
            verdict = "MODIFY"
            headline = f"Trim today's {today_type} (reduce intervals ~25-30%)."
            reasons.append("Recovery is amber: " + "; ".join(recovery["flags"]))
            if harder:
                reasons.append("Last session ran harder than planned: " + "; ".join(last_workout["notes"]))
            if high_load:
                reasons.append(f"7-day load is high ({load['tss_7d']} TSS).")
        else:
            verdict = "PROCEED"
            headline = f"Proceed with today's {today_type}, monitor how you feel."
            reasons.append("Recovery is amber: " + "; ".join(recovery["flags"]))
    elif rec == "green":
        if intensity in ("easy", "moderate") and load["tss_7d"] < thresholds["tss_ramp_7d_high"] * 0.6 and (
            recovery.get("readiness") or 0
        ) >= thresholds["readiness_high"] and not harder:
            verdict = "PUSH"
            headline = f"Green light — you could extend today's {today_type} a touch."
            reasons.append(
                f"Recovery strong (readiness {recovery.get('readiness')}) and recent load light "
                f"({load['tss_7d']} TSS/7d)."
            )
        else:
            verdict = "PROCEED"
            headline = f"Proceed as planned: {today_type}."
            reasons.append(f"Recovery is green (readiness {recovery.get('readiness')}).")
            if harder:
                reasons.append("Note last session ran hot — hold target power precisely today.")
    else:  # unknown recovery
        verdict = "PROCEED"
        headline = f"Proceed as planned: {today_type} (no recovery data)."
        reasons.append("No Oura data for today — going by the plan. Add Oura for recovery-aware advice.")

    return {"verdict": verdict, "headline": headline, "reasons": reasons}


def build_assessment(
    athlete: dict[str, Any],
    plan: dict[str, Any],
    rides: list[dict[str, Any]],
    oura_days: dict[str, Any],
    today: date,
    history: dict[str, Any] | None = None,
    trend_weeks: int = 8,
) -> dict[str, Any]:
    """Top-level: assemble the full structured assessment for `today`.

    If `history` is provided, also attaches overall fitness (CTL/ATL/TSB) and the
    top progression focus items, tying the daily call to the longitudinal picture.
    """
    thresholds = athlete.get("thresholds", {})
    recovery = assess_recovery(oura_days, today, thresholds, athlete)
    last_workout = assess_last_workout(rides, plan, today, thresholds)
    load = recent_load(rides, today)
    today_plan = plan_mod.workout_for(plan, today)
    upcoming = plan_mod.upcoming(plan, today + timedelta(days=1), days=3)
    verdict = make_verdict(recovery, last_workout, load, today_plan, thresholds)

    from . import fitness as fitness_mod

    fitness_now = fitness_mod.current(rides, today)
    focus: list[dict[str, Any]] = []
    if history is not None:
        from . import trends as trends_mod

        review = trends_mod.build_review(athlete, plan, history, oura_days, today, weeks=trend_weeks)
        rank = {"high": 0, "medium": 1, "low": 2, "info": 3}
        focus = sorted(
            [w for w in review["weaknesses"] if w["severity"] in ("high", "medium")],
            key=lambda w: rank.get(w["severity"], 9),
        )[:2]

    return {
        "date": today.isoformat(),
        "today_plan": today_plan,
        "upcoming": upcoming,
        "recovery": recovery,
        "last_workout": last_workout,
        "load": load,
        "verdict": verdict,
        "fitness": fitness_now,
        "focus": focus,
    }
