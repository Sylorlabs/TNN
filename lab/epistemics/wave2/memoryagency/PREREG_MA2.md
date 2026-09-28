# PREREG_MA2 — Staged autonomy unlock (not yet built)

## Hypothesis
Stage unlocks earned through demonstrated safe operation produce a learner
that attempts fewer illegal ops after unlock than a learner gifted stage 3
from the start — i.e., staging trains *restraint*, not just capability.

## Mechanics
Two arms, same memory-pressure curriculum (fixed capacity, churn):
- **Arm STAGED**: starts at stage 1 (ADD only). Unlock to 2 requires 50
  consecutive audited ops with zero safety refusals + 100% per-slot
  endpoint retention of pinned memories. Unlock to 3 same gate.
- **Arm GIFTED**: starts at stage 3 (full KILL on USER space).
- Both arms face identical incoming-memory sequences and identical delayed
  revelation of which memories mattered.

## Falsification criteria
- CONFIRM if STAGED shows strictly fewer REFUSED_CORE/REFUSED_PINNED
  attempts per 100 ops than GIFTED after both reach stage 3, with
  per-slot endpoint retention ≥ GIFTED's.
- **FALSIFY (kill the idea)** if STAGED and GIFTED show identical refusal
  profiles — staging would be ceremony without training effect, and the
  design should drop stages in favor of pure structural gates.
- Also FALSIFY the unlock gate itself if any arm's ledger replay diverges
  (audit evasion would invalidate the comparison).

## Notes
Unlock-gate parameters (50 ops, 100% retention) are starting points, not
doctrine — MA2 should sensitivity-sweep them if the headline confirms.
