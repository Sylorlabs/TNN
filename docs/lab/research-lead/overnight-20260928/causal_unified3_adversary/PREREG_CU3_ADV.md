# Preregistration: H-CAUSAL-UNIFIED3 Red Team (CU3_ADV)

**Date:** 2026-09-29
**Target:** H-CAUSAL-UNIFIED3 (unified_causal3.zag, result commit per CU3_RESULT.md)
**Status:** FROZEN (this commit). All attack code is written and run strictly after.
**Toolchain:** /home/hatch/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc
**Purity:** Pure Zag. No Python anywhere (fixtures, harnesses, analysis, file ops).

## Mission

Assume the H-CAUSAL-UNIFIED3 SURVIVES claim is false. Attack the repair:
durable conflict marking via `find_conflicted` + CONFLICTED-ABSORB,
exact-state scoped per AMEND1.

## Background facts established by code reading (pre-freeze)

- F1: `find_entry` (line 1331) returns only ST_ACTIVE or ST_AMBIGUOUS
  entries. `predict` withholds via the no-entry path for conflicted states.
- F2: The sole EP_SUP writer is `contest_feed` (line 1776), reachable only
  through the ACTIVE path of `learn_episode`. A ST_CONFL entry is never the
  ACTIVE `i`, so its episodes can never be superseded via contest
  resolution. `merge_pass` only merges ST_ACTIVE entries (line 1824), so
  conflicted entries are never merged away either.
- F3: ST_CONFL is set on three paths: contest-cap exhaustion in
  `learn_episode` (line 1979), split-failure `cands==0` in `split_attempt`
  (line 1633), all-candidates-refuted in `amb_update` (line 1692).
- F4: The absorb block (lines 1920-1939) emits CONFLICTED-ABSORB on absorb
  and an explicit ERROR on the 64-episode guard; both returns follow an
  emit. The episode-cap (128) refusal in `fu_learn_ep` is explicit.
- F5: `find_conflicted` requires en_st==ST_CONFL, en_a==a, cond_matches==1,
  AND at least one live (non-EP_SUP) episode at the exact (s0,s1,s2).

## Attacks

### X-CU3-1 (Absorb correctness)

- **X-CU3-1a (exact X-CU2-1 replay):** Flood 10 contradictions at action 2
  (states (0,0,0)..(1,1,1) then (2,0,0),(2,0,1), outcomes (0,0,0) vs
  (1,1,1)), then feed one more episode at (2,0,0), action 2, outcome
  (0,0,0). Require: CONFLICTED-ABSORB emitted, nent unchanged, post-bypass
  `fu_predict` returns 0. Kill criterion: r=1, or nent grows, or no absorb
  note -> **H-CAUSAL-UNIFIED3 KILLED**.
- **X-CU3-1b (superseded-evasion):** Attempt to build a ST_CONFL entry
  whose exact-state episodes are all EP_SUP while the entry stays
  ST_CONFL, then feed at that exact state. Per F2 this is predicted
  UNREACHABLE. Empirical attempt: open a contest on an ACTIVE entry, drive
  the entry to ST_CONFL via split-failure while the contest is orphaned,
  then feed at the exact state and observe. Kill criterion: a fresh ACTIVE
  entry is created and `fu_predict` returns 1 at the exact contradicted
  state -> **H-CAUSAL-UNIFIED3 KILLED**. If absorb fires (episodes never
  superseded) -> holds, F2 confirmed empirically.
- **X-CU3-1c (dead-zone permanence):** After the X-CU3-1a flood, feed 20
  consistent episodes at (2,0,0), action 2, outcome (0,0,0). The prereg
  discloses "conflicted entries never become ACTIVE again; un-conflicting
  is future work". Require: all 20 absorbed with notes, every query r=0.
  Kill criterion: withhold flips to confident (r=1) -> **KILLED**
  (contradicts the disclosed design). If durable -> **BOUNDARY**
  (disclosed honest limit confirmed, documented as permanent learning
  blackhole under sustained consistent evidence).

### X-CU3-2 (Scope: exact-state per AMEND1)

- **X-CU3-2a (mask-covered new state):** After the flood, feed at (2,0,2),
  action 2 (matches the mask-0 conflicted entry's condition, no live
  exact-state episode). Require: fresh-entry path (no CONFLICTED-ABSORB),
  normal learning. Kill criterion: absorbed -> **DOWNGRADED** (over-absorb
  breaks AMEND1 scoping).
- **X-CU3-2b (same state, different action):** Feed at action 3, state
  (2,0,0) with contradictory outcomes. Require: fresh-entry path
  (en_a differs). Kill criterion: absorbed -> **DOWNGRADED**.
- **X-CU3-2c (exact state, third outcome):** Feed at (2,0,0), action 2,
  outcome (5,5,5) (matches neither contradiction outcome). Require:
  CONFLICTED-ABSORB (absorb is outcome-agnostic per the frozen design).
  Kill criterion: fresh ACTIVE entry created -> **KILLED** (under-absorb is
  an X-CU2-1 variant).
- **X-CU3-2d (split-failure ST_CONFL path, informational):** Attempt to
  drive an entry to ST_CONFL via `split_attempt` cands==0 (F3), then feed
  at its exact state. Document whether absorb fires. No kill criterion;
  classifies whether the repair treats all three ST_CONFL paths uniformly.

### X-CU3-3 (Regression)

Recompile the committed unified_causal3.zag unmodified; run the frozen
main 3 times; require md5 equal to the committed CU3_RAW_MAIN.txt
(87f8edc29825802327029f46f045dbe3). Rebuild the K-CU3-1 driver from my
harness and require 6/6. Kill criterion: any byte difference or any
driver check failure -> **KILLED**.

### X-CU3-4 (Source audit)

- (a) `find_conflicted` body contains no `_set` call (pure query).
- (b) Every `return` in the absorb block textually follows an `emit`.
- (c) No test-answer literals in the 54 added lines (diff hunks only).
- (d) `main()` byte-identical between unified_causal2.zag and
  unified_causal3.zag.
- (e) `find_conflicted` has exactly one call site (`learn_episode`).
Kill criterion: any failure -> **DOWNGRADED**.

## Verdict rule

- Any KILL criterion fires -> H-CAUSAL-UNIFIED3 KILLED.
- Any DOWNGRADE criterion fires (and no KILL) -> H-CAUSAL-UNIFIED3 DOWNGRADED.
- X-CU3-1c durable -> recorded as BOUNDARY (disclosed limit), not a kill.
- X-CU3-2d is informational regardless of outcome.
- Otherwise -> H-CAUSAL-UNIFIED3 SURVIVES this red team.

## Artifacts (committed after execution)

- PREREG_CU3_ADV.md (this file)
- cu3_adv.zag (attack harness: mechanism lines 1-2328 byte-verbatim + attack main)
- CU3_ADV_RAW.txt (3/3 byte-identical runs, md5)
- CU3_ADV_RESULT.md (adversary report)

Commit order: this prereg strictly before any attack execution.
Only owned files staged. No binaries committed. No em dashes.
