# PREREG: COGOPS-COMPOSE (follow-up to COGNITIVE-OPS-LEARNER C408)

Date: 2026-10-03. Worker: COGOPS-COMPOSE.
Lane: `docs/lab/research-lead/overnight-20260928/cogops_compose/`
Branch: current lane branch (isolated commits; explicit pathspecs only).

## 1. Question

C408 demonstrated that a learner can specialize a researcher-supplied
VERIFY procedure into a learner-owned indexed version, select between
original and revised from a learned coverage record, and revise it for
new experience. Recommended follow-up #1: composition of two
learner-owned procedures.

Question: can the learner own TWO specialized procedures (a specialized
RETRIEVE and a specialized VERIFY) and COMPOSE them, by its own
assembly, to solve tasks that require both? Concretely: given a
composite goal the learner has never been told how to solve, does the
learner discover which of its procedures serves each need (by trial),
assemble them in the order the goal's dependency structure demands
(retrieve-then-verify for one goal type, verify-then-retrieve for
another), bind each need to the specialized or generic version from its
learned coverage, persist the assembled plan in learner state, reuse it,
and decline goals it cannot bind? No researcher-supplied pipeline may
encode "retrieve then verify" or any other assembly.

This tests Micah's priority #5 direction (cognitive-operation bodies
becoming learner-created) one step further: procedures that live in
learner state must also be COMBINED by learner-derived structure. It
does not yet claim general DAG/fan-out/fan-in composition; it is the
two-procedure case, honestly scoped.

## 2. Design

### 2.1 Researcher-supplied generic procedures

`ret_gen(A, rel, obj)` (procedure id 0): returns all subjects s such
that (s, rel, obj) is a fact. Fully generic: linear scan over all facts
(cost = nfacts checks), no index. It is the retrieval oracle.

`vfy_gen(A, C)` (procedure id 1): returns 1 iff every chain step matches
at least one fact, else 0. Fully generic: scans all facts per step
(cost = nsteps * nfacts), no early exit, no index. It is the
verification oracle (same role as in C408).

Neither is a strawman: both are correct on every input. The learner's
contribution is specialization, binding, assembly, and version
selection, never correctness repair.

### 2.2 Learner-owned specialized procedures (both built by the learner)

`ret_spec` (procedure id 2): built by `specialize_ret` from the
learner's retrieve episodes. Inverted index over arena facts restricted
to the retrieve working set (relations the learner actually used in
retrieve episodes): per-relation buckets of fact indices. At query time
it scans only the bucket for the pattern's relation and collects
subjects whose object matches. Returns -1 if the relation is outside
the learned coverage (safety net; the selection logic makes it
unreachable in the passing arms).

`vfy_spec` (procedure id 3): built by `specialize_vfy` from the
learner's verify episodes. Same design as C408: per-relation buckets,
scans only the bucket for each step's relation, -1 if uncovered.

Both bodies (working sets, buckets, provenance records
parent/ep0/ep1/nfacts/revision) live entirely in learner-owned state.

### 2.3 Composite goals (environment-defined; opaque identifiers)

Goals are defined by the world/driver, never by the learner. A goal is a
record: a goal tag, a list of needs, and a list of dependency links.
Each need has an opaque need tag and untyped integer fields. Each link
states that one need's field is filled from another need's input or
output. The learner code contains no goal-tag, need-tag, or relation
literals and no plan sequences; it parses goals generically.

Need tags: 501 = pattern need (served by the RETRIEVE family),
502 = chain need (served by the VERIFY family), 506 = novel need type
(served by nothing; used for the decline control). The learner is never
told these bindings.

Goal 503 ("find"): needs [501-pattern P, 502-chain template T with
subject slots], one fan-out link: T's subject slots are filled per
candidate from the pattern need's output subject list. Correct assembly:
RETRIEVE then VERIFY. Answer: per need in execution order, the appended
output records: [nret, subjects..., npass, passing-subjects...].

Goal 504 ("pivot"): needs [502-chain C (concrete), 501-pattern P' with
its relation field initially empty], one scalar link: P'.rel is filled
from C's first step relation (input-to-input copy). Correct assembly:
VERIFY then RETRIEVE. Answer: [verdict, nret, subjects...].

Goal 505 (decline control): needs [506 (3-field need, never trialed)].
No procedure family accepts its shape; the learner must decline.

### 2.4 Learner-driven composition (the load-bearing mechanism)

The researcher supplies generic machinery only: trial execution,
coverage lookup, topological ordering over links, field copying, plan
storage. The learner supplies all content:

