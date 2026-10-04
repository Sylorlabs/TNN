# REPORT: Grammar Constraints to Program Construction via a Created Intermediate Representation

## Verdict: GPI-1-COMPLETE. All 13 frozen kill bars PASS.

## Mission

Grammar constraints to program construction REQUIRING A NEW
INTERMEDIATE REPRESENTATION (L2/L3 boundary probe; on Micah's
high-value list; not previously done). Prior H1/H2 work proved
exact reuse of grammar to construction and was not redone. Here
X = a learned grammar constraint structure (balanced delimiters,
max nesting depth D, extracted by the learner from world probes),
and the target is an executable MAP-chain program the learner can
run, where no existing MAP encodes a construction plan. The
learner creates an intermediate construction plan, uses it to
assemble the program, executes the program, and the world accepts
or rejects. The intermediate is then reused on a second target and
revised after a constraint change, with white-box traces.

## Method (frozen; see PREREG.md + PREREG_AMENDMENT1.md)

Standalone pure-Zag experiment: gpi_world.zag (environment:
delimiter truth (40,41), Dmax, w_check, driver-only w_setdmax),
gpi_learner.zag (generic machinery + learned state: probe-driven
constraint extraction, plan builder, plan assembler, program
executor, no-intermediate direct-try control), gpi_driver.zag
(teaching, 7 arms, kill-bar evaluation). One u8 state buffer per
arm. No paired constraint to program examples anywhere. The
builder takes (P, D) as parameters; no per-target solution
literals (fixed-string grep verified: the literal `((()))`
appears 0 times in learner, driver, and world sources).

One transparent pre-implementation amendment (PREREG_AMENDMENT1):
plan linkage changed to root.child = core, root.next = tail (SEQ
executes child then next; NEST/PAIR ignore next) so the reuse arm
can share plan1's core node verbatim without mutating it; program
record carries per-program L/R bindings; ablation snapshots
PLAN_OPS after the full plan-driven construction. No bar weakened.

## Results by arm

ARM-T1 (construct P=4, exact depth 3): phase 0 taught only
alphabet observations (41 then 40, order scrambled) and the two
primitive emit MAPs. l_extract probed the world: both delimiter
orders tried, world accepted (40,41) so L=40, R=41 bound from the
verdict, not from a literal; nested probes d=0..5 gave accept for
0..3, reject for 4,5, so D=3. Pre-construction audit: plan region
0 nodes, byte sum 0, 2 MAPs with relseq length 1, 0 programs.
plan_build(4,3) created 5 plan nodes (root SEQ id4; NEST depthlv
1,2 ids 2,1; inner PAIR id0; tail PAIR count 1 id3; all tokL=40
tokR=41 live=1). Assembler walked the plan into an 8-op MAP
chain; executor ran it through MAP 0/1; output `((()))()`;
world ACCEPT; learner-measured depth 3, pairs 4. PLAN_OPS=31
(5 allocs + 8 assemble ops + 2 NEST level checks + 8 execute ops
+ 8 world-scan).

ARM-REUSE (P=6, exact depth 3, same constraint): plan_build_reuse
shared plan1's core node id 2 VERBATIM (same id, live=1,
unmutated: its child/next fields untouched) under a new root SEQ
id 6 with a new tail PAIR count 3 id 5; only 2 new nodes;
provenance kind 1 (6,2). Program `((()))()()()`, 12 ops, world
ACCEPT, depth 3, pairs 6.

ARM-REVISE (world change Dmax 3->4, target P=6 exact depth 4):
driver w_setdmax(4); learner re-probed at epoch 2 (depth 4 now
accepted) and re-extracted D=4, superseding epoch-1 facts.
plan_revise retired all 5 plan1 nodes (live=0, provenance kind 3
x5 with reason 2) and built a fresh plan (root id 10; new core
NEST depthlv 1,2,3 ids 8,7,6; tail PAIR count 2 id 9) with
provenance kind 2 (10,4). Program `(((())))()()`, 12 ops, world
ACCEPT under Dmax 4, measured depth 4. The old program1 string
re-executed: world still accepts it (acc=1) but measured depth 3
!= target 4, proving the old intermediate was insufficient for
the new target and the revision was necessary.

ARM-ABLATE: full plan-driven T1 (PLAN_OPS=31), then plan region
wiped (byte sum 0, 0 nodes). direct_try(4,3) with budget 20000
FOUND a program at DIRECT_OPS=4141. Cost ratio 4141/31 = 133x
(frozen bar >= 10). The intermediate is causally load-bearing.

ARM-NOCPLAN (PLAN_ON=0): construct fell back to direct_try with
budget 500: found=0 (DIRECT_OPS=489, budget exhausted). The
direct constraint to program jump fails.

ARM-FRESH (fresh learner, X learned, no plan ever built):
direct_try budget 500: found=0 (DIRECT_OPS=489).

ARM-XC (no extraction): plan_build(4,3) refused (-1), 0 plan
nodes. X is causally load-bearing for construction.

## Kill bars (frozen)

- K1 X-LEARNED: PASS. (70,80,40),(70,81,41),(70,82,3) live at
  epoch 1; probe facts (71,87) x4 for d=0..3, (71,88) x2 for
  d=4,5; EXTRACT trace lines present. Values from probe
  outcomes.
