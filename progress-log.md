# Progress Log

An append-only record of how the plan and key stats change over time, so the daily routine has
context on progression — and you have a readable history. The routine reads this at the start of
each run and adds a dated entry (in the same PR) whenever it changes a stat or the plan, or notices
a meaningful trend shift. **Newest entries at the top.**

The live config (`config/athlete.yaml`, `config/training-plan.yaml`) always holds current values —
the analysis math needs them. This log is the narrative of *how they got there*.

---

## 2026-08-29 (post-ride) — **Durability limiter is resolved. Sub-6% gate MET. Same-power HR is down 16 bpm in three weeks.** Plan change proposed, not yet applied — awaiting athlete decision.

- **Today's ride is a near-perfect controlled repeat of 8/08** — same 3×12 @ **249W**, same NP
  (**217 vs 217**), same IF (**0.678 vs 0.677**), 165 vs 159 min. So this is a clean read, not a
  trend line across drifting conditions:

  | | 8/08 | 8/29 | Δ |
  |---|---|---|---|
  | Tempo block HR @ 249W | 156 / 159 / 163 | **141 / 142 / 141** | −15 / −17 / **−22** |
  | Block-3 − block-1 drift | **+7 bpm** | **0 bpm** | −7 |
  | Whole-ride avg HR | 147 | **131** | **−16 bpm** |
  | Efficiency factor | 1.471 | **1.653** | **+12.4%** |
  | Decoupling | 9.8% | **5.7%** | −4.1 pts |

- **The durability series is complete and flat:** **+7 (8/08 @ 249W) → +2 (8/15 @ 244W) → −1
  (8/22 @ 244W) → 0 (8/29 @ 249W)**, fade 0.0% on all four. EF across the same four:
  **1.471 → 1.563 → 1.632 → 1.653**. Durability has been the standing limiter since 7/12; on this
  evidence **it is no longer the limiter.**
- **Pre-committed gate is MET.** Phase 3 Saturday was held at 165 min "until two consecutive long
  rides come in under 6%" decoupling: **8/22 3.8%** and **8/29 5.7%**. Both under. Note honestly
  that 5.7% is a *marginal* pass and higher than 8/22's, at slightly higher power (213W vs 208W
  avg) — but the cleaner same-power metric (block drift 0 bpm) is unambiguous, and the gate is
  read on decoupling as written.
- **NOT applied yet, deliberately.** The athlete has said he does not value long-ride performance
  for its own sake, which makes this a bigger question than the mechanical gate: it reopens
  whether the *Phase 2* Saturday should also come down from 165, and whether freed minutes are
  better spent as threshold volume. That interacts with **Tue 9/01**, which is the validation of
  the provisional FTP 320 — restructuring the week before that read would be premature. Proposal
  on the table: Phase 3 Sat **165 → 135** (gate, mechanical); Phase 2 Sat **165 → 135** with the
  3×12 tempo retained (goal-driven, needs athlete sign-off). Revisit 9/01.
- **Load recovered from the trough in one session:** 7-day TSS **182 → 309**, CTL **41.2 → 44.3**,
  ramp **−2.8 → +0.3/wk**, TSB **−10.5** (productive overload). Sun 8/30 stays at 90 min; Mon rest
  puts Tuesday at roughly **TSB −2**.
- **Next limiter, provisionally: time at 95-105% FTP.** With durability resolved and Z2 volume
  clearly working, the constraint on FTP from here is more likely weekly threshold minutes
  (currently ~85 min across Tue + Thu) than more aerobic volume. Do not act on this before 9/01.
- **Supporting evidence — the August EF gain does not track Z2 volume.** Weekly Z1-2 hours against
  the long-ride EF they preceded, and weekly Z4-5 minutes:

  | week of | Z1-2 hrs | Z4-5 min | total hrs | TSS | → long-ride EF |
  |---|---|---|---|---|---|
  | 6/29 – 7/13 | 4.2 / 6.6 / 1.9 | **0** | 4.5 / 7.2 / 2.6 | 226 / 353 / 133 | — |
  | 8/03 | 5.2 | 23 | 6.6 | 290 | 1.471 (8/08) |
  | 8/10 | **5.8** | 54 | 7.7 | 378 | 1.563 (8/15) |
  | 8/17 | 4.3 | **58** | 6.3 | 333 | 1.632 (8/22) |
  | 8/24 | **4.2** | 36 | 5.7 | 309 | **1.653 (8/29)** |

  Z1-2 volume went **5.8 → 4.3 → 4.2 hrs** across the exact window EF rose **1.563 → 1.653**.
  What was *added* over that period was threshold work: **0 min of Z4-5 in all of June/July**,
  then 23 → 54 → 58 → 36. Sub-maximal 20-min bests over the same span: **285W (7/15) → 305W
  (8/18) → 313W (8/27)**.
- **Recovery cost by session type — next-morning Oura, grouped by the preceding day.** Relevant to
  any decision to trade Saturday Z2 minutes for threshold minutes:

  | preceding session | n | mean TSS | → next-morning readiness | HRV | RHR | sleep score |
  |---|---|---|---|---|---|---|
  | Short Z2 | 12 | 55 | **85.8** | 64.2 | 43.6 | 84.8 |
  | Threshold / VO2 | 7 | 73 | **82.3** | 58.7 | 44.0 | 81.6 |
  | Long Z2 (≥115 min) | 6 | 122 | **78.2** | 58.0 | 45.7 | 82.2 |

  **Per session, the long rides have cost more next-morning recovery than the threshold sessions**
  (readiness 78.2 vs 82.3) — the opposite of the usual "Z2 is recovery-cheap" intuition. Sleep
  scores are near-identical across groups (82.2 vs 81.6), so this is not a weekend-sleep artifact.
  **Per unit of TSS the ordering reverses**, as theory expects: measured against the Short-Z2
  baseline, threshold costs ≈ **0.19 readiness points per TSS** above baseline vs ≈ **0.11** for
  long Z2, i.e. roughly **1.7× per TSS**.
  *Caveat:* n=6/7, and the two worst long-ride mornings (**8/01** — ready 78, HRV 41, RHR 49, five
  days after the 11-day gap; **8/08** — ready 69, HRV 51, RHR 50, the 9.8%-decoupling ride) both
  come from the de-trained / poor-durability period. Excluding them, long-ride mornings average
  readiness **80.5**, HRV **64**, RHR **43.8** — i.e. the long-ride recovery cost has been falling
  as durability resolved, and the gap vs threshold is probably smaller now than the table shows.
