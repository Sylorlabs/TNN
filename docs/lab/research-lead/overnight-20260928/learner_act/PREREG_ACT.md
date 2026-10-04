# PREREG: Learner-State ACT (generic action operation)

Date: 2026-09-30. Worker: Learner-State ACT Prereg Architect (subagent).
Status: PREREG-FROZEN (design only; no implementation in this commit).
Lane: Cluster D (no agentic action machinery) from the Core Freeze
Challenge failure analysis; gap G2 in CLA-1.

## Step 0 reference

NAMECHECK.md in this directory was written before any design work
began and records the standing rules honored here.

## The standing question

> Why can the existing general architecture not learn this behavior?

The frozen core's action output is not a function of any mutable
learner state. W6W7_ANALYSIS.md (e7bb3d0bc) established the fact:
CHOICE is the constant 0, emitted wherever the world file places an
ACT line. The core can represent uncertainty (it emits -2 correctly)
and can store transition models (as triples), but there is no read
path from the workspace to the actuator. Knowledge, uncertainty, and
goals are inert with respect to action. The missing piece is one
generic read path, not nine capabilities and not a planner.

## Ruling this design implements

Micah's ruling (2026-09-30): "APPROVED as a hypothesis. But do not
create a PLANNER subsystem or CURIOSITY subsystem. ACT should be a
generic operation that consults learner-created state. The action
choice must come from learned structures such as: goal +
hypotheses + expected consequences + uncertainty + learned
procedures, not source-code task cases."

This prereg specifies the generic operation, the learner-created
structures it consults, the experience-to-policy learning path, and
the falsifiable predictions. It integrates with CLA-1
(PREREG_CLA1.md, b4f61ff8a): the same node store, the same edge
discipline, the same utility ledger, the same event loop. No
parallel state format is created.

## 1. The generic ACT operation (core side)

On an ACT event, the core performs exactly one generic workspace
read and emits the result. The operation has five fixed steps and
no branches on task, world, relation, or content:

1. Context assembly. The core keeps a small protected register
   holding the refs of the last 4 events (fixed size, generic
   bookkeeping the event loop already performs; no semantics).
   These are the current context refs C.

2. Policy-root check. The core keeps one protected register,
   POLICY_ROOT, holding a workspace node address. The learner
   sets this register through ordinary workspace operations;
   source code never sets it. Default is null. If null, emit
   CHOICE 0.

3. Activation. From POLICY_ROOT, the core runs ACTIVATE (the
   CLA-1 spreading-retrieval primitive) collecting nodes within
   2 hops over any typed edge.

4. Structural match. Among collected nodes, keep those whose
   ref[0] equals one of the context refs C. This is pure address
   equality on refs. The core does not interpret type tags; it
   matches structure.

5. Selection and emit. Of the matches, select the node with the
   highest utility (the CLA-1 utility ledger; every node carries
   learner-updated utility). Emit its payload[0] as the CHOICE
   value. If no node matches, emit CHOICE 0.

The operation defines exactly one structural convention: the
action value of a guidance node is read from payload[0]. This is
the operation's register layout, analogous to a calling
convention. It carries no task, world, or domain meaning. The
core never maps values to tasks, never prefers one value over
another, and never conditions on what the value represents.

Backward compatibility: with POLICY_ROOT null or with no matching
guidance nodes, behavior is byte-identical to the constant-0
core. No existing world score changes.

What the core does NOT do: it does not search, does not plan,
does not rank goals, does not compute expected value, does not
generate candidate actions, does not interpret uncertainty. All
of that is learner-side workspace content (sections 2 and 3).

## 2. Learner-created structures consulted (workspace content)

The action choice comes from learned structures. The five inputs
Micah named are workspace conventions. The core never interprets
type tags; the conventions below are how the learner organizes
content so that the read protocol in section 1 finds it. First use
of a tag defines the type, per CLA-1.

(a) GOAL nodes. ref[0] = the target entity node (for example, the
    state the learner treats as the objective). Created by
    learner-side processes from experience (for example,
    detecting a self-loop in a taught transition model and
    reifying "reach this state" as a goal). A goal is an
    ordinary workspace node, not a source constant and not a
    mode flag.

(b) ACTION-GUIDE nodes (policy). ref[0] = context anchor node
    (the situation this guidance applies in); ref[1] = linked
    GOAL node; payload[0] = CHOICE value; payload[1] =
    confidence. Linked DEPENDS-ON to the model and hypothesis
    nodes the guidance stands on, so the CLA-1 dependency
    graph protects them together. These are the nodes the
    section 1 read protocol selects among.

