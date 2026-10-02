# REPORT: xdomain_grammar_construct -- Fourth Domain Pair (Grammar to Construction)

## Verdict: XDOMAIN-GRAMMAR-CONSTRUCT-COMPLETE. All 10 frozen kill bars PASS.

## Mission

Test H1 (learned typed contracts) and H2 (value-level function
composition) on a FOURTH domain pair with UNMODIFIED mechanism logic,
extending the generality pattern (Micah Battery D).

Prior:
- navigation x aggregation: H1 PASS, H2 PASS.
- arithmetic x planning: H1 PASS, H2 PASS.
- causal model x intervention planning: H1 PASS, H2 PASS.
- This work: grammar -> construction. H1 PASS, H2 PASS.

## Domain

X: grammar parameter extraction. Facts (rule, 71, divisor): rule 1
licenses divisor 16, rule 2 licenses divisor 8. Behavior: X(rule) =
find_obj(rule, 71). X(1) = 16, X(2) = 8. The divisor is a learned
well-formedness parameter: word v is valid iff v = D*q + r with
q, r in [1,7].

Y: constraint-guided construction. Behavior: Y(D) = smallest v =
D*q + r with q, r in [1,7]. Y(16) = 17, Y(8) = 9. Genuine
construction: searches the constraint space defined by the grammar
parameter.

Distractors: D1 extracts range-hi via r = 72 (D1(1) = 7; then
Y(7) = 8, wrong). D2 is identity (D2(v) = v).

No paired X+Y training. No hint. No task label. No researcher mapping.
No GRAMMAR_TO_CONSTRUCTION template.

Sealed Z: (1, 93) -> 17. "Given grammar rule 1, construct a valid
word." Requires X(1) = 16 then Y(16) = 17.

Z2 / ZPRIME: (2, 93) -> 9. X(2) = 8 then Y(8) = 9.

## H1 results (gc_h1.zag, mechanism UNMODIFIED from xt.zag)

3/3 byte-identical, sha256
`2e473c137cdf588fa94fa78a9a820fb140cb804f211e7f068c95c6e9ea422965`.

Learned signatures (from probe observations only, zero literals):
- X: 1->2 (NODE->NUM). Correct.
- Y: 2->2 (NUM->NUM). Correct.
- D1: 1->2. Correct.
- D2: 1->1. Correct.

TREAT:
- Singles: X(1) = 16 wrong, D1(1) = 7 wrong. (Y, D2 skipped by type.)
- Pairs: (X, Y): X(1) = 16, Y(16) = 17. Correct.
- Z-COMP z = 4 a = 0 b = 1. Z-SIG 1->2.
- ARM-RESULT PASS tries = 3.

Z2:
- Singles: X(2) = 8 wrong, D1(2) = 5 wrong; Z(2) = 9 correct.
- Z-SINGLE m = 4. tries = 3 <= 4. Z2-RESULT PASS.

NOTYPE:
- 4 singles + 2 pairs = 6 tries > 3. Contract prunes search.

ABL-X / ABL-Y / FRESH: all Z-FAIL as expected.

## H2 results (gc_h2.zag, mechanism logic UNMODIFIED from ci_h2.zag)

3/3 byte-identical, sha256
`f7713614f8056d9555369b72c71b910fddb7cfc6d4845d986c78aa65cb555447`.

Modes: 1 = GRAMMAR, 2 = CONSTRUCT (discovered pair, not given).
Stage2 requires learned Y as capability evidence.

TREAT:
- (1, 1): grammar(1) = 16, grammar(16) = -2 (no r = 71 fact). Skipped.
- (1, 2): grammar(1) = 16, construct(16) = 17. Correct.
- VC-COMPOSE ok m1 = 1 m2 = 2. ARM-RESULT PASS.

ZPRIME: (2, 93) -> 9 via (1, 2): grammar(2) = 8, construct(8) = 9.
PASS.

