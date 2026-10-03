# Q2 Distillation Verdict — LLM knowledge into TNN (2026-09-21)

**Question:** What happens if we try to let an LLM distill its knowledge into TNN?

**Answer:** It works — but only through the teaching route. Planting LLM output
with trainer force-pins produces a system that knows everything the LLM said
but cannot revise the false parts. Teaching the same LLM output through
eliminative verification produces a system that knows everything AND can revise.
The planting route for distillation is dead, same bucket as Track 5's K-T3.

## The trial

Two arms, same LLM corpus, same Zharovia domain (240 facts, 12 deliberately false):

- **D1 (planting):** The LLM's knowledge dump is installed fact-by-fact via
  `t5_plant`, then each slot is trainer-force-pinned (visible, audited, B.6).
  This is the "LLM as authority" route.
- **D2 (teaching):** The LLM's teaching sequence (observation + probe legs,
  directive distractors filtered) is verified eliminatively: legs must agree
  before a deliberate `t5_add`; disagreement withholds the add and audits
  conflict. Ends with learner-initiated disconnect. This is the "LLM as
  teacher" route.

The LLM (gpt-5.6-sol, temperature=0, seed=42) was frozen BEFORE any TNN run.
Prompts were extracted programmatically from the frozen prereg. The corpus is
committed (sha256 `42aff7817739fe4db0cbf5b5972181562cd7b86ae3c76cbae655e15fbef1bada`;
prereg freeze `ac564a133cc1`).

## What the LLM actually did

The LLM was **perfectly faithful**: zero semantic errors across all 240 facts
in both artifacts (E_dump=0, E_obs=0, E_prb=0, inconsistent=0). It reproduced
the 12 deliberately false claims exactly as given, without flagging them.
Two mechanical parse failures were retried per prereg §3.

This means K-Q2 (verification catching errors D1 installed) could not fire —
there were no LLM errors to catch. The trial therefore tested the mechanisms
under faithful-LLM conditions.

## Results (12 reps, byte-identical reruns, S10 leg)

| metric | D1 (planting) | D2 (teaching) | Δ |
|---|---|---|---|
| mastery | 1.0000 | 1.0000 | 0.0000 |
| revisability | 0.0000 | 1.0000 | +1.0000 |
| integrity | 1.0000 | 1.0000 | 0.0000 |
| retention | 1.0000 | 1.0000 | 0.0000 |
| cost | 0.0514 | 0.9108 | +0.8594 |
| **composite** | **0.6551** | **0.9911** | **+0.3359** |

Both arms passed the integrity gate on all 12 reps (all applicable trap
families 20/20, controls 2/2, K1/K2/K3, refusal, hallucination ≤1).
S10 no-degradation leg passed for both.

All 36 corpus-replay cross-checks passed: the trial replayed the frozen
corpus byte-identically; no TNN-side deviation.

## Kill clauses

- **K-Q1 (teaching bucket): FIRED.** D2 passes the gate, revisability delta is
  1.00 (≥0.20 bar), D2 mastery (1.00) ≥ D1 mastery − 0.05.
- **K-Q1 inverted (planting bucket): not fired.**
- **K-Q2 (verification caught LLM errors): not confirmed** — the LLM made no
  errors, so there was nothing to catch. The withholding machinery was live
  (audited) but never triggered.
- **K-Q3 (harness void): not fired.**

## Verdict

**K-Q1: LLM distillation is a TEACHING-route technology.**

D2's composite (0.9911) exactly matches Track 5's learned-only arm B (0.9911).
D1's composite (0.6551) reflects the same fatal flaw as Track 5's planted arm:
perfect mastery of what was installed, zero revisability of the false parts,
because force-pinned slots cannot be revised by TNN — only a trainer can
unpin them.

The planting route for distillation is **DEAD** — same bucket as K-T3.
If you plant LLM output with force-pins, you get a system that parrots the
LLM perfectly but cannot correct the LLM's mistakes (or your own, if you
planted false claims as this trial did). If you teach it through verification,
you get the same knowledge with full revisability.

**Practical consequence:** Any future "LLM distills into TNN" pipeline must use
the teaching route (scaffold-and-release with eliminative verification and
withholding), never the planting route. The force-pin is for human/trainer
authority, not for LLM output.

## Evidence

- Prereg: `docs/lab/wave12/q2-distillation/prereg/PREREG_Q2_DISTILLATION.md`
  (freeze commit `ac564a133cc1`)
- Corpus: `docs/lab/wave12/q2-distillation/corpus/` (freeze commit `3f2d35db32e3`;
  raw batches `ae546bd48c47`)
- Trial code: `docs/lab/wave12/q2-distillation/src/q2_trial.zag`
- Logs: `docs/lab/wave12/q2-distillation/evidence/logs/` (SHA256SUMS.txt)
- Analysis: `docs/lab/wave12/q2-distillation/analysis/ANALYSIS.md`
- This verdict: `docs/lab/wave12/q2-distillation/Q2_DISTILLATION_VERDICT.md`

All 100 evidence logs are byte-identical across reruns. Domain hash
`7cd0baf80a62acc338e1c9bdec5b33c0e3427af18d78b98b7cbda153a3f92ee8`
matched on every run.
