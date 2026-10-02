# NAMECHECK.md (wave-20260930-2021pdt, lane exp2)

## Step 0: Toolchain guard

Startup commands run verbatim:

```
bash ~/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh
export PATH="$HOME/safebin"
```

Setup output confirmed: SAFEBIN-READY: /home/hatch/safebin (36 tools, no python).
Verification output of `command -v python3`: (empty, no output).
Verification output of `command -v python`: (empty, no output).
znc resolves: /home/hatch/safebin/znc, version znc 2026.07.0-dev (edition 2026).

SAFEBIN ACTIVE: python3/python do not resolve in this PATH.

All computational research operations in this lane are implemented in pure Zag (compiled with the pinned znc). Shell is used only to invoke znc, run binaries, do git operations, and move/copy files. No forbidden executable has been invoked.
