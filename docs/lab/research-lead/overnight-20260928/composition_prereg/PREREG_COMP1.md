# PREREG: Compositional Machinery (COMP-1)

Date: 2026-09-30. Worker: Composition Prereg Author.
Status: PREREG-FROZEN (design only; no implementation in this commit).
Lane: Cluster C compositional machinery, per the cluster analysis
(905586a3b) and the composition scout (cd7a3dd28).
Verdict label target: COMPOSITION-PREREG-COMPLETE.

## Step 0 Name-Check

Recorded in NAMECHECK.md before any design work: toolchain guard
check executed (`which python3 python`), `/usr/bin/python3` exists
but is never invoked; strict non-use documented. Pure markdown
authorship; no code written; no interpreter used for any purpose.
No em dashes (shell byte grep). Contaminated paper verified
zero-diff. Sealed FW1-FW9 files never accessed. Prereg committed
alone before any implementation. Local only, owned path, explicit
pathspecs.

## The standing question

> Why can the existing general architecture not learn this behavior?

The composition scout (cd7a3dd28) gives the precise answer: the
frozen core implements one retrieval operation, exact-key lookup
over stored triples (`find_key` is called only for single lookups;
the `twohop` diagnostic performs two independent lookups, never a
chain). No existing mechanism constructs a compositional query plan
and no existing mechanism executes a multi-fact query. The
EXECUTE/APPLY execution vocabulary exists twice in spec form and
zero times in implementation. The gap is the plan CONSTRUCTOR, not
the executor.

## Frozen inputs and rulings

This prereg is built on, and constrained by:

- Composition scout (cd7a3dd28): three manifestations
  characterized; one execution mechanism, three discovery
  problems; falsifiable prereg specified (P1-P5, F1-F5);
  four open questions Q1-Q4, all decided here.
- ISA boundary ruling (0525377f3): the protected core may
  contain a SMALL, FROZEN, domain-neutral computational basis
  (ALLOC, READ, WRITE, LINK, COPY, COMPARE/EQ, ADD, BRANCH,
  APPLY/EXECUTE, generic registers). Frozen rule: no core
  operation may encode a target-domain regularity detector.
  Finite-difference analysis is OUT of core intelligence;
  trial/compositional discovery with learner-created
  structures is IN. Do not grow the arithmetic basis one
  benchmark at a time.
- Integration package A1-A12 (62e5ebb9f, approved with the
  ISA boundary added): MISS_POLICY register is the dispatch
  point for the query-miss path; POLICY_ROOT for action;
  zero modes/bridges/handlers.
- EXECUTE placement (1fc77503b): seventh primitive justified
  as `EXECUTE(root, frame)` over a minimal ISA; APPLY is
  EXECUTE's calling convention. This prereg uses the EXECUTE
  vocabulary and adds zero execution ops.
- CAM-1 prereg (68a41be8a): explicitly scopes out Cluster C.
  No overlap. The verified-plan handoff below respects the
  boundary.

## The mechanism: COMP-1

COMP-1 is a query-time plan construction and execution
mechanism. It fires on the query-miss path (the -2 path) via
the MISS_POLICY register dispatch. One mechanism covers all
three scout manifestations; the split bar is frozen in F1.

### COMP-1.1 Trigger

A QUERY arrives for a (subject, relation) pair with no exact-key
match. The CLA-2 event loop's miss rule consults MISS_POLICY.
The composition bootstrap policy fires when: the relation is
untaught (no taught triples carry it) and the subject has at
least one incident taught relation. If the subject has no
incident relations, the policy declines (nothing to compose
from) and the standard miss handling continues.

### COMP-1.2 Candidate construction (the plan constructor)

Candidate plans are built from two frozen inputs only:

(a) The plan template set, frozen at exactly three templates
    (generality argument in section "Q2 resolution"):

    - CHAIN-2: two-hop join over an ordered relation pair.
      Plan shape: LINK-READ r1 from subject, LINK-READ r2
      from the intermediate, EMIT the terminal value.
    - GATHER-n: multi-slot assembly on one subject. Plan
      shape: LINK-READ r_1 .. r_n from the subject, then
      APPLY a combining structure to the gathered values.
    - ITERATE-UNTIL: loop of single-relation steps with a
      termination predicate and a step counter. Plan shape:
      loop { LINK-READ r; BRANCH on the -2 sentinel;
      INC counter }.

