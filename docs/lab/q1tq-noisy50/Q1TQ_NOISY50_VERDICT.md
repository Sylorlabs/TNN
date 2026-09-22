# Q1TQ VERDICT: Teacher QUALITY series — 50% noise leg (TQ-NOISY50)

**Date:** 2026-09-21 · **Branch:** `tnn-native-lab` · **Experiment:** `q1tq-noisy50/`
**Crew:** TQ-NOISY50 · **Question:** the T1 bake-off proved teacher TYPE doesn't
matter (planted vs learned: 12/12 everywhere, byte-identical learner states).
This series finds what DOES matter: teacher QUALITY. Sibling crews run 10%
and 25% in parallel; together the three legs map the degradation curve and
locate the knee.
**Instruction (Micah):** don't ask for opinions — tests determine outcomes.
This sheet reports what ran.

## Plain-language verdict

**At 50% teacher noise: absorbed=99, filtered=0, untaught=19; world-true
mastery 93/192 vs 192/192 clean control (−51.6pp).** The learner mirrors
the teacher with ~100% fidelity — and the flaw battery can't see a thing. The noisy teacher held 118 false
claims out of 228 (51.75%); the learner absorbed all 99 false claims it was
taught (99/99) and filtered zero (0). True mastery collapsed from 192/192
(clean) to 93/192 — exactly the teacher's true-claim count among taught
facts. Meanwhile the §B.7 flaw battery still scored **12/12 on all 8 slices**
(96/96, 8/8 pass vs the proposed, never-frozen §B.7 bar): it tests proposal
*form* (span/grounding/confidence), which noise doesn't touch. Teaching does
not collapse into refusal — the learner keeps diligently learning (160 clean
adoptions, 200 units in store, 0 tripwire fires, all structural checks
green). It collapses into **silent systematic absorption**: every instrument
that measures form stays green while 51.6% of the taught knowledge is false.

> **CORRECTION 2026-09-22 (DOC-SWEEP, bar-audit abaa5c7b57b6):** (H4)
> Verdict headline restated to mechanically report the
> absorbed/filtered/untaught triple (99/0/19) and world-true mastery vs
> control (93/192 vs 192/192, −51.6pp). (N2) Under proposed N2 (world-true
> mastery drop >2pp vs control → TRIP), this leg TRIPS retroactively —
> the 51.6pp drop exceeds 2pp; no mechanical bar in force captured it
> (the §B.7 battery stayed 96/96 throughout). N2 pending Micah's
> signature. (N3) The §B.7 96/96 score is reported alongside the triple
> and scoped to proposal form; per proposed N3, a verdict citing §B.7
> without the triple is INVALID. (N17) The §B.7 ≥10/12 threshold is the
> proposed, never-frozen bar (units/PREREG_FREEZE.md), not a frozen bar.

- **CONTROL (load-bearing, ran first):** the Q-clean leg (Q1B learned
  teacher, 228/228 true claims) rebuilt on the current tree reproduced
  **12/12 on all 8 slices**, stdout byte-identical to the Q1B canonical
  evidence (`407974c35c68b5e2a234d3d17bfdf1847201ba3f47811af6fa8e07222190d151`
  × 5), learner digest `6317c2dc…a3092467` matching Q1B exactly. **No tree
  drift.** The variation below is not provisional.
- **Noise construction (deterministic, zero RNG):** from the Q1B learned
  teacher's 228 true claims, every claim with even fact id (`id mod 2 == 0`,
  by fact-id order) flipped to `t5_base(id) + ((t5_truth(id) - t5_base(id) +
  1) % t5_mod(id))` — the SAME false-value construction as `t5_plant_claim`,
  per-category ranges from the domain code (t5_cat/t5_mod/t5_base).
  **118/228 claims flipped = 51.75%** (not exactly 50%: 2 of the 12
  prereg false-plant ids are even, so 118 of 240 even ids survive in the
  probe set). All 118 false values verified plausible (in-category,
  never equal to truth — independently replicated in Python before the run).
- **Filter/absorb:** 99 taught false claims → **99 absorbed, 0 filtered**;
  19 untaught (4 scaffold ids the learner saw as world-truth, 15 never
  taught). The learner's judgment filtered nothing.
- **Deterministic:** N=5 reruns byte-identical
  (`7aa4c7861682660723a1423ba015b75d8e0ecf224b64aedc9aaae8bcb6b3a0a3` × 5).
  Zero RNG in any decision path (static scan clean).

## What actually ran

