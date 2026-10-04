# PREREG: Grammar Constraints to Program Construction via a Created Intermediate Representation

Status: PREREG-FROZEN. No implementation exists at this commit.
Scope: `docs/lab/research-lead/overnight-20260928/grammar_program_intermediate/` only.
Worker: Grammar-Program-Intermediate Worker (subagent, 2026-10-02).
Parent mandate: L2 ADAPTIVE REUSE is the top priority; L3 novel
intermediate form is the main architecture target. Grammar to
program construction REQUIRING A NEW INTERMEDIATE is explicitly on
Micah's high-value list and is not yet done.

## 1. What is being tested

Whether a learner holding a LEARNED grammar constraint structure X
can construct an executable MAP-chain PROGRAM for a target it has
never seen built, by CREATING an intermediate construction plan
that did not exist before the episode, using the plan to drive
program assembly, executing the program, and obtaining world
acceptance. The intermediate must then be REUSED on a second target
and REVISED after a constraint change, with white-box traces. The
direct constraint to program jump (no intermediate) must be shown
to fail or to be an order of magnitude more expensive. This is an
L2/L3 boundary probe: the report must state honestly whether the
intermediate was genuinely invented (open form) or selected from a
small researcher-shaped set, against Micah's invention criteria
(C0-A through C0-D). No finite operator menu may be widened to make
this work.

What is NOT tested: exact reuse of grammar to construction (done by
H1/H2 in xdomain_grammar_construct; not redone). No paired
constraint to program training examples exist anywhere in the
experiment.

## 2. Domain and scenario (all ids frozen)

Constraint family: balanced delimiter strings. World truth:
delimiters (40, 41) i.e. `(` and `)`, max nesting depth Dmax = 3,
then a world change sets Dmax = 4 (Section 6).

X (learned independently in phase 0, before any construction):
constraint facts written by the learner's extraction routine
`l_extract` from world probes, never from researcher literals:
- (CONSTR=70, 80, L): opener binding. Expected L = 40.
- (CONSTR=70, 81, R): closer binding. Expected R = 41.
- (CONSTR=70, 82, D): max depth. Expected D = 3 (epoch 1), 4 after
  revision (epoch 2).
Extraction probes (learner-owned, Section 4): alphabet observations
taught as (ALPHA=72, 89, c) for c = 41 then 40 (order scrambled, no
order hint); the learner tries both 2-char orders against the world
and binds the accepted order as (L, R); the learner builds nested
probe strings of depth d = 0..5 and records (PROBE=71, 87, d) for
accept / (PROBE=71, 88, d) for reject; D = max accepted d.

Primitive MAPs (preexisting, no construction plan): MAP 0 EMIT-OPEN
(rel 90), MAP 1 EMIT-CLOSE (rel 91). Each appends one bound token
to the output buffer. Max relseq length is 1 before, during, and
after every arm: no MAP ever encodes a multi-step construction.

Targets (given as goals, not paired examples):
- T1: P = 4 pairs, exact depth D = 3. Canonical program: the
  8-op chain spelling `((()))()`.
- T2 (reuse arm): P = 6 pairs, exact depth D = 3, same constraint.
  Canonical: `((()))()()()` (12 ops).
- T3 (revision arm): P = 6 pairs, exact depth D = 4, after the
  world change Dmax 3 -> 4. Canonical: `(((())))()()` (12 ops).

## 3. Frozen learner machinery (disclosed)

Standalone pure-Zag learner (gpi_learner.zag) plus environment side
(gpi_world.zag: delimiter truth, Dmax, w_check, w_setdmax) and
experiment side (gpi_driver.zag: teaching, arms, kill-bar
evaluation). One u8 state buffer, 4096 bytes:

- 0 NF, 1 NM, 2 NPLAN, 3 PLAN_ON (driver-set control flag, never
  written by the learner), 4 NPROG, 5 EPOCH, 6 WIPED, 7 pad.
- 8..11 PLAN_OPS i32, 12..15 DIRECT_OPS i32 (frozen counting
  rules, Section 7).
- 16..271: facts, 32 x 8B [sub,rel,obj,live,epoch,0,0,0].
- 272..527: MAPs, 8 x 32B [tag=20,live,start,end,rlen,flen,
  reason,pad, rels x8 @+8, facts x8 @+16, pad x8 @+24].
- 528..783: plan nodes, 32 x 8B
  [kind,depthlv,count,child,next,tokL,tokR,live].
  kind: 0 = SEQ (execute child list), 1 = PAIR (emit `count`
  flat pairs), 2 = NEST (open at absolute depth level `depthlv`,
  execute child, close). child/next: node ids, 255 = none.
  tokL/tokR: delimiter bytes bound at build time from X.
- 784..911: programs, 4 x 32B
  [plen,targetP,targetD,epoch,acc,measD,measP,pad, ops x24 @+8].
  ops are MAP ids (0 = open, 1 = close); L/R bindings stored per
  program at assembly.
