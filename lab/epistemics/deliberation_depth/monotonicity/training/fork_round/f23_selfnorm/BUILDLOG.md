# F23 SELFNORM — Build Log

Fork 23, "Self-Normalized Margin Head" (mech 23). Frozen authority:
PREREG_FORKROUND.md §3 (F23) + ideas/native1_forks.md Fork 4 (authoritative
on discrepancy). Pinned toolchain:
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.

## 0. PREREG ERRATUM (found 2026-09-24, before any build)

PREREG_FORKROUND.md §2 pins training features SHA256
`4682190cfd504cb692df122a6b054d8fad65ef860707e6a92abfdf04e65e897d`.
The on-disk `training/features/features.tsv` hashes to
`4682190cfd504cb692df122a6b054d8fad65ef860707e6a92abfdf04e65a897d`
(single hex char differs at position 59: `e` vs `a`). The on-disk value
matches TWO older frozen preregs verbatim (`v2/PREREG_TRAINING_V2.md:273`,
`sr_round/PREREG_SR.md:58`), and the file predates the freeze (produced by
frozen `run_features.sh`). The frozen commit 0566cc81's copy of
PREREG_FORKROUND.md also carries `...e897d` (verified via GitHub API), so
this is a transcription typo IN the frozen doc, not working-tree drift.
Training proceeds on the on-disk frozen file (the value two frozen preregs
agree on). This erratum is reported, not silently fixed — the frozen doc
needs a version-bumped correction by the coordinator.

## 1. Mechanism (frozen spec, operationalized)

- Features f1..f8 = §4 features, computed by the FROZEN harness
  (`pl_features` clone of policy.zag; harness modules copied byte-identical,
  SHA-verified above).
- Trailing maxima are CROSS-DEPTH (cross-leg), per the prereg §2 batch-driver
  provision and the task brief: at eval leg depth d, for each item,
  M1(d) = max f1 over that item's legs at depths ≤ d (inclusive),
  M4a(d) = max |f4| over the same. "Fit on frozen features.tsv" is only
  possible under this reading (features.tsv carries one f1 per
  (item, depth); within-run margins are not in the frozen file).
- f1' = min(1000, 1000·f1 / max(64, M1))  [f1 ≥ 0 so truncation is exact]
- f4' = clamp(trunc_toward_zero(1000·f4 / max(64, M4a)), −1000, 1000)
- Head: C = clamp((w1·f1' + w2·f2 + w3·f3 + w4·f4' + w5·f5 + w6·f6 + w7·f7
  + w8·f8)/1000 + b, 0, 1000). M4 release skeleton untouched (B9 gate).
- Eval: NEC-style BATCH driver (one binary, frozen ordered leg list, all 37
  TSVs per run, per-item (M1,M4a) state in memory). A/B = two runs,
  byte-compared. No gate (gate01 N/A; F23 = conf head only).

## 2. Optimizer + inits (RECORDED BEFORE FIRST TRAINING RUN)

