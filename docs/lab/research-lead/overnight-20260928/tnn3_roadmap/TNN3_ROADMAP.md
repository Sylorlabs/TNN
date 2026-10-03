# TNN-3 Roadmap Synthesis

Date: 2026-10-01. Synthesizer session: 6f5946f9-86a8-4075-bf9e-1a6fc9a99ea0.

## NO IMPLEMENTATION

This document is synthesis, not code. Nothing here has been implemented,
tested, or measured. It does not authorize implementation. Any TNN-3 work
building on this roadmap must go through its own preregistration with frozen
kill bars. The roadmap's job is to synthesize the eight input analyses into
a coherent direction, so a future preregistration can adopt or reject it on
concrete grounds.

Target of all input analyses: `tnn2.zag` at `f4de7ff46` (frozen), read-only.

---

## 0. What the eight inputs collectively establish

The eight analyses converge on a single architectural diagnosis with three
facets:

**The shared cause (synthesis `42b4dfa91`):** "enumerated-schema /
filled-slot." In construction, inquiry, and revision, the researcher
authored the schema (the space of possible structures and the procedure
that fills it) and the learner fills runtime-chosen slots (literals, cell
indices, miss content). The learner chose the operands, never the topology.
TNN-2 moved the content of cognition into learner state but left the form
in source code. TNN-1 was fixed templates with fixed content; TNN-2 is fixed
templates with variable content. Real advance, exactly one rung short of L3.

**The three hypotheses (synthesis section 5):**
- H1 (grammar): each mechanism's output space is enumerated in source.
  Fix with open compositional constructor.
- H2 (oracle): the environment supplies the answer via verification
  against expected/observed values. Fix with learner-internal
  prediction-based acceptance.
- H3 (procedure ownership): the mechanisms' operating procedures are
  source code, not learner state. Fix with procedures as learner-built
  graphs.

**The interaction finding (`9009ff259`):** no closed feedback loops exist.
Inquiry is a dead-end pipeline terminating at the driver. Promoted graphs
are never executed at query time (answers come from memoized facts), so
C0-D fails structurally. "The system has no unsupervised learning loop at
all." The bottleneck is construction's propose/verify pair, with
expected-gating as the tighter constraint.

**The H3 confirmation (`94cecdba4`):** the cheap policy-revisability check
was executed against the frozen source. No production path can modify the
trial search order, the guide schema, or the repair topology from
experience. H3 confirmed as structural fact. The 4-op ISA cannot express
structural revision procedures (effect-domain gap); closing it is a
protected-core boundary decision banked for Micah.

**The available designs:** H3-lite (`22197da2c`) parameterizes the three
mechanisms' decision points as learner-state policy nodes with no ISA
change. The revision generalization (`edbb0e9b5`) specifies a
repair-proposal generator within the frozen ISA. The inquiry generalization
(`dedfad368`) specifies derived questions and resolution via existing
type-3 supersession. The MUL comparison (`e2e34a4ac`) identifies
target-selection among accumulated MAPs as the underexploited site of
learner authority. The kill-bar draft (`76231baa8`) provides K-T3-ADV,
K-T3-TOPO, K-T3-CON-1/2, K-T3-INQ-1/2/3/4, K-T3-REV-1/2/3, all
DRAFT-NOT-FROZEN.

---

## 1. The minimal TNN-3 that addresses the red-team findings

The minimal TNN-3 is not a full L3 architecture. It is the smallest change
that retires the three ATTACK-SUCCESS verdicts' specific findings while
staying within the frozen ISA and adding no new modes, bridges, or handlers.

**Three components, each from an existing analysis:**

**(a) H3-lite policy nodes (`22197da2c`).** Three learner-state policy
nodes (tag 40, subtypes 1/2/3) for trial search order, guide template, and
repair dispatcher. Each with copy-then-revise initialization, a production
read path replacing a source literal, and a production write path from an
existing experience event. This addresses the H3 finding (policies
structurally unrevisable) at the decision level, not the procedure level.

