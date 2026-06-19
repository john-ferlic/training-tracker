"""Unit tests for the deterministic core: metrics, plan resolution, recovery
scoring, and the verdict engine. No API credentials required.

Run:  python -m pytest tests/        (or)   python tests/test_metrics.py
"""
from __future__ import annotations

import os
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from trainingtracker import analysis, metrics, plan as plan_mod  # noqa: E402

FTP = 250
THRESHOLDS = {
    "readiness_low": 70, "readiness_high": 85, "sleep_low": 70,
    "resting_hr_elevated": 5, "hrv_drop_pct": 12, "decoupling_high": 6.0,
    "tss_ramp_7d_high": 450, "if_overshoot": 0.08,
}
ATHLETE = {"ftp": FTP, "resting_hr": 48, "thresholds": THRESHOLDS}


def approx(a, b, tol=1e-6):
    return abs(a - b) <= tol


# ----- metrics ---------------------------------------------------------------
def test_normalized_power_constant():
    assert approx(metrics.normalized_power([200] * 3600), 200.0, tol=0.5)


def test_if_and_tss_full_hour_at_ftp():
    np_ = float(FTP)
    assert approx(metrics.intensity_factor(np_, FTP), 1.0)
    # One hour at NP == FTP is 100 TSS by definition.
    assert approx(metrics.training_stress_score(3600, np_, FTP), 100.0, tol=0.01)


def test_decoupling_positive_when_hr_drifts_up():
    watts = [200] * 1200
    hr = [120] * 600 + [140] * 600  # HR climbs in the back half at same power
    d = metrics.decoupling(watts, hr)
    assert d is not None and d > 10  # ~14%


def test_decoupling_near_zero_when_steady():
    d = metrics.decoupling([200] * 1200, [130] * 1200)
    assert d is not None and abs(d) < 1


def test_decoupling_needs_enough_data():
    assert metrics.decoupling([200] * 100, [130] * 100) is None


def test_summarize_ride_from_streams():
    activity = {
        "id": 1, "name": "Threshold", "type": "Ride",
        "start_date_local": "2026-06-17T08:00:00Z",
        "moving_time": 3600, "distance": 30000, "average_heartrate": 150,
        "max_heartrate": 165, "average_watts": 230, "max_watts": 400,
        "device_watts": True,
    }
    streams = {"watts": [240] * 3600, "heartrate": [150] * 1800 + [160] * 1800}
    s = metrics.summarize_ride(activity, streams, FTP)
    assert s["normalized_power"] == 240
    assert approx(s["intensity_factor"], 0.96, tol=0.01)
    assert s["tss"] is not None and 90 <= s["tss"] <= 95
    assert s["decoupling_pct"] is not None and s["decoupling_pct"] > 5
    assert s["is_zwift"] is False


def test_summarize_ride_marks_zwift():
    activity = {"id": 2, "type": "VirtualRide", "moving_time": 1800,
                "start_date_local": "2026-06-17T18:00:00Z", "average_watts": 180}
    s = metrics.summarize_ride(activity, None, FTP)
    assert s["is_zwift"] is True
    assert s["tss"] is not None  # falls back to average_watts


# ----- plan resolution -------------------------------------------------------
def test_plan_template_lookup():
    plan = {"week_template": {"thursday": {"type": "Threshold", "target_if": 0.88}}}
    w = plan_mod.workout_for(plan, date(2026, 6, 18))  # a Thursday
    assert w["type"] == "Threshold" and w["source"] == "template"


def test_plan_schedule_override_wins():
    plan = {
        "week_template": {"thursday": {"type": "Threshold"}},
        "schedule": {date(2026, 6, 18): {"type": "Race"}},
    }
    w = plan_mod.workout_for(plan, date(2026, 6, 18))
    assert w["type"] == "Race" and w["source"] == "schedule"


