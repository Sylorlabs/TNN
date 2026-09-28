# E51AJ — Completed shared-start replay, order and continuing-dose diagnostic

Status: COMPLETED_VERIFIED_EXPLORATORY_DIAGNOSTIC.
Scientific outcome: `REPLAY_ORDER_DOSE_DIAGNOSTIC_COMPLETE`.
Retention result: `MIXED_OR_UNREPLICATED_RETENTION_DIRECTION`.
Separate `no_final_behavioral_tradeoff`: **false in every replica**.
Run completed September 5, 2026 Pacific (`2026-09-05T07:46:13Z`).
R27 remains canonical. E51AJ is complete; the wider E51 research program is not.

## What the controlled extension found

Replay exposed fewer previously successful cases to loss at any time, and
lowered the worst simultaneous anchor loss, in all three tested populations.
But it ended with MORE missing shared-anchor successes in replicas 0 and 1,
and fewer only in replica 2. The preregistered rule requires all three, so the
replicated-retention claim fails. Lower cumulative disruption and better final
recovery are different properties; neither can stand in for the other.

Replay also reduced initial wrong commitments relative to sequential fitting
in all three replicas, but traded away known-case reachability in every replica.
It therefore fails the separate aggregate no-final-tradeoff rule. These are
mixed, informative effects, not evidence that replay never helps or that more
experimentation on TNN is pointless.

Continued A-only fitting lost shared-anchor successes in all three replicas,
including successes on A itself. Thus losses occur without post-fork alternation
among cohorts. This does not isolate the loss to a unique objective defect:
finite-sample support, generalization, fitting trajectory and action competition
remain possible contributors. Full evidence and all fixed comparisons are in
[the evidence package](R32_E51AJ_EVIDENCE.json) and
[complete tables](R32_E51AJ_ANALYSIS/TABLES.md).

## Frozen design and completed exposure

The [preregistration](R32_E51AJ_REPLAY_ORDER_DOSE_PREREG.md) was frozen at
`9ea141b050599854783258d82cfa3ee02efb1fad` before experimental exposure.
E51AJ is a controlled extension of E51AI, NOT an exact E51AI replication.
It removes arm-specific starting anchors and unequal full-cycle example counts.

Three new populations use training/probe stage ranges 119–122/123–126,
127–130/131–134, and 135–138/139–142. Each replica has four same-generator
cohorts, each containing 540 training and 540 separate probe trajectories.
Each probe panel has 2,160 trajectories: 1,680 known and 480 no-unique.
The entire experiment uses 6,480 unique training and 6,480 unique probe
trajectories. These are three populations on one inherited controller substrate,
not three independently developed systems, distinct tasks, or a million
independent test cases.

Every trained arm uses the same two 65-coordinate residual heads: bias,
32 current projected features and 32 same-episode lag features. Grounded
training targets, score-max candidate selection and zero UNKNOWN are unchanged.
Probe outcomes, retention membership, truth and stage/cohort identity do not
direct fitting. Current state already summarizes history; this is not a
memory-necessity test.

Checkpoint -1 recovers the zero-residual deployable hybrid. Four shared A→B→C→D
preparation blocks produce a learned checkpoint-0 fork. Its exact coefficients
and success vector are copied to every arm. Preparation is a fixed dose, not
an acquired-competence threshold.

The five continuing arms are sequential active cohort twice (0), current cohort
plus balanced prior-cohort replay (1), balanced per-block mixture (2), A-only
twice (3), and the frozen shared fork (4). All four trainable arms completed
32 continuation blocks, with four coordinate sweeps per head per block and
warm-started coefficients. All cohorts were encountered before the fork.

Arms 0–2 receive the EXACT same training-record multiset at every four-block
cycle endpoint: every record twice per cycle. Intermediate support, update
trajectories and actual optimizer work differ. A-only is count-matched, not
data-matched; the static arm is not compute-matched. No fresh trajectories arrive
after preparation.

Each trained arm's lineage includes 4,320 preparation plus 34,560 continuation
presentations, totaling 38,880. Counting shared preparation only once yields
427,680 scheduled primary-fit presentations across all replicas and arms.
The evidence field calls these physical training-record presentations; it does
not count coordinate-sweep reads, reverse-fit verification, or inherited-substrate
reconstruction as additional presentations. It is not a compute measure.

All 34 checkpoints per replica, five arms and four probe cohorts are retained:
1,101,600 probe-episode rows, 67,860 coefficient rows, 792 head-fit rows and
396 exposure/parameter-continuity rows. No early weak score stopped the horizon,
no budget was extended, and no scientific invocation was repeated.

## Preregistered primary result

An anchor is a success of the identical checkpoint-0 fork. Final missing counts
refer to checkpoint 32. Ever-lost counts retain every intervening loss, including
cases later recovered. The primary table is generated directly from independently
recomputed episode-level masks:

| Replica | Shared successes | Final loss: sequential | Final loss: replay | Ever lost: seq / replay | Worst loss: seq / replay | Retention direction |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 2091 | 1 | 14 | 31 / 24 | 16 / 15 | no |
| 1 | 2081 | 9 | 11 | 35 / 26 | 17 / 15 | no |
| 2 | 2082 | 17 | 6 | 48 / 28 | 20 / 12 | yes |

The final-loss condition fails in replicas 0 and 1, despite all replicas passing
the nonempty-anchor, ever-lost and worst-loss conditions. In replica 0, sequential
fitting regains 30 of 31 ever-lost anchors by the end; replay regains 10 of 24.
In replica 1 those counts are 26/35 and 15/26. In replica 2 they are 31/48 and
22/28. These decompositions explain why lower ever-lost counts do not guarantee
better final retention. No replica is discarded or favorable checkpoint selected.

The final sequential/replay reachability counts are 2,098/2,090, 2,076/2,074,
and 2,091/2,091. Replay-minus-sequential known-case differences are -3, -1,
and -8; no-unique differences are -5, -1, and +8. Thus the separate aggregate
behavioral flag fails in every replica, including the retention-positive one.

Pointwise final contrasts also matter. Replay loses/rescues 13/5 sequential
successes in replica 0, 9/7 in replica 1, and 19/19 in replica 2. Equal final
totals in replica 2 hide a swap of 19 successes, not identical behavior.
These descriptive decompositions do not replace the frozen primary rule.

## Entire horizon, recovery and parameter changes

[CURVE.csv](R32_E51AJ_ANALYSIS/CURVE.csv) preserves all 510 arm/checkpoint
panels; [RETENTION_MATRIX.csv](R32_E51AJ_ANALYSIS/RETENTION_MATRIX.csv) has
all 2,040 cohort panels. All eight cycle endpoints, the original hybrid, the
learned fork and every final arm appear in the complete tables. Both gains and
declines occur in every sequential, replay and mixture curve.

For example, replay's cycle-one/final reachability is 2,095→2,090,
2,080→2,074 and 2,089→2,091 across replicas. In replica 2 its last four
checkpoints are 2,093, 2,086, 2,087, 2,091. This is a measured nonmonotonic
trajectory, not justification to report the best earlier point.

Every sequential, replay and mixture arm changes coefficients in all 32
continuation blocks. A-only changes coefficients in 27, 14 and 32 blocks;
its last changes occur at checkpoints 27, 14 and 32 respectively. The
remaining scheduled fits still execute. Flat behavior is not sufficient to
infer frozen coefficients: replica-2 A-only has the same final-four total of
2,103 while its coefficients continue changing. Accepted-update counts for
all arms are saved in [PARAMETER_CHANGES.csv](R32_E51AJ_ANALYSIS/PARAMETER_CHANGES.csv)
and summarized in the complete tables.

All trainable arms lose at least one common-anchor success at checkpoint 1.
Sequential replicas 0 and 1 return to zero aggregate anchor loss at checkpoint 4,
but later lose cases again. A return does not establish uninterrupted retention
or sustained reacquisition. Frozen arm 4 preserves coefficients and outcomes
at every panel and has zero continuation losses by construction.

## Fixed secondary comparisons and cohort harm

Balanced mixture versus sequential fitting ends with anchor losses 10 versus 1,
13 versus 9, and 6 versus 17. Its ever-lost counts are lower in all replicas
(19 versus 31, 22 versus 35, 15 versus 48), but the endpoint advantage reverses
in the first two populations, just as it does for replay. This supports a
distinction between cumulative disruption and endpoint recovery, not a universal
advantage of mixing.

Replay versus mixture has final reachability differences -1, 0 and +5, and
initial wrong-commitment differences +5, -22 and +50. Mixture is not a universal
replacement winner. The schedules identify a support/optimization package,
not example order independent of the nonlinear fitting trajectory.

A-only versus the static fork loses 19, 19 and 11 anchor successes. It also
gains 9, 11 and 32 other successes, for net reachability -10, -8 and +21.
Its own A probe cohort loses 7, 3 and 3 anchors; damage is not confined to
cohorts omitted after preparation. Generalization to probes can change even
while repeatedly fitting the same training support. In replica 2, A-only's
net gain coexists with 38 fewer initial successes and 192 more initial wrong
commitments than the frozen fork.

Full cohort-specific retention and all twelve fixed final contrasts are in
[COHORT_RETENTION.csv](R32_E51AJ_ANALYSIS/COHORT_RETENTION.csv) and
[SECONDARY_CONTRASTS.csv](R32_E51AJ_ANALYSIS/SECONDARY_CONTRASTS.csv).
Aggregate gains never cancel pointwise or cohort-specific damage.

## Initial decisions, abstention and the baseline distinction