**(b) Repair-proposal generator (`edbb0e9b5` section 4a).** Wire
`t2_trial`'s execution and verification halves into the revision path,
plus a new repair-proposal generator (blame localization over all step
types via extended provenance, edit enumeration over the five repair
topologies, verification against triggering observation plus retained
licensing facts). This addresses the revision red team's single-schema
finding by converting literal-patch into search over a multi-member repair
family.

**(c) Inquiry resolution and candidate persistence (`dedfad368` sections
1-2).** Persist trial candidates as hypothesis structures linked to the
uncertainty node (instead of discarding them). Derive one guide per
discriminating sub-query with informativeness scoring. Add the
`resolve_uncertainty` transition via existing type-3 supersession,
called from `ev_observe`. This addresses the inquiry red team's L3
hardcoded finding (guides become revisable and differentiated) and the L6
absent finding (resolution path exists).

**What this minimal TNN-3 does NOT deliver (explicit non-overselling):**
- Procedures remain researcher-authored Zag code. C0-A still fails at the
  procedure level. Full H3 requires the protected-core structural-ops
  decision.
- The repair family remains researcher-enumerated. H1 is unaddressed at
  the operator level; the learner selects among given topologies but
  cannot invent a sixth.
- The acceptance oracle remains. H2 is unaddressed; verification still
  uses environment-supplied expected/observed values.
- The guide remains non-discriminating in the full sense. H3-lite makes
  guide content revisable; the informativeness criterion is
  researcher-authored.
- No capability improvement is predicted on FW1-FW9. The minimal TNN-3
  changes the locus of control, not scores.

**Why this is the right minimal scope:** each component directly retires
a named red-team finding (unrevisable policies, single-schema repair,
constant guides with no resolution) without requiring the governance
decisions (protected-core ops) or the expensive machinery (open
constructor) that the full hypotheses need. It is the cheapest experiment
that tests whether the shared architectural cause can be addressed
incrementally.

---

## 2. How H1, H2, and H3 relate

The synthesis (`42b4dfa91` section 5) defines three hypotheses at different
architectural levels. They are not three patches; they are competing
explanations to discriminate experimentally.

**H1 (enumerated output space) and H2 (oracle verification)** are about
what the mechanisms can emit and accept. They are experimentally separable:
- H1 discrimination: freeze the constructor change alone (open
  compositional proposals, everything else identical) and re-run the three
  red-team probe suites. H1 predicts all three move together.
- H2 discrimination: keep the finite grammar fixed and change only
  verification to masked queries (expected withheld) plus revision probes
  where corrected content must be derived. H2 predicts current mechanisms
  fail these while passing unmasked ones.
- Both can be true. The discrimination experiments determine which binds
  first.

**H3 (procedure ownership)** is about where the mechanisms themselves live.
It contains H1 as a special case in one sense (an enumerated grammar is a
procedure living in source), but it makes a distinct, stronger prediction:
that no experience can revise the mechanisms' policies. That prediction was
tested by the cheap check (`94cecdba4` section 5b) and confirmed. H3 is now
a structural fact, not just a hypothesis.

**Can they be addressed independently?** In experiments, yes. In
architecture, H3 conditions the other two:
- If no production path can revise mechanism policies (H3 confirmed),
  then H1's widened constructor would still be driven by an unrevisable
  search policy, and H2's learner-internal acceptance would still be
  computed by an unrevisable verifier.
- The H3 result tells you whether the mechanisms are even capable of
  self-modification before you invest in widening what they can emit (H1)
  or accept (H2).

**Note on the interaction analyst's H1/H2/H3:** the interaction analysis
(`9009ff259` section 6) uses the same labels for different hypotheses:
their H1 is verification-first (maps to synthesis H2), their H3 is
grammar-first (maps to synthesis H1), and their H2 is reuse-path-first
(the C0-D structural failure: promoted graphs never executed). These are
compatible, not conflicting. The interaction H2 (reuse path) is orthogonal
to the synthesis hypotheses and is required for any of them to matter for
C0-D.

---

## 3. Where H3-lite fits: stepping stone, not dead end

H3-lite (`22197da2c`) is a stepping stone with clearly marked limits.

