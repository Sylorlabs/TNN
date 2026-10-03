# NAMECHECK: F2 v6 (evidence-driven revision loop, double regime shift), wave-20261002-0521pdt

Lane: F2 (active experiment construction, v6 with harder sustained goal).
Worker: research worker, wave-20261002-0521pdt.
Working copy: ~/workspace/tnn-rsi, branch tnn-native-lab.
Lane dir: docs/lab/rsi/runs/wave-20261002-0521pdt/F2/ (write ONLY here).

## Step 0: toolchain guard (BEFORE anything else)

- Ran `bash docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`:
  `SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)`.
- Every shell in this lane runs with `PATH=/home/hatch/safebin`
  (via the exec `env` parameter).
- `which python3` returns NOTHING (empty output, exit 1, confirmed).
- `which python` returns NOTHING (empty output, confirmed).
- `which znc` returns `/home/hatch/safebin/znc`
  (pinned znc, verified via setup script).
- PURE ZAG ONLY for this entire lane. No Python at any stage
  (implementation, build, execution, analysis, artifact handling).
- Forbidden-executable invocation = automatic PROCESS-FAIL; none occurred.
- Dash scans via
  `docs/lab/research-lead/overnight-20260928/worker_snippets/check_no_dash.sh`
  before every commit.
- Zero em/en dashes in loop documentation.
- Pinned-znc constraints honored: no `as *i32` + slice construction;
  u8-cell loop idiom only. (AGENTS.md toolchain lessons read.)

## Scope

- F2 v6: harder sustained goal = TWO hidden progressive mid-stream law
  changes (double regime shift), requiring an evidence-driven revision
  loop (no fixed revision cap; fixed-point stop). Supersedes the
  interrupted v5 (prereg never frozen, implementation never committed,
  sealed world never written, no verdict).
- v6 mechanism: v5 base + evidence-driven L_run loop (section 3 of
  PREREG_F2V6.md). The v6 delta is applied AFTER the prereg freeze.
- Sealed worlds: SHIFT2 (double shift), SHIFT1 (NC4 single shift),
  OSC (NC5 oscillating; DEV). Hashes frozen in PREREG_F2V6.md.
- Prereg PREREG_F2V6.md frozen ALONE first (commit-order self-check).
- Then implementation in pure Zag, sealed eval (3x byte-identical),
  self red-team, verdict.
- Report BUILD-PASS or BUILD-FAIL only.
