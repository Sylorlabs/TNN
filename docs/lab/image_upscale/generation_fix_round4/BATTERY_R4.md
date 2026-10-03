# Upscale Round 4 — Battery Report (BATTERY_R4)

Date: 2026-09-27. Frozen prereg: `~/workspace/upscale_r4/PREREG_R4.md`.
Raw data: `~/workspace/upscale_r4/RAW_TABLE.csv` (158 rows: 88 dev + 70 sealed).

**Final status: REPAIR COMPLETE — full 10-image sealed battery adjudicated.**
The sealed_04 LINES panic was a hardcoded 16384-row take-buffer capacity
defect. A capacity-only repair (buffer rows = w*h, zero mechanism change)
was applied identically to all 6 sources, proven decision-neutral (77/77
dev output SHAs byte-identical vs unrepaired binaries), and the full matrix
rerun completed: 158/158 jobs, every job 2× byte-identical, plus 30/30
perturbation runs. BAR 1 is now adjudicated on the preregistered 10-image
sealed battery. Raw data: `RAW_TABLE.csv` (158 rows: 88 dev + 70 sealed);
the pre-repair CSV is kept as `RAW_TABLE_prerepair.csv`.

---

## 1. Seal integrity

Before any sealed run, `sha256sum -c SEALED_SHASUMS.txt` over all 10 sealed images:
**all 10 passed**. Frozen VOC2 SHA `cbead2f7…`, VOC3 SHA `e43cfebf…`, baseline source
`060193d0…`, metrics.py `82905ce5…`, PIL exactly `10.2.0`. Support files from
`recon_build`, `impl_p1`, and `upscale_gen/src` verified SHA-identical.

## 2. Builds

All 7 configs built from frozen sources with the pinned toolchain, clean builds, each
with the same 31 analyzer warnings, zero errors. Build scratch:
`~/workspace/upscale_r4/battery_build/` (binaries deleted after scoring per protocol).

| config | binary | source SHA prefix |
|---|---|---|
| baseline | bin_base | `060193d0ca8c948a` |
| C1 | bin_c1 | `a23e717931bec8a7` |
| C3 | bin_c3 | `cd5bab26306ae468` |
| P1 | bin_p1 | `636a0431bbd7993f` |
| P2 | bin_p2 | `d1620a96e90f743d` |
| P3 | bin_p3 | `b77fe3eed5f79d98` |
| P4 | bin_p4 | `8ed57695c1a5316b` |

Wrappers (verified byte-identical outputs to direct invocation):
- `p1force.sh`: `bin_p1 "$1" "$2" force` — bridge SHA `fea34201b7821c0e…`, trace shows 49 `p1_forced_plane` regions.
- `p2plane.sh`: `bin_p2 "$1" "$2" plane` — bridge SHA `94e6090c5150f463…`, trace reports `planemode=1`.

## 3. BAR 0 — PASS

Gate ran before the full battery. Baseline reproduction, bridge/sky:

| image | committed SHA prefix | rerun SHA prefix | committed PSNR | rerun PSNR |
|---|---|---|---|---|
| bridge | `2028ba1dd5cf12e2` | `2028ba1dd5cf12e2` | 18.47 | 18.47 |
| sky | `842558193c0a56fc` | `842558193c0a56fc` | 22.75 | 22.75 |

All 9 diverse dev PSNRs reproduced exactly (fabric 21.47, woodgrain 18.37, treebark
18.94, calmwaters 19.46, portrait 21.19, car 22.92, building 14.96, cat 16.60,
market 18.36) — all within ±0.02 dB. **BAR 0 PASS.**

## 4. Matrix protocol

- Dev: 8 configs (baseline/C1/C3/P1force/P2/P2plane/P3/P4) × 11 images.
- Sealed: 7 configs (baseline/C3/P1force/P2/P2plane/P3/P4) × 10 images.
- Every config/image executed **twice in fresh outdirs**; output SHA of
  `upscale_gen.bmp` required byte-identical between runs or the job fails.
- Scored with frozen `generation/src/metrics.py` (mean of per-channel dB) vs gt.bmp.
- Published bicubic column: PIL 10.2.0 `Image.BICUBIC` on exact box-downscaled LR
  (see §8). The binaries' own `upscale_bicubic.bmp` is **not** the reference.
