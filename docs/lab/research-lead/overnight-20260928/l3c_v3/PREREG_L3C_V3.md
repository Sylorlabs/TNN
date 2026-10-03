# PREREG: L3C v3 Alternative-Cover Dispatch (Candidate A)

Date: 2026-09-30. Status: FROZEN. No implementation exists at commit time.
Parent design: docs/lab/research-lead/overnight-20260928/l3c_v3_design/DESIGN_V3_DISJUNCTION.md
(Candidate A, recommended). Parent mechanism: l3c_v2.zag as committed in
20705ab5a (attack copy) / 593cc5906 (round-2 result), lines 1-700
(mechanism; main section excluded).

## 1. Question

Can the L3C construction mechanism cover disjunction WITHOUT a dedicated
researcher-authored OR case, by generalizing search to minimal set cover
over the existing separator vocabulary and emitting one dispatch node with
one labeled edge per cover element, reusing the interpreter's existing
union semantics with zero interpreter change?

## 2. Frozen specification

### 2.1 Cover search (new fn disc_cover, replaces nothing)

Vocabulary: level-1 single equality atoms plus level-3 tightest-bound
inequality atoms, exactly the existing disc2 atom types. 2-conjunctions are
excluded as cover elements (a conjunction cannot be expressed by one union
edge) and remain direct-path-only. This bound is frozen, not a gap to be
patched later.

Candidate atom: matches at least one contradiction row, matches zero
target rows, and matches at least EVID_MIN=2 contradiction instances
(per-element corroboration; EVID_MIN=2 matches the existing deferred
construction bar). Candidate enumeration order is frozen: fi 0..3,
equalities first (deduped by value), then tightest-bound GE/LE per feature.

Cover: a set of candidate atoms whose instance-mask union equals all cn
contradiction rows. Minimality (Occam, frozen): the smallest cardinality
wins. Exactly one distinct minimal cover -> FOUND, atoms written to the
COVER scratch buffer (+0 ncover, atom triples at +4+i*12). Two or more
distinct minimal covers -> AMBIGUOUS_COVER withhold (k = count, existing
anti-fiat policy). None -> NONE (HONEST_FAIL, unchanged).

Search bounds (frozen, disclosed): exhaustive subset enumeration over at
most 12 candidates; cn at most 30 (bitmask). Beyond either bound the search
returns NONE. Frozen families use at most 4 candidates and cn at most 4.

### 2.2 Builder (new fn build_cover, reuses existing generic ops only)

One DISP node D. One labeled edge per cover atom, every labeled edge
targeting the shared TERM(newout). One default edge D -> deftarget (the old
leaf). Built only with op_new_node, op_mark_term, op_mark_disp,
op_new_edge, op_label_edge. No new node kind, no new edge kind, no new op.
Conservative-default routing is preserved: unseen inputs fall through all
labeled edges to the old/base class, exactly as in direct construction.

### 2.3 Control flow changes (only changes to existing code)

try_construct_root: disc2 unchanged. r==1 -> build_chain (direct path,
unchanged). r==2 -> AMBIGUOUS withhold (unchanged). r==0 -> disc_cover:
1 -> build_cover (rule repoint, built flag, rep record in the existing
rep_addr format, trace BUILT_COVER); 2 -> AMBIGUOUS_COVER withhold (rule
ambig field = k, counter 5++, trace AMBIGUOUS_COVER); 0 -> HONEST_FAIL
(unchanged).

try_refine: disc2 unchanged. dr==1 -> build_chain (unchanged). dr==0 ->
disc_cover: 1 -> build_cover with oldt repoint and edge_set_to (trace
REFINE_COVER); 2 -> REFINE_WITHHOLD (dr=2); 0 -> REFINE_WITHHOLD (dr=0,
unchanged).

### 2.4 Interpreter

UNCHANGED. featv, pred_match, select_edge, interp, trace_last_edge,
path_uses are copied verbatim from the committed v2 source. The kill bar
requires the diff of these functions against 20705ab5a to be EMPTY.

### 2.5 Trace schema (frozen)

- BUILT_COVER sig=N ncover=K
- AMBIGUOUS_COVER sig=N k=K
- REFINE_COVER sig=N edge=E ncover=K
- REFINE_WITHHOLD sig=N dr=2 (new; dr=0/1 lines unchanged)
- All existing trace lines unchanged.

## 3. Frozen predictions (mode=1)

Common: observations interleave targets first, then contradictions as
listed. Truth eval uses ground truth, not base rate.

### P1 F2 disjunction truth family (sig 702), previously 3 HONEST_FAIL

Rows: (3,0,0,7)->2 x2; (3,1,0,7)->0; (3,0,9,7)->0; (3,1,0,7)->0;
(3,0,9,7)->0. Truth: out=0 iff f1==1 OR f2==9.
Predicted trace: HONEST_FAIL (clash_n=2), HONEST_FAIL (clash_n=3),
BUILT_COVER sig=702 ncover=2 (clash_n=4).
Predicted: built_delta=1. Truth eval 4/4:
(3,1,9,7)->0, (3,0,0,7)->2, (3,5,5,7)->2, (3,1,0,7)->0.
Predicted structure: rule(702) is DISP; exactly 2 labeled edges with atoms
(1,0,1) and (2,0,9), both targeting TERM(0); exactly 1 default edge
targeting TERM(2). The blind spot is closed: F2 no longer HONEST_FAILs.

