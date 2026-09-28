# PREREG_FS-F2C.md — "Colorconst Formation Improvement" (FROZEN)

**Crew:** FS-F2C (formation-improvement crew). **Date:** 2026-09-24.
**Status:** FROZEN — committed alone before any eval result exists.
**Parent scope:** FS-E2 abstained colorconst (formation 56.81%, Phase-0 `28aa3938`).
**Standing order served:** Micah: "PAMs v2 must accept truths" — abstained tasks
earn install authority via formation improvement.

## 1. Problem (Phase-0 diagnosis, committed `evidence/diag/`)

FS-E2's independent formation measurement (720/720 judgment agreement with the
frozen FS-E1 ledger, reproduced in `src/diag_phase0.py`) decomposes colorconst
formation errors (311/720 wrong, 56.81% accuracy) as:

| Mode | Count | Share of errors | Mechanism |
|---|---|---|---|
| E1 illuminant-shift false-DIFFERENT | 245 | 78.8% | truth SAME_SURFACE, judged DIFFERENT; **245/245** show a clear illuminant-shift signature (per-view mean channel-ratio spread > 1.25, median 1.86); dominant mean-chromaticity delta signs are warm/cool-ward |
| E2 missed real difference | 66 | 21.2% | truth DIFFERENT, judged SAME_SURFACE (frozen d in [10,79]); 19 borderline (within 20 of threshold 80), only 9/66 illuminant-masked |

E1 margins: 97 errors are >150 units past the threshold — no threshold move on
the frozen statistic can recover them. The frozen rule (warm mean-chromaticity
L1 x1000, DIFFERENT iff >= 80) has **no illuminant discounting**: any
d65↔warm / d65↔cool / warm↔cool shift between the two views of the SAME surface
pushes the statistic over threshold. The d65 illuminant handling IS implicated
in formation errors — but at the formation layer (missing von Kries
normalization), which is disjoint from FS-E1b's CH-CCN-3 challenge-quantity
repair (count≥4 threshold defect). This crew does not touch challenges.

## 2. Improved formation rule (exact specification — FROZEN)

**Name:** linear-space ratio-dispersion formation (`f_colorconst_ratio`).

Rationale (white-box, from §1): the R2-7 generator applies the illuminant as
an EXACT Bradford diagonal **in linear RGB** (then clips at 1.0 and
gamma-encodes to sRGB). For a SAME_SURFACE pair (same crop, two illuminants),
the per-pixel per-channel linear ratio viewB/viewA is therefore CONSTANT
across all pixels — equal to the illuminant gain ratio — regardless of what
the illuminants are. For a DIFFERENT pair (two crops), the ratio field varies
with the two surfaces. The rule tests exactly this: **"are the two views
related by a global per-channel gain?"** No illuminant estimation (no
gray-world assumption) is needed, so the E1 failure mode (illuminant shift
between views) cancels by construction. An earlier von Kries / gray-world
design reached only 83.19% on the calibration set (degenerate-channel noise
amplification); the ratio-dispersion design reaches 98.75%.

**Inputs:** F span bytes of one R2FX colorconst fixture: viewA = bytes
[0,6912), viewB = bytes [6912,13824), each 48x48 RGB row-major.