- Perturbations (pre-repair): `env -i` and different-cwd reruns on bridge +
  sealed_01 for all 8 binaries — 32/32 output SHAs identical to matrix runs.
- Perturbations (post-repair): `env -i` and different-cwd reruns on
  **sealed_04** (the new perturbation target) for all 7 sealed binaries —
  14/14 identical; bridge for all 8 binaries — 16/16 identical. **30/30.**

Result (post-repair rerun): **158/158 scored jobs sha_match=true** (zero
determinism failures). Pre-repair result was 151/151 + 7 panic records
(see §5).

## 5. sealed_04 — frozen pipeline panic (BLOCKER)

`sealed_04` (768×576 GT / 384×288 LR) crashes the frozen pipeline in the LINES
phase with `panic: slice index out of bounds` (Zag runtime), producing no
`upscale_gen.bmp`:

| config | runs observed | phase | LINES takes before panic |
|---|---|---|---|
| baseline | 2 | LINES | 16,847 |
| C3 | 2 | LINES | 17,890 |
| P1force | 2 | LINES | — (panics) |
| P2 | 2 | LINES | — (panics) |
| P2plane | 2 | LINES | — (panics) |
| P3 | 2 | LINES | 17,890 |
| P4 | 2 | LINES | 19,722 |

Both runs per config panicked identically (same stderr, no output file). This is an
inherited capacity defect in the frozen sources — no binary or source was modified.
Baseline itself panics, so no Δ can be computed for sealed_04 for any arm. (C1, not a
sealed candidate, happened to complete sealed_04 at 17.07 dB in ad-hoc probing —
diagnostic only, not part of the battery.)

**RESOLVED — see §5b.** The panic was repaired (capacity-only, decision-neutral)
and the full 10-image sealed battery was rerun; §7 below is the adjudicated table.

**Consequence (SUPERSEDED by the §5b repair):** this paragraph described the
pre-repair state, when the preregistered 10-image sealed bars could not be
adjudicated. After the repair, BAR 1 and the P2 abandonment bar ARE adjudicated
on the full 10-image sealed battery — see §5b and §7. The 9-image diagnostic
readings below are kept as the historical pre-repair record.

## 5b. sealed_04 LINES panic — root cause, repair, neutrality proof

**Root cause (capacity defect, inherited in all frozen sources).** `main()`
allocated the LINES take buffer with a HARDCODED 16384-row capacity:

    let ltakes:[]i64 = nio_alloc((16384 * 7 * 8) as i32) as []i64;

`glines_build()` writes `ltakes[nlt*7 .. nlt*7+6]` with no bound check.
Each LINES take consumes one 2x2 input block whose top-left pixel q0 is
marked in `taken2` — no two takes share a q0 — so the provable take bound
is nlt ≤ w*h input pixels. sealed_04's LR is 384×288 = 110,592 pixels; its
residual is edge-dense and the take rule wants **16,847 takes > 16,384
rows**. The read-back in `glines_commit()` (`ltakes[ti*7+k]`, ti up to
16,846) then indexes past the 114,688-element slice →
`panic: slice index out of bounds` (Zag runtime). Reproduced on the
pristine baseline: stdout prints
`LINES G=92101381 N=202164 takes=16847`, then the panic fires in the
commit/read-back phase. Any input whose Sobel-strong-edge 2x2 take count
exceeds 16,384 panics (theoretical max at 384×288 is w*h/4 = 27,648).
C1 survived only because its license gate takes a different SHAPES set →
a different residual → fewer LINES takes; its LINES code is byte-identical
to baseline (verified by source diff — the only C1-vs-baseline differences
are the SHAPES license gate).

**Repair (IDENTICAL one-line change in all 6 sources;
`r3src/azgen_c1.zag` untouched and frozen):**

    -    let ltakes:[]i64 = nio_alloc((16384 * 7 * 8) as i32) as []i64;
    +    let ltakes:[]i64 = nio_alloc((w * h * 7 * 8) as i32) as []i64;

plus a `// CAPACITY (2026-09-27 repair)` comment block. Capacity-only:
match rules, licenses, gain bars, take decisions, rendering math untouched.
At 384×288 the buffer is 6,193,152 bytes, under the znc 2^25 slice ceiling.
Full diff log: `repair_work/DIFF_LOG.md`.

