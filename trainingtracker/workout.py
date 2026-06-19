"""Deep single-workout analysis: classify the session (Z2 / Threshold / VO2max),
break it into work intervals, and measure power *fade* across those intervals —
the "struggled on the last few intervals" signal.

Built for a focused 3-workout-type program: Endurance (Zone 2), Threshold, VO2max.
"""
from __future__ import annotations

from typing import Any, Optional

from . import metrics

# Defaults; can be overridden from athlete.yaml -> analysis.interval_detection.
DEFAULTS = {
    "work_frac_ftp": 0.88,   # smoothed power above this %FTP counts as "work"
    "min_interval_s": 60,    # ignore surges shorter than this
    "gap_merge_s": 25,       # bridge brief dips within one interval
    "smooth_s": 10,          # rolling-average window for detection
}


def time_in_power_zones(watts: list[float], ftp: float) -> dict[str, float]:
    """Fraction of samples in each Coggan power zone."""
    zones = metrics.power_zones(ftp)
    counts = {name: 0 for name in zones}
    total = 0
    for w in watts:
        if w is None:
            continue
        total += 1
        for name, (lo, hi) in zones.items():
            if w >= (lo or 0) and (hi is None or w < hi):
                counts[name] += 1
                break
    return {name: round(c / total, 3) for name, c in counts.items()} if total else {}


def classify_workout(summary: dict[str, Any], tiz: dict[str, float]) -> str:
    """Classify the actual session from its intensity distribution.
    One of: VO2max, Threshold, SweetSpot, Endurance, Recovery, Mixed."""
    if_ = summary.get("intensity_factor")
    z5plus = (tiz.get("Z5 VO2max", 0) + tiz.get("Z6 Anaerobic", 0)
              + tiz.get("Z7 Neuromuscular", 0))
    z4 = tiz.get("Z4 Threshold", 0)
    z3 = tiz.get("Z3 Tempo", 0)
    z_easy = tiz.get("Z1 Recovery", 0) + tiz.get("Z2 Endurance", 0)

    if z5plus >= 0.06:
        return "VO2max"
    if z4 >= 0.12:
        return "Threshold"
    # Sweet-spot / sustained tempo (e.g. SST 2x15 @ ~90% FTP) — threshold-family work.
    if z3 >= 0.25 and (if_ is None or if_ >= 0.78):
        return "SweetSpot"
    if if_ is not None and if_ < 0.60:
        return "Recovery"
    if z_easy >= 0.6 and (if_ is None or if_ < 0.80):
        return "Endurance"
    return "Mixed"


def detect_intervals(watts: list[float], ftp: float, params: dict | None = None) -> list[tuple[int, int]]:
    """Return [(start_idx, end_idx)] work intervals. Assumes ~1 Hz samples."""
    p = {**DEFAULTS, **(params or {})}
    if not watts:
        return []
    sm = metrics.rolling_average(watts, p["smooth_s"])
    thr = p["work_frac_ftp"] * ftp
    n = len(sm)

    raw: list[list[int]] = []
    i = 0
    while i < n:
        if sm[i] >= thr:
            j = i
            while j < n and sm[j] >= thr:
                j += 1
            raw.append([i, j])
            i = j
        else:
            i += 1

    merged: list[list[int]] = []
    for seg in raw:
        if merged and seg[0] - merged[-1][1] <= p["gap_merge_s"]:
            merged[-1][1] = seg[1]
        else:
            merged.append(seg)

    return [(s, e) for s, e in merged if (e - s) >= p["min_interval_s"]]


def _mean(xs: list[float]) -> Optional[float]:
    xs = [x for x in xs if x is not None]
    return sum(xs) / len(xs) if xs else None


def interval_analysis(
    watts: list[float], hr: list[float], ftp: float, params: dict | None = None
) -> Optional[dict[str, Any]]:
    """Per-interval power/HR plus fade across the session."""
    bounds = detect_intervals(watts, ftp, params)
    if len(bounds) < 1:
        return None

    intervals = []
    for k, (s, e) in enumerate(bounds, 1):
        seg_w = watts[s:e]
        seg_hr = hr[s:e] if hr else []
        ap = _mean(seg_w)
        intervals.append({
            "n": k,
            "duration_s": e - s,
            "avg_power": round(ap) if ap else None,
            "pct_ftp": round(ap / ftp * 100) if ap else None,
            "avg_hr": round(_mean(seg_hr)) if seg_hr else None,
        })

    powers = [iv["avg_power"] for iv in intervals if iv["avg_power"]]
    fade_pct = first_last_pct = None
    if len(powers) >= 2:
        first_last_pct = round((powers[0] - powers[-1]) / powers[0] * 100, 1)
        half = max(1, len(powers) // 2)
        first_mean = _mean(powers[:half])
        last_mean = _mean(powers[-half:])
        if first_mean:
            fade_pct = round((first_mean - last_mean) / first_mean * 100, 1)

    return {
        "count": len(intervals),
        "intervals": intervals,
        # positive fade = power dropped on later intervals (faded / struggled)
        "fade_pct": fade_pct,
        "first_to_last_pct": first_last_pct,
        "mean_pct_ftp": round(_mean([iv["pct_ftp"] for iv in intervals]) or 0),
    }


def analyze_workout(
    activity: dict[str, Any], streams: dict[str, list] | None, ftp: float,
    params: dict | None = None
) -> dict[str, Any]:
    """Full enriched record for one ride: whole-ride metrics + zone distribution
    + classification + interval/fade analysis. This is what we persist to history."""
    record = metrics.summarize_ride(activity, streams, ftp)
    streams = streams or {}
    watts = streams.get("watts") or []
    hr = streams.get("heartrate") or []

    tiz = time_in_power_zones(watts, ftp) if watts else {}
    record["time_in_zones"] = tiz
    record["classified_type"] = classify_workout(record, tiz) if tiz else None
    record["intervals"] = interval_analysis(watts, hr, ftp, params) if watts else None
    return record
