# PREREG_WALLREMOVE: CTSVR Implementation (False-Wall to Free Revision)

Date: 2026-09-30. Status: FROZEN. This prereg is committed alone before
any implementation file for wall_remove_impl exists.

## 1. Objective

Implement the CTSVR mechanism (change-triggered stale-wall
verification) specified in WALL_REMOVE_DESIGN.md (design commit
5daf15951, DESIGN-COMPLETE) on top of the GOALREVISE learner
(goalrevise.zag, commit cb2a6fdbc, REVISE-TESTED), and test whether it
closes the removal asymmetry: Env C must end with the two removed
walls (5,11) and (10,3) revised to free, while Env A and Env B
behavior is unchanged and re-verify cost stays bounded.

## 2. Reference design (frozen)

Design: 5daf15951. Mechanism summary:

- Persistent state additions: gen (i32, init 0), wgen[225] (u8
  per-cell generation tag, meaningful when map==2), transferred (i32).
- T1 trigger: a bump fires while transferred==1. On T1: gen += 1, log
  the suspected env-change, stale set = cells with map==2 and
  wgen < gen. The T1 bump cell is marked wall with wgen = gen, so it
  is never in its own stale set.
- Revision policy: re-verify phase before the normal sweep. BFS gains
  want==3 targeting the nearest stale cell; BFS may route through
  stale cells (traversable). Probing a stale cell: bump==0 marks it
  free (REVISE wall removed); bump==1 keeps it wall and re-tags
  wgen=gen (REVISE wall confirmed), then replan. Each cell probed at
  most once per generation. Phase ends when the stale set empties.
- Cost bound: probes per T1 <= stale count S <= learned walls;
  re-verify actions <= S*(D+1); zero probes when T1 never fires; no
  timers or periods.

## 3. Implementation decisions (disclosed; within the design)

D1. T1 fires on a bump while transferred==1 during the normal sweep.
    Bumps that occur during the re-verify phase on non-probe cells
    (re-verify routing through unknown cells that turn out to be real
    walls) are treated as ongoing discovery: the cell is marked wall
    with wgen = gen (current generation) and logged as a wall learned,
    without refiring T1. Rationale: refiring T1 mid-re-verify would
    increment gen repeatedly and make already-handled walls stale
    again (gen thrash); the design's walkthrough and F4 both
    anticipate a clean re-verify episode. Probe bumps (bump==1 on a
    stale cell) are confirmations per the design, never T1 events.

D2. want==3 BFS targets the nearest stale cell (map==2, wgen<gen);
    traversal treats stale cells as passable; current-generation
    walls still block.

D3. Termination guarantee: if want==3 BFS finds no reachable stale
    cell, all remaining stale cells are tagged wgen = gen (kept wall)
    with a "stale unreachable" log line, so the re-verify phase
    always terminates. Conservative (keeps wall), disclosed.

D4. Probe audit: every probe attempt logs "PROBE <T> x,y gen=<g>"
    before stepping, so F1 (no double probe per generation) is
    checkable from the log with shell tools.

D5. Env A (transferred=0) tags learned walls wgen=0; the post-A wgen
    array is saved and restored alongside the post-A map, so Env B
    and Env C start from identical (map, wgen) state.

## 4. Environment and procedure (frozen; unchanged from 60e4dcc9a)

Same sealed world, layouts, env flag, information barrier, goals,
and action budget (5000/env) as GOALREVISE. Procedure: Env A
(explore, env 0, goal 14,14, transferred=0), save (map, wgen); Env B
(pristine transfer sweep, env 0, goal 14,0, transferred=1); restore
post-A (map, wgen); Env C (changed sweep, env 1, goal 14,0,
transferred=1). Reachability assert before Env C unchanged.

## 5. Measurements (frozen)

All GOALREVISE measurements plus: PROBE lines (x, y, gen); REVISE
env-change suspected lines (gen); REVISE wall removed / wall
confirmed lines; per-env probes, re-verify actions, final gen in the
GOAL_REACHED summary; post-run MAPDUMP at (14,7), (5,11), (10,3)
unchanged.

## 6. Design predictions (rationale, not kill bars)

- Env A: 174 actions, 2 bumps at (5,11) and (10,3); wgen=0 on both.
  Replicates cb2a6fdbc.
- Env B: 186 actions, 0 bumps, 0 probes, gen stays 0. CTSVR inert.
- Env C: the sweep replicates the 179-action path to the (14,7)
  bump; T1 fires (gen=1); stale set = {(5,11), (10,3)} (the only two
  walls in the transferred map); re-verify probes both; both return
  bump=0 (free in Env 1) and are marked free with REVISE wall removed
  lines; GOAL_REACHED with on511>=1, on103>=1, MAPDUMP c511=1,
  c103=1. Re-verify actions expected well under the F4 bound.

## 7. Falsifiers (frozen; from the design, F4 number frozen here)

- F1 (thrash): any cell probed twice within one generation
  (audit the PROBE lines).
- F2 (false trigger): any probe occurs in Env B.
- F3 (revision failure): Env C ends with (5,11) or (10,3) still
  marked wall (MAPDUMP c511/c103 != 1).
- F4 (cost blowout): re-verify actions in Env C exceed 25 percent of
  the frozen control Env C count (189 actions): bar is rv_actions
  <= 47.
- F5 (regression): Env A actions != 174 or Env B actions != 186.

## 8. Kill bars (numbered; frozen)

- K1 (CTSVR implemented): source audit shows T1 (bump while
  transferred==1 during sweep), gen/wgen state with save/restore,
  want==3 targeting and stale traversal in BFS, probe semantics
  (removed/confirmed), and D1-D5 as specified above. Missing
  element: FAIL.
- K2 (revision): Env C MAPDUMP shows c511=1 and c103=1;
  on511>=1 and on103>=1; REVISE wall removed lines for both cells
  present. Otherwise: FAIL.
- K3 (falsifiers): F1-F5 all pass per section 7. Any fires: FAIL.
- K4 (determinism and purity): 3/3 runs byte-identical; pure Zag at
  every stage (znc, shell, grep, git only; no Python in source,
  build, execution, analysis, or wave artifacts); zero em/en-dash
  bytes in wave documentation (byte-checked with shell). Otherwise:
  FAIL.

BUILD-PASS requires all four bars. Any FAIL is BUILD-FAIL. No
SURVIVES claim (promotion pipeline steps remain for the parent).

## 9. Governance

Pure Zag only. No Python anywhere in this wave. Prereg committed
alone before any implementation file exists. Commits local on
tnn-native-lab, owned path only:
docs/lab/research-lead/overnight-20260928/wall_remove_impl/. Use
pathspec commits. Builder reports BUILD-PASS or BUILD-FAIL only.

## 10. Honest scope (pre-registered)

- Bounded L1/L2: the trigger and probe policy are researcher-authored
  control flow; this measures the CTSVR mechanism, it does not invent
  representations.
- Lazy resolution (unvisited stale walls stay stale) and no-drift
  handling (no T1 without a contradiction) are inherited from the
  design and remain limitations.
- D1 is an implementation decision within the design's letter; if it
  changes outcomes vs the design's walkthrough, the difference is
  reported honestly rather than hidden.
