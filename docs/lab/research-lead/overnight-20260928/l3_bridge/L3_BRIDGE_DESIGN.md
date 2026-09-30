# L3_BRIDGE_DESIGN: From Form Inventor (bounded L2) to genuine L3

Status: DESIGN-COMPLETE (design only; no implementation; no verdicts claimed).
Parent context: Form Inventor R1-R6, INVENTOR-TESTED, commit `1b8e032c4`.
Result file: `form_inventor/FORMINVENTOR_RESULT.md`, section "C0 source audit".

## 0. Mission

Design the bridge that removes the Form Inventor's dedicated
diagnosis-to-construction recipes and replaces them with generic construction
operators plus learner-driven composition search, so that the semantics of any
invented form live in learner-created persistent state and are executed by
generic machinery only. Freeze a runnable C0-A audit a third party can apply
to committed source.

This document targets C0-A (runtime-defined semantics) and C0-B (open
structural form). It does not by itself satisfy C0-C (independent post-freeze
adversary) or C0-D (cognitive reuse); those remain promotion-pipeline steps.
No L3 claim is made here.

## 1. The exact C0-A violations in the current source

File: `form_inventor/inventor.zag` (commit `1b8e032c4`).

1a. `diagnose()` returns a signature enum, sig in {1, 3, 4, 0}, through
dedicated branches: two contiguous constant clusters (sig=1), three contiguous
constant clusters (sig=4), majority default plus exactly two isolated
exceptions (sig=3, with the count hard-coded as `ne!=2`), else 0.

1b. `build_tree(st, sig, dp)` selects a complete construction recipe by
signature: `if(sig==1)` writes a fixed 4-node tree; `else if(sig==4)` writes a
fixed 7-node tree; `else` writes a fixed 7-node tree built from `==` nodes
(the sig=3 recipe). Three complete topologies, chosen by a pre-training key.

1c. `node_count(sig)` is a lookup: sig==1 returns 4, otherwise 7. The size of
the invented form is decided before training, not discovered.

1d. `novelty_check(st, sig, dp, ...)` applies per-signature novelty logic
(threshold validity for sig=1/4, point distinctness for sig=3).

1e. Call sites pass the signature into construction:
`build_tree(st,isig,idp)` with `node_count(isig)` at invention, and
`build_tree(st,rsig,rdp)` at refit.

Asked "where are the semantics of the invented step/exception/cluster forms
implemented?", the honest answer today is "in dedicated branches written
before training." Under the strict reading of C0-A, that kills the L3 claim.
Every branch listed above must go.

## 2. What is already C0-A compliant (keep unchanged)

2a. `teval`: a generic recursive tree evaluator dispatching only on operator
codes 0..3 (const, less-than, equals, if-then-else). It contains no per-form
case. This is the correct shape for C0-A: one generic interpreter over
learner-created bytes, analogous to instruction dispatch.

2b. The node pool lives in persistent learner state (offsets 52..179, 8 nodes
of 16 bytes), with `live_sig`, `uses3`, `strikes3` counters beside it.

2c. `setnode` and `tree_exact_fit` are generic: a meaning-agnostic graph edit
and a behavioral fit check.

2d. The R4 promotion economy, R5 refit/strike logic, and R6 verification
halving schedule operate generically over the pool. Their control flow never
keys on a form identity.

The bridge keeps 2a-2d and replaces everything in section 1.

## 3. Bridge principle

Source may contain:
- generic execution machinery (the `teval` interpreter),
- generic construction operators (parameterized local graph edits),
- a generic search loop (propose, score, accept),
- generic scoring (fit gain versus description cost).

Source must not contain:
- any branch selecting a complete construction recipe keyed by a diagnosis
  value,
- any template or array enumerating complete tree topologies,
- any lookup from a diagnosis value to node count, structure, or parameters.

Learner state must contain: the node pool bytes (the invented form's
semantics), all fitted constants and split points, and the construction trace.
If the state bytes are wiped, no invented form remains. That is the C0-A test.

## 4. The new construction algorithm

### 4.1 Residual-facts interface (replaces the signature enum)

`diagnose()` is replaced by `residual_facts()`. Given the failure buffer (the
points where the best menu form fails), it returns no enum and no code that
construction can switch on. It returns the residual buffer itself: the failing
subject values, their observed outputs, and the per-point residual. The menu
form identity that failed may be logged to the trace for observability, but
construction control flow must not branch on it. There is deliberately no
value in this interface that selects a recipe, because there are no recipes.

### 4.2 Generic construction operators

Each operator performs one local, meaning-agnostic graph edit on the node
pool, parameterized only by learner-computed values:

- OP_CONST_LEAF(node, c): set a leaf to constant c, where c is fitted from
  buffer data by the generic constant fit.
- OP_SPLIT_LT(node, t, c_then, c_else): replace a leaf with
  IF(x < t, c_then, c_else); t and the constants are learner-fitted.
- OP_SPLIT_EQ(node, v, c_then, c_else): replace a leaf with
  IF(x == v, c_then, c_else); v and the constants are learner-fitted.
