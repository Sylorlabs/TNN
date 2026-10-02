# GOAL ARCHITECTURE: Unified Autonomous Goal-Execution Subsystem

Date: 2026-09-30. Document only; no implementation; no new claims.
Status: ARCH-DOCUMENTED (kill bars K1-K3 addressed in section 10).

This document consolidates four committed waves into one subsystem
specification: AUTOGOAL (navigation and transfer), GOALREVISE
(revision under layout change), WALL_REMOVE design (CTSVR), and
WALLREMOVE implementation (false-wall to free revision). Together
they form a complete autonomous goal-execution loop: navigate, revise
added walls, unlearn removed walls.

## 1. Phase lineage (all commits verified present via git log)

| Phase | Prereg | Implementation | Verdict | Commit |
|---|---|---|---|---|
| 0. AUTOGOAL | 3aa462ff2, amend1 fa63205a3 | autogoal.zag | GOAL-TESTED | 67947a848 |
| 1. GOALREVISE | 60e4dcc9a | goalrevise.zag | REVISE-TESTED | cb2a6fdbc |
| 2. WALL_REMOVE design | (design only) | WALL_REMOVE_DESIGN.md | DESIGN-COMPLETE | 5daf15951 |
| 3. WALLREMOVE impl | a28ab9873 | wallremove.zag | BUILD-PASS | ed3d7e212 |

Prereg order verified in every wave: each prereg is a strict ancestor
of its implementation commit (git merge-base --is-ancestor), and each
implementation was committed alone before result logging.

## 2. The unified loop

One continuing learner runs all environments with a persistent map.
The loop, as logged in all four waves:

1. HYPOTHESIZE: the persistent map is the hypothesis. map[225] holds
   0=unknown, 1=free, 2=wall. Unknown is treated as free (optimistic
   planning). Phase 3 adds gen, wgen[225], transferred (section 4).
2. PLAN: generic BFS over the learner's map. PLAN lines log target
   and path length. Normal modes target the nearest unknown cell
   (frontier exploration, Env A) or the nearest unswept cell
   (transfer sweep, Env B/C). Re-verify mode (Phase 3) uses
   want==3 to target the nearest stale wall cell.
3. ACT: step along the plan. Per-action lines log t, action, x, y,
   bump, goal.
4. FAILURE: a bump falsifies the prediction "target cell is free"
   (FAIL lines). Bumps are the only revision driver in Phases 0-1;
   Phase 3 adds the T1 transfer-contradiction trigger (section 5).
5. REVISE: Phase 0-1: mark the bumped cell wall (REVISE lines).
   Phase 3: mark wall with wgen=gen; fire T1 if transferred==1;
   enter re-verify and probe stale cells (wall removed / wall
   confirmed).
6. RETRY: replan from the current position (replans counter).
7. GOAL: GOAL_REACHED with summary counters when the goal sensor
   fires. Goal location is unknown until the sensor fires; PROGRESS
   lines (measurement-only true distance) show search, not
   beelining.

## 3. Phase 0: AUTOGOAL (67947a848, GOAL-TESTED)

Sealed 15x15 grid: 20 wall cells in two barriers with offset gaps;
start (0,0); Goal A (14,14); Goal B (14,0). Three runs: Env A
(frontier exploration), Env B (transfer sweep on the persisted map),
and a seeded random-walk control.

Results (3/3 byte-identical, md5 6f3fc370ca8709b98706a4641d1d1528,
exit 0, zero stderr):

- Env A: GOAL_REACHED in 174 actions, 2 bumps, 2 replans, 173 free
  cells and 2 walls learned. True shortest path is 28; the 6.2x
  factor is exploration (the goal location is unknown).
- Env B (transfer): GOAL_REACHED in 186 actions, 0 bumps, 14 new
  free cells, 0 new walls. No wall learned in A was ever attempted
  in B (zero repeated collisions); all B navigation ran on shortest
  paths over the learned map.
- Random control: UNREACHED at the 20000-action cap (seed 12345).

Frozen kill bars: K1 (prereg + amendment name dynamics, goal,
actions, sensors, both sealed maps, information barrier; source
audit passes), K2 (the log exhibits hypothesis, experiment,
planning, failure, revision, retry in one continuing run per
environment; map persists A to B), K3 (Env A >= 100 actions and
Goal A; Env B Goal B; PROGRESS lines), K4 (3/3 byte-identical;
pure Zag; zero stderr; zero em/en-dash bytes).

