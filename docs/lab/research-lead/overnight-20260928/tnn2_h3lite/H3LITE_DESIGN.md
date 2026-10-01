# H3-Lite Design: Learner-Revisable Policy Nodes for TNN-2's Three Mechanisms

Date: 2026-10-01. Designer session: 8f77eabf-3073-4dac-a83f-339f9ea28bbd.

## NOT IMPLEMENTED

This document is a design, not code. Nothing here has been implemented,
tested, or measured. It does not authorize implementation. Any TNN-3 work
building on this design must go through its own preregistration with frozen
kill bars. The design's job is to specify exactly what H3-lite would change,
where, and how it would be tested, so a future preregistration can adopt or
reject it on concrete grounds.

Target of analysis: `tnn2.zag` at `f4de7ff46` (frozen), read-only.
All line numbers refer to that source. Tag, field, and edge-type numbers
are from the frozen source's own conventions.

---

## 1. Concept recap

From the feasibility probe (commit `94cecdba4`, section 4):

**H3-lite pattern:** parameterize every researcher-chosen decision point in
the three mechanism procedures as a read from a learner-state policy node,
and add one production path that updates the policy from experience. The
procedure stays researcher-authored Zag code. Its degrees of freedom move
into learner state and become revisable.

This delivers H3's testable prediction (procedures revisable by experience)
with no ISA change, no new graph type, no new mode. It moves the locus of
control, not scores. It fixes no world and improves no frozen score.

Three policy nodes, one per mechanism. Each has:
- a tag marking it as a policy node (proposed: 40, unused in the frozen source),
- a subtype field identifying which policy it stores,
- the decision values in node fields,
- statistics in node fields or linked nodes,
- one production read path (the existing decision point),
- one production write path (the new update, specified below).

The bootstrap for all three is copy-then-revise: on first use, the policy
node is created with the researcher's current defaults copied in. The learner
does not invent the initial policy; it revises a copy. This dodges the
ex-nihilo bootstrap entirely, per the probe's section 2(b).

---

## 2. Design 1: Trial search order policy

### 2a. The decision point today

`t2_trial` (lines 586-672) searches in a fixed order written as source
literals:

- lines 592-593: chains k=2..4 (`while(k<=4)`), longest first
- line 605: sums (after chains)
- line 626: counts (after sums)
- line 647: single hops (last)

