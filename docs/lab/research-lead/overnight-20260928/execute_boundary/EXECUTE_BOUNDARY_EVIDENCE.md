# EXECUTE Boundary Evidence Package

Date: 2026-09-30. Worker: EXECUTE Boundary Evidence Worker.
Status: EXECUTE-EVIDENCE-READY. For Micah's ruling.

## The question

Micah approved APPLY/EXECUTE as an allowed ISA class in the Protected
Core ISA Ruling. He did not explicitly approve the exact placement
recommendation in EXECUTE_PLACEMENT.md (commit 1fc77503b): the protected
core primitive EXECUTE(root, frame), the internal four-op ISA
{MOVE, BRANCHEQ, INC, DEC}, and amendments A-C. CLA-2 and TNN-1 were
implemented on top of that unapproved placement. This package states
what was approved, what was added, who relies on it, and the options.

## 1. What Micah explicitly approved (commit 0525377f3)

The ISA Boundary Ruling is a FROZEN ARCHITECTURE RULING. Exact quotes:

Acceptable core primitives (machinery, not intelligence):
"ALLOC, READ, WRITE, LINK, COPY, COMPARE/EQ, basic arithmetic
such as ADD, BRANCH, APPLY/EXECUTE, generic state/register
operations."

"These do not tell TNN what to think. They give it machinery
with which learner-created structures can think."

Frozen rule: "No core operation may encode a target-domain
regularity detector."

Approved package: "The integration coordinator's package (A1-A12)
is APPROVED with the above boundary added:
- 10 generic core operations
- MISS_POLICY register
- POLICY_ROOT register
- generic sentinel/state machinery
- trial-based P-DEP (finite-difference OUT)
- edge-derived standing
- zero modes/bridges/handlers"

What this approves: the CLASS "APPLY/EXECUTE" as domain-neutral
machinery, alongside the other ISA classes. What it does not specify:
the primitive's exact signature, its internal dispatch table, the
frame model, any step budget, or the strike-down of overlapping
operations (APPLY, COPY, CORROBORATE, HOLE sentinel).

## 2. What the placement recommendation adds (commit 1fc77503b)

EXECUTE_PLACEMENT.md is analysis only. Its own status line:
"Status: analysis only; recommendation to Micah for approval before
any core change. No implementation in this commit."

Its recommendation (section 6): "Add ONE primitive to the protected
core: EXECUTE(root, frame) -> value | FAIL" with:
- "Fixed loop over a closed 4-op dispatch table: MOVE(dst, src),
  BRANCHEQ(a, b, t, f), INC(slot), DEC(slot)."
- "Operands resolve to frame slots or literal cells, structurally."
- "Execution context {current, frame, steps}; step budget BUDGET
  (frozen constant, learner-visible); unknown op_tag and
  non-integer INC/DEC operand FAIL cleanly; halt on terminal cell;
  output via root ref[0]."
- "Frame allocated and bound by the caller with the six primitives.
  No HOLE sentinel. No arithmetic beyond INC/DEC. No yield/resume.
  ACT-cells are terminal; plans chain invocations."
- "Source audit line: the table names no domain concept; zero
  branches on world/task identity; the integer guard is a
  value-kind check only."

The load-bearing justification is the regress argument (section 1):
the op_tag to action mapping cannot live in learner state because
executing a learner-authored dispatch table requires interpreting
it, which requires the mapping, which is the table: infinite
regress. The regress "bottoms out only where some layer maps
symbols to actions directly, in code."

Amendment A (to PREREG_CLA2): add the seventh primitive with the
exact spec above.

Amendment B (to COMPOSE_OPS_SPEC): "APPLY is struck as a separate
operation and re-specified as the calling convention of EXECUTE
(root plus frame bindings). COPY is struck from the core op set;
re-specified as a learner library procedure. CORROBORATE is struck
from the core op set; re-specified as learner-level composition.
The HOLE sentinel (2.3) is struck; replaced by frame-slot
indirection."

Amendment C (to UNIFIED_STRUCTURES): "the op table {COPY, BIND,
COMPARE, BRANCH, EMIT, LINK-READ} is replaced by {MOVE, BRANCHEQ,
INC, DEC}."

The amendments section states: "These amendments are specified here
for Micah's approval. They authorize no implementation; the
implementation prereg follows approval."

## 3. What was implemented before approval

CLA-2 (commit e639904f2, message: "CLA-2 implementation: amended
prereg (A1-A12) + ISA ruling + EXECUTE A-C") implemented the seventh
primitive with the exact 4-op ISA. Its source comments cite the
unapproved document as authority:
- cla2.zag line 78: "EXECUTE op tags (closed 4-op ISA; Amendment A
  of EXECUTE placement)"
