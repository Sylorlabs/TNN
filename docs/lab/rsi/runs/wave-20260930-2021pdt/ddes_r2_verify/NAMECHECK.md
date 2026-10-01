# NAMECHECK.md: ddes_r2_verify lane, wave 20260930-2021pdt

## Step 0: toolchain guard verification

Commands run (in order):

```
bash ~/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh
export PATH="$HOME/safebin"
command -v python3
command -v python
command -v znc
```

Outputs:

- setup_safebin.sh: `linked: 36 tools`, `znc: OK (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1)`, `verify: python3 absent from safebin PATH (OK)`, `verify: python absent from safebin PATH (OK)`, `SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)`
- `command -v python3`: empty (no output)
- `command -v python`: empty (no output)
- `command -v znc`: `/home/hatch/safebin/znc`

SAFEBIN ACTIVE: python3/python do not resolve in this PATH.

All computational verification in this lane uses the pinned znc and safebin shell tools only. No python3 or python invoked at any point in this lane. If any forbidden executable were invoked, this section would record the incident and the lane would be declared PROCESS-FAIL.