## 4. Phase 1: GOALREVISE (cb2a6fdbc, REVISE-TESTED)

Same world plus a sealed env flag: env 0 pristine (Amendment 1
layout, 20 walls); env 1 changed (+wall at (14,7), -wall at (5,11),
-wall at (10,3); 19 walls). One continuing learner runs Env A
(explore, env 0), saves the post-A map, runs Env B (pristine
transfer sweep, env 0) as control, restores the post-A map, then
runs Env C (changed-layout sweep, env 1). A true-map BFS asserts
Env 1 reachability before Env C runs.

Results (3/3 byte-identical, md5 1d8cc5009b2ba544ed1ed20ea5fac4a0,
exit 0, zero stderr):

- Env A: 174 actions, 2 bumps (at (5,11) and (10,3)), 2 replans.
  Replicates 67947a848 exactly.
- Env B (control): 186 actions, 0 bumps. Replicates the published
  transfer result; the bump handler stayed armed and never fired.
- Env C (changed): GOAL_REACHED in 189 actions, 1 bump, 1 replan.
  At action 179 the sweep planned target (14,7) plen=1, stepped S
  from (14,8), and the world returned BUMP=1. The learner marked
  (14,7) wall, replanned around it via
  (13,8)->(13,7)->(13,6)->(14,6) (plen=4), and reached (14,0)
  10 actions later. No other bumps in Env C.

Pre-registered questions, answered: Detection YES (bump fired at the
changed cell on first contact, unprompted; no false alarm, since the
single bump was at a true Env 1 wall). Revision YES for the added
wall. Recovery YES (+3 actions vs pristine control). Removed walls:
NOT revised. (5,11) and (10,3) are free in Env 1 but stayed marked
wall with step-on counts 0 in B and C. The sweep revises false-free
to wall via bumps but has no mechanism to revise false-wall to
free. This is the pre-registered removal asymmetry, confirmed
empirically.

## 5. Phase 2: WALL_REMOVE design (5daf15951, DESIGN-COMPLETE)

The asymmetry is structural: bumps can only falsify "free"
predictions, never "wall" predictions, and the BFS planner treats
map==2 as blocked for both targeting and pathing, so learned walls
are never re-examined.

CTSVR (change-triggered stale-wall verification) adds:

- gen: i32, init 0. The environment generation the map was learned
  under. Incremented on T1.
- wgen[225]: u8. Per-cell generation tag, meaningful when map[i]==2.
  Records the generation in which the wall marking was learned or
  last confirmed.
- transferred: i32, init 0. Set to 1 when the map is carried over
  from a previous environment instead of built fresh.

Trigger T1 (transfer contradiction): a bump fires while
transferred==1. Within one environment (Env A), bumps are
exploration of an incomplete map, so no trigger fires. Across
environments, the transferred map carries the implicit claim "this
layout still holds"; a bump contradicts that claim. On T1: gen += 1,
log the suspected env-change, and compute the stale set: all cells
with map[i]==2 && wgen[i] < gen. The T1 cell itself is marked wall
with wgen=gen, so it never appears in its own stale set.

Revision policy: after T1 the planner enters a re-verify phase.
BFS gains want==3, targeting the nearest stale cell, and may route
through stale cells (traversal is itself a probe). Probe outcomes:
bump==0 -> mark free, log "REVISE wall removed x,y"; bump==1 ->
keep wall, re-tag wgen=gen, log "REVISE wall confirmed x,y", and
replan. The phase ends when the stale set empties; the normal sweep
resumes. Each cell is probed at most once per generation
(post-probe wgen=gen removes it from the stale set). The goal check
at the loop top is unchanged, so goal pursuit is never starved.

Structural cost bound: probes per T1 <= stale count S <= learned
walls W (<=20 in the 15x15 worlds); re-verify actions <= S*(D+1);
zero probes when T1 never fires. No timers or periods anywhere.

Alternatives rejected with reasons: periodic re-probing
(steady-state cost, hand-tuned period); pure optimistic retry
(thrash on confirmed walls); per-cell decay timers (researcher-tuned
thresholds); full re-exploration (unbounded, discards good entries);
trigger-on-any-bump (fires during initial learning when nothing is
stale).

