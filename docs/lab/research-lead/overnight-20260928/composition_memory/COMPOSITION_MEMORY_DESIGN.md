# Composition Memory: Design for the Kind-Move Toward SUF

Status: DRAFT-NOT-FROZEN. Design only; nothing built, nothing tested.
This document proposes a construction-memory mechanism whose fragment
menu is created by experience, as the kind-move Micah's H1 ruling
requires. It does not begin H1 implementation. H1 remains deferred until
H2 evidence lands.

## 1. The kind-move vs the degree-move

Micah's 2026-10-01 ruling: "Do not expand from 3 templates to 30
templates. Do not add capability-shaped operators. The entrance criterion
for future construction work is Source-Underdetermined Form."

The degree-move: more fixed templates. Three assemblers become thirty.
Every new family is still a source literal. The source-only enumeration
E grows from 3 entries to 30 entries and still covers everything the
mechanism can produce. SUF-FAIL is preserved exactly. This is the
treadmill the ruling forbids.

The kind-move: the menu itself is history-created. The mechanism's
construction production path selects among fragments that did not exist
until experience built them. No source-only enumeration can list the
fragments, because the fragments are a function of learner history, not
of source. This is the direction SUF formalization `7dddf3933` section 6
sketches as the hypothetical PASS example. This design works out that
sketch into an implementable proposal with its weak points named.

One-System Rule compliance: fragments are the same executable graph
type as every other MAP (tag-20 nodes with the existing field layout),
not a second representation. The fragment store is a collection of MAP
nodes with additional bookkeeping fields, not a new subsystem, mode,
bridge, or handler.

## 2. Fragment lifecycle

### 2.1 Creation: what triggers fragment extraction, what is stored

Trigger: a construction or revision episode that ends in promotion. When
`promote_graph` (or its successor) promotes a verified executable graph,
the promotion path additionally runs fragment extraction. Extraction is
not a separate researcher-invoked step; it is part of the production
promotion path, so every promoted structure is a candidate for future
composition. This keeps the write path exercised by legitimate
experience, which section 3.2 condition (2) of the SUF formalization
requires.

What is extracted: the subgraph that actually executed during the
verification episode, determined from the execution trace, not from a
fixed source template of "the extractable part." Concretely, the
extraction walks the cells the executor touched between the graph's entry
point and its answer-producing step, and records that walked topology
with literals stripped to parameter slots. The walked topology is
history-determined (it depends on what the graph did on the data it saw);
a fixed "extract the middle third" rule would be source-enumerated and
is rejected.

What is stored per fragment (all in learner state, as fields on a
fragment MAP node or a small fragment record linked to it):

- F-shape: the structural signature of the fragment topology
  (signature function over wiring and node roles, literals excluded).
  This is what selection matches against, so matching is on shape, not
  content.
- F-interface: the fragment's entry point and exit point (which cell
  receives the input frame, which cell yields the output value), recorded
  from the execution trace. The interface is what makes splicing
  well-defined without a researcher-fixed splice template.
- F-slots: the parameter slots (positions where literals were stripped),
  with the stripped values recorded as the fragment's default fillings
  (overridable at splice time by the new problem's data).
- F-provenance: the experience that created it (world id, episode
  counter, the parent graph it was extracted from).
- F-utility: two counters, invocations and successes, both written by
  later experience (selection writes invocation; verification of the
  composite writes success). These are the learner-written ordering
  fields; see the weak-points section on why ordering must not be
  researcher-fixed.

The fragment store starts empty. No researcher seed fragments. A seed
would be a researcher default resolving the selection decision, failing
section 3.2 condition (3). The empty start is also what makes the
fresh-vs-experienced contrast test clean.

Memory policy interaction: fragments live under the same node budget as
other learner structures. Eviction, compression, and retirement of
fragments follow whatever general learner-owned memory policy exists;
no fragment-specific storage logic (per the no-treadmill rule on the
store/eviction failure). If a fragment is evicted, later selection
cannot select it; that is correct behavior, and the ablation test in
section 5 can use eviction as a natural ablation.

### 2.2 Selection: criterion and location

Location: in the construction production path, at the point where the
current TNN-2 design runs `t2_trial` over fixed assembler families.
The fragment-selection step runs before (or instead of) the fixed-family
trial loop: it reads the fragment store and selects candidate fragments
to compose. This is the candidate class (b) structural decision: which
prior fragments to compose, and where to splice them.

Criterion, in order of application:

1. Structural match: compute the shape signature of the current
   problem's dependency subgraph (the gathered dependency structure the
   construction path already builds before assembling). Select fragments
   whose F-shape has minimal structural distance to a sub-shape of the
   problem's dependency shape. The distance is computed by a generic
   signature comparison (equality of sub-signatures, or a generic
   edit-count over the signature representation), not by
   researcher-authored per-domain similarity weights. Any weighting used
   in the distance must itself live in learner-writable fields with an
   exercised write path, or the weights are researcher-owned and the
   selection is class (a)-flavored. The default design uses unweighted
   sub-signature matching precisely to avoid smuggling researcher
   judgment into the criterion.
