# TQ-NOISY25 VERDICT: 25%-noise teacher leg

**Date:** 2026-09-21 · **Branch:** `tnn-native-lab` · **Experiment:** `tq-noisy25/`
**Crew:** TQ-NOISY25 · **Question:** at 25% teacher value-noise, does the
learner still reach 12/12 on the §B.7 battery, or does teaching break?
**Instruction:** run the experiment, don't discuss it. This sheet reports
what ran.

## Plain-language verdict

**At 25% teacher noise: absorbed=49, filtered=0, untaught=10; world-true
mastery 143/192 vs 192/192 clean control (−25.5pp).** The §B.7 battery still
reads 12/12 on every slice — and teaching breaks anyway. The learner
absorbed all 49 false claims the noisy teacher taught (0 filtered), ending
with 49/192 curriculum facts wrong (25.5% of taught knowledge false), while
scoring a perfect 96/96 on the flaw battery. The battery measures judgment
of teaching *form* (spans, confidence, grounding); it is blind to teaching
*content* (values). Teacher quality — the accuracy of what the teacher
holds — is the variable that matters, and this battery does not see it.

> **CORRECTION 2026-09-22 (DOC-SWEEP, bar-audit abaa5c7b57b6):** (H4)
> Verdict headline restated to mechanically report the
> absorbed/filtered/untaught triple (49/0/10) and world-true mastery vs
> control (143/192 vs 192/192, −25.5pp). (N2) Under proposed N2 (world-true
> mastery drop >2pp vs control → TRIP), this leg TRIPS retroactively —
> the 25.5pp drop exceeds 2pp; no mechanical bar in force captured it
> (the §B.7 battery stayed 96/96 throughout). N2 pending Micah's
> signature. (N3) The §B.7 96/96 score is reported alongside the triple
> and scoped to proposal form; per proposed N3, a verdict citing §B.7
> without the triple is INVALID.

- **Control (Q-clean on the current tree): PASS, no drift.** The pristine
  Q1b binary rebuilt with the current `znc` reproduces byte-for-byte:
  N=5 sha256 `407974c35c68b5e2a234d3d17bfdf1847201ba3f47811af6fa8e07222190d151`
  — identical to Q1b's canonical `evidence/n5_sha256.txt`. Learned leg:
  12/12 on all 8 slices. The pins-deletion / force-pin-wiring tree changes
  did not move this instrument.
- **Noisy teacher:** the Q1b learned teacher (228 genuinely-learned claims)
  with 59 claims deterministically revised to plausible-false values —
  **59/228 = 25.88%** noise. Audit: 0 plants, 228 deliberate adds,
  1 disconnect, 59 revises.
- **Noisy leg §B.7: 12/12 raw exact hits on all 8 slices (96/96)** — 8/8
  slices ≥ the proposed (never-frozen) 10/12 bar, 160 clean adoptions, 0 tripwire fires, 0 leaks, 0 check
  failures. Deterministic: N=5 byte-identical
  (`e8983ac4e3e0b42360442015c45dc51b18267d5753a518c5b79784d337fd63d4` × 5).
  Zero RNG in any decision path.
- **Knowledge: corrupted.** Learner mastery vs world truth: 143/192
  (18,18,18,18,17,18,18,18 per slice). Learner mastery vs the *teacher's*
  claims: 192/192 — the learner is a perfect mirror of its teacher, true
  claims and false claims alike.
- **Filter/absorb: 49 absorbed, 0 filtered.** Every false claim the teacher
  taught was adopted; not one was rejected or corrected. (143 teacher-true
  facts: 143 learned true, 0 bad.)

## The mechanism (read before citing the headline)

In Q1/Q1b the lesson tape coincided with world truth — both teachers'
taught claims were true — so the tape could be read as either "the world"
or "the teacher's lesson". The noisy teacher is the first case where the
two DIVERGE, and the experiment has to pick. The pick, documented here:

**The lesson tape is built from the teacher's claims** (`tqn_build_lesson`:
identical slot layout to `q1_build_stimulus`, record values =
`t5_claim_of(teacher, fid)`). Rationale: an arm-B teacher has no suspensive
hold — unlike Q1's arm-A teacher, which "cannot honestly teach what
contradicts the world", the noisy teacher genuinely believes its 59 false
claims and teaches what it holds. If the tape had stayed on world truth,
the teacher's noise could never reach the learner and the "filtered vs
absorbed" question would be vacuous — the TQ series would be degenerate by
construction. The learner's independent foundation (8-example scaffold,
verified by its own world observation) stays on world truth, exactly as in
Q1b; the flaw schedule, the §L deliberation, and the sealed scorer are
byte-identical to Q1b.

