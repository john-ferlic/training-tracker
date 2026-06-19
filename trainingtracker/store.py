"""Local JSON cache of fetched data, so the briefing can run (and be inspected)
without re-hitting the APIs, and so trends persist across days."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from . import config

ACTIVITIES_PATH = config.DATA_DIR / "activities.json"
OURA_PATH = config.DATA_DIR / "oura.json"


def _write(path, payload: Any) -> None:
    config.ensure_data_dirs()
    path.write_text(json.dumps(payload, indent=2, default=str))


def _read(path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text())
    except (ValueError, OSError):
        return default


def save_activities(rides: list[dict[str, Any]]) -> None:
    _write(ACTIVITIES_PATH, {"fetched_at": datetime.now(timezone.utc).isoformat(), "rides": rides})


def load_activities() -> list[dict[str, Any]]:
    return _read(ACTIVITIES_PATH, {}).get("rides", [])


def save_oura(window: dict[str, Any]) -> None:
    _write(OURA_PATH, {"fetched_at": datetime.now(timezone.utc).isoformat(), "days": window})


def load_oura() -> dict[str, Any]:
    return _read(OURA_PATH, {}).get("days", {})
