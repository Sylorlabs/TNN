# E51AI — Longitudinal context and replay diagnostic

Status: pre-execution specification; frozen by the first scientific source commit.
Parent scientific source: `c8f62bac285e72653bd6e9412498575ea8036b77`.
Parent closure: `483f791885abd24067fcbf8fd678a863a30abee1`.
R27 remains canonical. E51AH and its sealed stages 109/110 are not reopened.

## Question and experimental lane

Does real one-step history add useful information to a continuously updated
candidate-value residual, and does bounded experience replay reduce subsequent
losses? Does additional training repair early weaknesses or consolidate them?

This is an EXPLORATORY LONGITUDINAL DIAGNOSTIC, not a qualification run. Its
entire learning curve is scheduled before execution. A poor early behavioral
score does not stop the curve. Integrity failures or the compute limit do.
Changing this rule prospectively under a new identifier does not relax E51AH.
No probe score controls training, dose, checkpoint selection, or stopping.

## Frozen inherited substrate

Reconstruct the same mature E51X/Y slot learner and E51AB local-384 direct
learner through the verified E51AH assembly lineage. Neither is updated.
E51AH's experimental entry point is replaced, not executed. Require the
inherited terminal reproduction and direct-reconstruction integrity checks.

The deployable control is the frozen score-max hybrid. The frozen slot/direct
union is a separate evaluator-only support ceiling, NOT an old deployed agent.
New residuals compete through the same score-max candidate action interface.
UNKNOWN is zero with no learned head or ambiguity label.

## Arms, all with two 65-coordinate residual heads

| Arm | Residual input | Ongoing experience |
| ---: | --- | --- |
| 0 | 32 current features plus their 32 squared coordinates | Current cohort repeated twice |
| 1 | 32 current features plus the preceding state's 32 features | Current cohort repeated twice |
| 2 | 32 current features plus 32 zeros (history destroyed) | Current cohort repeated twice |
| 3 | Same real-history features as arm 1 | Half current cohort, half previously encountered other cohorts |

All arms have 130 allocated coefficients, the same optimizer, update ceiling,
initialization and batch size. Arm 0 supplies a richer current-state control;
arm 2 has fewer effective degrees of freedom despite identical allocation.
Capacity equality is not equality of function class or conditioning. A gain
over arm 2 alone is not sufficient evidence for useful temporal information.
History destruction means zeroing, not a mislabeled random permutation.

Current features are exactly `e50_batch_column(record,f+1,0)` for f=0..31,
including its substitutions from columns 32/33. Columns 34..37 are never
feature inputs. Lag features use t-1 of the same trajectory, zero at t=0;
there is no next-state, other-world, or evaluation-outcome input. Squared
coordinates are trunc(x*x/1000), saturated at 4000. Current and lag values
outside [-4000,4000] are an integrity failure, not silently rescaled.

Static temporal audit qualification: current state already contains history
and transition summaries. Current-state-only is not memoryless; one lag tests
incremental information, not the necessity of all memory. The inherited
simulator uses pre-generated latent truth to shape some observation regimes;
the input-boundary audit does not rule out generator shortcuts.

## Data, stream and longevity

Reserve stages 111..114 for four training cohorts A..D, and stages 115..118
for four disjoint, never-trained development-probe cohorts. Each contains
540 trajectories, two per inherited generator cell, and 17 states/trajectory.
Stage/world and RNG-domain initial-state ranges must be disjoint from the
historical range through 110 and from one another. Stage IDs are not features.
These cohorts share the existing generator: this is not four unrelated tasks,
a distribution-shift benchmark, or long-horizon planning.

This pilot omits a continued-dose-A-only arm and task-only baselines. It can
describe changes over continued learning and isolate its paired input/replay
contrasts, but cannot uniquely attribute deterioration to cohort switching
rather than overtraining, or estimate cross-task transfer.

One fixed training record per trajectory is its LAST resource-feasible prefix
state, selected without correctness or candidate-value labels. Its two targets
are ordinary grounded candidate utilities minus frozen direct predictions.
This deliberately differs from E51AH's selected critical-state replay sampler;
comparisons are causal within E51AI, not isolated ablations against E51AH.

