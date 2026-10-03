# BUILD_LOG.md — G2 "Predictive Residual Percept (PRP)" fork

Pure-Zag construction of the PAM fork G2, per frozen prereg `PREREG_G2.md`
(committed alone as `c242ec0980c3bb1cb84f3014ab11e9b2484ed095` before any
build output existed).

## Toolchain

`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
Build command (from `forks/G2/src/`):
`znc_linux_x86_64_abed8aa1 g2_sense.zag --no-zagd --no-analyze --no-foreground-cache -o sense`
The `sense` binary and any `.zagd` cache are build artifacts and are never
committed. `R33_NATIVE_IO_V1.zag` was copied verbatim from Approach A
(`senses/rebuild/a_raw/`).

## Build history

| # | date (UTC) | change | result |
|---|---|---|---|
| 1 | 2026-09-22 | first full `g2_sense.zag` (~56KB): extractors, residual arena, FNV-1a-64, contract finalizer, batch memory stream, ledger | `wrote native binary sense (189101 bytes)` |
| 2 | 2026-09-22 | batch record: added `residuals=` line (needed for independent ledger re-verification) | `wrote native binary sense (189281 bytes)` |
| 3 | 2026-09-22 | **shapetrans prediction corrected to the frozen prereg**: replaced the 2x-downsampled-mask "scale persistence" prediction with a literal 90-degree clockwise rotation of the binary mask (`shape_rot_profile`); the predicted invariant is the radial profile recomputed on the rotated mask ("rigid shape persists"). No prereg constant touched. | `wrote native binary sense (187343 bytes)` |

## Implementation notes

- Zero RNG in every decision path; no wall-clock; no uninitialized reads.
- All state in byte arenas with explicit `t_get32`/`t_put64`/etc. accessors
  (per the znc `as []i32` aliasing hazard, ZNC-2026-09-21-007).
- Residual vector: 256 signed bytes, layout per prereg (0-63 primary fine,
  64-127 primary coarse, 128-191 secondary fine, 192-255 reserved zeros).
- Contract: INSTALL iff `residual_norm < 24` AND `pred_hash == obs_hash`
  (FNV-1a-64 over coarse predicted vs observed bytes); else WITHHOLD.
- Batch mode: executable installed-memory stream (cap 2048); retrieval ranks
  same-task memories by coarse-predicted-byte agreement (top-3, install-order
  tie-break); top-1 agreement modulates confidence ±100 (frozen).
- `ablated` manifest mode runs the identical percept pipeline with a
  contract-less always-install gate (the B4 control).
- Hash-chained batch ledger: `chain = FNV-1a-64(chain || record)`, record =
  277 bytes (tid, judgment, disposition, norm LE16, pred/obs hashes LE64,
  256 residuals). Genesis: `FNV-1a-64("G2-PRP-1")`.

## znc hazards encountered

- None beyond the documented set; the build compiled clean on the first
  attempt. The `shape_rot_profile` replacement was verified byte-identical
  across rebuilds (see EVAL_G2.md B6).

## Deliverables

- `src/g2_sense.zag`, `src/R33_NATIVE_IO_V1.zag` (pure Zag, no binaries)
- `augment/augment.py` (deterministic 240-fixture generator, splitmix64)
- `evidence/eval_g2.py`, `evidence/EVAL_G2.md`, `evidence/LEDGER.md`
- `PREREG_G2.md` (frozen, committed separately)

## Build/test phase (continuation, 2026-09-22)

- `evidence/bin_A` verified: rebuilt Approach A from frozen
  `senses/rebuild/a_raw/sense.zag` with the pinned toolchain; stdout
  byte-identical to the existing `bin_A` on a probe fixture. (bin_A is a
  local test artifact, never committed.)
- Audit of `src/g2_sense.zag` vs frozen prereg (mechanical spot-checks):
  q8/q4c/res8, residual layout, isqrt norm over active fine dims, EPS=24
  hard-coded in `g2_finalize`, FNV-1a-64 chain with L_0=FNV("G2-PRP-1"),
  colordisc task (6-dim relational invariants, P=inv(A), dist<=40) — all
  match §2.1–2.4.
- Contract gate reads `t_get64(ps,32)==1` (a per-task "prediction
  available" flag) IN ADDITION to the frozen `norm<24 && ph==oh` rule.
  The flag is 0 only when the forward model produced no prediction at
  all (shapetrans degenerate mask, motiondir nsteps<3). Eval checks
  whether it changes any disposition on the eval set (pok-induced
  withholds = records with WITHHOLD, norm<24, ph==oh); recorded in
  EVAL_G2.md.
- Bug fix (no constant touched): `evidence/eval_g2.py`'s `JCODE` table did
  not match the binary's `parse_truth()` judgment codes (e.g. t5 lacked
  PURE/RICH, t4/t6/t3 codes were wrong); independent ledger
  re-verification would have failed spuriously. Fixed to task-keyed codes
  matching the binary exactly. Also added the prereg-required
  `evidence/LEDGER.md` writer (genesis, final chains, verify outcome).
- Augmentation determinism check: re-ran `augment/augment.py`; all 240
  fixtures byte-identical to the existing `augment/out` (sha256 before/after
  match), confirming the splitmix64/seed-20260922 determinism claim.
  (`augment/out` is a regenerable artifact, not committed.)
- Eval infrastructure fix: single batch-mode run over the 425-fixture
  adversarial manifest takes longer than the 600 s subprocess timeout
  (pitchdisc/timbredisc percept cost dominates); timeout is 3600 s
  in `eval_g2.py`. A VM-side kill interrupted the eval after 2 of 6 batch
  reps (contract r0/r1, byte-identical); the batch loop now reuses a rep
  output file when it already holds all 425 records, so the rerun only
  executes the 4 missing reps and re-verifies determinism across all three.
- Independent ledger re-verification (python FNV-1a-64, task-keyed judgment
  codes matching the binary's `parse_truth`): batch contract run verifies
  PASS, 425/425 records, final chain cf4ab3fd62a17a71.
- **Verdict (mechanical, from the frozen bars): G2 is KILLED.** Contract-mode
  batch over the 425 adversarial fixtures: 209 installs, 50 false installs
  (installed with wrong judgment) = 23.92% false-install rate per install,
  far above the 8% kill bar (B5 FAIL). Per-task false-install rates:
  colordisc 20.8% (11/53), colorconst 0% (0/5), shapetrans 50% (2/4),
  pitchdisc 0% (0/24), timbredisc 14.3% (10/70), motiondir 50.9% (27/53).
  The pok "prediction available" flag fired 0 times on this set, so the gate
  behaved exactly as the frozen two-condition rule — the failure is in the
  rule itself, not the extra flag.
- Why it died: the contract gates on PREDICTION consistency (residual norm +
  coarse hash match), but a wrong judgment can be perfectly
  prediction-consistent. The adversarial set is deliberately misleading, and
  the misleading cases are self-consistent: motiondir's constant-velocity
  prediction holds under contrast-flatten/frame-drop/reversal while the
  direction judgment is wrong; colordisc's +/-24 noise keeps coarse residuals
  at 0 while flipping the RGB-dist judgment near the boundary; timbredisc
  installs 100% (stationary tones always match the persist-forward
  prediction) including the 10 distractor-harmonic misjudgments.
  Predictive consistency does not imply judgment correctness.
- What did NOT fail: B1 viability 75.4% mean primary (>= 60%, PASS);
  B2 head-to-head G2 75.4% vs A 72.6% (G2 wins, pitchdisc 100% vs 83.3%);
  B4 contract proof PASS (dispositions altered on 50.8% of adversarial
  fixtures, false installs 50 vs 132 ablated); B6 determinism+ledger PASS;
  integration 99.9% (>= 85%, PASS). The contract is load-bearing (B4) but
  not sufficient (B5) — it withholds 216/425, including 82 wrong judgments,
  yet still installs 50 wrong ones.
- Efficiency note (B3): G2 costs MORE than A per percept, not less —
  pitchdisc ~9.17M vs ~4.52M ops, shapetrans ~92k vs ~28k ops (the 90-degree
  rotation prediction), ~1x elsewhere. The hypothesis's O(N)-vs-O(N^2)
  saving has no O(N^2) baseline in A to beat; the residual layer is pure
  overhead. Bytes: G2 single-mode stdout ~733-788 B/fixture (10-per-task
  sample) vs A ~92-139 B, dominated by the 256-residual text list.
- Final eval completed 2026-09-23 ~06:15 UTC: all 6 batch reps byte-identical
  (3x per mode), ledgers independently verified 425/425 both modes,
  EVAL_G2.md + LEDGER.md written. Integration on the final binary: 925/925
  (100%). Verdict stands: KILLED on B5 (23.92% false-install > 8%).
- Note: a sibling agent concurrently produced batch/analysis artifacts in the
  shared scratch dir; all outputs are byte-identical (deterministic binary),
  and the committed EVAL_G2.md merges their detailed analysis with this
  run's mechanical numbers (sha256-verified identical).
