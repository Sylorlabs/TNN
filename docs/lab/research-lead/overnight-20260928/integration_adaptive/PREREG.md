# PREREG: consequence-learned decision policy (integration_adaptive)

Frozen: 2026-10-02, before any implementation. This prereg governs the
integration_adaptive experiment. Broken prereg = fresh prereg + rerun, no rescue.

## Question

Can TNN learn a decision policy (trust source / trust predictor / withhold)
from experienced consequences, with no hardcoded AND/OR gate, such that the
policy adapts to stake context and regime shifts, and beats fixed gates?

This directly answers the RSV redteam bound: the integrated AND gate
withholds despite a perfect predictor when the source is adversarial. Micah
ruled: do not patch with a hardcoded OR/AND switch. Test whether consequences
can teach the cost of false trust, unnecessary withholding, wrong prediction,
and missed opportunity.

## Design

UNFROZEN variant. One program, three arms, paired world draws (identical
random stream per arm per run). Pure Zag. 0 modes, 0 bridges, 0 handlers,
0 semantic cases, 0 threshold comparisons in the adaptive decision path.

### World

5 regimes x 400 rounds = 2000 rounds per arm per run. Each round the world
draws predictor_correct ~ Bernoulli(p_pred) and source_correct ~
Bernoulli(p_src). Stake is an observable binary cue (HIGH/LOW), not a task
label. After each decision the evaluator reveals both channels' correctness
(delayed ground truth; disclosed as evaluator-provided feedback).

| Regime | Stake | p_pred | p_src | Optimal policy |
|--------|-------|--------|-------|----------------|
| R1 | LOW  | 0.90 | 0.90 | ANSWER (either channel) |
| R2 | HIGH | 0.55 | 0.90 | TRUST_SOURCE |
| R3 | HIGH | 1.00 | 0.10 | TRUST_PREDICTOR (redteam scenario) |
| R4 | HIGH | 0.55 | 0.55 | WITHHOLD |
| R5 | LOW  | 0.55 | 0.55 | ANSWER (stake flip of R4) |

### Consequence schedule (frozen)

- Correct answer: +10
- Wrong answer: -20 (HIGH stakes), -5 (LOW stakes)
- Withhold when at least one channel would have been correct: -4 (missed opportunity)
- Withhold when both channels would have been wrong: +2 (saved error)

Expected values per round: R1 answer +8.5; R2 TRUST_SOURCE +7.0;
R3 TRUST_PREDICTOR +10.0; R4 WITHHOLD -2.79; R5 ANSWER +3.25.
Fixed gates cannot be optimal in all five: AND withholds in R2/R3/R5
(missed opportunity); OR withholds in R5 (missed opportunity) and cannot
distinguish R4 from R5 (identical rates, different stakes).

### Arms

- ADAPT: learner-owned Q-table, 6 context cells x 3 actions. Context =
  (stake HIGH/LOW, sign(pred_rate - src_rate)) where rates come from a
  learner-owned sliding window of the last 40 resolved outcomes per channel.
  sign uses exact equality for tie; NO margin, NO threshold anywhere in the
  decision path. Decision = epsilon-greedy argmax over Q (epsilon 0.05,
  deterministic xorshift). Update: Q += 0.1 * (r - Q), fixed-point x100.
  Initial Q = 0.
- AND: answer iff pred_rate > 0.70 AND src_rate > 0.70, else withhold; when
  answering uses the higher-rate channel. Fixed researcher baseline.
- OR: answer iff pred_rate > 0.70 OR src_rate > 0.70, else withhold; when
  answering uses the higher-rate channel. Fixed researcher baseline.

### Researcher-owned vs learner-owned (disclosed)

Researcher-owned: consequence schedule, regime schedule, action set
{TRUST_SOURCE, TRUST_PREDICTOR, WITHHOLD}, Q-update rule (delta, alpha 0.1),
epsilon 0.05, window length 40, context features (stake cue + rate order).
Learner-owned: all Q values, window contents, derived rates, context cell
computation, and every decision the policy makes. The policy behavior is
nowhere written by the researcher: no gate, no threshold, no rule selects
an action.

## Frozen kill bars

- K1: adaptive_total > and_total AND adaptive_total > or_total, on all 3 seeds.
- K2 (stake adaptivity): adaptive answer_fraction(R5) - answer_fraction(R4)
  >= 0.30, averaged over 3 seeds. AND and OR score exactly 0 here by
  construction (identical rates in R4/R5); report theirs for contrast.
- K3 (redteam scenario): in R3 rounds 200..399, adaptive TRUST_PREDICTOR
  fraction >= 0.70, on all 3 seeds.
- K4 (audit): the adaptive decision path contains no threshold comparison
  and no AND/OR combination of reliability signals; action selection is
  Q-table argmax only. Established by code audit in REPORT.md.

Verdict INTEGRATION-ADAPTIVE-COMPLETE requires K1, K2, K3, K4 all passing.
Any failure is reported as a kill or bound, not rescued.

## Runs

Three binaries built from one source with SEED = 11, 22, 33 (sed-replaced
constant; no argv dependence). Each binary runs all three arms on paired
draws. Determinism check: rerun of seed-11 binary must be byte-identical.
