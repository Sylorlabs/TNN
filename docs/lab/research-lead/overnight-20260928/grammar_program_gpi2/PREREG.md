# PREREG: GPI-2 Second Constraint-Family Generality Probe

Status: PREREG-FROZEN. No implementation exists at this commit.
Scope: `docs/lab/research-lead/overnight-20260928/grammar_program_gpi2/` only.
Worker: GPI-2 Generality Probe Worker (subagent, 2026-10-02).
Parent mandate: L2 ADAPTIVE REUSE is the top priority; L3 novel
intermediate form is the main architecture target. GPI-1 (ledger
C303) proved the learner creates a construction-plan intermediate
(SEQ/PAIR/NEST vocabulary) mediating a learned single-delimiter
depth-budget constraint and an executable MAP-chain program, then
reuses and revises it; honest verdict L2-COMPLETE, L3 not claimed,
C0-C failed (single constraint family, no adversary).

## 1. What is being tested

Whether the SAME intermediate machinery that passed GPI-1, with
the node vocabulary FROZEN, generalizes to a structurally
different constraint family. The learner must: extract the new
constraint from world probes (not handed), build a construction
plan using ONLY the existing SEQ/PAIR/NEST vocabulary (adding a
node kind to make it pass is FORBIDDEN and is itself a frozen bar,
K11), assemble a MAP-chain program from the plan, execute it, and
obtain world acceptance. Then: reuse the plan's core on a second
target in the new family, show the no-plan direct path fails, show
a fresh learner fails, and show a wrong constraint is refused.

THE LOAD-BEARING QUESTION: does the fixed vocabulary plus the plan
machinery handle the new family, or does it break? BOTH outcomes
are publishable. GENERALIZES: partial C0-C evidence (the
intermediate machinery now spans two constraint dimensions). BREAKS:
the report characterizes EXACTLY which vocabulary piece or builder
assumption fails, with a minimal failing case; that
characterization IS the result, and it precisely states the
invention gap the L3 track must close. The family is not contorted
to fit the vocabulary, and the vocabulary is not extended to fit
the family.

What is NOT tested: exact reuse of grammar to construction (done);
a third family; revision under world change (done in GPI-1, not
redone); invention of a new node kind (explicitly out of scope and
forbidden here).

## 2. The chosen family and the frozen structural-difference bar (K0)

Family: MULTI-TYPE STACK-DISCIPLINE WELL-FORMEDNESS. World truth:
three delimiter types, (40,41) `()`, (91,93) `[]`, (123,125) `{}`.
w_check accepts a string iff every byte is one of the six delimiter
bytes, the string is balanced, and EVERY CLOSE MATCHES THE MOST
RECENT OPEN TYPE. There is NO depth budget: arbitrarily deep
well-formed nesting is accepted.

K0 STRUCTURAL-DIFFERENCE (frozen at prereg; judged against this
section): the run family must be exactly the one above. It is
structurally different from GPI-1's (single delimiter pair, scalar
max-depth budget) by constraint DIMENSION, not parameters:

(a) Constraint kind. GPI-1 enforced a RESOURCE BUDGET: max depth D,
a scalar consumed by nesting (`(((` rejected for exceeding the
budget). GPI-2 enforces a SYMBOLIC CORRESPONDENCE: a relation
between open and close positions (`([)]` rejected for type
mismatch, while `(((` with one type is accepted at any depth).
Budget vs correspondence are different kinds of constraint; no
choice of GPI-1 parameters expresses type matching, and no choice
of GPI-2 parameters expresses a depth budget.

(b) Which plan field does the work. In GPI-1 the load-bearing plan
field was NEST.depthlv (absolute budget level, ENFORCED by the
assembler check `lv <= Dmax`); token identity was fixed globally.
In GPI-2 the load-bearing plan content is the PER-NODE
(tokL,tokR) BINDINGS (type identity varies per node);
well-formedness is enforced by the TREE STRUCTURE itself (each
NEST node closes its own type around its children), not by any
field check. The depthlv field is recorded but unenforced. A
different part of the frozen vocabulary carries the new dimension.

