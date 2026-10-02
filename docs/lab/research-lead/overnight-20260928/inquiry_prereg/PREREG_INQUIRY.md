# PREREG: Learner-Driven Inquiry (INQUIRY-1)

Date frozen: 2026-09-30. Author: Inquiry Prereg Author (subagent).
Status: FROZEN. No implementation may begin before this commit.
Predecessor: inquiry scout, commit `b4853a9f7`
(`docs/lab/research-lead/overnight-20260928/inquiry_scout/INQUIRY_SCOUT.md`).
Verdict label target: INQUIRY-BUILD-PASS or INQUIRY-BUILD-FAIL.

## 0. What this experiment decides

The ACT read path (Piece C) is built and red-teamed: it can read
learner-state structures and emit actions (ACT build commit
`f7d87938f`; bid aligned to directional semantics, commit
`75a9b0e04`). The current ACT tests pass because test
scaffolding (`mk_uncert` at act.zag line 252, `mk_guide` at
act.zag line 244) creates the UNCERTAINTY nodes and the
ACTION-GUIDEs. The learner itself creates neither.

This experiment decides whether the two missing pieces can be
learner-side workspace processes, or whether inquiry remains
researcher-driven:

- Piece A (uncertainty reification): a learner-side process that
  creates UNCERTAINTY nodes from admission events automatically,
  as part of normal operation.
- Piece B (inquiry guide construction): a learner-side process
  that derives ACTION-GUIDEs anchored at live UNCERTAINTY nodes,
  selecting information-seeking acts, using only generic
  primitives.

H0 (researcher-driven): inquiry happens because the researcher
supplied the uncertainty-to-action mapping (in guides, in a
scoring rule, or in equivalent machinery).
H1 (learner-driven): the learner constructs the
uncertainty-to-action mapping from its own experience, and the
mapping tracks the learner's actual uncertainty.

## 1. Definitions (frozen for this experiment)

**Learner-side workspace process.** A set of executable
structures stored in the learner workspace (EXECUTE-compatible
graphs or event-loop rules written with the frozen ISA), invoked
through the ordinary event flow, composed only of frozen generic
primitives (ALLOC, READ, WRITE, LINK, COPY, EQ, ADD, BRANCH,
APPLY/EXECUTE, generic register operations, per the ISA boundary
ruling at commit `0525377f3`). It may not branch on domain
identity, relation identity, task identity, uncertainty type,
or uncertainty content. Any such branch found by source
inspection fails K-INQ2 and triggers F-INQ5.

**UNCERTAINTY node (convention, from the ACT prereg section 2c,
commit `51a818141`).** Created when a query returns an admission
code. ref[0] = the queried key context node address. Payload
carries a type marker distinguishing ignorance from conflict
(marker values frozen by the implementation and reported in its
build report; the marker must be workspace content written by
the reification process, not a core tag).

**Admission codes (frozen observable interface).**
-2 = ignorance admission: query on a key for which no rule
fires (existing behavior).
-3 = conflict admission: query on a key for which two or more
ACTIVE rules fire with different predictions (new observable;
emitted by the query path; the emission logic is ordinary
query-path bookkeeping, not an inquiry decision).

**Live UNCERTAINTY node.** A node created by an admission event
that has not been resolved: no subsequent successful query on
its key context, and (for conflict) no demotion of a
contradicted rule. Liveness must be workspace-computable from
edges and subsequent events, not a core flag. The
implementation freezes its liveness convention in its build
report.

**ACTION-GUIDE (inquiry).** A guide node with ref[0] = the
UNCERTAINTY node address it is anchored at, payload[0] = the
selected CHOICE value. For this experiment the action
interface offers exactly two acts: INQUIRE (CHOICE 30), which
produces an OBSERVE resolving the uncertainty, and DECOY
(CHOICE 31), which produces no observation.

**Creation trace (frozen audit requirement).** Every
UNCERTAINTY node and every ACTION-GUIDE created during the
experiment must carry a complete creation trace: (a) a LINK
edge from the created node to the triggering event or node,
(b) a process identifier naming the workspace process that
wrote it (frozen vocabulary, reported in the build report),
(c) no authorship by test scaffolding, fixtures, or core code.
Any node without a complete learner-side trace fails K-INQ2
and triggers F-INQ1 (uncertainty) or F-INQ2 (guide).

**E-ruling (inquiry analog of the COMP-1 expected-value
ruling).** The guide-construction process receives as input
only the UNCERTAINTY node address and readable workspace
state. It never receives the correct act, the act
consequences, or any label distinguishing INQUIRE from DECOY
through any channel except the world's act consequences
during the experience window. Verified by source inspection
and by the experience-window design (section 3).

## 2. Architectural constraints (frozen)

