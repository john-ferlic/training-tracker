# Progress Log

An append-only record of how the plan and key stats change over time, so the daily routine has
context on progression — and you have a readable history. The routine reads this at the start of
each run and adds a dated entry (in the same PR) whenever it changes a stat or the plan, or notices
a meaningful trend shift. **Newest entries at the top.**

The live config (`config/athlete.yaml`, `config/training-plan.yaml`) always holds current values —
the analysis math needs them. This log is the narrative of *how they got there*.

---

## 2026-07-26 — 11-day off-bike gap; 2-week re-entry ramp + retest pushed 7/28 → 8/11

- **Gap (athlete-confirmed):** last ride Wed 7/15 (the clean 2×20 @ 285W SST, 0.0%
  fade, HR 163→167). Nothing 7/16–7/26 — life admin, not injury or illness. **11
  days off** heading into today (Sun 7/26), with the FTP retest originally scheduled
  for Tue 7/28.
- **Recovery held up:** Oura through 7/24 — readiness steady 77–92 (median 83),
  sleep mostly 7+ h, RHR flat 43–46, temperature deviation only a small bump
  7/19 (+0.28) / 7/20 (+0.39) and back to baseline. HRV drifted 76 → 52 across the
  layoff but readiness never flagged — reads as reduced training signal, not illness.
