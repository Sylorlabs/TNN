# Minimal Structural Operations: Decomposing Compose-Verify-Promote

Date: 2026-09-30. Worker: Minimal Structural Operations Investigator.
Status: COMPOSE-OPS-INVESTIGATION-COMPLETE. Analysis/prereg only; no
implementation in this commit.

Sources: L3 integration scout (`l3_integration/INTEGRATION_SCOUT.md`,
commit d7bddbc56); W2/W3 shared-cause analysis
(`w2w3_analysis/W2W3_ANALYSIS.md`, commit 2121fd16d); CLA-1 prereg
(`continuing_learner/PREREG_CLA1.md`, commit b4f61ff8a).
Micah's ruling: compose-verify-promote is a legitimate frontier, but
it must not be hardcoded as one giant intelligent oracle.

## 1. The oracle test (decomposition principle)

An operation is an oracle, and therefore forbidden, if it does the
learning rather than enabling it. The test applied to every candidate
below:

- (O1) The operation's specification must not mention task content:
  no procedures, laws, steps, sums, or grammars appear in any spec.
- (O2) The operation must be decision-agnostic: given random or
  adversarial learner choices, it must produce garbage or fail
  cleanly, not correct answers. If capability survives randomized
  learner decisions, the intelligence lives in the core, not the
  learner.
- (O3) The operation must be phase-local: it performs one dumb
  transformation (copy, bind, compare, mark). Any behavior that
  spans "notice a regularity, build the right structure, and confirm
  it" is at least two operations improperly fused.

The decomposition principle: the core provides mechanism, the learner
provides policy. Every choice that affects *which* regularity is
pursued, *what* counts as corroborated, and *when* a structure is kept
belongs to learner state. The core executes the learner's choices and
nothing else.

## 2. The proposed minimal operation set

Ten operations total: six adopted unchanged from CLA-1, four new.
The four new ops map exactly onto the three phases: CREATE needs
COPY; TEST needs APPLY and CORROBORATE; RETAIN needs PROMOTE.
Abstraction is deliberately NOT a core operation (see 2.2).

### 2.1 Adopted from CLA-1 (unchanged)

1. **ALLOC** -> node id. Core: reserves one fixed-size node record
   (type_tag, ref[4], payload[4]), returns its id. Learner: when to
   allocate, what type_tag to assign through use.
2. **WRITE**(node, field, value). Core: stores bytes. Learner: all
   content, including type tags and variable markers.
3. **LINK**(src, dst, edge_type). Core: stores a typed edge.
   Learner: topology and edge choice from the generic vocabulary.
4. **READ**(node, field) -> value. Core: returns bytes. Learner:
   what to read and how to interpret it.
5. **ACTIVATE**(node) -> neighbor set. Core: spreading retrieval
   over links. Learner: starting points and interpretation.
6. **DECAY**(node). Core: passive reduction of retention strength.
   Learner: nothing directly; counteracted via PROMOTE.

### 2.2 New: the construct-and-apply loop

7. **COPY**(src) -> dst. Core: duplicates a structure (the node and
   its internal links), returns the new root id. This is the CREATE
   atom: it gives the learner starting material for variation.
   Learner: which structure to copy, what to change afterward.
   Anti-oracle: COPY understands nothing about what it copies.
   Note: abstraction is a learner-level procedure built from COPY
   plus WRITE of a HOLE marker (see 2.3), not a core operation.
   Fusing "copy and generalize" into one ABSTRACT op would hide the
   learner's choice of *which* positions to generalize, which is
   exactly the learning decision (O3).

8. **APPLY**(structure, bindings) -> result. Core: traverses the
   given structure; fills HOLE slots from bindings; executes
   primitive op nodes per the frozen computational basis (section 3);
   returns the output value or a clean failure. This is the TEST
   atom and the missing "application at query time" from the W2/W3
   analysis. Learner: which structure to apply, which bindings to
   supply (drawn from the query), what to do with the result.
   Anti-oracle: APPLY does not know procedures from laws. Given a
   procedure structure it binds and looks up; given a law structure
   it computes; given garbage it returns garbage or fails. (O2)

9. **CORROBORATE**(structure, bindings, expected) -> outcome record.
   Core: runs APPLY(structure, bindings), compares the result to
   expected with the basis equality predicate, writes a small
   outcome record (match/mismatch, tick) linked to the structure.
   Single case only. The learner sequences multiple cases through
   its own policy loop, one event at a time. Learner: which cases
   to test, what corroboration threshold justifies promotion.
   Anti-oracle: CORROBORATE records; it does not judge. The
   threshold lives in learner state (O1, O3).

