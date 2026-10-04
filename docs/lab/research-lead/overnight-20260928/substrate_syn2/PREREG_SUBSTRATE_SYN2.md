# PREREG: Substrate Synergy Phase 2 (procedure to experiment, causal model to memory)

Worker: Substrate Synergy Phase 2 Worker.
Date: 2026-09-30.
Status: FROZEN. Committed alone before any implementation.

## Mission

Phase 1 (SYNERGY-TESTED, c22775f11) showed concept to procedure
(3 vs 23 episodes) and contradiction to revision (168 vs 136).
This experiment tests the two remaining required directions:
procedure to experiment and causal model to memory. The claim is
comparative cross-mechanism utility: mechanism B performs better
consuming mechanism A's output than without it. Coexistence alone
does not count.

## Direction 3: procedure to experiment (experiment efficiency)

### World W3

8 actions a0..a7. Each action has a fixed 1-step observable effect.
Effect table (frozen, permuted so action index carries no
information):

e(a0)=2 e(a1)=5 e(a2)=0 e(a3)=7 e(a4)=1 e(a5)=6 e(a6)=3 e(a7)=4

Passive phase: the learner observes each action once and records a
procedure fact (a_i, "eff", e(a_i)) with support 1 on the substrate.
Both conditions observe the identical passive stream and store the
identical 8 facts.

Hidden outcome rule (world truth, never shown to the planner):
outcome O occurs for pair (x,y) iff e(x)+e(y)=10.

Valid pairs (5 of 64): (1,1) 5+5, (3,6) 7+3, (6,3) 3+7,
(5,7) 6+4, (7,5) 4+6.

Active phase: find one pair producing O with the fewest
pair-experiments. Both conditions test pairs in fixed row-major
order (x=0..7, y=0..7); the planner stops at the first O.

- COND-PROC: the planner may read the ("eff") procedure facts.
  It restricts candidates to pairs with e(x)+e(y)=10 and tests
  them in row-major order. First candidate (1,1) succeeds.
  Predicted N_proc = 1.
- COND-BLIND: the planner may not read the ("eff") facts
  (simulates a planner that ignores the procedure store). It
  tests all 64 pairs in row-major order. First valid pair is
  (1,1) at row-major index 9 (0-based), i.e. the 10th experiment.
  Predicted N_blind = 10.

Metric: N = number of pair-experiments until the first O.

### Measurable prediction P3

N_proc < N_blind (predicted 1 < 10). Rationale: the procedure
store encodes the effect mapping; the planner uses it to prune
59 of 64 candidates before acting. The blind planner must probe
the space in fixed order.

## Direction 4: causal model to memory (retrieval efficiency)

### World W4

40 episodes. Episode i has cause token c_i and effect token e_i
(one-to-one, frozen pairing). Learning phase: the learner observes
all 40 episodes once and stores on the substrate, for both
conditions identically:

- flat episode facts: (ep_i, "cause", c_i) and (ep_i, "effect", e_i),
  80 facts;
- causal index facts: (e_i, "caused_by", c_i), 40 facts.

Retrieval task: 20 probes, the even-indexed effects
e_0, e_2, ..., e_38 in fixed order. For each probe, return the
cause. Retrieval routines (researcher-authored, frozen):

- COND-CAUSAL: one substrate query (e_k, "caused_by", ?) per
  probe. Examinations per probe: 1. Predicted total E_causal = 20.
- COND-FLAT: linear scan of (ep_j, "effect", ?) facts in episode
  order until the value matches the probe, then one query for
  (ep_j, "cause", ?). Examinations per probe: match position
  (1-based) + 1. Probe e_{2k} matches at position 2k+1, so
  examinations = 2k+2 for k=0..19. Predicted total
  E_flat = sum_{k=0..19}(2k+2) = 420.

Metric: E = total substrate fact examinations over the 20 probes;
accuracy = correct causes / 20 (predicted 20/20 for both).

### Measurable prediction P4

E_causal < E_flat (predicted 20 < 420) at equal accuracy 20/20.
Rationale: the causal links act as a direct index from effect to
cause; without them retrieval is a linear scan of episode facts.

## Kill bars (frozen)

- K1 (directions specified): PASS iff this prereg specifies 2
  synergy directions with measurable predictions P3, P4.
  Satisfied by this document.
- K2 (synergy demonstrated): PASS iff P3 and P4 both hold in the
  frozen runs (directional only, no magnitude threshold). If
  either fails, report SYNERGY2-LIMITED with the specific
  divergence and both numbers.
- K3 (purity): PASS iff pure Zag at every stage (source, znc
  build, execution), zero Python invocations, zero em-dash bytes
  in committed files, 3/3 byte-identical runs (md5 recorded),
  exit 0, zero stderr.

## Falsification

- If N_proc >= N_blind: procedures do not improve experiment
  design in this design; report both numbers.
- If E_causal >= E_flat: the causal index adds no retrieval
  value; report both numbers.
- If either condition fails to find O or a cause (accuracy
  shortfall), report SYNERGY2-LIMITED with the shortfall; the
  directional bars require the predicted accuracy levels.

## Honest scope

The effect table, the outcome rule, the episode pairing, the
planner search order, and the retrieval routines are
researcher-authored. The procedure facts and causal index facts
are learned from observation (one observation each, support 1),
but the learning is trivial recording. The synergy claim is
comparative: the experiment planner does better consulting the
procedure store than ignoring it, and the retriever does better
using the causal index than scanning flat episodes. This is not
a claim that the learner invented procedures, causal links,
planning, or retrieval.

## Governance

- Prereg committed alone before implementation.
- Pure Zag only. No Python at any stage.
- No em dashes in documentation.
- Owned path only:
  docs/lab/research-lead/overnight-20260928/substrate_syn2/.
- Commits local on tnn-native-lab. Nothing pushed.
