# REPORT: MUTATION-HOOK

## Verdict

Analytical task, no implementation. The investigation is complete.
Headline findings, each labeled tested or reasoned below:

1. A learner-writable hook table on the mutation path is mechanically
   implementable in pure Zag TODAY with no protected-core change:
   Zag has first-class function values, indirect calls work, and
   function values round-trip through byte memory as i64 (TESTED,
   T1/T2).
2. That only solves dispatch, not invention. A fn-value hook table
   lets the learner SELECT a researcher-written body, which is menu
   selection and explicitly does not count toward the strong sense
   (L3 treadmill rule). The strong sense needs the hook target to be
   a learner-constructed executable graph, which needs EXECUTE plus
   the 4-op ISA in the protected core (REASONED, A2.2/A2.3).
3. Of the six capabilities, the easiest is A2.6 (mutation-event
   observability) and the hardest is A2.2 (learner-created operation
   bodies). A2.2 is also the only one that requires a protected-core
   change, and it is gated on Micah's still-pending EXECUTE placement
   ruling (REASONED).
4. There is an incremental path: Phases 0 and 1 (event stream,
   allocator, inert hook dispatch) need no governance approval and
   make no invention claims; Phases 2+ (EXECUTE, strong-sense hook,
   shadow validation, missing-mechanism attribution) are gated
   (REASONED).

## 1. Task

EPOCH-STRONG froze six missing capabilities (A2.1-A2.6) blocking
learner-created stamping. This lane investigates one of them in
depth: learner-writable mutation hooks. Current state: the mutation
path is researcher-owned (`fact_add`/`fact_set_obj` in base); the
learner cannot intercept it. Goal: what would it take for the
learner to install a hook on the mutation path, which of the six is
easiest/hardest, whether there is an incremental path, and an honest
flag if protected-core changes are required.

Method: source audit of the frozen es_* lane sources (EPOCH-STRONG),
toolchain micro-probes compiled and run under safebin with the
pinned znc, and reasoned decomposition. Nothing was implemented;
no experiment was run.

## 2. TESTED findings

T1: Zag supports first-class function values and indirect calls.
Probe: `fn(i32)i32` typed locals, assignment of a named function,
passing as an argument, indirect invocation. Compiled with the
pinned znc under `PATH=$HOME/safebin`; program exited 42
(41+1 through the indirect call). Pure Zag, no other tooling.

T2: Function values round-trip through byte memory. Probe: store a
fn value as i64 bits with byte-wise writes (the codebase's own
little-endian idiom), reload with byte-wise reads, cast back to
`fn(i32)i32`, indirect-call. Two distinct functions stored at
offsets 0 and 8 both dispatched correctly (exit 0). Implication: a
hook slot can live in an ordinary S or L state cell; no language
extension is needed for a learner-writable hook table.

T3: The mutation path has exactly two entry points and the learner
calls neither. `grep` over the frozen es_* sources: `fact_add` is
called 21 times, all in es_world.zag (world setup); `fact_set_obj`
is called 2 times, both in es_main.zag (stage code, ES-C and ES-E);
`grep -c "fact_add\|fact_set_obj" es_learn.zag` is 0 (matches the
ES-B6 bar). The learner is not on the mutation path at all.

T4: Neither mutation function consults any hook slot. Read of
es_base.zag: `fact_add` writes the fact triple and bumps nf;
`fact_set_obj` writes the object field. No indirection, no event
counter, no notification. The mutation happens and nothing else
observes it.

T5: The learner's write vocabulary already reaches every S cell
mechanically. `ss(S,i,v)` is a plain function in es_module.zag,
used 19 times in es_learn.zag. The learner could `ss(S,932,v)`
today; the barrier is conventional (fixed researcher-defined
slots), not mechanical. A hook slot the learner writes needs no
new write primitive.

T6: Failure attribution can only blame existing structures. Read of
es_learn.zag `note_answer_disagree`: on a joint-answer disagreement
it calls `u_invalidate` on each spec-routing family that
contributed (judgment=1: the routing was sound; consequence=0: the
answer was wrong). The attribution vocabulary is the existing
contract set. There is no residual bucket, no "no existing
mechanism explains this" path. A2.4 is confirmed absent in source,
not just in behavior.

T7: No executable-graph construction exists in any lane. `grep` for
`EXECUTE(`/`fn EXECUTE` over all lane .zag sources: zero hits.
`grep` for "executable-graph" over all REPORT.md: only
epoch_strong/REPORT.md (the recommendation text). The TNN-2
post-freeze mechanism EPOCH-STRONG cited as prerequisite has not
landed anywhere checkable from this lane.

T8: The existing "hook" is not a learner-writable table. The
`hook=1` field in SUMMARY-EPOCHSTRONG is the compose
plan-invalidation check (es_learn.zag: on a plan-table hit,
re-validate cached fams, zero the stale slot, stash telemetry at
L+13276..13296). It is a hardcoded researcher-written code path,
not a table the learner writes. No confusion is warranted: this
lane's hook question is about the mutation path, and no such
table exists.

