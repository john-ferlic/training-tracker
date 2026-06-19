"""Configuration + path helpers. Loads .env and the YAML config files."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - dotenv is in requirements, but degrade gracefully
    def load_dotenv(*_args, **_kwargs):  # type: ignore
        return False

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = PROJECT_ROOT / "config"
# DATA_DIR defaults to <repo>/data, but can be redirected with TT_DATA_DIR — useful
# in the cloud sandbox if the repo is mounted read-only (point it at a writable path).
DATA_DIR = Path(os.environ.get("TT_DATA_DIR") or (PROJECT_ROOT / "data"))
BRIEFINGS_DIR = DATA_DIR / "briefings"
ENV_PATH = PROJECT_ROOT / ".env"

_ENV_LOADED = False


def load_env() -> None:
    """Load .env once from the project root."""
    global _ENV_LOADED
    if not _ENV_LOADED:
        load_dotenv(ENV_PATH)
        _ENV_LOADED = True


def get_env(key: str, required: bool = False, default: str | None = None) -> str | None:
    load_env()
    val = os.environ.get(key, default)
    if required and not val:
        raise RuntimeError(
            f"Missing required environment variable {key!r}. "
            f"Copy .env.example to .env and fill it in (see README)."
        )
    return val


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")
    with path.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Expected a mapping at the top of {path}")
    return data


def load_athlete() -> dict[str, Any]:
    return _load_yaml(CONFIG_DIR / "athlete.yaml")


def load_plan() -> dict[str, Any]:
    return _load_yaml(CONFIG_DIR / "training-plan.yaml")


def ensure_data_dirs() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    BRIEFINGS_DIR.mkdir(parents=True, exist_ok=True)
