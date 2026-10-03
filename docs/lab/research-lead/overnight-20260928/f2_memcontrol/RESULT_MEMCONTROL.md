# RESULT_MEMCONTROL: F2 Memorization Control

Date: 2026-09-30. Prereg: c4496e194 (committed before implementation).
Implementation: memcontrol.zag + world_a2m.zag + world_b2m.zag.

## Verdict: MEMORIZATION-TESTED

All three kill bars pass. The memorizer fails both goals that F2 passes.

## Results

### World A (confounded chain)

- K1 PASS: source audit confirms memcontrol.zag contains no candidate rule
  generation, no hypotheses, no experiment loop, no rule simulation. The only
  shared function with the F2 substrate is L_advance, which is the sealed
  worlds' own dynamics engine (called only inside w_act); the memorizer's
  planner never calls it and plans exclusively with M_wait / M_sim
  (nearest-neighbor transition memory).
- K2 PASS: sealed World A copy used (diff against world_a2.zag shows only
  the header comment and the main entry-point hunk changed; physics
  byte-identical). Same passive schedule, same planner search order and
  depths (1..8), same goal predicate (w_goal_met) and real verification.
  3/3 runs byte-identical (md5 f3482554f54c57d45ba7b121cb206963).
- Outcome: the memorizer's NN model selected MEM_PLAN [SD,W,W,SX]
  (lexicographically first model-predicted success at depth 4). Real
  execution yielded (1,0,0,0): X=1, Y=0, D=0. GOAL_REAL_MEM = 0.
- Mechanism of failure (confirmed by the run, predicted in the prereg):
  the passive WAIT transitions are history-confounded. The memorizer
  recorded (0,0,0,1) -> (0,1,0,0), which held in the passive trace only
  because X had been 1 two steps earlier. In the real goal execution that
  history is absent, so the chain the model relied on does not fire. The
  true dynamics are non-Markovian in the observed state; the memorizer's
  Markov model hallucinates a working plan and fails for real.

### World B (contextual delay)

- K1 PASS: same source audit as World A.
- K2 PASS: sealed World B copy used (diff against world_b2.zag shows only
  the header comment and the main entry-point hunk changed; physics
  byte-identical). Same passive schedule, same B2 planner search order
  (M depths 1..8, fixed SUFFIX), same triple predicate. 3/3 runs
  byte-identical (md5 89f29018253af4e7bd3d80e9a9905a95).
- Outcome: MEM_PLAN_B2 none found in NN model. The model cannot produce
  three consecutive (Y=1,K=0) observations: Y=1 in the model arises only
  via the single memorized (0,0,0) -> (0,1,0) transition, and WAIT always
  clears Y afterward, so the triple predicate is unsatisfiable in the
  model. No plan was executed. GOAL_REAL_MEM_B2 = 0.

### K3: comparison with F2 retry (RESULT_AUTOSCI2)

| World | F2 retry (causal) | MEM-CONTROL (memorizer) |
|-------|-------------------|-------------------------|
| A | PLAN [SX,W,W,W,SX], GOAL_REAL = 1, random 0/20 | PLAN [SD,W,W,SX], GOAL_REAL_MEM = 0 |
| B | PLAN_B2 M=[SX,CK,W,SX,W,SX], GOAL_REAL_B2 = 1, random 0/20 | no plan found, GOAL_REAL_MEM_B2 = 0 |

## Interpretation (per the frozen interpretation rule)

The memorizer fails both goals while F2 passes both. F2's goal achievements
are therefore not explained by passive-trace memorization plus
nearest-neighbor planning. The experiment-constructed causal model is doing
load-bearing work the memorizer cannot replicate:

- On World A, the memorizer had every transition it needed in memory and
  still failed, because delay dynamics are history-dependent and a
  state-only lookup misgeneralizes. F2's explicit delay rules reference
  history correctly.
- On World B, the memorizer could not even formulate a plan, because the
  delay-2 contextual law never appears as a stateless transition in the
  passive data. F2's experiment loop isolated the law and its planner
  exploited the timing.

The promotion assessment's strongest threat ("not by a simpler learner") is
addressed for the goal-achievement bars: the simpler learner was built, run
on the frozen protocol, and it loses 0-2.

## Scope and caveats (honest)

1. This control scopes strictly to the goal-achievement bars (K2-R5a). It
   cannot attempt the convergence bars (K2-R1/R3/R4), which concern
   hypothesis formation and elimination; a memorizer has no hypotheses by
   construction.
2. The memorizer was given no experiments (it cannot design them without a
   model). A stronger follow-up control could hand the memorizer F2's
   executed experiments for free and test whether the causal model adds
   anything over nearest-neighbor lookup given identical data. That
   isolates the model from the experiment-construction machinery; this wave
   tested the full pipeline against pure memorization.
3. The NN used Hamming distance with earliest-recorded tie-break, the most
   standard table-lookup choice. Any Markov (state-only) similarity model
   faces the same history-confounding barrier on delay dynamics, which is
   the principled reason for the failure, not a quirk of the metric.

## Purity and determinism

- Wave artifacts written and verified with shell tools only (cat, diff,
  md5sum, grep, znc). No Python was used for any wave work: no analysis,
  no verification, no editing, no harness.
- Disclosure: during setup, one compound shell command contained a stray
  `python3` heredoc whose payload only printed a fixed string to stdout. It
  touched no wave file, performed no analysis or verification, and produced
  no artifact. Noted here so the record is exact.
- 3/3 byte-identical per world (md5 checksums above).
- No em dashes in wave documentation.
- Build reproduction:
  cat memcontrol.zag world_a2m.zag > memcontrol_a_combined.zag
  znc memcontrol_a_combined.zag -o memcontrol_a_bin
  cat memcontrol.zag world_b2m.zag > memcontrol_b_combined.zag
  znc memcontrol_b_combined.zag -o memcontrol_b_bin

## Classification

MEMORIZATION-TESTED. The F2 retry's goal results survive the memorization
control. This does not promote F2 (promotion pipeline steps 4-11 remain for
the parent to schedule); it closes the specific "simpler learner" threat
named in assessment ffcfc50e8.
