# PREREG: One-System Integration (TNN-1)

Date: 2026-09-30. Worker: Integration Prereg Author.
Status: PREREG-FROZEN (design only; no implementation in this commit).
Lane: Consolidated architecture, per the integration scout (c0e99a601)
and the integration inventory (INVENTORY.md in the scout path).
Verdict label target: INTEGRATION-PREREG-FROZEN.

## Step 0 Name-Check

Recorded in NAMECHECK.md before any design work: toolchain guard
check executed (`which python3 python`), `/usr/bin/python3` exists
as a system binary but is never invoked; strict non-use documented.
Pure markdown authorship; no code written; no interpreter used for
any purpose. No em dashes (shell byte grep). Contaminated paper
verified zero-diff. Sealed FW1-FW9 files never accessed. Prereg
committed alone before any implementation. Local only, owned path,
explicit pathspecs.

## The standing question

> Why can the existing general architecture not learn this behavior?

The integration scout (c0e99a601) gives the precise answer: there
is no single architecture yet. Four separate implementations
(CLA-2, CAM-1, ACT, COMP-1) contain roughly 475 lines of the same
workspace machinery written four times (byte accessors, node/edge
accessors, allocators, linkers, teach paths, query paths,
activation, evidence bid). The re-measurement report found the
three measured implementations sum to 1255 cognition lines against
the frozen core's 586, with learned structures at 3/1/2 versus
baseline 0. The capability is real but the substrate is not one
system. No existing binary passes more than its own test suite.
The gap is consolidation: one workspace, one bid function, one
miss path, one event log, with the four mechanisms as usage
patterns of that workspace rather than four stacks.

## Frozen inputs and rulings

This prereg is built on, and constrained by:

- Integration scout (c0e99a601): duplication inventory of ~475
  lines; CLA-2 workspace format wins; CAM-1 menu deleted not
  ported; unified event flow specified; projected ~1100 cognition
  lines; integration prereg shape with K1-K5 and F-INT1 through
  F-INT4; four open questions Q1-Q4, all decided here.
- ISA boundary ruling (0525377f3): the protected core may contain
  a SMALL, FROZEN, domain-neutral computational basis (ALLOC, READ,
  WRITE, LINK, COPY, COMPARE/EQ, ADD, BRANCH, APPLY/EXECUTE,
  generic registers). Frozen rule: no core operation may encode a
  target-domain regularity detector. The basis is never grown one
  benchmark at a time.
- Integration package A1-A12 (62e5ebb9f, approved with the ISA
  boundary added): 10 generic core ops, MISS_POLICY, POLICY_ROOT,
  sentinel/state machinery, trial-based P-DEP, edge-derived
  standing, zero modes/bridges/handlers.
- EXECUTE placement (1fc77503b): seventh primitive `EXECUTE(root,
  frame)` over the closed 4-op ISA {MOVE, BRANCHEQ, INC, DEC};
  amendments A-C. NOTE: Micah's explicit ruling on this placement
  remains pending; the implementation uses it as a built candidate
  and this prereg inherits that status. The prereg does not
  canonize the placement.
- CAM-1 red team (7f0ce2d97): P-DEP is menu selection not
  composition (4 researcher templates in fixed priority);
  MAP semantics live in `eval_body`'s 4-way dispatch (C0-A
  ATTACK-SUCCESS); standing is circular (promotion writes
  SUPPORTS from verification facts); finite-difference genuinely
  gone (ATTACK-PASS); posture is bounded L2, not L3. The menu
  does not port. The verify/promote/contradict half ports.
- ACT red team (73d06a6d4): bid directionality diverges from
  CLA-2 (ACT counts bidirectional, CLA-2 incoming-only);
  genericity, POLICY_ROOT, uncertainty all PASS; 24/24
  confirmed. The divergence is resolved here (Q1).
- ACT bid analysis (5257ac268) and alignment (75a9b0e04):
  bid() now counts incoming evidence edges only, matching
  CLA-2 evcount() per spec A3. Outgoing SUPPORTS are claims,
  not evidence. All 24 tests pass under directional semantics.
- CLA-2 red team (bd7a3f440): 4/5 vectors pass; Finding F1
  (stale binary) remediated at ad7d3ac1c (fresh 15/15).