ABL-X: (2, 2) gives 3 not 17; grammar stage fails. VC-COMPOSE fail.
PASS-expected-fail.

ABL-Y: construct stage refuses (no Y capability). VC-COMPOSE fail.
PASS-expected-fail.

FRESH / NO-VC: fail as expected. TOTAL 6/6.

## Kill bars

- K1 H1-SOLVE: PASS. Z-COMP z = 4 a = 0 b = 1, tries = 3 (amended).
- K2 H1-CAUSAL: PASS. ABL-X, ABL-Y, FRESH all Z-FAIL.
- K3 H1-CONTRACT: PASS. NOTYPE 6 tries > TREAT 3 tries.
- K4 H1-REUSE: PASS. Z2 via Z direct, 3 tries <= 4.
- K5 H2-SOLVE: PASS. VC-COMPOSE ok m1 = 1 m2 = 2.
- K6 H2-CAUSAL: PASS. ABL-X, ABL-Y, FRESH, NO-VC all -2.
- K7 H2-REUSE: PASS. ZPRIME ans = 9.
- K8 DETERMINISM: PASS. 3/3 byte-identical both binaries.
- K9 NO-TEMPLATE: PASS. Grep audit: only absence-declaring comments;
  sig writes only in map_new (init), finalize_sig (computed),
  promote_comp (generic contract composition). No per-MAP literals.
- K10 TOOLCHAIN: PASS. Safebin active, `which python3 python` empty
  at startup and at completion, pure Zag, no forbidden executable.

## Why this matters

Four structurally different domain pairs now solved by BOTH H1 and H2
with unmodified mechanism logic:

1. navigation x aggregation (chain to count)
2. arithmetic x planning
3. causal model x intervention planning
4. grammar x construction (this work)

This pair is the first where X's output is a *constraint parameter*
(a well-formedness rule) rather than a domain entity, and Y's input
is that constraint rather than a domain value. The mechanisms do not
care: H1 admits the pair because learned signatures chain (1->2,
2->2); H2 discovers the mode pair because the value handoff verifies.
The generality pattern now covers constraint-producing and
constraint-consuming structures.

## Composition level

This pair tests Level 1 (exact reuse): X and Y execute unchanged; Z
invokes both; ablations prove causal dependence. Level 2 (adaptive
reuse: e.g., X or Y must be rebound/extended for a new rule family)
and Level 3 (novel intermediate structure) are NOT tested here.

## Honest boundaries

- Behavior induction assumed as prior learning (same as prior waves).
- H1 kinds binary NODE/NUM from syntactic probe.
- H2 modes (GRAMMAR, CONSTRUCT) researcher-defined; pair discovered.
- The construction range [1,7] is behavior-side knowledge, not
  learned here; the tested claim is composition generality.
- Expected used for final verification (internal verification is a
  separate frontier).
- One pair per wave; four pairs total across waves.
- Small distractor set.

## Architecture accounting

- gc_h1.zag: ~330 lines (mechanism identical to xt.zag).
- gc_h2.zag: ~240 lines (mechanism logic identical to ci_h2.zag).
- 0 modes, 0 bridges, 0 handlers, 0 new semantic cases.
- Frozen TNN-2 untouched (both standalone).

## Toolchain

Safebin PATH throughout. `which python3 python` empty at startup
(NAMECHECK Step 0) and re-verified at completion. Pinned znc, exit 0
both (only benign zagd notice). Zero em/en dashes byte-verified.
Committed locally, nothing pushed.

## Deliverables

- NAMECHECK.md (Step 0 guard)
- PREREG.md (frozen b6993f039, strictly before implementation)
- PREREG_AMEND1.md (frozen 6f4138037, pre-implementation trace
  correction, try counts 3/6/3)
- REPORT.md (this file)
- gc_h1.zag, gc_h1_bin, gc_h1_compile.txt, gc_h1_run1/2/3.txt
- gc_h2.zag, gc_h2_bin, gc_h2_compile.txt, gc_h2_run1/2/3.txt
