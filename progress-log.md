# Progress Log

An append-only record of how the plan and key stats change over time, so the daily routine has
context on progression — and you have a readable history. The routine reads this at the start of
each run and adds a dated entry (in the same PR) whenever it changes a stat or the plan, or notices
a meaningful trend shift. **Newest entries at the top.**

The live config (`config/athlete.yaml`, `config/training-plan.yaml`) always holds current values —
the analysis math needs them. This log is the narrative of *how they got there*.

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
