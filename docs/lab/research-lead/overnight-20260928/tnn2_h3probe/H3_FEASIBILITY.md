# H3 Feasibility Probe: Procedures as Learner-Built Graphs

Date: 2026-10-01. Prober session: 83064712-575d-441f-8a2e-b7533c139b3b.
Parent task: probe the feasibility of H3 from the red-team synthesis
(commit `42b4dfa91`).

**Framing, stated once and binding:** this document is analysis, not a
patch and not a TNN-3 proposal. It answers five feasibility questions
about H3 ("mechanisms' operating procedures are source code, not learner
state; fix = procedures as learner-built graphs"). Nothing here
authorizes implementation. Any TNN-3 work that follows must go through
its own preregistration with frozen kill bars. The probe's job is to
determine whether H3 is experimentally tractable and what its cheapest
discriminating test is.

Target under analysis: `tnn2.zag` at `f4de7ff46` (frozen), read-only.
All line numbers refer to that source.

---

## 0. What H3 claims, precisely

H3 (procedure-ownership hypothesis): the bottleneck is one level up
from H1. Even the procedures that fill the slots (the trial loop's
search order, the miss-to-guide pipeline, the tombstone/insert/rewire
sequence) are Zag source, not learner-constructed executable graphs.
C0-A fails in all three mechanisms for the same reason: the semantics
of how to construct, how to inquire, and how to revise reside in
researcher-authored code. The learner owns data and parameters; the
researcher owns every procedure.

H3's distinct, testable prediction: **no experience can revise the
mechanisms' policies.** That prediction is checkable against the frozen
source without building anything (see section 5).

The full H3 vision: the trial search policy, the guide-derivation
policy, and the repair policy are themselves constructed executable
graphs in learner state, bootstrapped from the protected ISA, executed
by the protected core. Then improving the constructor improves all
three policies at once, and three researcher-written mechanisms plus a
constructor collapse into one constructor plus three learner-built
policies (the mandated compression direction).

---

## 1. Can the 4-op ISA express "find stale SETREG, tombstone it, insert corrected step"?

### 1a. What the frozen ISA can and cannot do

The frozen ISA is four ops over frame registers, executed by the single
`execute()` at line 192:

- `MOVE` (101): copy a value into a frame slot. Source operand may be a
  frame slot (1000+n), a node index 0..999 (reads that node's field20
  only, via `res_op`), or negative (reads as 0).
- `BRANCHEQ` (102): compare two operands; jump to field12 target on
  equal, field16 target on not-equal (fails closed if it reaches a
  non-ISA cell).
- `INC` (103) / `DEC` (104): increment/decrement a frame slot.

The ISA's effect domain is **frame registers only**. It has exactly one
read bridge into the workspace (operand 0..999 reads field20 of a node)
and **no write bridge back**: `fr_set` writes frame slots, never nodes,
fields, or edges.

### 1b. What the revision procedure actually does

`t2_revise_graph` (lines 706-763) performs these structural operations,
all in Zag source, none expressible as ISA effects:

1. Scan all 4096 edge slots for ET_DEP (type 1) edges to the
   contradicted fact; take the source cell; require its tag to be 101
   (SETREG). Lines 711-717.
2. Scan all 1024 node slots for a BRANCHEQ cell (tag 102) whose field12
   equals the stale cell. Lines 719-724.
3. Allocate a literal node and a SETREG cell (`t2_lit`, `t2_set`); write
   fields 0/4/8/20. Lines 726-727.
4. Link a DEP edge from the new cell to the fact; rewire the guard's
   field12 to the new cell; seq-link the new cell to the successor;
   kill the stale cell's SEQ edge (`t2_kill_edge`). Lines 728-731.
5. Tombstone the stale cell: write tag 0 and active flag 0
   (`ns(W,stale,0,0); ns(W,stale,36,0)`). Line 732.
6. Re-execute the repaired root via `t2_exec`; on failure, undo every
   structural edit (lines 734-743); on success, contradict the old
   answer fact and teach the new one. Lines 744-761.

Steps 1-5 are mutations of the workspace graph store (node allocation,
field writes, edge link/kill, tombstoning). The ISA cannot perform any
of them: it cannot allocate a node, write a node field, link or kill an
edge, or deactivate a cell. Its only workspace interaction is a
read-only peek at field20.

### 1c. What the graph would look like, if the ISA had structural effects

For concreteness, here is the shape of "find stale SETREG, tombstone
it, insert corrected step" as a learner-built executable graph, under a
hypothetical ISA extended with structural ops (ALLOC, WF (write field),
LINK, KILL; these are named only to show the gap, not proposed):

- Input frame: slot0 = contradicted fact node n, slot1 = old_o,
  slot2 = new_o, slot3 = MAP node m.
- **Blame scan loop:** slot4 = edge cursor e (0..4095). Per iteration:
  read edge[e].from/.type/.to via structural reads; BRANCHEQ
  edge.type == 1; BRANCHEQ edge.to == slot0; read source cell tag;
  BRANCHEQ tag == 101; on match MOVE candidate <- edge.from; INC
  cursor; BRANCHEQ cursor < 4096 to loop.
- **Guard scan loop:** slot5 = node cursor; per iteration read tag;
  BRANCHEQ tag == 102; read field12; BRANCHEQ field12 == candidate;
  on match record guard.
- **Repair sequence:** ALLOC literal node; WF field20 <- slot2;
  ALLOC SETREG cell; WF fields; LINK DEP edge new-cell -> fact;
  WF guard.field12 <- new-cell; LINK SEQ new-cell -> succ;
  KILL SEQ stale -> succ; WF stale.tag <- 0; WF stale.active <- 0.
- **Verify branch:** EXECUTE repaired root on fresh frame (the
  APPLY/EXECUTE primitive from the protected-core ruling);
  BRANCHEQ result == -999999 to the revert block, which replays the
  inverse structural edits.

Every comparison and every register move in this sketch is expressible
in the frozen 4-op ISA. **Every structural step is not.** The sketch is
perhaps 40-60 cells; its control flow (two scan loops, one conditional
repair block, one revert block) is well within what BRANCHEQ + SEQ can
express. The blocker is purely the effect domain.

### 1d. The honest feasibility answer to Q1

No: the frozen 4-op ISA cannot express the revision procedure, because
the procedure's work is structural mutation of the workspace and the
ISA's effects are confined to frame registers. This is not a depth or
expressiveness limit in the computational sense; it is a missing effect
class.

Three ways to close the gap, with their costs stated plainly:

- **(a) Extend the ISA with structural ops** (ALLOC, WRITE field, LINK,
  KILL, edge/node READ). This is a protected-core boundary change: it
  grows the frozen computational basis. It is not benchmark-driven (no
  world requires it; H3 requires it), but under Micah's escalation rule
  a protected-core boundary change is his decision, not the loop's.
  Note the ISA ruling already lists ALLOC, READ, WRITE, LINK, COPY as
  the *allowed class* of protected-core machinery ("a small generic
  protected core + learner-created cognitive structures"); the frozen
  TNN-2 ISA contains none of the structural half. The ruling permits
  the class; the freeze fixed the instance. Reconciling those is
  governance work, banked, not decided here.
- **(b) A second executable graph type for structural procedures** with
  its own executor. This reintroduces exactly the two-graph-type
  problem the TNN-2 prereg eliminated (K-T2-2/K-T2-3 killed `exec_plan`
  vs `execute`). It would need a strong unification argument to survive
  the One-System Rule.
- **(c) H3-lite (section 4):** leave procedures in source, move their
  decision points into learner state. No ISA change, no new graph type.

The probe's finding: Q1's answer is "not with the frozen ISA; the gap
is precisely the structural effect class, and closing it is a
protected-core decision." That is a tractable, well-localized gap, not
a vague impossibility. H3 is feasible in principle; its cost is one
governance decision about the core boundary.

---

## 2. The bootstrap problem

If procedures are learner-built, what builds the first procedure? Four
candidate answers, in increasing order of radicalism:

**(a) A fixed minimal bootstrap builds the first procedure, then gets
out of the way.** The bootstrap is researcher-authored, small, and
generic: allocate cells, link edges, execute graphs. Its only job is to
enable the first learner-built procedure; after that, the learner's own
procedures (including procedures that revise procedures) take over.
C0-A still fails at the bootstrap level, and that must be stated
honestly rather than hidden. This is the standard bottom-turtle
resolution, and it is exactly parallel to MUL Rung B: the primitive
basis (INC/DEC/GOTO/TEST/CALL) was researcher-authored; ADD and MUL
were learner-built on top of it. Nobody demanded the learner invent
INC. The H3 claim would be scoped the same way: cognitive procedures
(search, repair, inquiry policies) are learner-built above a fixed
structural basis. The open empirical question is how small the
bootstrap can be while still enabling open procedure construction,
analogous to how small a Forth kernel can be.

**(b) Self-host from the existing trial loop.** `t2_trial` already is a
propose/execute/verify/promote loop. The H3-lite step (section 4) does
not replace it; it parameterizes it. The first "learner-built
procedure" in this path is not built ex nihilo but *derived*: the
learner's policy node starts as a copy of the researcher's default
order and is then revised by experience. Bootstrap = copy-then-revise,
not create-from-nothing. This dodges the philosophical bootstrap
entirely and is the cheapest experimental path.

**(c) The ISA is the bottom turtle by design.** Micah's protected-core
ruling already fixes a bottom: a small frozen domain-neutral
computational basis is machinery, not intelligence. H3 does not require
eliminating the bottom turtle; it requires that *cognitive* procedures
live above it in learner state. The regress stops at EXECUTE, which is
a deliberate architectural axiom, not a gap.

**(d) The worrying version: the procedure that builds procedures must
itself be learner-built, ad infinitum.** This is not required. What is
required is weaker and testable: that the learner can *revise* its
procedures from experience (the H3 prediction in section 0). Revision
of procedures does not need an infinite tower; it needs one
reflective level (a procedure that edits procedure graphs, executed by
the same core). The MUL Rung B analogy again: MUL calls ADD; nothing
calls the caller. One reflective level sufficed for hierarchical
construction; one reflective level (revise-the-reviser) suffices for
H3's testable claim.

**Probe assessment:** the bootstrap problem is solvable and already
partly solved by precedent. The MUL Rung B pattern (fixed basis, built
structure, CALL composition) is the template. The genuinely hard part
is not bootstrapping but the effect-domain gap in section 1: the
current basis lacks structural effects, so even the first
learner-built *structural* procedure has nothing to stand on. Fix the
effect domain (governance decision), and the bootstrap follows the MUL
pattern.

---

## 3. Can the MUL Rung B pattern extend to procedures?

### 3a. What MUL Rung B actually demonstrated

From the Rung B build report (`mul_rungb_build/BUILD_REPORT.md`):

- Phase 3a: learner-built ADD from the primitive basis (INC/DEC only;
  source scan confirmed zero occurrences of general addition in the
  Phase 3a/3b interpreters; `run_add` uses only `r=r+1`, `y=y-1`).
- Phase 3b: learner-built MUL as `[INIT_R0 INIT_I0 TEST_IY CALL_ADD
  INC_I GOTO(2)]`, invoking learner-built ADD via `CALL_ADD`.
- Held-out probes: (13,17) -> 221 correct with 17 nested ADD CALLs.
- Two-level ablation: ablating ADD nodes kills MUL (8/8 wrong) while
  ablating MUL nodes leaves ADD intact (8/8 correct). Genuine
  dependency, verified.
- The 0/4 revision result: the learner-built MUL could not be revised
  by the learner (per the frozen summary: "Its 0/4 revision result
  points toward the general revision problem").

### 3b. The structural analogy, and exactly where it breaks

What transfers directly:

- **Hierarchical composition via CALL.** A revision-procedure graph
  could CALL a blame-localization sub-procedure and a
  repair-application sub-procedure, each learner-built, each
  independently ablatable. The CALL-by-reference mechanism (invoke a
  learner-built graph by node index) is domain-agnostic; the Rung B
  evidence that composition works and that ablation verifies genuine
  dependency applies unchanged.
- **Basis-then-structure layering.** Fixed minimal basis, learner
  structure above it. H3's procedures would layer the same way:
  structural basis ops below, search/repair/inquiry policies above.
- **The 0/4 revision result reframes under H3.** MUL's construction
  procedure (the Phase 3b search that found the MUL graph) lived in
  researcher code, so there was no learner-owned procedure to revise;
  only MUL's literals were learner state. Under H3 the diagnosis is
  crisp: 0/4 is not a failure of revision machinery but evidence that
  procedure-ownership is the missing level. If the MUL-building
  procedure had been a learner-state graph, the revision target would
  have existed.

Where the analogy breaks:

- **Effect domain.** ADD/MUL operate on numeric registers, which is the
  ISA's native domain. Procedures operate on the workspace graph
  store, which is outside the ISA's effect domain (section 1). The
  Rung B pattern extends *structurally* (composition, ablation,
  layering) but the procedures need structural effects that the Rung B
  basis never had. This is the same gap as Q1, restated: hierarchical
  construction was demonstrated for computational procedures over
  registers, not for structural procedures over the graph store.
- **Search guidance.** Rung B's Phase 3b search had a numeric score
  (1..11 over candidate MUL graphs). A procedure-building search needs
  a score over *procedures*: does this repair policy fix more
  contradictions, does this search order find answers in fewer trials.
  That meta-score exists in principle (trial stats are already packed
  into header field 16; revision success/failure is a single bit per
  event) but no machinery consumes it. This is an instrumentation gap,
  not a fundamental one.

**Probe assessment:** the MUL Rung B pattern extends to procedures in
its compositional and layering structure, and its 0/4 revision result
is positive evidence *for* H3's diagnosis (the unrevisable thing was
the procedure, which lived in source). The extension is blocked only by
the structural-effect gap, which is the same single blocker as Q1. One
blocker, not two.

---

## 4. Minimal architectural change for learner-revisable procedures (H3-lite)

Full H3 (procedures as learner-built graphs) needs the governance
decision in section 1d. But there is a strictly weaker change that
delivers H3's *testable prediction* (procedures revisable by
experience) with no ISA change, no new graph type, no new mode:

**Pattern: parameterize every researcher-chosen decision point in the
three mechanism procedures as a read from a learner-state policy node,
and add one production path that updates the policy from experience.**

The procedure stays researcher-authored Zag code. Its degrees of
freedom move into learner state and become revisable. Concretely:

**Construction (`t2_trial`, lines 586-672).** The search order is
source literals: chains k=2..4 (line 593), then sums (line 605), then
counts (line 626), then single hops (line 647), with the
"composition-preserving" rationale in a comment (line 582). H3-lite:
a POLICY node (a small ordered list of family indices in learner
state) read at trial start; the loop nest dispatches on it. Update
path: when a family verifies, move it earlier in the order (a
Hebbian-style promotion already analogous to `ev_teach_in`); when a
family is tried and rejected beyond a learner-tracked count, demote
it. No new opcode; the policy is a node with edges, the update is
field writes on experience. This directly enables the H3
discrimination experiment: a world where chains-before-counts
systematically picks the wrong family first should, over trials,
flip the learner's order. Today that flip is impossible (section 5).

**Inquiry (`miss_inquire`, lines 795-812).** The guide's action (30)
and content (-999) are literals at line 808. H3-lite: read them from
a learner-state guide-template node, created on the first miss with
the current defaults, updated when evidence arrives about which
actions actually resolved uncertainty (the missing L6 link the
inquiry red team flagged). The update path is the resolution
procedure that does not yet exist; H3-lite forces its creation in
the smallest form: on any observation that contradicts an
uncertainty node, write the observed (s,r,o) into the template's
history fields and adjust the action/content toward actions that
preceded resolutions. Still researcher-authored update code; but the
*values* it writes are functions of experience, and the guide
content becomes revisable.

**Revision (`t2_revise_graph`, lines 706-763).** The repair topology
is a straight-line researcher sequence. H3-lite: a repair-policy
node selecting among the five repair topologies from the revision
generalization analysis (guard-predicate edit, branch rerouting,
multi-step repair, unroll/step-type conversion, deletion without
insertion). The operator dispatches on the policy value. Update
path: on verification success, reinforce the selected topology for
that blame signature; on failure (revert path, lines 734-743
already exists), demote it. The five topologies are still
researcher-enumerated (H1's concern is not addressed), but the
*choice among them* becomes learner-revisable, which is exactly the
revision red team's acceptance condition ("the SAME machinery can
derive structurally different repairs") at the policy level.

Why this is "not a patch": it fixes no world and improves no frozen
score. It changes the *locus of control* for mechanism behavior from
source literals to learner state, which is the shared architectural
cause the synthesis named. It is also the compression direction in
miniature: three hardcoded decision sites become three reads of
learner-state policy nodes, i.e., mechanism-specific source shrinks
while learner-state structure grows.

What H3-lite does NOT deliver (stated so it is not oversold): the
procedures themselves remain source; C0-A still fails at the
procedure level; the repair family remains researcher-enumerated
(H1 unaddressed); the acceptance oracle remains (H2 unaddressed).
H3-lite is the cheapest experiment that tests whether moving
*decisions* into learner state is sufficient for policy revision,
before paying the governance cost of moving *procedures* there.

---

## 5. Why H3 is the recommended first experiment, and the cheap check

### 5a. Why H3 first

The synthesizer's recommended order: (1) H3's cheap
policy-revisability check, (2) H2's masked verification probes, (3)
H1's constructor widening. Three reasons H3 goes first:

1. **Cheapest.** It is pure analysis of the frozen source. No new
   worlds, no implementation, no evaluation run. H2 needs masked
   probes (new sealed worlds); H1 needs constructor widening (new
   machinery, then re-running three red-team suites).
2. **Deepest.** H3 tests procedure ownership, which conditions the
   other two. If no production path can revise mechanism policies,
   then H1's widened constructor would still be driven by an
   unrevisable search policy, and H2's learner-internal acceptance
   would still be computed by an unrevisable verifier. The H3 result
   tells you whether the mechanisms are even *capable* of
   self-modification before you invest in widening what they can
   emit (H1) or accept (H2).
3. **Anti-treadmill.** Widening the constructor (H1) before fixing the
   oracle (H2) produces "a larger finite menu under the same generous
   acceptance test," which the synthesis names as the exact treadmill
   Micah forbade. H3 first avoids spending the most expensive change
   (new machinery) on top of the least examined assumption (that
   policies can change at all).

### 5b. The cheap policy-revisability check, executed

The check: for each mechanism, take the researcher-chosen decisions
from the synthesis tabulation (section 2a-2c), then search the
*production* (non-test) source for any write path to those decisions:
any `ns()`/`write_node` to the relevant fields, any edge type that
would alter them, any learner-state node they are read from. A
decision with no production write path is structurally unrevisable,
confirming H3 as a fact of the frozen architecture regardless of
which hypothesis explains the capability gap.

**Construction: trial search order.** Decisions: family set (chains,
sums, counts, single hops), order (k=2..4 chains, then sums, then
counts, then hops), bounds (depth 4, 96 paths, 12 values, 4095
subsets, total <= 900). Source: `t2_trial` lines 586-672; order is
literal loop bounds (`while(k<=4)`, line 593) and literal family
sequence; bounds are literals (`<16` in `t2_chain`, `<96` cap in
`t2_gather`, `<12` in `t2_gather_sum`, `total>900` in `t2_asm_sum`).
Production write paths to any of these: none. The only runtime
values are the gathered literals and the tried/rejected stats packed
into header field 16 (line 670), which no production code reads.
**Result: unrevisable. H3 confirmed for construction.**

**Inquiry: guide content and resolution.** Decisions: guide action 30,
content -999 (line 808, literals in `write_node`); what happens when
evidence arrives (absent entirely). Production write paths: none
modify an existing guide; no resolution procedure exists anywhere on
the production path (`ev_observe` never consults uncertainty nodes).
The red team independently found "no production path revises guides."
**Result: unrevisable. H3 confirmed for inquiry.**

**Revision: repair topology.** Decisions: always tombstone, always
insert literal SETREG (tag 101, line 726), always rewire
guard->new->succ (lines 727-731), replacement value always the
observed literal `new_o` (line 725). These are straight-line code in
`t2_revise_graph` (lines 706-763), not values read from state. The
only runtime-chosen quantities are `stale` (which cell, lines
711-717) and `new_o` (which literal, call-site). Production write
paths to the topology: none exist; there is no branch, no dispatch,
no policy read. `t2_trial` is never invoked on the revision path.
**Result: unrevisable. H3 confirmed for revision.**

### 5c. What the check's outcome means

The check is complete and H3 is confirmed as a structural fact of the
frozen TNN-2: **no production path in the frozen source can modify the
trial search order, the guide schema, or the repair topology from
experience.** This does not by itself prove H3 is the *binding*
bottleneck on capability (H1 and H2 may bind first in any given
world), but it proves the mechanisms cannot self-modify, which is the
precondition for any L3 procedure claim. Any future preregistration
for a TNN-3 mechanism can include the check as a kill bar directly:
"list every structural decision the learner can make that the source
cannot; demonstrate a production write path for each" (this is the
prereg checklist item the synthesis recommended in section 7).

---

## 6. Feasibility verdict

**H3-FEASIBILITY-PROBE-COMPLETE.**

Summary of findings:

1. **Q1:** The frozen 4-op ISA cannot express the revision procedure
   (or any structural procedure), because its effect domain is frame
   registers and the procedure's work is workspace graph mutation.
   The gap is precisely the structural effect class (ALLOC, field
   WRITE, edge LINK/KILL, node/edge READ). A concrete 40-60 cell
   sketch shows the control flow is ISA-expressible; only the
   effects are missing. Closing the gap is a protected-core boundary
   decision (banked for Micah; not decided here). The ISA ruling's
   allowed class (ALLOC, READ, WRITE, LINK, COPY) already names the
   missing half; the freeze fixed an instance without it.
2. **Q2:** The bootstrap problem is solvable by the MUL Rung B
   template (fixed minimal basis, learner structure above it, one
   reflective level, ISA as bottom turtle). The hard part is not
   bootstrapping but the effect-domain gap in (1); fix that and the
   bootstrap follows precedent.
3. **Q3:** The MUL Rung B pattern (hierarchical CALL composition,
   ablation-verified dependency, basis-then-structure layering)
   extends to procedures structurally, and its 0/4 revision result is
   positive evidence for H3's diagnosis (the unrevisable thing was
   the source-resident construction procedure). It does not extend
   across the effect-domain gap: Rung B demonstrated computational
   procedures over registers, not structural procedures over the
   graph store.
