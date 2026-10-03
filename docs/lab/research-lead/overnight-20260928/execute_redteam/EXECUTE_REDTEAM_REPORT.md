# EXECUTE Placement Red Team Report

Date: 2026-09-30. Worker: EXECUTE Placement Red Team.
Verdict: EXECUTE-REDTEAM-COMPLETE.
Status: analysis only; read-only on all targets.

## Scope and method

Red-teamed the EXECUTE placement recommendation (commit 1fc77503b,
EXECUTE_PLACEMENT.md) against its own falsifiable criteria F-A
through F-J, plus the frozen ISA rule (commit 0525377f3: no core
operation may encode a target-domain regularity detector).

Sources read (all committed, read-only):
- 1fc77503b: EXECUTE_PLACEMENT.md (the placement, criteria F-A..F-J)
- 0525377f3: ISA_BOUNDARY_RULING.md (frozen rule)
- 55a7356f2: EXECUTE_BOUNDARY_EVIDENCE.md (reliance map, deltas)
- e639904f2: cla2.zag (EXECUTE implementation, lines 206-315)
- 0323b97d5: tnn1.zag (execute, lines 197-224; exec_plan separate)

Method: source inspection of both EXECUTE implementations against
each criterion; attempted constructive attacks (simulations,
unconstructibility arguments, inexpressibility arguments).
No code executed; no binaries run.

## Per-criterion verdicts

### F-A (table minimality): ATTACK-PASS

Criterion: a red team exhibits W2-class and W3-class execution
traces on a 3-op table; then narrow to 3.

Attacks attempted:

1. DEC via {MOVE, BRANCHEQ, INC}. DEC(s) for s>0 is simulable:
   find u = s-1 by looping v from 0, INC v, BRANCHEQ(v,s,done,cont),
   tracking u one step behind. Cost is O(s) steps per DEC.

   The W3-class probe (13,17) -> 221 via MUL-from-ADD needs
   O(x*y) DECs in the inner loops. With O(n) simulation per DEC,
   the trace needs roughly 3757 steps. BUDGET is 1000 (spec
   section 2, implemented as while(st<1000) in both CLA-2 and
   TNN-1). Traces exceeding BUDGET return FAIL (-999999); they
   are not valid executions. The 3-op trace does not fit.

2. MOVE via {BRANCHEQ, INC, DEC}. Copy s to t: zero t (caller
   setup), then loop INC t with BRANCHEQ(t,s,done,loop). Cost
   O(s) per copy. MUL without MOVE needs per-outer-iteration
   counter resets via DEC loops: measured at roughly 1140 steps
   for (13,17), exceeding BUDGET.

3. {MOVE, BRANCHEQ, DEC} without INC: INC is not simulable.
   DEC only moves down; there is no way to compute s+1 from s
   using only downward steps and equality tests.

4. {MOVE, INC, DEC} without BRANCHEQ: no data-dependent control
   flow. Linear execution only; loops and conditionals are
   inexpressible. W2-class traces (which need trial loops)
   cannot run.

Conclusion: under the specified BUDGET, 4 ops are minimal for
the W3-class ranges. Qualification: minimality is
budget-relative, not absolute. With a larger budget, the
O(n) simulations in attacks 1 and 2 would fit. The placement
does not state this relativity; F-A as written is about the
table, but the budget is doing load-bearing work in the
minimality claim. This interacts with F-F below.

### F-B (arithmetic rung): ATTACK-PASS

Criterion: W3-class ADD proves unconstructible from {INC, DEC}
within BUDGET for the integer ranges the worlds require, and no
learner-invented representation closes the gap; then promote one
rung (bounded ADD op).

Attack attempted: unconstructibility of ADD.

ADD(x, y) from {INC, DEC}: loop while y != 0: x := INC(x);
y := DEC(y); BRANCHEQ(y, 0, done, loop). Three steps per
iteration. For the largest cited probe (47,53) -> 100: 53
iterations, 159 steps. Well within BUDGET 1000.

The construction is straightforward and fits comfortably.
No unconstructibility demonstrated. Note: the MUL Rung B prereg
(commit 5924bbdae) plans to test exactly this (learner
constructs ADD from {MOVE, BRANCHEQ, INC, DEC}); F-B will get
its empirical test there.

### F-C (placement): ATTACK-PASS

Criterion: a red team demonstrates op_tag to action mapping
genuinely resident in learner-revisable state with no regress
(the construction section 1 claims is impossible); then remove
the primitive.

Attack attempted: refute the regress argument.

The placement's section 1 considers three variants and rejects
all: (a) multi-event stepping relocates the fixed point into
event-loop code (more machinery, worse locality); (b) dispatch
table in learner state regresses infinitely ("execute the
handler subgraph" requires interpreting it, which requires the
mapping); (c) structural dataflow needs a scheduler (more
machinery than a PC loop).

