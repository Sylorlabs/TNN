# REPORT: TX1 Typed Arithmetic (formal_richer)

## Verdict: FORMAL-RICHER-COMPLETE

All 7 frozen kill bars pass. 3/3 byte-identical runs
(sha256 `86fb76dcc5c8efc9df3f30999a770e6cc30af6949f377588f1d3dd34eacc29e1`).

## What was built

TX1: a typed expression language richer than EXL. Int literals,
ADD/MUL/SUB over Int (SUB admits negatives; no value<64 rule),
LT (Int,Int)->Bool introducing a distinct Bool type. The learner
induces from 8 taught BUILD examples: the licensor set, the
decomp->eval map, and the Int/Bool type partition. The induced
types are causally active in construction: each goal carries a
type ascription (0=Int, 1=Bool) and only type-matching licensors
are admissible.

## Results

- Induced grammar: `nlic=4 lic=43:t0:ev41 lic=44:t0:ev42
  lic=48:t0:ev46 lic=49:t1:ev47`. DADD/DMUL/DSUB discovered as
  Int-producing, DLT as Bool-producing. Zero relation literals
  41,42,43,44,46,47,48,49 in the induction/construction source.
- W1 INDUCE: 12/12 valid, 0 type errors.
- W2 ABLATE (grammar deleted): 0/12. Errors return.
- W3 TYPEBLIND (licensors induced, type filter removed):
  10/12 valid with exactly 2 class-6 TYPE MISMATCH errors, on
  (0,Bool) and (1,Bool), as preregistered. The type partition is
  load-bearing: without it, value-correct but ill-typed forms
  (DSUB form for a Bool goal, DADD form for a Bool goal) are
  accepted.
- W4 FRESH: 0/12.

## Kill bars (frozen in PREREG.md, Amendment 1)

K1 12/12 PASS. K2 0/12 PASS. K3 10/12 with 2 type errors PASS.
K4 0/12 PASS. K5 3/3 byte-identical PASS. K6 zero forbidden
literals PASS (grep verified). K7 nlic==4 with partition
{DADD:Int, DMUL:Int, DSUB:Int, DLT:Bool} PASS.

## Development notes (transparent)

- Dry run exposed two issues, both fixed before sealed runs:
  (a) tx_induce had non-exclusive ifs that zeroed ok when
  recording the 4th licensor; fixed to if/else.
  (b) t2_gather's value-based cycle check rejects paths whose
  fact object numerically equals the target (P(0,1)=1 vs t=1),
  making (1,43,P(0,1)) ungatherable. PREREG Amendment 1 changed
  it to (1,43,P(1,0)), committed before sealed evaluation.
- (0,43,P(0,0)) is likewise cycle-rejected; the (0,Int) Int-path
  goes via (0,48,P(5,5)), deterministic.

## Architecture accounting

459 new Zag lines (262 patch, 197 driver). 0 modes, 0 bridges,
0 handlers, 0 new semantic cases. Frozen base untouched
(byte-identical copy, sha256 verified).

## Honest boundaries

- The goal's reqtype is given as a type ascription, not induced.
  Inducing expected types from usage context is the follow-up.
- Single-link construction only; no nested expressions.
- Candidate order is gather order, not learned.
- TX1 is a stepping stone toward Zag, not Zag mastery. The next
  steps: nested forms, let-bindings, conditionals, then a Zag
  subset where syntax/type errors become architecturally
  preventable.

## Commits

- PREREG frozen alone: `35c42d000`.
- PREREG Amendment 1: `e34e63236`.
- Implementation and sealed results: this commit.
