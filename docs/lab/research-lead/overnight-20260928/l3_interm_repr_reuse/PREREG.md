# PREREG: L3 Intermediate Novel Representation (L3-INR)

Status: PREREG-FROZEN 2026-10-02, before any implementation exists.
This document is never edited after freezing. Any change requires a new
prereg. Commit-order self-check: the freeze commit contains ONLY PREREG.md
and NAMECHECK.md. No learner source, no world source, no binary, no run log
exists under l3_interm_repr_reuse/ at freeze time.

Worker: L3-INR design worker (subagent, 2026-10-02). Design only; no
implementation in this task. A follow-up worker implements under this frozen
prereg.

## 1. Objective

Test whether a TNN learner, given a frozen MAP inventory that is provably
insufficient for a relational task, invents a novel intermediate
representation at runtime that satisfies Micah's L3 bar (12 criteria plus
Criterion 0 A through D), and later reuses that same representation on a
different task.

The invented thing here is a representation, not a procedure. L3-NIV2
(W2 failed, W3/W4 passed with CALR) demonstrated procedure invention:
multi-step instruction sequences constructed over a 5-op ISA and reused on
the same function under a changed surface encoding. L3-INR targets the
other L3 branch: representational invention. The learner must recruit a
new representational level, a directed relational graph sitting between raw
pair observations and outcomes, where no such level exists in source or in
the MAP inventory. It must then reuse that graph across tasks with
different output forms and different query semantics (pairwise prediction
versus total ranking), which exercises adaptive cross-task reuse rather
than exact reuse. Micah's current top priority is L2 adaptive reuse and the
standing question is whether mechanisms collapse into one general
operation; a representation that serves two different tasks without
rebuilding is direct evidence on that question.

## 2. Relation to the killed C281/C284 claim and the L3-REDTEAM attacks

Source: docs/lab/research-lead/overnight-20260928/l3_redteam/REPORT.md
(2026-10-02). Seven attacks SUCCEEDED against the procedure-invention claim
(C281/C284); three FAILED. Each successful attack is enumerated here with
the exact design feature that defeats or sidesteps it in this
representation-invention design. If any defeat below is judged insufficient
by the follow-up red team, that is a K10 finding and the claim dies.

1. A1 ORACLE-SELECTION (SUCCEEDED): C281 promoted a composition iff
r==target; the expected answer did all the rejecting. DEFEAT: the same
two-process information firewall as L3-NIV2 (section 3). The learner
process never receives expected values. Its only supervision is the
world's ACCEPT/REJECT consequence channel. Edge-set promotion, retention,
revision, commit, and defer decisions are functions of consequences only.
Audit arm A-INFO verifies by protocol log and source inspection that no
expected value crosses into the learner process. The sealed evaluator (a
separate process) holds expected values and returns only per-arm
PASS/FAIL, accept counts, TEST counts, and digests to the implementation
worker.

2. A2 TRANSFER-SEAL as worker-anticipation (SUCCEEDED as characterization):
the C284 transfer world's new answer was hand-derived in advance by the
same worker that built the machinery. DEFEAT: the sealed worlds S1, S2,
S3, S1p are designed by an INDEPENDENT ADVERSARY WORKER, a different
subagent instance than the implementer, AFTER the learner code freeze,
under the frozen generation constraints G1 through G8 (section 5). This
prereg constrains only the generation procedure, never the instances, and
hand-derives no order, no entity set, no pair, and no edge set. The design
worker and the implementation worker never see sealed contents; the
evaluator mediates and returns digests only.

3. V1 OP-REMOVAL (SUCCEEDED): the C281 "invention" was one greedy step over
a 5-op menu. DEFEAT: there is no operator menu here at all. The committed
structure is an edge set drawn from a space of 2^90 possible directed edge
sets over 10 entities. No menu is widened or narrowed by this experiment
(zero new opcodes, section 9). The compression kill bar (section 7,
|E| <= N) is what defeats the "pairwise MAP menu" characterization: no
inventory of pairwise MAPs satisfies it, and controls C0 and C1 confirm
the failure empirically.