### P2 Memorization-attack world (sig 704): per-element EVID_MIN bar

Rows: (3,0,0,7)->2 x2; (3,8,8,7)->2 x2;
(3,1,2,7)->0; (3,3,4,7)->0; (3,5,6,7)->0; (3,7,0,7)->0 (each once).
Every contradiction row is distinct and uncorroborated; narrow singleton
EQ atoms exist but each covers exactly 1 instance, below EVID_MIN=2; no
tightest-bound inequality separates (values interleave with targets on
every feature).
Predicted trace: HONEST_FAIL at clash_n=2, 3, 4. built_delta=0.
Predicted structure: rule(704) still TERM(2). No spurious memorized cover
is built. This is the per-element corroboration bar firing.

### P3 Ambiguity world (sig 705): exactly two distinct minimal covers

Rows: (3,0,0,7)->2 x2; (3,2,0,7)->2 x2;
(3,1,0,7)->0; (3,5,3,7)->0; (3,1,0,7)->0; (3,5,3,7)->0.
Candidates at clash_n=4: (f1==1) covers R1 x2; (f1==5) covers R2 x2;
(f2==3) covers R2 x2. Minimal covers: {(f1==1),(f1==5)} and
{(f1==1),(f2==3)}: exactly 2 distinct minimal covers.
Predicted trace: HONEST_FAIL (clash_n=2), HONEST_FAIL (clash_n=3),
AMBIGUOUS_COVER sig=705 k=2 (clash_n=4). built_delta=0.
Predicted structure: rule(705) still TERM(2), ambig field = 2.
Symmetric evidence is honestly withheld, not composed by fiat.

### P4 Minimality world (sig 706): minimality preference bar

Rows: (3,0,0,7)->2 x2; (3,2,5,7)->2 x2;
(3,1,0,7)->0; (3,1,9,7)->0; (3,1,0,7)->0; (3,1,9,7)->0.
Candidates at clash_n=4: (f1==1) covers all 4 instances; (f2==9) covers
R2 x2. Unique minimal cover {(f1==1)}, ncover=1.
Predicted trace: HONEST_FAIL (clash_n=2), HONEST_FAIL (clash_n=3),
BUILT_COVER sig=706 ncover=1 (clash_n=4). built_delta=1.
Truth eval 4/4 (truth: out=0 iff f1==1):
(3,1,5,7)->0, (3,0,0,7)->2, (3,2,9,7)->2, (3,1,0,7)->0.
The general single atom wins over any larger cover: minimality decides.

### P5 F1 regression (sig 701): direct path unchanged

Exact rows from l3c_v2_adv (round-1 adversary): root (3,0,0,7)->2 x2,
clash (3,1,0,7)->0 x2; refine (3,1,0,9)->7, (3,1,5,9)->7; refine
(3,1,2,9)->3 x2. Predicted: built_delta=3, eval 4/4, structure D1-D2-D3
chain with labeled atoms (1,0,1), (3,0,9), (2,0,2), all DISP. The cover
fallback never fires (disc2 returns 1 at every step).

### P6 F3 regression (sig 703): direct path unchanged

Exact rows from l3c_v2_adv: root (3,0,0,7)->2 x2, clash (3,1,0,7)->0 x2;
default-edge clashes (3,0,0,9)->0, (3,0,5,9)->0. Predicted: built_delta=2,
eval 5/5, structure: D1 default edge repointed to DISP with labeled atom
(3,0,9). The cover fallback never fires.

### P7 Determinism and purity

Three runs byte-identical (run1/run2/run3 sha256 match). Zero Python.
Dash-clean markdown per check_no_dash.sh. Contaminated paper untouched.

## 4. Kill bars

K1: this prereg commit strictly precedes any implementation commit
(merge-base verified); implementation and results committed only under
docs/lab/research-lead/overnight-20260928/l3c_v3/ with explicit pathspecs.
K2: P1 built correctly with 4/4 truth eval (F2 no longer HONEST_FAIL);
P2 produces no spurious cover (3 HONEST_FAIL); P3 withholds with k=2;
P4 builds ncover=1 with 4/4; P5 and P6 regression hold exactly.
K3: interpreter diff EMPTY against committed v2; zero new semantic cases,
modes, bridges, task-specific handlers, ops, node/edge kinds; pure Zag;
dash-clean; contaminated paper untouched.

## 5. Architecture delta (ONE-SYSTEM RULE record)

To be completed at implementation: cognition source lines added (counted
by diff); new hardcoded semantic cases: 0 (predicted); new modes: 0
(predicted); new bridges: 0 (predicted); new task-specific handlers: 0
(predicted); interpreter delta: 0 lines (predicted); new interpreter ops:
0 (predicted). Learner-state structures created: multi-edge dispatch nodes
authored by the learner at runtime (F2, MIN worlds); COVER/CAND scratch
buffers are search workspace, not persistent cognitive structure. The new
machinery is the general learning operation of cover-set composition, not
a disjunction-specific case.
