# Interventions — build log, runs, scoring

Job 1, one-brain follow-up, 2026-09-27 (PDT). Frozen inputs never edited; all runs read-only against the frozen `v7.tsv`.

## Control: pristine rebuild

- Source: `docs/lab/onebrain4/impl/onebrain_v4.zag`, SHA-256 `bbb1752ec5ee0c8bc3871bb41c4cfe65bc0d8e27f9357883d1712dbb4b006874` (matches frozen).
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`, SHA-256 `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`.
- Rebuild (cwd = build dir, `@import` resolves rel. to cwd per the R4 build log) produced binary SHA-256 `630586da251f37bd72d60fd426fd7039142b81653a08a3527c892c21a42720fe` — **byte-identical to the pinned R4 binary**. Control holds.

## Variants

Both variants change only `reint_better` (the reintegration comparator) and `reint_why` (its trace explainer, mirrored so `lose` lines stay honest), plus one `REINT_VARIANT` trace marker printed in `reint_delib`. Verified by diff against the frozen source: no other function touched.

| Variant | Change | Source SHA-256 | Binary SHA-256 |
|---|---|---|---|
| V1 `onebrain_v1_nosupport.zag` | inter + qual forced equal in `reint_better` (support-strength step disabled); `reint_why` skips both | `318c640025318e20c6d2b200a69b79b8dc94a57bff2e828156b8010c37c4d08c` | `ebf94b07ba05ecb964a56917de573cfb42cf8e6ebafb8a43d0915d1bc9650e97` |
| V2 `onebrain_v2_corrprotect.zag` | inter + qual skipped when either bid has gr@32==0 (correction-gated); `reint_why` mirrors the skip | `3a2b7bf92d11d8781b0d4332ee5b00207d61d79efcaa6da3f3ad5a7f7662a934` | `c9a7b8d85e6ebeb5180ba41fd61e10cc93259138070547b02d39ed05af993036` |

Build warnings: the same 2 pre-existing analyzer warnings as the pristine build (E0102 multiply-by-0, line 394 in `led_init`, verbatim from v3). No new warnings.

## Runs

Input: frozen `v7.tsv`, SHA-256 `3f3b3d6c34364460fdd54303729033e02c2da2f5c9960ea1586a72efd95bda3a` (matches FREEZE4). Mode `nov4` (reintegration on, V4 off). Each variant run twice.

| Run | Output SHA-256 | r2 == r1 | rc | stderr |
|---|---|---|---|---|
| V1 r1 | `7948df1d7aa289dac497309a5e944b51fd93f0207f2d43e83475963d48809707` | ✅ | 0 | empty |
| V1 r2 | `7948df1d7aa289dac497309a5e944b51fd93f0207f2d43e83475963d48809707` | ✅ | 0 | empty |
| V2 r1 | `7fcf3c760d4aeb7639b42ea14492c5e1b5dd01f029c5b80baa9db222c569d32` | ✅ | 0 | empty |
| V2 r2 | `7fcf3c760d4aeb7639b42ea14492c5e1b5dd01f029c5b80baa9db222c569d32` | ✅ | 0 | empty |

Determinism holds (byte-identical reruns). Zero RNG markers in either variant source (only "zero RNG" comments); rerun identity is the decision-path proof.

## Scoring (/44 vs frozen `expected_bid`)

| Mode | Score | Δ vs nov4 (35) |
|---|---|---|
| nov4 (baseline) | 35 | — |
| nov4nG (honest null) | 24 | −11 |
| **V1** (support-strength off) | **24** | −11 — matches nov4nG on all 44 items |
| **V2** (correction-protected) | **38** | +3 — the 3 harms repaired, fixes intact |

V1 item-level result: all 14 fixes reverted to the honest-null answer; all 3 harms reverted to the honest-null answer (16, correct); the other 27 items identical to both baselines.

V2 item-level result: exactly 3 items changed vs nov4 — q06, q07, q08 (19 → 16, all now correct). All 14 fixes unchanged. The other 27 items unchanged.

## Files in this directory

- `MECHANISM_REPORT.md` — the mechanism report (main deliverable).
- `INTERVENTIONS.md` — this file.
- `impl/onebrain_v1_nosupport.zag`, `impl/onebrain_v2_corrprotect.zag` — variant sources.
- `runs/v1_r1.out`, `runs/v1_r2.out`, `runs/v2_r1.out`, `runs/v2_r2.out` (+ empty `.err`) — full traces.
- Build binaries (`ob_v1`, `ob_v2`) are NOT committed (repo standard: no binaries).
