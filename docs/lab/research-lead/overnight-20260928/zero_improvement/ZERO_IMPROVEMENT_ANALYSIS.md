# Zero-Improvement Analysis: Why TNN-2 Moved No Worlds

**Status: ANALYSIS - ASSUMES AUDIT-CORRECTED 4/9 FOR PREPARATION**

**Date:** 2026-10-01
**Worker:** Zero-Improvement Analyzer
**Basis:** Re-clustering draft `ed2357141`; red-team reports `340e94e3e`,
`4e329c772`, `687ba0219`; synthesis `42b4dfa91`; prereg audit `8959a7c14`.

**Do not quote a freeze score from this document as final.** The evaluator's
reconciled committed report is authoritative. This analysis assumes the
audit's corrected reading (TNN-2 passes exactly FW1, FW2, FW4, FW5; fails
exactly FW3, FW6, FW7, FW8, FW9; zero regressions, zero fixes) for the
purpose of examining what zero world-level movement implies. If the
reconciled score differs, sections 2 and 4 require revision.

---

## 1. Why did nothing move? (per change, from the red-team reports)

### Change 1: Runtime construction (targeted FW3, FW8, FW9, half of FW7)

**What was built:** `t2_trial`, a miss-policy trial loop proposing
candidates from three researcher-written linear graph assemblers
(chain, count, sum), in fixed order, with fixed bounds, verified
against an environment-supplied `expected` answer.

**Why it moved nothing:**

- **FW3 (arithmetic/composition, 0/10):** Requires the learner to
  construct multiplication from the ISA basis. The construction red
  team found the candidate grammar contains exactly three linear
  families with no branching beyond fixed guard->set pairs, no
  nesting, no loops except unrolled INC runs, no subroutine calls,
  and DEC never emitted. There is no composition operator whose
  operand is a previously promoted graph. Multiplication is not a
  linear chain of guards and sets; it requires either iterative
  accumulation (a loop, unrepresentable) or hierarchical composition
  (CALL/inlining, absent). The template menu contains no path from
  its members to multiplication. The trial loop searches the menu
  for a member matching the given answer; when no member can express
  multiplication, the search correctly returns nothing. The failure
  is unrepresentability, not failed discovery.

- **FW8 (novel utterance, 0/5 novel with 4/4 retention):** Requires
  generating novel compositional forms. The assemblers produce only
  chains, counts, and (dead) sums over observed relations. "Novel"
  in FW8 means a surface form not seen in training; the menu can
  only emit wirings of observed literals into fixed topologies. When
  the required novel form falls outside the three linear families,
  no candidate verifies. Retention (4/4) works because it is
  retrieval, not construction.

- **FW9 (relational DAG, low multi-hop scores):** Requires multi-hop
  relational traversal. Chains are bounded at depth 4 by a researcher
  literal (`t2_gather` depth 1..4, 96-path cap). The boundary probe
  confirmed behaviorally: a 5-hop chain is refused with -2, correctly,
  because it is unrepresentable. FW9's DAG queries exceed the depth
  bound or require branching the linear families cannot express.

- **FW7 (planning, 0/4):** Requires actions composing toward a
  target. The construction families build relational graphs, not
  action sequences. Nothing in `t2_trial` proposes action
  compositions; the planning half of FW7 was targeted by Change 1
  only insofar as "construction" was assumed to generalize to
  action construction. It does not: the assemblers are
  relation-specific in their gathering (`t2_gather` over facts),
  and there is no action-composition assembler.

**Common mechanism of failure:** In every case, the required
structure lies outside the researcher-enumerated family, and the
learner has no means to extend the family. The trial loop is a
lookup loop over a fixed set; lookup cannot return what is not in
the set.

### Change 2: Miss-to-act inquiry (targeted FW6, half of FW7)

**What was built:** `miss_inquire`, creating a T_UNCERT node with
miss-specific (s, r) content, a guide node, and POLICY_ROOT linkage;
`ev_act` selecting among guides by context match and bid.

**Why it moved nothing:**

- **FW6 (active inquiry):** Requires the inquiry action to be
  contingent on epistemic state: different acts before vs. after
  diagnostics, varying with what is unknown. The inquiry red team
  found the guide's action value (slot 20 = 30) and content
  (slot 24 = -999) are researcher-authored constants at
  `miss_inquire` lines 805-808. `ev_act` returns slot 20, so the
  "action" is the constant 30 regardless of what is unknown.
  TNN-1 failed FW6 with constant CHOICE 0; TNN-2 fails with
  constant CHOICE 30. A different constant is not contingency.
  FW6's contract requires the literal CHOICE 0 in a specific
  phase-gated context; more fundamentally, it requires the act
  to vary with the learner's uncertainty. No varying occurs.

