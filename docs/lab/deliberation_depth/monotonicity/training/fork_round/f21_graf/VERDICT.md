# VERDICT — F21 GRAF (Per-Depth G-Anchored Fitter), mech 21

**Adjudication (§10): KILLED** — failing bars B2, B3, B13; falsification (a)
triggered (capacity problem). Honest kill, not bar-gaming.

## What was built
- Head form UNCHANGED: C(s) = clamp((Σ w_i·f_i)/1000 + b, 0, 1000).
- New training objective (frozen λ=1, μ=4, recorded in
  `params/FROZEN_HYPERPARAMS.md` BEFORE the first run):
  L = Σ_r n_r·G(r)² + λΣ(c−y)² + μΣ max(0, c_d−c_prev),
  G(r) = trunc(1000·Σ(c−y)/n_r), rungs = family×depth over released training
  cells. Deterministic integer coordinate descent (±8 then ±1, fixed sweep
  order w1..w8,b, first strict improvement), zero RNG.
- Pure Zag, pinned toolchain, A/B byte-identical builds AND runs (trainer,
  params, policy, all 37 legs). Training run twice → byte-identical params
  (`34848abf…e2f6d6651e7`). Independent Python replica of L matches the
  trainer's final L exactly (57589098954757). §5 checkpoint: weights ≠ init
  (1041 strict-improvement moves; L 3.95e14 → 5.76e13). GO.
- B9: release+correct identity vs M4 = 5240/5240 (100%). PASS.

## Kill-bar table (frozen analyzer + killbars.py; 37-leg battery)

| Bar | Threshold | F21 | Verdict |
|---|---|---|---|
| B1 accuracy (1→0) | = 0 | 0 | PASS |
| B2 theater (V1=V2) | = 0 | V1=0, **V2=181** | **FAIL** |
| B3 strict (Gviol) | = 0 every family | **15** (all 9 families ≥1) | **FAIL** |
| B4 meanConfCorrect | ≥ 0.50 | 0.971 | PASS |
| B4b honest-family floor | ≥ 0.50 | 0.586–1.000 | PASS |
| B5 separation | ≥ 0.20 | 0.712 | PASS |
| B6 recall | ≥ 0.95 | 1.000 (all families) | PASS |
| B7 abstention | ≤ 0.30 | 0.148 | PASS |
| B8 amended | pass | PASS (7 fam; VOID redteam/trap) | PASS |
| B9 release identity | 100% | 5240/5240 | PASS |
| B13 underconf floor | ≥ −0.100 | **7 offenders** (O×6, cost d1) | **FAIL** |
| B12 G>0 crossings | recorded | 14 | — |
| B3pi per-item | recorded | 499/3467 = 14.4% | — |

Deltas vs NEC m9 (B2 pass / B3=6 / B13=6): B2 **+181 V2** (worse),
B3 **+9** (worse), B13 **+1** (worse), B1 −42 (better: 0 vs 42).

## Falsification conditions (frozen)
- **(a) TRIGGERED.** Full-n legs still violate strict B3: admit (248/rung,
  Gviol=2), cost (125/rung, 1), logic (264/rung, 1), revoke (113/rung, 1).
  Per-depth anchoring failed ⇒ capacity problem, not fitting.
- (b) Not triggered (B6=1.00 ≥ 0.95; B4=0.971 ≥ 0.50).
- (c) Not triggered as stated (B3 fails too — no bar-gaming; honest failure).

## Why it died — failure mode FM9 (proposed, new)
**FM9: rung-incoherent linear capacity.** One linear head cannot be
simultaneously calibrated across (family×depth) rungs: the features do not
separate the subpopulations, so per-depth G-anchoring compromises and strict
B3 fails even on full-n legs with zero selection (admit/cost/logic/revoke
relrate = 1.00 at every rung — mode 6 does not apply).

Evidence:
- The fitter minimized ΣnG² 6.9× to full-sweep convergence, yet G still
  rises 1→2 on all four honest full-n legs (admit −0.023→−0.021,
  cost −0.101→0.000, logic −0.012→−0.003, revoke −0.079→−0.002).
- Ceiling O vs P at d1 is the stark form: O all-correct gets G=−0.579
  (mean conf 0.42 on correct cells), P all-wrong gets G=+0.419 — the same
  linear weights must raise conf on O while lowering it on P, and the
  8-feature space does not separate them. The P@4 rung alone (G=+0.820,
  n=40) is ~47% of final L; the optimum sacrifices O (B13 dies ×6) and
  admit's d1/d2 to feed it.
- The μ theater term was 4×10⁻⁹ of final L and the λ term 10⁻⁶: as
  literally specified, G(d) is 10⁶× the analyzer's G, so the rung term
  outweighs λ/μ by ~10⁶×/10⁹× in commensurate units. The fitter
  effectively minimized rung-means alone — and B2 got *worse* than the
  M4 baseline (V2 181 vs 160). A re-weighted revival is a new fork per
  round rules; not attempted here.
- B3pi 14.4% corroborates: per-item gaps rise across depths even where
  rung means were flattened — the rung-mean constraint does not bind
  item paths (Fable's Q5 circularity, measured).

This is the adversarial note's predicted failure, realized: "one linear
head may not be calibratable at all rungs simultaneously."

## §6 long horizon
Not applicable — killed at the short battery.

## Data notes
- `training/features/features.tsv` SHA-256 =
  `4682190cfd504cb692df122a6b054d8fad65ef860707e6a92abfdf04e65a897d`.
  PREREG_FORKROUND.md §2 (and the fork brief) record `…f04e65e897d` —
  single-character transcription typo; the on-disk file matches six earlier
  frozen records (v2 prereg/verdict, T05, SR prereg, SR build logs).
- Final weights: w=(2296,−1504,0,−1968,176,−353,768,−792), b=72
  (`params/mt21_params.zag`, sha256 `34848abf39c7425e4227a5f4d56da36f6ea866a3ac4700b279f69e2f6d6651e7`).
- Policy binary sha256
  `3ef3fb40f5948e473bebdaa567c456c2d15943e969395776194699e37d44e100`
  (A/B byte-identical; binary itself NOT committed per §8).
