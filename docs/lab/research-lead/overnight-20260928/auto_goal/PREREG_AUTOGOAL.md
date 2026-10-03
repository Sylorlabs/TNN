# PREREG_AUTOGOAL: Autonomous Goal Execution Prototype

Date: 2026-09-30. Status: FROZEN. This prereg is committed alone before any
implementation. No `.zag` for this wave exists at commit time.

## 1. Objective

Launch a longer-horizon autonomous goal-execution environment (directive
priority 7). TNN receives a goal, primitive actions, sensors, and an unknown
world. No procedure is supplied. The learner must run the full loop:
hypothesis -> experiment -> learning -> planning -> action -> failure ->
revision -> retry, for hundreds of actions, then transfer to a related
second environment. This wave builds the prototype and measures it.

## 2. Environment (frozen)

Grid world, 10x10 = 100 cells. Cell (x,y), x,y in 0..9. Index = y*10+x.

Actions (5): 0=N (y+1), 1=S (y-1), 2=E (x+1), 3=W (x-1), 4=WAIT.
Sensors: POS (x,y always visible), BUMP (1 iff the last move attempted a
wall cell or off-grid cell, else 0), GOAL (1 iff agent is on the goal cell).

Dynamics (sealed): a move into a wall cell or off-grid leaves the agent in
place with BUMP=1; otherwise the agent moves with BUMP=0. WAIT leaves the
agent in place with BUMP=0. The agent never moves diagonally and never
observes the wall layout except through BUMP and position change.

Sealed maps (identical wall layout in both environments; the learner never
reads these literals; structural barrier verified by source audit):

Walls (x,y):
(3,0),(3,1),(3,2),(3,4),(3,5),(3,6),
(6,3),(6,4),(6,5),(6,7),(6,8),
(4,8),(5,8).
Total 13 wall cells. 87 free cells.

Start S = (0,0) in both environments.
Goal A = (9,9). Goal B = (9,0).

The wall literals live inside the world_step function only. The learner
file calls w_step(action), w_x(), w_y(), w_bump(), w_goal(). It never
names a wall coordinate. The measurement-only function w_true_dist(x,y)
(BFS distance on the true map) is used ONLY for PROGRESS logging, never
by learner decision code; this is fenced by source audit.

Env A: unknown map, unknown goal. Episode ends when GOAL=1 (stepping on
the goal cell finds and reaches it simultaneously).
Env B: same map, new goal (9,0), agent position reset to (0,0). The
learner keeps its learned map across the boundary (transfer state).

## 3. Learner architecture (frozen)

State: map[100] bytes, 0=unknown, 1=free, 2=wall. gx,gy goal coords,
goal_known flag. All persistent across Env A -> Env B except goal_known,
gx, gy, and position (reset per environment).

Hypothesis H = (map, goal estimate). Planning is optimistic: unknown
cells are treated as free.

Env A loop (per action):
1. HYPOTHESIZE: current H.
2. PLAN: if goal_known, target = goal. Else target = nearest unknown
   cell by BFS over cells with map != wall (unknown treated as free),
   neighbor order N,S,E,W fixed. If no unknown cell is reachable, FAIL
   (fully mapped, goal not found; must not happen on the frozen maps).
   BFS yields a shortest path under H; take its first action.
3. ACT: execute one action via w_step. actions += 1.
4. SENSE + LEARN: read POS/BUMP/GOAL. On success mark the entered cell
   free. On BUMP=1 mark the attempted cell wall (FAIL event: the plan's
   prediction "target cell is free" was falsified).
5. REVISE + RETRY: after any map change, replan from the current
   position on the next iteration (replans counter += 1 when a bump
   invalidates the in-progress plan).
6. GOAL: if w_goal()=1, record gx,gy, set goal_known, end Env A.

Env B loop (transfer):
swept[100] zeroed. Each iteration: BFS over cells with map==1 (known
free only) for the nearest cell with swept=0. If none, FAIL. Plan the
BFS path (all moves on known-free cells; bumps are not expected but the
bump handler stays armed: a bump marks the wall and replans, which is
the revision machinery, not new code). Execute step by step, marking
swept. If w_goal()=1, end Env B. Transfer metrics: bumps_B (expected 0),
actions_B, and the fact that every Env B move follows a shortest path
on the learned map.

Action budget: 5000 per environment. Exceeding it is FAIL.

Random baseline (control): uniform random choice over {N,S,E,W} from a
seeded LCG (seed 12345, disclosed), no map, no planning, on Env A only,
cap 20000 actions. Report actions-to-goal or UNREACHED. Deterministic.

## 4. Measurements (frozen)

Per action: t, action, x, y, bump, goal (compact line).
Phase markers: PLAN (target, path length), FAIL (bump cell), REVISE
(wall learned), GOAL_REACHED.
Every 25 actions: PROGRESS t true_dist (measurement only).
Summary per environment: actions, bumps (failures), replans, cells
learned (free count, wall count), path efficiency (actions vs true
shortest path length from start to goal on the true map).
Transfer: actions_A vs actions_B, bumps_A vs bumps_B, cells relearned
in B (expected 0).

## 5. Kill bars (numbered; frozen)

- K1 (environment specified): this prereg names dynamics, goal,
  actions, sensors, both sealed maps, and the information barrier.
  Missing element: FAIL.
- K2 (autonomous loop implemented): the implementation exhibits
  hypothesis (map+goal estimate), experiment (frontier/sweep moves),
  planning (BFS), failure (bump), revision (map update), retry
  (replan), in one continuing run per environment. A missing phase
  in the log: FAIL.
- K3 (100+ actions, goal progress measured): Env A executes >= 100
  actions AND reaches Goal A; Env B reaches Goal B; PROGRESS lines
  show true distance shrinking over time. Fewer than 100 actions in
  Env A, or either goal unreached: FAIL.
- K4 (determinism and purity): 3/3 runs byte-identical per
  environment; pure Zag at every stage (znc, shell, grep, git only;
  no Python in source, build, execution, analysis, or wave
  artifacts); no em dashes or en dashes in wave documentation
  (byte-checked). Otherwise: FAIL.

GOAL-TESTED requires all four bars. Any FAIL is BUILD-FAIL for the
prototype (reported as GOAL-TESTED only if all pass).

## 6. Honest scope (pre-registered)

- The action semantics (N moves north) are primitives, given, not
  learned. The unknown is the world layout and goal location.
- The exploration strategy (optimistic BFS + frontier/sweep) is
  researcher-authored control flow. What is learned: the map (wall
  layout) as persistent state, and the goal location. Transfer is
  reuse of the learned map, not invention of a new representation.
- This is a bounded L1/L2 prototype: it demonstrates the long-horizon
  loop machinery, not L3 representational invention. A future wave
  may ask the learner to invent its own spatial representation.
- The random baseline is weak by design (no memory); it calibrates
  action counts, not intelligence.

## 7. Governance

Pure Zag only. No Python anywhere in this wave. Prereg committed alone
before any implementation file exists. Commits local on tnn-native-lab,
owned path only:
docs/lab/research-lead/overnight-20260928/auto_goal/. Builder reports
GOAL-TESTED or BUILD-FAIL only; no SURVIVES claim (promotion pipeline
steps 4-11 remain for the parent to schedule).