## 3. REASONED: the six capabilities decomposed

Notation: [CORE?] = does it require changing the protected ISA
(the frozen computational basis: ALLOC, READ, WRITE, LINK, COPY,
COMPARE/EQ, ADD-class arithmetic, BRANCH, APPLY/EXECUTE, generic
state/register ops). Lane-level base changes (fact store, world
interface, S/L layout in a new lane) are not core changes.

A2.1 Learner-allocated persistent state with learner-chosen
semantics. What it takes: a bump allocator over a carved region
(cursor in a fixed cell, region base fixed), callable from learner
code, plus a registry table the learner writes (cell, meaning
record, evidence). The learner already calls `z_alloc` for scratch
(compose allocates per-call buffers); what is missing is
persistence across calls and a semantics registry. Mechanics are
easy; the philosophical hard part is the registry's meaning
vocabulary being learner-chosen rather than researcher-enumerated,
but a learner-writable association table is the honest substrate
for that. [CORE? No. Lane-level base change.] Difficulty: easy.

A2.2 Learner-created operation bodies from the generic ISA. What it
takes: runtime construction of executable graphs plus a way to run
them. The sanctioned design is the pending proposal: EXECUTE(root,
frame) as a protected-core primitive over a 4-op ISA (MOVE,
BRANCHEQ, INC, DEC). The T1/T2 finding does NOT substitute: a
fn-value table only lets the learner pick among
researcher-compiled bodies, which is menu selection and fails the
L3 bar by name. There is no middle path for the strong sense: a
"bump counter on mutation" body must be constructed, not selected.
[CORE? YES. EXECUTE is a protected-core primitive and its placement
is still awaiting Micah's ruling from 2026-09-30.] Difficulty:
hardest. It is also load-bearing: the strong-sense forms of A2.3
and A2.5 depend on it, and A2.4's proposals are toothless without
a construction back end.

A2.3 Mutation-path interception (learner-writable hook table). What
it takes, mechanically: `fact_add`/`fact_set_obj` read a hook slot
(e.g. S+932; S is 16384 bytes, cells 930/931 used, free cells
abound), and on nonzero reload the fn value (T2 pattern) and
indirect-call it with (S, A, s, r, o) before/after the mutation.
The learner installs by writing the fn bits (T5: it can already
write any S cell). This is buildable now with no core change, BUT
its honest scope is dispatch infrastructure only: with fn values
the installable bodies are researcher-written, so the strong sense
("on mutation" behavior the learner created) needs A2.2 first. A
researcher-enumerated hook-body menu must not be presented as
progress toward invention. [CORE? No for the table and consult;
the strong-sense use is gated on A2.2's YES.] Difficulty:
easy-medium as infrastructure, hard as the strong sense (inherits
A2.2).

A2.4 Failure attribution to a MISSING mechanism. What it takes: a
residual path alongside `note_answer_disagree` (T6). The
unexplained-staleness signature is precise and already observable:
version-says-fresh AND checksum-says-stale AND answers disagree.
The missing piece is a latch: "no inventory detector predicts this
residual; posit a missing mechanism with this signature attached,"
handed to a hypothesis proposer. The deep difficulty is the
proposer: without researcher-enumerating "mutation tracker" as the
answer, proposing needs a general gap-to-structure mapping, which
is the invention engine itself, and its proposals need A2.2's
construction back end to be actionable. The detection half
(residual latching) could be prototyped early; the proposing half
is where generality lives or dies. [CORE? No. Learner-code change.]
Difficulty: hard, second hardest.

A2.5 Probationary validation of invented mechanisms. What it takes:
shadow mode for the hook table (a mode flag: shadow vs live). In
shadow, the candidate body runs but writes predictions to scratch
instead of gating behavior; a generic promotion rule (predictive
accuracy over N events, domain-neutral) promotes it to live. The
researcher-enumeration risk here is low: promote-on-predictive-
accuracy is generic machinery, not a semantic case. [CORE? No.]
Difficulty: medium. Gated on A2.2 in practice: there is nothing
honest to shadow-test until the learner can construct candidate
bodies. (Shadow-testing researcher-provided candidates would be
menu selection again.)

A2.6 Mutation-event observability. What it takes: the learner must
see mutation events. Cleanest base change: `fact_add` and
`fact_set_obj` bump a mutation-event counter cell (and optionally
append to a small ring buffer) that the learner reads. With A2.3's
table the hook consult itself can be the event source, so A2.6 is
subsumed by A2.3's implementation; standalone it is a few lines in
base. Alternative with zero base change: route experiment
mutations through a learner entry point (learner-as-mutator), but
that only covers experiment-driven mutations, not world setup.
[CORE? No.] Difficulty: easiest.

## 4. Difficulty ranking (easiest to hardest)

1. A2.6 mutation-event observability. Base change, a few lines, no
   invention claim. Subsumed by A2.3 when the table lands.
2. A2.1 learner-allocated persistent state. Bump allocator plus
   registry table; lane-level base change. Mechanics easy; the
   semantics-registry discipline is the part to keep honest.
3. A2.3 hook dispatch infrastructure. fn-value slot consult in the
   two mutation functions; verified inert by regression bars.
   Strong-sense use inherits A2.2's difficulty.
4. A2.5 probationary validation. Shadow mode plus a generic
   promotion rule; medium mechanics, but nothing honest to test
   until A2.2 exists.
5. A2.4 failure attribution to a missing mechanism. Learner code,
   no core change, but the general gap-to-structure proposer is the
   invention engine itself. Second hardest.
6. A2.2 learner-created operation bodies. Hardest. Requires the
   protected-core EXECUTE primitive plus 4-op ISA, pending Micah's
   ruling, and is the load-bearing prerequisite for the strong-sense
   forms of A2.3, A2.4, A2.5.

## 5. Incremental path

Phase 0 (no governance, pure infrastructure, no invention claims).
A2.6: mutation-event counter cell bumped by `fact_add` and
`fact_set_obj`. A2.1: bump allocator over a carved L region plus a
learner-writable registry table. Prereg-ready bars: counter
advances exactly once per mutation event and the learner reads it;
allocate/write/read-back across calls is stable; all pre-existing
regression outputs byte-identical with the new machinery unused.
Nothing here claims learning; it is substrate.

Phase 1 (no governance, inert dispatch). A2.3's table: hook slot
consult added to both mutation functions, slot default 0 meaning
no hook. Bars: byte-identical regression with slot 0; a unit probe
installs a researcher-written body via fn bits (T2 pattern) and
observes it fire exactly once per mutation; uninstall returns to
byte-identical. The probe body is labeled researcher-written in
the report; no invention claimed.

Phase 2 (governance). Micah rules on EXECUTE placement. A2.2
lands: 4-op ISA graphs constructible and runnable by the learner
from the generic ISA. This is the step this lane must not take
unilaterally.

Phase 3 (consumes Phase 2). A2.3 strong sense: hook slot points at
learner-constructed graphs. A2.5: shadow mode and generic
promotion. A2.4: residual latch plus proposer feeding A2.2's
constructor.

Phase 4. EPOCH-STRONG-2: the ES-B experience with (a)-(f) present;
bars discriminate learner-created vs researcher-placed by source
audit plus the ES-E neutral-mutation signature.

Dependencies: A2.6 and A2.1 are independent and buildable now.
A2.3's infrastructure form is independent; its strong-sense form
needs A2.2. A2.5 needs A2.2. A2.4's detection half is independent;
its proposing half needs A2.2. A2.2 needs governance.

## 6. Governance flags for Micah (decisions, not taken here)

G1. A2.2 requires a protected-core change: EXECUTE(root, frame) as
a primitive plus the 4-op ISA (MOVE, BRANCHEQ, INC, DEC). His
2026-09-30 EXECUTE placement ruling is still pending. This lane
flags it and does not implement it. No strong-sense hook work can
proceed honestly without this ruling.

G2. Boundary read, stated for correction: the mutation interface
(`fact_add`/`fact_set_obj`) is world-interface base code, not the
protected ISA, so Phases 0 and 1 are lane-level changes needing no
core approval. If he considers the world interface frozen,
Phases 0 and 1 need his approval too.

G3. Honest labeling guard: the fn-value hook table (T1/T2) must
never be reported as invention progress. Learner selection among
researcher-written bodies is menu selection under the L3 bar.
Phase 1's value is dispatch infrastructure and regression proof,
nothing more.

G4. Recommendation: approve Phases 0 and 1 as infrastructure when a
worker is available (no invention claims, preregistered bars,
pure Zag, safebin); keep Phases 2+ gated on G1. Do not authorize a
"learner installs a hook" demonstration until A2.2 exists: any
such demo built now would be menu selection wearing a hook's
clothing.

Seventh-gap note (from EPOCH-STRONG, not a new claim): even with
A2.1-A2.6, the learner has no cost-deliberation machinery to prefer
a cheap O(1) counter over the O(nf) checksum. Motivation pressure
is a further gap, not part of this lane's six.

## 7. What was NOT done (honesty section)

- Nothing was implemented. There are no mh_*.zag sources, no build
  script, no runs. The lane contains this REPORT.md and
  NAMECHECK.md only.
- No prereg was written because no experiment was run; the task's
  prereg requirement is conditional on building.
- The T1/T2 probes were thrown away in /tmp after confirming the
  results; they are toolchain checks, not lane artifacts.
- Difficulty rankings and the incremental path are reasoned, not
  tested. The tested parts are exactly T1-T8 in section 2.
- Whether A2.1-A2.6 jointly suffice for genuine invention is still
  untested, as EPOCH-STRONG already stated.

## 8. Artifacts

- `NAMECHECK.md`: toolchain guard Step 0, scope, commit discipline.
- `REPORT.md`: this file.
- No compiled artifacts. No commits yet; files are uncommitted in
  the lane directory.
