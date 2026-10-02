# NAMECHECK.md - H5R2-REPRO (independent reproduction worker, wave-20261001-2321pdt)

## Step 0 - toolchain guard
Safebin activation run first, before any research work.

Verification output (recorded verbatim):
```
safebin: /home/hatch/safebin
linked: 36 tools
znc: OK (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1)
verify: python3 absent from safebin PATH (OK)
verify: python absent from safebin PATH (OK)
SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)
PATH=/home/hatch/safebin
which python3 -> (no output, exit 1)
which python  -> (no output, exit 1)
```
Forbidden interpreters are absent from PATH. Pure Zag constraint acknowledged.