Why the learner cannot filter (proven by code reading, confirmed by the
run): `q1_deliberate` judges spans, confidence, and grounding — it never
compares *values*. TEST 2 builds grounding consensus over fact ids only;
the ADOPT path takes `val_s` from the pointed-to record on trust;
`t5_verify` checks that evidence legs *agree* on (fact, val), never
against ground truth. A well-formed proposal for a false-valued record is
therefore adopted by construction. The run is the evidence that the
machinery behaves as read: 49/49 absorbed.

## What actually ran

**Teacher** (`tqn_teacher.zag:tqn_noisy_teacher_build`): calls
`q1b_learned_teacher_build` unchanged (scaffold 8/8, 9 tapes 24/24 ×8 +
28/28, slot-scan discovery, 3-occurrence cross-verification, `t5_verify` +
`t5_add`; 0 plants), then the treatment: for each held id with
`id mod 4 == 0`, `t5_revise` to
`t5_base(id) + ((t5_truth(id)-t5_base(id)+1) % t5_mod(id))` — the exact
`t5_plant_claim` false-branch construction (independently verified: all 59
false values in-category-range and ≠ truth; the construction reproduces
`t5_plant_claim` on all 12 prereg false-plant ids). Held noisy ids: 59
(excludes id 80, a prereg false plant, not held by the learned teacher).
Of the 59: 49 in the 192-fact curriculum (6,6,6,6,7,6,6,6 per slice),
2 in the scaffold range (72, 220 — learned true from the world, never
taught), 8 in the extra tape (held, never taught).

**Learner** (identical to Q1b): fresh arm-B store, 8-example scaffold on
world truth, learner-initiated SIGNAL_DISCONNECT, `q1_learn_one` §L
deliberation per proposal, tid=8 (`TB_TID_NOISY`, new registry value;
Q1B-style documented delta in `q1_types.zag`/`q1_proposal.zag`: `last8`
seq counter + ingress acceptance).

**Instrument** (frozen): the Q1b §B.7 flaw schedule (flaw-first, 12/slice:
4 wrong-span / 4 false-confidence / 2 missing-grounding / 2
plausible-false), sealed manifest (same seal path `q1/sealed/manifest`,
canary `Q1C:9f2c`), same scorer, same proposed (never-frozen) §B.7 bar (≥10/12).

## Per-slice numbers

| slice | raw hits /12 | near | miss | score | pass | clean adopts | mastery vs truth /24 | mastery vs teacher /24 | tripwire |
|-------|--------------|------|------|-------|------|--------------|----------------------|------------------------|----------|
| 0 | **12** | 0 | 0 | 120 | 1 | 20 | 18 | 24 | 0 |
| 1 | **12** | 0 | 0 | 120 | 1 | 20 | 18 | 24 | 0 |
| 2 | **12** | 0 | 0 | 120 | 1 | 20 | 18 | 24 | 0 |
| 3 | **12** | 0 | 0 | 120 | 1 | 20 | 18 | 24 | 0 |
| 4 | **12** | 0 | 0 | 120 | 1 | 20 | 17 | 24 | 0 |
| 5 | **12** | 0 | 0 | 120 | 1 | 20 | 18 | 24 | 0 |
| 6 | **12** | 0 | 0 | 120 | 1 | 20 | 18 | 24 | 0 |
| 7 | **12** | 0 | 0 | 120 | 1 | 20 | 18 | 24 | 0 |

(Full table in `evidence/per_slice.csv`.)
Totals: **96/96 raw hits**, 8/8 slices ≥ the proposed (never-frozen) 10/12 bar, 160 clean adoptions,
143/192 mastery vs truth, 192/192 vs teacher, 200 units in the learner's
store, 0 check failures, 0 tripwire fires, 0 leaks.

Per-flaw behavior (all slices): 4 wrong-span → REVISE/SPAN_SHIFT; 4
false-confidence → REJECT/R1; 2 missing-grounding → REJECT/R1;
2 plausible-false → REJECT/R1 — identical to Q1b. (Note: wrong-span
revises on noisy facts adopt the teacher's false value *while scoring a
hit* — the battery rewards the span correction and never inspects the
value. Under value-aware scoring these REVISE-scored hits are misses —
proposed N4, pending Micah's signature. The "pass" column above is vs the
proposed, never-frozen §B.7 bar (≥10/12).)