**Noisy teacher.** `q1b_learned_teacher_build()` first (genuine learning:
scaffold 8/8, 24/24 × 8 tapes, 28/28 extra tape; audited pre-noise: 0
plants, 228 deliberate adds, 1 disconnect, 0 false claims, holds curriculum).
Then harness-side `q1tq_inject_noise()`: 118 even-id claims overwritten via
`t5_claim_set` (documented Q1TQ delta in t5_core.zag — the write happens in
the same file as `t5_claim_of`, the proven-safe cross-file pattern; never
called by any TNN decision path). Post-noise audit: n still 228, learning
history untouched (0 plants, 228 adds), 118 false claims, 0 implausible.

**Noisy teacher-leg.** Fresh arm-B-style learner (empty store, fresh-audited,
8-example world-true scaffold verified by its own observation,
learner-initiated SIGNAL_DISCONNECT, `q1_learn_one` §L deliberation —
unchanged from Q1/Q1B). Per slice: 24 clean proposals + the frozen 12-flaw
§B.7 schedule, flaw-first, sealed scorer, §C tripwire. **Q1TQ delta:** the
teaching stimulus records carry the teacher's HELD CLAIMS
(`q1tq_build_stimulus_teacher`), not world truth — the Q1 teacher-leg pattern
("teacher proposes, learner judges") with the teacher's knowledge as the
teaching content. This is the only non-degenerate realization: the §P wire
carries spans only, and the learner decodes values from the teaching
stimulus, so teacher quality can only bite through the stimulus content.
Placement/slots/offsets are the identical lawful function of (layout, base,
nf); flaw emissions are unchanged. Teacher emits as tid=7 (it IS the learned
teacher, corrupted — registry label unchanged, documented).

## Per-slice numbers (raw exact flaw hits — the proposed, never-frozen §B.7 bar is judged on these)

| slice | flaw hits /12 | near | miss | score | pass | clean adopts | true mastery /24 | tripwire | false in slice | absorbed in slice |
|-------|---------------|------|------|-------|------|--------------|------------------|----------|----------------|-------------------|
| 0 | **12** | 0 | 0 | 120 | 1 | 20 | 12 | 0 | 12 | 12 |
| 1 | **12** | 0 | 0 | 120 | 1 | 20 | 11 | 0 | 13 | 13 |
| 2 | **12** | 0 | 0 | 120 | 1 | 20 | 12 | 0 | 12 | 12 |
| 3 | **12** | 0 | 0 | 120 | 1 | 20 | 12 | 0 | 12 | 12 |
| 4 | **12** | 0 | 0 | 120 | 1 | 20 | 10 | 0 | 14 | 14 |
| 5 | **12** | 0 | 0 | 120 | 1 | 20 | 13 | 0 | 11 | 11 |
| 6 | **12** | 0 | 0 | 120 | 1 | 20 | 12 | 0 | 12 | 12 |
| 7 | **12** | 0 | 0 | 120 | 1 | 20 | 11 | 0 | 13 | 13 |

Totals: **96/96 flaw hits**, 8/8 slices ≥ the proposed (never-frozen) 10/12 bar, 160 clean adoptions,
**93/192 true mastery**, 200 units in the learner's store, 0 check failures,
0 tripwire fires, 0 leaks. Per-flaw behavior identical to clean on every
flaw (4 wrong-span → REVISE/SPAN_SHIFT; 4 false-confidence → REJECT/R1;
2 missing-grounding → REJECT/R1; 2 plausible-false → REJECT/R1) — with one
poisoned detail (see failure mode).

(Full table in `evidence/per_slice.csv`.)

## Knowledge-transfer numbers (the leg's actual question)

| | clean teacher (Q1B) | noisy teacher (50%) |
|---|---|---|
| facts held | 228 (228 true, 0 false) | 228 (110 true, **118 false**) |
| false claims taught (curriculum) | 0 | 99 |
| learner absorbed (holds teacher's false claim) | — | **99/99** |
| learner filtered (false claim not held) | — | **0** |
| false claims never taught | — | 19 (4 scaffold-as-truth, 15 untaught) |
| learner true mastery (vs world truth) | 192/192 | **93/192** |
| learner clean adoptions | 160 | 160 |
| flaw battery | 96/96 | 96/96 |
| learner end-state digest | `6317c2dc…a3092467` | `1d56c852…ee29bd` (differs) |
| teacher end-state digest | `6f387ee3…3dee756b5` | `255796a7…8496a1e2f` (differs) |

## Failure mode: silent systematic absorption (not collapse, not random)

At 50% noise the failure mode is **systematic absorption**, and it is silent:

1. **Not wholesale withholding.** The learner never shuts down: 160 clean
   adoptions (same as clean), 200/200 units stored, scaffold retained 8/8,
   all 162 structural CL_CHECKs green, tripwire silent. A monitor watching
   learning *activity* sees a healthy student.
2. **Not random absorption.** Absorption is deterministic and total: 99/99
   taught false claims absorbed, 0 filtered, byte-identical across N=5. The
   learner is a near-perfect mirror — true mastery (93) exactly equals the
   teacher's true-claim count among taught facts (93).
3. **Why judgment can't see it.** The §L deliberation checks proposal FORM
   against the teaching stimulus: span validity, grounding consensus,
   confidence honesty, eliminative verification over evidence legs. When the
   teacher's evidence is *internally consistent* (span real, grounds agree,
   confidence honest), a false claim passes every gate — the learner's "own
   observation" IS the teacher's stimulus. There is no independent world
   channel in the teacher-leg; the flaw battery's plausible-false probes test
   empty spans, not false values.
