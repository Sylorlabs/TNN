# Kill Bar Implementation Priority Order

**Status: DRAFT-NOT-FROZEN - AWAITING MICAH REVIEW**

Date: 2026-10-01 (UTC).

This document orders the 24 kill bars inventoried in
`bar_inventory/` (`1722884ad`) for implementation and evaluation.
It creates no new bars and modifies none. All bars remain
DRAFT-NOT-FROZEN; this ordering governs nothing until Micah
reviews the bars and freezes them through the normal
preregistration process.

Inputs: the bar inventory (`1722884ad`), the dependency graph in
the prereg structure synthesis (`206499c03`, section 2), the
roadmap order (`67a420cca`, section 7), and the gap bars
(`36e5a70e1`).

---

## 1. The 21 minimal TNN-3 bars, ordered by phase

### Phase 0: Process precondition (before any sealed evaluation)

**P0-1. K-T3-ADV (adversarial process).**

This is not a mechanism bar; it is the precondition for every
bar that references sealed worlds. The prereg structure states it
directly: "If K-T3-ADV fails (e.g., a world asset predates the
build freeze), the evaluation is BLOCKED, fail closed, and no
mechanism bar can pass." It must therefore be set up first: the
independent adversary designation, the post-freeze authorship
verification procedure, the world-count minima (with Micah's
resolution of the 6 open questions), and the fail-closed rule.

Nothing sealed can be attempted until this is in place. It has no
dependencies of its own.

### Phase 1: Diagnostics (runnable immediately against frozen TNN-2, in parallel)

These bars need no new machinery and can be evaluated against the
frozen TNN-2 build right now. All are predicted FAIL, which is the
point: they establish the baseline the roadmap's later steps must
beat, and they carry the treadmill guard that constrains Step 4.

**P1-1. K-H2-1 (masked accuracy).**
**P1-2. K-H2-2 (lie resistance).**
**P1-3. K-H2-3 (criterion causality and revisability).**
**P1-4. K-H2-4 (domain neutrality and reuse).**

The four H2 sub-clauses are mutually independent checks on the
same sealed trap worlds: accuracy against a baseline, lie
resistance, white-box causality, and domain neutrality with reuse
coupling. They can be evaluated in parallel on the same battery.
Per the roadmap and the gap-bars integration note, the H2 probes
must precede Step 4 (H1 widening): widening the constructor while
the acceptance oracle remains is the treadmill.

**P1-5. K-STATE-RET (structure retention) -- audit-grade.**

