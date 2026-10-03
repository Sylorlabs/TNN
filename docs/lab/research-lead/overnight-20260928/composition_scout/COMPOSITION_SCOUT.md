# Compositional Machinery Scout: Cluster C

Date: 2026-09-30. Worker: Compositional Machinery Scout (Cluster C).
Verdict label target: COMPOSITION-SCOUT-COMPLETE.
Status: scout only. No implementation proposed or written.

Sources: Cluster analysis (`freeze_cluster/CLUSTER_ANALYSIS.md`, commit
`905586a3b`); W2/W3 shared-cause analysis (`w2w3_analysis/W2W3_ANALYSIS.md`,
commit `2121fd16d`); frozen source
(`core_freeze/stage0/world_learn.zag`, freeze `87ac95d08`); interface
contract (`core_freeze/stage0/INTERFACE.md`); original W1/W8/W9 world
designs and battery outputs (`core_freeze/run_phase/battery/`); compose_ops
spec (`compose_ops/COMPOSE_OPS_SPEC.md`); unified structures
(`unified_structures/UNIFIED_STRUCTURES.md`); CAM-1 prereg
(`construct_apply/PREREG_CAM1.md`); CLA-2 prereg
(`continuing_learner/PREREG_CLA2.md`, G3 names this work as future work).

No sealed FW1-FW9 files were accessed. All world references are to the
original W1-W9 battery.

## 1. The three manifestations, characterized precisely

### 1a. W1 two-hop relation chaining

Battery evidence: `W1.out` shows `ANSWER 7005 599 -2` and
`ANSWER 7010 599 -2`. World file lines 15-18 teach:

- `(7005,501,7006)`, `(7006,502,21)`
- `(7010,501,7011)`, `(7011,501,22)`

Probes: `QUERY 7005 599 21`, `QUERY 7010 599 22`. Relation 599 is never
taught.

**Sharp finding:** 599 has no consistent meaning across the two probes.
Probe 1 needs 501-then-502. Probe 2 needs 501-then-501. No single
persistent rule of the form "599 = r_a composed with r_b" can cover
both. Any learner that commits to one meaning of 599 after probe 1
fails probe 2. The only general solution is **per-query compositional
search**: on miss, enumerate 2-chains from the subject and find the
one that terminates at a verifiable value.

Execution need: fixed 2-step join (one join variable, depth exactly 2).
Discovery need: search over relation pairs at query time. No persistent
induced structure is required. No regularity detection across examples
is required.

### 1b. W8 novel word composition

Design evidence (`DESIGN_WORLDS_PREFREEZE.md`, W8 section): five training
utterances teach tokens via relations 701 (verb), 702 (object), 703
(modifier); relation 704 carries the meaning code and **is** taught as a
relation. Five novel utterances present unseen token combinations;
probes ask `QUERY (utterance, 704, expected)`.

The combining regularity `m = 100*v + 10*o + d` must be induced from
the five training examples. That induction is Cluster B work
(regularity detection, reification of a combining function). What is
Cluster C is the **assembly**: given a novel utterance, gather v from
`(U,701)`, o from `(U,702)`, d from `(U,703)`, and feed the triple to
the combining function.

Execution need: fixed 3-gather on one subject plus function application.
Discovery need: split. The combining function is induced (B). The
assembly plan is generic once the function exists (C).

W8-novel is therefore a **B+C bridge case**: neither cluster alone
suffices, and each cluster's contribution is crisply separable.

### 1c. W9 graph traversal

Design evidence (`DESIGN_WORLDS_ADVERSARY.md`, section 4): 14 parent
edges per tree taught via relation 21001. Probes use relations 21007
(depth) and 21009 (grandparent), neither taught nor exemplified.

- Grandparent: `21009 = 21001 composed with 21001`. Same execution
  shape as W1's 2-hop, but with **consistent** semantics across probes.
- Depth: iterate 21001 until a node with no parent (lookup returns the
  -2 sentinel), counting steps. Unbounded depth, needs a loop with a
  termination predicate and a counter.

