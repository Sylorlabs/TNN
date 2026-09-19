# R32 E45 — Preserved Native Negatives and Evaluator Repair

Date: 2026-08-23

Status: `EXECUTED_NEGATIVE — NOT QUALIFYING`

Canonical effect: none. R27 remains canonical.

## What ran

Two complete native macOS ARM64 A/B/C/D qualification candidates ran on the fresh confirmation grid: six seeds × nine evaluator modes × five resource regimes × forty episodes, or 10,800 paired episodes per arm.

The reduced learned shadow-price estimator independently passed its held-out controls in the first run:

- validation cases: 2,700;
- target mean: 406 fixed-point units;
- learned reduced-12 MAE: 196;
- raw-cost MAE: 395;
- fixed-0.55 MAE: 269;
- learned-global-scalar MAE: 280;
- learned reduced-12 R²: 0.749.

This is a reduced native estimator, not a claim of full V28 29-feature parity.

## Negative 1 — arm-specific initiation candidate

Artifact: `R32_E45_NEGATIVE_BBF0FD92.json`

- source SHA256: `bbf0fd92296e6b76f4f7fc13f2ee6816e96e20d455602606729fa851bc4daa03`;
- native gate: `FAIL`;
- beneficial episodes: 0 / 10,800 per arm;
- resolvable episodes: 6,597 / 10,800 per arm;
- all four printed global arm rows were identical;
- D−A completion was non-positive in every seed;
- causal completion/regret gate: 0.

This candidate also used arm-specific initiation models. That confounded entry selection with option completion, so initiation was changed to a single shared model before the next run.

## Negative 2 — shared initiation candidate

Artifact: `R32_E45_NEGATIVE_886943CB.json`

- exact source SHA256: `886943cb2582e6c37d799d7514261a05f60fe2b5af386038716846dc60ee3d64`;
- native gate: `FAIL`;
- beneficial episodes: 0 / 10,800 per arm;
- resolvable episodes: 6,597 / 10,800 per arm;
- initiated episodes: 345 / 10,800 per arm;
- all four global arm rows remained identical;
- D−A completion by seed: `[0, -1, -4, 0, -1, 0]`;
- D−A regret improvement by seed: `[-5830, -6669, -8989, -3056, -5219, -4191]`;
- causal completion/regret gate: 0.

The shared initiation repair removed the causal confound but did not repair the collapse. This discriminates against “arm-specific initiation caused the entire failure.”

The obsolete shared-init source also compiled and ran on Linux x86-64, but its confirmation output diverged from macOS ARM64 after an identical shadow-validation prefix. The source had not explicitly initialized model and aggregate-metric arrays after allocation. That run is preserved as a deployment diagnostic, is not qualification evidence, and the live repair now zero-initializes every such array before training.

## Root cause

The evaluator, not the native compiler, caused the zero-positive collapse.

1. A single scalar `grounded_outcome` was used for every time step. “Replacement” and “reversal” therefore changed evidence patterns without changing the hidden world state.
2. Historical state equaled final truth in nearly every resolvable mode. The evaluator-side KEEP action was already correct at time zero, so investigation could not improve terminal utility.
3. The dynamic target used the ex-post best of KEEP/CURRENT/RESTORE/UNKNOWN. That is clairvoyant endpoint selection rather than the realized value of one frozen learner terminal policy.
4. With no positive option targets, one-step and recursive continuation learners received effectively collapsed supervision; feature masks could not create a valid causal difference.
5. Logical warrant read evaluator correctness, making warrant circular instead of an internal reconstructible property.

The native toolchain, core mechanisms, and shadow estimator behaved deterministically. The failure classification is `EVALUATOR + REPRESENTATION`, followed by invalid continuation training—not deployment.

## Required repair before another arm comparison

- Generate evaluator-only `truth_by_time` trajectories: no-unique, stable, unstable→stable, real replacement, and real reversal.
- Generate evidence from the contemporaneous hidden state while keeping truth and mode outside the policy call graph.
- Train and freeze one shared terminal controller; compute `T_t` from its realized choice at time `t`, not the ex-post best candidate label.
- Compute V44-style recursive value `G_t = max(T_t, -L_t + G_{t+1})`, skipping inspection when unaffordable.
- Use the same frozen initiation and terminal controllers for A/B/C/D; vary only one-step versus recursive continuation and the permitted state blocks.
- Require a nonzero, adequately sampled oracle-positive prevalence before interpreting causal deltas.
- Derive logical warrant only from live targets, provenance, consequence separation, support/contradiction, and parent trace; score soundness against truth separately.
- Skip censored temporal-hazard targets and avoid double-counting initiation shadow cost.

