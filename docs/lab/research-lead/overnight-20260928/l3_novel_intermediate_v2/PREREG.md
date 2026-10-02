# PREREG: L3 Novel Intermediate v2 (L3-NIV2)

Status: PREREG-FROZEN 2026-10-02, before any implementation exists.
This document is never edited after freezing. Any change requires a new
prereg. Commit-order self-check: the freeze commit contains ONLY PREREG.md
and NAMECHECK.md. No learner source, no world source, no binary, no run log
exists under l3_novel_intermediate_v2/ at freeze time.

Worker: L3-NIV2 design worker (subagent, 2026-10-02). Design only; no
implementation in this task. A follow-up worker implements under this frozen
prereg.

## 1. Objective

Test whether a TNN learner can create a novel intermediate procedure at
runtime that satisfies Micah's L3 procedure-invention bar (12 criteria plus
Criterion 0 A through D), where the previous claim on this line (C281/C284)
was KILLED by L3-REDTEAM (7 attacks succeeded, verdict L3-REDTEAM-COMPLETE,
reclassified L2+).

The experiment must demonstrate, in one continuing learner: construction of
a multi-step intermediate program M from a frozen generic ISA, with no final
form present in source and none hand-derived in this prereg; selection of M
by world consequences rather than expected answers; persistence of M in
learner state; reuse of M on new instances; revision of M after a
counterexample and world change; transfer of the underlying procedure across
a changed surface representation; goal-directed handling of genuine
ambiguity; and survival of an independent red team running the same attack
classes that killed C281/C284.

## 2. Why the last claim died, and how this design defeats each attack

Source: docs/lab/research-lead/overnight-20260928/l3_redteam/REPORT.md
(2026-10-02). Seven attacks SUCCEEDED, three FAILED. Each successful attack
is enumerated here with the exact design feature that defeats or sidesteps
it. If any defeat below is judged insufficient by the follow-up red team,
that is a K10 finding and the claim dies.

1. A1 ORACLE-SELECTION (SUCCEEDED): C281 promoted a composition iff
r==target; the expected answer did all the rejecting, so "discrimination"
was answer-key matching. DEFEAT: a two-process information firewall
(section 3). The learner process never receives expected values. Its only
supervision is the world's ACCEPT/REJECT consequence channel. Promotion,
retention, revision, and commit decisions are functions of consequences
only. Audit arm A-INFO verifies by protocol-log and source inspection that
no expected value crosses into the learner process. The sealed evaluator
(a separate process) holds expected values and returns only per-arm
PASS/FAIL, accept counts, TEST counts, and digests to the implementation
worker.

2. A2 TRANSFER-SEAL as worker-anticipation (SUCCEEDED as characterization):
the C284 transfer world's new answer was hand-derived in advance by the
same worker that built the machinery; "sealed" held against copying but
not against anticipation. DEFEAT: the sealed families S1 through S4 are
designed by an INDEPENDENT ADVERSARY WORKER, a different subagent instance
than the implementer, AFTER the learner code freeze, under the frozen
generation constraints G1 through G8 (section 5). This prereg constrains
only the generation procedure, never the instances, and hand-derives no
solution. The design worker and the implementation worker never see family
contents; the evaluator mediates and returns digests only.

3. V1 OP-REMOVAL (SUCCEEDED): the "invention" was one greedy step over a
5-op menu; with INC unsearchable the verdict fell back to L2. This is menu
selection, which Micah's taxonomy explicitly excludes from L3. DEFEAT:
open-form multi-step construction (section 4). The battery REQUIRES minimal
solutions of length at least 3 (G1a: exhaustive length-2 enumeration
provably fails). The old mechanism is preserved as control arm C2 and must
FAIL S1 while TREAT passes.

