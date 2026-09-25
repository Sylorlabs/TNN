# F35 CDC — Verdict

**Date:** 2026-09-25  
**Fork:** F35 CDC (Cluster-Discovered Ceilings), mechanism 35  
**Authority:** PREREG_FORKROUND.md FROZEN v2 §3; ideas/grok_forks.md Fork 5  
**Prereg commit:** 3a2eef44  
**Verdict:** **KILLED**

## §10 Verdict

**KILLED.** The mechanism fails four kill bars (B2, B3, B4b, B13) and triggers
mandatory falsifier #3 (eval strict B3 = 8 ≥ NEC's 6).

## Kill-bar table (frozen analyzer + custom metrics, 37-leg matrix)

| # | Bar | Measurement | Threshold | Result |
|---|-----|-------------|-----------|--------|
| B1 | §1 accuracy (n10) | 0 | = 0 | PASS |
| B2 | Theater (V1+V2) | V1=0, V2=85 | = 0 | **FAIL** |
| B3 | Law strict (G-violations) | 8 | = 0 every family | **FAIL** |
| B4 | Non-degenerate (meanConfCorrect) | 0.8772 (n=4005) | ≥ 0.50 | PASS |
| B4b | Honest-family floor | ceiling/D: 0.3970 (n=70) | ≥ 0.50 | **FAIL** |
| B5 | Separation | 0.2231 | ≥ 0.20 | PASS |
| B6 | Recall | 1.00 (by B9) | ≥ 0.95 | PASS |
| B7 | Abstention volume | 0.1475 (773/5240) | ≤ 0.30 | PASS |
| B8 | G-definedness (amended §4b) | PASS (redteam/trap VOID) | pass | PASS |
| B9 | Answer channel frozen | 5240/5240 = 100% | 100% | PASS |
| B12 | Refined reading (G>0 crossings) | 0 | recorded | RECORDED |
| B13 | Underconfidence floor | 21 violations (G < -0.100) | ≥ -0.100 | **FAIL** |
| B3pi | Per-item B3 (recorded) | 155/3467 = 4.47% | recorded | RECORDED |

## Mandatory falsifiers

1. **Discovery fails (I(cluster;battery)≈0):** NOT TRIGGERED.  
   I(cluster;battery) = 0.9063 bits (n=4222 training cells), well above the
   0.05-bit operationalization threshold. Clusters do carry battery information.
   Distribution: 8 clusters discovered (K=8, cap-bound).

2. **Partition does not stabilize within 2,000 items:** NOT TRIGGERED.  
   Last birth at block 2 (items 512-767); zero births/merges from block 3
   (item 768) onward. Stabilized by item 768 < 2000.

3. **Eval strict B3 ≥ NEC's 6:** **TRIGGERED.**  
   F35 B3 (G-violations) = 8. Prereg yardstick NEC m9 B3 = 6. 8 ≥ 6.

## Deltas vs NEC m9 (prereg yardstick: B2 pass, B3=6, B13=6)

| Metric | NEC m9 (prereg) | F35 CDC | Delta |
|--------|-----------------|---------|-------|
| B2 (V1+V2) | 0 (pass) | 85 | **+85 (worse)** |
| B3 (Gviol) | 6 | 8 | **+2 (worse)** |
| B13 (violations) | 6 | 21 | **+15 (worse)** |

F35 is strictly worse than NEC on all three yardstick metrics.

## Discovered cluster count

K=8 (prereg test cap TEST_KMAX=8; cap_bound=1, i.e., cap was binding).
Storage arena supports 64 prototypes; the 8-cap is test-only per prereg.

## Cluster↔battery MI

I(cluster;battery) = 0.9063 bits. Clusters are informative about battery
(admit/logic/revoke dominate clusters 0,1,5; trap clusters 3,4,7; ceiling
families spread across clusters).

## Per-cluster residual signs

(From SRS residuals: per-cluster, per-depth mean residual signs recorded in
analysis; see logs/train_stats_A.tsv and params/f35_params.txt for
per-cluster rho counts and transition ledgers.)

## Test-cap binding

**cap_bound=1: the K≤8 test cap was binding.** Training hit K=8 with 8 births
and 0 merges. The mechanism wanted more clusters than the prereg test cap
allowed. Per prereg, K≤8 is a test cap only, not an architectural limit;
the 64-prototype arena was not exhausted.

## Failure-mode analysis

**Primary failure (FM-number):** The mechanism exhibits **theater (B2)** with
85 V2 violations (confidence rising on wrong-wrong transitions) and **law
violations (B3)** with 8 G-violations, both worse than NEC. The cluster-
discovered ceilings do not produce monotone non-increasing calibration gaps.

**Secondary failures:**
- **B4b:** ceiling/D family mean confidence on released-correct is 0.3970,
  below the 0.50 honest-family floor. The D-family (distractor) items are
  systematically underconfident.
- **B13:** 21 (family,depth) slots with n_rel≥8 have G < -0.100, indicating
  systematic underconfidence across admit, ceiling/D, ceiling/O, cost, logic,
  and revoke families. The mechanism over-corrects for overconfidence,
  landing in underconfidence.

**Interpretation:** CDC's per-cluster SRS residuals and yield-gated confidence
produce a confidence signal that is (a) non-monotone in depth (V2 theater),
(b) miscalibrated in the G-law sense (B3), and (c) systematically depressed
(B13, B4b-ceiling/D). The clustering discovers battery structure (MI=0.906
bits) but the confidence built on it does not achieve the non-degenerate
non-overconfident depth the round requires.

## Process notes

1. **DESIGN.md date:** Written 2026-09-24, corrected to 2026-09-25 before any
   build or training. No binary existed and no training had occurred at
   either date. The design content predated all builds.

2. **Distance-recording resolution:** Only assigned cells record distances for
   τ; birth cells have no nearest-prototype distance. Documented in DESIGN.md
   §4. This is a faithful reading of "nearest-prototype distances" (a birth
   has no prototype to be near).

3. **Heldout handling:** Policy emits all 5,240 rows; heldout rows never
   update learned state (params frozen at eval). Per-item inference state is
   maintained per item for heldout evaluation.

4. **A/B determinism:** Both binaries byte-identical across A/B builds.
   Training outputs byte-identical across A/B runs. Eval outputs byte-
   identical across A/B runs (37 files each, 5,240 rows total).

## Evidence

- Sources: `src/` (SHA-256 in `logs/SRC_SHA256SUM.txt`)
- Params: `params/f35_params.txt` (SHA-256: faade316b1892aaa7e8fbb9a2ec8f1b4de0b8bcffb82f909188fd6b646b9669e)
- Cluster log: `params/cluster_log.tsv`
- Cellmap: `params/cellmap.tsv` (SHA-256: cdb0fa71c22e4de7de91c2b8540d42f92a067385da442ea582ee2f0e8a578122)
- Results: `results/eval/` (37 TSVs, analyzer-compatible names)
- Analyzer output: `analysis/analyze_35.txt`
- Training logs: `logs/train_A.log`, `logs/train_B.log`, `logs/train_stats_A.tsv`
- Eval logs: `logs/eval_A.log`, `logs/eval_B.log`

## Build provenance

- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
- Train binary A/B SHA-256: aaad6f8e032d3f05dd4012923a03a2d230c20ca101b9c44aa0ddde841c5b4038
- Policy binary A/B SHA-256: 76d7e97819120681671ac8759f1152d4827d30d9dbf0395da16948de36afb158
- Training input SHA-256: 4682190cfd504cb692df122a6b054d8fad65ef860707e6a92abfdf04e65a897d
