# REPORT: xdomain_grammar_l2 -- L2 Adaptive Reuse on Grammar to Program

Worker: Grammar-Program L2 Worker. Frozen PREREG.md committed ALONE
before implementation (commit 436998cce). Pure Zag, safebin toolchain,
pinned znc sha256
`498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`.
Zero Python invocations. Local commits only; nothing pushed.

## Verdict

**XDOMAIN-GRAMMAR-L2-COMPLETE.** K-GP-1 through K-GP-9 all PASS for
both H1 (learned typed contracts) and H2 (value-level function
composition). No partial credit needed: both mechanisms pass every
bar.

## What was tested

Grammar to program L2 adaptive reuse. The grammar (X) extracts a
licensed max program length per rule (rule 1: 2, rule 2: 4); the
program (Y) executes the canonical L-op program, returning its trace
encoding (repunit). Two sealed goals each require adapting the
grammar's licensed length, in opposite directions:

- World-E (extend): (1,93) -> 1111. Grammar learned short (L=2);
  goal needs a longer program. Learner must EXTEND to k=4.
- World-T (truncate): (2,93) -> 111. Grammar learned long (L=4);
  goal needs a shorter program. Learner must TRUNCATE to k=3.

The operators are generic: TRUNCATE rebinds the licensed length over
k in [1,L); EXTEND rebinds over k in (L,2L]. Candidate ranges are
pure arithmetic on the learned L. The parameters 4 and 3 are
discovered by exhaustive try-and-reject, never supplied.

## Kill bar results

K-GP-1 SEALED-REQUIRES-ADAPTATION: PASS. Z-E solves only via EXTEND
k=4 (TRUNCATE k=1 tried and rejected: Y(1)=1); Z-T solves only via
TRUNCATE k=3 (EXTEND k=5..8 tried and rejected: Y(5)=11111 and up).
Established by K-GP-2/3/4 below.

K-GP-2 L1-NECESSARILY-FAILS: PASS. L1-ONLY arms fail in both worlds
for both mechanisms. H1 World-E Phase 1: singles Y(1)=1, D1(1)=7;
pairs (X,Y)->11, (X,D1)->5, (D2,Y)->1, (D2,D1)->7; all miss 1111.
H1 World-T Phase 1: singles Y(2)=11, D1(2)=5; pairs (X,Y)->1111,
(X,D1)->-1, (D2,Y)->11, (D2,D1)->5; all miss 111 (the target 111 was
chosen so the unadapted single Y(2)=11 cannot solve). H2 Phase 1:
all four ordered mode pairs miss in both worlds
(E: 4/11/2/1; T: -1/1111/-1/-1 with the overflow guard firing on the
(2,2) pair).

K-GP-3 CORRECT-OPERATOR-SELECTED: PASS. H1 World-E: exactly 1
success, EXTEND k=4 (TRUNCATE k=1 and EXTEND k=3 tried and rejected).
H1 World-T: exactly 1 success, TRUNCATE k=3 (TRUNCATE k=1,2 and
EXTEND k=5..8 tried and rejected). H2 identical: (1,2,2,4) and
(1,2,1,3), each the single success among all candidates.

K-GP-4 ADAPTED-COMPOSITION-WITH-PROVENANCE: PASS. H1 TREAT arms
record Z-COMP with comp_a = adapted MAP (adapt_of=X id 0, correct
adapt_op and adapt_param) and comp_b=Y (id 1):
E: Z-PROV adapt_of=0 op=2 param=4; T: adapt_of=0 op=1 param=3.
H2 TREAT arms record VC-COMPOSE ok m1=1 m2=2 op=2 param=4 (E) and
m1=1 m2=2 op=1 param=3 (T).

K-GP-5 ABLATIONS-FAIL: PASS. ABL-X, ABL-Y, FRESH fail in both
worlds for both mechanisms with l2_on=1 (8/8 expected-fail arms).

K-GP-6 DETERMINISM: PASS. 3/3 runs byte-identical per binary.
gp_h1_bin runs: sha256
`0a8e1121fc5fb880d8f79cae4e4a2e28f6ee3fa1a32268b9c02428263db03468`.
gp_h2_bin runs: sha256
`718f09eff7406c77588f865e85d3bf2ca72a6b8934f95837151df0e5c6451f3f`.

K-GP-7 PARAMS-DISCOVERED: PASS. grep audit: 1111 and 111 occur only
in arm-harness comments and query literals (solve_z /
vc_compose_l2 calls), never in operator, candidate-range, or
composer logic. The discovered parameters 4 and 3 occur as literals
only in arm verdict checks (test oracle); candidate loops use pure
arithmetic on the learned L (k<L, k<=2*L). Training lengths (2,4)
occur only in fact-setup lines and teaching observations.

K-GP-8 NO-TEMPLATE: PASS. Zero occurrences of GRAMMAR_TO_PROGRAM or
GRAMMAR_PROGRAM in mechanism code.

K-GP-9 TOOLCHAIN: PASS. Safebin active, `which python3 python`
empty at startup and no forbidden executable invoked during the
session. Pinned znc sha256 recorded above. Pure Zag: no Python, C,
or other language in verifiers, scorers, harnesses, or analysis.

## Totals

gp_h1_bin: TOTAL 10/10 (2 TREAT PASS, 8 PASS-expected-fail).
gp_h2_bin: TOTAL 10/10 (2 TREAT PASS, 8 PASS-expected-fail).

## What this does NOT claim

- Behavior induction is not under test; X/Y/D1/D2 behaviors are
  installed as prior learning, per the H1/H2 honest boundaries.
- The rebind semantics of the adapted PARAM map (returns the
  discovered bound for the sealed query) is declared in the prereg;
  input-sensitivity of the rebound map is not claimed. What is
  claimed and shown: the learner selects the operator and discovers
  the parameter, with provenance, and every alternative is tried and
  rejected.
- Kinds are syntactic (probe_kind); no semantic kind claim.
- Expected answers used for final verification, same as the H1/H2
  lineage. Learner-owned verification remains future work.
- One domain pair, two adaptation shapes (extend, truncate). The
  novelty under test is the operators and their learner-driven
  selection, not the pair.
- 0 new modes, 0 bridges, 0 handlers, 0 new semantic cases.
  H2 modes GRAMMAR/PROGRAM are the inherited H2 capability-slot
  vocabulary.

## Files

- PREREG.md (frozen, committed ALONE in 436998cce)
- NAMECHECK.md (toolchain guard Step 0, build record, trace audit)
- gp_h1.zag / gp_h1_bin / gp_h1_compile.txt / gp_h1_run1..3.txt
- gp_h2.zag / gp_h2_bin / gp_h2_compile.txt / gp_h2_run1..3.txt
- REPORT.md (this file)

All commits local on tnn-native-lab; nothing pushed.