10. **PROMOTE**(node). Core: marks the node retained (protection
    flag / utility credit that the eviction policy reads, per
    CLA-1 section d and the LORG protection-set idea). Learner:
    when to promote, based on corroboration history it reads.
    Anti-oracle: PROMOTE marks; it never decides worth. A learner
    that promotes everything experiences the resource pressure
    Micah's Q2 ruling requires; the core does not rescue it with
    exception tables.
    Note: no DEMOTE operation is proposed. Structures that fail
    verification are simply never promoted, and DECAY reclaims them.
    This is an explicit minimality decision, falsifiable per F5.

### 2.3 The HOLE convention

One reserved payload value, HOLE, is defined by the core (a sentinel
like a max-int value, fully generic, like NULL). WRITE of HOLE into a
position marks a bindable slot; APPLY fills HOLE slots from bindings.
The learner assigns all other meaning. Alternative considered and
rejected for now: learner-assigned variable tags with a core
registry. The sentinel is simpler and equally generic; the registry
variant remains a compression candidate if the sentinel ever collides
with legitimate payloads.

### 2.4 Per-operation core vs learner table

| Op | Core provides (mechanism) | Learner decides (policy) |
|---|---|---|
| ALLOC | blank record, fresh id | when; type_tag via use |
| WRITE | byte storage | all content incl. HOLE placement |
| LINK | typed edge storage | topology |
| READ | byte retrieval | what to read; interpretation |
| ACTIVATE | spreading retrieval | seeds; interpretation |
| DECAY | passive weakening | nothing (counter via PROMOTE) |
| COPY | structural duplication | what to copy; what to vary |
| APPLY | traversal, binding, basis execution | which structure; bindings; use of result |
| CORROBORATE | apply, compare, record | which cases; promotion threshold |
| PROMOTE | retention mark eviction reads | when to promote |

## 3. The computational basis question (frozen, minimal)

APPLY needs a primitive vocabulary for the nodes it executes. For
W2, no computation is needed: binding plus traversal plus lookup
suffices. For W3, the learner must compose addition from something.
The proposal: a frozen minimal basis of **{EQ, ADD}** plus the
structural machinery (HOLE-bind, traverse, READ). EQ serves
CORROBORATE and the learner's own position-comparison; ADD serves
W3-class computation.

Why not a larger basis: every basis op is researcher-authored
capability, and Micah's standing rule forbids recreating the
arithmetic treadmill (the SUB/DIV/PARITY prohibition). The basis is
frozen once, identical across all worlds, and the learner still does
all composing. The sharp falsifiable consequence: FW3
(multiplication, per the FW1-FW9 design) is reachable ONLY via
learner-composed MUL-from-ADD (repeated addition as a
learner-built structure). If the program instead extends the basis
with MUL to pass FW3, that event is recorded as a treadmill
failure, not a success (see F6).

Why not a smaller basis (pure structural, no ADD): W3's regularity
is computation over inputs (per the W2/W3 analysis, invariance vs
computation are different faces). A structural-only APPLY cannot
evaluate x+y for unobserved pairs; the W3 trace in section 5 would
have a missing step, which is exactly falsification condition F4.

## 4. The bootstrap trigger policy (fixed, generic, replaceable)

Operations do not invoke themselves. The minimal honest story for
what starts the loop:

- On QUERY miss (the -2 path), the core consults the learner's
  registered miss-policy: a learner-owned structure saying what to
  do. Initially this is the bootstrap default, which is frozen
  generic machinery like the six primitives.
- Bootstrap default (fixed, task-blind): gather the K most recent
  triples sharing the query's relation (via ACTIVATE spreading);
  COPY one; pairwise READ plus EQ across the set to find varying
  positions; WRITE HOLE at varying positions; run compositional
  trials over the frozen basis up to a preregistered bound
  (depth 2, the same bound shape as L3B's, but over 2 basis ops,
  not a 205-program menu); CORROBORATE each trial against
  held-out exemplars; PROMOTE the first trial meeting the
  learner's corroboration threshold.
- The bootstrap knows nothing about procedures, steps, or sums.
  It knows: vary positions, try basis compositions, test, keep
  what predicts. (O1)
