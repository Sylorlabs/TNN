# NAMECHECK.md

## Step 0: Worker toolchain guard (mandatory startup)

Commands run:
1. `bash ~/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`
   Output: `safebin: /home/hatch/safebin / linked: 36 tools / znc: OK (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1) / verify: python3 absent from safebin PATH (OK) / verify: python absent from safebin PATH (OK) / SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)`
2. `export PATH="$HOME/safebin"`
3. `command -v python3` -> (empty, no output)
4. `command -v python` -> (empty, no output)
5. `command -v znc` -> `/home/hatch/safebin/znc`
6. `znc --version` -> `znc 2026.07.0-dev (edition 2026)`

SAFEBIN ACTIVE: python3/python do not resolve in this PATH.

All subsequent work in this lane runs with PATH=$HOME/safebin. Pure Zag only: shell is used solely to invoke znc, run binaries, do git ops, and move/copy files. No forbidden executable has been invoked.