4. V2 TWO-STEP-RULE (SUCCEEDED): strictly-positive-gain greedy trapped at
a local optimum. DEFEAT: scoring is over COMPLETE candidate edge sets via
world consequences, and the construction loop must retain zero- or
negative-immediate-gain edge additions whenever bounded lookahead shows
eventual full training acceptance. Transitive edges have zero immediate
gain until the path they complete closes; a per-step positive-gain rule
cannot build them. No per-step positive-gain requirement may appear in the
learner's promotion rule. Control C3 (GREEDY-EDGE, the exact greedy
constructor) must FAIL S1 training, proving the trap is real and the
treatment escapes it.

5. V3 AMBIGUOUS-LABELS (SUCCEEDED): under genuine ambiguity the learner
confidently built the WRONG intermediate, selected by the researcher's
op-order tie-break. DEFEAT: arm T5 (section 5). The learner may commit only
when exactly one edge set survives consequence testing plus
self-constructed discriminating probes; otherwise it must DEFER. S3a
(resolvable) requires goal-directed resolution through pair TESTs the
learner chooses itself; S3b (unresolvable within probe domain and budget)
requires DEFER. A confident wrong commit FAILS the arm. No
researcher-authored tie-break may decide a commit.

6. V4 OPNUM-SWAP (SUCCEEDED): the kill bar demanded byte p0==4, coupled to
the researcher's arbitrary op numbering. DEFEAT: every kill bar in section
7 is defined over world consequences and structural trace properties
(event types, parent pointers, edge counts, shared-edge lineage), never
over program bytes, edge encodings, or entity identifiers. Entity naming
is adversary-chosen and invisible to the verdict.

7. V5 FACT-ORDER (SUCCEEDED): distractor-first ordering tested nothing
because the expected answer selected regardless. DEFEAT: with
consequence-driven selection, distractor attributes are genuinely probed
and REJECTed by the world; the world consequence, not an answer key, does
the discriminating. The adversary designs surface attributes with near
zero rank correlation (G2), so attribute chasing fails on consequences.
Order-independence is spot-checked (audit A-ORDER).

Preserved from the FAILED attacks, still required here: A3 (no
install-without-probe path reachable on TREAT arms; audit A-TRACE), A4 at
byte level (no sealed-solution literals in learner source; audit A-LIT),
V6 (order-independence robustness; audit A-ORDER).

## 3. World protocol (frozen)

Two processes: LEARNER (learner plus driver) and WORLD (world plus sealed
evaluator). They communicate over a narrow message protocol. This is a test
harness boundary, not a cognitive subsystem: it adds no mode, bridge, or
handler to the learner.

Messages LEARNER to WORLD: OBSERVE (request training instances),
TEST-PAIR(a, b, y) presenting a pair and a predicted outcome y,
TEST-RANK(r) presenting a full ranking r, COMMIT(slot, graph-id) declaring
a persisted intermediate graph, DEFER declaring principled abstention.
Probe usage is accounted inside TEST-PAIR.
Messages WORLD to LEARNER: INSTANCE data during OBSERVE; ACCEPT or REJECT
for each TEST. REJECT carries no expected value, no distance measure, no
hint. Regime changes are NOT announced; the learner must detect them from
its own consequence stream.

The sealed evaluator inside WORLD holds the hidden orders and expected
values, scores held-out instances, and reports per arm only: PASS/FAIL,
accept counts, TEST counts, and sha256 digests. It never reveals
instances, orders, or expected values to the implementation worker. The
implementation worker never inspects sealed-world contents except via this
authorized evaluator.

Determinism: all runs seeded, seed recorded in the log, 3 of 3
byte-identical run logs per arm, sha256 digests recorded in the report.

## 4. Learner construction (frozen constraints, not a solution)

The implementation worker builds the learner under these frozen
constraints. They describe the construction procedure; they do not describe
or enumerate any solution. In particular this prereg names no entity, no
order, no pair, and no edge set.

