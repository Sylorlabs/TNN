# CALIBRATION_RECORD.md — FELT-INTENSITY V3

Date: 2026-09-20. Status: **FROZEN.** Trial cells compile only after this
record exists (runner-enforced, I-8); no human touches the constants
afterward.

Procedure: `PREREG_FELT_V3.md` §6 as amended by `PREREG_FELT_V3_AMEND1.md`
A3/A5/A6. Judgment-free replay on disjoint calibration variants v∈{7,8},
500 episodes each, same §8 curriculum formulas. I read for every admitted
memory at m+50 and at run end under each of the 45 grid points. No
judgments run during calibration (AUC is judgment-independent), so there
is no circularity.

Grid (frozen): α ∈ {10,12,14,16,18}, β ∈ {15,20,25}, γ ∈ {20,25,30} —
45 combinations, deterministic order (α, then β, then γ).

Objective (frozen): maximize mean `AUC_proven` over v∈{7,8}. Ties →
lowest grid index. (Rational arithmetic; the winning mean is exactly
37523/38225, shared by 27 grid points; grid 9 is the lowest tied index.)

## Frozen constants

```
CAL_ALPHA=12
CAL_BETA=15
CAL_GAMMA=20
THETA_INVEST=48        # prior + 1.5*alpha = 30 + 18  (A5)
THETA_SACRIFICE=36     # prior + 0.5*alpha = 30 + 6   (A5)
```

These exact values are written into `impl/calib_consts.zag`; the build
script refuses to compile trial cells unless the source constants equal
this record (I-8).

## Selection

- Grid index 9: α=12, β=15, γ=20.
- AUC_proven(v=7) = 150620/152900 = 0.9851 (npos=275, nneg=278)
- AUC_proven(v=8) = 102220/104500 = 0.9782 (npos=275, nneg=190)
- Mean = 37523/38225 ≈ 0.9816 (max over grid; 27-way exact tie, lowest
  index wins per the frozen tiebreak).

## Sanity gates (INVALID if any fails — none failed)

- G-C1 invest-reachability (A3 scope): min I over twice-corroborated
  (C≥2) right-important ∧ not-wrong ≥ θ_invest=48:
  v=7: 54 ≥ 48 PASS; v=8: 54 ≥ 48 PASS.
- G-C2 AUC_proven(selected) ≥ 0.60 on calibration data:
  v=7: 0.9851 PASS; v=8: 0.9782 PASS.
- G-C3 F4a′ on calibration (A3 scope): max I over non-designated junk ≤
  prior+10=40: v=7: 30 PASS; v=8: 30 PASS.

## All 45 AUCs (integer Mann-Whitney form: num/den)

den = 2·npos·nneg. npos/nneg are identical at every grid point
(v=7: 275/278; v=8: 275/190); only the intensity values move.

| gi | α | β | γ | AUC v=7 | AUC v=8 |
|----|---|---|---|---------|---------|
| 0 | 10 | 15 | 20 | 99510/152900 = 0.6508 | 51110/104500 = 0.4891 |
| 1 | 10 | 15 | 25 | 48400/152900 = 0.3165 | 0/104500 = 0.0000 |
| 2 | 10 | 15 | 30 | 48400/152900 = 0.3165 | 0/104500 = 0.0000 |
| 3 | 10 | 20 | 20 | 99510/152900 = 0.6508 | 51110/104500 = 0.4891 |
| 4 | 10 | 20 | 25 | 48400/152900 = 0.3165 | 0/104500 = 0.0000 |
| 5 | 10 | 20 | 30 | 48400/152900 = 0.3165 | 0/104500 = 0.0000 |
| 6 | 10 | 25 | 20 | 99510/152900 = 0.6508 | 51110/104500 = 0.4891 |
| 7 | 10 | 25 | 25 | 48400/152900 = 0.3165 | 0/104500 = 0.0000 |
| 8 | 10 | 25 | 30 | 48400/152900 = 0.3165 | 0/104500 = 0.0000 |
| 9 | 12 | 15 | 20 | 150620/152900 = 0.9851 | 102220/104500 = 0.9782 |
| 10 | 12 | 15 | 25 | 48400/152900 = 0.3165 | 0/104500 = 0.0000 |
| 11 | 12 | 15 | 30 | 48400/152900 = 0.3165 | 0/104500 = 0.0000 |
| 12 | 12 | 20 | 20 | 150620/152900 = 0.9851 | 102220/104500 = 0.9782 |
| 13 | 12 | 20 | 25 | 48400/152900 = 0.3165 | 0/104500 = 0.0000 |
| 14 | 12 | 20 | 30 | 48400/152900 = 0.3165 | 0/104500 = 0.0000 |
| 15 | 12 | 25 | 20 | 150620/152900 = 0.9851 | 102220/104500 = 0.9782 |
| 16 | 12 | 25 | 25 | 48400/152900 = 0.3165 | 0/104500 = 0.0000 |
| 17 | 12 | 25 | 30 | 48400/152900 = 0.3165 | 0/104500 = 0.0000 |
| 18 | 14 | 15 | 20 | 150620/152900 = 0.9851 | 102220/104500 = 0.9782 |
| 19 | 14 | 15 | 25 | 150620/152900 = 0.9851 | 102220/104500 = 0.9782 |
| 20 | 14 | 15 | 30 | 48400/152900 = 0.3165 | 0/104500 = 0.0000 |
| 21 | 14 | 20 | 20 | 150620/152900 = 0.9851 | 102220/104500 = 0.9782 |
| 22 | 14 | 20 | 25 | 150620/152900 = 0.9851 | 102220/104500 = 0.9782 |
| 23 | 14 | 20 | 30 | 48400/152900 = 0.3165 | 0/104500 = 0.0000 |
| 24 | 14 | 25 | 20 | 150620/152900 = 0.9851 | 102220/104500 = 0.9782 |
| 25 | 14 | 25 | 25 | 150620/152900 = 0.9851 | 102220/104500 = 0.9782 |
| 26 | 14 | 25 | 30 | 48400/152900 = 0.3165 | 0/104500 = 0.0000 |
| 27 | 16 | 15 | 20 | 150620/152900 = 0.9851 | 102220/104500 = 0.9782 |
| 28 | 16 | 15 | 25 | 150620/152900 = 0.9851 | 102220/104500 = 0.9782 |
| 29 | 16 | 15 | 30 | 150620/152900 = 0.9851 | 102220/104500 = 0.9782 |
| 30 | 16 | 20 | 20 | 150620/152900 = 0.9851 | 102220/104500 = 0.9782 |
| 31 | 16 | 20 | 25 | 150620/152900 = 0.9851 | 102220/104500 = 0.9782 |
| 32 | 16 | 20 | 30 | 150620/152900 = 0.9851 | 102220/104500 = 0.9782 |
| 33 | 16 | 25 | 20 | 150620/152900 = 0.9851 | 102220/104500 = 0.9782 |
| 34 | 16 | 25 | 25 | 150620/152900 = 0.9851 | 102220/104500 = 0.9782 |
| 35 | 16 | 25 | 30 | 150620/152900 = 0.9851 | 102220/104500 = 0.9782 |
| 36 | 18 | 15 | 20 | 150620/152900 = 0.9851 | 102220/104500 = 0.9782 |
| 37 | 18 | 15 | 25 | 150620/152900 = 0.9851 | 102220/104500 = 0.9782 |
| 38 | 18 | 15 | 30 | 150620/152900 = 0.9851 | 102220/104500 = 0.9782 |
| 39 | 18 | 20 | 20 | 150620/152900 = 0.9851 | 102220/104500 = 0.9782 |
| 40 | 18 | 20 | 25 | 150620/152900 = 0.9851 | 102220/104500 = 0.9782 |
| 41 | 18 | 20 | 30 | 150620/152900 = 0.9851 | 102220/104500 = 0.9782 |
| 42 | 18 | 25 | 20 | 150620/152900 = 0.9851 | 102220/104500 = 0.9782 |
| 43 | 18 | 25 | 25 | 150620/152900 = 0.9851 | 102220/104500 = 0.9782 |
| 44 | 18 | 25 | 30 | 150620/152900 = 0.9851 | 102220/104500 = 0.9782 |

