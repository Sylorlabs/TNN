# REPORT: GPI-3 Conjunctive Constraint-Family Generality Probe

## Verdict: GENERALIZES. All 15 frozen kill bars PASS.

## Mission

GPI-1 (ledger C303) proved the learner creates a construction-plan
intermediate (SEQ/PAIR/NEST vocabulary) mediating a learned
single-delimiter depth-budget constraint and an executable
MAP-chain program, then reuses and revises it; honest verdict
L2-COMPLETE, L3 not claimed, C0-C failed (single constraint
family). GPI-2 (ledger C311) proved the SAME machinery, with the
node vocabulary FROZEN, generalizes to a structurally different
family, multi-type stack-discipline well-formedness with no depth
budget; honest verdict L2-COMPLETE, GENERALIZES, C0-C partial
(two constraint dimensions, no adversary).

GPI-3 asked the next load-bearing question: does generality
COMPOSE? The family: the CONJUNCTION of the two previously
learned dimensions, multi-type stack discipline AND depth budget
simultaneously. The learner extracted both dimensions from one
probe campaign, built one plan whose per-node bindings carry the
type dimension while the restored assembler-side check enforces
the budget dimension, assembled and executed to world acceptance,
reused the core on a second target, revised under a
budget-dimension world change, and refused wrong constraints on
each dimension separately. Both outcomes were preregistered as
publishable; a break would have been reported as a precise
composition-gap characterization. The vocabulary was not extended
and the family was not contorted.

## Method (frozen; see PREREG.md)

Standalone pure-Zag experiment: gpi3_world.zag (environment:
three delimiter types, Dmax, w_check enforcing balanced plus
most-recent-open type matching plus depth <= Dmax;
driver-only w_dmax_set), gpi3_learner.zag (generic machinery
plus learned state: probe-driven extraction of the type
alphabet, the matching rule, AND the depth bound, plan builder
with budget refusal, plan assembler with restored depthlv check,
plan reviser, program executor, direct-try control),
gpi3_driver.zag (teaching, 7 arms, kill-bar evaluation). One u8
state buffer per arm. No paired constraint-to-program examples
anywhere. The builder takes (P, pattern, flat type) as
parameters; no per-target solution literals (grep-verified: the
contiguous solution byte pattern appears 0 times in all
sources; the learner contains zero delimiter byte literals).

No implementation bugs were found during bring-up: the first
compiled binary passed all in-binary bars on its first run.
No post-freeze changes of any kind were made.

## Results by arm

ARM-T1 (construct P=4, pattern [{},[],()], flat (), Dmax=3,
required depth 3 = Dmax boundary): phase 0 taught only six
alphabet observations in fixed scrambled order
[41,93,40,125,91,123] plus six primitive single-emit MAP slots.
l_extract phase A probed all 15 unordered char pairs in both
orders (30 probes): exactly three ordered pairs accepted,
binding types (40,41), (91,93), (123,125) in discovery order;
then five rule probes built from the LEARNED bindings
(crossed rejected, nested accepted), binding MATCH=1. Phase B
probed nested single-type strings L0^d R0^d for d=0..5 (built
from the learned type-0 bindings, type-valid at every depth):
accepts d=0..3, rejects d=4,5, binding Dmax=3. Pre-construction
audit: plan region 0 nodes, byte sum 0, 6 MAPs all rlen 1, 0
programs. plan_build(4,[123,91,40],3,40) created 5 plan nodes
(root SEQ id4; NEST depthlv 1 id2 bound (123,125); NEST
depthlv 2 id1 bound (91,93); inner PAIR id0 bound (40,41);
tail PAIR count 1 id3 bound (40,41); all live=1). The
assembler's restored depth check passed every NEST node
(depthlv 1,2 <= 3). Assembler walked the plan into an 8-op
MAP-chain program (ops [4,2,0,1,3,5,0,1]); executor ran it;
output `{[()]}()`; world ACCEPT; learner-measured depth 3,
pairs 4. PLAN_OPS=31 (5 allocs + 2 NEST visits + 8 assemble
ops + 8 execute ops + 8 world-scan), exactly the preregistered
prediction.

