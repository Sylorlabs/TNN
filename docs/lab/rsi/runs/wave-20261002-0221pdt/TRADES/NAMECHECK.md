# NAMECHECK.md: lane TRADES, wave wave-20261002-0221pdt

## Step 0: toolchain guard verification (worker startup)

- Ran: `bash docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`
  from ~/workspace/tnn-rsi.
- Output: `linked: 36 tools`, `znc: OK
  (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1)`,
  `SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)`.
- `which python3` in safebin PATH: NOT FOUND. `which python`: NOT FOUND.
- Every shell command in this lane uses `export PATH="$HOME/safebin"` first.
- No Python, C/C++, JavaScript, or Rust anywhere in this lane. Pure Zag +
  shell. Any forbidden-executable invocation is automatic PROCESS-FAIL and
  will be disclosed immediately in this file and the final report.
- Dash scans: `docs/lab/research-lead/overnight-20260928/worker_snippets/check_no_dash.sh`
  on all lane docs before each commit. Zero em/en dashes in loop docs.

## Guard event log

- 2026-10-02 (lane start): worker accidentally included the token `python3`
  in a shell command line (inside a compound sed invocation). The safebin
  PATH contained no python3 (`which python3` and `command -v python3` both
  return nothing, exit 1), so the shell reported command-not-found and the
  forbidden executable was NOT invoked. No PROCESS-FAIL event. The guard
  operated as designed: even a mistyped invocation cannot resolve. The
  intended sed edits in that command completed normally. No Python code has
  run in this lane.

## Steps

- Step 1: dev calibration prototype in /tmp (pure Zag, never committed):
  causal world logic plus policy variants on dev seeds, to set sane frozen
  kill bars with a power-analysis basis before freezing.
- Step 2: freeze PREREG_TRADES1.md ALONE (no implementation in that commit).
  Commit-order self-check: prereg commit strictly precedes implementation.
- Step 3: implement in pure Zag (trades_contestant.zag = INQ base plus
  CAUSAL-WIDE module; causal_world.zag; causal_score.zag; run_causal.sh).
- Step 4: dev smoke test in /tmp (never sealed), then sealed runs on the 8
  frozen seeds, 3/3 byte-identical reruns, compute-matched baselines,
  no-regression rerun of the 68-item arena battery.
- Step 5: self red team (REDTEAM_SELF.md), dash scan, commit lane dir with
  explicit pathspec. Report BUILD-PASS/BUILD-FAIL with the verdict line.

## Lane scope

One expensive candidate, one zero capability: WIDE-EIG-10, a 10-trace
EIG-guided deliberation ensemble for causal intervention choice (C9 intent),
with the verdict-aggregation rule frozen in the prereg. Target 10x
deliberation budget vs the single-trace EIG policy. Never faster+dumber:
no cheap-only variant is promoted; efficiency is fuel for more intelligence.