- cla2.zag line 207: "EXECUTE(root, frame) -> value | FAIL
  (Amendment A of EXECUTE placement)."

The CLA-2 builder's NAMECHECK.md states:
"Task: implement CLA-2 per frozen prereg 24351fd31 + integration
amendments A1-A12 (62e5ebb9f, ALL APPROVED) + ISA boundary ruling
(0525377f3, FROZEN) + EXECUTE placement amendments A-C (1fc77503b,
APPROVED)."

The "(1fc77503b, APPROVED)" annotation is false. The placement
document asks for Micah's approval; it does not record it. The
builder treated commit ancestry as approval: its standing rule 2
says the amendments "are all ancestors," verified by
git merge-base --is-ancestor. Ancestry is not approval.

Note: CLA-2's own frozen prereg (24351fd31) specified six
primitives (ALLOC, WRITE, LINK, READ, ACTIVATE, DECAY) with "No
execution primitive." The seventh primitive was added on the
strength of the unapproved amendments.

TNN-1 (commit 0323b97d5) ported CLA-2's execute. Its source
comment (tnn1.zag line 5) reads: "Seven primitives: ALLOC, READ,
WRITE, LINK, ACTIVATE, DECAY, EXECUTE." The implemented function
matches the placement spec:
- fn execute(W:[]u8,root:i32,fr:i32)i32 (EXECUTE(root, frame))
- closed dispatch on tags 101 (MOVE), 102 (BRANCHEQ), 103 (INC),
  104 (DEC); unknown tag returns -999999 (FAIL)
- step budget while(st<1000); halt on terminal cell; output via
  exec_val wrapper
- frame indirection via fr_get/fr_set; no HOLE sentinel

The integration prereg (7fc7148ac) was honest about the status:
"NOTE: Micah's explicit ruling on this placement remains pending;
the implementation uses it as a built candidate and this prereg
inherits that status. The prereg does not canonize the placement."

The TNN-1 red team (commit cbde38737) audited six vectors
(template smuggling, menu resurrection, line-count honesty,
integration genuineness, determinism, cross-suite interference).
Its report contains zero mentions of EXECUTE or the placement
boundary. The placement itself (falsifiable criteria F-A through
F-J in the placement doc) has never been red-teamed.

## 4. Which systems rely on the unapproved elements

Rely on the exact placement (EXECUTE(root, frame), 4-op ISA,
frame indirection, amendments A-C):
- CLA-2: primary implementer; source cites Amendment A.
- TNN-1: ports CLA-2's execute; 4-op dispatch; budget 1000.

Cite the placement as authority but do not implement EXECUTE:
- COMP-1: one comment, "MOVE/BRANCHEQ/INC per EXECUTE placement";
  no execute function.

Do NOT rely on it (verified by source grep):
- DEVINT-CLA2: zero matches for execute/EXECUTE.
- MUL-1: bespoke 7-op interpreter (ws_exec: ZERO_R, ZERO_C,
  ADD_X, ADD_Y, INC_C, TEST_CY, TEST_CX), not the 4-op ISA.
- Inquiry (both builds, including the clean re-freeze): zero
  matches; own event-driven mechanism.

## 5. Deltas between the placement spec and the implementation

(a) BUDGET learner-visibility. The spec: "step budget BUDGET
(frozen constant, learner-visible)". TNN-1: while(st<1000), a
code literal, not a learner-readable cell. The falsifiable
criterion F-F governs whether the budget is load-bearing; it has
not been tested.

(b) Primitive count naming. TNN-1's comment lists seven names
(ALLOC, READ, WRITE, LINK, ACTIVATE, DECAY, EXECUTE): consistent.
The builder's prose report enumerated six names while saying
seven: a documentation slip, not a source deviation.

(c) Otherwise the implementation matches the spec: closed table,
frame indirection, no HOLE sentinel, APPLY unified, clean FAIL
paths, no domain concepts in the dispatch.

## 6. Options and risks

Option 1: Approve the placement as implemented.
- For: the regress argument is the strongest justification
  offered for any core addition in this program; the 4-op table
  names no domain concept and satisfies the frozen rule on its
  face; implementations pass their test batteries (CLA-2 15/15,
  TNN-1 35/35); rejecting destroys CLA-2, TNN-1, and all
  downstream results for a boundary the analysis shows is
  minimal; any alternative the placement doc considered is more
  machinery, not less.
