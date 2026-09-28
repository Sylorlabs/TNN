# sealed_04 LINES panic — repair diff log (2026-09-27)

## Root cause
`main()` allocated the LINES take buffer with a HARDCODED 16384-row capacity:

    let ltakes:[]i64 = nio_alloc((16384 * 7 * 8) as i32) as []i64;

`glines_build()` writes `ltakes[nlt*7 .. nlt*7+6]` with no capacity guard.
LINES takes are 2x2 input blocks; each take's top-left pixel q0 is marked in
`taken2`, and no two takes share a q0 — so the provable bound is nlt <= w*h
pixels. For sealed_04 (LR 384x288 = 110,592 pixels) the take rule wants
16,847 takes > 16,384 rows -> the read-back in `glines_commit()` /
`g_render_lines()` (`ltakes[ti*7+k]`, ti up to 16,846) indexes past the
114,688-element slice -> `panic: slice index out of bounds` (Zag runtime).

Why 384x288 triggers it: max possible LINES takes = w*h/4 (2x2 blocks) =
27,648 at this size, well above 16,384. Any input whose Sobel-strong-edge
2x2 take count exceeds 16,384 panics. sealed_04's residual is edge-dense
(16,847 baseline takes; C1's license gate takes a different SHAPES set ->
different residual -> fewer LINES takes -> C1 happens to survive).
The C1-vs-baseline diff confirms: the LINES code itself is byte-identical
between them; only SHAPES take decisions differ.

## Repair (IDENTICAL in all 6 sources)
Capacity-only: rows = w*h (the tight provable bound), zero mechanism change.

OLD (one line, in main()):
    let ltakes:[]i64 = nio_alloc((16384 * 7 * 8) as i32) as []i64;

NEW:
    // CAPACITY (2026-09-27 repair): rows = w*h, the tight provable bound.
    // Each take marks its distinct q0 pixel in taken2, so nlt <= w*h.
    // The old fixed 16384-row buffer panicked ("slice index out of bounds")
    // on any input with >16384 LINES takes (e.g. sealed_04: 16847 takes at
    // 384x288). Capacity-only: take rules, licenses, gain bars, rendering
    // math untouched.
    let ltakes:[]i64 = nio_alloc((w * h * 7 * 8) as i32) as []i64;

## Per-source application
| # | source | line of change | other changes |
|---|---|---|---|
| 1 | ~/workspace/upscale_gen/src/azgen.zag (pristine baseline) | 775 | none |
| 2 | ~/workspace/upscale_r4/r3src/azgen_c3.zag | 1127 | none |
| 3 | ~/workspace/upscale_r4/impl_p1/azgen_p1.zag | 1165 | none |
| 4 | ~/workspace/upscale_r4/impl_p2/azgen_p2.zag | 996 | none |
| 5 | ~/workspace/upscale_r4/impl_p3/azgen_p3.zag | 1309 | none |
| 6 | ~/workspace/upscale_r4/impl_p4/azgen_p4.zag | 999 | none |
NOT touched: ~/workspace/upscale_r4/r3src/azgen_c1.zag (frozen per task;
its LINES path is byte-identical to baseline and it never panics on sealed_04).

## Decision-neutrality argument (by construction)
On any input where the unrepaired binary completes, nlt <= 16,383: the
take loop writes exactly rows 0..nlt-1 and commit/render read exactly rows
0..nlt-1. Rows >= nlt are never read by anything (commit, render, trace).
Growing the buffer changes nothing observable. The byte-identical SHA guard
on all 11 dev images x 6 binaries is the empirical proof (see below).

New source SHAs (full-file sha256, prefix 16) after repair:
  upscale_gen/src/azgen.zag      aea60c27109708df  (was 060193d0ca8c948a)
  upscale_r4/r3src/azgen_c3.zag  6f74e3a1d8f7da0d  (was cd5bab26306ae468)
  upscale_r4/impl_p1/azgen_p1.zag f5eb4d2a6e6bff23 (was 636a0431bbd7993f)
  upscale_r4/impl_p2/azgen_p2.zag de4bf0172429add1 (was d1620a96e90f743d)
  upscale_r4/impl_p3/azgen_p3.zag b3ff8fa3fea1b181 (was b77fe3eed5f79d98)
  upscale_r4/impl_p4/azgen_p4.zag 53d4bb68dc5183d9 (was 8ed57695c1a5316b)
  upscale_r4/r3src/azgen_c1.zag  a23e717931bec8a7  (UNTOUCHED, frozen)

Repaired binary SHAs (build_scratch/):
  (recorded from build logs at battery time)

---

## Repaired binary SHAs (sha256, recorded before deletion)

- bin_base: 7fcf661d622922bd430db82808861133de41ef50f51d275e215c534e697a96c6
- bin_c1:   196c0315cfad901cb17f0b3e82548e959b6e986ea413622acbbace4bb141a5cf (rebuilt from UNTOUCHED c1 source)
- bin_c3:   c46e11ef6da90039828aa2d06d5055e7d632d3bb1d68af308925a5251a604542
- bin_p1:   8aa90a6ff3818c758df96dda2580c7e5b4bb497d8cfc4076aa26d3b1cb1fb6b0
- bin_p2:   74d236e58f75325d2bc3fe1883b750b9a412391d555a5040c203274bb0a891cf
- bin_p3:   54d7f1845d86bb6a71ae495ff24ca1c7a78549ca4bf6bd86e74086c39524a385
- bin_p4:   8cdd269cb859cfb4e53486cc6e36f05aa390bb470986359034fb7f936e5461c3

## Rerun record (2026-09-27)

- Neutrality guard: 77/77 dev output SHAs byte-identical vs unrepaired binaries (guard_results.json).
- Full matrix: 158/158 jobs, 2x fresh-outdir runs, all sha_match=true (results_repair.jsonl).
- Perturbations: sealed_04 x7 sealed configs x{env -i, different cwd} = 14/14 identical; bridge x8 configs x2 = 16/16 identical (perturb_results.json).
- BAR 1 (10 sealed images): P2plane PASS (all 4 clauses); C3/P1force/P3 FAIL floor (-0.99 sealed_07); P2 FAIL; P4 FAIL (floor -0.57, texture -0.29).
- P2 abandonment bar: mean -0.633 <= 0 FIRES (binding: vocabulary retired, pivot to measured-only construction).
- P1 reading: +0.839 vs C3 +0.759, diff +0.080 within +-0.10 -> deliberation decorative or harmful.
- RAW_TABLE.csv rewritten (158 rows); pre-repair preserved as RAW_TABLE_prerepair.csv. Dev rows byte-identical between them.
- Binaries deleted after scoring; sources, diff log, build logs, results retained.
