# PREREG: COGOPS-3WAY (follow-up to COGOPS-COMPOSE C417)

Date: 2026-10-03. Worker: COGOPS-3WAY.
Lane: `docs/lab/research-lead/overnight-20260928/cogops_3way/`
Branch: current lane branch (isolated commits; explicit pathspecs only).

## 1. Question

C417 (COGOPS-COMPOSE) demonstrated that a learner can own two
specialized procedures (indexed RETRIEVE id 2, indexed VERIFY id 3),
discover need-to-procedure bindings by trial, assemble per-goal plans
in opposite orders from identical bindings, select versions per need
from learned coverage, persist/reuse/re-derive plans, and decline
unbindable goals. Its honest boundary: "two-procedure composition
only, not general DAG/fan-out/fan-in."

Question: does learner-driven composition scale to THREE procedures,
or does it break at 3? The challenge grows: 3! = 6 possible orders,
version selection per procedure per need, plan reuse across goals, and
a new fan-in aggregate link kind the assembler must honor. No
researcher-supplied pipeline may encode any assembly; the learner must
bind, order, version-select, persist, and decline by its own
trial-derived structure.

## 2. Design

### 2.1 Researcher-supplied generic procedures

`ret_gen(A, rel, obj)` (id 0): all subjects s with (s, rel, obj).
Cost = nfacts checks. (Same as C417.)

`vfy_gen(A, C)` (id 1): 1 iff every chain step matches a fact.
Cost = nsteps * nfacts, no early exit. (Same as C417.)

`cnt_gen(A, rel, subjbuf, nsubs)` (id 4): distinct-object count:
for each subject in the list, scans all facts, collects distinct
objects o with (subj, rel, o). Cost = nsubs * nfacts fact checks
(dedup comparisons not counted, same convention as C417). Always
correct; the learner's contribution is specialization, binding,
assembly, version selection, never correctness repair.

### 2.2 Learner-owned specialized procedures (all three built by the learner)

`ret_spec` (id 2): built by `specialize_ret` from the learner's
retrieve episodes. Per-relation buckets over the retrieve working
set. (Same design as C417.)

`vfy_spec` (id 3): built by `specialize_vfy` from the learner's
verify episodes. (Same design as C417.)

`cnt_spec` (id 5): built by `specialize_cnt` from the learner's
count episodes. Per-relation buckets over the count working set
(relations the learner actually used in count episodes); at query
time scans only the bucket for the pattern's relation per subject
and dedups objects. Returns -1 if the relation is outside the
learned coverage (unreachable in the passing arms; selection logic
prevents it).

All three bodies (working sets, buckets, provenance
parent/ep0/ep1/nfacts/revision) live entirely in learner-owned
state. This satisfies the task requirement: all three procedures
are learner-owned specialized procedures, not generic seeds.

### 2.3 Composite goals (environment-defined; opaque identifiers)

Goals are defined by the world/driver, never by the learner. Same
record layout as C417, plus a third link kind. Need tags: 801 =
pattern need (RETRIEVE family), 802 = chain need (VERIFY family),
807 = count need (COUNT family), 811 = novel need (served by
nothing; decline control). The learner is never told these bindings.

Family shape signatures (generic machinery, as arity was in C417):
family 0 accepts exactly 2-field needs; family 1 accepts
chain-shaped needs (nfields = 1 + 3*nsteps, 1 <= nsteps <= 16);
family 2 accepts exactly 3-field needs [rel, aggop, subj] with
aggop == 1 (distinct-object count). The decline need 811 =
[9,0,0]: 3 fields but aggop 0, refused by family 2; refused by
family 0 (not 2 fields) and family 1 (not chain-shaped).

Link kinds: 1 = scalar copy (as C417), 2 = fan-out subject fill
(as C417), 3 = aggregate subject-list fill: the destination count
need's subject list becomes the source need's output record
subjects (fan-in over a variable-size list).

Goal 808: needs [801-pattern P, 802-chain template T, 807-count
[rel2,1,0]]; links: kind-2 (need0 output -> need1 subject slots),
kind-3 (need1 output -> need2 subject list). Forced order:
RETRIEVE, VERIFY, COUNT.

