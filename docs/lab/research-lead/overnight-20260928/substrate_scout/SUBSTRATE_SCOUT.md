# Executable Representation Substrate: Frontier Scout Report

Date: 2026-09-30. Lane: scouting only, no implementation.
Status: SUBSTRATE-SCOUT-COMPLETE.

## 0. What this document is

A survey of the generic executable representation substrate frontier:
what it would be, how it differs from current mechanisms, the minimal
general mechanism that could get there, the gap, and a falsifiable
recommended research direction. This is territory mapping, not a build
proposal. Zero cognition source lines are added by this document.

## 1. The frontier, stated plainly

A generic executable representation substrate is a frozen core that
provides two fixed things and nothing else:

1. A generic construction machine: allocate cells, link them into
   structures, name and cite them. The cell algebra is fixed and tiny.
   It is not a menu of representations.
2. A generic execution machine: walk learner-authored structures and
   act on what they say. The executor dispatches over node kinds the
   learner created, not over semantic cases the researcher wrote.

Everything else, including what any structure MEANS, lives in
learner-created persistent state. That is the whole of Micah's
Criterion 0:

- C0-A (runtime-defined semantics): "where are the semantics
  implemented?" must be answered "in learner state", never "in this
  dedicated switch branch written before training".
- C0-B (open structural form): no choosing one complete answer from a
  finite researcher-enumerated solution family; variable-sized and
  growing structures whose exact final topology emerges incrementally.
- C0-C (multiple unforeseen forms): freeze the mechanism, then expose
  it to sealed worlds needing materially different representations,
  at least one family designed by an independent adversary after
  the freeze.
- C0-D (cognitive reuse): the invented structure must improve
  transfer, prediction, procedure learning, causal inference, memory,
  planning, or sample efficiency. Existence alone is insufficient.

The Core Freeze W9 bar is the concrete instance: 80 percent or better
on the task AND white-box evidence of genuinely new structural
topology in persistent learner state (not a shoehorn into existing
slots), reused on a second probe, with a source audit proving the
topology was not pre-allocated and no dedicated semantic case exists.

## 2. Where the current mechanisms sit

### 2a. L3B v2: the menu (bounded, C64)

The L3B v2 constructor is a 205-program finite menu with a fixed
archive. The independent adversary (C64) confirmed the boundary:
construction is selection among pre-enumerated candidates. The
telling detail from the v2 prereg: hand-built MUL(VAR,VAR) evaluates
to 25 at f0=5, so the execution substrate is open while the
construction substrate (rel_of plus build_expr) is closed. The
learner can run expressions it cannot build. Lane ruling stands:
never menu expansion; redesign toward incremental construction.

Distance to the frontier: a menu chooses; a substrate constructs.
L3B selects complete programs from a researcher-enumerated family,
which fails C0-B by definition.

### 2b. L3C v3: cover-set composition (a genuine step, bounded, C73)

L3C v3 closes the disjunction blind spot with cover-set composition:
the learner composes alternative covers from corroborated atoms using
the interpreter's pre-existing union semantics. The interpreter diff
is EMPTY. No OR semantic case exists. The red team confirmed
generalization to three-element disjunctions and confirmed
minimality on the cover path. This is the closest current mechanism
to a general learning operation: composition, not selection.

Distance to the frontier: the covers are still composed of
researcher-supplied atom types, and the structural form is fixed
(DISP with labeled edges). The learner decides WHICH pre-shaped
atoms to union, not WHAT a representation is. The node vocabulary
is fixed; only the combination is authored. This passes a weak
C0-A (semantics of composition are generic) but fails C0-B (the
structural form is not open) and has not faced C0-C (no
adversary-designed representation families).

### 2c. Causal edit invention (bounded, narrowed, C65/C71)

The learner diagnosed a binding envelope parameter and authored
EXTEND-DELAY when the old vocabulary was provably insufficient.
This is the closest precedent for learner-authored semantics:
the learner created a new operation, not a new parameter value.
But C71 narrowed it: the max_rules arm was dead code, and the
diagnose-and-relax behavior is delay-specific (scope-collapse).
The learner authored an edit operation inside an edit vocabulary;
it did not author a representation semantics.

Distance to the frontier: authored operations on fixed structures
are one level below authored structures themselves.

### 2d. The frozen core: fragmented researcher slots (W9 predicted FAIL)

The freeze protocol's honest-scope section states the diagnosis
verbatim: the learner owns at least three independent encodings
(44-byte fact slots, 1152-byte DDES hypothesis entries, rule-store
keys). There is no generic structural substrate, only
researcher-defined slots to fill. W9 was predicted FAIL on this
basis before the run. The run confirmed it (0/28, 0/31), though
confounded by eviction per the pre-registered C1 clause.

