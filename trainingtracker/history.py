"""Persistent per-workout history, keyed by Strava activity id, so each ride is
analyzed once and trends accumulate over time. This is the source of truth for
both the daily briefing and the longitudinal review."""
from __future__ import annotations

import json
from datetime import date, timedelta
from typing import Any

from . import config

HISTORY_PATH = config.DATA_DIR / "workout_history.json"


def load() -> dict[str, dict[str, Any]]:
    if not HISTORY_PATH.exists():
        return {}
    try:
        return json.loads(HISTORY_PATH.read_text())
    except (ValueError, OSError):
        return {}


def save(history: dict[str, dict[str, Any]]) -> None:
    config.ensure_data_dirs()
    HISTORY_PATH.write_text(json.dumps(history, indent=2, default=str))


def has(history: dict[str, dict[str, Any]], activity_id: Any) -> bool:
    return str(activity_id) in history


def upsert(history: dict[str, dict[str, Any]], record: dict[str, Any]) -> None:
    if record.get("id") is not None:
        history[str(record["id"])] = record


def records(history: dict[str, dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    """All records sorted oldest -> newest by date."""
    h = history if history is not None else load()
    return sorted(h.values(), key=lambda r: r.get("date") or "")


def recent(history: dict[str, dict[str, Any]] | None, today: date, days: int) -> list[dict[str, Any]]:
    cutoff = (today - timedelta(days=days)).isoformat()
    return [r for r in records(history) if (r.get("date") or "") >= cutoff]


def of_type(
    history: dict[str, dict[str, Any]] | None,
    types: set[str],
    today: date,
    weeks: int = 8,
) -> list[dict[str, Any]]:
    """Records whose classified (or planned) type is in `types`, within `weeks`."""
    cutoff = (today - timedelta(weeks=weeks)).isoformat()
    out = []
    for r in records(history):
        if (r.get("date") or "") < cutoff:
            continue
        t = r.get("classified_type") or r.get("planned_type")
        if t in types:
            out.append(r)
    return out