- CLA-2 build (e639904f2): 685 cognition lines, 15/15 tests.
- COMP-1 build (170e39424): 879 total lines, 10/10 tests,
  byte-identical 3x; e-ruling structural (mp_build does not
  take expected); P4 via plan-structure composition.
- COMP-1 prereg (4f6f0c5c8): three frozen templates, e-ruling,
  K1-K3.
- DEVINT-CLA2 build (35f9500b2): 11 developmental stages pass
  on the CLA-2 workspace, B1-B5 hold, 3/3 byte-identical.
- DEVINT-CLA2 prereg (f24063bcb): eleven-stage sequence,
  frozen bars B1-B5.

## The mechanism: TNN-1

TNN-1 is a single Zag source file implementing one continuing
learner on one workspace. It is not four systems with a router.
It is one workspace with four usage patterns.

### TNN-1.1 The unified workspace (Q0 resolved)

The unified workspace uses the CLA-2 format as the base,
confirmed from the scout's four reasons (most complete edge
vocabulary, EXECUTE with closed 4-op ISA, POLICY_ROOT and
MISS_POLICY as ordinary nodes, ACT protocol and MAP nodes
already present). The format is frozen here:

- Nodes: 40 bytes each. Header: 64 bytes. Layout per CLA-2
  (tag, 4 refs, 4 payload slots, valid flag).
- Edges: 16 bytes each (from, to, type, reserved).
- Edge types: the CLA-2 12-type vocabulary, which is a
  superset of every relation the other three implementations
  use. No new edge types.
- Node budget: 1024 nodes, 4096 edges (Q4 resolution). This
  is 4x headroom over the largest current test (COMP-1's
  256-node tests) and below CAM-1's 4096-node budget. The
  budget is a frozen constant, not a tuned parameter.
- Node types: all CLA-2 types, plus exactly these additions:
  T_PLAN, T_STEP, T_COMBINE (from COMP-1); T_UNCERT (from
  ACT). Template markers TM_CHAIN2, TM_GATHER, TM_ITER,
  TM_COMPOSED (from COMP-1). No other new types.

### TNN-1.2 What ports, what dies (exact specification)

PORTS (with the source each derives from):

1. Workspace machinery (CLA-2): byte accessors, node/edge
   accessors, allocator, linker, teach path, exact-key query
   path, activation (with ACT's visited-set logic folded in
   if the builder finds it necessary; the builder documents
   the decision), decay, retention (see TNN-1.6), event log.
   One spelling of each. The other three spellings are
   deleted.

2. Seven core primitives (CLA-2): ALLOC, READ, WRITE, LINK,
   ACTIVATE, DECAY, EXECUTE with the closed 4-op ISA. Zero
   new core operations. This is a frozen claim enforced by
   F-INT3.

3. POLICY_ROOT and MISS_POLICY (CLA-2, A12): ordinary nodes
   writable through ordinary WRITE. The dispatch mechanism
   for the query-miss path and the action path.

4. Plan construction (COMP-1): `mp_build`, `mp_build_compose`,
   `mp_trigger`, `exec_plan` port with accessor renaming only.
   The three frozen templates {CHAIN-2, GATHER-n,
   ITERATE-UNTIL} are preserved exactly. The e-ruling is
   preserved exactly: `mp_build` and `mp_build_compose` do
   not take `expected`; the e-ablation (F2) still passes.
   The 150-line bootstrap bound from the COMP-1 prereg
   becomes the budget for the ported miss policy. Plan node
   types T_PLAN, T_STEP, T_COMBINE and template markers port
   as workspace conventions. `exec_plan`'s step kinds map
   onto the 4-op ISA.

5. Verify/promote/contradict (CAM-1, minus the menu):
   `verify` (train/test split, spurious-regularity
   rejection), `promote` (MAP-node promotion), `contradict`
   (CONTRADICTS-edge demotion). These port as the
   verification half of the miss path.

6. Five-step ACT protocol (CLA-2 `ev_act`, ACT): context
   assembly, POLICY_ROOT check, two-hop activation,
   address-equality structural match, highest-bid selection.
   The bid is directional (incoming-only) per the Q1
   resolution. Uncertainty nodes (T_UNCERT) participate as
   ordinary candidates; no special case. `learn_confirm`
   and `learn_contra` port as edge operations (USE,
   CONFIRMS, CONTRADICTS), which already exist in the
   CLA-2 vocabulary.

