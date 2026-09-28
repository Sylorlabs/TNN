# F26 EFFIC — Training & Build Protocol

**Recorded BEFORE the first build / training run** (prereg §5 / task requirement).
Fork dir: `deliberation_depth/monotonicity/training/fork_round/f26_effic/`.
Authority: `PREREG_FORKROUND.md` §3 (F26) + §5b (repaired TRAIN-COORD v2)
+ `ideas/native2_forks.md` FORK 3 (**the ideas file is authoritative on
mechanism detail**; v2 §5b governs the trainer).

## 0. Frozen inputs (verified)

- Training cells: `training/features/features.tsv`.
  - Local SHA-256: `4682190cfd504cb692df122a6b054d8fad65ef860707e6a92abfdf04e65a897d`
    (matches frozen v2 prereg §11(b); verified above before any build).
- Toolchain (pinned, ONLY): `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
- Harness modules copied byte-identical (SHA-verified) into `src/`:
  `R33_NATIVE_SHA256_V2.zag`, `R33_NATIVE_IO_V1.zag`, `dlb_util.zag`,
  `dlb_json.zag`, `dlb_cfg.zag`, `dlb_ledger.zag`, `dlb_delib.zag`
  (SHAs recorded in §7 of this file at copy time).

## 1. Mechanism (frozen spec, ideas file authoritative)

- `cumE` = cumulative evidence units examined along the item's path to depth d.
  The frozen harness logs per-depth evidence as f5 = consumed·1000/ne, and
  `st.consumed` is reset at each `dlb_run` and accumulates across rounds 1..d
  within the run (verified in `dlb_delib.zag`: `st.*.consumed=0` at run start,
  `st.*.consumed=e+1` per examined unit). Therefore the logged f5 column IS
  cumE in f5 units (thousandths of the item's evidence budget) — no cross-depth
  summation is needed or wanted (summing f5 over separate per-depth runs would
  double-count rounds). cumE(d) = f5(d), integer, monotone nondecreasing in d.
- `E_ref` = median `cumE` over the leg's released cells at depth d
  (ideas file: "deterministic; even-count ties take the lower median").
  At training: per (family, depth) over training released cells.
  At eval: per (battery-item-set, depth) leg over that leg's released cells
  (two-pass within the leg; no cross-depth state required).
- `q = (cumE·1000)/E_ref` (integer division), with deterministic guard
  `E_ref_safe = max(1, E_ref)` (no f5==0 cell exists in training; guard is
  for eval robustness; recorded here).
- `f9 = (f1·1000)/(1000 + q)` (integer division; f1 = clamped margin).
- Head (task's explicit formula, recorded choice §1b):
  `C(s) = clamp( (Σ_{i=1..8} w_i·f_i)/1000 + b + (w_9·f_9)/1000, 0, 1000 )`,
  truncation-toward-zero division (`td_tdiv`, as in frozen `train.zag`).

### §1b Recorded head-form choice

The ideas file's FORK 3 writes the head as
`clamp((Σ_{1..8} w_i·f_i + w_9·f_9)/1000 + b, 0, 1000)` (single division);
the task restates it as `(Σ_{1..8} w_i·f_i)/1000 + b + w_9·f_9/1000`
(two divisions). The ideas file's ground rules say "Every term is (w·f)/1000".
These differ by at most 1 thousandth on cells where the two partial sums have
opposite signs — immaterial to every bar. **Implemented: the task's form**
(separate `w_9·f_9/1000` term), with truncation-toward-zero division in both
trainer and policy binary (byte-identical arithmetic by construction).

### §1c w9 box

The ideas file box-constrains w9 ≥ 0 only for F20/F22/F27. F26's head ADDS
the w9 term and the spec expects w9 > 0 (the sign is fitted and recorded).
**w9 ∈ [−1000,1000] unconstrained in sign** (ideas ground-rules box).
Kill (b): |w9| ≤ 8 after full training → KILL (refine-scale: the trainer's
coarse ±50 step never fired; any residual is refine noise).

## 2. Stillborn gate (prereg §5; computed BEFORE any build)

Within-leg std(q) on training legs (heldout=0 cells; legs = (family,depth);
q from §1; released cells only; population std):

- 51 training legs; 16 with std(q) < 100 → **16/51 = 31.4%**.
- Gate: std(q)<100 on >50% of training legs → STILLBORN.
- **31.4% < 50% → LIVE. Proceed to training + eval.**
- Full per-leg table in `analysis/stillborn_f26.out` (this file's numbers
  reproduced from `training/features/features.tsv` before any build).
- Note: several legs have genuinely zero q-spread (cost d8/d16, logic d16,
  revoke d16, trap d4, D/O/P d32, redteam d8/d16: all released cells at
  cumE=1000=E_ref) — expected saturation, not a defect; the gate counts legs
  and the fork clears it.

## 3. Inits (recorded)

**All ten parameters start at 0**: b=w1=…=w9=0. No RNG anywhere. Fixed file
order. Integer arithmetic throughout.

## 4. TRAIN-COORD v2 (repaired, per prereg §5b — implemented literally)

- **Training cells**: rows with `heldout=0` AND `rel4=1`. Correctness y:
  `correct4="1"` → Y=1000, else Y=0.
- **Objective**: L = Σ_cells (C − Y)², i64 sum (C,Y in thousandths).
  Per-cell C uses that cell's (family,depth) E_ref (frozen, computed once).
- **Sweep order (fixed)**: [b, w1, w2, w3, w4, w5, w6, w7, w8, w9].
- **Candidate generation**: per param visit: try **+50 first, then −50**;
  accept on **strict L-reduction alone** (no vetoes during search — v2).
  On accepting a ±50 step: refine loop — repeat passes over {+8,−8} accepting
  strict improvements until a full pass accepts nothing (cap 200 passes);
  then the same with {+1,−1}. If no ±50 step accepted, no refine for that param.
- **Boxes (recorded)**: w1..w9 ∈ [−1000,1000] (ideas ground rules);
  b ∈ [−1000,1000] (same units as confidence; recorded choice, as F25).
  w9 sign unconstrained (§1c).
- **Sweeps**: 8 full sweeps, no early stop (log shows all 8).
- **Vetoes V1–V3 on the FINAL answer only** (§5b). Violation → VOID
  (reported with evidence, no eval):
  - **V1 (theater)**: chain each training cell to the nearest previous
    same-id training cell (rel4=1, heldout=0; file-order scan back).
    For pair (prev p, cur i): V1 if y_p=1, y_i=0 and C_i ≥ C_p;
    V2 if y_p=0, y_i=0 and C_i > C_p. Veto if V1+V2 > 0.
    (Frozen analyzer semantics: `f1>=f0` for V1, `f1>f0` for V2.)
  - **V2 (B4 guard)**: training meanConfCorrect < 0.55 → VOID.
  - **V3 (B13 guard)**: any training (family,depth) with n_rel ≥ 8 and
    G = (ΣC − 1000·Σy)/n < −80 thousandths → VOID.
    Families indexed: admit=0, revoke=1, logic=2, cost=3, trap=4, redteam=5,
    P=6, D=7, O=8.

## 5. Base control (for falsification (a))

The same trainer with a mode flag: mode=1 = base head
`C = clamp((Σ_{1..8} w_i·f_i)/1000 + b, 0, 1000)` — w9 frozen at 0 and
skipped in sweeps; f9 column ignored. Trained under identical TRAIN-COORD v2
on identical cells. Base vetoes computed and reported (not adjudicated).
Base policy evaluated as **mech 27** for the high-depth B3/B8 comparison.
Kill (a): F26's high-depth (d∈{8,16} + ceiling d∈{16,32,64}) B3 violations
and B8 G-flatness **no better than base** despite the live q signal (§2)
→ KILL (failure mode: efficiency doesn't predict correctness).

## 6. Checkpoint rule (prereg §5)

Training checkpoint: **weights ≠ init** AND final-answer vetoes V1–V3 clear.
The fork's liveness signal is the stillborn gate (§2: LIVE). If the fitted
head violates any veto → **VOID** (reported with evidence, not killed, no
eval spend). Kill (b) w9 check (§1c) and kill (c) B4<0.50-honest apply at the
bar table.

## 7. Build & determinism gates (per task / prereg §8)

- Pure Zag, zero RNG. Pinned toolchain only.
- Harness copy SHAs (verified at copy, 2026-09-24):
  - R33_NATIVE_SHA256_V2.zag `9824f6db66a943917dbc7cd5e6862ab0967b7ea83161cfc357bb7d17ca683bcf`
  - R33_NATIVE_IO_V1.zag `e6379ddb0b05d95b5ba2e8454ef8cc6bc74d075c379296641e9f61d8`
  - dlb_util.zag `40ecdcec16de68d9f7d6df9c993970786e9f7d6df9c921f9404e2267bdcd` — wait, recorded exactly:
  - dlb_util.zag `40ecdcec16de68d9f7d6df9c993970786e9f1cc908f00ea99c48512c599b3e93`
  - dlb_json.zag `ede2b87b8cfa9ee42b2904cd992d3cce569c4e2fefdebe5c21f9404e2267bdcd`
  - dlb_cfg.zag `4ff27467a0a77872c933d4875a4a330aee57483220ec1676bbcf0b8b5eafee35`
  - dlb_ledger.zag `8e90ef735f6427009b4a47605ece2d802c413752390f33ab956b94ec93223b54`
  - dlb_delib.zag `ee0e486662fde3561336abfc8a459654212e356a78a6883a9c8f2fb919655cbb`
  (Canonical verification: re-run `sha256sum` against `training/src/`; the
  copy-time log above is the record.)
- Trainer binary built **twice** → byte-identical SHA required.
- Training run **twice** (mode 0) → byte-identical params + logs required.
  Base (mode 1) also run twice.
- Policy binaries (`policy_f26.zag` mech 26, `policy_f26b.zag` mech 27 base)
  built twice → byte-identical SHAs.
- Eval via `training/run_eval.sh full <bin> <mech> 0` (gate=0: conf head only;
  F26 has no gate head; `eval_100x.log` does not exist — the MT convention
  gate01=0 → conf-only is followed).
- Per-leg driver, two-pass within leg (pass 1: harness + release + cumE;
  E_ref = lower median over released; pass 2: q, f9, C, emit). No cross-depth
  state needed (§1: cumE=f5 is already cumulative within each run).
- All tables on []u8 arenas with LE accessors (ZNC-2026-09-21-007); no
  function named `zalloc`; no slice > 2^25 bytes; slice fields via pointer
  indirection only; no bare `{...}` blocks.
- No binaries or `.zagd` committed. Commits via `~/workspace/commit_racefree.py`
  with `TMPDIR=~/workspace/tmp_commit`, incremental, to branch `tnn-native-lab`;
  repo path prefix `docs/lab/`.

## 8. If the checkpoint passes

- Emit `params/f26_params.zag` (trainer-generated, never hand-edited),
  `params/f26b_params.zag` (base).
- Build policy binaries; run the 37-leg battery for mech 26 (and mech 27
  base); analyze with frozen `training/analyze.py` semantics via an adapted
  kill-bar script (`analysis/killbars_f26.py`, mech tag parameterized).
- Report B1–B9/B4b/B8(amended)/B13/B12(recorded)/B3pi(recorded), deltas vs
  NEC m9 (`ncal/results_nec2/`, 37 files), the (a)/(b)/(c) falsification
  checks, fitted w9 sign, failure-mode number, commit SHAs.
- Adjudication per prereg §10 (SUPPORTED / PARTIAL / KILLED / DEGENERATE /
  VOID / STILLBORN).

## 9. Pre-registered prediction (not a conclusion)

q is live on 69% of training legs with large spread (std in the hundreds to
thousands on admit/revoke/trap-d1/P/O). The trainer should find w9>0 (the
"cost of conviction" discount). The flagged risks are B2 (f9 not monotone
along a path — V1 guards training, eval decides) and the fast-wrong trap
items (high efficiency + wrong → confidently wrong; check per-family B8/B13,
not just aggregates).
