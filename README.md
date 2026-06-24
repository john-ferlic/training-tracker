# 🚴 Training Tracker

Pulls your workouts from **Strava** (which also covers **Zwift** — Zwift auto-uploads
every ride to Strava with power data) and your recovery from **Oura**, compares them
against your **training plan**, and tells you each morning whether to proceed, modify,
push, or rest — with the reasons.

Everything runs **locally on your Mac**. Your tokens and data never leave your machine.

```
Strava ─┐
        ├─► fetch (Python) ─► local cache ─┐
Oura  ──┘                                  │
                                           ▼
              training-plan.yaml ──►  analysis  ──►  daily briefing + recommendation
                                    (plan vs actual,        │
                                     recovery, decoupling)   └─► /training-brief for deep Claude reasoning
```

## What it looks at

- **Per ride** (from Strava power/HR streams): Normalized Power, Intensity Factor, TSS,
  Efficiency Factor, and **HR–power decoupling** — the key "this was harder than it should
  have been" signal (cardiac drift = aerobic fatigue or poor durability).
- **Plan compliance**: did you hit the planned power/IF/TSS, or run hot / cut it short?
- **Recovery** (from Oura): readiness, sleep, resting HR and HRV vs. your rolling baseline.
- **Load**: rolling 7-day TSS.
- **Per workout type** (Zone 2 / Threshold / VO2max): each session is classified from the actual
  data, with **interval-by-interval power fade** — did you hold power across every rep, or fade on
  the last few?
- **Trends over time** (the point of it): per-type progression (threshold durability, VO2
  repeatability, Z2 aerobic efficiency), overall **fitness** (CTL/ATL/TSB), and **weakness →
  plan-adaptation** suggestions that can actually rewrite your plan.

It combines the daily signals into a verdict — **PROCEED / MODIFY / PUSH / REST** — with reasons,
and tracks the longitudinal picture to tell you where to focus and how to adapt the plan.

---

## One-time setup (~10 minutes)

### 1. Install

```bash
cd "Training Tracker"
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
cp .env.example .env
```

### 2. Connect Strava (covers Zwift too)

1. Go to <https://www.strava.com/settings/api> and create an app (any name; set
   **Authorization Callback Domain** to `localhost`).
2. Copy the **Client ID** and **Client Secret** into `.env`.
3. Authorize and capture a refresh token:
   ```bash
   .venv/bin/python scripts/auth_strava.py
   ```
   This opens your browser, you click **Authorize**, and it writes
   `STRAVA_REFRESH_TOKEN` into `.env` for you.

### 3. Connect Oura

1. Go to <https://cloud.ouraring.com/personal-access-tokens> and create a token.
2. Paste it into `.env` as `OURA_ACCESS_TOKEN`.

### 4. Set your numbers

[`config/athlete.yaml`](config/athlete.yaml) is set to **FTP 315**. Still set your **max HR**
and **weight** (placeholders), and your timezone. Re-anchor `ftp` after each retest.

### 5. Your training plan

Your **20-week pyramidal FTP build** is already encoded in
[`config/training-plan.yaml`](config/training-plan.yaml) as 4 phases (Aerobic Base → Threshold
Build → VO2max → Consolidation/Peak), with FTP retests scheduled at the start of Phase 2 and
end of Phase 4. After a retest, update `ftp` in `athlete.yaml` (and re-anchor that phase's watt
targets, or ask Claude via `/training-review`).

### 6. Verify

```bash
.venv/bin/python -m trainingtracker setup-check
.venv/bin/python -m trainingtracker run        # first real fetch + briefing
```

---

## Daily use

**Option A — automatic in the cloud (recommended).** A daily Claude routine running in
Anthropic's cloud that posts a coaching summary you can chat into all day, and can propose plan
changes as reviewable PRs. Setup: **[cloud/SETUP.md](cloud/SETUP.md)**.

**Option B — on demand from the terminal:**

```bash
.venv/bin/python -m trainingtracker run
```

**Option C — deep reasoning with Claude.** In Claude Code, run:

```
/training-brief
```

This pulls fresh data and gives a fully reasoned recommendation you can talk to
("should I still do intervals?", "I felt flat yesterday", "move my rest day"). Uses your
Claude subscription — no API key needed. It can also adjust your plan file when warranted.

For the bigger picture, run **`/training-review`** — Claude analyzes your trends per workout
type, identifies your current limiter (e.g. threshold durability), and proposes specific edits
to `config/training-plan.yaml` (add a session, extend intervals, lengthen VO2 recoveries),
confirming with you before writing.

### Optional: Strava MCP connector (conversational)

