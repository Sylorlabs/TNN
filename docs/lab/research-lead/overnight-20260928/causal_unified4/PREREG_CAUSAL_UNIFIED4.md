# H-CAUSAL-UNIFIED4 Preregistration (FROZEN)

**Date:** 2026-09-29
**Hypothesis:** H-CAUSAL-UNIFIED4 (frontier: principled un-conflicting)
**Parent:** H-CAUSAL-UNIFIED3 SURVIVES (6/6 + 28/28); red team CU3_ADV SURVIVES, all 4 attacks hold.
**Toolchain:** /home/hatch/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc (znc 2026.07.0-dev, edition 2026)
**Purity:** Pure Zag. No Python at any stage (implementation, drivers, analysis, file ops).

## Problem statement

H-CAUSAL-UNIFIED3 closes X-CU2-1 (durable conflict marking via
CONFLICTED-ABSORB) but leaves a disclosed permanent blackhole: a ST_CONFL
entry can never learn again, even under unlimited consistent later
evidence. The CU3 red team confirmed this as an explicit BOUNDARY
(X-CU3-1c: 20 absorbed consistent episodes, permanent withhold) and named
un-conflicting as the natural next step. This hypothesis builds the
principled adjudication path.

## Frozen design

New pure function `conflict_adjudicate(W, cf, s0, s1, s2, seq)`, called at
the end of the CONFLICTED-ABSORB path in `learn_episode`, after the absorb
emit. It tallies live (non-EP_SUP) episodes of the conflicted entry `cf`
at the exact state (s0,s1,s2):

- 3 or more distinct outcome triples at the exact state: return 0. The
  entry stays ST_CONFL. Explicit frozen boundary (messy contradiction).
- Fewer than 2 distinct outcomes: return 0. Nothing to adjudicate.
- Exactly 2 distinct outcomes A (support sa) and B (support sb): apply the
  frozen `contest_feed` resolution criterion verbatim. If (sa>=2 and sa>sb)
  then A wins; else if (sb>=2 and sb>sa) then B wins; else return 0.

On resolution the function mirrors the `contest_feed` RESOLVE path:

1. All live loser-outcome episodes at the exact state are marked EP_SUP.
2. The entry is set ST_ACTIVE.
3. Effects are recomputed via `effects_over` (excl=cf); if unresolved,
   `split_attempt` runs (a split-failure conflict re-conflicts here, with
   its own explicit trace); then `merge_pass` runs.
4. An explicit UNCONFLICT trace is emitted naming action, cond, state, seq,
   winner outcome and support, loser outcome and support, and the
   supersession. No silent path: absorb still emits CONFLICTED-ABSORB first,
   and UNCONFLICT fires only on actual adjudication.

Rationale for the contest criterion: the untracked contradiction inside a
contest-capacity conflicted entry is exactly contest-shaped (two outcomes
at one state). The mechanism's own definition of "enough evidence to call
a law change" is support>=2 with strict majority (`contest_feed`). Any
other bar would be researcher fiat. This is the least-arbitrary choice,
and it introduces no new vulnerability class: a tracked contest resolves
on the same evidence.

Scope notes (frozen):

- Adjudication applies uniformly to all ST_CONFL sources. For a
  split-failure conflict, superseding losers and recomputing will normally
  re-conflict via `split_attempt`; that is honest and self-consistent.
- The 64-episode per-entry guard is unchanged and still refuses before
  absorb.
- `find_conflicted` is untouched (still a pure query).
- The F2 invariant from CU3_ADV is restated, not weakened: ST_CONFL entries
  may now contain EP_SUP episodes, but only as the explicit product of an
  UNCONFLICT adjudication. The property that matters is preserved and
  frozen: adjudication always leaves the winner's episodes live, so the
  `find_conflicted` exact-state live-episode requirement can never be
  defeated by supersession. A re-conflicted entry (ST_CONFL again after a
  later contradiction) still holds live episodes at the exact state, so
  later absorbs still take the absorb path (nent stable).

## Frozen kill bars

### K-CU4-1 (un-conflict works, principled)

Driver: the exact CU3 flood (20 episodes, action 2, states
(0,0,0)..(1,1,1) then (2,0,0) seq 17/18 and (2,0,1) seq 19/20; odd seqs
outcome (0,0,0), even seqs (1,1,1)).

- K-CU4-1a: flood opens 8 contests (nct=8); two untracked contradictions
  mark entries ST_CONFL at seq 18 and seq 20 with explicit traces. PASS.
- K-CU4-1b: immediate post-flood query Q(2,0,0,2) returns r=0. The withhold
  is intact before new evidence. PASS.
- K-CU4-1c: absorb episode at (2,0,0) outcome (0,0,0) (seq 21) emits
  CONFLICTED-ABSORB, then UNCONFLICT: tally (0,0,0) support 2 vs (1,1,1)
  support 1, winner (0,0,0), loser seq 18 SUPERSEDED. nent unchanged.
  PASS (grep for the UNCONFLICT line).
