# REDTEAM_SELF.md - DEVANG6 Adversarial Self Review

## Attack A: The learner retrieves/replays supplied templates rather than constructing language structure.

Claim under test: FINREG/POSSEG constructs segmentation from the learner's own
experience, not from researcher-supplied templates.

Evidence for construction:
- FIN_* statistics are accumulated from the learner's OWN chosen segmentations
  during training (mode_segb trains on 100 Family A episodes with the learner
  segmenting, then freezes). No template of Family B or C vocabulary is supplied.
- The developmental r schedule (r grows with experience) means early
  segmentations are made with weak statistics; the final lexicon reflects the
  learner's history, not a supplied answer.
- E-prime uses FRESH tuples (cubqa/redzo/blufi/cubwe/redhu/bluja) with DEVANG5
  role-matched scene prefixes. The learner scores 6/6 on never-before-seen
  lexical items. A retrieve/replay mechanism would have no template to replay.
- K_ABL leg 1 (gap 7 >= 4): the ablation (fixed-3, no learning) scores 5/12
  while the learner scores 12/12. If the learner were replaying a supplied
  template, the ablation (which has the same "supplied" nothing) would not
  systematically underperform by 7 points.

Counter-consideration: the scene generators DO supply the compositional
structure (which words go with which scenes). The learner does not invent the
mapping from scratch; it discovers it from co-occurrence. This is L2
structural learning (TNN constructs relationships from generic mechanisms),
not L3 representational invention. The prereg does not claim L3.

Verdict: Attack A FAILS to kill. Construction (L2) is genuine; L3 is not
claimed.

## Attack B: Break the old-language impossibility proof.

The prereg contains a fixed-point argument: on the old language, a wrong
analysis wins lexicon 40+20-55=5 vs 40-55+10=-5, ties margin 2v2; no
reweighting of old signal classes escapes.

Attack: the proof assumes the signal classes are fixed. Could a learner
invent a NEW signal class (not a reweighting) that breaks the fixed point?
The proof covers reweightings of OLD signal classes. A genuinely new signal
(e.g., one that detects the old language's hidden regularity) is outside the
proof's scope.

Response: correct, the proof is scoped to reweightings. But inventing a new
signal class that cracks the old language IS the L3 achievement the proof
demands as the alternative. The proof's job is narrower: to show that
parameter-tuning within the old vocabulary cannot succeed, forcing any
success to come from genuine structural invention. The proof holds in its
scope; the escape hatch it leaves open is exactly the capability being tested.

Verdict: Attack B FAILS to break the proof in-scope; it correctly identifies
the proof's boundary, which is the intended L3 criterion.

## Attack C: "The recalibrated K_ABL was chosen to make DEVANG6 pass."

This is the most dangerous attack: the recalibration could be post-hoc
rationalization.

Counter-evidence (the four honesty arguments, frozen in RECALIBRATION_K_ABL.md
before any DEVANG6 implementation):
1. The gap is the direct measure of load-bearing (purpose-fit). An ablation
   bar should measure what the ablation removes, which is the DIFFERENCE the
   mechanism makes, not the null's absolute score.
2. The new bar is STRICTER against non-load-bearing front-ends. Old bar passed
   learner 6/12 + ablation 5/12 (gap 1); new bar FAILS that (gap 1 < 4). The
   recalibration makes it HARDER for a vacuous mechanism to pass, not easier.
3. The threshold (4) sits 2 points below the observed DEVANG5 gap (6):
   documented anti-fit margin, not fit-to-data.
4. Calibrated on old data, decided on fresh data. The bar was frozen before
   B-tripleprime existed.

Decisive fresh-data test: on B-tripleprime, the gap is 7 >= 4 (PASS with
3 points of slack). The bar discriminated correctly on unseen data. Moreover,
the OLD bar (<= 5/12) would ALSO have passed here (5 <= 5, exactly at bar),
so the recalibration did not manufacture this pass; both bars agree on this
draw, and the new bar is the one that would have FAILED the vacuous
DEVANG5-style outcome.

Verdict: Attack C FAILS. The recalibration is validated, not self-serving.

## Attack D: Metric gaming / fabrication.

Check: were any numbers fabricated, cherry-picked, or computed with buggy tools?

- The floorcheck miscompile (FLOOR 12/12 reported, true 7/12) was a genuine
  compiler defect, NOT fabrication: it was CAUGHT by the lemma contradiction
  (12/12 floor vs 5/12 ablation inconsistent with fixed-3 lemma), isolated via
  synthetic repros, root-caused to `!(A && B)` in while conditions, fixed via
  De Morgan, verified on known-answer synthetic data, and re-measured. The
  corrected 7/12 is exactly consistent with the ablation's 5/12. A fabrication
  would not have been caught by its own consistency check.
- All sealed runs 3/3 byte-identical, zero stderr, hashes pre-verified.
- The K_SEAL failure (9/20) is reported honestly despite killing the build.
  A metric-gamer would have re-tuned the bar or hidden the draw.
- Commit-order self-check: prereg (bda385c32) strictly before implementation
  (f541f16e3). Verified below.

Verdict: Attack D FAILS. No gaming; the kill is reported.

## Attack E: The K_SEAL failure is bar-miscalibration, not a mechanism result.

Argument: C-tripleprime was made harder (prefix ambiguity) than the
calibration family (C-doubleprime), so 12/20 is an unfair bar.

Response:
- The bar (12/20) was frozen before C-tripleprime existed. It measures the
  right quantity (fresh-vocab accuracy).
- The prefix ambiguity was an intentional adversarial stress, disclosed in
  the generator. Adversarial is the point of K_SEAL.
- The deeper pattern (learner <= C2 on ALL three C-families: 12v14, 14v14,
  9v11) shows the mechanism adds no value on all-novel vocabulary regardless
  of the ambiguity stress. This is a capability gap, not a threshold error.
- The draw variance (12, 14, 9) IS a legitimate caveat: single-draw estimates
  are noisy. But noisy measurement of a real gap is not miscalibration; it
  motivates multi-draw calibration in a future wave, not retroactive
  bar-lowering now.

Verdict: Attack E FAILS to overturn the kill. The failure stands as a
mechanism result with a noted variance caveat.

## Attack F: The E-prime 6/6 is memorization of the 6 frozen lines.

The 6 E-prime lines are frozen (not sealed). Could the learner have memorized
them? The learner never sees E-prime during training (it trains on Family A,
then is probed on E-prime with no updates). The tuples are fresh
(cubqa/redzo/blufi/cubwe/redhu/bluja) and did not exist when the mechanism
was written. Memorization would require the answers to be in the binary;
the binary is byte-identical to DEVANG5's, which predates the E-prime tuples.
K_DISC holds.

Verdict: Attack F FAILS.

## Summary

All six attacks fail to kill the reported results. The BUILD-FAIL (K_SEAL)
stands as an honest mechanism result. The recalibrated K_ABL stands as a
validated bar. The floorcheck incident is resolved and documented.