(a) BINDING BY TRIAL. On first encountering a goal with no stored plan,
the learner tries each procedure family on each unbound need tag and
records the outcomes in a learner-state binding table
(tag, bound family, per-family ok/fail counts). RET accepts exactly
2-field needs (its arity); VFY accepts records shaped as chains
(nfields = 1 + 3*nsteps, 1 <= nsteps <= 16). A family that cannot
consume the shape fails the trial. The binding (501 -> RET, 502 -> VFY)
is therefore discovered from observed trial outcomes, not supplied.

(b) ASSEMBLY PER GOAL. From the bindings and the goal's links, the
learner topologically orders the needs and stores the plan
[(need index, need tag, family)...] in learner state. Goal 503
assembles to [RETRIEVE, VERIFY]; goal 504 assembles to [VERIFY,
RETRIEVE] from the SAME bindings. The order is derived per goal; no
pipeline is hardcoded.

(c) VERSION SELECTION PER NEED PER EXECUTION. At execution, each need
is bound to the specialized version iff its (link-filled) parameters
are covered by the corresponding learned coverage set, else the generic
version (C408-style selection, applied per need). The same stored plan
therefore executes as [spec, spec], [gen, gen], or [spec, gen] as
coverage changes.

(d) REUSE AND DECLINE. A stored plan is reloaded for later instances of
the same goal tag (no retrial). A goal whose needs cannot be bound
(505/506) yields NO_PLAN: the learner declines and records it.

### 2.5 Opaque identifiers

World A relations: 301, 302, 303 (8 facts each), distractors 307, 309
(4 facts each), 32 facts. World B relations: 401, 402 (8 facts each),
distractor 407 (8 facts), 24 facts. Subjects/objects are opaque
integers. Goal tags 503, 504, 505; need tags 501, 502, 506. No domain
labels appear in design, code, or docs. RETRIEVE/VERIFY are
experimental descriptions of the procedures under test (as in C408),
not modes in any architecture.

## 3. What "composition" means observably

- C1: the executed procedure sequence for goal 503 is [RET, VFY] and
  for goal 504 is [VFY, RET]; both sequences appear in learner-state
  plan dumps, assembled from identical learned bindings.
- C2: executed versions are the specialized procedures where covered
  (per-need use counters), with per-need fallback to generics where
  uncovered (G1's RETRIEVE, all of S4, S5's VERIFY).
- C3: every composite answer agrees byte-for-byte with an independent
  all-generic oracle composition (10/10).
- C4: no plan exists a priori. First encounter of 503/504 triggers
  trials + assembly (plans_built); repeats reload (plans_loaded);
  goal 505 triggers decline (declines=1).

## 4. How we verify the learner (not the researcher) composed them

(a) Source audit: `cc_learn.zag` (all learner logic) and `cc_main.zag`
(the driver) contain ZERO occurrences of any goal-tag, need-tag, or
relation literal (301, 302, 303, 307, 309, 401, 402, 407, 501, 502, 503,
504, 505, 506), verified by word-boundary grep. Literals appear only in
`cc_world.zag` (environment definitions) and as runtime values in
output. The learner code therefore cannot hardcode bindings, orders, or
a pipeline; it operates on whatever tags the goal records hold.

(b) Order dissociation: plans for 503 and 504 have opposite orders
from the same bindings. A researcher-supplied pipeline produces one
order; the learner produces both, following each goal's links.

(c) Trial record: the binding table shows trial outcomes (ok/fail
counts) for tags 501, 502, and 506; the 506 trials fail for both
families and the learner declines. If bindings were hardcoded, there
would be no trial outcomes and no principled decline.

(d) Version adaptation: the same stored 503 plan executes as
[spec, spec] in S2, [gen, gen] in S4 (coverage cleared / world B), and
[spec, gen] in S5 (retrieve re-specialized on B). Version content
tracks learner state, not researcher code.

(e) Re-derivation: after clearing plans AND bindings, the learner
re-runs trials and rebuilds a byte-identical 503 plan (S7).

On the "trial theater" objection (the arity checks are researcher
code): arity is a procedure signature, i.e. generic machinery, exactly
as vfy_gen taking a chain was generic machinery in C408. What is
learned is the tag-to-family map (in learner state, from observed
outcomes), the per-goal order, and the per-need versions. Evidences
(b) through (e) do not follow from arity alone.

## 5. Build plan (implementation follows this prereg commit)

