# Architecture Integration Specification: CLA-2 + CAM-1 + ACT + Compose-Ops

Date: 2026-09-30. Worker: Architecture Integration Coordinator.
Verdict label target: INTEGRATION-SPEC-COMPLETE.
Status: specification and compatibility report; no implementation code;
no prereg amended by this worker.

## Sources (frozen, read-only)

- CLA-2: `continuing_learner/PREREG_CLA2.md` (commit 24351fd31).
  Six primitives, one workspace, consolidated retention substrate,
  event loop with evidence rules. Primary architecture direction.
- CAM-1: `construct_apply/PREREG_CAM1.md` (commit 68a41be8a).
  PROPOSE -> VERIFY -> PROMOTE -> APPLY; one mechanism for W2/W3;
  MAP node format; split bar S1-S3; guards G1-G5.
- ACT: `learner_act/PREREG_ACT.md` (commit 51a818141).
  Five-step generic ACT read protocol; POLICY_ROOT register;
  GOAL / ACTION-GUIDE / UNCERTAINTY / CONSEQUENCE conventions.
- Compose-ops: `compose_ops/COMPOSE_OPS_SPEC.md` (commit 881b17638).
  Ten ops (six adopted + COPY / APPLY / CORROBORATE / PROMOTE);
  oracle test O1-O3; HOLE sentinel; frozen basis {EQ, ADD};
  bootstrap miss-policy; falsification F1-F7.

Related but out of scope for amendment here: contlearn2 is the
competing control (ruling D); FW1-FW9 are sealed evaluator assets
(ruling A) and were not accessed.

---

## Part 1: Interface contracts extracted

### 1A. CLA-2 provides

Workspace format: one node store, fixed records
(type_tag, ref[4], payload[4]). Learner assigns type tags through
first use; core never interprets tags.

Core primitives (six): ALLOC, WRITE, LINK, READ, ACTIVATE, DECAY.

Edge vocabulary (domain-free): DEPENDS-ON, SUPPORTS, CONTRADICTS,
REFINES, INSTANCE-OF, USE, CONFIRMS, SURPRISE, PROTECTION (with
decay clock and provenance link), MEMBER, REGRET.

Retention: three-step core eviction reading ONLY learner-authored
content: (1) PROTECTION check (skip nodes with live PROTECTION
edge); (2) evidence aggregation, bid(node) = fixed linear count
over the node's learner-authored evidence edges; (3) tie-break by
a learner-owned monotonic cursor. No weights, no per-node utility
scalar, no researcher-fixed adaptation targets.

Event loop (TEACH / QUERY / ACT / OBSERVE), world/task identity
stripped by the driver. Evidence rules:
- TEACH: encode event; create PROTECTION edge with learner-state
  probation duration; link INSTANCE-OF / association edges.
- QUERY hit: USE edges on participants; CONFIRMS where corroborated.
- QUERY miss: SURPRISE edges on retrieval path; consult HISTORY;
  on regret match create REGRET node and strengthen path evidence.
- OBSERVE: update evidence edges; CONTRADICTS on contradiction;
  contradicted structure retained as superseded history; refresh
  protection clocks on used nodes.

Node-type conventions (all learner-owned): fact clusters,
hypothesis graphs, executable programs, episode chains, operator
models, GROUP nodes with MEMBER edges, HISTORY nodes, REGRET
nodes, CANDIDATE nodes.

CLA-2 does NOT provide: POLICY_ROOT register, MISS_POLICY
register, 4-event context register, HOLE sentinel, COPY / APPLY /
CORROBORATE / PROMOTE operations, a per-node utility scalar, or
any query-miss dispatch point beyond the fixed SURPRISE/HISTORY/
REGRET rule.

### 1B. CAM-1 assumes and provides

Assumes: the CLA event loop and workspace. MAP structures as
ordinary workspace nodes in the (type_tag, ref[4], payload[4])
format. The standard typed-edge discipline (SUPPORTS,
INSTANCE-OF, CONTRADICTS, DEPENDS-ON). The utility/standing
machinery of the retention substrate. Exact-key lookup first on
the query path, with an APPLY hook on miss.

