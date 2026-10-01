# Source-Underdetermined Form (SUF): Testable Entrance Criterion

Status: FORMALIZATION-COMPLETE. Analysis only; this document standardizes
the SUF screen as the entrance criterion for future construction work per
Micah's 2026-10-01 ruling. It governs nothing until incorporated into a
preregistration Micah reviews and freezes. It builds on PROPERTY_DEFINITION.md
(`64eec921f`, proposal) and the TNN-2 SUF check (`8ef148a42`, all SUF-FAIL).

## 1. One-line statement

A mechanism exhibits Source-Underdetermined Form when at least one causal
structural decision in its production path is resolved by learner history
such that the produced form cannot be completely enumerated from source
alone.

## 2. Formal definition

Let S be the mechanism's frozen source code: every literal, constant, fixed
enumeration, schema, topology, wiring pattern, ordering, and bound it
contains. Let H range over reachable learner histories: the full persistent
learner state attainable through legitimate experience under the frozen
evaluation protocol (memories created, connections formed, structures built,
policies learned, all within the frozen architecture). Let Forms(S, H) be
the set of structural schemas the mechanism can produce given source S and
history H. A structural schema means a topology, wiring arrangement, operator
composition, node/edge creation pattern, ordering, or bound, where two
schemas are distinct when they differ in structure rather than merely in
filled parameter values. Filling indices or literals into a fixed schema
does not create a new schema.

SUF holds for a mechanism iff:

For every candidate enumeration E that takes only S as input, there exists
a reachable learner history H and a form f in Forms(S, H) such that f is not
listed by E.

Compactly: no source-only enumeration covers the mechanism's producible
forms, because learner history resolves at least one structural decision
outside every source-enumerable set.

Two clarifications are load-bearing (from `64eec921f`):

(a) "From source alone" excludes the learner's history, the environment's
answers, and any runtime oracle. An enumeration that must inspect H, or that
needs the oracle's expected values, does not count as from source alone.
Oracle-fed selection is not learner origination (the H2 boundary).

(b) "Structural" excludes parameter filling. Selecting among researcher-fixed
templates, filling indices or literals into fixed slots, or choosing values
within a source-fixed schema are class (a) operations. SUF concerns the
schema itself.

## 3. The testable criterion

### 3.1 What counts as a "causal structural decision in the production path"

A structural decision is a point in the mechanism's output production path
where one of the following is determined: topology choice (which shape the
produced structure takes), operator choice (which operations compose it),
wiring (how nodes or cells connect), node or edge creation (whether and
where new structure appears), ordering (the sequence in which candidates or
steps are tried or assembled), bounds (search depth, breadth, budget, or
termination conditions that delimit the form), or acceptance criteria that
select among structurally different forms.

"Causal" and "in the production path" restrict the set further. The decision
must lie on the path that actually produces the mechanism's output in the
evaluated worlds, not in dead code, not in a test-only branch, not in driver
harness code, and not in a branch unreachable under the frozen evaluation
protocol. A decision in `mp_set` (test-only, no production caller) does not
count. A decision gated by a driver flag (`dc`, `di`, `masked`) does not
count, because those are researcher inputs, not learner state. A decision
whose precondition requires a node type the cognition path cannot create
(the `comb_present` gate requiring a type-8 node) does not count, because it
is externally gated, not learner-resolved.

The enumeration of candidate decisions follows the DOF map template: list
every point where structure (not just value) is determined, with exact
source locations.

### 3.2 How to verify "resolved by learner history"

A structural decision is resolved by learner history iff all of the
following hold:

1. **Production read path.** The decision's code reads at least one field
   of persistent learner state (not a source literal, not a driver flag,
   not an oracle-supplied value) and the read value causally determines
   which structural alternative is taken. White-box evidence: the source
   lines showing the read and the branch or parameterization it controls.