Files (all new, pure Zag), prefix `cc_`:
- `cc_base.zag`: z_alloc, get32/set32, output helpers (o_app, o_i64,
  o_nl, o_flush; single _zag_raw_syscall write; _zag_print never used
  for dynamic content), world arena, fact store, ret_gen (id 0),
  vfy_gen (id 1). Output idiom follows frozen col_base.zag.
- `cc_world.zag`: setup_worldA (32 facts), setup_worldB (24 facts),
  ret_ep_pat (8 retrieve-episode patterns), vfy_ep_chain (4 verify
  chains), goal constructors mk_goal503_F0/F1/F2,
  mk_goal504_G0/G1, mk_goal503_H0/H1/H2/H3, mk_goal505. All literals
  live here.
- `cc_learn.zag`: ret/vfy working sets, cov_find/has/log/clear per
  region, specialize_ret, specialize_vfy, ret_spec (id 2),
  vfy_spec (id 3), ret_episode, vfy_episode, ret_version,
  vfy_version, goal parsers, topo order, bind_find/bind_new,
  try_family, learn_bindings, plan_find/plan_store, compose,
  execute_plan, clear_plans, clear_bindings. No literals.
- `cc_main.zag`: stages S1A-S7, oracle_503/oracle_504 (independent
  all-generic reference compositions), per-query compose + compare,
  dumps (LSTATE-RET, LSTATE-VFY, BIND, PLAN), summaries. No literals.
- `cc_full.zag`: concatenation of the four (exactly one `fn main`).
- `cc_build.sh`: assemble + compile with the pinned safebin znc.

Learner-state L (16384 bytes) layout:
- RET region: 0: ret_nrel; 4: ret_rel_ids[16]; 68: ret_cnt[16];
  132: ret_fidx[16][64]; 4228: ret_prov_parent (=0); 4232: ep0;
  4236: ep1; 4240: nfacts; 4244: rev.
- VFY region: 4248: vfy_nrel; 4252: vfy_rel_ids[16]; 4316: vfy_cnt[16];
  4380: vfy_fidx[16][64]; 8476: vfy_prov_parent (=1); 8480: ep0;
  8484: ep1; 8488: nfacts; 8492: rev.
- BIND table at 8496: 4 entries x 24 bytes:
  [tag, bound_fam, ok_ret, fail_ret, ok_vfy, fail_vfy].
- PLAN table at 8592: 4 entries x 32 bytes:
  [goal_tag, nneeds, idx0, tag0, fam0, idx1, tag1, fam1].
- Stats at 8720: plans_built, plans_loaded, trials, declines, agree,
  cs, cg, ret_spec_uses, ret_gen_uses, vfy_spec_uses, vfy_gen_uses.

Check counting: K buffer cells: K[0] plan-execution checks (any
version the plan used), K[4] all-generic oracle checks, K[8] trial
checks, K[12] episode scratch. Procedures take (kb, ko) as in C408.

Goal record layout (256-byte buffer): 0: goal_tag; 4: nneeds; needs
from offset 8, each [need_tag, nfields, fields...]; then nlinks;
then links, 28 bytes each:
[kind, dst_need, dst_kind, dst_slot, src_need, src_kind, src_slot].
Link kind 2 = fan-out (chain subject slots filled per candidate from
source need output); kind 1 = scalar copy (dst input field from src
input/output field).

Zag-defect workarounds honored (per AGENTS.md): get32/set32 only, no
`as *i32` slice construction; no _zag_print for dynamic content; no
`!(A && B)` in while conditions; if-nesting at most 3; allocation via
_zag_malloc as *u8 threaded through; no []u8 as *u8 casts.

## 6. Stages and frozen predictions

World A (32 facts): rel 301: (311+i,301,321+i); rel 302:
(311+i,302,322+i); rel 303: (311+i,303,320+i), i=0..7. Distractors:
307: (331+k,307,341+k); 309: (335+k,309,345+k), k=0..3.

World B (24 facts): rel 401: (411+i,401,421+i); rel 402:
(411+i,402,422+i), i=0..7. Distractor 407: (431+k,407,441+k), k=0..7.

S1A RET-LEARN (world A): 4 retrieve episodes (ep 0-3):
 R0 (301,323)->[313]; R1 (302,325)->[314]; R2 (301,321)->[311];
 R3 (302,322)->[311]. Learner logs rels {301,302}.
specialize_ret(ep 0-3). Predicted LSTATE-RET: nrel=2 ids=301,302
cnts=8,8 prov=0,0,3,32 rev=1.

