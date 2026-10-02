# Beam Evidence-Fit Redesign

Date: 2026-09-30. Worker: Beam Evidence-Fit Redesigner.
Status: DESIGN ONLY. No implementation. No code written.

## Problem statement

Two independent preregistered failures localize the Q4 discovery weakness
to the beam/search mechanism:

**R1 (e40cb1b51):** 8/8 coverage on all 5 seeds, but evidence fit
24-31/32, never 32/32. True accuracy 48-56/64, never 64/64. The beam
cannot fit observed evidence even at full coverage.

**R3 Arm 2 (023b4f84a):** Beam locks from round 6 onto a 3-op expression
containing D that fits growing evidence (up to 29/32) but generalizes
to 53/64. The true 4-op E was never generated in 25 beam extensions.

**Tax-off ties (R1):** 3 of 5 seeds show TAXOFF_UNIQ=0, indicating the
beam retains multiple expressions with equal evidence-fit but different
generalization. Per prereg, a tie indicates harness or beam defect.

## Root cause analysis

The frozen beam (r1.zag, copied from r4.zag and altexp.zag) has three
interacting defects:

### Defect 1: Scalar score collapses competing objectives

The score function is:

    sc = (c * 10000) / en - 200 * opc

where c is correct predictions, en is evidence count, opc is operator
count. This single scalar forces a premature tradeoff between accuracy
and simplicity at every selection step.

At en=32, each correct sample is worth 312.5 points; each operator costs
200 points. A 3-op expression fitting 30/32 scores 8775. A 4-op
expression fitting 31/32 scores 8887 and wins. But a 4-op expression
fitting 28/32 scores 7950 and loses to the 3-op overfitter, even if
that 4-op is on the path to the true 5-op solution. The intermediate
is pruned; the path is lost permanently.

This is the classic beam search pathology: greedy top-32 selection with
a tax-weighted score prunes the path to perfect fit.

### Defect 2: Arbitrary tie-breaking

Selection tie-break chain in beam_extend:

1. Higher score wins.
2. If scores tie, lower opc wins.
3. If opc ties, lower node ID wins.

Node ID is allocation order. It has no semantic meaning. When multiple
expressions fit evidence equally well, the beam's choice among them is
arbitrary with respect to generalization. The tax-off diagnostic
correctly flags this as a defect signal.

### Defect 3: Simplicity tax blocks compositional truth

From R3: the 200/opc tax scores a 3-op overfitter at approximately 9400
(10000 minus 600) versus 9200 for the true 4-op E (10000 minus 800).
The overfitter wins. The greedy beam then builds combinations of
overfitters. The true compositional chain AND(D,Y4) / NOT D /
AND(~D,Y5) is never expressed because its components were pruned.

The tax that helped Phase 1 find minimal D now defeats compositional
reuse. The bias is too strong and applied too early.

## Design: Pareto-diverse beam with evidence-first phasing

### Core principle

Do not collapse accuracy and complexity into a single scalar for
pruning decisions. Maintain the Pareto frontier of non-dominated
expressions, and separate the concerns of fitting evidence (search)
from preferring simplicity (selection).

### D1: Pareto-frontier retention (replaces scalar top-32)

Definition: Expression A dominates B if acc(A) >= acc(B) and
opc(A) <= opc(B), with at least one inequality strict.

The beam retains all non-dominated candidates up to a cap of 64.
Dominated expressions may be pruned. Non-dominated expressions are
never pruned due to beam width.

Consequences:

- The maximum-accuracy expression is always retained. The path to
  32/32 fit cannot be pruned by a simpler lower-accuracy expression.
- At each accuracy level, the simplest expression is retained.
  Simplicity bias is preserved but cannot dominate accuracy.
- The 3-op overfitter (30/32, 3 ops) and a 4-op partial (31/32, 4 ops)
  are both non-dominated. Both survive. The beam does not prematurely
  commit.

This directly addresses Defect 1. If a 32/32-fitting expression exists
in the candidate space, it is non-dominated and survives.

### D2: Two-phase selection (evidence first, simplify second)

The 24-round evidence loop is split:

- Rounds 1 through 16 (exploration): rank candidates by accuracy alone.
  The complexity tax is computed and stored but ignored for retention.
- Rounds 17 through 24 (consolidation): rank by accuracy; break ties
  by lower opc.

The final kept expression (beam index 0) is selected after round 24
by accuracy first, then opc.

Rationale: early rounds must explore the fit landscape without tax
pressure pruning promising paths. Late rounds consolidate toward
simpler expressions among those that fit well. This addresses the
timing aspect of Defect 3: the tax was applied too early, before the
search had found the fit frontier.

### D3: Principled tie-breaking (replaces node-ID arbitrariness)

