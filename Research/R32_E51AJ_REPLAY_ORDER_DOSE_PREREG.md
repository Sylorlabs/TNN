# E51AJ — Shared-start replay, order, and continuing-dose diagnostic

Status: prospective specification; frozen by the scientific source commit before
any stage 119–142 experiment executes. Date: 2026-09-05 Pacific.
Parent scientific source: `c46fbbf67e1b7d5a19dee7ca1164fc4c5b0eec22` (E51AI).
Parent result/analysis closure: `36cab59430c2b108411bad5c09da09767fdffbe4`.
Lane: EXPLORATORY_LONGITUDINAL_DIAGNOSTIC. R27 remains canonical.

## Decision and competing explanations

E51AI completed all 32 continuing blocks. Replay lost fewer first-encounter
successes than real history without replay, including on a supplemental common
success set, but did not preserve every prior success. Real history's total
reachability advantage coexisted with reduced no-unique preservation. The curve
was nonmonotonic. See `R32_E51AI_RESULT.md` and its verified evidence package.

The immediate question is whether replay's retention direction repeats on fresh
paired populations when treatments begin from one identical learned state and
have exactly matched example multisets at complete-cycle endpoints. Competing
explanations are (a) distributing prior experience across updates improves
retention, (b) concentrated cohort support/order drives the observed oscillation,
(c) continuing the same fitting objective can itself damage prior successes,
and (d) the previous apparent advantage is population-specific. A shared-start,
five-arm, three-population comparison separates more of these possibilities
without changing representation, objective, or adding model capacity.

This is a controlled extension, NOT an exact rerun/replication of E51AI: common
pretraining, anchors and balanced replay scheduling are prospectively different.
Three disjoint new populations replicate E51AJ's contrasts, conditional on the
same inherited frozen controller substrate. No selected E51AI checkpoint is used.

## Frozen inherited learner and input boundary

Reconstruct the mature E51X/Y slot controller and E51AB local-384 direct
controller through the unchanged E51AI assembly lineage. Require terminal
reproduction and frozen direct reconstruction. Their parameter hashes remain
238967492 and 1790306570. Do not execute E51AH or E51AI scientific entry points.

All trained arms use the same two 65-coordinate integer residual heads: bias,
32 current projected features, and 32 same-trajectory preceding-state features.
Projection is exactly `e50_batch_column(record,f+1,0)` for f=0..31, including
the inherited columns 32/33 substitutions. Lag is zero at t=0. Utility columns
34–37, future observations, truth, ambiguity, world/stage/mode/resource IDs,
probe results, retention membership and arm/checkpoint identity never become
learner features. Targets are ordinary grounded candidate utilities minus
frozen direct predictions on training records only. UNKNOWN stays zero, with
no learned UNKNOWN head. All arms use the inherited score-max candidate action
interface. Current state already summarizes history; this is not a memory-
necessity test. Inherited generator shortcuts are not excluded by input isolation.

Keep the E51AI strict-loss, deterministic integer coordinate fitter unchanged
except the prospectively specified scheduler and common real-history projection.
Use four sweeps/head/block; bias bound +/-4000, other coefficients +/-16000;
deployment residuals clip to +/-4000. Reverse-record traversal from an identical
clone must reproduce coefficients, losses and accepted-update counts exactly.

## Fresh data, common preparation and treatment fork

Three replicas r=0,1,2 use stage ranges 119–126, 127–134, 135–142 respectively.
In each range, the first four stages are training cohorts A–D, the last four
are disjoint development probes A–D. Each cohort contains 540 trajectories,
420 known and 120 no-unique, with 17 observed states per trajectory. Cohort
labels refer only to same-generator populations, not distinct tasks. Stage IDs
and all five RNG-domain initial-state intervals must be disjoint from the
historical range through 118 and from other declared intervals.

Select exactly one training record per trajectory: the LAST resource-feasible
prefix state, without conditioning on correctness, target value or evaluator
success. Thus each replica has 2,160 unique training and 2,160 unique probe
trajectories; the whole experiment has 6,480 of each. No fresh trajectories
arrive after the preparation phase: continuing blocks repeat observed experience.