- **Arithmetic on the proposed swap.** 30 min of Z2 at IF 0.66 ≈ **22 TSS**; 30 min at threshold
  (IF ≈ 0.98) ≈ **48 TSS**. Swapping one for the other is **+26 TSS and ~2.2× the load per
  minute**, not a wash — and TSS understates it, since it captures neither glycogen depletion nor
  autonomic load. A **TSS-neutral** version of the same trade: cut Saturday 30 min (−22) and add
  ~9 min of threshold (Tue 3×15 → 3×18, +15). That is the version to propose after 9/01.
- **Confounds, stated so this isn't over-read.** n=4, observational, and three real problems:
  (a) the **11-day gap (7/16-7/26)** means the 8/08 reading was partly de-trained, so some of the
  early gain is re-acquisition, not new adaptation; (b) total volume fell alongside Z2 (7.7 → 5.7
  hrs), partly the 8/25 test taper, so "less Z2" and "less everything" are not separable here;
  (c) EF is HR-based and moves with heat, fuelling and fan placement. **This does not show Z2 is
  unnecessary** — the August threshold block was built on a June/July base of 4-7 h/wk that was
  essentially all Z1-2. It shows only that *at this athlete's current 6-8 h/wk, the marginal
  aerobic hour is not where the return is.*

---

## 2026-08-29 — **Test-week load trough (7-day TSS 182, CTL 41.2). And: stop reading whole-ride decoupling on the Thursday over-unders.** No config change.

- **No stat or plan edit.** `sync-profile` clean — FTP 320, max HR 197, RHR 44, weight 79 all
  current. Today's session (Sat 165 min, 3×12 tempo @ 245-250W) is ridden as written; it is the
  second data point on the sub-6% durability gate.
- **Load trough, by design but worth naming.** Week of 8/24 is **182 TSS / 3 rides**, against
  **378** (8/10) and **333** (8/17) — the lightest week since the July gap. Cause is the test
  block: 8/23 and 8/24 off, the 8/25 ramp itself only **38 TSS**, 8/28 rest. CTL has slid
  **43.2 → 41.2** with a ramp of **−2.8/wk**; TSB **+4.6**. Today's 135 TSS is the week's biggest
  single stimulus and is what arrests that slide (projects CTL **43.4**, TSB **−7.3** tonight,
  back to **≈ −2** by Tuesday morning). *Do not trim volume this week* — the freshness argument
  that justified the 8/23 Sunday trim before the test does not apply now, and the athlete is
  already under-loaded. Sunday 8/30 stays at 90 min.
- **Correction: whole-ride decoupling is not a readable fatigue signal on over-under sessions.**
  The brief flagged 8/27 "harder than planned" on **11.7%** decoupling. On intensity it was not
  hot at all: **IF 0.881 vs 0.88 planned, TSS 91 vs 95**, overs **8 × 338W with 0.0% fade**.
  The decoupling number on this session type does not track intensity — **8/13 12.0% (NP 262) →
  8/20 6.1% (NP 271) → 8/27 11.7% (NP 282)** — because a sawtooth power profile plus warm-up and
  cool-down breaks the first-half/second-half EF comparison. Same class of artifact as the 8/20
  tempo-detection note: **do not re-derive fatigue from it.**
- **The readable number on this session is rep-to-rep HR at held power**, and it is healthy:
  **8/20 rep1 164 → rep2 168 bpm at 300W blended (+4)**; **8/27 rep1 164 → rep2 171 bpm at 312W
  blended (+7)**. The extra drift is the 12W (+4%) step in power, not fatigue — ride max HR
  **181 vs 197**, i.e. 16 bpm of headroom, and whole-session **EF is climbing at rising power:
  1.752 → 1.783 → 1.869**.
- **Read-ahead for 9/01 (the 320 validation).** 8/27's rep 2 averaged **171 bpm at 312W blended**
  with a last-over peak of **178**. A steady 3×15 @ 320W will sit above that, so the pre-committed
  "last-rep HR ≤ 175" line is the criterion most likely to be the one that bites — expect the
  power criterion (hold 318-322W, fade ≥ −2%) to pass more comfortably than the HR one. Judge the
  two together rather than failing the anchor on HR alone.
- **Recovery is green and improving off the 8/28 dip.** Readiness **86** (78 yesterday), HRV
  **67** vs 30-day mean **62**, RHR **43** vs base 44, temp **+0.04**. Softest input is sleep —
  **7.03 h, score 78**, the shortest of the last five nights, well clear of the 70 flag.

---

## 2026-08-28 — **FTP 305 → 320 from the 8/25 ramp. Phase 2/3/4 watt targets re-anchored. Durability series now negative.**

- **The 8/25 retest was ridden but never applied.** The test happened on schedule, and then three
  days of training ran on the stale 305 anchor. `sync-profile` reported "no stat changes" and will
  keep doing so: it reads FTP only from the **Strava profile field**, which wasn't updated after
  the test. That is a blind spot worth knowing about — *a completed FTP test will never surface
  through `sync-profile` unless you also set the new number in Strava.*
- **Stat change — `ftp: 305 → 320`** (+15W, +4.9%; **3.86 → 4.05 W/kg** at 79 kg).
  - Source: **8/25 Zwift ramp test**, 33.1 min. **Best 1-min 426W**; Zwift ramp FTP = 0.75 × 426 =
    **319.5 → 320**. Final ramp step 8:27 @ 352W avg, HR 175, ride max HR **187** (vs 197 max —
    no max-HR change, and nothing above 187 since May).
  - **Provisional, and flagged as such in both configs.** The 8/20 entry specified *20-min ×0.95*
    because the ramp has historically **under**-read for this rider (8/04 ramp said 305 while the
    8/18–8/20 sessions pointed at 315-322). A ramp was ridden instead. If the historical bias
    holds, 320 is a floor rather than a ceiling.
  - **Corroboration — the athlete was already self-anchoring above 305.** On 8/27 he rode the
    over-unders at **296W under / 338W over** against a prescription of 280/320. Those are within
    1-2W of the FTP-320 re-anchored numbers (295/336). He has been training at ~322 for a week.
  - **Sub-maximal 20-min bests keep climbing:** 7/15 **285W** → 8/18 **305W** → 8/27 **313W**.
    40-min: 7/15 **275W** → 8/18 **284W** → 8/27 **295W**. None of these were max efforts; 8/27's
    313W came inside a prescribed session that finished 16 bpm under max HR. They are floors.