4. **Q4:** The minimal change for learner-revisable procedures
   (H3-lite) is: parameterize the three mechanisms' researcher-chosen
   decision points as reads from learner-state policy nodes, with one
   production update path each from experience. No ISA change, no new
   graph type, no new mode. It delivers H3's testable prediction
   without H3's governance cost, and it is explicitly not a
   capability patch.
5. **Q5:** H3 is first because it is cheapest (pure source analysis),
   deepest (conditions H1/H2), and anti-treadmill (no expensive
   machinery before the self-modification precondition is checked).
   The cheap policy-revisability check was executed against the
   frozen source: all three mechanisms' policies are structurally
   unrevisable. H3 confirmed as architectural fact.

**Single blocker, stated plainly:** everything in H3 reduces to one
gap (the structural effect class in the ISA / protected core) plus
one governance decision (whether the protected core may expose it).
The bootstrap, the MUL extension, and the H3-lite path are all
tractable given that decision; none is tractable without it, except
H3-lite, which deliberately routes around it.

**Recommended next experiments (for the coordinator, not decided
here):** (a) adopt the policy-revisability check as a prereg kill
bar for any TNN-3 mechanism proposal; (b) run H2's masked
verification probes next, per the synthesizer's order; (c) bank the
protected-core structural-ops question for Micah with the Q1 sketch
as evidence.

---

*End of probe. No source modified. No worlds designed. No scores
claimed. Paper untouched.*