2. Utility ordering among structural matches: order by F-utility
   (successes per invocation), both learner-written. Ties broken by
   recency (also learner state: the episode counter).
3. Splice feasibility: the fragment's F-interface must be compatible
   with the splice point's frame shape (entry cell accepts the frame
   the problem provides; exit cell yields a value of the needed role).
   Compatibility is checked against the recorded interface, not against
   a source list of allowed pairings.

The selection decision reads only learner-state fields (F-shape,
F-utility, F-interface, provenance counters) and the current problem's
dependency shape (runtime data, not source). It does not read a source
list of candidates, because there is none: the candidate set is the
store's current contents.

### 2.3 Splice: operation and placement

The splice operation takes a selected fragment and a splice point in the
emerging composite graph and embeds the fragment's topology at that
point, connecting the fragment's entry cell to the splice point's input
and the fragment's exit cell to the splice point's output, filling
F-slots from the new problem's data where the problem provides values
and from the fragment's default fillings otherwise.

Placement of the operation: the splice machinery is generic graph
surgery (copy cells, rewire edges, fill slots) performed by the
construction production path, i.e., cognition code, reusing the same
graph-building primitives the existing assemblers use. It is not
proposed as a learner-executable ISA opcode: under protected-core
Alternative C, structural graph-mutation opcodes (ALLOC/LINK/KILL) are
deferred and are not added here. If implementing the splice turns out
to require a new protected-core operation, that is an escalation to
Micah under the protected-core boundary rules, not a silent addition.
The design intent is that no new core op is needed: everything the
splice does (allocate cells, link edges, copy values) is already done
by the existing assemblers in the frozen build.

What is learner-resolved vs researcher-fixed at the splice:

- Learner-resolved: which fragment, which splice point, which slot
  fillings. The splice point is determined by matching the fragment's
  F-interface against the emerging composite's open attachment points
  (points where the dependency shape has an unfilled sub-computation),
  not by a source-fixed list of splice locations.
- Researcher-fixed (honestly labeled): the splice mechanics themselves
  (how cells are copied and rewired) are generic machinery, like the
  assemblers' cell emission. The claim is not that the mechanics are
  learner-authored; the claim is that the selection-and-placement
  decision is.

### 2.4 Revision and retirement of fragments

Fragments participate in revision like any other MAP: a counterexample
that contradicts a composite built with a fragment triggers the revision
path, which can supersede the fragment (mark it superseded; the
copy-and-commit discipline applies: the revised fragment is built in
fresh cells and committed atomically, never mutated in place). A
superseded fragment is skipped by selection (the R3 probe pattern from
the reuse experiment). F-utility demotion past a threshold retires a
fragment from the candidate set without deleting it (retired fragments
remain inspectable white-box state; deletion vs retirement is a memory
policy question, not a fragment-mechanism question).

This gives the mechanism the revision event stream the sufficiency
stack requires, using the already-approved copy-and-commit substrate.

## 3. What makes the menu history-created

The anti-enumeration argument, stated as the SUF formalization requires:

Let S be the frozen source including this design. The source contains:
the extraction procedure (walk the executed trace, strip literals),
the selection procedure (sub-signature match, utility order, interface
check), the splice mechanics, and the field layouts. The source does
not contain, and cannot generate without H: any fragment's F-shape,
F-interface, F-slots, or F-utility values, because every one of those
is written by an experience episode.

