# Novel TNN experiment portfolio — 2026-09-11

These are new hypotheses, not results. Each has an engineering microbenchmark
that can be run without canonical R27 and a later scientific phase that remains
blocked until N17+N19 qualify.

## E01 — adaptive support-manifold routing

Hypothesis: N16 arm19 works because updates are routed away from a compact
old-support subspace. A fixed 75%-mean projection may leave avoidable plasticity
on the table. Maintain a bounded support basis whose rank expands only when
pointwise old-loss pressure rises and contracts when redundant.

Controls: unprojected update; fixed N16-style projection; random basis;
matched-rank static basis.

Primary endpoints: new-task gain, max pointwise old deficit, total old loss,
active basis rank, projection FLOPs/storage, recovery determinism.

Falsifier: no Pareto improvement over fixed projection after charging rank
selection and support-maintenance cost.

## E02 — conflict-triggered specialist isolation

Hypothesis: create/use a specialist only when the proposed update has measured
conflict with protected support, rather than routing every update through the
same specialist policy.

The trigger must be computed from learner-visible support statistics, not
evaluator labels. Compare fixed-always-specialist, never-specialist, random
trigger and threshold trigger under equal exposure and resource accounting.

Falsifier: trigger cost or false isolation eliminates its retention/plasticity
frontier advantage on fresh conflicts.

## E03 — future-relevance rehearsal memory

Hypothesis: memory autonomy improves when rehearsal priority estimates future
decision utility rather than recency/frequency alone. Hidden future relevance
is revealed only by later consequences, so the learner must update the priority
model from experience.

Controls: keep-all, FIFO, LRU, random, frequency, compression-only and fixed
rehearsal. Endpoints include delayed utility, eviction regret, retrieval cost,
retention, spill/refusal and fresh-process replay.

Falsifier: learned rehearsal does not outperform simple LRU/frequency at matched
memory+compute or leaks hidden relevance.

## E04 — uncertainty-budgeted active inquiry

Hypothesis: a TNN should spend observation/intervention budget when expected
uncertainty reduction times downstream consequence value exceeds cost.

Controls: passive, random query, fixed periodic query, uncertainty-only query.
Measure decision accuracy, cumulative consequence, query cost, calibration and
information gained per unit cost.

Falsifier: value-aware inquiry fails to dominate simpler uncertainty/random
controls on unseen ambiguity families.

## E05 — motif-generated connectivity with exact reconstruction

Hypothesis: repeated connection patterns can be stored as motifs plus bounded
instance parameters, reducing stored state while preserving exact or explicitly
bounded reconstruction.

Engineering phase: deterministic generate→materialize→hash→reconstruct round
trip, bounded expansion, collision/provenance checks and full cost accounting.

Scientific phase: compare dense explicit connectivity, random motifs, static
hand-authored motifs and learned motif proposals under matched capability and
retention floors.

Falsifier: stored-state savings disappear after expansion/provenance/cache costs
or reconstruction changes protected behavior.

## E06 — structural-value meta-controller

Hypothesis: before proposing a structural change, a metacontroller can predict
whether the expected reduction in persistent failure exceeds construction,
validation, rollback and ongoing compute cost.

The predictor is trained only on prior learner-visible experiment history; final
accept/reject truth remains behind the protected supervisor. Compare random,
evolutionary, fixed-rule and learned proposal-selection policies on unseen
failure families.

Falsifier: predicted value is uncalibrated, cannot beat simple controls after
search cost, or exploits evaluator/holdout leakage.

## Priority

E01 is first because it directly generalizes the only replicated new R33
learning mechanism (N16 arm19). E02 is next as a complementary routing policy.
E03/E04 build autonomy, E05 addresses storage/connectivity efficiency, and E06
belongs after shadow structural authority is qualified.

No scientific population for E01–E06 may be allocated from this document.
Each later batch needs a fresh identity/namespace, frozen native source,
preregistration, independent review, sealed assessment and complete resource
ledger. Engineering microbenchmarks must be labeled as such and cannot be
promoted into capability evidence after the fact.