- Against: retroactively legitimizes building on unapproved
  amendments; the CLA-2 builder's false "(APPROVED)" annotation
  goes uncorrected unless recorded; the placement's own
  falsifiable criteria (F-A through F-J) were never tested;
  sets a precedent that implementing first and ruling later
  works.

Option 2: Approve with conditions.
- Conditions could include: (i) record the governance breach in
  the ledger (ancestry is not approval; the CLA-2 NAMECHECK
  annotation was false); (ii) require a placement-focused red
  team against F-A through F-J before any EXECUTE-dependent
  system is considered for SURVIVES or before the freeze rerun
  treats EXECUTE as settled; (iii) resolve the BUDGET
  learner-visibility delta (accept the literal or require the
  readable cell per spec).
- For: keeps the working implementations, repairs governance
  credibility, closes the untested-criteria gap.
- Against: delays the freeze rerun; the red team may find the
  table is not minimal (F-A) or the budget is load-bearing
  (F-F), forcing rework anyway.

Option 3: Reject the placement.
- For: strongest governance signal; enforces "approval before
  implementation" absolutely.
- Against: CLA-2 and TNN-1 lose their executor; the regress
  argument says the replacement is worse (dispatch hidden in
  event-loop code, more machinery by honest accounting);
  MUL-1, DEVINT-CLA2, and inquiry are unaffected, but the
  integration milestone (TNN-1) is voided and must be rebuilt;
  no evidence the rejection produces a better boundary, only a
  costlier one.

## 7. Recommendation

Approve the placement as implemented (Option 1), with two
recorded conditions borrowed from Option 2:

1. Record the governance breach. The CLA-2 builder's
   "(1fc77503b, APPROVED)" annotation was false and must be
   corrected in the ledger: commit ancestry verified by
   merge-base is not approval, and the placement document's own
   text ("for Micah's approval... authorize no implementation")
   was the controlling statement. The integration prereg's
   honest note ("does not canonize the placement") is the
   correct posture and should be the template.

2. Require the placement red team (F-A through F-J) before
   SURVIVES consideration of any EXECUTE-dependent system and
   before the freeze rerun. The criteria were written to be
   falsifiable; they should be falsified or survived, not
   skipped. This is the same standard applied to every other
   frontier mechanism in this program.

Justification: the regress argument is load-bearing and has not
been refuted; the 4-op table satisfies the frozen rule (no
target-domain regularity detector; the integer guard is a
value-kind check); the implementation matches the spec except
the BUDGET visibility delta, which F-F already covers. Rejection
would impose large rework costs without a better boundary on
offer, and the honest path for the one real deviation (the
premature build) is a recorded correction, not retroactive
invalidation of working, tested implementations.

The BUDGET delta: accept the literal-1000 as an implementation
detail for now; F-F requires the red team to test whether it is
load-bearing, and if it is, the budget moves to learner state or
the design fails review per the placement doc's own terms.

## 8. What this ruling would and would not settle

Would settle: EXECUTE(root, frame) over {MOVE, BRANCHEQ, INC,
DEC} is a legitimate seventh protected-core primitive; the
Amendment B strike-downs (APPLY unified, COPY/CORROBORATE to
learner level, HOLE replaced by frame indirection) stand; the
Amendment C table replacement stands.

Would not settle: whether the table is minimal (F-A), whether
ADD-from-INC/DEC reaches W3-class ranges (F-B), whether the
budget is load-bearing (F-F), or any of the other falsifiable
criteria. Those remain open and are the red team's job.

Freeze rerun dependency (flag 3 from the rerun plan): with this
ruling, the inherited ambiguity is resolved and TNN-1 can be
frozen without modification on this axis. Without it, any freeze
is provisional.

## Sources consulted (all committed, read-only)

- 0525377f3: ISA_BOUNDARY_RULING.md (Micah's frozen ruling)
- 1fc77503b: EXECUTE_PLACEMENT.md and NAMECHECK.md (analysis,
  amendments A-C specified for approval)
- 4e36f31f2: FREEZE_RERUN_PLAN.md (flag 3: inherited ambiguity)
- 7fc7148ac: PREREG_INTEGRATION.md ("does not canonize the
  placement")
- e639904f2: cla2.zag (lines 5, 78, 207), NAMECHECK.md
  (false "(APPROVED)" annotation, line 6)
- 0323b97d5: tnn1.zag (lines 5, 65-69, 170-220)
- cbde38737: TNN1_REDTEAM_REPORT.md (no EXECUTE coverage)
- Source greps: devint_cla2.zag (0), mul1.zag (bespoke
  interpreter), inquiry.zag both builds (0), comp1.zag (1
  comment)

## Verdict: EXECUTE-EVIDENCE-READY