Reading the table: β never moves the AUC (no memory in either class is
ever contradicted, so the contradiction weight is unexercised); γ ≥ 25
at low α collapses the AUC because designated junk reads 30+γ above
twice-corroborated positives. The plateau at 0.9851/0.9782 is a tie
ceiling (boundary reads with a single corroboration).

## Class notes (for the checker's scoping)

- v=7 negative class: 278 reads = PROBE-observed junk + designated junk.
- v=8 negative class: 190 reads = designated junk only. The v=8 probe
  schedule `(m+8)%5==0` ⟺ `m%5==2` ⟺ `m%10∈{2,7}` lands only on
  important/wrong episodes, never on junk — so v=8 has no PROBE
  negatives by curriculum construction. Both variants clear the
  n_proven_neg_reads ≥ 50 bar (278, 190).
- npos=275 (not 296): 6 class-1 memories admitted at m≥475 receive no
  corroboration before run end (m+25 > 499) and are unproven; 15
  memories admitted at m≥450 get a single read (m+50 and run-end
  coincide). Verified against the ledger, not assumed.

## Determinism

Two runs per calibration cell, byte-identical (sha256-compared),
per §14:

- cal7: `116195f23da185e40580a0e318a660cc4ffa6240d50d2bccb5cfba33edac28ee`
- cal8: `4f3bbe9161a46fd74fb7045380aa9b9d3943ed197fcadb1ac80d7c9aa55dba39`

## Module hashes (what the calibration was computed with)

- felt_v3.zag: `b02173812578632a7c4cc79fd00220c6d1978424cdfa824687060f9022aa2032`
- felt_trial_v3.zag: `d94d396e3d31be96f713bbf4d1a246cd20c13c3de8c84edfdd20cfb7e70964c3`
- st_memory_core.zag: `60f5ef90dc4b274d57ea01147c44bcc543d9a8f27abf4d9f7203249dfbbf11aa`
  (byte-identical to wave-5 `strength-trial-run/trial/st_memory_core.zag`)
- substrate/cl/common.zag: `8aec83cb4feb83a20bc91c8179d7055d691c155414a359f7014386271aa6168b`
- substrate/R33_NATIVE_SHA256_V2.zag: `9824f6db66a943917dbc7cd5e6862ab0967b7ea83161cfc357bb7d17ca683bcf`
- substrate/R33_NATIVE_IO_V1.zag: `e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8`

Note: the calibration binary was compiled with a clearly-marked
temporary placeholder `calib_consts.zag` (grid midpoint α=14/β=20/γ=25)
because the trial driver and the calibration driver are one binary and
the placeholder's symbols are required at compile time. The
calibration path never references those symbols (it sweeps the grid
internally), so the FELT_CAL outputs are independent of the
placeholder. Proof: after freezing, the trial binary was recompiled
with the frozen constants and both calibration cells re-run —
FELT_CAL outputs byte-identical to the hashes above
(see IMPLEMENT_NOTES.md).