Repaired source SHAs (prefix 16): baseline `aea60c27109708df` (was
`060193d0ca8c948a`); C3 `6f74e3a1d8f7da0d` (was `cd5bab26306ae468`); P1
`f5eb4d2a6e6bff23` (was `636a0431bbd7993f`); P2 `de4bf0172429add1` (was
`d1620a96e90f743d`); P3 `b3ff8fa3fea1b181` (was `b77fe3eed5f79d98`); P4
`53d4bb68dc5183d9` (was `8ed57695c1a5316b`).

**Decision-neutrality proof (mandatory guard, run BEFORE any sealed rerun).**
All 6 repaired binaries (plus a fresh build of the untouched C1 source)
ran all 11 dev images; every `upscale_gen.bmp` SHA is byte-identical to
the unrepaired binaries' committed SHAs:

| config | dev SHAs identical | bridge SHA | sky SHA |
|---|---|---|---|
| baseline | 11/11 | `2028ba1d…` ✓ | `84255819…` ✓ |
| c3 | 11/11 | ✓ | ✓ |
| p1force | 11/11 | ✓ | ✓ |
| p2 | 11/11 | ✓ | ✓ |
| p2plane | 11/11 | ✓ | ✓ |
| p3 | 11/11 | ✓ | ✓ |
| p4 | 11/11 | ✓ | ✓ |

**77/77 byte-identical.** The repair is provably decision-neutral: on any
input the old pipeline could complete, nlt ≤ 16,383, the take loop writes
exactly rows 0..nlt−1 and commit/render/trace read exactly rows 0..nlt−1 —
rows ≥ nlt are never read by anything. Guard detail:
`repair_work/guard_results.json` (PSNRs also identical).

**Full rerun with repaired binaries:** 158/158 jobs (dev 8×11 + sealed
7×10), every job executed **twice in fresh outdirs**, all
`sha_match=true`. Perturbations: sealed_04 (the new perturbation target)
× 7 sealed configs × {`env -i`, different cwd} = 14/14 SHAs identical;
bridge × 8 configs × 2 = 16/16 identical. **30/30 total.**
Results: `repair_work/results_repair.jsonl`; perturbations:
`repair_work/perturb_results.json`.

---

## 6. Dev battery (11 images, complete)

**Post-repair note:** the full rerun with repaired binaries reproduces this
entire table byte-identically — every dev `upscale_gen.bmp` SHA and every
PSNR below matches the pre-repair battery exactly (see §5b neutrality
table; also verified at the CSV level: all 88 dev rows of
`RAW_TABLE_prerepair.csv` ≡ `RAW_TABLE.csv`). The dev numbers are unchanged.

PSNR dB, frozen metrics.py. `bic` = frozen PIL 10.2.0 reference column.

| image | baseline | C1 | C3 | P1force | P2 | P2plane | P3 | P4 | bic (PIL) |
|---|---|---|---|---|---|---|---|---|---|
| bridge | 18.47 | 20.00 | 19.74 | 19.86 | 18.40 | 19.20 | 19.74 | 20.00 | 27.76 |
| sky | 22.75 | 26.27 | 23.89 | 23.89 | 22.75 | 23.72 | 23.89 | 26.27 | 34.77 |
| fabric | 21.47 | 21.47 | 21.47 | 21.47 | 21.47 | 21.47 | 21.47 | 21.47 | 27.59 |
| woodgrain | 18.37 | 18.86 | 20.05 | 20.07 | 18.16 | 19.41 | 19.92 | 18.86 | 27.53 |
| treebark | 18.94 | 21.26 | 20.51 | 20.65 | 18.81 | 20.19 | 20.51 | 21.26 | 29.60 |
| calmwaters | 19.46 | 20.06 | 20.08 | 20.16 | 19.47 | 20.06 | 20.08 | 20.06 | 22.91 |
| portrait | 21.19 | 22.63 | 22.32 | 22.36 | 21.22 | 22.02 | 22.32 | 22.63 | 28.37 |
| car | 22.92 | 24.12 | 24.43 | 24.53 | 22.78 | 23.87 | 24.43 | 24.12 | 35.72 |
| building | 14.96 | 14.60 | 15.24 | 15.22 | 14.96 | 15.22 | 15.24 | 14.60 | 16.79 |
| cat | 16.60 | 17.08 | 17.19 | 17.27 | 16.59 | 17.10 | 17.19 | 17.08 | 21.12 |
| market | 18.36 | 19.38 | 19.07 | 19.08 | 18.34 | 18.86 | 19.07 | 19.38 | 24.03 |

