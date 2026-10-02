# WALL_REMOVE_DESIGN: False-Wall to Free Revision Mechanism

Date: 2026-09-30. Design only; no implementation.
Status: DESIGN-COMPLETE (kill bars K1-K3 addressed below).

## 1. Problem

RESULT_GOALREVISE.md (commit cb2a6fdbc, REVISE-TESTED) confirmed a
removal asymmetry in the continuing map learner:

- False-free to wall: revised. A bump fires, the attempted cell is
  marked wall, the planner replans. Env C: (14,7) added wall detected
  at action 179, revised, goal reached 10 actions later.
- False-wall to free: NOT revised. (5,11) and (10,3) were marked wall
  in Env A, are free in the Env 1 layout, and stay marked wall forever
  (on511=0, on103=0 in Env C). The learner never re-examines a cell it
  marked wall, because the BFS planner treats map==2 as blocked for
  both targeting and pathing.

The asymmetry is structural: revision is driven only by bumps, and
bumps can only falsify "free" predictions, never "wall" predictions.
A changed layout can therefore leave the learner with a permanently
wrong map in the false-wall direction while still reaching the goal.

## 2. Design requirements

R1. Trigger: the learner must detect, from its own sensor stream, that
    previously learned wall markings may be stale. No oracle signal,
    no researcher telling it the layout changed.
R2. Policy: stale wall markings must be re-examined with real actions,
    and revised to free (or confirmed) based on sensor outcomes.
R3. Bounded cost: zero re-probing when the environment is stable;
    re-probing cost bounded by a disclosed function of map size, never
    by a hand-tuned timer or period.
R4. No thrash: walls confirmed in the current environment are never
    re-probed; each stale cell is probed at most once per generation.

## 3. Mechanism: change-triggered stale-wall verification (CTSVR)

### 3.1 Persistent state (additions to the learner map)

- `gen: i32`, init 0. The environment generation the map was learned
  under. Incremented on T1.
- `wgen[225]: u8`. Per-cell generation tag, meaningful only when
  map[i]==2 (wall). Records the generation in which the wall marking
  was learned (or last confirmed).
- `transferred: i32`, init 0. Set to 1 when the map is carried over
  from a previous environment instead of built fresh. Env A builds
  fresh (transferred=0); Env B and C restore the post-A map
  (transferred=1).

Map cell values keep their existing meaning: 0 unknown, 1 free,
2 wall.

### 3.2 Trigger

T1 (transfer contradiction): a bump fires while `transferred==1`.

Rationale: within a single environment (Env A), bumps are exploration
of an incomplete map, not evidence of change, so no trigger fires and
no re-verification runs. Across environments, the transferred map
carries the implicit claim "this layout still holds"; a bump
contradicts that claim and is evidence the environment may have
changed. Env B (pristine): no bumps, T1 never fires, zero added cost.
Env C: the (14,7) bump at action 179 fires T1.

On T1:
- `gen = gen + 1`.
- Log `REVISE env-change suspected gen=<gen>`.
- Compute the stale set: all cells with `map[i]==2 && wgen[i] < gen`.

Note: the cell that caused the T1 bump is marked wall with
`wgen = gen` (current generation), so it is never in its own stale
set.

### 3.3 Revision policy

After T1, the planner enters a re-verify phase before resuming the
normal sweep:

1. Target selection: BFS gains `want==3`, which targets the nearest
   stale cell (`map[i]==2 && wgen[i] < gen`). The existing goal check
   at the top of the loop is unchanged, so goal pursuit is not
   starved; only sweep-target selection is redirected.
2. Pathing: BFS may route through stale cells (treat as traversable).
   Traversing a stale cell is itself a probe of that cell.
3. Probe execution: attempt the step onto the stale cell.
   - `bump==0`: the cell is free. Set `map[i]=1`, `wgen[i]=gen`,
     log `REVISE wall removed x,y`. This is the false-wall to free
     revision.
   - `bump==1`: the wall is confirmed. Keep `map[i]=2`, set
     `wgen[i]=gen` (confirmed for this generation),
     log `REVISE wall confirmed x,y`. Replan around it as today.
4. The re-verify phase ends when the stale set is empty; the normal
   sweep then resumes.
5. Walls newly learned during re-verify (bump into a cell with
   map[i]!=2) are tagged `wgen = gen` (current), never stale.

Per R4, each cell is probed at most once per generation: after a
probe its `wgen` equals `gen`, removing it from the stale set.

### 3.4 Worked example: Env C with (5,11) and (10,3)