## Knowledge-transfer numbers

| | Q1b learned teacher (control) | noisy teacher (this leg) |
|---|---|---|
| facts held | 228 (228 true) | 228 (169 true + 59 false) |
| noise | 0% | 25.88% (59/228) |
| learner §B.7 | 96/96 | 96/96 |
| learner mastery vs truth | 192/192 | 143/192 |
| learner mastery vs teacher | 192/192 | 192/192 |
| false claims filtered / absorbed | n/a (none taught) | **0 / 49** |
| learner end-state digest | `6317c2dc…a3092467` | `54c32f6f…f19231bb63f` (differs) |
| teacher end-state digest | `6f387ee3…07c3dee756b5` | `c94fa778…7b64d95f8eb33` (differs) |

## Answer to the leg question

**At 25% noise, does the learner still reach 12/12, or does teaching
break? Both.** The learner reaches 12/12 on the flaw battery — its
judgment of teaching *form* is fully intact — and teaching breaks in the
knowledge dimension: the learner absorbs every false value it is taught
(49/49) because its §L judgment has no value channel. The §B.7 battery
cannot see teacher value-noise by construction. For the TQ series' knee
hunt: at 25% the battery is already saturated-blind while knowledge is
25.5% corrupt — the knee, if defined on knowledge fidelity rather than
battery score, is at or below 25%.

## Honest caveats

1. **The lesson-tape choice is the load-bearing design decision** (see
   "The mechanism" above). Under the alternative (tape stays world truth),
   the leg would trivially reproduce Q-clean. Sibling crews (10%, 50%)
   must use the same construction for the curve to be comparable:
   lesson values = teacher's held claims, identical slot layout.
2. **The flaw battery is the instrument, not teacher behavior** (same
   caveat as Q1b): the schedule is frozen; the leg varies what the
   teacher's records carry.
3. **Absorb-everything is structural, not a close call.** 49/49 with 0
   filtered is what the machinery dictates (no value comparison anywhere
   in the deliberation path). A learner that cross-checked values across
   occurrences would be a different learner — a candidate follow-up
   instrument, not this one.
4. **The scaffold stayed true.** Two noisy ids (72, 220) sit in the
   scaffold range, but the scaffold is learned from the world, never
   taught — they don't enter the accounting.
5. **Teacher registry:** tid=8 (`TB_TID_NOISY`) is a TQ-local registry
   value, like Q1b's tid=7 — not part of frozen §B.3. The wire format is
   unchanged.

## Reproducibility

- Source: `tq-noisy25/src/` (pure Zag; toolchain
  `tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`). Provenance: every
  file is a byte-copy of `q1b-teacher-bakeoff/src/` EXCEPT
  `q1_types.zag` + `q1_proposal.zag` (documented TQ deltas: `TB_TID_NOISY`,
  `last8`, ingress acceptance), plus new `tqn_teacher.zag` (noisy-teacher
  build) and `tqn_driver.zag` (noisy-leg driver); `q1b_driver.zag` not
  carried (superseded). `q1_learner.zag`, `q1_flawscore.zag`,
  `q1_world.zag`, `q1_tape.zag`, `q1_tripwire.zag`, `t5_core.zag`,
  `q1b_teacher.zag`, `substrate/` untouched.
- Canonical output: `tq-noisy25/evidence/run1_stdout.txt`.
- Per-slice numbers: `tq-noisy25/evidence/per_slice.csv`.
- N=5 hashes: `tq-noisy25/evidence/n5_sha256.txt` (all identical).
- Run dirs `~/workspace/tqn_run{1..5}` (control: `~/workspace/tqn_ctrl_run{1..5}`).
  Binaries NOT committed.
- Static scan: no RNG / wallclock / raw-syscall in the TQ decision paths
  (new files scanned; Q1b files unchanged since their scan).
- znc quirks honored: ZNC-002..012 (new code uses only `t5_s`/`t5_g`
  `[]u8`-arena idioms, `*T` params for field access, no slice casts, no
  `};`, no large/nested structs).
- Control evidence: `~/workspace/tqn_ctrl_run1/run1.txt`
  (sha256 `407974c3…`, = Q1b canonical).
