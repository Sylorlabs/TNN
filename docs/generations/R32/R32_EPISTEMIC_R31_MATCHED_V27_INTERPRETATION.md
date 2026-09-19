# R32 V27 — Matched Cost-to-Regret Utility Envelope

Status: **REFERENCE_ONLY / UTILITY-SCALE MISMATCH CONFIRMED / NO RUNTIME CHANGE**

V27 held every evidence trajectory, persistent hypothesis state, provenance relation, terminal regret value, and action availability fixed. The only varied quantity was the scalar conversion from experienced observation cost into terminal-regret utility.

At **zero observation cost**, every resolvable episode that actually needed more evidence had a beneficial reusable consequence probe (**1.0000**), while genuine no-unique episodes still had no beneficial probe (**0.0000**). This shows that the retained evidence action and temporal hypothesis representation can resolve the constructed cases when resource cost is removed; the V26 failure is not simply that the observation contains no information.

At the current cost scale **1.0**, only **0.5752** of needed resolvable cases justify another observation. The worst dynamic mode is only **0.1169**. No-unique and costly cases correctly remain non-beneficial, but replacement/reversal are over-penalized before sufficient evidence can accumulate.

At cost scale **0.5**, needed-resolvable benefit rises to **0.8072**, while costly-case benefit remains **0.0938** and no-unique remains **0.0000**. The best separation occurs at **0.55**, with resolvable-minus-costly separation **0.7680**. A diagnostic feasible interval exists from **0.50 to 0.65**.

## Causal classification

**Utility/evaluator normalization is causal.** Candidate-selected data and pairwise ranking were not sufficient in V26 because raw observation cost was subtracted on a scale that makes multi-trial replacement/reversal economically negative. V27 demonstrates a nonempty cost envelope that preserves explicit UNKNOWN for no-unique cases and rejection of genuinely expensive evidence while making most needed ordinary observations rational.

This does **not** authorize hardcoding 0.5 or 0.55. Those values are evaluator diagnostics, not learned cognition. A fixed scalar selected from this battery would violate the delayed-regret requirement and would not adapt to resource pressure.

## Decision

- Retain the V17/V25 persistent temporal and provenance representation.
- Retain reusable grounded consequence probes and candidate-selected development.
- Reject raw-cost subtraction at scale 1.0 as an unqualified utility conversion.
- Do not promote any fixed multiplier.
- Next mechanism: learn a **resource shadow price** from delayed opportunity loss under varying budgets. The learner must map experienced resource consumption to future utility loss, then use that learned cost in INSPECT action values. Severe budgets must suppress probing; generous budgets may permit it. No ambiguity or mode label enters the learner.

R27 remains canonical. All results are REFERENCE_ONLY until native Zag qualification.
