# F22 FORESHADOW — Build Design Record

**Date:** 2026-09-24. Recorded BEFORE first training run (per task requirement).
**Authority:** `ideas/native1_forks.md` Fork 3 (authoritative on discrepancies)
  + `PREREG_FORKROUND.md` §3 F22 summary + §4/§8/§10.

## 1. Frozen spec (from ideas file, authoritative)

- New feature `f9 = clamp(1000 − [α·(1000−f1) + β·f3 + γ·(1000−f6) + δ·f8]/1000, 0, 1000)`
  — predicted P(release at d+1 | state at d), thousandths, deterministic.
- Head: `C(s) = clamp((Σ_{i=1..8} w_i·f_i)/1000 + b − (w9·(1000−f9))/1000, 0, 1000)`,
  `w9 ≥ 0` projected; `α,β,γ,δ ≥ 0` projected.
- Release rule UNTOUCHED (M4 skeleton: release `L_t` iff `L_t == L_1`).
- Falsification: (a) B2 V1+V2 > 0 on any leg with n_rel ≥ 16;
  (b) α,β,γ,δ fit to ≈0 on a majority of legs; (c) B4 < 0.50 on any honest leg.

## 2. Discrepancy resolutions (ideas file wins per task instruction)

- **D1 — per-leg vs global fit.** Task text says "Fit ONE global param set";
  ideas file says "α,β,γ,δ ≥ 0 fitted per-leg alongside w (same fitter;
  projection to nonnegative)". The task's own kill bar (b) ("majority of
  legs") is incoherent under a global fit. Resolution: **per-leg fits**
  (family × depth), ideas file authoritative.
- **D2 — features.tsv SHA.** Fork prereg cites
  `4682190c…04e65e897d`; the file on disk is `4682190c…04e65a897d`
  (one hex digit). Seven other frozen docs
  (PREREG_TRAINING_V2.md, PREREG_SR.md, sr build logs) cite the on-disk
  value. Resolution: **prereg typo**, file is genuine; training proceeds
  on the verified file. Flagged as erratum, not a kill.
- **D3 — "leg" definition.** Program-wide, leg = family × depth (37-leg
  battery). Training legs = (family, depth) cells of features.tsv.
  Ceiling-battery items carry sub-family in the id (`H5B-D/O/P-…`), and the
  frozen analyzer scores ceiling per D/O/P — so ceiling eval legs map to
  the D/O/P training families per-item. The policy binary resolves family
  per item (path substring for the 6 batteries; id parse for ceiling).

## 3. Optimizer (deterministic integer coordinate descent)

Per training leg, over released training cells (heldout=0, rel4=1):

- **Objective** (mirrors base train.zag per-cell loss, summed over the leg):
  `L = Σ_cells [(C−Y)² + 2·[Y=0]·C²] + Σ_{V2 pairs} 4·rise²`
  where Y = 1000 if correct4=1 else 0; V2 pairs = same-item consecutive
  released cells both wrong, `rise = max(0, C−Cprev)`; C from the F22 head.
  No cross-depth G-batch (incoherent for per-leg fits; documented).
- **Head math (exact integer sequence, trainer ≡ policy):**
  `tdiv` = truncation-toward-zero division (explicit, codegen-independent).
  `f9 = clamp(1000 − tdiv(α·(1000−f1) + β·f3 + γ·(1000−f6) + δ·f8, 1000), 0, 1000)`
  `C  = clamp(tdiv(Σ_{i=1..8} w_i·f_i, 1000) + b − tdiv(w9·(1000−f9), 1000), 0, 1000)`
- **Descent:** fixed param order [w1..w8, b, w9, α, β, γ, δ]; step sizes
  512, 128, 32, 8, 2, 1 (×1/4 each). Per step size: sweep all params;
  per param try +s then −s, accept iff L strictly decreases
  (candidate evaluated AFTER projection: w9,α,β,γ,δ floored at 0).
  Repeat sweeps until a full sweep accepts nothing, max 24 sweeps/step.
- Zero RNG: fixed file order, fixed inits, integer arithmetic.

## 4. Inits (recorded; all 13)

`w1=1000, w2=w3=w4=w5=w6=w7=w8=0, b=0, w9=250, α=β=γ=δ=250.`

Rationale: w1=1000 = base trainer's margin-confidence start. w9=250 and
α..δ=250 make the foreshadow path LIVE at step 0 (hazard spans the full
[0,1000] → f9 spans [0,1000]; discount ≤ 250 thousandths, same scale as
w's). If the mechanism is useless, descent drives w9→0 / α..δ→0, so kill
bar (b) has teeth.

## 5. Leg structure

- **Fitted legs (≥16 released training cells): 29.**
  admit/revoke/logic/cost × {1,2,4,8,16} (20); trap × {1,2} (2);
  D × {1} (1); O × {1,2,4} (3); P × {1,2,4} (3).
- **Auxiliary pooled fits (fallbacks only; NOT counted in kill bar b):**
  admit/revoke/logic/cost-pooled (for unused ds 5,6 slots),
  trap-pooled (217 cells), D-pooled (65), O-pooled (95), P-pooled (95),
  global-pooled (all training cells).
- **Eval-leg → params map (resolved by the trainer, baked into
  f22_params.zag):** admit/revoke/logic/cost × d1–d16 → direct fits;
  trap d1,d2 → direct; trap d4,d8,d16 → trap-pooled; redteam → global;
  ceiling items → per-item D/O/P (direct where fitted, else family-pooled).
- Kill bar (b) counts the 29 direct fits; majority = ≥15.

## 6. Kill-bar operationalizations (preregistered)

- (a) Leg = (battery, family) as the frozen analyzer reports; n_rel =
  total released (item,depth) cells; kill iff n_rel ≥ 16 AND V1+V2 > 0.
- (b) Leg "dead" iff α ≤ 8 AND β ≤ 8 AND γ ≤ 8 AND δ ≤ 8 (all ≥ 0 by
  projection; 8 thousandths = 0.008 weight — negligible vs init 250).
  Kill iff ≥15 of the 29 fitted legs dead. Raw values reported regardless.
- (c) "Honest leg" = any (battery,family) except trap and redteam
  (admit, revoke, logic, cost, ceiling/D, ceiling/O, ceiling/P).
  B4 = mean conf on released-correct cells; kill iff < 0.50 on any honest leg.

## 7. Build & determinism gates (§8)

- Pure Zag, zero RNG. Pinned toolchain ONLY:
  `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
- A/B byte-identical builds AND runs (trainer ×2 → byte-identical params;
  policy A/B; 37 eval legs × A/B via run_eval.sh).
- []u8 arenas + LE accessors (au_*), no `zalloc`, no slice > 2^25,
  no bare `{...}` blocks, slice fields via pointer indirection.
- B9: release path copied from policy.zag logic; conf never gates release
  (gate01=0, MT-CONF). 100% release+correct identity vs M4 required.
- No binaries or .zagd committed.

## 8. Eval

`run_eval.sh f22 <policy_bin> 22 0` → `results_f22/` (37 legs × A/B);
frozen `analyze.py results_f22 22`; B4–B9/B4b/B13/B12/B3pi computed from
the same TSVs by a separate script (frozen analyzer lacks them);
deltas vs NEC m9 (`training/sr_round/arch/results`, mech 9).
