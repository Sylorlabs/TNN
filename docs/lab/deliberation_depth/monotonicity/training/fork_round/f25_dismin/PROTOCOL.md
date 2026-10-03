# F25 DISMIN — Training & Build Protocol

**Recorded BEFORE the first training run** (prereg §5 / task requirement).
Fork dir: `deliberation_depth/monotonicity/training/fork_round/f25_dismin/`.
Authority: `PREREG_FORKROUND.md` §3 (frozen v1) + `ideas/native2_forks.md` FORK 2
(the ideas file is authoritative on any discrepancy).

## 0. Frozen inputs (verified)

- Training cells: `training/features/features.tsv`.
  - Local SHA-256: `4682190cfd504cb692df122a6b054d8fad65ef860707e6a92abfdf04e65a897d`
  - GitHub `sylorlabs/TNN` @ `0566cc81`, path
    `docs/lab/deliberation_depth/monotonicity/training/features/features.tsv`,
    blob `89fa14ca265f6cdca2494cedb17faafe33bf38d7`: content SHA-256
    `4682190cfd504cb692df122a6b054d8fad65ef860707e6a92abfdf04e65a897d`
    — **byte-identical to local**. The prereg's recorded hash
    (`...4e65e897d`) has a **single-character transcription typo at hex
    index 59** (`e` should be `a`); the frozen-commit file is the truth.
