# NAMECHECK.md: lane TRADES, wave wave-20261002-0521pdt

## Step 0: toolchain guard verification (worker startup)

- Ran: `bash docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`
  from ~/workspace/tnn-rsi.
- Output: `linked: 36 tools`, `znc: OK
  (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1)`,
  `SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)`.
- `which python3` in safebin PATH: NOT FOUND (exit 1). `which python`: NOT FOUND.
- Every shell command in this lane uses `export PATH="$HOME/safebin"` first.
- No Python, C/C++, JavaScript, or Rust anywhere in this lane. Pure Zag +
  shell only. Any forbidden-executable invocation is automatic PROCESS-FAIL
  and will be disclosed immediately in this file and the final report.
- Dash scans: `docs/lab/research-lead/overnight-20260928/worker_snippets/check_no_dash.sh`
  on all lane docs before each commit. Zero em/en dashes in loop docs.
- Note: `du` is not in the safebin tool set (exit 127); `ls -la`/`stat`
  used for sizes. Not a toolchain violation.

## Guard event log

- 2026-10-02 12:25 UTC (lane start): no forbidden invocations.

## Steps

- Step 1: read the frozen WIDE-EIG-10 prereg (wave-20261002-0221pdt/TRADES/
  PREREG_TRADES1.md, frozen alone at commit bbb986a79449d1c635ff57b7cb41611b2e9b5bb6),
  audit the uncommitted 0221pdt implementation against it, run the
  commit-order self-check (prereg commit strictly precedes every
  implementation commit; the implementation exists only as untracked files).
- Step 2: adopt the audited implementation, build all variants in pure Zag
  with the pinned znc under safebin, commit the sources pathspec-only.
- Step 3: sealed evaluation per the frozen protocol (K1..K10), red team,
  verdict.

## Lane scope

One expensive candidate, one zero capability: WIDE-EIG-10, a 10-trace
EIG-guided deliberation ensemble for causal intervention choice (C9 intent),
frozen verdict-aggregation rule, 10x deliberation budget vs single-trace
EIG. Never faster+dumber. Efficiency only as fuel for more intelligence.
