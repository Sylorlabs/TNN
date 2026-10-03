# HPIREV2 lane NAMECHECK: wave-20261002-1121pdt

Lane: HPIREV2 (H-PI-REV2 step-7: narrow the surviving single-conflict
bounded claim to a fresh frozen prereg; queue item 15).

## Step 0: Toolchain verification (worker toolchain guard)

- Ran `bash docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`.
- Result: SAFEBIN-READY: /home/hatch/safebin (36 tools, no python).
- `which python3` returns NOTHING (exit 1) under the safebin PATH.
- `which python` likewise returns NOTHING.
- `which znc` resolves to /home/hatch/safebin/znc.
- PURE ZAG ONLY for all computational research operations in this
  lane. Any forbidden-interpreter invocation is automatic
  PROCESS-FAIL with measurements quarantined.

## Step 1: Lane task

(a) Locate the H-PI-REV2 record and the exact surviving
    single-conflict bounded claim (provenance recorded in
    PROVENANCE.md).
(b) Write a FRESH frozen prereg narrowing the claim to precisely
    what survived; commit it ALONE before any implementation
    (commit-order self-check); red team the narrowing.
(c) Implement and run in pure Zag with byte-identical reruns if
    feasible this wave; otherwise deliver the frozen prereg plus
    a precise implementation plan for the next wave.

## Step 2: Git discipline

- Lane branch: lane-hpirev2-20261002-1121pdt.
- Write ONLY under docs/lab/rsi/runs/wave-20261002-1121pdt/hpirev2/
  in this worktree. Commits pathspec-limited to the lane dir plus
  the lane run dir.
- Never commit to tnn-native-lab; never rebase; never
  `git reset --hard`. Never push.
- Never write into scaling_5000_fixed or scaling_10000 dirs.
- Untracked files in the main worktree belong to other processes:
  read-only.

## Step 3: Standing rules observed

- No em-dashes in loop docs; verify with
  bash docs/lab/research-lead/overnight-20260928/worker_snippets/check_no_dash.sh.
- Frozen lanes: no CAUSALV7, no N+1 repair generations, no new
  semantic cases, never weaken a frozen kill bar, never count a
  prereg threshold before frozen execution, FW1-FW9 regression
  only.
- Debate Q2 OVERTURN qualifiers accompany every citation of the
  H-PI-REV2 result: bound holds only on rank-diagnosable single
  conflicts with probe-dependent trip.