The source-only enumeration E lists: the 3 base assembler schemas (the
honest fallback when the store is empty or no fragment matches), plus
the generic statement "composites of store fragments." But "composites
of store fragments" is not a source-only description of a form: it
smuggles H inside, exactly the move section 3.3 forbids ("the topology
the learner built" is not a source-only description). Written out
honestly, E covers only the base assemblers. Any composite whose
topology includes a fragment's F-shape is outside E, because no
source-only procedure can produce that F-shape: it was walked from an
execution trace of a graph that was itself built during experience.

The distinguishing test from section 6: a fresh learner and an
experienced learner, same query, same frozen source, produce
structurally different forms. Under 30 templates they cannot (same 30
for both). Under composition memory they can (the experienced learner's
store contains fragments the fresh learner's empty store lacks, so
selection resolves differently and the emitted topology differs in
wiring and composition, not just in filled literals).

Boundary honesty: the base assemblers remain source-enumerable, and a
composite that selection rejects in favor of a base assembler is a
source-enumerable form. SUF-PASS does not require every emitted form
to be outside E; it requires the existence of a reachable H and a form
f in Forms(S, H) outside E, demonstrated concretely (section 7 item 4
of the formalization).

## 4. SUF 4-condition test applied to fragment selection

Candidate class (b) decision: fragment selection-and-splice placement
in the construction production path (which fragments, spliced where).

Condition (1), production read path: the selection code reads the
fragment store's learner-state fields (F-shape, F-utility, F-interface)
and the read values causally determine which fragment is selected and
at which attachment point it is spliced. White-box evidence required
at build time: the source lines of the store read and the branch or
parameterization they control. Design note: the read must control a
structural alternative (different fragment implies different emitted
topology; different splice point implies different wiring), not merely
a value within one topology.

Condition (2), production write path: the fragment store is written by
(a) the extraction step on the promotion path (writes F-shape,
F-interface, F-slots, F-provenance), exercised every time a graph is
promoted during legitimate experience; and (b) the selection and
verification steps (write F-utility invocations and successes).
White-box evidence required: source lines of the writes plus run
transcripts showing the write paths firing during actual runs. Design
note: extraction-on-promotion is deliberately placed on the production
path rather than in a separate researcher-invoked utility, so that the
write path is exercised by experience itself.

Condition (3), history dependence not researcher default: the store
starts empty (no researcher default fragments), and its contents
differ across histories. A learner with only WORLD B experience has a
different fragment set than a learner with WORLD A arithmetic
experience; the differing contents are traceable to differing
episodes via F-provenance. White-box evidence required: the store's
contents after two different histories, with provenance records tying
each fragment to its creating episode.

Condition (4), ablation flips the structure: with source and current
input held fixed, emptying or resetting the fragment store changes the
emitted topology (the mechanism falls back to a base assembler schema
or fails where it previously emitted a composite). The ablation
procedure must be stated exactly (e.g., reset store to empty;
re-run the same query; compare emitted topologies structurally).
This is the anti-theater condition: a store that never changes a
structural outcome is theater.

## 5. Weak points (honest)

These are the points where the design could collapse back to class (a)
or to theater. Each is named so the eventual preregistration can carry
an explicit guard.

W1. Researcher judgment smuggled into the match criterion. If
"structural distance" uses researcher-chosen weights, thresholds, or
per-domain similarity rules, the selection decision is resolved by
those researcher choices, not by learner history. Guard: default to
unweighted sub-signature matching; any learned weights must live in
learner-writable fields with an exercised write path and must
themselves pass the 4-condition test, or they are researcher-owned.

W2. Source-fixed splice points. If the source enumerates where
fragments may be spliced (a fixed list of attachment templates), the
wiring decision is source-enumerable even when the fragment choice is
not. Guard: splice points are the emerging composite's open attachment
points derived from the problem's dependency shape; the source fixes
only the interface-compatibility check, not the locations.

W3. Source-templated extraction. If extraction follows a fixed rule
like "take cells 3..7" or "take the middle third," the fragment shapes
are source-determined slices, and E could enumerate "all slices of the
3 assembler schemas," collapsing the menu back to source-enumerable.
Guard: extraction walks the actual execution trace; the walked set is
determined by what executed on the data seen, which varies with
history and input beyond what S alone predicts.

W4. Researcher-fixed utility ordering. If the ordering among matching
fragments uses researcher-fixed weights combining utility, recency,
and match quality, the ordering decision is researcher-resolved.
Guard: ordering is by the learner-written F-utility counters with a
stated tie-break (recency from the learner's own episode counter);
the combination rule is fixed and generic (lexicographic), not a
weighted score with tuned coefficients.

W5. The composite's novel wiring. The wiring that connects fragments
to each other and to the problem's input/output must itself not be a
source-fixed schema, or E covers the composite as "fragment schema
plus fixed wiring schema." Guard: the inter-fragment wiring is derived
from the fragments' recorded F-interfaces chained through the
problem's dependency shape; where the dependency shape underdetermines
the wiring, the choice is recorded as a further learner-state decision
with its own write path, or the design admits the limitation.

W6. Extraction trigger gaming. "Extract on every promotion" could
flood the store with near-duplicate fragments whose selection is
effectively arbitrary. This does not break SUF formally (the menu is
still history-created), but it weakens the utility story and the
fresh-vs-experienced contrast. Guard: dedupe by F-shape signature on
insert (a fragment whose F-shape already exists increments the
existing fragment's provenance count rather than creating a new
entry); this is generic machinery, not a researcher judgment about
which fragments are "good."

W7. The empty-store fallback. With an empty store the mechanism emits
base-assembler forms, which is correct (the fresh learner behaves like
the current architecture). But the fallback must not become a
researcher-authored "default fragment" that selection prefers; the
fallback is the absence of selection, and the selection path must be
skipped (not run with a default) when the store is empty, so the
ablation in condition (4) is a true removal of the decision.

W8. Cross-domain applicability is not established by this design.
Section 2.2's criterion matches on structural shape, which is the
mechanism by which an arithmetic fragment could in principle be
selected for a planning-shaped problem. But nothing in the design
guarantees such transfer occurs or is useful; that is an empirical
question for the lifetime evaluation, and the design claims no
transfer result.

## 6. Fresh-vs-experienced contrast test

This is the behavioral signature section 7 item 6 of the SUF
formalization requires, specified here so the eventual preregistration
can freeze it.

Setup:

- Frozen source S including the composition-memory design (once built).
- Two learners: FRESH (empty state, H_0) and EXPERIENCED (state after
  a fixed WORLD A curriculum, H_A; the curriculum is part of the frozen
  evaluation protocol, not researcher tuning per run).
- Same query Q from a WORLD D composition problem, posed to both
  learners. No process reset between curriculum and query for
  EXPERIENCED (continuous learner state); FRESH is a reset learner.

Predictions:

- FRESH emits a source-enumerable form (one of the 3 base assembler
  schemas) or fails Q. Its emitted topology is an instance of E.
- EXPERIENCED emits a composite incorporating at least one fragment
  whose F-provenance traces to the WORLD A curriculum. Its emitted
  topology differs structurally from FRESH's (different wiring and
  composition, verifiable by the structural signature function), not
  merely in filled literals.

SUF-PASS demonstration: the pair (H_A, f_experienced) with f outside
E, plus the section 4 evidence (decision inventory, classification,
history-resolution proof, written-out E, causal-path attestation).
The contrast test alone does not establish SUF; it is the behavioral
corroboration of the white-box proof. If EXPERIENCED emits the same
schema as FRESH (only literals differ), the design has failed its own
entrance criterion even if the machinery runs.

Controls:

- Same Q, same S, same driver flags; only H differs.
- A second query Q2 from a domain with no structural overlap with
  WORLD A, where EXPERIENCED should behave like FRESH (no fragment
  selected). This guards against the failure mode where selection
  always fires regardless of match quality (which would suggest the
  criterion is vacuous).
- Byte-identical runs (3/3) per the determinism standard.

## 7. Relation to existing mechanisms

H3-lite: the policy nodes move researcher-fixed decision points into
learner-state policy nodes without changing the menu size (still
source-enumerable; SUF DECISIONS = 0 by preregistration). Composition
memory is the complementary move: it changes the menu itself. If
H3-lite shows that learner-held criteria produce causal improvement,
composition memory is the natural next step that also changes what the
criteria select among. The two compose: a fragment-selection policy
node (H3-lite style) could hold the selection criterion's learned
parameters, while the fragment store (this design) holds the
history-created menu. Neither implies the other.

Reuse path: the MAP-first query discipline (`ea8fc0ac1`) ensures a
promoted structure participates in later cognition instead of being
shadowed by a memorized fact. Composition memory extends reuse from
same-(subject, relation) invocation to cross-episode composition:
fragments are reused as parts of novel wholes. The reuse experiment's
honest finding (mechanical reuse works; the value-trace limitation
persists for cross-subject invocation) bounds what composition memory
can assume: selection matches on structural shape precisely because
literal-indexed invocation does not transfer.

Revision substrate: copy-and-commit with MAP retargeting is the
correctness substrate fragments inherit. Fragment supersession uses
the same discipline; no in-place fragment mutation.

H2 ordering: this design assumes nothing about H2's outcome. If H2
shows TNN cannot yet wield learner-internal accept/reject criteria,
composition memory's selection criterion (a learner-internal
criterion over structures) inherits that limitation, and the design
would need H2's successor first. The H2-before-H1 ordering constraint
(`c15a47d63`) governs.