- Crucially, the bootstrap is replaceable: as the learner builds
  better miss-handling structures, they supersede the default.
  Even the trigger policy becomes learner-owned over time. A
  frozen irreplaceable trigger would be oracle residue.

Open question (thin part, stated plainly): the compositional-trial
bound and the K for exemplar gathering are researcher-set
constants. Per Micah's LORG Q1 ruling, the program must test
whether these choices are load-bearing and move selection into
learner state where possible. The preregistered bound is a
starting measurement, not a principled value.

## 5. Worked composition: W2 (procedure from demonstrations)

Experience: 15 triples, three instances 8001..8003, each with
(instance, 801..804, op 9501..9504). The step to op mapping is
invariant across instances.

1. QUERY (8004, 801): exact lookup misses, -2. Miss-policy fires.
2. ACTIVATE from (8004, 801) spreads to recent same-relation
   triples: (8001,801,9501), (8002,801,9501), (8003,801,9501).
3. Learner: COPY the first; pairwise READ+EQ finds the subject
   position varying (8001/8002/8003), relation and object
   constant; WRITE HOLE at subject: (HOLE, 801, 9501). Repeat
   for relations 802, 803, 804.
4. Learner: ALLOC procedure node P; WRITE its ref slots to the
   four step-mappings (no new edge vocabulary needed; the node
   record's ref[4] carries part-whole directly).
5. VERIFY: hold out instance 8003. APPLY(P, {HOLE:=8003}) for
   step 801: traverse P, find (HOLE,801)->9501, bind, return
   9501. CORROBORATE against observed (8003,801,9501): match.
   Repeat 802..804: 4/4.
6. Learner: PROMOTE(P). The 15 raw triples remain unpromoted
   and decay.
7. Novel QUERY (8004, 802): exact miss; ACTIVATE spreads via
   DEPENDS-ON links from the exemplar triples to P; learner
   selects P; APPLY(P, {HOLE:=8004}) returns 9502.

Zero basis-arithmetic invocations occur anywhere in this trace.
That is falsifiable prediction P1: the structural path alone
carries W2, proving APPLY's binding/traversal is sufficient and
the computational basis does no work here.

## 6. Worked composition: W3 (law from examples)

Experience: 8 pairs 9001..9008, each with (pair,601,x),
(pair,602,y), (pair,600,x+y).

1. QUERY (9011, 600): after observing (9011,601,x) and
   (9011,602,y), exact lookup of (9011,600) misses, -2.
   Miss-policy fires.
2. ACTIVATE spreads to the pair triples. Learner: COPY the
   pattern; WRITE HOLE at the varying subject position:
   (HOLE,601,Vx), (HOLE,602,Vy), (HOLE,600,Vz).
3. Compositional trials over frozen {EQ, ADD}, depth <= 2,
   binding input positions to predict the output position.
   Candidates: ADD(Vx,Vy), EQ(Vx,Vy), ADD(Vx,Vx),
   ADD(Vy,Vy), ADD(ADD(Vx,Vy),Vx), ...
4. CORROBORATE each against the 8 exemplars: ADD(Vx,Vy)
   matches 8/8 on Vz; all others fail. The trace shows ADD
   selected and alternatives rejected: this is the
   anti-hardcoding evidence. The learner chose; the core
   executed.
5. Learner: ALLOC law node L with refs to the ADD composition
   over (HOLE,601) and (HOLE,602), output (HOLE,600); LINK L
   DEPENDS-ON the exemplar triples.
6. Learner: PROMOTE(L).
7. Novel QUERY (9012, 600) with inputs observed: exact miss;
   ACTIVATE finds L; APPLY(L, {HOLE:=9012}): READ (9012,601)
   -> x, READ (9012,602) -> y, execute ADD -> x+y. Returns
   the sum.

This is falsifiable prediction P2: the trace must show basis
alternatives genuinely tried and rejected, not ADD
pre-selected. A trace where only ADD is ever tried is
indistinguishable from hardcoding and fails the claim.

## 7. Falsification

Too big (oracle smuggling):
- F1: Randomize the learner's policy choices (which positions
  to hole, which basis ops to try, promotion threshold).
  Capability must collapse to -2. If W2/W3 still pass, the core
  is the oracle and the decomposition is rejected.
- F2: If any operation's spec is found to mention task content
  (procedure, law, step, sum), that operation is smuggling and
  is removed or re-specified.
- F3: If the computational basis grows per world or per
  failure, the program has entered the treadmill; the basis
  extension is recorded as a failure event, not progress.