At checkpoint 32, initial wrong commitments for sequential/replay are
133/125, 151/110 and 517/167. Replay reduces them by 8, 41 and 350, while
initial-success differences are 0, +13 and +78. However, the original hybrid's
wrong-commitment counts are 113, 102 and 77: replay is still worse than that
baseline by 12, 8 and 90. The shared learned fork is another reference, with
118, 105 and 168 wrong commitments. Common preparation already changes behavior.

Correct UNKNOWN choices are included in t=0 success; `t0unknown` counts only
unsuccessful UNKNOWN choices. Reachability means a successful state exists
within a resource-feasible prefix. It does not establish that a learned online
policy chooses that state or stops safely. The evaluator-only union is also
not a deployable policy. The tables keep union, hybrid and fork comparisons
separate.

The initial-decision pointwise decomposition is also retained: replica-2 replay
versus sequential loses 141 t=0 successes and rescues 219, while unsuccessful
UNKNOWN choices increase by 272. A-only versus static introduces 194 wrong
commitments and removes two. Aggregate improvements therefore do not establish
pointwise decision preservation.

## Identity, resources and reproducibility

Actions run `33952427608`, workflow `350761479`, attempt 1, job `101269590181`.
Scientific source `9ea141b050599854783258d82cfa3ee02efb1fad`, tree
`12056bc69c7b186cce063b0f69bd71a27900cd66`. Exact artifact `9965575939` is
8,098,800 bytes and contains 95 files. All 65 manifested scientific inputs
match the frozen source and remain unchanged locally.

| Evidence | SHA-256 |
| --- | --- |
| Artifact ZIP | `a64d9060e695a73a31a2d5c134a5000da0c7e79d40903a72958c0ba022f3c735` |
| Assembled source | `6988152bd8779e7bc2c29253d840363a610de2287cab61b34139874348b45182` |
| Preregistration | `d29cfd9186b5099b37acef028b04300ead7bb2545549a2d2be7f77e747ae09cf` |
| Raw log | `5573e0dda173f023e65598eb895f998ac61ecf9ccd0210f89ae09489c36bb84e` |
| Both native builds | `e39a2565915759ad1b17a94839c2b8d06b849c4889b556ba3d6213a94c5211c4` |
| Official compiler | `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef` |

Native runtime was 1,212.888 seconds, exit zero, below the fixed 5,400-second
limit. Peak resident memory was 487,296 KiB. The process-address-space cap was
2 GiB and the individual output-file cap 1 GiB. Whole-job duration was 22m27s;
it includes builds, preflight, execution and preservation, not just learning.

ZIP digest, size, CRC, duplicate/path/symlink safety, extracted bytes, source
identity, official compiler and immutable baseline were checked locally.
The frozen scientific parser reproduces its archived report exactly. A separate
bit-mask derivation recomputes pooled/cohort outcomes, common-anchor retention,
paired contrasts and both outcome rules from the native episode rows. All
21 analysis/archive/rendering tests and 11 frozen verifier tests pass; synthetic
fixtures are not new experimental evidence. No archived cognition is rerun.

The pre-execution ChatGPT Web review covered experimental design, not results,
compiler or archive arithmetic. A separate ChatGPT Web Pro reviewer completed
an interpretation audit, confirming the failed conditions and flagging recovery,
A-only and pointwise decision caveats. [Review provenance](R32_E51AJ_ANALYSIS/POSTEXECUTION_REVIEW.md)
and [delivery checks](R32_E51AJ_ANALYSIS/VALIDATION.md) record their distinct scopes.
The original metadata and exact ZIP remain in
`.scratch/e51aj/actions-33952427608-5H2tNi/`.
[Reproduction instructions](R32_E51AJ_ANALYSIS/README.md) regenerate all tables
and the evidence package without generating new scientific data.

## What closes and the next research question

This closes the specified three-replica replay-retention test and its separate
aggregate behavioral rule: neither succeeds. It does not close replay, context,
memory or TNN as research directions. It establishes that repeated ordinary
fitting under fixed support can alter and damage prior probe successes, even
without cohort alternation, and that endpoint recovery can disagree with
cumulative disruption.

The next proposed discriminator should keep fresh shared starts, representation,
support and dose fixed while separating ordinary fitting from a training-only
preservation constraint or action-ranking objective. Include the unchanged
objective and frozen fork as controls; freeze grounded targets and criteria
before exposure, never use probe success membership to accept updates, and
retain both pointwise losses and initial-decision tradeoffs. This is an
unexecuted research direction, not a preregistration or a claim that the remedy
works. No new stages are assigned or run dispatched by this closure.

AJ probe stages 123–126, 131–134 and 139–142 are now consumed diagnostics;
AI probes 115–118 remain consumed. AH stages 109/110 remain sealed, historical
AI/AH results and Baseline V1 remain unchanged, and no R32 promotion is authorized.
