# JUDGE_BRIEF.md - F1 windowed failure-density trigger wave

Provenance:
- RENDER_SHA: 3b159b401 (sealed evaluation commit; prereg 50de69403,
  implementation ba5ebbf8b, all on branch tnn-native-lab, local only)
- FIRST_RENDERED_WAVE: wave-20261001-2321pdt
- COMPONENT_LINEAGE: F1 BUILD-FAIL on consecutive-failure trigger
  (wave-20261001-2021pdt; K-C0C TRIP on W1 15/30, K1=2 trigger never
  fires on interleaved errors)
- NEW_KNOWLEDGE_CLAIM: A windowed failure-density trigger (fire when at
  least 2 of the last 8 truth-episodes are prediction failures) is a
  strict generalization of the consecutive-failure trigger that lets the
  learner discover EQ-gate structure from interleaved error streams at
  100 percent hidden accuracy with zero false positives on clean worlds,
  while exactly preserving previously passing behavior.

## Verdict: BUILD-FAIL

Governing bars (frozen in PREREG_TRIG.md, committed alone at 50de69403
before any implementation existed):

PASS:
- K-TRIG-FIRE: trigger fires within 12 episodes on all four sealed
  interleaving patterns (T-A alternating ep 2; T-B 1-in-3 ep 3;
  T-C 1-in-4 ep 4; T-D bursty ep 1). The old trigger fires on none.
- K-TRACE: 2+ episode-indexed construction events per pattern
  (3, 2, 2, 6).
- K-LEARN-INTERLEAVED: 30/30 hidden on all four patterns (bar: 80%).
  The learner discovers EQ r0,f0,f1 then ADD r0,r0,r0 from interleaved
  streams.
- K-TRIG-CLEAN: 0 triggers on all three clean worlds (frozen rate 0).
- K-C0C-REG on R-W3: 30/30 on the 2x->4x law-change family, 2+
  construction events, STALL/TRIGGER dynamics preserved.
- K-ABL-TA: 57pp drop when the structure is removed (bar: 40pp).
- K-BASE-TA: 57pp margin over the exact-match memorizer (bar: 40pp).
- K-C0A: zero forbidden semantic sites in the frozen source.
- NC-TRIG: the prior wave's frozen binary produces 0 triggers on
  sealed T-A, reproducing the W1 defect; the battery discriminates.
- Determinism: 22 invocations x 3 repetitions, all byte-identical.

TRIP (killing bar):
- K-C0C-REG on R-W2: 0/30 hidden (bar: 80%). The greedy depth-1 trial
  overfits sealed seed 2301 to
  [ADD r0,f1,f1; ADD r0,r0,f1; ADD r0,r0,f0; ADD r0,r0,f0].
  The prior wave's binary fails identically on the same fixtures
  (same structure, 0/30): pre-existing constructor seed-sensitivity,
  not a trigger regression. The new binary reproduces the prior
  wave's W2 exactly (same trigger episode, same 3 constructs, 30/30,
  identical structure), proving zero trigger regression.

## What the judge should know

1. The trigger is the deliverable and it works: every trigger-specific
   bar passes, the mechanism is generic (monitors only the learner's
   own binary error stream; no semantic cases added), and the audit is
   clean.
2. The BUILD-FAIL comes from a bar-calibration mistake in this lane's
   own prereg: K-C0C-REG used a fresh seed for the regression family
   without validating that the constructor (unchanged, greedy,
   seed-sensitive) could solve that seed. The bar conflated trigger
   regression with constructor robustness.
3. Recommended coordinator actions: (a) accept the windowed trigger as
   the fixed failure monitor (it strictly generalizes the old one and
   all trigger bars pass); (b) file the constructor's greedy-trial
   seed-sensitivity (sum3 and rW2 overfits, both reproduced by the old
   binary) as a separate finding for the constructor, not the trigger;
   (c) if a re-run is ordered, use the prior wave's exact W2 fixtures
   for the regression leg rather than a fresh seed.

Evidence paths (all under
docs/lab/rsi/runs/wave-20261001-2321pdt/F1/):
- PREREG_TRIG.md (frozen bars, fixture hashes)
- impl/f1_learn.zag, impl/f1_isa.zag; frozen binary impl/f1_learn
  (sha256 6f2b155b233a95ad1a8323e8565b9a798dc822db6eff57e065b71b5be8882847)
- IMPLEMENTATION.md, SEALED_EVAL.md
- sealed/ (fixtures, run_sealed.sh, score.zag, runs/1..3,
  DETERMINISM_SHA256.txt)

No em-dashes in this document. Bounded L2+ ceiling stands; no L3 claim.
