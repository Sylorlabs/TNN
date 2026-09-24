# CAST AUDIT — ZNC-2026-09-21-007 exposure, full lab tree
**Date:** 2026-09-24 (PDT) · **Auditor:** forensic subagent (b)+(c) · **Scope:** `~/workspace/tnn-lab`, all `*.zag` (10,587 files)
**Bug:** `nio_alloc(N) as []i32/[]u32/[]u16` miscompiles indexed access when 2+ same-size casts are allocated consecutively (2nd+ arrays' slots 0–2 read a previous array's slots at a layout-dependent offset; 9–11 in the 2026-09-21 probe, 65–67 in the CERT RV3 probe). `as []i64/[]u64` probed clean (sibling re-probing now — treated as PROVISIONALLY-OK).
**Method:** automated whole-tree sweep (code vs `//`-comment disambiguation), per-function cast-sequence extraction with allocation-size resolution, enclosing-function attribution. Cross-validated against the independent 2026-09-21 CERTIFIER-REBUILD audit (`redteam/certifier-rebuild/CAST_AUDIT.md`) — identical file set and classifications.

## 1. Complete inventory — code casts (`as []i32/[]u32/[]u16` in code, not comments)

73 code casts in 9 functions across 5 files. **All 73 are `[]i32`; zero `as []u32` / `as []u16` casts exist in code anywhere in the lab** (they appear only in comments).

