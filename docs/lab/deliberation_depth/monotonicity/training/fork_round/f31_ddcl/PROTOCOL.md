# F31 DDCL — Depth-Discounted Calibration Ledger: Training & Build Protocol

**Recorded BEFORE the first training run** (prereg §5 / task requirement).
Fork dir: `deliberation_depth/monotonicity/training/fork_round/f31_ddcl/`.
Frozen authority: repo `sylorlabs/TNN`, branch `tnn-native-lab`, commit
`3a2eef44` (v2) — `docs/lab/deliberation_depth/monotonicity/training/fork_round/PREREG_FORKROUND.md`
§3 (F31). `ideas/fable_forks.md` FORK 4 (Mechanism D) is authoritative on
mechanism detail. The v2 TRAIN-COORD repair does not affect this fork's ledger
design (noted in task); F31's base-head optimizer is chosen below and recorded
here, pre-training.

## 0. Frozen inputs (verified)

- Training cells: `training/features/features.tsv` (5240 rows).
  - Local SHA-256: `4682190cfd504cb692df122a6b054d8fad65ef860707e6a92abfdf04e65a897d`
    — matches the task's frozen hash. (Note: PREREG_FORKROUND.md §2
    transcribes `...e65e897d`; the on-disk file hashes `...e65a897d`,
    matching every prior round's recorded value — one-char prereg typo,
    file is genuine.)
  - Heldout flags honored: training stream = rows with heldout=0 AND
    rel4=1 (M4-released), in fixed file order. heldout=1 rows (420) are
    excluded from fitting AND from the ledger.
  - Training cells: 4222. Per-depth: d1=940, d2=893, d4=807, d8=786,
    d16=776, d32=15, d64=5.
- Toolchain (pinned, ONLY):
  `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`,
  SHA-256 `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`.
- Harness modules copied byte-identical (SHA-verified, see logs/SRC_SHA256SUM.txt):
  `R33_NATIVE_SHA256_V2.zag`, `R33_NATIVE_IO_V1.zag`, `dlb_util.zag`,
  `dlb_json.zag`, `dlb_cfg.zag`, `dlb_ledger.zag`, `dlb_delib.zag`,
  `feat.zag`, `gate.zag`, `policy.zag` (kept unused; eval driver is the
  new `policy_f31.zag`).

## 1. Mechanism (frozen spec, integer formalization)

Depth slots: dslot(d) ∈ {0..6} for depths {1,2,4,8,16,32,64}.

```
B(s)       = clamp((Σ_{i=1..8} w_i·f_i)/1000 + b, 0, 1000)   // base head
G_t(ds)    = mean_conf_t(ds) − mean_acc_t(ds)                // thousandths
             mean_conf_t = tdiv(sum_conf, count)
             mean_acc_t  = tdiv(sum_correct·1000, count)
offset(ds) = clamp(tdiv(G_t(ds)·damp, 1000), −200, 200)
C(s,ds)    = clamp(B(s) − offset(ds), 0, 1000)               // emitted head
```

**Unit disambiguation (recorded pre-training).** The ideas file writes
`offset(d) = clamp(G_empirical(d)·damp, −200, 200)` with `damp ∈ [200,800]`.
Read literally with G in thousandths, ANY |G| ≥ 1 thousandth saturates the
±200 cap on every depth — the damp meta-rule (±50 steps) would be
meaningless and the ledger would be a constant ±200 shift, not an empirical
correction. The only self-consistent integer reading: G_empirical is the
fractional gap, so the offset (in thousandths) is `tdiv(G_t·damp, 1000)`
with G_t in thousandths. E.g. G_t=100 (0.100 overconfident), damp=200 →
offset 20; damp=800 → 80. The ±200 cap then binds only for extreme gaps
(G_t > 250 at damp=800), matching the ideas file's "large-G correction is
correspondingly limited". This reading is adopted.

**Closed-loop recording (recorded pre-training).** The ledger records the
EMITTED confidence C(s,ds) (post-offset), not the base B(s) — this is the
ideas file's design: its Q3 failure mode (1) describes exactly this feedback
("high offset → low confidence → low mean_conf → ..."), and the damp
meta-rule exists to damp its oscillation. Feedforward (recording B) would
make both the failure mode and the meta-rule vacuous. Causal discipline:
the ledger entry for a training cell is appended AFTER emission, using the
label then observed; at eval time the ledger is frozen at train end.