The comment at lines 582-584 states the rationale ("composition-preserving:
longer chains before sums before counts before single hops"). The order is
a researcher-authored heuristic. No production code can change it. The
feasibility probe's cheap check confirmed: no write path exists to the
search order.

### 2b. Policy node layout

Tag 40 (T_POLICY, proposed, unused in frozen source). Subtype in field 4 = 1
(trial-order policy).

Family identifiers (fixed enumeration, researcher-defined; H1 unaddressed):
- 0 = chain k=2, 1 = chain k=3, 2 = chain k=4
- 3 = sum, 4 = count, 5 = single hop

Six order slots in fields 8, 12, 16, 20, 24, 28, holding family ids in
preference order (first tried to last tried). Field 32 holds a packed
statistics word: bits 0-5 = consecutive rejections of the current
first-choice family (saturating at 63), bits 6-11 = consecutive rejections
of the second-choice family, and so on is not feasible in one field;
instead field 32 holds only the first-choice rejection count, and
per-family attempt counts use the existing header field 16 trial stats
(line 670) which `t2_try_verify` already maintains.

Rationale for six slots rather than a linked list: the family set is fixed
at six members (researcher-enumerated), so fixed fields suffice. If a future
mechanism adds families, this layout needs revision; that is acceptable for
H3-lite scope.

### 2c. Initialization (copy-then-revise)

At the top of `t2_trial`, before the search loop: scan node slots 2..1023
for tag 40 with field 4 == 1. If absent, allocate a policy node and write
the researcher's defaults: fields 8,12,16,20,24,28 = 2,1,0,3,4,5
(chain-4 first, then chain-3, chain-2, sum, count, hop), matching the
current literal order. Field 32 = 0.

The defaults are copied from source, not invented. The learner's
contribution begins with the first update.

### 2d. Read path (the existing decision point, modified)

Replace the literal loop nest (lines 592-647) with a dispatch loop over
the policy node's order slots. For i in 0..5: family = ng(W,pol,8+i*4);
run that family's assembly and verification. The per-family assembly code
(`t2_asm_chain`, `t2_asm_sum`, `t2_asm_count`, single-hop) is unchanged;
only the order of invocation is policy-driven.

This is the minimal edit: the families remain researcher-written
assemblers, but their trial order becomes learner state.

### 2e. Write path (the new update)

In `t2_try_verify`, on verification success: identify which family
produced the verified graph (passed as a parameter from the dispatch
loop). Find that family's position p in the policy order. If p > 0, swap
it with the family at p-1 (one step earlier). This is a Hebbian-style
promotion: families that verify move earlier. Field writes only.

On verification failure of all families (trial returns -2): increment
field 32 (first-choice rejection count). When field 32 exceeds a fixed
threshold (proposed: 8, a researcher-chosen constant documented as such),
demote the first-choice family one step (swap with position 1) and reset
field 32 to 0. The threshold is a researcher heuristic; the order it
operates on is learner state.

### 2f. Trigger and information

- Trigger for promotion: `t2_try_verify` returning success for a family.
  Information used: which family verified.
- Trigger for demotion: trial exhausting all families without success,
  repeated. Information used: the existing tried/rejected stats in header
  field 16 plus the policy node's own rejection count.
- No new event types. No new machinery beyond field reads/writes on the
  policy node.

### 2g. Discrimination test

A sealed world where chains-before-counts systematically picks the wrong
family first (e.g., all answers are counts, chains always fail
verification). Run N trials. The H3-lite prediction: the learner's order
flips to counts-first within the demotion threshold. The frozen TNN-2
prediction: order never changes. This is the exact experiment the probe
named in section 4.

---

## 3. Design 2: Guide template policy

### 3a. The decision point today

`miss_inquire` (lines 795-812) creates a guide node with researcher
constants at line 808:

```
write_node(W,g,30,-999,0,0);
```

Slot 20 = 30 (action), slot 24 = -999 (content). Every guide in every
uncertainty gets the same action and content. The inquiry red team
(`4e329c772`) found this is L3-hardcoded and L6 (resolution) is absent:
no production path revises a guide or resolves an uncertainty.

### 3b. Policy node layout

Tag 40, subtype field 4 = 2 (guide-template policy).

- Field 20: default action (initialized to 30, the researcher's constant).
- Field 24: default content (initialized to -999).
- Field 28: resolution count (number of uncertainties resolved while this
  template was active).
- Field 32: miss count (number of guides created from this template).
- A history ring is desirable but exceeds fixed fields; instead, link
  the policy node via ET_REF (type 4) edges to the three most recent
  resolved uncertainty nodes, each carrying the action that preceded
  its resolution in field 20. When a fourth resolution occurs, kill the
  oldest ET_REF edge (fixed three-slot history, researcher-chosen bound
  documented as such).

### 3c. Initialization (copy-then-revise)

In `miss_inquire`, before guide creation: scan for tag 40 with field 4
== 2. If absent, allocate and write defaults (30, -999, 0, 0). The guide
creation at line 808 then reads field 20 and field 24 from the policy
node instead of literals:

```
write_node(W,g,ng(W,tpol,20),ng(W,tpol,24),0,0);
```

### 3d. The forced L6 resolution path

H3-lite for inquiry forces creation of the missing resolution procedure
in its smallest form. New production function `resolve_uncertainty`
(called from `ev_observe`):

1. When `ev_observe(W,s,r,o)` learns a fact, scan node slots for
   T_UNCERT (tag 30) nodes with field 20 == s and field 24 == r
   (the uncertainty this observation addresses).
2. For each match: create an ET_CON (type 3) self-edge on the
   uncertainty node and on its linked guide (found via reverse ET_DEP
   edges). This uses the existing supersession convention (`is_superseded`
   at line 132 already honors type-3 self-edges; `ev_act` at line 859
   already filters on it). No new convention.
3. Increment the template policy's field 28 (resolution count).
4. Record the resolved guide's action in the ET_REF history (field 20
   of the uncertainty node already holds s; the guide's action is read
   from the guide node before supersession).
5. Template adjustment: if field 28 (resolutions) is nonzero and the
   most recent three resolutions all followed guides with action A
   where A != field 20 (current default), set field 20 = A. This is a
   majority-of-three rule, researcher-authored as a heuristic, operating
   on learner-state history.

### 3e. Write path summary

- Read path: `miss_inquire` line 808 reads action/content from the
  template policy instead of literals.
- Write path: `resolve_uncertainty` (new, called from `ev_observe`)
  writes resolution counts, history edges, and occasionally the default
  action.
- Trigger: `ev_observe` learning a fact that matches an open
  uncertainty (s,r).
- Information used: the observed (s,r,o), the guide's action, the
  resolution event itself.

### 3f. What this does and does not fix

Does: guide content becomes revisable from experience; the L6
resolution link exists (uncertainties can be superseded); stale guides
stop being ACT-eligible after resolution (via the existing
`is_superseded` filter).

Does not: derive discriminating questions (the action is still a single
default, not computed from competing hypotheses); the informativeness
criterion from the inquiry generalization analysis (`dedfad368`) is not
implemented. H3-lite makes the guide *revisable*; it does not make it
*discriminating*. That distinction must survive into any preregistration.

### 3g. Discrimination test

Two-phase sealed test. Phase 1: N misses on relation R1, all guides get
action 30; then observations resolve them. Phase 2: misses on relation
R2 where the sealed world reveals answers only after a different action
(the world design must make this observable; the exact mechanism is the
adversary's choice). The H3-lite prediction: if resolutions in phase 1
consistently followed a non-30 action, the template's default shifts.
The frozen TNN-2 prediction: action is 30 forever. Note this test needs
the world to provide differential feedback on actions, which the current
frozen worlds may not; the test design is non-trivial and belongs to the
adversary, not this document.

---

## 4. Design 3: Repair dispatcher policy

### 4a. The decision point today

`t2_revise_graph` (lines 706-763) is straight-line researcher code:

- lines 711-717: find stale SETREG via ET_DEP scan (the only blame
  localization; guards and INC/DEC cells lack provenance).
- lines 719-724: find guard by field12 match.
- lines 726-727: always allocate literal node and SETREG cell.
- lines 728-731: always rewire guard -> new -> succ, kill stale edge.
- line 732: always tombstone the stale cell.
- lines 732-743: verify by re-execution; revert everything on failure.

The topology is fixed: tombstone + insert-literal-SETREG + rewire. The
revision red team (`687ba0219`) confirmed the learner chooses only which
cell (`stale`) and which literal (`new_o`); the researcher chose
everything else. `t2_trial` is never invoked on this path.

### 4b. The five repair topologies (from `edbb0e9b5`, section 2)

The policy selects among these researcher-enumerated topologies
(H1 unaddressed; the family remains fixed):

- 0: Guard-predicate edit. Change the BRANCHEQ cell's comparison literal
  (field 8) or tested slot (field 4) instead of touching the guarded step.
- 1: Branch rerouting. Repoint a guard's true-target (field 12) or a SEQ
  edge to an already-present step; no new cell allocated.
- 2: Multi-step coordinated repair. Revise two or more stale steps in one
  contradiction event (loop the blame scan; apply per-step edits).
- 3: Step-count / step-type conversion. Adjust unroll length (insert or
  delete INC cells); convert INC to DEC; convert SETREG constant to MOVE.
- 4: Step deletion without insertion. Tombstone a spurious step and
  rewire around it; no insertion.
- 5: Literal-patch (the current behavior). Retained as the default and
  as a fallback.

### 4c. Policy node layout

Tag 40, subtype field 4 = 3 (repair-dispatch policy).

- Field 20: preferred topology id (0-5, initialized to 5).
- Fields 24, 28, 32: packed success counts for topologies 0-5. Six
  topologies need six counters; three fields hold two each via
  16-bit halves (field 24: topo 0 in low 16, topo 1 in high 16;
  field 28: topo 2 low, topo 3 high; field 32: topo 4 low, topo 5
  high). Saturating at 65535; more than sufficient.
- Blame-signature specificity: a single global preference is crude.
  Refinement (optional, documented as extension): link the policy node
  via ET_REF edges to per-(relation, cell-tag) sub-policy nodes, each
  with its own field 20 preference. H3-lite minimal scope uses the
  global preference; the refinement is named but not specified further.

### 4d. Initialization (copy-then-revise)

In `revise_on_contradict` (line 685), before dispatch: scan for tag 40
with field 4 == 3. If absent, allocate with field 20 = 5 (literal-patch,
the researcher's current behavior) and zeroed counters.

### 4e. Read path (dispatch)

Replace the straight-line body of `t2_revise_graph` with a dispatch on
ng(W,rpol,20):

- 5: current lines 706-763 unchanged.
- 0-4: the corresponding repair implementation (researcher-written,
  specified only by the topology descriptions in section 4b; their
  implementation is future work, not this document).

Each topology implementation preserves the existing contract: verify by
`t2_exec` on the repaired root; revert all edits on failure (the
revert discipline at lines 734-743 is the template); return 1 on success,
0 on total failure.

If the preferred topology returns 0 (failure), the dispatcher tries the
next topology in order of descending success count (from the packed
fields), up to all six, before returning 0. This makes the dispatcher a
search over topologies, not a single attempt.

### 4f. Write path (the new update)

On verification success for topology T: increment T's counter in the
packed fields. If T != field 20 (current preference) and T's counter
exceeds the current preference's counter by a margin (proposed: 2, a
researcher heuristic), set field 20 = T. Preference follows demonstrated
success.

On total failure (all topologies tried, all reverted): no counter
changes (no evidence about which topology is better, only that none
sufficed for this case). The failure is recorded in the existing
tried/rejected manner if the revision lane adopts the header-field-16
convention from construction; that instrumentation is named as required
but not specified here.

### 4g. Trigger and information

- Trigger for dispatch: `revise_on_contradict` entry (the existing
  contradiction event).
- Trigger for counter update: the verify/revert outcome inside
  `t2_revise_graph`.
- Information used: blame signature (stale cell tag, relation), which
  topology succeeded, success counts.
- The five topology implementations are researcher-written; only the
  selection among them is learner-revisable. This is the exact boundary
  the revision red team drew: "the SAME machinery can derive
  structurally different repairs" is satisfied at the policy level,
  not at the operator-invention level.

### 4h. Discrimination test

Sealed graphs where the literal-patch topology systematically fails but
another topology succeeds (e.g., guard-predicate faults where the
counterexample means "this branch should fire on a different value").
Run repeated contradictions. The H3-lite prediction: the policy's
preference shifts from 5 to 0 after the margin is exceeded, and
subsequent revisions attempt guard-predicate edit first. The frozen
TNN-2 prediction: literal-patch attempted every time, failing every
time. This test also requires the sealed worlds to contain faults
addressable by non-default topologies, which is adversary work.

---

## 5. Update paths: consolidated table

| Mechanism | Policy node (tag 40, subtype) | Read path (existing decision point) | Write path (new) | Trigger | Information used |
|---|---|---|---|---|---|
| Construction | subtype 1, fields 8-28 order, 32 rejections | `t2_trial` loop nest (lines 592-647) becomes policy dispatch | `t2_try_verify` success/failure | verification outcome per family | which family verified; tried/rejected stats |
| Inquiry | subtype 2, field 20 action, 24 content, 28/32 counts | `miss_inquire` line 808 reads template | `resolve_uncertainty` (new, from `ev_observe`) | observation matching open uncertainty | observed (s,r,o); guide action; resolution event |
| Revision | subtype 3, field 20 preference, 24/28/32 packed counters | `t2_revise_graph` body becomes topology dispatch | counter update on verify/revert outcome | contradiction event + repair outcome | blame signature; succeeding topology; success counts |

Common properties:
- All reads replace source literals; all writes are field writes or
  edge link/kill on policy nodes.
- No ISA change. No new opcode, mode, bridge, or handler.
- No new event types; triggers are existing production events.
- All thresholds and margins (demotion threshold 8, majority-of-three,
  preference margin 2, history bound 3) are researcher-chosen heuristics,
  documented as such. They are not learner-revisable in H3-lite scope.
  A future step could parameterize them; that is explicitly out of scope.

---

## 6. Prereg kill bar: policy revisability (K-H3, draft)

The feasibility probe recommended adopting the policy-revisability check
as a prereg kill bar. Draft language follows. This is DRAFT-NOT-FROZEN:
it has not been reviewed by Micah and must not govern any evaluation
until frozen through the normal process.

---

**K-H3 (Policy Revisability).** For every structural decision the
mechanism makes that is not determined by its immediate input, the
preregistration must list:

1. the decision (e.g., "trial search order", "guide default action",
   "repair topology selection");
2. the learner-state node and fields storing the decision (tag, subtype,
   field numbers);
3. the production (non-test) code path that writes to those fields;
4. the experience event triggering the write;
5. a sealed test demonstrating the decision taking different values
   after different experience histories.

A structural decision is any choice among alternatives where the
alternatives are not dictated by the current input: search orders,
default parameters, topology selections, ranking criteria, thresholds
that affect behavior. Pure functions of the input (e.g., "which cell
matches this provenance edge") are not structural decisions.

**Failure conditions (any one fails K-H3):**

- (a) A structural decision is implemented as a source literal, loop
  bound, or straight-line code with no learner-state read. (This is the
  frozen TNN-2 condition for all three mechanisms.)
- (b) A structural decision is read from learner state but no
  production code path writes to it. (Read-only policy; revisability
  theater.)
- (c) A production write path exists but is unreachable in the sealed
  evaluation (e.g., gated behind a test-only flag). (Write-path theater.)
- (d) The demonstration test uses researcher-supplied experience
  histories that directly encode the expected decision (e.g., teaching
  the policy node the answer). The histories must be ordinary world
  interactions; the decision change must be an outcome, not an input.

**Passing K-H3 does not establish L3.** It establishes that the
mechanism's policies are revisable by experience, which is a precondition
for any procedure-level learning claim. C0-A/B/C/D are evaluated
separately.

---

### Notes on the draft

- The "list every structural decision the learner can make that the
  source cannot" phrasing from the synthesis (section 7 of `42b4dfa91`)
  is incorporated as the listing requirement.
- Condition (d) guards against the test-scaffolding failure mode the
  governance audit tracks: the policy must change because of experience,
  not because the test wrote the policy.
- The bar is deliberately scoped to decisions, not procedures. Full H3
  (procedures as learner-built graphs) would need a stronger bar; that
  stronger bar is not drafted here because its prerequisite (the
  protected-core structural-ops decision, banked for Micah) is unresolved.

---

## 7. What H3-lite does NOT deliver (non-overselling)

1. The procedures remain researcher-authored Zag code. C0-A still fails
   at the procedure level. H3-lite moves decisions into learner state;
   it does not move procedures there.
2. The repair family remains researcher-enumerated (five topologies plus
   literal-patch). H1 is unaddressed: the learner selects among given
   topologies but cannot invent a sixth.
3. The acceptance oracle remains. `t2_try_verify` still verifies against
   the environment-supplied expected/observed value. H2 is unaddressed:
   the learner does not generate its own acceptance criterion.
4. The guide remains non-discriminating. H3-lite makes guide content
   revisable; it does not implement the informativeness scoring from the
   inquiry generalization analysis. A revisable constant action is still
   a constant action until experience changes it.
5. All heuristics (thresholds, margins, history bounds, the six family
   ids, the five topology definitions) are researcher-chosen. H3-lite
   parameterizes decisions, not meta-decisions.
6. No capability improvement is predicted on the frozen FW1-FW9 battery.
   H3-lite changes the locus of control; frozen scores measure the
   researcher-enumerated envelope, which is unchanged.

---

## 8. Open questions and banked decisions

1. **Protected-core structural ops (banked for Micah).** Full H3 needs
   the ISA effect-domain gap closed (ALLOC, field WRITE, edge LINK/KILL
   in the protected core). The probe's Q1 sketch is the evidence. This
   design routes around it; it does not resolve it.
2. **Per-signature sub-policies (extension).** Section 4c names
   per-(relation, cell-tag) repair sub-policies via ET_REF edges. Worth
   specifying if H3-lite proceeds to preregistration, since a global
   repair preference is crude across heterogeneous faults.
3. **Inquiry discrimination test design.** Section 3g notes the test
   needs worlds providing differential feedback on actions. Whether the
   post-freeze adversary (GW1-GW9) can supply this is an open question
   for the adversary lane, not answered here.
4. **Interaction with the freeze evaluation.** H3-lite is not a patch
   to TNN-2 and must not be applied to the frozen binary. It is a
   candidate direction for TNN-3 preregistration only.
5. **K-H3 draft status.** DRAFT-NOT-FROZEN. Requires Micah's review
   before governing anything.

---

## Verdict

H3LITE-DESIGN-COMPLETE.

Three policy-node designs specified (trial order, guide template, repair
dispatcher) with layouts, initialization, read paths, write paths,
triggers, and discrimination tests. One prereg kill bar drafted (K-H3).
Non-deliveries stated. No implementation undertaken.

*End of design. No source modified. No scores claimed. Paper untouched.*