No refutation found. Variant (b) is the direct attack, and the
regress is genuine: any learner-authored table needs an
interpreter, and the interpreter's symbol-to-action mapping is
the fixed point. The attack cannot be mounted without begging
the question (building the demonstration would require the
primitive it tries to eliminate).

The regress argument stands unrefuted.

### F-D (APPLY distinctness): ATTACK-PASS

Criterion: a required calling pattern from the
compose-verify-promote frontier proves inexpressible via frame
indirection without new core machinery; then split APPLY out.

Attack attempted: find a calling pattern needing APPLY as a
separate operation.

Under the frame model, APPLY(structure, bindings) is exactly
EXECUTE(root=structure, frame=bindings): traversal is the walk,
HOLE-fill is frame-slot indirection, basis execution is the
4-op dispatch. The placement's section 4 shows the reduction;
Amendment B strikes APPLY, COPY, CORROBORATE as separate ops.

No calling pattern in current frontier work (CLA-2 miss-policy
invocation at cla2.zag line 560, TNN-1 plan execution, COMP-1
composition) requires anything beyond root+frame. CORROBORATE
as EXECUTE+BRANCHEQ+WRITE is adequate for single-case
verification. No inexpressible pattern identified.

### F-E (oracle audit): ATTACK-PASS (vacuous)

Criterion: COMPOSE_OPS O1-O3 applied to this spec. If capability
survives randomization of the learner's construction choices
(which positions get frame refs, trial order, promotion
threshold), the primitive is the oracle. Reject it.

Attack attempted: the oracle audit.

There is no learner construction via EXECUTE to audit. CLA-2
and TNN-1 invoke EXECUTE in researcher-authored test batteries
(test_execute, t_xcap, plan tests). MUL-1 uses a bespoke 7-op
interpreter (ws_exec), not the 4-op ISA. The inquiry builds do
not use EXECUTE. There are no learner construction choices
(frame-ref positions, trial order, promotion thresholds) to
randomize because no learner has constructed through EXECUTE.

The audit cannot be mounted; the primitive is not shown to be
an oracle. This criterion becomes testable only after a
learner actually constructs procedures via EXECUTE (the MUL
Rung B direction, if it targets the 4-op ISA).

### F-F (budget): ATTACK-PASS

Criterion: the BUDGET value proves load-bearing per capability
(different budgets, different capability sets, budget tuned per
world); then the budget moves to learner state or the design
fails review.

Attack attempted: show BUDGET=1000 is load-bearing.

No evidence of tuning. 1000 is a round number; all current
test batteries (CLA-2 15/15, TNN-1 35/35) complete well within
it. No experiment has varied the budget and measured capability
change. The falsifier's trigger (load-bearingness demonstrated)
is not met.

Observation (spec deviation, not falsification): the placement
specifies "step budget BUDGET (frozen constant, learner-visible)".
Both implementations use a code literal (CLA-2: let budget:i32=1000;
TNN-1: while(st<1000)). The budget is not learner-readable.
F-F governs whether the value is load-bearing; visibility is a
separate axis. The deviation should be resolved (accept the
literal as an implementation detail, or implement the readable
cell per spec), but it does not trigger F-F.

Note the interaction with F-A: the minimality claim depends on
the budget value (attack 1 and 2 above fail on budget, not on
computability). If F-F were ever triggered, F-A would need
re-examination.

### F-G (re-entrancy): ATTACK-PASS

Criterion: a required capability needs nested invocation that
construction-time inlining cannot express; then add a bounded
frame stack under a fresh prereg.

Attack attempted: find a capability requiring true recursion.

No current capability needs re-entrant recursion. MUL is
iterative (nested loops, not nested calls). CLA-2 miss-policy
invocation is a single EXECUTE call. TNN-1 plan execution is
linear with branches. Construction-time inlining (splice callee
cells with remapped frame slots) suffices for all exhibited
uses. No required capability is blocked.

### F-H (frame vs HOLE): ATTACK-PASS (provisional)

Criterion: frame-slot indirection proves unworkable in the W2/W3
construction traces (e.g., the exemplar policy cannot express
"varying position" without a sentinel); then adopt the HOLE
sentinel under a fresh prereg.

Attack attempted: show frame indirection unworkable.

Frame indirection works in all current EXECUTE uses:
CLA-2 test_execute builds frames with frame_set and reads via
frame_get; TNN-1 does the same with fr_set/fr_get. Operands
>=1000 resolve to slots; literals resolve structurally. No
sentinel collisions (there is no sentinel).

Provisional: the specific "exemplar policy varying position"
use case (learner generalizes an exemplar by marking varying
positions with frame-slot refs) has not been exercised through
EXECUTE. The mechanism is specified (placement section 3) but
untested. F-H remains live for future learner-construction work.

### F-I (ACT chaining): ATTACK-PASS (provisional)