ARM-REUSE (P=6, same pattern, same flat type): plan_build_reuse
shared plan1's core node id 2 VERBATIM (same id, live=1,
unmutated: child/next fields verified unchanged before and
after) under a new root SEQ id 6 with a new tail PAIR count 3
id 5; only 2 new nodes; provenance kind 1 (6,2). Program
`{[()]}()()()`, 12 ops, world ACCEPT, depth 3, pairs 6.

ARM-REVISE (world change Dmax 3->2, target P=5, pattern
[{},[]], flat ()): pre-change plan1 built, assembled, executed
(acc=1 under Dmax 3). Driver act: w_dmax_set(2), epoch=2.
l_extract ran a FULL re-extraction at epoch 2: f_compact
retired the epoch-1 constraint model and reclaimed its fact
slots, fresh probes re-bound the unchanged type alphabet and
rule, and the depth probes now gave D=2, superseding (70,87).
plan_revise retired all 5 plan1 nodes (live=0, provenance kind
3 x5 with reason 2) and built a fresh plan (root id 8; core
NEST depthlv 1 id6 bound (123,125); inner PAIR id5 bound
(91,93); tail PAIR count 3 id7 bound (40,41)) with provenance
kind 2 (8,4). Program `{[]}()()()`, 10 ops, world ACCEPT under
Dmax 2, measured depth 2, pairs 5. The old program1 string
re-executed under the new world: world REJECTS it (acc=0,
depth 3 > Dmax 2). This is sharper than GPI-1, where the old
program stayed world-accepted: here the old intermediate's
product is now invalid, proving the revision was necessary,
not merely insufficient.

ARM-ABLATE: full plan-driven T1 (PLAN_OPS=31), then plan region
wiped (byte sum 0, 0 nodes). direct_try(4,...,20000) over the
6-symbol op alphabet FOUND NOTHING: DIRECT_OPS=19995 (budget
exhausted partway through length-6 candidates; the solution
lives at length 8 among 6^8 = 1,679,616 candidates). The
intermediate is not a convenience: without it the target is
unreachable inside a 20000-op budget.

ARM-NOCPLAN (PLAN_ON=0): construct fell back to direct_try with
budget 500: found=0 (DIRECT_OPS=495, budget exhausted).

ARM-FRESH (fresh learner, X learned, no plan ever built):
direct_try budget 500: found=0 (DIRECT_OPS=495).

ARM-XC: (a) without l_extract, plan_build refused (-1), 0
nodes; (b1) with extraction but pattern [200,91,40] (200 never
observed, no learned type), plan_build refused (-1), 0 nodes;
(b2) with extraction but required depth 4 > Dmax 3 (all types
learned), plan_build refused (-1), 0 nodes. A wrong constraint
on EITHER dimension is refused, never built around.

## Kill bars (frozen)

- K0 STRUCTURAL-DIFFERENCE: PASS. The run used exactly the
  preregistered conjunctive family (three types, stack
  discipline, AND depth budget Dmax=3); the (a)(b)(c)
  justification in PREREG.md Section 2 distinguishes it from
  GPI-1 and GPI-2 by compositionality of enforcement, not
  parameters. Neither dimension was dropped.
- K1 X-LEARNED: PASS. Bindings (70,80..85) = 40,41,91,93,
  123,125 live; (70,86,1) MATCH live; (70,87,3) DMAX live;
  (71,97) x3 accepts, (71,98) x27 rejects; rule probes
  (71,95,1),(71,95,3) accept and (71,96,0),(71,96,2),(71,96,4)
  reject present; depth probes (71,93) x4 (d=0..3),
  (71,94) x2 (d=4,5); EXTRACT trace lines present. All values
  from probe outcomes.
