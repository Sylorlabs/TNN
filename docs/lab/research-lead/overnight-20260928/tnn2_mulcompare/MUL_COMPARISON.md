# TNN-2 vs MUL Rung B: Construction Comparison

Date: 2026-10-01. Comparator: TNN-2 vs MUL Rung B Comparator (analysis only).
Verdict: MUL-COMPARISON-COMPLETE.

Read-only sources: MUL Rung B build report and `mul1b.zag` @ `a2223cc11`;
MUL Rung B prereg @ `3ce154801`; TNN-2 build report and `tnn2.zag` @
`f4de7ff46`; TNN-2 prereg @ `7c1e30522`; construction red team report
(`tnn2_redteam_construction/CONSTRUCTION_REDTEAM.md`).

## 1. What MUL Rung B actually demonstrated

MUL Rung B (builder commit `a2223cc11`, MUL1B-BUILD-PASS, 8/8 tests,
3/3 byte-identical) demonstrated two-level learner construction with a
researcher-supplied composition operator.

Phase 3a (ADD): from the basis {MOVE, BRANCHEQ, INC, DEC} with no core
ADD anywhere in the search or execution path (K3 purity verified by
source scan), the learner ran a fixed trial order, length-first
lexicographic odometer search over cell codes 0..4 plus GOTO(t)
(alpha = 5+L). After 19,475 trials and 87 genuine rejections it
promoted `[COPY_RX INC_R DEC_Y TEST_Y0 GOTO(1)]` at L=5, materialized
as learner-owned workspace PROC nodes 0..5. Held-out: 8/8 probes plus
scaling (47,53)->100.

Phase 3b (MUL): the Phase 3b search alphabet was extended by one
researcher-authored code, CALL_ADD (search code 2, workspace op 8),
whose semantics is "EXECUTE the learner-owned ADD PROC with (r, x),
store in r". After ~127,000 trials (L=1..5 exhausted, found at L=6)
and 13 genuine rejections it promoted
`[INIT_R0 INIT_I0 TEST_Y0 CALL_ADD INC_I GOTO(2)]`, materialized as
PROC nodes 6..12. Held-out: 8/8 probes plus scaling (13,17)->221 with
17 nested ADD CALLs. Two-level ablation: destroying ADD nodes 0..5
kills both ADD and MUL probes; destroying MUL nodes 6..12 leaves ADD
intact. Transfer: rectangle area (6,7)->42 in a novel surface encoding
with 7 nested ADD calls.

Phase 5 (revision): 0/4. The revision heuristic (argument swapping)
never addressed the y=0 divergence; the learner overfitted to y>0
exemplars. Documented as a failure of L3 criterion (12), not of the
construction claim.

What the researcher supplied (from the frozen prereg `3ce154801`,
section 2): the CALL operator itself ("one generic composition
move: CALL(proc_root, arg_slots, out_slot)"), the phase order (ADD
first, then MUL), the search alphabets, and the length bounds. What
the prereg explicitly marked as the learner's discovery: the decision
to use CALL at all, its position in the program, the argument wiring
(r,x)->r, the loop shape, and TEST placement. The prereg is candid:
"At MUL-construction time the only PROC in the workspace is the
learner-built ADD, so CALL in practice invokes ADD". CALL target
selection was therefore trivial; there was exactly one possible
target. Nothing in the experiment required the learner to choose among
multiple candidate procedures.

Honest summary: MUL Rung B is strong L2 evidence of hierarchical
reuse (a promoted learner structure invoked as a component by a
later-promoted structure), but the composition operator was
researcher-authored per the frozen design, the search was finite
(alpha^L odometer enumeration), and revision failed. It did not
demonstrate invention of a composition operator.

## 2. What TNN-2's t2_trial does instead

`t2_trial` (tnn2.zag, miss policy) is propose/execute/verify/promote
over exactly three researcher-written assemblers, per the
construction red team report:

- Family A, `t2_asm_chain`: linear (GUARD -> SETREG) pairs assembled
  from BFS paths (depth 1..4, 96-path cap) gathered by `t2_gather`.
- Family B, `t2_asm_sum`: unrolled INC runs from subset sums of direct
  values. Dead in production: gated by `comb_present(W) >= 0`, which
  requires a type-8 node that only test `t_p2` creates. No cognitive
  path can reach it.
- Family C, `t2_asm_count`: (GUARD -> SETREG -> INC) per link plus a
  MOVE epilogue.

