# R32 E55B — Coordinate-Separable Joint Policy Validation

Date: 2026-08-30  
Status: `PREREGISTERED NATIVE VALIDATION — FROZEN BEFORE FRESH VALIDATION`  
Canonical: **R27 step 60,423**  
Parent: E55A native development diagnostic

## Frozen development result

E55A reproduced the conservative continuation policy C and then froze it. Exact forward/reverse terminal fitting on C's reached development states produced the E52A-basis coefficient vector:

`[-4887, 205, 1152, 113, -220, 1846, -841, 39]`

The preregistered generic damping search selected **1/4** as the best safe development terminal update. E55B therefore freezes the joint terminal coefficients to:

`[-1221, 51, 288, 28, -55, 461, -210, 9]`

Development metrics for the frozen coordinate candidate were:

- net utility 496,943 versus C 421,543 and terminal control 254,600;
- known success 1,071 versus control 1,015;
- known wrong 18 versus control 166;
- no-unique wrong 334 versus control 357;
- observations/opportunity loss identical to C: 1,242 / 137,257.

No validation world was consumed by E55A.

## Hypothesis

The E53/E54 joint failure was caused by forcing terminal and continuation refits into one candidate step. A coordinate-separable policy—learn continuation conservatively first, freeze it, then add a conservative terminal update on the already learner-selected E52A basis—should retain the continuation learner's observation economy while improving terminal decisions.

## Frozen mechanism

- full native Zag v2;
- R27 unchanged/canonical;
- UNKNOWN value fixed at neutral 0;
- no ambiguity labels, target, evaluator mode/resource, time index, remaining horizon, fixed observation count, or validation information in cognition;
- reproduce C from the frozen 3,240 development episodes using the E53 conservative optimizer;
- reproduce the E55A terminal fit forward/reverse and require the exact fitted and 1/4-damped coefficient vectors above;
- freeze C plus the 1/4 terminal vector before evaluating validation;
- no validation-driven refit or coefficient selection.

## Fresh evaluator namespace

E55B uses a new deterministic evaluator namespace, modulus **2,140,001**, distinct in provenance from legacy, E53, and E54 namespaces. Same world-family semantics; zero within-namespace component collisions/failures required.

- validation: 2,700 episodes (10 per base/mode/resource cell);
- sealed confirmation: 5,400 episodes allocated and hashed before validation, not executed unless every validation gate passes.

## Matched arms

1. A — frozen terminal-only control.
2. B — E52B-style naive on-policy continuation reference.
3. C — stable conservative continuation with frozen terminal geometry.
4. D — **coordinate-separable joint policy** = frozen C continuation + frozen E55A 1/4 terminal coefficients.

## Validation gates

D must satisfy all of:

- native/integrity/allocator/fit identity PASS;
- frozen coefficient reproduction PASS;
- deterministic stable C policy/reached distribution;
- positive net utility and utility > A, B, and C;
- known success >= A and known wrong <= A;
- no-unique wrong < A;
- strict every-populated-no-unique-cell safety (zero wrong commits in every populated no-unique cell);
- nontrivial continuation in a strict subset of feasible episodes;
- terminal reachability improvement relative to A.

If any gate fails, confirmation remains sealed and E55B is a native negative/partial result. No validation tuning is allowed.

## After E55B

If coordinate separation generalizes but strict no-unique safety remains the blocker, the next experiment may increase **learner-owned sparse structural connectivity** for the continuation/terminal value functions. That structural-plasticity phase must expose generic connection creation/pruning under resource pricing rather than manually adding an ambiguity feature.