4. V2 TWO-STEP-RULE (SUCCEEDED): strictly-positive-gain greedy trapped at a
local optimum under a minimal validity-rule change; the two-step program
was unreachable. DEFEAT: scoring is over COMPLETE candidate programs via
world consequences, and the construction loop must retain zero- or
negative-immediate-gain extensions whenever bounded lookahead shows
eventual full acceptance. No per-step positive-gain requirement may appear
in the learner's promotion rule. G1b requires the adversary to seal only
families on which the exact C281 greedy constructor (control C2) fails.

5. V3 AMBIGUOUS-LABELS (SUCCEEDED): under genuine ambiguity the learner
confidently built the WRONG intermediate, selected by the researcher's
op-order tie-break rather than the goal. DEFEAT: a hypothesis-set protocol
with active disambiguation (section 6). The learner may commit only when
exactly one candidate survives consequence testing plus self-constructed
discriminating probes; otherwise it must DEFER. S4a (resolvable) requires
goal-directed resolution through probes the learner constructs itself;
S4b (unresolvable within probe domain and budget) requires DEFER. A
confident wrong commit FAILS the arm. No researcher-authored tie-break may
decide a commit.

6. V4 OPNUM-SWAP (SUCCEEDED): the kill bar demanded byte p0==4, coupled to
the researcher's arbitrary op numbering rather than to what the learner
achieved. DEFEAT: every kill bar in section 7 is defined over world
consequences and structural trace properties (event types, parent
pointers, lineage), never over program bytes, op numbers, or instruction
encodings. Op numbering is an implementation detail invisible to the
verdict.

7. V5 FACT-ORDER (SUCCEEDED): the distractor-first ordering tested nothing,
because the expected answer selected regardless of order. DEFEAT: with
consequence-driven selection, distractor candidates are genuinely executed
and REJECTed by the world; the world consequence, not an answer key, does
the discriminating. Order-independence is additionally spot-checked
(audit A-ORDER).

Preserved from the FAILED attacks, still required here: A3 (no
install-without-construct path reachable on TREAT arms; audit A-TRACE),
A4 at byte level (no sealed-solution literals in learner source; audit
A-LIT), V6 (order-independence robustness; audit A-ORDER).

## 3. World protocol (frozen)

Two processes: LEARNER (learner plus driver) and WORLD (world plus sealed
evaluator). They communicate over a narrow message protocol. This is a test
harness boundary, not a cognitive subsystem: it adds no mode, bridge, or
handler to the learner.

Messages LEARNER to WORLD: OBSERVE (request training instances), TEST(x, y)
presenting an input x and a candidate output y, COMMIT(slot, program-id)
declaring a persisted intermediate. Probe usage is accounted inside TEST.
Messages WORLD to LEARNER: INSTANCE(x) during OBSERVE; ACCEPT or REJECT for
each TEST. REJECT carries no expected value, no distance measure, no hint.
Regime changes are NOT announced; the learner must detect them from its own
consequence stream.

The sealed evaluator inside WORLD holds the hidden rules and expected
values, scores held-out instances, and reports per arm only: PASS/FAIL,
accept counts, TEST counts, and sha256 digests. It never reveals
instances, rules, or expected values to the implementation worker. The
implementation worker never inspects sealed-world contents except via this
authorized evaluator.

Determinism: all runs seeded, seed recorded in the log, 3 of 3
byte-identical run logs per arm, sha256 digests recorded in the report.

## 4. Learner construction (frozen constraints, not a solution)

The implementation worker builds the learner under these frozen
constraints. They describe the construction procedure; they do not describe
or enumerate any solution.

(a) Basis: the frozen generic ISA already present in the learner. ZERO new
opcodes, ZERO new semantic cases, ZERO new modes, bridges, handlers, or
routers. The code-freeze commit records the exact basis; any basis change
requires a new prereg.

(b) Programs are variable-length instruction sequences. No architectural
length limit below a stated resource cap of 64 instructions. The cap is a
resource bound, never binding on the battery (required solutions are
length 3 to 6), not a form enumeration. No enumerated candidate family may
appear in source or prereg.

