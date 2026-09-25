# RSI Run 2 REDO — AF-DISC sign-fix log (2026-09-24)

**Prereg:** `RUN_PREREG3.md` (frozen, committed; byte-identical to local).
**Bug:** `RUN_D8_REPORT.md` §2. `chan_vals` packed signed `sn`/`so` as raw
signed bytes but `cv_sn`/`cv_so` read them as unsigned bytes with no sign
restoration. On this battery `sn ∈ {-1,+1}`: items with `sn=-1` read as
`cv_sn=255`, so D1's `sn_ge(2..6)` atoms really meant "sn == -1". The
proposer evaluates with the real `sn` (`atom_pre`), so every proposed
policy was a no-op and V3 correctly rejected all.

**Fix (8 lines, 2 files, exactly per RUN_PREREG3 §2):**

`src/afdisc.zag` and `src/deliberation.zag` (identical copies):

1. Pack: `((sn as i64)<<16)` → `(((sn+8) as i64)<<16)`
2. Pack: `((so as i64)<<24)` → `(((so+8) as i64)<<24)`
3. Read: `cv_sn` → `((((cv>>16)&255) as i32)-8`
4. Read: `cv_so` → `((((cv>>24)&255) as i32)-8`

This matches the existing `sm`/`psm` convention (`cv_sm`, `cv_psm` already
use +8/-8). `sn`,`so` ∈ [-3,+3] (sums of three ±1 in `pk_sn`/`pk_so`) →
[5,11] after +8: fits the byte; no sign bit ever set on pack.

Grep-verified: only the two `chan_vals` copies pack `sn`/`so`; only
`atom_true` (aid 8/9) in those two files reads `cv_sn`/`cv_so`.
Stale `build/afdisc_full.zag` / `build/delib_full.zag` carry the old code
and are REGENERATED from these fixed sources before the rerun (§6 step 1).

**Source SHAs (post-fix):**
- `src/afdisc.zag`: `577e0cb5bf3b483e6ef572ab29375e93e9388171974d465d3a9097a5dc1f006f`
- `src/deliberation.zag`: `fb334ccd84252aa729e4ba38ca745343d571a88a2035811438d6ab79ed62916d`

No other source touched. No binary committed. Rerun + evidence follow.
