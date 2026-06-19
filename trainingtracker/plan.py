"""Resolve a calendar date to its planned workout.

Supports periodized plans with phases (each a week range + its own weekly
template), resolved by week number from `meta.start_date`. Falls back to a single
top-level `week_template` for simple plans.

Priority: an exact-date entry under `schedule:` (tests, races) wins; otherwise the
phase whose week range contains the date; otherwise the top-level template.
"""
from __future__ import annotations

from datetime import date, timedelta
from typing import Any, Optional

WEEKDAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]


def _start_date(plan: dict[str, Any]) -> Optional[date]:
    s = (plan.get("meta") or {}).get("start_date")
    if s is None:
        return None
    return date.fromisoformat(s) if isinstance(s, str) else s


def week_number(plan: dict[str, Any], d: date) -> Optional[int]:
    """1-based training week for date `d` (week 1 = the start week)."""
    start = _start_date(plan)
    if start is None:
        return None
    return (d - start).days // 7 + 1


def _phase_for_week(plan: dict[str, Any], wk: int) -> Optional[dict[str, Any]]:
    for ph in plan.get("phases", []) or []:
        rng = ph.get("weeks") or [None, None]
        lo, hi = rng[0], rng[1]
        if lo is not None and hi is not None and lo <= wk <= hi:
            return ph
    return None


def workout_for(plan: dict[str, Any], d: date) -> dict[str, Any]:
    schedule = plan.get("schedule") or {}
    for key in (d, d.isoformat()):
        entry = schedule.get(key)
        if entry:
            return {**entry, "date": d.isoformat(), "source": "schedule"}

    weekday = WEEKDAYS[d.weekday()]

    if plan.get("phases"):
        wk = week_number(plan, d)
        ph = _phase_for_week(plan, wk) if wk else None
        if ph:
            entry = (ph.get("week_template") or {}).get(weekday)
            if entry:
                return {**entry, "date": d.isoformat(), "weekday": weekday,
                        "source": "phase", "phase": ph.get("name"), "week": wk}
        return {"type": "Unplanned", "date": d.isoformat(), "weekday": weekday,
                "source": "none", "week": wk}

    entry = (plan.get("week_template") or {}).get(weekday)
    if entry:
        return {**entry, "date": d.isoformat(), "weekday": weekday, "source": "template"}
    return {"type": "Unplanned", "date": d.isoformat(), "weekday": weekday, "source": "none"}


def upcoming(plan: dict[str, Any], start: date, days: int = 3) -> list[dict[str, Any]]:
    return [workout_for(plan, start + timedelta(days=i)) for i in range(days)]