When accuracy and opc are both tied, break ties by:

1. Evidence disagreement: prefer the expression whose pattern of
   correct predictions differs most from the beam consensus. Compute
   for each tied candidate the Hamming distance between its
   correct/incorrect vector and the majority vote vector across tied
   candidates. Prefer larger distance. Rationale: among equally
   fitting expressions, the most distinctive is most informative for
   the IV policy and least likely to be a trivial variant.

2. Structural novelty: prefer the expression whose operator multiset
   differs most from other beam members. Compute histogram of
   operators (AND, OR, XOR, NOT counts); prefer larger L1 distance
   from the beam mean histogram. Rationale: prevents beam collapse
   to syntactic variants of one form.

3. Recency: prefer higher node ID (more recently generated).
   Rationale: favors exploration over exploitation. This reverses the
   current arbitrary bias toward older nodes.

This addresses Defect 2. Ties are broken by criteria related to
informativeness and diversity, not allocation order.

### D4: Diversity floor (prevents beam collapse)

Reserve 8 of 64 Pareto slots for diversity candidates:

- 56 slots: top by Pareto rank (non-dominated, then by D2/D3 order).
- 8 slots: candidates maximizing structural novelty relative to the
  top 56, regardless of Pareto rank (but still requiring acc >= 50%
  to avoid pure noise).

Rationale: R3 showed the top hypotheses collapsing to overfitter
variants. A diversity floor ensures structurally different
expressions survive even when temporarily outscored, preserving the
option value of alternative structural hypotheses.

### D5: Honest tie reporting (replaces taxoff_unique)

Replace the binary taxoff_unique diagnostic with a tier report:

- Compute the maximum accuracy A_max across the beam.
- Count N_tie = number of beam members with acc == A_max.
- Report the opc range [min, max] within the max-accuracy tier.
- If N_tie == 1: report UNIQUE.
- If N_tie > 1: report UNDERDETERMINED(N_tie, opc_range), not DEFECT.

Rationale: a tie is not necessarily a defect. It may be genuine
underdetermination: the evidence does not distinguish among N
expressions. The honest signal is the count and complexity spread,
which informs the IV policy (more interventions needed) rather than
invalidating the seed. The current diagnostic conflates
underdetermination with implementation defect. Only flag DEFECT if
N_tie > 1 AND all tied expressions are syntactically identical
(indicating a deduplication failure).

## Expected behavior

On R1 F-PARCOND: the Pareto beam retains high-accuracy expressions
even when complex. Two-phase scoring finds the fit frontier in early
rounds without tax pruning. Expected outcome: EVFIT 32/32 on seeds
where a fitting expression is reachable by the candidate generator.

On R3 Arm 2: the 3-op overfitter and 4-op partials coexist as
non-dominated. The components of true E survive because they are not
dominated. The diversity floor prevents collapse to overfitter
variants. Expected outcome: E generated and selected, 64/64.

## Non-goals and honest scope

- The operator set is unchanged (AND, OR, XOR, NOT over terminals).
- Candidate generation is unchanged (beam combinations plus NOT).
  D1 through D5 affect only retention, ranking, and reporting.
- No new semantic cases. No researcher-authored solutions.
- This is a search improvement within bounded L2. It does not invent
  representations and makes no L3 or Criterion 0 claim.
- Generalization (64/64 true accuracy) still depends on the evidence
  being representative. Fitting 32/32 does not guarantee truth.

## Falsifiers for a future implementation

A builder implementing this design should preregister:

- F-FIT: on a task where a 32/32-fitting expression is in the
  reachable candidate space, EVFIT must equal 32/32.
- F-NODOM: instrument the beam to log every pruned candidate; assert
  no pruned candidate was non-dominated at prune time.
- F-TIE-HONEST: on a task with known underdetermination, the report
  must say UNDERDETERMINED with correct N_tie, not DEFECT.
- F-NOREGRESS: on Phase-1 tasks where the old beam achieved 64/64,
  the new beam must also achieve 64/64.

## Implementation estimate (for planning, not this task)

Approximately 200 lines changed in beam_extend (Pareto filter,
two-phase comparator, diversity selection), approximately 50 lines
for D3 helpers (disagreement distance, histogram distance) and D5
reporting. All implementable in pure Zag with existing primitives.
No new data structures beyond fixed-size arrays.

## Kill bar self-check

- K1 (design complete): this document specifies D1 through D5 with
  rationale, expected behavior, non-goals, falsifiers, and estimate.
- K2 (addresses evidence-fit failure): D1 preserves the max-accuracy
  path; D2 removes early tax pressure; D4 prevents collapse. Each
  defect maps to at least one design component.
- K3 (no implementation): no .zag file written or modified. No
  compiler invoked. Design only.