- **FW7 (planning, action half):** Requires goal-directed action
  sequences. A constant inquiry action cannot compose into
  sequences, and `ev_act` is only invoked by the driver/tests,
  never by cognition on the planning path. The inquiry "loop"
  terminates at the constant: miss -> flag -> 30 -> end. There is
  no path from the guide to a subsequent differentiated act.

**Common mechanism of failure:** The inquiry mechanism detects
(something missed) but does not inquire (no discriminating
question, no information-seeking act whose content varies with
the unknown, no use of any answer). FW6 and the action half of
FW7 require the act to be a function of learner state; the act
is a constant, so it is a function of nothing.

### Change 3: Generic revision (targeted the revision ceiling; prereg said it "may not move FW scores directly")

**What was built:** `t2_revise_graph`, a single-schema repair:
find the BRANCHEQ-guarded SETREG via provenance, tombstone it,
insert a literal SETREG holding the observed value, rewire.

**Why it moved nothing (and why this is not a falsification of
its limited claim):** The prereg explicitly stated Change 3 "may
not move FW scores directly but future-proofs Change 1." The
revision red team found the operator handles exactly one repair
topology (literal patch under an existing guard). It cannot
retarget guards, insert branches, reroute to existing steps, or
handle multi-step repairs. None of the five FW failure clusters
is a literal-patch problem: FW3 needs new operations, FW6 needs
contingent acts, FW7 needs action composition, FW8 needs novel
forms, FW9 needs deeper traversal. A literal patch cannot supply
any of these. The prereg's limited claim ("may not move scores")
is therefore confirmed, not falsified. Change 3 is included in
this analysis because its ceiling matters for the interaction:
construction emits template instances, revision patches
literals, and neither can change the other's grammar.

---

## 2. Is zero improvement worse than partial?

**Yes. Zero movement with zero regressions is stronger evidence
than partial movement would have been, and it points to a
different causal level.**

Consider the counterfactual: suppose TNN-2 had flipped FW9 (say,
from 5/30 to 20/30) while leaving the rest. That would suggest
the construction change is on the right track but incomplete:
the grammar is close, the bounds need widening, the verifier
needs adjustment. The natural next step would be incremental:
more families, deeper bounds, better search order. This is the
treadmill Micah forbade.

What actually happened (per the audit-corrected draft): not one
of the five targeted clusters moved, and not one of the four
passing worlds regressed. The pass/fail pattern is byte-identical
at the world level. This is not "close but incomplete." It is
orthogonality: the three changes operate at a causal level that
does not intersect the bottlenecks at all.

The logic:

- If a change addresses the true bottleneck partially, some
  worlds near the boundary should move. FW9's TNN-1 scores
  (5/30, 9/30) show it is near a boundary; a construction change
  that genuinely widened expressiveness should have moved it at
  least partially.
- If a change addresses a different problem than the bottleneck,
  nothing moves, because the bottleneck is untouched. The
  byte-identical pattern is exactly what orthogonality predicts.
- Zero regressions strengthen the conclusion: the changes are
  not harmful, just inert with respect to the failure clusters.
  They do not interfere with what works (FW1/FW2/FW4/FW5 still
  pass); they simply do not touch what fails.

**The evidential upshot:** partial improvement would have
licensed incrementalism ("widen the menu"). Zero improvement
falsifies the level at which the diagnosis was pitched. The
prereg's causal account was "TNN-1 fails for lack of X; TNN-2
adds X." The result shows the Xs, as implemented, were not the
causes. The next diagnosis must be pitched one level deeper:
not "what capability is missing" but "what property must the
capability have."

---

## 3. What does this say about the "targeted repair" strategy?

TNN-2 was designed after TNN-1's failures were known. Its three
changes were targeted at specific gaps: no runtime construction,
no inquiry loop, no generic revision. The targeting was at the
level of named capabilities. None of the targets moved.

**The implication is that the gap analysis was pitched at the
wrong level.** It identified missing capabilities correctly
(TNN-1 indeed had no construction, no inquiry, no revision) but
misidentified the missing property. The property FW3/FW6/FW7/FW8/
FW9 require is not "construction" in the abstract but
learner-originated structural form: the ability to produce a
topology the researcher did not enumerate. TNN-2 added
"construction" in the sense of runtime template instantiation,
which is a capability with the wrong property: the forms remain
researcher-enumerated.

