# Preregistration: H-CAUSAL-UNIFIED2 (Repair)

**Date:** 2026-09-29
**Hypothesis:** H-CAUSAL-UNIFIED2
**Status:** FROZEN (this commit). Implementation follows strictly after.
**Parent:** H-CAUSAL-UNIFIED (ba065e172), DOWNGRADED by independent red team
  (ADV_CAUSAL_UNIFIED_RESULT.md, prereg ae0c3e0d0).
**Toolchain:** /home/hatch/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc
**Purity:** Pure Zag. No Python anywhere (implementation, tests, analysis).

## Background

The H-CAUSAL-UNIFIED red team met two kill criteria and two downgrades:

- **X-CU1 KILL (provenance gaming):** `fu_hist_count` displays ENTRIES via
  `list_hypos` but counts EPISODES with `EP_SUP()`. Frozen output shows 4
  SUPERSEDED entries (H2, H6, H7, H8) while CAUSHIST reports superseded=2.
  The K-CU3 "decorative provenance repaired" claim is INVALID.
- **X-CU2 KILL (contest flooding):** When 8 contests are open, the 9th and 10th
  contradictions are silently dropped (`new_contest` returns -1, caller
  ignores it). Query on the dropped state returns a confident prediction
  (r=1) instead of withhold.
- **X-CU3 DOWNGRADE (entry cap):** `new_entry` returns -1 at 32 entries;
  `split_attempt`/`apply_split` and `learn_episode` failure paths are silent
  or leave partial state.
- **X-CU4 DOWNGRADE (doc error):** "127 machinery functions" should be 126.
  Port itself faithful; count claim wrong.

## Repair design (frozen)

New file `unified_causal2.zag`, copied from committed `unified_causal.zag`
at ba065e172, then exactly these changes. `unified_causal.zag` untouched.

**R1 (X-CU1):** `fu_hist_count` counts ENTRIES with `ST_SUPER()` over
`nent(W)` instead of EPISODES with `EP_SUP()` over `nep(W)`. Doc comment
corrected to "return the number of SUPERSEDED entries". The CAUSHIST line
then agrees with the listing it just emitted.

**R2 (X-CU2):** `new_contest` emits an explicit error on the -1 path naming
the state, e.g. `ERROR: contest capacity (8) exhausted; contradiction at
state (s0 s1 s2) has no contest slot`. In `learn_episode`, a -1 from
`new_contest` marks the entry `ST_CONFL()` and emits
`ENTRY ... CONFLICTED: contradiction untracked (contest cap)`, then
returns. `predict` already withholds on ST_CONFL entries (and `find_entry`
skips non-ACTIVE/AMBIGUOUS entries), so queries on the flooded state
withhold instead of predicting confidently. The K-CU5 guarantee becomes:
explicit contest plus withhold when a slot exists; explicit error plus
withhold when capacity is exhausted. No silent evidence loss.

**R3 (X-CU3):** `new_entry` emits an explicit error on the -1 path
(`ERROR: entry capacity (32) exhausted`). `apply_split` saves `nent(W)`
before creating children; on any child `new_entry` -1 it restores nent
(rolling back partial children), emits an explicit error, and returns 0.
`learn_episode`'s existing `if(i<0){return;}` now follows an already-emitted
error. `fu_learn_ep` emits an explicit error on the 128-episode cap
(`ERROR: episode capacity (128) exhausted`) instead of silently returning -1.

**R4 (X-CU4):** Result doc states 126 shared machinery functions, not 127.

**Explicit non-goals:** Capacities stay 8/32/128. No contest eviction or
merging policy is invented here; exhaustion is made explicit, not silent.
That is the honest bounded fix. Eviction policy is future work.

## Frozen kill bars

- **K-CU2-1 (provenance consistency):** After the frozen phase-C2 stream,
  the CAUSHIST superseded count EQUALS the number of SUPERSEDED entries in
  the hypotheses listing emitted just above it. (Was 2 vs 4; must agree.)
- **K-CU2-2 (flood withhold):** 10 contradictions at 10 distinct states
  (adversary pattern: states (0,0,0),(0,0,1),(0,1,0),(0,1,1),(1,0,0),
  (1,0,1),(1,1,0),(1,1,1),(2,0,0),(2,0,1), action 2, outcomes (0,0,0) vs
  (1,1,1)). The 9th and 10th emit the explicit capacity error. nct stays 8.
  A query on the 9th-contradiction state (2,0,0,2) returns r=0 (WITHHOLD),
  never a confident prediction.
- **K-CU2-3 (regression):** The repaired binary run on the frozen main
  produces all 28 PASS markers present in unified_causal/run_a.txt and 0
  FAIL markers. The only permitted output difference vs run_a.txt is the
  corrected CAUSHIST superseded count (2 -> 4); no new error emissions may
  appear in the frozen run (caps are not reached there).
- **K-CU2-4 (determinism):** 3 runs of the repaired main byte-identical
  via cmp; 3 runs of the flood test byte-identical via cmp.
- **K-CU2-5 (entry-cap audit):** A unit driver calls new_entry in a loop to
  the 32-entry cap and observes the explicit error emission; source audit
  confirms apply_split restores nent on child-allocation failure and that
  no new_entry/new_contest -1 path remains silent.

## Kill criteria

- K-CU2-1 fails (count still disagrees with listing) -> H-CAUSAL-UNIFIED2 KILLED.
- K-CU2-2 fails (confident prediction on flooded state, or no explicit
  error on 9th/10th contradiction) -> H-CAUSAL-UNIFIED2 KILLED.
- K-CU2-3 fails (any previously-passing check now fails, or unexpected
  output diffs beyond the corrected count) -> H-CAUSAL-UNIFIED2 KILLED.
- K-CU2-4 fails -> H-CAUSAL-UNIFIED2 KILLED.
- K-CU2-5 fails (a silent -1 path remains) -> H-CAUSAL-UNIFIED2 DOWNGRADED.

## Artifacts (to be committed after execution)

- PREREG_CAUSAL_UNIFIED2.md (this file)
- unified_causal2.zag (repaired implementation)
- unified_causal2/RESULT_CAUSAL_UNIFIED2.md
- unified_causal2/CU2_RAW_MAIN.txt (3 runs, md5)
- unified_causal2/CU2_RAW_FLOOD.txt (3 runs, md5)
- unified_causal2/CU2_RAW_ENTRYCAP.txt (unit driver output)

Commit order: prereg (this commit) strictly before implementation commit.
Only owned files staged. No binaries committed.
