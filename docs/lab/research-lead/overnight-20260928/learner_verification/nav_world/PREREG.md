# PREREG: Learner-Owned Verification of Composition via World Execution (H-LVNAV-1)

## Identity
- Worker: Learner-Owned Verification Worker (H-LVNAV-1, subagent, 2026-10-02)
- Mission: remove expected-answer dependency from composition verification.
  The learner commits to a composed MAP, EXECUTES it in a simulated world,
  observes the consequence, and judges success/failure from the world state,
  not from a harness answer key.
- Prereg frozen: this file is committed ALONE before any implementation file.
  Any design change requires transparent amendment and re-freeze, never a
  silent edit.
- Pure Zag. Paper untouched. Nothing pushed. 0 modes/bridges/handlers.
- Zero em/en dashes in this document.
- Lane directory: docs/lab/research-lead/overnight-20260928/learner_verification/nav_world/
  (a subdirectory: the parent learner_verification/ lane holds C181, already
  COMPLETE; this experiment must not overwrite it).

## Background
- Micah 2026-10-02 directive #5: reduce dependence on harness expected
  answers; prefer learner commitment -> world consequence -> learner-owned
  evaluation.
- C277: H1 (learned typed contracts) + H2 (value-level function composition)
  are canonical for cross-domain composition. C278: L2 operators
  EXTEND/TRUNCATE/SPECIALIZE adapt compositions. Verification in both still
  uses harness expected answers.
- Prior verification lanes: composition_learnerver (H-COMPVER-1, COMPLETE)
  replaced expected-answer DFS termination with learner prediction;
  composition_verify (iv lane) implemented commit -> downstream gate ->
  confidence update on abstract parity values. Neither executes a composed
  MAP in a stateful simulated world with rich unambiguous feedback, and
  neither measures agreement between learner-owned verification and harness
  verification with characterized divergence. This experiment does both.

## Design (frozen)

### World (environment; fixed law, no per-query expected values)
- 8x8 grid. Cell (x,y), x east 0..7, y north 0..7. Cell code = y*8+x.
- Start (0,0). Task goal (7,7), code 63. The goal is the task specification,
  known to the learner; it is not an answer key.
- Two world variants: OPEN (no special cells) and LAVA (lava cells at
  (3,0),(4,0),(5,0), codes 3,4,5).
- Frozen movement law: step E: x=min(x+1,7); step N: y=min(y+1,7).
  Entering a lava cell sets burned=1; the agent keeps moving.
- World state records: agent position, burned flag, step count, full trace
  of visited cells (max 14), variant. World state is written ONLY by
  world_* functions (world_reset, world_place, world_step, world_execute).
  The driver never writes world state directly.

### MAPs (learner-created executable structures)
- Node lists in a learner-owned arena. Node = 8 bytes: opcode u8 at offset
  0 (0=E, 1=N), next-node i32 at offset 4 (-1 = end).
- Primitive MAPs: X = 7 E-nodes; Y = 7 N-nodes; Xb = 3 E-nodes (short/broken).
- Composition (learner operation, H2-style chaining): compose(a,b) copies
  both node lists into a fresh arena region, links them, and returns a NEW
  MAP descriptor. The composed chain is a new persistent structure that did
  not exist before composition.

### Contract induction (learner operation, general frozen rule)
- Probe a MAP twice from fixed starts using the world movement law in the
  OPEN variant (prior experience; the LAVA world is new terrain at trial
  time). Contract = displacement (dx,dy) of probe 1; if probe 2 displacement
  differs, contract = UNKNOWN (-999,-999).
- Frozen probe starts (experimental setup): east-movers (X, Xb) from (0,0)
  and (0,5); north-mover (Y) from (0,0) and (5,0).
- Resulting contracts: X=(7,0), Y=(0,7), Xb=(3,0).

### Learner prediction, commit, verdict (learner-owned)
- Prediction: predicted final = start + (dx1+dx2, dy1+dy2) from the two
  composed contracts, clamped to 0..7, encoded as a cell code. Computed from
  induced contracts only.
- Commit: learner_commit stores (composed MAP id, predicted cell,
  status=PENDING) in learner state. The commitment is logged BEFORE any
  execution of that trial.