Execution need: fixed 2-chain (grandparent) plus unbounded iteration
with termination and counting (depth). Discovery need: hypothesizing
iteration itself as a meaningful query plan. No exemplars of iteration
exist in the taught edges. This is the hardest discovery problem of
the three.

## 2. One mechanism or three?

**One execution mechanism, three discovery problems.**

The execution core shared by all three is **multi-fact query answering
through a plan**: given a plan (a sequence of lookups and combinations),
execute it against the fact store.

- 2-hop: plan = LINK-READ, LINK-READ, EMIT.
- 3-gather: plan = LINK-READ x3, then APPLY combining structure.
- Traversal: plan = loop { LINK-READ, COMPARE, BRANCH } plus counter.

All three plans are expressible in the unified_structures EXECUTE
vocabulary (COPY, BIND, COMPARE, BRANCH, EMIT, LINK-READ, plus the step
budget for termination). See section 4 for the one noted gap (counting).

The discovery problems differ and cross the cluster boundary:

| Case | Discovery | Cluster |
|---|---|---|
| W1 two-hop | query-time search over relation pairs | C (pure) |
| W8 combining function | induction from 5 examples | B |
| W8 assembly | generic gather plan | C |
| W9 grandparent | consistent 2-chain hypothesis | C (pure) |
| W9 depth | hypothesizing iteration as an operation | B-adjacent |

**Resolution of a tension in the record.** The W2/W3 analysis calls
W1's probes "the mildest member of the construct-and-apply cluster."
Mechanistically this is imprecise. W1's probes need no persistent
induced structure and no regularity detection: per-query plan execution
suffices, and the inconsistent semantics of 599 across probes actively
punish committing to a learned meaning. They belong in Cluster C.
The shared symptom is real (anything beyond exact-key lookup fails),
but the missing machinery differs: B needs persistent construction,
C needs query-time combination. A system could compose without
inducing (fixed plan templates over learned facts) or induce without
composing (single-step rules applied by exact lookup). **Recommendation:
keep clusters B and C separate.** W8-novel is the documented bridge
case where both are needed; W9-depth sits at the boundary (the
iteration *plan* must be constructed, B-like; its *execution* is pure C).

## 3. Survey: does any existing TNN mechanism compose structures?

**Frozen core** (`world_learn.zag`, freeze `87ac95d08`): `find_key` is
called only for single exact-key lookups (learn at line 73, query at
line 114). The `twohop` function (lines 125-140) performs two
*independent* lookups for a diagnostic sign comparison; it does not
chain. `query()` (lines 111-122) reads the `expected` argument only for
importance bookkeeping (correct/wrong counters at lines 117-119);
`expected` never influences retrieval. **No composition machinery
exists in the frozen core.** The 1/9 result is consistent with this.

**compose_ops APPLY** (`COMPOSE_OPS_SPEC.md`, section 2.2, op 8):
traverses a structure, fills HOLE slots from bindings, executes
primitive op nodes per the frozen basis, returns a value or clean
failure. This is a plan executor for **persistent induced structures**,
which is Cluster B's application half. Cluster C needs the same
execution shape applied to **query-time constructed plans** rather than
persistent structures. The executor is not the gap; the **plan
constructor** is.

**unified_structures EXECUTE** (section 2): fixed domain-neutral op set
(COPY, BIND, COMPARE, BRANCH, EMIT, LINK-READ), opaque values, step
budget for termination. This vocabulary covers every execution need in
section 1: 2-hop chains, 3-gathers, and bounded loops with sentinel
termination (the -2 not-found sentinel already exists as cognitive
semantics per INTERFACE.md). **No new core execution ops are needed
for the execution half.** One noted awkwardness: depth counting needs
a counter, and EXECUTE has no arithmetic; the learner must build
successor structure from cells (the spec explicitly assigns this to the
learner). Honest but clunky; flagged as a possible minimal extension
point in section 6, not decided here.

