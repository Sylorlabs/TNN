# ARM_SPEC.md — U: Recompute-on-demand (Track A)

**Authority:** Coordinator frozen §3, second correction (2026-09-21).
Both coordinator corrections are acknowledged here:
1. First correction (2026-09-21): reassigned U from the original dual-route/PROM
   to STORE / Recompute-on-demand.
2. Second correction (2026-09-21, AUTHORITATIVE): confirmed the STORE /
   Recompute-on-demand assignment with the frozen mechanism text and binding
   kills, in the order: `units/arms/briefs/U.json` → second frozen §3 row →
   nothing earlier.

The original dual-route/PROM assignment is VOID and must not be referenced
as U evidence. The invalid wrong-arm M1 result (100/100) must never be
reported as U evidence.

## Frozen mechanism (verbatim from coordinator)
- **Family:** STORE
- **Mechanism:** "No stored chunks; cuts re-derived whenever needed (derivation
  window radius frozen); λ/μ op pricing; crossover sweep 0→1000 edits vs D.
  The anti-caching arm that makes D falsifiable."

## Binding kills
1. CPU >10× D and B4 <10%.
2. D-with-invalidation beats U on total cost including 100 edits.
3. Determinism fails.

## Implementation notes
- U persists no segmentation structure: no chunk registry, stable chunk IDs,
  merge table, or memoized cuts. (Observed 2026-09-21; see AMBIGUITIES.md.)
- Every recall derives segmentation deterministically from source bytes,
  logged state, query span, and bounded context. The derivation is the S
  crystallization rule evaluated transiently and discarded.
- U is provisionally non-ID: M1 swap probe N/A; M7 N/A with informational
  reread bytes; A15 swap schedule does not apply.
- Expected B4 reuse, persisted segmentation footprint, and persisted re-key
  cost are zero.
- Frozen cost: `cpu_ops + λ·(resident_bytes × queries) + μ·rekey_bytes`,
  λ = 1 op/64 resident bytes/query, μ = 10 ops/re-keyed byte.
- The required comparison is U versus the same derivation rule with
  persistent caching/invalidation over a 0→1000 edit sweep.

## Unresolved dependencies (BLOCKED, see AMBIGUITIES.md)
The following are required by the frozen spec but have no resolved value:
- Derivation-window radius (A-41).
- MA1/RC1 median memory-operation rate per 1,000 episodes.
- Whether existing Track-A D can serve as the required same-S-rule cached
  comparator.
- Exact S equations (θ_merge=0.15, ρ=1.5, σ_split=2.0 are listed in
  PREREG_FREEZE.md with brackets; translation to code is unverified).

No values for the above are asserted in this spec. The implementation uses
provisional values ONLY for engineering (build/test), NOT as frozen evidence.