(c) UNCERTAINTY records. Created when a QUERY returns -2 (the
    admission of ignorance). ref[0] = the queried key context.
    Uncertainty is therefore ordinary workspace content that
    can serve as a context anchor: a policy whose ref[0] is an
    uncertainty record fires when that uncertainty is live in
    the context refs. This is how inquiry becomes
    state-contingent without any curiosity drive in source.

(d) CONSEQUENCE structures. Expected outcomes of actions,
    expressed with the fixed edge vocabulary: an ACTION-GUIDE
    node links SUPPORTS to an outcome node ("taking this
    action supports reaching that outcome"). No new edge types
    are introduced. The learner builds these from OBSERVE
    outcomes (section 3).

(e) Learned procedures. Executable structures built under gap
    G1 (incremental construction). A policy node may ref a
    procedure structure as its means. Procedures are not
    required for the ACT operation itself; W7-class planning
    is iterated model querying, not procedure execution (per
    the W6W7 analysis). The slot exists so that when G1 is
    solved, procedures plug into action selection as
    workspace refs, not as a new subsystem.

## 3. How action policies get LEARNED (experience to policy)

No policy is installed by source code. Every ACTION-GUIDE node
is created by a learner-side workspace process from experience,
using only the generic primitives (ALLOC, WRITE, LINK, READ,
ACTIVATE, DECAY). The learning loop is the CLA-1 event loop:

- TEACH: model facts enter the workspace (for example, W7
  transition triples). The learner links them into structures.
- QUERY miss: the -2 admission is recorded in the experience
  log; the learner creates an UNCERTAINTY node linked to the
  query context.
- Goal formation: a learner-side process reifies goals from
  experience (reference example: self-loop detection in a
  transition model yields a GOAL node). The exact reification
  heuristics are learner content, not core code.
- Policy derivation: a learner-side process writes
  ACTION-GUIDE nodes anchored at context refs. Reference
  derivation D1 (W7-class): from the GOAL node and the
  transition model, chain lookups backward from the goal
  (from 9704, which action arrives here; repeat) and write
  one ACTION-GUIDE per visited state with payload[0] set to
  the chosen action. Reference derivation D2 (W6-class):
  from a live UNCERTAINTY record, write an ACTION-GUIDE
  anchored at that record selecting the inquiry action.
  D1 and D2 are reference examples of the general
  requirement, not frozen algorithms: any learner-side
  process that produces ACTION-GUIDE nodes via generic
  primitives satisfies the design.
- ACT: the core consults per section 1 and emits.
- OBSERVE: the outcome is compared with the expected
  consequence. Match: raise the utility of the participating
  ACTION-GUIDE, GOAL, and model nodes (the CLA-1 section d
  update rules). Mismatch: lower utility, create a
  CONTRADICTS edge from the outcome to the expectation, and
  the contradiction triggers re-derivation (C1-style relearn
  from fresh evidence; no REVISION_MODE).

Policy content therefore improves with experience and degrades
honestly when the world contradicts it. The utility ledger,
the dependency graph, and the protection set (CLA-1 section d)
govern policy retention exactly as they govern any other
workspace structure: there is no separate memory policy for
actions.

## 4. Falsifiable predictions

P-ACT1 (planning): a frozen CLA-1 implementation with this ACT
operation, exposed to a W7-class world (transition model taught,
goal inferable from experience), emits state-varying CHOICE
values and reaches the goal on a majority of instances. The
constant-0 baseline scores 0/4 on the same world.

P-ACT2 (inquiry attribution): on a W6-class world with a
non-degenerate action interface (at least two distinguishable
actions), the emitted actions correlate with the learner's
UNCERTAINTY records rather than with ACT line position.
Operational test: swap the decoy and inquiry ACT positions in
the world file; actions follow the -2 admission, not the file
position.

P-ACT3 (no free capability): with POLICY_ROOT null or with no
ACTION-GUIDE nodes in the workspace, ACT emits CHOICE 0 on all
worlds and no frozen-battery score changes relative to the
pre-ACT core.

P-ACT4 (structure ablation): deleting the ACTION-GUIDE nodes
(and only those) restores constant-0 behavior on W7-class
worlds; deleting the GOAL nodes (and only those) degrades
W7-class performance while leaving W1-style recall intact.
The capability is in the structures, not the handler.

P-ACT5 (generality): the identical frozen ACT handler serves
W6-class and W7-class worlds with zero source branches on
world, task, or relation identity.

P-ACT6 (memory prerequisite, honest dependency): under C75-level
eviction load, action policies are evicted and ACT performance
degrades toward the constant-0 baseline; with the CLA-1
preservation system active, policies survive sequential teaching
and ACT performance holds. The agentic cluster depends on the
memory cluster; this prereg does not claim otherwise.

Falsification conditions (any one rejects or narrows the design):

F-ACT1: a correct, stable policy is present in the workspace
(verified white-box) and a W7-class world remains unsolvable.
The primitive is then insufficient and the Cluster D diagnosis
is wrong.

F-ACT2: CHOICE values correlate with ACT file position rather
than with workspace state under a controlled swap test. The
handler is not genuinely state-consulting.

F-ACT3: any freeze world requires a per-world source branch in
the ACT handler to pass. The operation is not general.

F-ACT4: action capability appears with no ACTION-GUIDE
structures in the workspace. The core is smuggling content and
the learner-ownership claim is void.

## 5. Anti-treadmill guards: what this is NOT

- Not a planner. No search algorithm, no plan tree, no goal
  stack, no lookahead, no simulation loop in source. If the
  implementation contains any of these, it fails review.
- Not a curiosity module. No intrinsic reward, no uncertainty
  bonus, no exploration schedule, no drive term in source.
- Not per-world or per-capability handlers. One ACT code path
  for all worlds. A grep for world, task, or relation identity
  branching inside the ACT handler must return nothing.
- Not an interface fix. The singleton action set of the W6
  protocol is a world-design property the core cannot change.
  A future inquiry world needs a richer action channel; that
  is protocol work for the next freeze, not core repair.
- Not a second policy learner in disguise. Policy derivation
  (D1, D2, and their successors) lives in learner-side
  workspace processes. If derivation logic appears in core
  source as task cases, the implementation fails K-ACT2.
- Not a memory subsystem. Policy retention uses the CLA-1
  utility ledger, dependency graph, and protection set. No
  action-specific retention code is authorized.

## 6. Integration with CLA-1 (no parallel format)

- The ACT read protocol uses the CLA-1 node store
  (type_tag, ref[4], payload[4]), the fixed edge vocabulary,
  and the ACTIVATE primitive. No new store, no new edge
  types, no new primitives.
- POLICY_ROOT and the 4-event context register are protected
  core registers holding addresses and refs. They carry no
  semantics and are set by learner operations, never by
  source constants.
- GOAL, ACTION-GUIDE, UNCERTAINTY, and CONSEQUENCE structures
  are node-type conventions in the single workspace. The
  dependency graph gives policies shared fate with the model
  and goal nodes they stand on; the utility ledger scores
  them by outcomes; the protection set can pin them.
- The experience log records ACT events and their OBSERVE
  outcomes as ordinary entries, so policy learning is
  visible in the same stream as all other learning.
- This prereg fills CLA-1 gap G2 (uncertainty-contingent
  action). It does not touch G1 (executable construction) or
  G3 (hierarchical representation).

## 7. One-System Rule accounting (prereg; measured at implementation)

- Cognition source lines added: small by construction (one
  ACT handler implementing the five-step read protocol,
  plus two protected registers). Exact count is an
  implementation measurement; the prereg binds the
  direction: the handler is a read path, not a decision
  procedure.
- New hardcoded semantic cases: 0.
- New modes: 0.
- New bridges: 0.
- New task-specific handlers: 0.
- Learner-state structures created: GOAL, ACTION-GUIDE,
  UNCERTAINTY, CONSEQUENCE node-type conventions (4;
  all workspace content, all learner-owned, all generic).
- Standing question answered: the architecture could not
  learn action behavior because no read path existed from
  mutable learner state to the actuator. This design adds
  the read path and nothing else; every decision the
  learner makes about acting lives in structures the
  learner built.

## 8. What this prereg does NOT authorize

- No implementation in this commit. The implementation
  worker builds only after this prereg is reviewed.
- No planner, curiosity, or inquiry subsystem, mode,
  bridge, or task-specific handler may be introduced by
  the implementation. Any such addition fails K-ACT2.
- The reference derivations D1 and D2 are examples of the
  general requirement, not frozen algorithms. The
  implementation may use any learner-side derivation that
  produces ACTION-GUIDE nodes via generic primitives.
- No widening of the action interface and no per-world
  tuning of the ACT handler. FW1-FW9 remain sealed
  evaluator assets; the ACT design must not reference
  them.

## Kill bars for the implementation (frozen here)

K-ACT1: this prereg (frozen alone, before any implementation
commit) completely specifies the operation: the five-step read
protocol, the structure conventions, the learning loop,
predictions P-ACT1 through P-ACT6, falsification conditions
F-ACT1 through F-ACT4, and the section 5 guards.

K-ACT2: the implementation contains zero branches on world,
task, or relation identity in the ACT handler; zero new modes;
zero new bridges; zero task-specific handlers; all policy
content in workspace structures. Verified by source inspection
at review.

K-ACT3: pure Zag plus shell orchestration only; zero Python at
every step; all documents dash-clean via shell-only byte
checks; the contaminated paper untouched; commits local with
explicit pathspecs under learner_act/ only.
