# R32 E51A — Sequential Value Mechanism Audit (preregistered diagnostic)

Date: 2026-08-29
Status: PREREGISTERED_DIAGNOSTIC — NOT PROMOTION ELIGIBLE
Parent: main@9da6e30b29ab70b3038f5532af22d17a6c743b2b
Canonical: R27 step 60,423

## Why this exists

E51 identified continuation-versus-termination action value as the next causal question. The E50 source also preserves the earlier E45 sequential qualification harness, including a delayed recursive continuation target. Before writing another large controller, this audit tests whether two existing hard-coded restrictions are suppressing that learned continuation signal.

This audit is deliberately diagnostic. It reuses the historical E45 environment/seed structure, so it cannot promote R32 even if a treatment passes historical gates. A positive result only earns a fresh, separately preregistered native experiment with untouched seeds.

## Frozen factors

All four arms use the same E45 world generator, resource generator, state construction, terminal targets, terminal learner, consequence learner, provenance/dependence machinery, delayed utility/regret, evaluator separation, and qualification metrics embedded in the preserved E50 source.

Only two binary factors change:

1. Continuation training reachability
   - gated: update continuation value only when `learned_credit > 0` and the state is reachable;
   - ungated: update on every feasible reachable training state, so a weak initiation model cannot prevent the continuation learner from learning counterfactual delayed value.

2. Continuation decision transform
   - wrapped: preserve `e45_arm_continue_value(arm, predicted)`;
   - direct: use the learned predicted continuation advantage directly. The target is already `-observation_loss + future_best - terminal_best`, so direct mode removes hand-authored value transforms rather than adding a new rule.

## Arms

| Arm | Training | Decision value | Interpretation |
|---|---|---|---|
| A | gated | wrapped | exact historical sequential control |
| B | ungated | wrapped | tests training suppression only |
| C | gated | direct learned advantage | tests hand-coded decision transform only |
| D | ungated | direct learned advantage | minimum-hardcoding combination |

## Hypotheses

H1: If B improves over A, the initiation-credit gate is suppressing useful continuation learning.

H2: If C improves over A, the hand-coded continuation value transform is degrading an already-grounded learned advantage.

H3: If D improves most strongly, the remaining sequential value learner should be simplified around direct delayed utility/regret and then re-tested with fresh seeds and a matched terminal-only control.

H4: If all four arms preserve the same no-unique terminal failure, continuation is not the immediate bottleneck in this harness; the next experiment must combine a safer terminal learner with sequential continuation rather than tune stopping again.

## Non-negotiable boundaries

- No evaluator mode, truth, ambiguity label, hidden-set membership, fixed observation count, or answer key may enter policy features.
- UNKNOWN remains neutral no-commit value; no positive UNKNOWN reward is introduced.
- No threshold is tuned to the validation result.
- No result from this reused historical harness changes canonical status.
- R27 remains canonical unless a later fresh native candidate wins the full promotion battery.

## Required evidence

Each arm must:
- be generated deterministically from the same preserved source;
- compile twice with the persisted official Linux x86-64 Zag compiler;
- produce byte-identical binaries within the arm;
- preserve complete runtime output and exit code;
- report the historical no-unique, known-truth, causal completion/regret, and final qualification gates;
- retain source and binary SHA-256 values.

## Decision rule

Do not select an arm merely because aggregate utility rises. Prefer a mechanism only if it improves continuation behavior without worsening no-unique wrong commitments or known-truth performance. A historical PASS is still diagnostic only; it earns a new fresh-seed experiment, not promotion.
