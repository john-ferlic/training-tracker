"""Tests for the longitudinal/progression layer: interval detection + fade,
workout classification, the PMC fitness model, and weakness detection.

Run:  python -m pytest tests/   (or)   python tests/test_progression.py
"""
from __future__ import annotations

import os
import sys
from datetime import date, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from trainingtracker import fitness, profile, trends, workout  # noqa: E402

FTP = 250
DEFAULT_CUTOFF_W = round(workout.DEFAULTS["work_frac_ftp"] * FTP)


# ----- interval detection + fade --------------------------------------------
def test_detect_three_intervals():
    watts = ([240] * 600 + [120] * 300) * 3
    bounds = workout.detect_intervals(watts, FTP)
    assert len(bounds) == 3


def test_no_intervals_in_zone2():
    watts = [170] * 3000  # steady Z2, nothing above 0.88 FTP
    assert workout.detect_intervals(watts, FTP) == []


def test_interval_fade_detected():
    watts = [250] * 600 + [120] * 300 + [238] * 600 + [120] * 300 + [224] * 600
    hr = [150] * len(watts)
    ia = workout.interval_analysis(watts, hr, FTP)
    assert ia is not None and ia["count"] == 3
    assert ia["fade_pct"] is not None and ia["fade_pct"] > 5   # power dropped on later reps
    assert ia["first_to_last_pct"] > 5


def test_interval_no_fade_when_steady():
    watts = ([240] * 600 + [120] * 300) * 3
    ia = workout.interval_analysis(watts, [150] * len(watts), FTP)
    assert ia is not None and abs(ia["fade_pct"]) < 2


# ----- sub-threshold work (tempo blocks below the %FTP cutoff) ---------------
# Regression: a prescribed 3x12 tempo block at 0.76-0.90 FTP sits BELOW the
# 0.88 FTP work cutoff, so it registered as zero intervals and read as a
# skipped session. Real rides on 2026-08-08/08-15 hit exactly this.
def _long_ride_with_tempo(base=170, tempo=205, reps=3, rep_s=720, gap_s=600):
    watts = [base] * 900
    for _ in range(reps):
        watts += [tempo] * rep_s + [base] * gap_s
    return watts + [base] * 900


def test_sub_threshold_tempo_blocks_are_detected():
    watts = _long_ride_with_tempo()          # tempo 205 = 0.82 FTP, under the 0.88 cutoff
    ia = workout.interval_analysis(watts, [140] * len(watts), FTP)
    assert ia is not None, "tempo blocks below 0.88 FTP must not read as a skipped session"
    assert ia["count"] == 3
    assert all(700 <= iv["duration_s"] <= 740 for iv in ia["intervals"])
    assert ia["detection"]["basis"] == "adaptive"
    assert ia["detection"]["threshold_w"] < DEFAULT_CUTOFF_W


def test_steady_zone2_stays_empty_under_adaptive_detection():
    # The adaptive fallback must not invent structure in a genuinely flat ride.
    assert workout.interval_analysis([170] * 3000, [130] * 3000, FTP) is None


def test_noisy_zone2_does_not_invent_intervals():
    # Real trainer data wobbles; wobble is not structure.
    watts = [170 + (i % 7) - 3 for i in range(4000)]
    ia = workout.interval_analysis(watts, [130] * 4000, FTP)
    assert ia is None or ia["count"] == 0


def test_above_threshold_work_still_uses_the_ftp_cutoff():
    # When real above-cutoff work exists, detection must be unchanged.
    watts = ([240] * 600 + [120] * 300) * 3
    ia = workout.interval_analysis(watts, [150] * len(watts), FTP)
    assert ia is not None and ia["count"] == 3
    assert ia["detection"]["basis"] == "ftp"
    assert ia["detection"]["threshold_w"] == DEFAULT_CUTOFF_W


# ----- over/under sub-structure ---------------------------------------------
# Regression: in an over-under BOTH halves clear the work cutoff, so a correct
# set fuses into one block at the blended average and the reps vanish. The real
# 2026-08-13 session logged one 19:55 block at 295W instead of 4x(3min/2min).
def _over_under_set(under=225, over=260, unders_s=180, overs_s=120, reps=4):
    watts: list[int] = []
    for _ in range(reps):
        watts += [under] * unders_s + [over] * overs_s
    return watts


