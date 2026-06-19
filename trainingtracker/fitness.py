"""Overall fitness via the Performance Management Chart (Banister impulse-response):

  CTL ("Fitness")  = 42-day exponentially-weighted average of daily TSS
  ATL ("Fatigue")  =  7-day exponentially-weighted average of daily TSS
  TSB ("Form")     = CTL - ATL   (positive = fresh, negative = fatigued)

CTL needs ~6 weeks of history to be accurate; with less data treat it as a lower bound.
"""
from __future__ import annotations

from collections import defaultdict
from datetime import date, timedelta
from typing import Any, Optional

CTL_TC = 42
ATL_TC = 7


def daily_tss_map(records: list[dict[str, Any]]) -> dict[str, float]:
    m: dict[str, float] = defaultdict(float)
    for r in records:
        d = r.get("date")
        if d:
            m[d] += r.get("tss") or 0
    return dict(m)


def pmc(records: list[dict[str, Any]], today: date) -> list[dict[str, Any]]:
    tmap = daily_tss_map(records)
    present = sorted(tmap)
    if not present:
        return []
    start = date.fromisoformat(present[0])

    # Seed CTL/ATL with the average daily load over the first two weeks of data,
    # so early CTL isn't misleadingly near zero.
    seed_end = start + timedelta(days=14)
    seed_days = [v for k, v in tmap.items() if k < seed_end.isoformat()]
    seed = (sum(seed_days) / 14) if seed_days else 0.0

    ctl = atl = seed
    series: list[dict[str, Any]] = []
    d = start
    while d <= today:
        tss = tmap.get(d.isoformat(), 0.0)
        ctl += (tss - ctl) / CTL_TC
        atl += (tss - atl) / ATL_TC
        series.append({"date": d.isoformat(), "tss": round(tss),
                       "ctl": round(ctl, 1), "atl": round(atl, 1),
                       "tsb": round(ctl - atl, 1)})
        d += timedelta(days=1)
    return series


def _form_state(tsb: float) -> str:
    if tsb > 10:
        return "fresh / detraining risk"
    if tsb > 5:
        return "fresh"
    if tsb >= -10:
        return "neutral"
    if tsb >= -20:
        return "productive overload"
    return "high fatigue"


def current(records: list[dict[str, Any]], today: date) -> Optional[dict[str, Any]]:
    series = pmc(records, today)
    if not series:
        return None
    latest = series[-1]
    ramp = None
    if len(series) >= 8:
        ramp = round(latest["ctl"] - series[-8]["ctl"], 1)  # CTL change over 7 days
    span_days = (today - date.fromisoformat(series[0]["date"])).days
    return {
        "ctl": latest["ctl"],
        "atl": latest["atl"],
        "tsb": latest["tsb"],
        "ramp_7d": ramp,
        "form_state": _form_state(latest["tsb"]),
        "data_span_days": span_days,
        "ctl_reliable": span_days >= 42,
    }
