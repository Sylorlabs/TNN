# TNN-2 Alternative-Explanation Attack

Date: 2026-09-30 (PDT). Pipeline step 6: alternative-explanation attack.
Target: TNN-2 at frozen build `f4de7ff46` (read-only analysis of the three
red-team reports `340e94e3e`, `4e329c772`, `687ba0219`).

Method: for each claimed mechanism, formulate the SIMPLEST account that
predicts every observed behavior, including the red-team kills and the
parts the red teams acknowledged as genuine. Then push each account
simpler, then propose one unified account covering all three.

Style note: no claim here is a verdict on TNN-2. This step exists to make
the simple accounts explicit so the next generation must beat them.

---

## 1. Runtime executable-graph construction (Change 1)

### Simplest account

Construction is **parameterized retrieval from a fixed template library,
keyed by an environment-supplied answer**.

Concretely: `t2_trial` instantiates three researcher-written linear graph
assemblers (two reachable in production; the sum branch is test-gated by
a type-8 marker no cognitive path can create) in a fixed order
(chains k=2..4, counts, single hops last), filling data-derived literals
and wirings into fixed slots, and keeps the first candidate whose
executed output equals the `expected` value handed to it in the QUERY
event. The trial loop is a lookup loop: it does not discover an answer,
it searches the researcher's finite family for the first member that
reproduces an answer it was given.

### This account predicts every red-team finding

- Finite candidate grammar (3 linear families, no branching, no nesting,
  no subroutine reuse, DEC never emitted): predicted, because the
  templates are fixed in source.
- Hard bounds (depth 4, 96 paths, 12 values, 16 count links): predicted,
  because the bounds are literals in the researcher's code.
- Fixed search order: predicted, because the order is a hardcoded
  comment-marked "composition-preserving" sequence.
- Sum branch dead in production: predicted, because the type-8 gate is a
  researcher constant no cognitive path can satisfy.
- 5-hop query correctly refused: predicted, because the family has no
  member of that shape; refusal is not failed discovery, it is
  unrepresentability.
- The genuine parts (persistent promoted graph with provenance DEP
  edges, genuine rejections of failed guards, runtime composition of
  parts, T2-CHAIN4 exceeding the old 3-template ceiling): predicted,
  because "retrieval with parameters" still creates new persistent
  nodes, still evaluates guards honestly, and still fills slots at
  runtime. The new ceiling (4 hops) being equally hard is exactly what
  a larger finite menu predicts.

### What would falsify this account

Any ONE of these, observed without source change:

1. A promoted graph outside the three linear forms (branching, nesting,
   loops, DEC emitted, subroutine reuse of a previously promoted
   graph).
2. A construction bound that moves with learner state (e.g., a budget
   the learner manages) rather than a source literal.
3. Verification against world feedback on the query path rather than
   the environment-supplied `expected`.
4. Construction succeeding in a fresh world on a structure class that
   is not enumerable from the source plus the fact set.

### Is there a simpler account?

"**Lookup by observed facts.**" The learner's construction degrees of
freedom are: which BFS paths exist, which literals appear, which
candidate verifies first in a fixed order. All of these are
deterministic functions of the fact set plus researcher code. Nothing
the learner contributes is structural. The mechanism can be
re-described as: index into (fixed family x observed facts), return the
first member matching the given answer. That is the minimal
description. It is not construction; it is selection.

---

## 2. Learner-originated uncertainty to guide to action (Change 2)

### Simplest account

Inquiry is **a sticky miss flag wired to a constant output action**.

Concretely: on a genuine miss (retrieval, construction, and bootstrap
all fail honestly from empty state), the learner allocates a persistent
uncertainty node tagged 30 with the miss's subject/relation in its
slots, allocates a guide node with a researcher-constant action value
(30) and constant content (-999), and links both into POLICY_ROOT. ACT's
selection machinery is real code over learner state, but in every
exercised scenario exactly one guide exists, so selection is trivial.
No production path ever resolves an uncertainty or supersedes a guide,
so flags and guides persist forever and stay ACT-eligible.

### This account predicts every red-team finding

- L1 (miss trigger) and L2 (uncertainty creation) learner-originated
  PASS: predicted, because the flag allocation is genuinely on the miss
  path with miss-derived content in slots 20/24.
- L3 hardcoded (30/-999): predicted, because the "discriminating need"
  is two constants, not a computation over what would discriminate.
- L4 (POLICY_ROOT linkage) PASS: predicted, because the wiring into
  POLICY_ROOT is real persistent-state code.
- L5 (ACT machinery) real but trivially satisfied: predicted, because
  the machinery is general while its coverage is one candidate.