(b) The subject-incident relations: relations with taught
    triples on the query subject, read from the workspace.
    This is the structural bound on the candidate space
    (anti-spoof: no blind enumeration over relation ids).

Instantiation:

- CHAIN-2: for each ordered pair (r1, r2) of distinct
  incident relations, one candidate plan.
- GATHER-n: one candidate plan per n-subset of incident
  relations, for n from 2 up to the incident count. Fires
  only when a combining structure is present in the
  workspace (see "Cluster B boundary"); otherwise the
  template declines for lack of a combining function.
- ITERATE-UNTIL: for each incident relation r, one
  candidate plan.

All plans are learner-inspectable workspace structures built
from the EXECUTE vocabulary. No plan is executed yet.

### COMP-1.3 Execution

Each candidate plan is executed via the EXECUTE vocabulary
against the fact store, with the frozen step budget bounding
every run. Execution produces either a value or a clean
failure (sentinel, budget exhaustion, unbound slot). The
execution trace is retained in the workspace as a
plan-execution record.

Zero new core execution ops are used or needed. This is a
frozen claim of the prereg, enforced by F7.

### COMP-1.4 Verification (the E-ruling applies here)

**E-RULING (frozen):** The composition miss-policy MAY read
the query's `expected` value, but ONLY as post-hoc feedback
on an already-constructed candidate plan
(construct-then-verify). It may NOT use expected to generate
plans: no working backward from the answer to the plan, no
plan-shape selection conditioned on expected. The candidate
plan space must be fully determined by the templates and the
subject-incident relations before expected is consulted.

Rationale: this mirrors CAM-1's VERIFY step (construct, then
check against experience) and feedback-driven learning
generally. The interface already passes expected to query();
using it as post-hoc feedback does not encode a
target-domain regularity detector. What would violate the
ISA boundary is a core operation like FIND_CHAIN_TO_EXPECTED;
construct-then-verify is not that.

The e-ablation (F2) is mandatory and load-bearing: with
expected masked, the mechanism must still construct and
execute the same candidate plans, selecting by a non-e rule
(first non-sentinel result under the fixed template order).
If masking expected eliminates plan construction itself,
the capability was answer-key search.

### COMP-1.5 Promotion (the Cluster B boundary)

A candidate plan that verifies may be persisted to the
workspace as a PLAN node per the unified_structures
conventions (type tag, ref edges to the template and the
instantiated relations, SUPPORTS edge to the verifying
query). Repeated verification of the same plan shape is
visible in the workspace as evidence accumulation.

Persistent induction FROM repeated verification (turning a
verified plan into a standing reusable procedure without
further queries) is Cluster B's domain (CAM-1 territory),
not claimed here. This prereg claims query-time
construction, execution, and optional persistence of the
plan record. It does not claim induction.

## Q1 resolution (the e-ruling)

Decided above in COMP-1.4. Summary: e-verification allowed
as post-hoc feedback only; candidate space independent of
expected; e-ablation mandatory. If F2 fails, the claim
downgrades from "compositional machinery" to "compositional
search with feedback verification," and the battery must be
redesigned with consistent probe-relation semantics before
any stronger claim is tested.

## Q2 resolution (template load-bearing)

The template set {CHAIN-2, GATHER-n, ITERATE-UNTIL} is
researcher-chosen, and that is suspicious in exactly the
LORG-Q1 sense. This prereg answers the suspicion three ways:

1. Generality argument (frozen): each template is a
   structural shape over the EXECUTE vocabulary, not a
   semantic content. CHAIN-2 is "join twice"; GATHER-n is
   "collect slots then apply"; ITERATE-UNTIL is "step until
   sentinel." None names a domain relation, a world type,
   or a benchmark regularity. They are to plans what
   APPLY is to execution: machinery shapes.

2. Template-ablation test (frozen): remove ITERATE-UNTIL
   from the set. W1 two-hop and W9 grandparent must still
   pass; W9 depth must fail. Remove CHAIN-2: W1 and
   grandparent must fail; nothing else changes. This
   proves each template carries its own load and no hidden
   generalizer is doing the work.

3. Template-composition test (P4): a held-out 3-hop chain
   must be solved with no new template, via CHAIN-2
   applied twice (plan composition at the learner level).
   If templates compose, they are primitives, not a menu.
   This is the L3B anti-menu requirement applied to
   Cluster C: a finite non-composable template list would
   be a menu and would fail review.