| # | File (lab-relative) | Line | Function | Cast | Alloc size | Class | Sibling-rule note |
|---|---|---|---|---|---|---|---|
| 1 | `units/arms/V/cl/arm.zag` | 224 | `main` | `[]i32` | `4096 * 4` | **SINGLE** | STANDS: single cast proven safe by tprobe7. Upgrades to SUSPECT only if the sibling widens the trigger scope beyond consecutive same-size. |
| 2 | `units/arms/V/cl/arm.zag` | 111 | `vb_encode` | `[]i32` | `n * 4` | **SINGLE** | STANDS: single cast proven safe by tprobe7. Upgrades to SUSPECT only if the sibling widens the trigger scope beyond consecutive same-size. |
| 3 | `wave12/step1a-v2/armc-rerun-2026-09-21/thincert/builds/certsrc/thincert.zag` | 763 | `main` | `[]i32` | `512` | **SUSPECT** | STANDS: matches the proven trigger exactly (consecutive same-size casts; CERT RV3 white-box proof covers the `let r:[]u8=nio_alloc(N); r as []i32` variable form). Downgrades only if the sibling proves the variable-form immune (unlikely — real-world crash confirms it). |
| 4 | `wave12/step1a-v2/armc-rerun-2026-09-21/thincert/builds/certsrc/thincert.zag` | 764 | `main` | `[]i32` | `512` | **SUSPECT** | STANDS: matches the proven trigger exactly (consecutive same-size casts; CERT RV3 white-box proof covers the `let r:[]u8=nio_alloc(N); r as []i32` variable form). Downgrades only if the sibling proves the variable-form immune (unlikely — real-world crash confirms it). |
| 5 | `wave12/step1a-v2/armc-rerun-2026-09-21/thincert/builds/certsrc/thincert.zag` | 765 | `main` | `[]i32` | `512` | **SUSPECT** | STANDS: matches the proven trigger exactly (consecutive same-size casts; CERT RV3 white-box proof covers the `let r:[]u8=nio_alloc(N); r as []i32` variable form). Downgrades only if the sibling proves the variable-form immune (unlikely — real-world crash confirms it). |
| 6 | `wave12/step1a-v2/armc-rerun-2026-09-21/thincert/builds/certsrc/thincert.zag` | 772 | `main` | `[]i32` | `4` | **SUSPECT** | STANDS: matches the proven trigger exactly (consecutive same-size casts; CERT RV3 white-box proof covers the `let r:[]u8=nio_alloc(N); r as []i32` variable form). Downgrades only if the sibling proves the variable-form immune (unlikely — real-world crash confirms it). |
| 7 | `wave12/step1a-v2/armc-rerun-2026-09-21/thincert/builds/certsrc/thincert.zag` | 849 | `main` | `[]i32` | `512` | **SUSPECT** | STANDS: matches the proven trigger exactly (consecutive same-size casts; CERT RV3 white-box proof covers the `let r:[]u8=nio_alloc(N); r as []i32` variable form). Downgrades only if the sibling proves the variable-form immune (unlikely — real-world crash confirms it). |
| 8 | `wave12/step1a-v2/armc-rerun-2026-09-21/thincert/builds/certsrc/thincert.zag` | 850 | `main` | `[]i32` | `512` | **SUSPECT** | STANDS: matches the proven trigger exactly (consecutive same-size casts; CERT RV3 white-box proof covers the `let r:[]u8=nio_alloc(N); r as []i32` variable form). Downgrades only if the sibling proves the variable-form immune (unlikely — real-world crash confirms it). |
| 9 | `wave12/step1a-v2/armc-rerun-2026-09-21/thincert/builds/certsrc/thincert.zag` | 652 | `norm_import` | `[]i32` | `256` | **SUSPECT** | STANDS: matches the proven trigger exactly (consecutive same-size casts; CERT RV3 white-box proof covers the `let r:[]u8=nio_alloc(N); r as []i32` variable form). Downgrades only if the sibling proves the variable-form immune (unlikely — real-world crash confirms it). |
| 10 | `wave12/step1a-v2/armc-rerun-2026-09-21/thincert/builds/certsrc/thincert.zag` | 653 | `norm_import` | `[]i32` | `256` | **SUSPECT** | STANDS: matches the proven trigger exactly (consecutive same-size casts; CERT RV3 white-box proof covers the `let r:[]u8=nio_alloc(N); r as []i32` variable form). Downgrades only if the sibling proves the variable-form immune (unlikely — real-world crash confirms it). |
| 11 | `wave12/step1a-v2/armc-rerun-2026-09-21/thincert/builds/certsrc/thincert.zag` | 666 | `norm_import` | `[]i32` | `256` | **SUSPECT** | STANDS: matches the proven trigger exactly (consecutive same-size casts; CERT RV3 white-box proof covers the `let r:[]u8=nio_alloc(N); r as []i32` variable form). Downgrades only if the sibling proves the variable-form immune (unlikely — real-world crash confirms it). |
| 12 | `wave12/step1a-v2/checker/rngscan_v2.zag` | 823 | `main` | `[]i32` | `800004` | **SUSPECT** | STANDS: matches the proven trigger exactly (consecutive same-size casts; CERT RV3 white-box proof covers the `let r:[]u8=nio_alloc(N); r as []i32` variable form). Downgrades only if the sibling proves the variable-form immune (unlikely — real-world crash confirms it). |
| 13 | `wave12/step1a-v2/checker/rngscan_v2.zag` | 824 | `main` | `[]i32` | `256` | **SUSPECT** | STANDS: matches the proven trigger exactly (consecutive same-size casts; CERT RV3 white-box proof covers the `let r:[]u8=nio_alloc(N); r as []i32` variable form). Downgrades only if the sibling proves the variable-form immune (unlikely — real-world crash confirms it). |
| 14 | `wave12/step1a-v2/checker/rngscan_v2.zag` | 825 | `main` | `[]i32` | `256` | **SUSPECT** | STANDS: matches the proven trigger exactly (consecutive same-size casts; CERT RV3 white-box proof covers the `let r:[]u8=nio_alloc(N); r as []i32` variable form). Downgrades only if the sibling proves the variable-form immune (unlikely — real-world crash confirms it). |
| 15 | `wave12/step1a-v2/checker/rngscan_v2.zag` | 826 | `main` | `[]i32` | `256` | **SUSPECT** | STANDS: matches the proven trigger exactly (consecutive same-size casts; CERT RV3 white-box proof covers the `let r:[]u8=nio_alloc(N); r as []i32` variable form). Downgrades only if the sibling proves the variable-form immune (unlikely — real-world crash confirms it). |
| 16 | `wave12/step1a-v2/checker/rngscan_v2.zag` | 827 | `main` | `[]i32` | `256` | **SUSPECT** | STANDS: matches the proven trigger exactly (consecutive same-size casts; CERT RV3 white-box proof covers the `let r:[]u8=nio_alloc(N); r as []i32` variable form). Downgrades only if the sibling proves the variable-form immune (unlikely — real-world crash confirms it). |
| 17 | `wave12/step1a-v2/checker/rngscan_v2.zag` | 828 | `main` | `[]i32` | `256` | **SUSPECT** | STANDS: matches the proven trigger exactly (consecutive same-size casts; CERT RV3 white-box proof covers the `let r:[]u8=nio_alloc(N); r as []i32` variable form). Downgrades only if the sibling proves the variable-form immune (unlikely — real-world crash confirms it). |
| 18 | `wave12/step1a-v2/checker/rngscan_v2.zag` | 829 | `main` | `[]i32` | `256` | **SUSPECT** | STANDS: matches the proven trigger exactly (consecutive same-size casts; CERT RV3 white-box proof covers the `let r:[]u8=nio_alloc(N); r as []i32` variable form). Downgrades only if the sibling proves the variable-form immune (unlikely — real-world crash confirms it). |
| 19 | `wave12/step1a-v2/checker/rngscan_v2.zag` | 830 | `main` | `[]i32` | `256` | **SUSPECT** | STANDS: matches the proven trigger exactly (consecutive same-size casts; CERT RV3 white-box proof covers the `let r:[]u8=nio_alloc(N); r as []i32` variable form). Downgrades only if the sibling proves the variable-form immune (unlikely — real-world crash confirms it). |
| 20 | `wave12/step1a-v2/checker/rngscan_v2.zag` | 831 | `main` | `[]i32` | `2048` | **SUSPECT** | STANDS: matches the proven trigger exactly (consecutive same-size casts; CERT RV3 white-box proof covers the `let r:[]u8=nio_alloc(N); r as []i32` variable form). Downgrades only if the sibling proves the variable-form immune (unlikely — real-world crash confirms it). |
| 21 | `wave12/step1a-v2/checker/rngscan_v2.zag` | 832 | `main` | `[]i32` | `2048` | **SUSPECT** | STANDS: matches the proven trigger exactly (consecutive same-size casts; CERT RV3 white-box proof covers the `let r:[]u8=nio_alloc(N); r as []i32` variable form). Downgrades only if the sibling proves the variable-form immune (unlikely — real-world crash confirms it). |
| 22 | `wave12/step1a-v2/checker/rngscan_v2.zag` | 833 | `main` | `[]i32` | `2048` | **SUSPECT** | STANDS: matches the proven trigger exactly (consecutive same-size casts; CERT RV3 white-box proof covers the `let r:[]u8=nio_alloc(N); r as []i32` variable form). Downgrades only if the sibling proves the variable-form immune (unlikely — real-world crash confirms it). |
| 23 | `wave12/step1a-v2/checker/rngscan_v2.zag` | 834 | `main` | `[]i32` | `2048` | **SUSPECT** | STANDS: matches the proven trigger exactly (consecutive same-size casts; CERT RV3 white-box proof covers the `let r:[]u8=nio_alloc(N); r as []i32` variable form). Downgrades only if the sibling proves the variable-form immune (unlikely — real-world crash confirms it). |
| 24 | `wave12/step1a-v2/checker/rngscan_v2.zag` | 835 | `main` | `[]i32` | `2048` | **SUSPECT** | STANDS: matches the proven trigger exactly (consecutive same-size casts; CERT RV3 white-box proof covers the `let r:[]u8=nio_alloc(N); r as []i32` variable form). Downgrades only if the sibling proves the variable-form immune (unlikely — real-world crash confirms it). |
| 25 | `wave12/step1a-v2/checker/rngscan_v2.zag` | 836 | `main` | `[]i32` | `2048` | **SUSPECT** | STANDS: matches the proven trigger exactly (consecutive same-size casts; CERT RV3 white-box proof covers the `let r:[]u8=nio_alloc(N); r as []i32` variable form). Downgrades only if the sibling proves the variable-form immune (unlikely — real-world crash confirms it). |
| 26 | `wave12/step1a-v2/checker/rngscan_v2.zag` | 837 | `main` | `[]i32` | `2048` | **SUSPECT** | STANDS: matches the proven trigger exactly (consecutive same-size casts; CERT RV3 white-box proof covers the `let r:[]u8=nio_alloc(N); r as []i32` variable form). Downgrades only if the sibling proves the variable-form immune (unlikely — real-world crash confirms it). |
| 27 | `wave12/step1a-v2/checker/rngscan_v2.zag` | 838 | `main` | `[]i32` | `4` | **SUSPECT** | STANDS: matches the proven trigger exactly (consecutive same-size casts; CERT RV3 white-box proof covers the `let r:[]u8=nio_alloc(N); r as []i32` variable form). Downgrades only if the sibling proves the variable-form immune (unlikely — real-world crash confirms it). |
| 28 | `wave12/step1a-v2/checker/rngscan_v2.zag` | 839 | `main` | `[]i32` | `4` | **SUSPECT** | STANDS: matches the proven trigger exactly (consecutive same-size casts; CERT RV3 white-box proof covers the `let r:[]u8=nio_alloc(N); r as []i32` variable form). Downgrades only if the sibling proves the variable-form immune (unlikely — real-world crash confirms it). |
| 29 | `wave12/step1a-v2/checker/rngscan_v2.zag` | 613 | `scan_uninit` | `[]i32` | `512` | **SUSPECT** | STANDS: matches the proven trigger exactly (consecutive same-size casts; CERT RV3 white-box proof covers the `let r:[]u8=nio_alloc(N); r as []i32` variable form). Downgrades only if the sibling proves the variable-form immune (unlikely — real-world crash confirms it). |
| 30 | `wave12/step1a-v2/checker/rngscan_v2.zag` | 614 | `scan_uninit` | `[]i32` | `512` | **SUSPECT** | STANDS: matches the proven trigger exactly (consecutive same-size casts; CERT RV3 white-box proof covers the `let r:[]u8=nio_alloc(N); r as []i32` variable form). Downgrades only if the sibling proves the variable-form immune (unlikely — real-world crash confirms it). |
| 31 | `wave12/step1a-v2/checker/rngscan_v2.zag` | 615 | `scan_uninit` | `[]i32` | `512` | **SUSPECT** | STANDS: matches the proven trigger exactly (consecutive same-size casts; CERT RV3 white-box proof covers the `let r:[]u8=nio_alloc(N); r as []i32` variable form). Downgrades only if the sibling proves the variable-form immune (unlikely — real-world crash confirms it). |
| 32 | `wave12/step1a-v2/checker/rngscan_v2.zag` | 616 | `scan_uninit` | `[]i32` | `512` | **SUSPECT** | STANDS: matches the proven trigger exactly (consecutive same-size casts; CERT RV3 white-box proof covers the `let r:[]u8=nio_alloc(N); r as []i32` variable form). Downgrades only if the sibling proves the variable-form immune (unlikely — real-world crash confirms it). |
| 33 | `wave12/step1a-v2/checker/rngscan_v2.zag` | 617 | `scan_uninit` | `[]i32` | `512` | **SUSPECT** | STANDS: matches the proven trigger exactly (consecutive same-size casts; CERT RV3 white-box proof covers the `let r:[]u8=nio_alloc(N); r as []i32` variable form). Downgrades only if the sibling proves the variable-form immune (unlikely — real-world crash confirms it). |
| 34 | `wave12/step1a-v2/checker/rngscan_v2.zag` | 665 | `scan_uninit` | `[]i32` | `4` | **SUSPECT** | STANDS: matches the proven trigger exactly (consecutive same-size casts; CERT RV3 white-box proof covers the `let r:[]u8=nio_alloc(N); r as []i32` variable form). Downgrades only if the sibling proves the variable-form immune (unlikely — real-world crash confirms it). |
| 35 | `wave12/step1a-v2/rngscan-v3/checker/rngscan_v3.zag` | 1268 | `main` | `[]i32` | `800004` | **SUSPECT** | STANDS: matches the proven trigger exactly (consecutive same-size casts; CERT RV3 white-box proof covers the `let r:[]u8=nio_alloc(N); r as []i32` variable form). Downgrades only if the sibling proves the variable-form immune (unlikely — real-world crash confirms it). |
| 36 | `wave12/step1a-v2/rngscan-v3/checker/rngscan_v3.zag` | 1269 | `main` | `[]i32` | `256` | **SUSPECT** | STANDS: matches the proven trigger exactly (consecutive same-size casts; CERT RV3 white-box proof covers the `let r:[]u8=nio_alloc(N); r as []i32` variable form). Downgrades only if the sibling proves the variable-form immune (unlikely — real-world crash confirms it). |
| 37 | `wave12/step1a-v2/rngscan-v3/checker/rngscan_v3.zag` | 1270 | `main` | `[]i32` | `256` | **SUSPECT** | STANDS: matches the proven trigger exactly (consecutive same-size casts; CERT RV3 white-box proof covers the `let r:[]u8=nio_alloc(N); r as []i32` variable form). Downgrades only if the sibling proves the variable-form immune (unlikely — real-world crash confirms it). |
| 38 | `wave12/step1a-v2/rngscan-v3/checker/rngscan_v3.zag` | 1271 | `main` | `[]i32` | `256` | **SUSPECT** | STANDS: matches the proven trigger exactly (consecutive same-size casts; CERT RV3 white-box proof covers the `let r:[]u8=nio_alloc(N); r as []i32` variable form). Downgrades only if the sibling proves the variable-form immune (unlikely — real-world crash confirms it). |
| 39 | `wave12/step1a-v2/rngscan-v3/checker/rngscan_v3.zag` | 1272 | `main` | `[]i32` | `256` | **SUSPECT** | STANDS: matches the proven trigger exactly (consecutive same-size casts; CERT RV3 white-box proof covers the `let r:[]u8=nio_alloc(N); r as []i32` variable form). Downgrades only if the sibling proves the variable-form immune (unlikely — real-world crash confirms it). |
| 40 | `wave12/step1a-v2/rngscan-v3/checker/rngscan_v3.zag` | 1273 | `main` | `[]i32` | `256` | **SUSPECT** | STANDS: matches the proven trigger exactly (consecutive same-size casts; CERT RV3 white-box proof covers the `let r:[]u8=nio_alloc(N); r as []i32` variable form). Downgrades only if the sibling proves the variable-form immune (unlikely — real-world crash confirms it). |
| 41 | `wave12/step1a-v2/rngscan-v3/checker/rngscan_v3.zag` | 1274 | `main` | `[]i32` | `256` | **SUSPECT** | STANDS: matches the proven trigger exactly (consecutive same-size casts; CERT RV3 white-box proof covers the `let r:[]u8=nio_alloc(N); r as []i32` variable form). Downgrades only if the sibling proves the variable-form immune (unlikely — real-world crash confirms it). |
| 42 | `wave12/step1a-v2/rngscan-v3/checker/rngscan_v3.zag` | 1275 | `main` | `[]i32` | `256` | **SUSPECT** | STANDS: matches the proven trigger exactly (consecutive same-size casts; CERT RV3 white-box proof covers the `let r:[]u8=nio_alloc(N); r as []i32` variable form). Downgrades only if the sibling proves the variable-form immune (unlikely — real-world crash confirms it). |
| 43 | `wave12/step1a-v2/rngscan-v3/checker/rngscan_v3.zag` | 1276 | `main` | `[]i32` | `2048` | **SUSPECT** | STANDS: matches the proven trigger exactly (consecutive same-size casts; CERT RV3 white-box proof covers the `let r:[]u8=nio_alloc(N); r as []i32` variable form). Downgrades only if the sibling proves the variable-form immune (unlikely — real-world crash confirms it). |
| 44 | `wave12/step1a-v2/rngscan-v3/checker/rngscan_v3.zag` | 1277 | `main` | `[]i32` | `2048` | **SUSPECT** | STANDS: matches the proven trigger exactly (consecutive same-size casts; CERT RV3 white-box proof covers the `let r:[]u8=nio_alloc(N); r as []i32` variable form). Downgrades only if the sibling proves the variable-form immune (unlikely — real-world crash confirms it). |
| 45 | `wave12/step1a-v2/rngscan-v3/checker/rngscan_v3.zag` | 1278 | `main` | `[]i32` | `2048` | **SUSPECT** | STANDS: matches the proven trigger exactly (consecutive same-size casts; CERT RV3 white-box proof covers the `let r:[]u8=nio_alloc(N); r as []i32` variable form). Downgrades only if the sibling proves the variable-form immune (unlikely — real-world crash confirms it). |
| 46 | `wave12/step1a-v2/rngscan-v3/checker/rngscan_v3.zag` | 1279 | `main` | `[]i32` | `2048` | **SUSPECT** | STANDS: matches the proven trigger exactly (consecutive same-size casts; CERT RV3 white-box proof covers the `let r:[]u8=nio_alloc(N); r as []i32` variable form). Downgrades only if the sibling proves the variable-form immune (unlikely — real-world crash confirms it). |
| 47 | `wave12/step1a-v2/rngscan-v3/checker/rngscan_v3.zag` | 1280 | `main` | `[]i32` | `2048` | **SUSPECT** | STANDS: matches the proven trigger exactly (consecutive same-size casts; CERT RV3 white-box proof covers the `let r:[]u8=nio_alloc(N); r as []i32` variable form). Downgrades only if the sibling proves the variable-form immune (unlikely — real-world crash confirms it). |
| 48 | `wave12/step1a-v2/rngscan-v3/checker/rngscan_v3.zag` | 1281 | `main` | `[]i32` | `2048` | **SUSPECT** | STANDS: matches the proven trigger exactly (consecutive same-size casts; CERT RV3 white-box proof covers the `let r:[]u8=nio_alloc(N); r as []i32` variable form). Downgrades only if the sibling proves the variable-form immune (unlikely — real-world crash confirms it). |
| 49 | `wave12/step1a-v2/rngscan-v3/checker/rngscan_v3.zag` | 1282 | `main` | `[]i32` | `2048` | **SUSPECT** | STANDS: matches the proven trigger exactly (consecutive same-size casts; CERT RV3 white-box proof covers the `let r:[]u8=nio_alloc(N); r as []i32` variable form). Downgrades only if the sibling proves the variable-form immune (unlikely — real-world crash confirms it). |
| 50 | `wave12/step1a-v2/rngscan-v3/checker/rngscan_v3.zag` | 1283 | `main` | `[]i32` | `1024` | **SUSPECT** | STANDS: matches the proven trigger exactly (consecutive same-size casts; CERT RV3 white-box proof covers the `let r:[]u8=nio_alloc(N); r as []i32` variable form). Downgrades only if the sibling proves the variable-form immune (unlikely — real-world crash confirms it). |
| 51 | `wave12/step1a-v2/rngscan-v3/checker/rngscan_v3.zag` | 1284 | `main` | `[]i32` | `1024` | **SUSPECT** | STANDS: matches the proven trigger exactly (consecutive same-size casts; CERT RV3 white-box proof covers the `let r:[]u8=nio_alloc(N); r as []i32` variable form). Downgrades only if the sibling proves the variable-form immune (unlikely — real-world crash confirms it). |
| 52 | `wave12/step1a-v2/rngscan-v3/checker/rngscan_v3.zag` | 1285 | `main` | `[]i32` | `1024` | **SUSPECT** | STANDS: matches the proven trigger exactly (consecutive same-size casts; CERT RV3 white-box proof covers the `let r:[]u8=nio_alloc(N); r as []i32` variable form). Downgrades only if the sibling proves the variable-form immune (unlikely — real-world crash confirms it). |
| 53 | `wave12/step1a-v2/rngscan-v3/checker/rngscan_v3.zag` | 1286 | `main` | `[]i32` | `1024` | **SUSPECT** | STANDS: matches the proven trigger exactly (consecutive same-size casts; CERT RV3 white-box proof covers the `let r:[]u8=nio_alloc(N); r as []i32` variable form). Downgrades only if the sibling proves the variable-form immune (unlikely — real-world crash confirms it). |
| 54 | `wave12/step1a-v2/rngscan-v3/checker/rngscan_v3.zag` | 1287 | `main` | `[]i32` | `80004` | **SUSPECT** | STANDS: matches the proven trigger exactly (consecutive same-size casts; CERT RV3 white-box proof covers the `let r:[]u8=nio_alloc(N); r as []i32` variable form). Downgrades only if the sibling proves the variable-form immune (unlikely — real-world crash confirms it). |
| 55 | `wave12/step1a-v2/rngscan-v3/checker/rngscan_v3.zag` | 1288 | `main` | `[]i32` | `96` | **SUSPECT** | STANDS: matches the proven trigger exactly (consecutive same-size casts; CERT RV3 white-box proof covers the `let r:[]u8=nio_alloc(N); r as []i32` variable form). Downgrades only if the sibling proves the variable-form immune (unlikely — real-world crash confirms it). |
| 56 | `wave12/step1a-v2/rngscan-v3/checker/rngscan_v3.zag` | 1289 | `main` | `[]i32` | `96` | **SUSPECT** | STANDS: matches the proven trigger exactly (consecutive same-size casts; CERT RV3 white-box proof covers the `let r:[]u8=nio_alloc(N); r as []i32` variable form). Downgrades only if the sibling proves the variable-form immune (unlikely — real-world crash confirms it). |
| 57 | `wave12/step1a-v2/rngscan-v3/checker/rngscan_v3.zag` | 1290 | `main` | `[]i32` | `96` | **SUSPECT** | STANDS: matches the proven trigger exactly (consecutive same-size casts; CERT RV3 white-box proof covers the `let r:[]u8=nio_alloc(N); r as []i32` variable form). Downgrades only if the sibling proves the variable-form immune (unlikely — real-world crash confirms it). |
| 58 | `wave12/step1a-v2/rngscan-v3/checker/rngscan_v3.zag` | 1291 | `main` | `[]i32` | `96` | **SUSPECT** | STANDS: matches the proven trigger exactly (consecutive same-size casts; CERT RV3 white-box proof covers the `let r:[]u8=nio_alloc(N); r as []i32` variable form). Downgrades only if the sibling proves the variable-form immune (unlikely — real-world crash confirms it). |
| 59 | `wave12/step1a-v2/rngscan-v3/checker/rngscan_v3.zag` | 1292 | `main` | `[]i32` | `96` | **SUSPECT** | STANDS: matches the proven trigger exactly (consecutive same-size casts; CERT RV3 white-box proof covers the `let r:[]u8=nio_alloc(N); r as []i32` variable form). Downgrades only if the sibling proves the variable-form immune (unlikely — real-world crash confirms it). |
| 60 | `wave12/step1a-v2/rngscan-v3/checker/rngscan_v3.zag` | 1293 | `main` | `[]i32` | `96` | **SUSPECT** | STANDS: matches the proven trigger exactly (consecutive same-size casts; CERT RV3 white-box proof covers the `let r:[]u8=nio_alloc(N); r as []i32` variable form). Downgrades only if the sibling proves the variable-form immune (unlikely — real-world crash confirms it). |
| 61 | `wave12/step1a-v2/rngscan-v3/checker/rngscan_v3.zag` | 1294 | `main` | `[]i32` | `96` | **SUSPECT** | STANDS: matches the proven trigger exactly (consecutive same-size casts; CERT RV3 white-box proof covers the `let r:[]u8=nio_alloc(N); r as []i32` variable form). Downgrades only if the sibling proves the variable-form immune (unlikely — real-world crash confirms it). |
| 62 | `wave12/step1a-v2/rngscan-v3/checker/rngscan_v3.zag` | 1295 | `main` | `[]i32` | `96` | **SUSPECT** | STANDS: matches the proven trigger exactly (consecutive same-size casts; CERT RV3 white-box proof covers the `let r:[]u8=nio_alloc(N); r as []i32` variable form). Downgrades only if the sibling proves the variable-form immune (unlikely — real-world crash confirms it). |
| 63 | `wave12/step1a-v2/rngscan-v3/checker/rngscan_v3.zag` | 1296 | `main` | `[]i32` | `4` | **SUSPECT** | STANDS: matches the proven trigger exactly (consecutive same-size casts; CERT RV3 white-box proof covers the `let r:[]u8=nio_alloc(N); r as []i32` variable form). Downgrades only if the sibling proves the variable-form immune (unlikely — real-world crash confirms it). |
| 64 | `wave12/step1a-v2/rngscan-v3/checker/rngscan_v3.zag` | 1297 | `main` | `[]i32` | `4` | **SUSPECT** | STANDS: matches the proven trigger exactly (consecutive same-size casts; CERT RV3 white-box proof covers the `let r:[]u8=nio_alloc(N); r as []i32` variable form). Downgrades only if the sibling proves the variable-form immune (unlikely — real-world crash confirms it). |
| 65 | `wave12/step1a-v2/thin-certifier/certifier/thincert.zag` | 763 | `main` | `[]i32` | `512` | **SUSPECT** | STANDS: matches the proven trigger exactly (consecutive same-size casts; CERT RV3 white-box proof covers the `let r:[]u8=nio_alloc(N); r as []i32` variable form). Downgrades only if the sibling proves the variable-form immune (unlikely — real-world crash confirms it). |
| 66 | `wave12/step1a-v2/thin-certifier/certifier/thincert.zag` | 764 | `main` | `[]i32` | `512` | **SUSPECT** | STANDS: matches the proven trigger exactly (consecutive same-size casts; CERT RV3 white-box proof covers the `let r:[]u8=nio_alloc(N); r as []i32` variable form). Downgrades only if the sibling proves the variable-form immune (unlikely — real-world crash confirms it). |
| 67 | `wave12/step1a-v2/thin-certifier/certifier/thincert.zag` | 765 | `main` | `[]i32` | `512` | **SUSPECT** | STANDS: matches the proven trigger exactly (consecutive same-size casts; CERT RV3 white-box proof covers the `let r:[]u8=nio_alloc(N); r as []i32` variable form). Downgrades only if the sibling proves the variable-form immune (unlikely — real-world crash confirms it). |
| 68 | `wave12/step1a-v2/thin-certifier/certifier/thincert.zag` | 772 | `main` | `[]i32` | `4` | **SUSPECT** | STANDS: matches the proven trigger exactly (consecutive same-size casts; CERT RV3 white-box proof covers the `let r:[]u8=nio_alloc(N); r as []i32` variable form). Downgrades only if the sibling proves the variable-form immune (unlikely — real-world crash confirms it). |
| 69 | `wave12/step1a-v2/thin-certifier/certifier/thincert.zag` | 849 | `main` | `[]i32` | `512` | **SUSPECT** | STANDS: matches the proven trigger exactly (consecutive same-size casts; CERT RV3 white-box proof covers the `let r:[]u8=nio_alloc(N); r as []i32` variable form). Downgrades only if the sibling proves the variable-form immune (unlikely — real-world crash confirms it). |
| 70 | `wave12/step1a-v2/thin-certifier/certifier/thincert.zag` | 850 | `main` | `[]i32` | `512` | **SUSPECT** | STANDS: matches the proven trigger exactly (consecutive same-size casts; CERT RV3 white-box proof covers the `let r:[]u8=nio_alloc(N); r as []i32` variable form). Downgrades only if the sibling proves the variable-form immune (unlikely — real-world crash confirms it). |
| 71 | `wave12/step1a-v2/thin-certifier/certifier/thincert.zag` | 652 | `norm_import` | `[]i32` | `256` | **SUSPECT** | STANDS: matches the proven trigger exactly (consecutive same-size casts; CERT RV3 white-box proof covers the `let r:[]u8=nio_alloc(N); r as []i32` variable form). Downgrades only if the sibling proves the variable-form immune (unlikely — real-world crash confirms it). |
| 72 | `wave12/step1a-v2/thin-certifier/certifier/thincert.zag` | 653 | `norm_import` | `[]i32` | `256` | **SUSPECT** | STANDS: matches the proven trigger exactly (consecutive same-size casts; CERT RV3 white-box proof covers the `let r:[]u8=nio_alloc(N); r as []i32` variable form). Downgrades only if the sibling proves the variable-form immune (unlikely — real-world crash confirms it). |
| 73 | `wave12/step1a-v2/thin-certifier/certifier/thincert.zag` | 666 | `norm_import` | `[]i32` | `256` | **SUSPECT** | STANDS: matches the proven trigger exactly (consecutive same-size casts; CERT RV3 white-box proof covers the `let r:[]u8=nio_alloc(N); r as []i32` variable form). Downgrades only if the sibling proves the variable-form immune (unlikely — real-world crash confirms it). |