(c) Extraction task. GPI-1 extracted a SCALAR (max accepted depth
from probes d=0..5) and a BINARY order. GPI-2 must extract a
PARTITION (which of 15 unordered char pairs form the 3 types, from
30 ordered probes) and a RELATIONAL RULE (crossed `([)]`, `[(])`,
`{[}]` rejected vs nested `([])` accepted implies most-recent-open
matching). A depth-budget extractor cannot represent this answer;
a type-alphabet extractor cannot solve GPI-1. The probe designs are
disjoint.

Excluded as not-structurally-different (and not run): changing the
delimiter bytes, changing Dmax, adding a second depth budget, or
any single-type variant. If the run smuggles in a depth budget or
deviates from the family above, K0 FAILS.

## 3. Frozen hypothesis and preregistered break conditions

Hypothesis (frozen): GENERALIZES. Reasons, stated before the run:

1. The node format ALREADY carries per-node (tokL,tokR)
   (GPI-1 recorded them on every node but bound them all
   identically). The new family varies them per node; no format
   change is needed to express type identity per part.
2. NEST execution semantics (emit open, execute child, emit close)
   enforces stack discipline for ANY token binding, because each
   NEST node's close necessarily matches its own open and children
   are strictly enclosed. Cross-type well-formedness falls out of
   the tree structure; it needs no new combinator.
3. The builder's "nested core plus flat tail" decomposition maps
   cleanly: the target's nested TYPE PATTERN becomes the NEST
   chain's per-level bindings; the target's flat type becomes the
   tail PAIR's binding. The depth-budget check is dropped from the
   assembler because this family has no depth budget; that check
   was assembler-side constraint enforcement, not node-vocabulary
   semantics.

Preregistered break conditions (any one yields verdict
BREAKS-WITH-CHARACTERIZATION, never a vocabulary extension):

- B1: plan_build cannot produce a plan for a well-posed target
  (P, pattern, flat type) using only kinds 0,1,2 that assembles to
  a world-accepted, pattern-matching program.
- B2: per-node token bindings cannot be carried faithfully through
  assembly to execution within the frozen node/program formats.
- B3: the tree structure fails to enforce the matching discipline
  for some target in the family (a plan the builder produces is
  world-rejected for mismatch).

If any break fires, the report names the exact failing vocabulary
piece or builder assumption, gives the MINIMAL failing case
(smallest target that breaks), and states the invention gap. The
bars below are never weakened to avoid a break verdict.

## 4. Domain and scenario (all ids frozen)

World truth (experiment side only; learner sees only w_check
outcomes): types T0=(40,41), T1=(91,93), T2=(123,125). w_check:
1 iff every byte is in {40,41,91,93,123,125}, the string is
balanced, and every close matches the most recent open's type
(stack discipline). No depth limit. No world change in GPI-2.

X (learned in phase 0 by l_extract from probes, never from
literals):
- (CONSTR=70, 80+2t, Lt), (CONSTR=70, 81+2t, Rt) for t=0,1,2:
  the three type bindings in learner discovery order. Expected
  values (from the fixed scrambled teaching order, Section 6):
  (40,41), (91,93), (123,125).
- (CONSTR=70, 86, MATCH): 1 iff the rule probes confirm
  most-recent-open matching. Expected 1.
- Pair-probe facts (71,97,code) accept / (71,98,code) reject for
  the 30 ordered char-pair probes, code = i*6+j over the six
  observed chars. Expected: 3 accepts, 27 rejects.
- Rule-probe facts (71,95,k) accept / (71,96,k) reject, k=0..4.
  Expected: accepts k=1,3; rejects k=0,2,4.

Primitive MAPs (preexisting, no construction plan): six
single-emit MAPs taught in fixed order with rels 90..95:
MAP 0..5, even rel = open slot, odd rel = close slot. The MAPs are
generic emit slots; token bytes come from the program record's
per-type table (filled at assemble time from learned facts),
exactly as GPI-1's program record carried (L,R). Max relseq length
is 1 before, during, and after every arm: no MAP ever encodes a
multi-step construction.