2. **Production write path.** There exists a path, exercised during
   legitimate experience (not dead code, not test-only), by which the
   learner's own processing writes or modifies those fields. The write
   must be reachable in the evaluated worlds. White-box evidence: the
   source lines showing the write, plus a transcript or log showing the
   write path firing during an actual run.

3. **History dependence, not researcher default.** The learner-state value
   that resolves the decision must have been created or modified by the
   learner's experience, not shipped as a researcher default that experience
   never changes. If the field always holds its initial value in every
   evaluated world, the decision is resolved by the researcher default, not
   by learner history. White-box evidence: show the field taking at least
   two different values across different histories, with the differing
   values traceable to differing experiences.

4. **Ablation flips the structure.** Removing or resetting only the
   learner-state value (holding source and current input fixed) changes the
   structural outcome. This is the anti-theater condition: a value stored in
   learner state with no exercised production write path, or with a write
   path whose output never changes a structural decision, is theater, not
   learner resolution. This mirrors the K-H3 write-path audit's failure
   conditions and K-H2-3's sub-clause (b).

If any of (1) through (4) fails, the decision is not resolved by learner
history, regardless of where its inputs nominally live.

### 3.3 How to verify "cannot be completely enumerated from source alone"

The negative control (Step 4 of the operational test):

1. Construct the source-only enumeration E. List every structural form the
   mechanism can produce assuming arbitrary parameter values (any indices,
   any literals, any oracle answers) but no history-dependent structural
   choice. E is built from S alone: fixed topologies, fixed wirings, fixed
   orderings, fixed bounds, finite candidate families.

2. Check coverage. If every form the mechanism produced in the evaluated
   worlds is an instance of E (a listed schema with filled parameters),
   then the produced forms are enumerable from source alone and SUF fails
   on the observed evidence.

3. Check reachability beyond E. SUF-PASS additionally requires
   demonstrating at least one reachable learner history H and one form f in
   Forms(S, H) such that f is not listed by E. "Reachable" means attainable
   through legitimate experience under the frozen protocol, not through
   source edits, driver flags, or oracle injection. The demonstration may be
   constructive (an actual run producing f) or analytic (a white-box proof
   that some H drives the (b) decision outside E), but an analytic proof
   must identify the concrete H and the concrete f, not merely assert
   existence.

A common failure mode at this step: the enumeration E is drawn too narrowly
(e.g., listing only forms seen so far rather than all forms S permits), which
manufactures a false PASS. E must be the closure over S: everything S alone
permits, not everything observed. Conversely, E must not smuggle H inside
(e.g., "the topology the learner built" is not a source-only description).

### 3.4 Falsification condition (SUF-FAIL)

A mechanism is SUF-FAIL iff, after the Step 1 enumeration and Step 2
classification, the list of class (b) decisions (structural decisions
resolved by learner history outside every source-enumerable set) is empty;
or, if a nonempty (b) list is claimed, the Step 4 negative control covers
every produced form and no reachable H yielding an f outside E is
demonstrated. Either way, the mechanism's producible forms are enumerable
from source alone.

SUF-FAIL is a property of the mechanism under the frozen source, not a
verdict on the learner's effort. A SUF-FAIL mechanism can still exhibit
L2 structural learning (section 4.1), move values through learner state, and
pass capability-flavored checks; it cannot produce a form its programmers
could have listed in advance.

## 4. Distinctions from neighboring concepts

### 4.1 SUF vs L2 structural learning

