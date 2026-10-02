# NAMECHECK.md: wave-20261001-2321pdt, lane BATTERY-E4

Worker: BATTERY-E4 (replacement worker; executes discriminating
experiment E4, the within-cluster discriminator for Cluster 1's
refined shared cause, from the BATTERY-CLUSTER analysis).
Date: 2026-10-02.

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
nothing (exit=1). `which znc` resolves to /home/hatch/safebin/znc.

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
read-only inspection of state.bin via the committed v3/E1 lineage
offsets is permitted as an external probe). (iii) All writes are
inside docs/lab/rsi/runs/wave-20261001-2321pdt/BATTERY-E4/. (iv)
BATTERY, BATTERY-CLUSTER, and BATTERY-E1 lane directories are
read-only for this worker; their committed sources are extracted
with git show only, from the recorded commits: E1 prereg 793abbf65,
E1 worlds aa38427b8, E1 inspector/tools 4afcd9f3b, E1 runs
f5b1bab41.

## Provenance

- BATTERY-CLUSTER/CLUSTER_ANALYSIS.md: Cluster 1 (DERIVATION
  SUBORDINATION), hypotheses H1a/H1b/H1c/H1d; E4 prioritized as the
  within-cluster discriminator for H1a (precedence-reversal world).
- BATTERY-E1/E1_RUN.md (verdict E1-FIRSTCLASS): H1c killed;
  Cluster 1 refined to "derived structures exist but have no
  privileged standing in the read path; the flat instance-fact
  layer is consulted first and wins"; H1a wins for W1/W2.
- v3_inspect_state / e1_inspect_state / e1_struct_check lineage
  from lanes BATTERY and BATTERY-E1 (committed tools, read-only
  reuse).
- Frozen binary: freeze_shim2_bin
  9217054c5af6dec057c4530c4de3ba246f521acc6df741d1989a4504acc72954;
  tnn2.zag
  a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd;
  pinned znc
  498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef.
  All three hashes re-verified by this worker before freezing the
  E4 prereg.
