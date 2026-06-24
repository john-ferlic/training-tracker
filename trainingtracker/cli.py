"""Command-line entrypoints.

    python -m trainingtracker setup-check   # verify config + credentials
    python -m trainingtracker fetch         # pull Strava + Oura -> analyze -> history
    python -m trainingtracker brief         # today's recommendation from history
    python -m trainingtracker run           # fetch + brief (local one-shot)
    python -m trainingtracker analyze       # deep analysis of the latest workout (--id N)
    python -m trainingtracker review        # longitudinal trends, fitness, weaknesses
    python -m trainingtracker show-plan     # print today + next days from the plan
"""
from __future__ import annotations

import argparse
import sys
from datetime import date, datetime, timedelta
from typing import Any

from . import analysis, briefing, config, history, plan as plan_mod, store, trends, workout
from .briefing import render_markdown


def _today(athlete: dict[str, Any]):
    tzname = athlete.get("timezone")
    if tzname:
        try:
            from zoneinfo import ZoneInfo

            return datetime.now(ZoneInfo(tzname)).date()
        except Exception:
            pass
    return datetime.now().astimezone().date()


def _trend_weeks(athlete: dict[str, Any]) -> int:
    return int(athlete.get("trend_weeks", 8))


# ---------------------------------------------------------------------------
def cmd_setup_check(_args) -> int:
    ok = True
    print("Config files:")
    for name in ("athlete.yaml", "training-plan.yaml"):
        p = config.CONFIG_DIR / name
        print(f"  {'OK ' if p.exists() else 'MISSING'} {p}")
        ok = ok and p.exists()

    print("\nCredentials (.env):")
    for key, required in [
        ("STRAVA_CLIENT_ID", True), ("STRAVA_CLIENT_SECRET", True),
        ("STRAVA_REFRESH_TOKEN", True), ("OURA_ACCESS_TOKEN", True),
        ("ANTHROPIC_API_KEY", False),
    ]:
        val = config.get_env(key)
        tag = "OK " if val else ("MISSING" if required else "optional, unset")
        print(f"  {tag:14} {key}")
        if required and not val:
            ok = False

    print("\n" + ("All set — try: python -m trainingtracker run" if ok
                   else "Fill the gaps above (see README), then re-run setup-check."))
    return 0 if ok else 1


def cmd_fetch(_args) -> int:
    athlete = config.load_athlete()
    plan = config.load_plan()
    ftp = float(athlete.get("ftp") or 0)
    if not ftp:
        print("Set your FTP in config/athlete.yaml first.", file=sys.stderr)
        return 1
    weeks = _trend_weeks(athlete)
    window_days = max(int(athlete.get("history_days", 56)), weeks * 7)
    iv_params = athlete.get("interval_detection")
    today = _today(athlete)

    # --- Strava (covers Zwift) -> analyze new rides into history ---
    try:
        from .clients.strava import StravaClient, StravaError

        strava = StravaClient()
        activities = strava.list_activities(after=datetime.combine(
            today - timedelta(days=window_days), datetime.min.time()))
    except RuntimeError as e:
        print(f"Strava: {e}", file=sys.stderr)
        return 1

    hist = history.load()
    new_rides = 0
    for a in activities:
        if a.get("type") not in ("Ride", "VirtualRide"):
            continue
        if history.has(hist, a.get("id")):
            continue
        try:
            streams = strava.get_streams(a["id"])
        except StravaError:
            streams = None
        rec = workout.analyze_workout(a, streams, ftp, iv_params)
        if rec.get("date"):
            rec["planned_type"] = plan_mod.workout_for(plan, date.fromisoformat(rec["date"])).get("type")
        history.upsert(hist, rec)
        new_rides += 1
    history.save(hist)
    print(f"Strava: {new_rides} new rides analyzed ({len(hist)} total in history, "
          f"window {window_days}d).")

    # --- Oura ---
    try:
        from .clients.oura import OuraClient

        oura = OuraClient()
        window = oura.recovery_window(days=int(athlete.get("history_days", 56)), end=today)
        store.save_oura(window)
        print(f"Oura: saved {len(window)} days of recovery data.")
    except RuntimeError as e:
        print(f"Oura: {e}  (continuing without recovery data)", file=sys.stderr)

    return 0


