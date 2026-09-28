# N5 Fork A: Magnifying-Glass Build — Design

## Task
Micah's order (2026-09-26 ~00:07 PDT): build Fork A directly, with no subagents.
Pure-Zag arbitrary-scale `(span, offset, length) → sub-span` magnification,
genuine L12 term rewriting with capture-variable binding, alongside L0–L11.

## Architecture

### Magnifier (n5_zoom)
`n5_zoom(c, sid, roff, rlen, depth, why)` validates a span `(state, offset,
length)` and logs a traced absolute sub-span address:
`ZOOM-IN S<sid> [<roff>,<roff+rlen>) depth=<d> why=<reason>`.
Every L12/L13/L14 proposal logs its zoom before firing. Zoom depth is
deliberatively selected: depth=1 for locating bound terms in a state,
depth=2 for arithmetic sub-spans (pow-dist, num-pow, juxt).

### License ladder (L0–L14)
- L0 contra-assume: PBC assumption `It is not the case that <goal>.`
- L1 given: input premises.
- L2 cite: knowledge-store definitions/theorems.
- L3 construct-expand: definition expansion.
- L4 modus ponens.
- L5 lemma: knowledge-store lemma application.
- L6 pbc-state: derived under assumption.
- L7 goal-lemmasub: goal-directed lemma.
- L8–L11: (inherited N5 machinery: universal, disjunctive syllogism, etc.)
- **L12 subst-rewrite** (NEW): genuine Leibniz term rewriting.
- **L13 arith-eval** (NEW): deterministic arithmetic normalization.
- **L14 mt-apply** (NEW): modus tollens.

### L12: Genuine substitution with capture-variable binding

L12 consumes THREE parents (all cited in the proposal):
- p1: an equality premise E (`A=B`), parsed by `n5_parse_eq`.
- p2: the target (forward: any live state; goal: the goal itself, p2=-2).
- p3: a GENERAL SCHEMA containing literal `$A` and `$B` capture variables.

The schema is the general law; the equality is its instance. L12 marks the
schema used and cites it, so the trace shows the general law, not just the
instance. No schema → no L12 (forward, goal-directed, or reverse).

**Forward L12** (`n5_prop_subst`): for each equality E (`A=B`) and each live
target T (src 3/5/6), zoom into T to locate A, replace all occurrences with
`(B)` (parenthesized via `n5_paren_rep`), emit as src=3 prop.

**Goal-directed L12** (`n5_prop_goal_subst`): locate A in the goal bytes,
rewrite to a subgoal (src=4, p2=-2). Logs `GOAL-SUBST` and
`BIND via S<e> A="<A>" B="<B>"`.

**Reverse L12** (`n5_prop_subst_rev`): when a subgoal chain normalizes to
X=X (either via L13 ARITH chain, or directly for nested substitution),
consume the equality E to establish the ORIGINAL GOAL bytes (src=3).
Logs `SUBST-REV via S<e> + S<tt> schema=S<sch>` and the binding.
This is the step that genuinely proves the goal: the trace shows E's
binding consumed, not the goal copied.

### L13: Arithmetic normalization
Deterministic byte-rewrites on equation states:
- `n5_ar_paren`: `(2k)^4` → `2^4*k^4` (power distributes over product).
- `n5_ar_numpow`: `5^3` → `125` (integer power evaluation).
- `n5_ar_juxt`: `16*k^4` → `16k^4` (juxtaposition).
- `n5_ar_divwit`: divisibility witness (for `SUBST_NOVEL4`).

Each fires only on a zoomed sub-span; the trace logs the rule and span.

### L14: Modus tollens
From `if P then Q` and `not Q`, derive `not P`.

### Soundness guards
- Symbolic goals (containing `=`, `^`, `<`, `>`) require normalized EXACT
  equality in `n3_goal_match`; bare tautologies and src=4 subgoals cannot
  directly goal-match.
- Forward L12 never rewrites src=2 (assumption) states.
- Subgoals (src=4) bypass the contradiction scan: they are proof
  obligations, not assertions, and must not discharge PBC assumptions.
- `n5_parse_eq` skips cut-word trimming for spaceless symbolic math
  (so variable `a` in `x=a+b` is not cut as the English article).

## Provenance
Every L12 proposal cites all three parents (p1=equality, p2=target,
p3=schema). The audit ledger shows lic=12, the parent triple, and the
binding log. The reverse step verifies the subgoal cites the same schema.

## Files
- `n5a.zag`: the full implementation (single file, pure Zag).
- `tests/`: minimal fixtures (SUBST_MIN1, SUBST_NOVEL1-4, SUBST_NEST1,
  SUBST_NEG1-2).
- `runs/`: byte-identical run outputs and RUNLOG.txt.
