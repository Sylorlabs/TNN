# NAMECHECK.md (F1 lane, wave 20260930-2021pdt)

## Step 0: Toolchain verification (startup)

Commands run (2026-09-30 20:26 PDT):

```
bash ~/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh
export PATH="$HOME/safebin"
command -v python3
command -v python
```

Outputs:
- setup script: `SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)`; verify lines: `python3 absent from safebin PATH (OK)`, `python absent from safebin PATH (OK)`
- `command -v python3` : (empty)
- `command -v python` : (empty)

SAFEBIN ACTIVE: python3/python do not resolve in this PATH.

Lane worker will use only safebin tools (coreutils, git, pinned znc). All computational
research operations in Zag via znc. No forbidden executable has been invoked.
