"""Strava API client.

Covers both outdoor rides and Zwift (Zwift auto-uploads to Strava as
VirtualRide activities, with power). Handles OAuth token refresh and caches the
short-lived access token locally so we don't refresh on every call.

Docs: https://developers.strava.com/docs/reference/
"""
from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from typing import Any

import requests

from .. import config

API_BASE = "https://www.strava.com/api/v3"
TOKEN_URL = "https://www.strava.com/oauth/token"
TOKEN_CACHE = config.DATA_DIR / "strava_token.json"

# Strava default rate limits: 200 req / 15 min, 2000 / day.


class StravaError(RuntimeError):
    pass


class StravaClient:
    def __init__(self) -> None:
        self.client_id = config.get_env("STRAVA_CLIENT_ID", required=True)
        self.client_secret = config.get_env("STRAVA_CLIENT_SECRET", required=True)
        self.refresh_token = config.get_env("STRAVA_REFRESH_TOKEN", required=True)
        self._access_token: str | None = None
        self._expires_at: int = 0
        self._load_cached_token()

    # -- token handling ------------------------------------------------------
    def _load_cached_token(self) -> None:
        if TOKEN_CACHE.exists():
            try:
                data = json.loads(TOKEN_CACHE.read_text())
                self._access_token = data.get("access_token")
                self._expires_at = int(data.get("expires_at", 0))
            except (ValueError, OSError):
                pass

    def _save_cached_token(self) -> None:
        config.ensure_data_dirs()
        TOKEN_CACHE.write_text(
            json.dumps({"access_token": self._access_token, "expires_at": self._expires_at})
        )

    def _refresh(self) -> None:
        resp = requests.post(
            TOKEN_URL,
            data={
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "grant_type": "refresh_token",
                "refresh_token": self.refresh_token,
            },
            timeout=30,
        )
        if resp.status_code != 200:
            raise StravaError(
                f"Token refresh failed ({resp.status_code}): {resp.text[:300]}. "
                f"Re-run `python scripts/auth_strava.py` to reauthorize."
            )
        payload = resp.json()
        self._access_token = payload["access_token"]
        self._expires_at = int(payload["expires_at"])
        # Strava's refresh token is normally stable, but persist if it rotates.
        self.refresh_token = payload.get("refresh_token", self.refresh_token)
        self._save_cached_token()

    def _token(self) -> str:
        # Refresh if missing or within 5 minutes of expiry.
        if not self._access_token or time.time() > (self._expires_at - 300):
            self._refresh()
        assert self._access_token
        return self._access_token

    # -- HTTP ----------------------------------------------------------------
    def _get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        resp = requests.get(
            f"{API_BASE}{path}",
            headers={"Authorization": f"Bearer {self._token()}"},
            params=params or {},
            timeout=30,
        )
        if resp.status_code == 401:
            # token may have been revoked mid-run; force one refresh + retry
            self._refresh()
            resp = requests.get(
                f"{API_BASE}{path}",
                headers={"Authorization": f"Bearer {self._token()}"},
                params=params or {},
                timeout=30,
            )
        if resp.status_code == 429:
            raise StravaError("Strava rate limit hit (429). Try again later.")
        if resp.status_code != 200:
            raise StravaError(f"GET {path} failed ({resp.status_code}): {resp.text[:300]}")
        return resp.json()

    # -- endpoints -----------------------------------------------------------
    def list_activities(
        self,
        after: datetime | int | None = None,
        before: datetime | int | None = None,
        per_page: int = 100,
        max_pages: int = 5,
    ) -> list[dict[str, Any]]:
        """List summary activities between `after` and `before` (newest first
        within Strava's paging). Accepts datetimes or epoch seconds."""
        def epoch(v: datetime | int | None) -> int | None:
            if v is None:
                return None
            if isinstance(v, datetime):
                if v.tzinfo is None:
                    v = v.replace(tzinfo=timezone.utc)
                return int(v.timestamp())
            return int(v)

        out: list[dict[str, Any]] = []
        for page in range(1, max_pages + 1):
            params: dict[str, Any] = {"per_page": per_page, "page": page}
            a, b = epoch(after), epoch(before)
            if a is not None:
                params["after"] = a
            if b is not None:
                params["before"] = b
            batch = self._get("/athlete/activities", params)
            if not batch:
                break
            out.extend(batch)
            if len(batch) < per_page:
                break
        return out

    def get_activity(self, activity_id: int) -> dict[str, Any]:
        """Detailed activity (includes weighted_average_watts, device_watts, etc.)."""
        return self._get(f"/activities/{activity_id}", {"include_all_efforts": "false"})

    def get_streams(
        self, activity_id: int, keys: tuple[str, ...] = ("time", "watts", "heartrate", "cadence")
    ) -> dict[str, list[Any]]:
        """Per-second time series. Returns {key: [values...]} (only present keys)."""
        raw = self._get(
            f"/activities/{activity_id}/streams",
            {"keys": ",".join(keys), "key_by_type": "true"},
        )
        return {k: v.get("data", []) for k, v in raw.items() if isinstance(v, dict)}

    def get_athlete(self) -> dict[str, Any]:
        """Authenticated athlete profile. Includes `ftp` and `weight` (kg) when set
        in Strava — used to keep config/athlete.yaml current."""
        return self._get("/athlete")
