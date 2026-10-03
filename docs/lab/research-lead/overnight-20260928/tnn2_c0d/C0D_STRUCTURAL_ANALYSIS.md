# TNN-2 C0-D Structural Failure Analysis

Date: 2026-09-30 (PDT). Target: `tnn2.zag` @ `f4de7ff46` (frozen, read-only).
Method: read-only source audit; exact call-site enumeration by grep; enclosing
function attribution for every test-line reader. No source edits. No em dashes
used in this document per loop style rule.

Verdict: **C0D-STRUCTURAL-ANALYSIS-COMPLETE**.

## Claim under test

The interaction analyst (commit `9009ff259`) found: "promoted graphs are never
executed at query time (answers come from memoized facts; MAPs are read only
by revision and tests), so even genuine construction couldn't convert to
reuse. C0-D fails structurally."

Micah's C0-D requires: "cognitive reuse, the invented structure must improve
transfer, prediction, procedure learning, causal inference, memory, planning,
or sample efficiency, existence alone is insufficient."

This analysis verifies the structural claim from source, traces the exact
mechanism, judges whether the failure is wiring or architecture, states what
execution would and would not buy, relates the finding to the transfer
analyst's behavioral probes, and sketches the minimal wiring that would make
C0-D structurally possible. All line numbers refer to `tnn2.zag` @ `f4de7ff46`.

## 0. Verified call graph (production cognition only)

| Function | Line | Production callers |
|---|---|---|
| `activate` | 140 | `ev_query` (813), `ev_observe` (836) |
| `execute` | 192 | `t2_exec` (416) only |
| `exec_val` | 215 | tests only (`t_c6` 973, `t_c7` 980) |
| `t2_exec` | 412 | `t2_try_verify` (500), `t2_revise_graph` (732), test (`t_t2_revise` 1289) |
| `promote_graph` | 533 | `t2_trial` only (605, 628, 644, 659) |
| `t2_trial` | 586 | `mp_run` (668) only |
| `ev_teach_in` | 310 | `promote_graph` (541), `t2_revise_graph` (748), `bootstrap_miss` (783), `ev_observe` (852, 856) |
| `revise_on_contradict` | 685 | `ev_observe` (845) only |
| `ev_query` | 813 | driver, tests |
| `ev_act` | 859 | driver and tests only; called by no cognition function |

Readers of tag-20 (MAP) nodes, exhaustive by grep for `,0)==20`:

- Line 690, inside `revise_on_contradict`: scans all MAPs for a DEP edge to
  the contradicted fact. Production.
- Line 1281, inside test `t_t2_revise`: locates a MAP by relation. Test only.

Readers of a MAP's field20 (the graph root), exhaustive:

- Line 707, inside `t2_revise_graph`: `let root:i32=ng(W,m,20)`, then
  re-executes at line 732 via `t2_exec`. Production, revision only.
- Line 1285, inside test `t_t2_revise`. Test only.

No other code in the file reads a MAP node or a stored graph root.

## 1. Why promoted graphs are never executed at query time

The failure is not an accident of one missed call site. It is a two-step
structural guarantee: promotion shadows itself with a memoized fact, and the
query path cannot see MAPs.

**Step A: promotion teaches a shadowing fact.** `promote_graph` (533) writes
the MAP node (tag 20, field20 = graph root, field28 = answer, field4 = r,
field8 = s, plus DEP provenance edges), and then at line 541 calls
`ev_teach_in(W,s,r,ans)`. `ev_teach_in` (310) allocates a fresh tag-1 fact
node holding (s, r, ans). Every successful promotion therefore ends by
inserting an exact-match fact for the same (s, r) it just built a graph for.

**Step B: the query path answers from facts and cannot see MAPs.**
`ev_query` (813) runs:

1. `activate(W,s,r)` (140), which scans nodes with `ng(W,n,36)==1`
   (live) and `ng(W,n,0)==1` (tag 1, fact). MAP nodes carry tag 20, so the
   filter excludes them structurally. On a hit it returns the memoized
   `ng(W,n,28)` immediately.
2. Only on a miss: `mp_run` (668) -> `t2_trial` (586) -> per-candidate
   `t2_try_verify` (497) -> `t2_exec` (412) -> `execute` (192). This is
   verification-time execution inside the trial loop, not query-time reuse.
   On success, `promote_graph` runs Step A, and the answer returns.
