# NAMECHECK: CONTLEARN-OWNED (replacement worker)

Lane: CONTLEARN-OWNED. Wave: wave-20261001-2321pdt.

## Step 0 (worker toolchain guard)

Setup: sh docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh
export PATH="$HOME/safebin"

Verification output (exact):
  which python3 -> prints nothing (exit 1)

Setup log lines:
  safebin: /home/hatch/safebin
  linked: 36 tools
  znc: OK (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1)
  verify: python3 absent from safebin PATH (OK)
  verify: python absent from safebin PATH (OK)
  SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)

Result: TOOLCHAIN CLEAN. `which python3` prints nothing under safebin PATH.
Pure Zag plus shell for all research logic. If any forbidden interpreter is
invoked this wave is PROCESS-FAIL.
