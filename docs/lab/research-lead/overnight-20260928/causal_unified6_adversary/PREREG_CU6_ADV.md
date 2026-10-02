# PREREG H-CAUSAL-UNIFIED6 RED TEAM FROZEN

**Date:** 2026-09-29
**Adversary:** H-CAUSAL-UNIFIED6 Red Team (independent subagent)
**Target:** H-CAUSAL-UNIFIED6 SURVIVES (5/5). Prereg `2f48dd7e1`,
result `438c3344a`. Repair: `live_contra_at` helper + predict guard.
**Toolchain:** znc 2026.07.0-dev (edition 2026). Pure Zag. No Python
in prereg, fixtures, builds, runs, analysis, or scratch.
**Mission:** assume the repair is false. Attack it.

## Background analysis (frozen)

The guard fires iff a ST_CONFL entry for the queried action holds
2+ distinct live (non-EP_SUP) outcomes at the exact query state.
`conflict_adjudicate` sets messy=1 and refuses to carve when 3+
distinct outcomes exist, so a 3-outcome ST_CONFL entry is permanent
and the guard's third-outcome early-return is its only protection.
`contest_feed` ignores third outcomes
(`if(o<0){return 0;} // third outcome: not expected; ignore`),
so 3-outcome entries are constructible via CONFLICTED-ABSORB.
The builder tested only 2-outcome contradictions (K-CU6-1) and
adjudicated carves (K-CU6-2). The following attacks probe untested
paths.

## Attack X-CU6-1: three-outcome contradiction (KILL if guard misses)

Construction (mirrors builder K-CU6-1, plus a third outcome):
1. 20-episode flood on action 2 (builder K-CU6-1 fixture).
2. Carve at (2,0,0) via `2,0,0,2>0,0,0`.
3. Re-contradiction via `2,0,0,2>1,1,1` (carved entry -> ST_CONFL).
4. Third outcome via `2,0,0,2>2,2,2` (absorbed into ST_CONFL;
   adjudication messy, stays ST_CONFL with 3 live outcomes).
5. Fresh general entry via `2,0,2,2>7,7,7`.
6. Query (2,0,0).

PASS (defense holds) requires: r=0 with `WITHHOLD
(live-contradiction)` in raw, and an adversary helper confirms the
ST_CONFL entry holds 3 distinct live outcomes at (2,0,0).
KILL requires: query returns r=1 (the guard's third-outcome path is
broken; a live 3-way contradiction is shadowed).

## Attack X-CU6-2: tombstone chain robustness (KILL if guard misses)

Construction:
1. Steps 1-3 of X-CU6-1 (carved entry -> ST_CONFL with 2 outcomes
   at (2,0,0)).
2. Learn supporting episodes for a re-carve attempt at (2,0,0)
   from the oldest tombstone (tests oldest-first tie-break routing).
3. Fresh general entry via `2,0,2,2>7,7,7`.
4. Query (2,0,0) and (2,0,2).

PASS requires: (2,0,0) withholds (r=0, live-contradiction) unless
a legitimate adjudication retired the contradiction (in which case
the raw must show the carve and the guard correctly silent);
(2,0,2) predicts r=1 via the general entry (guard exact-state
scoped).
KILL requires: (2,0,0) returns r=1 while a ST_CONFL entry still
holds 2+ distinct live outcomes there (helper confirms).

## Attack X-CU6-3: untracked contradiction (contest cap) + shadow

Construction:
1. Open 8 tracked contests at 8 distinct states (exhaust contest
   capacity of 8).
2. At state S=(4,0,0): learn outcome A, then outcome B ->
   contradiction untracked (new_contest returns -1), entry marked
   ST_CONFL with 2 live outcomes at S.
3. Fresh general entry via a new state for action 2.
4. Query S.

PASS requires: r=0 with `WITHHOLD (live-contradiction)`, confirming
the builder's disclosure that the guard applies equally to
untracked tombstones.
KILL requires: query returns r=1 (untracked contradictions escape
the guard).

## Attack X-CU6-4: regression (DOWNGRADE if silent change)

1. Extract committed `unified_causal6.zag` from git HEAD (not
   working tree). Compile. Run the builder's K-CU6-1 and K-CU6-2
   fixtures and the 16/16 battery + 28/28 main.
2. Byte-compare (cmp) against committed `CU6_ADV_RAW_1.txt`,
   `CU6_TEST_RAW_1.txt`, `CU6_MAIN_RAW_1.txt`.
3. Diff committed `unified_causal6.zag` vs committed
   `unified_causal5.zag`; verify exactly the frozen change set
   (40-line helper + 10-line guard).

PASS requires: all byte-identical, diff exactly the frozen set.
DOWNGRADE requires: any byte difference or undeclared change
(KILL bars K-CU6-1/K-CU6-2 unaffected).

## Verdict rule (frozen)

- All four PASS: H-CAUSAL-UNIFIED6 SURVIVES this red team.
- X-CU6-1, X-CU6-2, or X-CU6-3 KILL fires: H-CAUSAL-UNIFIED6
  KILLED (repair does not close the demonstrated failure class).
- X-CU6-4 DOWNGRADE fires with all KILL attacks passing:
  DOWNGRADED.
- No bar may be weakened or retroactively changed.

## Governance

- This prereg is committed alone before any attack fixture,
  build, or run.
- Pure Zag throughout. No Python.
- Only adversary-owned paths staged:
  `docs/lab/research-lead/overnight-20260928/causal_unified6_adversary/`.
- No em dashes in loop documentation.
- Commits local; no push.
