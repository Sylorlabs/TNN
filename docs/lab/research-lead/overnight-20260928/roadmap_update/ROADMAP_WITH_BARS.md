# TNN-3 Roadmap with Kill Bar Mapping

Date: 2026-10-01 (UTC).

**Status: DRAFT-NOT-FROZEN - AWAITING MICAH REVIEW**

This document integrates the kill bar priority order (`20d810d4b`,
`bar_priority/BAR_PRIORITY.md`) into the TNN-3 roadmap synthesis
(`67a420cca`, `tnn3_roadmap/TNN3_ROADMAP.md`). It adds a bar mapping
to each roadmap phase. It changes none of the roadmap's
recommendations: the order, the gating constraints, the treadmill
warning, the risks, and the banked items are transcribed from the
roadmap. All 24 bars remain DRAFT-NOT-FROZEN; this mapping governs
nothing until Micah reviews the bars and a TNN-3 preregistration
freezes the bars it covers.

Inputs (read-only, no modifications):
- Roadmap: `67a420cca` (recommended order in its section 7).
- Priority: `20d810d4b` (phase order P0-P4 plus PX, 2 future, 1 audit).

Bar provenance (for orientation):
- 11 K-T3-* bars: kill-bar draft `76231baa8`.
- K-H3: H3-lite design `22197da2c`.
- K-TSEL-1/2: target-selection design `01c2aacfe`.
- K-REUSE-1/2: reuse-path design `5f15b9309`.
- K-H2-1/2/3/4: H2 probe design `4631c5918`.
- K-COMP-OP, K-INQ-INFO, K-XMECH, K-STATE-RET: gap bars `36e5a70e1`.

---

## Step 0 (done): H3 cheap policy-revisability check

Roadmap status: complete. Result: all three mechanisms structurally
unrevisable. H3 confirmed as architectural fact. Not repeated.

Bars in this step: none. The cheap check was a source-level audit,
not a bar evaluation. The bar that carries its prediction forward is
K-H3, which belongs to Step 2 below (Track B / P2B).

## Step 1: H2 probes (masked verification)

Roadmap order position: first active step. Keep the finite grammar
fixed; change only verification. Tests whether the oracle is the
binding constraint. Cost: new sealed worlds, no new machinery.

**Bars:**
- P0-1. **K-T3-ADV** (adversarial process). Process precondition: the
  sealed trap worlds for the H2 probes need the adversary protocol
  (independent adversary, post-freeze authorship verification,
  fail-closed rule) before any sealed evaluation runs.
- P1-1. **K-H2-1** (masked accuracy).
- P1-2. **K-H2-2** (lie resistance).
- P1-3. **K-H2-3** (criterion causality and revisability).
- P1-4. **K-H2-4** (domain neutrality and reuse).
- P1-5. **K-STATE-RET** (structure retention), audit-grade. Run now as
  diagnostic infrastructure to establish the baseline (predicted
  TNN-2: FAIL; rejected candidates evaporate). No dependencies.

Parallel structure: P0 first, then P1-1 through P1-4 and P1-5 are
fully parallel. All five can start immediately and independently.
Predicted TNN-2: FAIL all four H2 sub-clauses (this is the point;
they establish the baseline the later steps must beat).

**Gate role:** Step 1 is the treadmill guard for Step 4. The
roadmap's binding constraint: Step 4 (H1 widening) begins only after
the H2 results are recorded, whether they pass (H2 addressed) or
fail with a recorded plan to address the oracle. Widening the
constructor while verification still uses environment-supplied
expected values produces a larger finite menu under the same
generous acceptance test.

## Step 2: H3-lite (policy parameterization)

Roadmap order position: second. Implement the three policy nodes from
`22197da2c` with the K-H3 bar frozen in preregistration. Makes the
mechanisms' decisions revisable by experience. This is the minimal
TNN-3 core. Cost: moderate new machinery, no ISA change, no
governance decision.

**Bars:**
- P2B-1. **K-H3** (policy revisability). The five-part listing per
  structural decision (decision, learner-state location, production
  write path, triggering event, sealed history-dependent variation
  test). The three policy nodes (trial order, guide template, repair
  dispatcher) and their discrimination tests are parallel sub-tests.
- P0-1. **K-T3-ADV** continues to govern the sealed worlds used in
  the K-H3 discrimination tests (order-flip worlds, template-shift
  scenarios, topology-preference shifts).

Parallel structure: K-H3 is cross-cutting and conditions all
mechanism bars, but has no mechanism prerequisites of its own. It
runs in parallel with Track A (Step 2 reuse path below) and with
the Phase 1 diagnostics.

**Gate role:** K-H3 complete is the prerequisite for every Phase 3
bar (Step 3 below). The roadmap states the dependency as: the
repair dispatcher policy (H3-lite subtype 3) selects among the
repair topologies the generator enumerates; the inquiry bars need
the revisable guide policy (subtype 2).

**Theater warning (from the roadmap, section 6, risk 2):** H3-lite
could become revisability theater if write paths exist but are never
meaningfully exercised. K-H3 condition (d) guards this: sealed tests
must use ordinary world interactions where the decision change is an
outcome, not an input.