- **Plan change — Phase 2, 3 and 4 watt targets re-anchored to 320.** `target_if` and `target_tss`
  are FTP-relative and are unchanged, so the intended stimulus is identical; only the watt numbers
  move. Phase 1 and the 7/26-8/02 re-entry entries are left at their historical values.
  - Z2 band **195-225 → 205-235** across all three phases.
  - P2 Tue threshold **290-305 → 305-320**; the deferred **3×15 is now 3×15 @ 320W on Tue 9/01**.
  - P2 Thu over-unders **280/320 → 295/336**. Not a step up — see above, he rode 296/338 on 8/27.
  - P2 Sat tempo **230-275 → 245-288**, *with an explicit instruction to keep riding the blocks at
    245-250W.* The band moved; the session should not. See the durability series below.
  - P3 Tue VO2 **325-350 → 340-368**; P3 Thu 30/15s **345/195 → 362/205**.
  - P4 Tue **"98-100% FTP (re-anchor)" → 314-320**; P4 Thu **280/320+ → 295/336+**.
- **9/01 is the validation gate for the 320 number.** Written into the Tuesday entry: three reps
  held at **318-322W**, fade ≥ **−2%**, last-rep HR ≤ **175** ⇒ 320 is real. If rep 3 falls under
  **310W**, or HR passes **180** by mid-rep-2, the anchor is high and comes back to ~313.
- **History re-analysed at the new anchor** (`fetch --reanalyze`), so TSS/IF are consistent across
  the whole 56-day window rather than splicing two anchors. This restates the fitness numbers
  downward — **CTL 47.6 → 43.2, ATL 47.1 → 42.7, 7-day TSS 331 → 300** — which is arithmetic, not
  lost fitness: the same work divided by a bigger FTP. TSB is unchanged at **+0.5**.
- **Trend shift: the durability series went negative, three weeks running.** Same power, same
  session, block-3 HR minus block-1 HR: **8/08 249W → +7 bpm**, **8/15 244W → +2 bpm**,
  **8/22 244W → −1 bpm** (142/141/141, fade 0.0%). This is the standing limiter and it is
  resolving. Whole-ride decoupling on the same three rides: **9.8% → 8.0% → 3.8%**.
- **Live gate for Sat 8/29.** Phase 3's Saturday is held at 165 min "until two consecutive long
  rides come in under 6%" decoupling. 8/22 was **3.8%** — the first. **If 8/29 also comes in under
  6%, that gate is met** and Phase 3 Saturday can drop 165 → 135 min. Ride 8/29's tempo blocks at
  **245-250W**, not the new 288W ceiling, or the comparison is broken and the gate can't be read.
- **8/23 and 8/24 were both taken off** ahead of the test — the trimmed 60-min Sunday wasn't
  ridden. Extra freshness into 8/25; noted in the schedule entry so it isn't read as missing data.
- **Recovery today is the softest point of the block, mildly.** Readiness **78**, sleep **80**,
  **7.24 h**, RHR **45** vs base 44, HRV **53** vs base 61 (**−13%**, just past the 12% flag).
  HRV has been ≤60 on 4 of the last 6 days (51/53/60/67/53). Today is a scheduled rest day and
  that is the right call — no change proposed.

---

## 2026-08-22 — **Trend shift: the Saturday tempo blocks now have a clean durability number, and it is improving fast.** No config change.

- **No stat or plan edit.** `sync-profile` clean — FTP 305, max HR 197, RHR 44, weight 79 all
  current. The plan needs no touch either: with Saturday at 165 min (135 TSS) and Sunday at the
  trimmed 60 min (42 TSS), Tuesday's retest projects to **CTL 46.1 / ATL 44.3 / TSB +1.8**. The
  8/20 Sunday trim already bought the freshness; cutting further (Sun 60 → 40 min) would move the
  test to TSB +2.9, which does not change a 20-min effort for a rider who set a 40-min best of
  283W at TSB −11. Saturday stays whole — it is the durability session.
- **New metric, courtesy of the 8/20 detection fix.** The Saturday 3×12 tempo blocks are now
  detected, so for the first time there is a same-power, artifact-free durability read:
  - **8/08** — 3×12 @ **249W**, HR **156 / 159 / 163** → **+7 bpm** across the three blocks.
  - **8/15** — 3×12 @ **244W**, HR **143 / 144 / 145** → **+2 bpm** across the three blocks.
  - Fade **0.0%** on both. Absolute tempo HR fell **13 bpm for −5W**; whole-ride EF **1.471 →
    1.563** at 209W → 206W. That is a large durability gain in one week.
- **Whole-ride decoupling on the Saturday ride is not a clean read — use the intra-block drift
  instead.** 9.8% → 8.0% against the 6.0% flag looks red, but a 165-min ride with three back-half
  tempo blocks inflates the first-half/second-half Pw:HR comparison by construction — the same
  artifact class already documented for the over-unders on 8/13 and 8/20. **Block 3 HR minus
  block 1 HR at held power is the durability number to track on this session.** Do not re-derive
  a fatigue verdict from whole-ride decoupling here.
- **Focus for today's session:** repeat **244-250W** on the tempo blocks rather than riding the
  275W top of the prescribed band, so 8/22 is a clean third datapoint on the same scale instead
  of a new stimulus three days before the test. Read: **≤ +3 bpm** block 1 → block 3 = the trend
  holds; **≥ +6 bpm** = under-fuelled, and Sunday gets trimmed further.
- **Recovery is the best of the block and load is not limiting.** Readiness **91**, sleep **84**,
  **7.79 h**, RHR **41** vs base 44, HRV **68** vs base 61. 7-day TSS **295** (flag 450), CTL
  **45.3**, ATL **44.1**, TSB **+1.2**, ramp **−0.7/wk** — the intended pre-test unload, working.
- **8/20's 6.1% decoupling flag: ignore, as pre-committed.** Interval-shaped ride, eight recovery
  valleys, 0.0% fade across the overs, ride max HR 177 vs 197. Same rule limitation as 8/13.

---

## 2026-08-20 (evening) — **The gate fired on all three. FTP retest moves 9/08 → Tue 8/25.**

- **The session was ridden, complete, and above prescription.** 2 sets × 4×(3 min under / 2 min
  over), **19:53 + 19:56 = 39:49** of work, no unplanned stops. Every target overshot: **unders
  286W** (vs 280), **overs 322W** (vs 320), **blend 300W** (vs 296). NP 271, IF 0.888, 92 TSS,
  EF 1.783.
- **Gate result — all three criteria met:**
  1. Full 40 min as 2 sets, no stops ✅ (39:49, 8 overs + 8 unders)
  2. Last over of set 2 at HR ≤175 ✅ (**175** exactly, peak 177)
  3. Fade ≥ −2% ✅ (**0.0%** overall, **0.0%** across the overs, first→last 0.6%)
- **Against the HR spec written this morning, it landed almost exactly on prediction.** Set 1 avg
  **164** (predicted 160-166), peak **173** (predicted ≤174). Set 2 avg **168** (predicted 165-171),
  peak **177** (predicted ≤178). The 182 abort line was never approached.
