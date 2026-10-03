# PREREG: COGOPS-DIAMOND (follow-up to COGOPS-3WAY C422)

Date: 2026-10-03. Worker: COGOPS-DIAMOND.
Lane: `docs/lab/research-lead/overnight-20260928/cogops_diamond/`
Branch: current lane branch (isolated commits; explicit pathspecs only).

## 1. Question

C422 (COGOPS-3WAY) demonstrated learner-driven composition of three
learner-owned procedures across three forced chain orders. Its honest
boundary: "no diamond, no cycles, no multi-input fan-in beyond the
count aggregate."

Question: does the same learner composition machinery handle a
DIAMOND (fan-out then fan-in), or is it limited to chains? A diamond
needs four nodes: one source, two branches, one sink. The test: the
learner must assemble and execute a goal where one RETRIEVE output
fans out to two VERIFY branches whose outputs fan in to one COUNT,
using the same trial-learned bindings, topo assembly, and
coverage-driven version selection as C422. No researcher-supplied
diamond handler may exist: the only mechanism change from C422 is a
generic generalization of the fan-in link semantics (Section 2.4),
which behaves identically on chains.

## 2. Design

### 2.1 Machinery carried over from C422 (unchanged logic)

`ret_gen` (id 0), `vfy_gen` (id 1), `cnt_gen` (id 4): researcher-supplied
generic procedures, oracles and fallbacks. Learner-owned specialized
procedures `ret_spec` (id 2), `vfy_spec` (id 3), `cnt_spec` (id 5),
built from episodes with working sets, buckets, and provenance in
learner state L. Binding by trial over three families (shape
signatures as C422), Kahn topo order over goal links, plan persist /
reuse / re-derive, per-need version selection from learned coverage,
principled decline of unbindable goals.

### 2.2 The diamond goal (environment-defined; opaque identifiers)

