# Phase B Prime Pilot Result: STAB-NONE (PILOT-FAIL)

Date: 2026-09-30. Worker: Phase B Prime Pilot Builder.
Prereg: `237f7a1ee` (PREREG_PHASEB_PRIME_PILOT.md, frozen before implementation).
Design: `9f1864f9`.
Zero Python at every stage. This file is byte-verified free of em/en dashes.

## Verdict: PHASEB-PILOT-FAIL (STAB-NONE)

No candidate family reached the 0.8 stability threshold. Per the frozen
prereg section 10, this yields PILOT-FAIL; the main wave does not launch.

## Stability Scores (frozen selection rule applied)

| Family | p (recruited triples / 5) | Threshold | Status |
|--------|---------------------------|-----------|--------|
| G1 (mixed AND/OR) | 0/5 | >= 4/5 | FAIL |
| G2 (NOT-mixed) | 0/5 | >= 4/5 | FAIL |
| G3 (calibration) | 0/5 | >= 4/5 (never selectable) | CALIB-OK |
| G4 (nested) | 0/5 | >= 4/5 | FAIL |
| G5 (factored OR) | 0/5 | >= 4/5 | FAIL |

Selection: no family reaches p >= 0.8. Best p = 0/5. Result: STAB-NONE.

G3 calibration: G3 scored 0/5, below the 0.8 threshold. The apparatus
reproduces the known failure (original Phase B scored 0/5 on the same
family structure). No CALIB-VIOLATION. The measurement apparatus is
consistent with the prior wave.

## What was measured

25 pilot triples (5 per family x 5 families). Each triple: three
episodes (E1, E2, E3) with the family's fixed terminal bindings, fresh
persistent state per episode, the frozen Phase B beam (all design
section 2 constants), 8 passive samples plus up to 24 adaptive
interventions, keep margin 0.15, node bound 7. Per triple, in-run
consolidation ran exactly as the main wave would: DETECT over the three
kept trees, nshapes and winner recorded, RECRUITED fired iff freq >=
K_FREQ=3 with gain > 0 and F-BREAK pass.

Observed consolidation pattern (representative): nshapes=2, winner=-1.
The beam keeps 3-op trees at 64/64 true accuracy on every episode, but
the three kept trees have distinct canonical shapes. No fragment reaches
freq 3. This matches the Phase B post-mortem's Cause 1 diagnosis, now
confirmed across five independently designed families.

## Kill bars

- K1 (prereg frozen before implementation): PASS. Prereg `237f7a1ee`
  committed alone before pilot.zag existed.
- K2 (all families measured): PASS. 25 triples across G1-G5, 5 per
  family, all with fresh seeds per the frozen seed list.
- K3 (pure Zag, 3/3 byte-identical): PASS. Three runs, md5
  `2875992f38b06228fcd4b8cd9d050b9d` on all three. Exit 0, empty
  stderr. Zero Python at every stage (authoring, compilation, runs,
  verification). Shell-only dash check clean.

## Interpretation

The tax-consistency problem is deeper than the redesign anticipated.
Five families were designed with explicit anti-factoring rationales:
disjoint variable bindings (G1, G5), NOT-blocking (G2), nested forms
where the factored version is strictly simpler (G4). None produced a
single recruited triple. The beam's 200/opc simplicity tax finds a
different minimal equivalent on essentially every episode, across all
five structural hypotheses.

This is honest negative evidence about the Phase A consolidation
precondition, not a defect in the pilot. The pilot was designed to
detect exactly this outcome (STAB-NONE is a terminal outcome in the
frozen prereg, not an error). The result constrains future work: the
consolidation target cannot be aligned with the beam's minimizers by
family design alone, because the beam's minimizer set is episode-specific
in a way that resists all five structural interventions.

## Stage 2

Not run. Per the frozen prereg, Stage 2 (probe convergence validation)
is part of the pilot wave but is conditional on Stage 1 selecting a
family. With STAB-NONE, the pilot halts. No Y-probe construction, no
convergence validation.

## Files

- PREREG_PHASEB_PRIME_PILOT.md (prereg, `237f7a1ee`)
- pilot.zag (implementation, derived from frozen c0integ_b.zag)
- PILOT_RUN1.txt, PILOT_RUN2.txt, PILOT_RUN3.txt (byte-identical logs)
- PILOT_RUN1.err, PILOT_RUN2.err, PILOT_RUN3.err (empty)
- RESULT_PILOT.md (this file)

## Governance notes

- The contaminated research paper was not touched.
- No implementation existed before the prereg commit.
- Pathspec commits on owned paths only.
- Nothing pushed. Commits stay local.

## Verdict: PHASEB-PILOT-FAIL