**Why it is a stepping stone:**
- It delivers H3's testable prediction (procedures revisable by
  experience) without H3's governance cost (no protected-core change).
- It tests whether moving decisions into learner state is sufficient for
  policy revision, before paying for moving procedures there.
- The K-H3 prereg kill bar it drafts provides the exact acceptance test
  for the stepping stone: list every structural decision, its
  learner-state location, its production write path, its triggering
  event, and a sealed test showing variation across experience histories.
- If H3-lite succeeds (policies demonstrably revise from experience), it
  validates the H3 direction and motivates the full H3 investment. If it
  fails (policies parameterized but never meaningfully revised), it shows
  the problem is deeper than decision placement.

**Why it is not a dead end:**
- The policy-node infrastructure (tag 40, copy-then-revise bootstrap,
  production write paths) is reusable by full H3. When procedures become
  learner-built graphs, the policies they implement can start as H3-lite
  nodes.
- The discrimination tests H3-lite enables (sealed worlds where fixed
  order systematically fails) are the same tests full H3 would need.

**The limits, stated plainly (from `22197da2c` section 7):**
- Procedures remain researcher code. C0-A still fails at procedure level.
- Repair family stays researcher-enumerated. H1 unaddressed.
- Acceptance oracle remains. H2 unaddressed.
- All heuristics (thresholds, margins) are researcher-chosen.

**The risk to watch:** H3-lite could become "revisability theater" if the
write paths exist but are never meaningfully exercised (thresholds never
trigger, updates trivial). The K-H3 bar's condition (d) guards against
this: the demonstration test must use ordinary world interactions, and the
decision change must be an outcome, not an input.

---

## 4. The role of the target-selection policy

The MUL comparison (`e2e34a4ac` section 4-5) identifies a decision point
that TNN-2 has no design for and MUL Rung B never had to solve.

**The gap:** MUL Rung B had exactly one PROC (ADD) when MUL was built, so
CALL target selection was trivial. TNN-2's `t2_trial` promotes many MAPs
(chains, counts, single-hops), so any composition mechanism needs a policy
for choosing which promoted graphs to compose. No such policy exists in
TNN-2. The comparator names it "the underexploited site of learner
authority."