- 912..975: provenance log, 16 x 4B [kind,a,b,pad].
  kind 1 = REUSE (a = new root, b = reused node),
  kind 2 = SUPERSEDE (a = new root, b = old root),
  kind 3 = RETIRE (a = node, b = reason; reason 2 = superseded).
- 976..1103: output buffer, 128B. 1104..1231: scratch, 128B.
  1232..4095: spare, zero.

Learner routines (all disclosed, no hidden state):
- f_teach(sub,rel,obj): store an observation fact.
- l_extract(): probe-driven constraint extraction (Section 4).
  Writes (70,80,L),(70,81,R),(70,82,D) at current epoch.
- plan_build(P,D): reads current-epoch constraint; refuses (-1)
  if absent or if D > Dmax. Allocates: root SEQ; core =
  nest_chain(D): NEST(depthlv=1) -> NEST(depthlv=2) -> ...
  -> NEST(depthlv=D-1) -> PAIR(count=1); tail = PAIR(count=P-D).
  Links root.child = core, core.next = tail (sibling chain via
  next). Each NEST node carries its absolute depth level: the
  constraint budget propagated to each part. Returns root id.
- plan_build_reuse(P,D,core_id): new root SEQ with child =
  core_id (an existing live node: verbatim reuse, no rebuild),
  new tail PAIR(count=P-D); writes provenance kind 1
  (new_root, core_id).
- plan_revise(P,D,old_root): retires every node of the old plan
  (live=0, provenance kind 3, reason 2), builds a fresh plan via
  plan_build(P,D) under the new epoch constraint, writes
  provenance kind 2 (new_root, old_root).
- assemble(root,P,D): walks the plan; NEST(depthlv=l) checks
  l <= current Dmax else aborts; emits op ids into a new program
  record (PAIR: count x (0,1); NEST: 0, child ops, 1; SEQ: child
  list). Binds program L/R from the plan nodes.
- execute(prog): runs the op chain through MAP 0/1 into the
  output buffer; measures measD (max depth) and measP (pair
  count, counted on closes); calls w_check; records acc.
- construct(P,D): if PLAN_ON == 0, or no plan exists, falls back
  to direct_try (the no-intermediate control path). Else
  plan_build + assemble + execute.
- direct_try(P,D,budget): enumerates emit sequences of length
  2,4,...,2P in lex order (0 = open from current constraint
  facts, 1 = close); for each candidate builds the string,
  measures balanced/depth/pairs, calls w_check; stops at first
  candidate with pairs == P, depth == D, world accept. Counts
  DIRECT_OPS per Section 7. Returns 1 found / 0 not found
  (budget exhausted). Uses no plan state.

World side (environment only; learner never calls w_setdmax):
- w_check(buf,len): 1 iff every byte is 40/41, the string is
  balanced, and max depth <= w_dmax. w_dmax starts 3.
- w_setdmax(v): driver-only world change.

## 4. Phase 0: X is learned, not handed (frozen)

d_phase0(st): driver teaches (72,89,41),(72,89,40) and the two
primitive MAPs; driver sets PLAN_ON per arm; learner runs
l_extract(): delimiter-order probe (both orders, world decides),
depth probe d = 0..5 (world decides each), binds (70,80,L),
(70,81,R),(70,82,D). No construction happens in phase 0. No
constraint to program pair is ever taught.

## 5. Arms (each on its own fresh state unless noted)

- ARM-T1 (construct): phase0; audit plan region (Section 8, K2);
  plan_build(4,3); audit post (K4); assemble; execute; world
  verdict (K3).
- ARM-REUSE: phase0; plan_build(4,3) (= plan1); plan_build_reuse
  (6,3, core = plan1 core id); assemble; execute (K8).
- ARM-REVISE: phase0; plan_build(4,3) (= plan1); assemble+execute
  program1; driver w_setdmax(4); learner l_extract() (epoch 2);
  plan_revise(6,4, plan1 root); assemble; execute (K9). Also:
  re-measure program1's string under the new world (world still
  accepts; learner measD = 3 != target 4, so the old intermediate
  cannot serve the new target: revision was necessary).
- ARM-ABLATE: phase0; plan_build(4,3); snapshot PLAN_OPS;
  wipe plan region bytes (WIPED=1); direct_try(4,3,20000) (K5).
- ARM-NOCPLAN: phase0 with PLAN_ON=0; construct(4,3) falls back
  to direct_try(4,3,500) (K6).
- ARM-FRESH: fresh state; phase0 (X learned); direct_try(4,3,500)
  with no plan machinery ever run (K7).
- ARM-XC: phase0 WITHOUT l_extract; plan_build(4,3) must refuse
  (K10).

## 6. World change (frozen)

Between the pre and post halves of ARM-REVISE only, the driver
calls w_setdmax(4). Delimiters never change. The learner detects
the change only by re-probing (l_extract at epoch 2 observes depth
4 accepted). The old epoch-1 constraint facts are marked
superseded (live=0); epoch-2 facts are written.

