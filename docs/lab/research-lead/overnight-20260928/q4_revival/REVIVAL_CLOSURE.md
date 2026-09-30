# Q4 Revival Closure: REVIVAL-FAIL

Date: 2026-09-30. Worker: Q4 Revival Closer.
Plan: `290f0d061` (Q4_REVIVAL_PLAN.md), verdict rule section 7: revival
is conjunctive, R1 AND R2 AND R3 AND R4 must all PASS. ANY FAIL means
revival fails; the honest bounded-L2 claim stands; the failed R
localizes the weakness and becomes the defined next target.

## Verdict: REVIVAL-FAIL

Two conjuncts FAILED:

- R4: `8b0ede871` (R4-FAIL). F-R4 FIRED. Prereg `08c2d1f4f`.
- R1: `e40cb1b51` (R1-FAIL). F-R1 FIRED. Prereg `bea779792`.

Per plan section 7 the verdict is final and does not depend on R3 or
R2-form outcomes. There is no partial revival and no weakening of bars.

## Conjunct status

### R1: FAIL (e40cb1b51, prereg bea779792)

F-R1 fired: 0 of 5 fresh seeds meet the bar (bar: at least 4 of 5 seeds
with BOTH 8/8 combo coverage AND true 64/64). All results 3/3
byte-identical, pure Zag, zero Python.

Per-seed results:

| Seed  | Coverage | Evidence fit | True accuracy |
|-------|----------|--------------|---------------|
| 81113 | 8/8      | 24/32        | 48/64         |
| 82090 | 8/8      | 31/32        | 56/64         |
| 83067 | 8/8      | 30/32        | 56/64         |
| 84044 | 8/8      | 30/32        | 56/64         |
| 85021 | 8/8      | 30/32        | 56/64         |

Failure localization (preregistered, section 8 of the R1 prereg):

- Coverage: 8/8 on all 5 seeds. P-RAND succeeds at reaching full
  coverage within 24 rounds. Not a policy failure.
- Evidence fit: 24/32 to 31/32, never 32/32. At full coverage the beam
  fails to fit the observed evidence. This implicates the beam (the
  SEED=55 mode named in the prereg: 23/32 fit at 8/8 coverage).
- True accuracy: 48/64 to 56/64, never 64/64. No generalization.

The plan (section 1.3) expected that with 8/8 coverage the evidence
uniquely determines D and the 200/opc simplicity tax has no tie to
break, so 64/64 would be attributable to evidence plus search. The
actual outcome refutes that expectation: at full coverage the beam
cannot even fit the evidence. This is a search failure, not only a
generalization failure.

Tax-off diagnostic (mandatory, non-governing): seeds 82090, 84044, and
85021 show ties under tax-off ranking. Per the prereg, a tie at 8/8
coverage "indicates a harness or beam defect and invalidates the
seed." The beam retains multiple expressions with equal evidence fit
but different generalization, a defect signal consistent with the
evidence-fit shortfall. The verdict is 0/5 regardless.

### R2: R2-proof PASS; R2-form not run (9b206f99e, prereg 8ea3510f0)

R2PROOF-PASS. The analytic lower bound is verified: any TREE over
{AND, OR, NOT, XOR} computing 6-way parity uses at least 5 binary
operators. Five mechanical checks (V1 essentiality 384/384, V2 De
Morgan 12/12, V3 leaf arithmetic, V4 corollary, V5 tightness witness),
3/3 byte-identical runs, pure Zag. Preregistered caveat: the bound is
for trees; if a future mechanism emits DAGs with shared subexpressions,
the bound must be revisited before R2 can be claimed.

R2-form (Phase C of the plan, checks against the F-RECFOLD
hard-instance kept D: 64/64, F-NOREP pass, op count at most 9) has not
run. It awaits the F-RECFOLD evaluation result. Its outcome cannot
change this verdict.

### R3: still running (independent)

Tests reuse of the fixed 7-op D artifact beyond an installed perfect
terminal (Arms 1 and 2; Arm 3 deferred pending the structured-library
extension). Its outcome cannot change this verdict, but it stands on
its own for the independent reuse claim.

### R4: FAIL (8b0ede871, prereg 08c2d1f4f)

F-R4 FIRED. On 12 paired fresh seeds, P-DIS coverage 92 vs P-RAND
coverage 95; mean margin -0.25 vs the +0.75 dual bar; P-DIS wins 0/12
paired seeds (bar: at least 8/12); INCONCLUSIVE does not trigger
(BOTH8 = 8, below 10). 3/3 byte-identical runs, pure Zag.

The disagreement-IV policy is honestly retired. The mechanism is
passive plus random-IV discovery and the claim is updated accordingly.
R1 ran with P-RAND as named by the plan (Phase B).

## Honest bounded-L2 claim (unchanged)

Per plan section 7, the following claim from the revision (`a0cb66e15`,
Q4_CLAIM_REVISION.md) stands unchanged:

"bounded L2 structural learning with a real adversary-family solve and
a real reuse measurement, where the discovery component is
underdetermined-evidence plus researcher-authored simplicity bias
plus single-seed luck, and the active-intervention component is
decorative at the tested budget."

No partial revival. No bar weakening. No retroactive reinterpretation.

## Localized weakness: the beam/search

Two independent preregistered failures converge on the same component:

1. R4 exonerated the beam as a policy confound (coverage is a pure
   policy output), but R1 shows that even with full 8/8 coverage the
   beam cannot fit the observed evidence (24/32 to 31/32).
2. The tax-off ties at full coverage on 3 of 5 seeds indicate the beam
   retains multiple equally fitting expressions with different
   generalization, a defect signal named in the R1 prereg itself.

The defined next target is a beam/search mechanism that fits evidence
at full coverage and resolves ties honestly, rather than another
policy or another target family.

## What does NOT change

- L3 and Criterion 0 were never on the revival table (plan section 0).
  C0-A remains blocked (the beam, the 200/opc tax, and the IV policies
  are researcher-authored) and C0-B remains blocked (the closed frozen
  vocabulary {AND, OR, NOT, XOR}). R2-proof does not lift either
  blocker.
- The real measurements from the claim revision stand: the correct
  7-op F-PARCOND expression found from 32 observations on the original
  seed; Phase 2 reuse of kept D reaching 64/64 with 0 interventions
  versus scratch at 52/64 in 24; the C0-C first data point from the
  independent adversary family (b4e9b6a14); the C0-D pairing; the A1b
  pro-learner finding that the 24 interventions were epistemically
  necessary.
- R3 and R2-form, when they land, are judged by their own frozen bars
  and change only their own lanes.

## Governance

- Every R carried its own prereg; every prereg's first commit strictly
  precedes its implementation commit (commit-order self-check).
- Pure Zag at every stage: build, run, verification. Zero Python
  anywhere. Zero em/en dash bytes.
- Determinism: 3/3 byte-identical runs for R1, R4, and R2-proof.
- This closure alters no committed result and weakens no frozen bar.
  It is a verdict document only, local commits only.

Kill bars: K1 (closure complete) PASS. K2 (honest claim stated) PASS.
K3 (no overclaim) PASS.

Verdict: REVIVAL-CLOSED. The Q4 discovery claim is not revived.
