"""Render the structured assessment into a Markdown briefing and a short
notification summary."""
from __future__ import annotations

from datetime import date
from typing import Any

VERDICT_EMOJI = {"PROCEED": "✅", "MODIFY": "🔧", "PUSH": "🚀", "REST": "😴"}
RECOVERY_EMOJI = {"green": "🟢", "amber": "🟡", "red": "🔴", "unknown": "⚪"}


def _fmt_plan(w: dict[str, Any]) -> str:
    bits = [w.get("type", "?")]
    if w.get("duration_min"):
        bits.append(f"{w['duration_min']}min")
    if w.get("target_watts"):
        bits.append(f"{w['target_watts']}W")
    if w.get("target_if"):
        bits.append(f"IF {w['target_if']}")
    if w.get("target_tss"):
        bits.append(f"{w['target_tss']} TSS")
    line = " · ".join(str(b) for b in bits)
    if w.get("description"):
        line += f"\n  {w['description']}"
    return line


def notification_text(assessment: dict[str, Any]) -> tuple[str, str]:
    v = assessment["verdict"]
    emoji = VERDICT_EMOJI.get(v["verdict"], "")
    title = f"{emoji} {v['verdict']}: {assessment['today_plan'].get('type', 'Training')}"
    rec = assessment["recovery"]
    readiness = rec.get("readiness")
    prefix = f"{RECOVERY_EMOJI.get(rec['status'], '')} readiness {readiness} · " if readiness else ""
    return title, prefix + v["headline"]


def render_markdown(assessment: dict[str, Any], athlete: dict[str, Any], coach: str | None = None) -> str:
    d = date.fromisoformat(assessment["date"])
    weekday = d.strftime("%A")
    v = assessment["verdict"]
    rec = assessment["recovery"]
    load = assessment["load"]
    lw = assessment["last_workout"]

    lines: list[str] = []
    lines.append(f"# 🚴 Training Brief — {assessment['date']} ({weekday})")
    lines.append("")
    lines.append(f"## {VERDICT_EMOJI.get(v['verdict'], '')} Verdict: **{v['verdict']}**")
    lines.append(f"_{v['headline']}_")
    lines.append("")
    for r in v["reasons"]:
        lines.append(f"- {r}")
    lines.append("")

    lines.append("## Today's plan")
    tp = assessment["today_plan"]
    if tp.get("phase"):
        lines.append(f"_{tp['phase']} · week {tp.get('week')}_")
    lines.append(_fmt_plan(tp))
    lines.append("")

    lines.append(f"## Recovery (Oura) — {RECOVERY_EMOJI.get(rec['status'], '')} {rec['status'].upper()}")
    if rec.get("readiness") is not None or rec.get("sleep_score") is not None:
        row = []
        if rec.get("readiness") is not None:
            row.append(f"readiness **{rec['readiness']}**")
        if rec.get("sleep_score") is not None:
            row.append(f"sleep **{rec['sleep_score']}**")
        if rec.get("total_sleep_h") is not None:
            row.append(f"{rec['total_sleep_h']}h slept")
        if rec.get("resting_hr") is not None:
            base = rec.get("resting_hr_baseline")
            row.append(f"RHR {rec['resting_hr']}" + (f" (base {base})" if base else ""))
        if rec.get("hrv") is not None:
            base = rec.get("hrv_baseline")
            row.append(f"HRV {rec['hrv']}" + (f" (base {base})" if base else ""))
        lines.append(" · ".join(row))
        if rec.get("flags"):
            lines.append("")
            lines.append("Flags: " + "; ".join(rec["flags"]))
    else:
        lines.append("_No Oura data for today._")
    lines.append("")

    lines.append("## Last workout vs plan")
    if lw:
        ride = lw["ride"]
        tag = "ZWIFT" if ride.get("is_zwift") else (ride.get("type") or "Ride")
        when = "today" if lw["days_ago"] == 0 else ("yesterday" if lw["days_ago"] == 1 else f"{lw['days_ago']}d ago")
        lines.append(
            f"**{ride.get('name', 'Ride')}** ({tag}, {when}) — "
            f"{ride.get('moving_time_min', '?')}min · "
            f"NP {ride.get('normalized_power', '?')}w · "
            f"IF {ride.get('intensity_factor', '?')} · "
            f"{ride.get('tss', '?')} TSS · "
            f"avg HR {ride.get('avg_hr', '?')}"
            + (f" · decoupling {ride['decoupling_pct']}%" if ride.get("decoupling_pct") is not None else "")
        )
        if ride.get("classified_type"):
            iv = ride.get("intervals") or {}
            extra = ""
            if iv:
                extra = f" · {iv['count']} intervals @ ~{iv['mean_pct_ftp']}% FTP"
                if iv.get("fade_pct") is not None:
                    extra += f", fade {iv['fade_pct']}%"
            lines.append(f"Detected: **{ride['classified_type']}**{extra}")
        lines.append(f"Planned: {_fmt_plan(lw['planned']).splitlines()[0]}")
        if lw["harder_than_expected"]:
            lines.append("⚠️ **Harder than planned** — " + "; ".join(lw["notes"]))
        elif lw["easier_than_expected"]:
            lines.append("ℹ️ Easier than planned — " + "; ".join(lw["notes"]))
        elif lw["notes"]:
            lines.append("Notes: " + "; ".join(lw["notes"]))
    else:
        lines.append("_No rides found in the last 8 days._")
    lines.append("")

    lines.append("## Recent load")
    lines.append(f"7-day TSS **{load['tss_7d']}** · 3-day **{load['tss_3d']}** · {load['rides_7d']} rides this week")
    lines.append("")

    fit = assessment.get("fitness")
    if fit:
        ramp = f" · ramp {fit['ramp_7d']:+}/wk" if fit.get("ramp_7d") is not None else ""
        building = "" if fit.get("ctl_reliable") else " _(building)_"
        lines.append("## Fitness")
        lines.append(f"Fitness (CTL) **{fit['ctl']}**{building} · Fatigue {fit['atl']} · "
                     f"Form (TSB) **{fit['tsb']}** ({fit['form_state']}){ramp}")
        lines.append("")

    focus = assessment.get("focus") or []
    if focus:
        lines.append("## Focus (from your trends)")
        for w in focus:
            lines.append(f"- **{w['area']}**: {w['finding']} → {w['suggestion']}")
        lines.append("")

    lines.append("## Next 3 days")
    for w in assessment["upcoming"]:
        lines.append(f"- **{w['date']}**: {_fmt_plan(w).splitlines()[0]}")
    lines.append("")

    if coach:
        lines.append("## Coach")
        lines.append(coach.strip())
        lines.append("")

    lines.append(f"<sub>FTP {athlete.get('ftp')}w · generated by Training Tracker</sub>")
    return "\n".join(lines)


