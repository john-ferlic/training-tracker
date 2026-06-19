"""Optional: a natural-language coaching narrative for the daily briefing,
written by Claude via the Anthropic API.

This is strictly optional. If `anthropic` isn't installed or ANTHROPIC_API_KEY
isn't set, `coach_narrative()` returns None and the briefing falls back to the
built-in rule-based recommendation. Interactive deep-dive reasoning is always
available through the /training-brief slash command (which uses your Claude
subscription, no API key needed).
"""
from __future__ import annotations

import json
from typing import Any, Optional

from . import config

SYSTEM = """You are an experienced, evidence-based cycling coach writing a short \
daily briefing for one athlete. You are given today's planned workout, how recent \
rides compared to plan (power, intensity factor, TSS, HR-power decoupling), and \
Oura recovery signals (readiness, sleep, resting HR, HRV vs baseline).

Write 3-5 sentences, direct and practical. Decide whether the athlete should \
proceed as planned, modify (and exactly how — e.g. cut an interval, drop to Z2), \
push a little, or rest. Weigh recovery against the planned intensity: don't stack \
hard work onto poor recovery, but don't sandbag an easy day either. Reference the \
specific numbers that drive your call. No preamble, no headers, no emoji — just \
the recommendation and the why."""


def coach_narrative(assessment: dict[str, Any], athlete: dict[str, Any]) -> Optional[str]:
    api_key = config.get_env("ANTHROPIC_API_KEY")
    if not api_key:
        return None
    try:
        import anthropic
    except ImportError:
        return None

    model = config.get_env("ANTHROPIC_MODEL") or "claude-opus-4-8"
    payload = {
        "athlete": {k: athlete.get(k) for k in ("ftp", "max_hr", "weight_kg")},
        "assessment": assessment,
    }
    try:
        client = anthropic.Anthropic(api_key=api_key)
        resp = client.messages.create(
            model=model,
            max_tokens=16000,
            thinking={"type": "adaptive"},
            system=SYSTEM,
            messages=[
                {
                    "role": "user",
                    "content": (
                        "Here is today's data as JSON. Write the briefing.\n\n"
                        + json.dumps(payload, indent=2, default=str)
                    ),
                }
            ],
        )
    except Exception:
        # Never let the optional narrative break the briefing.
        return None

    text = "".join(b.text for b in resp.content if getattr(b, "type", None) == "text")
    return text.strip() or None