3. Then `bootstrap_miss` (763), then `miss_inquire` (795).

Because Step A always runs on promotion, the *next* query on the same (s, r)
takes branch 1 (exact hit) and never reaches branch 2. The promoted graph is
executed exactly twice in its lifetime: once at verification inside
`t2_trial`, and at most again at re-verification inside `t2_revise_graph`
(732) if a contradiction ever arrives on one of its licensing facts. It is
never executed to answer a query.

**Where the query path goes instead:** to the memoized fact store. Answers
come from `activate` over tag-1 facts. MAPs are derivation certificates that
the query path cannot read: the only production reader is
`revise_on_contradict` (690), and the only production executor of a stored
graph root is revision re-verification (707, 732).

**A second, independent layer: the graphs are value traces, not portable
procedures.** `t2_asm_chain` (363) builds guards and SETREG cells around
`t2_lit` (338) nodes holding the literal values gathered for the original
subject (`t2_gather`, 442, collects value paths, not relation traversals).
The traversed relation is recorded only in DEP provenance edges for
revision; it appears nowhere in the executable cells. The frozen 4-op ISA
(MOVE, BRANCHEQ, INC, DEC) has no relational-dereference operation:
`res_op` reads frame slots (operand >= 1000) or a fixed node id's field20
(operand >= 0, node id fixed at assembly). A cell cannot compute "the fact
(s, r)" at runtime. So even a query path that executed MAPs could not reuse
a chain graph on a new subject: the first guard compares the frame against
the original subject's literals and fails closed. The transfer probe P2
confirms empirically: executing subject 1's graph root on subject 7 returns
-999999.

## 2. What would have to change for a promoted graph to execute on a later query

This is a wiring sketch for TNN-3 root-cause work, not a patch: the frozen
build must not be modified. The changes are localized to two functions plus
a shadowing policy.

**Change 1: give `ev_query` a MAP branch.** In `ev_query` (813), add a
lookup before (or in place of) the `activate` exact-hit branch: scan live
tag-20 MAP nodes for field8 == s and field4 == r; on a hit, run
`t2_exec(W, ng(W,m,20), s)` and return the result when it is not -999999,
falling through to the existing path on execution failure. The MAP branch
must precede `activate`, because of Change 2.

**Change 2: stop the self-shadowing teach.** `promote_graph` line 541,
`ev_teach_in(W,s,r,ans)`, must be removed or replaced. As long as promotion
teaches an exact-match fact, an `activate`-first ordering makes any MAP
branch dead code, and a MAP-first ordering makes the taught fact dead
weight. The minimal consistent choice: promotion teaches no answer fact;
the MAP is the promoted artifact and the fact store keeps only observed or
taught facts.

**Change 3: a shadowing and liveness policy.** Legacy and mixed states need
a rule for when both a MAP and a fact exist for (s, r): e.g., a live,
executable MAP wins; on execution failure (-999999) fall back to the fact.
MAP liveness must respect supersession and eviction the way facts do
(`is_superseded`, `decay`), or procedures will outlive the regime they were
built for.

**Change 4: retarget the contradiction path.** `ev_observe` currently
contradicts an answer *fact* and `revise_on_contradict` finds MAPs through
DEP edges to that fact. If answers come from live graph execution, the
contradicted object should be the MAP itself; the DEP scan in
`revise_on_contradict` (688-700) already enumerates MAPs by licensing fact,
so the wiring mostly exists, but the fact-contradiction bookkeeping in
`t2_revise_graph` (742-751) would need to not fight the MAP branch.

Note on determinism: executing MAPs at query time allocates frames and
touches the allocator on every query, so the freeze's 3/3 byte-identical
property would need re-verification under the new path. This is a test
obligation, not a blocker.

## 3. Wiring omission or deep architectural issue

Both, at different levels. The omission is localizable; the reason it
happened is architectural.

**The localizable omission.** Nothing in the frozen ISA or node layout
prevents a MAP branch in `ev_query`. The MAP layout already stores the
graph root in field20; `t2_exec` already executes a root on a fresh frame;
`ev_query` already returns an i32 that an execution result could satisfy.
Two edits (the MAP branch, removing the shadow teach) would close the loop.
A builder who thought of the graph as "the promoted artifact" rather than
"the certificate for the taught fact" would have written it that way.