**CAM-1** (`construct_apply/PREREG_CAM1.md`, lines 243-245, 311-313):
explicitly scopes out Cluster C ("composition is Cluster C, out of
scope"). No overlap and no conflict.

**CLA-1 ACTIVATE**: spreading retrieval over links. Supplies candidate
facts for plan construction but executes no plan.

**CLA-2 G3** (`PREREG_CLA2.md`): names "hierarchical/graph-native
traversal" as future work, noting "nodes plus typed links express
hierarchy; traversal and compositional query machinery is future work."
This scout is the specification input to that gap. Nothing in CLA-2
yet constructs or executes query plans.

**Summary of the survey:** the execution vocabulary exists twice in
spec form (APPLY, EXECUTE) and zero times in implementation. No
existing mechanism constructs a compositional query plan. No existing
mechanism executes multi-fact queries. Cluster C is the least explored
of the four clusters, as expected.

## 4. The gap: a general composition operation in the CLA-2 workspace

The gap has two halves. The execution half is solved in spec
(EXECUTE/APPLY vocabulary suffices). The missing half is the
**composition policy**: on query miss with an untaught relation, what
builds the plan, and what verifies it?

Candidate plan templates (frozen, generic, domain-neutral; the prereg
author may revise this list, but any revision must carry the same
generality argument):

- **CHAIN-2**: two-hop join over a relation pair. Covers W1 probes and
  W9 grandparent.
- **GATHER-n**: multi-slot assembly on one subject, feeding a combining
  structure. Covers W8 assembly (n=3).
- **ITERATE-UNTIL**: loop of single-relation steps with a termination
  predicate (lookup miss / sentinel) and a step counter. Covers W9
  depth.

The trigger is the query-miss path (the -2 path), same architectural
location as the compose_ops bootstrap (section 4 of that spec). The
open design questions are in section 6.

### The expected-value question

The interface passes `expected` to `query()`; the frozen code already
reads it (for bookkeeping only). A compositional miss-policy could use
it as a **verification oracle** for candidate plans: execute plan,
compare result to expected, keep the plan that matches.

This must be an explicit prereg ruling, because it determines what the
test measures:

- With e-verification: the battery measures query-time compositional
  search (try plans, keep what verifies).
- Without e-verification: the probe relations 599, 21007, 21009 may be
  undiscoverable in principle (no exemplars, no consistent semantics
  for 599), and the battery measures the learner's compositional
  priors rather than its machinery.

Neither ruling is obviously correct. The scout's position: preregister
the ruling, then run the **e-ablation** (section 5, F2). If e-access is
load-bearing, the capability is answer-key search and the claim is
downgraded accordingly. Suppressing the question would be worse than
either answer.

### World-design observation (original battery only)

Because 599 means 501-then-502 in probe 1 and 501-then-501 in probe 2,
W1's probes test per-query search, not learned composition. A future
composition world that aims to test *retained* compositional readings
should give its probe relations consistent compositional semantics
across probes. (No sealed FW1-FW9 files were accessed; this observation
concerns W1 only and is offered to world designers, not used as a
design hint for substrate builders.)

## 5. Falsifiable prereg specification (the next step after this scout)

A future composition prereg should specify: query-time plan
construction plus execution over the EXECUTE vocabulary, in the CLA-2
workspace, firing on the query-miss path, with the e-ruling stated
up front.

**Predictions:**

- **P1**: W1 goes 12/12. The two two-hop probes return chained values
  via per-query CHAIN-2 search. (Pure C; no B dependency.)
- **P2**: W8 recall stays 4/4. Novel moves 0/5 toward 4/5
  **conditional** on the combining function being present as a learner
  structure. The composition prereg covers assembly only; the test
  either supplies the induced function or measures assembly in
  isolation. The Cluster B dependency is stated, not hidden.
- **P3**: W9 grandparent probes resolve via CHAIN-2; depth probes
  resolve via ITERATE-UNTIL, **conditional** on edge stability
  (Cluster A dependency: C75 must not evict the edges mid-world) and on
  the iteration plan being constructible (discovery dependency stated).
- **P4 (generality)**: a held-out compositional form not in the
  template list (e.g. a 3-hop chain) is solved with no new template,
  or the claim bounds itself honestly to fixed-depth plans.
- **P5 (separation)**: W2/W3 scores are unchanged by the composition
  change alone. This proves C does not collapse into B: plan execution
  without induction does not induce.

**Falsification conditions:**

- **F1**: W1 solved but W9 traversal not. The "one mechanism" claim
  narrows to fixed-depth plans; ITERATE-UNTIL is a separate
  mechanism, and the clusters re-divide.
- **F2 (the e-ablation)**: with e-access removed, composition fails.
  Then the capability is answer-key search, not compositional
  understanding; the claim is downgraded and the battery is redesigned
  with consistent probe-relation semantics.
- **F3**: each new world needs a new plan template. That is a template
  treadmill, not a general mechanism; the prereg is rejected.
- **F4**: composition machinery alone (no induction) solves W8-novel.
  Then the B/C boundary drawn in section 2 is wrong and the clusters
  merge.
- **F5**: the plan-constructor template list grows past the
  preregistered set without a generality argument. That is oracle
  creep; the implementation fails review.

**One-System Rule accounting for the prereg (projected):** the
execution vocabulary already exists in spec (EXECUTE); the prereg adds
only the miss-time plan policy. Projected: 0 new semantic cases, 0 new
modes, 0 new bridges, 0 task-specific handlers. Learner-state
structures created: plan nodes and plan-execution traces in the
workspace. Cognition source lines: bounded by the policy
implementation; the prereg must state the bound and the generality
argument that keeps it from growing per world (F3/F5 enforce this).

## 6. Open questions for the prereg author (not decided here)

- **Q1 (the e-ruling)**: may the miss-policy read the query's
  expected value for plan verification? See section 4. This is the
  single most consequential prereg decision.
- **Q2 (template load-bearing)**: are CHAIN-2, GATHER-n,
  ITERATE-UNTIL researcher-fixed vocabulary in the same suspicious
  sense as LORG's fixed weight subset (Micah's Q1 ruling on LORG)?
  The prereg must test whether the template set is load-bearing and
  move plan-shape selection into learner state where possible.
