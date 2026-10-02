# PREREG L3-BRIDGE: Generic construction replacing recipes

Status: PREREG-FROZEN. No implementation exists at this commit.
Parent design: `l3_bridge/L3_BRIDGE_DESIGN.md` (commit `e4f8642fc`).
Parent mechanism: Form Inventor R1-R6, INVENTOR-TESTED (commit `1b8e032c4`).
Scope: `docs/lab/research-lead/overnight-20260928/l3_bridge_impl/` only.

## 1. What is being built

A replacement for the Form Inventor's R3 construction step. The file
`bridge.zag` is derived from `form_inventor/inventor.zag` (commit
`1b8e032c4`) with the following surgical replacements. All menu machinery
(fit_const, fit_lin, fit_exc, fit_form, prior_order, verify_need, predict for
forms 0..2, true_subj/true_obj for families 0..11), the R1 failure hook
position, R4 promotion economy shape, R5 refit/strike counters, and R6
verification schedule are kept behaviorally identical.

REMOVED (deleted, not retained alongside):
- `diagnose()` signature enum and all its branches (sig 1/3/4/0).
- `build_tree(st, sig, dp)` and all three recipe branches.
- `node_count(sig)` lookup.
- Sig-keyed `novelty_check(st, sig, dp, ...)`.
- All call sites passing a signature into construction.

ADDED:
- Four generic operators (section 4.2 of design): OP_CONST_LEAF,
  OP_SPLIT_LT, OP_SPLIT_EQ, OP_PRUNE. Every `setnode` call in the new code
  occurs inside one of these four operators. No other code writes the node
  pool.
- Generic candidate generation (section 4.3): for the leaf being split,
  let v[0..m-1] be the sorted distinct subject values among the buffer
  points covered by that leaf. LT thresholds are v[1], v[2], ..., v[m-1]
  (each distinct value except the smallest; x < v[j] splits off the lower
  block). EQ values are v[0], v[1], ..., v[m-1]. Split constants are fitted
  by majority vote over covered outputs per side (first-max wins ties).
  Candidate order is frozen: for each leaf in node-index order, all LT
  candidates in increasing threshold order, then all EQ candidates in
  increasing value order.
- `construct_search(st, bs, bo, n)`: greedy hill-climbing search (section
  4.4). Starts from a single constant leaf fitted to the buffer majority.
  Each round evaluates every (leaf, operator, parameter) candidate by
  simulating the resulting tree on the buffer; applies the single move with
  the largest strictly positive gain; ties broken by candidate order (LT
  before EQ, lower leaf index first, smaller parameter first). Stops when no
  positive-gain move exists, the 8-node pool cap is reached, or a frozen
  move budget of 24 moves is exhausted. Returns 1 iff the final tree exactly
  fits the buffer.
- Generic behavioral novelty (section 4.5): a candidate is novel iff no
  menu form (0/1/2) and no currently live invented form achieves exact fit
  on the buffer. Menu forms are checked with `fit_form`; the live form (if
  live==3) is checked by evaluating the pre-construction saved pool on the
  buffer.
- Generic HONESTFAIL (section 4.6): if the search terminates without exact
  fit, emit HONESTFAIL and promote nothing.
- Refit (section 4.7): on world change with a live invented form, run
  `construct_search` fresh on the 4-example refit buffer in a scratch area;
  if it reaches exact fit AND the rebuilt tree is structurally equivalent
  to the live tree (same node count, same operator at each node index, same
  child pointers; constant/threshold values ignored), adopt the rebuilt
  tree and set refit_out=1; otherwise strike (strikes3++, live=-1,
  phase=0, examples kept).

## 2. Frozen scoring constants (disclosed)

- B_node = 0. Gain of a move = (buffer points correctly predicted after the
  move) - (buffer points correctly predicted before the move). A move is
  applied iff gain > 0. Rationale, disclosed: exception-learning moves fix
  few points (e.g. 1 of 40) while adding 3 nodes; any positive per-node cost
  would veto genuine exception splits and the search could not build family
  H. Complexity is controlled instead by the hard 8-node pool cap, the
  24-move budget, and the F-DEGENERATE EQ-node guard below. This is greedy
  fit-improvement search, not MDL with a node penalty; the deviation from
  the design's MDL sketch is disclosed here and frozen.
- BMAX = 40 (unchanged). Node pool cap = 8 nodes (unchanged). Move budget
  = 24 (frozen; worst case 8 nodes needs at most 7 splits, so 24 is ample
  headroom and can only bind on pathological oscillation, which would
  indicate a bug).
- F-DEGENERATE EQ-node cap = 4 (frozen; proposed value from design adopted).
  Counts nodes with op==2 (EQ) in the final promoted tree.
- Cost ceiling = 108 per family (frozen; 2x the recipe cost of 54, per
  design section 7).

## 3. Frozen cost accounting (disclosed)