### 2e. The eviction pathology is a representational poverty problem (C75)

C75 found that the 36-slot store cannot stably hold 6 sequential new
facts: evict_c breaks lowest-importance ties by lowest index, so
sequential teaches overwrite the same slot. Micah's new direction
is explicit: this must NOT become a cache-policy version treadmill.
The scout's reframing: the pathology is representational, not
scheduling. Importance is a researcher-defined scalar on a
researcher-defined slot. The learner cannot express "this structure
is a dependency scaffold for that hypothesis" or "these three facts
form one revisable unit" because the store has no edge vocabulary
the learner can author. Any fix that keeps flat triples plus a
smarter scalar is the treadmill. The general fix is one structural
workspace where dependencies are first-class, authored, executable
edges, and retention policy operates over that authored structure.
That is the same substrate as section 1, viewed from the memory
side: a generic executable representation substrate IS the memory
substrate if knowledge, dependencies, hypotheses, and structures
share one cell algebra.

## 3. Minimal general mechanism: sketch

What the frozen core must provide (protected, fixed, auditable):

- **Cells.** A fixed small set of cell kinds: value, reference,
  edge. Fixed at freeze; counted in the source audit. This is the
  cell algebra, not a representation menu. The audit criterion:
  no cell kind names a domain concept (no CAUSE cell, no PLAN
  cell, no WORD cell).
- **One workspace.** A single learner-owned structural region
  replacing the fragmented formats (fact slots, DDES entries,
  rule-store keys). One allocator, one address space. This is
  the stated continuing-learner priority and the direct answer
  to the W9 diagnosis.
- **A generic executor.** An interpreter that walks learner-authored
  graphs and acts. Dispatch is over cell kinds, never over
  domain semantics. The L3C v3 EMPTY-diff precedent is the bar:
  new capabilities must arrive with zero new semantic cases.
- **Citation.** A way for structures to name and reference other
  structures, so composition is possible. Without citation there
  is no reuse, and without reuse C0-D cannot be tested.

What the learner must author (all in persistent learner state):

- Node roles: which subgraphs mean what, established by use.
- Composition: how structures combine into larger structures.
- Revision: how structures are rewritten or retired when
  contradicted (the H-REVISE impossibility result and the C71
  scope-collapse both mark revision as the hard part; the
  substrate must make revision a first-class operation, not
  an afterthought).

What meaning is: operational. A learner-authored node acquires
semantics by its role in a graph that is executed and scored.
There is no separate grounding module; grounding is what happens
when an authored structure is used to predict, plan, or remember
and the outcome feeds back. This keeps the core small: the
researcher supplies execution, the world supplies consequences,
the learner supplies the structures in between.

## 4. Hard problems, honestly listed

1. **Bootstrapping without a menu.** What is the minimal fixed
   vocabulary that is not itself a menu? The fixed part must be
   cell algebra (allocate, link, cite, execute), never a
   representation catalog. The failure mode to watch: the cell
   kinds quietly becoming domain concepts (a LINK cell that is
   really a CAUSE cell). The source audit is the defense, and it
   must be adversarial, not self-administered.

2. **The oracle problem.** W9 demands white-box evidence of
   "genuinely new structural topology, not a shoehorn". The L3A
   red team (C77) showed what happens with a dishonest oracle: a
   hardcoded byte check made the verdict measure beam-byte
   reproduction instead of learning. Any substrate claim needs
   an honest, general structural oracle BEFORE the build, frozen
   in the prereg: what counts as new topology, stated as a
   graph property, not a byte pattern.

3. **Revision.** Authored structures must be revisable after
   counterexamples (Micah's criterion 12). The H-REVISE kill by
   impossibility proof and the C71 scope-collapse show that
   revision is where bounded mechanisms die. The substrate must
   give the learner a way to mark a structure wrong and rebuild
   it, with the old version retained as evidence (not silently
   overwritten; silent overwrite is how the eviction pathology
   destroys knowledge).

4. **Interference.** Structures must persist across worlds,
   compose, and transfer without researcher-supplied modularity.
   The freeze challenge's cross-world design (W1 through W9,
   persistent state) is the right test harness; a substrate
   that needs a reset per world is not a continuing learner.

5. **The treadmill test.** Every "generic" mechanism so far
   turned out bounded (menu, cover-set, edit-invent). The
   defense is C0-C: at least one evaluation family designed by
   an independent adversary AFTER the freeze. If the substrate
   only handles researcher-anticipated forms, it is a menu
   with better marketing.

## 5. Gap analysis: current mechanisms against the bars

