# E51AI — Completed longitudinal context and replay diagnostic

Status: COMPLETED_VERIFIED_EXPLORATORY_DIAGNOSTIC.
Scientific outcome: `LONGITUDINAL_CONTEXT_DIAGNOSTIC_COMPLETE`.
Frozen history-preserving signal: **false**.
Run completed September 4, 2026 Pacific (`2026-09-05T06:34:35Z`).
R27 remains canonical. This completes E51AI, not the E51 research program.

## What the experiment found

Continuing the same learners through all eight cycles exposed a useful but
incomplete tradeoff. Real one-step history improved final total and known-case
reachability relative to both current-state controls, but reduced no-unique
preservation and still lost frozen-union successes. It therefore failed the
prospectively specified history-preserving signal.

Replay helped retention in this run. Against real history without replay,
it ended with 9 rather than 22 missing first-encounter successes, and 33 rather
than 46 such successes were lost at any point. The difference is not solely an
artifact of different arm-specific anchors: on the same 2,063 shared anchor
successes, replay ended missing 5 versus 21 without replay. This supplemental
comparison was derived after execution and does not replace the frozen test.

Replay's final reachability was almost identical to history without replay,
2,084 versus 2,085, with 12 fewer known successes and 11 more no-unique successes.
It is a bounded retention/preservation tradeoff, not exact rescue, proof that
memory is necessary, cross-task continual learning, or promotion authority.

## Frozen design and actual exposure

The [preregistration](R32_E51AI_LONGITUDINAL_CONTEXT_PREREG.md) was frozen at
source `c46fbbf67e1b7d5a19dee7ca1164fc4c5b0eec22`. Four continuing residual
learners shared the same frozen slot/direct substrate, two 65-coordinate heads,
optimizer, allocated parameter count, and scheduled record count:

| Arm | Additional representation | Training support |
| --- | --- | --- |
| 0 | Current 32 features and their squares | Current cohort twice |
| 1 | Current 32 features and same-episode preceding-state features | Current cohort twice |
| 2 | Current 32 features and zeroed history | Current cohort twice |
| 3 | Same real history as arm 1 | Half current and half previously encountered cohorts; current twice in block one |

Stages 111–114 supplied 2,160 unique training trajectories; stages 115–118
supplied 2,160 disjoint development probes. Each cohort has 540 trajectories,
including 420 known and 120 no-unique. These are same-generator cohorts, not
four different tasks. One last resource-feasible prefix record per training
trajectory supplied ordinary grounded residual targets. No probe feedback
changed fitting, support, dose, stopping, or checkpoint selection.

All 32 A→B→C→D blocks completed: eight cycles, 34,560 scheduled training-record
presentations per arm, four coordinate sweeps per head per block. Each block
warm-started from the previous block's full 130-coefficient state, and every arm
changed actual coefficients in all 32 blocks. Accepted coordinate updates were 12,033 / 12,134 /
6,189 / 10,943 for arms 0 / 1 / 2 / 3. Reverse-traversal clone fits matched.
Allocated capacity is matched, but zeroed history has fewer effective degrees
of freedom. Record counts, sweeps, reverse verification, backtracking work,
accepted updates, and wall time are not interchangeable compute measures.

Arms 0–2 each received 8,640 presentations from each training cohort. Arm 3
received A/B/C/D totals 9,630 / 8,550 / 8,280 / 8,100, including 16,740 prior-cohort
presentations. Its finite warm-up schedule is not exactly cohort-balanced.

Checkpoint zero and every completed block retested all four probe cohorts.
Cycle-one frozen snapshots were reevaluated at the end without drift. The
archive contains 293,760 probe-episode rows and 17,160 checkpoint coefficients.
The native execution took 1,091 seconds, exit zero; the whole job took 20m1s.
No scientific run was repeated, no budget extended, and no qualification stage
opened. E51AH stages 109/110 and immutable Baseline V1 were untouched.

## Final checkpoint: exact comparisons

Each arm is measured on the same 2,160 probes: 1,680 known and 480 no-unique.
The frozen deployable score-max hybrid reaches 2,070 (1,602 known + 468
no-unique). The evaluator-only frozen union reaches 2,093; it is not a policy.

| Arm | Total | Known | No-unique | Union lost | Union rescued | Hybrid lost | Hybrid rescued |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 — current + squares | 2073 | 1618 | 455 | 41 | 21 | 22 | 25 |
| 1 — real history | 2085 | 1633 | 452 | 38 | 30 | 19 | 34 |
| 2 — zero history | 2073 | 1608 | 465 | 26 | 6 | 6 | 9 |
| 3 — history + replay | 2084 | 1621 | 463 | 26 | 17 | 6 | 20 |

