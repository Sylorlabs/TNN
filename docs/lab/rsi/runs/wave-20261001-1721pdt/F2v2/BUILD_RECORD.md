# BUILD_RECORD.md - F2 v2 (wave-20261001-1721pdt, lane F2v2)

Date: 2026-10-01. Frozen prereg: df0c7ed64 (PREREG_F2_V2.md, read fully
before implementation). Builder: replacement worker (prior lane worker
produced no output). Pure Zag; safebin toolchain guard recorded in
NAMECHECK.md Step 0 (python3/python absent; no forbidden executable invoked).

## Verdict: BUILD-FAIL

Killing bar: K3-R4 in World C. All other bars pass in both worlds.
No promotion claims are made (prereg section 9 boundaries apply).

## What was built

Three Zag sources (all under this lane dir), concatenated at build time:

- f2v2_learner.zag: generic F2 autonomous-scientist loop, adapted from the
  BUILD-PASS AUTOSCI2 learner strictly within prereg scope:
  per-world passive length (w_npass), world-provided context sets
  (w_nctx/w_ctx_cx/w_ctx_cv), declared-context-variable persistence in the
  shared generic advance L_advance (prereg section 4; used identically by
  sealed worlds and learner simulation), candidate generation skipping
  declared persistent vars as effects (disclosed physics: they change only
  via SET/CLR), observation budget 28, and the new C2 goal planner
  (L_plan_c2) plus C2 random control.
- f2v2_world_a.zag: World A (confounded chain) REPLICATED EXACTLY from
  F2/AUTOSCI2 (same physics, goal, planner, control); context set {ALWAYS}.
- f2v2_world_c.zag: World C (dual contextual delay), FRESH sealed physics
  per prereg section 5: X->Y1 delay 2 iff J==0; X->Y2 delay 3 iff K==1;
  J,K persistent; passive 14 steps with X at t=2,6,10 and J=0,K=1
  throughout; goal C2 setup J=1, K=0 by reset.
- build.sh: concatenation + znc compile (both binaries built clean).

## Per-bar results

### World A (regression anchor; 3/3 runs sha256 e0add990b02f66c22bf27b9c4396cc1d7407960e5066131b1b77b68fb72ec2c)

| Bar | Result | Numbers |
|-----|--------|---------|
| K3-R1 | PASS | NHYP 6 >= 2 (candidates X:0, Z:2, Y:3, D:1) |
| K3-R2 | PASS | source audit: no experiment/plan literal; experiments composed by iterative-deepening base-B enumeration; SUFFIX n/a (final-state goal) |
| K3-R3 | PASS | 3 search rounds, world_calls=0 every round; both executed experiments logged with per-hypothesis predictions showing disagreement |
| K3-R4 | PASS | true_h=2 alive=1, nalive=2, exhausted=1 (observational equivalence class, as in AUTOSCI2) |
| K3-R5a | PASS | PLAN [SX,W,W,W,SX], PLAN_AGREEMENT 1, GOAL_REAL 1 |
| K3-R5b | PASS | RANDOM_BASELINE 0/20 (fixed seed 12345) |
| K3-R6 | PASS | OBS_USED 6 <= 28 |
| K3-R7 | PASS | 3/3 byte-identical; pure Zag; no em dashes |

Program verdict line: F2V2_A PROGRAM_ALL_BARS_PASS (MASK 63).

### World C (fresh sealed; 3/3 runs sha256 4165ac70b2f3a6bd7525f82166175d25ade0e1870f1b684b59398fc4ee658cb3)

| Bar | Result | Numbers |
|-----|--------|---------|
| K3-R1 | PASS | NHYP 216 >= 2 (candidates X:6, Y1:6, Y2:6, J:0, K:0; cross product 6x6x6) |
| K3-R2 | PASS | source audit: no experiment/plan literal; SUFFIX_C constructed programmatically in a loop (disclosed protocol, no manipulations); executed experiments and goal plans differ across worlds in composition |
| K3-R3 | PASS | 6 search rounds, world_calls=0 every round; all 5 executed experiments logged with per-hypothesis predictions showing disagreement |
| K3-R4 | FAIL | true_h=83 alive=1, ty1=1, ty2=2, nalive=4, exhausted=1 (needs exactly one survivor) |
| K3-R5a | PASS | PLAN_C2 M=[SX,CJ,SK,W,SX,W,SX,W,SX] (9 primitives, full_len=24), PLAN_AGREEMENT 1, GOAL_REAL_C2 1 with obs=[1,0,1,1;1,0,1,1;1,0,1,1] |
| K3-R5b | PASS | RANDOM_BASELINE_C2 0/20 (7-symbol listed alphabet, length 26, seed 12345, semantic trajectory predicate) |
| K3-R6 | PASS | OBS_USED 17 <= 28 |
| K3-R7 | PASS | 3/3 byte-identical; pure Zag; no em dashes |

Program verdict line: F2V2_C PROGRAM_FAIL (MASK 31; bit5 = K3-R4 missing).
K3-R6 total across both worlds: 6 + 17 = 23 <= 28: PASS.

## Killing evidence (K3-R4, World C)

The experiment loop ran 5 discriminating experiments (all with logged
disagreement and zero world calls during search):

1. [SX,W,W,OY1] actual [1]: killed 144 (Y1 rules (Y2,3,*) and (X,2,K=1),
   exposed because K=0 after reset). nalive=72.
2. [SX,SJ,W,W,OY1] actual [0]: killed 36 (Y1 rule (X,2,ALWAYS), exposed by
   J=1 blocking). nalive=36. Y1 pinned to (X,2,J=0) = truth.
3. [SX,W,W,W,OY2] actual [0]: killed 24 (Y2 rules (X,3,ALWAYS),
   (X,3,J=0), (Y1,1,*), exposed because K=0 after reset). nalive=12.