def _fmt_trend(t: dict[str, Any]) -> str:
    d = t.get("direction")
    if d in (None, "insufficient data"):
        return "insufficient data"
    arrow = {"improving": "↗ improving", "declining": "↘ declining", "flat": "→ flat"}.get(d, d)
    ch = f" ({t['change_pct']:+}% recent vs earlier)" if t.get("change_pct") is not None else ""
    return f"{arrow}{ch}"


def render_workout(record: dict[str, Any], planned: dict[str, Any], athlete: dict[str, Any]) -> str:
    """Deep report for a single workout — classification, metrics, interval table, fade."""
    tag = "Zwift" if record.get("is_zwift") else "Ride"
    lines = [f"# {record.get('name', 'Ride')} — {record.get('date', '')} ({tag})", ""]
    cls = record.get("classified_type")
    plan_note = f"  (planned: {planned.get('type')})" if planned.get("type") else ""
    lines.append(f"**Detected type:** {cls or 'n/a'}{plan_note}")
    lines.append("")
    lines.append("## Metrics")
    lines.append(f"- {record.get('moving_time_min', '?')} min · {record.get('distance_km', '?')} km")
    lines.append(f"- NP {record.get('normalized_power', '?')}w · IF {record.get('intensity_factor', '?')} "
                 f"· {record.get('tss', '?')} TSS")
    lines.append(f"- Avg {record.get('avg_power', '?')}w / max {record.get('max_power', '?')}w · "
                 f"avg HR {record.get('avg_hr', '?')} · EF {record.get('efficiency_factor', '?')}")
    if record.get("decoupling_pct") is not None:
        lines.append(f"- Aerobic decoupling: {record['decoupling_pct']}%")

    iv = record.get("intervals")
    if iv:
        lines.append("")
        lines.append(f"## Intervals ({iv['count']})")
        lines.append("| # | dur | avg W | %FTP | avg HR |")
        lines.append("|---|-----|-------|------|--------|")
        for it in iv["intervals"]:
            mins = f"{it['duration_s'] // 60}:{it['duration_s'] % 60:02d}"
            lines.append(f"| {it['n']} | {mins} | {it.get('avg_power', '-')} | "
                         f"{it.get('pct_ftp', '-')}% | {it.get('avg_hr', '-')} |")
        if iv.get("fade_pct") is not None:
            f = iv["fade_pct"]
            verdict = "held well" if f < 2 else ("mild fade" if f < 5 else "significant fade — struggled late")
            lines.append("")
            lines.append(f"**Fade:** {f}% across reps (first→last {iv.get('first_to_last_pct', '?')}%) "
                         f"— {verdict}.")

    tiz = record.get("time_in_zones")
    if tiz:
        top = [(n, fr) for n, fr in sorted(tiz.items(), key=lambda kv: kv[1], reverse=True) if fr > 0][:3]
        if top:
            lines.append("")
            lines.append("## Time in zone (top)")
            for name, frac in top:
                lines.append(f"- {name}: {round(frac * 100)}%")

    if planned.get("description"):
        lines.append("")
        lines.append("## Planned")
        lines.append(_fmt_plan(planned))
    return "\n".join(lines)


