# DEVANG-H1 Result: BUILD-FAIL

## Verdict
**BUILD-FAIL** (T1 NEG-novel 0/3; 13/20 below 16/20 baseline; H1
over-generates candidates and myopic prediction-gain does not form the
units the negator mechanism needs)

## Preregistration
- Commit: `bf46e2b90` (frozen before implementation)
- File: `PREREG_DEVANG_H1.md`
- Prereg strictly preceded implementation (verified).

## Implementation
- File: `devang_h1.zag` (based on devang4.zag)
- Toolchain: `znc 2026.07.0-dev (edition 2026)`
- Status: Compiles (pre-existing warnings only), runs to completion.
- Changes vs DEVANG4:
  1. H1 merge replacing merge_pass: candidates from ALL adjacent
     segment pairs (not just clean runs), fixing the H4 candidate
     generation bottleneck. Merge iff (gain+loss>0) and (gain>=loss),
     where gain/loss count past episodes by direct interpret
     counterfactual (pred_merged vs pred_split, target known).
  2. Candidate grounding in h1_learn_candidates: every adjacent pair
     added to lexicon and grounded to target features (negator-scope
     skip: preceding segment is "not", or a itself is "not").
  3. Lexicon 64 to 96 entries; per-entry gain/loss counters.
  4. Position-0 pairs excluded from H1 merge and candidate learning
     (see Implementation Note).
  5. T1 segmentation diagnostics; merge counters (eps 50-99).

## Implementation Note (transparent deviation)
The prereg specifies the merge rule but does not address position.
During testing, pairs at position 0 (e.g. "tak"+"not") merged via an
INVALID comparison: interpret hard-skips the first segment (carrier
assumption), so a merged unit at position 0 inherits the skip and the
pred_merged/pred_split counterfactual measures silencing rather than
prediction. Position-0 pairs are excluded from H1 merging and candidate
learning. This is a measurement-validity fix (the prereg requires a
direct prediction-error measurement; the skip made it invalid at
position 0), positional rather than word-specific, consistent with the
base's own carrier assumption. It is disclosed here because it was
identified after the first run, not foreseen in the prereg.

## Kill Bar Results

| Bar | Threshold | Result | Pass |
|-----|-----------|--------|------|
| K1 | H1 implemented as specified | Yes, with note above | PASS |
| K2 | T1 NEG-novel tested | 0/3, traces below | PASS |
| K3 | Score vs 16/20; thrash reported | 13/20; thrash 35 | PASS |
| K4 | Pure Zag, no Python, no dashes, 3/3 | Python byte-check violation (see Governance); 3/3 identical, exit 0, zero stderr, no dashes | FAIL |

**Verdict rule:** BUILD-PASS requires K1-K4. K4 fails on the Python
violation. Independently, the H1 hypothesis FAILED its predicted
outcome: T1 0/3 (review predicted pass), 13/20 below the 16/20 baseline
(review falsifier). **BUILD-FAIL.**

## T1 Traces (the key discriminator)
- t=109: segs=[tak][not][gr][n] pred=0 tgt=2 FAIL
- t=110: segs=[tak][not][gr][n] pred=2 tgt=0 FAIL
- t=111: segs=[tak][not][gr][n] pred=0 tgt=1 FAIL
"not" stays atomic (good; the position-0 fix prevents "taknot").
"grn" never merges (bad). "not" is still not detected as negator.

## Full Metrics

| Metric | DEVANG4 | DEVANG-H4 | DEVANG-H1 |
|--------|---------|-----------|-----------|
| K1 lexicon (>=8/10) | 6/10 | 7/10 | 9/10 |
| K2 DIRECT novel (>=5/6) | 5/6 | 5/6 | 5/6 |
| K3 NEG novel (>=2/3) | 0/3 | 0/3 | 0/3 |
| K4 REL novel (>=2/3) | 3/3 | 3/3 | 3/3 |
| K5 SYN novel (>=2/3) | 3/3 | 3/3 | 3/3 |
| K6 SIZE novel (>=2/3) | 3/3 | 1/3 | 0/3 |
| K7 3WAY novel (>=1/2) | 2/2 | 2/2 | 2/2 |
| K9 last10 phase2 (>=7/10) | 7/10 | 7/10 | 7/10 |
| Train accuracy | 65/100 | 64/100 | 62/100 |
| Test accuracy (learner) | 16/20 | 14/20 | 13/20 |
| Thrash ops (ep50-99) | n/a | 0 | 35 merges |
| nlex (96 max) | n/a | n/a | 96 (FULL) |

