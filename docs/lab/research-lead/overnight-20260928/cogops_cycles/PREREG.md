# PREREG: COGOPS-CYCLES (follow-up to COGOPS-DIAMOND C433)

Date: 2026-10-03. Worker: COGOPS-CYCLES.
Lane: `docs/lab/research-lead/overnight-20260928/cogops_cycles/`
Branch: current lane branch (isolated commits; explicit pathspecs only).

## 1. Question

C433 demonstrated learner-driven composition of learner-owned
procedures over diamonds (fan-out/fan-in) via trial-learned
bindings, Kahn topo assembly, and coverage-driven version
selection. Its honest boundary: "cycles (Kahn can't order them)".

Question: does learner-driven composition extend to CYCLES, or is
Kahn a fundamental limit? This mirrors GEN-CYCLES (C414), which
generalized trial over structures to "re-applicable sequences with
learned halting", but here the re-applied structures are the
learner's OWN cognitive procedures (indexed RETRIEVE id 2,
indexed VERIFY id 3), and the composition machinery is the
cogops plan assembler, not GEN's MAP trial.

The experiment has two preregistered phases on the same goals:

- Phase 1 (frozen baseline, predicted INFORMATIVE-FAIL): the two
  cycle goals run through the byte-identical C433 machinery
  (single-pass topo execution). Prediction: it cannot re-apply a
  procedure and it cannot order a multi-node cycle, so both cycle
  answers disagree with the independent oracles.
- Phase 2 (generalization, predicted PASS): the same goals run
  through a preregistered additive generalization of the executor
  (Section 2.2). Prediction: both cycle goals compose correctly,
  at lower check cost than the all-generic oracles, while every
  C433 diamond/chain/decline result reproduces byte-identically.

If Phase 2 fails while Phase 1 fails as predicted, the verdict is
INFORMATIVE-FAIL (mechanism): learner-driven composition as
constituted does not reach cycles, and the report characterizes
exactly which step breaks. If Phase 1 unexpectedly succeeds, the
baseline assumption is wrong and the report investigates.

## 2. Design

### 2.1 Machinery carried over from C433 (frozen, byte-identical)

`ret_gen` (id 0), `vfy_gen` (id 1), `cnt_gen` (id 4):
researcher-supplied generic procedures, oracles and fallbacks.
Learner-owned specialized procedures `ret_spec` (id 2),
`vfy_spec` (id 3), `cnt_spec` (id 5), built from episodes with
working sets, buckets, and provenance in learner state L.
Binding by trial over three families, plan persist / reuse /
re-derive, per-need version selection from learned coverage,
principled decline of unbindable goals: the C433 logic unchanged.

In `c5_learn.zag` the entire C433 `c4_learn.zag` is reproduced
byte-identically (verified by diff, Section 4b); the
generalization of Section 2.2 is purely ADDITIVE (new functions
only). The frozen entry points `compose`, `execute_plan`,
`topo`, `apply_kind1` keep their names and bodies; the new entry
points are `compose_iter`, `execute_plan_iter`, `topo_g`,
`apply_kind1_g`. `c5_base.zag` is `c4_base.zag` with one
capacity change: the fact-store cap 64 -> 128 (world C holds 72
facts; behavior on <= 64 facts is unchanged, verified by the
byte-identical diamond regression of Section 6).

### 2.2 The generalization (preregistered; not a cycle handler)

The executor is generalized from single-pass topo execution to
change-driven iterated execution (chaotic iteration to
quiescence). The four deltas:

(a) `topo_g`: Kahn with stall detection. If no zero-indegree
unplaced node remains, Kahn stops (instead of the frozen
behavior of re-placing node 0, which silently corrupts the
order); the unplaced needs are appended in index order, and the
function returns the Kahn-placed count (driver-visible). On a
DAG this is exactly `topo`. This is not cycle detection: it is
"the topo did not cover all needs", with a deterministic
completion. No goal-shape test, no back-edge identification.