History exceeds both controls in total reachability by 12, and in known
reachability by 15 versus arm 0 and 25 versus arm 2. But its no-unique count is
3 below arm 0 and 13 below arm 2, and it loses 38 union successes. Thus both
the no-unique-preservation condition and the zero-union-loss condition fail.
No favorable intermediate checkpoint or alternative arm is substituted.

The baseline hybrid already misses 23 union successes at checkpoint zero.
Therefore union losses are not all newly introduced forgetting. The separate
hybrid and anchor comparisons identify those distinct reference questions.
For example, history rescues 34 hybrid misses but loses 19 hybrid successes;
replay rescues 20 but loses 6. Positive net gain does not imply preservation.

## Entire longevity curve

These are baseline and all eight cycle endpoints, not selected winners. The
[full curve](R32_E51AI_ANALYSIS/CURVE.csv) contains every intervening checkpoint.

| Checkpoint | Arm 0 | Arm 1 | Arm 2 | Arm 3 |
| --- | ---: | ---: | ---: | ---: |
| 0 — before learning | 2070 | 2070 | 2070 | 2070 |
| 4 — cycle 1 | 2076 | 2079 | 2073 | 2072 |
| 8 — cycle 2 | 2072 | 2088 | 2071 | 2072 |
| 12 — cycle 3 | 2072 | 2087 | 2070 | 2076 |
| 16 — cycle 4 | 2073 | 2090 | 2070 | 2077 |
| 20 — cycle 5 | 2072 | 2091 | 2072 | 2082 |
| 24 — cycle 6 | 2074 | 2090 | 2072 | 2079 |
| 28 — cycle 7 | 2074 | 2085 | 2074 | 2077 |
| 32 — cycle 8, fixed primary | 2073 | 2085 | 2073 | 2084 |

From cycle one to the fixed end, totals change by −3 / +6 / 0 / +12 for arms
0 / 1 / 2 / 3. Additional training is neither uniformly helpful nor monotonic.
History's observed cycle-five total of 2,091 declines to 2,085; this is a
description of the curve, not a selection rule. The final cycle also has
within-cycle dips: arm 1 records 2,070 / 2,071 / 2,081 / 2,085 at checkpoints
29–32; replay records 2,069 / 2,072 / 2,072 / 2,084.

There is no continued-dose-A-only or stationary-mixture comparator in E51AI.
The pattern cannot uniquely distinguish cohort-order interference, ordinary
continued fitting, objective mismatch, or training-support effects.

## Pointwise retention, forgetting and return

Each cohort's fixed anchor is its first-encounter checkpoint, j+1. The pooled
anchor combines different checkpoints and differs across arms; it is not a
single policy or a preregistered acquired-competence threshold.

| Arm | Anchor successes | Ever lost | Regained at final | Still missing | Never lost | Worst simultaneous loss after cycle 1 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 2064 | 52 | 29 | 23 | 2012 | 25 |
| 1 | 2070 | 46 | 24 | 22 | 2024 | 24 |
| 2 | 2066 | 33 | 20 | 13 | 2033 | 19 |
| 3 | 2069 | 33 | 24 | 9 | 2036 | 20 |

For each arm, ever-lost = regained-at-final + still-missing. New successes
outside the anchor set cannot cancel retention losses. Final retained fractions
are 98.886% / 98.937% / 99.371% / 99.565%; these do not describe uninterrupted
preservation. In particular, replay's worst simultaneous loss is 20 at
checkpoint 31, despite only 9 remaining at checkpoint 32.

Final missing first-encounter successes by cohort:

| Cohort | Arm 0 | Arm 1 | Arm 2 | Arm 3 |
| --- | ---: | ---: | ---: | ---: |
| A | 7 | 7 | 4 | 4 |
| B | 10 | 8 | 4 | 3 |
| C | 5 | 4 | 2 | 1 |
| D | 1 | 3 | 3 | 1 |

The supplemental shared-anchor check uses the same 2,063 first-encounter
successes in both history arms. Without replay, 40 were ever lost, 19 regained
at final, and 21 still missing. With replay, 28 were ever lost, 23 regained at
final, and 5 still missing. The corresponding never-lost counts are 2,023 and
2,035. This is descriptive evidence supporting the narrower replay contrast,
not a new primary test or an independent replication.

The frozen verifier names a later zero-loss observation
`first_zero_anchor_loss_return`. For replay cohorts C and D, that observation
is checkpoint 6, whose active cohort is B. Replay also includes previously
encountered cohorts, so this does not mean no C/D training happened; it means
the observation is not a clean same-cohort return or proof of sustained
reacquisition. All cohort-specific events are retained in the analysis tables.

