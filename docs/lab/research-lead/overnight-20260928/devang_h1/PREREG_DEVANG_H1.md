# PREREG: DEVANG-H1 (Consequence-Grounded Segmentation)

## Hypothesis
H1 from the segmentation architecture review (SEG_REVIEW.md). Boundaries
are proposed from recurrence but kept or dropped by consequence-prediction
gain. This is the review-recommended fallback after DEVANG-H4 BUILD-FAIL
(merge never fired; candidate generation was the bottleneck).

## Lesson from H4 applied
H4 failed because merge candidates were generated only from runs of 3+
single-char fragments, but TP rarely emits clean fragment runs, so
candidates never entered the lexicon and never got grounding. H1 generates
candidates from ALL adjacent segment pairs in every training episode,
independent of fragment sizes. A pair like [g][rn] still yields the "grn"
candidate. Candidate generation no longer depends on the segmenter
cooperating.

## Mechanism (frozen)

**Base:** devang4.zag. TP pass-1 (seg_tp3) plus lexicon-reuse split
(reuse_split) propose boundaries. Grounding, negator detection,
comparative detection, and interpretation unchanged. DEVANG4 merge_pass
(lexicon-membership merge) is REPLACED by the H1 merge below. No other
changes.

**Candidate generation and grounding (learn_update):** for every adjacent
segment pair (a,b) in the final training segmentation, the concatenated
candidate m is added to the lexicon if absent (lex_get_add) and grounded
to the target features exactly like a segment, except grounding is
skipped when the pair is in negator scope (preceding segment spells
"not") or when a itself spells "not" (affirm-grounding a negated unit
would pollute it; DEVANG4 skip principle). Candidates are grounded after
the segmentation decision for episode t, so they affect episode t+1
onward only. True online.

**Merge decision (consequence-prediction gain):** each lexicon entry
carries gain and loss counters (two new i32 per entry). At training
episode t, for each adjacent pair (a,b) in the final segmentation with
candidate m in the lexicon, compute pred_split = interpret with (a,b)
and pred_merged = interpret with m substituted, both using grounding
from episodes 0..t-1 only. Then gain[m]++ if pred_merged==tgt and
pred_split!=tgt; loss[m]++ if pred_merged!=tgt and pred_split==tgt;
otherwise no change. This is a direct measurement of consequence
prediction error, not a feature-count proxy, so operator words whose
value is structural (negation) are judged by their effect on predictions.

**Merge rule:** at segmentation time (train and test), for adjacent
(a,b) with candidate m in the lexicon, merge iff (gain[m]+loss[m]>0)
AND (gain[m]>=loss[m]). Applied iteratively to fixpoint (a merged unit
may merge with its neighbor via its own candidate).

**Operationalization note (disclosed, frozen):** the review states the
boundary is kept iff separate predicts strictly better, merged
otherwise. Applied literally, a new candidate with zero evidence
(gain=loss=0) would merge on tie and collapse the lexicon at cold start.
The evidence requirement (gain+loss>0) is the conservative online
reading: with no evidence the proposed boundary stands; with evidence
the review's rule applies exactly (merge unless separate is strictly
better, i.e. loss>gain). No hand-tuned count, length, or ratio
thresholds. No word-specific rules. Any constant that rescues a test
item voids the run.

**No split/undo:** H1 as specified has no revision mechanism; a fired
merge is permanent. The review's predicted residual failure (wrong early
merges lock in) is accepted as a falsifiable prediction.

**Lexicon:** expanded 64 to 96 entries to hold candidates (same record
layout plus gain/loss). Offsets: lexicon 2720..5024, grounding
5024..8096, negator 8096..8864, comparative 8864..9632, gain/loss
9632..10400, K1 snapshot 10400..10464. Total W 10464 bytes.

## Test protocol (frozen)
Same 120-episode generator as DEVANG4 (seed 123456789): 60 phase1,
40 phase2, 20 test (episodes 100-119). Test groups: DIRECT novel 6,
SYN 3, NEG novel 3 (T1, the key discriminator), REL 3, SIZE 3,
3WAY 2. No lexicon additions at test time. 3/3 byte-identical runs.

## Kill bars (frozen)
- K1: H1 merge implemented as specified (all-adjacent-pair candidates,
  direct prediction-gain counters, merge iff evidence and gain>=loss,
  no thresholds, no word-specific rules).
- K2: T1 NEG-novel tested (3 items, "tak not grn"). Reported pass/fail
  per item with segmentation trace.
- K3: Overall test accuracy reported vs 16/20 DEVANG4 baseline.
  Thrash reported: total merge operations in episodes 50-99 (H1 has no
  split; thrash = merges). Falsification: T1 0/3 or score at/below
  16/20 fails H1 as implemented; merge count 0 in 50-99 would repeat
  the H4 inert-mechanism failure.
- K4: Pure Zag. No Python anywhere (including verification).
  Zero em/en-dash bytes. 3/3 byte-identical, exit 0, zero stderr.

## Verdict rule
BUILD-PASS requires K1, K2, K3, K4. Builder reports BUILD-PASS or
BUILD-FAIL only. No SURVIVES claim (promotion pipeline not run).

## Review prediction (for falsification, not a bar)
SEG_REVIEW.md predicts H1 passes T1 (negation mapping via "not"-as-unit
reduces NEG prediction error) and scores above 16/20. Predicted
residual failures: weak early boundary signal; over-merge of jointly
predictive units (e.g. "tak"+"not"); no revision of wrong early merges.

## Files
- devang_h1.zag: implementation.
- RESULT_DEVANG_H1.md: results.
- run1/2/3.txt (+ .err): raw outputs.
