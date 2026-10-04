# NAMECHECK.md: DEVANG5 toolchain guard (wave-20261002-0521pdt)

## Step 0 (mandatory first, recorded before any other work)

- Ran `docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`:
  `SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)`.
- Exported `PATH="$HOME/safebin"`.
- `which python3` returns nothing (exit 1). `which python` returns nothing.
- Pinned znc verified by setup script:
  `znc: OK (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1)`.
- Toolchain rule for this wave: PURE ZAG ONLY for implementation,
  compilation, execution, generation, scoring, and analysis. Shell only
  for invoking znc, running built binaries, git ops, and file moves.
- Pinned znc constraint honored: no `as *i32` + `q[0..n]` slice
  construction inside functions; u8-cell loop idiom with
  little-endian pack/unpack helpers (get32/set32).
- Forbidden executable invoked at any stage = automatic PROCESS-FAIL
  for the wave. No near-misses to disclose at Step 0.

Recorded: 2026-10-02, before prereg freeze.