(c) Construction is a propose-and-test loop over COMPLETE candidate
programs. Scoring is the training ACCEPT count obtained through the
consequence channel. The promotion rule must not require strictly positive
per-step gain (anti-V2). The loop's revision operators are APPEND,
TRUNCATE, SUBSTITUTE: the L2 adaptive-reuse operator set (extend,
truncate, specialize, substitute). There is no separate invention engine:
the same operators serve construction, revision, and transfer
re-derivation. Architecture compression is the point: one mechanism, not a
new mode.

(d) DEFINE: the learner may persist a named sub-program (an abstraction) it
built during construction, and invoke it by name in later programs through
the existing APPLY/EXECUTE path. DEFINE is a persistent-state write of
learner-created structure (budgeted in section 9 as 0 new protected-core
ops), not new machinery.

(e) Commit rule: the learner commits a program only when it is the SOLE
survivor of consequence testing on all training instances plus active
disambiguation (section 6). A commit writes the program to a named
persistent slot with a lineage id and the full creation trace.

(f) Frozen budgets: B_CONSTRUCT = 50,000 TESTs (S1); B_PROBE = 200 TESTs
(S4 disambiguation); B_REVISE = 20,000 TESTs (S2); B_TRANSFER = 30,000
TESTs (S3); the from-scratch S3 control (C5) is allowed 50,000 TESTs. The
output domain of each regime has at least 2^16 distinct values, so direct
output brute force cannot fit inside the budgets (adversary constraint G6).

## 5. Battery arms (frozen)

### Sealed families (designed post-code-freeze by the independent adversary)

Adversary generation constraints (frozen; the adversary instantiates, the
prereg never names an instance):

- G1 (S1, base novel rule): (a) exhaustive enumeration of all programs of
length at most 2 over the frozen basis fails to fully accept S1 training;
the adversary exhibits this failure in the sealed key. (b) The exact C281
greedy constructor (control C2) fails S1 training. (c) A solution of
length 3 to 6 exists; the adversary exhibits it in the key. (d) 6 training
instances, 6 held-out instances.
- G2 (control plausibility): no existing MAP computes the S1 rule
(adversary attests; control C0 confirms by failing); held-out inputs lie
outside training neighborhoods so nearest-neighbor over accepted training
pairs fails (control C1 confirms).
- G3 (S2, revision): the rule changes after the T1 commit; the S1
reference solution scores at most 2 of 6 on S2 held-out; an edit-based
revision (APPEND/TRUNCATE/SUBSTITUTE lineage sharing at least half the
instructions, or reusing at least one defined abstraction) reaches full
training acceptance; 6 held-out instances.
- G4 (S3, transfer): the same underlying function as S1 under a changed
surface encoding (field positions and/or value encoding changed); the
adversary's S1 reference solution bytes score at most 2 of 6 on S3;
re-derivation reusing S1 abstractions is feasible within B_TRANSFER; 6
held-out instances.
- G5 (S4, ambiguity): S4a has exactly two programs consistent with all
training instances, discriminable by some input inside the probe domain,
with the hidden rule agreeing with exactly one on that input. S4b has at
least two programs consistent with all training instances AND with every
TEST the probe domain and B_PROBE budget allow; they differ only outside
the probe domain. The adversary documents resolvability in the key.
- G6: output domain at least 2^16 distinct values per regime.
- G7: no family is a trivial variant of FW1-FW9 or C281/C284 instances
(adversary attests in the key).
- G8 (firewall): the adversary worker is a different subagent instance
than the implementation worker; it designs S1 through S4 AFTER the learner
code-freeze commit, holds the sealed key, runs the evaluator, and releases
to the implementation worker only per-arm PASS/FAIL, accept counts, TEST
counts, and digests.

### TREAT arms (full learner)

