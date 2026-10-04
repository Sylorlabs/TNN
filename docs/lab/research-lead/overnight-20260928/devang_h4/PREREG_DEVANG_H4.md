# PREREG: DEVANG-H4 (Multi-level Revisable Chunks)

## Hypothesis
H4 from the segmentation architecture review (SEG_REVIEW.md, commit
9cef7f9d4). Chunks live in a hierarchy and boundaries are revisable.
Segmentation and grounding are mutually causal in both directions.

## Mechanism (frozen)

**Split rule:** a chunk splits when its fragments develop independent
grounding records. Operationalized as: for a segment of length > 1,
try every split point into (a, b); split at the first point where
both fragments are in the lexicon, each fragment's best-feature count
strictly exceeds the whole chunk's best-feature count, and the two
fragments' best features differ.

**Merge rule:** adjacent segments merge when their conjunction
predicts a consequence feature better than either alone.
Operationalized as: for adjacent segments (a, b) with merged
candidate m in the lexicon, merge iff m's best-feature count strictly
exceeds both a's best-feature count and b's best-feature count.
Applied iteratively to fixpoint.

**Treadmill guard:** both criteria are strict prediction-gain
comparisons (count > count). No hand-tuned count, length, or ratio
thresholds. No word-specific rules. Any constant that rescues a test
item voids the run.

**Pair grounding:** in learn_update, after grounding individual
segments, adjacent segment pairs are added to the lexicon as merge
candidates and grounded to the target features. This gives merged
candidates the grounding records the merge rule needs. True online:
candidates are grounded after the segmentation decision for episode t,
so they affect episode t+1 onward only.

**Base:** devang4.zag (commit d9ebbfe6d) with merge_pass and
reuse_split replaced by the H4 merge/split passes. TP pass 1,
grounding, negator detection, and interpretation unchanged.

## Test protocol (frozen)
Same 120-episode generator as DEVANG4 (seed 123456789): 60 phase1,
40 phase2, 20 test (episodes 100-119). Test groups: DIRECT novel 6,
SYN 3, NEG novel 3 (T1, the key discriminator), REL 3, SIZE 3,
3WAY 2. No lexicon additions at test time. 3/3 byte-identical runs.

## Kill bars (frozen)
- K1: H4 split/merge implemented as specified (prediction-gain
  comparisons only, no thresholds, no word-specific rules).
- K2: T1 NEG-novel tested (3 items, "tak not grn"). Reported
  pass/fail per item with segmentation trace.
- K3: Overall test accuracy reported vs 16/20 DEVANG4 baseline.
  Thrash rate reported: total merge+split operations in episodes
  50-99. Falsification per review: (a) thrash indicates instability;
  (b) T1 fails despite correct "not" segmentation means the
  root-cause claim is wrong; (c) score at or below 16/20 fails H4.
- K4: Pure Zag. No Python anywhere (including verification).
  Zero em/en-dash bytes. 3/3 byte-identical, exit 0, zero stderr.

## Verdict rule
BUILD-PASS requires K1, K2, K3, K4. Builder reports BUILD-PASS or
BUILD-FAIL only. No SURVIVES claim (promotion pipeline not run).

## Files
- devang_h4.zag: implementation.
- RESULT_DEVANG_H4.md: results.
- run1/2/3.txt (+ .err): raw outputs.
