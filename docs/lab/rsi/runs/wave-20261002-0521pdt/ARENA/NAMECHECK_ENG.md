# NAMECHECK: ARENA-ENG lane, wave-20261002-0521pdt

## Step 0: Worker toolchain guard (MANDATORY FIRST, recorded before any other work)

- Ran: `bash docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`
  result: `SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)`
- `export PATH="$HOME/safebin"` applied to every exec call in this lane
  (via the tool `env` parameter).
- `which python3` returns NOTHING (exit 1). `which python` also empty.
- `which znc` resolves to `/home/hatch/safebin/znc` (pinned Linux binary).
- PURE ZAG ONLY for all research logic. Shell use restricted to: invoking
  znc, running compiled binaries, git ops (pathspec-only), file moves,
  timing via `date`.
- Pinned znc quirk honored: no `as *i32` + `q[0..n]` slice construction;
  u8-backed cells with get32/set32 helpers only.
- If any forbidden executable is invoked, this lane's work is automatically
  PROCESS-FAIL.

Step 0 completed 2026-10-02 05:26 PDT, before any diagnosis or code.