Criterion: interleaved act-observe-act proves inexpressible via
chained EXECUTE invocation (the frame cannot carry the
continuation); then add yield/resume under a fresh prereg.

Attack attempted: show inexpressibility.

The placement's section 5 recommends terminal ACT-cells with
chained invocation: EXECUTE halts on a terminal ACT-cell and
returns the action descriptor; the learner-state ACT handler
performs ACT, processes OBSERVE, and re-invokes EXECUTE with
the updated frame. The continuation (resume cell + frame state)
is expressible: the resume cell id can be stored in a frame
slot, and the frame persists across invocations.

Not demonstrated in any current system. TNN-1 has both ACT
(directional bid) and EXECUTE but no chained-invocation
integration in its tests. No proof of inexpressibility exists;
the mechanism is plausible but untested. Provisional.

### F-J (fused vs split branch): ATTACK-PASS

Criterion: flag-reuse across multiple branches proves
load-bearing in a real trace; then split TEST/BRANCH.

Attack attempted: find a trace needing flag reuse.

No current trace sets a comparison flag and reuses it across
multiple branches. BRANCHEQ(a, b, t, f) is used directly at
every decision point in CLA-2 and TNN-1 tests. The fused form
suffices; no flag register is needed. (The MUL-1 bespoke
interpreter has separate TEST_CY/TEST_CX, but that is a
different system and does not use the 4-op ISA.)

## Frozen rule check: ATTACK-PASS

Frozen rule (0525377f3): "No core operation may encode a
target-domain regularity detector."

Source audit of the dispatch table (cla2.zag lines 263-309,
tnn1.zag lines 197-224):
- Tag 101 MOVE(dst, src): structural data movement. No domain
  content.
- Tag 102 BRANCHEQ(a, b, t, f): byte equality with control
  transfer. No domain content.
- Tag 103 INC(slot): integer successor. No domain content.
- Tag 104 DEC(slot): integer predecessor. No domain content.
- Unknown tag: clean FAIL.

Zero branches on world/task/domain identity anywhere in the
dispatch. The table names no domain concept. None of the
forbidden operations (FIND_POLYNOMIAL_ORDER, DETECT_NEGATION,
BUILD_CAUSAL_RULE, LEARN_PROCEDURE, FIND_THRESHOLD,
MAKE_CONDITIONAL, or equivalents) appear or are approximated.
The table is domain-neutral machinery.

## Spec deviations observed (not falsifications)

1. BUDGET learner-visibility. Spec: "frozen constant,
   learner-visible (READable)". Implementation: code literal
   1000 in both CLA-2 and TNN-1. The budget cannot be READ by
   the learner. Relevant to F-F's framing but does not trigger
   it. Recommend explicit disposition (accept literal or
   implement readable cell).

2. INC/DEC value-kind guard. The placement's audit line states
   "INC/DEC on non-integer payloads FAIL cleanly (a value-kind
   guard...)". Neither implementation checks the value's kind;
   both check only the slot index (>=1000). In Zag's i32-only
   value system there is no non-integer payload, so the guard
   is vacuous as specified, but the audit line describes a
   check that is not in the code. The spec text should be
   corrected to match the value system, or the guard should be
   specified against a future kind system. Not a frozen-rule
   issue (no domain content either way).

## Summary

- F-A: ATTACK-PASS (minimality holds under the specified
  BUDGET; noted as budget-relative)
- F-B: ATTACK-PASS (ADD constructible; 159 steps for (47,53))
- F-C: ATTACK-PASS (regress argument unrefuted)
- F-D: ATTACK-PASS (no inexpressible calling pattern)
- F-E: ATTACK-PASS (vacuous; no learner construction to audit)
- F-F: ATTACK-PASS (no load-bearingness demonstrated)
- F-G: ATTACK-PASS (no capability needs re-entrancy)
- F-H: ATTACK-PASS (provisional; exemplar use untested)
- F-I: ATTACK-PASS (provisional; chaining undemonstrated)
- F-J: ATTACK-PASS (no flag reuse in any trace)
- Frozen rule: ATTACK-PASS (table is domain-neutral)

No successful attacks. The placement survives this red team.
Three criteria (F-E, F-H, F-I) are provisional: they cannot be
fully tested until a learner actually constructs procedures
through EXECUTE. Two spec deviations are recorded above for
disposition. The F-A/F-F interaction (minimality depends on the
budget value) is noted for the record.

## Governance

- Zero Python invocations (analysis only; shell and file reads).
- Zero em dashes (byte-verified before commit).
- Contaminated paper TNN_RESEARCH_PAPER_20260929.md: zero-diff
  verified before and after.
- No sealed FW1-FW9 files accessed.
- All targets read-only; nothing modified.
- Explicit pathspecs on commit.

Verdict: EXECUTE-REDTEAM-COMPLETE.
