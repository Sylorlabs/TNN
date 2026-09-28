# F36 MEY — Build Log

**Mechanism:** 36 (Marginal-Yield Ledger)  
**Date:** 2026-09-25 UTC  
**Authority:** `sylorlabs/TNN`, branch `tnn-native-lab`, commit `3a2eef44`  
**Compiler:** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`  
**Compiler SHA-256:** `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`

## Source files

| File | Purpose |
|------|---------|
| `src/train_mey.zag` | Ledger trainer: reads frozen `features.tsv`, counts (n,k) per (m,y,depth) cell, emits `mey_rho` |
| `src/policy_mey.zag` | Batch policy: 37-leg eval, MEY confidence head, sidecar emitter |
| `src/mey_params.zag` | Generated: 280 `mey_kN`/`mey_nN` + `mey_rho(cell)` (281 fns) |
| `src/R33_NATIVE_IO_V1.zag` … `src/dlb_util.zag` | Harness (7 files, byte-identical copies) |

## Build SHAs

- Trainer A/B: byte-identical, SHA-256 `bb212643ad675971310aa37988cccb953299ee1a2c36fbe9886ac281683db146`
  (after `au_zero` fix; retrained ledger byte-identical to pre-fix, confirming
  no allocator-luck contamination)
- Policy A/B: byte-identical, SHA-256 `3bc9482f4c90ff9191866a4dd92402e5f0db06b099cf0e317400e76d1d99fe11`

## Critical fixes during build

1. **Uninitialized ledger arenas:** `train_mey.zag` allocated `narr`/`karr` without
   `au_zero`. Added explicit zeroing; rebuilt; retrained; ledger verified
   140/140 cells vs independent Python reimplementation.
2. **`dlb_run` ledger args:** `policy_mey.zag` initially passed `0,0` for `*LG,*DOut`.
   Fixed to allocate real `LG`/`DOut` per leg (mirrors `policy_f20.zag`).
3. **Native codegen hazards (new):**
   - Per-function statement-count limit: `my_leg` with inline path-rule + sidecar
     emit tripped `unknown identifier in expression: chars` / `]`. Fixed by
     extracting `my_pathrule()` and `my_sidecar()` helpers.
   - Inline `(y as i32)` cast inside `&&` expression miscompiled. Fixed by
     hoisting to `let yi:i32=y as i32;`.
   - `ms_slot` indexed write via `ms.*.idb[o+k]`: aliased to local `idb` first.

## Training

- Features SHA: `4682190cfd504cb692df122a6b054d8fad65ef860707e6a92abfdf04e65a897d`
- Rows: 5240; released training rows: 4222; nonempty cells: 41/140; mean ρ×1000: 584
- Yield-bin pooled: y0 n=2051 ρ=976; y1 n=161 ρ=423; y2 n=74 ρ=671; y3 n=1936 ρ=908

## Evaluation

- 37 legs (6 batteries × 5 depths + ceiling × 7 depths)
- Policy A/B byte-identical; all 74 TSV pairs (37 main + 37 sidecar) byte-identical
- Release+correct identity vs M4: **5240/5240 = 100%**
- Path-rule verification: 604/604 y-decrease cases satisfy C ≤ min(C0,C_prev);
  0 cases of C strictly below min(C0,C_prev) (trauma never binds visibly)

## Implementation verification

- `pl_features` is a faithful port of frozen `ft_features8` (f1..f8 all 8 verified)
- `rel4 = (L_t == L_1)` matches trainer's counting rule exactly
- Sidecar columns (12): id depth t correct rel f1 f5 my y m C0 C