def cmd_brief(args) -> int:
    athlete = config.load_athlete()
    plan = config.load_plan()
    hist = history.load()
    rides = history.records(hist)
    oura = store.load_oura()
    today = _today(athlete)
    assessment = analysis.build_assessment(
        athlete, plan, rides, oura, today, history=hist, trend_weeks=_trend_weeks(athlete))

    coach_text = None
    if not args.no_coach:
        from .coach import coach_narrative

        coach_text = coach_narrative(assessment, athlete)

    md = render_markdown(assessment, athlete, coach_text)
    config.ensure_data_dirs()
    dated = config.BRIEFINGS_DIR / f"{today.isoformat()}.md"
    (config.BRIEFINGS_DIR / "latest.md").write_text(md)
    dated.write_text(md)
    print(md)
    print(f"\n(written to {dated})", file=sys.stderr)
    return 0


def cmd_run(args) -> int:
    rc = cmd_fetch(args)
    if rc != 0 and not args.allow_partial:
        print("Fetch failed; not generating briefing. Use --allow-partial to "
              "brief from cached data anyway.", file=sys.stderr)
        return rc
    args.no_coach = getattr(args, "no_coach", False)
    return cmd_brief(args)


def cmd_analyze(args) -> int:
    athlete = config.load_athlete()
    plan = config.load_plan()
    hist = history.load()
    recs = history.records(hist)
    if not recs:
        print("No workouts in history yet. Run: python -m trainingtracker fetch", file=sys.stderr)
        return 1
    if args.id:
        rec = hist.get(str(args.id))
        if not rec:
            print(f"No workout with id {args.id} in history.", file=sys.stderr)
            return 1
    else:
        rec = recs[-1]  # most recent by date
    planned = plan_mod.workout_for(plan, date.fromisoformat(rec["date"])) if rec.get("date") else {}
    print(briefing.render_workout(rec, planned, athlete))
    return 0


def cmd_review(args) -> int:
    athlete = config.load_athlete()
    plan = config.load_plan()
    hist = history.load()
    oura = store.load_oura()
    today = _today(athlete)
    weeks = args.weeks or _trend_weeks(athlete)
    review = trends.build_review(athlete, plan, hist, oura, today, weeks=weeks)
    md = briefing.render_review(review, athlete)
    config.ensure_data_dirs()
    (config.BRIEFINGS_DIR / "review-latest.md").write_text(md)
    print(md)
    return 0


def cmd_show_plan(args) -> int:
    athlete = config.load_athlete()
    plan = config.load_plan()
    today = _today(athlete)
    head = plan_mod.workout_for(plan, today)
    if head.get("phase"):
        print(f"{head['phase']} · week {head.get('week')}  (FTP {athlete.get('ftp')}w)\n")
    for i in range(args.days):
        d = today + timedelta(days=i)
        w = plan_mod.workout_for(plan, d)
        label = "TODAY" if i == 0 else d.strftime("%a")
        extra = []
        if w.get("duration_min"):
            extra.append(f"{w['duration_min']}min")
        if w.get("target_watts"):
            extra.append(f"{w['target_watts']}W")
        if w.get("target_if"):
            extra.append(f"IF {w['target_if']}")
        print(f"{label:6} {d.isoformat()}  {w.get('type','?'):11} {' · '.join(extra)}")
        if w.get("description"):
            print(f"            {w['description']}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="trainingtracker", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="command", required=True)

    sub.add_parser("setup-check", help="verify config + credentials").set_defaults(func=cmd_setup_check)
    sub.add_parser("fetch", help="pull Strava + Oura, analyze into history").set_defaults(func=cmd_fetch)

    b = sub.add_parser("brief", help="today's recommendation from history")
    b.add_argument("--no-coach", action="store_true", help="skip the optional Claude narrative")
    b.set_defaults(func=cmd_brief)

    r = sub.add_parser("run", help="fetch + brief (local one-shot)")
    r.add_argument("--no-coach", action="store_true")
    r.add_argument("--allow-partial", action="store_true",
                   help="still brief from cached data if fetch fails")
    r.set_defaults(func=cmd_run)

    a = sub.add_parser("analyze", help="deep analysis of one workout (default: latest)")
    a.add_argument("--id", type=int, help="Strava activity id (default: most recent)")
    a.set_defaults(func=cmd_analyze)

    rv = sub.add_parser("review", help="longitudinal trends, fitness, and weaknesses")
    rv.add_argument("--weeks", type=int, default=0, help="window in weeks (default: athlete.trend_weeks)")
    rv.set_defaults(func=cmd_review)

    s = sub.add_parser("show-plan", help="print today + upcoming planned workouts")
    s.add_argument("--days", type=int, default=4)
    s.set_defaults(func=cmd_show_plan)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
