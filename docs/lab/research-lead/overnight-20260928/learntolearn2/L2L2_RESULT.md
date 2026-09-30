# L2L2 Result: Minimal Learning-to-Learn (retry, focused scope)

Verdict: BUILD-PASS (5/5 kill bars). Bounded learning-to-learn, honest L1/L2 scope.

## Numbers

- Family A (offset 3, inputs 1-20): 13 examples to 8 consecutive correct.
- Family B (offset 7, inputs 21-40), with retained state: 10 examples (3 fewer).
- Family B fresh (no retained state): 13 examples (same as A).
- Ablation (B with form_known forced 0): 13 examples (back to A speed).

## Kill bars

- P1 TRANSFER: PASS. B(10) < A(13), difference 3 >= 2.
- P2 NO-PSEUDO-TRANSFER: PASS. Fresh B(13) is not faster than A(13); B is not
  intrinsically easier.
- P3 CAUSAL TRACE: PASS. Transferred state is `form_known` (set when offset
  fitting first succeeded in A) plus `offset_hyp`/`trusted`. Forcing form_known=0
  slows B back to 13. Transfer is causally traced to retained state.
- P4 DETERMINISM: PASS. 3/3 byte-identical, exit 0. stderr carries only the
  standard toolchain availability warning, no program errors.
- P5 GOVERNANCE: PASS. Pure Zag, zero Python at every stage, zero em-dash bytes.

## Mechanism trace

In A, the learner runs 4 examples of pure memorization (nearest-seen) before
attempting offset fitting; offset 3 is discovered at example 5 and trusted from
example 6. In B with retention, the learner predicts with the retained offset 3
on example 1, detects the mismatch (d=7 vs 3), distrusts, refits offset 7 from
2 consistent new differences, and is correct from example 3. The speedup comes
from knowing the offset hypothesis form is viable (form_known=1), skipping the
4-example memorization preamble.

## Honest classification

Bounded learning-to-learn (L1/L2), not L3. The hypothesis form (fixed offset) is
researcher-supplied; only the constant and the trust flag are learned. The
transfer is real but small (3 examples) and within a single supplied form. This
is a clean minimal demonstration of state-dependent learning speed, with causal
ablation, nothing more.

## Files

- PREREG_L2L2.md (4b4c8c345, strict ancestor of implementation)
- l2l2.zag
- L2L2_RAW.txt (md5 63f42ff213f0a8ebf6e9253b72114327)

Commits: prereg 4b4c8c345; implementation + raw + result (this wave).