For each replica initialize one 130-coefficient residual at zero. First train
A, B, C, D for one block each, 1,080 records/block (each cohort record twice).
This common four-block preparation is performed once, with all intermediate
coefficients, initial/final hashes, losses and reverse-fit identity recorded.
Fork its exact final coefficients into FIVE arms. This fork is checkpoint 0.
This is a fixed preparation dose, NOT an acquired-competence threshold.

| Arm | Continuing experience after the shared fork |
| ---: | --- |
| 0 | Sequential A→B→C→D; current cohort's 540 records twice per block. |
| 1 | Same active-cohort order; current 540 plus 180 records from each other previously observed cohort. |
| 2 | Balanced mixture each block: 270 records from each of A–D. |
| 3 | Continue A alone: its 540 records twice per block. |
| 4 | Frozen fork: zero further fitting, evaluated at every checkpoint. |

Run eight complete cycles, 32 continuing blocks, with persistent coefficients.
All four trainable arms receive 34,560 continuing record presentations plus the
shared 4,320 preparation presentations in their lineage: 38,880 total per
replica. The static arm receives only the shared preparation. Physical common
preparation runs once, not five times. Allocation is 130 coefficients/arm.
Exposure counts are NOT optimizer operations, wall time, or unique experience.

## Exact continuing schedules and multiset matching

Let b=0..31 be the continuing block, p=0..1079 the position, a=b mod 4,
c=floor(b/4) the cycle, and row=540*cohort+episode. Arm 0 uses
row=540*a+(p mod 540); arm 3 uses row=p mod 540.

Arm 1 uses the same current records at p<540. For remaining positions let
l=p-540, rank=l mod 3, k=floor(l/3), and j be the rank-th cohort excluding a.
Let phase=a when a<j, otherwise a-1. Its episode is
`((phase*180+k)*29+c*97) mod 540` in old cohort j. All old cohorts were genuinely
encountered during common preparation; there is no future-cohort access.

Arm 2 uses cohort j=p mod 4 and episode
`(((b mod 2)*270+floor(p/4))*29+c*97) mod 540`.
29 is coprime to 540. In EVERY four-block cycle, each of the 2,160 training
records appears exactly twice in arms 0, 1 and 2. This is exact record-multiset
matching, not just equal total counts. Each receives 8,640 continuing records
from each cohort. Arm 3 receives 34,560 from A and zero from B–D; its different
support is the declared dose comparator, not a data-matched order comparator.

Scheduler constants and indices do not enter the learner. Audit all schedules
synthetically before data, and emit each block's cohort counts and ordered row
hash for independent reconstruction. Counts and four sweeps are matched across
trained arms; differing accepted updates and backtracking prevent a claim of
equal actual compute. Replay here redistributes stored training examples, not
learned retrieval or autonomous memory selection.

## Checkpoints, evaluation isolation and retention

Evaluate the zero-initialized arms at checkpoint -1 to recover the deployable
hybrid. Evaluate the shared learned fork at 0, then all arms at 1..32. Thus
there are 34 panels/replica, five arms, four 540-trajectory probe cohorts:
1,101,600 native probe-episode rows. Emit all 66,300 panel coefficients plus
1,560 common-preparation coefficients (67,860 coefficient rows in total).
There are 792 head-fit rows (24 preparation, 768 continuing).

The single primary retention anchor is the identical checkpoint-0 success
vector for ALL arms in a replica. Record per-episode outcome, known/no-unique
reachability, t=0 successful/unsuccessful UNKNOWN/wrong commitment, paired losses
and rescues versus the frozen deployable hybrid and separate evaluator union,
and fixed-anchor loss/gain at every checkpoint. Retain the full matrix, not
just endpoints. Report ever-lost, never-lost, regained-at-final, final-missing,
worst simultaneous loss, and exact coefficient changes.

