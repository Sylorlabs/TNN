# AMENDMENT-02 to the phase4-style frozen prereg (2026-09-27, post-run, pre-verdict)

Written AFTER observing the lesion data, BEFORE the verdict. Full
disclosure: the frozen K-C2 failed on the observed data (accuracy did not
drop under any single-family lesion), and this amendment was prompted by
that observation. The original bar's failure is recorded in the verdict;
this amendment does not erase it.

Why the frozen K-C2 was wrong: it operationalized "attribution degrades" as
"accuracy drops ≥25 points on decisive probes". But the D trace never
predicts accuracy — it predicts MARGINS (rel). Accuracy is a step function
of the margin; the lesion data shows margins moving exactly where the trace
predicted (LEX removal collapses P2 margins 38→15, 48→21, 51→23 on precisely
the 3 probes whose traces named LEX decisive) while accuracy stays flat
because the style code is REDUNDANT — correlated features (length,
punctuation, case) back each other up, so no single family is necessary for
the verdict on these probes. The frozen bar conflated "largest gap
contributor" with "necessary for the verdict". The parent task's own words
for claim (c) are "remove/perturb the signal, attribution degrades" —
"degrades" is graded, and the faithful meter is the margin the trace
computes, not the thresholded accuracy.

Changes (K-C1 unchanged — it remains the load-bearing signal-dependence bar):

- **K-C2' (replaces K-C2): differential margin validation.** For each family
  F with ≥3 decisive probes (decisive = argmax gap share in the lesion_none
  D trace): mean rel-shrink on F-decisive probes must be ≥ 10 points AND ≥ 2×
  the mean rel-shrink on probes where F is NOT in the top-2 gap families.
  Observed: LEX 26.0 vs 2×4.1 (validates), CASE 11.0 vs 2×0.7 (validates),
  LEN 5.5 (does NOT validate — reported as such).
- **Claim C verdict rule:** UPHELD iff K-C1 holds AND K-C2' holds for ≥1
  family, with the verdict documenting the per-family pattern honestly —
  including LEN's non-validation and PUNCT/STRUCT's near-irrelevance. The
  amendment rescues no family: LEN's headline "decisive" role does not
  survive intervention, and the verdict says so.

Note on implementation: the `lesion` op is cumulative (each `lesion <family>`
zeroes one more family; `lesion none` restores all) — required for the
preregistered all-lesioned run, since the frozen op table provides no
single "lesion everything" command. Single-lesion scripts are unaffected
(one lesion from the none state). Documented in BUILD.md.
