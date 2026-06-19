"""Cycling metrics: Normalized Power, Intensity Factor, TSS, Efficiency Factor,
and aerobic (Pw:Hr) decoupling.

These are deterministic and fully unit-testable without any API credentials.
"""
from __future__ import annotations

from typing import Any, Optional

Number = float


def rolling_average(values: list[Number], window: int) -> list[float]:
    """Trailing moving average. None values are treated as 0 (coasting)."""
    if window <= 1:
        return [float(v or 0) for v in values]
    out: list[float] = []
    running = 0.0
    from collections import deque

    q: deque[float] = deque()
    for v in values:
        x = float(v or 0)
        q.append(x)
        running += x
        if len(q) > window:
            running -= q.popleft()
        out.append(running / len(q))
    return out


def normalized_power(watts: list[Number], sample_hz: float = 1.0) -> Optional[float]:
    """Coggan Normalized Power: 30s rolling avg -> 4th power -> mean -> 4th root."""
    if not watts:
        return None
    window = max(1, int(round(30 * sample_hz)))
    roll = rolling_average(watts, window)
    if not roll:
        return None
    fourth_mean = sum(r ** 4 for r in roll) / len(roll)
    return fourth_mean ** 0.25


def intensity_factor(np_value: Optional[float], ftp: float) -> Optional[float]:
    if np_value is None or not ftp:
        return None
    return np_value / ftp


def training_stress_score(
    duration_sec: float, np_value: Optional[float], ftp: float
) -> Optional[float]:
    """TSS = (sec * NP * IF) / (FTP * 3600) * 100."""
    if np_value is None or not ftp or duration_sec <= 0:
        return None
    if_ = np_value / ftp
    return (duration_sec * np_value * if_) / (ftp * 3600) * 100.0


def efficiency_factor(np_value: Optional[float], avg_hr: Optional[float]) -> Optional[float]:
    """EF = NP / average HR. Rising over time at the same effort = improving aerobic fitness."""
    if np_value is None or not avg_hr:
        return None
    return np_value / avg_hr


def decoupling(watts: list[Number], hr: list[Number], min_samples: int = 600) -> Optional[float]:
    """Aerobic decoupling (Pw:Hr) as a percentage.

    Splits the effort in half and compares power/HR ratio. A positive value means
    HR drifted upward relative to power in the second half (cardiac drift) — a sign
    of fatigue or limited aerobic durability. Most meaningful for steady efforts;
    treat with care on interval sessions. Needs ~10+ minutes of paired data.
    """
    n = min(len(watts), len(hr))
    if n < min_samples:
        return None
    half = n // 2

    def ratio(ws: list[Number], hs: list[Number]) -> Optional[float]:
        pairs = [(float(w or 0), float(h)) for w, h in zip(ws, hs) if h]
        if not pairs:
            return None
        ap = sum(p[0] for p in pairs) / len(pairs)
        ah = sum(p[1] for p in pairs) / len(pairs)
        if ah == 0:
            return None
        return ap / ah

    r1 = ratio(watts[:half], hr[:half])
    r2 = ratio(watts[half:], hr[half:])
    if not r1 or not r2:
        return None
    return (r1 - r2) / r1 * 100.0


def power_zones(ftp: float) -> dict[str, tuple[Optional[float], Optional[float]]]:
    """Coggan 7-zone model, watts (lower, upper)."""
    return {
        "Z1 Recovery": (0, 0.55 * ftp),
        "Z2 Endurance": (0.56 * ftp, 0.75 * ftp),
        "Z3 Tempo": (0.76 * ftp, 0.90 * ftp),
        "Z4 Threshold": (0.91 * ftp, 1.05 * ftp),
        "Z5 VO2max": (1.06 * ftp, 1.20 * ftp),
        "Z6 Anaerobic": (1.21 * ftp, 1.50 * ftp),
        "Z7 Neuromuscular": (1.51 * ftp, None),
    }


def hr_zones(max_hr: float) -> dict[str, tuple[float, Optional[float]]]:
    """5-zone %HRmax model, bpm (lower, upper)."""
    return {
        "Z1": (0, 0.60 * max_hr),
        "Z2": (0.60 * max_hr, 0.70 * max_hr),
        "Z3": (0.70 * max_hr, 0.80 * max_hr),
        "Z4": (0.80 * max_hr, 0.90 * max_hr),
        "Z5": (0.90 * max_hr, None),
    }


def summarize_ride(
    activity: dict[str, Any], streams: dict[str, list[Any]] | None, ftp: float
) -> dict[str, Any]:
    """Combine a Strava activity summary/detail + optional streams into the
    metrics we reason over. Falls back to Strava's summary fields when streams
    are unavailable."""
    streams = streams or {}
    watts = streams.get("watts") or []
    hr = streams.get("heartrate") or []

    # True NP from streams when available; otherwise fall back to Strava's
    # weighted average, then plain average power (rough, but keeps load tracking
    # working for older rides we didn't pull streams for).
    np_value = (
        normalized_power(watts)
        if watts
        else (activity.get("weighted_average_watts") or activity.get("average_watts"))
    )
    moving_time = activity.get("moving_time") or 0
    avg_hr = activity.get("average_heartrate")
    if not avg_hr and hr:
        valid = [h for h in hr if h]
        avg_hr = sum(valid) / len(valid) if valid else None

    if_ = intensity_factor(np_value, ftp)
    tss = training_stress_score(moving_time, np_value, ftp)
    ef = efficiency_factor(np_value, avg_hr)
    decoup = decoupling(watts, hr) if (watts and hr) else None

    activity_type = activity.get("type") or activity.get("sport_type")
    return {
        "id": activity.get("id"),
        "name": activity.get("name"),
        "date": (activity.get("start_date_local") or activity.get("start_date") or "")[:10],
        "type": activity_type,
        "is_zwift": activity_type == "VirtualRide",
        "moving_time_min": round(moving_time / 60, 1) if moving_time else None,
        "distance_km": round(activity["distance"] / 1000, 1) if activity.get("distance") else None,
        "elevation_m": activity.get("total_elevation_gain"),
        "avg_power": activity.get("average_watts"),
        "normalized_power": round(np_value) if np_value else None,
        "max_power": activity.get("max_watts"),
        "intensity_factor": round(if_, 3) if if_ else None,
        "tss": round(tss) if tss else None,
        "avg_hr": round(avg_hr) if avg_hr else None,
        "max_hr": activity.get("max_heartrate"),
        "efficiency_factor": round(ef, 3) if ef else None,
        "decoupling_pct": round(decoup, 1) if decoup is not None else None,
        "avg_cadence": activity.get("average_cadence"),
        "has_power_meter": activity.get("device_watts", False),
        "suffer_score": activity.get("suffer_score"),
    }