(a) Basis: frozen generic machinery already present in the learner: a
named-slot state store, LINK edge storage, neighbor lookup, and iterated
expansion over stored edges (the generic reachability evaluator). ZERO new
opcodes, ZERO new semantic cases, ZERO new modes, bridges, handlers, or
routers. The code-freeze commit records the exact basis and the frozen MAP
inventory; any basis change requires a new prereg.

(b) The intermediate representation is a directed edge set E over the
learner's internal entity ids, held in a named persistent slot. Edge-set
size is variable; no architectural cap below a stated resource bound of
200 edges. The bound is a resource bound, never binding on the battery
(required solutions use at most 10 edges), not a form enumeration. No
enumerated edge-set family may appear in source or prereg.

(c) Construction is a propose-and-test loop over COMPLETE candidate edge
sets. Scoring is the training ACCEPT count obtained through the
consequence channel. The promotion rule must not require strictly positive
per-edge gain (anti-V2). Among candidates with equal full training
acceptance, fewer edges are preferred (a stated simplicity tie-break,
disclosed in section 10; it names no topology). The loop's revision
operators are ADD-EDGE and DEL-EDGE: the L2 adaptive-reuse operator set
(extend, truncate, specialize, substitute) applied to structure rather than
programs. There is no separate invention engine: the same operators serve
construction, revision, and re-derivation. One mechanism, not a new mode.

(d) The generic evaluator answers pair queries by reachability over
whatever edge set occupies the slot. It is written once, operates over any
slot contents, and contains no dominance, order, or ranking literals
(covered by A-LIT). The invented representation is the edge set; the
evaluator is generic machinery. This is the C0-A split: runtime-defined
semantics live in learner-created persistent state; source holds only
generic machinery.

(e) DEFINE: the learner may persist a named edge set (an abstraction) it
built during construction. A commit writes the edge set to a named
persistent slot with a lineage id and the full creation trace.

(f) Commit rule: the learner commits an edge set only when it is the SOLE
survivor of consequence testing on all training pairs plus active
disambiguation (section 6). A commit writes the program to a named
persistent slot with a lineage id and the full creation trace.

(g) Frozen budgets: B_CONSTRUCT = 3000 TESTs (T1); B_RANK = 300 TESTs
(T3); B_REVISE = 2000 TESTs (T4); B_PROBE = 150 TESTs (T5); B_SURFACE = 50
TESTs (T3b confirmation). Pair outcomes are binary, so per-output brute
force is cheap; brute force is defeated instead by the compression kill
bar (|E| <= N, section 7) together with the trace audit that held-out
pairs were never probed (G7, K5). The ranking output domain is 10
factorial (about 3.6M), so ranking brute force is infeasible inside any
budget.

## 5. Battery arms (frozen)

### Sealed worlds (designed post-code-freeze by the independent adversary)

Adversary generation constraints (frozen; the adversary instantiates, the
prereg never names an instance):

