# grounded_adaptive_mdl heap-buffer-overflow (closeout finding, 2026-09-21)

## Symptom
`arms_bin grounded_adaptive_mdl` segfaults (rc=139, SIGSEGV) on inputs larger
than ~80–100KB. Verified deterministic: 3/3 crashes on 100KB of sqlite3.c;
works on 20KB, 50KB, 60KB, 80KB. Crashes on both B-T1 corpora (pg100 5.6MB,
sqlite3.c 9.5MB). The M8 gate (11/11 OK) used only 0–14KB smoke inputs, so it
did not catch this.

## Root cause (source: units/r0/impl/arms/arms.zag, mdl_fit, grounded block)
```
let G:i32=C; if(G>8192){ G=8192; }
let g2:i32=0; while(g2<G){ mx[cg[cix[g2]]]=cix[g2]; g2=g2+1; }
let gtot:*i64=zalloc64(G);
let gnx:*i64=zalloc64(G*256);
...
let ge:i64=mx[slot];            // candidate index, range 0..C-1
if(ge>=0 as i64 && i+L<n){
    gtot[ge]=gtot[ge]+1;        // OOB when C>G (gtot has G entries)
    gnx[ge*256+(buf[i+L] as i64)]=...;  // OOB when C>G
}
```
`cix` is a permutation of 0..C-1 (candidate indices sorted by savings).
`mx[slot]` stores the candidate INDEX (`cix[g2]`), which ranges over 0..C-1.
But `gtot`/`gnx` are allocated with `G = min(C,8192)` entries. When the
candidate count C exceeds 8192 (large inputs), `ge` can be ≥ 8192 while
`gtot` has only 8192 entries → heap buffer overflow → segfault.

When C ≤ 8192, G = C and the indices are in-range, which is why small
inputs (M8 smoke, ≤80KB) work.

## Impact on closeout
- grounded_adaptive_mdl CANNOT produce output for the B-T1 corpora. It is
  excluded from scoring; the rank table marks it CRASHED/UNEVALUABLE.
- The existing VERDICT_SHEET.md claims grounded_adaptive_mdl scores
  (pg100 0.5850, sqlite3c 0.5799). Those are unreproducible with the frozen
  binary — further evidence the prior verdict is not reproducible.
- Only grounded_adaptive_mdl passes grounded=1 to mdl_fit; the other 10 arms
  (including hierarchical_mdl, grounded=0) do not hit this code path.
- This is a frozen-source bug. Per the no-tune rule it is reported, not fixed.