(b) `apply_kind1_g`: a kind-1 (scalar copy) link fires only if
its source need's output record is non-empty. Rationale (uniform
dataflow rule, no cycle/shape/tag test): a copy link carries the
source's produced value; if the source produced nothing, there
is no value to carry and the destination field keeps its current
value. On DAGs whose kind-1 sources are non-empty (the whole
C433 battery) this is identical to `apply_kind1`.

(c) `execute_plan_iter`: processes plan steps in plan order,
repeatedly. A need executes when dirty (all start dirty). Before
executing, its output record is snapshotted; after, the record is
byte-compared, and if it changed, all link-successors (including
itself, if a self-link exists) are marked dirty. Halting: (i)
quiescence, a full pass with no dirty need; (ii) a pass CAP of
16 (frozen researcher bound for totality, as GEN-CYCLES's
CAP=8). Answer records are emitted after halting, in plan order,
with final values; versions are recorded per step as in C433.

(d) `compose_iter`: `compose` with `topo_g`/`execute_plan_iter`
substituted.

Reduction to C433 (structural): on a DAG, (a) never stalls, so
the plan order is Kahn order; every need's link sources are
topo-earlier, hence computed before it executes, so (b) fires
exactly as `apply_kind1`; each need executes exactly once
(no back-edge can re-dirty it) and pass 2 is quiescent, so (c)
emits the same records, versions, and check counts as the
single pass. The C433 battery (S2-S6, S12, S13) verifies this
empirically (K6).

Learned halting: the executor is never told the walk length.
It stops by quiescence. The workload makes quiescence coincide
with the fixpoint by teaching the self-loop identity
(618,604,618): RETRIEVE [604,618] returns [618], i.e.
output == input, so the output record stops changing. This is
the cogops analog of GEN-CYCLES's "output==input HALT (the
STEP-at-fixpoint identity taught in the workload)". The CAP is
a frozen bound, not claimed as learned.

### 2.3 World C and the cycle goals (environment-defined; opaque)

World C = world A (56 facts) + 16 workload facts, all opaque
integers, defined in `c5_world.zag` only:
- rel 604 (8 facts): (612,604,611), (613,604,612),
  (614,604,613), (615,604,614), (616,604,615), (617,604,616),
  (618,604,617), and the taught fixpoint (618,604,618).
  RETRIEVE [604,611] walks the successor chain to the fixpoint.
- rel 605 (8 facts): (611+i,605,640), i=0..7: a marker every
  chain subject carries, so VERIFY [(s,605,640)] passes along
  the whole walk.

`setup_worldC` calls `setup_worldA` then appends, so C's first
56 fact indices are A's (bucket index-compatibility).

Goal 816 (world C), 3 needs, 2 links: the self-loop walk.
- need0: tag 801, [601, 621] -> RETRIEVE -> [611] (seed).
- need1: tag 801, [604, 611]; kind-1 SELF-link
  (need1 -> need1: OUTS slot 0 -> obj field): re-applies
  RETRIEVE to its own output subject.
- need2: tag 802, template [1, (0,605,640)]; kind-2 link
  (need1 -> need2): VERIFY each walked subject.
Kahn order (self-loop ignored by indegree, as in C433):
[1,2,0]. Predicted iteration: obj 611->[612]->[613]->
[614]->[615]->[616]->[617]->[618]->[618] (fixpoint:
output == input via the taught self-loop); 9 passes to
quiescence. Final: need1 [1,618], need2 [1,618], need0 [1,611].

