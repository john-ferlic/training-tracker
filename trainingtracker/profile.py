"""Detect when the athlete's measured stats drift from config/athlete.yaml and
suggest updates: FTP + weight (from the Strava profile), resting-HR baseline
(from Oura), and max HR (from observed ride peaks).

Read-only — it only *reports* suggestions. The cloud routine (or you) applies them
via a reviewed branch/PR, so the file's comments and formatting are preserved and
each change (especially a new max HR, which can be a HR-strap glitch) gets eyeballed.
"""
from __future__ import annotations

import statistics
from typing import Any

# Thresholds to avoid day-to-day thrash — only suggest meaningful changes.
WEIGHT_MIN_DELTA = 1.0     # kg
RESTING_HR_MIN_DELTA = 3   # bpm
MAX_HR_MIN_BUMP = 2        # bpm (only ever bump up, to a new observed peak)
MAX_HR_SUSPICIOUS = 12     # bpm jump above which we flag a likely artifact


def suggest_profile_updates(
    athlete: dict[str, Any],
    strava_athlete: dict[str, Any] | None,
    oura_days: dict[str, Any] | None,
    rides: list[dict[str, Any]] | None,
) -> list[dict[str, Any]]:
    changes: list[dict[str, Any]] = []
    sa = strava_athlete or {}

    # FTP — from the Strava profile (changes when you retest and it's set in Strava)
    s_ftp, cur = sa.get("ftp"), athlete.get("ftp")
    if s_ftp and cur and abs(s_ftp - cur) >= 1:
        changes.append({"field": "ftp", "current": cur, "suggested": int(round(s_ftp)),
                        "reason": f"Strava profile FTP is {int(round(s_ftp))} vs config {cur}"})

    # Weight — from the Strava profile (kg)
    s_wt, cur = sa.get("weight"), athlete.get("weight_kg")
    if s_wt and cur and abs(s_wt - cur) >= WEIGHT_MIN_DELTA:
        changes.append({"field": "weight_kg", "current": cur, "suggested": round(s_wt, 1),
                        "reason": f"Strava profile weight is {round(s_wt, 1)}kg vs config {cur}"})

    # Resting HR baseline — median of Oura's resting HR over the stored window
    rhrs = [d.get("resting_hr") for d in (oura_days or {}).values() if d.get("resting_hr")]
    cur = athlete.get("resting_hr")
    if rhrs and cur:
        base = round(statistics.median(rhrs))
        if abs(base - cur) >= RESTING_HR_MIN_DELTA:
            changes.append({"field": "resting_hr", "current": cur, "suggested": base,
                            "reason": f"Oura resting-HR median is {base} over {len(rhrs)}d vs config {cur}"})

    # Max HR — only ever bump UP, to a new observed peak
    maxes = [r.get("max_hr") for r in (rides or []) if r.get("max_hr")]
    cur = athlete.get("max_hr")
    if maxes and cur:
        peak = int(round(max(maxes)))
        if peak >= cur + MAX_HR_MIN_BUMP:
            reason = f"new observed peak HR {peak} in recent rides vs config {cur}"
            if peak > cur + MAX_HR_SUSPICIOUS:
                reason += " — large jump, verify it isn't a HR-strap artifact"
            changes.append({"field": "max_hr", "current": cur, "suggested": peak, "reason": reason})

    return changes