- K-CU4-1d: post-adjudication query Q(2,0,0,2) returns r=1 predicting
  (0,0,0). The withhold is retired BY EVIDENCE, explicitly. PASS.
- K-CU4-1e: the untouched (2,0,1) conflicted entry still withholds:
  Q(2,0,1,2) returns r=0. Adjudication is scoped to the state with
  evidence. PASS.

Explicit supersession: old K-CU3-1d ("post-bypass query still withholds
r=0") is SUPERSEDED by K-CU4-1d. This is a new frozen bar for a new
hypothesis, not a retroactive alteration of the CU3 verdict.

### K-CU4-2 (X-CU2-1 still closed; no silent-forget)

- K-CU4-2a: nent never increases at any point in the K-CU4-1 driver. No
  fresh entry is ever created at the conflicted state; the absorb path is
  preserved. PASS.
- K-CU4-2b: the now-ACTIVE entry holds an EP_SUP episode at the exact
  state (the seq-18 loser), and the UNCONFLICT trace names the superseded
  loser. The contradiction history is explicitly retired, not silently
  forgotten. PASS.
- K-CU4-2c: feed a re-contradiction at (2,0,0) outcome (1,1,1) after
  adjudication. It takes the normal ACTIVE path (find_entry returns the
  entry), opens no contest (cap still exhausted), and the entry is marked
  ST_CONFL again with the explicit "contradiction untracked (contest cap)"
  trace; query Q(2,0,0,2) returns r=0. Then one more (1,1,1) episode is
  absorbed (nent stable), proving `find_conflicted` still covers the
  re-conflicted entry. The machinery keeps working; nothing is silently
  dropped. PASS.

### K-CU4-3 (messy boundary stays conflicted)

Separate driver: same flood, then absorb one episode at (2,0,0) with a
THIRD outcome (2,2,2).

- K-CU4-3a: no UNCONFLICT emit (grep count 0). PASS.
- K-CU4-3b: query Q(2,0,0,2) returns r=0; entry still ST_CONFL. PASS.

### K-CU4-4 (regression)

Repaired `main()` output byte-identical to committed CU3_RAW_MAIN.txt
(md5 87f8edc29825802327029f46f045dbe3): 28 PASS markers, 0 FAIL. The new
path never triggers in the frozen run. PASS.

### K-CU4-5 (determinism)

3/3 byte-identical runs of each new driver; 3/3 of the repaired main.
PASS.

### K-CU4-6 (explicitness audit)

- (a) The UNCONFLICT emit fires only on actual adjudication (code path
  review plus K-CU4-3a zero-count).
- (b) `conflict_adjudicate` mutates the store only through the documented
  resolution path (loser supersession, ST_ACTIVE, recompute).
- (c) No new silent path: every absorb still emits CONFLICTED-ABSORB; the
  64-guard still emits its ERROR.
- (d) `find_conflicted` remains a pure query (zero `_set` calls).

## Mapping to K-CU3 bars

- K-CU3-1a (flood nct=8): still PASS (K-CU4-1a).
- K-CU3-1b (immediate withhold): still PASS (K-CU4-1b).
- K-CU3-1c (no fresh entry on bypass): still PASS (K-CU4-2a).
- K-CU3-1d (post-bypass withhold r=0): SUPERSEDED by K-CU4-1d (new bar).
- K-CU3-1e (second bypass withhold): SUPERSEDED (entry is ACTIVE after
  adjudication; later episodes take the normal path).
- K-CU3-1f (fresh-state learning intact): still PASS (fresh-entry path
  untouched; covered by K-CU4-4 regression plus a fresh-state check in the
  driver).
- K-CU3-2 (regression): still PASS (K-CU4-4).
- K-CU3-3 (determinism): still PASS (K-CU4-5).
- K-CU3-4 (explicitness): still PASS (K-CU4-6).

## Verdict rule

SURVIVES iff K-CU4-1 through K-CU4-6 all PASS. Any FAIL is a KILL or
DOWNGRADE per the frozen bar it violates. No bar may be altered after
results.

## Deliverables (this hypothesis, branch tnn-native-lab)

- causal_unified4/PREREG_CAUSAL_UNIFIED4.md (this file)
- causal_unified4/unified_causal4.zag (implementation)
- causal_unified4/cu4_test.zag (K-CU4-1/2/3 driver; mechanism lines
  byte-verbatim from unified_causal4.zag, only main replaced)
- causal_unified4/CU4_RAW_MAIN.txt (regression, 3/3 identical)
- causal_unified4/CU4_RAW_TEST.txt (new-bar driver, 3/3 identical)
- causal_unified4/CU4_RESULT.md (result)