Run A,B,C,D in order for EIGHT cycles: 32 persistent learning blocks. Parameters
are initialized only once. Each arm receives 1080 records/block and exactly
four coordinate sweeps/candidate. Arms 0..2 duplicate the 540 current records.
Arm 3 pairs the current 540 with a deterministic round-robin selection from
other cohorts already encountered, using only their saved training records.
Before any prior cohort exists it also duplicates current records. No probe
record ever enters replay. Replay changes support at matched record count;
finite round-robin weighting is reported, not asserted to be exact balancing.
Within each selected old cohort, the row is
`((position_within_replay / number_of_other_cohorts)*29 + block_index*97 + other_cohort_rank*17) mod 540`.
The coprime stride and rotating offset avoid repeatedly sampling a contiguous,
mode-ordered prefix. These constants and indices are scheduler-only, with no
label-based stratification, tuning, or visibility to the learner.

The lifetime is 2160 unique training trajectories and 34,560 scheduled training
record presentations per arm, plus the specified repeated optimizer sweeps.
This is a bounded longevity pilot, not a claim of lifelong competence. More
wall-clock runtime or resetting a model 32 times would not satisfy the design.

## Optimizer and reproducibility

Warm-start deterministic integer coordinate descent on squared residual error,
bias bound +/-4000, coefficient bound +/-16000. Each coordinate proposal is
backtracked until it strictly reduces the exact integer raw-prediction loss,
or makes no update. Exactly four sweeps are attempted even if no update occurs.
Deployment residuals are clipped to +/-4000, consistent across all arms.
For each update, fit a clone in reverse record traversal from the same prior
weights. Require identical final weights, losses and accepted-update counts.
Strict loss and warm-start identity are integrity gates. Emit all checkpoint
coefficients and parameter hashes. Synthetic tests precede scientific data.

## Fixed observations, not adaptive validation

Evaluate all four development-probe cohorts at checkpoint 0 and after every
block (1..32). Evaluate only resource-feasible states; retain the distinction
between successful-state existence and an actual stopping policy.
Record known/no-unique reachability, t=0 choices, pointwise paired losses and
rescues against both union and deployable hybrid, and all per-episode outcomes.

For probe j, retention anchor is the model immediately after first exposure to
training cohort j (checkpoint j+1). Record loss and gain of individual anchor
successes thereafter, plus peak-to-current count loss. Emit the full matrix,
including weaknesses: do not select the best checkpoint as the primary result.
Freeze an additional copy of each model after cycle one; reevaluate it at the
end and require identical predictions and weights on the identical probes.
This distinguishes ongoing parameter learning from evaluation or time drift.

All observations are consumed development diagnostics, including the untouched
probe records. They cannot be presented later as fresh validation. No
validation/confirmation stage is reserved, generated, or opened by E51AI.

## Frozen primary comparisons

The primary checkpoint is 32; earlier checkpoints are learning-curve evidence.
Compare real history (1) against BOTH current-only controls (0 and 2).
Report whether it exceeds both in total AND known reachability, has no lower
no-unique reachability than either, and loses zero union successes. This is a
narrow history-preserving SIGNAL only, requiring a new fresh replication.
Otherwise report observed differences/tradeoffs without claiming necessity.

Replay contrast is arm 3 vs arm 1: report final/worst anchor losses, recovery
after first deterioration, known/no-unique reachability and union losses.
Lower forgetting alone is not useful if acquisition or abstention collapses.
There is no post-hoc arm substitution, selected winner, or promotion.
Final outcome is `LONGITUDINAL_CONTEXT_DIAGNOSTIC_COMPLETE` when integrity
passes; incomplete execution has no completed scientific outcome. An integrity
failure overrides all behavioral comparisons.

## Budget, artifacts and limits

One native Linux run, maximum 3600 seconds for execution (75-minute job ceiling).
Archive partial logs on failure; never automatically rerun scientific data.
Preserve preregistration, source and transitive manifests, hardcoding ledger,
official compiler identity, two byte-identical binaries, synthetic test result,
raw logs, parameter checkpoints, per-episode probe outcomes, derived matrices,
run/source identifiers and independently checked artifact digest.

A native negative rejects only this input/optimizer/sampler/dose combination.
It neither refutes TNN nor establishes memory necessity. Full-tape or feasible
prefix reachability does not establish online stopping, autonomous mechanism
creation, multi-task continual learning, transfer, or integrated intelligence.
