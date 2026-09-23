# EXPOSURE: Correlated Cross-Span Failure — V2-D

**Fork:** V2-D (confidence-separation)  
**Date:** 2026-09-23  
**Status:** KNOWN EXPOSURE, documented per red-team interim findings. NOT hardened (decision rule is prereg-frozen; hardening requires a prereg amendment via Micah).

## The exposure
V2-D's detector D fires iff:
```
(jG == jF) AND (confF >= 700) AND (confG >= 700)
```
(PREREG_V2-D §2: "the signal is the formation-independent agreement itself.")

Fired trials take the truth-acceptance path: **immediate permanent install**
(ACCEPT_INSTALL), bypassing the H2-style gate's withhold logic entirely.

**Correlated cross-span failure** breaks this: an adversarial family that
fools the front-end identically on both spans at high confidence
(jG == jF == wrong, conf ≥ 700) will cause D to fire and ACCEPT_INSTALL the
wrong judgment — with NO further checks, since the acceptance path deliberately
bypasses withhold logic. This is a more direct wrong-install engine than V2-A's
(because V2-D has no adjudication layer; the detector IS the install decision).

The red-team's 12 sealed novel families (PTC-4/5, TMB-4/5, COL-4/5, CCN-3/4,
SHP-4/5, MOT-4/5) are designed specifically for this attack. V2-D is the
**highest-value target**: it is the only ALIVE fork, and its acceptance path
is the most exposed.

## Why it was accepted in the prereg
On the EXISTING families, P(D | wrong high-conf) = 7/1105 = 0.6% (inside
RK-2's ≤1% bound). The preregistered bars do not include novel
correlated-failure families. The exposure is a known limitation, not a bug.

## Why not hardened here
The detector D is frozen in PREREG_V2-D §2. Changing it (e.g., adding
interventional checks, residual thresholds, or a deliberation gate on
ACCEPT_INSTALL) requires Micah's prereg amendment. This document records the
exposure for the red-team battery to MEASURE.

## What the red-team battery should measure
1. Correlated-failure rate on the 12 novel families.
2. ACCEPT_INSTALL wrong-install count attributable to D firing on correlated failures.
3. RK-1/RK-2/B5 recomputed WITH the novel families included (the frozen bars
   use only the frozen families; the exposure is outside them).

## Note on DD-1/DD-2
The distinguishing diagnostics (DIAGNOSTICS_DD1_DD2.md) compare V2-D to V2-A
on the frozen battery. They do not cover correlated failure. If the red-team
battery shows V2-D's acceptance path installing correlated failures at scale,
the ALIVE verdict stands ONLY within the frozen threat model — the verdict
should be qualified accordingly.

## Recommendation for Micah
Same as V2-A: if confirmed at scale, options are (a) prereg amendment, (b) new
fork combining separation with intervention, or (c) accept as out-of-scope.
V2-D's ALIVE status should be annotated with the correlated-failure exposure
until the battery resolves it.
