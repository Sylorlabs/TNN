# PREREG: Cross-Domain Grammar to Construction (fourth pair)

## Worker

Cross-Domain Grammar to Construction Worker. Unfrozen variant only.
Frozen read-only. This prereg is committed BEFORE any implementation
(commit-order self-check).

## Question under test

Micah Battery D: GENERAL CROSS-DOMAIN COMPOSITION. Three domain pairs
already solved by BOTH H1 (learned typed contracts) and H2 (value-level
function composition) with unmodified mechanism logic:

1. navigation x aggregation (chain to count)
2. arithmetic x planning
3. causal model x intervention planning

This work: the FOURTH pair, grammar -> construction. H1 and H2
mechanism logic UNMODIFIED (only the domain behaviors change, exactly
as in the causal_interv wave). No GRAMMAR_TO_CONSTRUCTION template.

## Domain design

X: grammar parameter extraction. Facts (rule, 71, divisor): rule 1
licenses divisor 16, rule 2 licenses divisor 8. Behavior: X(rule) =
find_obj(rule, 71). X(1) = 16, X(2) = 8. This is a learned
well-formedness parameter: the divisor defines which encoded words
are valid (word v valid iff v = D*q + r with q, r in [1,7]).

Y: constraint-guided construction. Behavior: Y(D) = the smallest v =
D*q + r with q, r in [1,7] (first valid encoding under divisor D).
Y(16) = 17 (q=1, r=1). Y(8) = 9 (q=1, r=1). Genuine construction:
searches the constraint space defined by the grammar parameter.

Distractors:
- D1: extract range-hi. Facts (rule, 72, hi): D1(1) = 7, D1(2) = 5.
  Then (D1, Y): Y(7) = 8, which is not the target. Type-compatible
  but wrong.
- D2: identity. D2(v) = v. Type-incompatible in the composition
  position (or produces wrong values).

No paired X+Y training. No hint. No task label. No researcher mapping
between grammar facts and construction.

Sealed Z: (1, 93) -> 17. "Given grammar rule 1, construct a valid
word." Requires X(1) = 16 then Y(16) = 17.

Z2 / ZPRIME: (2, 93) -> 9. X(2) = 8 then Y(8) = 9.

## H1 design (mechanism UNMODIFIED from xt.zag)

probe_kind(v): 1 = NODE iff v appears as a fact subject, else 2 = NUM.
Subjects in facts: 1, 2 (rules). So rules are NODE; divisors, words
are NUM.

Learned signatures (from teaching observations only, zero literals):
- X: input rule (NODE), output divisor (NUM). sig 1->2.
- Y: input divisor (NUM), output word (NUM). sig 2->2.
- D1: input rule (NODE), output hi (NUM). sig 1->2.
- D2: input rule (NODE), output rule (NODE). sig 1->1.

Teaching: X on (1->16), (2->8); Y on (16->17), (8->9); D1 on (1->7),
(2->5); D2 on (1->1), (2->2). Each n = 2, finalize_sig sets majority.

Goal (1, 93) -> 17: kin = 1 (NODE), kout = 2 (NUM, 17 not a subject).

Predicted TREAT: singles X(1) = 16 wrong, D1(1) = 7 wrong. Pairs:
(X, Y): type 1->2, 2->2 admits; X(1) = 16, Y(16) = 17. Correct.
(D1, Y): admits; D1(1) = 7, Y(7) = 8. Wrong, rejected. (X, D2),
(D1, D2): type-rejected. (D2, Y): type-rejected. Z-COMP z=4 a=0 b=1.
Tries = 4 (2 singles + 2 pairs).

Predicted NOTYPE: more tries than TREAT (contract prunes search).

Predicted ABL-X / ABL-Y / FRESH: Z-FAIL.

Predicted Z2: (2, 93) -> 9 via Z direct, tries <= 4.

## H2 design (mechanism logic UNMODIFIED from ci_h2.zag)

