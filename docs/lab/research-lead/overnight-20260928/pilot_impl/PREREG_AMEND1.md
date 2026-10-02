# Amendment 1 to PREREG_PILOT.md (transparent, before any run)

Parent prereg: `76878a918` (PREREG_PILOT.md).
Date: 2026-09-30 UTC. No pilot code written yet; no runs performed.

## Reason

Section 3 defines F-REL for P2 as "P2d vs P2b" with margin 0 ("must
equal"), but P2d is an 8-item domain-0 re-query while P2b is a 4-item
held-out probe. Comparing scores across different probe scales is not
the apples-to-apples comparison F-REL intends.

## Amendment (strengthening, not weakening)

Arm B mode 2 additionally reports P2D: the same 8-item domain-0
re-query probe as Arm A P2d, run immediately after mode 2's E2
experience. F-REL for P2 is redefined as:

- F-REL-P2: Arm A P2d (8 items) >= Arm B mode-2 P2D (8 items) - 0.
  Margin 0: must equal.

The original P2b (held-out 4 items, floor >= 3/4) is unchanged and
remains an immediate floor (F-E2b) in both arms. P2D is an additional
Arm B reference measurement, not a new floor.

No floor value is lowered; no falsifier is weakened. This amendment is
committed before any implementation file and before any run.

## Self-check

- [x] Committed before implementation and before any run.
- [x] Does not alter any frozen workload, floor value, or falsifier.
- [x] Zero em-dash bytes (shell-verified before commit).
- [x] No Python at any stage.
