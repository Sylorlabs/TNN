# RUNLOG — Experiment (a): verify R2-4's 824/1,102 gate-side ceiling

**Prereg:** `PREREG_CEILING_TEST.md` §2 (commit `98080233c11a492916c4c54530c24b5fc66a9c4d`).
**Date:** 2026-09-23. **Toolchain:** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.

## Inputs (frozen, SHA-verified before build)
- `case_r24_rk3.txt`: `ea49515fbff14b280ea62d4e05015f71a310ae957680c767c6b46bc5e48cda42`
- `expect_r24_rk3.txt`: `c49147100b0c3dd07a35a524a2907d4e08415ff64df194d36efd5c01f8762b98`
- `diagnose.zag`: `2aed8371d2245b3c1ac2bef9251a2bb7dc30b25f64fdc7539824324dbcbd6243`
- Natives: `R33_NATIVE_IO_V1.zag` (`e6379ddb…`), `R33_NATIVE_SHA256_V2.zag` (`9824f6db…`).

## Build
`znc diagnose.zag` → `diagnose` (118,670 bytes). Analyzer warnings only (3, pre-existing).

## Runs (3×)
`./diagnose case_r24_rk3.txt expect_r24_rk3.txt report_N.txt > stdout_N.txt`, N=1,2,3.

| Run | Exit | stdout SHA-256 | report SHA-256 |
|-----|------|----------------|----------------|
| 1 | 0 | `d1162477310b777f94c53e7f4d2f7584829ad8c7d2aa68513cb846bdb3fbaa93` | `9ee3bdecdd103181e11e25201f425e1e1d6faba346a04c62f80f33ee142e7b0f` |
| 2 | 0 | `d1162477310b777f94c53e7f4d2f7584829ad8c7d2aa68513cb846bdb3fbaa93` | `9ee3bdecdd103181e11e25201f425e1e1d6faba346a04c62f80f33ee142e7b0f` |
| 3 | 0 | `d1162477310b777f94c53e7f4d2f7584829ad8c7d2aa68513cb846bdb3fbaa93` | `9ee3bdecdd103181e11e25201f425e1e1d6faba346a04c62f80f33ee142e7b0f` |

**Byte-identical ×3: YES** (1 unique SHA).

## Key output lines (identical all runs)
```
DIAG,LOAD,0,11840
DIAG,REPRODUCE,0,104
DIAG,CHC,1102
DIAG,REPLAY,0,0
DIAG,KNOW,0,1062,824
DIAG,BUCKETS,278,621,99,0,0
DIAG,CEIL,1,824
DIAG,VERDICT,1,1
```

## Prereg criteria check
1. 3 byte-identical: **PASS**.
2. `DIAG,CEIL,1,824` (tension=1, ceil=824): **PASS**.
3. Input SHAs match §1; `DIAG,REPRODUCE,0,104` (0 mismatch vs expect): **PASS**.

**Verdict (a): REAL.** The `824/1,102 = 74.77%` gate-side ceiling is independently
reproduced. K3 buckets confirmed: never-PASS 278, conflict-withheld 621,
suppressed 99, pred0 0, other 0. Gate replay fidelity 0/11,840 mismatches.