If a fourth template is ever needed, it requires a fresh
prereg carrying the same three-part argument. F5 enforces
this: template-set growth without a generality argument
fails review.

## Q3 resolution (policy location)

Plan construction lives in a frozen generic bootstrap
miss-policy installed via the MISS_POLICY register
(approved amendment A2), following the compose_ops section 4
pattern: fixed generic machinery that the learner's own
structures supersede over time. The bootstrap tries
templates in the fixed order CHAIN-2, GATHER-n,
ITERATE-UNTIL, instantiating over subject-incident
relations. A learner process may author its own dispatch
structure into MISS_POLICY (via ordinary WRITE to the
register node), replacing or reordering the bootstrap.
The bootstrap is replaceable; it is not a second
cognitive subsystem.

## Q4 resolution (counting)

The composition mechanism adds no counter primitive and no
arithmetic operation. ITERATE-UNTIL's step counter uses the
frozen ISA arithmetic basis (per the ISA boundary ruling
and the EXECUTE placement: INC/DEC or ADD as approved).
The prereg does not decide the arithmetic basis; it
references the frozen ISA boundary. If the approved basis
lacks increment, the learner constructs successor chains
from cells (honest and clunky, per the scout). Basis creep
to serve W9 depth is a treadmill signal, not a success.

## One mechanism: the argument and the split bar

The scout's finding stands: one execution mechanism (plan
construction plus EXECUTE-vocabulary execution), three
discovery problems (relation-pair search, gather-plus-
combine, iteration hypothesis). The construction mechanism
in COMP-1.2 is identical across all three: instantiate
templates over subject-incident relations, execute, verify.
What differs is which template verifies, which is a
discovery outcome, not a mechanism difference.

The split bar is frozen in F1: if W1-style fixed-depth
composition succeeds while ITERATE-UNTIL traversal fails
(or vice versa) in a way traceable to the template rather
than to retention or induction dependencies, the "one
mechanism" claim narrows and ITERATE-UNTIL becomes a
separate mechanism under its own prereg. Until F1 fires,
no split.

## Predictions

- P1: W1 reaches 12/12 on the original battery. The two
  two-hop probes (599) return chained values via per-query
  CHAIN-2 search. Pure C; no Cluster B dependency. Note
  the scout's world-design observation: 599's inconsistent
  semantics across probes mean this tests search, not
  retained compositional meaning. P1 claims search
  success, nothing stronger.

- P2: W8 recall stays 4/4. Novel utterances move from 0/5
  toward 4/5 CONDITIONAL on the combining function being
  present in the workspace as a learner structure. The
  composition prereg covers assembly only. The test runs
  in two configurations: (i) combining function supplied
  (assembly in isolation); (ii) combining function induced
  by Cluster B machinery (the B+C bridge). Configuration
  must be stated before the run; the prereg claims (i)
  fully and (ii) as a bridge result shared with B.

- P3: W9 grandparent probes resolve via CHAIN-2; depth
  probes resolve via ITERATE-UNTIL. CONDITIONAL on Cluster
  A edge stability (C75 must not evict tree edges
  mid-world; composition is tested on a stable store
  first, then under pressure) and on the iteration plan
  being constructible (the discovery dependency is
  stated, not hidden).

- P4 (generality): a held-out compositional form not in
  the template list (a 3-hop chain over consistent
  relations) is solved with no new template, via
  learner-level composition of CHAIN-2 with itself. If
  this fails while P1 passes, the templates are a fixed
  menu and the mechanism claim bounds itself honestly to
  fixed-depth plans.

- P5 (separation): W2/W3 scores are unchanged by the
  composition change alone. Plan execution without
  induction does not induce. This proves C does not
  collapse into B.

## Falsification conditions

- F1 (split bar): W1 solved but W9 traversal not, or the
  reverse, traceable to the template rather than to
  retention/induction dependencies. The "one mechanism"
  claim narrows to fixed-depth plans; ITERATE-UNTIL
  becomes a separate mechanism under a fresh prereg.

- F2 (the e-ablation): with expected masked, plan
  construction collapses (not just plan selection: the
  mechanism stops building candidate plans). Then the
  capability is answer-key search, not compositional
  machinery. The claim is downgraded to "compositional
  search with feedback verification" and the battery is
  redesigned with consistent probe-relation semantics
  before any stronger claim.

