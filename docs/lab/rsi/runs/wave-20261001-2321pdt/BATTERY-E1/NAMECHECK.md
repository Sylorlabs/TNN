# NAMECHECK.md: wave-20261001-2321pdt, lane BATTERY-E1

Worker: BATTERY-E1 (replacement worker; executes discriminating
experiment E1 from the BATTERY-CLUSTER analysis).
Date: 2026-10-01/02.

## Step 0 (toolchain guard, mandatory first)

Executed before any other work:

```
cd ~/workspace/tnn-rsi && sh docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh && export PATH="$HOME/safebin"
```

Verification output (exact):

```
safebin: /home/hatch/safebin
linked: 36 tools
znc: OK (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1)
verify: python3 absent from safebin PATH (OK)
verify: python absent from safebin PATH (OK)
SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)
```

`which python3` prints nothing (exit=1). `which python` prints
nothing (exit=1).

Toolchain: safebin only (36 tools: coreutils, git, pinned znc). No
Python anywhere in this lane. All research logic (world generator,
inspector, checker, controls, audit) is Zag compiled with the pinned
znc. Shell is used only for invoking znc, running binaries, git ops,
and move/copy of files. Any forbidden-interpreter invocation is
automatic PROCESS-FAIL with disclosure.

## Adversary independence attestation

(i) This worker has not authored mechanism-build or mechanism-repair
code in the previous two waves. (ii) The frozen mechanism source was
not modified; the frozen binary is used as-is (white-box
read-only inspection of state.bin via the committed v3 lineage
offsets is permitted as an external probe). (iii) All writes are
inside docs/lab/rsi/runs/wave-20261001-2321pdt/BATTERY-E1/. (iv)
BATTERY and BATTERY-CLUSTER lane directories are read-only for this
worker; their committed sources are extracted with git show only.

## Provenance

- BATTERY-CLUSTER/CLUSTER_ANALYSIS.md (commit 1a564788c): two
  clusters, eight hypotheses; E1 prioritized first by information
  gain (tests H1c for Cluster 1, DERIVATION SUBORDINATION).
- v3_struct_check / v3_inspect_state lineage from lane BATTERY
  (committed tools, read-only reuse of the state-layout offsets).
- Frozen binary: freeze_shim2_bin
  9217054c5af6dec057c4530c4de3ba246f521acc6df741d1989a4504acc72954;
  tnn2.zag
  a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd.
