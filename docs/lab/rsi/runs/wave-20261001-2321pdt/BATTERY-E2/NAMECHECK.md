# NAMECHECK.md -- BATTERY-E2 lane wave-20261001-2321pdt

Lane: BATTERY-E2 (replacement worker; executes discriminating
experiment E2 from the BATTERY-CLUSTER analysis; H2a vs H2b for
Cluster 2, GUIDE CONTENT DECOUPLING).

## Step 0 (safebin toolchain guard, recorded verbatim)

Commands run:
```
cd ~/workspace/tnn-rsi
sh docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh
export PATH="$HOME/safebin"
which python3
```

Exact verification output:
```
safebin: /home/hatch/safebin
linked: 36 tools
znc: OK (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1)
verify: python3 absent from safebin PATH (OK)
verify: python absent from safebin PATH (OK)
SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)
```

`which python3` printed nothing (exit code 1). `python` likewise
absent. All subsequent work in this lane runs under PATH=$HOME/safebin
with pure Zag (pinned znc) for research logic and shell only for
invocation, git ops, file moves, and hashing.

## Adversary independence attestation

This worker has not authored mechanism-build or mechanism-repair code
in the previous two waves. This lane writes only inside
docs/lab/rsi/runs/wave-20261001-2321pdt/BATTERY-E2/. The BATTERY and
BATTERY-CLUSTER lane directories are treated as read-only sources
(extracted via git show from recorded commits, never edited).

## Scope guard

This lane executes exactly one discriminating experiment (E2) and
writes no patch, mode, bridge, handler, or semantic case. A
forbidden-interpreter invocation would be disclosed as PROCESS-FAIL
per governance; none has occurred.
