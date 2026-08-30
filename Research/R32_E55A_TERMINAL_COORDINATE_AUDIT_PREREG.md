# R32 E55A — Post-Continuation Terminal Coordinate Audit

Date: 2026-08-30  
Status: `PREREGISTERED NATIVE DEVELOPMENT DIAGNOSTIC — FROZEN BEFORE EXECUTION`  
Canonical: **R27 step 60,423**  
Parents: E53/E54

## Question

E53 and E54 both learned the same stable, positive-utility conservative continuation policy C. E54 started the joint terminal basis at the safe zero point, yet D still accepted zero updates. In the current joint optimizer every candidate couples a continuation refit with a terminal-coefficient refit. E55A isolates the terminal coordinate:

> After the conservative continuation policy has been learned and frozen, does the already learner-selected E52A terminal interaction basis contain any conservative full-development improvement at all?

This is a development-only diagnostic. It cannot promote R32 and does not open validation or confirmation.

## Frozen mechanism

- Full native Zag v2.
- R27 remains untouched/canonical.
- E53 conservative continuation training is reproduced on the same frozen 3,240 development episodes.
- UNKNOWN remains value 0.
- No evaluator label enters policy features.
- The learned continuation weights, bias, pair structure, and shadow price are then frozen.
- Terminal pair identities are exactly the eight E52A learner-selected pairs; no new terminal feature or pair is permitted in E55A.
- Terminal coefficients start at zero.

## Terminal coordinate test

1. Roll the frozen conservative continuation policy through all development episodes and record the reached terminal states.
2. Refit the eight E52A terminal coefficients exactly on those reached states, forward and reverse.
3. Require identical coefficients and sufficient-statistic traces.
4. Test generic damping fractions of the fitted terminal delta: 1, 1/2, 1/4, 1/8, 1/16, and 1/32.
5. Keep continuation fixed for every candidate.
6. Evaluate each candidate over the complete frozen development set.
7. A terminal candidate is admissible only if it strictly improves net delayed utility over the frozen continuation policy while keeping known success >= the original terminal control, known wrong <= control, and no-unique wrong <= control.
8. Pick the admissible candidate with highest net utility; ties prefer fewer wrong commitments then smaller coefficient magnitude.

External evaluator labels are used only to compute delayed utility and the frozen qualification constraints after decisions; they never become policy inputs.

## Interpretation

- **Accepted terminal update:** the E52A basis is useful, but E53/E54's simultaneous update geometry blocked it. Freeze the selected candidate and preregister a fresh validation of coordinate-separable joint improvement.
- **No accepted terminal update:** retire the fixed E52A terminal basis for this sequential policy. The next experiment may increase learner-owned structural capacity using a generic sparse connectivity Foundry rather than hand-selecting another ambiguity feature.

No fresh validation or confirmation world is consumed by E55A.