- OP_PRUNE(node): collapse a subtree to its fitted constant (used by the
  refit economy to shrink stale structure).

No operator knows about steps, clusters, or exceptions. `setnode` remains the
only primitive that writes the pool, and every `setnode` call in the new code
must occur inside one of these four operators.

### 4.3 Candidate generation (generic, from residual data)

Candidates are proposed from the residual buffer by generic change-point
machinery, not by form templates:

- LT thresholds: midpoints between consecutive distinct sorted subject values
  in the residual buffer.
- EQ values: distinct subject values appearing in the residual buffer.
- Constants: fitted per side by a generic constant fit (majority vote over the
  buffer outputs covered by that side).

This proposes splits wherever the data changes. It does not know which named
form, if any, will result. With BMAX=40 the candidate set per leaf per round
is bounded (at most 39 LT midpoints, 40 EQ values).

### 4.4 Search loop (replaces `build_tree`)

`construct_search(st, buffer)`:

1. Initialize: a single constant leaf fitted to the buffer majority.
2. Loop: for each leaf node, for each operator in 4.2, for each candidate
   parameter from 4.3, compute the MDL gain:
   gain = (residual bits saved by the move) - (B_node bits per added node),
   with B_node a frozen, disclosed constant.
3. Apply the single best positive-gain move. Append the move to the
   construction trace in learner state.
4. Stop when no move has positive gain, or the 8-node pool cap is reached,
   or a frozen move budget is exhausted.
5. Gate promotion on the unchanged generic `tree_exact_fit`.

Node count, topology, and operator mix emerge from search. Nothing is looked
up. The old `node_count(sig)` disappears entirely.

### 4.5 Generic novelty (replaces sig-keyed `novelty_check`)

A candidate is novel iff no existing form (menu forms 0/1/2 and the currently
live invented form, if any) achieves exact fit on the buffer. This is a
behavioral check, identical for every candidate, with no per-signature logic.

### 4.6 Honest failure (generic)

If the search terminates at the constant leaf without reaching exact fit, the
learner emits HONESTFAIL and promotes nothing. Same observable behavior as
family J today, reached by a generic mechanism instead of the sig=0 path.

### 4.7 Refit and revision (R5/R6 keep their shape)

On world change, refit calls `construct_search` fresh on the new buffer
instead of `build_tree(st, rsig, rdp)`. Strikes, uses counters, the halving
verification schedule, and the construction trace are unchanged; they already
operate generically over the pool.

## 5. Worked sketch (what the search does on known families)

- Family G (step): search starts from the constant leaf; the best first move
  is OP_SPLIT_LT at the change midpoint; exact fit; 4 nodes; promotes. Same
  outcome the old sig=1 recipe produced, reached by search.
- Family K (three clusters): two nested OP_SPLIT_LT moves; 7 nodes.
- Family H (two isolated exceptions): nested OP_SPLIT_EQ moves; 7 nodes.
- Novel family (four contiguous clusters): three nested OP_SPLIT_LT moves;
  7 nodes total (root IF + 2 nested IFs + 4 const leaves), inside the 8-node
  cap. The old code could not build this at all: no recipe exists for it.
- Novel family (step with an embedded exception):
  IF(x < T1, IF(x == p, e, v0), v1); 7 nodes (root IF + LT + nested IF + EQ +
  3 const leaves). Also unbuildable by the old recipes, which never mix `<`
  and `==` in one tree.

The last two are the C0-B content: topologies outside the old finite menu,
assembled node by node.

## 6. C0-A audit (frozen; runnable by a third party on committed source)

### 6.1 Audit questions

- A1: "Where are the semantics of the invented form implemented?" Required
  answer: "In learner-created bytes in the node pool, executed by the generic
  `teval` interpreter." Any answer of the form "in this dedicated branch
  written before training" fails the audit.
- A2: "Does any source branch select a complete construction recipe?" Required
  answer: "No."
- A3: "Is the final topology enumerable from source before training?"
  Required answer: "No. Node count, topology, and operator mix are outcomes of
  the search in section 4.4."

### 6.2 Mechanical checks

- M1: the legacy signature constants used as construction discriminators
  (`sig==1`, `sig==3`, `sig==4` selecting construction, and `node_count(sig)`)
  return zero hits in the committed source outside deleted legacy code.
- M2: the construction entry point accepts the failure buffer and budgets; it
  accepts no diagnosis enum. Verified by signature inspection of
  `construct_search`.
- M3: every `setnode` call in committed source occurs inside one of the four
  operators of section 4.2. Verified by inspection; no template writes a whole
  tree.
- M4: `teval` is unchanged from the INVENTOR-TESTED commit and still
  dispatches only on operator codes 0..3.

Any M-check failure voids the C0-A claim for that build. This audit is frozen
in this document; the builder may not narrow it, and a failed audit is a
falsification, not a prompt for rewording.

## 7. Test battery (frozen)

Regression (must still reach exact fit, as today):
- R-G, R-H, R-K: exact fit required. Cost ceiling frozen at 2x the recipe
  cost: 108 per family. Rationale, disclosed: open search costs candidate
  evaluations; the ceiling prices openness instead of hiding it.