- **Fitness cost:** CTL **31.8** (from ~40+ pre-gap), TSB **+21.3** ("fresh /
  detraining risk"), ramp **-5.9/wk**. Legs will be springy but the pattern is
  lost — HR-for-power and aerobic drift will be off for a session or two, so power
  in reps needs a deliberate step-down before it steps back up.
- **Why 8/11, not 8/04:** first draft of this update pushed the retest by one week
  (to 8/04) and repeated the W6 template. On second look that's too rushed — 11
  days off is closer to a phase-transition-sized layoff than a normal down-week,
  and anchoring a 12+ week Phase-2 block off a low false number is the expensive
  mistake. Pushing to 8/11 costs one week of schedule and buys a full re-entry
  ramp + one W6-template repeat as the calibration check before testing.
- **Plan changes (this PR):**
  - **Phases shifted +2 weeks.** Phase 1 [1,6] → **[1,8]**; Phase 2 [7,12] →
    **[9,14]**; Phase 3 [13,16] → **[15,18]**; Phase 4 [17,20] → **[19,22]**.
    Final test 10/27 → **11/10**. Structure preserved, calendar delayed.
  - **Re-entry ramp — schedule overrides 7/26 → 8/02:**
    - **Sun 7/26** — Endurance **60 min Z2 200–230W** (NO tempo). 44 TSS.
      If HR runs away or legs empty, cut to 45 min easy spin.
    - **Mon 7/27** — Rest (20-min spin fine if stiff).
    - **Tue 7/28** — Endurance **60 min Z2**. 44 TSS. (Was the FTP test.)
    - **Wed 7/29** — SST re-entry: **2×10 @ 275W (~87% FTP)**, 60 min total,
      52 TSS. If end-of-rep-1 HR <162, take rep 2 to 12 min. Deliberately below
      the 7/15 2×20 @ 285W — one step-back rep before rebuilding.
    - **Thu 7/30** — Endurance **60 min Z2**. 42 TSS.
    - **Fri 7/31** — Full rest.
    - **Sat 8/01** — Long ride re-entry: **120 min Z2** (not 180), NO tempo.
      87 TSS. Fuel per the 7/10 rule (~2 g/kg pre + 60–90 g/hr on-bike).
    - **Sun 8/02** — Endurance **60 min Z2**. 42 TSS.
    - Re-entry week total: ~311 TSS vs the W6 template's ~440 TSS — about 70%.
  - **Week of 8/03 — normal Phase 1 W6 template** (no overrides). SST Wed 8/05
    back to **2×15 @ 285W** (one rep below the 7/15 2×20 — proves the top of the
    ladder is back before testing). Long Sat 8/08 = 180 min. If that week
    executes clean (decoupling <5% at proper fueling, SST 0% fade), test 8/11
    is honest.
  - **Test Tue 8/11** — 20-min × 0.95 or ramp. Re-anchor watt targets after.
- **Watches (in priority order):**
  1. **Wed 7/29 SST HR/fade** — first hard data point. HR climbing >167 at
     end of rep 1 at 275W or fade >2% means still detrained; push next week's
     8/05 SST down to 2×15 @ 280W instead of 285W.
  2. **Sat 8/01 long-ride decoupling** — >5% at proper fueling = aerobic base
     didn't fully hold; slide the test one more week to 8/18.
  3. **HRV recovery** — the 76 → 52 drift across the gap should reverse in the
     first week back if the read was accurate (reduced-signal, not illness).
     If HRV keeps dropping *while* training resumes, that's the illness flag
     the temp-dev bump didn't catch — pause and reassess.

---

## 2026-07-10 — Wed 7/08 SST banked as 2×20 @ 285W (0% fade); ladder restored

- **In-session upgrade earned:** Wed 7/08 SST executed clean at **285W / 90% FTP** with
  interval 1 = 16:51 (HR 158) → interval 2 = 19:52 (HR 160), fade **0.0%**, mean 90% FTP.
  Per the 6/29 rule ("if interval #1 finishes with HR <165, take #2 to 20 min") the athlete
  bumped rep 2 to 20 min. That's a **de-facto 2×20 banked six weeks before the 7/28 retest**.
- **Ladder restored:** the 7/01 miss had trimmed the pre-retest 2×20 count from 3 → 2.
  With 7/08 now effectively a 2×20 rep, the revised ladder is
  **7/08 (~2×20 upgrade) → 2×20 on 7/15 → 2×20 on 7/22 → retest 7/28** — three 2×20s under
  the 317 anchor again. Retest confidence back to the 6/29 baseline.
- **Aerobic-cost trend confirmed:** same 285W, lower HR — 6/24 SST intervals HR 163→167,
  7/08 SST intervals HR 158→160. -5 bpm at the same power over two weeks. Central adaptation
  still tracking the direction the 7/03 log flagged.
- **New watch — pre-ride fueling (not durability):** Thursday 7/09 endurance ran hot on
  paper (NP 227w / IF **0.717** vs 0.65, decoupling **5.5%**) but the athlete confirmed the
  ride was essentially fasted. That reframes the read cleanly:
  - 7/05 short endurance was *harder* — IF **0.736** — but decoupling was **0.4%**. If
    aerobic base were the issue, 7/05 should have looked worse; the delta is fueling.
  - 5.5% decoupling on an 80-min fasted Z2-upper is textbook back-half glycogen drop,
    not an aerobic under-adaptation signal.
  - Efficiency factor 1.658 says HR-for-power stayed strong overall — the drift was in
    the tail, consistent with running out of on-board fuel.
  So the signal is **fueling discipline**, not durability. Rule: **carb-load before any
  Z2 ride ≥60 min**, and 60–90 g/hr on-bike for the Saturday long ride and any Wednesday
  SST. If a Thursday endurance IF overshoot repeats *with* proper fueling, then dial the
  trainer target down to 210W — but don't treat well-fueled effort creep and fasted
  decoupling as the same problem.
- **Focus:** protect Saturday 7/11 long ride (180 min, 130 TSS — the week's biggest lever)
  with **~2 g/kg carbs in the 2 hr pre-ride + 60–90 g/hr on-bike**. Execute the 7/15 SST
  at 2×20 without a further bump. No plan or FTP change.

---

## 2026-07-03 — Wed SST missed; Z2 durability trending sharply better

- **Missed session:** Wed 7/01 SST (planned 2×17 @ 285W progression) — no ride logged.
  Rest of the week was on plan (Tue 90-min Z2, Thu 80-min Z2).
- **Progression impact:** original 6/29 plan was 2×17 → 2×20 → 2×20 → 2×20 → retest 7/28
  (three 2×20 sessions banked). With 7/01 skipped, revised ladder is
  **2×17 on 7/08 → 2×20 on 7/15 → 2×20 on 7/22 → retest 7/28** (two 2×20s banked).
  Retest confidence slightly reduced but the 317 anchor still tests cleanly with two
  full 2×20 reps under it. Do NOT jump straight to 2×20 on 7/08 to catch up — the
  step from 2×15 to 2×20 without an intermediate is where SST progressions blow up.
- **Aerobic durability trend (positive):** Z2 decoupling has walked down over the last
  five endurance rides — **7.7% → 5.6% → 2.7% → 4.5% (long) → 3.1% → 2.7% → 0.7% → -0.2%**
  (7/02: 80 min, NP 225w / 71% FTP, HR 135, decoupling -0.2%). HR at the same NP is
  falling: 6/17 endurance was NP 210 @ HR 138; 7/02 was NP 225 @ HR 135. That's the
  Phase 1 central adaptation showing up — the aerobic engine is holding power with
  less cardiac cost.
- **Focus stays:** protect Saturday's 180-min long ride (biggest weekly stimulus) and
  execute the 2×17 on Wed 7/08 cleanly. No junk volume to "make up" the missed SST.

---

## 2026-06-29 — Wed SST calibration fixed; FTP 317 anchor confirmed

- **Plan change:** Phase 1 Wednesday SST — `target_if` 0.82 → **0.74**, `target_tss` 78 → **65**.
  The old numbers were calibrated for the 2×20 endpoint of the "build toward 2×20" progression,
  not the 2×15 starting structure. With a clean 2×15 @ 285W and a proper WU/CD, overall IF
  lands ~0.72–0.74 and TSS ~60–65 — which the briefing was mis-grading as "under-target."
  Note in the file says to step the targets to IF 0.78 / TSS 72 once built to 2×20.
- **FTP 317 confirmed by interval data, not just overall NP:**
  - 6/24 SST (`Zwift - SST`): 2×14:50 @ **285W / 90% FTP**, fade **0.0%**, HR 163→167
    (drift 4 bpm, sustainable). Textbook execution.
  - 6/18 SST: intervals also at **285W**, max interval power 285, mean %FTP 90, fade 0.0%.
  - Earlier read of "FTP probably ~310" based on overall ride NP/IF was wrong — overall NP
    is dragged down by WU + recovery + CD math, not by soft execution. Withdrawn. Anchored
    FTP stays at 317 through the scheduled 7/28 retest.
- **Decoupling 13.4% on 6/24 was a structural artifact** (long low-power CD pulls the
  back-half Pw:Hr down vs. front-half). Within-interval HR drift was only ~2.5%. Not a
  durability flag for this ride shape.
- **Wed 7/01 prescription:** step to **2×17 @ 285W** (in-session upgrade rule: if interval
  #1 finishes with HR <165, take #2 to 20 min). Then full 2×20 the following Wednesday,
  three 2×20 sessions banked before the 7/28 retest.

---

## 2026-06-24 — baseline

- **Stats:** FTP **317 W** · max HR **197** · resting HR **44** · weight **79 kg**.
- **Plan:** 20-week pyramidal build — Phase 1 (Aerobic Base), week 2 of 6. Next FTP retest at the
  start of Phase 2 (2026-07-28).
- **Recent reads:**
  - Threshold/sweet-spot holding power well — ~0% fade across SST blocks on recent sessions.
  - Aerobic durability (Z2 decoupling) is the early watch-item — the long Saturday Z2 is the lever.
  - `resting_hr` synced 48 → 44 from the Oura median (was a placeholder).
- **Focus:** execute Phase 1 cleanly (consistent Z2 + the long ride); don't add junk volume.
