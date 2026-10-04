# Q4 Claim Revision After Alternative-Explanation Attack

Date: 2026-09-30. Worker: Q4 Claim Reviser.
Attack result: 73d9637a2 (ATTACK-COMPLETE). This document revises the
Q4 L2/C0 claim to reflect the attack findings.

Prior claim: Q4PARCOND_RESULT.md (5f56cc491, corrected by cffc56e5b).

## K1: Valid claims identified

The following claims from the F-PARCOND result STAND, in weakened form:

1. The learner's beam found a correct general 7-op expression for
F-PARCOND (IF X1 THEN X2 XOR X3 ELSE X2 AND X3) from 32 observations,
achieving 64/64 true accuracy. This is a real measurement, not an
artifact. The expression generalizes to the unseen 8th combo correctly.

2. Phase 2 reuse: the kept D was composed as an atomic terminal in
C' = D XOR X4, reaching 64/64 with 0 interventions while scratch
reached only 52/64 in 24 interventions. The reuse ratio 0.0 is a real
measurement.

3. C0-C first data point: F-PARCOND was designed by an independent
adversary post-freeze (b4e9b6a14). The learner's mechanism solved an
adversary-selected family it had never seen. This measurement is real,
though its interpretation is narrowed (see K2).

4. C0-D pairing: the reuse measurement (0 vs 24 interventions, 64/64 vs
52/64) is a real demonstration that a kept structure improves later
cognition. The operationalization is thin (see K2), but the numbers
stand.

5. Pro-learner finding from A1b: the 24 interventions were epistemically
necessary. Passive-8 evidence alone leaves 8 tied behaviors (TIES=8,
first-top 56/64). The active evidence-gathering component, whatever its
policy quality, did necessary work.

## K2: Weakened claims specified

The following claims FALL or are materially weakened:

1. "The learner discovered F-PARCOND structure" as a ROBUST discovery
claim. The 32 observations underdetermine the target: they cover only
7/8 input combos, so two behaviors tie at 32/32 evidence fit. The
beam's 64/64 came from evidence plus the researcher-authored 200/opc
simplicity tax plus single-seed luck. On a fresh seed (SEED=33) with
the same 7/8 coverage, the beam preferred a 2-op WRONG expression
(32/32 evidence, 56/64 true). On SEED=55, outright fit failure
(23/32, 40/64). The simplicity tax does not systematically recover
truth from underdetermined evidence. The discovery headline does not
survive step 6 intact.

2. The disagreement-IV "active" component. RANDIV (deterministic random
interventions, same 24-round budget) reached 32/32 evidence fit with a
5-op expression and 64/64 true accuracy, matching the learner's
accuracy with fewer ops. The disagreement-driven intervention policy
shows no advantage over random at this budget. It is decorative.

3. The "minimal 7-op" language. A 5-op solution was found by RANDIV.
An analytic 4-op form exists: D = (x1 ^ (x2 & x3)) & (x2 | x3),
verified on all 8 combos. The K2 bar (opc <= 7) was calibrated to the
known 6-op reference plus one; a natural compactness bar of <= 5
would have failed the original 7-op run. The bar is calibrated to the
known answer.

4. The implication that the evidence determined the answer. It did not:
the evidence admitted two tied behaviors, and the researcher-authored
simplicity tax selected between them. On the preregistered seed it
selected correctly; on SEED=33 it selected a 2-op wrong answer. The
"discovery" of the 8th combo's value is attributable to the
researcher's MDL bias, not to learning.

5. C0-C interpretation narrowed. The mechanism is byte-identical
between training families and F-PARCOND; the beam enumerates
expressions over the frozen functionally-complete vocabulary
{AND, OR, NOT, XOR}. The adversary's independence is real, but the
test as operationalized cannot distinguish "adapted to a new form"
from "the frozen vocabulary covered it." D has a compact 4-op form,
so "conditional computation" is one reading of a simple 3-bit
Boolean function.

6. C0-D operationalization is thin. Phase 2 installs the learner's
own learned D signature (which happened to be exactly the true
behavior) as an atomic terminal, then tests one-step composition.
This is composition given a perfect component, not re-derivation.
The 0-vs-24 comparison inherits the single-seed luck documented
above.

## K3: Revival criteria defined

The discovery claim could be revived by meeting ALL of the following,
preregistered before implementation:

R1. Multi-seed robustness: the beam reaches true 64/64 on at least 4
of 5 fresh preregistered seeds, with the intervention policy achieving
8/8 combo coverage on each seed. This defeats the underdetermination
reading: if the evidence covers all combos, the evidence (not the tax)
determines the answer.

R2. No compact analytic alternative: the discovered form must have no
known expression at or below half its operator count that the frozen
vocabulary could also express. This defeats the vocabulary-coverage
reading: if the target is genuinely complex, coverage alone does not
explain the solve.

R3. Imperfect-component reuse: the reuse test must use a component
that is correct but non-minimal, or that must be re-derived under
changed surface conditions, rather than installing an exact terminal.
This thickens the C0-D operationalization beyond composition-given-a-
perfect-part.

R4. Active-policy advantage: the disagreement-IV policy (or its
successor) must beat random interventions on a preregistered metric
(e.g., combo coverage per intervention, or seeds-to-criterion) by a
preregistered margin. This revives the "active" component or retires
it honestly.

Until R1-R4 are met, the honest Q4 claim is: bounded L2 structural
learning with a real adversary-family solve and a real reuse
measurement, where the discovery component is underdetermined-evidence
plus researcher-authored simplicity bias plus single-seed luck, and
the active-intervention component is decorative at the tested budget.

## Governance

- Revision only. No implementation, no new measurements.
- Zero Python used (read/grep/git only).
- Zero em dash bytes (byte-verified).
- This revision does not alter any committed result; it reinterprets
the claim those results support.

Verdict: REVISED
