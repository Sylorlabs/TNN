# PREREG — Fix the Key-Ambiguity in TNN's Upscale Generation Path (Crew A)

Written 2026-09-26 BEFORE any implementation or run. This prereg governs the
head-to-head test. Tests decide; nothing here may be tuned after seeing scores.

## Problem (from HONEST_RESULT.md, generation/)

Baseline generation-from-learned-atoms: 18.47 dB (bridge), 22.75 dB (sky) vs
bicubic 25.89/33.20. Mechanism: the low-res matching key (2x2 box downscale of
atom deviations, SSD match) is AMBIGUOUS — many high-res patches downscale to
the same key. Concrete failure: a smooth 32x32 bridge-arch block matched a BRICK
atom; the brick's 64x64 high-frequency texture was stamped on the smooth arch
(SHAPES RMSE 54.5). High gain at input res does NOT predict high-res accuracy.

## Arms (all: SHAPES matching discipline changes ONLY; LINES path byte-identical
## to baseline in every arm; construction = measured mean + measured atom
## deviation, unchanged)

- **Arm 0 (reference, not a contender):** pristine `azgen.zag` recompiled.
  Must reproduce the baseline outputs byte-identically (validates the build
  pipeline). Expected: 18.47 dB bridge / 22.75 dB sky.

- **Arm 1 — FINER/SCALE-AWARE KEYS (cross-scale consistency):** for each SHAPES
  block, match atoms at the fine key (s×s, existing) AND at a coarse key
  (s/2×s/2, computed on the fly: 2x2-box downscale of the stored key and of
  the block deviations, round-half-away). TAKE iff (a) the fine-winner is in
  the coarse top-3, AND (b) gain ≥ 9/value (unchanged bar), AND (c) take beats
  the finer split (unchanged). Disagreement → take rejected at that level
  (split/nofit path unchanged → measured-means fallback). Ambiguity flags
  (fine-winner ≠ coarse-winner) counted in the trace. Coarse check skipped
  (auto-pass) when a coarse dim < 2.

- **Arm 2 — SMOOTH-REGION GATING:** τ_min = 25th percentile of atom key-variance
  (per-value SSD of mean-subtracted keys, ×1000, pooled over scales 0–3,
  thin scale excluded). R_band = 75th percentile of r_A =
  (atom full-res deviation energy per value)/(atom key variance), ×1000,
  pooled scales 0–3, zero-variance atoms excluded. For a block with
  σ²_B < τ_min (smooth; compared as e×1000 < τ_min×nval to stay in i64):
  candidate atoms restricted to those with full-res energy-per-value
  ≤ σ²_B × R_band (compared as eA_perval1000×nval ≤ e×R_band; NULL atom
  always allowed). Non-smooth blocks: baseline matching unchanged.

- **Arm 3 — FABLE'S "Local Variance Ratio Gate with Double-Validation":**
  1. σ²_B per block; τ_min/τ_mid = 25th/75th percentile of atom key-variance
     (same derivation as Arm 2's τ_min).
  2. σ²_B < τ_min → reject ALL atoms → NO-FIT (measured-means fallback).
  3. Else top-K=3 by key SSD (K = min(3, na−1)).
  4. Double-validation: for each of the 3, downscale its full-res deviations
     2x2-box to s×s (d_A, mean-subtracted); keep iff inner product
     P = Σ(B−mean_B)·(d_A−mean(d_A)) > 0.
  5. <2 survivors → reject all → NO-FIT.
  6. Winner = min downscaled-SSD among survivors vs the actual block B.
  7. Ambiguity flag if winner ≠ key-SSD top-1 → strict bar gain ≥ 18×nval
     (2× the 9/value precedent), else reject.
  8. Take iff gain ≥ bar AND beats split. Output = measured block mean +
     winner's high-res deviations.
  MODIFICATION TO FABLE'S PROPOSAL (required by the brief): every fallback is
  measured block means (CONSTRUCTED-NO-FIT); bicubic is forbidden in the
  generation output path and survives only as the scoring baseline.

## TNN-involved step (deliberation BEFORE the head-to-head decides)

`delib.zag` runs TNN's deliberation machinery (survey → per-block measurement →
deliberate) on the bridge failure: for each 32×32 block at si=0 it replicates
the baseline take decision and each arm-rule's take decision (SHAPES only),
measuring σ²_B vs τ_min, ambiguity count (atoms within 2× winner SSD),
winner key-variance, winner full-res energy, and the correlation P.
The bad take = the taken smooth block (σ²_B < τ_min) whose winner has maximal
full-res energy (the brick-on-arch archetype). The deliberation votes for the
arm-rule that rejects the bad take with the FEWEST total extra rejections
across all blocks; tie-break by arm order 2, 3, 1. The vote is ADVISORY —
the head-to-head TEST decides the winner. Full trace → RUNLOG.md.
(Simplification, recorded: deliberation evaluates si=0 only; the real arms
run the full 32→4 recursion.)

## Learned constants (measured, not crew-picked)

τ_min, τ_mid, R_band are computed from `vocab.bin` by `corpstat.zag`
(deterministic insertion-sort percentiles, i64 ×1000 fixed point) and
cross-checked with an independent Python/numpy computation. Values are
hardcoded into the arm binaries with provenance comments and recorded in
RUNLOG.md with the derivation. The 25th/75th percentile choices and the 2×
strict-bar multiplier are design choices, recorded here as such.

## Bars

- BAR 1 (improvement): winning arm beats baseline generation (18.47 dB
  bridge, 22.75 dB sky) on BOTH images.
- BAR 2 (honesty): ALL arms reported on ALL test images — no arm hidden,
  no image cherry-picked. Diverse held-out set included IF it exists at
  scoring time (checked; never trained on).
- BAR 3 (compliance): no drawing operators (no Bresenham/DDA/chords/walks/
  procedural gradients); no bicubic in the generation output path; zero RNG;
  byte-identical reruns (every binary run twice, outputs SHA-256 compared).
- BAR 4 (stretch): match/beat old per-image 25.96 dB on bridge. Likely
  unmet — reported honestly either way.
- KILL (program): if no arm beats baseline on both images → honest loss
  with mechanism analysis. Do NOT tune to the test.
- KILL (Arm 3, Fable's): if Arm 3 improves <2 dB over 18.47 dB on bridge,
  OR rejects >30% of top-level SHAPES blocks (nofits fraction), Arm 3 is
  killed — reported, not hidden.

## Method notes

- Vocab and azteach reused as-is (no reteaching). Held-out images never
  enter training (they never did).
- PSNR = mean of per-channel dB; SSIM = Gaussian-window per-channel mean
  (src/metrics.py, unchanged).
- Build with the pinned toolchain
  ~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1.
  Binaries built in build/, deleted after scoring (disk 98%).
- No commits (coordinator handles all commits). No binaries or rendered
  images left in repo dirs.

---
## Dated correction (2026-09-27, appended — original text above untouched)

The header's "Written 2026-09-26" is off by one day: this prereg was written
and the entire session ran on 2026-09-27 UTC. Content, mechanisms, and kill
bars are unaffected. Additionally, the deliberation later proved the
"a smooth 32x32 bridge-arch block" description imprecise: the worst take's
block is mid-variance by the corpus τ_min (3,575,392 > 2,985,492), not smooth.
The frozen mechanisms and bars stand as written.