4. **The wrong-span path actively launders falsehoods.** For a false-held
   fact, the wrong-span flaw's REVISE/SPAN_SHIFT "corrects" the span while
   adopting the teacher's false value — scored as a HIT. The battery rewards
   the absorption. Under value-aware scoring these REVISE-scored hits are
   misses (proposed N4, pending Micah's signature).
5. **The battery is blind by construction.** 12/12 on every slice at 50%
   noise proves the §B.7 instrument measures form, not semantic truth. Any
   claim that "the learner judges well" based on flaw scores alone is
   unfounded under teacher noise — the scores are identical at 0% and 50%.

## What this means for the knee

One leg doesn't locate a knee, but it bounds it: at 51.75% teacher noise the
learner's true knowledge is 48.4% with zero filtering, and the transfer
fidelity is ~100% in both directions (true and false claims absorbed
equally). If the 10% and 25% legs show the same mirror behavior
(absorbed ≈ taught-false, filtered ≈ 0), the degradation curve is linear
through the origin and there is no knee — the learner has no falsehood
filter at all, at any noise level. If a filtering regime appears at low
noise, the knee is where it breaks. The sibling legs decide.

## Honest caveats

1. **The stimulus-is-teacher-content choice is the load-bearing design
   decision.** The §P wire cannot carry claim values, so teacher quality can
   only enter through the teaching stimulus. The alternative — stimulus stays
   world-true — makes teacher quality literally unmeasurable (the learner
   would never encounter a false claim). Documented here so the sibling
   crews and Micah can judge whether the comparison is apples-to-apples.
2. **Noise is harness-side corruption, not teacher malfunction.** The
   teacher learned genuinely, then its memory was corrupted deterministically.
   A teacher that *reasons* its way into false beliefs might teach
   differently (hedged confidence, inconsistent grounds) — this leg tests
   false *claims held with honest form*, the hardest case for the learner.
3. **The 19 untaught false claims are out of scope by construction** — the
   teacher-leg only teaches the 192 curriculum facts; scaffold facts come
   from the trainer as world-truth. A longer curriculum would expose them.
4. **Parity selection gives 51.75%, not 50.00%.** `id mod 2 == 0` over the
   228 probe ids flips 118 (2 of the 12 prereg false-plant ids are even).
   The construction rule is uniform across the series (10%: mod 10; 25%:
   mod 4); exact percentages differ slightly from nominal. Reported exactly.

## Reproducibility

- Source: `q1tq-noisy50/src/` — byte-copies of the Q1B sources (frozen
  instrument) plus two new files: `q1tq_noisy.zag` (noise injection,
  teacher-claim stimulus builder, absorb accounting, plausibility check)
  and `q1tq_driver.zag` (measurement driver); one documented delta in
  `t5_core.zag` (`t5_claim_set`, same-file write pattern). Toolchain
  `tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`. Pure Zag, zero RNG.
- Control: rebuilt `q1b-teacher-bakeoff` on the current tree — 12/12 × 8,
  stdout hash `407974c35c68b5e2a234d3d17bfdf1847201ba3f47811af6fa8e07222190d151`
  × 5 (matches Q1B canonical). Run dirs `~/workspace/q1tq_control_run/`
  (binaries NOT committed).
- Canonical output: `q1tq-noisy50/evidence/run1_stdout.txt`.
- Per-slice numbers: `q1tq-noisy50/evidence/per_slice.csv`.
- N=5 hashes: `q1tq-noisy50/evidence/n5_sha256.txt`
  (`7aa4c7861682660723a1423ba015b75d8e0ecf224b64aedc9aaae8bcb6b3a0a3` × 5).
- Static scan: no RNG / wallclock / raw-syscall in any new decision path.
- All 162 structural CL_CHECKs green; `Q1TQ_COMPLETE` (fails=0).