- L6 absent: predicted, because nothing in the source creates a
  resolution transition or a supersession edge on guides.
- Ambiguous evidence yields arbitrary selection: predicted, because
  two content-identical guides differ only in slot4 and bid ties break
  by edge order; there is no informativeness basis.
- Misleading evidence locks in: predicted, because the guide revision
  path does not exist.
- Empty-state creation and clean scaffolding audit: predicted, because
  the flag creation is genuinely on the production path with no test
  pre-population.

### What would falsify this account

Any ONE of these, observed without source change:

1. A guide whose action value or content varies with the uncertainty
   (two different misses producing two different derived actions).
2. An uncertainty node that is resolved, removed, or marked superseded
   when the missing fact is later learned, with stale guides becoming
   ACT-ineligible.
3. ACT preferring the more informative inquiry under ambiguity, on a
   basis computed by the learner (not tie-breaking by edge order).
4. A guide revised or retired after contradictory evidence, via a
   production path.

### Is there a simpler account?

"**A miss alarm with a fixed output wire.**" The learner decides WHEN
to ring the alarm (genuinely, from the miss path). The researcher
decided WHAT the alarm sounds like (always 30), and there is no way to
turn the alarm off. The entire inquiry mechanism is: detect miss,
create flag, output constant. Everything beyond that (ACT bid
machinery, context matching, supersession) is real machinery with
nothing learner-derived to operate on. That is the minimal description.

---

## 3. Counterexample-driven executable-graph revision (Change 3)

### Simplest account

Revision is **a researcher-written patch script with runtime-filled
operands: find the SETREG via provenance, tombstone it, insert the
observed literal as a new SETREG, rewire the guard**.

Concretely: `t2_revise_graph` executes exactly one repair schema with no
branches over alternatives. The learner's contribution is operand
selection: which cell (by provenance lookup, last-match-wins on ties)
and which value (the just-observed literal `new_o`). The researcher
contributed: always SETREG, always tombstone, always guard->new->succ
rewiring, never touching the guard predicate, never inserting without
deleting, never rerouting to an existing step, never loop manipulation,
never multi-step repair. `t2_trial` (the genuine search machinery) is
never invoked by the revision path. The T2-REVISE test demonstrates the
single anticipated repair: the revised graph does not compute 999, it
stores 999.

### This account predicts every red-team finding

- Exactly one repair topology (guard->new-SETREG(literal)->succ, old
  SETREG tombstoned): predicted, because it is the only code path.
- Cannot revise INC/DEC/BRANCHEQ steps, cannot change the guard
  condition, cannot insert without deleting, cannot reroute to an
  existing step, cannot do loop/sequence conversion, one step per
  event: predicted, because each is the absence of a code path.
- Learner chooses operands, researcher chose procedure: predicted,
  because the variable parts (cell index, literal) are lookups and the
  fixed parts (cell type, rewire shape, tombstone) are constants in the
  operator.
- Genuine topology edit, revert-on-failure, standing untouched, test
  passing: predicted, because a fixed procedure can still be a real
  procedure; "real" and "researcher-authored" are orthogonal.
- C0-A/B/C fail, C0-D unestablished: predicted, because the repair
  semantics live in source (A), the output topology is the only one the
  code can produce (B), any other required repair shape gets return 0
  (C), and continued functioning after memorization is not reuse (D).

### What would falsify this account

Any ONE of these, observed without source change:

1. Two structurally different repairs produced by the same operator
   (e.g., a guard-predicate change AND a literal swap).
2. The revision path invoking the trial/search machinery over a repair
   space with more than one member.
3. The corrected content being derived (computed, searched, selected
   among alternatives) rather than the observed literal.
4. A sealed-world counterexample repaired in a shape the researcher did
   not pre-shape (e.g., repair by rerouting to an existing step).
5. A second step revised in coordination with the first in one event.

### Is there a simpler account?

"**Overwrite the stored constant with the new stored constant.**" At
the semantic level, the revision does not restructure a computation; it
replaces one memorized literal behind an unchanged guard shape with a
newer memorized literal. The red team calls this L0 storage dressed as
revision, and the minimal description agrees: the graph edit is real,
but what changed semantically is which constant is stored. The
"revision" is a store operation with a tombstone. That is the minimal
description.

---

## 4. The unified hypothesis

### Claim

One account covers all three mechanisms:

> **FORM comes from the researcher; CONTENT comes from the learner.
> All three mechanisms fill runtime values (literals, cell indices,
> node IDs, fact pointers) into fixed researcher-authored structures.
> The learner never invents a form.**