7. Post-promotion corroboration (red-team fix): promotion
   writes SUPPORTS edges from verification facts, but
   standing does not count those edges until post-promotion
   corroboration (a subsequent independent query hitting
   the MAP node). This breaks the circularity the CAM-1
   red team found. Frozen mechanism, specified here:
   a MAP node carries a corroboration counter edge
   (E_CORROB, learner-visible); standing = (SUPPORTS
   count minus CONTRADICTS count) over edges added after
   the promotion event, not the promotion's own edges.

8. Bootstrap miss policy (CLA-2): P-INV trial, learner-
   supersedable via ordinary WRITE to the MISS_POLICY
   node. The composition bootstrap (COMP-1's template
   dispatch) is installed as the learner-set policy that
   supersedes the P-INV bootstrap, demonstrating the
   supersession mechanism the CLA-2 red team verified
   exists.

DIES (deleted, not ported):

1. CAM-1's `eval_body` 4-way dispatch (the menu). Deleted.
   The red team showed it is bounded L2 menu selection;
   porting it would port the ceiling.
2. CAM-1's `B_COPY_B` and `B_DBL_B` dead code. Deleted.
3. Three of the four byte-accessor sets. Deleted.
4. Three of the four node/edge accessor sets. Deleted.
5. Three of the four allocators, linkers, teach paths,
   query paths. Deleted.