def render_review(review: dict[str, Any], athlete: dict[str, Any]) -> str:
    """Longitudinal review: fitness, per-type trends, volume, weaknesses + adaptations."""
    lines = [f"# 📈 Training Review — last {review['window_weeks']} weeks ({review['date']})", ""]

    fit = review.get("fitness")
    if fit:
        ramp = f" · ramp {fit['ramp_7d']:+}/wk" if fit.get("ramp_7d") is not None else ""
        lines.append("## Overall fitness")
        lines.append(f"- Fitness (CTL): **{fit['ctl']}**{ramp}")
        lines.append(f"- Fatigue (ATL): {fit['atl']}")
        lines.append(f"- Form (TSB): **{fit['tsb']}** — {fit['form_state']}")
        if not fit.get("ctl_reliable"):
            lines.append("- _CTL still building — needs ~6 weeks of data to be accurate._")
        lines.append("")

    tr = review["trends"]
    lines.append("## By workout type")
    th = tr["threshold"]
    lines.append(f"### Threshold — {th['sessions']} sessions")
    lines.append(f"- Power held: {_fmt_trend(th['power_held_pctftp'])}")
    fade_note = f", recent avg {th['avg_fade_recent']}%" if th.get("avg_fade_recent") is not None else ""
    lines.append(f"- Durability (less fade = better): {_fmt_trend(th['durability_fade'])}{fade_note}")
    lines.append(f"- Efficiency: {_fmt_trend(th['efficiency'])}")
    v = tr["vo2max"]
    lines.append(f"### VO2max — {v['sessions']} sessions")
    lines.append(f"- Power held: {_fmt_trend(v['power_held_pctftp'])}")
    vfade = f", recent avg {v['avg_fade_recent']}%" if v.get("avg_fade_recent") is not None else ""
    lines.append(f"- Repeatability (less fade = better): {_fmt_trend(v['repeatability_fade'])}{vfade}")
    z = tr["z2"]
    lines.append(f"### Zone 2 — {z['sessions']} sessions")
    lines.append(f"- Aerobic efficiency (EF rising = base improving): {_fmt_trend(z['aerobic_efficiency'])}")
    zd = f", recent avg {z['avg_decoupling_recent']}%" if z.get("avg_decoupling_recent") is not None else ""
    lines.append(f"- Decoupling (lower = better): {_fmt_trend(z['decoupling'])}{zd}")
    lines.append("")

    vol = review["volume"]
    lines.append(f"## Volume (last {vol['weeks']} weeks) — actual vs planned")
    for t in ("Endurance", "Threshold", "VO2max"):
        lines.append(f"- {t}: {vol['actual'].get(t, 0)} done / ~{vol['planned'].get(t, 0)} planned")
    lines.append("")

    weak = review["weaknesses"]
    lines.append("## Weaknesses & plan adaptations")
    if not weak:
        lines.append("_No clear weaknesses flagged — keep progressing._")
    else:
        icons = {"high": "🔴", "medium": "🟠", "low": "🟡", "info": "🟢"}
        for w in weak:
            lines.append(f"- {icons.get(w['severity'], '•')} **{w['area']}** — {w['finding']}")
            lines.append(f"  → {w['suggestion']}")
    lines.append("")
    lines.append("_In Claude Code, run `/training-review` to turn these into actual plan edits._")
    return "\n".join(lines)