L2 (Micah's taxonomy): the system constructs new relationships, procedures,
causal structures, or combinations from generic mechanisms, where the exact
learned structure did not exist in source. TNN-2's construction is L2:
the exact graph (which literals, which indices) did not exist in source
before the run.

SUF-absent L2 is the precise characterization of TNN-2. The learned
structure's content is new; its form is not. Every TNN-2 graph is one of 3
fixed assembler topologies with filled slots. L2 as currently evidenced does
not require SUF, and SUF is not implied by L2. SUF is a necessary condition
for the L3 claim as Micah defined it (final structure not enumerated
beforehand, created after experience), but SUF alone does not satisfy the
full 12-criterion L3 bar. The sufficiency stack (section 7) maps onto those
criteria.

Test: a mechanism can be L2-PASS and SUF-FAIL simultaneously. TNN-2's
construction is the canonical instance.

### 4.2 SUF vs H3-lite policy nodes

H3-lite moves researcher-fixed decision points into learner-state policy
nodes: trial search order (node 1), guide default action (node 2), repair
topology dispatch (node 3). Each move satisfies the write-path audit shape
(decision, fields, read path, write path, triggering experience, behavioral
variation).

H3-lite does NOT establish SUF, by its own preregistration (`dab50dd68`):
"The policy value spaces (six order slots over six fixed families; one
default action; six fixed topologies) are enumerable from source. Learner
history selects among researcher-enumerated alternatives; it does not create
new structural forms." The H3-lite standing metric requires SUF DECISIONS
to read zero; any nonzero claim fails the experiment's non-claims.

The distinction: H3-lite changes *who holds the selector* (learner state
instead of source literal) without changing *the size of the menu* (still
source-enumerable). SUF requires the menu itself to be underdetermined by
source. A policy node that reorders six fixed families is learner-held
selection within a source-enumerable set: class (a). A policy node whose
reordering could produce a seventh family, or a wiring the source never
lists, would be class (b); H3-lite's nodes cannot, because their value
spaces are fixed enumerations.

This is why Micah scoped H3-lite as diagnostic: it tests whether moving
criteria into learner-writable state produces causal improvement *before*
expanding the protected core, and its SUF non-claim keeps the inference
honest.

### 4.3 SUF vs C0-A (runtime-defined semantics)

C0-A: the semantics must reside in learner-created persistent state while
source holds only generic execution or construction machinery; a dedicated
pre-written semantic case kills the claim.

SUF is the form-level counterpart of C0-A. C0-A governs *meaning* (where
interpretation lives); SUF governs *shape* (whether the produced topology is
enumerable from source). A mechanism could in principle satisfy one without
the other: learner-held semantics applied to source-enumerable forms
(C0-A without SUF), or history-dependent form selection under
researcher-fixed interpretation (SUF without C0-A). The TNN-3 bars should
require both, and the six open-questions review retains the C0-A regression
bar alongside any SUF entrance criterion.

### 4.4 SUF vs C0-B (open structural form)

C0-B: no choosing one complete answer from a finite researcher-enumerated
solution family; the exact final topology emerges incrementally.

SUF is the testable formalization of C0-B's "not enumerated" clause. C0-B
adds a further requirement SUF does not state: incremental emergence (the
topology is built up over experience, not selected whole). A mechanism could
be SUF-PASS via a single history-dependent choice among a
history-constructed (not source-listed) family, yet still select the final
topology whole rather than emerging it incrementally; that would satisfy
SUF while leaving C0-B's emergence clause untested. Treat SUF as necessary
for C0-B and let C0-B's preregistration carry the incremental-emergence
requirement separately.

## 5. Worked example: TNN-2 construction SUF-FAIL

This applies the section 3 criterion to frozen TNN-2 construction
(`tnn2.zag`, build `f4de7ff46`), reproducing and formalizing the `8ef148a42`
check. Production path: `ev_query` miss (line 827) to `mp_run` (668) to
`t2_trial` (586) to assemblers `t2_asm_chain` (363), `t2_asm_sum` (398),
`t2_asm_count` (379) to `t2_try_verify` (497) to `promote_graph` (533).

Step 1 (structural decisions, with source locations from `8ef148a42`):

- C-1: Phase order: chains k=2..4, then sums, then counts, then single
  hops (`t2_trial` lines 591-666).