Targets (given as goals, not paired examples):
- T1: P = 4 pairs, nested pattern opens [123,91,40] (`{` outer,
  `[` middle, `(` inner), flat type open 40 (`()` tail).
  Canonical program bytes: 123,91,40,41,93,125,40,41
  (`{[()]}()`), 8 ops.
- T2 (reuse arm): P = 6 pairs, same pattern, same flat type.
  Canonical: 123,91,40,41,93,125,40,41,40,41,40,41
  (`{[()]}()()()`), 12 ops.

The pattern is given as OPEN BYTES (world terms), never as
learner-internal type indices; the builder maps each byte to a
learned type via the extracted bindings. The driver knows the
expected bytes (it owns the world truth, as in GPI-1); the learner
never sees them except through probes and its own output.

## 5. Frozen learner machinery (disclosed)

Standalone pure-Zag learner (gpi2_learner.zag) plus environment
side (gpi2_world.zag: the three types and w_check) and experiment
side (gpi2_driver.zag: teaching, arms, kill-bar evaluation). One u8
state buffer, 4096 bytes:

- 0 NF, 1 NM, 2 NPLAN, 3 PLAN_ON (driver-set control flag, never
  written by the learner), 4 NPROG, 5 EPOCH, 6 WIPED, 7 NPROV.
- 8..11 PLAN_OPS i32, 12..15 DIRECT_OPS i32 (frozen counting
  rules, Section 9).
- 16..527: facts, 64 x 8B [sub,rel,obj,live,epoch,0,0,0].
- 528..783: MAPs, 8 x 32B [tag=20,live,start,end,rlen,flen,
  reason,pad, rels x8 @+8, facts x8 @+16, pad x8 @+24].
- 784..1039: plan nodes, 32 x 8B
  [kind,depthlv,count,child,next,tokL,tokR,live].
  IDENTICAL layout and semantics to GPI-1 (vocabulary frozen):
  kind 0 = SEQ (execute child then next), 1 = PAIR (emit `count`
  flat pairs), 2 = NEST (emit open, execute child, emit close).
  child/next: node ids, 255 = none. tokL/tokR: per-node delimiter
  bytes bound at build time from X.
