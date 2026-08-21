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

    # --- Adaptive fallback -----------------------------------------------
    # A fixed %FTP cutoff can only see work ABOVE it. Prescribed tempo
    # (0.76-0.90 FTP) sits below 0.88 FTP, so a perfectly executed 3x12 tempo
    # block registered as no intervals at all and looked like a skipped
    # session. When nothing sustained clears the FTP cutoff, fall back to
    # splitting the ride's own power distribution and look for structure there.
    "adaptive_floor_frac_ftp": 0.60,   # ignore coasting/recovery when splitting
    "adaptive_min_separation": 1.15,   # work mode must be >=15% above the easy mode
    "adaptive_max_work_frac": 0.80,    # reject a split that calls most of the ride "work"
    "min_work_frac": 0.02,             # a tier finding <2% of the ride found nothing

    # --- Over/under sub-structure ----------------------------------------
    # In an over-under BOTH halves clear the work cutoff (e.g. under 280W /
    # over 320W against FTP 305 => cutoff 268W), so a correct set fuses into
    # one continuous block at the blended average and the rep structure is
    # lost. Re-split each block internally to recover it.
    "segment_min_s": 45,               # shortest credible over/under sub-segment
    "segment_min_separation": 1.08,    # overs must sit >=8% above unders
    "segment_min_count": 3,            # need >=3 alternations to call it over-under
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


def _segments_above(sm: list[float], thr: float, p: dict) -> list[tuple[int, int]]:
    """Merged, length-filtered runs of smoothed power at or above `thr`."""
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


def _otsu_threshold(values: list[float], bins: int = 64) -> Optional[float]:
    """Otsu's method: the cut that maximizes between-class variance.

    Used to find the natural work/recovery split in a ride's own power
    distribution when a fixed %FTP cutoff can't see the work. Returns None
    when the data is degenerate (flat, or too few samples to split).
    """
    vals = [float(v) for v in values if v is not None]
    if len(vals) < bins:
        return None
    lo, hi = min(vals), max(vals)
    if hi - lo < 1e-6:
        return None

    width = (hi - lo) / bins
    hist = [0] * bins
    for v in vals:
        idx = min(bins - 1, int((v - lo) / width))
        hist[idx] += 1

    total = len(vals)
    total_sum = sum((lo + (i + 0.5) * width) * hist[i] for i in range(bins))
    best_var, best_thr = -1.0, None
    w_bg = 0
    sum_bg = 0.0
    for i in range(bins):
        w_bg += hist[i]
        if w_bg == 0:
            continue
        w_fg = total - w_bg
        if w_fg == 0:
            break
        sum_bg += (lo + (i + 0.5) * width) * hist[i]
        mean_bg = sum_bg / w_bg
        mean_fg = (total_sum - sum_bg) / w_fg
        between = w_bg * w_fg * (mean_bg - mean_fg) ** 2
        if between > best_var:
            best_var, best_thr = between, lo + (i + 1) * width
    return best_thr


def _split_quality(sm: list[float], thr: float, p: dict) -> Optional[tuple[float, float]]:
    """(lower_mean, upper_mean) for a candidate split, or None if degenerate."""
    lower = [v for v in sm if v < thr]
    upper = [v for v in sm if v >= thr]
    if not lower or not upper:
        return None
    return sum(lower) / len(lower), sum(upper) / len(upper)


def choose_work_threshold(sm: list[float], ftp: float, p: dict) -> tuple[float, str]:
    """Pick the power level separating work from recovery in THIS ride.

    Prefers the calibrated %FTP cutoff — it is the coach-facing definition and
    is what threshold/VO2 sessions should be judged against. Only when nothing
    sustained clears it does this fall back to an adaptive split, so rides with
    real above-threshold work are detected exactly as before.
    """
    abs_thr = p["work_frac_ftp"] * ftp
    n = len(sm)
    covered = sum(e - s for s, e in _segments_above(sm, abs_thr, p))
    if covered >= p["min_work_frac"] * n:
        return abs_thr, "ftp"

    # Nothing above threshold — look for sub-threshold structure (tempo, SST).
    candidates = [v for v in sm if v >= p["adaptive_floor_frac_ftp"] * ftp]
    thr = _otsu_threshold(candidates)
    if thr is None or thr >= abs_thr:
        return abs_thr, "ftp"

    quality = _split_quality(candidates, thr, p)
    if quality is None or quality[1] < quality[0] * p["adaptive_min_separation"]:
        return abs_thr, "ftp"

    covered = sum(e - s for s, e in _segments_above(sm, thr, p))
    if not (p["min_work_frac"] * n <= covered <= p["adaptive_max_work_frac"] * n):
        return abs_thr, "ftp"
    return thr, "adaptive"


def detect_intervals(watts: list[float], ftp: float, params: dict | None = None) -> list[tuple[int, int]]:
    """Return [(start_idx, end_idx)] work intervals. Assumes ~1 Hz samples."""
    p = {**DEFAULTS, **(params or {})}
    if not watts:
        return []
    sm = metrics.rolling_average(watts, p["smooth_s"])
    thr, _basis = choose_work_threshold(sm, ftp, p)
    return _segments_above(sm, thr, p)