**Class totals:** SUSPECT functions: 7 · SINGLE: 2 · UNKNOWN: 0 · ARENA (comment-only/workaround): see below.
**Files with code casts:** 5 — `wave12/step1a-v2/thin-certifier/certifier/thincert.zag`, `wave12/step1a-v2/armc-rerun-2026-09-21/thincert/builds/certsrc/thincert.zag` (byte-identical copy), `wave12/step1a-v2/checker/rngscan_v2.zag`, `wave12/step1a-v2/rngscan-v3/checker/rngscan_v3.zag`, `units/arms/V/cl/arm.zag`.

### Per-function cast sequences (source order)

**`units/arms/V/cl/arm.zag` :: `main` → SINGLE**
- L224 `as []i32` size `4096 * 4` — `let tokbuf:[]i32 = nio_alloc(4096 * 4) as []i32;`

**`units/arms/V/cl/arm.zag` :: `vb_encode` → SINGLE**
- L111 `as []i32` size `n * 4` — `let toks:[]i32 = nio_alloc(n * 4) as []i32;`

**`wave12/step1a-v2/armc-rerun-2026-09-21/thincert/builds/certsrc/thincert.zag` :: `main` → SUSPECT**
- L763 `as []i32` size `512` — `let mtierr:[]u8=nio_alloc(512); let mtier:[]i32=mtierr as []i32;`
- L764 `as []i32` size `512` — `let moffr:[]u8=nio_alloc(512); let moff:[]i32=moffr as []i32;`
- L765 `as []i32` size `512` — `let mlenr:[]u8=nio_alloc(512); let mlen:[]i32=mlenr as []i32;`
- L772 `as []i32` size `4` — `let mcpr:[]u8=nio_alloc(4); let mcp:[]i32=mcpr as []i32;`
- L849 `as []i32` size `512` — `let foffr:[]u8=nio_alloc(512); let foff:[]i32=foffr as []i32;`
- L850 `as []i32` size `512` — `let flenr:[]u8=nio_alloc(512); let flen:[]i32=flenr as []i32;`

**`wave12/step1a-v2/armc-rerun-2026-09-21/thincert/builds/certsrc/thincert.zag` :: `norm_import` → SUSPECT**
- L652 `as []i32` size `256` — `let coffr:[]u8=nio_alloc(256); let coff:[]i32=coffr as []i32;`
- L653 `as []i32` size `256` — `let clenr:[]u8=nio_alloc(256); let clen:[]i32=clenr as []i32;`
- L666 `as []i32` size `256` — `let str:[]u8=nio_alloc(256); let st:[]i32=str as []i32;`

**`wave12/step1a-v2/checker/rngscan_v2.zag` :: `main` → SUSPECT**
- L823 `as []i32` size `800004` — `let loffr:[]u8=nio_alloc(800004); let loff:[]i32=loffr as []i32;`
- L824 `as []i32` size `256` — `let fb0r:[]u8=nio_alloc(256); let fb0:[]i32=fb0r as []i32;`
- L825 `as []i32` size `256` — `let fb1r:[]u8=nio_alloc(256); let fb1:[]i32=fb1r as []i32;`
- L826 `as []i32` size `256` — `let fl0r:[]u8=nio_alloc(256); let fl0:[]i32=fl0r as []i32;`
- L827 `as []i32` size `256` — `let fl1r:[]u8=nio_alloc(256); let fl1:[]i32=fl1r as []i32;`
- L828 `as []i32` size `256` — `let fpor:[]u8=nio_alloc(256); let fpoff:[]i32=fpor as []i32;`
- L829 `as []i32` size `256` — `let fplr:[]u8=nio_alloc(256); let fplen:[]i32=fplr as []i32;`
- L830 `as []i32` size `256` — `let fscr:[]u8=nio_alloc(256); let fscan:[]i32=fscr as []i32;`
- L831 `as []i32` size `2048` — `let fnor:[]u8=nio_alloc(2048); let fname_off:[]i32=fnor as []i32;`
- L832 `as []i32` size `2048` — `let fnlr:[]u8=nio_alloc(2048); let fname_len:[]i32=fnlr as []i32;`
- L833 `as []i32` size `2048` — `let fnfr:[]u8=nio_alloc(2048); let fn_file:[]i32=fnfr as []i32;`
- L834 `as []i32` size `2048` — `let fnsr:[]u8=nio_alloc(2048); let fn_start:[]i32=fnsr as []i32;`
- L835 `as []i32` size `2048` — `let fner:[]u8=nio_alloc(2048); let fn_end:[]i32=fner as []i32;`
- L836 `as []i32` size `2048` — `let stkr:[]u8=nio_alloc(2048); let stack:[]i32=stkr as []i32;`
- L837 `as []i32` size `2048` — `let rchr:[]u8=nio_alloc(2048); let reach:[]i32=rchr as []i32;`
- L838 `as []i32` size `4` — `let jlpr:[]u8=nio_alloc(4); let jlp:[]i32=jlpr as []i32;`
- L839 `as []i32` size `4` — `let nhpr:[]u8=nio_alloc(4); let nhp:[]i32=nhpr as []i32;`

**`wave12/step1a-v2/checker/rngscan_v2.zag` :: `scan_uninit` → SUSPECT**
- L613 `as []i32` size `512` — `let voffr:[]u8=nio_alloc(512); let voff:[]i32=voffr as []i32;`
- L614 `as []i32` size `512` — `let vlnr:[]u8=nio_alloc(512); let vln:[]i32=vlnr as []i32;`
- L615 `as []i32` size `512` — `let vstr:[]u8=nio_alloc(512); let vst:[]i32=vstr as []i32;`
- L616 `as []i32` size `512` — `let valr:[]u8=nio_alloc(512); let valn:[]i32=valr as []i32;`
- L617 `as []i32` size `512` — `let vier:[]u8=nio_alloc(512); let vie:[]i32=vier as []i32;`
- L665 `as []i32` size `4` — `let retc:[]u8=nio_alloc(4); let retp:[]i32=retc as []i32;`

**`wave12/step1a-v2/rngscan-v3/checker/rngscan_v3.zag` :: `main` → SUSPECT**
- L1268 `as []i32` size `800004` — `let loffr:[]u8=nio_alloc(800004); let loff:[]i32=loffr as []i32;`
- L1269 `as []i32` size `256` — `let fb0r:[]u8=nio_alloc(256); let fb0:[]i32=fb0r as []i32;`
- L1270 `as []i32` size `256` — `let fb1r:[]u8=nio_alloc(256); let fb1:[]i32=fb1r as []i32;`
- L1271 `as []i32` size `256` — `let fl0r:[]u8=nio_alloc(256); let fl0:[]i32=fl0r as []i32;`
- L1272 `as []i32` size `256` — `let fl1r:[]u8=nio_alloc(256); let fl1:[]i32=fl1r as []i32;`
- L1273 `as []i32` size `256` — `let fpor:[]u8=nio_alloc(256); let fpoff:[]i32=fpor as []i32;`
- L1274 `as []i32` size `256` — `let fplr:[]u8=nio_alloc(256); let fplen:[]i32=fplr as []i32;`
- L1275 `as []i32` size `256` — `let fscr:[]u8=nio_alloc(256); let fscan:[]i32=fscr as []i32;`
- L1276 `as []i32` size `2048` — `let fnor:[]u8=nio_alloc(2048); let fname_off:[]i32=fnor as []i32;`
- L1277 `as []i32` size `2048` — `let fnlr:[]u8=nio_alloc(2048); let fname_len:[]i32=fnlr as []i32;`
- L1278 `as []i32` size `2048` — `let fnfr:[]u8=nio_alloc(2048); let fn_file:[]i32=fnfr as []i32;`
- L1279 `as []i32` size `2048` — `let fnsr:[]u8=nio_alloc(2048); let fn_start:[]i32=fnsr as []i32;`
- L1280 `as []i32` size `2048` — `let fner:[]u8=nio_alloc(2048); let fn_end:[]i32=fner as []i32;`
- L1281 `as []i32` size `2048` — `let stkr:[]u8=nio_alloc(2048); let stack:[]i32=stkr as []i32;`
- L1282 `as []i32` size `2048` — `let rchr:[]u8=nio_alloc(2048); let reach:[]i32=rchr as []i32;`
- L1283 `as []i32` size `1024` — `let stor:[]u8=nio_alloc(1024); let stoff:[]i32=stor as []i32;`
- L1284 `as []i32` size `1024` — `let stlr:[]u8=nio_alloc(1024); let stlen:[]i32=stlr as []i32;`
- L1285 `as []i32` size `1024` — `let pnor:[]u8=nio_alloc(1024); let pinoff:[]i32=pnor as []i32;`
- L1286 `as []i32` size `1024` — `let pnlr:[]u8=nio_alloc(1024); let pinlen:[]i32=pnlr as []i32;`
- L1287 `as []i32` size `80004` — `let fdr:[]u8=nio_alloc(80004); let fdepth:[]i32=fdr as []i32;`
- L1288 `as []i32` size `96` — `let vofr:[]u8=nio_alloc(96); let v_off:[]i32=vofr as []i32;`
- L1289 `as []i32` size `96` — `let vlnr:[]u8=nio_alloc(96); let v_len:[]i32=vlnr as []i32;`
- L1290 `as []i32` size `96` — `let varr:[]u8=nio_alloc(96); let v_alloc:[]i32=varr as []i32;`
- L1291 `as []i32` size `96` — `let vmr:[]u8=nio_alloc(96); let v_master:[]i32=vmr as []i32;`
- L1292 `as []i32` size `96` — `let vsr:[]u8=nio_alloc(96); let v_skip:[]i32=vsr as []i32;`
- L1293 `as []i32` size `96` — `let vcsr:[]u8=nio_alloc(96); let v_cstart:[]i32=vcsr as []i32;`
- L1294 `as []i32` size `96` — `let vcer:[]u8=nio_alloc(96); let v_cend:[]i32=vcer as []i32;`
- L1295 `as []i32` size `96` — `let vhr:[]u8=nio_alloc(96); let v_hit:[]i32=vhr as []i32;`
- L1296 `as []i32` size `4` — `let jlpr:[]u8=nio_alloc(4); let jlp:[]i32=jlpr as []i32;`
- L1297 `as []i32` size `4` — `let nhpr:[]u8=nio_alloc(4); let nhp:[]i32=nhpr as []i32;`

