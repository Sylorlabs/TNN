# DEVANG2 Result: BUILD-FAIL

## Verdict
**BUILD-FAIL**

## Preregistration
- Commit: `402e53d32`
- File: `PREREG_DEVANG2.md`
- Prereg strictly preceded implementation.
- Note: Prereg layout documentation corrected post-freeze for arithmetic
  error (6304+512=6816, not 6560). Kill bars, world design, and learner
  specification unchanged. Implementation follows corrected layout.

## Implementation
- File: `devang2.zag`
- Toolchain: `znc 2026.07.0-dev (edition 2026)`
- Status: Executes to completion. No crashes.
- Fixes vs DEVANG1:
  1. Lexicon entries expanded to 24 bytes (16-char string field).
  2. Bounds check in lex_add (rejects len > 16).
  3. Memory layout corrected (neg_tot/cmp overlap fixed).
  4. K1 measured at t=60 via in-loop snapshot.

## Kill Bar Results

| Bar | Threshold | Result | Pass |
|-----|-----------|--------|------|
| K1 | 8/10 words by end phase 1 | 3/10 | FAIL |
| K2 | DIRECT novel 5/6 | 5/6 | PASS |
| K3 | NEG novel 2/3 | 1/3 | FAIL |
| K4 | REL novel 2/3 | 3/3 | PASS |
| K5 | Synonym novel 2/3 | 1/3 | FAIL |
| K6 | SIZE novel 2/3 | 3/3 | PASS |
| K7 | 3-way composition 1/2 | 0/2 | FAIL |
| K8 | Beat best control by 15pp | 0 (13 vs 17) | FAIL |
| K9 | 7/10 on final ten phase-2 | 6/10 | FAIL |
| K10 | Strict online audit | PASS (by inspection) | PASS |
| K11 | Episode t excluded from own bigram | PASS (by inspection) | PASS |
| K12 | 3/3 byte-identical runs | PASS (md5 f184c2683dd28550f738f63f7e1c8615) | PASS |

**Sub-bars K2..K7,K9:** 3/7 (need >= 4). FAIL.

**Verdict rule:** BUILD-PASS requires K1, K8, K10, K11, K12 plus at
least 4 of {K2..K7, K9}. K1 FAIL, K8 FAIL, sub-bars 3/7 FAIL.
**BUILD-FAIL.**

## Additional Metrics
- Train accuracy: 43/100
- Test accuracy (learner): 13/20
- C1 (no-seg): 4/20
- C2 (fixed-width-3): 17/20
- C3 (substring): 0/20

## Root Cause Analysis

The implementation is memory-safe (no crashes), but the bigram DP
segmentation fails to discover word boundaries. Observed: nseg=1 for
early episodes, with whole 9-char utterances (e.g., "takredbal") stored
as single lexicon entries instead of segmenting into "tak"+"red"+"bal".

The length-averaged scoring (disclosed deviation from prereg) does not
solve the fundamental problem: with zero bigram counts at t=0, all
segmentations score equally, and the DP defaults to single segments.
The learner never recovers because the lexicon fills with whole
utterances, and grounding cannot map them to features.

C2 (fixed-width-3) scores 17/20, beating the learner's 13/20. The
segmentation is the bottleneck, not the grounding or interpretation.

## Online Audit (K10, K11) by Code Inspection
- **K10**: Training loop segments episode `t` using bigram counts from
  episodes `0..t-1` only. `learn_update` is called AFTER `seg_dp` and
  `interpret`. Test episodes (100..119) do not call `learn_update`.
  **PASS by inspection.**
- **K11**: Bigram counts are updated in `learn_update`, which runs after
  segmentation. Episode `t`'s bigrams are not in W during its own
  segmentation. **PASS by inspection.**

## Governance Findings
- **Prereg order**: PASS. Prereg commit `402e53d32` strictly precedes
  implementation.
- **Python use**: None. Pure Zag implementation.
- **Em dashes**: None in source or documentation (verified via od).
- **Scoring deviation**: RETAINED from DEVANG1 (length-averaged vs
  sum-of-logs). Disclosed in prereg section 2.
- **K1 timing**: FIXED. Measured at t=60 via in-loop snapshot.

## Classification
Developmental L2 (structural learning attempt), not L3. The mechanism
(bigram DP segmentation, grounded lexicon, learned negator/comparative)
is researcher-designed; the learner fills parameters. No representational
invention claimed.

## Comparison with DEVANG1
- DEVANG1: BUILD-FAIL (crash, no output).
- DEVANG2: BUILD-FAIL (runs, but segmentation fails to discover words).
- Progress: Memory safety achieved. Mechanism failure isolated to
  segmentation design, not implementation bugs.

## Files
- `PREREG_DEVANG2.md`: Frozen preregistration (commit 402e53d32).
- `devang2.zag`: Implementation (memory-safe, mechanism fails).
- `RESULT_DEVANG2.md`: This file.
- `DEVANG2_RAW.txt`: Raw output (3/3 identical).

## Builder Label
**BUILD-FAIL**