This yields a general lesson for TNN-3, stated as a constraint
on future targeted repair:

1. **Target the property, not the capability name.** A prereg
   that says "add construction to fix FW3" is underdetermined:
   template instantiation is a kind of construction and it does
   not fix FW3. The prereg must say "add learner-originated
   topology construction," with a kill bar that fails a
   template menu deterministically.

2. **The kill bars must test form-origination, not just
   capability presence.** The TNN-2 kill bars (K-T2-3: structures
   constructed at runtime through the trial loop; K-T2-4:
   uncertainty node created; K-T2-5: non-constant act choice)
   were all satisfiable by slot-filling. The synthesis
   (section 7) notes that a checklist item of the form "list
   every structural decision the learner can make that the
   source cannot" would have caught all three. That item did
   not exist at TNN-2 preregistration time.

3. **Seeing the failures in advance does not help if the
   diagnosis is at the wrong level.** TNN-2 had the advantage
   of knowing exactly which worlds TNN-1 failed. It still moved
   none, because "design a fix for FW3" without "the fix must
   let the learner originate form" produces a template menu
   that covers the designer's imagination of FW3 but not FW3
   itself. The sealed worlds punish imagination; only the
   property generalizes.

**For TNN-3:** the five symptom clusters should be retained as
benchmarks, but every change prereg must name the property it
adds (not just the capability) and include a bar that a
researcher-enumerated schema fails deterministically. The
kill-bar draft (`76231baa8`) and its review (`eb354e3a2`)
already move in this direction; this analysis confirms the
direction is necessary, not optional.

---

## 4. Did anyone anticipate this failure mode?

### The prereg (freeze prereg `ce1a7c5f8`): anticipated falsification in general, not the specific mode.

The prereg contained an explicit falsification clause (quoted in
the re-clustering draft, section 4): a FW score at or below 4/9
"would falsify the root-cause analysis and require
re-clustering." This is good governance: the prereg did not
assume success, and it specified what failure would mean. The
current re-clustering exercise is the prereg working as designed.

What the prereg did NOT contain was any anticipation of the
specific failure mode. There was no checklist item, kill bar, or
falsifier of the form "the learner must originate structural
form" or "enumerate every structural decision the learner can
make that the source cannot." The TNN-2 build prereg's kill bars
(K-T2-3 through K-T2-5, per the synthesis section 1) tested that
runtime filling, persistence, and selection machinery work.
They do work. The bars were satisfied in letter while the
generality failed, because the bars did not probe who chose the
schema. The failure mode was therefore unanticipated at
preregistration time, though the possibility of failure in
general was provided for.

### The red teams: discovered the mode, did not predict it in advance.

The three red teams were chartered to attack the mechanisms as
built. They found the shared enumerated-schema/filled-slot
pattern empirically, by source audit and boundary probing. The
construction red team demonstrated 5-hop unrepresentability
behaviorally; the inquiry red team traced the constant guide to
source lines 805-808; the revision red team enumerated the
single repair topology exhaustively. None of these was predicted
before the attack; each was a finding. The synthesis then named
the shared pattern. So the failure mode was discovered, not
forecast.

### The synthesis (after red teams, before freeze completion): predicted the interpretation, not the zero.

