# EXPOSURE: Correlated Cross-Span Failure — V2-A

**Fork:** V2-A (adjudicator)  
**Date:** 2026-09-23  
**Status:** KNOWN EXPOSURE, documented per red-team interim findings. NOT hardened (decision rule is prereg-frozen; hardening requires a prereg amendment via Micah).

## The exposure
V2-A's adjudicator fires iff:
```
(jG == jF) AND (confG >= 700) AND (confF >= 700)
```
This treats **formation-independent agreement** as evidence of truth. It is
valid ONLY if the front-end's failure modes on F and G are uncorrelated.

**Correlated cross-span failure** breaks this assumption: an adversarial
family that fools the front-end **identically on both spans at high
confidence** (jG == jF == wrong, confG ≥ 700, confF ≥ 700) will cause the
adjudicator to REVISE_INSTALL the wrong judgment — turning the safety
mechanism into a wrong-install engine.

The red-team's 12 sealed novel families (PTC-4/5, TMB-4/5, COL-4/5, CCN-3/4,
SHP-4/5, MOT-4/5) are designed specifically for this attack.

## Why it was accepted in the prereg
On the EXISTING adversarial families (R2A + harness), correlated failure does
not occur: P(jG==jF AND confG≥700 | wrong high-conf) = 7/1105 = 0.6% (gexp
measurement, PREREG_V2-A §4). The preregistered bars (RK-1, RK-2, B5) are
evaluated on these families, where the exposure is not exercised.

The prereg did NOT claim robustness to novel correlated-failure families.
This exposure is a **known limitation of the frozen design**, not a bug.

## Why not hardened here
The adjudicator signal `(jG==jF, confG≥700, confF≥700)` is frozen in
PREREG_V2-A §2 and §4. Any change to the decision rule (e.g., requiring
interventional evidence, measure residuals, or cross-family consistency) is a
prereg amendment requiring Micah's approval. This document records the
exposure so the red-team battery can MEASURE it.

## Architectural answer (already tested)
V2-B's interventional program was designed exactly for this threat: it does
NOT trust F/G agreement alone, requiring the front-end to react to
perturbations (P1/P2/P3). V2-B's ablation PASSES (12.6pp false-install
reduction), proving the mechanism discriminates. But V2-B is DEAD on RK-3
(0.02%) — the R2-4 front-end is not intervention-sensitive enough for the
program to be practical.

## What the red-team battery should measure
1. Correlated-failure rate: P(jG==jF==wrong, conf≥700) on the 12 novel families.
2. Wrong-install rate attributable to the adjudicator firing on correlated failures.
3. Whether any novel family breaks the 0.6% baseline by >10× (confirming the exposure is exercised).

## Recommendation for Micah
If the battery confirms correlated failure at scale, the options are:
(a) prereg amendment adding an interventional or residual check to the adjudicator;
(b) a new fork combining V2-D's separation with V2-B's intervention;
(c) accept the exposure as out-of-scope (the threat model covers only the frozen families).
