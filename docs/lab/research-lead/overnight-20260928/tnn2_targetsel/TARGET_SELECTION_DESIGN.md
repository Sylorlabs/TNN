# Target-Selection Policy Design for Graph Composition

**Status: NOT IMPLEMENTED.** This document is design only. No source was
modified, no binary was built, no experiment was run. It answers six
design questions for the coordinator. Any TNN-3 work that follows must
go through its own preregistration with frozen kill bars.

Date: 2026-10-01. Designer: Target-Selection Policy Designer.
Verdict on completion: TARGET-SELECTION-DESIGN-COMPLETE.

Read-only sources: MUL comparator report (`tnn2_mulcompare/`,
commit `e2e34a4ac`); H3 feasibility probe (`tnn2_h3probe/`, commit
`94cecdba4`); `tnn2.zag` at frozen `f4de7ff46`; interaction analysis
(commit `9009ff259`); alternative-explanation attack (commit
`ccee9e5e6`).

## 0. The decision to be designed

The MUL comparator's finding, quoted verbatim: "TNN-2 accumulates many
MAPs, so composition needs a **target-selection policy** MUL Rung B
never had to solve. That decision is the underexploited site of learner
authority."

MUL Rung B's Phase 3b had exactly one PROC in the workspace (the
learner-built ADD), so CALL target selection was trivial. TNN-2's
`t2_trial` promotes a MAP (tag 20 node) per verified graph, and a
continuing learner accumulates many. If a future trial loop composes
promoted graphs via inlining (the comparator's freeze-compatible
route), someone must decide *which* MAPs to splice into a new
candidate, in what order, under what budget. Today that decision is
nobody's design: not researcher-authored (there is no fixed order to
parameterize), and not learner-authored (nothing reads MAPs on the
proposal path at all).

MAP layout, for reference (from `promote_graph`, lines 533-544):
field4 = r, field8 = s, field20 = graph root, field24 = promotion
index (header counter at promotion time), field28 = answer; type-1
DEP edges to the licensing facts. The graph itself is walkable via
the existing `t2_sig` skeleton (line 511), which records (tag,
literal) per cell up to 32 cells.

## 1. What information is available at composition time?

At the moment a composition candidate would be proposed, the
following are readable from learner state without any new machinery:

- **Per-MAP identity fields:** (s, r) the graph was promoted for,
  promotion index (a recency ordering), the answer it produced.
- **Per-MAP structural signature:** cell count and op mix via a
  `t2_sig`-style walk; literal values embedded in SETREG cells;
  graph depth (chain length) from the walk.
- **Per-MAP provenance:** DEP edges to the facts that licensed
  promotion. Two MAPs licensed by overlapping facts are more likely
  to compose usefully than two licensed by disjoint facts; this is
  the only currently available relatedness signal between graphs.
- **The current miss context:** the triggering (s, r), the gathered
  facts, and the direct-value inventory that `t2_gather` already
  collects. A MAP whose licensed (s, r) shares a subject or relation
  with the current miss is a more plausible composition operand.
- **Verification history:** trial statistics are packed into header
  field 16 (line 670) but no production code reads them. If read,
  they would say which families verified recently; they say nothing
  per-MAP today.

What is **not** available and would have to be created:

- **Reuse history.** The interaction analyst (commit `9009ff259`)
  found that promoted graphs are never executed at query time:
  answers come from memoized facts taught by `promote_graph` itself
  (`ev_teach_in` at line 543). No MAP has ever been *used* as a
  component, so no usage record exists. A selection policy needs a
  signal that distinguishes useful operands from dead ones, and the
  current architecture generates no such signal.
- **Composition outcome records.** Even the trial loop's own
  per-candidate outcomes evaporate: `t2_trial` returns a root or -2,
  and the rejected candidates are never recorded (the inquiry
  generalization analyst flagged the same loss pattern for trial
  candidates before `miss_inquire`). A policy that learns from
  failed compositions needs the failures persisted, not just the
  promotion.

Honest summary: identity, structure, provenance, and miss context
are available now. The two signals a learner-authored policy most
needs (which operands get reused successfully, which compositions
failed and why) do not exist because the architecture has no reuse
path and no failure memory. Designing the selector without
designing those two is theater.

## 2. What a learner-authored selection policy would look like

Not a fixed order. The comparator explicitly warns that a
researcher-fixed policy ("try each promoted MAP once,
head-position, after chains fail") is just a larger menu over a
history-dependent pool. A learner-authored policy must satisfy two
properties:

**(a) Its ranking is a function of learner state that experience
rewrites.** Concretely: each MAP gets a score node (or score fields
on the MAP itself, e.g. the currently unused field12/field16) that
production code updates on observed outcomes. The composition
proposal loop reads scores and tries operands in score order. The
scores start from a neutral prior (e.g. recency, or provenance
overlap with the current miss) and move with experience. The
researcher authors the *update rule's form* (increment on success,
decrement on failure); the learner authors the *resulting ranking*,
which differs across histories.