Goal 809: needs [807-count [relA,1,subj0], 801-pattern [0,obj],
802-chain template T]; links: kind-1 (need1.rel := need0 input
field0, the pivot), kind-2 (need1 output -> need2 subject slots).
Forced order: COUNT, RETRIEVE, VERIFY. The count runs first on a
literal subject; its input relation is pivoted into the retrieve.

Goal 812: needs [802-chain C (concrete), 801-pattern [0,obj],
807-count [rel2,1,0]]; links: kind-1 (need1.rel := need0 input
field2 = step-0 relation), kind-3 (need1 output -> need2 subject
list). Forced order: VERIFY, RETRIEVE, COUNT.

Goal 810 (decline control): needs [811 (3 fields [9,0,0])]. No
family accepts; learner must decline.

Three of the six possible orders are exercised (RVC, CRV, VRC),
all forced by goal link structure from identical learned
bindings. The learner code contains no goal-tag, need-tag, or
relation literals and no plan sequences.

### 2.4 Learner-driven composition (the load-bearing mechanism)

Same machinery as C417, extended to three families:

(a) BINDING BY TRIAL over families 0, 1, 2. Trial outcomes
recorded per family (ok/fail counts). 801 -> RETRIEVE (2 fields),
802 -> VERIFY (chain shape), 807 -> COUNT (3 fields, aggop 1),
811 -> unbound (all refuse).

(b) ASSEMBLY PER GOAL: topological order over all three link
kinds; plan stored as [(need index, need tag, family)...] with 3
steps. Same bindings produce three different orders.

(c) VERSION SELECTION PER NEED PER EXECUTION from each family's
learned coverage: ret_version -> 2/0, vfy_version -> 3/1,
cnt_version -> 5/4.

(d) REUSE AND DECLINE as C417.

### 2.5 Opaque identifiers

World A relations: 601, 602, 603 (each: 8 subjects x 2 objects =
16 facts), distractors 607, 609 (4 facts each), 56 facts. World B
relations: 701, 702 (16 facts each), distractor 707 (8 facts), 40
facts. Subjects/objects are opaque integers. Goal tags 808, 809,
810, 812; need tags 801, 802, 807, 811. No domain labels appear in
design, code, or docs. RETRIEVE/VERIFY/COUNT are experimental
descriptions of the procedures under test (as in C417), not modes
in any architecture.

## 3. What "composition" means observably

- C1: executed procedure sequences are [RET,VFY,CNT] for 808,
  [CNT,RET,VFY] for 809, [VFY,RET,CNT] for 812; all three appear
  in learner-state plan dumps, assembled from identical learned
  bindings.
- C2: executed versions are the specialized procedures where
  covered (per-need use counters), with per-need fallback to
  generics where uncovered.
- C3: every composite answer agrees byte-for-byte with an
  independent all-generic oracle composition (12/12).
- C4: no plan exists a priori. First encounter builds
  (plans_built); repeats reload (plans_loaded); 810 declines
  (declines=1).

## 4. How we verify the learner (not the researcher) composed them

