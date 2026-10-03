# RESULT_SEGREDESIGN: TP-Threshold Segmentation Prototype

## Verdict
**REDESIGN-BLOCKED** (frozen K3 not met; approach validated, see below)

## Preregistration
- Commit: `fc82df44b` (PREREG_SEGREDESIGN.md, frozen before implementation)
- Amendment: `5dfdc776d` (PREREG_SEGREDESIGN_AMEND1.md, exploratory V2)
- Prereg strictly preceded implementation. Amendment preceded V2/V3.

## Implementation
- File: `segproto.zag` (self-contained, pure Zag)
- Toolchain: `znc` (native binary)
- Status: Compiles, runs to completion. 3/3 byte-identical outputs
  (md5 74435cea2066a6f788f797758649605b).
- Contains: word definitions and phase-1 episode generator copied
  verbatim from DEVANG2 (seed 123456789, identical 60 episodes),
  V0 baseline (exact `seg_dp` copy), V1 (frozen TP-threshold),
  V2a/V2b (exploratory ratio bidirectional), V3 (exploratory +4).

## Kill Bar Results

| Bar | Threshold | Result | Pass |
|-----|-----------|--------|------|
| K1 | Approach defined in prereg | PREREG_SEGREDESIGN.md | PASS |
| K2 | Prototype in pure Zag, runs | Compiles, 3/3 identical | PASS |
| K3 | V1 > V0 AND V1 >= 5/10 | V1=4/10, V0=3/10 | FAIL |

**Verdict rule:** REDESIGN-PROTOTYPED requires K1,K2,K3. K3 FAIL.
**REDESIGN-BLOCKED.**

## Measurements (all at t=60, 60 phase-1 episodes, identical sequence)

| Variant | Words /10 | Found |
|---------|-----------|-------|
| V0 baseline (bigram DP) | 3/10 | tak, bal, cub |
| V1 frozen (TP, +26, -15) | 4/10 | tak, red, blu, cub |
| V2a exploratory (ratio, 250) | 4/10 | tak, red, blu, cub |
| V2b exploratory (ratio, 300) | 4/10 | tak, red, blu, cub |
| V3 exploratory (TP, +4, -15) | 6/10 | tak, not, red, blu, sph, cub |

Cold start (t=0): V0 nseg=1 [takredbal] (whole utterance, poisons
lexicon). V1/V2/V3 nseg=9 [t|a|k|r|e|d|b|a|l] (single chars, no
poisoning). The cold-start fix works as designed.

V0 lexicon (20 entries) contains whole utterances: [takredbal],
[taknotred], [kbigerbal], [smalbal]. This confirms the DEVANG2
"never recovers" mechanism: the 64-entry finite lexicon fills with
unusable whole-utterance entries.

## Analysis

1. **TP-threshold fixes the cold start.** Laplace-smoothed TP gives
   s(p)=-40 at t=0 for all p, below THETA, so boundaries everywhere.
   Single characters enter the lexicon (max 26), never whole
   utterances. The finite lexicon is preserved for real words.

2. **TP normalizes the function-word boundary.** P(a|k)=1.0 within
   "tak" vs P(r|k)=0.22 across tak|red. Raw bigram frequency cannot
   see this (both occur 18 times); TP can. V1 discovers "red" and
   "blu"; V0 does not.

3. **The +26 Laplace prior is too conservative.** V1 (+26) leaves
   "not" split as [n][o] (12 observations insufficient to merge).
   V3 (+4) merges "not", "sph", reaching 6/10. The prior strength,
   not the TP cue itself, was the limiter.

4. **V3 over-merges.** Weaker prior creates spurious units:
   [takred] c=6, [takb] c=15, [takblu] c=4. The "kb" boundary
   (tak|b-initial-word) has high forward TP because many words start
   with b. Precision/recall tradeoff; future work.

5. **Remaining failures (all variants):** "bal" (b/a/l too frequent),
   "biger" (5 chars, shared bigrams), "smal" (rare, shares s with
   sph). These need grounding or lexicon-reuse cues, not pure
   distributional TP.

## Governance Findings
- **Prereg order:** PASS. fc82df44b strictly precedes implementation.
- **Amendment order:** PASS. 5dfdc776d precedes V2/V3.
- **Python use:** None. Pure Zag (implementation, compilation,
  execution, analysis).
- **Em dashes:** None (verified via od).
- **No deviation:** V1 implemented exactly as frozen. V2/V3 clearly
  marked exploratory.

## Classification
Segmentation mechanism redesign (L2 infrastructure). The TP cue is
generic (no word-specific knowledge); the learner still discovers
the actual words. Not L3.

## Recommendation
Freeze V3 (TP-threshold, +4 Laplace, THETA=-15) or a calibrated
variant as the segmentation for DEVANG3. Address over-merging
([takb]) via backward-TP or lexicon-reuse in the next wave. The
grounding cue remains the principled fix for "bal"/"smal".

## Files
- `PREREG_SEGREDESIGN.md`: Frozen prereg (fc82df44b).
- `PREREG_SEGREDESIGN_AMEND1.md`: Exploratory amendment (5dfdc776d).
- `segproto.zag`: Prototype implementation.
- `RESULT_SEGREDESIGN.md`: This file.
- `run1.txt`: Raw output (3/3 identical).

## Builder Label
**REDESIGN-BLOCKED** (K3: V1=4/10 < 5/10; V1 does beat V0 4>3;
exploratory V3=6/10 validates the approach)
