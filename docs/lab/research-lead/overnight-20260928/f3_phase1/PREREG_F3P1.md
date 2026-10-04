# PREREG_F3P1: F3 Phase 1 -- DNF Representation + Persistent State, R-A/R-B Regression

Date: 2026-09-30. Worker: F3 Phase 1 Builder.
Status: PREREGISTRATION. Frozen before implementation. No implementation exists yet.

## 1. Mission

Build F3 Phase 1 per the frozen design `68aa2f6e8` (F3_DESIGN.md),
build-order item 1: "Representation + persistent state (sections 2-3)
with R-A/R-B."

Phase 1 scope is DELIBERATELY narrow:
- DNF rule-set representation (design section 2).
- 7-item persistent learner state (design section 3).
- OP-PROP (passive proposal, singleton literals, both polarities,
  context guards retained) + OP-PROBE (learned action-effect table).
- Hypothesis-level experiment loop and planning, reading ONLY the
  effect table (no literal action-code branches in decision code).
- Regression worlds R-A and R-B (F2's frozen worlds A and B).

Explicitly NOT in Phase 1 (later phases per design section 11):
- Multi-rule hypotheses (Phase 1 enumerates k=1 rule per effect var;
  the state and simulation support k<=4, but enumeration is single-rule).
- Per-rule refutation (Phase 2; Phase 1 kills whole hypotheses).
- OP-GROW, OP-SPLIT, OP-VAR (Phases 2-4).
- EXTEND/STOP adaptive horizon (Phase 5; Dcur fixed at 4).
- Verification stream, REVISE, doubt gating, history use (Phase 7;
  verify_buf/history/doubt allocated and zeroed, not routed).
- Latent variables (F4).

## 2. Frozen representation (design section 2)

Hypothesis for effect variable V: a SET of rules H_V = {R1..Rk},
0 <= k <= 4. Each rule is a CONJUNCTION of literals.
Each literal is (src, polarity, delay): src in 0..nvars-1,
polarity in {+, -}, delay d >= 1.

Literal (s,+,d) holds at t iff s(t-d)=1.
Literal (s,-,d) holds at t iff s(t-d)=0.

Prediction (frozen): V(t)=1 iff EXISTS rule R in H_V such that EVERY
literal of R holds at t.

Phase 1 refutation (hypothesis-level, F2-analogous): a hypothesis is
eliminated when a real experiment's observation vector disagrees with
its simulated vector. Per-rule refutation arrives in Phase 2.

State encoding (all learner-created, offsets fixed):
- rules[V]: 1 byte nrules + 4 rules x (1 byte nlit + 3 lits x 3 bytes)
  = 41 bytes per var, 4 vars max = 164 bytes.
- effects[a]: action code a = kind*8+v, 16 codes max. 3 bytes each:
  (type, var, val). type in {0=NULL, 1=SETS, 2=ADVANCES_TIME,
  3=OBSERVES}. 48 bytes.
- verify_buf: 16 bytes, allocated, zeroed, NOT routed in Phase 1.
- history: 4 slots x 164 bytes = 656 bytes, allocated, empty.
- doubt[V]: 4 bytes, zeroed, not gated in Phase 1.
- varied[v]: 4 bytes; set to 1 when v is SET/CLR during experiments.
- Dcur: i32 = 4, fixed in Phase 1 (EXTEND is Phase 5).

## 3. OP-PROBE (learned action effects; design section 6)

At start, for each action code a = kind*8+v (kind 0..3, v < nvars):
controlled probe, 3 repetitions, all manipulable vars held at fixed
values via setup actions:
- kind 0 (SET v): setup CLR v (others 1); probe; expect v 0->1.
- kind 1 (CLR v): setup SET all; probe; expect v 1->0.
- kind 2 (WAIT): probe; expect time advance, no var change.
- kind 3 (OBSERVE v): setup SET v; probe; expect return == v pre-state.

Frozen classification (design section 6), with one documented
clarification: SETS records the observed post value, because the
worlds have both SET (to 1) and CLR (to 0) actions and planning needs
both. "Exactly one variable v changes deterministically across 3
probes" -> effects[a] = SETS(v, postval). "Only timestamps advance"
-> ADVANCES_TIME. "Return value equals v's pre-state across probes"
-> OBSERVES(v). Else NULL.

Audit requirement: planning, simulation, and experiment construction
read ONLY effects[]. No kind==0 / kind==1 style branches in learner
decision code. The probe setup itself is harness-side initialization,
not decision code.

## 4. OP-PROP (phase-1 version; design section 4)

From the passive trace (12 steps, same schedule as F2):
for each effect variable V, for each src c != V, polarity in {+,-},
delay d in 1..Dcur:
- Fit: literal true on at least one positive observation (ok > 0)
  AND never refuted (no observation where the literal holds and
  V=0; for polarity - the dual: no observation where s(t-d)=0
  and V=0).
- Context guards (retained from F2; design: "rules gain an optional
  context guard literal"): if ctxvar >= 0, for each passing base
  literal also try guards (ctxvar,+,d) and (ctxvar,-,d); keep the
  guarded rule iff it still has ok > 0 and is never refuted.
  A guard is an ordinary literal in the conjunction.

Each passing (base [+ guard]) becomes a candidate rule.
Hypotheses = Cartesian product of one candidate rule per effect var
(effect var = var with >= 1 candidate), exactly as F2 enumerates.
Each hypothesis is a DNF set with k=1 per var.

Growth trace: every proposal logged as
  PROP V=<v> lit=(<src>,<pol>,<d>) [guard=(<s>,<pol>,<d>)] ok=<n>
and every rule-set construction logged. Dcur=4 logged.

## 5. Experiment loop and planning (phase-1, F2-analogous)

- Disagreement search: iterative-deepening base-B enumeration over
  manipulation primitives from effects[] (SETS codes + ADVANCES_TIME)
  plus OBSERVE codes from effects[], depths 1..6, first sequence with
  >= 1 OBSERVE where live hypotheses' simulated observation vectors
  disagree. Pure simulation; zero world calls during search.
- Execute for real, eliminate disagreeing hypotheses, until nalive=1
  or exhaustion (no disagreeing sequence) or budget out (18 obs).
- Planning: goal mode 0 (World A): BFS over manipulation primitives
  from effects[], final-state goal via w_goal_met. Goal mode 1
  (World B): M-search + fixed SUFFIX ([OBS Y, OBS K, WAIT] x3),
  triple predicate. Both read effects[] only.
- Random-action control: 20 runs, fixed seed 12345, same as F2.

## 6. Worlds and baseline

- R-A: `autosci2/world_a2.zag` (A-confounded-chain), goal mode 0.
  Frozen F2: 2 experiments, GOAL_REAL=1.
- R-B: `autosci2/world_b2.zag` (B-contextual-delay), goal mode 1.
  Frozen F2: 1 experiment, GOAL_REAL_B2=1.
- Worlds concatenated AFTER the learner file at build time from
  their committed paths (not copied into the owned dir).
- The worlds' w_verify is F2-specific (takes F2 hysel/candbuf);
  Phase 1 uses its own adjudication (goal + experiment count) and
  does NOT call w_verify. Documented, not hidden.

## 7. Kill bars (frozen)

- K1: DNF representation + 7-item state implemented as specified
  (auditable offsets, growth trace shows PROP/RULE-SET events,
  no literal action-code branches in decision code).
- K2: R-A: GOAL_REAL=1 AND experiments <= 4 (F2=2, +2).
  R-B: GOAL_REAL_B2=1 AND experiments <= 3 (F2=1, +2).
  (F-COST falsifier: exceeding either bound kills Phase 1.)
- K3: pure Zag (znc/shell/grep/git only, zero python3 invocations),
  zero em/en-dash bytes (byte-checked), 3/3 byte-identical runs per
  world, exit 0, zero stderr bytes.

## 8. Falsifiers

- F-COST: R-A experiments > 4 or R-B experiments > 3.
- F-GOAL: GOAL_REAL=0 on R-A or GOAL_REAL_B2=0 on R-B.
- F-REGRESS: any behavior worse than frozen F2 beyond the +2
  experiment allowance (e.g., truth lost, nalive=0).
- F-PURITY: any Python invocation, any em/en-dash byte, or
  non-deterministic runs.

## 9. Honest scope

Phase 1 is a representation+state migration with no regression, not a
capability advance. The DNF machinery, negative literals, learned
effect table, and growth trace are real; multi-rule sets, per-rule
refutation, growth operators, adaptive horizon, and doubt-gated
planning are later phases. No L3 claim. No SURVIVES claim
(promotion steps 4-11 remain).

## 10. Commit order

This prereg is committed alone before any implementation file exists.
Implementation + results follow in a separate commit. Order verified
with git merge-base --is-ancestor before reporting.