**`wave12/step1a-v2/thin-certifier/certifier/thincert.zag` :: `main` → SUSPECT**
- L763 `as []i32` size `512` — `let mtierr:[]u8=nio_alloc(512); let mtier:[]i32=mtierr as []i32;`
- L764 `as []i32` size `512` — `let moffr:[]u8=nio_alloc(512); let moff:[]i32=moffr as []i32;`
- L765 `as []i32` size `512` — `let mlenr:[]u8=nio_alloc(512); let mlen:[]i32=mlenr as []i32;`
- L772 `as []i32` size `4` — `let mcpr:[]u8=nio_alloc(4); let mcp:[]i32=mcpr as []i32;`
- L849 `as []i32` size `512` — `let foffr:[]u8=nio_alloc(512); let foff:[]i32=foffr as []i32;`
- L850 `as []i32` size `512` — `let flenr:[]u8=nio_alloc(512); let flen:[]i32=flenr as []i32;`

**`wave12/step1a-v2/thin-certifier/certifier/thincert.zag` :: `norm_import` → SUSPECT**
- L652 `as []i32` size `256` — `let coffr:[]u8=nio_alloc(256); let coff:[]i32=coffr as []i32;`
- L653 `as []i32` size `256` — `let clenr:[]u8=nio_alloc(256); let clen:[]i32=clenr as []i32;`
- L666 `as []i32` size `256` — `let str:[]u8=nio_alloc(256); let st:[]i32=str as []i32;`

### ARENA — files mentioning the pattern only in comments (already on the []u8-arena workaround)

118 files contain `as []i32/[]u32/[]u16` solely inside `//` comments documenting ZNC-2026-09-21-007 and the arena convention. Spot-verified sample (all comment-only): `units/teachers/harness/harness.zag` (the wave-12 teacher harness — see §4), `units/teachers/arm1/teacher.zag`, `units/teachers/arm3/varB/teacher.zag`, `units/teachers/arm3/varC/teacher.zag`, `prose-learning/{src,v2/src,v3/src}/prose_learn*.zag`, `docs/lab/prose-learning/v3/src/prose_learn3.zag`, `senses/rebuild/a_raw/sense.zag`, `htd-1/builds/comp/comp.zag`, `dialogue/**/*.zag` (18 files), `units/arms/T/work/bbattery/batt.zag`, `math/math.zag`, `senses/pam-rebuild/**` (30+ files), `senses/web-search/internet-trial/phase3/repairs_v4/**` (30+ files), `knowledge/kb_control/crewB/src/kbcore.zag`, `deliberation_depth/**/dlb_util.zag`, `consciousness_cost/harness_cost/dlb_util.zag`, `docs/lab/physics_rulebook/gen/physgen.zag`, `training_paradigms/source_trust/merge_validate/impl/**/merge.zag`, `kb/autopsy/channels/src/chan.zag`.

## 2. Blast radius — file → dependent verdicts → rank → reasoning

Rank scale: **(1) VERDICT LIKELY WRONG** — miscompile plausibly changes a reported number · **(2) NEEDS RE-VERIFICATION** — survived possibly by allocator luck; must be rebuilt from arena sources + rerun (byte-identical rerun of the committed binary is NOT sufficient — the binary itself may be miscompiled) · **(3) PROVABLY BENIGN** — pattern present but values provably unaffected.

