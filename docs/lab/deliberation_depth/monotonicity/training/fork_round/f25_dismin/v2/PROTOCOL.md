# F25 DISMIN v2 — Training & Build Protocol

**Recorded BEFORE the first v2 training run** (prereg §5 / task requirement).
Fork dir: `deliberation_depth/monotonicity/training/fork_round/f25_dismin/v2/`
(`v2/src`, `v2/params`, `v2/logs`, `v2/results`, `v2/analysis`).
v1 evidence in `f25_dismin/` (PROTOCOL.md, VERDICT_F25.md, v1 logs) is
UNTOUCHED by this run.
Authority: `PREREG_FORKROUND.md` FROZEN v2 (commit `3a2eef44`) §3 (F25) +
**§5b repaired TRAIN-COORD v2** + `ideas/native2_forks.md` FORK 2 (the ideas
file is authoritative on mechanism detail; v2 §5b overrides the trainer's
veto application).

## 0. Frozen inputs (verified)

- Training cells: `training/features/features.tsv`.
  - Local SHA-256: `4682190cfd504cb692df122a6b054d8fad65ef860707e6a92abfdf04e65a897d`
    (verified by sha256sum before writing this protocol — matches the v2
    prereg's corrected hash; the v1 one-char typo is fixed in v2).
- Toolchain (pinned, ONLY): `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
- Harness modules copied byte-identical (SHA-verified) into `v2/src/`:
  `R33_NATIVE_SHA256_V2.zag`, `R33_NATIVE_IO_V1.zag`, `dlb_util.zag`,
  `dlb_json.zag`, `dlb_cfg.zag`, `dlb_ledger.zag`, `dlb_delib.zag`.

## 1. Mechanism (frozen spec, unchanged)

```
A(s) = clamp((a_1·f_1 + a_2·f_2 + a_3·f_3 + a_4·f_4)/1000 + a_0, 0, 1000)
B(s) = clamp((b_1·f_5 + b_2·f_6 + b_3·f_7 + b_4·f_8)/1000 + b_0, 0, 1000)
C(s) = min(A(s), B(s))            (after Δ shift: a_0,b_0 each += Δ)
```

Feature semantics (frozen `feat.zag` / v1 PROTOCOL §1): f1 = clamped margin
@t; f2 = t·1000/64; f3 = leader-changed flag (0/1000); f4 = margin delta vs
t−1 (clamped ±1000); f5 = consumed/ne·1000; f6 = nalive/nh·1000;
f7 = sole-survivor flag (0/1000); f8 = max margin drop along path. All
integer thousandths.

## 2. Inits (recorded)

**All ten parameters start at 0**: a_0=a_1=a_2=a_3=a_4=0, b_0=b_1=b_2=b_3=b_4=0.
No RNG anywhere. Fixed file order. Integer arithmetic throughout
(truncation-toward-zero division for possibly-negative numerators).

## 3. TRAIN-COORD v2 (prereg §5b, implemented literally)

Per head (A on f1..f4, B on f5..f8), independently:

- **Training cells**: rows with `heldout=0` AND `rel4=1` (expect 4222, as v1).
  Correctness y: `correct4="1"` → Y=1000, else Y=0.
- **Objective**: L = Σ_cells (C − Y)², i64 sum (C,Y in thousandths).
- **Accept rule (CHANGED vs v1)**: candidates accepted on **strict L-reduction
  alone** (`o2 < best`). No vetoes on candidates. Veto statistics are still
  LOGGED per candidate (evidence) but do not gate acceptance.
- **Step sequence (recorded interpretation of "±50, then ±8, then ±1
  refine")**: per sweep, per param in fixed order [bias, w1..w4]: for each
  step size s in [50, 8, 1]: try **+s first, then −s**; each try only if it
  stays inside the box; the **first strict L-reduction is accepted**
  (incumbent updated immediately; if +s accepted, −s is skipped); then the
  next step size. Then the next param.
- **Boxes (recorded choice, same as v1)**: weights ∈ [−1000,1000]
  (ideas ground rules); bias a_0/b_0 ∈ [−1000,1000].
- **Sweeps**: 8 max, full sweeps, deterministic (no early stop; log shows all).
- **Vetoes on the FINAL head only** (computed after the 8 sweeps; a head
  violating ANY veto is **VOID**, reported with evidence):
  - **V1 (theater)**: chain each training cell to the nearest previous
    same-id training cell (rel4=1, heldout=0). For pair (prev p, cur i):
    V1 if y_p=1, y_i=0 and C_i ≥ C_p; V2 if y_p=0, y_i=0 and C_i > C_p.
    Veto iff V1+V2 > 0 over training cells.
  - **V2 (B4 guard)**: training meanConfCorrect = (Σ C over released correct
    training cells)/(1000 · n_correct) < 0.55 → VOID.
    (Integer form: reject iff ΣC·1000 < 550·n_correct... precisely: VOID iff
    NOT (n_correct > 0 AND ΣC ≥ 550·n_correct).)
  - **V3 (B13 guard)**: any training (family,depth) slot with n_rel ≥ 8 and
    G = (ΣC − 1000·Σy)/n < −80 (thousandths, i.e. G < −0.080) → VOID.
    Families indexed: admit=0, revoke=1, logic=2, cost=3, trap=4, redteam=5,
    P=6, D=7, O=8; depth slots 1,2,4,8,16,32,64.

## 4. Δ bias-shift grid (after TRAIN-COORD)

- Δ ∈ {0, 50, 100, …, 500}, scanned **ascending**.
- Candidate: a_0' = a_0+Δ, b_0' = b_0+Δ; C_Δ(s) = min(A_Δ(s), B_Δ(s)) where
  the Δ is added to the biases **inside the clamp** (ideas file: "added to
  both a_0 and b_0"; this corrects v1's post-clamp addition, which differed
  on cells with negative unclamped head values).
- Score: Σ C_Δ over correct training cells ("training B4 margin" ≡
  score/(1000·n_correct) − 0.50; maximizing the margin ≡ maximizing the score).
- Veto: V3 recomputed under C_Δ (same formula as §3); Δ rejected if any
  training (family,depth) slot with n_rel ≥ 8 has G < −80 thousandths.
  (Only V3 gates the grid — per the ideas file and §5b's "F24's stage-2 w9
  grid keeps its per-candidate V3 veto"; the grid starts from nonzero fitted
  heads, so it is not locked.)
- Selection: strictly-greater score wins; **ties → smaller Δ**.
  (If all Δ are V3-rejected: Δ*=0, score=−1 — recorded, nothing taken.)
- Final params: a_0+Δ*, b_0+Δ* (Δ* recorded in params file + log). Final
  biases may exceed the [−1000,1000] training box — that is the point of the
  shift (compensating min's structural pessimism); recorded, not a violation.

## 5. Checkpoint rule (prereg §5 + §5b)

Training checkpoint: **weights ≠ init** AND the fork's liveness signal —
F25's is the **veto rate** (fraction of training released cells with
min(A,B) < max(A,B) − 50, measured with FINAL shifted heads) strictly above 0
AND **both heads pass the final vetoes** (a VOID head → the fork is VOID:
the DISMIN intervention — min of two *fitted* heads — cannot be honestly
instantiated). Provably dead at checkpoint → **VOID** (reported with
evidence, not killed, no eval spend).

## 6. Pre-registered prediction (not a conclusion)

Under v2 the trainer can move: the V2-as-search-gate lock is gone, so
coordinate descent on strict L-reduction from the zero init should fit both
heads to the training cells (expect nonzero weights, bias terms tracking
base rates). Whether the FINAL heads pass V1–V3 is the open question:
- V2 (meanConfCorrect ≥ 0.55): the squared-error objective on a ~50/50-ish
  label mix should push correct-cell confidence up; likely pass, but the
  min-pessimism is not yet in play at head level (each head is fitted alone).
- V1 (theater): the objective does not penalize conf rises on wrong→wrong
  chains directly; the final veto may bite.
- V3 (G ≥ −0.080 per slot): squared-error fitting tends to calibrate, but
  sparse slots could dip; the Δ grid's V3 gate then guards the shift.
The training log (§7) is the evidence either way. If both heads pass and
the veto rate is live, the fork proceeds to the 37-leg battery.

## 7. Build & determinism gates (per task / prereg §8)

- Pure Zag, zero RNG. Pinned toolchain only.
- Trainer binary built **twice** → byte-identical SHA required.
- Training run **twice** → byte-identical params + logs required.
- All tables on []u8 arenas with LE accessors (ZNC-2026-09-21-007); no
  function named `zalloc`; no slice > 2^25 bytes; slice fields via pointer
  indirection only; no bare `{...}` blocks.
- No binaries or `.zagd` committed (per AGENTS.md: filter build binaries
  and `.zag-cache` out of commit walks).
- Commits via `~/workspace/commit_racefree.py` with `TMPDIR=~/workspace/tmp_commit`,
  incremental, to branch `tnn-native-lab`; repo path prefix `docs/lab/`
  (pass lab-relative paths NOT starting with docs/lab/).

## 8. If the checkpoint passes

- Emit `v2/params/f25_params.zag` (final shifted params; generated by the
  trainer — never hand-edited).
- Emit training-cells dump `v2/logs/train_cells.tsv`
  (id, family, depth, y, A, B, C with final heads) for the per-head-vs-min
  B8-on-training analysis.
- Build `v2/src/f25_policy.zag`: frozen M4 release skeleton + deliberation
  (adapted from frozen `training/src/policy.zag`), conf = min(A,B) with final
  params baked in; per-leg driver `<polbin> <items> <depth> <gate> <out.tsv>`
  with the frozen TSV columns + a `.ab` sidecar per leg
  (id, depth, t, released, f1..f8, A, B) for the eval veto-rate measurement.
  Build twice byte-identical.
- Run the 37-leg battery (`run_eval.sh f25v2 <bin> 25 0`; gate=0 = conf head
  only, same as the training MT-CONF convention), verify A/B byte-identical
  per leg, move TSVs + M4 reference copies into `v2/results/`.
- Analyze with frozen `training/analyze.py` (`analyze.py v2/results 25 4`);
  custom analysis in `v2/analysis/` for: B4/B4b/B5/B6/B7 aggregates, amended
  B8, B12, B13, B3pi, eval veto rate, NEC-m9 deltas, per-head vs min B8 on
  training, falsification checks (a)/(b)/(c).
- Report B1–B9/B4b/B8/B13/B12/B3pi kill-bar table, §10 verdict, failure-mode
  number if killed.
