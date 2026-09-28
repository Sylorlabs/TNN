# Amendment 2026-09-27-G1-FIX1 (DRAFT)

**Status:** DRAFT by the fix1 crew — recorded per amendment 2026-09-27-A's
rule ("any future change to `g1_candidate.zag` semantics needs its own
amendment"). Awaiting coordinator disposition; does NOT enact the §8 draft.

## What changed

`selfpam/src/g1_candidate.zag` semantics (mirrored byte-identically into
`round2/forks/R2-3/src/g1_candidate.zag` per the vendoring rule):

- **id 2 (`selfpam-fact-gate`)**: judgment changed from
  `span_sum(evidence)/8` (order-blind) to `span_seq(evidence)/8`
  (position-weighted sum Σ(i+1)·b_i mod 2^31, order-sensitive).
  This is the fix for the R2-3 order-blindness misses (100 of 101 admitted
  pairs were exact byte-permutations whose plain sums collide).
- **id 3 (`selfpam-sum-gate`)**, NEW experimental: the pre-fix1 id-2 law
  (`span_sum(evidence)/8`) kept selectable as a legacy control.
- **id 4 (`selfpam-fnv-gate`)**, NEW experimental: FNV-1a 32-bit digest,
  exact comparison (tolerance 0), as a comparison variant.
- `round2/forks/R2-3/src/sense.zag`: gate-id range extended 0..2 → 0..4.
  `r2p_gates.zag`: id 3/4 branches added (delegating to `sp_gate_*`).
  Ids 0/1 behavior unchanged (regression-proven byte-identical).

`codec.zag`'s `span_sum` is UNTOUCHED (still the §8-drafted SPAN-SUM value;
`corr.zag` and the cc1_guard tests are unaffected).

## What did NOT change

- The §8 draft still defines meas=SPAN-SUM with tolerance 8, UNSIGNED,
  awaiting Micah. `span_seq/8` is a **PROPOSED revised §8 value** with
  evidence in `selfpam/push100/fix1/` — proposed, not enacted.
- DEMO_ONLY scope unchanged. G1 stays withhold-only; no install
  disposition is reachable; the candidate gate remains experimental
  (registration acceptance only).

## Evidence

- Fix1 report: `selfpam/push100/fix1/FIX1_REPORT.md` (per-variant rates:
  id 2 and id 4 reach 1200/1200 = 100% withhold, 0 errors, 0 overlap;
  id 3 reproduces the pre-fix1 1099/1200 exactly; ×3 byte-identical
  reports+ledgers; all 11 hash chains verified; id 0/1 regressions
  byte-identical to the committed R2-3 evidence).
- Red-team report: `selfpam/push100/fix1/REDTEAM_FIX1.md`.

## Kill / revert

If this amendment is not adopted, reverting is mechanical: restore the
four `.zag` sources to their amendment-A SHAs
(`g1_candidate.zag`
`6ba9ea447387db4e47f13ea2295ea7da4ba735c27c8d41c638ca0fefa8abdecb`,
`sense.zag`
`6c1363f4c64c3b8f7ae99222c09f8efe5eff921aa2dc42c5cd0642ca6b123462`,
`r2p_gates.zag`
`01a38a25f7b93def95eece2a3d35cfc396ebaba266785d1b0969a669f7a7391e`)
and rebuild; the R2-3 evidence already committed is unaffected.