Mean Δ vs baseline (11 images), wins = Δ ≥ −0.005 (ties count, per R3 convention):

| config | mean Δ | wins/11 | losses | worst |
|---|---|---|---|---|
| C1 | +1.113 | 10 | 1 | −0.36 (building) |
| C3 | +0.955 | 11 | 0 | +0.00 (fabric tie) |
| P1force | +1.006 | 11 | 0 | +0.00 (fabric tie) |
| P2 | −0.049 | 5 | 6 | −0.21 |
| P2plane | +0.694 | 11 | 0 | +0.00 (fabric tie) |
| P3 | +0.943 | 11 | 0 | +0.00 (fabric tie) |
| P4 | +1.113 | 10 | 1 | −0.36 (building) |

Dev reproduces the R3 reference numbers exactly (C1 +1.11, C3 +0.955).

**Preregistered P1 reading:** P1 mean Δ (+1.006) is within ±0.10 dB of C3's +0.955
(diff +0.051) → per prereg, the deliberation is decorative or harmful. (Sealed,
10 images: P1 +0.839 vs C3 +0.759, diff +0.080 — also within ±0.10.)

**P4 vs C1:** P4 outputs are **byte-identical to C1 on 10/11 dev images**
(SHA-identical). The only difference is `building`, where the gate licenses 0 takes
and P4's plane-fallback for unlicensed takes changes the bytes — PSNR unchanged at
14.60. The C1 repair changed nothing measurable on dev.

**Bicubic note:** every arm and baseline sits 0.5–3.3 dB below the frozen PIL bicubic
reference on every dev image (e.g. bridge: best arm 20.00 vs PIL 27.76). The
binaries' own `upscale_bicubic.bmp` scores 0.5–3.3 dB *worse* than PIL's bicubic —
the Zag bicubic implementation is inferior to the reference; the published column is
PIL.

## 7. Sealed battery (10 images, COMPLETE — adjudicated)

PSNR dB, full rerun with repaired binaries (§5b). `bic` = frozen PIL 10.2.0.

| image | baseline | C3 | P1force | P2 | P2plane | P3 | P4 | bic (PIL) |
|---|---|---|---|---|---|---|---|---|
| sealed_01 | 24.56 | 24.56 | 24.56 | 24.56 | 24.56 | 24.56 | 24.56 | 33.01 |
| sealed_02 | 21.77 | 22.72 | 22.72 | 21.76 | 22.24 | 22.72 | 21.20 | 38.95 |
| sealed_03 | 20.79 | 22.82 | 22.82 | 20.78 | 22.52 | 22.82 | 23.27 | 35.26 |
| sealed_04 | 17.45 | 17.94 | 17.99 | 17.44 | 17.88 | 17.94 | 17.07 | 23.07 |
| sealed_05 | 21.53 | 22.16 | 22.47 | 20.92 | 21.64 | 22.09 | 21.58 | 28.10 |
| sealed_06 | 19.49 | 21.56 | 21.64 | 19.38 | 20.89 | 21.56 | 20.38 | 28.82 |
| sealed_07 | 23.42 | 22.43 | 22.43 | 23.42 | 23.42 | 22.43 | 23.42 | 30.40 |
| sealed_08 | 21.04 | 21.85 | 21.91 | 20.96 | 21.47 | 21.85 | 22.53 | 31.15 |
| sealed_09 | 19.65 | 20.31 | 20.33 | 19.65 | 19.94 | 20.31 | 19.85 | 26.47 |
| sealed_10 | 19.87 | 20.81 | 21.09 | 19.76 | 20.40 | 20.81 | 21.35 | 29.05 |

Notable raw facts: on sealed_01 **all 7 configs are byte-identical to baseline**
(gates refused everything); on sealed_07, C3/P1force/P3 score *below* baseline
(−0.99) while P2/P2plane/P4 tie baseline exactly. On sealed_04 (the repaired
image), every config completes; P4 scores 17.07 — numerically identical at 2dp
to C1's ad-hoc 17.07 (C1 is not a sealed candidate; diagnostic only).

Per-image Δ vs baseline (10 images):