**Relation to H1:** target selection is the decision point within H1's open
constructor. Even with recursive composition via inlining (the
freeze-compatible route the comparator specifies), the learner must choose
which operand graphs to splice. A researcher-fixed selection policy ("try
each promoted MAP once, head-position, after chains fail") is a larger menu
over a history-dependent pool. A learner-driven selection policy is the
further step.

**Relation to H3:** target selection is a prime candidate for H3-lite
parameterization. It is a structural decision (which operand graphs, in
what arrangement) with no current learner-state representation. The H3-lite
pattern applies directly: a policy node storing selection preferences,
updated from composition success/failure.

**Why it matters for the roadmap:** the minimal TNN-3 in section 1 does
not include composition, so it does not need target selection. But any
TNN-3 that pursues H1 (open constructor) must design target selection as a
general mechanism, not bolt it on per world. The comparator's warning
stands: "what part of the composition topology was actually chosen by the
learner?" For the inlining design, the honest answer is which operand
graphs and their arrangement within the researcher's operator set, but not
the operators. Moving the selection policy into learner state is the next
architectural step after the operators exist.

---

## 5. What a TNN-3 preregistration needs to contain

Based on the kill-bar draft (`76231baa8`) and the K-H3 bar (`22197da2c`
section 6), a TNN-3 preregistration must contain:

**A. Frozen bar text.** The exact statements of K-T3-ADV, K-T3-TOPO,
K-T3-CON-1/2, K-T3-INQ-1/2/3/4, K-T3-REV-1/2/3, and K-H3 (or explicit
amendments with rationale). The draft is DRAFT-NOT-FROZEN; Micah must
review the 6 open questions in section 11 of the draft before freezing.

**B. Structural signature function.** The deterministic function for
K-T3-TOPO, fixed in the prereg. The draft proposes canonical string over
cell tags, edge types, step counts, adjacency shape (no literals, no
addresses, no allocation order).

**C. Adversary protocol.** Per K-T3-ADV: independent adversary agents,
post-freeze authorship verified by `git merge-base --is-ancestor` (fail
closed BLOCKED), minimum world counts, pairwise-distinct signatures,
non-triviality rationale per world.

**D. Policy revisability listing (K-H3).** For every structural decision
the mechanism makes that is not determined by immediate input:
1. the decision (e.g., "trial search order", "guide default action",
   "repair topology selection", "composition target selection");
2. the learner-state node and fields storing it (tag, subtype, field
   numbers);
3. the production (non-test) code path that writes to those fields;
4. the experience event triggering the write;
5. a sealed test demonstrating the decision taking different values after
   different experience histories.

**E. Explicit non-claims.** What L2 the design achieves, what L3 it does
not, and which of H1/H2/H3 it addresses. The minimal TNN-3 in section 1
addresses H3 at the decision level only; the prereg must state that
plainly.

**F. Architecture accounting.** Per the standing rule: cognition source
lines added, new hardcoded semantic cases (must be zero), new modes
(must be zero), new bridges (must be zero), new task-specific handlers
(must be zero), learner-state structures created. The capability-source
delta should be stated.

---

## 6. The three biggest risks

**Risk 1: Prereg spec gap redux.** TNN-2 failed because K-T2-4/K-T2-5
tested chain structure, not question content; the builder satisfied the
letter (guides learner-constructed, 30 read from slot20, 30 not 0) while
the spirit (derived discriminating need) went unbuilt. The inquiry
generalization (`dedfad368` section 6) names this as the primary cause.
TNN-3 could repeat this if bars are not precise about derived content,
informativeness ordering, and resolution effects. Mitigation: the
kill-bar draft's insistence on observable derived content (K-T3-INQ-1:
guide fields must match checker-computed values), dominance tracking
(K-T3-INQ-3), and the K-H3 listing requirement (decisions must be
enumerated, not assumed).

**Risk 2: H3-lite as revisability theater.** Policies could be
parameterized as learner-state nodes with production write paths that are
never meaningfully exercised: thresholds set so high they never trigger,
updates so small they never change behavior, or sealed tests that
directly encode the expected decision. This would pass K-H3's letter
(write path exists) while failing its spirit (policies actually revise
from experience). The H3-lite design (`22197da2c` section 5) documents
all thresholds as researcher-chosen heuristics, which is honest but also
the attack surface. Mitigation: K-H3 condition (d) requires sealed tests
with ordinary world interactions where the decision change is an outcome.
Additionally, the prereg should require the discrimination tests from the
H3-lite design (sections 2g, 3g, 4h) as committed evaluation assets.

**Risk 3: Solving H1 before H2 (the treadmill).** Widening the constructor
(H1: open compositional proposals) before fixing the oracle (H2:
learner-internal acceptance) produces "a larger finite menu under the same
generous acceptance test." The synthesis (`42b4dfa91` section 5) names this
as the exact treadmill Micah forbade, and the recommended order is
explicit: H3 check, then H2 probes, then H1 widening. The interaction
analyst (`9009ff259` section 6) concurs: H1 (verification-first in their
terms) before H3 (grammar-first in their terms). A TNN-3 that implements
recursive composition while `t2_try_verify` still matches
environment-supplied expected values has built a more expensive
slot-filler, not a more general learner. Mitigation: the prereg must
either include masked verification probes or explicitly scope the design
as H3-lite-only (decisions revisable, grammar still fixed, oracle still
present) with H1/H2 as named future work.

---

## 7. Recommended order

Synthesizing the synthesis recommendation (`42b4dfa91` section 5),
the H3 probe's execution (`94cecdba4` section 5), and the interaction
analyst's bottleneck analysis (`9009ff259` section 6):

**Step 0 (done):** H3's cheap policy-revisability check. Executed against
the frozen source. Result: all three mechanisms structurally unrevisable.
H3 confirmed as architectural fact. This step is complete and need not be
repeated.