- R-J: HONESTFAIL required; no promotion.
- R-REFIT: the H-strike scenario from the INVENTOR-TESTED retained sequence;
  refit must rebuild through `construct_search` and re-promote.

Openness:
- T-ADV4: an adversary-designed family requiring a topology outside the old
  three (four contiguous clusters, or a step with an embedded exception, per
  section 5). The old code cannot build it by construction. The search must
  reach exact fit within the 8-node cap and the cost ceiling.

Controls: menu families A-E unchanged; the construction hook must never fire
where a menu form fits.

### 7.1 Falsifiers (frozen)

- F-RECIPE: any M-check failure in section 6.2, or discovery that a
  construction branch keys on a diagnosis value.
- F-NOVEL-FAIL: T-ADV4 not built within budget.
- F-DEGENERATE: the built tree on a cluster family uses more than a frozen cap
  of EQ nodes (memorization guard; exact cap frozen at build prereg, proposed
  value 4).
- F-COST: any regression family exceeds cost 108.
- F-MENU-REDUCIBLE: the T-ADV4 solution is behaviorally identical to a menu
  form on the full input range.

## 8. Feasibility assessment (K3; honest)

Feasible. The generic evaluator and the node pool already exist and are
already C0-A compliant. The search is a small greedy loop; candidate
generation is bounded by the buffer (BMAX=40); rounds are bounded by the
8-node cap; each candidate evaluation is a buffer scan through `teval`. The
expected cost inflation over the recipes is modest: tens of candidate
evaluations per accepted move, each linear in the buffer.

Risks, disclosed rather than minimized:

- The search may rediscover exactly the old three topologies on G/H/K. That
  still satisfies the mechanism requirement: C0-A and C0-B constrain the
  mechanism, not the empirical novelty on old families. T-ADV4 is the
  empirical novelty test, and it is the one the old code fails by
  construction.
- The search may fail T-ADV4 within budget. That falsifies this design as
  specified. The honest response is a transparently amended design (for
  example, a small beam width), not a quiet reintroduction of recipes.
- Residual researcher footprint, explicitly not removed by this design: the
  operator vocabulary {const, <, ==, if} (its removal belongs to the
  OP-RECRUIT v2 track; the two designs compose, with recruitment supplying
  operators the search can then compose); the MDL node-cost constant B_node
  and the scoring rule (learner-authored scoring is future work); the budgets
  BMAX, the node cap, and the cost ceiling.

Verdict: the bridge is buildable at the frozen spec above. It genuinely
advances C0-A (no dedicated semantic case survives the audit) and C0-B (the
final topology emerges incrementally from search over an open combinatorial
space). It does not complete L3: C0-C still needs a true independent
post-freeze adversary (T-ADV4 is a step toward it, designed after this freeze
but not yet by an independent party), and C0-D needs demonstrated reuse of an
invented form improving later cognition across families. The full L3 verdict
additionally requires the 11-step promotion pipeline. Under the strict
reading, this design supplies the mechanism half of L3; the claim "L3
achieved" is not made here and must not be inferred.

## 9. Build order

1. Replace `novelty_check` with the generic behavioral novelty of 4.5; keep
   the recipes; regression gate (R-G/R-H/R-K/R-J unchanged).
2. Add the operators (4.2), candidate generation (4.3), and `construct_search`
   (4.4) alongside `build_tree`; test both paths; recipes still pass.
3. Switch the invention and refit call sites to `construct_search`; delete
   `build_tree`, `node_count(sig)`, the sig-keyed `novelty_check`, and the
   signature branches of `diagnose`.
4. Run the C0-A audit M1-M4 on the committed source before any battery run.
5. Run the frozen battery of section 7, including T-ADV4.

## 10. Kill-bar self-check

- K1 (bridge mechanism specified, removes the dedicated branches): sections
  4.1-4.7 replace every branch cited in section 1 (diagnose enum, build_tree
  recipes, node_count lookup, sig-keyed novelty, sig-keyed call sites).
- K2 (C0-A audit criterion defined): section 6 gives audit questions plus
  four mechanical checks, runnable by a third party on committed source,
  frozen against narrowing.
- K3 (honest feasibility assessment): section 8 gives a feasible verdict
  with disclosed costs, disclosed failure modes, and an explicitly bounded
  residual researcher footprint.

## 11. Relation to sibling tracks

- OP-RECRUIT v2 (learner-driven operator recruitment) removes the operator
  vocabulary footprint this design discloses in section 8. The two compose:
  recruitment invents operators, this search composes them.
- The Form Inventor's R1 failure diagnosis, R4 promotion economy, R5
  refit/strikes, and R6 verification schedule are retained unchanged in
  shape; only the R3 construction step is replaced.
- The discovery-hypothesis battery (A-D) attacks program discovery from a
  different direction; if hypothesis D (novelty retention) survives, its
  retention criterion is a candidate replacement for the greedy MDL loop in
  a later amendment.