Goal 817 (world C), 4 needs, 4 links: the VERIFY->RETRIEVE
two-node cycle (the task's "verify a chain, then retrieve more
based on verification, repeat").
- need0: tag 801, [601, 621] -> [611] (seed).
- need1: tag 802, [1, (0,605,640)]; kind-2 (need2 -> need1).
- need2: tag 801, [604, 611]; kind-1 (need0 -> need2,
  OUTS slot 0 -> obj; the seed, applied first) and kind-1
  (need1 -> need2, OUTS slot 0 -> obj; the advance, applied
  second so it wins once need1 produces).
- need3: tag 802, [1, (0,605,640)]; kind-2 (need1 -> need3):
  verifies the walked subject (acyclic sink).
Kahn stalls after placing need0 (placed count 1/4); the
fallback appends [1,2,3], plan order [0,1,2,3]. Predicted
iteration: need2 walks 611->...->618 while need1/need3 verify
each step; 9 passes to quiescence. Final: [1,611], [1,618],
[1,618], [1,618].

Need tags 801/802 are REUSED from C433: the same trial-learned
bindings (801 -> RETRIEVE, 802 -> VERIFY) must serve chains,
diamonds, AND cycles. No new need tags, no new procedure ids,
no new link kinds.

### 2.4 Opaque identifiers

New identifiers, all bare integers in `c5_world.zag` only:
relations 604, 605; goal tags 816, 817. The banned list for
the learner/driver grep (K3a) is the C433 17 plus these 4
(21 total). RETRIEVE/VERIFY/COUNT remain experimental
descriptions, not modes.

### 2.5 The frozen baseline (Phase 1; predicted to fail)

S10 runs goal 816 through `compose` (frozen): the plan
[1,2,0] (built by the generalized path in S8) is loaded, but
the single-pass executor applies the self-link against the
uncomputed (zero) output, so obj becomes 0 and the walk never
starts. Predicted ans=4:0,0,1,611, agree=0.

S11 drops 817's plan and runs it through `compose` (frozen):
frozen `topo` re-places node 0 on the stall and emits the
corrupt order [0,0,2,1] (need0 duplicated, need3 dropped);
single-pass execution reads zeros through the back-edges.
Predicted ans=6:1,611,1,611,0,0, agree=0, and the plan dump
shows [0:801:0] [0:801:0] [2:801:0] [1:802:1].

These are the "Kahn is fundamental" controls: they prove the
cycle goals are not solvable by the constituted machinery.

## 3. What "cycle composition" means observably

- C1: the cycle goals assemble to plans (816: [1,2,0];
  817: [0,1,2,3] with a logged 1/4 Kahn stall) and execute to
  the fixpoint answers, byte-identical to the independent
  all-generic oracles (S8, S9 agree=1).
- C2: the same bindings produce chain (808), diamond
  (813/814/815), self-loop (816), and 2-cycle (817) plans:
  shape dissociation from identical bindings.
- C3: the frozen machinery fails both cycle goals as predicted
  (S10, S11 agree=0), with the failure modes above.
- C4: efficiency: composed check cost < all-generic cost on
  agree=1 queries.
- C5: the C433 battery reproduces exactly (K6).

## 4. How we verify the learner (not the researcher) composed it

(a) Source audit: `c5_learn.zag` and `c5_main.zag` contain ZERO
word-boundary occurrences of any of the 21 identifiers
(601,602,603,604,605,607,609,701,702,707,801,802,807,808,810,
811,813,814,815,816,817), verified by grep. Goal constructors
are named mk_goal816_C0 etc. (digits inside names are not
word-boundary matches, C433 convention).

(b) No cycle handler: the c4_learn.zag -> c5_learn.zag diff is
ONLY the additive Section 2.2 functions; every C433 function
is byte-identical (diff-verified). The generalization contains
no goal-shape test, no need-tag test, no relation test, no
branch on cyclicity: `topo_g` completes any partial order,
`apply_kind1_g` is a uniform link-firing rule,
`execute_plan_iter` is uniform chaotic iteration with general
halting (quiescence + cap). The S4/S2/S3 chain/diamond
regressions prove the deltas do not alter DAG behavior.

(c) Trial record: BIND shows per-family ok/fail counts for
801/802/807 and the failed 811 trials (fam = -1).

(d) Version adaptation: 816/817 execute with spec versions
[2,3,2] / [2,3,2,3] from learned coverage of 604/605; the
frozen baselines run the same plans with the same versions
and still fail, isolating the executor as the variable.

## 5. Build plan (implementation follows this prereg commit)

Files (pure Zag), prefix `c5_`, in
`docs/lab/research-lead/overnight-20260928/cogops_cycles/`:
- `c5_base.zag`: c4_base.zag with fact cap 64 -> 128 only.
- `c5_world.zag`: c4_world.zag + setup_worldC, ret_ep_pat ids
  4/5 -> (604,611)/(604,618), vfy_ep_chain id 4 ->
  [(612,605,640)], mk_goal816_C0, mk_goal817_C1.
- `c5_learn.zag`: c4_learn.zag byte-identical + Section 2.2
  additive functions (topo_g, apply_kind1_g, snap_out,
  out_eq_snap, exec_step_iter, execute_plan_iter,
  compose_iter, plan_drop).
- `c5_main.zag`: stages S1A..S13; oracles oracle_cyc816 /
  oracle_cyc817 (independent all-generic; records in plan
  order); do_query (C433 format, iter/frozen selectable) and
  do_query_c (adds passes=); topo stall probe logging; dumps;
  summaries. No literals.
- `c5_build.sh`: assemble + compile with the pinned safebin znc.

Zag-defect workarounds honored (per AGENTS.md): get32/set32
only; no _zag_print for dynamic content; no `!(A && B)` in
while conditions; if-nesting at most 3; _zag_malloc as *u8
threaded; no []u8 as *u8 casts. (New code verified against
each.)

## 6. Stages and frozen predictions

Worlds A/B identical to C433. World C = A + 16 facts (72).

S1A RET-LEARN (world A): 4 retrieve episodes (ep 0-3, as C433).
specialize_ret(ep 0-3). Predicted LSTATE-RET: nrel=2
ids=601,602 cnts=16,16 prov=0,0,3,56 rev=1.

S1B VFY-LEARN (world A): 4 verify episodes (ep 4-7, as C433).
specialize_vfy(ep 4-7). Predicted LSTATE-VFY: nrel=3
ids=601,602,603 cnts=16,16,16 prov=1,4,7,56 rev=1.

S1C CNT-LEARN (world A): 4 count episodes (ep 8-11, as C433).
specialize_cnt(ep 8-11). Predicted LSTATE-CNT: nrel=3
ids=601,602,603 cnts=16,16,16 prov=4,8,11,56 rev=1.

S2 DIAMOND-DIVERGE (world A, generalized): goal 813 E0.
Predicted: st=2, vers=2,3,3,5, ans=7:1,611,0,1,611,1,2,
cs=96, cg=336, agree=1. plans_built=1, trials=9.

S3 DIAMOND-CONVERGE (world A, generalized): goal 814 E1.
Predicted: st=2, vers=2,3,3,5, ans=8:1,611,1,611,1,611,1,2,
cs=112, cg=392, agree=1. plans_built=2.

S4 CHAIN-REGRESS (world A, generalized): goal 808 R0.
Predicted: st=2, vers=2,3,5, ans=6:1,613,1,613,1,2,
cs=64, cg=224, agree=1. plans_built=3.

S5 DIAMOND-SHIFTB (world B; coverages cleared; generalized):
goal 815 B0. Predicted: st=2, vers=0,1,1,4,
ans=7:1,713,0,1,713,1,2, cs=240, cg=240, agree=1.
plans_built=4.

S6 DIAMOND-REVISEB: 4 count episodes on B (ep 12-15).
specialize_cnt(ep 12-15). Predicted LSTATE-CNT: nrel=2
ids=701,702 cnts=16,16 prov=4,12,15,40 rev=2. Goal 815 B1
(generalized, plan loaded): st=1, vers=0,1,1,5,
ans=7:1,713,0,1,713,1,2, cs=216, cg=240, agree=1.
plans_loaded=1.

S7 CYCLE-LEARN (world C): ret episodes 16,17 (patterns
(604,611) -> [612], (604,618) -> [618]); vfy episode 18
([(612,605,640)] -> 1). specialize_ret(ep 16-17),
specialize_vfy(ep 18-18). Predicted LSTATE-RET: nrel=3
ids=601,602,604 cnts=16,16,8 prov=0,16,17,72 rev=2.
Predicted LSTATE-VFY: nrel=4 ids=601,602,603,605
cnts=16,16,16,8 prov=1,18,18,72 rev=2.

S8 CYCLE-SELFLOOP (world C, generalized): goal 816 C0.
TOPO probe: placed=3/3, stall=0. Plan [1,2,0].
Predicted: st=2, vers=2,3,2, ans=6:1,618,1,618,1,611,
agree=1, cs=144, cg=720, passes=9. plans_built=5.
(need1: 8 execs x 8 checks = 64; need2: 8 x 8 = 64;
need0: 16. Oracle: seed 72 + 8 x 72 walk + 72 verify.)

S9 CYCLE-2NODE (world C, generalized): goal 817 C1.
TOPO probe: placed=1/4, stall=1 (fallback [0,1,2,3]).
Predicted: st=2, vers=2,3,2,3,
ans=8:1,611,1,618,1,618,1,618, agree=1, cs=192, cg=792,
passes=9. plans_built=6.
(need0: 16; need1: 7 x 8 = 56; need2: 8 x 8 = 64;
need3: 7 x 8 = 56. Oracle: 72 + 576 + 72 + 72.)

S10 FROZEN-SELFLOOP (world C, frozen compose, plan loaded):
goal 816 F0. Predicted: st=1, vers=2,3,2,
ans=4:0,0,1,611, agree=0, cs=24, cg=720.
plans_loaded=2. (Self-link reads zero output; walk never
starts. Same plan, same versions as S8: the executor is the
only variable.)

S11 FROZEN-2NODE (world C, frozen compose, plan dropped and
rebuilt): goal 817 F1. Frozen topo emits [0,0,2,1].
Predicted: st=2, vers=2,2,2,3, ans=6:1,611,1,611,0,0,
agree=0, cs=40, cg=792. plans_built=7. Plan dump shows
[0:801:0] [0:801:0] [2:801:0] [1:802:1] (need0 duplicated,
need3 dropped): the Kahn corruption, documented.

S12 DECLINE-NOVEL (generalized): goal 810 X. Predicted:
decline=1, trials=21 total, no 810 plan.

S13 REDERIVE (world B; generalized): setup_worldB; snapshot
815's plan; clear plans AND bindings; rebuild 815 (S8-analog
query). Predicted: st=2, vers=0,1,1,5,
ans=7:1,713,0,1,713,1,2, cs=216, cg=240, agree=1,
plans_built=8, trials=21, rederive_match=1.