| config | s01 | s02 | s03 | s04 | s05 | s06 | s07 | s08 | s09 | s10 |
|---|---|---|---|---|---|---|---|---|---|---|
| C3 | +0.00 | +0.95 | +2.03 | +0.49 | +0.63 | +2.07 | −0.99 | +0.81 | +0.66 | +0.94 |
| P1force | +0.00 | +0.95 | +2.03 | +0.54 | +0.94 | +2.15 | −0.99 | +0.87 | +0.68 | +1.22 |
| P2 | +0.00 | −0.01 | −0.01 | −0.01 | −0.61 | −0.11 | +0.00 | −0.08 | +0.00 | −0.11 |
| P2plane | +0.00 | +0.47 | +1.73 | +0.43 | +0.11 | +1.40 | +0.00 | +0.43 | +0.29 | +0.53 |
| P3 | +0.00 | +0.95 | +2.03 | +0.49 | +0.56 | +2.07 | −0.99 | +0.81 | +0.66 | +0.94 |
| P4 | +0.00 | −0.57 | +2.48 | −0.38 | +0.05 | +0.89 | +0.00 | +1.49 | +0.20 | +1.48 |

Aggregate readings (wins = Δ ≥ −0.005, ties count):

| config | mean Δ | wins/10 | losses | worst |
|---|---|---|---|---|
| C3 | +0.759 | 9 | 1 | −0.99 (sealed_07) |
| P1force | +0.839 | 9 | 1 | −0.99 (sealed_07) |
| P2 | −0.094 | 3 | 6 | −0.61 (sealed_05) |
| P2plane | +0.539 | 10 | 0 | +0.00 |
| P3 | +0.752 | 9 | 1 | −0.99 (sealed_07) |
| P4 | +0.564 | 8 | 2 | −0.57 (sealed_02) |

Category-group mean Δ (10 images):

| config | animal | mixed | object | people | smooth | texture |
|---|---|---|---|---|---|---|
| C3 | +0.74 | +0.94 | +0.54 | +0.63 | +1.26 | +0.47 |
| P1force | +0.78 | +1.22 | +0.58 | +0.94 | +1.29 | +0.47 |
| P2 | −0.04 | −0.11 | −0.05 | −0.61 | −0.01 | −0.00 |
| P2plane | +0.36 | +0.53 | +0.70 | +0.11 | +1.08 | +0.23 |
| P3 | +0.74 | +0.94 | +0.54 | +0.56 | +1.26 | +0.47 |
| P4 | +0.85 | +1.48 | +0.45 | +0.05 | +1.05 | **−0.29** |

**BAR 1 adjudication (preregistered, 10 sealed images):** mean Δ ≥ +0.50 AND
wins ≥ 8/10 AND no single image < −0.50 AND every category-group mean Δ ≥ 0.

| config | mean ≥+0.50 | wins ≥8/10 | none <−0.50 | groups ≥0 | **BAR 1** |
|---|---|---|---|---|---|
| C3 | +0.759 ✓ | 9 ✓ | −0.99 ✗ | ✓ | **FAIL** |
| P1force | +0.839 ✓ | 9 ✓ | −0.99 ✗ | ✓ | **FAIL** (diagnostic arm; cannot win per prereg) |
| P2 | −0.094 ✗ | 3 ✗ | −0.61 ✗ | ✗ | **FAIL** |
| P2plane | +0.539 ✓ | 10 ✓ | +0.00 ✓ | ✓ | **PASS** |
| P3 | +0.752 ✓ | 9 ✓ | −0.99 ✗ | ✓ | **FAIL** |
| P4 | +0.564 ✓ | 8 ✓ | −0.57 ✗ | texture −0.29 ✗ | **FAIL** |

P2plane — P2's measured-only analysis mode (P2 take geometry, atom-takes
rendered as PLANE-FIT) — satisfies all four BAR 1 clauses on the
preregistered 10-image sealed battery. Per the prereg, a BAR 1 winner must
still clear the independent red-team gate (category-shift traps, close-call
±1–2 LSB perturbation amplification, operator neutering, hardcode audit,
sealed-image leakage audit) and the eyes gate before any victory is
declared; those are coordinator scope and are NOT adjudicated here.