Cost = (examples observed via true_subj/true_obj) + (candidate tree
simulations during construct_search). One candidate simulation = one full
evaluation of one candidate tree on the buffer = 1 cost unit. The initial
constant-leaf fit and the final tree_exact_fit gate each count as 1.
Rationale: the ceiling prices openness instead of hiding it (design
section 7).

## 4. Frozen C0-A audit M1-M4 (third-party runnable on committed source)

- M1: the tokens `sig==1`, `sig==3`, `sig==4` used as construction
  discriminators, and the identifier `node_count`, return zero hits in
  `bridge.zag` outside comments that explicitly mark deleted legacy code.
  (`build_tree` likewise zero hits outside such comments.)
- M2: the construction entry point `construct_search` accepts
  `(st, bs, bo, n)` plus budgets; it accepts no diagnosis enum. Verified by
  signature inspection.
- M3: every `setnode` call in `bridge.zag` occurs textually inside one of
  the four operator functions (OP_CONST_LEAF, OP_SPLIT_LT, OP_SPLIT_EQ,
  OP_PRUNE). Verified by inspection; no function writes a whole tree.
- M4: `teval` is byte-identical to the INVENTOR-TESTED commit `1b8e032c4`
  version and still dispatches only on operator codes 0..3.

Any M-check failure voids the C0-A claim for the build. The builder may not
narrow this audit. A failed audit is a falsification.

## 5. Frozen test battery

Families 0..11 keep the exact true_subj/true_obj definitions from commit
`1b8e032c4`. Family 12 (T-ADV4) is new and frozen here:

- true_subj(12,i) = 12000 + i.
- true_obj(12,i): if i<5 { if i==2 return 9; return 0; } return 5.
- This is a step (0 for i<5, 5 for i>=5) with one embedded exception
  (i=2 maps to 9). The old recipes cannot build it: diagnose() on its
  buffer returns 0 (not two clusters, not three clusters, not exactly two
  isolated exceptions), so the old code HONESTFAILs by construction. The
  search must build IF(x<T, IF(x==p, 9, 0), 5): 7 nodes, 1 EQ node.

Battery expectations (frozen; K2 gate uses bounds, not exact values):

- R-G (fam 6), R-K (fam 10), R-H (fam 8), fresh: adopted=3, promoted=1,
  cost <= 108, EQ nodes <= 4, exact fit on the 40-point buffer.
- R-J (fam 9), fresh: adopted=-1, promoted=0 (HONESTFAIL; no promotion).
- R-REFIT: retained sequence A,B,C,D,E,G,Gp,H,G2 on one persistent state,
  in that order. Menu families A-E adopt form 1. G invents (adopted=3).
  Gp refits (refit_out=1; the rebuilt step tree is structurally equivalent
  to the live step tree). H strikes at refit (refit_out=0; the rebuilt
  tree is not structurally equivalent to the live step tree) then
  re-invents (adopted=3, promoted=1). G2 adopts menu form 2 at n=6 after
  the H-form strike (adopted=2).
- T-ADV4 (fam 12), fresh: adopted=3, promoted=1, cost <= 108, exact fit,
  EQ nodes <= 4, node count <= 8, and the built tree is NOT behaviorally
  identical to any menu form (F-MENU-REDUCIBLE guard).
- Menu controls: families 0..4 adopt form 1 (costs unchanged from
  INVENTOR-TESTED: 20/11/8/6/5); family 7 (G2) fresh adopts form 2. The
  invention hook must never fire where a menu form fits (BMAX reached
  without invention on A-E and G2-fresh).

## 6. Frozen falsifiers

- F-RECIPE: any M1-M4 failure, or discovery that any construction branch
  keys on a diagnosis value.
- F-NOVEL-FAIL: T-ADV4 not built within budget (cost > 108, or no exact
  fit, or node cap exceeded).
- F-DEGENERATE: any promoted tree uses more than 4 EQ nodes.
- F-COST: any of R-G/R-H/R-K/T-ADV4 exceeds cost 108.
- F-MENU-REDUCIBLE: the T-ADV4 solution is behaviorally identical to a
  menu form on inputs 12000..12039.

## 7. Kill bars for this build

- K1: this prereg frozen (M1-M4, battery, falsifiers) BEFORE any
  implementation commit. Satisfied by this file's commit.
- K2: bridge implemented; battery expectations of section 5 met.
- K3: C0-A audit M1-M4 passes on the committed `bridge.zag`.
- K4: pure Zag (no Python anywhere including scratch/diagnostics), no em
  dashes in loop documentation, deterministic (byte-identical output
  across 3 runs).

Builders report BRIDGE-TESTED or BRIDGE-BLOCKED with the falsifier that
fired. No SURVIVES claim is made here: C0-C (independent post-freeze
adversary) and C0-D (cognitive reuse) remain open promotion-pipeline steps
per the design section 8.