def test_plan_phase_resolution():
    plan = {
        "meta": {"start_date": "2026-06-15"},
        "phases": [
            {"name": "P1", "weeks": [1, 6], "week_template": {"tuesday": {"type": "Endurance"}}},
            {"name": "P2", "weeks": [7, 12], "week_template": {"tuesday": {"type": "Threshold"}}},
        ],
    }
    w1 = plan_mod.workout_for(plan, date(2026, 6, 16))   # week 1 Tuesday
    assert w1["type"] == "Endurance" and w1["phase"] == "P1" and w1["week"] == 1
    w7 = plan_mod.workout_for(plan, date(2026, 7, 28))   # week 7 Tuesday
    assert w7["type"] == "Threshold" and w7["phase"] == "P2" and w7["week"] == 7


# ----- recovery scoring ------------------------------------------------------
def _oura(today, readiness, sleep, rhr, hrv):
    days = {}
    # a week of baseline history
    for i in range(1, 8):
        d = (date.fromisoformat(today)).toordinal() - i
        ds = date.fromordinal(d).isoformat()
        days[ds] = {"resting_hr": 48, "average_hrv": 64, "readiness": 80, "sleep_score": 80}
    days[today] = {"readiness": readiness, "sleep_score": sleep,
                   "resting_hr": rhr, "average_hrv": hrv}
    return days


def test_recovery_green():
    r = analysis.assess_recovery(_oura("2026-06-18", 88, 85, 47, 66),
                                 date(2026, 6, 18), THRESHOLDS, ATHLETE)
    assert r["status"] == "green" and r["flags"] == []


def test_recovery_red_low_readiness():
    r = analysis.assess_recovery(_oura("2026-06-18", 55, 80, 48, 64),
                                 date(2026, 6, 18), THRESHOLDS, ATHLETE)
    assert r["status"] == "red"


def test_recovery_amber_single_flag():
    r = analysis.assess_recovery(_oura("2026-06-18", 66, 80, 48, 64),
                                 date(2026, 6, 18), THRESHOLDS, ATHLETE)
    assert r["status"] == "amber" and len(r["flags"]) == 1


# ----- verdict engine --------------------------------------------------------
def test_verdict_rest_day_stays_rest():
    v = analysis.make_verdict({"status": "green", "flags": [], "readiness": 90},
                              None, {"tss_7d": 100, "tss_3d": 0, "rides_7d": 0},
                              {"type": "Rest"}, THRESHOLDS)
    assert v["verdict"] == "REST"


def test_verdict_red_recovery_modifies_hard_day():
    rec = {"status": "red", "flags": ["readiness 55"], "readiness": 55}
    v = analysis.make_verdict(rec, None, {"tss_7d": 300, "tss_3d": 0, "rides_7d": 3},
                              {"type": "VO2max"}, THRESHOLDS)
    assert v["verdict"] == "MODIFY"


def test_verdict_green_low_load_can_push():
    rec = {"status": "green", "flags": [], "readiness": 90}
    load = {"tss_7d": 120, "tss_3d": 0, "rides_7d": 2}  # < 0.6*450
    v = analysis.make_verdict(rec, None, load, {"type": "Endurance"}, THRESHOLDS)
    assert v["verdict"] == "PUSH"


def test_build_assessment_end_to_end():
    plan = {"week_template": {"thursday": {"type": "Threshold", "target_if": 0.88,
                                           "target_tss": 90, "duration_min": 75}}}
    rides = [{
        "id": 9, "name": "Wed threshold", "date": "2026-06-17", "type": "Ride",
        "is_zwift": False, "moving_time_min": 75, "tss": 95, "intensity_factor": 0.98,
        "normalized_power": 245, "avg_hr": 158, "decoupling_pct": 9.0,
    }]
    oura = _oura("2026-06-18", 58, 70, 53, 56)  # poor recovery
    a = analysis.build_assessment(ATHLETE, plan, rides, oura, date(2026, 6, 18))
    assert a["today_plan"]["type"] == "Threshold"
    assert a["recovery"]["status"] == "red"
    assert a["last_workout"]["harder_than_expected"] is True
    assert a["verdict"]["verdict"] in ("MODIFY", "REST")
    assert a["load"]["tss_7d"] == 95


def _run_all():
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    passed = 0
    for fn in fns:
        fn()
        passed += 1
        print(f"  PASS {fn.__name__}")
    print(f"\n{passed}/{len(fns)} tests passed.")


if __name__ == "__main__":
    _run_all()