- K2 NO-PLAN-PRE: PASS. Plan nodes 0, region byte sum 0,
  NM=2, both MAPs rlen=1, programs 0.
- K3 CONSTRUCT: PASS. root>=0, program 0, plen 8, bytes
  40,40,40,41,41,41,40,41, acc=1, measD=3, measP=4.
- K4 INTERMEDIATE-CREATED: PASS. 5 nodes with exact frozen
  shape (root SEQ ch=2 nx=3; NEST d=1 ch=1; NEST d=2 ch=0;
  PAIRs count 1; tokL=40 tokR=41 live=1).
- K5 ABLATE: PASS. found=1, DIRECT_OPS=4141, PLAN_OPS=31,
  ratio 133 >= 10.
- K6 NOCPLAN: PASS. found=0 within budget 500; plan region
  empty.
- K7 FRESH: PASS. found=0 within budget 500.
- K8 REUSE: PASS. plan2 root.child == plan1 core id 2
  (exact); provenance REUSE (6,2); 2 new nodes; program
  `((()))()()()` 12 ops acc=1 measD=3 measP=6.
- K9 REVISE: PASS. epoch 2, (70,82,4); plan1 nodes 0..4
  live=0; SUPERSEDE (10,4) + 5 RETIRE entries; new core
  depthlv 1,2,3; program `(((())))()()` 12 ops acc=1
  measD=4; old string still world-accepted (acc=1) with
  measD=3 != 4.
- K10 X-CONTROL: PASS. plan_build=-1, 0 nodes.
- K11 DETERMINISM: PASS. 3/3 byte-identical runs, sha256
  af19e887e6fe2b11639950d7ff6157664d43bdaee62f4c42c3d75d5812246f28.
- K12 ARCHITECTURE: PASS. 0 new edge types (no edges used);
  0 new MAP types (2 primitive emit MAPs, max rlen 1 in all
  7 arms); 0 modes, bridges, handlers, opcodes, semantic
  cases; builder parameterized by (P,D).
- K13 NO-DASH: PASS (check_no_dash.sh on all docs).

## Ablation numbers (quoted)

PLAN_OPS (full plan-driven T1) = 31. DIRECT_OPS (ablated,
budget 20000) = 4141, success. Ratio = 133x. NOCPLAN/FRESH
(budget 500): DIRECT_OPS = 489, failure. The intermediate is
not a convenience: without it the same target costs two
orders of magnitude more search, and fails outright inside a
500-op budget.

## Traces

Full white-box traces are in gpi_run1.txt (== run2, run3):
EXTRACT lines, per-arm plan node dumps (id, kind, depthlv,
count, child, next, tokL, tokR, live), program records
(plen, target, epoch, acc, measD, measP, bindings, op ids),
program strings as characters, provenance log dumps
(REUSE/SUPERSEDE/RETIRE entries), op counters, and the
kill-bar table.

## Cognition lines added

1046 (gpi_world.zag 42 + gpi_learner.zag 492 +
gpi_driver.zag 512). 0 new edge/MAP types, 0 opcodes, 0
modes, 0 bridges, 0 handlers, 0 semantic cases.

## L2 vs L3 assessment (honest, against the invention criteria)

The intermediate plan was genuinely CREATED at episode time:
it did not exist before (K2 audit), its exact node topology
was computed from the learned constraint plus the target
parameters (open form: any (P,D) yields a different tree; not
selected from an enumerated family of plans), it drove
assembly and execution, it was reused by node-id sharing
(K8), and it was revised with retirement plus provenance
under a constraint change (K9). The decomposition content
(depth levels per part, pair counts per part, token bindings)
is learner-computed, never researcher-enumerated.

Downgrade, stated plainly: the node VOCABULARY (SEQ/PAIR/NEST
combinators) and the builder's decomposition STRATEGY (nested
core plus flat tail) are researcher-designed. The learner did
not invent the NEST combinator; it instantiated a supplied
structural vocabulary with computed parameters. Against
Micah's C0: C0-A is partial (plan nodes are learner-created
persistent state, but NEST/PAIR execution semantics live in
the source executor); C0-B holds for topology (open, computed,
never chosen from a finite family) but not for the combinator
set; C0-C fails (single constraint family, no independent
adversary, no sealed post-freeze worlds); C0-D holds
(reuse and revision demonstrated, K8/K9).

VERDICT ON THE BOUNDARY: L2-COMPLETE (strong structural
learning: genuinely constructed, causally load-bearing,
reused, revised intermediate). L3 is NOT claimed: the
intermediate's topology is invented but its combinator
vocabulary is researcher-shaped. No finite operator menu was
widened to make this work (3 node kinds throughout; the
assessment above is the finding, not a patch).

## Follow-ups (not authorized by this task; recorded only)

- Delimiter-pair change revision (structure/token separation
  under a token swap) as a second revision arm.
- Adversarial constraint families (non-delimiter constraints)
  to probe C0-C.
- Whether the NEST combinator itself can be learner-derived
  from SEQ+PAIR plus depth-target failure (the real L3 step).

Commits: prereg 5293381da, amendment 4754f8bdb (both alone,
pre-implementation). Implementation + runs + this report to be
committed next. Local only, never pushed.
