# H5 DEPTH — Training v2 VERDICT (MT2-CONF-10× / MT2-CONF-100×)

Frozen: 2026-09-24. Prereg: `PREREG_TRAINING_V2.md` (this directory).
Question: **does genuine upward calibration training produce calibrated — not merely silent — depth?**

## Verdict (plain)

**The strong hypothesis is FALSIFIED (strict reading) / PARTIAL (refined reading).
The hypothesis is NARROWED, not buried.**

- The v2 training machinery WORKS: upward calibration signal proven live, theater
  term firing, head NON-DEGENERATE (mean correct-cell confidence 0.747, correct−wrong
  separation 0.433), and PERFECT calibration (G = 0.000 flat across depths) on
  5 of 9 families. This is the opposite of v1's degenerate silence.
- But the law is NOT achieved: at 100× the eval matrix shows **44 V2 violations
  (all ceiling/P) + 7 strict G-rises** (4 zero-crossings under the refined reading),
  concentrated on the adversarial families (P/O/redteam).
- The failure is NOT bug-caused: all four §8 machinery checks pass
  (feature indexing, upward motion, theater liveness, implementation integrity).
- The residual is CHARACTERIZED (see §6): a mean-optimizing (MSE) curriculum cannot
  buy worst-case law compliance — the global optimum sacrifices the adversarial 2%.
  A 98.9%-accurate linear P/O separator EXISTS in the head class; the curriculum
  does not find it because the loss does not prioritize it.
- Developmental: violations more than halved 10×→100× (V2 95→44, Gviol 16→7);
  4 families went fully clean. The machinery learns — it asymptotes against the
  adversarial worst case.

Narrowed hypothesis that survives: **upward calibration training teaches genuine,
non-degenerate calibration and eliminates violations on honest families, but
worst-case law compliance on adversarial families requires worst-case (not average)
optimization.** The §6 abstention-gate experiment is the recommended next test.

## 1. What v2 changed (frozen in prereg §4/§5)

- Feature indexing fixed: feature k reads TSV field 7+k (`f1..f8`; v1 read `f2..f8,0`).
- Symmetric calibration loss `L = (C−Y)² + 4·rise²` (v1's extra asymmetric
  confident-wrong term removed); representable integer updates with `DIV2=40000`
  (v1: 4000000, which truncated every correct-cell upward step to zero).
- G-batch (one-sided law guardrail) retained; weight clamp ±2,000,000 with binding log.
- Head form unchanged: `C = clamp((Σwᵢfᵢ)/1000 + b, 0, 1000)`; init M4-like
  (`w1=1000`, rest 0). Frozen input `features.tsv`
  (SHA-256 `4682190c…65a897d`, 5240 cells, 4820 train / 420 heldout).

## 2. Machinery audit — PREREG §8 (all BEFORE official training)

| # | Check | Result |
|---|-------|--------|
| 1 | Field-index probe (synthetic cell, only f3=1000) | PASS — weight index 2 moved +50/+45 (v1 bug would move index 1) |
| 2 | Upward representability (correct cell, exact tdiv amounts) | PASS — mcC 100→190 over 2 phase-0 epochs, exact hand-computed steps |
| 3 | Theater probe (wrong→wrong rising chain) | PASS — v2 fired epochs 0–1, pushed w1 1000→816→728 |
| 4 | Build A/B | PASS — `train2_bin_a` ≡ `train2_bin_b` (SHA `8d55bdfd…b8f789`) |
| 5 | Training A/B | PASS — 10× and 100× params+logs byte-identical across binaries |
| 6 | Eval A/B | PASS — 37×2 legs per tag, all byte-identical |
| 7 | Policy build A/B | PASS — per-tag build trees byte-identical |
| 8 | Release identity vs M4 | PASS — 5240/5240 identical release/correct (§1 admissibility) |

Determinism: zero RNG anywhere; every artifact reproduced byte-for-byte.

## 3. Training results

