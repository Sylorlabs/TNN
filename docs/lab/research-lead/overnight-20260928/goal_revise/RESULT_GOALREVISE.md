# RESULT_GOALREVISE: Map Revision Under Transfer Surprise

Date: 2026-09-30. Prereg 60e4dcc9a (committed alone before implementation).
Verdict: REVISE-TESTED. All four kill bars pass.

## Commits (local, tnn-native-lab, owned path only)

- Prereg: 60e4dcc9a (frozen before any implementation file existed)
- Implementation + result: this commit (goalrevise.zag, RESULT, 3 raw logs)
- Order verified: prereg strictly precedes implementation
  (git merge-base --is-ancestor on 60e4dcc9a).

## What was built

Single-file pure-Zag program (goalrevise.zag), adapted from autogoal.zag
(67947a848): sealed world with an env flag selecting the pristine layout
(env 0, Amendment 1, 20 walls) or the changed layout (env 1: +wall at
(14,7), -wall at (5,11), -wall at (10,3); 19 walls). One continuing
learner runs Env A (explore, env 0, goal (14,14)), saves the post-A map,
runs Env B (pristine transfer sweep, env 0, goal (14,0)) as control,
restores the post-A map, then runs Env C (changed-layout transfer sweep,
env 1, goal (14,0)). The sweep routine is shared code with B/C log
labels. A true-map BFS asserts Env 1 reachability before Env C runs.

## Results (3/3 byte-identical, md5 1d8cc5009b2ba544ed1ed20ea5fac4a0,
exit 0, zero stderr)

Env A: GOAL_REACHED in 174 actions, 2 bumps (at (5,11) and (10,3)),
2 replans. Replicates 67947a848 exactly.

Env B (pristine control): GOAL_REACHED in 186 actions, 0 bumps,
14 new free cells, 0 new walls. Replicates the published transfer
result; the bump handler stayed armed and never fired.

Env C (changed layout): GOAL_REACHED in 189 actions, 1 bump, 1 replan.
The single bump fired at action 179: the sweep planned target (14,7)
with plen=1, stepped S from (14,8), and the world returned BUMP=1:

  PLAN C sweep target=14,7 plen=1
  C 179 a=1 x=14 y=8 b=1 g=0
  FAIL C bump at 14,7
  REVISE C wall learned 14,7
  PLAN C sweep target=14,6 plen=4

The learner marked (14,7) wall (revision), replanned around it via
(13,8)->(13,7)->(13,6)->(14,6) (plen=4), and reached (14,0) 10 actions
later. No other bumps in Env C.

Post-run map dump: c147=2 (14,7 marked wall: revised), c511=2 and
c103=2 ((5,11) and (10,3) still marked wall). Step-on counts in Env C:
on511=0, on103=0. The learner never re-examined the removed walls.

## Kill bars

- K1 PASS: prereg names the exact changed cells, both sealed layouts,
  the env flag, and the barrier. Source audit: wall literals live only
  inside w_iswall; w_iswall is called only by w_step and
  measurement-only w_true_dist; the env flag (ws+24) is read only by
  w_step and w_true_dist; w_true_dist is called only for PROGRESS /
  TRUE_DIST logging and the reachability assert, never by learner
  decision code (bfs, l_env_a, l_env_bc).
- K2 PASS: every bump is attributed to a cell. Env C had exactly 1
  bump, at (14,7), which is a wall in the sealed Env 1 layout (added
  cell): no false alarm. The map dump shows (14,7)=wall (revised) and
  (5,11)=(10,3)=wall (stale, see honest scope). Step-on counts for the
  removed cells are 0 in both B and C.
- K3 PASS: actions_C=189, bumps_C=1, replans_C=1 (replan counted on the
  bump break). Actions to first bump: 179. Post-bump to goal: 10
  actions. GOAL_REACHED in Env C. Transfer cost of the surprise: +3
  actions vs pristine B (186), all attributable to the bump, revision,
  and 4-step detour.
- K4 PASS: 3/3 runs byte-identical; pure Zag at every stage (znc,
  shell, grep, git only; zero Python invocations); zero stderr; zero
  em/en-dash bytes in wave documentation (byte-checked).

## Answers to the pre-registered questions

- Detection: YES. The bump handler fired at the changed cell on first
  contact (action 179). The learner did not need to be told the layout
  changed; the failed prediction ("(14,7) is free") was falsified by
  the sensor.
- Revision: YES for the added wall. (14,7) was marked wall in the
  persistent map and the planner routed around it thereafter.
- Recovery: YES. Goal reached 10 actions after the bump; total +3
  actions vs the pristine control.
- Removed walls: NOT revised. (5,11) and (10,3) are free in Env 1 but
  the learner's map still marks them wall and the sweep never steps on
  them (on511=on103=0). The sweep strategy revises false-free to wall
  via bumps but has no mechanism to revise false-wall to free. This is
  the pre-registered removal asymmetry, confirmed empirically.

## Honest scope

- Bounded L1/L2: the revised structure is the map (wall layout); the
  revision operator (bump -> mark wall -> replan) is researcher-authored
  control flow, same as 67947a848. This wave measures that machinery
  under layout change; it does not invent new representations.
- The change is small (3 cells) and the added wall sits on the
  deterministic sweep path, by design. A larger or adversarially placed
  change could outrun the sweep's coverage; not tested here.
- The removal asymmetry means a changed layout can leave the learner
  with a permanently wrong map in the false-wall direction while still
  reaching the goal. Any claim of "full map maintenance" would need a
  re-exploration mechanism; none exists in this learner.
- Env B is a control replicating 67947a848, not a new result.

## Files

- goalrevise.zag (implementation)
- GOALREVISE_RAW_1.txt, GOALREVISE_RAW_2.txt, GOALREVISE_RAW_3.txt
  (byte-identical)
- PREREG_GOALREVISE.md

Builder label: REVISE-TESTED.