- K2 NO-PLAN-PRE: PASS. NPLAN 0, region byte sum 0, NM 6,
  all MAPs rlen 1, NPROG 0.
- K3 CONSTRUCT: PASS. root 4 >= 0; program 0 plen 8, ops
  [4,2,0,1,3,5,0,1], bytes 123,91,40,41,93,125,40,41, acc 1,
  measD 3, measP 4.
- K4 INTERMEDIATE-CREATED: PASS. 5 nodes with the exact frozen
  Section 8 shape (all per-node tokL/tokR, live=1, root.child=2,
  root.next=3).
- K5 ABLATE: PASS. found=0 within budget 20000;
  DIRECT_OPS=19995 (exact); PLAN_OPS snapshot=31 (exact).
  The intermediate is necessary.
- K6 NOCPLAN: PASS. found=0 within 500 (DIRECT_OPS=495
  exact); plan region still empty.
- K7 FRESH: PASS. found=0 within 500 (DIRECT_OPS=495 exact).
- K8 REUSE: PASS. plan2 root.child = 2 = plan1 core (exact
  id); provenance (1,6,2); 7 nodes total (2 new); core
  verified unmutated; program 12 ops `{[()]}()()()`, acc 1,
  measD 3, measP 6.
- K9 REVISE: PASS. epoch 2; (70,87,2) live; (70,86,1) live;
  plan1 nodes 0..4 live=0; RETIRE (3,i,2) x5 present;
  SUPERSEDE (2,8,4) present; NPLAN=9; new root 8 SEQ(child 6,
  next 7); node 6 NEST d=1 (123,125) child 5; node 5 PAIR
  count 1 (91,93); node 7 PAIR count 3 (40,41); program 1:
  plen 10, ops [4,2,3,5,0,1,0,1,0,1], bytes
  123,91,93,125,40,41,40,41,40,41, acc 1, measD 2, measP 5;
  OLD program 0 re-executed under Dmax=2: acc=0.
- K10 X-CONTROL: PASS. (a), (b1), (b2) all refuse (-1),
  0 nodes each.
- K11 DETERMINISM: PASS. 3/3 byte-identical runs, sha256
  8c7937c6110e2ab6c468ab7c4cee7c953549a23df8e544a55951913b21906cc2.
- K12 ARCHITECTURE: PASS. Grep audit: pn_alloc called only
  with kinds 0,1,2 (2 SEQ, 3 PAIR, 1 NEST sites); 0 delimiter
  byte literals in gpi3_learner.zag (93/94 are fact-rel ids,
  not byte values); 0 contiguous solution-pattern occurrences
  in any source; 0 new MAP types (six primitive single-emit
  slots, max rlen 1 in every arm); 0 modes, bridges, handlers,
  opcodes, semantic cases; builder parameterized by
  (P,pattern,flat).
- K13 COMMIT-ORDER: PASS. Prereg commit 2065f8d87 (PREREG.md
  + NAMECHECK.md alone, pre-implementation) strictly precedes
  the implementation commit; verified from git log on
  tnn-native-lab.
- K14 NO-DASH: PASS (check_no_dash.sh on NAMECHECK.md,
  PREREG.md; this report likewise verified).

## Generality verdict: GENERALIZES

The fixed SEQ/PAIR/NEST vocabulary handled the conjunctive
family with no break (preregistered break conditions B1/B2/B3:
none fired). The mechanism of generality, stated precisely:

1. The two enforcement mechanisms are orthogonal in the frozen
   design: per-node (tokL,tokR) bindings plus tree structure
   determine WHICH bytes are emitted at each position (the
   type dimension), while the assembler-side `depthlv <= Dmax`
   check constrains HOW DEEP the NEST chain may go (the
   budget dimension). Neither mechanism reads or writes the
   other's load-bearing field, so they composed without
   interference. The depth check that GPI-2 dropped as
   vacuous was restored without touching any node semantics.