Modes: 1 = GRAMMAR (extract divisor via r = 71 walk, requires X
learned as capability), 2 = CONSTRUCT (build valid word, requires Y
learned as capability). Ordered mode pairs tried; pair discovered.

Predicted TREAT: (1, 1): grammar(1) = 16, grammar(16) = -1 (no
r = 71 fact from 16; stage2 needs -2 to skip cleanly... see note).
(1, 2): grammar(1) = 16, construct(16) = 17. Correct. VC-COMPOSE ok
m1 = 1 m2 = 2.

Note: grammar_exec on a non-rule returns -2 (no fact), so (1,1)
stage2 is skipped. (2,1): construct(1)? construct requires a divisor;
construct(1) would build Y(1) = 2 (q=1,r=1: 1*1+1 = 2), then
grammar(2) = 8 != 17. Wrong, rejected. (2,2): construct(1) = 2,
construct(2) = 3. Wrong. Only (1,2) verifies.

Predicted ZPRIME: (2, 93) -> 9 via (1, 2): grammar(2) = 8,
construct(8) = 9. PASS.

Predicted ABL-X / ABL-Y / FRESH / NO-VC: all -2 as expected.

## Predicted outcomes (frozen bars)

- H1 TREAT: Z-COMP z = 4 a = 0 b = 1, ARM-RESULT PASS, tries = 4.
- H1 Z2: (2, 93) -> 9 via Z direct, tries <= 4, Z2-RESULT PASS.
- H1 NOTYPE: tries > 4 (contract prunes).
- H1 ABL-X / ABL-Y / FRESH: Z-FAIL.
- H2 TREAT: VC-COMPOSE ok m1 = 1 m2 = 2, ARM-RESULT PASS.
- H2 ZPRIME: ans = 9, ARM-RESULT PASS.
- H2 ABL-X / ABL-Y / FRESH / NO-VC: -2, PASS-expected-fail.

## Kill bars (all must hold, else verdict fails)

- K1 H1-SOLVE: PASS iff Z-COMP z = 4 a = 0 b = 1 and tries = 4.
- K2 H1-CAUSAL: PASS iff ABL-X, ABL-Y, FRESH all Z-FAIL.
- K3 H1-CONTRACT: PASS iff NOTYPE tries > TREAT tries.
- K4 H1-REUSE: PASS iff Z2 solves via Z direct with tries <= 4.
- K5 H2-SOLVE: PASS iff VC-COMPOSE ok m1 = 1 m2 = 2.
- K6 H2-CAUSAL: PASS iff ABL-X, ABL-Y, FRESH, NO-VC all -2.
- K7 H2-REUSE: PASS iff ZPRIME ans = 9.
- K8 DETERMINISM: PASS iff 3/3 runs byte-identical per binary.
- K9 NO-TEMPLATE: PASS iff grep finds no GRAMMAR_TO_CONSTRUCTION,
  no CHAIN_COUNT, and no per-MAP signature literals in mechanism code.
- K10 TOOLCHAIN: PASS iff safebin active, `which python3 python`
  empty, pure Zag, no forbidden executable invoked.

## Composition level classification (per parent directive)

This pair tests Level 1 (exact reuse): X and Y execute unchanged; Z
invokes both. Level 2 (adaptive reuse) and Level 3 (novel
intermediate structure) are NOT tested here; recorded as follow-ups.

## What this does NOT claim

- Behavior induction (how X/Y got behaviors) assumed as prior
  learning, as in all prior pair waves. Tested claim is composition
  generality.
- H1 kinds binary NODE/NUM from syntactic probe.
- H2 modes (GRAMMAR, CONSTRUCT) researcher-defined; pair discovered.
- Expected used for final verification (internal verification is a
  separate frontier).
- One pair; fourth of a planned battery.

## Verdict on pass

XDOMAIN-GRAMMAR-CONSTRUCT-COMPLETE: fourth domain pair solved by both
H1 and H2 with unmodified mechanism logic, extending the generality
pattern to grammar -> construction.