Initial state for Env C: transferred=1, gen=0, map has (5,11)=2
wgen 0, (10,3)=2 wgen 0, (14,7)=0 (unknown).

1. Action 179: sweep steps S from (14,8) toward target (14,7);
   bump=1. Map said traversable, world said wall: contradiction.
2. T1 fires (transferred==1): gen=1. (14,7) marked wall, wgen=1.
   Stale set: {(5,11), (10,3)}.
3. Re-verify phase: BFS want==3 targets nearest stale cell, e.g.
   (10,3). Planner routes to it; the step onto (10,3) returns
   bump=0 (it is free in Env 1). Log `REVISE C wall removed 10,3`;
   map=1, wgen=1.
4. Next stale cell (5,11): step returns bump=0. Log
   `REVISE C wall removed 5,11`; map=1, wgen=1.
5. Stale set empty; normal sweep resumes; goal reached.
6. Post-run checks: on511>=1, on103>=1, map dump shows c511=1 and
   c103=1. K2 satisfied.

## 4. Cost bound (K3)

- Probes are bounded by the stale count S at T1. Each stale cell is
  probed at most once per generation (R4), so total probes per T1
  event <= S <= W, where W is the number of learned walls (<=20 in
  the 15x15 worlds).
- Each probe costs at most one bump action plus its detour. Let D be
  the longest re-verify detour (D <= 225 cells). Re-verify actions
  per T1 <= S * (D + 1). Practical expectation: tens of actions.
- Zero probes when T1 never fires (Env B: 0 added actions).
- No periodic or timer-based re-probing exists, so there is no
  steady-state cost in a stable environment.

The bound is structural (a function of map contents), not a tuned
constant. A future implementation must report measured re-verify
actions against this bound.

## 5. Alternatives considered and rejected

- Periodic re-probing: nonzero cost in stable environments and a
  hand-tuned period. Rejected under R3.
- Pure optimistic retry (treat all walls as traversable always):
  every plan would repeatedly bump into long-confirmed walls.
  Rejected under R4 (thrash).
- Per-cell decay timers: researcher-tuned thresholds that silently
  set the revision rate. Rejected; the treadmill guard from the
  segmentation review applies: criteria must be event-driven
  comparisons, not hand-tuned timeouts.
- Full re-exploration on T1: discards good map entries and is
  unbounded. Rejected; CTSVR keeps confirmed entries and only
  re-examines the stale set.
- Trigger on any bump (including Env A exploration bumps): would fire
  during initial learning when nothing is stale, adding noise. The
  `transferred==1` condition in T1 exists to prevent exactly this.

## 6. Falsification conditions for a future implementation

A builder implementing CTSVR must preregister separately and freeze
these falsifiers before implementation:

- F1 (thrash): any cell probed twice within one generation.
- F2 (false trigger): any probe occurs in Env B (no T1 possible).
- F3 (revision failure): Env C ends with (5,11) or (10,3) still
  marked wall.
- F4 (cost blowout): re-verify actions exceed 25 percent of the
  control Env C action count (frozen number at prereg time).
- F5 (regression): Env A or Env B action counts differ from the
  published 174 / 186 (CTSVR must be inert when T1 never fires).

## 7. Honest scope

- Bounded L1/L2: the revised structure is the map; the trigger and
  the probe policy are researcher-authored control flow, same as the
  existing bump handler. This design measures a mechanism; it does
  not invent representations.
- Lazy resolution: stale walls that are never visited stay stale.
  Unvisited wrong entries do not affect behavior, so this is a cost
  feature, but any claim of "full map maintenance" would be false.
  Disclosed, not hidden.
- No-drift handling: gradual change that never produces a
  contradiction fires no T1 and gets no revision. CTSVR revises on
  evidence of change, not on suspicion of it.
- Assumes a truthful bump sensor, same as the existing learner.
- This is the map-level analog of doubt triggers: T1 plays the role
  the V-world doubt triggers play in the verification subsystem, and
  the generation counter plays the role of F3's doubt score on
  environment stationarity.

## 8. Kill-bar self-check

- K1 PASS: trigger T1 (bump while transferred==1; section 3.2) and
  revision policy (generation tags, want==3 targeting, probe
  semantics, re-tag on confirm; section 3.3) are specified at
  buildable precision.
- K2 PASS: section 3.4 walks Env C end to end and shows (5,11) and
  (10,3) revised to free with the expected log lines and post-run
  checks.
- K3 PASS: section 4 bounds probes by the stale count and re-verify
  actions by S*(D+1), with zero cost when T1 never fires; no timers
  or periods anywhere in the design.

Builder label: DESIGN-COMPLETE.