S1B VFY-LEARN (world A): 4 verify episodes (ep 4-7):
 V0 (311,301,321),(311,302,322) v=1
 V1 (312,303,321),(312,301,322) v=1
 V2 (313,302,324),(313,303,322) v=1
 V3 (314,301,324),(314,303,329) v=0
Learner logs rels {301,302,303}. specialize_vfy(ep 4-7). Predicted
LSTATE-VFY: nrel=3 ids=301,302,303 cnts=8,8,8 prov=1,4,7,32 rev=1.

S2 COMPOSE-503 (world A): first query F0 triggers trials then plan
build [(501,RET),(502,VFY)].
 F0: P=(301,323)->[313]; T=(S,302,324),(S,303,322): 313 passes both
   -> answer [1,313,1,313]; vers [spec,spec]; cs=24 (8+16), cg=96.
 F1: P=(302,326)->[315]; T=(S,301,325),(S,303,324): 315 passes
   -> [1,315,1,315]; vers [spec,spec]; cs=24, cg=96.
 F2: P=(301,321)->[311]; T=(S,302,329),(S,301,321): 311 fails step 0
   -> [1,311,0]; vers [spec,spec]; cs=24, cg=96.
Predicted: plans_built=1, plans_loaded=2, trials=4, agree=3.
BIND after S2: (501: fam 0, ok_ret 1, fail_vfy 1),
(502: fam 1, fail_ret 1, ok_vfy 1).
PLAN-503: n=2 [0:501:0] [1:502:1].

S3 COMPOSE-504 (world A): bindings reused; plan build
[(502,VFY),(501,RET)] (opposite order from same bindings).
 G0: C=(311,301,321),(311,302,322) v=1; step0.rel=301;
   P'=(301,325)->[315] -> answer [1,1,315]; vers [spec,spec];
   cs=24 (16+8), cg=96.
 G1: C=(312,303,321),(312,301,322) v=1; step0.rel=303;
   P'=(303,324)->[315] -> [1,1,315]; vers [spec,gen] (303 not in
   ret coverage {301,302}); cs=48 (16+32), cg=96.
Predicted: plans_built=2, plans_loaded=3, agree=5.
PLAN-504: n=2 [0:502:1] [1:501:0].

S4 SHIFT-B (world B; ret coverage cleared first): 503 queries; plan
reloaded; versions per execution from coverage.
 H0: P=(401,423)->[413]; T=(S,402,424),(S,401,423): 413 passes
   -> [1,413,1,413]; vers [gen,gen]; cs=72, cg=72.
 H1: P=(402,427)->[416]; T=(S,401,426),(S,402,427): 416 passes
   -> [1,416,1,416]; vers [gen,gen]; cs=72, cg=72.
Predicted: plans_loaded=5, agree=7.

S5 REVISE-B: 4 retrieve episodes on B (ep 8-11):
 (401,421)->[411]; (402,428)->[417]; (401,425)->[415];
 (402,422)->[411]. specialize_ret(ep 8-11). Predicted LSTATE-RET:
 nrel=2 ids=401,402 cnts=8,8 prov=0,8,11,24 rev=2. (vfy untouched.)
 H2: P=(401,424)->[414]; T=(S,402,425),(S,401,424): 414 passes
   -> [1,414,1,414]; vers [spec,gen]; cs=56 (8+48), cg=72.
 H3: P=(402,429)->[418]; T=(S,401,428),(S,402,422): 418 fails
   -> [1,418,0]; vers [spec,gen]; cs=56, cg=72.
Predicted: plans_loaded=7, agree=9.

S6 DECLINE-505: goal 505, need 506 (3 fields [9,0,0]). Trials: RET
fails (3 fields, not 2), VFY fails (nsteps=9 needs 28 fields, has 3).
No binding; compose returns NO_PLAN; decline recorded.
Predicted: declines=1, trials=6 total, BIND has 506 entry fam=-1.

S7 REDERIVE: dump PLAN-503 bytes; clear plans AND bindings; recompose
an H2-identical 503 query on B: trials re-run (4), plan rebuilt;
dumped bytes identical to pre-clear. Execute: vers [spec,gen],
answer [1,414,1,414], cs=56, cg=72, agree=10.
Predicted: plans_built=3, trials=10, rederive_match=1.

Frozen totals: agree=10/10; plans_built=3; plans_loaded=7; trials=10;
declines=1; cs=400 (24*4+48+72*2+56*2); cg=768 (96*5+72*4); 400 < 768.

