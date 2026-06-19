---
description: Pull fresh Strava + Oura data and give a reasoned training recommendation for today
---

You are acting as the user's cycling coach. Produce a concrete recommendation for today's
training, grounded in their actual data and plan.

Focus from the user (optional): $ARGUMENTS

Do this in order:

1. **Refresh data** (best effort): run `python -m trainingtracker fetch`.
   If it fails (missing credentials, network), say so briefly and continue with cached data.

2. **Compute the deterministic briefing**: run `python -m trainingtracker brief --no-coach`.
   This writes `data/briefings/latest.md` and prints the structured assessment.

3. **Read the underlying data** so you can reason beyond the rules:
   - `config/athlete.yaml` (FTP, max HR, thresholds)
   - `config/training-plan.yaml` (the plan you're comparing against)
   - `data/activities.json` (recent rides with NP, IF, TSS, HR, decoupling)
   - `data/oura.json` (readiness, sleep, resting HR, HRV by day)

4. **Reason and recommend.** Go past the rule-based verdict:
   - Did recent sessions hit their planned power/IF/TSS targets, or did they run hot/easy?
     Look at HR-power **decoupling** (>~6% on a steady ride = aerobic fatigue / poor durability)
     and whether HR was high for the target power.
   - Read the **Oura trend** over several days, not just today — a 3-day slide in readiness,
     rising resting HR, or HRV below baseline means accumulating fatigue even if today's
     single number looks OK.
   - Weigh recovery against **today's planned intensity**. Don't stack a hard VO2/threshold day
     onto poor recovery; don't waste a green-light day on junk either.
   - Consider the **next 3 days** — if a key session is coming, protect it.

5. **Output** (keep it tight, specific, and numeric):
   - **Verdict**: Proceed / Modify / Push / Rest — and if Modify, the exact change
     (e.g. "3×12 → 3×10 @ the same power", or "swap for 60min Z2").
   - **Why**: the 2-4 signals that drove it, with numbers.
   - **Watch**: one thing to monitor during/after the session.

6. If a change to the upcoming plan is clearly warranted (e.g. an extra recovery day),
   offer to edit `config/training-plan.yaml` — but propose the edit and confirm before writing.

---

**Strava MCP (optional, conversational only):** If a Strava MCP connector is available in this
session (tools named like `mcp__*strava*`), you may use it to answer the user's ad-hoc follow-ups
— e.g. "pull up my ride from last Tuesday" or "how did today compare to the same workout 3 weeks
ago." **But the numeric analysis — intervals, fade %, NP, IF, TSS, decoupling — must come from the
local pipeline** (`python -m trainingtracker ...` / `data/workout_history.json`), which has the full
per-second streams. Don't compute fade or NP from MCP summaries; they may be downsampled.