- F3 (template treadmill): any new world class requires a
  new plan template to pass. That is a template treadmill,
  not a general mechanism; the prereg is rejected.

- F4 (boundary violation): composition machinery alone,
  with no induced combining structure in the workspace,
  solves W8-novel. Then the B/C boundary drawn here and
  in the scout is wrong; the clusters merge and both
  preregs are revised.

- F5 (oracle creep): the plan-template set grows past the
  three frozen templates without a fresh prereg carrying
  the Q2 three-part argument. The implementation fails
  review.

- F6 (unbounded candidates): the implementation builds
  candidate plans from relations NOT incident on the
  query subject (blind enumeration over relation ids, or
  expected-conditioned candidate generation). That is
  answer-key search regardless of e-ablation outcome;
  the implementation fails review.

- F7 (execution creep): the implementation requires any
  new core execution operation beyond the EXECUTE
  vocabulary to execute its plans. The "zero new ops"
  claim fails; the implementation fails review.

## One-System Rule accounting (prereg; measured at implementation)

- New core execution operations: 0 (frozen claim).
- New hardcoded semantic cases: 0.
- New modes: 0.
- New bridges: 0.
- New task-specific handlers: 0.
- New state formats: 0. Plans, plan-execution traces,
  and verified-plan records are node/edge conventions
  in the single CLA-2 workspace.
- Cognition source lines added: projected at most 150
  for the bootstrap miss-policy (candidate construction,
  template instantiation, execution dispatch,
  construct-then-verify loop). Every line is the general
  operation "construct and test compositional query
  plans," with zero branches on world type, relation id,
  or subject range. Exact count is an implementation
  measurement; growth past the bound without a fresh
  prereg fails review.
- Learner-state structures created: plan nodes,
  plan-execution traces, verified-plan records with
  SUPPORTS edges. All within the one workspace format.

## Dependencies on other clusters (no double work)

- Cluster A (retention): P3 is conditional on edge
  stability. Composition is tested on a stable store
  first; testing under memory pressure comes after,
  and confounded results are attributed to A, not C.
- Cluster B (construct-and-apply): P2 draws the
  boundary crisply. COMP-1 never induces a combining
  function; it assembles around one. The bridge
  configuration (ii) is shared evidence, claimed by
  neither cluster alone.
- Cluster D (learner-state ACT): independent. Plan
  execution does not select actions.

## Kill bars for the implementation (frozen here)

K1: this prereg (frozen alone, before any implementation
commit) completely specifies the mechanism: trigger,
candidate construction with the structural bound,
execution over the EXECUTE vocabulary, the E-ruling,
verification, promotion boundary, Q1-Q4 resolutions,
predictions P1-P5, falsification F1-F7, cluster
dependencies, and the One-System accounting bound.

K2: the implementation contains zero task-specific
handlers, zero new hardcoded semantic cases, zero modes,
zero bridges, zero new core execution operations, a
template set of exactly the three frozen templates, and
candidate plans built exclusively from subject-incident
relations. Verified by source inspection at review.

K3: pure Zag plus shell orchestration only (invoke znc,
run binaries, git ops, move/copy files); zero Python and
zero other implementation languages at every step; all
documents dash-clean via the shell-only byte check; the
contaminated paper untouched; commits local with explicit
pathspecs under composition_prereg/ only; no sealed
FW1-FW9 files accessed at any step.

## What this prereg does NOT authorize

- No implementation in this commit. The implementation
  worker builds only after review.
- No new core execution operations, even if plan
  execution proves awkward. Awkwardness is reported;
  F7 decides.
- No fourth template without a fresh prereg (F5).
- No induction of combining functions (Cluster B's
  work). COMP-1 assembles around learner structures;
  it does not create them from examples.
- No tuning to the original W1/W8/W9 battery beyond
  what the frozen mechanism specifies. The mechanism
  must work from templates and structure, not from
  battery-specific adjustments.
- No use of expected for plan generation (E-ruling).
  Expected is post-hoc feedback only.

## Generation tracking

Per the standing rule, the composition generation will
track: capabilities passed (P1-P5), cognition source
lines (bound 150), semantic cases (0), modes (0),
bridges (0), handlers (0), learner-state bytes (workspace
conventions only), new learned structures (plan nodes,
execution traces, verified-plan records).
