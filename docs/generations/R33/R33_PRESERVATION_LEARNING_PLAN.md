# R33 preservation learning after E51AJ

Status: reconciled design, not a launched experiment. Execute only after relevant
sensory/telemetry qualification and the fixed-family capacity study. No fresh
partitions are allocated here. R27 remains canonical.

## Inherited evidence

[E51AJ](R32_E51AJ_RESULT.md) is a completed three-population same-generator
diagnostic. Replay reduced ever-lost and worst simultaneous losses in all three
populations, but final old-success losses were sequential 1/9/17 versus replay
14/11/6. A-only continuation lost 19/19/11 prior successes, including losses in
its own A cohort. The frozen fork lost none. `no_final_behavioral_tradeoff` was
false. This is mixed evidence, not a replay cure and not a proof that switching
alone caused forgetting.

The checkpoint-zero fork was created by four fixed preparation blocks, not by
a mastery threshold. Exact full-cycle multiset equality did not imply equal
intermediate support, optimization trajectories or actual compute. AJ measured
feasible-state reachability and initial decisions; it did not learn online
stopping. Probes and training stages are consumed as listed in the registry.

## Nearest prior experiments: do not rename them

E51AD enforced exact preservation of 12,334 development trajectories in a
conservative mechanism router, but its best router was 29 validation trajectories
below score-max. E51AE tested a trajectory-critical
candidate residual; E51AG replicated its negative behavior. E51AH added missing
training preservation records and remained a development failure. E51AI compared
short persistent residual learners with real lag/replay. E51AJ changed schedules
and tested the direction across three fresh paired populations.

The new question is **longitudinal update preservation at fixed support**,
not another conservative router, same hinge grid, or replay-order rerun.
Training preservation cannot guarantee preservation on unseen states; exact
training guarantees must be reported alongside fresh counterexamples.

## Proposed primary contrast

Create paired diagnostic branches from one fully identified learned parent per
population. Fix admitted representation, action support, optimizer proposal rule,
training example multiset/order, primary presentation dose and all parent state.
The primary estimand uses adaptive branch-local proposals: every branch applies
the identical proposal algorithm to its own current state. After one rejection,
the numerical proposals are not claimed identical across branches. Compare:

1. Ordinary fitting with unchanged update acceptance.
2. Branch-local proposals, admitted only if they satisfy a training-only
   preservation condition on a fixed, prospectively selected training anchor set.
3. Frozen parent with no continuing learning, as a retention identity control.
4. Ordinary updates at preregistered reduced doses or independently randomly
   thinned acceptance schedules. Freeze the schedules without using treatment
   performance, probe labels, or constraint outcomes. This controls for less
   learning; frozen-parent alone cannot establish a preservation-rule benefit.

The condition protects training action-value/ranking behavior under a defined
tolerance while requiring useful progress on current training examples. It is
an experimental update rule, not an oracle that observes probe correctness.
Select anchors by a fixed training-visible rule before probes are exposed;
never use AJ/AI probe success bitsets or held-out failure membership in fitting.
Record rejected updates, constraint costs and achievable training progress.

The preservation reference is the original named fork checkpoint, never the
preceding accepted update. Freeze its complete state digest, the protected
action-value/ranking quantities, tie rule, anchor identities, cumulative
tolerance from that original reference, and useful-current-learning minimum
before exposure. A per-update tolerance is not a cumulative guarantee. Numeric
tolerances, learning minima and thinning schedules must be filled in by B003's
source-frozen preregistration; this design does not allocate an executable batch.

Explicit transaction: propose in isolated candidate state → evaluate the
training-only constraint and progress condition → commit or reject. Rejection
restores candidate parameter, optimizer, recurrent, memory and learner RNG
state; the external presentation schedule advances once, and rejected proposals,
consumed audit nonces and spent compute remain in non-rewindable supervisor
history. No unlogged retry or extra example is permitted. Continuing learner
updates are never reset to hide interference.

Count unique experiences, presentations, visited states, proposals, accepted
updates, rejected updates, optimizer operations, checking operations and actual
compute separately. Plot retained capability versus both newly learned gain
and accepted updates, and also versus measured training/checking compute.
Matched presentations, matched accepted updates and matched compute are distinct
comparisons; do not assert all three from one dose label. A shared exogenous
proposal stream, if later useful, is a separately registered estimand rather
than a silent change to the branch-local protocol.

A constraint that simply freezes all useful updates is not a success. Report
retention against learned gain, including a stability/plasticity frontier.
Any tolerance/penalty grid is tuned on separately recorded development data,
then frozen before validation. Do not use post-hoc winning checkpoints.

## Secondary experiments, separately registered

Change action-ranking objective while keeping support fixed; then expand
training support while holding objective fixed; then evaluate replay-selected
anchors versus fixed anchors under matched budgets. Do not combine these
changes in the primary treatment. A no-switch continuation control separates
switching effects from optimization drift; a zero-update control checks that
measurement itself does not mutate state.

## Outcomes and interpretation

Primary retained-success bitsets and per-population old losses; newly learned
successes; cumulative ever-lost and worst simultaneous loss; final recovery;
initial correct/failed-UNKNOWN/wrong commitment; actual online policy only when
implemented; per-cohort interference; parameter movement and measured compute.
Show both parent-fork and original-hybrid reference points.

Success requires reduced loss without merely refusing learning, trading known
for unresolved cases, or increasing initial wrong commitments under the frozen
preregistered criterion. Per-population reversals remain visible. Reachability
does not imply a policy will choose the successful observation prefix.

Falsifiers include unchanged fresh preservation despite satisfied training
constraints, a benefit explained by the reduced-dose controls, constraint-only
overfitting, zero useful plasticity, increased wrong commitments or failed
UNKNOWN, new support-related harm, or hidden
extra resource/help. Such outcomes constrain the mechanism; they do not prove
that memory, recurrence, more parameters or a new architecture must be necessary.

Integrated independent training review: [review dispositions](R33_INDEPENDENT_REVIEWS.md).