Native evaluation never fits, changes learner coefficients, or advances a
training RNG. Check all weight bytes/coefficients before and after each panel;
check cached features/targets/metadata remain unchanged. Native static-arm
outcome checks and independent ledger verification must match checkpoint 0 at
every later panel. Preserve per-cohort rows and all failures. A later return to
zero anchor loss does not erase prior loss or establish sustained reacquisition.
No acquisition threshold, return-specific dose or cross-task transfer is claimed.

These repeated development probes never control fitting, scheduling, dose,
checkpoint choice or stopping. They are consumed diagnostics, not fresh future
qualification data. Evaluator union is not a deployable old policy. Feasible-
state success is not an online stopping policy. Correct UNKNOWN is included in
t0success; t0unknown counts only unsuccessful UNKNOWN choices.

## Frozen primary and secondary comparisons

Primary contrast: arm 1 minus arm 0 at checkpoint 32, separately for all three
replicas. A REPLICATED_RETENTION_DIRECTION requires a nonempty common anchor,
STRICTLY fewer final missing anchor successes in each replica, no more ever-lost
anchor successes in each, and no greater worst simultaneous anchor loss in each.
Otherwise report MIXED_OR_UNREPLICATED_RETENTION_DIRECTION. Do not pool away a
replica reversal, replace the comparator or pick a favorable earlier checkpoint.
This descriptive directional rule is not a significance test or qualification.

Separately flag NO_FINAL_BEHAVIORAL_TRADEOFF only if every replica has replay
total, known, no-unique and t=0 success counts no lower than arm 0, with no more
t=0 wrong commitments. Report all differences even when the retention direction
passes. Neither this flag nor retention permits loss-free or safety claims.
The flag compares the listed aggregate counts, not pointwise preservation:
it cannot exclude swapped successes, cohort-specific damage or earlier harm.

Secondary fixed contrasts are arm 2 vs 0 (support distribution across blocks
at exactly matched complete-cycle multisets), arm 1 vs 2 (replay concentration
vs balanced mixing), and arm 3 vs static arm 4 (continuing A-only dose vs no
further learning). Also report all arms' losses against static and hybrid.
If A-only deteriorates, continued fitting alone can damage the shared anchor
under that support; this does not uniquely explain a sequential-arm failure.
Mixture comparisons isolate the declared scheduling package, not a unique
biological mechanism or order independent of optimizer trajectory.

Integrity-passing completion outcome is REPLAY_ORDER_DOSE_DIAGNOSTIC_COMPLETE,
regardless of behavioral direction. Integrity failure overrides behavioral
claims. Positive net gain cannot cancel pointwise damage. No promotion, fresh
qualification or topology change follows automatically from any outcome.

## Budget, artifacts and terminal handling

Exactly one native Linux scientific invocation, reconstructing the inherited
substrate once and executing all three predetermined replicas in order. Fixed
native execution cap 5,400 seconds; build/preflight cap 20 minutes; workflow
ceiling 115 minutes. Single native process. No reruns or cap extensions.
Use a 2-GiB process-address-space ceiling and 1-GiB individual output-file limit
on the Linux runner; archive cap 4 GiB. Record actual runtime and process exit.
Synthetic preflight uses no experimental generator entry point or populations.

Require official compiler SHA-256
`498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`, two
byte-identical builds, frozen source/transitive manifests, source/run/attempt
identities, preregistration/hardcoding pins, raw logs, coefficient records,
per-episode outcomes, all integrity markers, and independent local archive and
scientific checks. Freeze complete source before any exposure.

Always preserve partial evidence on timeout/interruption. An incomplete schedule
is censored, not a completed scientific negative; an integrity failure is
invalid. Never automatically resume or rerun consumed data. Poor scores alone
do not stop the fixed diagnostic horizon. E51AH stages 109/110, E51AI evidence,
its consumed probes 115–118, and Baseline V1 remain unchanged. The wider E51
program remains open; this experiment investigates one bounded causal package.
