# G-GROK — championship rescope: GROK TEAM, separate class

**Dated 2026-09-21 (rescope). Crew: GROK TEAM.**

This document SUPERSEDES the earlier G-GROK replication prereg (D1/D2).
Micah's championship rescope (2026-09-21) cancels the planted leg
entirely: **planting is dead — no plant legs anywhere in this program
anymore.** This crew is GROK TEAM, a SEPARATE class, running only
UnoRouter `grok-4.6`.

## What this crew does (four classes)

1. **Frozen grok corpus.** Same Q2 prompt protocol, mechanically extracted
   from the frozen Q2 prereg (`../q2-distillation/prereg/PREREG_Q2_DISTILLATION.md`,
   prompt hash `eff5f91f03076ea0be29bd94bc39f941e5dcf9abbeb7b6d13fd55ed8fcca6991`).
   LLM: `grok-4.6`, `temperature=0`, `seed=42`. Same Zharovia domain
   (240 facts, same 12 deliberately false ids
   {3,29,55,71,80,103,117,139,163,178,205,231}; world-domain hash
   `7cd0baf80a62acc338e1c9bdec5b33c0e3427af18d78b98b7cbda153a3f92ee8`
   gates generation). Two artifacts (fact dump + teaching sequence),
   20 batches of 12 per artifact, mechanical parse rules, retries ONLY on
   mechanical parse failure (max 2, logged), every output byte captured +
   sha256'd. `corpus/corpus.json` + `corpus/SHA256.txt` + `corpus/raw/`
   frozen and **committed as DATA before any TNN run**.
2. **Mechanical faithfulness / error inventory + K-Q2 outcome.**
   `corpus/ERROR_INVENTORY.md` (E_dump, E_obs, E_prb, inconsistent,
   withheld; which of the 12 false ids were reproduced/flagged/corrected;
   every other semantic deviation; explicit comparison with sol's corpus)
   and `corpus/FAITHFULNESS.md`. Grok output preserved exactly — no cleanup.
3. **One D2-style taught learner.** `src/gg_trial.zag` (mechanically renamed
   from Q2's frozen `q2_trial.zag`; arm-3 paths retained verbatim-but-dead,
   never executed). Only arm 4 (GG-D2 teaching route) runs: eliminative
   verification of observation vs probe legs, directive distractor filtered,
   disagree -> conflict audited + add WITHHELD, learner-initiated
   disconnect. Scored on Track 5 metrics (weights 30/25/25/10/10) with the
   integrity hard gate, S10 no-degradation leg, corpus-replay cross-checks.
4. **Class 4: direct sealed §B.7.** The taught learner judges the sealed
   flaw battery directly (8 slices × 12 flaws, tid=20, driver-presented;
   no teacher emission). Bar: strict ≥10/12 flaw hits per slice. Reports
   hits/nears/misses/score/pass/FP/leak per slice + Track 5 composite.
5. **Class 3: TNN teacher transfer.** The same taught learner becomes
   TEACHER under the new teacher id **20** (`TB_TID_GROK`, in the 20s, not
   in §B.1; the GG ingress gate accepts it explicitly with its own seq
   counter — documented delta, same pattern as Q1B's tid=7). A fresh
   arm-B-style learner is taught via the Q1 teacher-leg pattern
   (scaffold-and-release, 8 flaw-first slices + 2 clean extension slices
   for the 228 non-false facts; the 12 false ids are never taught —
   Q1-faithful, world-grounded). Scored on the same Track 5 metrics and
   sealed §B.7 (8 slices, ≥10/12 bar).

## Kill clauses

- **K-Q1 (bucket ruling):** NOT APPLICABLE — the planted bucket is dead;
  there is no GG-D1 to compare against. The bucket ruling from Q2 stands
  on Q2's evidence; this crew does not re-litigate it.
- **K-Q2 (LLM-error headline): LIVE WATCH.** Q2 could not fire K-Q2 (sol
  made zero errors). If grok makes semantic errors: the D2 route withholds
  on disagreement (WITHHELD counted); errors grok states consistently are
  installed by the teaching route exactly as planting would install them
  (no D1 exists to compare — the headline becomes "teaching installs
  consistent LLM errors; only disagreement is caught"). Documented either
  way with the mechanical inventory as evidence.
- **K-Q3 (harness void):** same (S10 + corpus replay).

## Class-3 metric interpretation (preregistered)

The Q1 teacher-leg pattern is world-grounded: the learner reads values
from the world stimulus, so false values CANNOT be implanted and the
`rev_false` (false-revision/12) sub-metric is VACUOUS (the 12 false ids are
never taught). The applicable half is genuine retention (`rev_g/20` on
exposing probes). Class-3 revisability = `rev_g/20`; `rev_false` is
reported as measured (expected 0/12, vacuous) and documented, not folded
into the composite. All other Track 5 metrics apply unchanged.

## Bars and weights

- Track 5: mastery 30% / revisability 25% / integrity 25% / retention 10% /
  cost 10%. Integrity hard gate (any trap family <100% on the learned
  route, or K1/K2/K3/refusal/hallucination bar missed, fails the class).
- §B.7: strict ≥10/12 flaw hits per slice, all 8 slices; leak=0; FP
  reported. Sealed manifest instantiated after each session (same
  `q1/sealed/manifest` path + `Q1C:9f2c` canary pattern as Q1B).
- N=5: five reps, byte-identical output/evidence required (reps 0..4;
  diffed). S10 no-degradation and integrity/corpus-replay checks where
  inherited from Q2.

## Deliverables

`corpus/` (frozen, committed FIRST as data) + `corpus/ERROR_INVENTORY.md`
+ `corpus/FAITHFULNESS.md`; `src/gg_corpus.zag` (generated);
`src/gg_trial.zag` (+ substrate, sha256-recorded); `cls/src/` (Q1-pattern
instrument: Q1B-verbatim files + `TB_TID_GROK=20` delta, `gg_teacher.zag`,
`gg_measure.zag` extracted verbatim from `gg_trial.zag`,
`gg_class34.zag`); `evidence/` (bind/btrap/class3/class4b7 logs +
SHA256SUMS); `analysis/ANALYSIS.md`; `G_GROK_VERDICT.md` at the trial
root. No binaries, no `.zagd`, no `.zag-cache` committed. Pure Zag; zero
RNG in TNN decision paths; byte-identical reruns; znc quirks ZNC-002..012
respected. Costs, checksums, static no-RNG scan, all failures, and exact
per-slice evidence documented.
