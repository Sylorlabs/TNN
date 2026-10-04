# PREREG_GOALREVISE: Map Revision Under Transfer Surprise

Date: 2026-09-30. Status: FROZEN. This prereg is committed alone before any
implementation file for this wave exists. No `.zag` for goal_revise exists
at commit time.

## 1. Objective

Test whether the autonomous goal-execution learner (GOAL-TESTED,
67947a848) revises its persistent map when the world layout changes under
it. The Env B transfer sweep arms the bump handler but never fired it
(0 bumps). This wave changes the sealed layout between transfer episodes
and measures: detection (bump at a changed cell), revision (map corrected),
recovery (goal still reached, actions to adapt), and the removal asymmetry
(cells the learner marked wall that become free are never re-examined).

## 2. Environment (frozen)

Grid 15x15, same actions/sensors/dynamics as PREREG_AUTOGOAL (3aa462ff2)
and Amendment 1 (fa63205a3). Two sealed layouts selected by a world env
flag. The learner never reads the flag or the wall literals (barrier
verified by source audit, same as 67947a848).

Env 0 (pristine): the Amendment 1 layout, 20 walls:
x=5:  (5,0),(5,1),(5,2),(5,3),(5,4),(5,6),(5,7),(5,8),(5,9),(5,10),(5,11)
x=10: (10,3),(10,4),(10,5),(10,6),(10,7),(10,9),(10,10),(10,11),(10,12)

Env 1 (changed): Env 0 with exactly three cell changes:
- ADD wall at (14,7). In Env 0 this cell is free. The learner visited it
  in Env A (known-free in its map). It lies on the deterministic Env B
  sweep path: the published B log steps (14,9)->(14,8)->(14,7)->(14,6).
- REMOVE wall at (5,11). In Env 0 this cell is a wall. The learner bumped
  it in Env A and marked it wall in its persistent map.
- REMOVE wall at (10,3). In Env 0 this cell is a wall. The learner bumped
  it in Env A and marked it wall in its persistent map.

Env 1 has 19 walls. Nothing else changes.

Connectivity (Env 1): goal (14,0) is reachable from (0,0). The published
B route descends x=14; with (14,7) walled the detour runs
(14,8)->(13,8)->(13,7)->(13,6)->(14,6)->(14,5)->...->(14,0), all free
cells in Env 1. The implementation asserts reachability with a true-map
BFS before running (abort if unreachable).

## 3. Learner and procedure (frozen)

Learner: identical to 67947a848 (map[225] persistent; optimistic planning;
Env A frontier exploration; transfer sweep with armed bump handler that
marks the bumped cell wall and replans). No learner code changes except
duplicating the sweep routine for distinct B/C log labels.

Procedure (one continuing learner, map persists):
1. Env A in world env 0, goal (14,14). Frontier exploration (l_env_a).
   Save the post-A map.
2. Env B in world env 0, goal (14,0). Transfer sweep (l_env_b). This is
   the pristine-transfer control; expected to replicate 0 bumps.
3. Restore the post-A map (discard B's additions, so B and C start from
   the identical map state; the only difference between B and C is the
   world layout).
4. Env C in world env 1, goal (14,0). Transfer sweep (l_env_c, same code
   as l_env_b with C labels). The bump handler is the revision machinery.

The random baseline is not re-run (67947a848 already calibrates
non-triviality; Env B is this wave's control).

Action budget: 5000 per environment. Sealed goal positions; the learner
never reads them (GOAL sensor only).

## 4. Measurements (frozen)

Per action: t, action, x, y, bump, goal (same compact lines as 67947a848,
labeled A/B/C). Phase markers: PLAN, FAIL (bump cell), REVISE (wall
learned), GOAL_REACHED. PROGRESS every 25 actions (measurement-only true
distance under the active layout).

Summary per environment: actions, bumps, replans, cells learned,
GOAL_REACHED or FAIL. For Env C additionally:
- bump locations; each bumped cell checked against the sealed Env 1
  layout (analysis-side only, never by the learner): a bump at a cell
  that is free in Env 1 is a false alarm.
- whether (14,7) is marked wall in the learner map after the bump.
- whether (5,11) and (10,3) are ever stepped on in Env C (expected:
  never; the learner's map still marks them wall).
- actions from Env C start to first bump, and from last bump to
  GOAL_REACHED (recovery intervals).

## 5. Design predictions (rationale, not kill bars)

- Env B replicates 0 bumps (control).
- Env C: the sweep follows the deterministic Env B path (identical start
  map, algorithm, start, goal) until it steps (14,8)->(14,7), where the
  world returns BUMP=1. Predicted bumps_C = 1, at (14,7), with no other
  bumps (no other walls can be encountered: the removed cells are marked
  wall in the learner map and avoided; all other Env 1 cells are free).
- (14,7) is marked wall (revision), the sweep replans around it, and
  GOAL_REACHED fires for (14,0).
- (5,11) and (10,3) are never stepped on in Env C: the sweep cannot
  discover removed walls (removal asymmetry). The learner map stays
  wrong there, which is reported as a limitation, not a failure.

## 6. Kill bars (numbered; frozen)

- K1 (changed layout specified): this prereg names the exact changed
  cells, both sealed layouts, the env flag, and the information barrier.
  Missing element: FAIL.
- K2 (revision behavior measured): the Env C log shows every bump with
  its cell; each bumped cell is checked against the sealed Env 1 layout;
  the post-run learner map is dumped showing (14,7) wall status and
  (5,11)/(10,3) wall status; step-on counts for the removed cells are
  reported. If bumps cannot be attributed to specific cells, or the map
  dump is missing: FAIL.
- K3 (recovery quantified): actions_C, bumps_C, replans_C reported;
  actions-to-first-bump and post-last-bump-to-goal intervals reported;
  GOAL_REACHED in Env C, or a FAIL line with the blocking cause if the
  goal is unreachable under the revised map. Missing numbers: FAIL.
- K4 (determinism and purity): 3/3 runs byte-identical; pure Zag at
  every stage (znc, shell, grep, git only; no Python in source, build,
  execution, analysis, or wave artifacts); no em dashes or en dashes in
  wave documentation (byte-checked). Otherwise: FAIL.

REVISE-TESTED requires all four bars. Any FAIL is BUILD-FAIL. No
SURVIVES claim (promotion pipeline steps 4-11 remain for the parent).

## 7. Honest scope (pre-registered)

- This measures the existing bump->mark->replan machinery under a
  layout change; it does not test invention of new representations.
  Bounded L1/L2.
- The change is small (3 cells) and placed where the deterministic
  sweep must encounter it. A 0-bump Env C would mean the sweep avoided
  the changed cell and the wave is inconclusive on detection (reported
  honestly, not re-run with a new layout).
- The removal asymmetry ((5,11),(10,3) never re-examined) is a
  pre-registered limitation of the sweep strategy, not a learner bug
  introduced by this wave.
- Env B is a control for the transfer machinery, not a second
  independent result; its 0-bump replication is expected, not novel.

## 8. Governance

Pure Zag only. No Python anywhere in this wave. Prereg committed alone
before any implementation file exists. Commits local on tnn-native-lab,
owned path only:
docs/lab/research-lead/overnight-20260928/goal_revise/. Use pathspec
commits (`git commit -- <owned path>`) to avoid sweeping concurrent
workers. Builder reports REVISE-TESTED or BUILD-FAIL only.
