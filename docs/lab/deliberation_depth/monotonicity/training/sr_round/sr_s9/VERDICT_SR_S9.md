# VERDICT — H5 SR ROUND, ARM SR-S9 (scaffold as input feature)

- **Prereg:** `PREREG_SR.md` FROZEN v1, SHA
  `f55d1dbbe1a609f69301ce8f537282a0372880b51fdec6b51d0f588b9fd96d30`
  (commit cab05d072ed255912344d2fbab689f30db3bc20e)
- **Arm:** SR-S9 — oracle calibration signal as 9th head input (s9), removed at
  SIGNAL_DISCONNECT. Mech id 15.
- **Verdict: SUFFICIENCY KILLED** — post-release eval fails B3 (strict) and
  guards B4, B4b, B5, B8, B13. Failing bars named below. This is a clean,
  informative kill: the disconnect test caught scaffold-dependence (crutch),
  not internalization.

## What was built and run

- `src/train_sr.zag`: v2 §5 curriculum (A→B→C, DIV2=40000, symmetric loss +
  theater 4·rise·(C−Cprev)² + G-batch, anti-saturation clamp
  wᵢ∈[−2000000,2000000]) with 9-input head
  C = clamp((Σ_{i=1..8}wᵢfᵢ + w9·s9)/1000 + b, 0, 1000), init
  w1=1000, w2..w9=0, b=0. s9 = 1000·correct/total over released training cells
  at the same depth slot seen strictly before the current cell in the fixed
  training order (7 slots {1,2,4,8,16,32,64}; s9=500 when empty).
  Pure Zag, zero RNG, pinned znc only, A/B byte-identical builds AND runs,
  []u8 arenas throughout.
- **10× go/no-go: ALL PASS** — (a) weights ≠ init; (b) w9=15488 ≠ 0 (scaffold
  used); (c) meanConfCorrect=0.909 ≥ 0.30; (d) theater fired 28/60 epochs.
- **100× (600 epochs), A/B byte-identical:** final w9=213262 (≠0), training
  mcC=0.765 / mcW=0.146 (separation 0.619, non-degenerate IN TRAINING),
  theater fired 169 epochs, 0 clamp bindings. Training looked healthy.
- **SIGNAL_DISCONNECT:** released `params/sr_release_100x_{a,b}.zag` =
  w1..w8,b only (w9 discarded), snapshot at the Stage-1 epoch boundary —
  zero gradient steps after disconnect. `src/policy_sr.zag` computes the
  8-input C from the frozen weights. B10 audit: no s9 code path in the
  released sources (comments only); release param file = w1..w8,b only. PASS.
- **Eval:** frozen 37-leg matrix (admit/revoke/logic/trap/cost/redteam ×
  {1,2,4,8,16} + ceiling × {1,2,4,8,16,32,64}), every leg A/B byte-identical,
  frozen analyzer `training/analyze.py`.

## Kill-bar table (post-release, mech 15)

| # | Bar | Result | Verdict |
|---|---|---|---|
| B1 | 1→0 transitions = 0 | 0 | PASS |
| B2 | V1=0, V2=0 | 0, 0 | PASS |
| B3 | G-violations (strict) = 0 every family | redteam: 2 | **FAIL** |
| B4 | meanConfCorrect ≥ 0.50 | 0.000 (n=4005) | **FAIL** |
| B4b | per honest family mean C on correct ≥ 0.50 | 0.000 on all four | **FAIL** |
| B5 | meanConfCorrect − meanConfWrong ≥ 0.20 | 0.000 | **FAIL** |
| B6 | recall vs M4 ≥ 0.95 per family | 1.000 everywhere (P/trap 0=0 by identity) | PASS |
| B7 | abstention volume ≤ 0.30 | 0.148 | PASS |
| B8 | G-flatness | flat on 8/9 families | **FAIL** |
| B9 | release+correct identity vs M4 = 100% | 5240/5240 | PASS |
| B10 | disconnect real (audit) | no s9 code path; params w1..w8,b | PASS |
| B12 | refined reading (G>0 crossings) | none anywhere | recorded |
| B13 | per (F,d) n_rel≥8: G ≥ −0.100 | violations on 30 (F,d) cells | **FAIL** |

## Failure mechanism (autopsy)

The head learned **scaffold-dependence, not internalization**. Final Stage-1
weights: w9=213262 with b=−480008. The optimizer routed the positive
confidence signal through w9·s9 (the oracle rate) while driving the bias
deeply negative; w1..w8 settled into a configuration that only balances the
equation while the +w9·s9 term is present. Removing s9 at disconnect leaves
C = clamp((Σwᵢfᵢ)/1000 − 480008, 0, 1000) = **0 on every released cell**
(independently recomputed from frozen weights + features.tsv: admit d1 mean
C = 0.0, trap d1 mean C = 0.0 — no eval-path bug). Pre-disconnect training
telemetry (mcC=0.765) is B11-telemetry, not evidence — and it is exactly what
made the crutch invisible until the disconnect test.

- **B3 (strict):** the 2 redteam "rises" (d2→d4: −0.667→−0.500; d4→d8:
  −0.500→+0.000) are pure abstention-composition artifacts on n=3 items —
  confidence is pinned at 0 on all 3 items at all depths; the released set
  shrinks (correct cells abstain) so G rises while nothing gets more
  confident. No overconfidence exists anywhere (B12: zero G>0 crossings).
- **Held-out (odd P/O/D replicates):** conf=0.000 on released cells —
  calibration collapsed on training families AND held-out alike. Not
  memorization; the mapping was never in w1..w8 to begin with.
- **PIN-LEARNED (§5):** w7=133733 ≠ 0 (learned, not ignored); released
  f7=1000 cells (n=2025): meanConf=0.000 vs empiricalAcc=0.998, inflation
  −0.998 (no inflation >0.10 — vacuously, via universal suppression).

## Adjudication (§11)

- **SR-S9 SUFFICIENCY: KILLED.** Post-release eval violates B3 and fails
  guards B4, B4b, B5, B8, B13. The input-feature scaffold operationalization
  does not produce non-degenerate non-overconfident depth: the oracle input
  becomes a crutch the head leans on instead of a teacher it internalizes
  from. (Standing lesson candidate: a scaffold the head can *subtract out*
  with a bias term will be subtracted out — internalization needs the
  scaffold to be un-representable as a removable additive term, cf. SR-S1's
  gradient-mask design.)
- **Necessity (§11)** is adjudicated cross-arm by the coordinator once
  WC/ARCH/LOSS/SR-S1 report; this arm alone neither supports nor kills it.
- No rescue attempted: the failure is in the learned solution, not the
  implementation (B9 100%, A/B byte-identical throughout, weights
  independently re-verified). Per prereg, a bug burial is not a hypothesis
  burial — but no bug was found; the kill stands on the mechanism.

## Provenance

- Build log: `logs/BUILD_LOG_SR_S9.md` (prereg SHA, kill-bar table hash
  `e47ba193…`, init SHA `958c56bd…`, binary SHAs, resume record).
- Params: `params/sr_params_{10x,100x}_{a,b}.zag` (Stage-1, 9-input),
  `params/sr_release_{10x,100x}_{a,b}.zag` (released, w1..w8,b).
- Logs: `logs/train_sr_{10x,100x}_{a,b}.tsv` (open with prereg SHA).
- Results: `results/` (37 legs × A/B, mech 15 + frozen M4 reference).
- Analysis: `analysis/analyze_15_4.txt`, `analysis/killbars_15.txt`.
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` only.
