# NAMECHECK - HPIREV2 wave-20261001-2321pdt

## Step 0 - Toolchain guard

SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)
znc: OK (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1)
which python3 -> not found (exit 1)
which python  -> not found (exit 1)
verify: python3 absent from safebin PATH (OK)
verify: python absent from safebin PATH (OK)

Recorded at lane startup, 2026-10-01.

## Step 1 - Prereg freeze (committed alone)

Narrowed prereg PREREG_PI_REV2_NARROWED.md committed ALONE in
commit 00b31af53, before any implementation file. Five fresh sealed
single-conflict worlds (A2/B1/B2/C2/D2), 25 file hashes frozen
therein, kill bars K-SC-W1..W5, K-SC-B, K-ARCH1/2 frozen. Design
seeds disclosed (non-independent). Pre-freeze mechanical
validation caught and fixed 3 design slips, disclosed in the
prereg. Dash check passed before commit.

## Step 2 - Implementation

- Executor harness s8_exec.zag: lines 1-606 of proc_revise2.zag
  copied byte-verbatim (prefix hash verified 8d2b16ab...), plus 433
  new harness lines (helpers + new main). No machinery altered.
- Validator source /tmp/val_main.zagpart copied into the lane as
  val_main_s8.zagpart for certification evidence.
- s8_exec_bin: 3/3 byte-identical builds, sha256
  aee1b6f21a4b5309a3c93e9f66d9c38553bd75db926feeba123207373117ddbc.

## Step 3 - Execution and verification

- 15 sealed runs (5 worlds x 3): all exit 0, all stderr 0 bytes,
  3/3 byte-identical per world. Transcription fidelity 5/5 EXACT
  (STAGE lines vs sealed files). 25/25 sealed file hashes verified
  against the prereg at load time.
- All prechecks PASS on all worlds (V0 learnable, V1a-e
  disjointness, V3 impossibility, V2 real counterexample).
- Revision measurements matched pre-freeze predictions exactly:
  A2 (0,81) alt=3 evals=6; B1 (0,33) alt=2 evals=6; B2 (0,47)
  alt=4 evals=6; C2 (0,59) alt=2 evals=11; D2 (0,80) alt=24 evals=6.
- K-SC-W1: PASS 5/5 (fails_total=0). K-SC-W2: PASS 5/5 (<=25).
  K-SC-W3: PASS 15/15 (reuse_correct=1, 0 post-W3 revision
  lines). K-SC-W4: PASS. K-SC-W5: PASS (pure Zag; which
  python3/python print nothing; no other interpreter invoked).
- K-SC-B regression: s7_exec_bin hash-verified
  (155cea26...), 3x re-runs byte-identical to the step-7 record
  (f56080d6...). S1: w_fails_total=1. S2:
  COUNTEREXAMPLE_DETECTED at the W3 reuse probe. S3: 0 post-W3
  revision lines. No silent wrong convergence.
- K-ARCH1: PASS (frozen source hash dd3cb02d... unchanged).
  K-ARCH2: PASS (0/0/0/0/0).
- No interpreter invoked other than the safebin at any stage.
  Final verdict: BUILD-PASS on the narrowed claim.

Recorded 2026-10-01 after execution.