- 1040..1167: programs, 4 x 32B
  [plen,tP,tD,epoch,acc,measD,measP,
   T0L,T0R,T1L,T1R,T2L,T2R, tp0,tp1,tp2, ops x16 @+16].
  Ops are PRIMITIVE MAP IDS 0..5 (op = 2t for open of learned
  type t, 2t+1 for close). The per-type byte table T0L..T2R is
  filled at assemble time from the learned bindings (the analog
  of GPI-1's program-level L,R, generalized to three types).
  tp0..tp2 record the target pattern open bytes for traces.
- 1168..1231: provenance log, 16 x 4B [kind,a,b,pad].
  kind 1 = REUSE (a = new root, b = reused node).
- 1232..1359: output buffer, 128B. 1360..1487: scratch, 128B.
- 1488..1615: assemble stack, 64 x 2B [nid,phase].
- 1616..4095: spare, zero.

Learner routines (all disclosed, no hidden state):
- f_teach / f_find / f_count: as GPI-1 (fact store, newest-live
  lookup, live count).
- m_teach_emit(rel): primitive single-emit MAP slot (rlen = 1).
- pn_alloc(kind,depthlv,count,child,next,tokL,tokR): plan node
  alloc; kinds only 0,1,2 (K11 grep audit).
- prov_add(kind,a,b): provenance log.
- type_of_open(b): returns t in 0..2 with (70,80+2t) == b at
  current epoch, else -1. type_of_pair(L,R): returns t with both
  bindings matching, else -1. Both read ONLY learned facts.
- l_extract(): probe-driven constraint extraction (Section 6).
  Writes the six type bindings, MATCH, and all probe facts.
  Contains NO delimiter byte literals: every probe string is
  built from observed fact chars or learned bindings.
- plan_build(st,P,pat,patlen,flat_open): reads current-epoch
  constraint. Refuses (-1) if: patlen < 1, patlen > 8, P <
  patlen, any pat[l] maps to no learned type, or flat_open maps
  to no learned type. Else builds: inner = PAIR(count=1) bound
  to the type of pat[patlen-1]; NEST chain lv = patlen-1 down to
  1, each NEST(depthlv=lv) bound to the type of pat[lv-1] with
  child = inner; core = outermost NEST; tail = PAIR(count =
  P-patlen) bound to the flat type; root = SEQ(child = core,
  next = tail). Returns root id. The decomposition strategy is
  GPI-1's (nested core plus flat tail); only the PER-LEVEL
  BINDINGS are new, and they come from the target pattern plus
  learned facts, never from literals.
- plan_build_reuse(st,P,pat,patlen,flat_open,core_id): new root
  SEQ shares the existing live core node VERBATIM (no rebuild, no
  mutation) plus a new tail PAIR; provenance kind 1.
- assemble(root,...): iterative depth-first walk with explicit
  stack (no recursion), same as GPI-1. SEQ: child subtree then
  next subtree. NEST: resolve (tokL,tokR) to type t via learned
  bindings (refuse if unresolvable); emit op 2t, walk child,
  emit op 2t+1; count one NEST-visit. PAIR: count times emit
  (2t, 2t+1). THE DEPTH-BUDGET CHECK IS DROPPED: GPI-1's
  assembler enforced `depthlv <= Dmax`; this family has no depth
  budget, so there is nothing to enforce. This is disclosed
  here: the check was assembler-side constraint enforcement, not
  node-vocabulary semantics. Node kinds, fields, and execution
  semantics are unchanged. Fills the program's per-type byte
  table from learned facts; records tp0..tp2.
- execute(prog): runs the op chain: for each op (MAP id), checks
  the MAP live, takes byte = program Ttable[op], open iff the
  MAP rel is even (rels 90..95: even = open slot); tracks depth,
  maxd, pairs; calls w_check; records acc, measD, measP.
- direct_try(st,w,P,pat,patlen,flat_open,budget): the
  no-intermediate control. Enumerates op sequences (MAP ids
  0..5) of length 2,4,...,2P in lex order (position 0 varies
  fastest: digit k = (num / 6^k) mod 6), bytes from the learned
  per-type table. Target eval per candidate: the (nested core,
  flat tail) decomposition check dt_match: first 2D bytes are D
  opens equal to pat[0..D-1] followed by D closes each matching
  its mirror open's type; remaining 2*(P-D) bytes are (P-D)
  repeats of [flat_open, flat_close]. This eval is EXACTLY the
  byte string the plan path must produce (the nested core bytes
  are fully determined by pat plus bindings; the tail by the
  flat type), so it is sound and complete for the goal's
  canonical form. On eval pass, calls w_check; returns 1 on
  first full pass, else 0 (budget exhausted). Counts DIRECT_OPS
  per Section 9. Knows the target (P,pat,flat): the goal is
  given; the question is whether an intermediate is needed.
- construct(...): if PLAN_ON == 0, or plan_build refuses, falls
  back to direct_try; else plan_build + assemble + execute.

World side (environment only): w_check as in Section 4. No
w_setdmax (no world change in GPI-2).

## 6. Phase 0: X is learned, not handed (frozen)

d_phase0_noteach(st, plan_on): driver teaches six alphabet
observations (72,89,c) in FIXED scrambled order
[41,93,40,125,91,123] (no order hint) and the six primitive MAPs
(rels 90..95); sets PLAN_ON; epoch = 1. No extraction yet.

l_extract(st, w) (learner-owned):
1. Collect the six observed chars c[0..5] from facts (72,89).
   Refuse (-1) unless exactly six distinct chars are present.
2. Pair discovery: for i in 0..5, for j in i+1..5: probe the
   2-char strings [c[i],c[j]] and [c[j],c[i]] against w_check;
   teach (71,97,i*6+j) on accept, (71,98,i*6+j) on reject.
   Exactly three accepts are expected; each accepted ordered
   pair binds one type in discovery order t=0,1,2:
   (70,80+2t,L),(70,81+2t,R), superseding any older bindings.
   With the frozen teaching order the discovery order is
   (40,41),(91,93),(123,125). Refuse unless exactly three pairs
   are found.
3. Rule probes, built from the LEARNED bindings (no literals):
   P0=[L0,L1,R0,R1] (crossed), P1=[L0,L1,R1,R0] (nested),
   P2=[L1,L0,R1,R0] (crossed), P3=[L2,R2] (single pair sanity),
   P4=[L2,L1,R2,R1] (crossed). Teach (71,95,k) on accept,
   (71,96,k) on reject. Bind (70,86,1) iff P0,P2,P4 rejected and
   P1,P3 accepted (most-recent-open matching confirmed);
   otherwise bind (70,86,0).
4. Return 1 on success, -1 on any refusal.

No construction happens in phase 0. No constraint-to-program pair
is ever taught. The learner source contains no delimiter byte
literals (grep-verified, K11).

## 7. Arms (each on its own fresh state unless noted)

- ARM-T1 (construct): phase0 (PLAN_ON=1); l_extract; audit plan
  region (K2); plan_build(4,[123,91,40],3,40); audit post (K4);
  assemble; execute; world verdict plus driver byte check (K3).
- ARM-REUSE: phase0; l_extract; plan_build(4,...) (= plan1);
  plan_build_reuse(6,[123,91,40],3,40, core = plan1 core id);
  assemble; execute (K8).
- ARM-ABLATE: phase0; l_extract; plan_build(4,...); assemble;
  execute; snapshot PLAN_OPS; wipe plan region bytes (WIPED=1);
  direct_try(4,[123,91,40],3,40,20000) (K5).
- ARM-NOCPLAN: phase0 with PLAN_ON=0; l_extract;
  construct(4,...,500) falls back to direct_try (K6).
- ARM-FRESH: fresh state; phase0 (PLAN_ON=1, X learned);
  direct_try(4,...,500) with no plan machinery ever run (K7).
- ARM-XC: (a) phase0 WITHOUT l_extract: plan_build(4,...) must
  refuse; (b) phase0 WITH l_extract:
  plan_build(4,[200,91,40],3,40) (200 = never-observed byte, no
  learned type) must refuse (K9).

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

## 9. Frozen cost-counting rules

- PLAN_OPS: +1 per plan node allocated; +1 per NEST node visited
  in assemble; +1 per op appended in assemble; +1 per op executed
  in execute; +len per w_check call from the plan path.
  Expected T1: 5 + 2 + 8 + 8 + 8 = 31.
- DIRECT_OPS: per direct_try candidate: +len (build) + len
  (scan) + 1 (target eval). Budget check before each candidate:
  if DIRECT_OPS + cost > budget, stop with not-found.
- Extraction probes are not counted (same as GPI-1; the bars
  compare construction cost only).
- Predicted orders: direct_try(4,...) must exhaust lengths 2
  (36 candidates, 180 ops), 4 (1296 candidates, 11664 ops), and
  part of 6 (46656 candidates, 13 ops each) before budget 20000
  is hit: 180 + 11664 = 11844, then (20000-11844)/13 = 627
  length-6 candidates, found = 0. The solution lives at length 8
  (6^8 = 1679616 candidates), unreachable inside any frozen
  budget. NOCPLAN/FRESH (budget 500): 180 + 35 length-4
  candidates = 495 ops, found = 0.

## 10. Frozen kill bars

- K0 STRUCTURAL-DIFFERENCE: PASS iff the run uses exactly the
  Section 2 family (three types, stack discipline, no depth
  budget) and the report cites the (a)(b)(c) justification. Any
  deviation (e.g. a smuggled depth budget) FAILS K0.
- K1 X-LEARNED: post-phase0: (70,80..85) live with values
  40,41,91,93,123,125; (70,86,1) live; f_count(71,97) = 3;
  f_count(71,98) = 27; (71,95,1),(71,95,3) present;
  (71,96,0),(71,96,2),(71,96,4) present; EXTRACT trace lines
  present. Values from probe outcomes, not literals.
- K2 NO-PLAN-PRE: pre-construction: NPLAN = 0 AND plan region
  (784..1039) byte sum = 0; NM = 6; every MAP has rlen = 1
  (no MAP encodes a construction plan); NPROG = 0.
- K3 CONSTRUCT: plan_build(4,...) returns root >= 0; program 0:
  plen = 8, ops [4,2,0,1,3,5,0,1], bytes
  123,91,40,41,93,125,40,41, acc = 1, measD = 3, measP = 4.
- K4 INTERMEDIATE-CREATED: post-T1 NPLAN = 5 with the exact
  Section 8 shape (all tokL/tokR per node, live = 1,
  root.child = 2, root.next = 3). PLAN-CREATE trace lines
  present for all 5.
- K5 ABLATE: after wipe, direct_try(4,...,20000) found = 0
  (budget exhausted; DIRECT_OPS and PLAN_OPS snapshot quoted).
  The intermediate is necessary: without it the target is
  unreachable inside a 20000-op budget.
- K6 NOCPLAN: PLAN_ON=0: construct found = 0 within budget 500;
  plan region still empty (NPLAN = 0).
- K7 FRESH: fresh learner, X learned, no plan ever built:
  direct_try(4,...,500) found = 0.
- K8 REUSE: plan2 root.child = plan1 core node id 2 (exact id
  equality; core unmutated, still live); provenance kind 1
  (6,2) exists; new nodes for plan2 = 2 (ids 5,6); program:
  plen = 12, bytes 123,91,40,41,93,125,40,41,40,41,40,41,
  acc = 1, measD = 3, measP = 6.
- K9 X-CONTROL: (a) without l_extract, plan_build = -1 and
  NPLAN = 0; (b) with extraction but pat[0] = 200 (unlearned),
  plan_build = -1 and NPLAN = 0. Wrong constraint is refused,
  never built-around.
- K10 DETERMINISM: 3/3 runs byte-identical; sha256 digests
  quoted.
- K11 ARCHITECTURE: grep audit on all three .zag sources:
  pn_alloc is called only with kind in {0,1,2} (no new node
  kind defined or used); 0 new MAP types (six primitive
  single-emit MAPs; max rlen 1 in every arm); 0 modes,
  0 bridges, 0 handlers, 0 opcodes, 0 semantic cases; builder
  takes (P,pat,flat) as parameters (no per-target solution;
  grep-verified: the contiguous solution byte pattern never
  appears in learner.zag; the learner contains no delimiter
  byte literals at all).
- K12 NO-DASH: worker_snippets/check_no_dash.sh passes on every
  doc file in this directory.
- K13 COMMIT-ORDER: the prereg commit (this file plus
  NAMECHECK.md, and nothing else) strictly precedes the
  implementation commit; verified from git log in the report.

Verdict rule: ALL of K0..K13 PASS for GENERALIZES (with the honest
L2 assessment: topology computed, vocabulary researcher-shaped;
C0-C partial: two constraint dimensions, still no adversary).
If B1/B2/B3 fires (K3 or K4 failing because the vocabulary cannot
express the family), the verdict is BREAKS-WITH-CHARACTERIZATION
and the report gives the minimal failing case plus the exact
invention gap. Bars are never weakened. VOID is terminal. If the
intermediate turns out to be selected from a researcher-shaped set
rather than invented, the report downgrades honestly instead of
claiming L3.

## 11. Deliverables

NAMECHECK.md (this dir), PREREG.md (this file), gpi2_world.zag,
gpi2_learner.zag, gpi2_driver.zag, gpi2_full.zag (concatenation),
gpi2_bin, gpi2_compile.txt, gpi2_run1.txt, gpi2_run2.txt,
gpi2_run3.txt (3/3 byte-identical, sha256), REPORT.md with per-bar
results, creation/reuse traces, ablation numbers, the generality
verdict (GENERALIZES or BREAKS-WITH-CHARACTERIZATION), the honest
L2 vs L3 assessment, and cognition lines added.