The synthesis (section 4) was written after the red teams but
before the freeze evaluator finished. It predicted that any
freeze score, including a high one, would not establish
generality or L3: "capability improved within the
researcher-enumerated envelope; the envelope is unchanged in
kind." It framed FW1-FW9 as a regression/targeted-repair battery
for TNN-2 per Micah's ruling. What it did not predict was the
actual zero: it allowed that TNN-2 might score above 4/9 on
capability ("that is a legitimate capability result... the
three new mechanisms fixed the capability gaps they were
designed to fix"). The audit-corrected 4/9 shows they did not
fix even the capability gaps. The synthesis anticipated the
interpretation correctly but was more generous than the result
about capability movement.

### Summary

| Party | Anticipated falsification? | Anticipated the specific mode? |
|---|---|---|
| Freeze prereg | Yes (explicit clause) | No (no form-origination bar) |
| Red teams | N/A (chartered to find it) | Discovered, not predicted |
| Synthesis | Yes (score does not imply generality) | Partially (named the pattern, did not predict zero movement) |

The honest record: the governance worked (falsification was
provided for and re-clustering is happening), but the specific
failure mode was a genuine discovery, not a confirmed
prediction. This is how the process is supposed to work.

---

## 5. What property must a mechanism have to move a cluster?

This section does not propose TNN-3 designs. It states, per
cluster, the property a mechanism must possess for the cluster
to be movable at all. Each property is phrased as a necessary
condition derived from why the current mechanism fails.

### FW3 (arithmetic/composition)

**Required property:** the constructible space must not be
enumerable from source alone. Concretely: there must exist
constructible graphs whose topology cannot be derived from the
source without also supplying the learner's history. The MUL
comparison (`e2e34a4ac`) states the positive form: with
recursive composition, "the set of buildable graphs grows with
the learner's experience: each promoted graph becomes a
potential operand." Multiplication specifically requires either
an iterative accumulation structure (loop) or hierarchical
composition (a MUL graph that invokes an ADD graph). A finite
menu of linear families has neither. The property is
history-parameterized generativity: source + history is
required to enumerate the space; source alone is insufficient.

### FW6 (active inquiry)

**Required property:** the inquiry act must be a non-constant
function of learner epistemic state, and there must exist a
resolution transition. Concretely: there must be at least two
uncertainty states u1 != u2 such that the mechanism emits
act(u1) != act(u2), where the difference is derived from what
would discriminate between the learner's live hypotheses, and
there must be a production path that retires or revises the
uncertainty when evidence arrives. The current mechanism has
act(u) = 30 for all u and no resolution path. The property is
state-contingent discrimination with closure: the question
varies with the unknown, and the unknown can be closed.

### FW7 (planning)

**Required property:** action structures must compose toward a
represented target, with the composition chosen at runtime.
Concretely: given a goal state, the mechanism must produce a
sequence (or conditional structure) of acts whose selection
depends on the goal and on intermediate outcomes, where the
space of sequences is not a fixed menu. The current mechanisms
have no action-composition assembler (construction builds
relational graphs) and a constant inquiry act. The property is
goal-conditioned composition: the plan is a function of the
goal, not a constant or a menu selection.

### FW8 (novel utterance)

**Required property:** the mechanism must emit surface forms
whose compositional structure was not enumerated in source.
Concretely: there must exist a generable utterance whose parse
or construction tree contains a combination of parts that no
source-written assembler produces. The current assemblers emit
only chains, counts, and dead sums of observed literals; any
"novel" form they emit is a novel filling of a fixed topology,
which FW8's novelty criterion (0/5 on genuinely novel forms)
does not credit. The property is combinatorial novelty: new
arrangements, not new fillings.

### FW9 (relational DAG)

**Required property:** traversal depth and branching must not
be bounded by researcher literals. Concretely: for any bound B
written in source, there must exist a legitimate query whose
answer requires exceeding B, and the mechanism must be able to
exceed it using learner-managed resources (a budget, a
termination condition derived from the query, or unbounded
recursion with cycle detection). The current chain depth is
capped at 4 by literal; the boundary probe confirmed 5-hop is
unrepresentable rather than undiscovered. The property is
learner-scaled search: the bound, if any, comes from the
learner's resources, not the researcher's constants.

### The common property

All five reduce to one: **the mechanism's output space must not
be enumerable from the source alone.** In each case the current
mechanism's outputs form a finite (or finitely-parameterized)
set fixed before experience, and the failing worlds require an
output outside that set. The learner must be able to extend the
set through experience: new topologies, new acts, new plans,
new arrangements, new depths. "Extend the set" is the property;
any TNN-3 proposal must say how its mechanisms extend rather
than fill.

A useful test formulation, adapted from the synthesis section 7:
for each mechanism, the preregistration must list every
structural decision the learner can make that the source
cannot. If the list is empty, the mechanism cannot move any
cluster, regardless of its capability score on previously seen
worlds.

---

## Caveats

1. This analysis assumes the audit-corrected 4/9 reading of an
   untracked evaluator draft. It is preparation, not a verdict.
   If the reconciled committed report differs, sections 2 and 4
   (which depend on the exact zero-movement pattern) must be
   revised; sections 1, 3, and 5 (which depend on the red-team
   findings about mechanism properties) stand regardless of the
   score, because the red teams attacked the mechanisms as
   built, not as scored.

2. "Zero improvement" refers to world-level pass/fail movement.
   The draft notes a marginal FW1 improvement (12/12 vs 10/12).
   Margin changes within a passing world do not affect the
   cluster analysis, which is about which capabilities are
   present at all.

3. The W (supplementary) battery is not addressed here; it
   awaits the reconciled report. TNN-1 had W 4/9 with the same
   world set passing. If TNN-2's W pattern differs, that would
   be a separate finding.

---

**End of analysis.**