- C-2: Chain depths attempted: k in {2,3,4}, longer first (line 592).
- C-3: BFS gather bound: depth 1..4, 96-path cap (`t2_gather` ~442-473).
- C-4: Graph family: exactly 3 assemblers, each emitting one fixed topology
  (lines 363-411).
- C-5: Sum budget: decline when total <= 0 or total > 900 (line ~401).
- C-6: Subset enumeration order: size descending, bitmask descending
  (lines ~616-641).
- C-7: Search termination: first candidate to verify stops the whole search
  (lines 604-608, 627-629, 643-645, 658-660).
- C-8: Verification criterion: unmasked accepts iff expected != -2 and
  v == expected; masked accepts first candidate with clean execution
  (`t2_try_verify` lines 497-509).
- C-9: Promotion schema: tag-20 MAP with fixed fields plus shadow
  `ev_teach_in` (`promote_graph` lines 533-544).
- C-10: Literal slots filled from data vectors (assembler calls passing v,
  f, vals buffers).

Step 2 (classification):

- C-1, C-2, C-3, C-4, C-5, C-6: class (a). Fixed orders, literals, and three
  fixed topologies, all readable from S alone.
- C-7: class (a). The candidate family is finite and fixed by source (at
  most 96 BFS paths at depths 2..4, at most 4095 nonempty subsets of at
  most 12 values, at most 16 relations, single hops); the rule
  (first-to-verify under the fixed order) is a source literal. Learner
  history selects which candidate survives but cannot go outside the
  family. (The DOF map's MIXED label K4 does not survive the section
  3.2 test: selection within a source-fixed finite set is class (a).)
- C-8: class (a). The acceptance rule is a source literal and the oracle
  supplies the acceptance value. Oracle-fed selection is not learner
  origination.
- C-9: class (a). Fixed MAP schema; the shadow teach is a source-written
  call at line 541.
