# CLASS-3 ADVANTAGE — Preregistration

**Date:** 2026-09-21  
**Question (from Micah):** Is Grok best specifically at teaching a TNN teacher that then trains another TNN? Is class 3's apparent advantage architectural? Are the championship tests legitimate real-world cases or toy evaluations?

## Hypotheses

- **H1 (restructure):** The class-3 advantage comes from the teacher *restructuring* knowledge (reorganization improves learnability).
- **H2 (verification filter):** The advantage comes from a verification/filtering step (bad content filtered before teaching).
- **H3 (noise interaction):** The class-3 minus class-4 gap correlates with source corpus faithfulness errors (noisy sources lose more).
- **H4 (step anomaly):** Step's class-3 mastery loss (0.9563 vs 1.0) has a specific, identifiable mechanical cause.

## Kill bars

- **H1 KILLED if:** the class-3 advantage decomposes entirely into cost accounting with zero mastery/revisability/integrity/retention improvement, AND a mechanism other than restructuring explains the cost delta.
- **H2 SUPPORTED if:** a specific filtering gate is identified in code whose skipped items exactly predict the mastery delta.
- **H2 KILLED if:** no filtering gate exists, or the gate's skips do not match the observed mastery loss.
- **H3 SUPPORTED if:** gap magnitude correlates with independently measured corpus transcription errors across all four sources.
- **H3 KILLED if:** a source with zero transcription errors shows a negative gap (breaks the correlation).
- **H4 SOLVED if:** the exact skipped fact IDs are identified and their cause is traced to a deterministic mechanism, with per-slice skip counts matching the verdict exactly.

## Method

1. Decompose all four sources' class-3 vs class-4 composites into the five Track-5 components (from frozen verdicts).
2. Read the teacher-build and teaching-loop code for each crew; identify any filtering gate.
3. Mechanically audit all four corpora for transcription errors (input-claim hash, dump/obs/probe mismatches).
4. Reimplement the deterministic held-out and slice-fact functions in Python; compute the predicted skip pattern; compare against the step verdict's per-slice skips.
5. Classify each crew's teacher as complete (no held-out) or incomplete (D2 held-out geometry).

## Confounders registered in advance

- Class-4 mastery (legA: 198 curriculum probes) and class-3 mastery (teach3: 192 slice facts) are different batteries; the prereg's "same Track 5 metrics" was not implemented identically.
- Teacher completeness (held-out exclusion) was not standardized across crews.
- Cost formula uses op counts that differ structurally between routes.

## Interpretation rule

If the gap is fully explained by (a) cost-accounting differences and (b) teacher completeness, then the "source pattern" (grok/sol win, step/swe lose) is an implementation artifact, not a source-LLM property. The architectural claim must be restated as: the teacher route is an honest, amortized channel — cheaper to learn from, but filtered by what the teacher holds.
