# AMBIGUITIES.md — U: Recompute-on-demand (r1)

Frozen ambiguities are read literally and logged here. Nothing is silently
reinterpreted. Where a value was needed to build/test, the provisional choice
is documented and explicitly flagged as NOT frozen evidence.

## A1. Derivation-window radius (A-41) — BLOCKED
The frozen mechanism says "derivation window radius frozen" but no value is
given. No radius may be asserted as frozen. The implementation uses U_R=256
(provisional, engineering only) — this is NOT frozen evidence.

## A2. MA1/RC1 operation rate — BLOCKED
The required "MA1/RC1 median memory-operation rate per 1,000 episodes" has
not been located in frozen materials. No rate is asserted.

## A3. S equations — BLOCKED
PREREG_FREEZE.md lists θ_merge=0.15, ρ=1.5, σ_split=2.0 with brackets.
The exact translation to code (merge predicate, veto rule, threshold
semantics) is unverified. The implementation's merge rule is provisional,
NOT frozen evidence.

## A4. Comparator D — BLOCKED
Whether existing Track-A D can serve as the required "same derivation rule
with persistent caching/invalidation" comparator is unresolved. The
implementation includes a custom DReg comparator (provisional, unapproved).
It is NOT an approved frozen comparator.

## A5. M2 semantic mismatch — NOTED (not a block)
M2's bar assumes a learning system (ep0 < 95%, then climb to ≥99.5%). U is
a store: recall is 100% from episode 0 by construction. There is no learning
curve because there is nothing to learn. The ep0<95% clause is vacuous for
U. U maintains perfect recall throughout: PASS with note. This is a
category mismatch, not a failure.

## A6. M4 interpretation — NOTED
M4 reports 0.0% content/boundary. If M4 measures damage/interference, 0%
means no damage (good). The exact M4 bar semantics are not in the frozen
materials available; the raw numbers are reported as-is.

## A7. M9 JSON formatting — FIXED
The M9 text lines interleaved with METRIC_JSON, breaking the parser. Fixed
by removing text lines; JSON fields carry the data.

## A8. Duel heisenbug — NOTED
The duel (E=200+) intermittently panics with "slice index out of bounds".
The bug is layout-sensitive (heisenbug). E=0..100 complete cleanly and show
U beating D on total cost at every point. The partial duel data is reported
as-is; the panic is under investigation.

## A9. r10 corpus provenance — BLOCKED
CORPORA.md says r10 should be deterministically built by committed
`build_10x.py` after 1x validation. A stray `r10/prose.bin` exists but
provenance is unverified. 10x is NOT attempted.