No failed result above is evidence against temporally extended options. Both runs lacked a valid positive option-completion learning problem.

## Clean repaired evaluator — B404 native negative

The repaired terminal-projection harness is frozen at source SHA256
`b404223658f51dc95cc20a76af515e8a3bc828a373e3a244d12a2cd7fb3d9f1e`.
It compiled twice to the same official Linux x86-64 binary SHA256
`57aa5ff0545ed518ebb6969595b05c464f89a3626089f41ba12df9933a67ec08`
and completed the full fresh native battery in 324 seconds. The complete output
SHA256 is `41c01ee95972951444993e27c066b7673c1d3c5b08570b0b83dfe9d039e6c7ae`.

This is a valid negative rather than an evaluator failure:

- shadow, baseline-parity, oracle-prevalence, mode, resource, and core controls passed;
- B showed a narrow recursive-credit signal relative to A: longer mean observation,
  better conditional success, and slightly lower regret;
- D did not convert that signal into a causal completion/regret improvement;
- all 2,400 no-unique D episodes made non-UNKNOWN wrong commitments;
- UNKNOWN choices were zero, all 60 no-unique cells failed, and the known-truth
  joint-seed count was zero.

The terminal UNKNOWN target is grounded zero utility. With zero initialization it
stays exactly zero, so UNKNOWN is chosen only when every commit value is negative.
Blocked mode order trained the no-unique examples first and then overwrote their
calibration with seven known-truth blocks. This motivated a fresh order-only
discriminator rather than another full qualification run.

Evidence: `R32_E45_NATIVE_QUALIFICATION_NEGATIVE_B4042236_BLOCKED_TERMINAL_EVIDENCE.json`.

## E46 order-only discriminator — valid native negative

E46 froze the B404 causal state and feature machinery, one common auxiliary
snapshot, seven equal-zero terminal heads, and one exact set of 55,080 training
records per model. The blocked control and six precommitted interleavings differed
only in cross-mode placement; every mode retained the same resource→episode
subsequence. All models received 220,320 updates. Fresh validation was indexed by
model × seed × mode × resource × time with exactly 20 observations per cell.

The official x86-64 source SHA256 is
`6e78954f00b107829ee50f988704d6a79a6ac924f4e38679acd293018edec51e`.
Two builds were byte-identical at binary SHA256
`a482da44043b44861c51c8b1556cc607d36e19797abb4a394246567edf8d0f7f`.
The 917-second raw output has SHA256
`9019127d2db60a6ff4fe8102cf383ea4a34690d5630f50cd8318d080e607c386`.
Integrity passed and the sealed confirmation set was not executed.

The blocked control reproduced the failure: 5 UNKNOWN and 20,395 wrong commits
in 20,400 no-unique decisions, with 0/1,020 time cells safe. Order mattered, but
did not rescue the controller:

| Treatment suffix | No-unique UNKNOWN | Safe cells | Known success | Known wrong |
|---:|---:|---:|---:|---:|
| control | 5 | 0/1,020 | 54,189 | 17,116 |
| 6 | 145 | 0/1,020 | 54,613 | 13,124 |
| 7 | 12,954 | 376/1,020 | 37,817 | 921 |
| 8 | 6,209 | 9/1,020 | 42,668 | 4,209 |
| 0 | 16,517 | 893/1,020 | 21,845 | 1,016 |
| 1 | 14,023 | 646/1,020 | 28,516 | 1,600 |
| 2 | 822 | 0/1,020 | 51,923 | 8,066 |

The suffix-0 treatment showed the strongest abstention effect and passed every
terminal-time no-unique cell, but failed 127 earlier cells and collapsed known
success from 54,189 to 21,845. The suffix-6 treatment preserved known performance
best but produced almost no UNKNOWN behavior. No treatment passed the joint
no-unique, pooled-known, key-mode, terminal-time, and per-seed gates.

The preregistered bounded outcome is `NO_TESTED_ORDER_RESCUE`. It establishes a
large order-sensitive abstention/resolution tradeoff, not that all schedules or
all representations fail. E47 therefore tests only two missing continuous causal
co-presence features under the original blocked order.

Evidence: `R32_E46_TERMINAL_ORDER_DISCRIMINATOR_NEGATIVE_6E78954F_NO_TESTED_ORDER_RESCUE_EVIDENCE.json`.

## E47 representation-only discriminator — valid native negative

E47 held the blocked E46 order, auxiliary snapshot, targets, learning rule, and
validation gates fixed. Four zero-initialized terminal models were trained in
lockstep on the same 55,080 canonical samples: the baseline, epoch two-hypothesis
co-viability in feature slot 3, option support/contradiction co-mass in slot 5,
and both statistics together. The helper that constructs the two statistics has
no evaluator mode, truth, seed, count, target, resource, or time argument.