- **Clearance held throughout.** Every under after the first shed HR — set 1 **−2 / −5 / −4**,
  set 2 **−4 / −2 / −5**. Never two consecutive unders under 3 bpm. 286W is comfortably a
  recovery valley for this rider.
- **This is the session that failed twice, now passed at higher power.** vs **8/13**, one week
  earlier: set 1 **295W → 300W** at HR **167 → 164** (+5W, **−3 bpm**), peak **178 → 173**, and a
  complete set 2 where 8/13 managed 15:44 of 20:00. vs **8/06**: peak HR **189 → 177** (96% → 90%
  of max) for a *harder* session.
- **New 40-min best territory, two days after the last one.** Best 40-min power: pre-gap 7/15
  **275W** → 8/18 **284W** → 8/20 **283W**. Best 20-min: 7/15 **285W** → 8/18 **305W** → 8/20
  **301W**. Note these are prescribed sessions, not max efforts — they are floors, not ceilings.
- **The overs sat at 106% of the 305 anchor and did not fade at all** (322/323/323/321/323/323/
  323/321). 16 minutes above threshold, dead flat, finishing 20 bpm under max HR. Against FTP 305
  that is not plausible; against ~318 it is exactly right.
- **Plan changes (this PR):**
  - **Retest moved 9/08 → Tue 8/25**, replacing the 9/08 slot entirely. Rationale written into
    the schedule entry.
  - **Tuesday's 3×15 @ 305 deferred to 9/01** and must be re-anchored to the tested FTP first
    (~3×15 @ 318 if the test lands where the evidence points).
  - **Sunday 8/23 trimmed 90 → 60 min** purely to freshen for the test — projected TSB **+1.4**
    at 90 min vs **+3.2** at 60. Saturday stays at 165 min; the durability session is not the one
    to cut.
- **Load is now the thing to watch, not recovery.** CTL **49.0** (was 46.8 this morning), ATL
  **60.0**, TSB **−11.0**, ramp **+2.3/wk** (was +0.1). 7-day TSS **427** against the 450 flag,
  5 rides this week. Projected 7-day through 8/22 is ~430 — under the flag but the first genuinely
  loaded week of the block. The Fri rest / trimmed Sun / Mon rest sequence is what keeps 8/25 usable.
- **Decoupling 6.1% tripped the "harder than planned" rule and should be ignored here.** It is an
  interval session with eight recovery valleys; the whole-ride first-half/second-half Pw:HR
  comparison is not meaningful on that shape — the same artifact documented for 8/13. Interval HR
  and fade both say the opposite. This is a limitation of the rule, not a signal about the ride.
- **Classifier now reads this session as VO2max** (19% of time in Z5) rather than Threshold. That
  is correct against a 305 anchor — the overs are 106% FTP. It should revert to Threshold once
  FTP is re-anchored, which is itself a sign the anchor is wrong.

---

## 2026-08-20 — Thursday over-unders are the FTP-anchor diagnostic; the "capped and clean" gate gets numbers

- **No config changes today.** `sync-profile` clean — FTP 305, max HR 197, RHR 44, weight 79 all
  current. No plan edit either: the 8/18 pre-commitment to leave Thursday's targets *as written*
  is precisely what makes today a valid test, so touching the watts would destroy the datapoint.
  This entry exists to carry the decision rule forward to the next run.
- **Recovery: a one-night dip, already gone.** 8/19 was the week's only red number — readiness
  **73**, sleep **69**, **5.85 h**, RHR **46**. Today: readiness **89**, sleep **88**, **8.25 h**,
  RHR **44** (= base), HRV **61** vs base 62; hrv_balance contributor 92, recovery_index 100.
  Nothing carried over.
- **Tuesday was absorbed.** The 8/18 threshold session (90 TSS, IF 0.876) was followed by 8/19
  easy Z2 at **197.6W / HR 126 / EF 1.580 / decoupling 0.4%** — in line with the 8/16 benchmark
  (200W / HR 124 / EF 1.630). No HR drift at Z2 two days after the best threshold work on record.
- **Load is neutral, not limiting.** CTL **46.8**, TSB **−0.1**, 7-day TSS **335** (flag 450),
  3-day **144**, ramp **+0.1/wk**. Room to work; Friday is a full rest day before Saturday's
  165-min durability session, which stays the protected session of the week.
- **Detector caveat — read this before judging any over-under session.** `work_frac_ftp` 0.88 ×
  FTP 305 = **268W**, and the prescribed *unders* are 280W (92% FTP). Both unders and overs sit
  above the work threshold, so a correctly-ridden set of 4×(3 min @ 280 / 2 min @ 320) is
  detected as **one continuous ~20:00 interval at the blended average of 296W**, not as eight
  reps. Eight short reps in the table would mean the session was ridden *wrong*. Prior runs read
  the single long interval as a failure to follow the structure; it is the opposite.
- **Re-reading the two prior attempts, this changes the record.**
  - **8/06 was never this session.** "Zwift - At/Over/Under" is a stock workout: 3×**8:53 @ 303W**,
    HR **167 → 175 → 179**, max HR 189, **18% of time in Z5**, decoupling 7.9%. Nine-minute blocks,
    not 3/2 — and ridden two days after the 8/04 ramp test. It tells us nothing about the
    prescribed over-under and should stop being counted against it.
  - **8/13 set 1 was textbook.** **19:55 @ 295W** against a prescribed 20:00 @ **296W** blended —
    within 5 seconds and 1 watt — at HR **167**, ride max power 374W (the overs were hit).
  - **8/13 set 2 is where it broke:** 8:03 + 4:25 + 3:16 = **15:44 of 20:00 (79%)**, in three
    pieces. But the set-2 HRs were **167 / 165 / 165** — flat-to-lower than set 1, not drifting.
    Whatever ended the session, it was not a heart-rate ceiling and not cardiac drift.
  - **The 12.0% decoupling is substantially an artifact.** Decoupling compares first-half to
    second-half Pw:HR over the whole ride; inserting unplanned rest into the back half drops
    second-half average power while HR stays elevated, which inflates it mechanically. With
    interval HR flat at 165-167 throughout, 12% is not independent evidence of aerobic drift.
  - **Net: the prescribed session has one real attempt, not two, and it half-worked.** The
    limiter on display is *completing 40 min in this format*, not the wattage.
- **Why today is still the diagnostic.** Thursday prescribes under **280W** / over **320W** against
  the 305 anchor. Against the current **315-322** FTP estimate that is **~88% / ~101%** — the
  unders are sweet spot and the overs are barely over, so if the estimate is right this rides like
  a threshold alternation rather than a true lactate-shuttling set. That softness is the point:
  a *complete, HR-capped* 40 min at these numbers is the evidence the anchor is stale.
