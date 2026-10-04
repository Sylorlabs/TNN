# NAMECHECK.md - INTERACTIVE lane, wave-20261002-0221pdt

## Step 0: Toolchain guard (worker toolchain guard, owner's governance ruling)

- Ran: `bash docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`
- Result: SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)
- Exported PATH="$HOME/safebin" for all shells.
- `which python3` -> not found (exit nonzero, empty output). `which python` -> not found.
- Pinned znc verified: sha256 498abcb5ab346f8c... matches pinned prefix 498abcb5.
- `znc --version` -> znc 2026.07.0-dev (edition 2026)
- No Python will be invoked in this lane. Forbidden-executable invocation = automatic PROCESS-FAIL.

## Lane identity

- Lane: INTERACTIVE (investigate runnable interactive TNN)
- Wave: wave-20261002-0221pdt
- Branch: tnn-native-lab
- Working copy: ~/workspace/tnn-rsi
- Lane dir: docs/lab/rsi/runs/wave-20261002-0221pdt/INTERACTIVE/
- Investigation only; no source-tree modifications.

## Notes

- Dash-scan of lane docs will use docs/lab/research-lead/overnight-20260928/worker_snippets/check_no_dash.sh before commit.

## Step 1: build and run record

- Build: `znc tnn_chat.zag --no-zagd --no-analyze --no-foreground-cache -o tnn_chat`
  in build/, exit 0. Pinned znc sha256 498abcb5ab346f8c... re-verified pre-build.
- Source sha c0776ad6... matches frozen authority manifest. Binary sha
  1ada2fae63ddd63d37f06705459c0d8b1d9c8dffc859af25949221bf5895749c,
  byte identical to the 2026-09-23 recorded binary hash.
- 3-prompt probe: ran, exit 0, byte-captured in build/run3.out; second run
  byte identical (cmp clean), deterministic.
- 5-exchange probe chat: ran, exit 0, byte-captured in build/probe5.out;
  4/5 passes, turn 4 is the informative knowledge-boundary failure
  (see PROBE_CHAT.md).
- No Python invoked at any point. PATH was $HOME/safebin for every command.