- **Algorithm:** deterministic full-batch integer coordinate descent.
- **Objective** (training cells = heldout==0 && rel4==1, n=4222):
  L(w,b) = Σ_cells [ (C−Y)² + 2·[Y=0]·C² + 4·rise·(C−Cprev)² ],
  C = clamp((Σ w_i·f_i')/1000 + b, 0, 1000), Y = 1000·y,
  rise = max(0, C−Cprev) iff y==0 and a previous released same-item cell
  exists with y_prev==0 (prev = nearest previous same-id released cell in
  file/depth order), else 0.
  This is the BASE trainer's loss (train.zag) on transformed features.
- **No G-batch term.** Rationale (recorded pre-run): the base trainer's
  G-batch was the one-way downward ratchet that degenerated MT-CONF to
  conf≡0 (VERDICT_TRAINING.md Layer-2 analysis); the per-cell gradient never
  fires under DIV=4000000. F23's theory needs a genuinely fitted head, so
  the objective is pure calibration + theater penalty, optimized by exact
  coordinate descent where every step's L-delta is evaluated honestly.
- **Inits:** w = (1000,0,0,0,0,0,0,0), b = 0 (margin head, as base init).
- **Schedule:** step sizes ±64, ±16, ±4, ±1; coordinate order w1..w8, b;
  sweep a step size until no single-coordinate ±step improves L (integer
  strict improvement); max 50 sweeps per step size. Zero RNG. Fixed file
  order. All integer arithmetic (truncation-toward-zero division).
- **Transform pre-pass:** one depth-ordered pass per item over training
  cells (id→slot map, NOT relying on contiguity): M1=max(M1,f1),
  M4a=max(M4a,|f4|), then f1', f4' as above. Stored per cell.
- **Artifacts:** `params/f23_params_A.zag`, `params/f23_params_B.zag`
  (two training runs → must be byte-identical), `logs/train_A.tsv`,
  `logs/train_B.tsv` (sweep, step, L, w1..w8, b per sweep).

## 3. Pre-registered empirical probe (data property, not a design choice)

On frozen features.tsv (4222 released training cells, 940 items):
- f1 is monotonically non-decreasing across depth legs for 939/940 items;
  f1 ≥ 100 everywhere (64-floor never binds for f1).
- Under the frozen cross-leg inclusive trailing max, **f1' == 1000 on
  4221/4222 cells (99.98%)** — the f1' feature is empirically constant.
  (Within-run margins also never dip: f8>0 on 1/4222 cells, so the
  alternative within-run reading agrees.)
- |f4| non-monotonic for 115/940 items → f4' carries sign/scale variation.
- Ceiling eval items == ceiling training items (120/120 id overlap); all
  1000 eval ids globally unique across the 7 batteries.

Consequence: the transform destroys the absolute-margin signal on this
data (f1' carries ~zero variance). The build proceeds FAITHFULLY anyway —
the prereg's kill criteria are empirical. Kill-bar interpretations
(recorded pre-run):
- (a) clamp attractors: fires iff any eval leg has >50% released cells at
  conf ≡ 0 or ≡ 1000.
- (b) theater rises vs baseline: baseline = M4 (the non-degenerate
  reference head; V1+V2 = 0+160). MT-CONF-100x (V=0) is degenerate
  (conf≡0 → trivially zero theater), so "rises vs MT-CONF" would kill any
  non-degenerate fork by construction — documented as a degenerate reading.
  (b) fires iff F23 V1+V2 > 160. NEC m9 (0/0) reported as CTL yardstick.
- (c) w1 on f1' ≈ 0: adjudicated on (i) fitted w1 value AND (ii) f1'
  constancy on train + eval legs. If f1' is constant on ~all cells, w1 is
  unidentifiable from b (perfect collinearity) and the margin signal is
  destroyed regardless of w1's numeric value → (c) fires on the
  constancy evidence.

## 4. Determinism gates (§8)

Pure Zag, zero RNG. Pinned toolchain only. A/B byte-identical builds and
runs. Training ×2 → byte-identical params. B9 100% identity vs M4 required
(release rule untouched). []u8 arenas + LE accessors (au_get64/au_put64
from frozen dlb_util.zag). No fn named zalloc. No slice > 2^25 bytes.
No binaries or .zagd committed (params .zag + logs + TSVs only).

## 5. Run ledger

| step | artifact | status |
|---|---|---|
| harness copy | src/*.zag (7 files) | SHA-verified byte-identical |
| leg list | leglist.tsv (37 rows, frozen order) | DONE (sha256 b45f24d9…) |
| trainer | src/f23_train.zag | DONE (see §6 for bug history) |
| train A/B | params/f23_params_{A,B}.zag | DONE — byte-identical (sha256 17616e39…) |
| batch driver | src/f23_batch.zag | TODO |
| eval A/B | results_f23/*_m23_d*_{A,B}.tsv (74 files) | TODO |
| analysis | analysis/killbars.md | TODO |

## 6. Trainer bug history (all found and fixed before any committed training run)

Three bugs were caught by differential testing against an independent
Python reference (transform + loss + coordinate-descent landscape):

1. **TSV column off-by-one.** Feature fields were read from
   `tabs[7+k]..tabs[8+k]` instead of `tabs[6+k]..tabs[7+k]`, shifting every
   feature by one column (f1 read f2's value, etc.). Caught because the
   transform audit dump mismatched Python 5240/5240.

2. **rel4/correct4 column confusion.** `rel4` was parsed from col 6
   (correct4) and `correct4` from col 7 (f1), due to using `tabs[5]/tabs[6]`
   instead of `tabs[4]/tabs[5]`. This mislabeled y and the released set.
   Caught by per-cell loss decomposition (cell 0 showed y=0, should be y=1).

3. **M1/M4a update lost its `rel4==1` guard** during edits, updating
   trailing maxima on unreleased cells. Caught by transform audit
   (761/5240 mismatches, e.g. TRAP-A1-001 depth 4).

4. **Accept/revert logic bug (critical).** The coordinate descent used two
   sequential `if`s:
   `if(Ln<Lcur){Lcur=Ln;improved=1;} if(Ln>=Lcur){revert;}`
   After an accept, `Ln>=Lcur` is true by equality, so every accepted move
   was immediately reverted. The optimizer appeared "stuck at init" while
   the log showed improving L values. Fixed to if/else. Caught by tracing
   accepts vs final weights.

After fixes: transform 0/5240 mismatches vs Python; loss matches Python
exactly (1026562500 at init, 1026000000 at optimum); Python confirms 0
improving single moves at the Zag optimum (local optimum verified).

## 7. Training result (A/B byte-identical)

- Binary SHA (3 builds): `8ebde0ea323a3fb5b893fb7c0b000c060e5f70e65e3f14540b63a4d40400841b`
- Params A/B SHA: `17616e3984ed1e362c7bf2e98595f1a101e6f69d216e4669dd4e5b0b493c6e46`
- Logs A/B SHA: `50c25fa424d602e773d74d28b8a116285327af9021b0fe2f4c311b4b6392db98`
- Transform A/B SHA: `194e7328aca78828bcb26ba8b27a27bc51771a12ae01e29dc020ad9f8383351d`
- Final: w = (1256, 256, 0, 0, 256, 256, 0, 192), b = 192, L = 1026000000.
  (Init L = 1026562500; 5 sweeps at step 64, then converged; steps 16/4/1
  no-ops.)
- Note: w1=1256 (not ≈0) but f1'≡1000 on 4221/4222 train cells, so w1 is
  collinear with b; the margin signal is destroyed per §3 kill-bar (c)
  interpretation (constancy evidence). The numeric w1 is an artifact of the
  collinearity, not a live margin signal.

## 8. Batch eval driver (2026-09-25)

- Implemented `src/f23_batch.zag`: one invocation over `leglist.tsv` (37 legs
  in frozen order), per-item (M1,M4a) trailing-max retained across depth legs,
  frozen M4 harness (dlb_run) + pl_features (copied from training/src/policy.zag),
  F23 head on (f1',f4'), M4 release/correct/cert skeleton preserved exactly.
- Compiled with pinned toolchain; binary tested on 1 leg then full 37-leg A/B.
- Full battery: 37 legs A + 37 legs B, all 74 files byte-identical A/B.
- Output: `results_f23/<battery>_m23_d<depth>_<AB>.tsv` (analyzer-compatible 11-col).
- M4 reference TSVs copied from `mechanisms/results/` for B9 comparison.

## 9. Eval results (2026-09-25)

- Frozen analyzer: F23 V1=0, V2=0, Gviol=2 (redteam). M4: V1=0, V2=160, Gviol=14.
- B9: 5240/5240 release+correct identity vs M4 (PASS).
- Clamp attractor: 35/37 legs at 100% conf=1000 on released cells.
- B-metrics: B1 PASS, B2 PASS, B3 FAIL (redteam Gviol=2), B4 PASS (1.000),
  B4b PASS, B5 FAIL (0.000 separation), B6 PASS, B7 PASS (0.148),
  B8 FAIL (ceiling/P G≡+1.000 fails nonvacuity; trap VOID), B9 PASS,
  B12 recorded, B13 PASS, B3pi recorded.
- NEC m9 deltas: V1 Δ0, V2 Δ0, Gviol Δ−4.

## 10. Verdict: KILLED

- Fork bar (a) FIRES: 35/37 legs at 100% conf=1000 (clamp attractor).
- Fork bar (b) does NOT fire: F23 V1+V2=0 ≤ 160.
- Fork bar (c) FIRES: f1'≡1000 on 99.98% cells; w1=1256 unidentifiable
  from bias; absolute margin signal destroyed.
- Additionally fails B3 (strict), B5, B8 (ceiling/P).
- Failure mode FM-SELFNORM-001: self-normalization by trailing max destroys
  the absolute f1 margin signal; fitted head saturates at conf=1000 clamp.
- Confirms H5 hypothesis: absolute f1 margin is load-bearing for calibration.
- Prereg SHA erratum: feature-SHA transcription (one hex digit); extant frozen
  file used, reported in analysis/killbars.md.
