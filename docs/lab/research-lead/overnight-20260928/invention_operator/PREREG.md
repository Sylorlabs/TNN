# PREREG.md -- Invention Operator-Authorship Experiment

**Frozen before implementation. Commit first, then build.**

## Hypothesis

H-OPAUTH-1: A learner given 8 generic transformation primitives (no
pre-assembled invention operator) will, through Q-learning over
consequence history, assemble the extend-sequence
[STAGE, EXEC, PROBE, APPEND, VERIFY, PROMOTE] and use it to solve a
plen-6 invention problem. The assembled sequence is learner-created;
it does not appear in source.

## Background: the operator-authorship boundary

H1/H2/H3 all PASS at L2 but the OPERATORS are researcher-authored:
- H1: `mutate_try` is a monolithic extend function. Learner selects
  parent/fact only.
- H2: fragment extraction + DFS is researcher-designed. Learner selects
  the (m,s,l) triple.
- H3: constraint checkers + backtracking are researcher-designed. The
  driver supplies constraints explicitly.

This experiment decomposes H1's monolithic operator into 8 primitives.
The learner must discover the useful sequence, not just select among
researcher-provided extensions.

## Mechanism

**Primitives** (researcher-provided, generic graph operations):
- OP_STAGE (0): stage longest chain MAP on subject
- OP_EXEC (1): execute staged chain to endpoint
- OP_PROBE (2): find continuing facts past endpoint
- OP_APPEND (3): append continuing fact as new cell
- OP_VERIFY (4): verify extended chain against goal
- OP_PROMOTE (5): promote as new MAP with DEP to parent
- OP_SHRINK (6): remove last cell (distractor)
- OP_SWAPREL (7): change a relation (distractor)

**State**: (done_mask[6 bits], endpoint_live[1 bit]) = 128 states.
**Actions**: 8 primitives. Q-table: 1024 entries, learner-owned.

**Learning**: epsilon-greedy Q-learning. Reward shaping:
+2 STAGE, +2 EXEC, +5 PROBE(hit), +5 APPEND, +10 VERIFY, +100 PROMOTE,
-1 per step, -10 precondition violation. Episode ends on PROMOTE
success or 12 steps or violation.

**Training**: 100 episodes on plen-6 problem (subject 301). Invented
plen-6 MAP deleted between episodes to isolate operator learning.
Q-values persist.

## Kill bars (frozen)

**K1 (discovery)**: After training, greedy policy (eps=0) on plen-6
produces a valid plen-6 MAP (verified, promoted). The action sequence
is a successful extend-sequence.

**K2 (not in source)**: The successful action sequence does not appear
as a literal sequence in source (verified by grep for the op id
sequence).

**K3 (causal)**: Ablation with policy disabled (uniform random actions,
no Q-learning) fails to solve plen-6 within 100 episodes.

**K4 (transfer)**: Greedy policy solves plen-7 (subject 501, different
facts) without additional training.

**K5 (determinism)**: 3/3 byte-identical runs.

K1-K5 must all PASS for INVENTION-OPERATOR-COMPLETE.

## Predicted failure modes

1. Sparse reward: Q-learning may not find the 6-step sequence in 100
   episodes despite shaping. (Would indicate the discovery problem is
   harder than the selection problem.)
2. Reward hacking: learner may find a degenerate sequence that collects
   shaping rewards without solving (e.g., STAGE, EXEC, PROBE, then stop).
   The +100 PROMOTE must dominate.
3. The primitives may be too coarse (each does significant work),
   making this "selection among macro-operators" rather than true
   operator assembly. (Honest bound to record.)

## Honest SUF scope

Researcher-owned: primitives, Q-learning machinery, reward shaping,
state representation, episode structure.
Learner-owned: Q-values, the assembled sequence, the policy.
Claim: the OPERATOR (as an assembled sequence) is learner-created.
The PRIMITIVES are researcher-provided. This moves the boundary from
"operator" to "primitive" but does not reach full L3.
