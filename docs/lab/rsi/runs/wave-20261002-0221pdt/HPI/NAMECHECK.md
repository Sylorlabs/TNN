# HPI lane NAMECHECK: wave-20261002-0221pdt

Lane: HPI (H-PI-REV2 re-execution + newest-live-among-all-live gate test)

## Step 0: Toolchain verification (worker toolchain guard)

- Ran `bash docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`.
- Result: SAFEBIN-READY: /home/hatch/safebin (36 tools, no python).
- `which python3` returns nothing (exit 1) under the safebin PATH.
- `which python` likewise returns nothing.
- PURE ZAG ONLY for all computational research operations in this lane.
- Branch: tnn-native-lab; working copy ~/workspace/tnn-rsi; HEAD at lane start: 8930dcc17d9f332140cf64f0c239172610faced3.

## Step 1: Sub-task A setup

- Prereg: 72168c608 (amended H-PI-REV2 step-5, frozen alone in wave-20261001-1721pdt).
- Must re-read 72168c608 verbatim before any re-execution. Do not modify it.
- Debate Q2 OVERTURN qualifiers must accompany every citation of the H-PI-REV2 result:
  bound holds only on rank-diagnosable single conflicts with probe-dependent trip.

## Step 2: Sub-task B setup

- PREREG_H5R2_SYNTH.md must be committed ALONE first (prereg commit-order self-check).
- Debate Q5 UPHOLD scope boundary (H5R2 SEPARATED) must be respected explicitly.
- Byte-identical reruns 3/3 required.

## Step 3: Git discipline

- Write ONLY under docs/lab/rsi/runs/wave-20261002-0221pdt/HPI/.
- Commit only the lane dir with explicit pathspec. Never `git add -A`. Never push.
- Retry commits on ref-lock failure. Never `git reset --hard`, never rebase.

## Step 4: Reporting

- Sub-task A: REEXEC_STEP5.md with REEXEC-PASS / REEXEC-FAIL.
- Sub-task B: PREREG_H5R2_SYNTH.md (frozen alone), implementation, SEALED_EVAL.md,
  REDTEAM_SELF.md, VERDICT lines (BUILD-PASS / BUILD-FAIL).
