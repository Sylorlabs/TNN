# Source-Underdetermined Form (SUF): the property TNN-3 must have

Status: PROPOSAL, not a frozen bar. Offered as vocabulary for future preregistrations. It governs nothing until incorporated into a preregistration Micah reviews and freezes.

## 1. Name

**Source-Underdetermined Form (SUF).**

One-line statement: a mechanism exhibits SUF when the structural form of its outputs cannot be enumerated from the source code alone; at least one structural decision in the production path is genuinely resolved by learner history, so the space of producible forms is underdetermined by the source.

## 2. Formal definition

Let S be the mechanism's source code (including all literals, constants, and fixed enumerations it contains). Let H range over possible learner histories (the full persistent learner state reachable through legitimate experience). Let Forms(S, H) be the set of structural schemas the mechanism can produce given source S and history H. A structural schema here means a topology, wiring, operator arrangement, ordering, or bound, considered distinct from another schema when they differ in structure rather than merely in filled parameter values (filling indices or literals into a fixed schema does not create a new schema).

SUF holds for a mechanism iff:

For every candidate enumeration E that takes only S as input, there exists a reachable learner history H and a form f in Forms(S, H) such that f is not listed by E.

In compact form: there is no enumeration from source alone that covers the mechanism's producible forms, because learner history can resolve at least one structural decision outside the source-enumerable set.

Two clarifications are load-bearing:

(a) "From source alone" excludes the learner's history, the environment's answers, and any runtime oracle. An enumeration that needs to inspect H, or that needs the oracle's `expected` values, does not count as from source alone. This is exactly the boundary the H2 (oracle) analysis draws: oracle-fed selection is not learner origination.

(b) "Structural" excludes parameter filling. The DOF map recorded 5 MIXED decisions and roughly 240 RESEARCHER decisions; the MIXED decisions move values (indices, literals) within source-fixed schemas. SUF is about the schema itself. A mechanism that selects among 3 fixed templates using learner state fails SUF, because E can list all 3 templates from source alone. TNN-2's construction is the canonical failure: 3 fixed linear assembler families, researcher-fixed wirings, bounds, and order, with learner-chosen indices. Every producible graph is enumerable from source alone by listing the 3 families and noting the parameter slots.

## 3. Why this is the right level

The zero-improvement analysis established that TNN-2's diagnosis was pitched at the wrong level. The gap analysis correctly identified missing capabilities (construction, inquiry, revision) but the implemented mechanisms satisfied the capability names while violating the property the clusters actually required. Concretely:

- "Add construction to fix FW3" is underdetermined: template instantiation is a kind of construction, and it does not fix FW3. FW3 needed a specific property of construction (history-parameterized generativity), not construction in the abstract.
- "Add inquiry to fix FW6" is underdetermined: a constant act is a kind of inquiry act, and it does not fix FW6. FW6 needed state-contingent discrimination, not an act in the abstract.
- The result was byte-identical pass/fail at the world level: zero clusters moved, zero regressions. That signature means the changes operated at a causal level that did not intersect the bottlenecks at all. Partial movement would have licensed incremental widening (the menu treadmill Micah forbade). Zero movement is evidence the diagnosis named the wrong property.

SUF names the property whose absence explains the zero. Every TNN-2 mechanism fails SUF: its producible forms are enumerable from source alone. Every cluster's failure mode is consistent with SUF absence: the required form in each case lies outside the source-enumerable set, and nothing in the mechanism can go outside it.

## 4. Sub-properties per cluster

Each frozen cluster needs SUF in a cluster-specific shape. These are specializations, not separate properties.

**FW3 (arithmetic/composition): history-parameterized generativity.**
The produced form must be a function of learner history such that distinct histories yield forms not jointly enumerable from source. Example shape: reusing a previously learned repeated-addition schema inside a new construction to express multiplication-like behavior, where the reuse decision and the resulting composite topology depend on what the learner previously built. Test-relevant contrast: TNN-2's assemblers take only runtime indices; no accumulated structure enters the production path.