- T1 BASE: OBSERVE S1 training, construct within B_CONSTRUCT, COMMIT, then
6 held-out instances. PASS: at least 5 of 6 held-out ACCEPT.
- T2 REUSE: adversary-supplied unseen instances of the S1 family; the
persisted M is applied with NO reconstruction. PASS: at least 5 of 6, and
the trace shows zero CONSTRUCT events for the reused slot.
- T3 REVISE: the world switches to S2 unannounced. The learner must detect
the change from its consequence stream, REVISE with edit operators
carrying lineage to M, re-COMMIT as M prime, then 6 held-out. PASS: at
least 5 of 6 within B_REVISE, with valid edit lineage (parent pointers;
at least half the instructions shared in order, or at least one defined
abstraction reused). A fresh from-scratch build, even if it solves S2,
FAILS this arm's lineage requirement.
- T4 TRANSFER: the world switches to the S3 surface encoding. The learner
re-derives within B_TRANSFER, reusing at least one S1-defined abstraction
(trace evidence required). PASS: at least 5 of 6.
- T5a AMBIG-RESOLVABLE (S4a): the learner must probe within B_PROBE,
isolate the sole survivor, and COMMIT the world-consistent program. PASS:
commits the correct program and scores at least 5 of 6 on 6 follow-up
instances.
- T5b AMBIG-UNRESOLVABLE (S4b): PASS only if the learner emits DEFER (no
commit) within B_PROBE. Any confident commit of a wrong program is FAIL.

### Control arms

- C0 NO-INVENT: construction, DEFINE, and revision disabled; full MAP
inventory available; same budgets. Must FAIL S1 (below 5 of 6 held-out;
expected at most 2 of 6). Proves existing MAPs insufficient for the task
family.
- C1 MEMORIZE: may spend its budget finding ACCEPTed (x, y) training
pairs, then answers held-out by 1-nearest-neighbor in input space. Must
FAIL (below 5 of 6).
- C2 GREEDY: the exact C281 m_construct algorithm (single-instruction
appends, strictly positive gain per round, first-max tie-break), scoring
by training ACCEPT count. Must FAIL S1 training (never reaches full
acceptance). This is the killed mechanism as a control.
- C3 BYTECOPY: T1's committed program bytes applied to S3 held-out. Must
FAIL (at most 2 of 6). Proves the surface change defeats byte copying, so
T4 must genuinely re-derive.
- C4 ENUM2: exhaustive enumeration of all programs of length at most 2
over the basis, on S1 training. Must FAIL (no full acceptance). The
bounded-search control.
- C5 SCRATCH-S3: abstraction table cleared, construction enabled, 50,000
TESTs on S3. Efficiency baseline for KC0D and K6b; no pass/fail of its
own.

### Audit arms (follow-up red-team worker; source and trace inspection)

- A-INFO: the learner process receives no expected values (protocol log
plus source inspection of the channel). A1-style.
- A-TRACE: every COMMITTED program has a CONSTRUCT event chain in the
trace; no install-without-search path is reachable on TREAT arms. A3-style.
- A-LIT: the sealed reference solutions appear nowhere in learner source
(the auditor holds the key). A4-style.
- A-ORDER: training-instance order permutation spot check reproduces the
T1 verdict. V6-style.

## 6. Ambiguity protocol (frozen)

The learner maintains a hypothesis set: all candidate programs fully
accepted on training. While more than one candidate survives and probe
budget remains, the learner must generate discriminating inputs itself
(active inquiry): pick an x on which survivors disagree, TEST each
survivor's output on x, keep only ACCEPTed survivors. Commit requires
exactly one survivor. If the budget exhausts with more than one survivor,
the learner must emit DEFER. Any researcher-authored tie-break deciding a
commit is forbidden; a commit trace showing tie-break selection is a K10
finding (the red team kills the claim).

Internal verification, learner-owned evaluation: every promotion,
retention, revision, commit, and defer decision in sections 4 through 6 is
driven by the ACCEPT/REJECT consequence stream produced AFTER the learner's
own commitments (its TESTs and COMMITs). The harness's expected answers
exist only inside the sealed evaluator for final scoring; they never enter
the learner's decision path. This is the learner commitment to later world
consequence to learner-owned evaluation chain, and it is what replaces the
expected-answer supervision that A1 exposed.