Mapping:

| Mechanism | Fixed form (researcher) | Filled content (learner) |
|---|---|---|
| Construction | 3 linear assemblers, fixed search order, hard bounds, slot layout, verifier semantics | literals, paths, subsets from observed facts; which candidate verifies first |
| Inquiry | constant action 30, constant content -999, guide node shape, POLICY_ROOT linkage pattern | which (s,r) missed; when the flag is created |
| Revision | single repair schema: find SETREG, tombstone, insert literal SETREG, rewire guard->new->succ | which cell (provenance lookup), which literal (observed value) |

A second, equivalent statement of the same hypothesis: **TNN-2 is
answer-fed, not answer-derived.** Every mechanism receives its answer
from the environment and routes it into a researcher-shaped structure,
never computing an unknown:

- Construction receives `expected` from the QUERY event and searches
  for the first template instantiation matching it.
- Inquiry receives no question to derive; its action is the constant
  30 regardless of what is unknown.
- Revision receives `new_o` from the contradicting observation and
  stores it.

The learner's total degrees of freedom across all three mechanisms can
be compressed to: **indices and literals**. Which fact, which literal,
which cell, which node ID. Never a topology, never a procedure, never
a question.

### The unified account predicts the genuine parts too

The red teams each found genuine machinery. The unified hypothesis
predicts it, because content-layer activity is real:

- Persistent promoted graphs with provenance DEP edges: content
  (new nodes) is learner-created; only the form was fixed.
- Genuine guard rejections during trial: evaluating a fixed form
  honestly is still honest evaluation.
- Real ACT machinery (bid, context, supersession): a real selector
  with learner-derived candidates missing; trivially satisfied.
- Real topology edits with revert-on-failure: a fixed procedure is
  still a procedure.
- Empty-state creation with no scaffolding: the content layer is
  genuinely learner-driven.

Nothing in the red-team evidence requires attributing FORM to the
learner. The simplest account that explains everything attributes all
form to the researcher and all content to the learner. By Occam's
razor, the learner is a **retrieval and routing system with
researcher-shaped slots**, not a structure inventor.

### Falsification of the unified hypothesis

The unified hypothesis is falsified by ANY of the per-mechanism
falsifiers in sections 1-3. Concretely, the cheapest decisive
observation would be one instance, without source change, of the
learner producing a FORM: a graph topology outside the researcher
family, a guide action varying with the uncertainty, or a repair
schema with more than one member. One such instance breaks the
"indices and literals only" bound and forces a more complex account.

### Is there an even simpler unified account?

Candidate: "TNN-2 is a lookup table with learner-managed keys." The
learner creates persistent nodes (keys: uncertainty nodes, promoted
graphs, revised cells); researcher code defines how those keys are
consumed (constant action, fixed search order, single patch schema).
This is simpler in words but equivalent in content to the
form/content split, so the form/content statement is kept as the
canonical form: it names exactly which half of each mechanism is
researcher-authored, which is what the next generation must change.

A strictly weaker (and therefore not better) candidate: "TNN-2 is
retrieval only." This is rejected as TOO simple: it fails to predict
the runtime composition of parts in construction (T2-CHAIN4 genuinely
exceeds the old template ceiling) and the real topology edits in
revision. The unified hypothesis must be at least as complex as
"fixed forms, runtime content," and no more complex.

---

## 5. What the next generation must beat (falsification checklist)

For TNN-3 or any successor mechanism, the simple accounts above are
defeated only by observations the red teams specified. Consolidated
minimum bar:

1. A learner-created executable graph whose topology is not enumerable
   from the source plus the fact set (breaks the construction account).
2. A guide whose action/content is computed from the uncertainty and
   varies across uncertainties (breaks the inquiry account).
3. An uncertainty that is resolved or a guide that is superseded on
   learning, via a production path (breaks the sticky-flag account).
4. A revision whose repair topology is selected among genuine
   alternatives, or a repair shape outside the single schema (breaks
   the literal-patch account).
5. Any form bound (depth, constant action, schema) violated by learner
   state rather than source edit (breaks the unified account).

Until such an observation, the standing simple hypothesis is:
researcher forms, learner content, answers supplied by the environment.

---

## Verdict

**ALTERNATIVE-EXPLANATION-ATTACK-COMPLETE.**

Simplest accounts formulated for all three mechanisms; each predicts
all red-team findings including the genuine parts; per-mechanism and
unified falsification criteria stated; the unified hypothesis
("form from researcher, content from learner; learner degrees of
freedom are indices and literals") covers all three with no extra
machinery. This step does not promote or demote TNN-2.
