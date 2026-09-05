# E51AJ — Post-execution interpretation review

Reviewer task label: `chatgpt web E51AJ interpretation reviewer`.
Explicit model: `chatgpt-web/pro`, effort `ultra`.
Agent ID: `01a0708d-8e6c-7d71-94a9-c3660b456b3a`; runtime nickname: Pauli.
Status: completed, read-only. Date: 2026-09-05 Pacific.

The earlier pre-execution agent was not found on attempted reuse; a fresh
ChatGPT Web reviewer was created. No Sol substitution occurred. This review
did not repeat archive/compiler verification, execute cognition, or edit files.
The main task performed the independent source/archive and raw-mask checks.

## Conclusions returned and checked against stored evidence

The reviewer confirmed the precise failed primary condition: replay must have
strictly fewer final-missing shared-anchor successes in every replica. The
sequential/replay counts 1/14 and 9/11 fail; 17/6 passes. Nonempty anchors,
ever-lost and worst-simultaneous-loss conditions pass in all three. The correct
aggregate label remains `MIXED_OR_UNREPLICATED_RETENTION_DIRECTION`.

The separate aggregate behavioral flag fails on total/known/no-unique counts
in replicas 0 and 1 and on known counts in replica 2. Initial-decision aggregate
improvements do not override those failures. Behavioral failure is separate
from integrity-valid diagnostic completion. Sources:
[frozen rules](../R32_E51AJ_REPLAY_ORDER_DOSE_PREREG.md),
[complete comparisons](TABLES.md), and [final contrasts](SECONDARY_CONTRASTS.csv).

The reviewer identified three important interpretation boundaries:

- Final recovery is not uninterrupted preservation. Replica-2 replay cohort B
  ends retaining every anchor but lost and regained four along the way. Balanced
  mixing has fewer ever-lost cases than replay in all three replicas without
  uniformly better endpoint retention. There is no metric-independent winner.
- A-only is not a data-matched order comparator. It loses 7/3/3 final anchors on
  A itself, so omission of B–D cannot by itself describe all damage. This does
  not establish the unique cause of sequential-arm losses.
- Aggregate decision improvements can hide pointwise swaps. Replica-2 A-only
  introduces 194 initial wrong commitments and removes two versus static.
  Replay versus sequential reduces wrong commitments by 350 but increases
  unsuccessful UNKNOWN choices by 272; it loses 141 initial successes and
  rescues 219. Common preparation already raises replica-2 wrong commitments
  from 77 to 168.

These counts were reconciled by the main task with
[cohort retention](COHORT_RETENTION.csv), [baselines](BASELINES.csv) and
[secondary pointwise transitions](SECONDARY_CONTRASTS.csv). The final report
retains these distinctions; no primary rule was changed.

## Proposed next diagnostic, not executed

The reviewer suggested a bias-only counterfactual on retained replica-2 A-only
evidence: set the two final head biases back to their common-fork values, holding
the other 128 coefficients, decision inputs and exact integer/clipping/action
semantics fixed. At t=0 the lag features are zero and UNKNOWN is fixed, so this
could test bias contribution to initial-commitment harm conditional on final
feature weights. It would not explain why bias shifts arose or establish a
training remedy.

This is a post-hoc hypothesis, not a measured result, frozen E51AJ contrast or
authorization to rerun consumed populations. A separate analysis contract must
first establish whether all required decision inputs are retained; coefficient
and success rows alone do not establish counterfactual action outcomes. Any
required reconstruction or cognitive reevaluation must be declared explicitly,
not disguised as archive verification. No such counterfactual was executed.

The next training proposal remains a fresh shared-start, fixed-support
objective/update-constraint comparison, with original-objective and static
controls and pointwise/initial-decision accounting. Both proposals remain
unexecuted; E51AJ's scientific sources, budgets and outcome rules are unchanged.