## 7. Kill bars (frozen; ANY single FAIL kills the L3 claim)

Mapped to Micah's 12 procedure-invention criteria:

- K1 (criterion 1: final structure not in source, not enumerated as one
complete candidate): A-LIT passes; this prereg hand-derives no solution
(true by construction: no program bytes, shapes, or rule instances appear
above). FAIL on any sealed-solution literal in learner source or any
complete candidate enumerated in source or prereg.
- K2 (criterion 2: created after experience): the T1 trace shows the first
OBSERVE/TEST strictly before the slot's first CONSTRUCT event. FAIL
otherwise.
- K3 (criterion 3: persistent learner state): T2 passes with zero
CONSTRUCT events for the reused slot (persistence, not rebuild).
- K4 (criterion 4: white-box creation trace): A-TRACE passes; every
propose, TEST, REVISE, DEFINE, and COMMIT event is logged with monotonic
sequence numbers and parent pointers, sufficient to replay the creation.
- K5 (criterion 5: hidden instances solved): T1, T3, T4 at least 5 of 6;
T5a commits the correct program; T5b DEFERS.
- K6 (criterion 6: ablation destroys the advantage): C0 fails S1 (the
construction advantage destroyed); C5 uses at least twice the TESTs of T4
or fails S3 within 50,000 TESTs (the abstraction advantage destroyed).
- K7 (criterion 7: reused later): T2 passes.
- K8 (criterion 8: transfers across changed surface representation): T4
passes and C3 fails.
- K9 (criterion 9: beats memorization and search controls): C0, C1, C2,
and C4 all fail as specified.
- K10 (criterion 10: survives independent red team): a follow-up red-team
worker (a different instance than the implementer) runs the L3-REDTEAM
attack classes adapted to this design (menu-pinning attempt,
consequence-channel leak audit, greedy-trap check, ambiguity commit
check, byte-bar check, order check) and reports REDTEAM-SURVIVES. Any
successful break of a K1 through K9 or KC0 bar is a K10 FAIL.
- K11 (criterion 11: revisable after a counterexample): T3 passes WITH
valid edit lineage (section 5). A solve without lineage fails K11 even at
6 of 6.
- K12 (the 7/12 rule): the verdict L3-NIV2-SURVIVES requires K1 through
K11 ALL green. Any red is L3-KILLED with reclassification by evidence
(L2+ or L2). 7 of 12 is not "basically L3"; partial credit does not exist.

Mapped to Criterion 0:

- KC0A (runtime-defined semantics in learner-created persistent state;
source holds only generic machinery): source audit finds no branch, case,
or literal keyed to any sealed-family property; the only task-facing
semantics are the generic ISA and the consequence channel; this prereg
names no rule family concretely (the adversary does, post-freeze). A
pre-written semantic case is KC0A FAIL and kills the claim outright.
- KC0B (open structural form; final topology emerges incrementally, never
chosen from a finite researcher-enumerated family): G1a and G1b hold; the
construction enumerates no candidate family; programs are variable-length
under a non-binding 64-instruction resource cap; the final topology is
assembled incrementally by the propose/test/revise loop.
- KC0C (multiple unforeseen forms; sealed post-freeze worlds; at least one
evaluation family designed by an independent adversary): S1 through S4 are
sealed; all four are designed by the independent adversary post-code-freeze
under G1 through G8; the design and implementation workers are blind
(evaluator-mediated digests only).
- KC0D (cognitive reuse improving transfer, prediction, procedure learning,
causal inference, memory, planning, or sample efficiency): the T4 trace
references at least one S1-defined abstraction inside the S3 solution AND
the T4 TEST count is at most half the C5 TEST count (sample-efficiency
gain attributable to the invented intermediate).

## 8. Verdict and VOID