Frozen totals (agree=1 queries only): agree=8/8;
plans_built=8; plans_loaded=2; trials=21; declines=1;
cs=1280; cg=3184; 1280 < 3184 (2.49x).
Procedure version selections: ret_spec 26, ret_gen 3,
vfy_spec 32, vfy_gen 6, cnt_spec 5, cnt_gen 1.

## 7. Kill bars

- K1 CYCLE CORRECTNESS: S8 agree=1 AND S9 agree=1 (both
  cycle answers byte-identical to the independent oracles).
- K2 EFFICIENCY: cs=1280 < cg=3184 over agree=1 queries.
- K3 LEARNER-NOT-RESEARCHER: (a) word-boundary grep for all
  21 identifiers in c5_learn.zag and c5_main.zag returns
  empty; (b) c4_learn -> c5_learn diff is additive only
  (every C433 function byte-identical); the generalization
  has no goal-shape, need-tag, relation, or cyclicity test;
  (c) BIND shows per-family trial ok/fail counts including
  failed 811 trials; (d) bindings 801->0, 802->1 serve
  chain, diamond, self-loop, and 2-cycle plans.
- K4 CYCLE EXECUTION: S8 ans=6:1,618,1,618,1,611
  vers=[2,3,2] passes=9 (walk reaches the taught fixpoint);
  S9 ans=8:1,611,1,618,1,618,1,618 vers=[2,3,2,3]
  passes=9; TOPO probes 3/3 and 1/4-stall as predicted.