The frozen 4-op ISA is tag 101 MOVE, 102 BRANCHEQ, 103 INC, 104 DEC,
run by the single frozen `execute` (byte-identical to the TNN-1 base).
There is no CALL tag, no MAP/graph-node reading anywhere in the
proposal path, no call stack in the executor, and DEC is never emitted
by any assembler. Verification is `t2_try_verify`: execute the
candidate and accept iff output equals the environment-supplied
`expected` (unmasked mode; masked mode never engages in the freeze
protocol since flags=0). Promoted graphs become type-20 MAP nodes with
field20 = graph root and provenance DEP edges.

So the concrete difference: MUL Rung B's Phase 3b grammar contains a
composition operator whose operand is a previously promoted
learner-owned graph; TNN-2's proposal grammar contains no operator
whose operand is a previously promoted graph. TNN-2 never reuses
promoted graphs as components.

## 3. Why t2_trial does not use recursive composition

Three layers, in causal order:

(a) Prereg scope. The frozen TNN-2 prereg (`7c1e30522`) specified
"integrate the MUL Rung B trial loop (propose/execute/verify/promote)"
as the pattern to import, not the two-level CALL composition. Kill bar
K-T2-3 ("every miss-path executable structure is constructed at
runtime through the trial loop") is satisfiable without any
composition. The omission happened at preregistration, before the
builder wrote code; the builder then satisfied the prereg as written.

(b) ISA freeze. A CALL cell tag would be a new opcode, and the prereg
freezes the ISA with falsifier F-T2-1 (no new opcode/mode/bridge/
handler/semantic case). The natural MUL Rung B route (add op 8 to the
executor) was therefore closed to the builder without violating the
freeze.

(c) Architectural friction for the freeze-compatible route. Inlining
(copying a promoted graph's cells into a new candidate) needs no new
opcode, but nothing in the architecture supports it: the assemblers
never read MAP nodes; the frame contract initializes only slots 0 and
1 (`t2_exec`), so spliced subgraphs need slot remapping; `execute`
has no call stack, so true nested invocation is impossible and only
inlining works; and the verifier's expected-answer protocol gives the
proposal policy no reason to prefer composed candidates over flat
ones. The builder would have had to invent a composition proposal
policy from scratch, with no kill bar rewarding it.

Conclusion: primarily a prereg-scoping and builder choice operating
under constraints that neither required nor rewarded composition;
secondarily a genuine architectural gap (no in-ISA calling
convention, no graph-operand proposal policy, no multi-MAP target
selection).

## 4. Could t2_trial be modified to compose previously promoted graphs?

Yes, without a new opcode, via inlining. The concrete change list:

1. Graph reader: given a MAP node, retrieve its graph root
   (field20) and walk cells via SEQ/BRANCHEQ edges. The walk already
   exists in skeletal form: `t2_sig` walks SEQ plus BRANCHEQ
   true-targets recording (tag, literal) per cell.
2. Splicer: copy the walked cells into a fresh candidate graph with
   slot remapping (promoted graph's working slots mapped to fresh
   frame slots, or sequential composition where graph G1's output
   slot feeds G2's input slot). `t2_exec` would need to initialize
   slots beyond 0 and 1; `fr_set`/`fr_get` already exist, so this is
   mechanical but it changes the frame contract.
3. Composition proposal policy: for example, for each promoted MAP in
   reverse promotion order, try sequential composition with each
   chain candidate and substitution of one chain link. Enumeration
   order, depth cap, and per-trial budget would be researcher-fixed
   unless derived from learner state (see section 6).
4. Verifier and promotion unchanged: execute, compare, count genuine
   rejections, promote via `promote_graph`.

What must not change (frozen constraints): no new cell tag (ISA
freeze); the single executor rule K-T2-2. Note the trap: MUL Rung B
implemented CALL with separate executors (`run_add`/`run_mul`,
`ws_exec_add`/`ws_exec_mul`); importing that structure naively into
TNN-2 would violate the one-executor rule. Inlining keeps `execute`
untouched.

The hard part is not mechanical but semantic: the selection policy.
With many MAPs accumulated, which graphs should be composed, in what
order, under what bound? MUL Rung B never solved this because only
one PROC existed. A researcher-fixed policy ("try each promoted MAP
once, head-position, after chains fail") is a larger menu over a
history-dependent pool. A learner-driven policy (selection among
candidate compositions guided by verification history or uncertainty
state) is a further, currently undesigned step.

## 5. Relationship between MUL Rung B's CALL and TNN-2's 4-op ISA

Compatible in concept, incompatible in the frozen letter.

Concept: MUL Rung B's base cell ops are the same computational basis
under different names (INIT/COPY = MOVE, TEST = BRANCHEQ, INC, DEC,
GOTO = SEQ back-edge). CALL is exactly nested EXECUTE: invoke a
learner-owned graph with an argument frame, take its result. TNN-2's
protected primitive `EXECUTE(root, frame)` is the same operation
invoked from outside a running graph (by `t2_exec` and by the revision
operator's re-execution). Both systems promote to learner-owned
persistent graphs with provenance. Both are pure Zag. At the level of
"what the machinery means", CALL is the missing in-graph form of an
already-approved primitive.

Frozen letter: TNN-2's ISA has four tags and `execute` is frozen
byte-identical to the base; adding CALL handling to `execute` is a new
opcode and a modification of the protected executor. The prereg
forbids both. Inlining (section 4) is the freeze-compatible route to
the same capability: the composed structure is bigger, but every cell
is one of the four frozen tags and `execute` never changes.

One asymmetry to keep: MUL Rung B's CALL target was unambiguous (one
PROC). In TNN-2, composition needs target selection among many MAPs,
which is a new decision the architecture has no policy for. That
decision is where learner authority could genuinely live, and it is
currently nobody's design.

## 6. Would recursive composition answer the construction red team?

It implements the red team's named remedy, and it changes the right
architectural property, but it does not by itself reach L3.

What it fixes: the constructible family becomes history-dependent.
With recursive composition, the set of buildable graphs grows with the
learner's experience: each promoted graph becomes a potential operand,
and composition of compositions yields unbounded depth. The family is
no longer enumerable from the source alone; the source plus the
learner's history is required. That is a genuine change in kind from
"finite researcher-enumerated family", and it is the specific
generative property MUL Rung B demonstrated standalone.

What it does not fix: the composition operators themselves
(splice/chain/substitute), the slot-remapping rules, the proposal
order, and the bounds remain researcher-authored. Against Micah's
conjunctive C0: C0-A is partial (operand graphs are learner-created
persistent state; the operators are not); C0-B is partial (the
operator set is a finite fixed menu; the operand pool is open);
C0-D is the strongest gain, because reusing a promoted graph as a
component is exactly L3 criterion 8 (reused later) and feeds
criterion 9 (transfer). C0-C (multiple unforeseen forms) is
untested until sealed post-freeze worlds require novel compositions
the fixed operator set happens to express.

The "larger finite menu" objection therefore survives at the operator
level: recursive composition converts a finite enumerable family into
a history-parameterized generative family, which is strictly more
open, but the ways of combining remain fixed. The skeptic's question
stands and should be asked of any TNN-3 proposal: what part of the
composition topology was actually chosen by the learner? The honest
answer for the inlining design is: which operand graphs, and their
arrangement within the researcher's operator set, but not the
operators. Moving the proposal/selection policy itself into learner
state (selection among candidate compositions driven by the learner's
verification history or uncertainty) is the next architectural step,
and per the no-patch-treadmill rule it should be designed as a
general mechanism, not bolted on per world. A new CALL opcode added
because one world needs it is rejected; a new mode, bridge, or router
for composition is presumptively rejected.

## 7. Bottom line for the research program

- MUL Rung B proved hierarchical reuse works: learner-built ADD
  called by learner-built MUL via a researcher-supplied CALL
  operator. Strong L2. Not L3 (operator authored, revision 0/4).
- TNN-2's prereg imported the trial pattern but dropped the
  composition operator, and the ISA freeze closed the CALL route.
  The result is generate-and-test over a finite family, as the
  construction red team found (CONSTRUCTION-ATTACK-SUCCESS).
- The missing piece is a freeze-compatible composition mechanism
  (inlining, not a new opcode) plus, harder, a target-selection
  policy for choosing among accumulated MAPs. The selection policy
  is the underexploited site of learner authority: it is the one
  decision MUL Rung B never had to make and TNN-2 has no design for.
- Recursive composition is worth building, but it should be judged
  as a history-parameterized generative family, not as L3, until
  the operators or the selection policy themselves show learner
  origin. The post-freeze adversarial battery is the right place to
  test whether fixed composition operators suffice for genuinely
  new structures or whether they fail exactly where the red team
  predicts.