**Preregistered P2 abandonment bar** — mean Δ(P2 − P2plane) over the 10
sealed images, fires iff ≤ 0. Per-image (P2−P2plane): +0.00, −0.48, −1.74,
−0.44, −0.72, −1.51, +0.00, −0.51, −0.29, −0.64 → **mean −0.633 ≤ 0 →
FIRES**. Every image is ≤ 0; no image favors atoms-over-planes, and
sealed_04 (−0.44) does not move the sign. Per prereg this bar is **binding
on the program, not advisory**: the learned vocabulary is retired and the
line pivots to measured-only construction.

## 8. BAR 2 — PASS (all arms)

No arm may score below baseline − 0.10 on bridge/sky:

| config | bridge Δ | sky Δ | verdict |
|---|---|---|---|
| C1 | +1.53 | +3.52 | PASS |
| C3 | +1.27 | +1.14 | PASS |
| P1force | +1.39 | +1.14 | PASS |
| P2 | −0.07 | +0.00 | PASS |
| P2plane | +0.73 | +0.97 | PASS |
| P3 | +1.27 | +1.14 | PASS |
| P4 | +1.53 | +3.52 | PASS |

## 9. Method notes

- **Frozen PIL bicubic column:** PIL 10.2.0. JPEG decode → RGB; drop last GT row if
  odd height; exact harness LR = channel-wise `(a+b+c+d+2)//4` box downscale;
  `Image.fromarray(LR).resize((2w,2h), Image.BICUBIC)`; PSNR = frozen metrics.py mean
  of per-channel dB. Reference script: `battery_build/bicubic_ref.py`.
- **Implementer sanity-PSNR discrepancy (documented, not a defect):** the P1–P4
  implementers' reports quote dB-of-mean-SSE (e.g. P3 bridge 19.63), while the frozen
  metrics.py uses mean-of-per-channel-dB (19.74). Pixel outputs are byte-identical
  (P3 bridge SSE = 200345689 exactly as the implementer reported; SHA
  `937b7fdbd0cda9c8…` matches). All battery numbers use the frozen formula.
- **Determinism (post-repair rerun):** 158/158 scored config/image jobs produced
  byte-identical `upscale_gen.bmp` SHAs across two fresh-outdir runs.
  Perturbation reruns (`env -i`, different cwd): sealed_04 × 7 sealed binaries
  14/14, bridge × 8 binaries 16/16 — 30/30 SHAs identical to matrix runs.
  (Pre-repair: 151/151 + 7 panic records; bridge + sealed_01 32/32.)
- **No sealed image was visually inspected** at any point. Sealed_04's pixels
  were read numerically (shape/content statistics) for panic diagnosis only.
  No frozen source, harness, or metric was modified — except the §5b
  capacity repair, applied identically to the 6 named sources.
- Binaries and `.zag-cache`/`.zagd.semantic-ready` artifacts deleted after scoring;
  build logs, `results_repair.jsonl`, `perturb_results.json`,
  `guard_results.json`, and `repair_work/DIFF_LOG.md` retained in
  `repair_work/` (pre-repair `results.jsonl` retained in `battery_build/`).

## 10. Bar/reading summary

| item | status |
|---|---|
| BAR 0 (baseline reproduction) | **PASS** (repaired baseline: bridge `2028ba1d…`/18.47, sky `84255819…`/22.75) |
| BAR 1 (sealed, 10-image prereg) | **ADJUDICATED** — P2plane **PASS** (all 4 clauses); C3/P1force/P3 FAIL floor (−0.99 sealed_07); P2 FAIL; P4 FAIL (floor −0.57, texture −0.29). Red-team + eyes gates still outstanding (coordinator scope). |
| BAR 2 (bridge/sky ≥ baseline−0.10) | **PASS** — all 7 arms |
| P1 deliberation reading (±0.10 dB) | P1 within ±0.10 of C3 on dev (+0.051) and sealed (+0.080) → decorative or harmful |
| P2 vocab abandonment bar | **FIRES** (10-image mean −0.633 ≤ 0 — binding: vocabulary retired, pivot to measured-only) |
| 2× determinism | 158/158 sha_match |
| Perturbations (env −i, cwd) | 30/30 identical (sealed_04 14/14, bridge 16/16) |
| Repair decision-neutrality | **77/77** dev output SHAs byte-identical vs unrepaired binaries (§5b) |

---

**REPAIR COMPLETE — full 10-image sealed battery adjudicated (see §5b, §7)**