## 8. Standing architectural metric (reporting template)

For the eventual build report, the twelve fields Micah requires,
with the design's predicted values (predictions, not results):

- RESEARCHER-OWNED STRUCTURAL DECISIONS: extraction procedure shape
  (trace-walk, literal-strip), selection procedure shape
  (sub-signature match, lexicographic utility order, interface check),
  splice mechanics, field layouts, dedupe rule. (Count at build.)
- LEARNER-OWNED STRUCTURAL DECISIONS: fragment selection (which),
  splice placement (where), slot fillings (with what). Predicted: 3,
  each with a 4-condition proof.
- SOURCE-ENUMERABLE FORMS: 3 base assembler schemas (fallback).
- SUF DECISIONS: predicted 2 (selection-and-splice as one decision;
  extraction-boundary as a possible second if the trace-walk boundary
  varies structurally with history; else 1). Zero until evidenced.
- LEARNER-INTERNAL CRITERIA: structural match criterion,
  utility ordering. Predicted 2.
- REUSE EVENTS: fragment invocations in composites (count at eval).
- REVISION EVENTS: fragment supersessions (count at eval).
- COGNITION LINES: count at build (new mechanism code only).
- MODES: 0. BRIDGES: 0. HANDLERS: 0. SEMANTIC CASES: 0.
  (Any nonzero here fails the One-System Rule for this design.)

