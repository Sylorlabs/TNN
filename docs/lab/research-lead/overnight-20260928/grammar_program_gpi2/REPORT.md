# REPORT: GPI-2 Second Constraint-Family Generality Probe

## Verdict: GENERALIZES. All 14 frozen kill bars PASS.

## Mission

GPI-1 (ledger C303) proved the learner creates a construction-plan
intermediate (SEQ/PAIR/NEST vocabulary) mediating a learned
single-delimiter depth-budget constraint and an executable MAP-chain
program, then reuses and revises it; honest verdict L2-COMPLETE, L3
not claimed, C0-C failed (single constraint family). GPI-2 asks the
load-bearing question: does the SAME intermediate machinery, with
the node vocabulary FROZEN, generalize to a structurally different
constraint family, or does it break? The family: MULTI-TYPE
STACK-DISCIPLINE WELL-FORMEDNESS (three delimiter types (), [], {}
where every close must match the most recent open type; no depth
budget). Both outcomes were preregistered as publishable; a break
would have been reported as a precise invention-gap
characterization. The vocabulary was not extended and the family was
not contorted.

## Method (frozen; see PREREG.md)

Standalone pure-Zag experiment: gpi2_world.zag (environment: three
delimiter types, w_check enforcing balanced plus most-recent-open
type matching, no depth limit), gpi2_learner.zag (generic machinery
plus learned state: probe-driven extraction of the type alphabet
and the matching rule, plan builder, plan assembler, program
executor, direct-try control), gpi2_driver.zag (teaching, 6 arms,
kill-bar evaluation). One u8 state buffer per arm. No paired
constraint-to-program examples anywhere. The builder takes
(P, pattern, flat type) as parameters; no per-target solution
literals (grep-verified: the contiguous solution byte pattern
appears 0 times in all sources; the learner contains zero delimiter
byte literals).

Two implementation bugs were found and fixed during bring-up,
before the final runs (both were code defects against the frozen
design, not design changes): (1) l_extract taught one probe fact
per unordered char pair (15 facts) instead of one per ordered
probe (30 facts), failing the preregistered K1 count of 27
rejects; fixed to teach both orders. (2) The driver's d_provdump
was missing its loop increment, causing an infinite loop that
overflowed the output buffer; fixed by adding i=i+1. Neither fix
touched a frozen bar or the vocabulary.

## Results by arm

ARM-T1 (construct P=4, pattern [{},[],()], flat ()): phase 0 taught
only six alphabet observations in fixed scrambled order
[41,93,40,125,91,123] plus six primitive single-emit MAP slots.
l_extract probed all 15 unordered char pairs in both orders (30
probes): exactly three ordered pairs accepted, binding types
(40,41), (91,93), (123,125) in discovery order; then five rule
probes built from the LEARNED bindings (crossed [L0,L1,R0,R1],
[L1,L0,R1,R0], [L2,L1,R2,R1] rejected; nested [L0,L1,R1,R0] and
[L2,R2] accepted), binding MATCH=1. Pre-construction audit: plan
region 0 nodes, byte sum 0, 6 MAPs all rlen 1, 0 programs.
plan_build(4,[123,91,40],3,40) created 5 plan nodes (root SEQ id4;
NEST depthlv 1 id2 bound (123,125); NEST depthlv 2 id1 bound
(91,93); inner PAIR id0 bound (40,41); tail PAIR count 1 id3 bound
(40,41); all live=1). Assembler walked the plan into an 8-op
MAP-chain program (ops [4,2,0,1,3,5,0,1], one per primitive MAP
slot); executor ran it; output `{[()]}()`; world ACCEPT;
learner-measured depth 3, pairs 4. PLAN_OPS=31 (5 allocs + 2 NEST
visits + 8 assemble ops + 8 execute ops + 8 world-scan), exactly
the preregistered prediction.

ARM-REUSE (P=6, same pattern, same flat type): plan_build_reuse
shared plan1's core node id 2 VERBATIM (same id, live=1,
unmutated: child/next fields verified unchanged before and after)
under a new root SEQ id 6 with a new tail PAIR count 3 id 5; only
2 new nodes; provenance kind 1 (6,2). Program `{[()]}()()()`,
12 ops, world ACCEPT, depth 3, pairs 6.

