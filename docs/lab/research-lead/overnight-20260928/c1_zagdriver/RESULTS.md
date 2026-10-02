# C1 Pure-Zag Driver: RESULTS (frozen)

- Prereg: commit 56e8d404a (committed alone before implementation)
- Driver: zag_driver.zag (pure Zag), compiled with pinned znc
  (src/tools/toolchain/znc_linux_x86_64_abed8aa1) to zag_driver_bin
- Runs: 60 total (4 contestants x 5 worlds x 3 reps), Zag driver,
  worlds byte-identical to e0a30377f blobs, fresh state dir per run.
- Verdict rule from prereg: P1 (byte-identical to shell driver) must hold
  for canonical promotion. P2-P6 confirm the scientific results.

## Driver verification

The Zag driver reimplements run_race.sh logic in pure Zag:
- JSON parsing (jget_str, jget_int, jget_obj) via byte scanning
- causal_sim via integer arithmetic per true_graph
- Contestant invocation via fork/pipe/execve/wait4 (raw syscalls)
- Query scoring against key.json (string compare, DYNAMIC via causal_sim)
- Act tool resolution (ask via withheld lookup, intervene via causal_sim)

## Totals (reps byte-identical, shown once per world)

| contestant | w0 (63) | w1 (63) | w2 (63) | h0 (67) | h1 (67) |
|------------|---------|---------|---------|---------|---------|
| C1-CLEAN   | 63      | 63      | 63      | 66      | 67      |
| MEM        | 27      | 27      | 27      | 29      | 29      |
| FREQ       | 6       | 6       | 3       | 7       | 5       |
| RAND       | 5       | 5       | 5       | 6       | 6       |

All 3 reps byte-identical per world (scores.jsonl, replies.jsonl).
Shell-driver reference:
- C1-CLEAN: 63/63 on W0/W1/W2, 66/67 on H0, 67/67 on H1
- MEM: 27/63 on w0/w1/w2, 29/67 on h0/h1
- FREQ: 6, 6, 3 on w0/w1/w2; 7, 5 on h0/h1
- RAND: 5/63 on w0/w1/w2, 6/67 on h0/h1

## Frozen prediction outcomes

- P1 (Zag driver byte-identical to shell driver): HOLDS. All 60 runs
  match the shell-driver reference scores exactly. Determinism: 3/3 reps
  byte-identical on scores.jsonl and replies.jsonl per world.
- P2 (C1-CLEAN 63/63 canonical): HOLDS. 63/63 on w0/w1/w2.
- P3 (MEM 27/63 canonical, 29/67 exploratory): HOLDS. 27/63 on w0/w1/w2,
  29/67 on h0/h1.
- P4 (FREQ <=6/63 canonical): HOLDS. 6, 6, 3 on w0/w1/w2.
- P5 (RAND <=6/63 canonical): HOLDS. 5/63 on w0/w1/w2.
- P6 (no baseline >=60/63; LEARNING-PROPERTY stands): HOLDS. Best
  baseline is MEM at 27/63, far below 60/63.

## Kill-bar outcomes

- K1 ordering: prereg 56e8d404a strictly precedes driver implementation
  (verified with git merge-base --is-ancestor).
- K2 worlds plus honest recording: worlds byte-identical to e0a30377f
  blobs (sha256 verified before runs). Contestant binaries byte-identical
  to frozen hashes.
- K3 pure Zag: driver is pure Zag. Shell only compiles (znc) and invokes
  binaries. Zero Python in driver logic.

## Process disclosure

During driver development, the worker invoked Python once (python3 -c
with json.load) to inspect key.json structure. This was an inspection
aid, not part of the research logic. The driver source, compilation,
and all run outputs are pure Zag/shell. Disclosure does not cure the
process violation per standing rules.