C1. Pieces A and B are learner-side workspace processes per
the definition above. No core source changes are authorized
for this experiment. The CLA-2 workspace, the ACT read path,
and the query path (with the -3 emission) are the only
permitted substrate.

C2. Combined cognition source lines for Pieces A and B:
at most 300. Exceeding this fails K-INQ2 (the mechanism is
then not the small generic process this experiment tests).

C3. Zero new hardcoded semantic cases, zero new modes, zero
new bridges, zero new task-specific handlers. Any found
fails K-INQ2.

C4. The K-ACT2 bar from the ACT prereg (commit `51a818141`,
section 5: the inquiry machinery must not be "a second
policy learner in disguise") applies to both Piece A and
Piece B, verified by source inspection.

C5. Determinism: the full Phase 1-4 battery plus controls
must be byte-identical across 3 runs (K-INQ3).

C6. Pure Zag for all research logic. Zero Python. The
contaminated paper stays untouched. Commits local with
explicit pathspecs. No sealed FW1-FW9 access (K-INQ4).

## 3. Experiment design (frozen)

Three fresh domains, all disjoint in relations and entities
from each other and from all prior builds. Structural fixture
requirements (exact strings are the builder's; these
properties are verifiable by inspection):

- D1 (Phases 1-2): one novel relation R1, 12 novel entities,
  8 taught facts, 24 unanswerable query keys (12 for Phase 1,
  12 disjoint keys for Phase 2).
- D2 (Phase 3): W6-class world, one novel relation R2, novel
  entities, designed per section 3.3.
- D3 (Phase 4): one novel relation R3, 8 novel entities,
  taught contradictory rule pairs producing conflict
  admissions on 16 query keys (8 for the experience window,
  8 disjoint keys for measurement).

### 3.1 Phase 1: uncertainty reification (Piece A)

Setup: CLA-2 workspace, ACT read path active (POLICY_ROOT
set, bid-aligned act_bin from commit `75a9b0e04`). Domain D1.
No acts available. The learner receives 12 queries on the 12
Phase-1 keys, each returning -2.

P-INQ1 (reification count): after the 12 admissions, exactly
12 UNCERTAINTY nodes exist in the workspace, each with
ref[0] = the queried key context node, each carrying a
complete learner-side creation trace per section 1.

Ablation A1: with the reification process disabled and only
that process (query path, ACT path, and all else intact),
the same 12 queries produce 0 UNCERTAINTY nodes. The
reification is load-bearing, not decorative.

### 3.2 Experience window W1 and Phase 2: guide construction (Piece B)

Experience window W1 (D1, not scored except for the sanity
gate below): 20 events. Both acts available. INQUIRE (30)
produces an OBSERVE that resolves the queried key (a
subsequent query on that key returns the answer, not -2).
DECOY (31) produces no observation. The learner may act
arbitrarily during W1. Sanity gate G-W1: after W1, the
workspace contains act-to-consequence associations readable
by the construction process (verifiable by inspection; a
gate, not a kill bar: if absent, Phase 2 cannot be scored
and the experiment reports BLOCKED, not FAILED).

Phase 2 setup: 12 fresh unanswerable keys in D1 (disjoint
from Phase 1 keys and from W1 keys). Each query returns -2.

P-INQ2 (construction): for each of the 12 live UNCERTAINTY
nodes, exactly one ACTION-GUIDE appears within K=10
subsequent events, with ref[0] = the uncertainty node
address and payload[0] = 30 (INQUIRE). No guide may select
31. No guide may appear for a non-live or non-existent
uncertainty node. Each guide carries a complete learner-side
creation trace.

Ablation A2: with the guide-construction process disabled
(ACT read path intact, the 12 UNCERTAINTY nodes present), no
ACTION-GUIDEs appear within 30 subsequent events, and ACT
emits 0 at inquiry opportunities. The construction is
load-bearing.

### 3.3 Phase 3: the B4 attribution test (end to end, D2)

Setup: fresh W6-class world D2. Pieces A and B active, ACT
read path active, POLICY_ROOT set. No researcher-supplied
guides anywhere. The world presents, per trial, two act
opportunities: one at the genuine inquiry position (tied to
a -2 admission event for a fresh key) and one at a decoy
position (no admission, unrelated context). Trial count:
12. The genuine/decoy position order follows a frozen
alternating sequence fixed in the fixture (positions
1..12 alternate genuine-first and decoy-first; the sequence
is frozen in the build report).

P-INQ3 (attribution): in at least 10 of the 12 trials, the
emitted inquiry act (CHOICE 30) occurs at the opportunity
following the -2 admission, not at the decoy position. (Under
the position-driven null, the expected count is 6; the exact
binomial tail for 10+ of 12 at p=0.5 is 79/4096 = 0.019,
below 0.05. The bar is the count: 10.)

P-INQ4 (functionality): after the Phase 3 inquiry acts, 20
follow-up queries on the previously -2 keys are issued; at
least 16 return answers (not -2). Inquiry is functional,
not performative.

P-INQ3b (no pre-play): let e_first_inq be the event index
of the learner's first emitted inquiry act (CHOICE 30) in
D2, and e_first_adm be the event index of its first -2
admission in D2. Required: e_first_inq > e_first_adm,
strictly. Any pre-play (inquiring before experiencing
uncertainty in the novel domain) fails Phase 3 outright.

### 3.4 Experience window W3 and Phase 4: novel-domain transfer (D3)

Uncertainty type for D3: conflicting evidence. Two ACTIVE
rules with contradictory predictions on the same query key
produce a -3 admission. The researcher specifies the domain,
the contradictory rule pairs, and the action interface. The
researcher does NOT specify any inquiry mapping for the
conflict type. The INQUIRE act in D3 produces an OBSERVE
carrying the correct resolution (which rule was right); the
DECOY act produces nothing.

Experience window W3 (D3, same design as W1): 20 events on
the 8 experience keys, both acts available, consequences
observable. Sanity gate G-W3 as in G-W1.

Phase 4 measurement: 8 fresh conflict keys (disjoint from
W3 keys). Each query returns -3.

P-INQ5 (transfer): all of the following hold on the novel
conflict type with zero researcher mapping:
(a) exactly 8 UNCERTAINTY nodes appear, each with ref[0] =
the conflicted key context and the conflict type marker,
each with a complete learner-side creation trace
(P-INQ1 applied to the new type);
(b) for each, one ACTION-GUIDE appears within 10 events,
anchored at the uncertainty node, selecting CHOICE 30
(P-INQ2 applied to the new type);
(c) 16 follow-up queries on the conflicted keys: at least
12 return the resolution answer (not -3), and the
contradicted rule is demoted (CONTRADICTS edge present,
verifiable by inspection).

### 3.5 Controls (frozen, run in D1/D2 fixtures)

C1 (scaffolding baseline): the current ACT build
configuration with researcher-supplied guides
(`mk_uncert`/`mk_guide` scaffolding), same D2 fixture.
Expected: passes the P-INQ3/P-INQ4 equivalents (it
already passes P-ACT2 per ACT-BUILD-COMPLETE). Purpose:
calibrates the world design. If the learner-driven
configuration fails where C1 passes, the failure is in
Pieces A/B, not the world.

C2 (null policy): POLICY_ROOT null, all else as in Phase 3.
Expected: constant 0 emitted, zero inquiry acts. Purpose:
verifies the world does not leak inquiry through other
channels.

C3 (random guides): guides with payload[0] drawn from a
frozen alternating 30/31 sequence (deterministic, not
random; the name is historical). Expected: the P-INQ3
count is below 10 (expected 6) and P-INQ4 below 16.
Purpose: verifies the checks are not vacuous.

## 4. Kill bars (frozen)

K-INQ1 (ordering): this prereg is committed alone before any
inquiry implementation begins. The implementation commit must
have this prereg commit as a strict ancestor, verified by
`git merge-base --is-ancestor`. Any implementation work
predating this commit fails K-INQ1.

K-INQ2 (no researcher-authored inquiry): zero
researcher-authored uncertainty-to-action mappings anywhere
in source, scaffolding, fixtures, or build scripts. Verified
by three independent checks, all of which must pass:
(i) source inspection of Pieces A and B: no branches on
domain, relation, task, uncertainty type, or uncertainty
content; no scoring rule; no enumerated probe or act space;
(ii) creation-trace audit: every UNCERTAINTY node and every
ACTION-GUIDE in Phases 1-4 carries a complete learner-side
trace per section 1; any node with scaffolding, fixture, or
core authorship fails the bar;
(iii) the e-ruling of section 1: the construction process
never receives the correct act through any channel except
world consequences in the experience windows.
Additionally: Pieces A and B combined add at most 300
cognition source lines; zero new semantic cases, modes,
bridges, or handlers.

K-INQ3 (determinism): the full battery (Phases 1-4 plus C1,
C2, C3) is byte-identical across 3 runs, exit 0.

K-INQ4 (governance): pure Zag for all research logic; zero
Python or other forbidden executables; the contaminated
paper `TNN_RESEARCH_PAPER_20260929.md` zero-diff; commits
local with explicit pathspecs; no sealed FW1-FW9 files
accessed at any step.

## 5. Falsification (frozen)

F-INQ1: any UNCERTAINTY node whose creation trace shows
scaffolding, fixture, or core authorship. Piece A is then
not learner-side.

F-INQ2: any ACTION-GUIDE whose uncertainty-to-action mapping
is traceable to researcher code or fixture content. Piece B
is then not learner-side.

F-INQ3: P-INQ3 count below 10 of 12 (the B4 swap test
fails; actions track position, not uncertainty).

F-INQ4: Phase 4 fails AND failure analysis shows the
construction process branching on uncertainty type. This is
the menu outcome: genuine learner-side inquiry within
trained types, researcher-bounded outside them (bounded L2,
not L3).

F-INQ5: K-ACT2 violation found by source inspection in
Piece A, Piece B, or their interaction: any task,
uncertainty, domain, or content branch in core or in the
learner-side processes.

Triggering any F-INQ falsifier yields INQUIRY-BUILD-FAIL for
the phase it falsifies; F-INQ1, F-INQ2, or F-INQ5 yield
INQUIRY-BUILD-FAIL for the experiment.

## 6. Verdict taxonomy (frozen)

INQUIRY-BUILD-PASS: all of P-INQ1, P-INQ2, P-INQ3, P-INQ3b,
P-INQ4, P-INQ5 hold at their frozen bars; both ablations A1
and A2 behave as specified; no F-INQ falsifier triggered;
K-INQ1 through K-INQ4 hold.

INQUIRY-BUILD-FAIL: any prediction below its bar, any
ablation misbehaving, any falsifier triggered, or any kill
bar failed. The build report must localize the failure to
the phase and piece using section 7.

BUILD-PASS/BUILD-FAIL only. No SURVIVES, L2/L3, or
transfer claim is made at build time; those require the
full eleven-stage promotion pipeline.

## 7. Failure localization (frozen)

- Phase 1 fail: the event loop cannot reify its own
  ignorance as workspace content. The -2 admission is a
  workspace dead end: an output with no structural
  consequence. This localizes the gap upstream of all
  inquiry, in the experience-to-structure path.
- Phase 2 fail with Phase 1 pass: uncertainty exists as
  content but no general process maps it to action. The
  failure analysis must distinguish "the process needs
  more experience" (fixable: widen W1) from "the process
  needs researcher cases per uncertainty type" (fatal to
  the learner-driven claim; triggers F-INQ4 logic).