Frozen falsifiers for the implementer: F1 no cell probed twice per
generation; F2 no probe in Env B; F3 Env C must not end with
(5,11)/(10,3) still wall; F4 re-verify <= 25 percent of control
Env C actions; F5 Env A/B counts unchanged at 174/186.

## 6. Phase 3: WALLREMOVE implementation (ed3d7e212, BUILD-PASS)

wallremove.zag extends goalrevise.zag with CTSVR per design
5daf15951. Two prereg-disclosed implementation decisions: D1
(re-verify-phase bumps on non-probe cells are current-gen
discoveries, no T1 refire); D3 (unreachable stale cells tagged
current-gen; never triggered in the frozen test).

Results (3/3 byte-identical, md5 64d285b023ef2660213b66a4243d6fc0,
exit 0, zero stderr):

- Env A: 174 actions, 2 bumps, 2 replans. Replicates cb2a6fdbc
  exactly; both walls tagged wgen=0.
- Env B: 186 actions, 0 bumps, 0 probes, rv_actions=0, gen=0.
  CTSVR fully inert; replicates the published transfer result.
- Env C: GOAL_REACHED in 234 actions, 2 bumps, 4 probes,
  rv_actions=46, gen=2. Trace: action 179, the (14,7) bump fires
  T1 (gen=1); re-verify probes (10,3) -> removed and (5,11) ->
  removed, discovering real walls (10,4) en route (D1); a later
  normal-sweep bump at (5,10) fires a second T1 (gen=2), making
  (14,7) and (10,4) stale again; confirmatory re-probes confirm
  both; goal reached at action 234. Post-run: c147=2 (confirmed),
  c511=1 and c103=1 (revised to free), on511=2, on103=2.

Kill bars: K1 PASS (source audit: T1 gate, gen/wgen with
save/restore, want==3 targeting, probe semantics, D1-D5 as
preregistered; information barrier unchanged). K2 PASS (both
removal lines present; map dump and step-on counts confirm). K3
PASS (F1 0 duplicates; F2 0 B-probes; F3 revised; F4 46 <= 47;
F5 174/186). K4 PASS (3/3 byte-identical; pure Zag; zero stderr).

The removal asymmetry is closed for walls the learner visits.

## 7. State contract (final, as implemented in wallremove.zag)

- map[225]: u8. 0=unknown, 1=free, 2=wall. Persistent across
  environments; saved/restored with the post-A map at transfer
  boundaries.
- gen: i32, init 0. Environment generation counter; incremented on
  T1.
- wgen[225]: u8. Generation tag per wall cell; saved/restored with
  the map; valid only when map[i]==2.
- transferred: i32, init 0. 1 when the map was carried over from a
  previous environment; 0 when built fresh.
- Derived: the stale set = {i : map[i]==2 && wgen[i] < gen}.

## 8. Interfaces between phases

- Phase 0 to 1: the frozen world (w_iswall, w_step, w_true_dist),
  the information barrier (wall literals only in w_iswall; env flag
  read only by w_step and measurement-only w_true_dist), and the
  Env A/Env B protocol are unchanged. Phase 1 adds only the env
  flag, the second layout, the B/C sweep split, and the C-phase
  questions.
- Phase 1 to 2: the documented removal asymmetry (on511=on103=0;
  stale map entries) is the design input. The design's worked
  example (section 3.4 of WALL_REMOVE_DESIGN.md) is the executable
  contract the implementer tested against.
- Phase 2 to 3: T1, the gen/wgen/transferred state, want==3, probe
  semantics, the structural cost bound, and falsifiers F1-F5 pass
  unchanged into the prereg; D1 and D3 are prereg-disclosed
  implementation decisions, not design changes.
- External contracts: sensors (bump falsifies "free"; goal sensor
  reports location; position known); planner (BFS, optimistic);
  logger (PLAN / per-action / FAIL / REVISE / PROBE / MAPDUMP
  lines; measurement-only PROGRESS and TRUE_DIST lines never feed
  decision code).

## 9. Capability summary (what the subsystem does, with evidence)

- Navigate to an unknown goal in an unknown 15x15 layout: Env A,
  174 actions, 2 bumps, GOAL_REACHED (67947a848).
- Persist the learned map across environments and reuse it with
  zero repeated wall collisions: Env B, 186 actions, 0 bumps
  (67947a848, replicated twice).