- **Gate for moving the retest (replaces "capped and clean" in the 8/18 addendum).**
  - **Move the FTP retest up from 9/08 to Tue 8/25** only if *all three* hold: the **full 40 min**
    is completed as 2 sets with **no unplanned stops** (i.e. two ~20:00 intervals at ~296W blended,
    per the detector caveat above); the **last over of set 2 at HR ≤175**; **fade ≥ −2%**.
  - **Keep the retest at 9/08** if set 2 fragments again, or HR ramps past **178**. A clean but
    short result keeps 9/08 — a repeat of 8/13 is a repeat, not progress.
  - **Decoupling is deliberately *not* in the gate** for this session, because fragmentation
    inflates it (see above) and it would double-count the completion criterion. Record it, but
    judge this session on completion and interval HR.
- **HR spec for the session, derived from 8/13's correctly-executed set 1** (avg **167**, peak
  **178**, over-peaks ramping 169 → 173 → 176 → 177 — which then failed in set 2, so today must
  run under it). Max HR 197.
  - **Set 1:** avg **160-166** (84% max), peak **≤174**; over-peaks by rep ≤166 / ≤170 / ≤172 /
    ≤174; each under sheds 5-8 bpm, floor ≤168 by rep 4.
  - **Set 2:** avg **165-171** (87% max), peak **≤178**; over-peaks ≤172 / ≤174 / ≤175 / **≤175**
    (the gate); each under sheds ≥4 bpm.
  - **Cross-check:** 8/18 held 20 min at **304W** — above today's 296W blend — at avg 162 / peak
    170 (rep 1). Set 1 running hotter than that means fuel, heat or fatigue, not fitness; back off
    early rather than at rep 8.
  - **Abort at any over peaking ≥182** (92% max). 8/06 peaked **189** (96%) and ran away.
  - **Clearance check:** on 8/13 each 3-min under shed **−2 / −7 / −7 bpm** — 280W is a genuine
    recovery valley for this rider, so the unders were working. Two consecutive unders shedding
    **<3 bpm** ends the session regardless of power.
  - **Do not expect set-2 cardiac drift.** On 8/13 HR was flat between sets (167 → 167) with the
    overs holding 318W throughout. Power broke while HR and watts both held — the reason fuelling,
    not pacing, is the variable under test.