Goal 813 (world A), 4 needs, 4 links:
- need0: tag 801, [601, 621] -> RETRIEVE -> [611].
- need1: tag 802, template [2, (0,602,622), (0,603,620)];
  kind-2 link (need0 -> need1): VERIFY 611 -> passes -> P1 = [611].
  (Step-0 (611,602,622): 622 is among 611's 602-objects {622,632};
  step-1 (611,603,620): 620 is among 611's 603-objects {620,630}.)
- need2: tag 802, template [2, (0,602,629), (0,601,621)];
  kind-2 link (need0 -> need2): VERIFY 611 -> fails step 0
  (629 not among 611's 602-objects {622,632}) -> P2 = [].
- need3: tag 807, [603, 1, 0];
  kind-3 links (need1 -> need3) and (need2 -> need3):
  COUNT distinct objects over P1 ++ P2 = [611] via 603
  -> {621,631} -> 2.

Predicted plan (Kahn, highest-index zero-indegree node per round):
[0:801:0] [2:802:1] [1:802:1] [3:807:2]. Predicted execution:
vers = [2,3,3,5]. Answer records in plan order:
need0 [1,611]; need2 [0]; need1 [1,611]; need3 [1,2]:
ans = 7:1,611,0,1,611,1,2. cs = 16+32+32+16 = 96;
cg = 56+112+112+56 = 336.

Goal 814 (world A), convergent variant, 4 needs, 4 links:
- need0: tag 801, [601, 621] -> [611].
- need1: tag 802, template [2, (0,601,621), (0,602,622)];
  kind-2 (need0 -> need1): 611 passes -> P1 = [611].
- need2: tag 802, template [2, (0,603,620), (0,601,631)];
  kind-2 (need0 -> need2): 611 passes both ((611,603,620) and
  (611,601,631), 631 among 611's 601-objects {621,631}) -> P2 = [611].
- need3: tag 807, [601, 1, 0];
  kind-3 (need1 -> need3), kind-3 (need2 -> need3):
  COUNT over [611] ++ [611] via 601 -> distinct {621,631} -> 2.

Predicted plan: [0:801:0] [2:802:1] [1:802:1] [3:807:2].
vers = [2,3,3,5]. ans = 8:1,611,1,611,1,611,1,2.
cs = 16+32+32+32 = 112; cg = 56+112+112+112 = 392.

Goal 815 (world B diamond, mirrors 813's divergent shape):
- need0: tag 801, [701, 723] -> [713].
- need1: tag 802, template [2, (0,702,724), (0,701,723)];
  kind-2 (need0 -> need1): 713 passes -> P1 = [713].
- need2: tag 802, template [2, (0,702,729), (0,701,723)];
  kind-2 (need0 -> need2): 713 fails step 0 -> P2 = [].
- need3: tag 807, [701, 1, 0];
  kind-3 (need1 -> need3), kind-3 (need2 -> need3):
  COUNT over [713] via 701 -> {723,733} -> 2.

Predicted plan: [0:801:0] [2:802:1] [1:802:1] [3:807:2].
All-generic versions (coverages cleared): vers = [0,1,1,4],
ans = 7:1,713,0,1,713,1,2, cs = 240, cg = 240.
After count re-specialized on B: vers = [0,1,1,5],
cs = 40+80+80+16 = 216, cg = 240.

Goal 808 A0 (chain regression, world A, same as C422 A0):
need0 [601,623]->[613]; need1 T=(S,602,624),(S,603,622): 613
passes; need2 [601,1,0] over [613] -> 2.
Predicted: plan [0:801:0] [1:802:1] [2:807:2], st=2,
vers = [2,3,5], ans = 6:1,613,1,613,1,2, cs = 64, cg = 224.

Goal 810 (decline control, as C422): need 811 [9,0,0]; all
families refuse; decline.

Need tags 801/802/807/811 are REUSED from C422: the same
bindings must serve diamonds and chains, which is the shape
dissociation claim. No new need tags, no new procedure ids, no
new link kinds.

### 2.3 Learner-state layout (C422 layout, plan table widened)

RET/VFY/CNT regions and BIND table (at 12744) unchanged.
PLAN table at 13000: 4 entries x 56 bytes (was 44):
[goal_tag, nneeds, idx0, tag0, fam0, idx1, tag1, fam1,
 idx2, tag2, fam2, idx3, tag3, fam3] = 14 ints. Capacity only.
Stats block moved from 13176 to 13224 (13 ints, same order):
plans_built, plans_loaded, trials, declines, agree, cs, cg,
ret_spec_uses, ret_gen_uses, vfy_spec_uses, vfy_gen_uses,
cnt_spec_uses, cnt_gen_uses.

### 2.4 The one mechanism change (preregistered generalization)

`apply_kind3` changes from "first incoming kind-3 link wins" to
"subjects from ALL incoming kind-3 links concatenate in
goal-record link order into the destination need's subject
list". This is the generic fan-in generalization of the link
kind C422 already defined as "fan-in over a variable-size
list". On a chain (single kind-3 source) the behavior is
byte-identical to C422; on a diamond (two sources) it is the
unique compositional reading. It is NOT a diamond handler: it
contains no goal-shape test, no branch count, no goal tag; it
applies uniformly to any DAG. The S4 chain regression exists to
verify the generalization did not alter chain behavior.

### 2.5 Opaque identifiers

Worlds A/B identical to C422 (56 / 40 facts). Goal tags 813,
814, 815 (new), 808, 810 (reused). Need tags 801, 802, 807,
811 (reused). No domain labels anywhere. RETRIEVE/VERIFY/COUNT
are experimental descriptions, not modes.

### 2.6 Amendment A1 (pre-implementation, 2026-10-03)

Caught before any implementation commit: the as-committed Section 2.2
listed goal 813's need1 step-1 object as 621 and goal 814's need2
step-0 object as 621. World A's 603-facts are (611+i,603,620+i) and
(611+i,603,630+i), so 611's 603-objects are {620,630}: 621 matches
nothing and both templates would fail, turning 813 into a both-fail
diamond and 814 into a divergent one instead of the intended
divergent / convergent pair. Corrected above to 620 in both places;
all downstream frozen predictions (answers, check costs, totals) are
unchanged because they were computed for the intended semantics.
Verified by hand against the world fact listings before re-freeze.
The original lines are preserved in git history (commit f2647ad8c).

## 3. What "diamond composition" means observably

- C1: the diamond goals assemble to 4-step plans with the
  predicted topo order [0,2,1,3]; the plan dumps show two
  kind-2 fan-out links and two kind-3 fan-in links honored.
- C2: every composite answer (diamonds + chain regression)
  agrees byte-for-byte with an independent all-generic oracle
  composition (6/6).
- C3: the divergent diamond (813) correctly fans in an empty
  branch (P2 = [] contributes nothing); the convergent diamond
  (814) correctly dedups across branches (concat [611,611]
  counts 2).
- C4: the same bindings produce diamond plans (813, 814, 815)
  and a chain plan (808): shape dissociation from identical
  bindings.
- C5: no plan exists a priori; 815 re-derives byte-identical
  after plans + bindings are wiped; 810 declines.

## 4. How we verify the learner (not the researcher) composed it

(a) Source audit: `c4_learn.zag` and `c4_main.zag` contain ZERO
occurrences of any of the 17 identifiers
(601,602,603,607,609,701,702,707,801,802,807,808,810,811,813,814,815),
verified by word-boundary grep. Goal constructors are named
mk_goal813_E0 etc.; tag digits inside names are not
word-boundary matches (C422 convention).

(b) No diamond handler: the only link-semantics change is the
multi-source accumulation in apply_kind3, which is exercised on
a chain (S4) with identical behavior to C422 and on diamonds
with the natural fan-in reading. The assembly path
(learn_bindings, topo, plan_new, execute_plan) is the C422
logic with widened records.

(c) Trial record: BIND shows per-family ok/fail counts for
801/802/807 and the failed 811 trials (fam = -1).

(d) Version adaptation: 815 executes as [0,1,1,4] with
coverages cleared and [0,1,1,5] after count re-specialization;
813/814 execute as [2,3,3,5].

## 5. Build plan (implementation follows this prereg commit)

Files (all new, pure Zag), prefix `c4_`, in
`docs/lab/research-lead/overnight-20260928/cogops_diamond/`:
- `c4_base.zag`: byte-copy of C422's c3_base.zag.
- `c4_world.zag`: C422's c3_world.zag + mk_goal813_E0,
  mk_goal814_E1, mk_goal815_B0 (mk_goal808_A0 and mk_goal810
  carried over unchanged).
- `c4_learn.zag`: C422's c3_learn.zag + Section 2.3/2.4
  deltas: 56-byte plan entries, stats at 13224,
  multi-source apply_kind3, compose buffers W=320 / OUTS=640 /
  SUBL=512, vbuf count word at offset 16 (versions at 0,4,8,12).
- `c4_main.zag`: stages S1A..S8, oracle_dia (independent
  all-generic diamond reference; records emitted in the
  predicted plan order [need0, need2, need1, need3], count over
  link-order concatenation), oracle_808 (as C422), per-query
  compose + compare, dumps, summaries. No literals.
- `c4_full.zag`: concatenation of the four (exactly one
  `fn main`).
- `c4_build.sh`: assemble + compile with the pinned safebin znc.

Zag-defect workarounds honored (per AGENTS.md): get32/set32
only, no `as *i32` slice construction; no _zag_print for dynamic
content; no `!(A && B)` in while conditions; if-nesting at most
3; allocation via _zag_malloc as *u8 threaded through; no
[]u8 as *u8 casts.

## 6. Stages and frozen predictions

Worlds identical to C422.

S1A RET-LEARN (world A): 4 retrieve episodes (ep 0-3, same as
C422). specialize_ret(ep 0-3). Predicted LSTATE-RET: nrel=2
ids=601,602 cnts=16,16 prov=0,0,3,56 rev=1.

S1B VFY-LEARN (world A): 4 verify episodes (ep 4-7, same as
C422). specialize_vfy(ep 4-7). Predicted LSTATE-VFY: nrel=3
ids=601,602,603 cnts=16,16,16 prov=1,4,7,56 rev=1.

S1C CNT-LEARN (world A): 4 count episodes (ep 8-11, same as
C422). specialize_cnt(ep 8-11). Predicted LSTATE-CNT: nrel=3
ids=601,602,603 cnts=16,16,16 prov=4,8,11,56 rev=1.

S2 DIAMOND-DIVERGE (world A): goal 813 query E0. First query
triggers trials (9), plan built [0:801:0] [2:802:1] [1:802:1]
[3:807:2]. Predicted: st=2, vers=2,3,3,5,
ans=7:1,611,0,1,611,1,2, cs=96, cg=336, agree=1.
plans_built=1, trials=9.
BIND after S2: (801: fam 0, ok0 1, f1 1, f2 1),
(802: fam 1, f0 1, ok1 1, f2 1),
(807: fam 2, f0 1, f1 1, ok2 1).

S3 DIAMOND-CONVERGE (world A): goal 814 query E1. Bindings
reused; plan built. Predicted: st=2, vers=2,3,3,5,
ans=8:1,611,1,611,1,611,1,2, cs=112, cg=392, agree=1.
plans_built=2.

S4 CHAIN-REGRESS (world A): goal 808 A0 query R0. Bindings
reused; plan built [0:801:0] [1:802:1] [2:807:2]. Predicted:
st=2, vers=2,3,5, ans=6:1,613,1,613,1,2, cs=64, cg=224,
agree=1. plans_built=3.

S5 DIAMOND-SHIFTB (world B; all coverages cleared): goal 815
query B0. Plan built; versions all generic. Predicted: st=2,
vers=0,1,1,4, ans=7:1,713,0,1,713,1,2, cs=240, cg=240,
agree=1. plans_built=4.

S6 DIAMOND-REVISEB: 4 count episodes on B (ep 12-15, same
patterns as C422). specialize_cnt(ep 12-15). Predicted
LSTATE-CNT: nrel=2 ids=701,702 cnts=16,16 prov=4,12,15,40
rev=2. Goal 815 query B1: plan reloaded. Predicted: st=1,
vers=0,1,1,5, ans=7:1,713,0,1,713,1,2, cs=216, cg=240,
agree=1. plans_loaded=1.

S7 DECLINE-NOVEL: goal 810 query X. Trials: all three
families refuse need 811. Predicted: decline=1, trials=21
total, BIND has 811 entry fam=-1 with f0=f1=f2=1, no plan
stored for 810.

S8 REDERIVE: dump first plan bytes (14 ints); clear plans AND
bindings; rebuild goal 815 on B (D2-analog query S8): trials
re-run (9), plan rebuilt; dumped bytes identical to pre-clear.
Predicted: st=2, vers=0,1,1,5,
ans=7:1,713,0,1,713,1,2, cs=216, cg=240, agree=1,
plans_built=5, trials=21, rederive_match=1.

Frozen totals: agree=6/6; plans_built=5; plans_loaded=1;
trials=21; declines=1; cs=944; cg=1672; 944 < 1672 (1.77x).
Procedure uses: ret_spec 3, ret_gen 3, vfy_spec 5, vfy_gen 6,
cnt_spec 5, cnt_gen 1.

Derivation notes: ret_spec = one bucket scan (16 on A and B);
vfy_spec = 16 per chain step (no early exit); cnt_spec = 16
per subject; ret_gen = nfacts (56 A / 40 B);
vfy_gen = nsteps * nfacts (112 A / 80 B for 2-step chains);
cnt_gen = nsubs * nfacts.
E0: 16+32+32+16=96 vs 56+112+112+56=336.
E1: 16+32+32+32=112 vs 56+112+112+112=392.
R0: 16+32+16=64 vs 56+112+56=224.
B0: 40+80+80+40=240 vs 240.
B1/S8: 40+80+80+16=216 vs 240.

## 7. Kill bars

- K1 DIAMOND CORRECTNESS: agree=6/6 (every diamond and chain
  answer byte-identical to the all-generic oracle).
- K2 EFFICIENCY: cs=944 < cg=1672 (composed plans strictly
  fewer fact-checks than all-generic composition).
- K3 LEARNER-NOT-RESEARCHER: (a) word-boundary grep for all 17
  identifiers in c4_learn.zag and c4_main.zag returns empty;
  (b) no diamond handler: the only link-semantics delta is the
  multi-source apply_kind3, which S4 exercises on a chain with
  C422-identical behavior; (c) BIND table shows per-family
  trial ok/fail counts including the failed 811 trials;
  (d) same bindings produce diamond plans (813, 814, 815) and a
  chain plan (808).
- K4 DIAMOND EXECUTION: E0 ans=7:1,611,0,1,611,1,2
  vers=[2,3,3,5] (empty branch fans in cleanly); E1
  ans=8:1,611,1,611,1,611,1,2 vers=[2,3,3,5] (cross-branch
  dedup correct); plan dumps show the [0,2,1,3] topo order.
- K5 REUSE AND RE-DERIVATION: S6 plans_loaded=1; S8 rebuilt
  815 plan bytes identical to pre-clear (rederive_match=1).
- K6 DECLINE: S7 decline recorded, trials=21 total, no plan
  stored for 810, binary does not crash.
- K7 DETERMINISM: 3/3 runs byte-identical stdout; stderr empty.
- K8 TOOLCHAIN: safebin active for every command;
  `which python3` and `which python` return nothing; zero
  forbidden-executable invocations; all computation pure Zag;
  shell only for znc/binary/git/assembly/byte-verification.
- K9 HYGIENE: zero em/en dash bytes in all lane docs
  (byte-verified).

## 8. Verdict mapping (frozen)

- K1-K6 PASS: DIAMOND COMPOSITION DEMONSTRATED.
  Learner-driven composition handles fan-out/fan-in: the same
  trial-learned bindings, topo assembly, and coverage-driven
  versions that composed chains now assemble diamond plans
  (source, two branches, sink) with divergent and convergent
  branches, correct empty-branch fan-in, cross-branch dedup,
  chain regression intact, plans persisted/reused/re-derived,
  unbindable goals declined, answers correct at lower check
  cost. No diamond handler is researcher-supplied.
- K1 FAIL: DIAMOND COMPOSITION INCORRECT. Diagnose whether the
  defect is in multi-source fan-in, topo order over the DAG,
  branch plumbing, or version selection.
- K2 FAIL: COMPOSITION VACUOUS on efficiency. The claim
  survives on correctness only; record as such.
- K3 FAIL: RESEARCHER CONTAMINATION. The lane is VOID for its
  learner-composition claim.
- K4 FAIL: DIAMOND EXECUTION WRONG. The plan assembles but a
  branch result is mishandled; diagnose.
- K5 FAIL: PLAN NOT RE-DERIVABLE. The plan bytes depend on
  researcher-supplied state; diagnose.
- K6 FAIL: NO PRINCIPLED DECLINE. The learner answers
  unbindable goals or crashes; the trial machinery is not what
  governs binding.
- K7/K8/K9 FAIL: PROCESS-FAIL per standing governance.

## 9. What this establishes (and does not)

Establishes: whether learner-driven composition of
learner-owned procedures reaches the diamond (fan-out/fan-in)
generality GEN achieved: same bindings assemble diamond and
chain plans, divergent and convergent branches, empty-branch
fan-in, cross-branch dedup, correctness equal to generic
oracles at lower check cost.

Does not establish: cycles (a DAG topo cannot order them);
multi-input fan-in beyond the count aggregate; 4+ procedures;
retirement of the generic procedures; learner CREATION of a
procedure from scratch; learner invention of the need-tag
ontology; scaling beyond the tested sizes; whether the learner
could invent the multi-source link semantics itself (the
generalization is researcher-supplied by design; the learner's
contribution is assembling and executing diamonds with it).

## 10. Deliverables

In this lane: PREREG.md (this file), NAMECHECK.md (Step 0
guard), c4_base.zag, c4_world.zag, c4_learn.zag, c4_main.zag,
c4_build.sh, c4_full.zag (assembled; exactly one `fn main`),
c4_bin, c4_compile.txt, c4_run1/2/3.txt (+ .err), REPORT.md.
