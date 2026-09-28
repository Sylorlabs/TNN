# R32 V10 preliminary confirmation — fresh seeds 9711–9713

Status: **REFERENCE_ONLY / RETAIN V10 MECHANISM / HARDER DIAGNOSTICS REQUIRED**

V10 preserves the exact R31-derived A control and the R32 persistent-hypothesis/provenance/temporal-instability representation. Relative to V9, the only scientific change is decision economics: `UNKNOWN` is the neutral zero-regret fallback; correct/wrong commit value is learned from delayed grounded outcomes; observations pay full cost through next-state Bellman credit. No ambiguity label, confidence threshold, fixed probe count, transformer/tokenizer/VAD, or graph cognition is used.

Three fresh seeds (9711–9713), 40 evaluations per condition, give:

- **core hard correctness:** D **0.9792** vs A **0.9819**
- **expanded resolvable correctness:** D **0.9811** vs A **0.9283**
- **genuine-ambiguity UNKNOWN:** D **0.6500** vs A **0.5000**
- **mean wrong commitment:** D **0.0270** vs A **0.0956**
- **cost-too-high abstention:** D **0.2917** vs A **0.2250**
- **entity replacement correctness:** D **0.9917** vs A **0.7750**
- unnecessary abstention remains low (D ~**0.0139**)

The primary R32 success pattern is therefore present in this preliminary panel: ambiguity recognition is materially above the historical R31 ~0.5717 boundary while average difficult-resolvable correctness remains above ~0.97.

## Causal classification

- Persistent hypotheses alone do not hurt R31 (B reproduces A).
- Provenance-only state is not the main source of gain.
- V7 showed temporal/source instability adds useful ambiguity signal.
- V8 exposed a reusable-observation credit bug on fresh seed 9711.
- V9 fixed runaway inspection but still had incorrect abstention economics.
- V10's neutral-abstention Bellman economics repairs both while retaining the R31 hard frontier on average.

**Retain:** V10 decision formulation + temporal/provenance epistemic state.

## Boundary / next challenge

Do not call ambiguity solved. The evaluation count is still modest, and source-7 repeated trials are rare in genuine-ambiguity cases. Next run must deliberately make one-shot evidence insufficient and force the policy to decide whether repeated same-apparatus consequence trials are worth their cost. It must include:

- truly no-unique-answer alternating/stochastic consequences;
- biased-but-nonunique evidence;
- temporarily unstable evidence that later becomes stable;
- stable weak evidence requiring repeated trials;
- same-lineage dependence so repetition cannot become fake independent votes;
- expensive decisive evidence where UNKNOWN is economically rational;
- entity replacement and apparent replacement reversal during repeated observation.

Promotion remains blocked until native Zag qualification; R27 remains canonical.