- Toolchain (pinned, ONLY): `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
- Harness modules copied byte-identical (SHA-verified) into `src/`:
  `R33_NATIVE_SHA256_V2.zag`, `R33_NATIVE_IO_V1.zag`, `dlb_util.zag`,
  `dlb_json.zag`, `dlb_cfg.zag`, `dlb_ledger.zag`, `dlb_delib.zag`.

## 1. Mechanism (frozen spec)

```
A(s) = clamp((a_1·f_1 + a_2·f_2 + a_3·f_3 + a_4·f_4)/1000 + a_0, 0, 1000)
B(s) = clamp((b_1·f_5 + b_2·f_6 + b_3·f_7 + b_4·f_8)/1000 + b_0, 0, 1000)
C(s) = min(A(s), B(s))            (after Δ shift: a_0,b_0 each += Δ)
```

Feature semantics (frozen `feat.zag`): f1 = clamped margin @t; f2 = t·1000/64;
f3 = leader-changed flag (0/1000); f4 = margin delta vs t−1 (clamped ±1000);
f5 = consumed/ne·1000; f6 = nalive/nh·1000; f7 = sole-survivor flag (0/1000);
f8 = max margin drop along path. All integer thousandths.

## 2. Inits (recorded)

**All ten parameters start at 0**: a_0=a_1=a_2=a_3=a_4=0, b_0=b_1=b_2=b_3=b_4=0.
No RNG anywhere. Fixed file order. Integer arithmetic throughout
(truncation-toward-zero division for possibly-negative numerators, as in
frozen `train.zag`'s `tr_tdiv`).

## 3. TRAIN-COORD (shared trainer, implemented literally)

Per head (A on f1..f4, B on f5..f8), independently:

- **Training cells**: rows with `heldout=0` AND `rel4=1` (4222 cells).
  Correctness y: `correct4="1"` → Y=1000, else Y=0.
- **Objective**: Σ_cells (C − Y)², i64 sum (C,Y in thousandths).
- **Sweep order (fixed)**: param index 0 (bias a_0/b_0), then 1,2,3,4 (weights).
- **Candidate generation**: for each param, try **+50 first, then −50**,
  each only if it stays inside the box. **First strict improvement accepted**
  (objective strictly decreases AND all vetoes pass); then move to next param.
- **Boxes (recorded choice)**: weights ∈ [−1000,1000] (ideas ground rules);
  bias a_0/b_0 ∈ [−1000,1000] (same units as confidence; ideas file does not
  pin the bias box — this choice is recorded here).
- **Sweeps**: 8 max, full sweeps, deterministic. (Cheap enough to run all 8;
  no early stop — the log shows all sweeps.)
- **Hard vetoes on EVERY candidate** (reject = not accepted, incumbent keeps):
  - **V1 (theater)**: chain each training cell to the nearest previous
    same-id training cell (rel4=1, heldout=0). For pair (prev p, cur i):
    V1 if y_p=1, y_i=0 and C_i ≥ C_p; V2 if y_p=0, y_i=0 and C_i > C_p.
    Veto if V1+V2 > 0 over training cells.
  - **V2 (B4 guard)**: training meanConfCorrect = (Σ C over released correct
    training cells)/(1000 · n_correct) < 0.55 → reject.
  - **V3 (B13 guard)**: any training (family,depth) slot with n_rel ≥ 8 and
    G = (ΣC − 1000·Σy)/n < −80 (thousandths, i.e. G < −0.080) → reject.
    Families indexed: admit=0, revoke=1, logic=2, cost=3, trap=4, redteam=5,
    P=6, D=7, O=8.

## 4. Δ bias-shift grid (after TRAIN-COORD)

- Δ ∈ {0, 50, 100, …, 500}, scanned **ascending**.
- Candidate: a_0' = a_0+Δ, b_0' = b_0+Δ; C_Δ(s) = min(A_Δ(s), B_Δ(s)).
- Score: training meanConfCorrect under C_Δ ("B4 margin" ≡ score − 0.50;
  maximizing the margin ≡ maximizing the score).
- Veto: V3 recomputed under C_Δ (same formula as §3); Δ rejected if any
  training (family,depth) slot with n_rel ≥ 8 has G < −80 thousandths.
- Selection: strictly-greater score wins; **ties → smaller Δ**.
- Final params: a_0+Δ*, b_0+Δ* (Δ* recorded in params file).

## 5. Checkpoint rule (prereg §5)

Training checkpoint: **weights ≠ init** AND the fork's liveness signal —
F25's is the **veto rate** (fraction of training released cells with
min(A,B) < max(A,B) − 50) strictly above 0. If the intervention is provably
dead at checkpoint → **VOID** (reported with evidence, not killed, no eval
spend — same discipline as F26/F27's stillborn gates).

## 6. Pre-registered prediction (not a conclusion)

Under the literal §3 reading, TRAIN-COORD appears unable to leave the zero
init: any single ±50 step from 0 yields C(s) ≤ 50 on every cell (features
≤ 1000 in magnitude; |50·f/1000| ≤ 50), so training meanConfCorrect ≤ 0.05
< 0.55 and **every first-step candidate fails the V2 veto** (most also fail
V3, since G ≤ 0.05 − acc < −0.080 wherever slot accuracy > 0.13). The
incumbent can therefore never move; 8 sweeps accept nothing; params stay 0.
The training log (§7) will confirm or refute this empirically — the log is
the evidence either way. If confirmed, the fork is VOID at checkpoint per
§5, and the finding generalizes: the shared TRAIN-COORD's V2-as-search-gate
kills F24/F26/F27 identically (all use the same trainer from the same zero
init). No spec deviation will be made to "fix" it — the frozen spec is
implemented as written.

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
  incremental, to branch `tnn-native-lab`; repo path prefix `docs/lab/`.

## 8. If the checkpoint passes (not predicted)

Only then: emit `src/f25_params.zag`, build `src/f25_policy.zag` (M4 release
skeleton, C=min of shifted heads, per-item driver matching frozen
`policy.zag`'s TSV columns + `.ab` sidecar with per-cell A,B for the veto-rate
measurement), build twice byte-identical, run the 37-leg battery
(`run_eval.sh full <bin> 25 0`), analyze with frozen `analyze.py`, report
B1–B9/B4b/B8/B13/B12/B3pi deltas vs NEC m9, per-head vs min B8 on training,
veto rate, and the (a)/(b)/(c) falsification checks.
