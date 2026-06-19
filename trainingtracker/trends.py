"""Longitudinal progression analysis for the 3-workout program (Z2 / Threshold /
VO2max): per-type trends, weakness detection, and concrete plan adaptations.

Reads the persistent workout history and answers: where is the athlete improving,
where is the limiter, and how should the plan change?
"""
from __future__ import annotations

from datetime import date, timedelta
from statistics import mean
from typing import Any, Optional

from . import fitness, history as history_mod, plan as plan_mod

Z2 = {"Endurance", "Recovery"}
THRESHOLD = {"Threshold", "SweetSpot"}   # sweet-spot is threshold-development work
VO2 = {"VO2max", "Anaerobic"}

# Map any workout type (classified or planned) to one of the 3 tracked families.
FAMILY = {
    "Recovery": "Endurance", "Endurance": "Endurance",
    "SweetSpot": "Threshold", "Tempo": "Threshold", "Threshold": "Threshold",
    "VO2max": "VO2max", "Anaerobic": "VO2max",
}


def _vals(records: list[dict[str, Any]], getter) -> list[float]:
    out = []
    for r in records:  # records come in oldest -> newest
        v = getter(r)
        if v is not None:
            out.append(float(v))
    return out


def _trend(values: list[float], higher_is_better: bool, flat_band: float = 0.03) -> dict[str, Any]:
    """Compare the recent half of a metric series to the earlier half."""
    n = len(values)
    if n < 2:
        return {"n": n, "direction": "insufficient data",
                "latest": round(values[-1], 2) if values else None}
    k = max(1, min(3, n // 2))
    recent = mean(values[-k:])
    prior = mean(values[:-k])
    pct = (recent - prior) / abs(prior) if prior else 0.0
    if abs(pct) <= flat_band:
        direction = "flat"
    elif (pct > 0) == higher_is_better:
        direction = "improving"
    else:
        direction = "declining"
    return {"n": n, "recent": round(recent, 1), "prior": round(prior, 1),
            "change_pct": round(pct * 100, 1), "direction": direction,
            "latest": round(values[-1], 1)}


# ---- per-type trends --------------------------------------------------------
def threshold_trend(records: list[dict[str, Any]]) -> dict[str, Any]:
    fade = _vals(records, lambda r: (r.get("intervals") or {}).get("fade_pct"))
    held = _vals(records, lambda r: (r.get("intervals") or {}).get("mean_pct_ftp"))
    ef = _vals(records, lambda r: r.get("efficiency_factor"))
    return {
        "sessions": len(records),
        "power_held_pctftp": _trend(held, higher_is_better=True),    # holding more power
        "durability_fade": _trend(fade, higher_is_better=False),     # less fade = better
        "efficiency": _trend(ef, higher_is_better=True),
        "avg_fade_recent": round(mean(fade[-3:]), 1) if fade else None,
    }


def vo2_trend(records: list[dict[str, Any]]) -> dict[str, Any]:
    fade = _vals(records, lambda r: (r.get("intervals") or {}).get("fade_pct"))
    held = _vals(records, lambda r: (r.get("intervals") or {}).get("mean_pct_ftp"))
    reps = _vals(records, lambda r: (r.get("intervals") or {}).get("count"))
    return {
        "sessions": len(records),
        "power_held_pctftp": _trend(held, higher_is_better=True),
        "repeatability_fade": _trend(fade, higher_is_better=False),
        "reps_completed": _trend(reps, higher_is_better=True),
        "avg_fade_recent": round(mean(fade[-3:]), 1) if fade else None,
    }


def z2_trend(records: list[dict[str, Any]]) -> dict[str, Any]:
    ef = _vals(records, lambda r: r.get("efficiency_factor"))
    decoup = _vals(records, lambda r: r.get("decoupling_pct"))
    return {
        "sessions": len(records),
        "aerobic_efficiency": _trend(ef, higher_is_better=True),   # EF rising = base improving
        "decoupling": _trend(decoup, higher_is_better=False),      # lower = better durability
        "avg_decoupling_recent": round(mean(decoup[-3:]), 1) if decoup else None,
    }


# ---- volume (actual vs planned) --------------------------------------------
def volume(history, plan: dict[str, Any], today: date, weeks: int) -> dict[str, Any]:
    actual = {"Endurance": 0, "Threshold": 0, "VO2max": 0, "Other": 0}
    for r in history_mod.recent(history, today, weeks * 7):
        fam = FAMILY.get(r.get("classified_type"))
        actual[fam if fam else "Other"] += 1

    planned = {"Endurance": 0, "Threshold": 0, "VO2max": 0, "Rest": 0, "Other": 0}
    for i in range(weeks * 7):
        t = plan_mod.workout_for(plan, today - timedelta(days=i)).get("type")
        fam = FAMILY.get(t)
        if fam:
            planned[fam] += 1
        elif t == "Rest":
            planned["Rest"] += 1
        else:
            planned["Other"] += 1
    return {"weeks": weeks, "actual": actual, "planned": planned}


# ---- weakness detection + plan adaptations ---------------------------------
def weaknesses(
    thr: dict[str, Any], vo2: dict[str, Any], z2: dict[str, Any],
    vol: dict[str, Any], thresholds: dict[str, Any]
) -> list[dict[str, Any]]:
    fade_high = thresholds.get("decoupling_high", 6.0)  # reuse as a fade reference too
    out: list[dict[str, Any]] = []

    # Threshold durability
    af = thr.get("avg_fade_recent")
    if af is not None and af >= 4:
        improving = thr["durability_fade"].get("direction") == "improving"
        sev = "high" if af >= 7 and not improving else ("medium" if af >= 4 else "low")
        out.append({
            "area": "Threshold durability",
            "severity": sev,
            "finding": f"Power fades ~{af}% across the last intervals of recent threshold "
                       f"sessions{' (and not improving)' if not improving else ' (improving)'}.",
            "suggestion": "Add a threshold session (or a 4th interval / +2-3 min per rep). "
                          "Trim one easy ride to absorb the load.",
            "plan_change": {"type": "Threshold", "action": "increase"},
        })
    elif thr.get("sessions", 0) >= 3 and thr["power_held_pctftp"].get("direction") == "improving":
        out.append({"area": "Threshold", "severity": "info",
                    "finding": "Threshold power held is trending up — durability improving.",
                    "suggestion": "Hold current threshold dose; progress interval power.",
                    "plan_change": None})

    # VO2 repeatability
    vf = vo2.get("avg_fade_recent")
    if vf is not None and vf >= 6:
        out.append({
            "area": "VO2max repeatability",
            "severity": "high" if vf >= 10 else "medium",
            "finding": f"Power drops ~{vf}% on later VO2 reps — repeatability is the limiter.",
            "suggestion": "Keep total reps but lengthen recoveries (or shorten reps slightly), "
                          "then rebuild duration. Consider a 2nd VO2 block when recovery allows.",
            "plan_change": {"type": "VO2max", "action": "adjust_recovery"},
        })

    # Aerobic base (Z2)
    ad = z2.get("avg_decoupling_recent")
    ef_dir = z2.get("aerobic_efficiency", {}).get("direction")
    if (ad is not None and ad >= 5) or ef_dir == "declining":
        out.append({
            "area": "Aerobic base",
            "severity": "medium",
            "finding": (f"Z2 decoupling ~{ad}% (>5% = drift) " if ad is not None else "")
                       + (f"and efficiency {ef_dir}." if ef_dir else "."),
            "suggestion": "Add Zone-2 volume (a longer ride or +20-30 min midweek). "
                          "Aerobic base underpins both threshold and VO2.",
            "plan_change": {"type": "Endurance", "action": "increase"},
        })
    elif ef_dir == "improving":
        out.append({"area": "Aerobic base", "severity": "info",
                    "finding": "Z2 efficiency (EF) is rising — aerobic base improving.",
                    "suggestion": "Maintain Z2 volume.", "plan_change": None})

    # Volume balance vs plan
    actual, planned = vol["actual"], vol["planned"]
    for t in ("Threshold", "VO2max", "Endurance"):
        if planned.get(t, 0) - actual.get(t, 0) >= 2:
            out.append({
                "area": f"{t} volume",
                "severity": "low",
                "finding": f"Completed {actual.get(t,0)} {t} sessions vs ~{planned.get(t,0)} planned "
                           f"in {vol['weeks']} weeks.",
                "suggestion": f"You're under-doing {t}. Protect those sessions or move them to "
                              f"better-recovered days.",
                "plan_change": None,
            })
    return out


def build_review(
    athlete: dict[str, Any], plan: dict[str, Any], history, oura, today: date, weeks: int = 8
) -> dict[str, Any]:
    thr_recs = history_mod.of_type(history, THRESHOLD, today, weeks)
    vo2_recs = history_mod.of_type(history, VO2, today, weeks)
    z2_recs = history_mod.of_type(history, Z2, today, weeks)
    all_recs = history_mod.records(history)

    thr = threshold_trend(thr_recs)
    vo2 = vo2_trend(vo2_recs)
    z2 = z2_trend(z2_recs)
    vol = volume(history, plan, today, weeks)
    weak = weaknesses(thr, vo2, z2, vol, athlete.get("thresholds", {}))

    return {
        "date": today.isoformat(),
        "window_weeks": weeks,
        "fitness": fitness.current(all_recs, today),
        "trends": {"threshold": thr, "vo2max": vo2, "z2": z2},
        "volume": vol,
        "weaknesses": weak,
    }