**The architectural reason the omission happened.** TNN-2's construction
was specified and built as a *miss policy*: `mp_run` is literally headed
"trial-based miss policy (Change 1)". A miss policy, in this architecture,
produces an answer value for a miss, and the architecture's standing
contract for a produced answer is `ev_teach_in`: answers are facts. The
query/answer contract is value-typed (`ev_query` returns i32), inherited
from the TNN-1 standing machine, which the root-cause analysis correctly
identified as "a competent retrieval/standing machine". TNN-2 grafted
construction onto a memoization machine without changing what an answer is.
Nobody forgot a call site; the design never promoted the graph to a
first-class answerer, because the architecture has no slot for
"procedure-valued answers": no procedure standing, no procedure
contradiction, no procedure eviction, no procedure identity across
revision. Making the wiring coherent (Change 3 and Change 4 above) is
architectural work, not a two-line fix.

**The deeper layer is architectural, full stop.** Section 1, Layer 2: the
graphs are value traces because the frozen ISA cannot express relational
dereference. A subject-general reusable procedure ("follow relation r from
the query subject") is inexpressible in MOVE/BRANCHEQ/INC/DEC over frame
slots and fixed node ids. Fixing that touches the protected-core boundary
(a memory/lookup primitive), which is Micah's decision under the ISA
freeze, not a builder's wiring choice. This is exactly the H2 hypothesis
in the interaction report: procedures as write-only certificates.

Summary judgment: the query-path bypass is a wiring omission inside a
memoization-shaped architecture; the value-trace encoding is a deep
architectural limitation at the ISA boundary. Either one alone is fatal to
C0-D. Both are present.

## 4. Would executing promoted graphs satisfy C0-D

No. Execution is necessary but not sufficient. It would make C0-D
*testable*; it would not make it *true*.

**Why it is necessary.** C0-D demands that the invented structure improve
transfer, prediction, procedure learning, causal inference, memory,
planning, or sample efficiency. A structure the cognition path never
executes is causally inert downstream: it cannot improve anything, because
nothing downstream can observe it except revision (which reads MAPs only to
patch literals) and tests. The current architecture cannot even run the
C0-D experiment. This is the precise sense in which C0-D "fails
structurally, not just empirically" (interaction report, section 6).

**Why it is not sufficient.** Suppose the section 2 wiring lands and MAPs
execute at query time. What executes is still:

- a template instance from a finite researcher-authored family (construction
  red team, commit `340e94e3e`: CONSTRUCTION-ATTACK-SUCCESS; three
  assemblers, two reachable in production, hard depth/path/value bounds).
  Re-executing a template instance reuses the researcher's template, not an
  invented structure.
- a value trace bound to its licensing instance (section 1, Layer 2).
  Re-execution on the same (s, r) recomputes the known answer: a slower
  cache, not improved capability. Re-execution on a new subject fails
  closed (-999999). No transfer, no prediction gain, no sample efficiency.
- a structure promoted because its execution matched an
  environment-supplied `expected` (`t2_try_verify`, 497; in the sealed
  evaluation the driver supplies the answer). The graph never produced
  knowledge the system did not already have handed to it.

There is a further subtlety that cuts against naive re-execution. A value
trace goes stale when licensing facts change; re-executing it then returns
a *wrong* answer with full confidence. The current design (memoize the
answer, revise the graph on contradiction) is arguably more correct than
blind re-execution of traces. That is why revision exists, and why the
revision red team finding matters here: the repair is a single-schema
literal patch (commit `687ba0219`: REVISION-ATTACK-SUCCESS), so the
staleness remedy is as narrow as the construction it serves. Execution
without portable procedures and without general revision would trade one
degeneracy (inert certificates) for another (confident stale traces).

**What would count.** C0-D needs the executed structure to do something the
fact store cannot: answer new (s, r) pairs by executing a learned procedure
(transfer), compose promoted graphs as components of new graphs (the MUL
Rung B direction: graphs calling graphs, not facts), or recompute
correctly when licensing facts change without a researcher-shaped repair
schema. None of that is reachable from value traces in the frozen ISA.

## 5. Relation to the transfer analyst's behavioral probes

The transfer analyst's probes (`tnn2_transfer/transfer_driver.zag`,
results in `probes_run1.txt`, work in progress, read-only here) are the
behavioral counterpart of this structural analysis. The structural findings
predict their outcomes exactly, which is a consistency check on both.

