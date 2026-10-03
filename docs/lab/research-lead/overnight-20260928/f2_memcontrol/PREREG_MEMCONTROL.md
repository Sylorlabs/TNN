# PREREG_MEMCONTROL: F2 Memorization Control

Date: 2026-09-30. Status: FROZEN. This prereg is committed alone before any
implementation file for this wave exists.

## 1. Objective

Run the missing memorization control flagged by the F2 promotion assessment
(ffcfc50e8): "Random control (0/20) proves 'not by luck' but not 'not by a
simpler learner.'" Implement a nearest-neighbor / table-lookup baseline on
the same frozen World A and World B protocols (AUTOSCI2, b9ab0acb6) and test
whether F2's goal achievements are explained by memorization.

## 2. Control design (frozen): MEM-CONTROL

A baseline learner with NO causal machinery:

- No candidate rule generation, no hypotheses, no experiment loop, no rule
  simulation. Source audit must confirm none of these exist in memcontrol.zag.
- Passive phase: identical to F2. 12 steps, same environment schedule, free
  observations (passive observations are free per the AUTOSCI2 prereg).
- Transition memory: records the 11 observed WAIT transitions
  (pre-state to post-state). The post-WAIT snapshot is taken BEFORE the next
  environment passive action, so environment SETs never contaminate a WAIT
  transition. This detail is frozen here.
- Goal planning: the same iterative-deepening search as F2 (same
  digit-to-primitive order, same max depths: 8 for World A; 8 for the World B
  M search), the same goal predicates, the same fixed B2 SUFFIX
  ([OBS Y, OBS K, WAIT] x 3). Simulation uses nearest-neighbor lookup on the
  memorized transitions instead of rule simulation:
  - SET v: state[v] = 1. CLR v: state[v] = 0. Action interface semantics,
    identical to F2's simulator treatment of direct effects.
  - WAIT: nearest memorized pre-state by Hamming distance on the full state
    vector; ties broken by earliest recorded transition (deterministic).
    Apply the recorded post-state.
  - OBSERVE v: read the current state's variable value (needed to simulate
    the B2 SUFFIX observation log).
- Real execution: RESET, goal setup, execute the found plan exactly once,
  verify with the same predicates as F2 (w_goal_met for World A; the triple
  predicate on the real observation log for World B2).
- The memorizer runs NO experiments. It has no model to disagree under, so
  it cannot design discriminating experiments. This is the point of the
  control: it tests whether F2's goal achievement is explained by
  memorized-transition planning without any causal model.

## 3. Sealed worlds (frozen)

world_a2m.zag and world_b2m.zag are copies of world_a2.zag and world_b2.zag
with physics byte-identical; only the main entry call is renamed
(L_run to M_run) so the control links. A diff of each pair must show only
the entry-point hunk changed.

## 4. Kill bars (numbered; frozen)

- K1 (control implemented): pure-Zag memorization baseline as specified in
  section 2; source audit confirms no rule, candidate, hypothesis, or
  experiment machinery.
- K2 (frozen protocol): runs on the sealed World A and World B copies;
  same passive schedule, same planner search order and depths, same goal
  predicates and verification; 3/3 runs byte-identical per world.
- K3 (comparison documented): GOAL_REAL_MEM per world reported against the
  F2 retry results (RESULT_AUTOSCI2: World A GOAL_REAL = 1, World B
  GOAL_REAL_B2 = 1).

## 5. Design prediction (pre-freeze calibration; not a wave result)

Hand analysis of the frozen design predicts the memorizer FAILS both goals:

- World A: the passive WAIT transitions are history-confounded. Example:
  (0,0,0,1) -> (0,1,0,0) was observed only because X had been 1 two steps
  earlier in passive history; the true dynamics are non-Markovian in the
  observed state. The Markov NN model is expected to select [SD,W,W,SX]
  (lexicographically first model-predicted success at depth 4), whose real
  execution yields (1,0,0,0), missing Y=1.
- World B: the model cannot produce three consecutive (Y=1,K=0)
  observations. Y=1 in the model arises only via the single memorized
  (0,0,0) -> (0,1,0) transition, and WAIT always clears Y afterward, so the
  triple predicate is unsatisfiable in the model and no plan is found.

The runs decide. If the memorizer succeeds on either goal, that outcome is
reported as-is; the prediction does not alter any bar.

## 6. Interpretation rule (frozen before results)

- If the memorizer fails both goals while F2 passes both: F2's goal
  achievements are not explained by passive-trace memorization plus
  nearest-neighbor planning. The experiment-constructed causal model is
  doing load-bearing work the memorizer cannot replicate. Report
  MEMORIZATION-TESTED with the threat addressed.
- If the memorizer succeeds on either goal: that goal's result does not
  discriminate F2 from memorization. Report MEMORIZATION-TESTED with the
  weakened scope stated explicitly.

This control does not test convergence (K2-R1/R3/R4): those bars concern
hypothesis formation and elimination, which a memorizer cannot attempt by
construction. The control scopes strictly to the goal-achievement bars
(K2-R5a), which is where the "simpler learner" threat bites.

## 7. Governance

Pure Zag only. No Python anywhere in this wave, including verification and
analysis. Prereg committed alone before any implementation file exists.
Commits local on tnn-native-lab, owned path only:
docs/lab/research-lead/overnight-20260928/f2_memcontrol/. Builder reports
MEMORIZATION-TESTED with comparison only; no SURVIVES claim. No em dashes
in wave documentation.