The source SHA256 is
`b7b49f4d23e67c4370d6ac449622ac828687cf67df9b5404f2120edff73becbd`.
Two official x86-64 builds were byte-identical at binary SHA256
`ae019a51b806cd024d29fd9f0e70e08e88e5bb19d0cc272c57f8a1b2b790798e`.
The 950-second raw output has SHA256
`bd78ac606e4182101e7e9011bbbf80dbbf82192d9fa10e3e1e0c516cb50ac401`.
Integrity passed, the sealed confirmation set was not executed, and independent
recomputation found no malformed records, grid omissions, partition errors, or
gate discrepancies.

Both statistics varied substantially. Slot 3 ranged from 1 to 441 on training
and slot 5 from 0 to 1,000; all 55,080 slot-3 observations and 31,894 slot-5
observations were interior. The added representation nevertheless did not make
the blocked terminal controller safe:

| Model | No-unique UNKNOWN | No-unique wrong | Safe cells | Known success | Known wrong |
|---|---:|---:|---:|---:|---:|
| baseline | 0 | 20,400 | 0/1,020 | 54,136 | 17,259 |
| slot 3 | 5 | 20,395 | 0/1,020 | 54,136 | 17,201 |
| slot 5 | 0 | 20,400 | 0/1,020 | 54,136 | 17,262 |
| slots 3 + 5 | 0 | 20,400 | 0/1,020 | 54,136 | 17,258 |

The UNKNOWN target was grounded zero on every training record. Consequently its
zero-initialized bias and all UNKNOWN weights remained exactly zero: abstention
requires every warranted commit head to be negative. The learned added-feature
weights did not achieve that geometry. For example, the joint model learned
positive slot-3 weight for RESTORE (+836) and positive slot-5 weight for CURRENT
(+311), preserving a positive commitment in the ambiguous cases. This is not a
claim that the features are constant or uninformative; it is a valid negative for
these two linear features under the blocked online presentation.

The preregistered outcome is `NO_TESTED_REPRESENTATION_RESCUE`. The bounded causal
classification is `REPRESENTATION_INSUFFICIENT_UNDER_BLOCKED_ONLINE_LINEAR_HEAD`,
with a remaining interaction question between presentation order and the joint
representation. It does not establish failure of all grounded representations,
all curricula, or nonlinear grounded value heads.

Evidence: `R32_E47_TERMINAL_REPRESENTATION_DISCRIMINATOR_NEGATIVE_B7B49F4D_NO_TESTED_REPRESENTATION_RESCUE_EVIDENCE.json`.

## E48 one-pass online versus batch fit — valid native negative

E48 isolated a remaining training-dynamics question without changing the causal
world generator, targets, auxiliary snapshot, validation grid, or UNKNOWN
semantics. M0/M1 were the exact blocked one-pass online baseline/joint pair. M2/M3
instead used an order-invariant, complete-dataset integer batch fit from the same
fresh 55,080 canonical records, with either baseline features or the joint E47
co-viability and support/contradiction co-mass features.

The batch algorithm was frozen before validation. It builds complete-dataset
sufficient statistics, takes deterministic coordinate sweeps, and retains only
strict reductions in the exact fixed-point clipped training loss. Forward and
reverse record traversal produced identical statistics, final parameters, loss
traces, and stopping points: 28 accepted baseline sweeps and 12 joint sweeps,
each ending at the first non-improving sweep. This makes it a test of one-pass
online versus this specified batch fit—not a proof that presentation overwrite is
the sole cause, nor that no linear solution exists.

The source SHA256 is
`24e8098f805fa1f1548250ac5c7968658caeb8293534b2cb5f2ae0d06d442d0a`.
Two official x86-64 builds were byte-identical at binary SHA256
`5efdab6533f66fabe9ef90c9edd6092e8c90cceeef58c8fe44e1fd4dc680a884`.
The fully inspectable 1,065-second native ledger has SHA256
`0df6a38241c63275f0fd2eea15154875dadbce46580921811ba7fcec00f5d950`.
It contains all canonical rows, all final terminal parameters, the forward/reverse
batch audit, and the complete fresh validation grid. Integrity passed and sealed
confirmation was not executed.