def _alternating_segments(block: list[float], p: dict) -> Optional[list[tuple[int, int, str]]]:
    """Recover over/under structure inside one continuous work block.

    Returns [(start, end, "over"|"under")] when the block clearly alternates
    between two sustained power levels, else None for a steady block.
    """
    thr = _otsu_threshold(block)
    if thr is None:
        return None
    quality = _split_quality(block, thr, p)
    if quality is None or quality[1] < quality[0] * p["segment_min_separation"]:
        return None

    runs: list[list[Any]] = []
    for i, v in enumerate(block):
        label = "over" if v >= thr else "under"
        if runs and runs[-1][2] == label:
            runs[-1][1] = i + 1
        else:
            runs.append([i, i + 1, label])

    # Absorb sub-threshold flickers (ramp transitions) into the longer neighbour.
    changed = True
    while changed and len(runs) > 1:
        changed = False
        for i, run in enumerate(runs):
            if run[1] - run[0] >= p["segment_min_s"]:
                continue
            prev_len = runs[i - 1][1] - runs[i - 1][0] if i > 0 else -1
            next_len = runs[i + 1][1] - runs[i + 1][0] if i + 1 < len(runs) else -1
            target = i - 1 if prev_len >= next_len else i + 1
            runs[target][0] = min(runs[target][0], run[0])
            runs[target][1] = max(runs[target][1], run[1])
            runs.pop(i)
            changed = True
            break

    # Coalesce neighbours that ended up sharing a label.
    coalesced: list[list[Any]] = []
    for run in runs:
        if coalesced and coalesced[-1][2] == run[2]:
            coalesced[-1][1] = run[1]
        else:
            coalesced.append(run)

    if len(coalesced) < p["segment_min_count"]:
        return None
    if not all((r[1] - r[0]) >= p["segment_min_s"] for r in coalesced):
        return None
    return [(r[0], r[1], r[2]) for r in coalesced]


def _mean(xs: list[float]) -> Optional[float]:
    xs = [x for x in xs if x is not None]
    return sum(xs) / len(xs) if xs else None


def _fade(powers: list[float]) -> tuple[Optional[float], Optional[float]]:
    """(fade_pct, first_to_last_pct). Positive = power dropped on later reps."""
    if len(powers) < 2:
        return None, None
    first_last = round((powers[0] - powers[-1]) / powers[0] * 100, 1)
    half = max(1, len(powers) // 2)
    first_mean = _mean(powers[:half])
    last_mean = _mean(powers[-half:])
    fade = None
    if first_mean:
        fade = round((first_mean - last_mean) / first_mean * 100, 1)
    return fade, first_last


def interval_analysis(
    watts: list[float], hr: list[float], ftp: float, params: dict | None = None
) -> Optional[dict[str, Any]]:
    """Per-interval power/HR plus fade across the session."""
    p = {**DEFAULTS, **(params or {})}
    if not watts:
        return None
    sm = metrics.rolling_average(watts, p["smooth_s"])
    thr, basis = choose_work_threshold(sm, ftp, p)
    bounds = _segments_above(sm, thr, p)
    if len(bounds) < 1:
        return None

    intervals = []
    for k, (s, e) in enumerate(bounds, 1):
        seg_w = watts[s:e]
        seg_hr = hr[s:e] if hr else []
        ap = _mean(seg_w)
        entry: dict[str, Any] = {
            "n": k,
            "duration_s": e - s,
            "avg_power": round(ap) if ap else None,
            "pct_ftp": round(ap / ftp * 100) if ap else None,
            "avg_hr": round(_mean(seg_hr)) if seg_hr else None,
        }
        parts = _alternating_segments(sm[s:e], p)
        if parts:
            entry["segments"] = [
                {
                    "n": i,
                    "label": label,
                    "duration_s": b - a,
                    "avg_power": round(_mean(seg_w[a:b]) or 0) or None,
                    "pct_ftp": round((_mean(seg_w[a:b]) or 0) / ftp * 100) or None,
                    "avg_hr": round(_mean(seg_hr[a:b]) or 0) or None if seg_hr else None,
                }
                for i, (a, b, label) in enumerate(parts, 1)
            ]
        intervals.append(entry)

    powers = [iv["avg_power"] for iv in intervals if iv["avg_power"]]
    fade_pct, first_last_pct = _fade(powers)

    result: dict[str, Any] = {
        "count": len(intervals),
        "intervals": intervals,
        # positive fade = power dropped on later intervals (faded / struggled)
        "fade_pct": fade_pct,
        "first_to_last_pct": first_last_pct,
        "mean_pct_ftp": round(_mean([iv["pct_ftp"] for iv in intervals]) or 0),
        # How the work cutoff was chosen, so a low/absent count can be read
        # correctly instead of as a skipped session.
        "detection": {
            "basis": basis,          # "ftp" = calibrated cutoff, "adaptive" = ride's own split
            "threshold_w": round(thr),
            "threshold_pct_ftp": round(thr / ftp * 100),
        },
    }

    # Over-unders: fade across the *overs* is the meaningful progression signal;
    # whole-block averages blend the unders back in and mask it.
    overs = [
        seg["avg_power"]
        for iv in intervals
        for seg in iv.get("segments", [])
        if seg["label"] == "over" and seg["avg_power"]
    ]
    if overs:
        over_fade, over_first_last = _fade(overs)
        unders = [
            seg["avg_power"]
            for iv in intervals
            for seg in iv.get("segments", [])
            if seg["label"] == "under" and seg["avg_power"]
        ]
        result["structure"] = "over_under"
        result["over_under"] = {
            "over_count": len(overs),
            "under_count": len(unders),
            "over_avg_power": round(_mean(overs) or 0),
            "under_avg_power": round(_mean(unders) or 0) if unders else None,
            "fade_pct_overs": over_fade,
            "first_to_last_pct_overs": over_first_last,
        }
    else:
        result["structure"] = "steady"

    return result


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