4. [SX,W,SK,W,W,OY2] actual [0]: killed 6 (Y2 rule (Y1,1,K=1), exposed by
   SET K then observing). nalive=6. Y2 pinned to (X,3,K=1) = truth.
5. [SX,W,W,W,W,OX] actual [0]: killed 2 (X rules (Y1,2,ALWAYS) and
   (Y1,2,J=0), exposed by X decay). nalive=4.

Round 6: EXHAUSTION (no disagreeing sequence to depth 6 among survivors).

Survivors [80,81,82,83] share the TRUE Y1/Y2 rules (true_h=83 alive) but
differ only in the X rule: (Y1,2,K=1), (Y2,1,ALWAYS), (Y2,1,J=0),
(Y2,1,K=1). X is a candidate effect under the frozen generic rule
(prereg 6.2: "for each effect variable e", "No other filter"); its
period-4 pulse structure makes these rules sufficient on the passive
trace. These four X-rule variants are pairwise indistinguishable within
the frozen search depth of 6: distinguishing any pair requires
manipulating J or K and then observing X (minimum 7 primitives), and any
sequence that could expose an X rule needs OBS X at t>=4 plus a
disagreeing observation (also 7+ primitives). The full depth-6 scan at
round 6 confirmed zero disagreement. They therefore survive to exhaustion
as an observational equivalence class, so nalive=4, not 1.

K3-R4 demands "exactly one survivor, equal to the true law pair".
nalive=4 violates it. This is a bar failure, not a loop malfunction: the
loop correctly identified both true contextual laws (Y1 and Y2 pinned to
truth, true_h alive), and the goal phase then SUCCEEDED on the learned
model (GOAL_REAL_C2=1, agreement 1, control 0/20), because the sustained
dual goal depends only on Y1/Y2. But the frozen bar is explicit, so the
verdict is BUILD-FAIL.

Note on the design calculation: prereg section 5 predicted "cross
product: 9 hypotheses" by hand, but the prereg explicitly leaves the
exact count to runtime ("verified at runtime, not frozen"). The runtime
count is 216 (X:6, Y1:6, Y2:6; self-causes excluded by the generic
c!=e condition; J,K excluded as effects by the disclosed persistence
physics). K3-R1 (>=2) is unaffected. The deeper issue is not the count
but the X-variant equivalence class described above, which the frozen
depth-6 search cannot resolve.

## Determinism evidence (K3-R7)

- Zero randomness in decision paths: no RNG in the learner; the only
  stochastic element is the random-action CONTROL, which uses a fixed-seed
  LCG (seed 12345, disclosed a priori) and does not feed back into any
  decision.
- World A: 3/3 runs byte-identical, sha256
  e0add990b02f66c22bf27b9c4396cc1d7407960e5066131b1b77b68fb72ec2c.
- World C: 3/3 runs byte-identical, sha256
  4165ac70b2f3a6bd7525f82166175d25ade0e1870f1b684b59398fc4ee658cb3.
- Pure Zag: implementation, build (znc via safebin), execution, and log
  handling used only the 36 safebin tools; `which python3` and
  `which python` return nothing; no forbidden executable invoked.
- No em dashes in any wave documentation (verified by grep).

## K3-R2 source audit detail

- grep for hardcoded sequence arrays in all three .zag files: none found.
- Experiments are produced exclusively by L_find (iterative deepening,
  depths 1..6, base-B composition over the primitive alphabet, first
  disagreeing sequence with >=1 OBSERVE).
- Goal plans are produced exclusively by L_plan (World A) and L_plan_c2
  (World C: depths 1..9 over the prereg's listed 7-symbol order).
- SUFFIX_C ([OBS Y1, OBS J, OBS Y2, OBS K, WAIT] x3) is built by a
  counted loop, not a literal; it is the preregistered fixed measurement
  protocol (disclosed in prereg, contains no manipulations).
- Executed experiments differ across worlds (A: [SD,W,OZ], [SD,W,W,OY];
  C: [SX,W,W,OY1], [SX,SJ,W,W,OY1], [SX,W,W,W,OY2], [SX,W,SK,W,W,OY2],
  [SX,W,W,W,W,OX]). Goal plans differ (A: [SX,W,W,W,SX] len 5;
  C: [SX,CJ,SK,W,SX,W,SX,W,SX] len 9).

## Honest boundaries (prereg section 9; what this does and does not establish)

- The World C goal result (GOAL_REAL_C2=1, control 0/20) is bounded L2
  structural learning on one fresh sealed world, not L3 and not broad
  generality. The BUILD-FAIL on K3-R4 further bounds it: the loop did not
  isolate a unique hypothesis.
- No claim is made beyond the two tested worlds.

## Architecture accounting

- Cognition source lines added: learner ~700 lines (generic F2 loop
  reuse with prereg-mandated generic adaptations); worlds are authored
  test substrate, not cognition.
- New hardcoded semantic cases: 0.
- New modes / bridges / routers / task-specific handlers: 0.
- New learner-state structures: 0 (hypotheses remain rule-set data;
  persistence is a generic advance property, not a per-world case).

## Files (all under docs/lab/rsi/runs/wave-20261001-1721pdt/F2v2/)

- NAMECHECK.md (Step 0 toolchain guard)
- PREREG_ANALYSIS.md (prereg analysis, written before implementation)
- BUILD-LOG.md (file-creation order)
- f2v2_learner.zag (generic learner)
- f2v2_world_a.zag (World A replicate)
- f2v2_world_c.zag (World C fresh sealed)
- build.sh (build script)
- world_a_run1/2/3.log (3/3 byte-identical)
- world_c_run1/2/3.log (3/3 byte-identical)
- BUILD_RECORD.md (this file)