def test_over_under_block_is_decomposed():
    watts = [120] * 300 + _over_under_set() + [120] * 300
    ia = workout.interval_analysis(watts, [160] * len(watts), FTP)
    assert ia is not None and ia["count"] == 1, "the set should fuse into one work block"
    segs = ia["intervals"][0].get("segments")
    assert segs is not None, "the block must be re-split into over/under reps"
    assert len(segs) == 8
    assert [s["label"] for s in segs] == ["under", "over"] * 4
    assert ia["structure"] == "over_under"
    assert ia["over_under"]["over_count"] == 4
    assert ia["over_under"]["under_count"] == 4
    assert abs(ia["over_under"]["fade_pct_overs"]) < 2


def test_over_under_reports_fade_across_overs():
    # Overs decay 260 -> 250 -> 240 -> 230 while the unders hold: the blended
    # block average hides this, fade_pct_overs must not.
    watts = [120] * 300
    for over in (260, 250, 240, 230):
        watts += [225] * 180 + [over] * 120
    ia = workout.interval_analysis(watts, [160] * len(watts), FTP)
    assert ia is not None and ia["structure"] == "over_under"
    assert ia["over_under"]["fade_pct_overs"] > 5


def test_steady_threshold_block_is_not_split():
    # A single sustained 20 min effort has no over/under structure to find.
    watts = [120] * 300 + [240] * 1200 + [120] * 300
    ia = workout.interval_analysis(watts, [165] * len(watts), FTP)
    assert ia is not None and ia["count"] == 1
    assert "segments" not in ia["intervals"][0]
    assert ia["structure"] == "steady"


# ----- classification --------------------------------------------------------
def test_classify_vo2():
    tiz = {"Z5 VO2max": 0.20, "Z2 Endurance": 0.5, "Z1 Recovery": 0.3}
    assert workout.classify_workout({"intensity_factor": 0.95}, tiz) == "VO2max"


def test_classify_threshold():
    tiz = {"Z4 Threshold": 0.5, "Z2 Endurance": 0.4, "Z1 Recovery": 0.1}
    assert workout.classify_workout({"intensity_factor": 0.88}, tiz) == "Threshold"


def test_classify_endurance_and_recovery():
    z2 = {"Z2 Endurance": 0.9, "Z1 Recovery": 0.05}
    assert workout.classify_workout({"intensity_factor": 0.68}, z2) == "Endurance"
    assert workout.classify_workout({"intensity_factor": 0.5}, z2) == "Recovery"


def test_classify_sweetspot_vs_tempo_touch():
    sst = {"Z3 Tempo": 0.40, "Z2 Endurance": 0.5, "Z1 Recovery": 0.1}
    assert workout.classify_workout({"intensity_factor": 0.82}, sst) == "SweetSpot"
    # a mostly-Z2 ride with a short tempo block stays Endurance
    light = {"Z3 Tempo": 0.20, "Z2 Endurance": 0.7, "Z1 Recovery": 0.1}
    assert workout.classify_workout({"intensity_factor": 0.70}, light) == "Endurance"


def test_analyze_workout_end_to_end():
    activity = {"id": 7, "name": "3x12 Threshold", "type": "Ride",
                "start_date_local": "2026-06-15T07:00:00Z", "moving_time": 4320,
                "average_watts": 210, "average_heartrate": 152}
    watts = ([240] * 720 + [120] * 360) * 3
    rec = workout.analyze_workout(activity, {"watts": watts, "heartrate": [150] * len(watts)}, FTP)
    assert rec["classified_type"] == "Threshold"
    assert rec["intervals"]["count"] == 3


# ----- fitness (PMC) ---------------------------------------------------------
def _steady_records(today, weeks=8, tss=80):
    recs = []
    rid = 0
    for w in range(weeks):
        for dow in (0, 2, 4, 5):  # Mon/Wed/Fri/Sat
            d = today - timedelta(days=(weeks - w) * 7 - dow)
            rid += 1
            recs.append({"id": rid, "date": d.isoformat(), "tss": tss})
    return recs