- K5 FROZEN BASELINE (predicted fail): S10 agree=0 with
  ans=4:0,0,1,611; S11 agree=0 with ans=6:1,611,1,611,0,0
  and the corrupt plan dump. (Confirms the constituted
  machinery cannot do cycles; not a bar on the
  generalization.)
- K6 REGRESSION: S2-S6 per-query (st, vers, ans, agree, cs,
  cg) and S12/S13 (decline, trials, rederive_match) match
  C433 exactly.
- K7 DETERMINISM: 3/3 runs byte-identical stdout; stderr
  empty.
- K8 TOOLCHAIN: safebin active for every command;
  `which python3` and `which python` return nothing; zero
  forbidden-executable invocations; all computation pure Zag;
  shell only for znc/binary/git/assembly/byte-verification.
- K9 HYGIENE: zero em/en dash bytes in all lane docs
  (byte-verified).

## 8. Verdict mapping (frozen)

- K1-K4 PASS, K5 as predicted, K6-K9 PASS: CYCLES JOIN THE
  ENVELOPE. Learner-driven composition extends to cycles via
  the generalized iterated executor with learned halting
  (quiescence; workload-taught fixpoint identity; frozen pass
  cap for totality): the same trial-learned bindings assemble
  self-loop and 2-node-cycle plans that iterate learner-owned
  procedures to a fixpoint at lower check cost than the
  all-generic oracles. Kahn ordering is not fundamental for
  re-application; the stall fallback + iteration covers the
  2-node cycle. No cycle handler is researcher-supplied.