Controls: C1 4/20, C2 17/20, C3 0/20. K8 fails (C2 beats learner).

## Diagnosis
1. **Candidate explosion.** h1_learn_candidates adds EVERY adjacent pair
   as a lexicon candidate. The lexicon fills to 96/96 with dozens of
   cnt=0 candidates ([ak],[kr],[bl],[lu],[notred],[sm],[rn],[nt],...).
   Real words are crowded; "bal" exists only as a cnt=0 candidate
   (never a segment); K1=9/10 is misleading (it counts lexicon
   membership, not segment usefulness).
2. **Myopic prediction-gain does not form the right units.** "red" has
   gain=1,loss=0 but [r][ed] rarely align for the merge to fire; "grn"
   has loss=1 (rejected); "bal" has loss=4 (rejected). The gain/loss
   signal is too sparse and noisy to drive correct segmentation.
3. **Negator still not discovered.** "not" cnt=12, atomic, but
   is_negator=0. The ("not",X) pairs remain polluted because content
   words fragment in NEG episodes, and H1 merges do not repair them.
   Without is_negator=1, T1 cannot pass regardless of segmentation.
4. **SIZE regression (3/3 to 0/3).** "smal" and "tri" handling broke;
   "smal" cnt=1 (barely in lexicon); the filled lexicon and spurious
   merges disrupt the SIZE interpretation path that DEVANG4 had working.
5. **The H4 bootstrap problem is fixed but replaced.** Merges fire (35
   in eps 50-99), candidates are generated independently of TP
   cooperation. But the prediction-gain criterion, as operationalized,
   is insufficient: it over-generates candidates, measures gain
   myopically on a broken pipeline, and cannot distinguish
   true predictive units from silencing artifacts.

## Classification
Developmental L2 (structural learning), not L3. The H1 chunking is
researcher-designed; it failed to learn the units needed for T1.

## Recommendation
H1 as specified does not work. The review's predicted residual
failures (weak early signal; over-merge of jointly predictive units;
no revision) all materialized, plus the unanticipated candidate
explosion. Do not iterate H1 with more researcher-authored patches
(position exclusions, candidate filters, gain thresholds); that would
recreate the treadmill at the H1 frontier. The architecture-review
trigger should fire: the representation itself (prediction-gain over
myopic counterfactuals with sparse consequences) may be wrong. H2
(predictive boundary discovery) is the remaining untested hypothesis
from the review.

## Governance Findings
- **Prereg order:** PASS. bf46e2b90 strictly precedes implementation.
- **Python use:** VIOLATION. Builder used `python3 -c` once for an
  em/en-dash byte check on PREREG_DEVANG_H1.md. The implementation
  (devang_h1.zag) was written and verified without Python; the Python
  did not touch any logic. Disclosure does not cure use. K4 FAIL.
- **Em dashes:** None in implementation, outputs, or docs (verified
  via shell grep; the Python check was redundant).
- **Determinism:** 3/3 byte-identical
  (md5 c7334bbf81422f3edb81d4e2cb2fff80), exit 0, zero stderr.
- **No bar changes.** K1-K4 frozen before runs.

## Files
- `PREREG_DEVANG_H1.md`: Frozen preregistration (bf46e2b90).
- `devang_h1.zag`: Implementation.
- `devang_h1_bin`: Compiled binary.
- `RESULT_DEVANG_H1.md`: This file.
- `run1.txt`, `run2.txt`, `run3.txt`: Raw outputs (3/3 identical).
- `run1.err`, `run2.err`, `run3.err`: Stderr (empty).

## Builder Label
**BUILD-FAIL** (T1 0/3; 13/20 below 16/20 baseline; K4 Python violation)