## Initial decisions are different from reachable success

| Policy | t=0 successful | t=0 unsuccessful UNKNOWN | t=0 wrong commitment |
| --- | ---: | ---: | ---: |
| Frozen hybrid / checkpoint zero | 1385 | 672 | 103 |
| Arm 0 at checkpoint 32 | 1361 | 520 | 279 |
| Arm 1 at checkpoint 32 | 1385 | 550 | 225 |
| Arm 2 at checkpoint 32 | 1384 | 638 | 138 |
| Arm 3 at checkpoint 32 | 1390 | 633 | 137 |

Each row sums to 2,160. Correct UNKNOWN choices are included in successful
decisions, not in `t0unknown`. The real-history arm has the same number of
initial successes as the hybrid while making 122 more wrong commitments.
Replay improves initial successes by 5 but still makes 34 more wrong commitments
than the hybrid. Successful-state existence must not be sold as safe online
stopping or unqualified decision improvement.

## Identity, integrity and independent checks

Actions run `33949274757`, attempt 1; workflow `350732604`; job `101260866273`.
Scientific source `c46fbbf67e1b7d5a19dee7ca1164fc4c5b0eec22`, tree
`03cf947e05765875ec63131e802d444f1490f2c4`. Artifact `9964554609` contains 83
files; all 53 declared source inputs match the frozen commit and Git blob IDs.

| Item | SHA-256 |
| --- | --- |
| Exact artifact ZIP | `80c049ff197d7d466b694baf1a2611f1e3535de78a0ee5faa66ebdf3de121c6e` |
| Assembled source | `20916b1836b15fa591d204766f3eadf8f62a2e23ab4203e717ff279fb078bb61` |
| Preregistration | `cf3ab1ae1fef2acbac855a462c6379f7fb7efb682ec14934ac7f3be91bd8d469` |
| Raw log | `4fde4c4372adb1fdb0855f59845d2b6ba7e37893508c5fcbaf003146d1be5fbc` |
| Both native builds | `6c14c131829b47e1b9ff35bd9bc43fe908b784d96699c5f0ac41a5e73b43f584` |
| Official compiler | `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef` |

ZIP digest and size match GitHub metadata; archive paths, duplicates, symlinks,
CRC and extracted bytes were checked. The independently rerun frozen scientific
verifier agrees exactly with the archived report. All required source/build,
synthetic preflight, feature/data, fit/reverse-order, continuity, frozen-model,
snapshot and execution-completion checks passed. The baseline matches its
immutable authority commit. Sixteen postprocessing tests and nine frozen
verifier tests pass; synthetic tests are not scientific observations.

The main task audited the frozen continuity, replay, evaluation and retention
paths and independently recomputed retention using episode-key sets. A verdict
from the separately launched ChatGPT Web reviewer was not retrieved in this
continuation; no independent-agent approval is claimed. That is separate from
the completed native and local verification.

The exact archive and API metadata remain in
`.scratch/e51ai/actions-33949274757-k1tM4Q/`. [Machine-readable evidence](R32_E51AI_EVIDENCE.json)
preserves identities, all verified checkpoint totals, retention analysis and
analysis hashes. [Reproduction instructions](R32_E51AI_ANALYSIS/README.md)
describe how to regenerate every table without rerunning cognition.

## What this closes and what comes next

E51AI closes its complete scheduled measurement and rejects the specified
history-preserving signal at checkpoint 32. It establishes bounded continued
parameter learning and documents a replay-retention tradeoff. It neither
refutes the TNN approach nor qualifies an improved general learner.

The next proposal should separately test whether replay's retention advantage
replicates on fresh paired populations, and whether the within-cycle dips come
from ordering, continuing dose, or an objective/support mismatch. Relevant
controls include continued-dose-one-cohort and stationary mixtures, plus a
separately specified trajectory/preservation-aware objective. Additional
context, episodic retrieval, curriculum, and structural mechanisms remain
experimental candidates, not presumed solutions or completed work.

No next experiment is dispatched or assigned fresh stages by this result.
Every further run needs its own prospective controls, exposure and compute
budget. Probes 115–118 are now consumed development evidence, never fresh
qualification data. Current state already summarizes history, zero-history
has lower effective capacity, and E51AI lacks distinct tasks, independent
replications, acquisition thresholds and online stopping. Those boundaries
remain visible in the [generality scorecard](R32_E51_GENERALITY_SCORECARD.md).
