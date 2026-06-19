"""Oura Ring API v2 client (Personal Access Token).

Pulls daily readiness, daily sleep, and detailed sleep periods (for resting HR
and HRV), which feed the recovery side of the analysis.

Docs: https://cloud.ouraring.com/v2/docs
"""
from __future__ import annotations

from datetime import date, timedelta
from typing import Any

import requests

from .. import config

API_BASE = "https://api.ouraring.com/v2/usercollection"


class OuraError(RuntimeError):
    pass


class OuraClient:
    def __init__(self) -> None:
        self.token = config.get_env("OURA_ACCESS_TOKEN", required=True)

    def _get(self, path: str, params: dict[str, Any]) -> list[dict[str, Any]]:
        resp = requests.get(
            f"{API_BASE}{path}",
            headers={"Authorization": f"Bearer {self.token}"},
            params=params,
            timeout=30,
        )
        if resp.status_code == 401:
            raise OuraError(
                "Oura auth failed (401). Check OURA_ACCESS_TOKEN in .env "
                "(create one at https://cloud.ouraring.com/personal-access-tokens)."
            )
        if resp.status_code != 200:
            raise OuraError(f"GET {path} failed ({resp.status_code}): {resp.text[:300]}")
        return resp.json().get("data", [])

    def _window(self, path: str, days: int, end: date | None = None) -> list[dict[str, Any]]:
        end = end or date.today()
        # Oura treats end_date as inclusive of that day's data; pad by one day.
        start = end - timedelta(days=days)
        return self._get(
            path,
            {"start_date": start.isoformat(), "end_date": (end + timedelta(days=1)).isoformat()},
        )

    def daily_readiness(self, days: int = 14, end: date | None = None) -> list[dict[str, Any]]:
        return self._window("/daily_readiness", days, end)

    def daily_sleep(self, days: int = 14, end: date | None = None) -> list[dict[str, Any]]:
        return self._window("/daily_sleep", days, end)

    def sleep_periods(self, days: int = 14, end: date | None = None) -> list[dict[str, Any]]:
        return self._window("/sleep", days, end)

    def recovery_window(self, days: int = 14, end: date | None = None) -> dict[str, dict[str, Any]]:
        """Merge readiness + sleep score + detailed sleep, keyed by 'YYYY-MM-DD'.

        Each day: {date, readiness, sleep_score, total_sleep_h, resting_hr,
        average_hrv, efficiency, temperature_deviation}.
        """
        readiness = {r["day"]: r for r in self.daily_readiness(days, end)}
        sleep_score = {s["day"]: s for s in self.daily_sleep(days, end)}
        # Detailed sleep can have multiple periods per day; keep the longest.
        periods: dict[str, dict[str, Any]] = {}
        for p in self.sleep_periods(days, end):
            d = p.get("day")
            if not d:
                continue
            if d not in periods or (p.get("total_sleep_duration") or 0) > (
                periods[d].get("total_sleep_duration") or 0
            ):
                periods[d] = p

        merged: dict[str, dict[str, Any]] = {}
        for d in sorted(set(readiness) | set(sleep_score) | set(periods)):
            r = readiness.get(d, {})
            ss = sleep_score.get(d, {})
            pp = periods.get(d, {})
            total_sleep = pp.get("total_sleep_duration")
            merged[d] = {
                "date": d,
                "readiness": r.get("score"),
                "readiness_contributors": r.get("contributors", {}),
                "sleep_score": ss.get("score"),
                "total_sleep_h": round(total_sleep / 3600, 2) if total_sleep else None,
                "resting_hr": pp.get("lowest_heart_rate"),
                "average_hrv": pp.get("average_hrv"),
                "efficiency": pp.get("efficiency"),
                "temperature_deviation": r.get("temperature_deviation"),
            }
        return merged
