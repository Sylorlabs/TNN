# NAMECHECK: wave-20261002-0521pdt CONTLEARN (lane CLH2, longer-horizon delayed rebind)

## Step 0: toolchain guard (mandatory first, recorded before any research operation)

- 2026-10-02 05:31 PDT: ran
  docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh
  (exit 0; linked 36 tools; znc OK at
  /home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1;
  verify lines confirm python3 and python absent from safebin PATH).
- Exported PATH="$HOME/safebin" for this worker session.
- `which python3` returns nothing (exit 1) under safebin PATH.
- `which python` returns nothing (exit 1) under safebin PATH.
- `which znc` resolves to /home/hatch/safebin/znc; znc 2026.07.0-dev.
- PURE ZAG ONLY for this lane: research logic in Zag; shell only for znc
  invocation, binary execution, git ops, and file moves. Any invocation
  of a forbidden executable (python3, python, cc, node, etc.) is
  automatic PROCESS-FAIL for this lane's current scientific wave.
- Pinned znc (2026-09-30) codegen rule honored: no `as *i32` plus
  q[0..n] slice construction inside functions; u8-cell loop idiom with
  little-endian pack/unpack helpers only.
- Git discipline: pathspec-only commits. Never git add -A, stash, reset,
  clean, rebase, or reset --hard. Never weaken a frozen kill bar.
  Commits LOCAL ONLY, never push.

## Lane

- Wave: wave-20261002-0521pdt. Lane: CONTLEARN (CLH2: longer-horizon
  delayed rebind, backlog item 29).
- Working copy: ~/workspace/tnn-rsi, branch tnn-native-lab.
- Docs: docs/lab/rsi/runs/wave-20261002-0521pdt/CONTLEARN/
