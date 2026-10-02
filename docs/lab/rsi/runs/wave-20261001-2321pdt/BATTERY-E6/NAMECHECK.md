# BATTERY-E6 NAMECHECK (toolchain verification record)

Lane: BATTERY-E6 (replacement worker; executes E6, the within-cluster discriminator after E2)
Wave: wave-20261001-2321pdt
Worker session: c91462f7-2138-417c-9788-36fb03161ac8

## Step 0: Safebin toolchain guard verification (MANDATORY, run first)

Executed before any research operation:

```
cd ~/workspace/tnn-rsi
sh docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh
export PATH="$HOME/safebin"
which python3
```

Exact verification output (2026-10-02, from `muse.exec`):

```
safebin: /home/hatch/safebin
linked: 36 tools
znc: OK (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1)
verify: python3 absent from safebin PATH (OK)
verify: python absent from safebin PATH (OK)
SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)
---PATH---
/home/hatch/safebin
---which python3---
(exit=1, no output)
```

Result: PASS. `which python3` prints nothing (exit code 1). python3 and python
are both absent from the safebin PATH. Pure-Zag constraint holds.

## Governance notes

- PURE ZAG ONLY for all research operations in this lane (implementations,
  verifiers, scorers, harnesses, analysis, scratch).
- Shell only for invocation: znc compile/run, git ops, file move/copy.
- Any forbidden-interpreter invocation = PROCESS-FAIL; must be disclosed and
  cleanly re-frozen if the result matters.
- Scope: this lane may only commit under
  docs/lab/rsi/runs/wave-20261001-2321pdt/BATTERY-E6/.
- BATTERY, BATTERY-CLUSTER, and BATTERY-E2 lane dirs are READ-ONLY for this
  worker: extract committed sources via `git show` from recorded commits.
- No push. Local commits only. No `git reset --hard`. No rebase.
- Docs checked with check_no_dash.sh before commit (no em-dashes).
