# NAMECHECK.md (fork_battery lane, wave-20260930-2021pdt)

## Step 0: Safebin activation and toolchain verification

Commands run (exact):

1. `bash ~/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`
   Output: `safebin: /home/hatch/safebin`, `linked: 36 tools`, `znc: OK (.../znc_linux_x86_64_abed8aa1)`, `verify: python3 absent from safebin PATH (OK)`, `verify: python absent from safebin PATH (OK)`, `SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)`
2. `export PATH="$HOME/safebin"` then `command -v python3` -> output: (empty), return code 1
3. `command -v python` -> output: (empty), return code 1
4. `command -v znc` -> `/home/hatch/safebin/znc`
5. `command -v git` -> `/home/hatch/safebin/git`

SAFEBIN ACTIVE: python3/python do not resolve in this PATH.

All subsequent work in this lane is pure shell + pinned znc + git.
No forbidden executable invoked. No PROCESS-FAIL.
