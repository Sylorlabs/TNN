# R32 E51AH — Grounded Preservation Replay Causal Discriminator

Preregistered: 2026-08-31

Parent branch: `r32-agent-sequential-frontier`

Parent source head: `80069f979084f0dcc6341fffe59b8e1a7ad2e7f1`

Canonical status: R27 remains canonical

## Pre-execution clarification — 2026-09-04

No E51AH development, validation, or confirmation has executed. This clarification
resolves decision-rule ambiguity before the first native trigger. The earliest
development-eligible replay arm is selected before validation. Only that arm
determines the primary outcome and can open confirmation; the remaining arms
are descriptive comparisons, never post-validation substitutes. Integrity failure
has precedence over every scientific outcome, including a confirmation failure.
Tradeoff means opposite net changes in known and no-unique reachability, not
merely nonzero paired gain and loss counts within an unchanged category.

The evaluator-only oracle must choose the highest positive candidate utility
(UNKNOWN at zero otherwise) and score that choice through the grounded evaluator.
The earlier E51AE/E51AG oracle counters assigned success unconditionally; their
reported exactness alone is not independent evidence of candidate expressivity.
This caveat leaves their measured learned-arm comparisons unchanged.

## Observed failure

E51AE and its E51AG three-partition replication produced a stable tradeoff.
Relative to the frozen mature slot-plus-direct union, the learned candidate-value
residual recovered additional known trajectories while losing far more no-unique
trajectories. E51AG reported exact direct-action oracle counters on all three
fresh partitions, subject to the oracle-scoring caveat above. E51AH independently
scores its diagnostic oracle without using it in learning or winner selection.

The parent residual critical set contains direct-required and union-neither
episodes but no slot-covered preservation examples. Its global residual already
fails the development preservation gate, and the local arms inherit that global
fit. This creates two live explanations:

1. **missing preservation credit/support:** ordinary experiences where the frozen
   behavior was already successful, or an override would be harmful, were absent
   from residual fitting;
2. **current-state discrimination limit:** even with grounded preservation replay,
   the current evaluator-blind 32-feature state and tested linear/local geometry
   cannot separate useful corrections from harmful overrides.

## Preregistered question

Can one grounded replay example from every development trajectory teach the
existing residual learner to preserve the mature union while retaining useful
candidate corrections, without adding context, topology, evaluator labels, or a
learned UNKNOWN head?

## Frozen intervention

The mature E51X/E51Y slot learner and E51AB local-384 direct-candidate learner are
reconstructed and frozen. E51AH changes only the residual training support.

For each stage-108 development trajectory, the sampler stores one
trajectory-critical learner record and the two ordinary grounded candidate-value
residual targets:

- slot-covered trajectory: select a state where the frozen slot action succeeds,
  prioritizing the state with greatest candidate-over-slot override risk;
- direct-required trajectory: select the direct-success state with the weakest
  current correct-candidate margin;
- frozen-union-neither trajectory with positive candidate utility: select the
  accessible state with the strongest correct-candidate margin;
- frozen-union-neither trajectory without positive candidate utility: select the
  accessible state closest to safe UNKNOWN under the frozen candidate scores.

Selection uses frozen learner scores, resource feasibility, and grounded action
consequences. It does not use mode, resource, world, task, ambiguity, validation,
or correctness identifiers as learner inputs. Target/evaluator fields are zeroed
from every stored learner record before fitting.

## Arms

| Arm | Description |
| ---: | --- |
| 0 | frozen mature slot-plus-direct evaluator union control |
| 1 | parent E51AE-style critical-only global residual |
| 2 | count-matched critical-only global residual; parent critical records repeated deterministically to the replay-set size |
| 3 | grounded preservation-replay global residual |
| 4 | grounded preservation-replay 32-cell local conditional residual, 384-sweep ceiling |
| 5 | evaluator-only direct-action oracle ceiling |

Arm 2 matches record count but is not an exact weighting control: when the replay
count is not divisible by the critical count, the deterministic prefix receives
one extra copy. The full-cycle count and remainder are reported. This residual
weighting difference limits causal attribution to count alone.
Arms 1-4 use the same 32 learner-visible terminal
features and frozen action interface. No arm changes topology or candidate set.

## Partitions

- stage 108: development, 12,960 trajectories, 48 per generator cell;
- stage 109: untouched validation, 5,400 trajectories, 20 per generator cell;
- stage 110: sealed confirmation, 10,800 trajectories, 40 per generator cell;
- all stage/world and RNG-domain ranges must be disjoint from stages through 107.

Validation remains sealed unless at least one replay arm satisfies all development
opening gates. Confirmation remains sealed unless the first eligible replay arm
is exact on validation.

## Development opening gates

A replay arm is validation-eligible only when all of the following hold:

- parent/native reconstruction and world-domain integrity pass;
- replay contains exactly one isolated learner record per development trajectory;
- both candidate residual targets have positive and negative support;
- forward/reverse fit identity and strict-loss gates pass;
- all frozen-union development trajectories remain reachable;
- at least one frozen-union-neither development trajectory is rescued;
- mature slot and direct parameter hashes remain unchanged.

If neither replay arm is eligible, stage 109 must not execute and the outcome is
`PRESERVATION_REPLAY_DEVELOPMENT_FAILURE`.

## Validation metrics

For every arm report:

- total, known, and no-unique reachability;
- state-zero success, UNKNOWN, and wrong counts;
- paired gains and losses relative to the frozen union control;
- mode/resource decomposition for evaluator audit only;
- source/model hashes and frozen-controller identity.

## Frozen decision rules

The lowest-numbered eligible replay arm determines the strongest satisfied rule:

1. `PRESERVATION_REPLAY_EXACT_CONFIRMED`: exact 5,400/5,400 validation and exact
   10,800/10,800 sealed confirmation;
2. `PRESERVATION_REPLAY_EXACT_NOT_CONFIRMED`: exact validation but confirmation
   is non-exact with otherwise valid integrity;
3. `PRESERVATION_REPLAY_PARETO_IMPROVEMENT`: validation total and known
   reachability exceed arm 0, no-unique reachability is not below arm 0, and
   paired losses are zero;
4. `PRESERVATION_REPLAY_TRADEOFF`: the selected replay arm gains known reachability
   while losing no-unique reachability, or conversely, relative to arm 0;
5. `PRESERVATION_REPLAY_NO_GAIN`: replay arms are valid but neither exact nor a
   paired-loss-free Pareto improvement;
6. `INVALID_E51AH_INTEGRITY_FAILURE`: any required integrity gate fails; this rule
   has precedence over rules 1-5 and development failure.

Only exact validation opens stage 110. A non-exact improvement is evidence for a
later fresh-partition replication, not promotion.

## Closure interpretation

- Exact or paired-loss-free improvement supports the missing-preservation-credit
  hypothesis and keeps the next branch in curriculum/credit/replay.
- Development failure or a repeated validation tradeoff rejects this grounded
  replay treatment within the current 32-feature linear/local residual family and
  advances the causal branch to short-context memory or representation.
- No result may justify post-validation tuning of E51AH, evaluator-label exposure,
  graph privilege, or R32 promotion.