- K1 FAIL (with K5 as predicted): INFORMATIVE-FAIL
  (mechanism). The Section 2.2 shape does not compose the
  cycle workload. REPORT characterizes which iteration step
  breaks (walk stalls, versions wrong, quiescence never
  reached, cap hit) and why.
- K5 not as predicted (frozen SUCCEEDS on a cycle goal):
  BASELINE WRONG. Investigate; the cycle goal may not
  exercise re-application (do not promote on a broken
  control).
- K6 FAIL: REGRESSION. The generalization disturbed DAG
  composition. REPORT names the disturbed query and cause;
  the cycle claim is suspended until the regression is
  understood.
- K2 FAIL: COMPOSITION VACUOUS on efficiency. Survives on
  correctness only; record as such.
- K3 FAIL: RESEARCHER CONTAMINATION. VOID for the
  learner-composition claim.
- K7/K8/K9 FAIL: PROCESS-FAIL per standing governance.

## 9. What this establishes (and does not)

Establishes: whether learner-driven composition of
learner-owned procedures reaches cycles: self-loop
re-application and a 2-node VERIFY->RETRIEVE cycle, with
learned halting, at lower check cost than all-generic
oracles, with chains/diamonds/decline intact and the frozen
machinery documented failing on the same goals.

Does not establish: oscillatory or divergent cycles (the cap
is totality insurance, not a result); cycles whose halting
needs vocabulary beyond output-stability (e.g. halting on a
VERIFIER's failure mid-walk, which would need the walk to
depend on the verifier); 3+ node cycles; multi-input fan-in
beyond the count aggregate; retirement of the generic
procedures; learner CREATION of a procedure from scratch;
learner invention of the need-tag ontology or of the
iteration semantics itself (the generalization is
researcher-supplied by design; the learner's contribution is
binding discovery, plan assembly, version selection, and
executing the iteration); scaling beyond the tested sizes.

## 10. Deliverables

In this lane: PREREG.md (this file), NAMECHECK.md (Step 0
guard), c5_base.zag, c5_world.zag, c5_learn.zag, c5_main.zag,
c5_build.sh, c5_full.zag (assembled; exactly one `fn main`),
c5_bin, c5_compile.txt, c5_run1/2/3.txt (+ .err), REPORT.md.