6. One of the two activation functions (keep CLA-2's).
7. Two of the three bid functions (keep CLA-2's
   incoming-only `evcount` semantics).
8. Three of the four test drivers (keep one unified
   driver).

### TNN-1.3 The unified event flow

One teach path, one query path, one action path:

```
TEACH(subj, rel, obj):
  allocate fact node, set tag/refs/payload, link edges,
  log event, decay, done.
  (CLA-2 ev_teach; the only teach.)

QUERY(subj, rel, expected?):
  exact-key lookup -> hit? return value.
  miss -> MISS_POLICY dispatch:
    null -> bootstrap (P-INV trial, learner-supersedable)
    learner-set -> plan construction (COMP-1 mp_build over
      3 frozen templates, instantiated over
      subject-incident relations only)
    constructed plan -> execute via EXECUTE vocabulary
      (frozen step budget)
    executed plan -> verify (CAM-1 train/test split;
      expected used as post-hoc feedback ONLY, per the
      e-ruling; in live mode expected is absent and
      selection falls back to first non-sentinel)
    verified -> promote as MAP node (with post-promotion
      corroboration per TNN-1.2.7)
    failed -> return -2 (S_MISS).
  (One miss path replacing three.)

ACT():
  5-step protocol (CLA-2 ev_act):
    context assembly -> POLICY_ROOT check -> 2-hop
    activation -> address-equality match ->
    highest-directional-bid selection.
  Uncertainty nodes participate as ordinary candidates.
  A plan constructed for a query miss may later be
  selected by ACT as an action guide through the same
  edges (cross-capability integration, tested by F-INT4).
```

CAM-1's PROPOSE/VERIFY/PROMOTE/APPLY becomes: plan
construction is the propose step, the train/test split is
the verify step, MAP promotion is the promote step,
EXECUTE is the apply step. Four named phases, one code
path, zero new operations.

### TNN-1.4 The composition that matters

The integration's thesis, frozen: a query miss triggers
plan construction (COMP-1), the constructed plan is
verified (CAM-1's split), the verified plan is promoted as
a MAP node (CLA-2's standing, with corroboration), and
future queries hit the MAP node via exact-key lookup.
Action selection (ACT) runs on the same workspace,
selecting among ACTION-GUIDEs by the same directional bid
function. One workspace, one bid, one miss path, one
event log, three capabilities. A plan built for a query
can later guide an action; a contradiction against a MAP
node demotes both its query standing and its action
candidacy through the same CONTRADICTS edges.

### TNN-1.5 Q1 resolution (bid directionality)

RESOLVED: incoming-only (directional), matching CLA-2
`evcount()`. Decided by the ACT bid analysis (5257ac268)
and implemented at 75a9b0e04. Rationale, frozen: the bid
is a signed count over evidence edge types. An outgoing
SUPPORTS edge from guide G to outcome O is G's claim about
the world, not evidence for G. Counting outgoing edges
conflates a node's claims with its credibility. Prediction
correctness is captured directionally via incoming
CONFIRMS (+1) and CONTRADICTS (-1). The integration
implements one bid function; the ACT red team's spec
divergence is closed.

### TNN-1.6 Q3 resolution (retention unification)

RESOLVED: CLA-2's three-step retention routine is the
unified policy, with ACT's signed-bid eviction as the
step-1 ordering. CAM-1 has no retention; nothing to merge.
The builder ports CLA-2's routine and uses the directional
bid for eviction ordering. ACT's `evict_to_cap` test
stand-in is replaced by the real routine. One retention
policy, not three.

### TNN-1.7 DEVINT-CLA2 relationship

DEVINT-CLA2 (35f9500b2) is an 11-stage developmental
curriculum that runs on the CLA-2 workspace format. The
integrated binary must support the DEVINT-CLA2 curriculum:
the builder re-runs the 11 stages against the integrated
workspace and reports stage-by-stage results. This is a
frozen prediction (P-INT5), not an optional extra. If the
curriculum fails on the integrated workspace, the port
broke something the standalone CLA-2 format supported.

## Predictions

- P-INT1: the integrated binary passes CLA-2's 15/15
  tests (8 original + 7 amendment: EXECUTE, EXECUTE-FAIL,
  SIGNED-BID, ACT, ACT-NULL, BOOTSTRAP, REGISTERS), all in
  one process.

- P-INT2: the integrated binary passes ACT's 24/24 tests
  (P-ACT1 planning, P-ACT2 inquiry, P-ACT3 null policy,
  P-ACT4 ablation, P-ACT5 generality, P-ACT6 memory
  prerequisite), all in one process, with the directional
  bid. No test changes from the aligned ACT.

- P-INT3: the integrated binary passes COMP-1's 10/10
  tests (P1 two-hop, F2 e-ablation, P2 GATHER plus
  GATHER-decline control, P3 grandparent, P3 depth via
  ITERATE counter, P4 3-hop via plan-structure composition,
  P5 separation, both template ablations), all in one
  process. The e-ablation still passes: masking expected
  does not collapse plan construction.

- P-INT4: the integrated binary passes CAM-1's P6
  (spurious-regularity rejection) and P7 (contradiction
  demotion) as ported integration tests, using the
  verify/promote/contradict machinery with post-promotion
  corroboration. The menu (eval_body dispatch) does not
  appear.

- P-INT5: the DEVINT-CLA2 11-stage curriculum re-runs on
  the integrated workspace with all B1-B5 bars holding
  (persistence, exact stage numbers, blindness,
  interference, delayed reuse).

- P-INT6: 3/3 byte-identical determinism across the full
  49-test battery (15 + 24 + 10) plus the ported P6/P7
  and the DEVINT-CLA2 re-run, all in one process, exit 0.

- P-INT7: cognition lines land below the 1200 hard ceiling
  (projected ~1100 per the scout's honest arithmetic).
  The exact count is an implementation measurement.

## Falsification conditions

- F-INT1 (line count): the integrated cognition line
  count exceeds 1200. The integration has failed to
  compress; the One-System claim is weakened and the
  build fails review. The builder does not get to re-argue
  the ceiling after seeing the count.

- F-INT2 (regression): any test from the three suites
  (P-INT1 through P-INT3) fails in the integrated binary
  but passed standalone. The port introduced a regression;
  the build fails until the regression is fixed without
  new machinery.

- F-INT3 (template smuggling): source scan finds a fourth
  template in the propose path, a domain-conditional in
  the miss path, or any researcher-authored semantic case
  (a branch on world type, relation identity, or task
  type in the cognitive path). The integration smuggled
  in researcher knowledge; the build fails review. The
  CAM-1 menu must not reappear in any form.

- F-INT4 (coexistence without integration): the
  integrated system cannot pass a cross-capability test:
  a plan constructed for a query miss (COMP-1 path),
  promoted as a MAP node (CAM-1 path), later selected by
  ACT as an action guide through the same edges, with a
  contradiction against the MAP node demoting both its
  query standing and its action candidacy. If the
  mechanisms coexist but do not interact through shared
  state, the integration is four systems in a trench
  coat and the One-System claim fails.

- F-INT5 (execution creep): the implementation requires
  any new core execution operation beyond the 7 frozen
  primitives and the 4-op ISA to execute its plans or
  run its protocols. The "zero new ops" claim fails;
  the build fails review.

- F-INT6 (e-ablation collapse): with expected masked, plan
  construction collapses (not just selection). The
  compositional capability was answer-key search; the
  claim downgrades per the COMP-1 F2 ruling.

## One-System Rule accounting (prereg; measured at implementation)

- New core execution operations: 0 (frozen claim,
  enforced by F-INT5).
- New hardcoded semantic cases: 0 (enforced by F-INT3).
- New modes: 0.
- New bridges: 0.
- New task-specific handlers: 0.
- New state formats: 0. Plans, MAP nodes, uncertainty
  nodes, and guides are node/edge conventions in the
  single CLA-2 workspace format.
- Cognition source lines: hard ceiling 1200 (enforced by
  F-INT1). Projected ~1100. Every line is general
  workspace operation, miss-path dispatch, plan
  construction, verification, promotion, retention, or
  the ACT protocol, with zero branches on world type,
  relation id, or subject range.
- Learner-state structures created: plan nodes,
  plan-execution traces, MAP nodes with corroboration,
  uncertainty nodes, ACTION-GUIDEs, all within the one
  workspace format.

## Kill bars for the implementation (frozen here)

K1: this prereg (frozen alone, before any implementation
commit) completely specifies the mechanism: the unified
workspace format (TNN-1.1), the exact port/delete list
(TNN-1.2), the unified event flow (TNN-1.3), the
composition thesis (TNN-1.4), Q1/Q3/Q4 resolutions,
the DEVINT-CLA2 relationship (TNN-1.7), predictions
P-INT1 through P-INT7, falsification F-INT1 through
F-INT6, and the One-System accounting bound. The
implementation commit must be a strict descendant of
this prereg commit (verified by git merge-base).

K2: the implementation contains zero new core execution
operations, zero hardcoded semantic cases, zero modes,
zero bridges, zero task-specific handlers, a template set
of exactly the three frozen templates, candidate plans
built exclusively from subject-incident relations, one
directional bid function, one retention policy, and
cognition lines below the 1200 hard ceiling. Verified by
source inspection and measurement at review. The CAM-1
menu must not reappear in any form.

K3: pure Zag plus shell orchestration only (invoke znc,
run binaries, git ops, move/copy files); zero Python and
zero other implementation languages at every step; all
documents dash-clean via the shell-only byte check; the
contaminated paper untouched; commits local with explicit
pathspecs under integration_prereg/ and the builder's
owned path only; no sealed FW1-FW9 files accessed at any
step.

K4: the integrated binary passes P-INT1 (15/15), P-INT2
(24/24), P-INT3 (10/10), P-INT4 (ported P6/P7), and
P-INT5 (DEVINT-CLA2 11 stages), all in one process,
byte-identical across 3 runs (P-INT6). Any F-INT2
regression fails the build.

K5: the cross-capability integration test (F-INT4) passes:
a query-miss plan becomes an action guide through shared
edges, and contradiction demotes both candidacies. The
mechanisms interact through shared state, not merely
coexist.

## What this prereg does NOT authorize

- No implementation in this commit. The implementation
  worker builds only after review.
- No new core execution operations, even if the port
  proves awkward. Awkwardness is reported; F-INT5 decides.
- No fourth template without a fresh prereg (F-INT3).
- No resurrection of the CAM-1 menu (eval_body dispatch)
  in any form. The red team killed it; this prereg buries
  it.
- No bidirectional bid. Q1 is resolved: directional only.
- No tuning to any test battery beyond what the frozen
  mechanism specifies. The port must be faithful
  accessor-renaming and specified glue, not
  battery-specific adjustment.
- No weakening of the 1200-line ceiling after the count
  is measured (F-INT1).
- No claiming L3 or SURVIVES. The builder reports
  BUILD-PASS or BUILD-FAIL only. The eleven-stage
  promotion pipeline governs any stronger claim.

## Generation tracking

Per the standing rule, the integration generation will
track: capabilities passed (P-INT1 through P-INT7),
cognition source lines (hard ceiling 1200), semantic
cases (0), modes (0), bridges (0), handlers (0),
learner-state bytes (one workspace: 1024 nodes, 4096
edges), new learned structures (plan nodes, MAP nodes
with corroboration, uncertainty nodes, ACTION-GUIDEs,
all in the one format).
