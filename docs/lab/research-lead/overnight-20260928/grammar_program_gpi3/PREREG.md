# PREREG: GPI-3 Conjunctive Constraint-Family Generality Probe

Status: PREREG-FROZEN. No implementation exists at this commit.
Scope: `docs/lab/research-lead/overnight-20260928/grammar_program_gpi3/` only.
Worker: GPI-3 Generality Probe Worker (subagent, 2026-10-02).
Parent mandate: L2 ADAPTIVE REUSE is the top priority; L3 novel
intermediate form is the main architecture target. Composition
X+Y->Z without paired examples is a core frontier question.

## 1. What is being tested

GPI-1 (ledger C303) proved the learner creates a construction-plan
intermediate (SEQ/PAIR/NEST vocabulary) mediating a learned
single-delimiter DEPTH-BUDGET constraint and an executable
MAP-chain program, then reuses and revises it; honest verdict
L2-COMPLETE, L3 not claimed, C0-C failed (single constraint
family). GPI-2 (ledger C311) proved the SAME machinery, with the
node vocabulary FROZEN, generalizes to a structurally different
family, MULTI-TYPE STACK-DISCIPLINE WELL-FORMEDNESS, with no depth
budget; honest verdict L2-COMPLETE, GENERALIZES, C0-C partial (two
constraint dimensions, no adversary).

GPI-3 asks the next load-bearing question: does the fixed
vocabulary plus the plan machinery handle the CONJUNCTION of the
two previously learned constraint dimensions, or does it break?
The family: MULTI-TYPE STACK DISCIPLINE AND DEPTH BUDGET
SIMULTANEOUSLY. The learner must extract BOTH dimensions from one
probe campaign (type alphabet plus matching rule AND scalar depth
bound, the depth probes built from the LEARNED type bindings so
the two extractions are sequenced, not independent), build one
plan whose per-node bindings carry the type dimension while the
assembler-side check enforces the budget dimension, assemble and
execute, and obtain world acceptance. Then: reuse the core on a
second target, REVISE under a world change to the budget
dimension (Dmax 3->2, sharper than GPI-1: the old program is now
REJECTED by the new world, not merely insufficient), show the
no-plan direct path fails, show a fresh learner fails, and show
wrong constraints refused on EACH dimension separately.

THE LOAD-BEARING QUESTION: does generality COMPOSE? GPI-2 showed
dimension B works with the vocabulary frozen. GPI-1 showed
dimension A works. GPI-3 tests whether A AND B, learned together
and enforced together, compose without interference and without
any vocabulary change. BOTH outcomes are publishable.
GENERALIZES: the intermediate machinery now spans the conjunction
of the two dimensions, which is compositional generality
(X+Y->Z where X and Y are the two previously learned constraint
dimensions). BREAKS: the report characterizes EXACTLY which
enforcement piece or builder assumption fails under conjunction,
with a minimal failing case; that characterization IS the result
and precisely states the composition gap. The family is not
contorted to fit the vocabulary, and the vocabulary is not
extended to fit the family.

What is NOT tested: exact reuse of grammar to construction (done);
a third independent family (not this probe); revision under a
type-dimension change (the revise arm changes only the budget
dimension, as in GPI-1); invention of a new node kind
(explicitly out of scope and forbidden here); whether the learner
can DERIVE the decomposition strategy from failure (that is the
L3 strategy-invention probe, a different lane).

## 2. The chosen family and the frozen structural-difference bar (K0)

Family: CONJUNCTIVE WELL-FORMEDNESS. World truth: three delimiter
types, (40,41) `()`, (91,93) `[]`, (123,125) `{}`, plus a max
nesting depth Dmax = 3. w_check accepts a string iff every byte is
one of the six delimiter bytes, the string is balanced, EVERY
CLOSE MATCHES THE MOST RECENT OPEN TYPE, AND the maximum nesting
depth is <= Dmax.

K0 STRUCTURAL-DIFFERENCE (frozen at prereg; judged against this
section): the run family must be exactly the one above. It is
structurally different from GPI-1 and GPI-2 by CONJUNCTION, not
parameters:

(a) Constraint kind. GPI-1 enforced a single RESOURCE BUDGET
(scalar max depth). GPI-2 enforced a single SYMBOLIC
CORRESPONDENCE (type matching, no budget). GPI-3 enforces BOTH
simultaneously: a string must satisfy the budget AND the
correspondence. No choice of GPI-1 parameters expresses type
matching; no choice of GPI-2 parameters expresses a depth
budget; and neither single-dimension family expresses their
conjunction. The new dimension probed is COMPOSITIONALITY of
constraint enforcement, which neither prior probe tested.

(b) Which plan machinery does the work. In GPI-1 the load-bearing
machinery was the assembler-side budget check (`depthlv <=
Dmax`) with fixed token identity. In GPI-2 the load-bearing
machinery was per-node (tokL,tokR) bindings plus tree-structured
matching, and the budget check was DROPPED as having nothing to
enforce. In GPI-3 BOTH enforcement mechanisms operate at once on
the same plan: per-node bindings plus tree structure carry the
type dimension, and the assembler-side `depthlv <= Dmax` check
is RESTORED because the family has a budget. The probe tests
whether the two mechanisms compose without interference. A
different COMBINATION of the frozen machinery carries the new
dimension.

(c) Extraction task. GPI-1 extracted a scalar bound plus a binary
order. GPI-2 extracted a partition (3 types from 30 ordered
probes) plus a relational rule. GPI-3 must extract BOTH answers
from one campaign: the partition plus rule (GPI-2's task) AND
the scalar bound (GPI-1's task), where the depth probes are
built from the LEARNED type bindings (nested single-type
strings, which are type-valid at any depth and therefore
isolate the budget dimension). A single-dimension extractor
cannot represent this answer; the extraction is sequenced
(type first, then depth through the learned types).

Excluded as not-structurally-different (and not run): changing
the delimiter bytes, changing Dmax alone, a single-type
variant, or running the two dimensions in separate experiments.
If the run drops either dimension (e.g. the assembler check is
omitted, or the type probes are skipped), K0 FAILS.

## 3. Frozen hypothesis and preregistered break conditions

Hypothesis (frozen): GENERALIZES. Reasons, stated before the run:

1. The two enforcement mechanisms are orthogonal in the frozen
   design: per-node (tokL,tokR) bindings plus tree structure
   determine WHICH bytes are emitted at each position (the type
   dimension), while the assembler-side `depthlv <= Dmax` check
   constrains HOW DEEP the NEST chain may go (the budget
   dimension). Neither mechanism reads or writes the other's
   load-bearing field, so they should compose without
   interference.
2. The depth probes isolate the budget dimension cleanly:
   nested strings of a single learned type are type-valid at
   every depth, so probe outcomes vary only with Dmax. The
   type probes are unaffected by the budget because all probe
   strings are depth <= 2 < Dmax.
3. The builder's "nested core plus flat tail" decomposition is
   unchanged; the required depth of a target is its pattern
   length, checked against the learned Dmax before building.

Preregistered break conditions (any one yields verdict
BREAKS-WITH-CHARACTERIZATION, never a vocabulary extension):

- B1: plan_build cannot produce a plan for a well-posed target
  (P, pattern, flat type, depth within Dmax) using only kinds
  0,1,2 that assembles to a world-accepted, pattern-matching
  program satisfying BOTH dimensions.
- B2: the two enforcement mechanisms interfere (e.g. the
  restored depth check blocks a type-valid plan, or per-node
  bindings cannot be carried faithfully alongside the budget
  check within the frozen node/program formats).
- B3: a plan the builder produces is world-rejected on either
  dimension (type mismatch or depth overrun).

If any break fires, the report names the exact failing
machinery piece or builder assumption, gives the MINIMAL
failing case (smallest target that breaks), and states the
composition gap. The bars below are never weakened to avoid a
break verdict.

## 4. Domain and scenario (all ids frozen)

World truth (experiment side only; learner sees only w_check
outcomes): types T0=(40,41), T1=(91,93), T2=(123,125); Dmax = 3
(driver-settable via w_dmax_set for the revise arm only).
w_check: 1 iff every byte is in {40,41,91,93,123,125}, the string
is balanced, every close matches the most recent open's type
(stack discipline), and max depth <= Dmax (w[0]).

X (learned in phase 0 by l_extract from probes, never from
literals):
- (CONSTR=70, 80+2t, Lt), (CONSTR=70, 81+2t, Rt) for t=0,1,2:
  the three type bindings in learner discovery order. Expected
  values (from the fixed scrambled teaching order, Section 7):
  (40,41), (91,93), (123,125).
- (CONSTR=70, 86, MATCH): 1 iff the rule probes confirm
  most-recent-open matching. Expected 1.
- (CONSTR=70, 87, D): the learned depth bound. Expected 3 at
  epoch 1, 2 at epoch 2 (after the world change).
  NOTE: rel 87 is used (not 82) because 82 is T1's open
  binding in the GPI-2-compatible schema; the schema keeps all
  GPI-2 rel assignments and adds 87 for the budget dimension.
- Pair-probe facts (71,97,code) accept / (71,98,code) reject for
  the 30 ordered char-pair probes, code = i*6+j over the six
  observed chars. Expected: 3 accepts, 27 rejects.
- Rule-probe facts (71,95,k) accept / (71,96,k) reject, k=0..4.
  Expected: accepts k=1,3; rejects k=0,2,4.
- Depth-probe facts (71,93,d) accept / (71,94,d) reject for
  nested single-type probes d=0..5 built from the LEARNED
  type-0 bindings. Expected at epoch 1: accepts d=0..3,
  rejects d=4,5. Expected at epoch 2 (Dmax=2): accepts d=0..2,
  rejects d=3,4,5.

Primitive MAPs (preexisting, no construction plan): six
single-emit MAPs taught in fixed order with rels 90..95:
MAP 0..5, even rel = open slot, odd rel = close slot. The MAPs
are generic emit slots; token bytes come from the program
record's per-type table (filled at assemble time from learned
facts). Max relseq length is 1 before, during, and after every
arm: no MAP ever encodes a multi-step construction.

Targets (given as goals, not paired examples):
- T1: P = 4 pairs, nested pattern opens [123,91,40] (`{` outer,
  `[` middle, `(` inner), flat type open 40 (`()` tail),
  required depth 3 = Dmax (boundary). Canonical program bytes:
  123,91,40,41,93,125,40,41 (`{[()]}()`), 8 ops.
- T2 (reuse arm): P = 6 pairs, same pattern, same flat type.
  Canonical: 123,91,40,41,93,125,40,41,40,41,40,41
  (`{[()]}()()()`), 12 ops.
- T3 (revise arm, after Dmax 3->2): P = 5 pairs, nested
  pattern opens [123,91] (depth 2 <= new Dmax), flat type open
  40. Canonical: 123,91,93,125,40,41,40,41,40,41
  (`{[]}()()()`), 10 ops. The old T1 program (`{[()]}()`,
  depth 3) is REJECTED by the new world.

The pattern is given as OPEN BYTES (world terms), never as
learner-internal type indices; the builder maps each byte to a
learned type via the extracted bindings. The builder also
refuses any target whose pattern length exceeds the learned
Dmax. The driver knows the expected bytes (it owns the world
truth, as in GPI-1/GPI-2); the learner never sees them except
through probes and its own output.

## 5. Frozen learner machinery (disclosed)

Standalone pure-Zag learner (gpi3_learner.zag) plus environment
side (gpi3_world.zag: the three types, Dmax, w_check,
driver-only w_dmax_set) and experiment side (gpi3_driver.zag:
teaching, arms, kill-bar evaluation). One u8 state buffer, 4096
bytes, with the IDENTICAL region layout to GPI-2 (the node
vocabulary, node field layout, and all region offsets are
unchanged):

- 0 NF, 1 NM, 2 NPLAN, 3 PLAN_ON (driver-set control flag,
  never written by the learner), 4 NPROG, 5 EPOCH, 6 WIPED, 7
  NPROV.
- 8..11 PLAN_OPS i32, 12..15 DIRECT_OPS i32 (frozen counting
  rules, Section 10).
- 16..527: facts, 64 x 8B [sub,rel,obj,live,epoch,0,0,0].
- 528..783: MAPs, 8 x 32B (layout as GPI-2).
- 784..1039: plan nodes, 32 x 8B
  [kind,depthlv,count,child,next,tokL,tokR,live].
  IDENTICAL layout and semantics to GPI-1/GPI-2 (vocabulary
  frozen): kind 0 = SEQ (execute child then next), 1 = PAIR
  (emit `count` flat pairs), 2 = NEST (emit open, execute
  child, emit close). child/next: node ids, 255 = none.
  tokL/tokR: per-node delimiter bytes bound at build time.
- 1040..1167: programs, 4 x 32B (layout as GPI-2).
- 1168..1231: provenance log, 16 x 4B [kind,a,b,pad].
  kind 1 = REUSE (a = new root, b = reused node);
  kind 2 = SUPERSEDE (a = new root, b = old root);
  kind 3 = RETIRE (a = node id, b = reason).
- 1232..1359: output buffer, 128B. 1360..1487: scratch, 128B.
- 1488..1615: assemble stack, 64 x 2B [nid,phase].
- 1616..4095: spare, zero.

Learner routines (all disclosed, no hidden state):
- f_teach / f_find / f_count: as GPI-2 (fact store, newest-live
  lookup at current epoch, live count). f_teach unchanged.
- f_compact (NEW, disclosed, non-cognitive memory management):
  at the start of l_extract, all facts with sub 70 or 71 (the
  learned constraint model X: bindings plus probe evidence)
  are retired (live=0), and the fact store is compacted so
  live facts occupy slots 0..dst-1 contiguously. Driver-taught
  alphabet facts (72,89) are never retired. Rationale: full
  re-extraction after a world change rebuilds X from fresh
  probes instead of double-teaching 49 more facts into a
  64-slot store; without compaction the revise arm's
  re-extraction would overflow the store. This changes no
  cognitive content: it only reclaims slots of superseded
  evidence. f_find semantics are unaffected (no within-epoch
  duplicate (sub,rel) pairs are ever taught).
- m_teach_emit(rel): primitive single-emit MAP slot, as GPI-2.
- pn_alloc(kind,depthlv,count,child,next,tokL,tokR): plan node
  alloc; kinds only 0,1,2 (K12 grep audit).
- prov_add(kind,a,b): provenance log, as GPI-2.
- type_of_open(b) / type_of_pair(L,R): read ONLY learned
  facts, as GPI-2.
- l_extract(): probe-driven constraint extraction (Section 7).
  Phase A: pair discovery plus rule probes, IDENTICAL to
  GPI-2 (30 ordered pair probes, 5 rule probes from LEARNED
  bindings, MATCH binding). Phase B (NEW): depth-bound
  probing. Uses the LEARNED type-0 bindings (L0,R0): for
  d=0..5 probe the nested single-type string L0^d R0^d;
  teach (71,93,d) on accept, (71,94,d) on reject; bind
  (70,87,D) with D = max accepted d. These probes are
  type-valid at every depth, so outcomes isolate the budget
  dimension. Refuse (-1) unless exactly three types, MATCH
  confirmed as in GPI-2, and D >= 0. Contains NO delimiter
  byte literals: every probe string is built from observed
  fact chars or learned bindings.
- plan_build(st,P,pat,patlen,flat_open): as GPI-2, PLUS the
  budget refusal: reads Dm = f_find(st,70,87); refuses (-1)
  if Dm < 0 or patlen > Dm (the target's required depth is
  its pattern length). All other refusals as GPI-2 (bad
  lengths, P < patlen, unresolvable types). Builds the same
  nested-core-plus-flat-tail shape with per-level bindings.
- plan_build_reuse(st,P,pat,patlen,flat_open,core_id): as
  GPI-2, PLUS the same patlen > Dm refusal.
- plan_retire_all(st,reason): retire every live plan node
  (live=0) with provenance kind 3 (RETIRE), as GPI-1.
  Disclosed: NPLAN is not reset; retired ids stay allocated
  but dead; new nodes take fresh ids.
- plan_revise(st,P,pat,patlen,flat_open,old_root): retire the
  whole old plan (reason 2 = superseded by world change),
  build fresh under the new-epoch constraint, record
  SUPERSEDE provenance kind 2 (new root, old root).
- assemble(root,...): iterative depth-first walk with explicit
  stack, as GPI-2, with ONE disclosed restoration: the
  DEPTH-BUDGET CHECK returns. GPI-1's assembler enforced
  `depthlv <= Dmax` per NEST node; GPI-2 dropped it because
  its family had no budget. This family HAS a budget, so each
  NEST node at assemble time checks its depthlv against the
  current-epoch learned Dmax and assembly refuses if any
  level exceeds it. This is assembler-side constraint
  enforcement (as disclosed in GPI-1/GPI-2), not a change to
  node-vocabulary semantics: node kinds, fields, and
  execution semantics are unchanged. The check adds no op
  count (it rides inside the existing per-NEST-visit step).
- execute(prog): as GPI-2 (runs the op chain, world verifies).
- dt_match / direct_try: IDENTICAL to GPI-2 (the
  no-intermediate control; the canonical target form has
  depth = patlen <= Dmax, so no change is needed).
- construct(...): as GPI-2 (PLAN_ON dispatch, plan path else
  direct_try fallback).

World side (environment only): w[0] = dmax (driver-settable).
w_check as in Section 4. w_dmax_set is driver-only; the
learner never calls it and never reads w[0].

## 6. Phase 0: X is learned, not handed (frozen)

d_phase0_noteach(st, plan_on): driver teaches six alphabet
observations (72,89,c) in FIXED scrambled order
[41,93,40,125,91,123] (no order hint) and the six primitive MAPs
(rels 90..95); sets PLAN_ON; epoch = 1. No extraction yet.
Driver also sets w_dmax_set(w,3) before any arm's probes run
(the revise arm later sets 2, then restores 3).

l_extract(st, w) (learner-owned): phase A exactly as GPI-2
(pair discovery over the six observed chars, 30 ordered
probes; type bindings in discovery order; 5 rule probes from
learned bindings; MATCH). Phase B: depth probes as in
Section 5, binding (70,87,D). No construction happens in phase
0. No constraint-to-program pair is ever taught. The learner
source contains no delimiter byte literals (grep-verified,
K12).

## 7. Arms (each on its own fresh state unless noted)

- ARM-T1 (construct): phase0 (PLAN_ON=1, dmax=3); l_extract;
  audit plan region (K2); plan_build(4,[123,91,40],3,40);
  audit post (K4); assemble (depth check active, all levels
  <= 3); execute; world verdict plus driver byte check (K3).
- ARM-REUSE: phase0; l_extract; plan_build(4,...) (= plan1);
  plan_build_reuse(6,[123,91,40],3,40, core = plan1 core id);
  assemble; execute (K8).
- ARM-REVISE: phase0; l_extract (epoch 1, D=3);
  plan_build(4,[123,91,40],3,40) (= plan1); assemble;
  execute (acc=1 under Dmax 3). Driver act: w_dmax_set(w,2);
  st[5]=2 (epoch 2, driver act as in GPI-1). l_extract (full
  re-extraction at epoch 2: compaction retires epoch-1 X,
  fresh probes; depth probes now give D=2). plan_revise to
  target (5,[123,91],2,40); assemble; execute (K9: acc=1,
  depth 2). Then re-execute the OLD program 0 under the new
  world: expected acc=0 (depth 3 > Dmax 2). Driver restores
  w_dmax_set(w,3) before the next arm.
- ARM-ABLATE: phase0; l_extract; plan_build(4,...);
  assemble; execute; snapshot PLAN_OPS; wipe plan region
  bytes (WIPED=1); direct_try(4,[123,91,40],3,40,20000) (K5).
- ARM-NOCPLAN: phase0 with PLAN_ON=0; l_extract;
  construct(4,...,500) falls back to direct_try (K6).
- ARM-FRESH: fresh state; phase0 (PLAN_ON=1, X learned);
  direct_try(4,...,500) with no plan machinery ever run (K7).
- ARM-XC: (a) phase0 WITHOUT l_extract: plan_build(4,...)
  must refuse; (b1) phase0 WITH l_extract:
  plan_build(4,[200,91,40],3,40) (200 = never-observed byte,
  no learned type) must refuse; (b2) phase0 WITH l_extract:
  plan_build(6,[123,91,40,91],4,40) (all types learned, but
  required depth 4 > Dmax 3) must refuse (K10).

## 8. Expected node shapes (frozen)

T1 plan_build(4,[123,91,40],3,40) allocates, in order:
- id0: PAIR, depthlv 0, count 1, child 255, next 255,
  tokL 40, tokR 41, live 1 (innermost pair, type of pat[2]).
- id1: NEST, depthlv 2, count 0, child 0, next 255,
  tokL 91, tokR 93, live 1 (type of pat[1]).
- id2: NEST, depthlv 1, count 0, child 1, next 255,
  tokL 123, tokR 125, live 1 (type of pat[0]; the core).
- id3: PAIR, depthlv 0, count 1, child 255, next 255,
  tokL 40, tokR 41, live 1 (tail, flat type).
- id4: SEQ, depthlv 0, count 0, child 2, next 3,
  tokL 123, tokR 125, live 1 (root).
Assembled ops: [4,2,0,1,3,5,0,1] spelling
123,91,40,41,93,125,40,41. Reuse T2 adds id5 PAIR(count 3,
flat type) and id6 SEQ(child 2, next 5); core id 2 shared
verbatim; provenance (1,6,2).

T3 plan_revise (after retiring ids 0..4) allocates:
- id5: PAIR, depthlv 0, count 1, child 255, next 255,
  tokL 91, tokR 93, live 1 (inner, type of pat[1]).
- id6: NEST, depthlv 1, count 0, child 5, next 255,
  tokL 123, tokR 125, live 1 (type of pat[0]; the core).
- id7: PAIR, depthlv 0, count 3, child 255, next 255,
  tokL 40, tokR 41, live 1 (tail, flat type).
- id8: SEQ, depthlv 0, count 0, child 6, next 7,
  tokL 123, tokR 125, live 1 (root).
Provenance: RETIRE (3,0,2),(3,1,2),(3,2,2),(3,3,2),(3,4,2);
SUPERSEDE (2,8,4). Assembled ops: [4,2,3,5,0,1,0,1,0,1]
spelling 123,91,93,125,40,41,40,41,40,41 (`{[]}()()()`).

## 9. Frozen cost-counting rules

- PLAN_OPS: +1 per plan node allocated; +1 per NEST node
  visited in assemble (the depth check rides inside this
  step, no extra count); +1 per op appended in assemble; +1
  per op executed in execute; +len per w_check call from the
  plan path. Expected T1: 5 + 2 + 8 + 8 + 8 = 31.
- DIRECT_OPS: per direct_try candidate: +len (build) + len
  (scan) + 1 (target eval). Budget check before each
  candidate: if DIRECT_OPS + cost > budget, stop with
  not-found.
- Extraction probes are not counted (as in GPI-1/GPI-2; the
  bars compare construction cost only).
- Predicted orders: direct_try(4,...) exhausts lengths 2 (36
  candidates, 180 ops), 4 (1296 candidates, 11664 ops), and
  part of 6 before budget 20000 is hit: 180 + 11664 = 11844,
  then (20000-11844)/13 = 627 length-6 candidates,
  DIRECT_OPS = 19995, found = 0. The solution lives at length
  8 (6^8 = 1679616 candidates), unreachable inside any frozen
  budget. NOCPLAN/FRESH (budget 500): 180 + 35 length-4
  candidates = 495 ops, found = 0. IDENTICAL to GPI-2: the
  enumeration code is unchanged and the target length is
  unchanged.

## 10. Frozen kill bars

- K0 STRUCTURAL-DIFFERENCE: PASS iff the run uses exactly the
  Section 2 family (three types, stack discipline, AND depth
  budget Dmax=3) and the report cites the (a)(b)(c)
  justification. Dropping either dimension FAILS K0.
- K1 X-LEARNED: post-phase0 epoch 1: (70,80..85) live with
  values 40,41,91,93,123,125; (70,86,1) live; (70,87,3) live;
  f_count(71,97) = 3; f_count(71,98) = 27; (71,95,1),
  (71,95,3) present; (71,96,0),(71,96,2),(71,96,4) present;
  f_count(71,93) = 4; f_count(71,94) = 2; EXTRACT trace lines
  present. All values from probe outcomes, not literals.
- K2 NO-PLAN-PRE: pre-construction: NPLAN = 0 AND plan region
  (784..1039) byte sum = 0; NM = 6; every MAP has rlen = 1
  (no MAP encodes a construction plan); NPROG = 0.
- K3 CONSTRUCT: plan_build(4,...) returns root >= 0;
  program 0: plen = 8, ops [4,2,0,1,3,5,0,1], bytes
  123,91,40,41,93,125,40,41, acc = 1, measD = 3, measP = 4.
- K4 INTERMEDIATE-CREATED: post-T1 NPLAN = 5 with the exact
  Section 8 shape (all tokL/tokR per node, live = 1,
  root.child = 2, root.next = 3). PLAN-CREATE trace lines
  present for all 5.
- K5 ABLATE: after wipe, direct_try(4,...,20000) found = 0;
  DIRECT_OPS = 19995 (budget exhausted); PLAN_OPS snapshot
  = 31 quoted. The intermediate is necessary.
- K6 NOCPLAN: PLAN_ON=0: construct found = 0 within budget
  500 (DIRECT_OPS = 495); plan region still empty.
- K7 FRESH: fresh learner, X learned, no plan ever built:
  direct_try(4,...,500) found = 0 (DIRECT_OPS = 495).
- K8 REUSE: plan2 root.child = plan1 core node id 2 (exact
  id equality; core unmutated, still live); provenance kind
  1 (6,2) exists; new nodes for plan2 = 2 (ids 5,6);
  program: plen = 12, bytes
  123,91,40,41,93,125,40,41,40,41,40,41, acc = 1, measD = 3,
  measP = 6.
- K9 REVISE: epoch = 2; (70,87,2) live; (70,86,1) live;
  plan1 nodes 0..4 live = 0; RETIRE provenance (3,i,2) for
  i=0..4 present; SUPERSEDE (2,8,4) present; NPLAN = 9;
  new root 8 = SEQ(child 6, next 7); node 6 = NEST d=1
  (123,125) child 5; node 5 = PAIR count 1 (91,93); node 7
  = PAIR count 3 (40,41); program 1: plen = 10, ops
  [4,2,3,5,0,1,0,1,0,1], bytes
  123,91,93,125,40,41,40,41,40,41, acc = 1, measD = 2,
  measP = 5; OLD program 0 re-executed under Dmax=2: acc = 0
  (the old intermediate's product is now world-rejected,
  proving the revision was necessary).
- K10 X-CONTROL: (a) without l_extract, plan_build = -1 and
  NPLAN = 0; (b1) with extraction but pat[0] = 200
  (unlearned), plan_build = -1 and NPLAN = 0; (b2) with
  extraction but required depth 4 > Dmax 3, plan_build = -1
  and NPLAN = 0. A wrong constraint on EITHER dimension is
  refused, never built-around.
- K11 DETERMINISM: 3/3 runs byte-identical; sha256 digests
  quoted.
- K12 ARCHITECTURE: grep audit on all three .zag sources:
  pn_alloc is called only with kind in {0,1,2} (no new node
  kind defined or used); node field layout and region
  offsets identical to GPI-2; 0 new MAP types (six primitive
  single-emit MAPs; max rlen 1 in every arm); 0 modes,
  0 bridges, 0 handlers, 0 opcodes, 0 semantic cases; 0
  delimiter byte literals in gpi3_learner.zag; the builder
  takes (P,pat,flat) as parameters (no per-target solution;
  grep-verified: the contiguous solution byte pattern never
  appears in any source).
- K13 COMMIT-ORDER: the prereg commit (this file plus
  NAMECHECK.md, and nothing else) strictly precedes the
  implementation commit; verified from git log in the
  report.
- K14 NO-DASH: check_no_dash passes on every doc file in
  this directory.

Verdict rule: ALL of K0..K14 PASS for GENERALIZES (with the
honest L2 assessment: topology computed, vocabulary
researcher-shaped; C0-C partial: three constraint probes now,
two single dimensions plus their conjunction, still no
adversary). If B1/B2/B3 fires (K3 or K4 failing because the
vocabulary cannot express the conjunction), the verdict is
BREAKS-WITH-CHARACTERIZATION and the report gives the minimal
failing case plus the exact composition gap. Bars are never
weakened. VOID is terminal. If the intermediate turns out to
be selected from a researcher-shaped set rather than
invented, the report downgrades honestly instead of claiming
L3.

## 11. Deliverables

NAMECHECK.md (this dir), PREREG.md (this file),
gpi3_world.zag, gpi3_learner.zag, gpi3_driver.zag,
gpi3_full.zag (concatenation), gpi3_bin, gpi3_compile.txt,
gpi3_run1.txt, gpi3_run2.txt, gpi3_run3.txt (3/3
byte-identical, sha256), REPORT.md with per-bar results,
creation/reuse/revision traces, ablation numbers, the
generality verdict (GENERALIZES or
BREAKS-WITH-CHARACTERIZATION), the honest L2 vs L3
assessment, and cognition lines added.