| Mechanism | C0-A (semantics in learner state) | C0-B (open form) | C0-C (unforeseen forms) | C0-D (reuse) | W9 bar |
|---|---|---|---|---|---|
| L3B v2 menu | No: selection over fixed vocabulary | No: finite family | Not tested; predicted fail | Partial: versions reused, not structures | Fail |
| L3C v3 cover-set | Partial: composition generic, atoms fixed | No: fixed DISP form | Not tested | Partial: covers reused within task | Fail |
| Causal edit-invent | Partial: authored op, fixed vocabulary | No: edit ops only | Tested narrow; scope-collapsed | Not demonstrated | Fail |
| Frozen core slots | No: slots are researcher formats | No | No | No | Fail (predicted and observed) |
| Substrate (target) | Yes: roles authored in state | Yes: cell algebra, open topology | Required: post-freeze adversary family | Required: second-probe reuse | The test |

The gap is not incremental. No current mechanism is one tweak
away: each fails C0-B structurally, not parametrically. This is
why Micah's direction rejects per-world patches. The missing
piece is architectural: one learner-owned structural workspace
plus a generic executor, replacing fragmented slots.

## 6. Recommended research direction (falsifiable)

**Direction.** Build the minimal cell-algebra substrate under the
frozen-core philosophy, in this order:

1. Freeze the core first: fix the cell kinds, the allocator, the
   executor, and the structural oracle in a preregistered source
   audit. The audit criterion is explicit: no cell kind names a
   domain concept; the executor has zero domain semantic cases.
2. Sealed W9-class worlds: at least two representation families
   designed by an independent adversary AFTER the freeze,
   requiring materially different structural forms (for example
   hierarchical composition in one family, graph-structured
   dependencies in another).
3. Measure: task score at 80 percent or better AND white-box
   structural inspection showing new topology in persistent
   learner state AND reuse on a second probe AND transfer to
   the adversary's second family.
4. Independent red team with the explicit mandate to show the
   substrate is a menu in disguise.

**What would prove it wrong (kill conditions, frozen before build):**

- K-A: the learner succeeds only after the researcher adds a
  cell kind per world. The treadmill reappears; the substrate
  is a menu. Kill the claim.
- K-B: authored structures never transfer to the second probe
  or the adversary family. C0-D fails; the structures are
  storage, not representation. Kill the claim.
- K-C: the honest structural oracle cannot distinguish authored
  topology from slot-shoehorning. The measurement is void;
  the claim is UNVERIFIABLE, not surviving.
- K-D: revision of an authored structure after a counterexample
  requires researcher intervention. Criterion 12 fails;
  the substrate is write-once. Kill the claim.

**Explicitly rejected:** per-world node kinds, dedicated semantic
branches, eviction-policy version treadmills, new modes or
bridges around the workspace. Capability-source delta must stay
near zero: the only source change permitted is the fixed cell
algebra and executor, audited once.

**Sequencing note.** The eviction/memory question Micah posed
("what general learner-owned memory representation/policy would
let one frozen learner preserve newly useful knowledge,
dependencies, hypotheses and structures without task-specific
storage logic?") is answered by the same substrate: retention
policy operates over authored dependency structure, not over
researcher scalars. Do not run a separate cache-policy lane;
fold retention into the substrate prereg as a required property
(the oracle must verify dependency edges, and a pressure test
must show structured retention beating flat eviction on a
sealed world).

## 7. Verdict

SUBSTRATE-SCOUT-COMPLETE. The frontier is farther than a
single mechanism: it requires replacing the fragmented state
formats with one learner-owned structural workspace plus a
generic executor, under a frozen honest oracle and post-freeze
adversary families. The gap table shows no current mechanism
is close on C0-B. The recommended direction is falsifiable
with four frozen kill conditions. The eviction pathology is
best understood as the same frontier viewed from the memory
side, and should be folded into the substrate program, not
run as a separate policy treadmill.

## Kill-bar self-check

- K1: PASS. The survey covers L3B v2 (menu), L3C v3 (cover-set),
  causal edit invention, the frozen core's fragmented formats,
  the eviction pathology, and the frontier definition with
  C0-A through C0-D and the W9 bars.
- K2: PASS. Section 6 states four frozen kill conditions (K-A
  through K-D) that would prove the recommended direction
  wrong. Each is observable before any capability claim.
- K3: PASS. Pure markdown, no Python at any step, dash-clean
  per the shell-only check (run at commit time), contaminated
  paper untouched.

## One-System Rule accounting

- Cognition source lines added: 0 (scouting only).
- New hardcoded semantic cases: 0.
- New modes: 0.
- New bridges: 0.
- New task-specific handlers: 0.
- Learner-state structures created: 0.