- Detect a layout change unprompted and revise the map: Env C,
  action-179 bump at (14,7), revised, goal reached +3 actions vs
  control (cb2a6fdbc).
- Revise added walls: mark wall, replan around (cb2a6fdbc).
- Revise removed walls: probe stale cells, mark free on bump==0
  (ed3d7e212; (5,11) and (10,3) both revised).
- Confirm real walls under suspicion: bump==1 re-tags wgen=gen
  ((14,7), (10,4) confirmed in gen=2 re-verify).
- Stay inert when nothing changed: 0 probes, gen=0 in Env B
  (ed3d7e212).

## 10. Limitations (K3; consolidated from all four waves, no new ones)

1. Bounded L1/L2, not L3. Action semantics (N/E/S/W moves) are
   given primitives. The exploration strategy (optimistic BFS,
   frontier/sweep), the bump-to-wall revision operator, the T1
   trigger, and the probe policy are all researcher-authored
   control flow. What is learned and persists: the map (wall
   layout plus generation tags) and the goal location. Transfer is
   reuse of the learned map, not representational invention.
2. Lazy resolution. Stale walls that are never visited stay stale;
   unvisited wrong entries do not affect behavior, so this is a
   cost feature, but any claim of "full map maintenance" would be
   false (inherited from the design).
3. No revision without contradiction. Gradual drift that never
   produces a bump fires no T1 and gets no revision (inherited
   from the design).
4. T1 over-fires. The frozen rule fires on any normal-sweep bump
   while transferred==1, including bumps on unknown cells. In Env C
   the (5,10) bump fired a second T1 that re-staled already-handled
   walls, costing two confirmatory re-probes. F4 still held
   (46/47) but the margin is thin. The design's honest-scope
   section notes a candidate refinement (narrow T1 to bumps that
   contradict learned cells); it is a design change and was not
   made.
5. The D3 "stale unreachable" fallback is implemented but was
   never triggered; it is untested code.
6. Small scale by design. The change is 3 cells on 15x15 and the
   added wall sits on the deterministic sweep path. A larger or
   adversarially placed change could outrun the sweep's coverage;
   not tested.
7. The random baseline is weak by design (no memory); it calibrates
   that the task is non-trivial, not that the learner is
   intelligent.
8. Transfer benefit is reliability, not speed. Env B took more
   actions than Env A (186 vs 174) because the sweep is
   systematic; the benefit is 0 bumps and navigation on learned
   shortest paths.
9. Truthful sensors assumed. The bump sensor and goal sensor are
   taken at face value in all phases, same as the existing
   learner.
10. No doubt-in-planning integration. This subsystem plans on the
    map as if it were certain; calibrated doubt (as in the
    verification subsystem's SUSPECT flags or F3's doubt score) is
    not wired into the planner. That integration seam is future
    work, owned by the continuing-learner track once F3
    stabilizes.
11. The re-verify cost bound held on the frozen test but is
    structural, not tight: adversarial layouts could push
    S*(D+1) far above the observed 46 actions.

## 11. Kill-bar self-check (document only)

- K1 PASS: sections 2 through 8 specify the loop, all four
  phases, the final state contract, and the phase-to-phase and
  external interfaces, all grounded in committed evidence
  (commits listed in section 1, results summarized in sections
  3, 4, 6).
- K2 PASS: sections 7 and 8 show the phases integrated into one
  state contract (gen/wgen/transferred added to the Phase 0
  map), one loop (T1/CTSVR plugging into the Phase 0-1 bump
  handler), and one planner (want==3 as a BFS mode), with the
  evidence chain intact end to end.
- K3 PASS: section 10 consolidates every limitation stated in
  the four waves' honest-scope sections plus the two known
  gaps surfaced during implementation (T1 over-firing, D3
  untested), and adds no new limitations.

Builder label: ARCH-DOCUMENTED.

## 12. Files

- GOAL_ARCHITECTURE.md (this document)

Related (read-only references, owned by other waves):
- auto_goal/RESULT_AUTOGOAL.md (67947a848)
- goal_revise/RESULT_GOALREVISE.md (cb2a6fdbc)
- wall_remove/WALL_REMOVE_DESIGN.md (5daf15951)
- wall_remove_impl/RESULT_WALLREMOVE.md (ed3d7e212)