## 9. Explicit non-claims

1. This design does not establish SUF. SUF is established only by a
   built mechanism passing the section 7 evidence bar of `7dddf3933`
   under a frozen preregistration Micah reviews and freezes.
2. This design does not bypass, shorten, or preempt the H1 deferral.
   H1 (open construction) remains deferred until H2 evidence lands,
   per Micah's 2026-10-01 ruling and the H2-before-H1 ordering
   constraint in `c15a47d63`.
3. This design does not establish utility (the composites must solve
   real problems under kill bars), learner-internal verification
   (acceptance must not be oracle-fed), revisability beyond the
   inherited substrate, or cognitive reuse beyond the fragment
   mechanism itself. Those are the sufficiency stack; SUF is the
   entrance gate only.
4. This design does not establish L3 or any part of the 12-criterion
   L3 bar.
5. The predicted metric values in section 8 are predictions. The
   standing rule applies: report the measured numbers or report
   nothing.
6. DRAFT-NOT-FROZEN: this document is a design sketch for discussion
   and future preregistration drafting. It freezes nothing and
   authorizes no implementation.

## 10. Open design questions

1. Signature granularity: how fine should F-shape signatures be?
   Too coarse and selection matches spuriously (W8 risk); too fine
   and no fragment ever matches a novel problem (the Q2 control
   becomes the norm, and the mechanism never fires). The calibration
   of the signature function is the highest-information empirical
   question and cannot be settled on paper.
2. Whether extraction should also fire on revision episodes that do
   not end in promotion (partial repairs that verify locally but are
   not promoted as wholes). Firing only on promotion is simpler and
   keeps the write path crisp; firing on verified partial repairs
   could enrich the store but complicates provenance.
3. Whether F-utility should decay with time or interference (a
   learner-owned forgetting curve over fragments) or whether
   eviction under the general memory policy suffices. The design
   defaults to the general policy (no fragment-specific logic).
4. Interaction with the lifetime evaluation: the WORLD A curriculum
   that stocks the store must itself be preregistered as part of the
   evaluation protocol, or the curriculum becomes a researcher
   degree of freedom that confounds the fresh-vs-experienced
   contrast. The curriculum is protocol, and protocol is frozen
   before the run.
5. Whether the splice operation, as specified, truly needs no new
   protected-core operation. This must be verified by white-box
   inspection of the existing assemblers' primitives at build time;
   any gap is a Micah escalation, not a silent addition.

No em dashes were used in this document.
