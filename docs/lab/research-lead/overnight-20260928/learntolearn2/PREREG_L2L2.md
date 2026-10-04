# PREREG_L2L2.md - Learning-to-Learn Minimal Transfer (retry, focused scope)

Status: PREREGISTRATION. Frozen before any implementation. Two task families, shared latent
structure, different surfaces. Tighter scope than the first I2 attempt (two families only).

## Design

Latent structure: a fixed-offset mapping. Family A: pairs (x, x + kA) with kA = 3,
inputs x in {1..10}, surface labeled "family A". Family B: pairs (x, x + kB) with kB = 7,
inputs x in {11..20}, surface labeled "family B". Different symbols, different offset
value, same latent rule form: output = input + one unknown constant.

Learner: online predictor. Before seeing each answer, it predicts the output for the
given input, then records the error. State: (a) a memorized table of seen pairs,
(b) one retained hypothesis "offset = k" (initially unknown), (c) a flag whether the
offset hypothesis is trusted.

Mechanism: on the first few examples, the learner cannot fit a single offset, so it
falls back to nearest-seen memorized pairs (slow, many errors). Once it has seen at
least 3 consistent pairs, it solves the offset k from differences, stores it as the
retained hypothesis, and trusts it (predicts x + k). Because the offset is trusted
state, family B starts by testing the offset hypothesis immediately: it fits kB from
the first 2 examples of B and predicts the rest correctly.

## Validity bars (kill bars)

- P1 TRANSFER: examples-to-criterion (8/10 consecutive correct) on family B is
  strictly fewer than on family A, by at least 2 examples.
- P2 NO-PSEUDO-TRANSFER: the same family B presented to a fresh learner with no
  retained state must NOT be faster than family A for the original learner. This
  rules out "B is just easier".
- P3 CAUSAL TRACE: the transferred state is named in the code and visible in the
  output trace: `offset_hyp=k, trusted`. Ablating that state (run B with trusted=0,
  offset_hyp=unknown) must slow B back to approximately the A speed. If B stays fast
  after ablation, P3 fails.
- P4 DETERMINISM: 3/3 runs byte-identical, exit 0, zero stderr.
- P5 GOVERNANCE: pure Zag, zero Python at every stage, zero em-dash bytes in docs.

## Verdict rule

BUILD-PASS iff P1, P2, P3, P4, P5 all pass. BUILD-FAIL otherwise. This is bounded
learning-to-learn (L1/L2), not L3: the hypothesis form (fixed offset) is supplied by
the researcher; only the constant is learned. Report honest classification.

## Files

- l2l2.zag : learner + families + ablation switch
- L2L2_RAW.txt : raw output (3 runs)
- L2L2_RESULT.md : result report