- G1 (S1, base relational world): (a) 10 entities, adversary-named; one
hidden strict total order. (b) 18 training pairs (about 40 percent of the
45 pairs), 6 held-out pairs. (c) Held-out includes at least 3 pairs
requiring at least 2-hop transitive inference and at least 1 pair
requiring 3-hop inference under the true order; the adversary exhibits the
hop counts in the sealed key. (d) An edge set of at most 9 edges achieving
full training acceptance exists; the adversary exhibits it in the key.
(e) The exact C2 greedy-attribute constructor and the exact C3
greedy-edge constructor fail S1 training; the adversary exhibits both
failures in the key.
- G2 (MAP insufficiency and distractor attributes): (a) no MAP in the
frozen inventory computes the S1 rule; the adversary attests and control
C0 confirms by failing. (b) Each entity carries surface attributes
designed by the adversary with |Spearman rank correlation| < 0.2 against
the hidden order; the adversary exhibits the correlations in the key.
(c) Held-out pairs lie outside the training pair set, so verbatim pair
memorization cannot cover them; control C1 confirms.
- G3 (S2, revision world): the order is permuted after the T1 commit; the
S1 reference edge set scores at most 2 of 6 on S2 held-out; an
edit-lineage revision (ADD-EDGE/DEL-EDGE with |E intersect Eprime| >=
|E|/2) reaching full training acceptance exists within B_REVISE; the
adversary exhibits it in the key. 6 held-out pairs.
- G4 (S3, ambiguity world): exactly two total orders are consistent with
all training pairs. S3a is resolvable: some learner-chosen pair TEST
sequence within B_PROBE discriminates the two orders. S3b is
unresolvable: no TEST sequence within the probe domain and B_PROBE
discriminates them; the two orders differ only outside the probe domain.
The adversary documents resolvability in the key.
- G5 (S1p, surface-recode world): the same hidden order as S1; entity
labels unchanged; surface attribute values recoded by the adversary
(|Spearman| < 0.2 retained, exhibited in the key). 6 fresh held-out pairs.
An attribute-bound approach fails; an id-anchored edge set transfers with
zero reconstruction.
- G6: no world is a trivial variant of FW1-FW9 or C281/C284 instances
(adversary attests in the key).
- G7 (brute-force accounting): the battery does not rely on output-domain
size to defeat pair-outcome brute force; the compression bar (|E| <= 10)
and the no-probe trace audit (section 7, K5) carry that load, and this is
disclosed as a design decision rather than hidden.
- G8 (firewall): the adversary worker is a different subagent instance
than the implementation worker and the red-team worker; it designs S1,
S2, S3, S1p AFTER the learner code-freeze commit, holds the sealed key,
runs the evaluator, and releases to the implementation worker only
per-arm PASS/FAIL, accept counts, TEST counts, and digests.

### TREAT arms (full learner)

- T1 INVENT: OBSERVE S1 training pairs, construct within B_CONSTRUCT,
COMMIT slot G, then 6 held-out pairs. PASS: at least 5 of 6 held-out
ACCEPT, AND |E| <= 10, AND the trace shows at least 4 of the 6 held-out
pairs received zero TEST-PAIR events during construction.
- T2 REUSE-SAME: 6 adversary-supplied unseen pairs from S1; the persisted
G is applied with NO reconstruction. PASS: at least 5 of 6, and the trace
shows zero CONSTRUCT events for slot G after the T1 commit.
- T3 REUSE-DIFFERENT-TASK: Task B ranking over the S1 entities. The
learner builds a ranking procedure over slot G from generic machinery
(referencing the slot only, no entity or order literals) within B_RANK,
then TEST-RANK. PASS: exact order match on all 10 positions, AND the
trace shows the ranking procedure read slot G, AND control C5 fails as
specified.
- T3b SURFACE-TRANSFER: S1p world (recoded attributes, same order). The
learner applies G with at most B_SURFACE confirmation TESTs and NO
reconstruction. Then 6 held-out pairs. PASS: at least 5 of 6 with zero
CONSTRUCT events for a new slot.
- T4 REVISE: the world switches to S2 unannounced. The learner must
detect the change from its consequence stream, REVISE with ADD-EDGE and
DEL-EDGE carrying lineage to G, re-COMMIT as Gprime, then 6 held-out.
PASS: at least 5 of 6 within B_REVISE, with valid edit lineage
(|E intersect Eprime| >= |E|/2). A fresh from-scratch build, even if it
solves S2, FAILS this arm's lineage requirement.
- T5a AMBIG-RESOLVABLE (S3a): the learner must probe within B_PROBE,
isolate the sole surviving edge set, and COMMIT the world-consistent one.
PASS: commits the correct edge set and scores at least 5 of 6 on 6
follow-up pairs.
- T5b AMBIG-UNRESOLVABLE (S3b): PASS only if the learner emits DEFER (no
commit) within B_PROBE. Any confident commit of a wrong edge set is FAIL.

### Control arms