**Algorithm (integer math only, deterministic; all i64):**
1. Linearize each byte through LUT[c] = round(10000 * lin(c/255)), with
   lin(x) = x/12.92 for x <= 0.04045 else ((x+0.055)/1.055)^2.4
   (256-entry table embedded in the binary; generated once from this
   definition — see `src/gen_lut.py`; this is the exact inverse of the
   generator's gamma).
2. Per channel c in {R,G,B}: S1 = S2 = n = 0. For each pixel i in 0..2303:
   ra = viewA[3i+c], rb = viewB[3i+c] (raw bytes).
   - Skip the pixel if ra >= 250 or rb >= 250 (clipped pixels carry no
     surface information).
   - la = LUT[ra], lb = LUT[rb]. Skip the pixel if la < 100 or lb < 100
     (dark/noise gate; L_MIN = 100 linear x10000 units).
   - r_i = lb*1000 // la (integer division; la >= 100 > 0; 0 <= r_i <= 100000).
   - S1 += r_i; S2 += r_i*r_i; n += 1.
3. Per channel: if n < 64, contribution = 0. Else:
   num = S2*n - S1*S1 (if num < 0, num = 0); den = S1*S1 (if den < 1, den = 1);
   contribution = num*300 // den.
   (num is n^2 times the variance of the ratio field; contribution is the
   squared coefficient of variation x300.)
4. Statistic: **d = contribution_R + contribution_G + contribution_B**.
5. Judgment: **DIFFERENT iff d >= T, else SAME_SURFACE**, with **T = 44**.

**Overflow proof (i64):** lb <= 10000 so lb*1000 <= 1e7; la >= 100 so
r_i <= 100000 and r_i^2 <= 1e10; S1 <= 2304*1e5 = 2.304e8, S1^2 <= 5.31e16;
S2 <= 2304*1e10 = 2.304e13, S2*n <= 5.31e16;
num = (1/2)*sum_{i,j}(r_i-r_j)^2 <= 2.654e16;
num*300 <= 7.96e18 < 2^63-1 = 9.223e18. No overflow possible.

The other five formation functions (colordisc, shapetrans, pitchdisc,
timbredisc, motiondir) are carried over UNCHANGED from FS-E2's independent
implementation. Formation reads F only; G (d65 re-render) is challenge
evidence and is never shown to the formation path.

**Non-goals:** challenge quantities (FS-E1b owns CH-CCN-3); adversarial
families CCN-1/CCN-2 (challenge-layer scope); shapetrans/timbredisc formation.

## 3. Bars (FROZEN — all must pass)

| # | Bar | Criterion |
|---|---|---|
| (a) | colorconst formation accuracy | **>= 85%** on a FRESH deterministic draw of colorconst family-0 controls, **n = 1200**, judged by the frozen binary |
| (b) | NO-REGRESSION | formation accuracy on colordisc / pitchdisc / motiondir (same frozen binary, same fixture sets as FS-E2 Phase-0) must be **>= 92.96 / 97.92 / 96.63 minus 1pp** (i.e. >= 91.96 / 96.92 / 95.63) |
| (c) | determinism | both eval runs **byte-identical** (TSV SHAs equal across r1/r2) |

Reference (non-gating, diagnostic): the frozen rule re-scored on the same
fresh 1200 draw, to show the improvement delta.

## 4. Fresh-draw procedure (FROZEN)

- Generator: `src/gen_fresh.py`, importing the FROZEN R2-7 generator
  (`gen_colorconst`, `Rng`, `stream_seed`, `write_r2fx`, `write_truth`) —
  the same code that built the frozen suite; no generator changes.
- **MASTER_F2C = 20260924** (disjoint from the frozen suite's 20260923);
  stream = 401 (STREAM_NORMAL+1, colorconst normal stream id); family = 0;
  indices 0..1199. Per-fixture seed construction identical to R2-7
  (splitmix64 chain), so the draw is deterministic and reproducible.
- Output: `forks/FS-F2C/fixtures_fresh/f2c_colorconst_<i>.r2fx` +
  `.truth` sidecars + `MANIFEST.sha256` + `gen_ledger.jsonl`
  (id, family, truth, sha256 per fixture).
- The draw script is committed WITH this prereg; fixtures are generated
  AFTER this prereg is committed, and the prereg names the seed so the draw
  cannot be re-rolled on failure.

## 5. Eval procedure (FROZEN)

1. Build `src/f2c_form.zag` with the pinned toolchain
   `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
   (pure Zag, integer math only, zero RNG in any decision path). Record
   source and binary SHA-256.
2. Run twice (`run_eval.py` glue only): batch mode over the 1200 fresh
   colorconst fixtures + the FS-E2 Phase-0 fixture lists for
   colordisc/pitchdisc/motiondir normals; compare judgments vs `.truth`.
3. Score: accuracy per task per run; verify r1/r2 byte-identical; verify bar
   (b) against FS-E2 Phase-0 levels; verify bar (a) >= 85%.
4. Write VERDICT_FS-F2C.md (FINAL: ALIVE/DEAD per bars — ALIVE means
   colorconst EARNS FS-E2 scope), commit evidence + verdict. Never commit
   binaries or .zagd.

## 6. Calibration record (diagnosis-phase, frozen here)

- Design path (all on the 720 r2n colorconst controls, FS-E2 Phase-0 set):
  frozen rule 56.81% -> sRGB von Kries variants 70.7-79.6% -> linear-space
  von Kries 77.1-83.2% -> **ratio-dispersion 98.75%** (lmin=100).
  The ratio-dispersion design won on white-box principle (it tests the
  generative SAME_SURFACE condition directly: constant per-channel gain
  field in linear space) AND on margin, so it is the frozen rule.
- Threshold T = 44 (K=300 scale): the max-accuracy T on the 720 calibration
  set is uniquely T = 44 (98.75%; T = 43 or 45 both admit a 10th error —
  see `evidence/diag/final.txt`). The integer band is a single value because
  K=300 quantizes d coarsely, but the UNDERLYING separation is wide: at
  T = 44, correct SAME_SURFACE fixtures have d <= 10 at p90 (median 2) and
  correct DIFFERENT fixtures have d >= 227 at p10 (median 1086) — a ~20x
  relative margin. Only the 9 individually-understood hard fixtures
  (dark/low-data or heavily clipped crops) live near the boundary.
- Calibration-set result (diagnostic, NOT the bar): 711/720 = 98.75%
  (E1 rescued 243/245 = 99.2%; E2 rescued 65/66 = 98.5%).
  Residual 9 errors: 7 DIFFERENT misses (5 on dark/low-kept-pixel crops where
  the ratio test has little data, incl. 2 with d=0; 2 on near-proportional
  crops) + 2 SAME_SURFACE false-DIFFERENT (fixtures 37/534: 93.5%/heavy
  clipping — clip exclusion removes the informative pixels).
- The (a)-bar is measured on the disjoint fresh 1200-draw, so the
  calibration cannot overfit the bar.

## 7. Failure handling

If any bar fails: verdict DEAD, colorconst stays ABSTAIN-scoped, and the
diagnosis of the failure is committed. No re-draws, no threshold re-tuning
after seeing eval results.