**(b) The policy generalizes across misses, not just within one.**
A policy that re-ranks MAPs only for the current (s, r) is a
per-query heuristic. A policy worthy of the name maintains operand
scores that persist across misses, so that a MAP that composed
successfully for one relation is tried earlier for the next. This
is the difference between a selection *heuristic* and selection
*knowledge*. The MAP's own persistence (they are never evicted in
the frozen source) makes this representable; nothing currently
writes the scores.

What it is not: it is not a neural ranker, a bandit library import,
or a researcher-tuned weight vector. The minimal honest form is a
per-MAP scalar score in learner state, updated by a fixed small
rule on two observable events (composition verified, composition
rejected), with ties broken by provenance overlap with the current
miss. Everything the learner "knows" about operand quality lives
in those scalars.

## 3. The feedback signal: what tells the learner a composition was useful?

This is the hard question, and the design must not dodge it.

**Today, nothing can.** Under the frozen architecture the signal
does not exist, for two compounding reasons already established by
other lanes:

1. Verification is oracle-gated. `t2_try_verify` accepts a candidate
   iff its output equals the environment-supplied `expected`. A
   composed graph that verifies gets the same reward as a flat graph
   that verifies: promotion. The learner cannot distinguish "this
   composition was useful" from "this flat graph happened to match."
   The oracle tells it the answer, not the value of the method.
   (This is H2's territory: the environment supplies the answer.)
2. There is no reuse path. Even a genuinely good composition is
   promoted, memoized via `ev_teach_in`, and never executed again.
   The interaction analyst's structural C0-D finding means the
   architecture cannot *observe* reuse value because reuse never
   happens.

**The minimal signal that would work** requires both gaps closed:

- (i) A reuse path: on later queries, the system must sometimes
  execute a promoted graph instead of answering from the memoized
  fact, so that operand quality becomes observable. The interaction
  analyst's H2 (reuse-path-first) is the prerequisite.
- (ii) A per-composition outcome record: when a composed candidate
  verifies, credit is assigned to its operands (increment their
  scores); when it is rejected after genuine execution, debit them.
  The existing genuine-rejection counting (header field 16) is the
  instrumentation point, but it must be made per-MAP and
  production-readable.

Until (i) and (ii) exist, any "target-selection policy" operates on
no signal and its scores are decorative. This is the design's
central dependency: **target selection is downstream of the reuse
path.** Building the selector first, without the reuse path, would
be the exact treadmill the program forbids: a new mechanism whose
inputs are researcher constants and whose outputs change nothing.

A weaker but honest interim signal, if the reuse path is deemed too
large for one generation: composition *verification rate* per
operand. Even without reuse, the trial loop can record, per MAP,
how often compositions using it as an operand verify versus get
rejected. This measures "composability," not "usefulness," and the
limitation must be stated: a MAP can be highly composable under the
oracle and still never reused. But it is a learner-observable
signal that exists entirely within the trial loop, needs no query
path change, and would already discriminate operand quality better
than a fixed order.

## 4. Minimal policy representation

The smallest representation that satisfies section 2's two
properties:

- **One score scalar per MAP**, stored in a learner-state field
  (MAP field12 and field16 are written as -1 at promotion and never
  read; field12 is the natural score slot, field16 a use-count).
- **One update rule**, fixed in form, learner-fed in content:
  on verified composition with operand set O, for each m in O:
  score(m) += 1; on genuine rejection, score(m) -= 1 (floored at a
  minimum so no operand is permanently banished; banishment would
  be a researcher-chosen absorbing state).
- **One tie-breaker**, computed from available state, not stored:
  provenance overlap between the operand's DEP facts and the
  current miss's gathered facts (count of shared fact nodes).
- **One proposal order**: operands sorted by (score desc, overlap
  desc, promotion index desc as final recency tie-break).

That is the whole policy: N scalars, one rule, one tie-breaker.
It is deliberately not a graph, not a predicate inventory, not a
ranking model. A scalar per operand is the minimal structure whose
values the learner (not the source) determines. Anything smaller
(a single global order) is researcher-fixed; anything larger
should justify its complexity against this baseline.

Deliberately excluded from the minimal form: operand *pair*
scores (combinatorial state the learner has no signal to fill),
negative-transfer guards (no evidence of interference yet;
the transfer lane may supply it), and decay (recency is already
the final tie-break; time-based decay adds a researcher-chosen
timescale with no grounding).

## 5. Relation to H3-lite

Target selection is a **fourth H3-lite site**, alongside the three
the feasibility probe named (trial search order, guide template,
repair dispatcher). The pattern is identical: a researcher-chosen
decision point becomes a read from a learner-state policy node with
a production update path from experience. No ISA change, no new
graph type, no new mode.

There is one asymmetry worth stating plainly. The other three
H3-lite sites *parameterize an existing researcher default*: there
is a literal loop order to replace with a policy-ordered dispatch,
literal guide constants to replace with a template node, a
straight-line repair to replace with a policy dispatch. Target
selection has **no existing default to parameterize**; the decision
is absent, not hardcoded. H3-lite for target selection therefore
*creates* a decision point rather than *moving* one. That makes it
the most architecturally honest of the four (nothing is being
relabeled) and also the one most exposed to the "new subsystem"
objection under the One-System Rule. The defense: it is not a new
mechanism but a policy node read by the existing trial loop, the
same structural move as the other three sites, and it shrinks
rather than grows the researcher-authored proposal code path (the
fixed family order becomes one policy among candidates).

Ordering with the other three: the H3 probe recommended H3's check
first, then H2's probes, then H1's widening. Target selection sits
*between* H3-lite and H1: it needs H3-lite's policy-node pattern
(decisions in learner state) and it needs the reuse path (section
3's dependency) before its signal exists. A sensible build order is:
reuse path first (else no signal), then the score scalars with the
interim composability signal, then promotion of the interim signal
to a reuse-based signal once the query path executes graphs.

## 6. Draft prereg kill bar for target selection

Draft language, intended as a starting point for the kill-bar
drafter, not a frozen bar:

> **K-TSEL-1 (learner-chosen composition targets).** In a sealed
> world, after the learner has promoted at least two MAPs A and B
> such that both are syntactically composable with the current
> miss's chain candidates, but only compositions using A verify
> (compositions using B are genuinely rejected by execution, not by
> budget exhaustion), the learner must attempt an A-composition
> before any B-composition on a subsequent miss with the same
> structure. **Discrimination condition:** the same frozen binary,
> run on a control history in which B composed successfully and A
> did not, must attempt B before A. A fixed proposal order fails
> this bar by construction, because its attempt order is identical
> across histories. The bar is satisfied only if the attempt order
> is a function of learner-state scores that differ between the two
> histories, with the score fields, their update events, and the
> two histories' score values all shown in the white-box trace.
>
> **K-TSEL-2 (no oracle shortcut).** The score updates in K-TSEL-1
> must be computed from the learner's own verification outcomes
> (verified vs genuinely rejected after execution), not from any
> field of the environment-supplied `expected` and not from
> researcher-authored per-world operand lists. The prereg must name
> the exact fields the update rule reads; reading any other field
> is a bar violation.

Why two bars: K-TSEL-1 proves the learner (not the source) chose
the targets, via the history-discrimination test. K-TSEL-2 proves
the choice was earned from the learner's own experience rather
than from the oracle, closing the H2-flavored shortcut where scores
parrot environment answers. Together they are the target-selection
analogue of the synthesis's recommended prereg checklist item:
"list every structural decision the learner can make that the
source cannot."

Explicit non-requirement: the bars do not require the composed
graph to be *reused* later (that is C0-D's job and needs the reuse
path); they require only that the *selection among operands* be
learner-determined and experience-derived. Selection and reuse are
separate claims and should be barred separately.

---

## 7. What this design does not do (stated so it is not oversold)

- It does not implement anything. There is no code, no binary, no
  measurement in this document.
- It does not fix the oracle problem (H2). The interim
  composability signal still rewards matching `expected`; only the
  reuse path plus reuse-based scoring escapes the oracle.
- It does not widen the composition operators (H1). The operators
  (splice, chain, substitute) remain researcher-authored under this
  design; only the operand *selection* moves into learner state.
  The "larger finite menu" objection survives at the operator
  level, exactly as the MUL comparator stated.
- It does not make procedures learner-built (full H3). The update
  rule's form is researcher-authored; the learner authors the
  scores. This is H3-lite, one rung below full H3, by design.
- It does not claim L3. At best, a future implementation passing
  K-TSEL-1/K-TSEL-2 would demonstrate learner-authored selection
  among researcher-authored operators over learner-authored
  operands: partial C0-A, partial C0-B, no C0-C until sealed
  post-freeze worlds require novel selections, no C0-D until the
  reuse path exists.

*End of design. No source modified. No worlds designed. No scores
claimed. Paper untouched.*