- C0 NO-INVENT: construction, DEFINE, and revision disabled; full frozen
MAP inventory available; same budgets. Must FAIL T1 (below 5 of 6
held-out; expected at most 3 of 6). Proves the existing MAPs are
insufficient for the task family.
- C1 MEMORIZE: may spend its budget TESTing pairs, then stores accepted
pairs and answers held-out by 1-nearest-neighbor in pair space. Must FAIL
(below 5 of 6).
- C2 GREEDY-ATTR: greedy single-attribute threshold constructor (best
immediate ACCEPT gain per round, first-max tie-break), scoring by
training ACCEPT count. Must FAIL S1 training (never reaches full
acceptance). The attribute-shortcut mechanism as a control.
- C3 GREEDY-EDGE: adds the single edge with maximum immediate ACCEPT gain
each round and requires strictly positive gain per round (the V2-style
greedy constructor over structure). Must FAIL S1 training (never reaches
full acceptance). Proves transitive edges are unreachable to greedy
construction.
- C4 SCRATCH-RANK: slot G cleared and inaccessible; the control may build
a fresh edge set AND a ranking procedure for Task B within 600 TESTs
(2x B_RANK). Efficiency baseline for KC0D; no pass/fail of its own except
as used in KC0D.
- C5 NAIVE-REUSE: T1's committed edge set applied to Task B with NO
ranking procedure (pairwise reachability answers only, or the raw edge
list presented as the ranking). Must FAIL Task B. Proves T3 required
genuine query re-derivation over the representation, not byte reuse.

### Audit arms (follow-up red-team worker; source and trace inspection)

- A-INFO: the learner process receives no expected values (protocol log
plus source inspection of the channel). A1-style.
- A-TRACE: every COMMITTED edge has a CONSTRUCT or TEST lineage event in
the trace; no install-without-probe path is reachable on TREAT arms.
A3-style.
- A-LIT: the hidden orders and the sealed reference edge sets appear
nowhere in learner source, including the generic evaluator (the auditor
holds the key). A4-style.
- A-ORDER: training-pair order permutation spot check reproduces the T1
verdict. V6-style.

## 6. Ambiguity protocol (frozen)

The learner maintains a hypothesis set: all candidate edge sets fully
accepted on training pairs. While more than one candidate survives and
probe budget remains, the learner must generate discriminating pairs
itself (active inquiry): pick a pair on which survivors disagree,
TEST-PAIR each survivor's prediction, keep only ACCEPTed survivors. Commit
requires exactly one survivor. If the budget exhausts with more than one
survivor, the learner must emit DEFER. Any researcher-authored tie-break
deciding a commit is forbidden; a commit trace showing tie-break selection
is a K10 finding (the red team kills the claim).

Internal verification, learner-owned evaluation: every promotion,
retention, revision, commit, and defer decision in sections 4 through 6 is
driven by the ACCEPT/REJECT consequence stream produced AFTER the
learner's own commitments (its TESTs and COMMITs). The harness's expected
answers exist only inside the sealed evaluator for final scoring; they
never enter the learner's decision path.

## 7. Kill bars (frozen; ANY single FAIL kills the L3 claim)

Mapped to Micah's 12 procedure-invention criteria, here applied to
representational invention:

- K1 (criterion 1: final structure not in source, not enumerated as one
complete candidate): A-LIT passes; this prereg hand-derives no order, no
entity set, no pair, and no edge set (true by construction: none appear
above). FAIL on any sealed-order literal or sealed reference edge set in
learner source, or any complete edge set enumerated in source or prereg.
- K2 (criterion 2: created after experience): the T1 trace shows the first
OBSERVE/TEST-PAIR strictly before the slot's first CONSTRUCT event. FAIL
otherwise.
- K3 (criterion 3: persistent learner state): T2 passes with zero
CONSTRUCT events for slot G after the T1 commit (persistence, not
rebuild).
- K4 (criterion 4: white-box creation trace): A-TRACE passes; every
propose, TEST, REVISE, DEFINE, and COMMIT event is logged with monotonic
sequence numbers and parent pointers, sufficient to replay the creation.
- K5 (criterion 5: hidden instances solved): T1 at least 5 of 6 with
|E| <= 10 and at least 4 of 6 held-out pairs never probed; T3 exact order
match; T3b at least 5 of 6; T4 at least 5 of 6; T5a commits the correct
edge set; T5b DEFERS.
- K6 (criterion 6: ablation destroys the advantage): C0 fails T1 (the
construction advantage destroyed); C4 comparison under KC0D (the
representation advantage destroyed: without slot G, Task B costs at least
twice the TESTs or fails).
- K7 (criterion 7: reused later): T2 passes.
- K8 (criterion 8: transfers across changed surface representation): T3b
passes (attribute recoding does not disturb the id-anchored
representation) AND C5 fails (naive byte reuse does not solve the new
task, so T3's transfer required genuine query re-derivation). This
operationalizes criterion 8 as representation transfer across a surface
recode plus task transfer with re-derived queries; the difference from
L3-NIV2's surface-encoding transfer is stated here, not hidden.
- K9 (criterion 9: beats memorization and search controls): C0, C1, C2,
and C3 all fail as specified.
- K10 (criterion 10: survives independent red team): a follow-up red-team
worker (a different instance than the implementer and the adversary) runs
the L3-REDTEAM attack classes adapted to this design (menu-pinning
attempt against the edge-set space, consequence-channel leak audit,
greedy-trap check, ambiguity commit check, byte-bar check, order check)
and reports REDTEAM-SURVIVES. Any successful break of a K1 through K9 or
KC0 bar is a K10 FAIL.
- K11 (criterion 11: revisable after a counterexample): T4 passes WITH
valid edit lineage (section 5). A solve without lineage fails K11 even at
6 of 6.
- K12 (the 7/12 rule): the verdict L3-INR-SURVIVES requires K1 through
K11 ALL green. Any red is L3-KILLED with reclassification by evidence
(L2+ or L2). 7 of 12 is not "basically L3"; partial credit does not exist.

Mapped to Criterion 0:

- KC0A (runtime-defined semantics in learner-created persistent state;
source holds only generic machinery): source audit finds no branch, case,
or literal keyed to dominance, order, rank, or any sealed-world property;
the only task-facing semantics are the generic slot store, LINK edge
storage, neighbor lookup, iterated expansion, and the consequence
channel; this prereg names no order or entity set concretely (the
adversary does, post-freeze). A pre-written semantic case is KC0A FAIL and
kills the claim outright.
- KC0B (open structural form; final topology emerges incrementally, never
chosen from a finite researcher-enumerated family): G1e holds; the
construction enumerates no edge-set family; edge sets are variable-size
under a non-binding 200-edge resource cap; the final topology is assembled
incrementally by the propose/test/revise loop over a 2^90 space. If the
red team shows the committed topologies collapse to a small
researcher-anticipatable set, KC0B fails and the claim dies.
- KC0C (multiple unforeseen forms; sealed post-freeze worlds; at least one
evaluation family designed by an independent adversary): S1, S2, S3, and
S1p are sealed; all four are designed by the independent adversary
post-code-freeze under G1 through G8; the design, implementation, and
red-team workers are pairwise distinct instances, blind except through
the evaluator (digests only).
- KC0D (cognitive reuse improving transfer, prediction, procedure
learning, causal inference, memory, planning, or sample efficiency): the
T3 trace shows the ranking procedure reading slot G, AND the T3 TEST
count is at most half the C4 TEST count (sample-efficiency gain
attributable to the invented intermediate), AND T3b passes (the same
representation transfers across the surface recode with zero
reconstruction).

## 8. Verdict and VOID

L3-INR-SURVIVES iff K1 through K12 and KC0A through KC0D all PASS, with
the red team reporting REDTEAM-SURVIVES under K10. Any other outcome is
L3-KILLED. Bars are frozen: moving a bar after results invalidates the
verdict. The verdict names the exact frozen bars that governed it.

VOID (terminal; correction proceeds only as a fresh prereg, never
amend-and-promote): any implementation source, binary, or run log dated
before this freeze commit; any expected value reaching the learner
process; any edit to this prereg after freezing; the adversary, the
implementer, and the red-team worker not being three distinct instances;
any sealed-content inspection outside the authorized evaluator.

## 9. Architecture accounting (0-new-machinery budget)

- New protected-core ops: 0.
- New modes, bridges, handlers, routers, semantic opcodes: 0.
- New finite operator menu entries: 0. There is no operator menu in this
design; nothing is widened.
- New learner-state kinds: 1. A named edge-set slot with a lineage id.
This is learner-created persistent structure, explicitly not machinery:
it is the accumulated experience the architecture exists to hold,
consistent with the ONE-SYSTEM RULE (capability from new learned state,
not new subsystems).
- New harness code: the WORLD/evaluator is test harness, not learner
cognition; it holds hidden orders the learner never sees.
- ADD-EDGE and DEL-EDGE are persistent-state edits over learner state,
executed through existing machinery (the slot store). The generic
reachability evaluator is frozen generic machinery recorded at code
freeze. Cognition lines added, and any hardcoded semantic cases, are
recorded by the implementation worker at code freeze; any hardcoded
semantic case is KC0A FAIL.
- One-system check: construction, revision, transfer re-derivation, and
ambiguity handling all run through the single propose/test/revise loop of
section 4. No INVENT_MODE, REVISION_MODE, RANK_MODE, or per-task handlers.

## 10. Known boundaries (honest)

- Whether an incrementally built relational edge set counts as L3
representational invention, as opposed to strong L2 structural learning
(constructing relationships from generic mechanisms), is exactly what K1
through K12 adjudicate. This prereg asserts nothing in advance and
downgrades nothing by fiat; the bars decide.
- The simplicity tie-break (fewer edges preferred at equal acceptance,
section 4c) is a stated researcher-chosen selection pressure, disclosed
here. It names no topology: chains, stars, and other sparse forms all
satisfy it. If the red team shows this pressure is what does the
inventing (for example the learner cannot build the transitive form
without it and the form is then researcher-determined), that is a K10
finding.
- KC0B is claimed over the open edge-set space, not over primitives. The
generic graph machinery (slot store, LINK, neighbor lookup, iterated
expansion) is fixed, researcher-supplied generic machinery, permitted by
the protected-core ISA ruling as a small frozen domain-neutral
computational basis comparable to a CPU ISA.
- The "independent adversary" is a follow-up worker under a procedural
firewall (G8), not an external party. Independence is procedural and is
documented here as a limitation, not as equivalence to external review.
- N = 10 entities and 6 held-out pairs per arm make this a mechanism
demonstration, not a generality proof. FW1-FW9-style overclaiming is
disallowed: a pass establishes the mechanism under these bars, not broad
generality.
- If the battery proves infeasible within the frozen budgets, the honest
outcome is BUILD-FAIL, not a prereg amendment. If the L2 adaptive-reuse
operator set has not landed a stable ADD-EDGE/DEL-EDGE by code freeze,
the implementation worker records that at freeze (BUILD-FAIL if the
operators are unavailable) rather than inventing parallel machinery.
- The design deliberately reuses the L2 adaptive-reuse operator vocabulary
(extend, truncate, specialize, substitute) as the construction engine,
because Micah's current top priority is L2 adaptive reuse and the
composition ruling asks whether mechanisms collapse into one general
operation. If that reuse turns out to be cosmetic, K6/KC0D will show it.

## 11. Sequencing (frozen)

1. This prereg frozen and committed (design worker). No implementation
exists at freeze time.
2. The implementation worker builds LEARNER and WORLD under this prereg
and makes a code-freeze commit recording the basis machinery, the frozen
MAP inventory, the budget accounting, and the seed scheme. It has seen no
sealed content.
3. The adversary worker (a different instance) designs S1, S2, S3, S1p
post-code-freeze under G1 through G8, holds the sealed key, and runs the
evaluator.
4. The implementation worker receives only per-arm PASS/FAIL, accept
counts, TEST counts, and digests.
5. The independent red-team worker (a different instance again) runs the
K10 attack classes; REDTEAM-SURVIVES is required.
6. The verdict is computed from the frozen bars; the report names the
exact bars that governed it.

Commit-order self-check for this freeze: the freeze commit contains
PREREG.md and NAMECHECK.md ONLY, added with explicit pathspecs. No .zag,
no binary, no log exists under l3_interm_repr_reuse/ at freeze time.
