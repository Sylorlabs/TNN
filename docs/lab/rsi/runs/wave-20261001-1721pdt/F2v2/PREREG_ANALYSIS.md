# PREREG_ANALYSIS.md - F2 v2 (wave-20261001-1721pdt, lane F2v2)

Written BEFORE any implementation file exists. This is the prereg analysis
step. Commit-order rule: the frozen prereg (df0c7ed64) was committed alone
before any implementation; this analysis is written before implementation
files so the coordinator can order commits correctly.

## Frozen prereg under implementation

- Commit: df0c7ed64, "FREEZE F2 v2 prereg (writing-only; committed alone
  before any implementation)". File:
  docs/lab/rsi/runs/wave-20261001-1421pdt/f2_retry/PREREG_F2_V2.md
- Read fully on 2026-10-01. No .zag for F2 v2 existed at freeze time.

## Prior history (sourced per prereg section 2)

- F2 v1 (autosci, prereg 2a87efa77, result 4ebde580a, 2026-09-30):
  BUILD-FAIL on K-AS5b. The loop worked in both sealed worlds; World B's
  goal (transient Y=1 within 6 steps, ~5% random base rate) was a weak goal
  instance that the frozen random control hit 1/20 on seed 12345.
  Bar failure, not loop failure.
- F2 retry (autosci2, prereg b9ab0acb6, result 2026-09-30): harder World B
  goal B2 (three consecutive steps with Y=1 AND K=0; 0/160 random
  pre-freeze) achieved BUILD-PASS on all seven bars with no architectural
  changes. Memorization control and independent reproduction later closed.
- This v2 is the next harder step, harder than B2 in four ways: two
  independent contextual laws (not one), two delays (2 and 3) managed
  simultaneously, two context variables BOTH actively verified (J=0, K=1;
  persistent, not self-maintaining), and fresh sealed physics (World C).

## Objective

Test the unchanged F2 loop (passive hypotheses, disagreement-driven
experiment construction, elimination, model-based goal planning) on fresh
sealed World C with sustained dual contextual goal C2: three consecutive
steps with (Y1=1 AND J=0 AND Y2=1 AND K=1). World A (confounded chain)
replicated exactly as regression anchor.

## Frozen kill bars (K3-R1..R7)

- K3-R1: >= 2 hypotheses fully consistent with passive trace, EACH world.
- K3-R2: construction not enumeration. Source audit: no complete
  experiment/plan literal in source; iterative-deepening composition over
  primitives only; SUFFIX_C is the preregistered fixed measurement
  protocol (disclosed, no manipulations). Executed experiments AND goal
  plans differ across worlds in composition.
- K3-R3: every executed experiment logged with per-hypothesis predicted
  observation vectors showing disagreement; world-action counter proves
  zero real-world actions during search.
- K3-R4: World A: true hypothesis {Z<-(X,2), Y<-(Z,1), D<-(X,1)} survives
  AND loop ends by search exhaustion to depth 6 (nalive=2 equivalence
  class, as in AUTOSCI2). World C: exactly one survivor, equal to the
  true law pair {(X,2,J=0), (X,3,K=1)}.
- K3-R5: World A: planned sequence achieves Goal A for real AND random
  control 0/20. World C: full plan (M+SUFFIX_C) achieves C2 for real AND
  random control (7-symbol alphabet, len(M)+17, seed 12345) 0/20.
- K3-R6: total active-phase OBSERVE actions across BOTH worlds <= 28.
- K3-R7: 3/3 byte-identical runs per world; pure Zag; no em dashes in docs.
BUILD-PASS requires all seven in both worlds. No promotion claims.

## Implementation plan

Base: the F2/AUTOSCI2 learner logic (BUILD-PASS), reused unchanged in
structure. Generic adaptations required by the prereg (all in scope):

1. Per-world passive length: w_npass() (12 for A, 14 for C); trace stride
   parameterized (was hardcoded 12).