**FW6 (active inquiry): epistemic-state-contingent discrimination with a resolution transition.**
The inquiry act must be indexed by a learner-maintained representation of uncertainty (what is unknown, what would discriminate), and the resolution path must transition that representation. A constant act (CHOICE 0, CHOICE 30) fails regardless of its value; the act space must be underdetermined by source. Test-relevant contrast: TNN-2's miss flag is L2 infrastructure, but the act and content are researcher constants at fixed source lines, and no resolution transition exists.

**FW7 (planning): goal-conditioned composition.**
Action sequences must be composed conditioned on a learner-represented goal, and the composition operator (how steps combine) must itself be selectable outside the source-enumerable set. Enumerated step templates assembled in a fixed order fail; the composition structure must depend on the goal representation, which is learner state. Test-relevant contrast: TNN-2's assemblers build relational graphs, not action sequences, and composition order is a researcher literal.

**FW8 (novel utterance): combinatorial novelty.**
Outputs must be new arrangements of known parts, where the arrangement space expands through experience rather than being fixed in source. Filling new literals into fixed topologies is not combinatorial novelty; the topology must be arrangeable in ways the source does not enumerate. Test-relevant contrast: TNN-2 emits fixed topologies with new literals (the red team's "fixed templates with variable content").

**FW9 (relational DAG): learner-scaled search.**
Search bounds (depth, branching, traversal extent) must be set from learner resources or experience, not from researcher literals. A depth-4 ceiling written as a source literal fails even if the learner fills everything inside the 4 levels; the bound itself must be a learner decision. Test-relevant contrast: the confirmed depth-4 ceiling is architectural, and GW1 confirmed it behaviorally.

## 5. Operational test

The zero-improvement analysis proposed: "list every structural decision the learner can make that the source cannot; if the list is empty, the mechanism cannot move any cluster." Operationalized as a white-box procedure:

Step 1. Enumerate every structural decision in the mechanism's output production path: topology choice, operator choice, wiring, node/edge creation, ordering, bounds, acceptance criteria that select among forms. (The DOF map is the template for this enumeration; SUF asks the follow-up question the DOF map did not ask.)

Step 2. For each decision, classify its value space:
  (a) source-enumerable: the set of possible values is fixed by source literals or finite source enumerations (e.g., "choose among 3 templates", "k in 2..4", "constant 30"). Learner history may select within this set, but cannot go outside it.
  (b) source-underdetermined: learner history can resolve the decision to a value outside every source-enumerable set. This requires a production write path from learner state to the structural decision (the H3 probe's effect-domain question), exercised in the cluster worlds rather than dead code.

Step 3. The mechanism passes the SUF screen iff at least one structural decision classifies as (b), and the (b) decisions are on the causal path of the cluster being tested (not in unreachable code, not in a test-only branch like `mp_set`).

Step 4 (negative control). Construct the source-only enumeration E: list every form the mechanism can produce assuming arbitrary parameter values but no history-dependent structural choice. If any form the mechanism actually produced in a cluster world is missing from E, the classification in Step 2 was wrong; re-examine. If E covers everything produced, SUF fails.

Pass/fail: SUF screen PASS requires a nonempty list from Step 3 with the Step 4 control satisfied. This screen is necessary but not sufficient for cluster movement (see section 6). It is cheap, white-box, and can be run against frozen source before any worlds are executed, which makes it suitable as a preregistration gate: a mechanism that fails the SUF screen cannot move any cluster, so running the worlds would be uninformative.

## 6. Necessary vs sufficient

SUF is necessary. The zero-improvement result is the evidence: three mechanisms, all SUF-absent, moved zero clusters with zero regressions. The contrapositive is the claim: if a mechanism moves a cluster, it exhibits SUF in that cluster's shape, because moving the cluster requires producing a form outside the source-enumerable set (each cluster's failure analysis identifies the required form as outside TNN-2's enumerable set).

SUF is not sufficient. Four gaps, each corresponding to an existing analysis thread:

(a) Utility. A random topology generator exhibits SUF (its forms are not enumerable from source) and is useless. SUF must be paired with world-pass criteria: the underdetermined forms must actually solve the cluster worlds. The kill bars (K-T3-*) carry the utility requirement.

(b) Verifiability. SUF forms selected by oracle comparison are still answer-fed (the H2 problem). SUF must be paired with learner-internal verification: the acceptance criterion must itself be learner-owned, not oracle-fed. The H2 probes and K-H2 bars carry this requirement. Note the ordering constraint from the roadmap: widening SUF-shaped mechanisms before H2 is addressed produces a larger finite menu under the same oracle (the treadmill warning).

(c) Revisability. SUF forms that cannot be revised after counterexamples are one-shot novelties (the GW8 finding: revision is one-shot; the H3 analysis: 4-op ISA cannot express structural revision). SUF must be paired with structural revisability: the learner must be able to modify the forms it originated. K-H3 and the protected-core decision carry this requirement.

(d) Cognitive reuse. SUF forms that are causally inert at query time do not constitute cognitive structure (the C0-D analysis: promoted graphs shadow themselves; no score establishes reuse). SUF must be paired with a reuse path: originated forms must be executable at query time and improve later performance. K-REUSE-1/2 carry this requirement.

The sufficiency stack is therefore: SUF AND utility (K-T3) AND learner-internal verification (K-H2) AND revisability (K-H3) AND cognitive reuse (K-REUSE). SUF is the gate at the entrance: without it, the rest of the stack cannot engage, because there is no learner-originated form for verification, revision, or reuse to operate on.

## 7. Relation to existing vocabulary

- Enumerated-schema / filled-slot (red-team synthesis): the diagnosis SUF formalizes. "Enumerated schema" means the form set is enumerable from source alone; "filled slot" means the learner's contribution is restricted to class (a) value selection in the Step 2 classification.
- L2 structural learning vs L3 representational invention: L2 as currently evidenced (TNN-2) is SUF-absent structural learning, forms enumerable from source, content from learner. SUF is a necessary condition for the L3 claim as Micah defined it (final structure not enumerated beforehand, created after experience), but SUF alone does not satisfy the full 12-criterion L3 bar; the sufficiency stack in section 6 maps onto those criteria.
- C0-A (runtime-defined semantics): SUF is the form-level counterpart. C0-A requires semantics to reside in learner-created state; SUF requires form to be underdetermined by source. A mechanism could in principle satisfy one without the other; the TNN-3 bars should require both.
- H1/H2/H3: SUF is the property H1 (construction grammar is researcher-enumerated) denies and H3 (operating procedures live in source) blocks at the effect-domain level. H2 (oracle supplies the answer) is orthogonal to SUF and must be addressed independently, per the roadmap ordering.

## 8. Caveats and open questions

1. This definition has not been tested against a positive case. It was reverse-engineered from failures (TNN-1, TNN-2, MUL comparator). A mechanism that passes the SUF screen has not yet been observed; the screen's discriminative power on real candidates is unvalidated.

2. The structural vs parameter distinction in section 2 can be gamed at the margin (e.g., a "parameter" that indexes into a large but finite source table of topologies is still source-enumerable; a table grown by learner experience is not). Preregistrations using SUF should fix the distinction with the Step 4 negative control rather than relying on intuition.

3. SUF is stated per mechanism, but clusters may require SUF across interacting mechanisms (K-XMECH territory). The composition of two SUF-absent mechanisms does not yield SUF; whether the composition of two SUF-present mechanisms preserves it depends on the interaction, and is left open.

4. The name is a proposal. If Micah prefers vocabulary closer to the parent's own phrasing ("output space not enumerable from source alone"), the substance is in sections 2 and 5, and the label can change without loss.