- **Interval detection fixed in code (this PR), and it settles both corrections with real data.**
  The detector had two blind spots, both now closed, validated against re-pulled Strava streams
  for all 31 rides in history — **zero changes to any ride that already detected intervals, zero
  false positives on the 20 easy rides**, three rides corrected:
  - **Sub-threshold work was invisible.** A fixed 0.88×FTP cutoff cannot see work below it, so
    prescribed tempo (0.76-0.90 FTP) registered as nothing. Now, when nothing sustained clears
    the cutoff, detection falls back to splitting the ride's own power distribution (Otsu), with
    guards so flat rides still return nothing. **8/15 now resolves as 12:00 / 11:58 / 11:58 @
    244W, HR 143 / 144 / 145, fade 0.0%.** 8/08 resolves as 11:59 / 11:57 / 11:58 @ 249W. That is
    3×12 min tempo ridden to the second, twice — the "not being ridden" claim is dead, measured
    rather than inferred. It also surfaced **6/28: 2×10:06 @ 249W**, the Phase 1 Sunday 2×10 tempo,
    likewise ridden correctly.
  - **Over-unders fused into one block.** With unders at 280W above the 268W cutoff, a correct set
    merged into a single ~20:00 interval at the blended average. Blocks are now re-split
    internally. **8/13 set 1 resolves as under 2:56 @ 281 / over 2:00 @ 318 / under 3:00 @ 281 /
    over 1:59 @ 318 / under 3:00 @ 280 / over 2:00 @ 318 / under 3:01 @ 280 / over 1:59 @ 316** —
    four complete under/over pairs, exactly as prescribed. Set 2 gives two more complete pairs
    then fragments. **Fade across the overs: 0.2%.**
  - **New signal: `fade_pct_overs`.** Whole-block averages blend the unders back in and mask the
    progression; an over-under should be judged on the overs. 8/13's overs held **318W flat across
    all six** (first→last 0.0%) while the session fell apart — further evidence the failure was
    substrate, not power.
  - Absent intervals are now stated explicitly in the briefing ("no sustained work blocks found at
    any cutoff — read time-in-zone") instead of silently rendering nothing, which is what both
    misreadings grew from. Detection basis and threshold are recorded on every ride.
  - `fetch --reanalyze` added: stored rides keep whatever the detector produced when they were
    first analyzed, so any detection or FTP change needs a re-run to reach history. All 31 rides
    re-analyzed on this branch.
  - **Known limitation:** Phase 3 Thursday prescribes 30/15s (30 sec @ 345W / 15 sec @ 195W).
    Segments shorter than `segment_min_s` (45 s) are not resolved, so that session will report as
    fused blocks. Left untuned deliberately — no 30/15 session has been ridden yet, so there is
    nothing to validate against. Revisit with real data when the VO2 block opens 9/14.
- **CORRECTION to the 8/18 entry: the Saturday tempo blocks *are* being ridden.** That entry
  claimed 8/08 and 8/15 were "both flat Z2 with no tempo detectable" and made it a plan change.
  Wrong, and wrong the same way as the over-under read. Z3 Tempo is defined in `metrics.py` as
  **0.76-0.90 × FTP = 232-274W** — essentially identical to the prescribed 230-275W band. Actual
  time in that band: **8/08 = 36.2 min**, **8/15 = 36.2 min**, against a prescribed 3×12 = **36
  min**. Executed precisely, two weeks running. The false negative came from two directions at
  once: the interval detector's 268W work threshold sits *above* most of the tempo band so
  `intervals` returns null, and 36 min at ~250W inside a 165-min ride averaging 206W moves VI by
  almost nothing (hence 1.04 / 1.02). Plan description corrected in this PR. **Neither VI nor the
  interval table can see sub-threshold work — use time-in-zone for anything below 268W.**
- **That makes the durability limiter more stubborn, not less.** Prior read was "decoupling is
  high because he's skipping the stimulus." Actual: he is delivering the stimulus as prescribed
  and decoupling is *still* **9.8% (8/08)** and **8.0% (8/15)**. Note the pre-gap long rides had
  **0%** Z3 (6/27, 7/04, 7/12) — so the tempo blocks are new as of 8/08, and it is plausible that
  adding 36 min of tempo is itself part of why decoupling rose from 6.2% (7/12) to 8-10%. Worth
  isolating before concluding the durability deficit is worsening. Saturday stays protected either
  way; if anything its value goes up.
- **Asked whether tonight's session could move to Friday's rest day.** Load is identical —
  7-day TSS through 8/22 is **433** under either ordering, 3-day through 8/22 is **230** under
  either, and a rest day is still taken (it moves from Fri to Thu). The cost is purely ordering:
  it puts a 95-TSS threshold session the day before the long ride. Given the correction above —
  Saturday is being executed correctly and is the only session treating the standing limiter —
  the ruling is: **do not insert Friday on top of an unchanged Saturday.** Either skip the
  over-unders this week (retest stays 9/08, next attempt 8/27, nothing structural lost — the
  preferred option), or reshuffle to Fri over-unders / Sat easy 90 / Sun long 165, accepting one
  recovery day before Tuesday's 3×15 @ 305 instead of two. The over-unders is a diagnostic;
  Saturday is treatment. Do not trade treatment for a test.
- **Asked whether to bump the watts today — answer is no, and the reason is which half failed.**
  8/18 held **40:00 of work at 301W avg** (299/304, HR 162/169, fade −1.7%) — more total work at
  higher power than 8/13's 36:48 at ~297W, and clean. So threshold *expression* clearly supports
  the set-1 blend. But 8/13 failed in **set 2**, and adding watts loads the half that has never
  been completed. Time-at-target before watts — the same call made for Tuesday (3×15 @ 305 rather
  than 2×20 at a higher number). Note also that in an over-under the *unders* are the recovery
  valley: raising them is the harder change, not the softer one, and neither number moves today.
  The real re-anchor comes from the retest, and it will be a larger step than freelancing would
  give — at a tested FTP near 318 the session becomes roughly **under 300 / over 340**.
- **Fuelling is part of the test, not a footnote.** Set-2 HR flat at 165-167 while power broke up
  is consistent with substrate running out rather than a cardiovascular ceiling, which fits the
  fuelling read carried since 8/13 — though it is circumstantial, not proven. The 8/18 success came
  with the rule applied. Same rule today: main meal 3 h out, 60-90 g carb/hr and 500-800 mg
  sodium/hr on the bike, fan on. An under-fuelled result is not a fitness result and should not be
  used to move the retest either way.

---

## 2026-08-18 — Aerobic engine snapped back; **durability drift is the standing limiter** → Phase 3 Saturday held at 165 min

- **The 8/13 watch resolved — and it split two ways.** The call was: "Watch 8/15
  decoupling. If it's still >6% *with proper fuelling*, the durability deficit is
  structural and Phase 3's reduced Saturday (135 min) should be held at 165 instead."
  - **Efficiency: fixed.** 8/08 159min @ 209W, HR **147**, EF **1.471** → 8/15 165min
    @ 206W, HR **135**, EF **1.563**. **-12 bpm** at the same power, and EF is now back
    above the pre-gap 7/12 ride (1.522). The lower HR reads as the fuelling rule landing.
  - **Drift: not fixed.** Decoupling **8.0%** — still over the 6.0% flag, and the third
    straight long ride above it: **7/12 6.2% → 8/08 9.8% → 8/15 8.0%**. Against a
    pre-gap baseline of **7/04 1.5%**.
  - Read: whole-ride efficiency and within-ride durability are recovering on different
    clocks. The 1-hour engine is done (see below), the 3-hour engine is not.
- **Plan change (this PR): Phase 3 Saturday 135 → 165 min**, TSS 98 → 120. The VO2 block
  does not get to shrink the one session that treats the limiter. Reverts to 135 once two
  consecutive long rides land under 6%.
- **Plan change (this PR): the Saturday tempo blocks are not being ridden.** Phase 2
  Saturday prescribes 3×12 min tempo @ 230-275W. Both post-gap long rides were flat Z2 —
  **8/08 VI 1.04, 8/15 VI 1.02** (NP 217/211 vs avg 209/206). Nothing above 88% FTP was
  detectable either. Made explicit in the description: the tempo blocks *are* the
  durability stimulus, not a garnish. Fuelling rule written into the plan alongside it.
- **Short Z2 is now the best it has ever been.** 8/16: 80 min @ 200W, HR **124**,
  EF **1.630**, decoupling **0.8%**. Trend at ~200W: 6/23 HR 140 → 7/11 HR 132 →
  8/12 HR 129 → **8/16 HR 124**. That is **-16 bpm at the same power** across the block,
  and it is now better than the pre-gap 7/11 peak (EF 1.627).
- **Threshold prescription stepped up (this PR).** Tuesday's description carried a stale
  "first one back (8/11)" note. Replaced with the live progression: **2×20 @ 300W**,
  rep 2 to 305W only if rep 1 finishes at **HR ≤172**. Basis: 8/11 held 16:55 + 19:55
  @ **294W** at HR **169/171**, fade **0.0%**, decoupling **-1.4%**. Stepping watts and
  duration in the same session is the aggressive move; this steps duration first and buys
  the 305 datapoint conditionally.
- **The 305 anchor still looks stale-low**, unchanged from 8/13. 8/13's over-unders
  fragmented on fuelling but the *last* fragment was the day's highest power (3:16 @
  **303W**), fade **-4.7%**, ride max HR **178 vs 197 max**. `ftp` stays 305 in config
  until the **9/08** retest — no inference edits.
- **Load:** CTL **45.4**, TSB **+3.4**, 7-day TSS **332**, ramp **+0.2/wk** (was +2.8/wk
  on 8/13). The ramp has flattened — expected, and appropriate with a retest three weeks
  out and durability being rebuilt rather than loaded.