The kill-bar review's recommendation, adopted by the prereg
structure, is to run this as a governance audit probe rather than
a bar. It has no dependencies ("this probe can be run against any
build at any time, including the frozen TNN-2"). Run it now as
diagnostic infrastructure: dump learner state after trials with
rejections and report the retained-structure ratio. Predicted
TNN-2: FAIL (candidates evaporate). It does not gate any build;
it detects the verdicts-without-structures pattern early.

Phase 1 ordering summary: P1-1 through P1-4 and P1-5 are fully
parallel. All five can start immediately.

### Phase 2: Parallel build tracks (independent of each other)

Two tracks proceed in parallel. They share no dependencies.

**Track A: Reuse path.**

**P2A-1. K-REUSE-1 (query-time MAP execution).**
**P2A-2. K-REUSE-2 (no shadow facts).**

No prerequisites. The reuse path is orthogonal to H1/H2/H3
("can proceed in parallel"). K-REUSE-1 and K-REUSE-2 are two
independent checks on the same mechanism (execution event vs
absence of shadowing) and can be evaluated in parallel. Track A
is the enabler for K-TSEL-1/2, K-T3-CON-2, and conceptually
K-T3-INQ-4.

**Track B: H3-lite (policy parameterization).**

**P2B-1. K-H3 (policy revisability).**

No mechanism prerequisites; it is cross-cutting and conditions
all mechanism bars ("any bar testing derived content or
history-dependent behavior implicitly requires the relevant
decisions to be in learner state with production write paths").
The three policy nodes (trial order, guide template, repair
dispatcher) are independent decisions and their five-part
listings plus discrimination tests can be built and evaluated in
parallel. Track B is the minimal TNN-3 core and the prerequisite
for every Phase 3 bar.

Phase 2 ordering summary: Track A and Track B are fully
parallel. Within Track A, P2A-1 and P2A-2 are parallel. Track B
is a single bar with three parallel sub-tests.

### Phase 3: Mechanism completion (requires Phase 2 Track B)

These bars need the H3-lite policy nodes from Track B: each tests
behavior that is only meaningful once the relevant decision is
revisable by experience.

**P3-1. K-T3-INQ-1 (derived discriminating need).**
**P3-2. K-T3-INQ-3 (ambiguity handled non-arbitrarily).**

Both need the revisable guide policy (H3-lite subtype 2). They
are independent of each other (different scenarios, different
observables) and can be evaluated in parallel once Track B is in
place.

**P3-3. K-T3-REV-1 (sealed repairs, derived content).**
**P3-4. K-T3-REV-2 (retained-set regression).**
**P3-5. K-T3-REV-3 (successive revision including revert).**

These need the repair-proposal generator from the roadmap's Step
3, which builds on the H3-lite repair dispatcher (Track B
subtype 3): the generator enumerates repair topologies, the
policy learns the order. K-T3-REV-2 and K-T3-REV-3 are checks on
the revision mechanism's discipline and can ride the same
evaluation runs as K-T3-REV-1; all three are parallel in
evaluation.

**P3-6. K-T3-INQ-2 (evidence updates behavior).**

Needs the H3-lite guide policy plus the inquiry resolution path
from Step 3 (the L6 link). It is the last of the inquiry bars
because resolution is the missing infrastructure; P3-1 and P3-2
test need-derivation and ambiguity handling, which do not require
the resolution transition.

Phase 3 ordering summary: all six bars require Track B
complete. Within Phase 3, P3-1/P3-2, P3-3/P3-4/P3-5, and P3-6
are three parallel groups.

### Phase 4: H1 widening (requires Phase 1 H2 result AND Phase 2)

The roadmap's critical constraint: Step 4 must not precede Step 1.
Widening the constructor while `t2_try_verify` still matches
environment-supplied expected values produces "a larger finite
menu under the same generous acceptance test." The H2 probes
(Phase 1) are therefore a gate: Step 4 begins only after the H2
results are in, whether they pass (H2 addressed) or fail with a
recorded plan to address the oracle.

**P4-1. K-T3-CON-1 (sealed construction, derived content).**

Needs the open constructor from Step 4 (recursive composition via
inlining). Gate: Phase 1 H2 results recorded. Independent of
Track A.

**P4-2. K-TSEL-1 (learner-chosen composition targets).**
**P4-3. K-TSEL-2 (no oracle shortcut).**

Need Track A complete (the reuse signals the selector reads do
not exist without query-time MAP execution) AND Phase 1 H2
results recorded (per the treadmill warning, target selection is
Step 4 work). K-TSEL-1 and K-TSEL-2 test the same policy from
two sides (history discrimination vs field-access discipline)
and are evaluated together.

**P4-4. K-T3-TOPO (learner-chooses-topology audit).**

Audits the diversity sets produced by K-T3-CON-1 (and
K-T3-REV-1). It does not gate individual world passes; it runs
with the mechanism bars, not before them. Order it alongside
P4-1 and P3-3.

**P4-5. K-T3-CON-2 (construction reuse, C0-D).**

Needs Track A complete (construction reuse via inlining requires
promoted graphs to be executable components; K-REUSE-1 makes MAP
execution observable). Independent of the H2 gate.

**P4-6. K-T3-INQ-4 (inquiry reuse and transfer, C0-D).**

Conceptually needs Track A (reuse requires the reused artifact
on a live read path). The inquiry reuse here is about
uncertainty/guide structures rather than MAPs, so the dependency
is architectural rather than mechanical; order it with Track A
complete.

Phase 4 ordering summary: P4-1 needs the H2 gate; P4-2/P4-3
need Track A plus the H2 gate; P4-4 rides with P4-1 and P3-3;
P4-5 and P4-6 need Track A. P4-1, P4-2/P4-3, P4-5, P4-6 are
parallel once their gates clear.

### Integration: cross-mechanism bar (rides the sealed battery)

**PX-1. K-XMECH (graceful cross-mechanism interference).**

Integration-level. It "can be evaluated in the same battery as
the mechanism bars; it does not need to wait for them to pass."
It is only meaningful once the individual mechanisms exist
(construction output, inquiry resolution, revision), so include
its interference worlds in the K-T3-ADV battery from the start
and evaluate it alongside Phase 3 and Phase 4. It needs no
separate evaluation infrastructure. Parallel with everything
from Phase 3 onward.

---

## 2. Parallel vs sequential: the complete map

**Fully parallel (no ordering constraints among them):**

- Phase 1: K-H2-1, K-H2-2, K-H2-3, K-H2-4, K-STATE-RET (audit).
  All five can start immediately and independently.
- Phase 2: Track A (K-REUSE-1, K-REUSE-2) vs Track B (K-H3).
  The two tracks share nothing.
- Within Track A: K-REUSE-1 vs K-REUSE-2.
- Within Track B: the three policy-node discrimination tests.
- Phase 3 groups: (K-T3-INQ-1, K-T3-INQ-3) vs (K-T3-REV-1,
  K-T3-REV-2, K-T3-REV-3) vs (K-T3-INQ-2), once Track B is done.
- Phase 4 (gates cleared): K-T3-CON-1 vs K-TSEL-1/2 vs
  K-T3-CON-2 vs K-T3-INQ-4.
- K-XMECH: parallel with all of Phase 3 and Phase 4.

**Strictly sequential (must wait):**

1. K-T3-ADV before any sealed-world bar. (Process gate.)
2. Phase 1 H2 results recorded before Phase 4 begins.
   (Treadmill guard. This is the roadmap's binding constraint.)
3. Track B (K-H3) before all Phase 3 bars. (Revisability
   precondition.)
4. Track A (K-REUSE-1/2) before K-TSEL-1/2 and K-T3-CON-2.
   (Signal-existence precondition.)
5. Track A before K-T3-INQ-4. (Architectural precondition.)

**Critical path.** The longest dependency chain is:

K-T3-ADV (P0) -> K-H3 (P2B) -> Phase 3 mechanism bars ->
K-TSEL-1/2 (P4, also needs Track A).

The H2 probes (Phase 1) and the reuse path (Track A) are off
the critical path: they run in parallel and their only role as
gates is that Phase 1 results must be recorded before Phase 4,
and Track A must finish before the bars that consume its
signals.

---

## 3. The 2 future-generation bars: triggers

### K-COMP-OP (learner-originated composition operators)

**Status:** Explicit non-claim for the minimal TNN-3. Drafted
with teeth for a future generation.

**Trigger:** A future generation claims that its composition
operators (the ways of combining graphs: splice, chain,
substitute, or successors) are learner-originated rather than
researcher-authored. The bar gives that claim a concrete test:
a passing composed graph whose combination topology is not
producible by any operator in the builder's fixture log.

**Preconditions (must hold before this bar is attempted):**
K-REUSE-1 must pass (composition needs executable MAPs as
operands) and K-TSEL-1/2 must pass (operand selection must
already be learner-driven, or operator novelty is confounded
with operand novelty).

**Predicted TNN-2:** FAIL by absence (no composition operators
at all). The bar is untestable against the frozen build, which
is expected: it targets a future claim, not TNN-2.

### K-INQ-INFO (informativeness-ranked inquiry)

**Status:** Explicit non-claim for the minimal TNN-3. Drafted
with teeth for a future generation.

**Trigger:** A future generation implements an informativeness
criterion for ranking candidate inquiries on non-dominated
uncertainties (worlds where no single guide dominates by
adversarial design, so K-T3-INQ-3's dominance test does not
apply).

**Preconditions (must hold before this bar is attempted):**
K-H3 must pass (the guide policy must be revisable for rankings
to vary across histories) and the Step 3 inquiry resolution path
must exist (without resolution, informativeness has no
observable consequence).

**Predicted TNN-2:** FAIL (constant action 30, constant content
-999, no ranking, no uncertainty-resolution path).

---

## 4. The 1 audit-grade bar: when to run it

### K-STATE-RET (structure retention)

**Placement:** Audit-grade preferred, per the kill-bar review
(`eb354e3a2`) recommendation adopted by the prereg structure
(`206499c03`, section 5a gap 5). The gap-bars draft provides
both formulations; Micah decides the final placement.

**When to run it:** As a governance audit probe, alongside the
sealed evaluation battery, not as a generation-gating kill bar.
It has no dependencies and can be run at any time, including
right now against frozen TNN-2 to establish the baseline
(predicted FAIL: rejected candidates evaporate; only verdict
counts survive).

**What it detects:** The verdicts-without-structures pattern:
trials that record how many candidates were rejected but retain
none of the rejected structures themselves. The audit reports
the retained-to-rejected ratio; no frozen pass/fail threshold is
needed for the diagnostic use. If Micah instead places it as a
bar, the bar-grade formulation (three genuine rejections,
signatures recoverable, functional reference by a later
inquiry/revision, 3/3 byte-identical) applies.

**Relationship to the battery:** It complements K-T3-TOPO
(TOPO governs passing structures; STATE-RET governs rejected
ones) and K-T3-INQ-4 (which partially covers guide retention).
Run it on every evaluation; it is cheap and it catches the
failure mode before it becomes a bar failure in a later
generation.

---

## 5. Summary table

| Phase | Bars | Gates | Parallel with |
|---|---|---|---|
| P0 | K-T3-ADV | None | Nothing (first) |
| P1 | K-H2-1, K-H2-2, K-H2-3, K-H2-4, K-STATE-RET (audit) | None; runnable now | Each other |
| P2A | K-REUSE-1, K-REUSE-2 | None | P2B, P1 |
| P2B | K-H3 | None | P2A, P1 |
| P3 | K-T3-INQ-1, K-T3-INQ-3, K-T3-REV-1, K-T3-REV-2, K-T3-REV-3, K-T3-INQ-2 | P2B complete | Each other (3 groups), PX-1 |
| P4 | K-T3-CON-1, K-TSEL-1, K-TSEL-2, K-T3-TOPO, K-T3-CON-2, K-T3-INQ-4 | P1 results recorded; P2A for TSEL/CON-2/INQ-4; P2B for all | Each other, PX-1 |
| PX | K-XMECH | Mechanisms exist (P3/P4) | P3, P4 |
| Future | K-COMP-OP | K-REUSE-1 + K-TSEL-1/2 pass; future claim | n/a |
| Future | K-INQ-INFO | K-H3 pass + Step 3 resolution; future claim | n/a |
| Audit | K-STATE-RET | None; run every evaluation | Everything |

Count check: 1 + 4 + 2 + 1 + 6 + 6 + 1 = 21 minimal bars.
Plus 2 future plus 1 audit = 24 total. Matches the inventory.

---

## Verdict

BAR-PRIORITY-COMPLETE.

Prioritization only. DRAFT-NOT-FROZEN. No new bars, no bar text
modified, no implementation, no source edits. All 24 bars remain
DRAFT-NOT-FROZEN pending Micah's review of the 6 open questions,
the signature-function decision, and the K-STATE-RET placement
decision. This ordering governs nothing until a TNN-3
preregistration freezes the bars it covers.

*End of prioritization. No source modified. No scores claimed.
Paper untouched.*
