# ARENA-GEN-VERIFY NAMECHECK

Worker: ARENA-GEN-VERIFY (replacement worker for wave-20261001-2321pdt)
Task: independently verify ARENA-GEN NARROW verdict.

## Step 0: Worker toolchain guard (MANDATORY, done first)

Command sequence:
  cd ~/workspace/tnn-rsi
  sh docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh
  export PATH="$HOME/safebin"

Verification output (2026-10-02):
  safebin: /home/hatch/safebin
  linked: 36 tools
  znc: OK (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1)
  verify: python3 absent from safebin PATH (OK)
  verify: python absent from safebin PATH (OK)
  SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)
  which python3 -> (no output, exit=1)
  PATH after export: /home/hatch/safebin

python3 DOES NOT resolve. Proceeding under pure-Zag rule; shell only for git/file ops.