- C-10: class (a). Filling indices and literals into fixed slots is
  parameter filling, explicitly excluded from "structural" by
  clarification (b). (The DOF map's MIXED labels K5/H4 do not survive.)

Two apparent learner knobs are not structural decisions at all: `dc`,
`di`, and `masked` are driver flags, not learner state; the sum phase gate
`comb_present` requires a type-8 node the cognition path cannot create, so
it is externally gated.

Step 3: the class (b) list is empty. No structural decision in the
construction production path is resolved by learner history outside a
source-enumerable set. In particular, section 3.2 condition (1) fails
everywhere: no structural decision's code reads a history-written
learner-state field to select among structurally different alternatives.

Step 4 (negative control): E = {chain topologies for k=2..4 with the fixed
guard+set wiring; sum topologies of `total` unrolled INC cells for total in
1..900; count topologies with the fixed chain+inc+MOVE-epilogue wiring;
single-hop chains}. Every graph produced in the freeze and GW worlds is an
instance of E with filled literals. E covers everything produced.

Verdict: CONSTRUCTION SUF-FAIL. Consistent with `8ef148a42`. The same
procedure yields INQUIRY SUF-FAIL (one fixed 2-node schema, constant act 30)
and REVISION SUF-FAIL (one fixed replace-SET-step schema); see `8ef148a42`
for the full tables.

## 6. Hypothetical PASS example

What would a SUF-PASS construction mechanism look like? It must differ from
TNN-2 not in degree (more templates) but in kind (the form space itself
must be history-dependent). Micah's H1 ruling forbids the degree move
("Do not expand from 3 templates to 30 templates"); the PASS example must
show the kind move.

Consider a construction mechanism with a composition memory. During WORLD A
(arithmetic experience), the learner builds and promotes a repeated-addition
schema: a MAP whose executable structure chains an increment cell a
learner-determined number of times, where the chaining pattern itself (not
just the count) was assembled by a previous construction episode and stored
as a reusable fragment. During WORLD D (a novel composition problem), the
construction production path reads the fragment store (learner state,
written by the WORLD A episode through an exercised production write path),
selects the repeated-addition fragment based on a structural match between
the current problem's dependency shape and the fragment's recorded shape
(a structural decision: which prior fragment to compose, and where to splice
it), and emits a composite graph whose topology (fragment + novel wiring)
is not listed in any source-only enumeration.

Why this passes:

- Step 1: the fragment-selection-and-splice decision is structural
  (topology choice and wiring determined at that point).
- Step 2: it classifies as (b). The value space (which fragments exist,
  what shapes they have) is determined by H, not S. No source-only
  enumeration can list the fragments, because the fragments did not exist
  until experience created them. Section 3.2 conditions: (1) the decision
  code reads the fragment store; (2) the store is written by construction
  episodes through a production write path; (3) the store's contents differ
  across histories (a learner that never saw WORLD A has no
  repeated-addition fragment); (4) ablating the fragment store changes the
  produced topology (without it, the mechanism falls back to a
  source-enumerable default or fails).
- Step 4: E (source-only) lists the base assembler schemas. The composite
  fragment-splice form is not in E. A concrete H (the WORLD A history) and
  a concrete f (the composite graph) are demonstrated.

Why "30 templates" would still fail: thirty fixed families are still a
source-only enumeration with thirty entries. The PASS example's menu is not
a longer list; it is a list whose entries are created by experience. The
test that distinguishes them: a fresh learner and an experienced learner,
given the same query under the same frozen source, produce structurally
different forms. Under 30 templates, they cannot (both select within the
same 30). Under the PASS mechanism, they can (the experienced learner has
fragments the fresh learner lacks).

Non-goals of this example: it does not by itself establish utility (the
composite must actually solve WORLD D), learner-internal verification (the
acceptance criterion must not be oracle-fed), revisability, or reuse. Those
are the sufficiency stack (section 7). The example isolates SUF.

## 7. White-box evidence required to claim SUF-PASS

A SUF-PASS claim must present, at minimum, all of the following. Missing
any item demotes the claim to SUF-UNPROVEN (not SUF-FAIL; the screen is
inconclusive until the evidence is supplied).

1. **Decision inventory (Step 1).** Every structural decision in the
   mechanism's production path, each with exact source location (file,
   function, line). The inventory must be exhaustive over the path that
   produced the claimed forms; an omitted decision that is in fact
   class (b) is a missed pass, and an omitted decision that is class (a)
   but load-bearing for the enumeration is a false pass.

2. **Classification table (Step 2).** Each decision classified (a) or (b)
   with justification. Every (a) claim cites the source literals or finite
   enumerations fixing the value space. Every (b) claim identifies the
   learner-state fields read, the production read path (source lines), and
   why the value space is not source-enumerable.

3. **History-resolution proof (section 3.2).** For each claimed (b)
   decision, all four conditions with evidence:
   - (1) source lines of the read path and the structural branch it
     controls;
   - (2) source lines of the production write path, plus a run transcript
     or log showing the write path firing during legitimate experience;
   - (3) demonstration that the field takes at least two values across
     different histories, each traceable to differing experience (not
     researcher defaults);
   - (4) ablation: with source and current input held fixed, removing or
     resetting only the learner-state value changes the structural
     outcome. State the ablation procedure exactly so it is reproducible.

4. **Negative control (Step 4).** The source-only enumeration E, written
   out (not gestured at), constructed as the closure over S. Then either
   (i) a produced form f from an actual run that is not an instance of E,
   with the run identified (world, seed, transcript location); or (ii) an
   analytic reachability argument naming a concrete H and a concrete f in
   Forms(S, H) outside E, with the derivation from the (b) decision's
   mechanics. If every produced form is an instance of E and no such
   (H, f) is demonstrated, the claim fails.

5. **Causal-path attestation.** For each (b) decision, evidence it lies on
   the production path of the claimed forms: not dead code (coverage or
   transcript), not test-only (has a production caller), not driver-gated
   (no driver flag in its precondition chain), not externally gated (no
   precondition requiring state the cognition path cannot create).