- Execution: the driver reads the committed MAP id from learner state and
  runs world_execute on exactly that MAP. The driver never selects a
  composition.
- Learner-owned verdict (frozen rule): PASS iff final==goal AND burned==0
  AND final==predicted. It reads ONLY world state (final cell, burned flag)
  and the learner's own commitment (predicted cell). It never consults any
  harness expected value. Status becomes RESOLVED.

### Harness verification (status quo, driver side only)
- HV (value key): researcher expected final = 63. Verdict: PASS iff the
  learner's committed prediction == 63.
- HT (trace key): researcher expected trace = canonical X;Y trace, codes
  1,2,3,4,5,6,7,15,23,31,39,47,55,63. Verdict: PASS iff the executed trace
  matches cell by cell (length 14 required).
- The tokens hv_expected and ht_expected appear ONLY in lv_main.zag
  (driver/harness block); they never appear in lv_mech.zag (learner/world).
  No learner function ever receives an expected value.

### Battery (frozen)
- IND: run the frozen probes, induce and store the three contracts, log
  probe deltas and induced contracts.
- T1: OPEN world, compose X;Y, start (0,0).
  Expect L=PASS, HV=PASS, HT=PASS.
- T2: OPEN world, compose Xb;Y, start (0,0).
  Expect L=FAIL, HV=FAIL, HT=FAIL.
- T3: LAVA world, compose X;Y, start (0,0).
  Expect L=FAIL, HV=PASS, HT=PASS. Preregistered divergence D1: both harness
  keys under-specify the task (neither expresses "arrive unburned"); the
  learner's world-state observation catches the lava violation that the keys
  cannot see.
- T4: OPEN world, compose Y;X (alternative route), start (0,0).
  Expect L=PASS, HV=PASS, HT=FAIL. Preregistered divergence D2: the trace
  key over-specifies; it rejects a valid alternative derivation that
  reaches the goal cleanly.
- CTRL arm (prediction-only verdict, no world read): verdict = (predicted
  == goal). Expect T1 PASS, T2 FAIL, T3 PASS (spurious: the lava violation
  is unobserved without world execution), T4 PASS. Proves world observation
  is load-bearing for D1.

### Honest labeling
- Researcher scaffold: trial composition choice (which MAPs per trial),
  probe starts, the verdict rule (goal + unburned + prediction-consistent),
  the world law, the harness keys.
- Learner-owned: the composed structures, the induced contract values, the
  prediction values, the world-state observation, the verdict computed from
  that observation. The harness keys are never consulted by the learner
  path.

## Frozen kill bars
- K1 (prereg order): this file committed alone before any implementation
  file; verified by commit order in git log.
- K2 (determinism): 3 runs byte-identical (sha256sums + cmp).
- K3 (boundary audit): grep shows hv_expected/ht_expected only in
  lv_main.zag, zero occurrences in lv_mech.zag; direct writes to world
  state cells occur only inside world_* functions; the driver contains zero
  direct world-state writes.
- K4 (commit before execution): in the transcript, each trial's COMMIT line
  has a smaller line number than its EXEC, CONSEQUENCE, and LEARNER-VERDICT
  lines; status=PENDING is logged at commit time.
- K5 (preregistered verdicts): T1 (PASS,PASS,PASS), T2 (FAIL,FAIL,FAIL),
  T3 (FAIL,PASS,PASS), T4 (PASS,PASS,FAIL) for (L,HV,HT); CTRL T3 = PASS.
- K6 (agreement measured and explained): learner-vs-HV agreement 3/4 (75%),
  learner-vs-HT agreement 2/4 (50%); both divergences match D1/D2 with the
  preregistered explanations; no unpreregistered divergence.
- K7 (toolchain): build.sh guard aborts if python3/python resolve in PATH;
  no forbidden executable invoked (NAMECHECK.md Step 0).
- K8 (governance): 0 modes/bridges/handlers; paper untouched; nothing
  pushed; zero em/en dashes in docs; explicit pathspecs on every git
  add/commit.

## Verdict on pass
LEARNER-VERIFICATION-COMPLETE (with agreement rates vs harness: 3/4 vs the
value key, 2/4 vs the trace key, divergences characterized as D1/D2).