## Step 3: Repair-proposal generator and inquiry resolution

Roadmap order position: third. The within-ISA changes: wire
`t2_trial`'s execution and verification halves into the revision
path plus a repair-proposal generator (`edbb0e9b5` section 4a);
persist trial candidates as hypothesis structures, derive guides per
discriminating sub-query, add the `resolve_uncertainty` transition
(`dedfad368` sections 1-2). Completes the minimal TNN-3 from the
roadmap's section 1. The generator can be built and tested with a
fixed repair order first; the H3-lite dispatcher (Step 2) learns
the order.

**Bars (all require Step 2 K-H3 complete):**
- P3-1. **K-T3-INQ-1** (derived discriminating need). Needs the
  revisable guide policy.
- P3-2. **K-T3-INQ-3** (ambiguity handled non-arbitrarily). Needs the
  revisable guide policy. Parallel with P3-1.
- P3-3. **K-T3-REV-1** (sealed repairs, derived content). Needs the
  repair-proposal generator building on the H3-lite repair
  dispatcher.
- P3-4. **K-T3-REV-2** (retained-set regression). Rides the same
  evaluation runs as P3-3.
- P3-5. **K-T3-REV-3** (successive revision including revert). Rides
  the same evaluation runs as P3-3.
- P3-6. **K-T3-INQ-2** (evidence updates behavior). Needs the guide
  policy plus the inquiry resolution path (the L6 link). Last of the
  inquiry bars because resolution is the missing infrastructure.
- PX-1. **K-XMECH** (graceful cross-mechanism interference). Include
  its interference worlds in the K-T3-ADV battery from the start and
  evaluate alongside. Needs no separate infrastructure; only
  meaningful once the mechanisms exist.

Parallel structure: three groups once Step 2 is done: (P3-1, P3-2)
vs (P3-3, P3-4, P3-5) vs (P3-6). PX-1 runs with all of them.

## Step 4: H1 widening (open constructor), only after Step 1

Roadmap order position: fourth. Recursive composition via inlining
(per `e2e34a4ac` section 4), plus the target-selection policy as a
learner-state mechanism. This step must not precede Step 1, per the
treadmill warning (roadmap section 6, risk 3). It also requires the
post-freeze adversarial battery (K-T3-ADV) to test whether fixed
composition operators suffice for genuinely new structures.

**Gates (all must clear):**
1. Phase 1 H2 results recorded (Step 1 complete). Treadmill guard.
2. Step 2 K-H3 complete (all Step 4 bars need revisable decisions).
3. For P4-2/P4-3 and P4-5/P4-6: reuse path complete (Step 2 Track A
   below), because the signals those bars consume do not exist
   without query-time MAP execution.

**Bars:**
- P4-1. **K-T3-CON-1** (sealed construction, derived content). Needs
  the open constructor. Gate: H2 results recorded. Independent of
  the reuse track.
- P4-2. **K-TSEL-1** (learner-chosen composition targets). Needs
  reuse path complete (selector reads reuse signals) and H2 gate.
  Evaluated together with P4-3.
- P4-3. **K-TSEL-2** (no oracle shortcut). Same gates as P4-2.
- P4-4. **K-T3-TOPO** (learner-chooses-topology audit). Audits the
  diversity sets produced by P4-1 and P3-3. Runs with the mechanism
  bars, not before them; order alongside P4-1 and P3-3.
- P4-5. **K-T3-CON-2** (construction reuse, C0-D). Needs reuse path
  complete (construction reuse via inlining requires promoted graphs
  to be executable components; K-REUSE-1 makes MAP execution
  observable). Independent of the H2 gate.
- P4-6. **K-T3-INQ-4** (inquiry reuse and transfer, C0-D). Needs
  reuse path complete (architectural precondition).
- PX-1. **K-XMECH** continues alongside.

Parallel structure: P4-1 vs P4-2/P4-3 vs P4-5 vs P4-6 are parallel
once their gates clear. P4-4 rides with P4-1 and P3-3.

**Treadmill warning (from the roadmap, section 6, risk 3, restated
unchanged):** a TNN-3 that implements recursive composition while
`t2_try_verify` still matches environment-supplied expected values
has built a more expensive slot-filler, not a more general learner.

## Parallel track: the reuse path (interaction H2)

Roadmap order position: parallel with the above, not ordered after.
Routing `ev_query` hits through MAP execution instead of memoized
facts is required for C0-D regardless of which synthesis hypothesis
binds. Orthogonal to H1/H2/H3.

**Bars:**
- P2A-1. **K-REUSE-1** (query-time MAP execution). No prerequisites.
- P2A-2. **K-REUSE-2** (no shadow facts). No prerequisites. Parallel
  with P2A-1 (two independent checks on the same mechanism).

Parallel structure: Track A runs fully parallel with Track B
(Step 2 K-H3) and with Phase 1. Its only gate role: it must finish
before P4-2/P4-3 (K-TSEL-1/2), P4-5 (K-T3-CON-2), and P4-6
(K-T3-INQ-4), which consume its signals.