Derivation notes (so the numbers are checkable): ret_spec costs one
bucket scan (8 checks); vfy_spec costs 8 per chain step (no early
exit); ret_gen costs nfacts (32 on A, 24 on B); vfy_gen costs
nsteps*nfacts (64 on A, 48 on B for 2-step chains). F0: 8+16=24 vs
32+64=96. G0: 16+8=24 vs 96. G1: 16+32=48 vs 96. H0/H1: 24+48=72 vs
72. H2/H3: 8+48=56 vs 72.

## 7. Kill bars

- K1 COMPOSITION CORRECTNESS: agree=10/10 (every composite answer
  byte-identical to the all-generic oracle).
- K2 EFFICIENCY: cs=400 < cg=768 (composed plan strictly fewer
  fact-checks than all-generic composition).
- K3 LEARNER-NOT-RESEARCHER: (a) word-boundary grep for all 14
  literals (301,302,303,307,309,401,402,407,501,502,503,504,505,506)
  in cc_learn.zag and cc_main.zag returns empty; (b) PLAN-503 order
  [RET,VFY] vs PLAN-504 order [VFY,RET] from identical bindings;
  (c) BIND table shows trial ok/fail counts including the failed
  506 trials; (d) same 503 plan executes as [spec,spec] (S2),
  [gen,gen] (S4), [spec,gen] (S5).
- K4 VERSION SELECTION: S4 vers=[gen,gen] on both queries; S5
  vers=[spec,gen] on both queries; G1 vers=[spec,gen] (per-need
  fallback inside one plan).
- K5 RE-DERIVATION: S7 rebuilt PLAN-503 bytes identical to pre-clear.
- K6 DECLINE: S6 decline recorded, trials=10 total, no plan stored
  for 505, binary does not crash.
- K7 DETERMINISM: 3/3 runs byte-identical stdout; stderr empty.
- K8 TOOLCHAIN: safebin active for every command; `which python3`
  and `which python` return nothing; zero forbidden-executable
  invocations; all computation pure Zag; shell only for
  znc/binary/git/assembly/byte-verification.
- K9 HYGIENE: zero em/en dash bytes in all lane docs (byte-verified).

## 8. Verdict mapping (frozen)

- K1-K6 PASS: COMPOSITION DEMONSTRATED. Two learner-owned procedures
  (specialized RETRIEVE + specialized VERIFY) are composed by
  learner-assembled plans: bindings discovered by trial (K3a, K3c),
  per-goal order derived from goal structure (K3b), per-need versions
  from learned coverage (K4), plans persisted and reused (K3d, K5),
  unbindable goals declined (K6), answers correct (K1) at lower check
  cost (K2).
- K1 FAIL: COMPOSITION INCORRECT. Diagnose whether the defect is in
  trial binding, link plumbing, fan-out fill, or version selection.
- K2 FAIL: COMPOSITION VACUOUS on efficiency. The claim survives on
  correctness only; record as such.
- K3 FAIL: RESEARCHER CONTAMINATION. The lane is VOID for its
  learner-composition claim.
- K4 FAIL: VERSION SELECTION NOT COVERAGE-DRIVEN. Diagnose.
- K5 FAIL: PLAN NOT RE-DERIVABLE. The plan bytes depend on
  researcher-supplied state; diagnose.
- K6 FAIL: NO PRINCIPLED DECLINE. The learner answers unbindable
  goals or crashes; the trial machinery is not what governs binding.
- K7/K8/K9 FAIL: PROCESS-FAIL per standing governance.

## 9. What this establishes (and does not)

Establishes: whether two learner-owned specialized procedures can be
composed by learner-derived structure (trial-learned bindings,
per-goal assembled order, coverage-driven per-need versions,
persisted/reused/re-derivable plans, principled decline), with
correctness equal to the generic oracles at strictly lower check cost.

Does not establish: general DAG/fan-out/fan-in composition beyond two
procedures; retirement of the generic procedures; learner CREATION of
a procedure from scratch (seeds are researcher-supplied by design);
behavior on non-chain structures; scaling beyond the tested sizes;
whether the learner can invent the need-tag ontology itself.

## 10. Deliverables

In this lane: PREREG.md (this file), NAMECHECK.md (Step 0 guard),
cc_base.zag, cc_world.zag, cc_learn.zag, cc_main.zag, cc_full.zag
(assembled), cc_build.sh, cc_bin, cc_compile.txt, cc_run1/2/3.txt
(+ .err), REPORT.md.