- Phase 3 fail with Phase 2 pass: guides exist but do not
  track live uncertainty (stale anchoring, or position
  correlation winning the swap test). This is a B4 failure
  with the full mechanism in place: the attribution gap is
  about guide-maintenance dynamics, not missing machinery.
- Phase 4 fail with Phase 3 pass: the construction process
  is real but narrow. Bounded-L2 outcome (F-INQ4). Still
  valuable evidence about the generality boundary; still
  not L3.
- Pre-play (P-INQ3b) fail at any phase: the inquiry is
  scripted, not uncertainty-driven. This is the strongest
  negative: it indicates a researcher-supplied script
  survived into the implementation.

## 8. Dependencies and ordering (frozen)

- Requires: CLA-2 workspace (commit `e639904f2`), ACT read
  path with directional bid (commit `75a9b0e04`), ACT prereg
  conventions (commit `51a818141`).
- Independent of: COMP-1 plan construction (single-act
  inquiry needs no plans), MUL-1 (no arithmetic), DEVINT-CLA2
  (but DEVINT-CLA2 stage S8 is the natural integration
  target once Phases 1-3 pass standalone).
- Recommended order: Phases 1-3 standalone first; Phase 4
  after Phase 3 passes; DEVINT-CLA2 S8 integration after.
- Does not require sealed FW1-FW9. Uses fresh W6-class
  worlds designed for this experiment; W6 itself is sealed
  and must not be referenced or accessed.

## 9. One-System accounting (to be measured at implementation)

- Cognition source lines added: at most 300 for Pieces A+B
  combined (K-INQ2 bound).
- New hardcoded semantic cases: 0 (any found fails K-INQ2).
- New modes: 0. New bridges: 0. New task-specific
  handlers: 0.
- Learner-state structures created by the experiment:
  UNCERTAINTY nodes and inquiry ACTION-GUIDEs (workspace
  content, learner-owned). These are the structures whose
  authorship is under test.

## 10. Prereg metadata

- Frozen commit: this commit (to be recorded by the prereg
  author at commit time).
- Predecessor: inquiry scout `b4853a9f7`.
- Governing specs: ACT prereg `51a818141`, ACT build
  `f7d87938f`, ACT bid alignment `75a9b0e04`, CLA-2 build
  `e639904f2`, ISA boundary ruling `0525377f3`.
- Amendments: none at freeze. Any amendment requires a new
  frozen commit strictly before the implementation it
  governs; the original stays in history.