| File | Dependent verdicts / evidence | Rank | Reasoning |
|---|---|---|---|
| `wave12/step1a-v2/thin-certifier/certifier/thincert.zag` (+ byte-identical copy at `wave12/step1a-v2/armc-rerun-2026-09-21/thincert/builds/certsrc/thincert.zag`) | (a) Thin-certifier gate evidence 2026-09-20 (clean representative build PASS attestation + 5 dirty-plant attestations; frozen source sha `9b55fa2f…`, binary `d5e4de74…`) → feeds the **unsigned** Arm C gate amendment (replay+certifier as no-RNG gate; `wave12/step1a-v2/gate/AMENDMENT_2026-09-20_ARMC_GATE_S3.md` + `RESIDUAL_RISK_STATEMENT_ARMC.md`) — Arm C stays parked until Micah signs. (b) `armc-rerun-2026-09-21/RE-RUN-LOG.md` §2 independent re-derivation (rebuilt old source byte-identical, re-ran). (c) CERT RV3 0-flips claim (`crossref/runs/T2/CERT/reverify/VERIFY.md`). | **(2)** for (a)/(b); **(3)** for (c) | All suspect tables are indexed in live paths: `mtier/moff/mlen` in the per-file R1 checks (L782–819), `foff/flen` in the R1c builddir walk (L865–867), `coff/clen/st` in `norm_import` (L663–690). CERT RV3 white-box proof: slots 0–2 of the 2nd/3rd casts alias the previous array's slots 65–67; ≤65-entry manifests read deterministic-but-wrong entries 0–2 (allocator luck), ≥~70-entry manifests crash with "invalid or double free" (no attestation). For (c): RV3 ran 13/14 adversarial cases 3× old vs new with byte-identical attestation digests (`reverify/evidence/thincert_full_digests.txt`, 73 digests) and 0 flips; largest historical manifest has 2 entries — **no verdict flip, impact NONE**. For (a)/(b): the committed attestations predate RV3 and were allocator-luck-dependent; byte-identical rerun of the old binary (done in armc-rerun) proves determinism, not correctness. **Fix: rebuild from the arena sources (`redteam/certifier-rebuild/thincert_rb.zag`, zero casts) + rerun the step1a-v2 evidence set; do not re-certify from old-binary reruns.** Note: `n_v2=` tripwire readings inside these attestations come from the retired rngscan_v2 (below) — informational only, not a rule. |
| `wave12/step1a-v2/checker/rngscan_v2.zag` | (a) Its own validation evidence `wave12/step1a-v2/results/` (5 dirty + 1 clean attestations; frozen source `ee962e53…`, binary `9bbaf539…`). (b) Informational `n_v2=` tripwire field inside thin-certifier attestations (not a rule). | **RETIRED — no verdict depends on it** | v2 was killed by its own blind red team and is **not a gate**; the no-RNG gate is now hardened-replay + thin-certifier (Micah-approved, amendment drafted). Its `results/` attestations are superseded self-validation, cited by no committed arm verdict. The 5×512 (`scan_uninit` L613–617), 7×256 + 7×2048 + 2×4 (`main` L824–839) sequences are all indexed — the instrument is untrusted. Documented kill mechanisms were design blind spots (zeroed pages hiding uninit reads; a hand-rolled data structure the scanner couldn't see through; a map hidden behind an exemption) — **not attributed to ZNC-007**; no evidence ties the miscompile to the kills, but it cannot be ruled out as a contributing factor to a missed plant. **Do not revive without an arena rebuild (none exists for v2 — retire the `n_v2` tripwire or rebuild it).** |
| `wave12/step1a-v2/rngscan-v3/checker/rngscan_v3.zag` | Its own validation (`rngscan-v3/results/`, `attestations/`); killed by its blind red team; not a gate. | **RETIRED — no verdict depends on it** | Same as v2: 7×256, 7×2048, 4×1024, 8×96, 2×4 consecutive sequences in `main` (L1269–1297), all indexed. **Arena rebuild already exists** (`redteam/certifier-rebuild/rngscan_v3_rb.zag`, used in the T2-CERT red-team re-derivation). No committed verdict rests on v3 output. |
| `units/arms/V/cl/arm.zag` | `units/arms/V/VERDICT.md` — Arm V (BPE enemy): **PASS on build specs / UNADJUDICATED on comparative** (VC1–VC4 blocked by missing frozen harness). | **(3)** | Both casts are SINGLE (L111 `n*4`, L224 `4096*4`) — the proven-safe pattern per the tprobe7 reproducer (a lone cast reads correctly). The verdict's build specs were additionally cross-verified 33/33 against an independent Python reference (merge choices, IDs, ranks, counts). Residual risk only if the sibling widens the trigger scope beyond consecutive same-size. |
| `units/teachers/harness/harness.zag` | Teacher-protocol driver for the Q1/teacher-battery workstreams (`q1-planted-teaches`, `q1b-teacher-bakeoff`, `q1c-teacher-conflict`, `q1n-noisy-teacher`, `q1tq-noisy50`, `units/teachers/battery/*`). | **ARENA — remediated 2026-09-21; (3) for verdicts on covered paths** | See §4. Post-fix behavior verified byte-identical to pre-fix baseline; det 5/5, pertA 5/5, pertB 5/5 byte-identical. Pre-fix verdicts whose harness paths are covered by that battery are unaffected; verdicts exercising uncovered paths → (2). |

## 3. The 33-use question and the sibling-rule column

The AGENTS.md note ("the wave-12 teacher harness uses this cast 33 times") counts the **pre-remediation** file. The 2026-09-21 CERTIFIER-REBUILD audit independently found the same 5-file code-hit set as this audit (their counts: rngscan_v3 30, thincert 9, thincert-copy 9, rngscan_v2 23, arm.zag 2 — all reproduced exactly here). Disposition since then: rngscan_v3 and thincert rebuilt to arenas; rngscan_v2 left live as an informational tripwire (still SUSPECT — see §2); arm.zag singles left as-is.

**Sibling-rule column** (per §1 table): every SUSPECT classification rests on the *proven core* of the trigger (2+ consecutive same-size casts, CERT RV3 white-box proof covering the `let r:[]u8=nio_alloc(N); r as []i32` variable form). A sibling finding can only *narrow* the trigger (e.g. "only direct `nio_alloc(N) as []i32` casts, not the variable form") — which would downgrade thincert/rngscan from SUSPECT to UNKNOWN, but the real-world thincert_old crash makes that narrowing unlikely. A *widening* (e.g. single casts affected) would upgrade the two arm.zag SINGLEs. The u64/i64 re-probe can only upgrade the §5 list.

## 4. harness.zag 33-use analysis (wave-12 teacher harness)

**Verdict: ARENA — the 33 uses are gone; the file was remediated 2026-09-21 and the AGENTS.md note is stale.**

- Current state (`units/teachers/harness/harness.zag`, 3001 lines): **zero** `as []i32`, **zero** `as []u32`, **zero** `as []u16` in code — the sole `as []i32` match is the `// ---- ZNC-007 typed-array arenas ----` documentation comment (L167–176). All indexed narrow tables now go through `[]u8` arenas with explicit LE accessors (`au32_get/set`, `ai32_get/set` with sign extension, `au16_get/set`; L177–184), documented as byte-layout-identical to the native LE typed arrays.
- Remediation record: `units/teachers/harness/ZNC007_AUDIT.md` (2026-09-21 night, Track B coordinator). It found 6 trigger sites pre-fix: RTape `eoff`/`elen` (CONFIRMED — replay length/event-type validation), `order_a`/`order_b` in `test_det` (CONFIRMED — determinism verdict), `Student.alast` (SUSPECT), `etype` `as []u16` (CONFIRMED, 16 index sites), plus a live semantic bug (a missed 16th etype site reading byte *j* instead of u16 event *j*). All converted to arenas; remediation marked COMPLETE 2026-09-21 ~10:40 UTC with independent coordinator verification.
- Behavioral evidence (fix crew, in ZNC007_AUDIT.md): post-patch `all` stdout/stderr **byte-identical** to pre-patch baseline; det 5/5 byte-identical, pertA 5/5, pertB 5/5. The malformed/seq double-free and pertA panic pre-exist the patch (identical before/after) — separate open ticket.
- Remaining `as []i64` (1, L706, SINGLE — `i64a`, fine) and `as []u64` (20; §5). Consecutive same-size u64 sequences exist in **test-only** paths: `med_init` (L2169/2171/2172, 3×2048) and `test_smoke` (L2187/2188/2192, 3×2048) — allocated and freed without indexed reads (`a1`/`a2`/`a6` never indexed; `m.a`/`m.b` stored in struct). `student_consider_t` has `nio_alloc(0) as []u64` pairs (L1374/1400) — zero-size, never indexed. All PROVISIONALLY-OK pending the sibling's u64 re-probe; would upgrade to SUSPECT only if u64 aliasing is proven. Note: ZNC007_AUDIT.md site 3 records *empirically observed* `as []u64` indexed-write corruption seen by the repair crew — passed to the sibling as a re-probe lead.
- Blast radius of the pre-fix harness: the CONFIRMED sites sat in the replay-parse path (`elen[0..2]` vs expected constants, `rt.elen[j]`, `etype[j]`) and the determinism test — i.e. pre-fix `test_replay` / `test_det` verdicts were the exposed surface. The byte-identical post-fix evidence covers the standard battery; verdicts from harness paths outside det/pertA/pertB/`all` should be re-run under the arena build (rank 2), everything on covered paths is rank 3.

## 5. `as []i64` / `as []u64` — PROVISIONALLY-OK inventory

486 files, **649 code casts** (6 further matches are comments). Original 2026-09-21 probe: `as []i64` CLEAN, `as []u64` CLEAN for back-to-back same-size casts. A sibling agent is re-probing across layouts now; until that lands these stay PROVISIONALLY-OK, not confirmed.

Functions with **consecutive same-size** i64/u64 casts — these become SUSPECT if the re-probe finds u64/i64 aliasing:

| File | Function | Consecutive same-size sequence (line:size-bytes) | Indexed? / notes |
|---|---|---|---|
| `knowledge/keyboard/audit281.zag` | `main` | L549–550 `4096*8`, L552–553 `21000*8` | Flagged for sibling rule; usage not yet traced |
| `knowledge/keyboard/run_battery.zag` | `main` | L125–126 `4096*8`, L128–129 `65536*8` | Flagged for sibling rule; usage not yet traced |
| `units/teachers/harness/harness.zag` | `med_init` | L2169/2171/2172 `2048` (u64) | Test scaffolding; arrays freed without indexed reads |
| `units/teachers/harness/harness.zag` | `test_smoke` | L2187/2188/2192 `2048` (u64) | Test scaffolding; `a1`/`a2`/`a6` never indexed |
| `units/teachers/harness/harness.zag` | `student_consider_t` | L1374/1400 `0` (u64) | Zero-size dummies, never indexed — benign regardless of probe outcome |
| `units/teachers/learner/forcepin/scratch/test_wired.zag` | `main` | L43–44 `16` (u64) | Scratch test |
| `units/teachers/learner/tests/test_determinism.zag` | `run_once` | L16–17 `16` (u64) | Test driver |
| `units/teachers/learner/tests/test_driver.zag` | `main` | L17–18 `16` (u64) | Test driver |
| `units/teachers/learner/tests/test_pins.zag` | `main` | L187–188 `16` (u64); `mk_grounds` L68–69 `16` (u64) | Test driver |
| `units/teachers/learner/tests/test_retract.zag` | `main` | L19–20 `16` (u64) | Test driver |

All other i64/u64 code casts (single casts, or multiple casts with no consecutive same-size pair in the function) carry no proven-trigger shape even if u64 re-probes dirty. Full per-file line listing: `u64_perfile.json` (486 files).

## 6. Method notes and limitations

- Sweep pattern: `\bas\s+\[\](i32|u32|u16)\b` / `(i64|u64)` per line after `//`-comment stripping (naive quote handling). Casts split across two source lines would be missed — none observed in the 73 code hits (every one resolved to a `nio_alloc` size on its line).
- Allocation-size resolution: direct `nio_alloc(N) as []T` plus the `let v:[]u8=nio_alloc(N); … v as []T` variable form (the form used by all SUSPECT sites). All 73 code-cast sizes resolved; zero unresolved.
- Classification is on the per-function cast sequence in source order (loop-carried allocations noted but not specially modeled).
- The lab tree is not a git repo; committed-verdict mapping was done via working-tree docs (`docs/lab`, `crossref`, `wave12`) and MEMORY.md. Pins cited were copied from those sources, not invented.
- Did NOT edit `~/AGENTS.md` (coordinator consolidates).

## Artifacts

- This report: `~/workspace/i32-investigation/CAST_AUDIT.md`
- Machine-readable per-function inventory: `~/workspace/i32-investigation/per_fn.json`
- Raw hit lists: `~/workspace/i32-investigation/cast_hits_i32.txt` (207 incl. comments), `~/workspace/i32-investigation/cast_hits_i64.txt` (655 incl. comments)
- u64/i64 per-file line listing: `~/workspace/i32-investigation/u64_perfile.json`
- Audit script: `~/workspace/i32-investigation/audit.py`

## Appendix A — `as []i64/[]u64` per-file line listing (PROVISIONALLY-OK)

Format: `file` — line:type …

- `GROK47_OVERNIGHT/teacher/work/c3s_src/forcepin.zag` — 83:i64, 84:i64, 85:i64, 86:i64
- `GROK47_OVERNIGHT/teacher/work/legA/forcepin.zag` — 83:i64, 84:i64, 85:i64, 86:i64
- `coding/reflection/cleanliness/sources/CLN-G4/tnn.zag` — 9:i64
- `coding/reflection/cleanliness/sources/CLN-G5/tnn.zag` — 19:i64
- `coding/reflection/cleanliness/work/selfcrit/CLN-G4_dirty.zag` — 13:i64
- `coding/reflection/long_horizon/machinery/lh_emit.zag` — 493:i64
- `coding/reflection/long_horizon/results/A8.zag` — 33:i64
- `coding/reflection/long_horizon/results/A9.zag` — 33:i64
- `coding/reflection/long_horizon/results/B6.zag` — 33:i64
- `coding/reflection/long_horizon/results/B7.zag` — 33:i64
- `coding/reflection/long_horizon/results/C7.zag` — 33:i64
- `coding/reflection/long_horizon/results/C8.zag` — 33:i64
- `coding/reflection/long_horizon_adv/machinery/adv_emit.zag` — 159:i64
- `coding/reflection/long_horizon_adv2/machinery/adv2_emit.zag` — 159:i64
- `coding/reflection/loop/learner.zag` — 216:i64, 321:i64, 439:i64, 459:i64
- `coding/reflection/loop/work/run/CLN-G4-DIRTY/CLN-G4-DIRTY_i1.zag` — 9:i64
- `coding/reflection/speed_intel/learner_si3.zag` — 208:i64, 313:i64, 431:i64, 451:i64
- `coding/reflection/speed_intel/work_a1/learner.zag` — 208:i64, 313:i64, 431:i64, 451:i64
- `coding/reflection/speed_intel/work_a1/pilot16/run/G05-t4_countocc/G05-t4_countocc_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_a1/pilot16/run/G08-t4_selsort/G08-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_a1/pilot16/run/G09-t4_countocc2/G09-t4_countocc2_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_a1/pilot16b/run/G05-t4_countocc/G05-t4_countocc_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_a1/pilot16b/run/G09-t4_countocc2/G09-t4_countocc2_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_a1/sweep_si/b16_r1/run/G05-t4_countocc/G05-t4_countocc_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_a1/sweep_si/b16_r1/run/G08-t4_selsort/G08-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_a1/sweep_si/b16_r1/run/G09-t4_countocc2/G09-t4_countocc2_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_a1/sweep_si/b16_r2/run/G05-t4_countocc/G05-t4_countocc_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_a1/sweep_si/b16_r2/run/G08-t4_selsort/G08-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_a1/sweep_si/b16_r2/run/G09-t4_countocc2/G09-t4_countocc2_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_a1/sweep_si/b16_r3/run/G05-t4_countocc/G05-t4_countocc_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_a1/sweep_si/b16_r3/run/G08-t4_selsort/G08-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_a1/sweep_si/b16_r3/run/G09-t4_countocc2/G09-t4_countocc2_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_a1/sweep_si/b2_r1/run/G05-t4_countocc/G05-t4_countocc_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_a1/sweep_si/b2_r1/run/G08-t4_selsort/G08-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_a1/sweep_si/b2_r1/run/G09-t4_countocc2/G09-t4_countocc2_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_a1/sweep_si/b2_r2/run/G05-t4_countocc/G05-t4_countocc_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_a1/sweep_si/b2_r2/run/G08-t4_selsort/G08-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_a1/sweep_si/b2_r2/run/G09-t4_countocc2/G09-t4_countocc2_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_a1/sweep_si/b2_r3/run/G05-t4_countocc/G05-t4_countocc_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_a1/sweep_si/b2_r3/run/G08-t4_selsort/G08-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_a1/sweep_si/b2_r3/run/G09-t4_countocc2/G09-t4_countocc2_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_a1/sweep_si/b4_r1/run/G05-t4_countocc/G05-t4_countocc_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_a1/sweep_si/b4_r1/run/G08-t4_selsort/G08-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_a1/sweep_si/b4_r1/run/G09-t4_countocc2/G09-t4_countocc2_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_a1/sweep_si/b4_r2/run/G05-t4_countocc/G05-t4_countocc_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_a1/sweep_si/b4_r2/run/G08-t4_selsort/G08-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_a1/sweep_si/b4_r2/run/G09-t4_countocc2/G09-t4_countocc2_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_a1/sweep_si/b4_r3/run/G05-t4_countocc/G05-t4_countocc_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_a1/sweep_si/b4_r3/run/G08-t4_selsort/G08-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_a1/sweep_si/b4_r3/run/G09-t4_countocc2/G09-t4_countocc2_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_a1/sweep_si/b8_r1/run/G05-t4_countocc/G05-t4_countocc_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_a1/sweep_si/b8_r1/run/G08-t4_selsort/G08-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_a1/sweep_si/b8_r1/run/G09-t4_countocc2/G09-t4_countocc2_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_a1/sweep_si/b8_r2/run/G05-t4_countocc/G05-t4_countocc_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_a1/sweep_si/b8_r2/run/G08-t4_selsort/G08-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_a1/sweep_si/b8_r2/run/G09-t4_countocc2/G09-t4_countocc2_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_a1/sweep_si/b8_r3/run/G05-t4_countocc/G05-t4_countocc_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_a1/sweep_si/b8_r3/run/G08-t4_selsort/G08-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_a1/sweep_si/b8_r3/run/G09-t4_countocc2/G09-t4_countocc2_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_a2/learner_si2.zag` — 208:i64, 313:i64, 431:i64, 451:i64
- `coding/reflection/speed_intel/work_a4/learner_si4.zag` — 208:i64, 313:i64, 431:i64, 451:i64
- `coding/reflection/speed_intel/work_a4/runs/b2_none_r1/work/G05-t4_countocc/G05-t4_countocc_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_a4/runs/b2_none_r1/work/G08-t4_selsort/G08-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_a4/runs/b2_none_r1/work/G09-t4_countocc2/G09-t4_countocc2_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_a4/runs/b2_none_r2/work/G05-t4_countocc/G05-t4_countocc_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_a4/runs/b2_none_r2/work/G08-t4_selsort/G08-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_a4/runs/b2_none_r2/work/G09-t4_countocc2/G09-t4_countocc2_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_a4/runs/b2_none_r3/work/G05-t4_countocc/G05-t4_countocc_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_a4/runs/b2_none_r3/work/G08-t4_selsort/G08-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_a4/runs/b2_none_r3/work/G09-t4_countocc2/G09-t4_countocc2_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_a4/runs/b4_a_r1/work/G05-t4_countocc/G05-t4_countocc_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_a4/runs/b4_a_r1/work/G08-t4_selsort/G08-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_a4/runs/b4_a_r1/work/G09-t4_countocc2/G09-t4_countocc2_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_a4/runs/b4_a_r2/work/G05-t4_countocc/G05-t4_countocc_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_a4/runs/b4_a_r2/work/G08-t4_selsort/G08-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_a4/runs/b4_a_r2/work/G09-t4_countocc2/G09-t4_countocc2_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_a4/runs/b4_a_r3/work/G05-t4_countocc/G05-t4_countocc_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_a4/runs/b4_a_r3/work/G08-t4_selsort/G08-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_a4/runs/b4_a_r3/work/G09-t4_countocc2/G09-t4_countocc2_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_a4/runs/b4_b_r1/work/G05-t4_countocc/G05-t4_countocc_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_a4/runs/b4_b_r1/work/G08-t4_selsort/G08-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_a4/runs/b4_b_r1/work/G09-t4_countocc2/G09-t4_countocc2_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_a4/runs/b4_b_r2/work/G05-t4_countocc/G05-t4_countocc_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_a4/runs/b4_b_r2/work/G08-t4_selsort/G08-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_a4/runs/b4_b_r2/work/G09-t4_countocc2/G09-t4_countocc2_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_a4/runs/b4_b_r3/work/G05-t4_countocc/G05-t4_countocc_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_a4/runs/b4_b_r3/work/G08-t4_selsort/G08-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_a4/runs/b4_b_r3/work/G09-t4_countocc2/G09-t4_countocc2_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_a4/runs/b4_c_r1/work/G05-t4_countocc/G05-t4_countocc_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_a4/runs/b4_c_r1/work/G08-t4_selsort/G08-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_a4/runs/b4_c_r1/work/G09-t4_countocc2/G09-t4_countocc2_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_a4/runs/b4_c_r2/work/G05-t4_countocc/G05-t4_countocc_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_a4/runs/b4_c_r2/work/G08-t4_selsort/G08-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_a4/runs/b4_c_r2/work/G09-t4_countocc2/G09-t4_countocc2_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_a4/runs/b4_c_r3/work/G05-t4_countocc/G05-t4_countocc_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_a4/runs/b4_c_r3/work/G08-t4_selsort/G08-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_a4/runs/b4_c_r3/work/G09-t4_countocc2/G09-t4_countocc2_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_a4/runs/b4_combo_r1/work/G05-t4_countocc/G05-t4_countocc_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_a4/runs/b4_combo_r1/work/G08-t4_selsort/G08-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_a4/runs/b4_combo_r1/work/G09-t4_countocc2/G09-t4_countocc2_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_a4/runs/b4_combo_r2/work/G05-t4_countocc/G05-t4_countocc_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_a4/runs/b4_combo_r2/work/G08-t4_selsort/G08-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_a4/runs/b4_combo_r2/work/G09-t4_countocc2/G09-t4_countocc2_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_a4/runs/b4_combo_r3/work/G05-t4_countocc/G05-t4_countocc_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_a4/runs/b4_combo_r3/work/G08-t4_selsort/G08-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_a4/runs/b4_combo_r3/work/G09-t4_countocc2/G09-t4_countocc2_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_a4/runs/b4_none_r1/work/G05-t4_countocc/G05-t4_countocc_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_a4/runs/b4_none_r1/work/G08-t4_selsort/G08-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_a4/runs/b4_none_r1/work/G09-t4_countocc2/G09-t4_countocc2_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_a4/runs/b4_none_r2/work/G05-t4_countocc/G05-t4_countocc_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_a4/runs/b4_none_r2/work/G08-t4_selsort/G08-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_a4/runs/b4_none_r2/work/G09-t4_countocc2/G09-t4_countocc2_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_a4/runs/b4_none_r3/work/G05-t4_countocc/G05-t4_countocc_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_a4/runs/b4_none_r3/work/G08-t4_selsort/G08-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_a4/runs/b4_none_r3/work/G09-t4_countocc2/G09-t4_countocc2_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_a4/runs/b4_si4none_r1/work/G05-t4_countocc/G05-t4_countocc_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_a4/runs/b4_si4none_r1/work/G08-t4_selsort/G08-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_a4/runs/b4_si4none_r1/work/G09-t4_countocc2/G09-t4_countocc2_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_a4/runs/b4_si4none_r2/work/G05-t4_countocc/G05-t4_countocc_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_a4/runs/b4_si4none_r2/work/G08-t4_selsort/G08-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_a4/runs/b4_si4none_r2/work/G09-t4_countocc2/G09-t4_countocc2_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_a4/runs/b4_si4none_r3/work/G05-t4_countocc/G05-t4_countocc_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_a4/runs/b4_si4none_r3/work/G08-t4_selsort/G08-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_a4/runs/b4_si4none_r3/work/G09-t4_countocc2/G09-t4_countocc2_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_adaptive_code/learner_adapt.zag` — 208:i64, 313:i64, 431:i64, 451:i64
- `coding/reflection/speed_intel/work_adaptive_code/pilot_fresh/run/G13-t4_selsort/G13-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_adaptive_code/sweep_adapt/a_fresh_r1/run/G13-t4_selsort/G13-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_adaptive_code/sweep_adapt/a_fresh_r2/run/G13-t4_selsort/G13-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_adaptive_code/sweep_adapt/a_fresh_r3/run/G13-t4_selsort/G13-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_adaptive_code/sweep_adapt/a_frozen_r1/run/G05-t4_countocc/G05-t4_countocc_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_adaptive_code/sweep_adapt/a_frozen_r1/run/G08-t4_selsort/G08-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_adaptive_code/sweep_adapt/a_frozen_r1/run/G09-t4_countocc2/G09-t4_countocc2_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_adaptive_code/sweep_adapt/a_frozen_r2/run/G05-t4_countocc/G05-t4_countocc_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_adaptive_code/sweep_adapt/a_frozen_r2/run/G08-t4_selsort/G08-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_adaptive_code/sweep_adapt/a_frozen_r2/run/G09-t4_countocc2/G09-t4_countocc2_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_adaptive_code/sweep_adapt/a_frozen_r3/run/G05-t4_countocc/G05-t4_countocc_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_adaptive_code/sweep_adapt/a_frozen_r3/run/G08-t4_selsort/G08-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_adaptive_code/sweep_adapt/a_frozen_r3/run/G09-t4_countocc2/G09-t4_countocc2_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_adaptive_code/sweep_adapt/b_fresh_r1/run/G13-t4_selsort/G13-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_adaptive_code/sweep_adapt/b_fresh_r2/run/G13-t4_selsort/G13-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_adaptive_code/sweep_adapt/b_fresh_r3/run/G13-t4_selsort/G13-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_adaptive_code/sweep_adapt/b_frozen_r1/run/G05-t4_countocc/G05-t4_countocc_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_adaptive_code/sweep_adapt/b_frozen_r1/run/G08-t4_selsort/G08-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_adaptive_code/sweep_adapt/b_frozen_r1/run/G09-t4_countocc2/G09-t4_countocc2_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_adaptive_code/sweep_adapt/b_frozen_r2/run/G05-t4_countocc/G05-t4_countocc_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_adaptive_code/sweep_adapt/b_frozen_r2/run/G08-t4_selsort/G08-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_adaptive_code/sweep_adapt/b_frozen_r2/run/G09-t4_countocc2/G09-t4_countocc2_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_adaptive_code/sweep_adapt/b_frozen_r3/run/G05-t4_countocc/G05-t4_countocc_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_adaptive_code/sweep_adapt/b_frozen_r3/run/G08-t4_selsort/G08-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_adaptive_code/sweep_adapt/b_frozen_r3/run/G09-t4_countocc2/G09-t4_countocc2_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_adaptive_code/sweep_adapt/c_fresh_r1/run/G13-t4_selsort/G13-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_adaptive_code/sweep_adapt/c_fresh_r2/run/G13-t4_selsort/G13-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_adaptive_code/sweep_adapt/c_fresh_r3/run/G13-t4_selsort/G13-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_adaptive_code/sweep_adapt/c_frozen_r1/run/G05-t4_countocc/G05-t4_countocc_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_adaptive_code/sweep_adapt/c_frozen_r1/run/G08-t4_selsort/G08-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_adaptive_code/sweep_adapt/c_frozen_r1/run/G09-t4_countocc2/G09-t4_countocc2_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_adaptive_code/sweep_adapt/c_frozen_r2/run/G05-t4_countocc/G05-t4_countocc_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_adaptive_code/sweep_adapt/c_frozen_r2/run/G08-t4_selsort/G08-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_adaptive_code/sweep_adapt/c_frozen_r2/run/G09-t4_countocc2/G09-t4_countocc2_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_adaptive_code/sweep_adapt/c_frozen_r3/run/G05-t4_countocc/G05-t4_countocc_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_adaptive_code/sweep_adapt/c_frozen_r3/run/G08-t4_selsort/G08-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_adaptive_code/sweep_adapt/c_frozen_r3/run/G09-t4_countocc2/G09-t4_countocc2_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_adaptive_code/sweep_adapt/ctl_fresh_r1/run/G13-t4_selsort/G13-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_adaptive_code/sweep_adapt/ctl_fresh_r2/run/G13-t4_selsort/G13-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_adaptive_code/sweep_adapt/ctl_fresh_r3/run/G13-t4_selsort/G13-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_adaptive_code/sweep_adapt/ctl_frozen_r1/run/G05-t4_countocc/G05-t4_countocc_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_adaptive_code/sweep_adapt/ctl_frozen_r1/run/G08-t4_selsort/G08-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_adaptive_code/sweep_adapt/ctl_frozen_r1/run/G09-t4_countocc2/G09-t4_countocc2_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_adaptive_code/sweep_adapt/ctl_frozen_r2/run/G05-t4_countocc/G05-t4_countocc_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_adaptive_code/sweep_adapt/ctl_frozen_r2/run/G08-t4_selsort/G08-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_adaptive_code/sweep_adapt/ctl_frozen_r2/run/G09-t4_countocc2/G09-t4_countocc2_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_adaptive_code/sweep_adapt/ctl_frozen_r3/run/G05-t4_countocc/G05-t4_countocc_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_adaptive_code/sweep_adapt/ctl_frozen_r3/run/G08-t4_selsort/G08-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_adaptive_code/sweep_adapt/ctl_frozen_r3/run/G09-t4_countocc2/G09-t4_countocc2_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_adaptive_code/sweep_adapt/d_fresh_r1/run/G13-t4_selsort/G13-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_adaptive_code/sweep_adapt/d_fresh_r2/run/G13-t4_selsort/G13-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_adaptive_code/sweep_adapt/d_fresh_r3/run/G13-t4_selsort/G13-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_adaptive_code/sweep_adapt/d_frozen_r1/run/G05-t4_countocc/G05-t4_countocc_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_adaptive_code/sweep_adapt/d_frozen_r1/run/G08-t4_selsort/G08-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_adaptive_code/sweep_adapt/d_frozen_r1/run/G09-t4_countocc2/G09-t4_countocc2_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_adaptive_code/sweep_adapt/d_frozen_r2/run/G05-t4_countocc/G05-t4_countocc_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_adaptive_code/sweep_adapt/d_frozen_r2/run/G08-t4_selsort/G08-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_adaptive_code/sweep_adapt/d_frozen_r2/run/G09-t4_countocc2/G09-t4_countocc2_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_adaptive_code/sweep_adapt/d_frozen_r3/run/G05-t4_countocc/G05-t4_countocc_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_adaptive_code/sweep_adapt/d_frozen_r3/run/G08-t4_selsort/G08-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_adaptive_code/sweep_adapt/d_frozen_r3/run/G09-t4_countocc2/G09-t4_countocc2_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_adaptive_code/sweep_adapt/e_fresh_r1/run/G13-t4_selsort/G13-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_adaptive_code/sweep_adapt/e_fresh_r2/run/G13-t4_selsort/G13-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_adaptive_code/sweep_adapt/e_fresh_r3/run/G13-t4_selsort/G13-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_adaptive_code/sweep_adapt/e_frozen_r1/run/G05-t4_countocc/G05-t4_countocc_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_adaptive_code/sweep_adapt/e_frozen_r1/run/G08-t4_selsort/G08-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_adaptive_code/sweep_adapt/e_frozen_r1/run/G09-t4_countocc2/G09-t4_countocc2_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_adaptive_code/sweep_adapt/e_frozen_r2/run/G05-t4_countocc/G05-t4_countocc_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_adaptive_code/sweep_adapt/e_frozen_r2/run/G08-t4_selsort/G08-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_adaptive_code/sweep_adapt/e_frozen_r2/run/G09-t4_countocc2/G09-t4_countocc2_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_adaptive_code/sweep_adapt/e_frozen_r3/run/G05-t4_countocc/G05-t4_countocc_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_adaptive_code/sweep_adapt/e_frozen_r3/run/G08-t4_selsort/G08-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_adaptive_code/sweep_adapt/e_frozen_r3/run/G09-t4_countocc2/G09-t4_countocc2_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_promo_loop/classic_work/G05-t4_countocc/G05-t4_countocc_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_promo_loop/classic_work/G08-t4_selsort/G08-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_promo_loop/classic_work/G09-t4_countocc2/G09-t4_countocc2_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_promo_loop/ctrl_r1_work/G05-t4_countocc/G05-t4_countocc_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_promo_loop/ctrl_r1_work/G08-t4_selsort/G08-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_promo_loop/ctrl_r1_work/G09-t4_countocc2/G09-t4_countocc2_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_promo_loop/ctrl_r2_work/G05-t4_countocc/G05-t4_countocc_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_promo_loop/ctrl_r2_work/G08-t4_selsort/G08-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_promo_loop/ctrl_r2_work/G09-t4_countocc2/G09-t4_countocc2_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_promo_loop/ctrl_r3_work/G05-t4_countocc/G05-t4_countocc_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_promo_loop/ctrl_r3_work/G08-t4_selsort/G08-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_promo_loop/ctrl_r3_work/G09-t4_countocc2/G09-t4_countocc2_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_promo_loop/new_r1_work/G05-t4_countocc/G05-t4_countocc_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_promo_loop/new_r1_work/G08-t4_selsort/G08-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_promo_loop/new_r1_work/G09-t4_countocc2/G09-t4_countocc2_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_promo_loop/new_r2_work/G05-t4_countocc/G05-t4_countocc_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_promo_loop/new_r2_work/G08-t4_selsort/G08-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_promo_loop/new_r2_work/G09-t4_countocc2/G09-t4_countocc2_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_promo_loop/new_r3_work/G05-t4_countocc/G05-t4_countocc_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_promo_loop/new_r3_work/G08-t4_selsort/G08-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_promo_loop/new_r3_work/G09-t4_countocc2/G09-t4_countocc2_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_promo_loop/si4none_r1_work/G05-t4_countocc/G05-t4_countocc_i1.zag` — 3:i64
- `coding/reflection/speed_intel/work_promo_loop/si4none_r1_work/G08-t4_selsort/G08-t4_selsort_i1.zag` — 19:i64
- `coding/reflection/speed_intel/work_promo_loop/si4none_r1_work/G09-t4_countocc2/G09-t4_countocc2_i1.zag` — 3:i64
- `coding/reflection/task1/harness/work/baseline_t4x/t1_03_i1.zag` — 9:i64
- `coding/reflection/task1/harness/work/baseline_t4x/t1_04_i1.zag` — 9:i64
- `coding/reflection/task1/harness/work/baseline_t4x/t2_01_i1.zag` — 19:i64
- `coding/reflection/task1/harness/work/baseline_t4x/t2_02_i1.zag` — 19:i64
- `coding/reflection/task1/harness/work/baseline_t4x/t4_02_i1.zag` — 3:i64
- `coding/reflection/task1/harness/work/baseline_t4x/t4_05_i1.zag` — 3:i64
- `coding/reflection/task1/harness/work/baseline_t4x/t4_11_i1.zag` — 19:i64
- `coding/reflection/task1/harness/work/baseline_t4x/t4m_05_i1.zag` — 3:i64
- `coding/reflection/task1/harness/work/final_inf/t1_03.zag` — 9:i64
- `coding/reflection/task1/harness/work/final_inf/t1_04.zag` — 9:i64
- `coding/reflection/task1/harness/work/final_inf/t2_01.zag` — 19:i64
- `coding/reflection/task1/harness/work/final_inf/t2_02.zag` — 19:i64
- `coding/reflection/task1/harness/work/final_inf/t2_03.zag` — 8:i64
- `coding/reflection/task1/harness/work/final_inf/t2_07.zag` — 3:i64
- `coding/reflection/task1/harness/work/final_inf/t4_02.zag` — 3:i64
- `coding/reflection/task1/harness/work/final_inf/t4_05.zag` — 3:i64
- `coding/reflection/task1/harness/work/final_inf/t4_11.zag` — 3:i64
- `coding/reflection/task1/harness/work/final_inf/t4m_05.zag` — 3:i64
- `coding/reflection/task1/harness/work/final_scr/t1_03.zag` — 9:i64
- `coding/reflection/task1/harness/work/final_scr/t1_04.zag` — 9:i64
- `coding/reflection/task1/harness/work/final_scr/t2_01.zag` — 19:i64
- `coding/reflection/task1/harness/work/final_scr/t2_02.zag` — 19:i64
- `coding/reflection/task1/harness/work/final_scr/t2_03.zag` — 8:i64
- `coding/reflection/task1/harness/work/final_scr/t2_07.zag` — 3:i64
- `coding/reflection/task1/harness/work/final_scr/t4_02.zag` — 3:i64
- `coding/reflection/task1/harness/work/final_scr/t4_05.zag` — 3:i64
- `coding/reflection/task1/harness/work/final_scr/t4_11.zag` — 3:i64
- `coding/reflection/task1/harness/work/final_scr/t4m_05.zag` — 3:i64
- `coding/reflection/task1/harness/work/rep_inf_1/t1_03.zag` — 9:i64
- `coding/reflection/task1/harness/work/rep_inf_1/t1_04.zag` — 9:i64
- `coding/reflection/task1/harness/work/rep_inf_1/t2_01.zag` — 19:i64
- `coding/reflection/task1/harness/work/rep_inf_1/t2_02.zag` — 19:i64
- `coding/reflection/task1/harness/work/rep_inf_1/t2_03.zag` — 8:i64
- `coding/reflection/task1/harness/work/rep_inf_1/t2_07.zag` — 3:i64
- `coding/reflection/task1/harness/work/rep_inf_1/t4_02.zag` — 3:i64
- `coding/reflection/task1/harness/work/rep_inf_1/t4_05.zag` — 3:i64
- `coding/reflection/task1/harness/work/rep_inf_1/t4_11.zag` — 3:i64
- `coding/reflection/task1/harness/work/rep_inf_1/t4m_05.zag` — 3:i64
- `coding/reflection/task1/harness/work/rep_inf_2/t1_03.zag` — 9:i64
- `coding/reflection/task1/harness/work/rep_inf_2/t1_04.zag` — 9:i64
- `coding/reflection/task1/harness/work/rep_inf_2/t2_01.zag` — 19:i64
- `coding/reflection/task1/harness/work/rep_inf_2/t2_02.zag` — 19:i64
- `coding/reflection/task1/harness/work/rep_inf_2/t2_03.zag` — 8:i64
- `coding/reflection/task1/harness/work/rep_inf_2/t2_07.zag` — 3:i64
- `coding/reflection/task1/harness/work/rep_inf_2/t4_02.zag` — 3:i64
- `coding/reflection/task1/harness/work/rep_inf_2/t4_05.zag` — 3:i64
- `coding/reflection/task1/harness/work/rep_inf_2/t4_11.zag` — 3:i64
- `coding/reflection/task1/harness/work/rep_inf_2/t4m_05.zag` — 3:i64
- `coding/reflection/task1/harness/work/rep_inf_3/t1_03.zag` — 9:i64
- `coding/reflection/task1/harness/work/rep_inf_3/t1_04.zag` — 9:i64
- `coding/reflection/task1/harness/work/rep_inf_3/t2_01.zag` — 19:i64
- `coding/reflection/task1/harness/work/rep_inf_3/t2_02.zag` — 19:i64
- `coding/reflection/task1/harness/work/rep_inf_3/t2_03.zag` — 8:i64
- `coding/reflection/task1/harness/work/rep_inf_3/t2_07.zag` — 3:i64
- `coding/reflection/task1/harness/work/rep_inf_3/t4_02.zag` — 3:i64
- `coding/reflection/task1/harness/work/rep_inf_3/t4_05.zag` — 3:i64
- `coding/reflection/task1/harness/work/rep_inf_3/t4_11.zag` — 3:i64
- `coding/reflection/task1/harness/work/rep_inf_3/t4m_05.zag` — 3:i64
- `coding/reflection/task1/harness/work/rep_inf_4/t1_03.zag` — 9:i64
- `coding/reflection/task1/harness/work/rep_inf_4/t1_04.zag` — 9:i64
- `coding/reflection/task1/harness/work/rep_inf_4/t2_01.zag` — 19:i64
- `coding/reflection/task1/harness/work/rep_inf_4/t2_02.zag` — 19:i64
- `coding/reflection/task1/harness/work/rep_inf_4/t2_03.zag` — 8:i64
- `coding/reflection/task1/harness/work/rep_inf_4/t2_07.zag` — 3:i64
- `coding/reflection/task1/harness/work/rep_inf_4/t4_02.zag` — 3:i64
- `coding/reflection/task1/harness/work/rep_inf_4/t4_05.zag` — 3:i64
- `coding/reflection/task1/harness/work/rep_inf_4/t4_11.zag` — 3:i64
- `coding/reflection/task1/harness/work/rep_inf_4/t4m_05.zag` — 3:i64
- `coding/reflection/task1/harness/work/rep_inf_5/t1_03.zag` — 9:i64
- `coding/reflection/task1/harness/work/rep_inf_5/t1_04.zag` — 9:i64
- `coding/reflection/task1/harness/work/rep_inf_5/t2_01.zag` — 19:i64
- `coding/reflection/task1/harness/work/rep_inf_5/t2_02.zag` — 19:i64
- `coding/reflection/task1/harness/work/rep_inf_5/t2_03.zag` — 8:i64
- `coding/reflection/task1/harness/work/rep_inf_5/t2_07.zag` — 3:i64
- `coding/reflection/task1/harness/work/rep_inf_5/t4_02.zag` — 3:i64
- `coding/reflection/task1/harness/work/rep_inf_5/t4_05.zag` — 3:i64
- `coding/reflection/task1/harness/work/rep_inf_5/t4_11.zag` — 3:i64
- `coding/reflection/task1/harness/work/rep_inf_5/t4m_05.zag` — 3:i64
- `coding/reflection/task1/harness/work/rep_scr_1/t1_03.zag` — 9:i64
- `coding/reflection/task1/harness/work/rep_scr_1/t1_04.zag` — 9:i64
- `coding/reflection/task1/harness/work/rep_scr_1/t2_01.zag` — 19:i64
- `coding/reflection/task1/harness/work/rep_scr_1/t2_02.zag` — 19:i64
- `coding/reflection/task1/harness/work/rep_scr_1/t2_03.zag` — 8:i64
- `coding/reflection/task1/harness/work/rep_scr_1/t2_07.zag` — 3:i64
- `coding/reflection/task1/harness/work/rep_scr_1/t4_02.zag` — 3:i64
- `coding/reflection/task1/harness/work/rep_scr_1/t4_05.zag` — 3:i64
- `coding/reflection/task1/harness/work/rep_scr_1/t4_11.zag` — 3:i64
- `coding/reflection/task1/harness/work/rep_scr_1/t4m_05.zag` — 3:i64
- `coding/reflection/task1/harness/work/rep_scr_2/t1_03.zag` — 9:i64
- `coding/reflection/task1/harness/work/rep_scr_2/t1_04.zag` — 9:i64
- `coding/reflection/task1/harness/work/rep_scr_2/t2_01.zag` — 19:i64
- `coding/reflection/task1/harness/work/rep_scr_2/t2_02.zag` — 19:i64
- `coding/reflection/task1/harness/work/rep_scr_2/t2_03.zag` — 8:i64
- `coding/reflection/task1/harness/work/rep_scr_2/t2_07.zag` — 3:i64
- `coding/reflection/task1/harness/work/rep_scr_2/t4_02.zag` — 3:i64
- `coding/reflection/task1/harness/work/rep_scr_2/t4_05.zag` — 3:i64
- `coding/reflection/task1/harness/work/rep_scr_2/t4_11.zag` — 3:i64
- `coding/reflection/task1/harness/work/rep_scr_2/t4m_05.zag` — 3:i64
- `coding/reflection/task1/harness/work/rep_scr_3/t1_03.zag` — 9:i64
- `coding/reflection/task1/harness/work/rep_scr_3/t1_04.zag` — 9:i64
- `coding/reflection/task1/harness/work/rep_scr_3/t2_01.zag` — 19:i64
- `coding/reflection/task1/harness/work/rep_scr_3/t2_02.zag` — 19:i64
- `coding/reflection/task1/harness/work/rep_scr_3/t2_03.zag` — 8:i64
- `coding/reflection/task1/harness/work/rep_scr_3/t2_07.zag` — 3:i64
- `coding/reflection/task1/harness/work/rep_scr_3/t4_02.zag` — 3:i64
- `coding/reflection/task1/harness/work/rep_scr_3/t4_05.zag` — 3:i64
- `coding/reflection/task1/harness/work/rep_scr_3/t4_11.zag` — 3:i64
- `coding/reflection/task1/harness/work/rep_scr_3/t4m_05.zag` — 3:i64
- `coding/reflection/task1/harness/work/rep_scr_4/t1_03.zag` — 9:i64
- `coding/reflection/task1/harness/work/rep_scr_4/t1_04.zag` — 9:i64
- `coding/reflection/task1/harness/work/rep_scr_4/t2_01.zag` — 19:i64
- `coding/reflection/task1/harness/work/rep_scr_4/t2_02.zag` — 19:i64
- `coding/reflection/task1/harness/work/rep_scr_4/t2_03.zag` — 8:i64
- `coding/reflection/task1/harness/work/rep_scr_4/t2_07.zag` — 3:i64
- `coding/reflection/task1/harness/work/rep_scr_4/t4_02.zag` — 3:i64
- `coding/reflection/task1/harness/work/rep_scr_4/t4_05.zag` — 3:i64
- `coding/reflection/task1/harness/work/rep_scr_4/t4_11.zag` — 3:i64
- `coding/reflection/task1/harness/work/rep_scr_4/t4m_05.zag` — 3:i64
- `coding/reflection/task1/harness/work/rep_scr_5/t1_03.zag` — 9:i64
- `coding/reflection/task1/harness/work/rep_scr_5/t1_04.zag` — 9:i64
- `coding/reflection/task1/harness/work/rep_scr_5/t2_01.zag` — 19:i64
- `coding/reflection/task1/harness/work/rep_scr_5/t2_02.zag` — 19:i64
- `coding/reflection/task1/harness/work/rep_scr_5/t2_03.zag` — 8:i64
- `coding/reflection/task1/harness/work/rep_scr_5/t2_07.zag` — 3:i64
- `coding/reflection/task1/harness/work/rep_scr_5/t4_02.zag` — 3:i64
- `coding/reflection/task1/harness/work/rep_scr_5/t4_05.zag` — 3:i64
- `coding/reflection/task1/harness/work/rep_scr_5/t4_11.zag` — 3:i64
- `coding/reflection/task1/harness/work/rep_scr_5/t4m_05.zag` — 3:i64
- `coding/reflection/task1/harness/work/run_informed_1/t1_03.zag` — 9:i64
- `coding/reflection/task1/harness/work/run_informed_1/t1_04.zag` — 9:i64
- `coding/reflection/task1/harness/work/run_informed_1/t2_01.zag` — 19:i64
- `coding/reflection/task1/harness/work/run_informed_1/t2_02.zag` — 19:i64
- `coding/reflection/task1/harness/work/run_informed_1/t2_03.zag` — 8:i64
- `coding/reflection/task1/harness/work/run_informed_1/t2_07.zag` — 3:i64
- `coding/reflection/task1/harness/work/run_informed_1/t4_02.zag` — 3:i64
- `coding/reflection/task1/harness/work/run_informed_1/t4_05.zag` — 3:i64
- `coding/reflection/task1/harness/work/run_informed_1/t4_11.zag` — 3:i64
- `coding/reflection/task1/harness/work/run_informed_1/t4m_05.zag` — 3:i64
- `coding/reflection/task1/harness/work/run_informed_r1/t1_03.zag` — 9:i64
- `coding/reflection/task1/harness/work/run_informed_r1/t1_04.zag` — 9:i64
- `coding/reflection/task1/harness/work/run_informed_r1/t2_01.zag` — 19:i64
- `coding/reflection/task1/harness/work/run_informed_r1/t2_02.zag` — 19:i64
- `coding/reflection/task1/harness/work/run_informed_r1/t2_03.zag` — 8:i64
- `coding/reflection/task1/harness/work/run_informed_r1/t2_07.zag` — 3:i64
- `coding/reflection/task1/harness/work/run_informed_r1/t4_02.zag` — 3:i64
- `coding/reflection/task1/harness/work/run_informed_r1/t4_05.zag` — 3:i64
- `coding/reflection/task1/harness/work/run_informed_r1/t4_11.zag` — 3:i64
- `coding/reflection/task1/harness/work/run_informed_r1/t4m_05.zag` — 3:i64
- `coding/reflection/task1/harness/work/run_informed_r2/t1_03.zag` — 9:i64
- `coding/reflection/task1/harness/work/run_informed_r2/t1_04.zag` — 9:i64
- `coding/reflection/task1/harness/work/run_informed_r2/t2_01.zag` — 19:i64
- `coding/reflection/task1/harness/work/run_informed_r2/t2_02.zag` — 19:i64
- `coding/reflection/task1/harness/work/run_informed_r2/t2_03.zag` — 8:i64
- `coding/reflection/task1/harness/work/run_informed_r2/t2_07.zag` — 3:i64
- `coding/reflection/task1/harness/work/run_informed_r2/t4_02.zag` — 3:i64
- `coding/reflection/task1/harness/work/run_informed_r2/t4_05.zag` — 3:i64
- `coding/reflection/task1/harness/work/run_informed_r2/t4_11.zag` — 3:i64
- `coding/reflection/task1/harness/work/run_informed_r2/t4m_05.zag` — 3:i64
- `coding/reflection/task1/harness/work/run_informed_r3/t1_03.zag` — 9:i64
- `coding/reflection/task1/harness/work/run_informed_r3/t1_04.zag` — 9:i64
- `coding/reflection/task1/harness/work/run_informed_r3/t2_01.zag` — 19:i64
- `coding/reflection/task1/harness/work/run_informed_r3/t2_02.zag` — 19:i64
- `coding/reflection/task1/harness/work/run_informed_r3/t2_03.zag` — 8:i64
- `coding/reflection/task1/harness/work/run_informed_r3/t2_07.zag` — 3:i64
- `coding/reflection/task1/harness/work/run_informed_r3/t4_02.zag` — 3:i64
- `coding/reflection/task1/harness/work/run_informed_r3/t4_05.zag` — 3:i64
- `coding/reflection/task1/harness/work/run_informed_r3/t4_11.zag` — 3:i64
- `coding/reflection/task1/harness/work/run_informed_r3/t4m_05.zag` — 3:i64
- `coding/reflection/task1/harness/work/run_informed_r4/t1_03.zag` — 9:i64
- `coding/reflection/task1/harness/work/run_informed_r4/t1_04.zag` — 9:i64
- `coding/reflection/task1/harness/work/run_informed_r4/t2_01.zag` — 19:i64
- `coding/reflection/task1/harness/work/run_informed_r4/t2_02.zag` — 19:i64
- `coding/reflection/task1/harness/work/run_informed_r4/t2_03.zag` — 8:i64
- `coding/reflection/task1/harness/work/run_informed_r4/t2_07.zag` — 3:i64
- `coding/reflection/task1/harness/work/run_informed_r4/t4_02.zag` — 3:i64
- `coding/reflection/task1/harness/work/run_informed_r4/t4_05.zag` — 3:i64
- `coding/reflection/task1/harness/work/run_informed_r4/t4_11.zag` — 3:i64
- `coding/reflection/task1/harness/work/run_informed_r4/t4m_05.zag` — 3:i64
- `coding/reflection/task1/harness/work/run_informed_r5/t1_03.zag` — 9:i64
- `coding/reflection/task1/harness/work/run_informed_r5/t1_04.zag` — 9:i64
- `coding/reflection/task1/harness/work/run_informed_r5/t2_01.zag` — 19:i64
- `coding/reflection/task1/harness/work/run_informed_r5/t2_02.zag` — 19:i64
- `coding/reflection/task1/harness/work/run_informed_r5/t2_03.zag` — 8:i64
- `coding/reflection/task1/harness/work/run_informed_r5/t2_07.zag` — 3:i64
- `coding/reflection/task1/harness/work/run_informed_r5/t4_02.zag` — 3:i64
- `coding/reflection/task1/harness/work/run_informed_r5/t4_05.zag` — 3:i64
- `coding/reflection/task1/harness/work/run_informed_r5/t4_11.zag` — 3:i64
- `coding/reflection/task1/harness/work/run_informed_r5/t4m_05.zag` — 3:i64
- `coding/reflection/task1/harness/work/run_scratch_r1/t1_03.zag` — 9:i64
- `coding/reflection/task1/harness/work/run_scratch_r1/t1_04.zag` — 9:i64
- `coding/reflection/task1/harness/work/run_scratch_r1/t2_01.zag` — 19:i64
- `coding/reflection/task1/harness/work/run_scratch_r1/t2_02.zag` — 19:i64
- `coding/reflection/task1/harness/work/run_scratch_r1/t2_03.zag` — 8:i64
- `coding/reflection/task1/harness/work/run_scratch_r1/t2_07.zag` — 3:i64
- `coding/reflection/task1/harness/work/run_scratch_r1/t4_02.zag` — 3:i64
- `coding/reflection/task1/harness/work/run_scratch_r1/t4_05.zag` — 3:i64
- `coding/reflection/task1/harness/work/run_scratch_r1/t4_11.zag` — 3:i64
- `coding/reflection/task1/harness/work/run_scratch_r1/t4m_05.zag` — 3:i64
- `coding/reflection/task1/harness/work/run_scratch_r2/t1_03.zag` — 9:i64
- `coding/reflection/task1/harness/work/run_scratch_r2/t1_04.zag` — 9:i64
- `coding/reflection/task1/harness/work/run_scratch_r2/t2_01.zag` — 19:i64
- `coding/reflection/task1/harness/work/run_scratch_r2/t2_02.zag` — 19:i64
- `coding/reflection/task1/harness/work/run_scratch_r2/t2_03.zag` — 8:i64
- `coding/reflection/task1/harness/work/run_scratch_r2/t2_07.zag` — 3:i64
- `coding/reflection/task1/harness/work/run_scratch_r2/t4_02.zag` — 3:i64
- `coding/reflection/task1/harness/work/run_scratch_r2/t4_05.zag` — 3:i64
- `coding/reflection/task1/harness/work/run_scratch_r2/t4_11.zag` — 3:i64
- `coding/reflection/task1/harness/work/run_scratch_r2/t4m_05.zag` — 3:i64
- `coding/reflection/task1/harness/work/run_scratch_r3/t1_03.zag` — 9:i64
- `coding/reflection/task1/harness/work/run_scratch_r3/t1_04.zag` — 9:i64
- `coding/reflection/task1/harness/work/run_scratch_r3/t2_01.zag` — 19:i64
- `coding/reflection/task1/harness/work/run_scratch_r3/t2_02.zag` — 19:i64
- `coding/reflection/task1/harness/work/run_scratch_r3/t2_03.zag` — 8:i64
- `coding/reflection/task1/harness/work/run_scratch_r3/t2_07.zag` — 3:i64
- `coding/reflection/task1/harness/work/run_scratch_r3/t4_02.zag` — 3:i64
- `coding/reflection/task1/harness/work/run_scratch_r3/t4_05.zag` — 3:i64
- `coding/reflection/task1/harness/work/run_scratch_r3/t4_11.zag` — 3:i64
- `coding/reflection/task1/harness/work/run_scratch_r3/t4m_05.zag` — 3:i64
- `coding/reflection/task1/harness/work/run_scratch_r4/t1_03.zag` — 9:i64
- `coding/reflection/task1/harness/work/run_scratch_r4/t1_04.zag` — 9:i64
- `coding/reflection/task1/harness/work/run_scratch_r4/t2_01.zag` — 19:i64
- `coding/reflection/task1/harness/work/run_scratch_r4/t2_02.zag` — 19:i64
- `coding/reflection/task1/harness/work/run_scratch_r4/t2_03.zag` — 8:i64
- `coding/reflection/task1/harness/work/run_scratch_r4/t2_07.zag` — 3:i64
- `coding/reflection/task1/harness/work/run_scratch_r4/t4_02.zag` — 3:i64
- `coding/reflection/task1/harness/work/run_scratch_r4/t4_05.zag` — 3:i64
- `coding/reflection/task1/harness/work/run_scratch_r4/t4_11.zag` — 3:i64
- `coding/reflection/task1/harness/work/run_scratch_r4/t4m_05.zag` — 3:i64
- `coding/reflection/task1/harness/work/run_scratch_r5/t1_03.zag` — 9:i64
- `coding/reflection/task1/harness/work/run_scratch_r5/t1_04.zag` — 9:i64
- `coding/reflection/task1/harness/work/run_scratch_r5/t2_01.zag` — 19:i64
- `coding/reflection/task1/harness/work/run_scratch_r5/t2_02.zag` — 19:i64
- `coding/reflection/task1/harness/work/run_scratch_r5/t2_03.zag` — 8:i64
- `coding/reflection/task1/harness/work/run_scratch_r5/t2_07.zag` — 3:i64
- `coding/reflection/task1/harness/work/run_scratch_r5/t4_02.zag` — 3:i64
- `coding/reflection/task1/harness/work/run_scratch_r5/t4_05.zag` — 3:i64
- `coding/reflection/task1/harness/work/run_scratch_r5/t4_11.zag` — 3:i64
- `coding/reflection/task1/harness/work/run_scratch_r5/t4m_05.zag` — 3:i64
- `coding/reflection/task1/src/task1_learner.zag` — 1039:i64, 1157:i64, 1204:i64, 1291:i64, 751:i64, 960:i64
- `coding/reflection/task2/learner.zag` — 208:i64, 313:i64, 431:i64, 451:i64
- `coding/reflection/task4/src/learner4.zag` — 208:i64, 313:i64, 431:i64, 451:i64
- `coding/speed-intel/quality-buying/work_code/learner_qb.zag` — 208:i64, 313:i64, 431:i64, 451:i64
- `coding/src/learner.zag` — 208:i64, 313:i64, 431:i64, 451:i64
- `knowledge/keyboard/audit281.zag` — 549:i64, 550:i64, 552:i64, 553:i64, 555:i64, 557:i64
- `knowledge/keyboard/run_battery.zag` — 125:i64, 126:i64, 128:i64, 129:i64, 131:i64
- `training_paradigms/source_trust/battery/build_k/fork.zag` — 56:i64
- `training_paradigms/source_trust/fork_k/k.zag` — 56:i64
- `units/arms/F-B/cl/arm.zag` — 78:i64
- `units/teachers/harness/harness.zag` — 1287:u64, 1374:u64, 1400:u64, 1422:u64, 1607:u64, 1713:u64, 2024:u64, 2025:u64, 2162:u64, 2169:u64, 2171:u64, 2172:u64, 2187:u64, 2188:u64, 2192:u64, 2200:u64, 2861:u64, 2870:u64, 2892:u64, 705:u64, 706:i64
- `units/teachers/learner/delib.zag` — 124:i64, 125:i64, 126:i64, 127:i64, 128:i64, 140:i64, 141:i64, 142:i64, 145:i64, 146:i64, 147:i64, 148:i64, 149:i64, 150:i64, 163:i64, 164:i64, 165:i64, 166:i64
- `units/teachers/learner/forcepin/forcepin.zag` — 83:i64, 84:i64, 85:i64, 86:i64
- `units/teachers/learner/forcepin/scratch/delib.zag` — 124:i64, 125:i64, 126:i64, 127:i64, 128:i64, 140:i64, 141:i64, 142:i64, 145:i64, 146:i64, 147:i64, 148:i64, 149:i64, 150:i64, 163:i64, 164:i64, 165:i64, 166:i64
- `units/teachers/learner/forcepin/scratch/forcepin.zag` — 83:i64, 84:i64, 85:i64, 86:i64
- `units/teachers/learner/forcepin/scratch/store.zag` — 145:i64, 146:i64, 181:i64, 32:i64, 33:i64, 34:i64, 35:i64, 36:i64, 37:i64, 38:i64, 39:i64, 40:i64, 41:i64, 42:i64, 43:i64, 44:i64, 45:i64, 46:i64
- `units/teachers/learner/forcepin/scratch/test_wired.zag` — 43:i64, 44:i64
- `units/teachers/learner/store.zag` — 145:i64, 146:i64, 185:i64, 32:i64, 33:i64, 34:i64, 35:i64, 36:i64, 37:i64, 38:i64, 39:i64, 40:i64, 41:i64, 42:i64, 43:i64, 44:i64, 45:i64, 46:i64
- `units/teachers/learner/tests/test_determinism.zag` — 16:i64, 17:i64
- `units/teachers/learner/tests/test_driver.zag` — 17:i64, 18:i64
- `units/teachers/learner/tests/test_pins.zag` — 187:i64, 188:i64, 68:i64, 69:i64
- `units/teachers/learner/tests/test_retract.zag` — 19:i64, 20:i64
- `wave12/championship/class3-standardized/src/forcepin.zag` — 83:i64, 84:i64, 85:i64, 86:i64
- `wave12/q2-distillation-sol/src/forcepin.zag` — 83:i64, 84:i64, 85:i64, 86:i64
- `wave12/q2-distillation-step37/src/forcepin.zag` — 83:i64, 84:i64, 85:i64, 86:i64
- `wave12/q2-distillation-swe/src/forcepin.zag` — 83:i64, 84:i64, 85:i64, 86:i64