- **Recovery is running green and getting greener.** Last 5 days readiness
  88/88/84/91/**87**, RHR **40-43** vs base 44, HRV **85/65/78/63** vs base 62. Today's
  sleep score **75** is the week's low (7.4h) — the only soft number on the board.
- **No stat changes.** `sync-profile` clean — FTP 305, max HR 197, RHR 44, weight 79 all
  current.

### Addendum, same day — the session was ridden, and it is the best threshold work on record

- **8/18 executed: 2×20 @ 299W (HR 162) + 304W (HR 169)**, fade **−1.7%**, decoupling
  **2.7%**, EF **1.801**, NP 267, IF 0.876, 90 TSS, ride max HR **177**. The HR gate
  (rep 1 avg ≤172) passed by 10 bpm, so rep 2 took the 305W step.
- **vs 8/11, one week earlier, same format:** rep 1 **294W/HR 169 → 299W/HR 162**
  (+5W, +3 min, **−7 bpm**); rep 2 **294W/HR 171 → 304W/HR 169** (**+10W, −2 bpm**).
  EF **1.711 → 1.801** (+5.3%).
- **vs 7/15, the pre-gap best at the same 2×20 format:** **285/284W at HR 163/167 →
  299/304W at HR 162/169**. That is **+15W and +20W at the same heart rate**, with
  decoupling **8.0% → 2.7%** and EF **1.653 → 1.801** (+9.0%).
- **Rep 2 was the stronger rep** (−1.7% fade) and ride max HR was **177 against a 197
  max — 20 bpm of headroom** at 304W for 20 minutes. Average work HR ~165 = **84% of
  max**. That is not threshold-limit physiology.
- **FTP estimate tightens upward: 315-322** (was 312-320 on 8/13). `ftp` **stays 305**
  in config — still no inference edits; the **9/08** retest decides it.
- **Plan (this PR): next Tuesday's rung is time, not watts — 3×15 @ 305W**, 45 min of
  work vs today's 40. Durability is the standing limiter, so time-at-threshold is the
  better currency than another 5W.
- **Open question for Thu 8/20:** over-unders are prescribed under 280 / over 320 against
  the 305 anchor. If true FTP is ~318 those overs are barely over threshold — but this
  session has failed twice (8/06 ran genuinely hard, HR ramping 167→175→179; 8/13
  fragmented on fuelling), so targets stay as written and Thursday is the diagnostic.
  If it also runs capped and clean, move the retest up from 9/08 to 8/25.
- **Load after the session:** CTL **47.6**, TSB **−7.3**, 7-day TSS **422** (approaching
  the 450 flag), ramp back to **+2.4/wk**.

---

## 2026-08-13 — Threshold expression now **above** pre-gap; 305 anchor looks stale → retest inserted 9/08

- **Headline: the gap is paid back at threshold, and then some.** Same 20-minute
  block, same heart rate, +10W:
  - **7/15** (pre-gap best, FTP 317 anchor): 2×20 @ **285/284W**, HR **163 → 167**, fade 0.4%.
  - **8/11** (post-gap, 305 anchor): 16:55 + 19:55 @ **294W**, HR **169 → 171**, fade **0.0%**,
    decoupling **-1.4%**.
  - **8/13**: 19:55 @ **295W**, HR **167**.
  That clears the 8/06 watch ("fade >3% or HR >175 by end of rep 1 = 305 still optimistic")
  by a wide margin — it went the other way.
- **Therefore: FTP 305 is probably under-reading.** A 20-min block at a true 97% FTP
  should be close to maximal; his HR sat at **167-171** against a **197** max (85-87%),
  with **zero** fade. That is sweet-spot/upper-threshold physiology, not threshold-limit
  physiology. Best guess at true current FTP: **312-320**. The 8/04 ramp likely
  under-read — it came at the end of a re-entry week that deliberately carried no
  threshold work, and the 8/06 log already noted ramp protocols under-read for diesel
  riders. **Not changing `ftp` on inference** — 305 stays in config until a real test.
- **Plan change (this PR): FTP retest added Tue 2026-09-08.** End of Phase 2 (week 13),
  six days before the Phase 3 VO2 block opens Mon 9/14. Prefer **20-min × 0.95 over a
  ramp** this time. Rationale: Phase 3 watt targets (VO2 325-350W, 30/15s at 345W) are
  all anchored to FTP; opening that block on a stale-low anchor makes the intervals too
  easy and wastes the block. Previously the next test was **11/03** — after the entire
  VO2 phase.
- **The one real regression: long-ride durability.** Short Z2 has fully recovered, long
  Z2 has not.
  - Short Z2, same power: **6/21 198W @ HR 138** → **8/12 198W @ HR 129**. **-9 bpm**
    at identical power, decoupling 7.7% → **0.5%**. Clean win.
  - Long rides: **7/04** 180min, 223W @ HR 142, EF 1.578, decoupling **1.5%** →
    **8/08** 159min, 217W @ HR 147, EF 1.471, decoupling **9.8%**. Less power, higher
    HR, decoupling up 6×. Long-ride EF trend 1.557 → 1.578 → 1.522 → 1.479 → **1.471**.
  - Read: the 3-hour engine took more of the gap's damage than the 1-hour engine, and
    the Saturday long ride is the lever that fixes it. No plan change — Phase 2 Saturday
    (165 min + 3×12 tempo) is already the right medicine. **Watch: 8/15 decoupling.**
    If it's still >6% *with proper fueling*, the durability deficit is structural and
    Phase 3's reduced Saturday (135 min) should be held at 165 instead.
- **CTL 46.5, ramp +2.8/wk** — above the ~40-44 pre-gap level, up from **31.8** on 7/26.
  Fitness is fully rebuilt. TSB -5.2 (neutral).
- **8/13 over-unders aborted — fueling/hydration, not fatigue.** Session ran 20 min @
  295W clean (HR 167), then fragmented: 8:03 @ 299W, 4:25 @ 298W, 3:16 @ 303W. Athlete
  reported hip-flexor cramp in set 2 rep 1, then side stitch and "dead / can't feel my
  quads." Diagnosis is **not** central fatigue:
  - Oura was green that morning — readiness **87**, RHR **41** (base 44), HRV **61**, 7.96h.
  - Ride max HR **178** vs **197** max — 19 bpm of headroom left on the table. Work HR
    flat at **165-167** all session (vs 8/06 same workout, which ramped 154 → **179**).
  - Fade **-4.7%** — the final fragment (303W) was the *highest* power of the day.
  - Fueling: big pasta/burger lunch 5.5h out (glycogen fine), but the 45-min pre-ride
    meal was PB sandwich + yogurt + fruit (~25-30g fat, 5-8g fiber — slow gastric
    emptying, gut competing with legs for blood flow), and **water only** on the bike
    across 71 min with 47% of time in Z4.
  - **New standing rule — indoor threshold/VO2 fueling:** main meal **3h** out
    (~2 g/kg = ~158g carb, low fat / low fibre); if eating inside 60 min, fast carb only;
    on-bike **60-90 g carb/hr + 500-800 mg sodium/hr**; fan on. The 7/10 entry flagged a
    version of this (fasted Z2, 5.5% decoupling) — second occurrence, so it's a pattern,
    not a one-off. The 8/08 long ride's 9.8% decoupling likely belongs to it too.
- **Ignore the 12.0% decoupling on 8/13** — the athlete stopped mid-set with HR high and
  power at zero, which corrupts the Pw:Hr split. Not a durability datapoint.
- **Adherence:** 22/35 endurance and 7/9 threshold sessions in 8 weeks. Most of the
  endurance shortfall is the 11-day gap itself; excluding it, ~81%. Not a flag yet.
- **No stat changes.** `sync-profile` clean — FTP 305, max HR 197, RHR 44, weight 79 all
  current.

---

## 2026-08-06 — Retest came in at 305 (317 → **305**, -3.8%); all watt targets re-anchored

- **FTP 317 → 305** (Zwift ramp test, Tue 8/04). The 7/26 log's prediction was
  "315–322 base case, <312 = something didn't repair." It came in **305** — below
  the stated floor. The honest read: **the 7/26 estimate was too optimistic**, not
  that the test was bad. That entry leaned on the ~1–3% short-gap literature and
  argued the Phase 1 ceiling wouldn't unwind in 10 days. Actual loss was **3.8%**
  over what became a **19-day** disruption (last real training block ended 7/15;
  the 7/27–8/02 re-entry week was all Z2 + one soft SST). Longer gap than the
  model assumed, and the re-entry week deliberately carried no threshold work —
  so there was nothing holding the top end. Worth remembering next time: the
  "trained cyclists barely lose FTP" argument is about *aerobic* retention, and
  threshold expression decays faster than the aerobic base under it.
- **The ramp test itself looks valid, not a bad day:**
  - Peak sustained block **341W for 427s**, avg HR **180**, ride max HR **192** =
    97% of the 197 max on record. He genuinely emptied it — this wasn't a test
    abandoned early.
  - Ramp protocol (75% of best 1-min) usually *under*-reads for diesel riders,
    which is this athlete's profile (0.0% fade on 2×20 SST, strong Z2 durability).
    That was the argument for treating 305 as pessimistic.
  - **But the 8/06 over-unders killed that argument.** Athlete ran them at the
    305 anchor (280/320W) and reported "extremely difficult." If 305 under-read
    true FTP, a 305-anchored session should have felt *easier* than usual. It
    felt harder. Two independent signals converge: **305 is real**, and may even
    be slightly generous for right now.
- **No max-HR change.** 8/04 ramp peaked 192 vs the 197 on record (5/02, 5/09
  VO2 efforts). Below baseline, so `max_hr: 197` stays. `resting_hr: 44` and
  `weight_kg: 79` unchanged — `sync-profile` suggested nothing.
- **Plan changes (this PR) — re-anchored 317 → 305 across Phases 2–4:**
  - Phase 2 Tue Threshold: `300-330` → **`290-305`**.
  - Phase 2 Thu Over-unders: under `290` / over `330` → **under `280` / over `320`**.
  - Phase 2/3/4 Z2: `200-230` → **`195-225`** (230W was 75.4% of 305 — that had
    drifted into tempo, which is exactly how Z2 rides quietly turn into junk).
  - Phase 2 tempo: `240-285` → **`230-275`** (Sat long ride, 3×12 blocks).
  - Phase 3 VO2: `340-365` → **`325-350`**; 30/15s `360/200` → **`345/195`**.
  - Phase 4 Thu over-unders: under `290` / over `330+` → **under `280` / over `320+`**.
  - Phase 1 and the 7/26–8/02 re-entry overrides left at the old anchor — both
    are in the past, and rewriting them would falsify the historical record.
- **Progression step-back on Tue 8/11 (review this one):** plan template says
  2×20 @ 100% FTP. Encoded a note to **open at 2×15 @ 295W** instead. Rationale:
  8/11 is the first true threshold session in ~4 weeks, and 8/06 at the correct
  anchor already ran very hard. Build 2×15 → 2×20 → 3×15 across W9–W11 rather
  than opening at the endpoint. Same mistake the 7/03 entry called out about
  jumping 2×15 → 2×20 without an intermediate.
- **Watches:**
  1. **8/11 threshold HR/fade at 295W.** Fade >3% or HR >175 by end of rep 1 =
     305 is still optimistic; drop the anchor to ~298 and re-test in 3 weeks.
  2. **Z2 decoupling is back to 4.8%** (was down to -0.2% on 7/02 pre-gap).
     Under the new 305 anchor the Z2 band is honest again; if decoupling doesn't
     walk back under 3% within two weeks of consistent Z2, the aerobic base took
     more of a hit than the FTP number alone shows.
  3. **CTL 32.9, ramp -2.5/wk.** Fitness is still bleeding. Consistency over
     intensity for the next 2–3 weeks — the Saturday long ride is the lever.
- **Goal line in `meta` still reads "Raise FTP from 315."** Left as-is — it
  records the original intent of the block. The working anchor is 305.

---

## 2026-07-26 — 11-day off-bike gap; 1-week re-entry ramp + retest pushed 7/28 → 8/04

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
- **Why 8/04, not 8/11 (revised after athlete pushback):** first two drafts of this
  update over-cautioned. The classic "5–7% loss in 2 weeks" figure comes from
  Coyle-era studies of trained athletes stopping *completely*; more recent work
  (Mujika & Padilla; Ronnestad) puts short-gap (10–14 d) FTP loss in a trained
  cyclist at **~1–3%**, not 5–6%. The 8 weeks of Phase 1 built a ceiling; 10
  days off doesn't unwind the adaptations — it temporarily masks their expression
  (HR-for-power drift, neuromuscular pattern). Those come back inside a week,
  which is exactly what the re-entry week is for. One week of pattern re-sync is
  enough runway; the "repeat W6 as calibration" week was over-caution, not
  physiology.
- **Plan changes (this PR):**
  - **Phases shifted +1 week.** Phase 1 [1,6] → **[1,7]**; Phase 2 [7,12] →
    **[8,13]**; Phase 3 [13,16] → **[14,17]**; Phase 4 [17,20] → **[18,21]**.
    Final test 10/27 → **11/03**. Structure preserved, calendar delayed by 1 wk.
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
  - **Test Tue 8/04** — 20-min × 0.95 or ramp. Re-anchor watt targets after.
    Realistic expectation: **315–322W**. Pre-gap trajectory pointed toward ~325;
    with the gap, holding 317 is base case and a small bump is the good case.
    A test <312 says either the aerobic base didn't fully repair or the taper
    was off — not that real FTP dropped.
  - **Post-test week (8/03-8/09)** — falls in the new Phase 2 window and runs
    the Phase 2 template: Mon 8/03 Rest, **Tue 8/04 Test**, Wed 8/05 Endurance
    75 min, Thu 8/06 Over-unders, Fri Rest, Sat 8/08 long endurance 165 min
    with tempo, Sun 8/09 Z2 90. Standard Phase 2 W1 shape with the test
    replacing Tuesday's threshold session.
- **Watches (in priority order):**
  1. **Wed 7/29 SST HR/fade** — first hard data point. HR climbing >167 at
     end of rep 1 at 275W or fade >2% means still detrained; push next week's
     8/05 SST down to 2×15 @ 280W instead of 285W.
  2. **Sat 8/01 long-ride decoupling** — >5% at proper fueling = aerobic base
     didn't fully hold; slide the test one more week to 8/11.
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
