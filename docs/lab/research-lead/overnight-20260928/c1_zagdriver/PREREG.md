# PREREG: C1 Pure-Zag Race Driver Re-run

Date: 2026-09-30 UTC
Status: FROZEN (committed alone before any implementation).

## Question

Does the C1 family result reproduce under a pure-Zag race driver?
The tooling audit (70c520637) found the entire C1 family contaminated
by the shell driver (run_race.sh implements JSON parsing, causal
simulation, and query scoring in shell). This re-run replaces the
shell driver with a pure-Zag implementation and re-executes the
contestant and baselines. If the numbers match, the contamination
was in the tooling only, not the scientific result.

## Frozen worlds

Reuse byte-identical worlds from commit e0a30377f
(docs/lab/research-lead/overnight-20260928/c1_clean/worlds/):
w0, w1, w2 (canonical), h0, h1 (exploratory consistency only).
World files are verified by sha256 against the e0a30377f blobs before
any run; worlds are never regenerated or modified.

## Frozen contestants

- C1-CLEAN contestant: docs/lab/research-lead/overnight-20260928/c1_clean/contestant_bin
  (from the C1-CLEAN freeze; 63/63 on W0/W1/W2 under the shell driver).
- B1 MEM: docs/lab/research-lead/overnight-20260928/c1_baseline/mem_bin
  (freeze 11b957715; sha256 aad8d533e52fd969723742ba09aad6c6110c4a571d84c6d2b26a2e732f78216a).
- B2 FREQ: docs/lab/research-lead/overnight-20260928/c1_baseline/freq_bin
  (freeze 11b957715; sha256 59a0e7ae7ec44aa3010693d9245e49a05817150dfc94a2b27df73a9f39458e44).
- B3 RAND: docs/lab/research-lead/overnight-20260928/c1_baseline/rand_bin
  (freeze 11b957715; sha256 0d562d69fe516e4f5f6df95108f61f86dd939a18898b2ab09e69866f57152fd7).

Binaries are invoked, never rebuilt. Interface: binary takes
<turn.json> <statedir>, prints one JSON reply line on stdout.

## The Zag driver (to be implemented after this prereg)

A pure-Zag program implementing the run_race.sh logic:

1. Parse key.json: extract true_graph (integer), build query map
   (qid to expected string; "DYNAMIC" for causal queries).
2. Read turns.jsonl line by line.
3. For each turn, write turn.json, invoke the contestant binary
   (fork/exec via raw syscalls, capture stdout via pipe), parse reply.
4. Turn kinds:
   - brief/save/load/end: invoke, record reply.
   - obs: if ev.t is "cobs", update causal state (BP, BQ, BR) from
     ev.P/Q/R. Invoke, record reply.
   - query: invoke, extract "answer" from reply, compare to expected
     (from key.json, or DYNAMIC via causal_sim on the turn's q.do/q.val,
     selecting q.ask component). Record score.
   - act: loop with budget 3. Invoke. If reply contains "tool", resolve:
     ask: look up qid in key.json withheld section, return the object.
     intervene: run causal_sim with var/val, update BP/BQ/BR, return
     cobs object. Send toolresult turn, continue. Else break.
5. causal_sim(tg, p, q, r, dv, vv): set the dv component to vv, then
   propagate per the true graph:
   - tg 0: if dv != Q then q = p; if dv != R then r = q.
   - tg 1: if dv != R then r = p; if dv != Q then q = r.
   - tg 2: if dv != P then p = q; if dv != R then r = p.
6. Write scores.jsonl, replies.jsonl, stage_scores.txt, costs.txt
   in the same format as run_race.sh.

Pure Zag only for parsing, simulation, scoring. Shell only invokes
znc to compile the driver and runs the driver binary.

## Runs

4 contestants x 5 worlds x 3 reps = 60 runs.
Each run starts with a fresh state dir.
Determinism: 3/3 reps per (contestant, world) must be byte-identical
on replies.jsonl and scores.jsonl (costs.txt may differ on wall_ms).

## Frozen predictions

- P1: The Zag driver produces byte-identical scores.jsonl to the
  shell driver for all 60 runs (modulo wall_ms in costs.txt).
  Rationale: the driver is a faithful reimplementation; any divergence
  is a driver bug, not a contestant property.
- P2: C1-CLEAN scores 63/63 on w0/w1/w2, 66/67 on h0, 67/67 on h1,
  matching the shell-driver result.
- P3: MEM scores 27/63 on w0/w1/w2, 29/67 on h0/h1.
- P4: FREQ scores at most 6/63 on any canonical world.
- P5: RAND scores at most 6/63 on any canonical world.
- P6: No baseline reaches 60/63 on any canonical world
  (verdict C1-BASELINE-LEARNING-PROPERTY stands).

## Kill bars

- K1: This prereg commit strictly precedes the driver implementation
  commit (verified with git merge-base --is-ancestor).
- K2: Worlds byte-identical to e0a30377f blobs (sha256 verified
  before runs). Contestant binaries byte-identical to frozen hashes.
- K3: Zero Python at any step. Driver is pure Zag. Shell only
  compiles (znc) and invokes binaries.