## Explicitly not in the roadmap: full H3

Roadmap status: pending the protected-core structural-ops
governance decision banked for Micah (brief `092566072`,
recommendation Alternative C: H3-lite only, defer, NOT DECIDED).
The H3-lite stepping stone (Step 2) is the recommended way to gather
evidence for that decision.

No bars are assigned to full H3 in this mapping. If Micah later
approves structural graph mutation, the bar set would need a
K-H3-full formulation; none exists yet.

## The 2 future-generation bars: triggers (not in the roadmap phases)

Explicit non-claims for the minimal TNN-3. They give teeth to future
claims without being attempted now.

- **K-COMP-OP** (learner-originated composition operators). Trigger: a
  future generation claims its composition operators are
  learner-originated. Preconditions: K-REUSE-1 passes (composition
  needs executable MAPs as operands) and K-TSEL-1/2 pass (operand
  selection must already be learner-driven). Predicted TNN-2: FAIL
  by absence.
- **K-INQ-INFO** (informativeness-ranked inquiry). Trigger: a future
  generation implements an informativeness criterion for
  non-dominated uncertainties. Preconditions: K-H3 passes and the
  Step 3 inquiry resolution path exists. Predicted TNN-2: FAIL
  (constant action, no ranking, no resolution path).

## The 1 audit-grade bar: placement

- **K-STATE-RET** (structure retention). Per the kill-bar review
  recommendation adopted by the prereg structure: run as a
  governance audit probe alongside every sealed evaluation battery,
  not as a generation-gating kill bar. No dependencies; run now
  against frozen TNN-2 for the baseline, and on every later
  evaluation. Complements K-T3-TOPO (passing structures) and
  K-T3-INQ-4.

## Master table

| Roadmap phase | Priority phase | Bars | Gates in |
|---|---|---|---|
| Step 1: H2 probes | P0, P1 | K-T3-ADV; K-H2-1, K-H2-2, K-H2-3, K-H2-4; K-STATE-RET (audit) | P0 first; P1 fully parallel |
| Step 2: H3-lite | P2B | K-H3 (three policy-node tests) | None; parallel with P1, P2A |
| Parallel: reuse path | P2A | K-REUSE-1, K-REUSE-2 | None; parallel with P1, P2B |
| Step 3: repair + inquiry | P3 | K-T3-INQ-1, K-T3-INQ-3; K-T3-REV-1, K-T3-REV-2, K-T3-REV-3; K-T3-INQ-2 | P2B (K-H3) complete |
| Step 4: H1 widening | P4 | K-T3-CON-1; K-TSEL-1, K-TSEL-2; K-T3-TOPO; K-T3-CON-2; K-T3-INQ-4 | P1 results recorded; P2A for TSEL/CON-2/INQ-4; P2B for all |
| Integration | PX | K-XMECH | Mechanisms exist (P3/P4); parallel with P3, P4 |
| Future (non-claims) | -- | K-COMP-OP, K-INQ-INFO | Future claims only |
| Audit (every battery) | -- | K-STATE-RET | None; run each evaluation |

Count check: Step 1: 1 + 4 + 1 audit = 6. Step 2: 1. Reuse: 2.
Step 3: 6. Step 4: 6. PX: 1. Total minimal: 6 + 1 + 2 + 6 + 6 + 1
= 22? No: K-STATE-RET is counted once (audit), and K-T3-ADV once
(process). Mechanism bars: 4 (P1) + 1 (P2B) + 2 (P2A) + 6 (P3) +
6 (P4) + 1 (PX) = 20, plus K-T3-ADV (process) = 21 minimal.
Plus 2 future plus 1 audit = 24 total. Matches the inventory
(`1722884ad`).

## Critical path (from the priority document, restated)

K-T3-ADV (P0) -> K-H3 (P2B) -> Phase 3 mechanism bars ->
K-TSEL-1/2 (P4, also needs Track A).

The H2 probes (Step 1) and the reuse path (Track A) are off the
critical path: they run in parallel, and their only gate roles are
that Step 1 results must be recorded before Step 4, and Track A must
finish before the bars that consume its signals.

## What this mapping does not do

- It does not freeze any bar. All 24 remain DRAFT-NOT-FROZEN.
- It does not resolve the 6 open kill-bar questions (draft
  `76231baa8` section 11); Micah's review is still required.
- It does not decide the K-STATE-RET placement (bar-grade vs
  audit-grade); the audit-grade placement above follows the review
  recommendation, but Micah decides.
- It does not change the roadmap's order, risks, or banked items.
- It does not authorize implementation. Any TNN-3 work needs its own
  preregistration with frozen bars.

---

## Verdict

ROADMAP-UPDATE-COMPLETE.

Integration only. DRAFT-NOT-FROZEN. No new bars, no bar text
modified, no roadmap recommendations changed, no implementation, no
source edits. Paper untouched.

*End of integration. No source modified. No scores claimed. Paper
untouched.*