Strava ships an official **MCP connector** (subscriber-only, read-only) for *talking to* your data
in Claude. It's a nice add-on for ad-hoc questions, but it is **not** the analysis engine:

- **Keep the direct API as the data pipeline.** The deterministic analysis — interval fade,
  Normalized Power, decoupling, TSS, CTL/ATL/TSB — needs the **complete per-second streams**, which
  the REST `streams` endpoint returns in full. MCP tool results are LLM-oriented and may be
  downsampled/truncated, and the connector's conversational rate limits aren't suited to backfilling
  streams for dozens of rides in a headless cron job.
- **Use the MCP for chat.** Once connected, `/training-brief` and `/training-review` will use it for
  conversational follow-ups ("how did today compare to the same workout last month?") while still
  pulling the hard numbers from the local pipeline.

**To connect it:** in the Claude app, add the **Strava** connector from the connector directory
(or Strava → Settings → connect to Claude). No code or credentials change here — the Python pipeline
keeps using your direct Strava API token.

### Optional: hands-off cloud routine

Want the morning briefing to run in **Anthropic's cloud** (even with your Mac off) and leave a
session you can chat into all day? The code is already cloud-ready — see
**[cloud/SETUP.md](cloud/SETUP.md)** for the account-side wiring (push to GitHub, connect your
account, create the routine, add token secrets). Each run re-fetches fresh data and posts a
coaching summary you can open and ask follow-ups on.

---

## Tracking progress & finding weaknesses

Every ride is analyzed once and stored in `data/workout_history.json`, so trends accumulate.

- **Per workout** (`analyze`): classifies the session (Z2 / Threshold / VO2max) from the actual
  power distribution, detects each work interval, and measures **fade** — how much power dropped
  on the later reps. "Struggled on the last few threshold intervals" shows up as a fade %.
- **Per type over time** (`review`):
  - **Threshold** — is interval power trending up? Is fade shrinking (durability improving)?
  - **VO2max** — repeatability: are later reps holding, or collapsing?
  - **Zone 2** — is efficiency (EF) rising and decoupling falling? That's your aerobic base improving.
- **Overall fitness** — a Performance Management Chart: **CTL** (Fitness, 42-day load), **ATL**
  (Fatigue, 7-day), **TSB** (Form = CTL−ATL). Needs ~6 weeks of data to be accurate.
- **Weakness → plan change** — `review` flags the limiter and suggests a concrete adaptation;
  `/training-review` turns that into an actual plan edit. The daily brief also surfaces your top
  focus item so it's in front of you every day.

---

## Commands

| Command | What it does |
|---|---|
| `python -m trainingtracker setup-check` | Verify config + credentials |
| `python -m trainingtracker fetch` | Pull Strava + Oura into the local cache |
| `python -m trainingtracker brief` | Build today's briefing from cached data (`--notify` to also notify) |
| `python -m trainingtracker run` | fetch + brief + notify — the daily entrypoint |
| `python -m trainingtracker analyze` | Deep report on the latest workout (intervals, fade, zones); `--id N` for a specific ride |
| `python -m trainingtracker review` | Longitudinal trends per workout type, fitness (CTL/ATL/TSB), weaknesses + plan suggestions |
| `python -m trainingtracker show-plan --days 5` | Print upcoming planned workouts |

Briefings are written to `data/briefings/YYYY-MM-DD.md` (and `latest.md`).

---

## Optional: auto-written coach narrative

By default the scheduled briefing uses a fast, built-in rule-based recommendation (no API
key, works offline). If you want each automated briefing to *also* include a natural-language
coach paragraph written by Claude, set `ANTHROPIC_API_KEY` in `.env`
(and `pip install anthropic`). Override the model with `ANTHROPIC_MODEL` if you like
(defaults to `claude-opus-4-8`). This is purely additive — the interactive `/training-brief`
gives you Claude's reasoning regardless.

---

## Tuning

All decision thresholds live under `thresholds:` in `config/athlete.yaml` — readiness cutoffs,
how many bpm of resting-HR elevation counts as a flag, the decoupling threshold, weekly-load
ceiling, etc. Adjust them as you learn your own numbers.

## Tests

```bash
.venv/bin/python tests/test_metrics.py      # or: .venv/bin/python -m pytest tests/
```

## Notes

- **Zwift has no public API** — but because Zwift auto-uploads to Strava as `VirtualRide`
  activities (with power), Strava is the single source for both. Zwift rides are tagged in
  the briefing.
- The **cloud routine** ([cloud/SETUP.md](cloud/SETUP.md)) runs even when your Mac is off, and
  re-fetches fresh data on each run.
- Locally, the only outbound calls are to Strava and Oura (and Anthropic, only if you opt into
  the coach narrative).
