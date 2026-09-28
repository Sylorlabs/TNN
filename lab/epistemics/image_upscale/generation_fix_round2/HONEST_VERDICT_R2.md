# HONEST VERDICT — Upscale Repair Round 2

Date: 2026-09-27. Prereg: PREREG_R2.md (frozen before implementation).

## Mechanism

(a) Energy-consistent match-time score: score(A) = 4·keySSD(A) + (√UHF(A) − √Hhat(B))²,
    gain vs NULL atom, take iff gain ≥ 108·bw·bh AND gain ≥ gain_split.
(b) Diverse 12-image vocabulary (brick_wall, stone_wall, foliage, lake_water,
    fabric, woodgrain, treebark, portrait, car, building, cat, market),
    caps 96/96/64/48/64, farthest-point selection.

## Bar verdicts

| Bar | Requirement | Result | Verdict |
|-----|-------------|--------|---------|
| BAR 1 (soundness) | (a) on old vocab ≥ baseline −0.05 dB | +0.059 dB (264.8M vs 268.5M SSE; takes 31 vs 35) | **PASS** |
| BAR 2 (no regression) | (a)+(b) on bridge AND sky ≥ baseline −0.10 dB | Bridge −0.47 dB (299.3M vs 268.5M); Sky −0.11 dB (420.2M vs 409.2M) | **FAIL** |
| BAR 3 (broad coverage) | ≥7/9 wins; mean ≥+0.30 dB; every category ≥0 | 6/9 wins; mean +0.297 dB; people −0.62 dB | **FAIL** |

**Mechanism (a)+(b) KILLED per prereg.** BAR 2 fails decisively; BAR 3 fails on
7/9 wins and people-category.

## Per-image deltas vs baseline (new − baseline, dB; positive = better)

| Image | Category | Baseline gen PSNR | New gen PSNR | Δ dB |
|-------|----------|-------------------|--------------|------|
| bridge | (original) | 18.47* | 18.00* | −0.47 |
| sky | (original) | — | — | −0.11 |
| fabric | texture | 21.47 | 22.03 | **+0.56** |
| woodgrain | texture | 18.37 | 19.02 | **+0.65** |
| treebark | texture | 18.94 | 18.77 | −0.17 |
| calmwaters | smooth | 19.46 | 19.73 | **+0.27** |
| portrait | people | 21.19 | 20.57 | −0.62 |
| car | object | 22.92 | 22.65 | −0.27 |
| building | object | 14.96 | 15.23 | **+0.27** |
| cat | animal | 16.60 | 17.43 | **+0.83** |
| market | mixed | 18.36 | 18.51 | **+0.15** |

*Bridge PSNR derived from SSE (GT 512×184). Bicubic: bridge 25.89 dB, sky —.

Category means (Δ dB): texture +0.35, smooth +0.27, people −0.62, object +0.00,
animal +0.83, mixed +0.15.

## What failed and why

The diverse vocabulary (b) is the failure point, not the score (a):

- (a) alone on old vocab: +0.059 dB, takes 31 vs 35, no regression. Sound.
- (b) alone (new vocab + old score): 299.5M SSE on bridge vs 268.5M baseline
  (−0.47 dB). The score is irrelevant; the vocab is worse.
- Farthest-point selection over 12 images optimizes for training-set diversity,
  not test reconstruction. The 4-image vocab concentrated capacity on
  brick/stone/foliage/water textures useful for bridge/sky. The 12-image vocab
  spreads capacity across portraits, cars, cats, markets — irrelevant for the
  originals — and dilutes the useful atoms.
- On the diverse set, (a)+(b) helps 6/9 (fabric, woodgrain, calmwaters,
  building, cat, market) but hurts portrait (−0.62) and car (−0.27), and
  treebark (−0.17). The gains are real but narrow, not broad.

## Honest residuals

1. The energy score (a) is a sound, small improvement (+0.06 dB). It does not
   regress and it changes winners sensibly (7/35 takes on bridge). It is not
   sufficient alone (ceiling +0.025 dB on old vocab per oracle).
2. Vocabulary coverage is the binding constraint, but "more diverse" via
   farthest-point is the wrong way to get it. The selection objective must
   align with reconstruction, not just diversity.
3. The array-size panic (takes > 16384) is a pre-existing bug in azgen.zag,
   exposed by the new vocab's different SHAPES/LINES balance. Fixed by
   increasing to 65536 (capacity only; no logic change; bridge/sky outputs
   byte-identical before/after).
4. Teaching is byte-identical across 3 runs (SHA 51c67ed3...). Generation is
   byte-identical across 2 runs per image (bridge, sky verified).

## What was NOT done

- Diverse eval second run for byte-proof: mechanism killed by BAR 2, so the
  full double-run was not completed. Bridge/sky double-runs verify determinism.
- No post-result tuning. The array-size fix is a bug fix, not tuning.

---
## Evidence

- PREREG_R2.md (frozen)
- azteach2.zag, azgen2.zag (sources)
- vocab_new.bin (SHA 51c67ed32b422c29422acbb84a1e75e6a4341549bd7ef94533b5ca1ec364fba0)
- MANIFEST.tsv, SEALCHECK.txt (corpus provenance, 0 overlap)
- GEN_SCORES.txt per image, RESULTS.tsv (diverse)
- teach.log, teach2.log, teach3.log (byte-identical teaching)
