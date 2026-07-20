# Progress Log

An append-only record of how the plan and key stats change over time, so the daily routine has
context on progression — and you have a readable history. The routine reads this at the start of
each run and adds a dated entry (in the same PR) whenever it changes a stat or the plan, or notices
a meaningful trend shift. **Newest entries at the top.**

The live config (`config/athlete.yaml`, `config/training-plan.yaml`) always holds current values —
the analysis math needs them. This log is the narrative of *how they got there*.

---

## 2026-07-20 — 4-day unplanned rest (Thu–Sun) mid-taper; autonomic watch on

- **Missed sessions:** last logged ride was Wed **7/15 SST**. Thu 7/16 (Z2 75'/52 TSS),
  Sat 7/18 (long Z2 180'/130 TSS) and Sun 7/19 (Z2+tempo 90'/72 TSS) were all skipped.
  That's **254 TSS not banked**, including the week's biggest aerobic stimulus (Saturday
  long ride). 7-day TSS 136 · 3-day 0 · form (TSB) 8.2 — plenty fresh, but the aerobic
  stimulus for week 6 is gone.
- **Wed 7/15 SST was clean:** 2×19:51 @ **285W / 90% FTP**, fade **0.0%**, interval HR
  163→167 (drift 4 bpm within reps — sustainable). Overall NP 246 / IF 0.777 / TSS 89
  reads "harder than planned" on the briefing rule, but that's the same structural
  artifact as 6/24: the 8.0% overall decoupling is dragged by long low-power CD/recovery
  pulls, not by within-interval drift. Under the 2×20 progression the calibrated target
  is IF 0.78 — this session hit it. Second 2×20 banked.
- **Autonomic signals worth watching, not acting on:** HRV has walked down the last
  five mornings — 63 (7/15) → 58 → 76 → 52 → 53 → **54** today (base 61, so today is
  ~11% low, right at the threshold). Body-temperature deviation flipped positive and
  climbed: -0.29 (7/17) → -0.08 → +0.28 → **+0.39** today. Readiness held (81), sleep
  fine (86, 8.5h), RHR 44 = base 43. Pattern is more "mild systemic load / could be
  pre-illness / heat / life stress" than a clear red flag. Not enough to modify a
  30-min recovery spin, but the direction matters this close to retest.
- **Retest ladder — Wed 7/22 is now the anchor session.**
  Pre-retest 2×20s banked: 7/08 (upgrade) ✓ · 7/15 ✓ · **7/22 pending** · retest 7/28.
  With the weekend gone, this Wednesday's 2×20 @ 285W is the last confirmation rep
  under the 317 anchor. Do NOT try to "make up" the Saturday long ride mid-week —
  that would jeopardize 7/22.
- **This week's execution:**
  - **Mon 7/20** — per plan: 30 min genuine recovery.
  - **Tue 7/21** — Z2 90' / IF 0.66 as planned; if HRV/body-temp still off tomorrow
    AM (HRV <55 or temp >+0.3), drop to 60' Z2. Do not push the tempo end.
  - **Wed 7/22** — the key session. Full **2×20 @ 285W** as planned. If the athlete
    wakes up with obvious illness signs, defer 24 h and let the retest slide a day —
    do not execute this session sick.
  - **Thu–Sun** — plan as written. No compensatory volume for the missed weekend;
    residual TSB helps the retest.
- **Focus:** protect Wed 7/22 2×20. Sanity-check body temp / HRV tomorrow morning
  before Tuesday's Z2.

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