6. **Fresh-vs-experienced contrast.** Run the same query under the same
   frozen source on a fresh learner and on the experienced learner whose
   history supplies the (b) values. Show structurally different forms
   (different schemas, not different fillings). This is the behavioral
   signature of section 6's distinguishing test and guards against
   analytic errors in the classification.

7. **Standing metric row.** The twelve fields Micah requires for every new
   mechanism report (researcher-owned structural decisions,
   learner-owned structural decisions, source-enumerable forms, SUF
   decisions, learner-internal criteria, reuse events, revision events,
   cognition lines, modes, bridges, handlers, semantic cases), with SUF
   DECISIONS equal to the number of evidenced (b) decisions from item 3.

## 8. SUF under the continuous-learner evaluation policy

Micah's 2026-10-01 clarification: "freeze" freezes researcher-authored
architecture and source, not the learner. The scientific ideal is FROZEN
RESEARCHER CODE + CONTINUOUSLY CHANGING LEARNER STATE.

SUF is stated against frozen S with H as the variable, so it is already
the continuous-learner criterion: it asks whether the frozen architecture
permits H to resolve structural decisions. In a lifetime stream (WORLD A
to learn, WORLD B to retain and reuse, WORLD C to revise, WORLD D to
discover, return to WORLD A-like problems with no reset), SUF-PASS has a
characteristic signature: Forms(S, H_t) grows or shifts structurally as
H_t accumulates, and a reset learner placed at the same stream position
cannot produce the experienced learner's forms. Cross-domain connection
(a structure learned for arithmetic recognized as useful for planning) is
the strong form of this signature: the (b) decision's value space at time
t contains structures built at times far earlier and in different domains.

Isolation tests (fresh-start worlds with reset learner state) remain useful
for causal attribution: they establish the baseline Forms(S, H_0). The
lifetime version measures the SUF-relevant quantity directly: how
Forms(S, H_t) diverges from Forms(S, H_0) through experience alone, with
source frozen throughout. A mechanism that is SUF-FAIL shows no such
divergence at the structural level (only parameter filling varies); a
mechanism that is SUF-PASS must show it, and the lifetime stream is where
the demonstration is cleanest.

Stability vs rigidity (Micah): SUF is the precise form of the requirement
that architectural stability coexist with cognitive plasticity. The
architecture (S) is stable; cognition (H, and through it the producible
forms) is plastic. SUF-FAIL is the failure mode "architectural stability +
frozen cognition": the form space does not move no matter how rich H
becomes. SUF does not ask for architectural instability (editing S per
world); it asks whether the frozen S leaves structural decisions to H.

## 9. Open questions

1. The screen has no validated positive case. It was reverse-engineered
   from failures (TNN-1, TNN-2). Its discriminative power on a real
   candidate is unproven; the first SUF-PASS claim will test the
   formalization itself, and section 7's evidence bar is deliberately set
   so that a false pass is harder than a missed pass.

2. The structural vs parameter boundary can be gamed at the margin (a
   "parameter" indexing a large finite source table of topologies is still
   source-enumerable; a table grown by learner experience is not). Section
   7 item 4 (the written-out E) is the backstop: disputes are settled by
   the enumeration, not by intuition about the label.

3. Composition of mechanisms is open: two SUF-absent mechanisms composed do
   not yield SUF; whether two SUF-present mechanisms preserve it depends on
   the interaction. Preregistrations for multi-mechanism candidates should
   run the screen per mechanism and state the composition assumption.

4. SUF is necessary, not sufficient. The sufficiency stack for future
   invention, per Micah's ruling: SUF AND useful behavior (kill bars) AND
   learner-internal verification (K-H2 family) AND revisability (K-H3
   family) AND cognitive reuse (K-REUSE family). SUF is the entrance gate:
   without a learner-originated form, verification, revision, and reuse
   have nothing to operate on.
