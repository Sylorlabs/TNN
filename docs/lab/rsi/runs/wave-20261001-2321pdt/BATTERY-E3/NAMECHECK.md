# NAMECHECK.md: wave-20261001-2321pdt, lane BATTERY-E3

Worker: BATTERY-E3 (replacement worker; executes discriminating
experiment E3 from the BATTERY-CLUSTER analysis: the blind
composition probe with the oracle withheld, testing H1d).
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

`which python3` prints nothing (exit=1).

Toolchain: safebin only (36 tools: coreutils, git, pinned znc). No
Python anywhere in this lane. All research logic (world
generator, blind driver, scorer, inspector, audit) is Zag compiled
with the pinned znc. Shell is used only for invoking znc, running
binaries, git ops, and move/copy of files. Any
forbidden-interpreter invocation is automatic PROCESS-FAIL with
disclosure.

## Adversary independence attestation

(i) This worker has not authored mechanism-build or
mechanism-repair code in the previous two waves. (ii) The frozen
mechanism source was not modified: the blind driver reuses the
byte-identical cognition region of freeze_shim2.zag (verified by
diff and SHA-256 in the K-C0A audit); only the transport driver
section is new, and it contains no cognition. The oracle-present
control uses the frozen freeze_shim2_bin as-is (hash verified).
(iii) All writes are inside
docs/lab/rsi/runs/wave-20261001-2321pdt/BATTERY-E3/. (iv) The
BATTERY and BATTERY-CLUSTER lane directories are read-only for
this worker; their committed sources were extracted with git show
only (no working-copy reads were needed beyond the committed
docs).

## Provenance

- BATTERY-CLUSTER/CLUSTER_ANALYSIS.md: two clusters, eight
  hypotheses; E3 prioritized third (after E1, E2), described as
  "the riskiest one" in the dispatch because a FAIL reframes every
  construction claim in the wave.
- BATTERY/PREREG_POSTFREEZE.md (prereg SHA-256
  dcf5e26ac3b095565f7c89926bd63ccb14efda3061cc6985e34c436a2de8037c)
  and BATTERY/POSTFREEZE_RUN.md: PF-A2 caveat (BFS traversal
  verified against the QUERY-carried oracle value); PF-A2 bar
  FAIL.
- Frozen source: docs/lab/research-lead/overnight-20260928/
  core_freeze_tnn2_shim/freeze_shim2.zag (cognition: ev_query,
  mp_run, t2_trial, t2_try_verify masked/unmasked branches) and
  shim_driver2.zag (transport: QUERY exp passed as `expected`,
  flags=0).
