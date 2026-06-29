# Progress Log

An append-only record of how the plan and key stats change over time, so the daily routine has
context on progression — and you have a readable history. The routine reads this at the start of
each run and adds a dated entry (in the same PR) whenever it changes a stat or the plan, or notices
a meaningful trend shift. **Newest entries at the top.**

The live config (`config/athlete.yaml`, `config/training-plan.yaml`) always holds current values —
the analysis math needs them. This log is the narrative of *how they got there*.

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