def test_pmc_steady_state():
    today = date(2026, 6, 18)
    recs = _steady_records(today)
    cur = fitness.current(recs, today)
    assert cur is not None
    assert cur["ctl"] > 20                # accumulated real fitness
    assert abs(cur["tsb"]) < 12           # steady load => form near balance
    assert cur["form_state"] in ("neutral", "fresh", "productive overload")


# ----- trends + weaknesses ---------------------------------------------------
def _thr_records(fades, helds):
    base = date(2026, 5, 1)
    recs = []
    for i, (f, h) in enumerate(zip(fades, helds)):
        recs.append({
            "id": 100 + i, "date": (base + timedelta(days=i * 4)).isoformat(),
            "classified_type": "Threshold", "tss": 90, "efficiency_factor": 1.8 + i * 0.02,
            "intervals": {"count": 3, "fade_pct": f, "mean_pct_ftp": h},
        })
    return recs


def test_threshold_trend_improving():
    recs = _thr_records([8, 7, 5, 3, 2], [95, 96, 97, 99, 100])
    t = trends.threshold_trend(recs)
    assert t["power_held_pctftp"]["direction"] == "improving"
    assert t["durability_fade"]["direction"] == "improving"  # fade shrinking


def test_weakness_flags_threshold_durability():
    recs = _thr_records([7, 8, 7, 9, 8], [96, 96, 95, 96, 95])  # persistent high fade
    thr = trends.threshold_trend(recs)
    vo2 = trends.vo2_trend([])
    z2 = trends.z2_trend([])
    vol = {"weeks": 8, "actual": {"Threshold": 5, "VO2max": 3, "Endurance": 8},
           "planned": {"Threshold": 5, "VO2max": 3, "Endurance": 8}}
    weak = trends.weaknesses(thr, vo2, z2, vol, {"decoupling_high": 6.0})
    durability = [w for w in weak if w["area"] == "Threshold durability"]
    assert durability, "expected a threshold durability weakness"
    assert durability[0]["plan_change"]["type"] == "Threshold"
    assert durability[0]["plan_change"]["action"] == "increase"


def test_build_review_smoke():
    today = date(2026, 6, 18)
    recs = _thr_records([7, 8, 8], [96, 95, 96])
    hist = {str(r["id"]): r for r in recs}
    plan = {"week_template": {"thursday": {"type": "Threshold"}}}
    review = trends.build_review({"thresholds": {"decoupling_high": 6.0}}, plan, hist, {}, today, weeks=8)
    for key in ("fitness", "trends", "volume", "weaknesses"):
        assert key in review


# ----- profile / stat sync -------------------------------------------------
def test_suggest_profile_updates_flags_real_changes():
    athlete = {"ftp": 317, "weight_kg": 79, "resting_hr": 48, "max_hr": 197}
    strava = {"ftp": 325, "weight": 78.5}  # FTP up 8, weight 0.5kg (below threshold)
    oura = {"2026-06-10": {"resting_hr": 44}, "2026-06-11": {"resting_hr": 43},
            "2026-06-12": {"resting_hr": 44}}
    rides = [{"max_hr": 199}, {"max_hr": 192}]
    ch = {c["field"]: c for c in profile.suggest_profile_updates(athlete, strava, oura, rides)}
    assert ch["ftp"]["suggested"] == 325
    assert ch["resting_hr"]["suggested"] == 44       # median 44 vs 48 (>=3)
    assert ch["max_hr"]["suggested"] == 199          # peak 199 >= 197+2
    assert "weight_kg" not in ch                     # 0.5kg delta is below threshold


def test_suggest_profile_updates_no_change_and_no_lowering():
    athlete = {"ftp": 317, "weight_kg": 79, "resting_hr": 44, "max_hr": 197}
    strava = {"ftp": 317, "weight": 79.0}
    oura = {"2026-06-10": {"resting_hr": 44}}
    rides = [{"max_hr": 198}, {"max_hr": 150}]  # peak 198 = +1, below +2 bump; never lowers
    assert profile.suggest_profile_updates(athlete, strava, oura, rides) == []


def _run_all():
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in fns:
        fn()
        print(f"  PASS {fn.__name__}")
    print(f"\n{len(fns)}/{len(fns)} tests passed.")


if __name__ == "__main__":
    _run_all()