2. The depth probes isolated the budget dimension cleanly:
   nested strings of a single learned type are type-valid at
   every depth, so probe outcomes varied only with Dmax. The
   type probes were unaffected by the budget because all
   probe strings sit at depth <= 2 < Dmax. The extraction
   sequenced the two dimensions (type first, then depth
   through the learned types) rather than probing them
   independently.
3. The builder's "nested core plus flat tail" decomposition
   was unchanged; the required depth of a target is its
   pattern length, refused against the learned Dmax before
   building. The refusal logic now guards both dimensions
   (unknown type, depth overrun).

What the probe did NOT show (honest limits): the builder's
decomposition STRATEGY is still researcher-designed, and the
targets are still (nested core, flat tail) shapes. The revise
arm changed only the budget dimension; revision under a
type-dimension change was not tested. C0-C is now less
partial (two single dimensions plus their conjunction) but
there is still no independent adversary and no sealed
post-freeze worlds. The f_compact memory management is
disclosed experiment-harness machinery, not a cognitive
claim.

## L2 vs L3 assessment (honest, against the invention criteria)

The intermediate plan was genuinely CREATED at episode time
for the conjunctive family: it did not exist before (K2), its
exact node topology and per-node type bindings were computed
from the learned two-dimensional constraint plus the target
pattern (open form: any (P,pattern,flat) yields a different
tree; not selected from an enumerated family), it drove
assembly and execution to world acceptance under BOTH
dimensions, it was reused by node-id sharing (K8), and it was
revised with retirement plus provenance under a world change
(K9), where the old product is now world-rejected. It was
causally load-bearing (K5: the target is unreachable without
it inside a 20000-op budget).

Downgrade, stated plainly: the node VOCABULARY (SEQ/PAIR/NEST)
and the builder's decomposition STRATEGY (nested core plus
flat tail) are researcher-designed, now validated across two
single dimensions plus their conjunction rather than one.
The learner did not invent the NEST combinator, did not
derive the binding strategy from failure, and did not invent
the conjunction handling: it instantiated a supplied
structural vocabulary with computed parameters, and the
conjunction worked because the two enforcement mechanisms
were designed orthogonally. Against Micah's C0: C0-A is
partial (plan nodes are learner-created persistent state, but
NEST/PAIR execution semantics and the depth-check placement
live in the source); C0-B holds for topology and per-node
bindings (open, computed, never chosen from a finite family)
but not for the combinator set or the decomposition
strategy; C0-C is PARTIAL-PLUS (three probes: two single
dimensions and their conjunction; still no independent
adversary, no sealed worlds); C0-D holds (reuse and revision
demonstrated, K8/K9).

VERDICT ON THE BOUNDARY: L2-COMPLETE, with compositional
generality across the conjunction of the two constraint
dimensions. L3 is NOT claimed: the intermediate's topology
and bindings are invented but its combinator vocabulary,
decomposition strategy, and dimension-orthogonal design are
researcher-shaped. No finite operator menu was widened (3
node kinds throughout; the assessment above is the finding,
not a patch).

The invention gap the L3 track must close, stated concretely
and unchanged from GPI-2: the learner must one day DERIVE the
per-level binding strategy, the decomposition strategy, or a
new combinator from experience of failure, rather than
instantiating a researcher-supplied decomposition. A probe
for that: freeze the builder's strategy, give the learner a
family whose solutions the current strategy cannot express,
and test whether the learner revises the STRATEGY (not just
the plan).

## Cognition lines added

1451 (gpi3_world.zag 68 + gpi3_learner.zag 748 +
gpi3_driver.zag 635). 0 new node kinds, 0 new MAP types, 0 new
edge types, 0 modes, 0 bridges, 0 handlers, 0 opcodes, 0
semantic cases. Region offsets and node field layout
identical to GPI-2.

## Commits

Prereg (alone, pre-implementation): 2065f8d87.
Implementation + 3/3 runs + this report: committed next on
tnn-native-lab. Local only, never pushed.