Too small (capability unreachable):
- F4: Attempt the section 5 and 6 traces under a preregistered
  optimal learner policy using only these ten ops. If any step
  has no legal construction, the set is insufficient and the
  missing step names the required addition.
- F5: Ablate each of the four new ops in turn (replace with
  learner-level reimplementation or remove). Predicted: removing
  COPY breaks CREATE (no variation material); removing APPLY
  breaks TEST (nothing executes); removing CORROBORATE breaks
  TEST (no recorded evidence); removing PROMOTE breaks RETAIN
  (verified structures decay like noise). If a phase survives
  its op's removal, the op was not minimal.
- F6: FW3 (multiplication) must be reachable via
  learner-composed MUL-from-ADD within the trial bound, or the
  bound/basis choice is falsified. Note carefully: this
  falsifies the bound/basis parameters, not the four-op set;
  the op set stands or falls on W2/W3 (F4).

Discrimination:
- F7: W2 must pass with zero basis-arithmetic invocations in
  the trace (P1). W3 must pass with a trace showing ADD
  selected among tried alternatives (P2). These separate the
  structural path from the computational path and prove neither
  is doing the other's work.

## 8. Relation to CLA-1: extension, not replacement

The six CLA-1 primitives are storage, structure, and retrieval.
The four new operations are the construct-and-apply loop the
W2/W3 analysis proved missing (no regularity-to-structure path,
no persistent function format, no query-time application).
Nothing in CLA-1 is removed or altered; the workspace format
(type_tag, ref[4], payload[4]) is unchanged, and procedures and
laws arrive as new learner-assigned node-type conventions, not
new stores.

PROMOTE plugs directly into CLA-1 section (d): it is the
operation by which the learner writes the protection set and
utility ledger that the generic eviction reads. APPLY addresses
CLA-1 gap G1 (incremental executable construction): it is the
executor over learner-built structure that G1 needs. The HOLE
sentinel is one reserved payload value, not a semantic case:
it carries no domain meaning.

## 9. Open questions (stated plainly)

- Q1: The compositional-trial bound (depth 2) and exemplar
  gathering constant K are researcher-set. Test whether they
  are load-bearing; move selection into learner state where
  possible (Micah's LORG Q1 ruling applies here too).
- Q2: COPY vs learner-level rebuild (ALLOC+WRITE+LINK
  traversal). COPY is specified as a core op for the CREATE
  phase; the traversal alternative is slower but sufficient.
  The F5 ablation should test whether COPY earns its place.
- Q3: CORROBORATE is single-case by design; multi-case testing
  is learner policy sequenced over events. If learner-side
  sequencing proves unworkable, a bounded multi-case variant
  may be needed, but that variant risks becoming a
  verify-oracle and needs its own O1-O3 audit.
- Q4: The {EQ, ADD} basis is the smallest basis reaching W3.
  Whether EQ alone plus learner-constructed arithmetic is
  reachable (the elegant extreme) or MUL must join the basis
  (the treadmill-adjacent compromise) is an experimental
  question for the FW3 discriminator, per F6.

## 10. Frozen predictions

- P1: W2-class behavior is reachable via the structural path
  with zero basis-arithmetic invocations in the trace.
- P2: W3-class behavior is reachable with a trace showing ADD
  selected among genuinely tried basis alternatives.
- P3: Randomizing learner policy choices collapses both
  capabilities to -2 (anti-oracle, F1).
- P4: Each of the four new ops is load-bearing per the F5
  ablations; no phase survives its op's removal.
- P5: FW3 is reachable via learner-composed MUL-from-ADD or
  the bound/basis parameters are falsified (F6); a basis
  extension to pass FW3 counts as a treadmill event.

## ONE-SYSTEM RULE accounting (this investigation)

- Cognition source lines added: 0 (analysis only).
- New hardcoded semantic cases: 0. New modes: 0. New bridges: 0.
- New task-specific handlers: 0.
- Proposed new core operations: 4 (COPY, APPLY, CORROBORATE,
  PROMOTE), each phase-local and decision-agnostic per O1-O3.
- Learner-state structures created: 0 (none built; the
  investigation specifies the format they would take:
  procedure nodes, law nodes, HOLE slots, corroboration
  records, promotion marks, all learner-assigned).
- Standing question answered ("why can the existing
  architecture not learn this"): because no operation exists
  that copies with variation, executes learner structure, tests
  predictions against experience, or marks retention; the
  proposal adds exactly those four, and nothing else.