2. World-provided CONTEXT SETS: w_nctx(), w_ctx_cx(i), w_ctx_cv(i),
   replacing the single ctxvar. World A: {ALWAYS}. World C: {ALWAYS,
   (J==0), (J==1), (K==0), (K==1)}.
3. Declared-context-variable PERSISTENCE in the shared generic advance
   (prereg section 4): persistent vars retain value across WAIT in BOTH
   the sealed world and the learner simulation ("Both use the same
   generic advance function"). Persistence set derived generically from
   the context set (a variable appearing as a non-ALWAYS cx). This is
   disclosed physics, not a learner change and not a per-world case.
4. Candidate generation SKIPS declared persistent variables as EFFECTS.
   Rationale: section 4 states they "retain their value across WAIT and
   change only via SET/CLR", so no rule can govern them. Hypothesizing
   rules for them would create inert hypotheses (identical predictions in
   sim and reality by construction) that can never be discriminated,
   making K3-R4 incoherent. Causes may still be J/K; contexts reference
   them. This follows the disclosed physics, not a world-specific rule.
5. X (controllable, non-persistent) REMAINS a candidate effect, per 6.2
   ("for each effect variable e", "No other filter"). The prereg's
   design-calculation count ("cross product: 9") is explicitly NOT frozen
   ("the exact count is verified at runtime, not frozen"); K3-R1 needs
   only >= 2.
6. Observation budget L_BUDGET = 28 (prereg section 3 change 7). Enforced
   per world in code; K3-R6 total verified across both world outputs in
   the build record (separate binaries cannot share a counter).
7. World C goal mode (gmode 2): C2 planner (iterative deepening depths
   1..9 over the prereg's LISTED 7-symbol order {SET X, CLR X, SET J,
   CLR J, SET K, CLR K, WAIT}; for each M simulate M + 3 WAITs under the
   first survivor and take the first M whose trajectory contains three
   consecutive (Y1=1,J=0,Y2=1,K=1) steps); SUFFIX_C = [OBS Y1, OBS J,
   OBS Y2, OBS K, WAIT] x 3 constructed programmatically (no literal);
   full plan M + SUFFIX_C executed once for real; C2 random control over
   the 7-symbol listed manipulation alphabet, fixed-seed LCG
   (seed 12345, multiplier 1103515245, mod 2^31), length len(M)+17,
   semantic trajectory predicate (cause, not observe).

## Runtime predictions (design calculations, NOT frozen, to verify)

- Candidate counts: the hand calculation in prereg section 5 lists only
  Y1/Y2 X-based candidates, but a full 6.2 enumeration also admits X
  self-consistency candidates (period-4 pulses: (Y1,2),(Y2,1),(X,4) with
  spurious contexts), Y1 self-loop (Y1,4) and cross (Y2,3) candidates,
  and Y2 cross (Y1,1) and self-loop (Y2,4) candidates. Expect roughly
  X:9, Y1:9, Y2:9 (729 hypotheses), not 9. K3-R1 (>=2) is unaffected.
- Risk to K3-R4 (World C): X-rule variants appear indistinguishable
  within the frozen search depth 6 (distinguishing any pair needs a J/K
  manipulation plus an X observation = 7 primitives minimum), and no
  selected sequence (<= 6 primitives) can expose them, because exposing
  an X-rule needs OBS X at t>=4 plus a disagreeing observation. If the
  loop reaches Y1/Y2 pinned to truth with the X-variant class intact, it
  will exhaust with nalive > 1 and K3-R4 will FAIL. This is an empirical
  question; the build record will report the actual experiment
  trajectory, survivor count, and verdict honestly.

## Files to be created after this analysis

f2v2_learner.zag (generic learner), f2v2_world_a.zag (World A replicate),
f2v2_world_c.zag (World C fresh sealed), build.sh, run logs (3x per
world, sha256), BUILD_RECORD.md (per-bar numbers, determinism evidence,
BUILD-PASS or BUILD-FAIL with killing evidence).