ARM-ABLATE: full plan-driven T1 (PLAN_OPS=31), then plan region
wiped (byte sum 0, 0 nodes). direct_try(4,...,20000) over the
6-symbol op alphabet FOUND NOTHING: DIRECT_OPS=19995 (budget
exhausted partway through length-6 candidates; the solution lives
at length 8 among 6^8 = 1,679,616 candidates). The intermediate is
not a convenience: without it the target is unreachable inside a
20000-op budget.

ARM-NOCPLAN (PLAN_ON=0): construct fell back to direct_try with
budget 500: found=0 (DIRECT_OPS=495, budget exhausted).

ARM-FRESH (fresh learner, X learned, no plan ever built):
direct_try budget 500: found=0 (DIRECT_OPS=495).

ARM-XC: (a) without l_extract, plan_build refused (-1), 0 nodes;
(b) with extraction but pattern [200,91,40] (200 never observed,
no learned type), plan_build refused (-1), 0 nodes. Wrong
constraint is refused, never built around.

## Kill bars (frozen)

- K0 STRUCTURAL-DIFFERENCE: PASS. The run used exactly the
  preregistered family (three types, stack discipline, no depth
  budget); the (a)(b)(c) justification in PREREG.md Section 2
  distinguishes it from GPI-1 by constraint dimension
  (correspondence vs budget), plan field roles (per-node bindings
  vs level budget), and extraction task (relation vs scalar).
- K1 X-LEARNED: PASS. Bindings (70,80..85) = 40,41,91,93,123,125
  live; (70,86,1) MATCH live; (71,97) x3 accepts, (71,98) x27
  rejects; rule probes (71,95,1),(71,95,3) accept and
  (71,96,0),(71,96,2),(71,96,4) reject present; EXTRACT trace
  lines present. All values from probe outcomes.
- K2 NO-PLAN-PRE: PASS. NPLAN 0, region byte sum 0, NM 6, all
  MAPs rlen 1, NPROG 0.
- K3 CONSTRUCT: PASS. root 4 >= 0; program 0 plen 8, ops
  [4,2,0,1,3,5,0,1], bytes 123,91,40,41,93,125,40,41, acc 1,
  measD 3, measP 4.
- K4 INTERMEDIATE-CREATED: PASS. 5 nodes with the exact frozen
  Section 8 shape (all per-node tokL/tokR, live=1, root.child=2,
  root.next=3).
- K5 ABLATE: PASS. found=0 within budget 20000; DIRECT_OPS=19995
  quoted against PLAN_OPS=31. The intermediate is necessary.
- K6 NOCPLAN: PASS. found=0 within 500; plan region empty.
- K7 FRESH: PASS. found=0 within 500.
- K8 REUSE: PASS. plan2 root.child = 2 = plan1 core (exact id);
  provenance (1,6,2); 7 nodes total (2 new); core verified
  unmutated; program 12 ops `{[()]}()()()`, acc 1, measD 3,
  measP 6.
- K9 X-CONTROL: PASS. Both (a) and (b) refuse (-1), 0 nodes.
- K10 DETERMINISM: PASS. 3/3 byte-identical runs, sha256
  f12bf62b884a77e3e7d4920feb232dd220d99f6e47fd4470770e79ea7d8dc935.
- K11 ARCHITECTURE: PASS. Grep audit: pn_alloc called only with
  kinds 0,1,2 (2 SEQ, 3 PAIR, 1 NEST sites); 0 delimiter byte
  literals in gpi2_learner.zag; 0 contiguous solution-pattern
  occurrences in any source; 0 new MAP types (six primitive
  single-emit slots, max rlen 1 in every arm); 0 modes, bridges,
  handlers, opcodes, semantic cases; builder parameterized by
  (P,pattern,flat).
- K12 NO-DASH: PASS (check_no_dash.sh on NAMECHECK.md, PREREG.md;
  this report likewise verified).
