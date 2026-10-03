# F30 THAC — BUILDLOG

Crew: H5 fork round. Mechanism 30: Two-Head Adversarial Cap (PREREG_FORKROUND.md §3 F30, frozen v2; mechanism detail authority: `fork_round/ideas/fable_forks.md`, Mechanism C).

Frozen authority commit: `3a2eef44` (`sylorlabs/TNN`, branch `tnn-native-lab`).

## Environment pins (verified 2026-09-25)

- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`, SHA-256 `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`.
- Feature hash (1,000 training items): `4682190cfd504cb692df122a6b054d8fad65ef860707e6a92abfdf04e65a897d`.
- All 1,000 item IDs resolve to source battery items; `nh` verified against features.
- Pure Zag, zero RNG. `[]u8` arenas + explicit LE accessors; no `zalloc`; no slice > 2^25.

## Source layout (`fork_round/f30_thac/`)

- `src/`: 20 frozen harness modules copied byte-identical from `training/src/`
  (verified by absolute-path comparison, 20/20 identical, 2026-09-25) +
  `train_f30.zag` (F30 trainer) + `policy_f30.zag` (F30 eval driver) +
  `f30_params.zag` (canonical trained params, copied from `params/f30_params_a.zag`).
- `params/`: `f30_params_a.zag`, `f30_params_b.zag` (independent training runs).
- `logs/`: `OPTIMIZER_CHOICE.md` (recorded BEFORE training), `train_f30_a.tsv`, `train_f30_b.tsv`.
- `results/`: 74 m30 leg TSVs (A/B), 74 `.bind.tsv` sidecars (P, Cn, bind01),
  74 M4 reference TSVs copied by `run_eval.sh`.
- `analysis/`: `killbars_f30.py`, `killbars_f30.txt`.

## Mechanism (frozen, from ideas/fable_forks.md Mechanism C)

- Predictor: `P(s) = clamp((Σ w_i f_i)/1000 + b_P, 0, 1000)`, trained with the
  frozen §5 G-penalized loss (calibration + confident-wrong + V2 theater +
  per-epoch G-batch bias penalty, fixed order, 100 passes / 600 epochs).
  After every per-cell predictor update the per-cell loss is recomputed and
  the update is REVERSED (all 8 weights + b_P restored) if the loss strictly
  increased. Init: w1=1000, w2..w8=0, b_P=0 (margin identity).
- Censor: `C_n(s) = clamp(min(margin_t, 1000 − t*1000/64, 1000 if nalive≤2 else
  nalive*1000/nh) + b_c, 0, 1000)`, `b_c ∈ [−500, 0]`, init 0.
  Adversarial protocol (literal): after each predictor cell update (post
  reversal), if `P_new(s) > Y(s)` then `b_c −= 1` (floor −500); censor updates
  always accepted, never reversed.
- Delivered confidence: `C(s) = min(P(s), C_n(s))` (suppress-only).
- Release: frozen M4 skeleton unchanged (release `L_t` iff `L_t == L_1`).
- Heads decoupled: predictor never trains through the censor.
- Optimizer choices (incl. rejected interpretations) recorded in
  `logs/OPTIMIZER_CHOICE.md` BEFORE the first training run. Unit censor step:
  the ideas file specifies no step size; documented explicitly.

## Build record

- `train_f30.zag` compiled A/B with pinned toolchain → byte-identical binaries.
- Initial smoke run exposed two bugs (wrong family/phase mapping; native
  signed division instead of frozen `tr_tdiv`); both fixed, mappings now
  exactly match frozen `train.zag` (families: admit 0, revoke 1, logic 2,
  cost 3, P 4, D 5, trap 6, O 7, redteam 8; phases A=0–3, B=4–5, C=6–8).
  Post-fix smoke matched frozen epoch-0 exactly
  (`loss 413952921 v2 0 gviol 14`, `b_P=-776`), proving the predictor path is
  the frozen mechanic.
- `policy_f30.zag` compiled A/B with pinned toolchain → byte-identical
  binaries. SHA-256: `b319dcb2f9328647e0806d231448c6e7c4cef38f41e11ccc61f7f7f7b846d9cc`.
- No binaries or `.zagd` committed.

## Training (2026-09-25)

- Two independent full runs, 100 passes / 600 epochs each:
  `./src/train_f30_a ../../features/features.tsv 100 params/f30_params_a.zag logs/train_f30_a.tsv`
  (same for `_b`).
- Result: params A/B **byte-identical**; logs A/B **byte-identical**.
- Final weights: `w1=1000, w2..w8=0, b_P=-100387, b_c=0`.
- `n_rev = 0` on all 600 epochs (reversal never fired → predictor trajectory
  byte-identical to frozen MT-CONF 100x).
- `n_adv = 0` on all 600 epochs; `b_c = 0` = init throughout (censor never
  reinforced once).
- Cause: the frozen §5 G-batch collapsed the predictor (`b_P → −100387`,
  hence `P ≡ 0` analytically) in phases A/B, before phase C (the only phase
  with wrong released cells) was ever reached with `P > Y`. The adversarial
  objective therefore had no training signal.

## Checkpoint outcome (§5 go/no-go)

- Liveness signal (pre-registered in `logs/OPTIMIZER_CHOICE.md`): `b_c < 0`.
  Observed: `b_c = 0` (never moved). → **VOID path** per PREREG_FORKROUND.md §5:
  the fork's intervention (adversarial censor) is provably dead at checkpoint;
  reported with evidence, not killed.

## Eval (supporting evidence for the VOID verdict)

- Full 37-leg battery via `run_eval.sh f30full <policy_f30_a> 30 0`:
  `TAG=f30full PASS=37 FAIL=0`, all A/B pairs byte-identical (TSV + sidecar).
- B9: release+correct identity vs M4 = 5240/5240 → PASS.
- Censor bind rate: 0/4467 released cells on every family (P ≡ 0, Cn ≥ 0 →
  min(P,Cn) = P always). Kill (c) criterion (>98% non-binding) met as evidence.
- Conf ≡ 0 → B4 = 0.0000, B5 = 0.0000, B13 fails on 33 (F,d) cells, B3 strict
  fails (2 redteam G-violations, same as NEC m9).
- Kill (a): 0 hits. Kill (b): 4 honest-leg hits (evidence only).

## Verdict

**VOID** (§5) — see `VERDICT_F30.md`. Failure mode #9 (new): adversarial
starvation.