**Step 1: H2 probes (masked verification).** Keep the finite grammar fixed.
Change only verification: masked queries where `expected` is withheld,
plus revision probes where corrected content must be derived from retained
facts rather than copied from the observation. This tests whether the
oracle is the binding constraint. If current mechanisms fail masked probes
while passing unmasked ones, H2 binds and must be addressed before H1
widening. Cost: new sealed worlds, no new machinery.

**Step 2: H3-lite (policy parameterization).** Implement the three policy
nodes from `22197da2c` with the K-H3 bar frozen in preregistration. This
makes the mechanisms' decisions revisable by experience and provides the
discrimination tests (order-flip worlds, template-shift scenarios,
topology-preference shifts). Cost: moderate new machinery, no ISA change,
no governance decision. This is the minimal TNN-3 in section 1, minus the
repair-proposal generator and inquiry resolution which can follow.

**Step 3: Repair-proposal generator and inquiry resolution.** The
within-ISA changes from `edbb0e9b5` section 4a and `dedfad368` sections
1-2. These complete the minimal TNN-3. They depend on Step 2 only in the
sense that the revision dispatcher policy (H3-lite subtype 3) selects
among the repair topologies the generator enumerates; the generator can
be built and tested with a fixed order first.

**Step 4: H1 widening (open constructor), only after Step 1.** Recursive
composition via inlining (per `e2e34a4ac` section 4), plus the
target-selection policy (section 4 above) as a learner-state mechanism.
This step must not precede Step 1, per the treadmill warning. It also
requires the post-freeze adversarial battery (K-T3-ADV) to test whether
fixed composition operators suffice for genuinely new structures.

**Parallel track (not ordered after the above):** the reuse path
(interaction H2). Routing `ev_query` hits through MAP execution instead
of memoized facts is required for C0-D regardless of which synthesis
hypothesis binds. It is orthogonal to H1/H2/H3 and can proceed in
parallel, but no generality claim converts to capability without it.

**Explicitly not in the roadmap:** full H3 (procedures as learner-built
graphs) pending the protected-core structural-ops governance decision
banked for Micah. The H3-lite stepping stone (Step 2) is the recommended
way to gather evidence for that decision.

---

## 8. Banked items (no blocking)

1. Protected-core structural ops (ALLOC, field WRITE, edge LINK/KILL in
   the protected core): banked for Micah with the H3 probe's Q1 sketch
   (`94cecdba4` section 1c) as evidence. Full H3 needs this; H3-lite
   routes around it.
2. Informativeness criterion placement for inquiry: if TNN-3 adopts
   derived questions, where does "which question is worth asking" live?
   Source placement keeps inquiry at L2. Learner placement is the hard
   open problem. Banked from synthesis section 6.
3. The 6 open questions from the kill-bar draft (`76231baa8` section 11):
   world counts, builder signature-logging burden, per-world vs fixed
   signature function, K-T3-INQ-3 prescriptiveness, kill-bar vs falsifier
   promotion, C0-A regression bar strength. Awaiting Micah's review.
4. K-H3 draft status: DRAFT-NOT-FROZEN. Requires Micah's review before
   governing anything.
5. Target-selection policy design: named as required for H1 widening
   (section 4 above) but not yet designed. The MUL comparison specifies
   the problem; the design is future work.

---

## Verdict

TNN3-ROADMAP-SYNTHESIS-COMPLETE.

Eight input analyses synthesized into: the minimal TNN-3 (H3-lite plus
repair-proposal generator plus inquiry resolution), the H1/H2/H3
relationship (H3 conditions the others; H3 check done; H2 before H1),
H3-lite as stepping stone (with theater risk named), target-selection as
the underexploited learner-authority site, preregistration structure
(bars plus K-H3 listing plus accounting), three biggest risks (spec gap
redux, revisability theater, H1-before-H2 treadmill), and recommended
order (H2 probes, H3-lite, repair/inquiry completion, H1 widening after
H2, reuse path in parallel, full H3 pending governance).

*End of roadmap. No source modified. No scores claimed. Paper untouched.*