**Damp meta-rule (recorded pre-training).** damp is global (one value, per
the ideas file's singular `damp ∈ [200,800]`). damp₀ = 200
(most conservative start; corrections strengthen only after demonstrated
stability — anti clamp-death posture). After each ledger append at slot ds:
recompute G_t(ds); sign-flip = prev_sign(ds) ≠ 0, new sign ≠ 0, signs
differ (zero crossings through exact 0 are not flips). On flip:
damp = max(200, damp−50); stable_run = 0. On no flip: stable_run += 1;
if stable_run ≥ 100: damp = min(800, damp+50); stable_run = 0.
(`stable_run` counts consecutive global-stream appends without any flip.)

**Ledger structure (no arbitrary limits).** Per the task and Micah's
no-arbitrary-limits law, the ledger is NOT architecturally capped: per-depth
entry storage grows in 256-entry chunks (4 bytes/entry: conf u16 + correct
u8 + pad; 1 KiB/chunk), allocated on demand, unbounded. The ideas file's
2048 figure is used ONLY as a preregistered test constant for this
experiment: per-depth FIFO capacity 2048 (following frozen prereg §3's
"per-depth FIFO ledger (cap 2048)"), implemented as oldest-entry drop with
sum decrements. It NEVER binds here (max per-depth training entries 940 <
2048), so the FIFO path is inert — noted, not tested. (The ideas file also
says "2048 total entries"; the frozen prereg's per-depth reading governs
the experiment. Under the total reading it would bind (4222 > 2048);
documented as a divergence with rationale.)

## 2. Training (two stages, both deterministic)

**Stage A — base head fit.** Coordinate descent (the round's repaired
TRAIN-COORD v2 convention, §5b — same mechanics, this fork's objective):
objective Σ over training released cells (heldout=0, rel4=1, all depths)
of (B−1000·y)², y = correct4. Init: w1..w8 = 0, b = 0 (recorded HERE,
before training). Steps: ±50, then ±8, then ±1 refine; fixed order
w1..w8,b; first-improvement; accept on strict objective reduction only;
8 sweeps; early stop if a sweep moves nothing. All integer ops,
truncation-toward-zero division, fixed file order. Zero RNG.

**Stage B — online ledger pass.** Single pass over the training stream in
file order (heldout=0, rel4=1). Per cell: B from Stage-A weights;
ds = dslot(depth); off = clamp(tdiv(G_t(ds)·damp,1000), −200, 200) from the
CURRENT ledger; C = clamp(B − off, 0, 1000); append (C, correct4) to
ledger[ds]; damp meta-update per §1. Frozen at train end: per-depth
sum_conf/sum_correct/count, final damp, per-depth offsets. These are baked
into `f31_params.zag` (generated by train_f31.zag, never hand-edited):
`f31_w1..w8`, `f31_b`, `f31_damp`, `f31_off0..6`.

**Stage-A veto check (final answer only, per §5b intent):** after fitting,
compute theater count (V1+V2 over training released adjacent-depth pairs),
train meanConfCorrect (all training released cells), and any (fam,depth)
n≥8 with G < −0.080. Reported as diagnostics.

**Checkpoint amendment (2026-09-24, pre-eval, with rationale).** PROTOCOL.md
as first written made these vetoes VOID conditions. That is WITHDRAWN:
frozen prereg §5b scopes TRAIN-COORD — and its V1–V3 vetoes — to
"F24, F25, F26, F27 only". F31's frozen spec (ideas file, Mechanism D)
contains no vetoes, and the task's F31 kill conditions are the §3
falsifiers (a)/(b)/(c), adjudicated on the battery. The vetoes test the
BASE head; F31's final answer is the ledger-corrected head, and the veto
dimensions (theater, underconfidence) are adjudicated on the final head by
the frozen bar table itself (B2, B13). Checkpoint per frozen §5 stands:
weights ≠ init AND DDCL liveness (ledger entries at all depths, ≥1 nonzero
offset, ≥1 damp adaptation). The veto diagnostics (theater=175 on the base
head, v3 fail on the base head) are reported as evidence in VERDICT.md,
not hidden. A dead intervention would be VOID; this one is live
(7/7 depths ledgered, 6/7 nonzero offsets, 45 damp adaptations).

**§5 checkpoint liveness:** base weights ≠ 0-init required; plus DDCL
liveness: ledger counts > 0 at multiple depths, ≥1 nonzero offset, damp
meta-adaptations logged. Dead → VOID.

## 3. Eval driver (policy_f31.zag)

Frozen harness deliberation at fixed depth (byte-identical dlb_* copies),
M4 release skeleton (release L_t iff L_t == L_1, else ABSTAIN), features
f1..f8 via the frozen pl_features, confidence
C = clamp(B − f31_off[dslot], 0, 1000), cert `f31-ddcl`. No abstention gate
(gate01 must be 0). TSV columns identical to mech.zag.
Eval: `run_eval.sh f31full <policy_f31_a> 31 0` (37 legs × A/B determinism).

## 4. Kill bars (frozen §4 table + F31-specific, prereg §3)

- B1–B9, B4b (frozen analyzer semantics), amended B8 (§4b); B13 kills.
- Recorded (no kill): B12, B3pi. Deltas vs NEC m9
  (`training/ncal/results_nec/`, mech 9 legs).
- KILL_A (feedback oscillation): ∃ dslot with |offset| = 200 (cap hit)
  AND a strict eval G-rise into or out of that depth (both rungs n_rel ≥ 8).
- KILL_B (redteam tiny-n): redteam strict G-violations (no n filter, frozen
  analyzer semantics) for m31 ≥ NEC m9's redteam G-violations.
- KILL_C (over-correction → B13): B13 fails at (F,d) with |offset(d)| ≥ 50
  (nontrivial correction applied — failure plausibly from the offset).
- Report: per-depth offset(d) values; whether any hit the ±200 cap.

## 5. Build & determinism gates (frozen §8)

Pure Zag, zero RNG. Pinned toolchain only. A/B byte-identical builds AND
runs. Training ×2 → byte-identical params. B9 100% identity vs M4.
[]u8 arenas + LE accessors; no fn named zalloc; no slice > 2^25 bytes.
No binaries or .zagd committed (commit_racefree.py, TMPDIR=~/workspace/tmp_commit).
