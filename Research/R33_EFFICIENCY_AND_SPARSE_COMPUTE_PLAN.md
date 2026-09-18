# R33 efficiency and sparse/conditional computation

Status: prospective; execute after usable dense/reference mechanisms exist.
Never trade away retention, transfer, robustness or inspection to claim savings.

## Candidate mechanisms

Routed PAMs/experts, block-sparse interactions, event-driven processing, local
recurrence, lazy motif expansion, associative retrieval, memory tiering, shared
motifs, conditional module activation and learned resource allocation. Measure
each mechanism separately before combining it into a recipe.

## Comparison views

At matched capability, minimize measured active cost while holding required
retention/transfer/robustness floors. At matched active compute, test whether
larger stored sparse capacity helps. At matched total resource envelope, allow
the learner to allocate computation and memory while recording that allocation.
Also show equal-storage and equal-training-compute views; do not imply that all
budgets were matched simultaneously.

Dense gates, cache misses, retrieval, event queues, padding, load imbalance,
bookkeeping, traces, checkpointing and canary/search costs count. Logical
operation estimates and measured CPU/wall time have different meanings; report
both where possible and record hardware/build/precision/concurrency.

## Matrix and reporting

Use the [capacity plan](R33_PARAMETER_SCALING_PLAN.md) for cell/region definitions.
Vary active region count at fixed stored capacity; stored region count at fixed
target active budget; sparse pattern at fixed nonzero count; shared versus
specialized parameters; and event-driven versus fixed-period updates on the same
stream. Include a dense and an unchanged-parent control.

Plot capability against active inference operations, training operations, memory
bytes and human interventions. Show a Pareto set rather than one composite score
that can hide a violated floor. Record per-seed distributions and worst required
slices. Efficiency under one easy routing distribution is not universal savings.

## Falsifiers

Savings disappear after routing/lookup cost; inactive capacity is inaccessible;
rare skills are forgotten; delays grow unbounded under contention; repeated
shared-source evidence is overcounted; raw retrieval is suppressed; audit logs
are sampled away; or sparse arms receive extra help. A failed sparse variant
does not rule out conditional computation as a family.

The inherited compute-efficiency document contains an empty result table and
describes an evaluator, not an endogenous allocator. R33 will not copy it as
measured efficiency evidence.