**10× go/no-go (prereg §5) — all four PASS:**
(a) final weights ≠ init (`w1=13425, w6=19963, w7=9048, b=−26009`);
(b) theater fired 23 epochs / 526 events; (c) mcC = 0.775 ≥ 0.30;
(d) phase-A loss fell pass0→pass1. Clamp bindings: 0.

**100× final weights** (`params/mt2_params_100x.zag`, SHA `8c826a42…3d5e`):
`w = [119402, −5941, 0, −7477, 1006, 169884, 92249, 6000]`, `b = −225895`.
Theater: 114 epochs / 1956 events. Clamp bindings: 0 (never saturated).
Loss plateaued (<1% change over final 10 epochs/phase). Training G-violations
persisted at 5–7/epoch — the P/O/admit/redteam rises (see §6, not a stall artifact).

**Non-degeneracy (eval, mech 14):** meanConfCorrect = 0.747 (bar ≥0.50 PASS);
correct−wrong separation = 0.433 (bar ≥0.20 PASS).

## 4. Eval matrix results (37 legs × A/B, mech 13 = 10×, mech 14 = 100×)

| mech | 1→0 | V1 | V2 | Gviol (strict) |
|------|-----|----|----|----------------|
| M0 | 0 | 0 | 0 | 0 |
| M1 | 41 | 41 | 166 | 17 |
| M2 | 41 | 41 | 44 | 15 |
| M3 | 1 | 1 | 160 | 12 |
| **M4 (baseline)** | 0 | 0 | **160** | **14** |
| M5 | 0 | 0 | 0 | 10 |
| M6 | 0 | 0 | 0 | 10 |
| M7 | 42 | 42 | 161 | 16 |
| M8 | 0 | 0 | 13 | 10 |
| **MT2-CONF-10× (m13)** | 0 | 0 | **95** | **16** |
| **MT2-CONF-100× (m14)** | 0 | 0 | **44** | **7** |

Per-family at 100× (strict G-rises; refined = only zero-crossings):

| family | V2 | Gviol | G curve | note |
|--------|----|-------|---------|------|
| revoke | 0 | 0 | 0.000 flat | PERFECT |
| logic | 0 | 0 | 0.000 flat | PERFECT |
| cost | 0 | 0 | 0.000 flat | PERFECT |
| trap | 0 | 0 | 0.000 flat (d1–d4) | PERFECT (M4: V2=90) |
| D | 0 | 0 | 0.000 flat | PERFECT — acc rises 0.25→1.0 with depth, conf tracks it exactly |
| admit | 0 | 1 | −0.355→−0.926, one +0.066 rise d4→d8 | strict-only; stays negative (underconfident) |
| ceiling/O | 0 | 2 | −1.000→−0.004→+0.000 | d2→d4 crosses 0 (refined violation) |
| ceiling/P | 44 | 2 | +0.000→+0.996→+1.000 | maximal overconfidence on wrong answers |
| redteam | 0 | 2 | −0.333→+0.000→+1.000 (n=3) | both cross 0 |

Refined reading: 4 G-crossings (O×1, P×1, redteam×2) + 44 V2. Phase-A/B
(admit/revoke/logic/trap/cost/D) fully clean under the refined reading.

## 5. P/O mirror confrontation

- P and O released training cells occupy the same index-state region: f1, f2, f3,
  f4, f6, f7, f8 have IDENTICAL support across the families; only f5 (evidence
  fraction) differs, with INTERLEAVED values (47, 95, 142, 190, 285 appear in both).
  0/90 P cells have a feature-identical O cell at the same depth.
- The head scores both ≈1000: calibrated on O (acc≈1), maximally overconfident
  on P (acc=0, G=+1.000, conf rising with depth → 44 V2).
- Linear separability probe (deterministic perceptron, P-wrong vs O-correct, n=180):
  **98.9% separable** — a separator EXISTS in the head class, but the v2 head
  scores 50.0% (calls everything correct). The MSE curriculum's global optimum
  sacrifices the 90 P cells (2% of data) to keep 3880 honest-correct cells calibrated.