| Model | No-unique UNKNOWN | No-unique wrong | Safe cells | Known success | Known wrong |
|---|---:|---:|---:|---:|---:|
| M0 online baseline | 0 | 20,400 | 0/1,020 | 54,182 | 17,218 |
| M1 online joint | 0 | 20,400 | 0/1,020 | 54,182 | 17,218 |
| M2 batch baseline | 12,219 | 8,181 | 346/1,020 | 50,338 | 2,158 |
| M3 batch joint | 12,260 | 8,140 | 318/1,020 | 48,575 | 1,632 |

Batch fitting therefore moved the controller strongly toward abstention and
reduced wrong commitments, but neither batch arm was safe in every no-unique
cell and both lost pooled known-truth success versus M0. The terminal UNKNOWN
target remained zero on all 55,080 samples; the UNKNOWN bias and all UNKNOWN-head
weights stayed exactly zero, so abstention still required every commit value to
fall below grounded zero.

The preregistered outcome is `NO_TESTED_BATCH_SAFETY_RESCUE`. The bounded causal
classification is `ONE_PASS_ONLINE_VS_SPECIFIED_BATCH_FIT_INSUFFICIENT_WITH_CURRENT_LINEAR_VALUE_GEOMETRY`. It rejects neither richer endogenous causal features,
nonlinear grounded value heads, nor a separately justified grounded nonzero
UNKNOWN value. R27 remains canonical.

Evidence: `R32_E48_ONLINE_BATCH_REPRESENTATION_NEGATIVE_24E8098F_NO_TESTED_BATCH_SAFETY_RESCUE_EVIDENCE.json`.

## E49 grounded quadratic commit-value discriminator — valid native negative

E49 retained E48's order-invariant batch fitting, evaluator, targets, fresh
grid, and joint E47 representation. It changed one capacity coordinate only:
the otherwise masked terminal slot 13 held
`trunc(co_viability × support/contradiction_co_mass / 1000)` for M1, while M0
kept that slot zero. The helper takes neither evaluator labels nor targets.

The source SHA256 is
`62326d5874ae77aa4ceb542807cedfed7e91d72ab158aa453ea1db6aa92214c7`.
Two official builds were byte-identical at SHA256
`09bf24bc8e181da7096985a26daf14381f62196c0b7a57621f31651ffa2a6869`.
The 1,025-second raw native ledger SHA256 is
`fdc5c08d5637975a673c75610cc25cd63f243a91bb8b8d358a537aed02730d38`.
Integrity passed, including E45–E48 seed reservation, exact zero UNKNOWN targets,
36,594 interior quadratic records, batch forward/reverse identity, and all 9,180
fresh validation cells at 20 observations each.

| Model | No-unique UNKNOWN | No-unique wrong | Known success | Known wrong |
|---|---:|---:|---:|---:|
| M0 E48-joint batch control | 12,354 | 8,046 | 48,350 | 1,449 |
| M1 + grounded quadratic slot 13 | 11,754 | 8,646 | 48,615 | 1,541 |

The treatment added 265 known successes but also 92 known wrong commitments; more
importantly, it made 600 fewer no-unique UNKNOWN choices and 600 more wrong
commitments. It failed the every-cell no-unique gate and therefore cannot be
called a safety rescue. The bounded outcome is
`NO_TESTED_GROUNDED_QUADRATIC_RESCUE`. It does not reject all nonlinear grounded
value mechanisms or richer endogenous causal representation. R27 remains
canonical.

Evidence: `R32_E49_GROUNDED_QUADRATIC_COMMIT_VALUE_NEGATIVE_62326D58_NO_TESTED_QUADRATIC_RESCUE_EVIDENCE.json`.

## E50 provenance and temporal contention representation — valid native negative

E50 retained the E49 matched joint batch control and added two endogenous
terminal coordinates only: provenance-adjusted co-viability
`trunc(slot3 * source_diversity / 1000)` and transition contention
`min(transition_support, transition_counterevidence)`. Neither helper receives
mode, truth, seed, count, target, resource, or time. The fresh 55,080-record
native run passed its seed, input, structural, batch, UNKNOWN-head, and complete
9,180-cell validation integrity checks. The new terms were interior on 55,080
and 8,852 records, respectively.

M1 moved no-unique validation from 12,488 UNKNOWN / 7,912 wrong to 12,428
UNKNOWN / 7,972 wrong: 60 less abstention and 60 more wrong commitments. It
failed every-cell no-unique safety (`complete_gate=0`) and returned
`NO_TESTED_GROUNDED_PROVENANCE_TEMPORAL_CONTENTION_RESCUE`. This is a valid
negative for the paired representation under the frozen batch mechanism; R27
remains canonical.

Evidence: `R32_E50_PROVENANCE_TEMPORAL_CONTENTION_NEGATIVE_3ECA4702_NO_TESTED_CONTENTION_RESCUE/EVIDENCE.json`.
