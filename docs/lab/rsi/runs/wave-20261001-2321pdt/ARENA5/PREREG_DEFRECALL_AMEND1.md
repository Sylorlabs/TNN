# AMENDMENT 1 to PREREG_DEFRECALL (ARENA5, wave-20261001-2321pdt)

Status: FROZEN AMENDMENT. Committed alone before any battery
generation, implementation build, or evaluation run under the
amended spec. The original prereg (PREREG_DEFRECALL.md) is otherwise
unchanged; all kill bars K1-K8, the mechanism spec, and the
evaluation protocol stand as frozen.

## What broke

The frozen fresh seed 71503461337031 does not yield a battery.
The world_gen fresh-seed variant (1-line seed change, verified)
aborts with exit code 2 and the message "DSL EXHAUSTION FAILED:
old language expresses transform" (world_gen.zag line 399).

Root cause: world_gen draws a random Zem transform per seed and
refuses to generate when that transform is expressible by the old
DSL (a validity check ensuring the Zem capability requires genuine
learning). Seed 71503461337031 draws such a transform. This is a
generator-validity failure, not an unfavorable exposure pattern:
there is no battery to evaluate on.

## Amendment (frozen)

The seed-selection rule is amended to the following deterministic
procedure, which selects for generator validity only:

- Candidate seeds are 71503461337031, 71503461337032,
  71503461337033, and so on, in increasing order.
- For each candidate, run the world_gen fresh-seed variant (with
  that candidate as the seed literal). The FIRST candidate for
  which world_gen exits 0 and produces a valid 68-item battery
  (battery.json n=68, cap-15 bare-prompt probe present, 10-name key
  present) becomes the frozen fresh seed.
- The seed actually used, and the number of candidates tried, are
  recorded in SEALED_EVAL.md. No other selection criterion is
  applied.

Why this is not seed shopping: the DSL-exhaustion check concerns
only the random Zem transform (capabilities 10, 12, 16). The C15
exposure pattern is structural and seed-independent (exactly 9 of
10 entity indices appear in expo events on every seed; verified
from the frozen world_gen.zag and frozen in the prereg section
4/K1). Selecting for generator success cannot bias the C15
outcome. The kill bars (K1 >= 0.900, K2 byte-identical to the v6
fresh baseline, K3-K8) are unchanged and are evaluated on the
selected battery exactly as frozen.

## Commit-order note

This amendment is committed alone, before the battery is generated
and before the DEFRECALL implementation is built or run. The
implementation source (defrecall_contestant.zag) was written after
the original prereg freeze and is unchanged by this amendment.
