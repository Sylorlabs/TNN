# L3B Residual-Growth: Result

Verdict: **L3B-GROWTH-PASS**

Frozen run of the L3B residual-growth experiment, preregistered alone at
`c5be6dfb5` before implementation. All kill bars K-RG-1 through K-RG-9 PASS.

## What was built

A Zag learner that grows new executable structure from prediction failures.
The growth machinery is generic: CREATE, CONNECT, SPLIT, MERGE on a node
store, a failure monitor (3 consecutive failures), a ring buffer of the
last 8 failures, and a fixed-vocabulary residual analyzer (EQ, MUL(q),
ADD(d), SUB(d) in fixed order, with a symbol-binding rule), applied
identically to both families. When a regularity is found over the last 3
failures, `build_expr` assembles a base-language program using only the
construction operators, and the frozen base interpreter `binterp_eval`
executes it. On contradiction (the grown relation stops holding), the old
version is retired and a new one is grown, reusing unchanged run subtrees
via SPLIT.

The base predictor (single constant branches, ci in 1..8, fires iff c0==n)
was checked computationally to be inadequate: no single branch scores more
than 1/12 on E_1..E_12 in either family (K-RG-1).

## Evidence per bar

- K-RG-1 PASS: `RG-KX1 maxA=1 maxB=1` (512 canonical singles x 12 episodes x 2 families).
- K-RG-2 PASS: TRACE-CREATE fired at LEARN ep 3 in both instances with the
  preregistered relations: inst1 rel1=EQ k1=0 rel2=MUL k2=2; inst2
  rel1=ADD k1=2 rel2=EQ k2=0. Constructor call log validated.
- K-RG-3 PASS: hiddenA=3, hiddenB=3 on sealed n in {1,4,8} and {1,5,8}.
- K-RG-4 PASS: ablations (growth disabled) scored 0 of 6 (bar allows at most 2).
- K-RG-5 PASS: 14 of 14 post-growth episodes correct (bar requires at least 10).
- K-RG-6 PASS: TRACE-RETIRE of v1 reason=contradiction; v2 built rel2=ADD
  k2=4 differing from v1 rel2=MUL k2=2; SPLIT reused the unchanged run-1
  subtree; FOLLOWUP 2 of 2 exact.
- K-RG-7 PASS: three runs byte-identical (cmp on full stdout).
- K-RG-8 PASS: pure Zag throughout, shell-only byte checks; no em dashes
  in loop documentation (worker_snippets/check_no_dash.sh).
- K-RG-9 PASS: C0-A combined audit: A1 (interpreter region has no
  dedicated relation cases and names all five ops), A2 (no
  apply_rel/COUPLED/tag 7 vocabulary in source), A3 (every logged
  constructor call validates: CREATE op 1..5, CONNECT slot 0..1, valid
  ids), A4 (interpreter generality on hand-written programs never
  produced by growth: 17, 11, 5, 15).

## C0-A semantics-location answer

Question: where are the semantics of the grown structure implemented?
Answer: in the pre-existing base interpreter `binterp_eval`, delimited by
INTERP-BEGIN / INTERP-END, which existed before any growth. The grown
structure is base-language program data (op codes 1..5, links, const
values). Growth adds no production, no semantic case, no branch, and no
dedicated vocabulary anywhere; the source audit (A1, A2) and the call-log
audit (A3) verify this mechanically.

## Notes

- This verdict is the builder-side L3B-GROWTH-PASS only. It is not an L3
  claim and does not invoke SURVIVES; the partial C0 evidence here is one
  component of a larger evaluation, per the preregistered verdict ladder.
- Implementation detail: integer arrays are byte arrays holding
  little-endian i32 cells (the established loop idiom), because the
  native compiler miscompiles `*i32` slice construction inside functions.
- Raw output: L3B_RAW.txt. Harness: run_l3b.sh. Source: l3b.zag.
  Prereg: PREREG_L3B.md (frozen alone at c5be6dfb5).