(a) Source audit: `c3_learn.zag` and `c3_main.zag` contain ZERO
occurrences of any goal-tag, need-tag, or relation literal
(601,602,603,607,609,701,702,707,801,802,807,808,809,810,811,812),
verified by word-boundary grep. Goal constructors are named
mk_goal808_A0 etc.; the tag digits inside those names are not
word-boundary matches (same convention as C417's mk_goal503_F0).

(b) Order dissociation: three distinct forced orders from the
same bindings. A researcher-supplied pipeline produces one order;
the learner produces three, following each goal's links.

(c) Trial record: the binding table shows per-family trial
ok/fail counts for tags 801, 802, 807, and 811; the 811 trials
fail for all three families and the learner declines.

(d) Version adaptation: the same stored 808 plan executes as
[spec,spec,spec] in S2, [gen,gen,gen] in S5 (coverages cleared /
world B), and [gen,gen,spec] in S6 (count re-specialized on B).

(e) Re-derivation: after clearing plans AND bindings, the learner
re-runs trials and rebuilds a byte-identical 808 plan (S8).

## 5. Build plan (implementation follows this prereg commit)

Files (all new, pure Zag), prefix `c3_`:
- `c3_base.zag`: z_alloc, get32/set32, output helpers (o_app,
  o_i64, o_nl, o_flush; single _zag_raw_syscall write; _zag_print
  never used for dynamic content), world arena, fact store,
  chain buffers, ret_gen (id 0), vfy_gen (id 1), cnt_gen (id 4).
- `c3_world.zag`: setup_worldA (56 facts), setup_worldB (40
  facts), ret_ep_pat (8 patterns), vfy_ep_chain (4 chains),
  cnt_ep_pat (8 count episodes), goal constructors
  mk_goal808_A0/A1/A2, mk_goal809_B0/B1, mk_goal812_C0/C1,
  mk_goal808_D0/D1/D2/D3, mk_goal810. All literals live here.
- `c3_learn.zag`: ret/vfy/cnt working sets, cov_find/has/log/
  clear per region, specialize_ret/vfy/cnt, ret_spec (id 2),
  vfy_spec (id 3), cnt_spec (id 5), episodes, ret/vfy/cnt
  _version, goal parsers, topo order, bind_find/bind_new,
  try_family (3 families), learn_bindings, plan_find/plan_store,
  apply_kind1/apply_kind3, compose, execute_plan, clear_plans,
  clear_bindings. No literals.
- `c3_main.zag`: stages S1A-S8, oracle_808/oracle_809/oracle_812
  (independent all-generic reference compositions), per-query
  compose + compare, dumps (LSTATE-RET/VFY/CNT, BIND, PLAN),
  summaries. No literals.
- `c3_full.zag`: concatenation of the four (exactly one
  `fn main`).
- `c3_build.sh`: assemble + compile with the pinned safebin znc.

Learner-state L (16384 bytes) layout:
- RET region: 0: ret_nrel; 4: ret_rel_ids[16]; 68: ret_cnt[16];
  132: ret_fidx[16][64]; 4228: ret_prov_parent (=0); 4232: ep0;
  4236: ep1; 4240: nfacts; 4244: rev.
- VFY region: 4248: vfy_nrel; 4252: vfy_rel_ids[16]; 4316:
  vfy_cnt[16]; 4380: vfy_fidx[16][64]; 8476: vfy_prov_parent
  (=1); 8480: ep0; 8484: ep1; 8488: nfacts; 8492: rev.
- CNT region: 8496: cnt_nrel; 8500: cnt_rel_ids[16]; 8564:
  cnt_cnt[16]; 8628: cnt_fidx[16][64]; 12724: cnt_prov_parent
  (=4); 12728: ep0; 12732: ep1; 12736: nfacts; 12740: rev.
- BIND table at 12744: 8 entries x 32 bytes:
  [tag, bound_fam, ok0, f0, ok1, f1, ok2, f2].
- PLAN table at 13000: 4 entries x 44 bytes:
  [goal_tag, nneeds, idx0, tag0, fam0, idx1, tag1, fam1, idx2,
  tag2, fam2].
- Stats at 13176: plans_built, plans_loaded, trials, declines,
  agree, cs, cg, ret_spec_uses, ret_gen_uses, vfy_spec_uses,
  vfy_gen_uses, cnt_spec_uses, cnt_gen_uses.

Check counting: K buffer cells: K[0] plan-execution checks,
K[4] all-generic oracle checks, K[8] trial checks, K[12] episode
scratch. Fact-row inspections only (dedup comparisons not
counted). Costs: ret_spec = bucket size per query; ret_gen =
nfacts; vfy_spec = bucket size per step; vfy_gen = nsteps *
nfacts; cnt_spec = nsubs * bucket size; cnt_gen = nsubs * nfacts.

Goal record layout (256-byte buffer): as C417, plus link kind 3
= aggregate subject-list fill.

Zag-defect workarounds honored (per AGENTS.md): get32/set32
only, no `as *i32` slice construction; no _zag_print for dynamic
content; no `!(A && B)` in while conditions; if-nesting at most
3; allocation via _zag_malloc as *u8 threaded through; no
[]u8 as *u8 casts.

## 6. Stages and frozen predictions

World A (56 facts): rel 601: (611+i,601,621+i) and
(611+i,601,631+i); rel 602: (611+i,602,622+i) and
(611+i,602,632+i); rel 603: (611+i,603,620+i) and
(611+i,603,630+i), i=0..7. Distractors: 607: (631+k,607,641+k);
609: (635+k,609,645+k), k=0..3.

World B (40 facts): rel 701: (711+i,701,721+i) and
(711+i,701,731+i); rel 702: (711+i,702,722+i) and
(711+i,702,732+i), i=0..7. Distractor 707: (731+k,707,741+k),
k=0..7.

S1A RET-LEARN (world A): 4 retrieve episodes (ep 0-3):
 (601,623)->[613]; (602,625)->[614]; (601,621)->[611];
 (602,622)->[611]. Learner logs rels {601,602}.
 specialize_ret(ep 0-3). Predicted LSTATE-RET: nrel=2
 ids=601,602 cnts=16,16 prov=0,0,3,56 rev=1.

S1B VFY-LEARN (world A): 4 verify episodes (ep 4-7):
 (611,601,621),(611,602,622) v=1;
 (612,603,621),(612,601,622) v=1;
 (613,602,624),(613,603,622) v=1;
 (614,601,624),(614,603,629) v=0.
 Learner logs rels {601,602,603}. specialize_vfy(ep 4-7).
 Predicted LSTATE-VFY: nrel=3 ids=601,602,603 cnts=16,16,16
 prov=1,4,7,56 rev=1.

S1C CNT-LEARN (world A): 4 count episodes (ep 8-11):
 (601,611)->2; (602,611)->2; (603,612)->2; (601,613)->2.
 (Each subject has 2 distinct objects per relation.)
 Learner logs rels {601,602,603}. specialize_cnt(ep 8-11).
 Predicted LSTATE-CNT: nrel=3 ids=601,602,603 cnts=16,16,16
 prov=4,8,11,56 rev=1.

S2 COMPOSE-808 (world A): first query A0 triggers trials (9)
 then plan build [(801,RET),(802,VFY),(807,CNT)].
 A0: P=(601,623)->[613]; T=(S,602,624),(S,603,622): 613
   passes both; count {613} via 601 -> {623,633} -> 2.
   Answer 6:1,613,1,613,1,2; vers [2,3,5]; cs=64 (16+32+16);
   cg=224 (56+112+56).
 A1: P=(602,626)->[615]; T=(S,601,625),(S,603,624): 615
   passes; count {615} via 601 -> {625,635} -> 2.
   Answer 6:1,615,1,615,1,2; vers [2,3,5]; cs=64; cg=224.
 A2: P=(601,621)->[611]; T=(S,602,629),(S,601,621): 611
   fails step 0 (629 not among {622,632}); count over {} -> 0.
   Answer 4:1,611,0,1,0; vers [2,3,5]; cs=48 (16+32+0);
   cg=168 (56+112+0).
 Predicted: plans_built=1, plans_loaded=2, trials=9, agree=3.
 BIND after S2: (801: fam 0, ok0 1, f1 1, f2 1),
 (802: fam 1, f0 1, ok1 1, f2 1),
 (807: fam 2, f0 1, f1 1, ok2 1).
 PLAN-808: n=3 [0:801:0] [1:802:1] [2:807:2].

S3 COMPOSE-809 (world A): bindings reused; plan build
 [(807,CNT),(801,RET),(802,VFY)] (COUNT first).
 B0: need0 [601,1,611] count -> 2; need1 [0,625] rel:=601
   (pivot from need0 input f0) -> [615];
   need2 T=(S,602,626),(S,603,624): 615 passes.
   Answer 5:1,2,1,615,1,1; vers [5,2,3]; cs=64 (16+16+32);
   cg=224 (56+56+112).
 B1: need0 [602,1,612] count -> {623,633} -> 2;
   need1 [0,623] rel:=602 -> [612];
   need2 T=(S,601,622),(S,603,621): 612 passes both.
   Answer 5:1,2,1,612,1,1; vers [5,2,3]; cs=64; cg=224.
 Predicted: plans_built=2, plans_loaded=3, agree=5.
 PLAN-809: n=3 [0:807:2] [1:801:0] [2:802:1].

S4 COMPOSE-812 (world A): bindings reused; plan build
 [(802,VFY),(801,RET),(807,CNT)] (third distinct order).
 C0: need0 C=(611,601,621),(611,602,622) v=1;
   need1 [0,626] rel:=601 (step-0 rel) -> [616];
   need2 [602,1,0] count {616} via 602 -> {627,637} -> 2.
   Answer 5:1,1,1,616,1,2; vers [3,2,5]; cs=64 (32+16+16);
   cg=224.
 C1: need0 C=(612,603,621),(612,601,622) v=1;
   need1 [0,624] rel:=603 -> [615];
   need2 [601,1,0] count {615} via 601 -> {625,635} -> 2.
   Answer 5:1,1,1,615,1,2; vers [3,0,5] (603 not in ret
   coverage {601,602}: per-need fallback inside one plan);
   cs=104 (32+56+16); cg=224.
 Predicted: plans_built=3, plans_loaded=4, agree=7.
 PLAN-812: n=3 [0:802:1] [1:801:0] [2:807:2].

S5 SHIFT-B (world B; all three coverages cleared): 808 queries;
 plan reloaded; versions per execution from coverage.
 D0: P=(701,723)->[713]; T=(S,702,724),(S,701,723): 713
   passes; count {713} via 701 -> {723,733} -> 2.
   Answer 6:1,713,1,713,1,2; vers [0,1,4]; cs=160; cg=160.
 D1: P=(702,727)->[716]; T=(S,701,726),(S,702,727): 716
   passes; count {716} via 701 -> {726,736} -> 2.
   Answer 6:1,716,1,716,1,2; vers [0,1,4]; cs=160; cg=160.
 Predicted: plans_loaded=6, agree=9.

S6 REVISE-B: 4 count episodes on B (ep 12-15):
 (701,711)->2; (702,711)->2; (701,712)->2; (702,713)->2.
 specialize_cnt(ep 12-15). Predicted LSTATE-CNT: nrel=2
 ids=701,702 cnts=16,16 prov=4,12,15,40 rev=2. (ret and vfy
 untouched: still cleared.)
 D2: P=(701,724)->[714]; T=(S,702,725),(S,701,724): 714
   passes; count {714} via 701 -> {724,734} -> 2.
   Answer 6:1,714,1,714,1,2; vers [0,1,5]; cs=136
   (40+80+16); cg=160.
 D3: P=(702,729)->[718]; T=(S,701,728),(S,702,722): 718
   fails step 1 (722 not among {729,739}); count over {} -> 0.
   Answer 4:1,718,0,1,0; vers [0,1,5]; cs=120 (40+80+0);
   cg=120.
 Predicted: plans_loaded=8, agree=11.

S7 DECLINE-810: goal 810, need 811 (3 fields [9,0,0]).
 Trials: RET refuses (3 fields, not 2), VFY refuses (not
 chain-shaped), CNT refuses (aggop 0, not 1). No binding;
 compose returns NO_PLAN; decline recorded.
 Predicted: declines=1, trials=12 total, BIND has 811 entry
 fam=-1 with f0=f1=f2=1.

S8 REDERIVE: dump PLAN-808 bytes (11 ints); clear plans AND
 bindings; recompose a D2-identical 808 query on B: trials
 re-run (9), plan rebuilt; dumped bytes identical to pre-clear.
 Execute: vers [0,1,5], answer 6:1,714,1,714,1,2, cs=136,
 cg=160, agree=12.
 Predicted: plans_built=4, trials=21, rederive_match=1.

Frozen totals: agree=12/12; plans_built=4; plans_loaded=8;
trials=21; declines=1; cs=1184; cg=2272; 1184 < 2272 (1.92x).
Procedure uses: ret_spec 6, ret_gen 6, vfy_spec 7, vfy_gen 5,
cnt_spec 10, cnt_gen 2.

Derivation notes: ret_spec costs one bucket scan (16 checks on
A and B); vfy_spec costs 16 per chain step (no early exit);
cnt_spec costs 16 per subject; ret_gen costs nfacts (56 A /
40 B); vfy_gen costs nsteps*nfacts (112 A / 80 B for 2-step
chains); cnt_gen costs nsubs*nfacts. A0: 16+32+16=64 vs
56+112+56=224. C1: 32+56+16=104 vs 224. D2: 40+80+16=136 vs
160. D3: 40+80+0=120 vs 120.

## 7. Kill bars

- K1 COMPOSITION CORRECTNESS: agree=12/12 (every composite
  answer byte-identical to the all-generic oracle).
- K2 EFFICIENCY: cs=1184 < cg=2272 (composed plans strictly
  fewer fact-checks than all-generic composition).
- K3 LEARNER-NOT-RESEARCHER: (a) word-boundary grep for all 16
  literals
  (601,602,603,607,609,701,702,707,801,802,807,808,809,810,811,812)
  in c3_learn.zag and c3_main.zag returns empty; (b) PLAN-808
  order [RET,VFY,CNT], PLAN-809 order [CNT,RET,VFY], PLAN-812
  order [VFY,RET,CNT], all from identical bindings; (c) BIND
  table shows per-family trial ok/fail counts including the
  failed 811 trials; (d) same 808 plan executes as
  [spec,spec,spec] (S2), [gen,gen,gen] (S5), [gen,gen,spec]
  (S6).
- K4 VERSION SELECTION: S5 vers=[0,1,4] on both queries; S6
  vers=[0,1,5] on both queries; C1 vers=[3,0,5] (per-need
  fallback inside one plan); B0/B1 vers=[5,2,3] (COUNT first,
  specialized).
- K5 RE-DERIVATION: S8 rebuilt PLAN-808 bytes identical to
  pre-clear.
- K6 DECLINE: S7 decline recorded, trials=21 total, no plan
  stored for 810, binary does not crash.
- K7 DETERMINISM: 3/3 runs byte-identical stdout; stderr empty.
- K8 TOOLCHAIN: safebin active for every command; `which
  python3` and `which python` return nothing; zero
  forbidden-executable invocations; all computation pure Zag;
  shell only for znc/binary/git/assembly/byte-verification.
- K9 HYGIENE: zero em/en dash bytes in all lane docs
  (byte-verified).

## 8. Verdict mapping (frozen)

- K1-K6 PASS: THREE-WAY COMPOSITION DEMONSTRATED.
  Learner-driven composition scales to three learner-owned
  procedures: trial-learned bindings, three distinct per-goal
  orders from identical bindings, coverage-driven per-need
  versions across three families, plans persisted and reused,
  unbindable goals declined, answers correct at lower check
  cost. No pipeline, mode, or procedure sequence is
  researcher-supplied.
- K1 FAIL: COMPOSITION INCORRECT. Diagnose whether the defect
  is in trial binding, link plumbing, fan-out/fan-in fill, or
  version selection.
- K2 FAIL: COMPOSITION VACUOUS on efficiency. The claim
  survives on correctness only; record as such.
- K3 FAIL: RESEARCHER CONTAMINATION. The lane is VOID for its
  learner-composition claim.
- K4 FAIL: VERSION SELECTION NOT COVERAGE-DRIVEN. Diagnose.
- K5 FAIL: PLAN NOT RE-DERIVABLE. The plan bytes depend on
  researcher-supplied state; diagnose.
- K6 FAIL: NO PRINCIPLED DECLINE. The learner answers
  unbindable goals or crashes; the trial machinery is not what
  governs binding.
- K7/K8/K9 FAIL: PROCESS-FAIL per standing governance.

## 9. What this establishes (and does not)

Establishes: whether three learner-owned specialized procedures
can be composed by learner-derived structure (trial-learned
bindings over three families, three distinct per-goal assembled
orders, coverage-driven per-need versions, persisted/reused/
re-derivable plans, principled decline), with correctness equal
to the generic oracles at strictly lower check cost.

Does not establish: general DAG/fan-out/fan-in composition
beyond three procedures in chain-with-fan-in form; retirement of
the generic procedures; learner CREATION of a procedure from
scratch (seeds are researcher-supplied by design); learner
invention of the need-tag ontology itself; behavior on
non-chain structures; scaling beyond the tested sizes; whether
the learner can invent the aggop vocabulary itself.

## 10. Deliverables

In this lane: PREREG.md (this file), NAMECHECK.md (Step 0
guard), c3_base.zag, c3_world.zag, c3_learn.zag, c3_main.zag,
c3_build.sh, c3_full.zag (assembled; exactly one `fn main`),
c3_bin, c3_compile.txt, c3_run1/2/3.txt (+ .err), REPORT.md.