- Conclusion: the residual is a **mean-vs-maximum mismatch**, not a representational
  impossibility and not a training bug. The G-batch fires on P rises but cannot move
  the global optimum.

## 6. Sole-survivor pin — learned handling (prereg §7)

- (a) `w7 = 92249 ≠ 0` — pin weight learned, large positive. PASS.
- (b) Released f7=1000 eval cells (n=2025): meanConf = 0.538 vs acc = 0.998,
  inflation −0.460 ≤ +0.10. PASS (head is UNDERconfident on the pin population).
- (c) Wrong pin cells listed: 5, all `RT-K12-01` (redteam), depths 1–16,
  conf = 1000 each. The head overgeneralizes "sole survivor → correct" to this
  adversarial item; population-level handling is learned, item-level is not.
- (d) Non-degeneracy PASS → no universal suppression. PASS.
- The pin is handled through LEARNED weights, not a hardcoded suppressor. Residual
  item-level overconfidence on RT-K12-01 is admitted as a violation-class instance.

## 7. Falsification accounting (prereg §3, §9)

- Mechanical bar: ≥1 V2 or G-rise on the eval matrix at 100× → FIRED
  (44 V2 + 7 strict rises). **H (strong form) FALSIFIED.**
- Burial rule: v2 fails AND feature indexing ✓, upward motion ✓, theater ✓,
  implementation integrity ✓ all pass → not bug-caused; the "leave open" clause
  does not apply.
- PARTIAL clause: refined reading shows violations eliminated on Phase-A/B with
  adversarial-family residual (O/redteam/P) AND counts strictly reduced vs M4
  (V2 160→44, Gviol 14→7) with the residual characterized → **PARTIAL: hypothesis
  NARROWED, not buried.**
- What keeps it alive: genuine non-degenerate calibration learned; 5 families
  perfect; developmental improvement 10×→100×; residual precisely characterized.
- What would bury it: a worst-case-optimizing curriculum (or the §6 gate) also
  failing with machinery checks passing.

## 8. Reproduction

- Compiler: `tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
- `src/train2.zag` builds A/B byte-identical (`8d55bdfd…b8f789`).
- Train: `train2_bin features.tsv {10,100} params/mt2_params_{10,100}x.zag logs/log_{10,100}x.tsv`
  — A/B byte-identical (params `fa1a9a20…59` / `8c826a42…5e`; logs `f215fd6b…41` / `9851191c…5e`).
- Policy: per-tag build trees (`work/build_policy.sh`) with frozen params +
  trivial `mt_gate.zag`; A/B byte-identical (`bfe02e3e…82af` / `c110b66e…5e`).
- Eval: `work/run_eval.sh {10x,100x} {13,14}` — 37 legs × A/B, all byte-identical
  (148 TSVs in `work/results/`).
- Analysis: `analysis/` (baselines m0–m8 symlinked from `mechanisms/results/`,
  v2 m13/m14 from `work/results/`); `analyze.py` (frozen), `pin_analysis.py` (new).
- No binaries or `.zag-cache` committed (Micah's standing law).

## 9. Recommended follow-ups

1. **§6 abstention-gate experiment** (condition met: non-degenerate + violations
   persist): freeze the 100× head, train a learned abstention gate on the same
   8 features + conf, re-run the matrix. Tests whether the residual is removable
   at the release locus. NOTE: the mirror binds the gate too — expect it to learn
   an f5-quirk P-detector; interpret accordingly.
2. **Worst-case loss curriculum**: replace mean MSE with a minimax/G-aware loss
   (penalize max family-depth G-rise); tests the §6 diagnosis directly.
3. **Admit underconfidence**: the head is strongly underconfident on admit at
   depth>1 (G≈−0.9) — calibration-poor but law-safe; a richer head or longer
   curriculum may recover it.
4. RT-K12-01 (the 5 wrong pin cells): case study for item-level pin handling.
