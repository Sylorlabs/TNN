# NAMECHECK: EVIDENCE-CHECK lane (wave-20261001-2321pdt)

## Step 0 (mandatory toolchain guard)

Command sequence run at lane start:

```
cd ~/workspace/tnn-rsi && sh docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh && export PATH="$HOME/safebin"
```

Exact verification output:

```
safebin: /home/hatch/safebin
linked: 36 tools
znc: OK (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1)
verify: python3 absent from safebin PATH (OK)
verify: python absent from safebin PATH (OK)
SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)
PATH=/home/hatch/safebin
---which python3---
(exit=1, no output)
```

`which python3` prints nothing (exit code 1). Safebin active; no forbidden executables invoked in this lane. This is a verification lane: no experiments, no Python. Shell used for git/file ops only.

## Task

EVIDENCE-CHECK for wave-20261001-2321pdt: verify every one of the 47 verdicts in WAVE_RECORD.md has corresponding evidence on disk (lane dir exists and contains a JUDGE_BRIEF.md or VERDICT file). Result written to EVIDENCE_CHECK.md in this dir.