## 7. Frozen cost-counting rules

- PLAN_OPS: +1 per plan node allocated; +1 per NEST level check
  in assemble; +1 per op appended in assemble; +1 per op executed
  in execute; +len per w_check call from execute/assemble path.
- DIRECT_OPS: per direct_try candidate: +len (build) + len
  (scan) + 1 (target eval). Budget check before each candidate:
  if DIRECT_OPS + cost > budget, stop with not-found.
- Expected orders (to be measured, bars use the ratio): T1
  PLAN_OPS ~31 (5 alloc + 8 assemble + 2 NEST checks + 8 execute
  + 8 w_check); direct_try(4,3) DIRECT_OPS ~1500 (lengths 2,4,6
  all fail: 4+16+64 candidates; first success at len 8 is
  `((()))()` = bits 00011101, lex index 29).

## 8. Frozen kill bars

- K1 X-LEARNED: post-phase0 facts (70,80,40),(70,81,41),
  (70,82,3) exist, live, epoch 1; probe facts (71,87,d) for
  d = 0..3 and (71,88,d) for d = 4,5 exist; EXTRACT trace lines
  present. The values came from probe outcomes, not literals
  (learner.zag contains no 40/41/3 as constraint values; the
  driver teaches only alphabet observations).
- K2 NO-PLAN-PRE: pre-construction: plan node count == 0 AND plan
  region byte sum == 0; NM == 2; every MAP has rlen == 1
  (no MAP encodes a construction plan); NPROG == 0.
- K3 CONSTRUCT: plan_build(4,3) returns root >= 0; program:
  plen == 8, ops spell bytes 40,40,40,41,41,41,40,41,
  acc == 1, measD == 3, measP == 4.
- K4 INTERMEDIATE-CREATED: post-T1 plan node count == 5 with
  shape root SEQ(kind 0); NEST depthlv 1,2; PAIR count 1 (core);
  PAIR count 1 (tail); all tokL == 40, tokR == 41, live == 1;
  core.next == tail id; root.child == core id. PLAN-CREATE trace
  lines present for all 5.
- K5 ABLATE: after wipe, direct_try(4,3,20000) found == 1 with
  DIRECT_OPS / PLAN_OPS_snapshot >= 10 (both quoted). The
  intermediate is causally load-bearing: without it,
  construction costs an order of magnitude more.
- K6 NOCPLAN: PLAN_ON=0: construct(4,3) found == 0 within budget
  500; plan region still empty (node count == 0).
- K7 FRESH: fresh learner, X learned, no plan: direct_try(4,3,
  500) found == 0.
- K8 REUSE: plan2 root.child == plan1 core node id (exact id
  equality); provenance kind 1 (plan2 root, core id) exists;
  new nodes allocated for plan2 == 2 (root + tail); program2:
  plen == 12, bytes `((()))()()()`, acc == 1, measD == 3,
  measP == 6.
- K9 REVISE: post w_setdmax(4): EPOCH == 2; (70,82,4) live at
  epoch 2; all 5 plan1 nodes live == 0; provenance kind 2
  (plan3 root, plan1 root) and kind 3 retire entries exist;
  new core NEST depthlv 1,2,3; program3: plen == 12, bytes
  `(((())))()()`, acc == 1, measD == 4; program1 string still
  w_check == 1 under Dmax 4 but measD == 3 != 4 (old
  intermediate insufficient for the new target).
- K10 X-CONTROL: without l_extract, plan_build(4,3) == -1 and
  plan node count == 0.
- K11 DETERMINISM: 3/3 runs byte-identical; sha256 digests
  quoted.
- K12 ARCHITECTURE: 0 new edge types (no edges used anywhere);
  0 new MAP types (only the two primitive emit MAPs; max rlen 1
  in every arm); 0 modes, 0 bridges, 0 handlers, 0 opcodes, 0
  semantic cases; builder takes (P,D) as parameters (no
  per-target solution literals; grep-verified: no `((()))`
  byte pattern in learner.zag).
- K13 NO-DASH: worker_snippets/check_no_dash.sh passes on every
  doc file in this directory.

Verdict rule: ALL of K1..K13 PASS for COMPLETE. Any bar may be
reported as informative-negative; bars are never weakened. VOID is
terminal. If the intermediate turns out to be selected from a
researcher-shaped set rather than invented, the report downgrades
honestly instead of claiming L3.

## 9. Deliverables

NAMECHECK.md (this dir), PREREG.md (this file), gpi_world.zag,
gpi_learner.zag, gpi_driver.zag, gpi_full.zag (concatenation),
gpi_bin, gpi_compile.txt, gpi_run1.txt, gpi_run2.txt,
gpi_run3.txt (3/3 byte-identical, sha256), REPORT.md with per-bar
results, creation/reuse/revision traces, ablation numbers,
cognition lines added, and the explicit L2 vs L3 assessment.
