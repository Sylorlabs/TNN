# N16 Smoke01 — superseded authoring fixture

Smoke namespace810000, population0, BUILD_01. Engineering-only; no development/validation/confirmation population was exposed.

Key rows (`old_lost`, `old_gate_hits`, `new_gain`, `new_gate_hits`, `anchor_loss`):

- arm3 single-prototype/no-preservation: 37, 82, +298, 415, 0.
- arm4 single-prototype/legacy96 preservation: 3, 82, +112, 415, 0.
- arm6 single-prototype/dual512 preservation: 0, 82, +44, 415, 0.
- arm7 four-cluster/parent256: 4, 82, +9, 444, 0.
- arm8 four-cluster/dual512: 2, 82, +19, 444, 0.
- arm9 eight-cluster/parent256: 8, 49, +29, 442, 0.
- arm10 eight-cluster/dual512: 3, 49, +10, 442, 0.
- arm11 strict eight-cluster/dual512 tolerance1: 3, 40, +32, 423, 1.

Interpretation used only for authoring: four-cluster routing did not reduce old-route activation on this fixture. Eight-cluster routing did reduce old gate hits while preserving high new gate coverage, but combining it immediately with strict tolerance0 preservation suppressed useful learning. The scientific arm matrix was therefore revised before development to expose eight-cluster routing without preservation and to separate preservation coverage from tolerance.