- K13 COMMIT-ORDER: PASS. Prereg commit 287440073 (PREREG.md +
  NAMECHECK.md alone, pre-implementation) strictly precedes the
  implementation commit; verified from git log on tnn-native-lab.

## Generality verdict: GENERALIZES

The fixed SEQ/PAIR/NEST vocabulary handled the new family with no
break (preregistered break conditions B1/B2/B3: none fired). The
mechanism of generality, stated precisely:

1. The node format ALREADY carried per-node (tokL,tokR); GPI-1
   bound them identically on every node, GPI-2 varies them per
   node. No format change was needed to express type identity per
   part. The vocabulary had latent capacity the first family did
   not exercise.
2. NEST's execution semantics (emit open, execute child, emit
   close) enforces stack discipline for ANY binding, because each
   NEST node's close necessarily matches its own open and children
   are strictly enclosed. Cross-type well-formedness falls out of
   the tree structure; no new combinator was needed.
3. The "nested core plus flat tail" decomposition mapped cleanly:
   the target's nested type pattern became the NEST chain's
   per-level bindings; the flat type became the tail PAIR's
   binding. The depth-budget assembler check was dropped (the
   family has no depth budget); that check was assembler-side
   constraint enforcement, not node-vocabulary semantics.

What the probe did NOT show (honest limits): the builder's
decomposition STRATEGY is still researcher-designed, and the
targets are still (nested core, flat tail) shapes. A family whose
canonical solutions are not tree-decomposable this way (e.g.
requiring branching children or cross-node coordination beyond
enclosure) would be the next probe. C0-C is now PARTIAL (two
constraint dimensions) rather than failed, but there is still no
independent adversary and no sealed post-freeze worlds.

## L2 vs L3 assessment (honest, against the invention criteria)

The intermediate plan was genuinely CREATED at episode time for the
new family: it did not exist before (K2), its exact node topology
and per-node type bindings were computed from the learned
constraint plus the target pattern (open form: any (P,pattern,flat)
yields a different tree; not selected from an enumerated family),
it drove assembly and execution to world acceptance, it was reused
by node-id sharing (K8), and it was causally load-bearing (K5: the
target is unreachable without it). The per-level type bindings are
learner-computed from probe outcomes, never researcher-enumerated.

Downgrade, stated plainly: the node VOCABULARY (SEQ/PAIR/NEST) and
the builder's decomposition STRATEGY (nested core plus flat tail)
are researcher-designed, now validated across two families rather
than one. The learner did not invent the NEST combinator and did
not derive the binding strategy from failure; it instantiated a
supplied structural vocabulary with computed parameters. Against
Micah's C0: C0-A is partial (plan nodes are learner-created
persistent state, but NEST/PAIR execution semantics live in the
source); C0-B holds for topology and now for per-node bindings
(open, computed, never chosen from a finite family) but not for
the combinator set; C0-C is PARTIAL (two structurally different
constraint dimensions, still no independent adversary, no sealed
worlds); C0-D holds (reuse demonstrated, K8).

VERDICT ON THE BOUNDARY: L2-COMPLETE, with generality across two
constraint dimensions (depth-budget and type-discipline). L3 is NOT
claimed: the intermediate's topology and bindings are invented but
its combinator vocabulary and decomposition strategy are
researcher-shaped. No finite operator menu was widened (3 node
kinds throughout; the assessment above is the finding, not a
patch).

The invention gap the L3 track must close, stated concretely: the
learner must one day DERIVE the per-level binding strategy (or a
new combinator) from experience of failure, rather than
instantiating a researcher-supplied decomposition. A probe for
that: freeze the builder's strategy, give the learner a family
whose solutions the current strategy cannot express, and test
whether the learner revises the STRATEGY (not just the plan).

## Cognition lines added

1195 (gpi2_world.zag 48 + gpi2_learner.zag 619 +
gpi2_driver.zag 528). 0 new node kinds, 0 new MAP types, 0 new
edge types, 0 modes, 0 bridges, 0 handlers, 0 opcodes, 0 semantic
cases.

## Commits

Prereg (alone, pre-implementation): 287440073.
Implementation + 3/3 runs + this report: committed next on
tnn-native-lab. Local only, never pushed.
