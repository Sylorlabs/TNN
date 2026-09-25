# NO_LIMITS_REPAIR_NOTES.md — R4: the arbitrary revision-table cap is deleted

Parent-directed repair on the 2026-09-25 R4 resume (the last law violation
before close). Micah's standing no-stupid-limits law: load-bearing limits
are worked around, arbitrary design limits are killed.

## What was arbitrary

The frozen prereg specified the revision table as "64 rows × 16 bytes" with
"(cap 64 → SP_R_REV_CAP fail-closed)" — a design cap, not a physical one.
Any subject whose dispute history exceeds 64 revisions would refuse
legitimate overseer revisions: exactly the "limits are not a thing TNN
needs" violation.

## What replaced it (physically chunked, logically unbounded)

Same shape as the committed R2 repair: revision rows are 16-byte records in
65,536-row chunks; each chunk is 65536×16 + 8 (next-chunk header) =
1,048,584 bytes — strictly under znc's genuine 2^25-byte (33,554,432)
per-slice ceiling (load-bearing toolchain limit, worked around, never
presented as a TNN design limit). Chunks chain on demand; chunk pointers
ride the flat gate arena as i64 words. `G_REV_HEAD` (first chunk) and
`G_REV_N` (total row count) track the table.

Semantically exact vs the capped version:

- Append order = row index order → newest-row (latest-wins) preserved.
- `chain_prev` audit chains preserved.
- Effective-store `|SUP` rewrite of superseded `|EXT` lines preserved.
- All 7 warrant checks in prereg order; the cap check is gone.
- `sp_rev_cycle`'s walk bound changed from `hops<=SP_REV_CAP` to `hops<=n`
  (n = live row count): data-derived, not arbitrary. n+1 hops among n rows
  force a repeated row by pigeonhole, i.e. a periodic walk that can never
  reach the target — over-long walks still fail closed (refuse).
- `SP_R_REV_CAP=15` kept as a reserved, now-unused ledger reason code.

## Proof it is equivalent where it matters

- Smoke battery reproduces the inherited pre-change SHA exactly
  (`6855928854e38255e7275a18c5b07c82675fe1bc0752a616ba9ca90ba2e6d2e0`,
  3/3 byte-identical).
- Redteam pre-revision section (218 lines incl. all F4 checks) byte-identical
  to the pre-change binary's section.
- Long-horizon bal/int reproduce frozen SHAs (`cc7e86ed...` / `356b7873...`).
- New `rt_r4_uncapped` probe: 100 overseer M_REVISE rows applied on one gate
  — all 100 applied (`SP_R_REVISE_OK`), `G_REV_N=100`, `SP_L_REVISE=100`,
  zero refusals, exact read-back at rows 64 and 99, supersession holds
  past the old cap, effective store `|SUP`/`|EXT` correct, end-to-end
  INSTALL of the recovered claim + CONTRADICTED withhold of the
  revised-away falsehood.
- Zero RNG hits across all three trees; all batteries 3× byte-identical.

## Non-goals (deliberately untouched)

- Chunk allocations are not recursively freed on gate teardown (matches the
  R2 chunk pattern; test gates are few). Lifecycle cleanup is not added —
  scope drift avoided unless evidence requires it.
- The prereg's 64-row description is NOT amended (frozen). The deviation is
  documented here and in VERDICT_R4.md §"Directed deviation".
