# Preregistration: H-CAUSAL-UNIFIED3 (Repair)

**Date:** 2026-09-29
**Hypothesis:** H-CAUSAL-UNIFIED3
**Status:** FROZEN (this commit). Implementation follows strictly after.
**Parent:** H-CAUSAL-UNIFIED2 (6ec2609da), DOWNGRADED by independent red team
  (CU2_ADV_RESULT.md, prereg a4bc16b6a).
**Toolchain:** /home/hatch/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc
**Purity:** Pure Zag. No Python anywhere (implementation, tests, analysis).

## Background

The H-CAUSAL-UNIFIED2 red team ran four attacks. X-CU2-2 (split rollback),
X-CU2-3 (flood liveness), and X-CU2-4 (source audit) passed or were
informational. X-CU2-1 succeeded and downgraded the hypothesis:

- **X-CU2-1 DOWNGRADE (conflict-bypass via continued learning):**
  After the K-CU2-2 flood (10 contradictions, contest cap 8, entries for the
  9th/10th marked ST_CONFL), the immediate post-flood query on (2,0,0)
  withholds (r=0). But feeding ONE more episode at (2,0,0), action 2,
  outcome (0,0,0) creates a FRESH entry: `find_entry` skips non-ACTIVE /
  non-AMBIGUOUS entries, so it returns -1, and `learn_episode` calls
  `new_entry`. The fresh ACTIVE entry learns the single episode with no
  memory of the contradiction. The next query returns r=1 with
  `(exact-episode)`. The contradiction (0,0,0 vs 1,1,1) is silently
  forgotten. The R2 guarantee ("explicit error plus withhold when capacity
  is exhausted") holds only if learning stops after the flood; for a
  continuing learner the withhold is not durable.

## Repair design (frozen)

New file `unified_causal3.zag`, copied byte-identical from committed
`unified_causal2.zag` at 6ec2609da, then exactly these changes.
`unified_causal2.zag` untouched. `main()` kept byte-identical.

**R1 (X-CU2-1): durable conflict marking.** Add `find_conflicted`, a pure
query mirroring `find_entry` but matching only ST_CONFL() entries (most
specific match wins, same specificity rule). In `learn_episode`, when
`find_entry` returns -1, check `find_conflicted(W,a,s0,s1,s2)` before
creating a fresh entry:

- If a conflicted entry covers (a, state): absorb the episode into that
  entry via `entry_add_ep`, keep ST_CONFL(), emit an explicit note
  (`ENTRY action A [cond] CONFLICTED-ABSORB: episode kept under conflict
  at seq S (WITHHOLD preserved)`), and return. No contest is opened, no
  effects are recomputed, no fresh entry is created. Queries keep
  withholding through the existing no-entry path (`find_entry` skips
  conflicted entries), and the contradiction evidence stays grouped with
  the conflicted entry instead of being silently forgotten.
- If no conflicted entry covers the state: the existing fresh-entry path
  runs unchanged.

Per-entry episode-list guard (new, disclosed): the absorb path checks
`en_neps(W,cf)>=64` first. On overflow it emits an explicit error
(`ERROR: conflicted-entry episode list full (64); episode refused at seq S
(WITHHOLD preserved)`) and returns without adding. This avoids writing
past the 64-slot per-entry episode region. The normal (non-conflicted)
path keeps its pre-existing disclosed 64-episode bound unchanged; this
repair does not alter it.

Why absorb rather than inherit-on-create: absorbing keeps all episodes
for the conflicted (action, state) region in one entry, so a future
contest-eviction policy (explicit non-goal, future work) can adjudicate
from complete evidence. Creating fresh conflicted entries would fragment
the evidence across entries.

**Explicit non-goals:** Capacities stay 8/32/128. No contest eviction or
merging policy is invented here. Conflicted entries never become ACTIVE
again in this repair; un-conflicting is future work. The dead
`en_st(W,i)==ST_CONFL()` branch in `predict` (unreachable because
`find_entry` never returns conflicted entries) is left untouched to keep
the diff minimal.

## Frozen kill bars

- **K-CU3-1 (durable withhold):** Exact X-CU2-1 replication on the repaired
  binary: flood 10 contradictions at the 10 K-CU2-2 states, action 2,
  outcomes (0,0,0) vs (1,1,1). Require: (a) 9th/10th emit the explicit
  contest-capacity error, nct stays 8; (b) immediate post-flood query on
  (2,0,0) returns r=0; (c) record nent; feed one more episode at (2,0,0),
  action 2, outcome (0,0,0); require the CONFLICTED-ABSORB note is emitted;
  (d) nent is unchanged (no fresh entry created); (e) post-bypass query on
  (2,0,0) returns r=0 (WITHHOLD), never r=1.
- **K-CU3-2 (regression):** The repaired binary run on the frozen main
  produces output byte-identical to the committed unified_causal2 main
  output (caps are not reached in the frozen run, so the new path never
  triggers). All 28 PASS markers present, 0 FAIL markers.
- **K-CU3-3 (determinism):** 3 runs of the repaired main byte-identical
  via cmp; 3 runs of the K-CU3-1 driver byte-identical via cmp.
- **K-CU3-4 (explicitness audit):** Source audit confirms: the absorb path
  always emits its note; the 64-overflow path always emits its error; no
  new silent -1 or silent-drop path is introduced; `find_conflicted` is a
  pure query with no store mutation.

## Kill criteria

- K-CU3-1 fails (post-bypass r=1, or nent grows, or no absorb note) ->
  H-CAUSAL-UNIFIED3 KILLED.
- K-CU3-2 fails (any output diff vs the committed v2 main output, any
  missing PASS, any FAIL) -> H-CAUSAL-UNIFIED3 KILLED.
- K-CU3-3 fails -> H-CAUSAL-UNIFIED3 KILLED.
- K-CU3-4 fails (a silent path is found in the new code) ->
  H-CAUSAL-UNIFIED3 DOWNGRADED.

## Artifacts (to be committed after execution)

- PREREG_CAUSAL_UNIFIED3.md (this file)
- unified_causal3.zag (repaired implementation)
- CU3_RAW_MAIN.txt (3 runs, md5)
- CU3_RAW_BYPASS.txt (K-CU3-1 driver, 3 runs, md5)
- CU3_RESULT.md (result doc)

Commit order: prereg (this commit) strictly before implementation commit.
Only owned files staged. No binaries committed. Pure Zag.