Provides: one four-operation loop for regularity ->
persistent reusable structure -> application:
- PROPOSE: exemplar alignment by relation-set signature;
  P-INV (invariance, order 0) and P-DEP (dependence via
  finite-difference analysis, discovered order k).
- VERIFY: candidate predicts K held-back exemplars;
  SUPPORTS edges from corroborating exemplars.
- PROMOTE: verified candidate reified as MAP node.
  Format: refs [trigger-relation, parameter-dimension,
  exemplar-group, reserved]; payload [body-kind (0 literal,
  k polynomial order), coefficient slots..., corroboration
  count, standing]. Standing starts at corroboration count;
  CONTRADICTS edges decrement standing; below the demotion
  threshold the map is demoted to CANDIDATE and APPLY skips it.
- APPLY: on exact-key miss, find MAP nodes whose trigger
  matches the query relation and whose parameter binds the
  query subject; evaluate the body; prefer higher standing
  on disagreement; else -2.

Needs from the core: a query-miss hook for APPLY; a way to
read standing for arbitration; payload space for
[body-kind, coefficients..., corroboration, standing].

### 1C. ACT assumes and provides

Assumes: the CLA node store (type_tag, ref[4], payload[4]),
the fixed edge vocabulary, the ACTIVATE primitive, and a
utility value per node ("the CLA-1 utility ledger; every node
carries learner-updated utility"). No new store, no new edge
types, no new primitives.

Needs from the core (not present in CLA-2):
- POLICY_ROOT: one protected register holding a workspace
  node address, set by the learner through ordinary
  workspace operations, never by source constants.
  Default null.
- Context register: the refs of the last 4 events
  (described as "generic bookkeeping the event loop
  already performs").

Provides: the five-step generic ACT read protocol:
(1) assemble context refs C; (2) if POLICY_ROOT null emit
CHOICE 0; (3) ACTIVATE from POLICY_ROOT, 2 hops, any typed
edge; (4) keep nodes whose ref[0] equals a context ref
(pure address equality; core does not interpret tags);
(5) select the match with highest utility; emit its
payload[0] as CHOICE; if none, CHOICE 0. Register layout
convention only: action value lives in payload[0].

Learner-side conventions provided: GOAL nodes (ref[0] =
target entity), ACTION-GUIDE nodes (ref[0] = context anchor,
ref[1] = GOAL, payload[0] = CHOICE value, payload[1] =
confidence, DEPENDS-ON to model/hypothesis nodes),
UNCERTAINTY records (created on QUERY -2; ref[0] = queried
key context), CONSEQUENCE structures (ACTION-GUIDE SUPPORTS
outcome node), procedure refs as means.

Learning loop: TEACH model facts; QUERY miss creates
UNCERTAINTY; goal formation and policy derivation are
learner-side processes writing ACTION-GUIDE nodes;
OBSERVE match raises utility of participants, mismatch
lowers utility plus CONTRADICTS edge plus re-derivation.

### 1D. Compose-ops provides

Ten operations: the six CLA primitives unchanged, plus four new:
- COPY(src) -> dst: structural duplication (node + internal
  links). The CREATE atom. Anti-oracle: understands nothing
  about what it copies.
- APPLY(structure, bindings) -> result: traverse structure,
  fill HOLE slots from bindings, execute primitive op nodes
  per the frozen computational basis {EQ, ADD} plus structural
  machinery (HOLE-bind, traverse, READ). The TEST atom and the
  missing query-time application from the W2/W3 analysis.
- CORROBORATE(structure, bindings, expected) -> outcome record:
  runs APPLY, compares with the basis equality predicate,
  writes a small outcome record (match/mismatch, tick) linked
  to the structure. Single case; the learner sequences cases.
- PROMOTE(node): marks the node retained (protection flag /
  utility credit the eviction policy reads). Marks, never
  decides worth. No DEMOTE (explicit minimality decision).

HOLE convention: one reserved payload value (sentinel like
max-int, fully generic like NULL). WRITE of HOLE marks a
bindable slot; APPLY fills HOLE slots from bindings.

Computational basis: frozen {EQ, ADD} plus structural
machinery. Identical across all worlds. FW3 (multiplication)
reachable only via learner-composed MUL-from-ADD; a basis
extension to pass FW3 is recorded as a treadmill failure (F6).

Bootstrap miss-policy (fixed, generic, replaceable): on QUERY
miss, the core consults the learner's registered miss-policy.
Bootstrap default: gather K most recent same-relation triples
via ACTIVATE; COPY one; READ+EQ to find varying positions;
WRITE HOLE; compositional trials over {EQ, ADD} to depth 2;
CORROBORATE each against held-out exemplars; PROMOTE the
first meeting the learner's corroboration threshold. The
bootstrap is replaceable: learner-built miss-handling
structures supersede the default.

Relation to CLA stated in the spec: the six ops adopted from
CLA-1; PROMOTE "plugs directly into CLA-1 section (d)"; APPLY
addresses gap G1. Note: the spec was written against CLA-1;
CLA-2 has since SUPERSEDED CLA-1 section (d). The plug point
has moved (see incompatibilities).

---

## Part 2: Integration points (exact connection details)

### IP-1. Shared node record format: COMPATIBLE, no change needed

All four specs use (type_tag, ref[4], payload[4]) with
learner-assigned tags the core never interprets. CAM-1's MAP
node, ACT's GOAL / ACTION-GUIDE / UNCERTAINTY nodes, and the
compose-ops procedure/law structures are all node-type
conventions in this one format. No format negotiation needed.

### IP-2. Shared edge vocabulary: COMPATIBLE, no change needed

CLA-2's extended vocabulary covers every edge type the other
three specs use:
- CAM-1: SUPPORTS (verification records), INSTANCE-OF (map to
  group), CONTRADICTS (revision), DEPENDS-ON (map protects
  exemplars). All present.
- ACT: DEPENDS-ON (policy to model/hypothesis), SUPPORTS
  (guide to outcome). All present.
- Compose-ops: LINK over the generic vocabulary. Present.
No new edge types are required by any spec. The audit rule
(no edge type names a domain concept) is satisfiable as is.

### IP-3. MAP node exemplar-group ref: COMPATIBLE via GROUP convention

CAM-1's MAP refs[2] (exemplar-group) points at a GROUP node
with MEMBER edges to the exemplar nodes, per CLA-2's GROUP
convention. Shared fate for the map and its exemplars falls
out of the aggregation. No change needed; builders must use
the GROUP/MEMBER convention rather than inventing a
group-table format.

### IP-4. CAM-1 PROMOTE into CLA-2 retention: RE-SPECIFY as edges

Compose-ops PROMOTE is specified as "protection flag / utility
credit that the eviction policy reads". CLA-2's eviction reads
PROTECTION edges and evidence-edge counts; there are no flags
and no utility credits. Integration: PROMOTE (whether as a
core op or a learner-side macro, see INCOMPAT-1) must
materialize as: (a) a PROTECTION edge on the promoted node
with a decay clock (the probation-at-birth rule already does
this on TEACH; PROMOTE extends/refreshes it), and (b)
SUPPORTS/CONFIRMS evidence edges from the verification
records. The promotion mark IS the authored edge set, not a
separate bit. Builders must not implement a per-node boolean
flag; that would be a second retention format and would fail
CLA-2's K2 ("no second memory engine").

### IP-5. ACT policy retention into CLA-2 retention: COMPATIBLE

ACT already specifies ACTION-GUIDE nodes linked DEPENDS-ON to
model/hypothesis nodes (shared fate via graph position) and
utility updated by OBSERVE outcomes. Under CLA-2 this maps to:
match -> USE/CONFIRMS evidence edges on participants;
mismatch -> CONTRADICTS edge plus DECAY pressure. No
action-specific retention code. The mapping must be written
into the ACT implementation plan (see INCOMPAT-8).

### IP-6. QUERY-miss sequencing: SPECIFY the order

CLA-2(f), CAM-1 APPLY-on-miss, and the compose-ops miss-policy
all attach behavior to QUERY miss. The integrated miss path,
in order:
1. Exact-key lookup. Hit -> CLA-2 QUERY-hit evidence rules.
2. On miss: create SURPRISE edges on the retrieval path
   (CLA-2 evidence rule; always runs).
3. Consult the registered miss-policy (see INCOMPAT-2). The
   miss-policy may invoke CAM-1 APPLY: retrieve candidate MAP
   nodes via ACTIVATE, bind, evaluate via core APPLY, arbitrate
   by standing. If an answer is produced: record USE on the
   answering MAP node and return it.
4. If no map applies: consult HISTORY for a regret match
   (CLA-2 rule); on match create the REGRET node and
   strengthen the path's evidence.
5. Return -2.

This ordering preserves W1 bit-for-bit behavior (step 1),
CLA-2's evidence accounting (steps 2, 4), and CAM-1's
construction (step 3). It requires the miss-policy register
(INCOMPAT-2) and the standing/bid arbitration rule
(INCOMPAT-11).

### IP-7. Computational basis {EQ, ADD}: FLAGGED, not changed here

The basis is researcher-authored capability, frozen once and
identical across worlds, with treadmill guards F3/F6 in the
spec. It does not branch on world identity. Whether this
satisfies the One-System Rule's "no new semantic cases" bar
for APPLY's executor is a judgment call reserved for Micah;
the spec's own justification (section 3) is the record. This
coordinator flags it as the one deliberate researcher-authored
capability in the integration, to be tracked in the per-
generation accounting as "computational basis ops: 2".

---

## Part 3: Incompatibilities

Twelve incompatibilities found. Each states the conflict, the
specs involved, and the minimal resolution. None is resolved
by this worker; resolutions marked [NEEDS-MICAH] require his
approval before builders implement.

### INCOMPAT-1. Core primitive count: 6 vs 10 [NEEDS-MICAH]

CLA-2 section (a) specifies six core primitives. The
compose-ops spec specifies ten (the six plus COPY, APPLY,
CORROBORATE, PROMOTE) and CAM-1's loop assumes the four new
operations exist. ACT needs only the six plus ACTIVATE.

Minimal resolution options:
(a) Extend CLA-2 section (a) to ten primitives, adopting the
four ops per COMPOSE_OPS_SPEC.md section 2.2, with the
PROMOTE plug point re-mapped from CLA-1(d) to CLA-2(d) via
IP-4 (edges, not flags).
(b) Keep six core primitives; implement COPY, CORROBORATE,
and PROMOTE as learner-side macros over the six, and add
only APPLY as a core op (it must execute at query time
inside the core's QUERY path, which learner code cannot do).

Recommendation: (a) for COPY and APPLY; the spec's F5
ablations ("removing COPY breaks CREATE", "removing APPLY
breaks TEST") are written against core ops, and APPLY at
query time cannot be learner-side. CORROBORATE and PROMOTE
are expressible learner-side (APPLY + EQ + WRITE + LINK for
the former; PROTECTION + evidence edges for the latter),
so a stricter minimal core would be eight primitives
(six + COPY + APPLY). But adopting the spec's ten keeps
the F5 predictions testable as written. Either choice is
architectural; Micah decides.

Note the tension with the long-term trajectory (specialized
source decreasing): every added core op must stay
decision-agnostic per the oracle test O1-O3, or it becomes
the treadmill.

### INCOMPAT-2. No miss-policy dispatch in the CLA-2 event loop [NEEDS-MICAH]

Compose-ops section 4 requires: on QUERY miss, the core
consults "the learner's registered miss-policy", with a
frozen generic bootstrap default that learner-built
structures supersede. CLA-2 section (f) has a fixed QUERY-
miss rule (SURPRISE, HISTORY, REGRET) with no dispatch
point and no register.

Minimal resolution: add one protected core register,
MISS_POLICY, holding a workspace node address (null
default). On QUERY miss, after the SURPRISE rule, the core
invokes the registered miss-policy structure; null means
the frozen bootstrap default. The bootstrap is core code
(frozen generic machinery); replacement policies are
learner-authored structures. This parallels ACT's
POLICY_ROOT (same mechanism class, different event).

Without this, CAM-1's APPLY-on-miss has no invocation path
and the compose-ops bootstrap cannot run. This is the
single most load-bearing integration amendment.

### INCOMPAT-3. ACT utility selection vs CLA-2 evidence bid [NEEDS-MICAH]

ACT step 5 selects "the node with the highest utility (the
CLA-1 utility ledger; every node carries learner-updated
utility)". CLA-2 superseded the utility ledger as a per-node
scalar: bid(node) is a linear count over learner-authored
evidence edges. There is no per-node utility value for ACT
to read.

Minimal resolution: re-specify ACT step 5 as "select the
match with the highest CLA-2 evidence bid (count over USE /
CONFIRMS / SUPPORTS edges per the eviction aggregation)".
One-line change to the ACT prereg. The core already
computes bid(node) for eviction; ACT reuses the same
function. This also unifies action selection with retention
(the same bid governs both), which is the desired
architectural compression.

### INCOMPAT-4. ACT registers absent from CLA-2 [NEEDS-MICAH]

ACT needs POLICY_ROOT and the 4-event context register.
CLA-2 specifies neither. POLICY_ROOT appears only in the
ACT prereg; the context register appears only there as well
("generic bookkeeping the event loop already performs" is
asserted, not specified).

Minimal resolution: add both registers to CLA-2's protected
core state: POLICY_ROOT (workspace node address, null
default, learner-set) and a 4-slot event-context ring
(refs of the last 4 events, maintained by the event loop).
Both are content-free bookkeeping. Small addition; needs
approval because it changes the core register file.

### INCOMPAT-5. CAM-1 MAP payload exceeds payload[4] for order >= 1 [NEEDS-MICAH]

CAM-1's MAP payload is [body-kind, coefficient slots...,
corroboration count, standing]. payload[4] is fixed.
Order 0 fits: [0, literal, corroboration, standing].
Order 1 (W3: z = a*x + b*y + c) needs body-kind + 3
coefficients + corroboration + standing = 6 slots. Does
not fit. Order 2 (FW3 discriminator) is worse.

Minimal resolution (recommended): chain coefficient nodes.
MAP refs become [trigger-relation, parameter-dimension,
exemplar-group, coeff-chain]; the coeff-chain is an
ordinary linked list of COEFF nodes (learner-assigned
type), each carrying up to 4 coefficients in payload.
Corroboration count and standing are NOT stored in
payload at all: corroboration count is the number of
SUPPORTS edges (counted, not stored), and standing is
SUPPORTS count minus CONTRADICTS count (see INCOMPAT-11).
This is more CLA-2-native than the prereg's payload
counters: it replaces stored scalars with counted edges,
exactly the consolidation's philosophy ("no weights,
count edges"). MAP payload is then [body-kind, reserved,
reserved, reserved], and even order-0 fits with room.

Alternative: widen the node record. Rejected: it changes
the one shared format (IP-1) for all specs.

### INCOMPAT-6. Regularity-detection location: finite differences vs trials [NEEDS-MICAH]

This is the deepest architectural incompatibility.

CAM-1's PROPOSE specifies P-DEP via "successive
finite-difference analysis, ONE generic mathematical
operation", with "generic integer difference/fit/evaluate
routines" in the core. The compose-ops spec freezes the
computational basis at {EQ, ADD} and discovers regularities
by trial: compose basis expressions, CORROBORATE each,
keep what predicts. Finite differences require SUBTRACTION;
SUB is not in {EQ, ADD}, and adding it edges toward the
arithmetic treadmill Micah prohibited (the SUB/DIV/PARITY
ruling).

So CAM-1's P-DEP as written cannot be built from the
compose-ops basis, and the compose-ops trial mechanism
cannot perform CAM-1's finite-difference analysis. The two
specs place regularity-detection intelligence in different
locations: CAM-1 puts a smart PROPOSE in the core learn
path; compose-ops puts dumb ops in the core and the trial
policy in the learner (with a fixed generic bootstrap).

Minimal resolution options:
(a) Re-specify CAM-1's P-DEP as trial-based search over
the frozen basis (align -> HOLE -> basis trials ->
corroborate), retiring the finite-difference core routine.
PROPOSE becomes a learner-side policy over the ten ops;
the compose-ops bootstrap is its initial form. This is
the most Micah-aligned option (core provides mechanism,
learner provides policy; no SUB).
(b) Keep finite-difference analysis as a core routine with
Micah's explicit approval, treating difference/fit as
generic mathematical operations distinct from the
prohibited operator treadmill. This preserves CAM-1 as
written but adds researcher-authored mathematical
capability to the core, and needs a principled boundary
for why SUB-in-service-of-fitting is allowed while
SUB-as-basis-op was rejected.

Recommendation: (a). Under (a), CAM-1's four operations
are learner-side policies over the ten core ops, not
additional core machinery: PROPOSE = ACTIVATE + READ + EQ
grouping + COPY + WRITE HOLE + basis trials; VERIFY =
CORROBORATE sequencing + SUPPORTS links; PROMOTE =
IP-4 edge authoring; APPLY = miss-policy retrieval +
core APPLY + standing arbitration. The unity claim
(W2/W3 same mechanism) is preserved: both are trial-
discovered regularities in the MAP format.

This is genuinely architectural and must go to Micah.

### INCOMPAT-7. CAM-1 G3 fixed K vs compose-ops learner-state threshold [NEEDS-MICAH]

CAM-1 guard G3: the corroboration minimum K and demotion
threshold are "single constants, identical for W2-class
and W3-class worlds". Compose-ops: "The threshold lives
in learner state (O1, O3)". Fixed constant vs learner-
owned value.

Minimal resolution: K starts as a preregistered bootstrap
constant (satisfying G3's anti-tuning intent: one K for
all world classes), recorded in a learner-state node that
the strengthen rule can revise with experience (satisfying
the learner-ownership requirement and Micah's LORG Q1
ruling). The initial value is fixed; its subsequent
history is learned. Document the initial K in the
implementation prereg.

### INCOMPAT-8. ACT's utility-ledger references point at superseded CLA-1(d) [NEEDS-MICAH]

ACT section 3: "raise the utility of the participating
ACTION-GUIDE, GOAL, and model nodes (the CLA-1 section d
update rules)". CLA-2 SUPERSEDED CLA-1 section (d). There
are no utility update rules anymore; there are evidence
rules.

Minimal resolution: remap the vocabulary. "Raise utility"
-> author USE / CONFIRMS evidence edges on the
participants (via the OBSERVE rule). "Lower utility" ->
create CONTRADICTS edge from outcome to expectation and
let DECAY pressure apply. "Re-derivation" -> the
contradiction triggers the learner's policy-derivation
process over fresh evidence (already specified in ACT
section 3's last sentence). No semantic change to the
ACT design; it is a re-targeting onto the consolidated
substrate. One-paragraph amendment to the ACT prereg.

### INCOMPAT-9. Bootstrap-to-CAM-1 supersession protocol unspecified [NEEDS-MICAH]

The compose-ops bootstrap is "replaceable: as the learner
builds better miss-handling structures, they supersede the
default." CAM-1 is the better miss-handling structure. But
neither spec states the replacement condition or mechanism:
when does the learner's MISS_POLICY stop being the
bootstrap and start being CAM-1? What does the learner
write, and where?

Minimal resolution: specify the supersession protocol.
Recommended: when the learner has at least one promoted
MAP node, its miss-policy process writes the address of
its own dispatch structure into MISS_POLICY (via the
register-write mechanism, INCOMPAT-12), superseding the
bootstrap. The bootstrap remains as the null-default for
a fresh learner. The condition ("at least one promoted
MAP") is observable in workspace content, not a source
branch. Until the protocol is specified, builders cannot
implement replacement; they can only implement the
bootstrap.

### INCOMPAT-10. HOLE sentinel absent from CLA-2 [NEEDS-MICAH]

Compose-ops defines HOLE as one reserved payload value
(sentinel like max-int). CLA-2's core conventions do not
include it. The sentinel is content-free (like NULL) and
the alternative (learner-assigned variable tags with a
core registry) was considered and rejected in the spec.

Minimal resolution: add the HOLE sentinel to CLA-2's core
conventions: one reserved payload value, defined in the
frozen core, never assigned by the learner to real data.
APPLY treats it as a bindable slot. Small addition;
needs approval because it reserves part of the payload
value space.

### INCOMPAT-11. Bid function sign of CONTRADICTS unspecified [NEEDS-MICAH]

CLA-2: bid(node) = "fixed linear count over the node's
learner-authored evidence edges". CAM-1's revision
mechanism needs standing to DECREASE under contradiction:
"later contradictory evidence creates CONTRADICTS edges
and decrements standing; when standing falls below the
demotion threshold the map is demoted". If bid counts
CONTRADICTS as positive evidence, contradiction would
protect the contradicted map: backwards.

Minimal resolution: specify the bid as a signed count:
SUPPORTS / CONFIRMS / USE edges contribute +1;
CONTRADICTS edges contribute -1. The aggregation stays
a fixed linear count (still content-free; the core does
not weigh edge kinds differently beyond the sign, which
is part of the fixed vocabulary semantics). CAM-1's
"standing" is then exactly bid(map-node), unifying the
revision mechanism with the retention mechanism: a
demoted map (bid below threshold) is both skipped by
APPLY and a preferred eviction candidate. This is the
desired compression: one number serves retention and
revision.

### INCOMPAT-12. Register write mechanism unspecified [NEEDS-MICAH]

ACT: "The learner sets this register through ordinary
workspace operations; source code never sets it." Neither
ACT nor CLA-2 specifies HOW a learner-side process writes
a protected core register. The six primitives have no
register-write operation.

Minimal resolution (recommended): reserve low node
addresses as register slots. Node 0's payload[0] is
POLICY_ROOT; node 1's payload[0] is MISS_POLICY; the
context ring is core-maintained (not learner-written).
WRITE to these addresses via the ordinary WRITE primitive
sets the registers; the core reads them on ACT / QUERY-
miss. No new primitive; the reservation is a documented
address convention, auditable by inspection. The
alternative (a seventh primitive, e.g. SETREG) adds core
surface; the reservation approach is smaller.

---

## Part 4: Amendments requiring Micah's approval (checklist)

The builders must not implement until these are ruled on.
Each is minimal and stated as a concrete prereg edit.

A1. [INCOMPAT-1] CLA-2 section (a): adopt COPY/APPLY/
CORROBORATE/PROMOTE per COMPOSE_OPS_SPEC.md 2.2 (option
(a)), or six + APPLY only (option (b)). Core op count
goes 6 -> 10 or 6 -> 8.

A2. [INCOMPAT-2] CLA-2: add MISS_POLICY protected register
(null default; learner-set; bootstrap default behavior
specified in the implementation prereg).

A3. [INCOMPAT-3] ACT step 5: select by CLA-2 evidence bid,
not per-node utility scalar.

A4. [INCOMPAT-4] CLA-2: add POLICY_ROOT register and
4-event context ring to protected core state.

A5. [INCOMPAT-5] CAM-1 MAP format: coefficient chain via
refs[3]; corroboration/standing derived from SUPPORTS /
CONTRADICTS edge counts, not payload scalars.

A6. [INCOMPAT-6] CAM-1 P-DEP: re-specify as trial-based
search over the frozen basis (option (a)), or approve
finite-difference core routines explicitly (option (b)).

A7. [INCOMPAT-7] CAM-1 G3: K starts as a preregistered
bootstrap constant in a learner-state node, revisable by
the strengthen rule.

A8. [INCOMPAT-8] ACT section 3: remap "raise/lower utility"
to USE/CONFIRMS/CONTRADICTS evidence-edge operations.

A9. [INCOMPAT-9] Specify the bootstrap-to-CAM-1
supersession protocol (recommended: first promoted MAP
node triggers the learner writing its dispatch address
into MISS_POLICY).

A10. [INCOMPAT-10] CLA-2 core conventions: add the HOLE
payload sentinel.

A11. [INCOMPAT-11] CLA-2 bid function: signed count
(SUPPORTS/CONFIRMS/USE +1, CONTRADICTS -1).

A12. [INCOMPAT-12] Register-write mechanism: reserved
node addresses 0 and 1 (POLICY_ROOT, MISS_POLICY),
writable via ordinary WRITE.

Plus one flagged judgment (no edit proposed):
J1. [IP-7] The {EQ, ADD} computational basis is
researcher-authored capability. Track as "computational
basis ops: 2" in the per-generation accounting. Whether
it satisfies the One-System Rule is Micah's call.

Recommended package: A1(a) with the 8-op strict-minimum
noted as fallback; A2; A3; A4; A5; A6(a); A7; A8; A9;
A10; A11; A12. Under this package the core gains: 4 ops,
3 registers (POLICY_ROOT, MISS_POLICY, context ring),
1 sentinel, and the bid/evidence-rule refinements. Zero
new modes, zero new bridges, zero task-specific handlers,
zero new edge types, zero new state formats. The
intelligence (which regularities to pursue, which
policies to write, when to promote) stays in learner
state in all cases.

---

## Part 5: Builder monitoring (read-only)

Checked 2026-09-30 at spec writing time. Branch state:
newest commits are the C1 pure-Zag race prereg (56e8d404a),
the FW1-FW9 seal (396895595), C1 baseline results
(8a2929098), and the tooling audit (70c520637).

- CLA-2 builder: no implementation commit after prereg
  24351fd31. The continuing_learner/ directory contains
  the older contlearn2 implementation (179b4a950), which
  is the competing control lane per ruling D, not the
  CLA-2 builder. No divergence.
- CAM-1 builder: no implementation commit after prereg
  68a41be8a. No divergence.
- ACT builder: no implementation commit after prereg
  51a818141. No divergence.
- Compose-ops: spec only (881b17638), no builder assigned
  in this lane; its ops are inputs to the CLA-2 builder
  per A1.

No builder has started implementing. Nothing to flag.
The builders should not start until the A1-A12 amendments
are ruled on; implementing against the unamended preregs
would bake in the incompatibilities above (in particular
INCOMPAT-2, without which CAM-1 has no invocation path,
and INCOMPAT-5, without which MAP nodes cannot carry
polynomial bodies).

---

## Part 6: What this specification does NOT do

- It does not amend any prereg. All amendments are listed
  as proposals for Micah in Part 4.
- It does not write implementation code. Coordination and
  verification only, per the task brief.
- It does not access the sealed FW1-FW9 world files.
- It does not change the frozen bars of any spec: K1/K2/K3
  kill bars, CAM-1's S1-S3 split bar, the compose-ops
  F1-F7 falsifications, and ACT's F-ACT1-F-ACT4 all stand
  as written. The amendments are interface refinements;
  none weakens a falsification condition.
- It does not resolve INCOMPAT-6 option (a) vs (b) or the
  A1 10-op vs 8-op choice. Those are Micah's.

## One-System Rule accounting (this lane)

- Cognition source lines added: 0 (specification only).
- New hardcoded semantic cases: 0. New modes: 0.
- New bridges: 0. New task-specific handlers: 0.
- New state formats: 0. Learner-state structures: 0.
- Standing question for the integration ("why can the
  existing specs not compose as written"): because three
  specs were authored against CLA-1's utility-ledger
  vocabulary and one against a superseded retention
  section, while the fourth (CLA-2) replaced both with
  counted evidence edges; and because the invocation
  paths (miss dispatch, register writes) were assumed by
  the consumers but never specified by the substrate.

## Verdict

INTEGRATION-SPEC-COMPLETE. Twelve incompatibilities
documented, integration points specified, twelve minimal
amendments plus one flagged judgment listed for Micah's
approval, builders monitored with no divergence found.