- **Q3 (policy location)**: does plan construction live in a frozen
  generic core miss-policy or in learner-owned structures? The
  learner-owned direction is preferred per the One-System Rule; a
  frozen bootstrap is acceptable only if replaceable by
  learner-built policy over time (the compose_ops section 4 pattern).
- **Q4 (counting)**: W9 depth needs a counter and EXECUTE's core op
  set has no arithmetic. Options: learner-built successor chains
  (honest, clunky), or one minimal SUCC op (risks basis creep toward
  the arithmetic treadmill). Flagged, not decided; the prereg author
  must argue it explicitly.

## 7. Relation to the other clusters (no double work)

- **Cluster A**: P3 depends on edge stability. Composition tests are
  confounded until retention is fixed; the prereg should state the
  dependency and test composition on a stable store first.
- **Cluster B**: P2 and P5 draw the boundary. The compose-verify-promote
  frontier (ruling G) builds persistent structures; composition
  executes query-time plans. W8-novel needs both; the prereg must not
  claim B's work as C's results.
- **Cluster D**: independent. Plan execution does not select actions;
  the learner-state ACT hypothesis is orthogonal.

## 8. Verdict

**COMPOSITION-SCOUT-COMPLETE.** The three manifestations are one
execution mechanism (query-time plan construction and execution over
the existing EXECUTE vocabulary) with three distinct discovery
problems (search, induction-plus-assembly, operation hypothesis).
No existing mechanism constructs or executes compositional query
plans; the executor exists in spec, the plan constructor does not.
Section 5 specifies the falsifiable prereg that is the next step.
Section 6 lists the four open questions the prereg author must decide.
Zero source lines added by this scout; zero modes, bridges, handlers,
or semantic cases.