L3-NIV2-SURVIVES iff K1 through K12 and KC0A through KC0D all PASS, with
the red team reporting REDTEAM-SURVIVES under K10. Any other outcome is
L3-KILLED. Bars are frozen: moving a bar after results invalidates the
verdict. The verdict names the exact frozen bars that governed it.

VOID (terminal; correction proceeds only as a fresh prereg, never
amend-and-promote): any implementation source, binary, or run log dated
before this freeze commit; any expected value reaching the learner
process; any edit to this prereg after freezing; the adversary and the
implementer being the same worker instance; any sealed-content inspection
outside the authorized evaluator.

## 9. Architecture accounting (0-new-machinery budget)

- New protected-core ops: 0.
- New modes, bridges, handlers, routers, semantic opcodes: 0.
- New finite operator menu entries: 0. The basis is frozen as-is and
recorded at code freeze.
- New learner-state kinds: 1. A named program slot with a lineage id. This
is learner-created persistent structure, explicitly not machinery: it is
the accumulated experience the architecture exists to hold, consistent
with the ONE-SYSTEM RULE (capability from new learned state, not new
subsystems).
- New harness code: the WORLD/evaluator is test harness, not learner
cognition; it holds expected values the learner never sees.
- DEFINE and REVISE are persistent-state writes and structural edits over
learner state, executed through existing machinery (the EXECUTE path and
the state store). Cognition lines added, and any hardcoded semantic cases,
are recorded by the implementation worker at code freeze; any hardcoded
semantic case is KC0A FAIL.
- One-system check: construction, revision, transfer re-derivation, and
ambiguity handling all run through the single propose/test/revise loop of
section 4. No COMPOSE_MODE, INVENT_MODE, REVISION_MODE, or per-regime
handlers.

## 10. Known boundaries (honest)

- C0-B is claimed over unbounded composition, not over primitives. The ISA
basis is fixed, researcher-supplied generic machinery, permitted by the
protected-core ISA ruling as a small frozen domain-neutral computational
basis. If the red team shows the constructed forms collapse to a small
researcher-anticipatable set, KC0B fails and the claim dies. The prereg
does not fake open form: the 64-instruction cap is stated as a resource
bound, and the battery's required solutions sit far below it.
- Whether consequence-driven multi-step construction with runtime-defined
abstractions counts as L3 representational invention, as opposed to strong
L2 structural learning, is exactly what K1 through K12 adjudicate. This
prereg asserts nothing in advance and downgrades nothing by fiat; the bars
decide.
- The "independent adversary" is a follow-up worker under a procedural
firewall (G8), not an external party. Independence is procedural and is
documented here as a limitation, not as equivalence to external review.
- N = 6 held-out instances per regime makes this a mechanism
demonstration, not a generality proof. FW1-FW9-style overclaiming is
disallowed: a pass establishes the mechanism under these bars, not broad
generality.
- If the battery proves infeasible within the frozen budgets, the honest
outcome is BUILD-FAIL, not a prereg amendment. If the L2 adaptive-reuse
operator set has not landed a stable APPEND/TRUNCATE/SUBSTITUTE by code
freeze, the implementation worker records that at freeze (BUILD-FAIL if
the operators are unavailable) rather than inventing parallel machinery.
- The design deliberately reuses the L2 adaptive-reuse operator vocabulary
(extend, truncate, specialize, substitute) as the construction engine,
because Micah's current top priority is L2 adaptive reuse and the
composition ruling asks whether mechanisms collapse into one general
operation. If that reuse turns out to be cosmetic, K6b/KC0D will show it.

## 11. Sequencing (frozen)

1. This prereg frozen and committed (design worker). No implementation
exists at freeze time.
2. The implementation worker builds LEARNER and WORLD under this prereg
and makes a code-freeze commit recording the basis ISA, the budget
accounting, and the seed scheme. It has seen no sealed content.
3. The adversary worker (a different instance) designs S1 through S4
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
no binary, no log exists under l3_novel_intermediate_v2/ at freeze time.