- **P1 (persistence).** `P1 requery_ans=5` with `P1 map_after=45` (MAP
  intact). The probe then calls `t2_exec` *manually* (`P1 reexec=5`) to
  show the graph still computes the answer. That manual call is the tell:
  `ev_query` itself never executed the graph; the requery answer came from
  the memoized fact via `activate`. Behaviorally the system "remembers";
  structurally it remembers a fact, not a procedure. The probe cannot
  distinguish these without the white-box reader enumeration in section 0.
- **P2 (cross-subject).** `P2 rebuilt_fresh_map=1`, `P2 maps_after=2`: the
  second subject gets a brand-new MAP; the first graph is not reused.
  `P2 oldroot_on_7=-999999`: direct execution of the first graph on the
  new subject fails closed. This is the behavioral signature of the Layer 2
  value-trace finding: the graphs are not subject-general procedures, so
  there is no reuse to observe even if the query path executed them.
- **P3 (revision reuse).** Contradiction updates the MAP answer field
  (`map_ans_field=999`) and teaches new facts; requery returns 999 from
  the new fact. Consistent with revision-as-literal-patch flowing through
  the fact store, the only channel revision has into future queries.
- **P4 (interference).** Output truncated in `probes_run1.txt` (ends at
  `P4 map=45`); no behavioral conclusion can be drawn from it yet.

**The discriminator this analysis hands the transfer analyst:** any
apparent transfer in future probes must be attributed to the fact store
(shared licensing facts visible to `t2_gather`, corrected facts from
revision), never to graph reuse, because the reader enumeration proves no
query-time path reaches a MAP. A probe that wants to claim procedure reuse
must show, white-box, that a MAP node was read during the transfer query;
under the frozen build that event is impossible outside revision. If the
section 2 wiring ever lands, the probes should be re-run with that
white-box check as the reuse criterion, not answer equality.

## 6. Minimal change making C0-D structurally possible

"Structurally possible" means: the architecture can run the C0-D
experiment (an executed structure feeding a later query), not that C0-D is
satisfied. The minimal wiring, as a sketch for TNN-3 (never for the frozen
build):

1. `ev_query` (813): MAP-lookup branch before `activate`; on a live MAP
   for (s, r), return `t2_exec(W, ng(W,m,20), s)`; fall through on
   -999999.
2. `promote_graph` (533): delete line 541 (`ev_teach_in(W,s,r,ans)`); the
   MAP becomes the promoted artifact.
3. Liveness/shadowing policy: live executable MAP wins over facts;
   supersession and decay apply to MAPs as they do to facts.
4. `ev_observe` contradiction retargeted at the MAP rather than a shadow
   fact (the DEP scan in `revise_on_contradict` already enumerates the
   MAPs).

Explicitly out of scope for "minimal": template generality (C0-B),
expected-gated verification, portable procedures (Layer 2, ISA boundary),
and general revision. Those are separate architectural changes with their
own preregistrations. Landing the four wiring items would convert the
C0-D verdict from "fails structurally" to "testable, currently failing
behaviorally", which is the honest staging the interaction report's H2
recommends.

## Consequences for frozen claims

- BUILD-PASS (`f4de7ff46`) and REPRO-PASS (`fdf1fa626`) are unaffected:
  this analysis concerns reuse structure, not build integrity or
  determinism.
- The C0-D failure is structural and prior to any behavioral measurement:
  no future score on FW1-FW9 or the post-freeze battery can establish C0-D
  for the construction mechanism, because the mechanism's output is
  causally inert at query time regardless of score. Even a 9/9 would be
  fact-memoization performance, not procedure reuse.
- The failure has two independent sufficient causes (query-path bypass;
  value-trace encoding at the ISA boundary). TNN-3 root-cause work must
  address both; fixing one leaves C0-D failing on the other.
- No new opcodes, modes, bridges, handlers, or semantic cases are proposed
  here. The Layer 2 fix would touch the protected-core boundary and is
  therefore banked as Micah's decision, not taken here.

Verdict: **C0D-STRUCTURAL-ANALYSIS-COMPLETE**.
