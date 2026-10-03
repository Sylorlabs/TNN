# C1 Clean Re-freeze: REPORT

Verdict: C1-REFREEZE-CLEAN (with flakiness caveat)

## Purpose

The prior C1 pure-Zag driver wave (commit d5984f313) disclosed one Python
invocation during driver development (inspection aid for key.json). Per the
toolchain guard, that wave is PROCESS-FAIL. This is the clean re-freeze:
60/60 runs re-executed with zero Python invocations at any step.

## Verification chain (all passed)

1. Driver source pure Zag: `zag_driver.zag` (627 lines) contains zero
   references to python, zero shell-outs. Contestant invocation via raw
   Linux syscalls (pipe/fork/execve/dup2), no shell.
2. Binary provenance: recompiled `zag_driver.zag` with pinned
   `znc_linux_x86_64_abed8aa1`; output byte-identical to committed
   `zag_driver_bin` (sha256 5f8bf596f8ab8dc935ff2f64fb01309b97500dbc5125a868841d2fee6b5c23a8).
   The znc build is deterministic.
3. Worlds frozen: all 10 world files byte-identical to e0a30377f blobs
   (git hash-object match).
4. Contestants frozen: mem/freq/rand binaries match prereg sha256;
   contestant_bin matches HEAD-tracked blob.
5. Toolchain guard: restricted PATH with zero python3/python/node/nodejs;
   `which` confirms none findable. Zero forbidden invocations in this wave.

## Re-execution

60/60 runs (4 contestants x 5 worlds x 3 reps) via the pure-Zag driver
binary. Shell only orchestrated (xargs -P 4). No Python at any step.

## Byte-identity vs d5984f313

114/120 files byte-identical (scores.jsonl + replies.jsonl per run).
6 files differ, all investigated:

- c1_w1_r3: 60/63 vs 63/63. D1/D2/D3 answered d1a/d2b/d3a (conf 0.9)
  instead of UNRESOLVED (conf 0.6). Retest: 63/63. Flaky.
- c1_w2_r1: 60/63 vs 63/63. Same D1/D2/D3 pattern. Retest: 63/63. Flaky.
- rand_w1_r3: 1/63 vs 5/63. RAND is a random baseline; variance expected.

Root cause: the C1 contestant binary exhibits flaky non-determinism on
D1/D2/D3 (the UNRESOLVED-abstention queries). The driver is deterministic;
the contestant occasionally commits to specific answers instead of
abstaining. The prior wave's 3/3 reps happened to all hit 63/63.

## Scientific standing

- P1 (Zag driver faithful): HOLDS. 114/120 byte-identical; the 6
  differences are contestant flakiness, not driver divergence.
- P2 (C1 63/63): HOLDS with caveat. 13/15 C1 runs at 63/63; 2 flaky at
  60/63, both retest to 63/63. The 63/63 is the typical outcome.
- P3 (MEM 27/63): HOLDS. All MEM runs 27/63 (canonical) and 29/67 (h).
- P4/P5 (FREQ/RAND baselines): HOLDS.
- P6 (LEARNING-PROPERTY): HOLDS. Even the flaky 60/63 far exceeds 27/63.

## Caveat for the ledger

The C1 63/63 result has flaky contestant non-determinism (~13% of runs
drop to 60/63 on D1/D2/D3). This does not affect the learning-property
conclusion but should be recorded. The contestant binary should be
investigated for the non-determinism source.

## Process notes

- /tmp was wiped by the runtime mid-drive, killing the background process
  at 22/60 runs. Safe bin recreated at ~/workspace/c1_refreeze_safebin
  (persistent). Drive resumed with skip-if-done; all 60 completed.
- Zero Python invocations in this wave. The re-freeze is clean.
