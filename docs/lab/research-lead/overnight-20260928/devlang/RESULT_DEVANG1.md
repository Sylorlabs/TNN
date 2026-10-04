# DEVANG1 Result: BUILD-FAIL

## Verdict
**BUILD-FAIL**

## Preregistration
- Commit: `e23627a40`
- File: `PREREG_DEVANG1.md`
- Prereg strictly preceded implementation.

## Implementation
- File: `devang1.zag` (committed as evidence of attempt)
- Toolchain: `znc 2026.07.0-dev (edition 2026)`
- Status: Does not execute to completion. Panics with "slice index out of bounds" during training.

## Defects Identified

### 1. Lexicon string field overflow (FIXED, then regressed)
- Original layout: 8 bytes for string content per lexicon entry.
- Utterances up to 9 chars ("takredbal") overflowed, with length byte overwriting 9th char.
- Symptom: `lex_find` failed to match identical utterances; `nlex` grew to 31 after 31 episodes instead of ~8.
- Fix attempted: Expanded to 24-byte entries with 16-byte string field. This introduced new crashes.
- Reverted to 16-byte entries; added truncation guard in `lex_add`.
- Status: Not fully resolved.

### 2. Segmentation scoring deviation (DISCLOSED)
- Prereg specified: sum of log bigram scores minus boundary cost.
- Implementation uses: length-averaged log bigram score minus boundary cost.
- Reason: Sum formulation structurally favors single long segment (each extra segment pays boundary cost).
- Kill bars not changed. Deviation disclosed here and in source comments.

### 3. Unresolved crash: "slice index out of bounds"
- Location: During training loop, exact point varies with code changes.
- Observed crash points:
  - After `gen_episodes` completes, during learner state allocation or early training.
  - At t=0, after segmentation and lexicon insertion, during `interpret` or `learn_update`.
  - At t=31 (NEG phase) in earlier version before lexicon fix.
- Debugging performed:
  - Traced with emit markers through `gen_episodes`, W allocation, training loop entry.
  - Isolated to training loop; `gen_episodes` completes successfully.
  - Minimal loop pattern test inconclusive due to toolchain differences.
- Root cause: Not identified. Suspected memory corruption from lexicon layout changes or buffer overflow in segmentation/grounding code.
- Status: UNRESOLVED. Program does not produce output.

### 4. K1 measurement timing (NOT FIXED)
- Prereg requires K1 (8/10 words discovered) measured at end of phase 1 (t=60).
- Implementation measures after all 100 training episodes.
- Status: Would need fix, but program does not run.

## Kill Bar Results
None measurable. Program does not execute to completion.

| Bar | Threshold | Result |
|-----|-----------|--------|
| K1 | 8/10 words by end phase 1 | UNMEASURABLE |
| K2 | DIRECT novel 5/6 | UNMEASURABLE |
| K3 | NEG novel 2/3 | UNMEASURABLE |
| K4 | REL novel 2/3 | UNMEASURABLE |
| K5 | Synonym novel 2/3 | UNMEASURABLE |
| K6 | SIZE novel 2/3 | UNMEASURABLE |
| K7 | 3-way composition 1/2 | UNMEASURABLE |
| K8 | Beat best control by 15pp | UNMEASURABLE |
| K9 | 7/10 on final ten phase-2 | UNMEASURABLE |
| K10 | Strict online audit | UNMEASURABLE (code review: segmentation uses prior state only - PASS by inspection) |
| K11 | Episode t excluded from its own bigram | UNMEASURABLE (code review: update after segmentation - PASS by inspection) |
| K12 | 3/3 byte-identical runs | UNMEASURABLE |

## Online Audit (K10, K11) by Code Inspection
- **K10**: Training loop segments episode `t` using bigram counts from episodes `0..t-1` only. `learn_update` is called AFTER `seg_dp` and `interpret`. Test episodes (100..119) do not call `learn_update`. **PASS by inspection.**
- **K11**: Bigram counts are updated in `learn_update`, which runs after segmentation. Episode `t`'s bigrams are not in W during its own segmentation. **PASS by inspection.**

## Governance Findings
- **Prereg order**: PASS. Prereg commit `e23627a40` strictly precedes implementation.
- **Python use**: None. Pure Zag implementation. No Python in source, build, or verification.
- **Em dashes**: Source contains no em dash bytes (verified by inspection; loop docs rule).
- **Scoring deviation**: DISCLOSED. Length-averaged vs sum-of-logs. Bars unchanged.
- **K1 timing**: Deviation from prereg (measures post-phase-2, not at t=60). Not fixed due to crash.

## Classification
Developmental L2 (structural learning attempt), not L3. The mechanism (bigram DP segmentation, grounded lexicon, learned negator/comparative) is researcher-designed; the learner fills parameters and discovers segmentations. No representational invention claimed.

## Recommendation
The design is sound but the implementation has memory-safety defects. A rewrite with:
1. Fixed-size lexicon entries accommodating max utterance length (16 chars).
2. Bounds checking on all buffer accesses.
3. Simpler segmentation (e.g., fixed max 8, no dynamic).
4. K1 measured at t=60 via snapshot.

...could achieve the preregistered goals. The current artifact is not salvageable without significant rework.

## Files
- `PREREG_DEVANG1.md`: Frozen preregistration (committed e23627a40).
- `devang1.zag`: Implementation attempt (with defects, committed as evidence).
- `RESULT_DEVANG1.md`: This file.

## Builder Label
**BUILD-FAIL**
