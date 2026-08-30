# R32 E53 — Conservative Average-Cost Joint Policy Improvement

Date: 2026-08-30  
Status: `PREREGISTERED NATIVE DISCRIMINATOR — FROZEN BEFORE EXECUTION`  
Canonical: **R27 step 60,423**  
Parent evidence: E51D → E52A → E52B

## Causal question

E52B showed that reached-state/on-policy fitting contains real epistemic leverage (+288 known successes and -108 known wrong commitments in its primary comparison), but naive repeated refitting oscillated between endogenous reached-state distributions and spent more observation value than it recovered. E53 asks whether a generic conservative average-cost policy-improvement substrate can stabilize that endogenous distribution shift and learn the long-run shadow price of observation without adding a researcher-authored ambiguity feature.

This is a decision/credit-assignment experiment, not a new representation experiment.

## Immutable scientific boundary

- R27 remains canonical and is not modified.
- Maintained cognition and experimental mechanism are **native Zag v2**.
- The persisted official Linux x86-64 Zag compiler under `Research/toolchain/` is the compilation authority.
- `UNKNOWN` remains a neutral terminal action with value **0**. It receives no positive target, ambiguity reward, confidence threshold, or privileged feature.
- Policy/features may not receive evaluator truth, evaluator mode, resource ID, target, ambiguity class, fixed observation count, time index, remaining horizon, or sealed-validation/confirmation information.
- Evaluator truth may be used only after an action for delayed utility/regret targets and external qualification gates.
- No validation or confirmation result may be used to select architecture, coefficients, replay mixture, shadow price, damping, or stopping criteria.

## Frozen parents

### Terminal substrate

The E50 model-0 terminal linear geometry is the frozen terminal control. E53 also preserves the **learner-selected E52A terminal basis** as the joint-policy basis:

- KEEP: `(21×23)`, `(19×21)`
- CURRENT: `(1×23)`, `(0×1)`, `(1×19)`
- RESTORE: `(1×23)`, `(0×1)`, `(1×19)`
- UNKNOWN: no trainable interaction and value 0

E52A's learned coefficients are the initial joint-policy coefficients. In the joint treatment, only coefficients on this already learner-selected basis may be re-estimated from reached development states; E53 does not hand-select a new terminal feature pair.

### Continuation substrate

The E51B/E52B continuation action remains an advantage in the same grounded utility units as terminal actions. Observation incurs its actual opportunity loss. The continuation policy has no initiation heuristic separate from the learned action value.

## Four matched arms

All arms receive matched worlds and the same protected substrate.

1. **A — terminal-only control:** frozen E50 model-0 terminal policy, no continuation.
2. **B — naive on-policy control:** deterministic E52B-style repeated reached-state refitting against the frozen terminal policy.
3. **C — conservative continuation:** frozen terminal policy plus conservative replay-based continuation improvement.
4. **D — conservative joint policy:** E52A terminal interaction basis plus conservative replay-based terminal-coefficient and continuation improvement.

## Learner-owned conservative optimizer

The protected substrate may provide exact sufficient-statistic accumulation, deterministic replay storage, candidate enumeration, resource accounting, policy/reached-state hashing, rollback, and bounded generic pair-product primitives. It does not encode which environmental condition is ambiguous or which action is correct.

For C and D, each development iteration performs:

1. roll the current policy through every development episode;
2. record only states actually reached by that policy and the actual delayed terminal/continuation utility and observation opportunity cost;
3. retain prior accepted reached-state distributions in replay;
4. build deterministic candidate replay mixtures from current and prior accepted distributions;
5. refit continuation value exactly on each candidate replay ledger;
6. allow the existing generic sparse pair-product Foundry to select at most four continuation interactions from development residual reduction;
7. for D, re-estimate coefficients only on the frozen E52A terminal interaction basis using reached terminal-state residuals;
8. derive candidate observation shadow prices from the current policy's observed opportunity-cost distribution and current shadow price rather than from evaluator mode/labels;
9. derive candidate update damping from generic bounded fractions of the fitted update;
10. evaluate each candidate on the **complete development set**;
11. accept only a candidate that strictly improves complete-development net delayed utility after actual observation cost while satisfying the frozen external development safety constraints;
12. otherwise roll back exactly.

### Generic candidate families

To keep the experiment finite while leaving the decision to development utility, the optimizer exposes only generic candidates:

- replay emphasis: current-only and progressively stronger retention of prior accepted reached distributions;
- parameter damping: full, half, quarter, and eighth fitted updates;
- shadow price: current shadow, observed mean step opportunity cost, half/double that observed mean, and the midpoint between current and observed mean;
- continuation structure: generic bounded pairwise feature products, maximum four accepted interactions;
- terminal structure in D: **only** the eight pairs already selected by E52A; coefficients may change, pair identity may not.

The learner chooses among these candidates solely by complete-development delayed net utility subject to external frozen safety constraints. Tie-break order is: higher net utility, fewer observations, fewer wrong commitments, then deterministic lexicographic candidate order.

## Frozen development acceptance constraints

A proposed C/D update is accepted only if:

- complete-development net utility strictly exceeds the currently accepted policy;
- known-success count is not below the terminal-only development control;
- known-wrong commits are not above the terminal-only development control;
- no-unique wrong commits are not above the terminal-only development control;
- policy inputs remain evaluator-blind;
- deterministic forward/reverse sufficient statistics and candidate choice agree.

These constraints are external optimizer/qualification constraints. The labels used to compute them are never inserted into policy features.

Maximum conservative improvement rounds: **6**. An exact repeated policy hash or reached-state hash is treated as a cycle; the repeated candidate is rejected and the conservative loop stops. A round with no accepted candidate also stops.

## Development and independence boundary

Development reuses the frozen E52/E51B development worlds (**3,240 episodes**) so E53 changes the optimizer rather than the development distribution.

E52B established that the original one-million-state simulator namespace can no longer provide component-disjoint validation/confirmation reservations. E53 therefore preregisters an **expanded independent simulator RNG namespace**:

- E53 RNG modulus: `2,000,003`;
- same bounded world-family semantics, but a separate deterministic RNG state space;
- validation and confirmation seeds are allocated component-disjoint within that namespace across raw, truth/history/passive/active evidence, and resource streams;
- the namespace itself is distinct from every pre-E53 reservation, so an `(E53 namespace, component state)` cannot collide with a prior `(legacy namespace, component state)`;
- any within-E53 component collision or allocation failure invalidates the experiment.

Validation: **2,700 episodes** (10 per base/mode/resource cell).  
Sealed confirmation: **5,400 episodes**, allocated and hashed but not executed unless every validation/integrity gate passes.

A generator-namespace change is evaluator infrastructure only and is matched across A/B/C/D. It does not enter cognition.

## Determinism and native authority

Required before behavioral interpretation:

- E50 parent integrity passes;
- E53 preregistration hash is recorded before native result generation;
- native Zag v2 source is assembled deterministically;
- source SHA-256 recorded;
- persisted compiler SHA/provenance recorded;
- source compiled twice independently;
- resulting binaries are byte-identical;
- deterministic forward/reverse fitting and candidate-selection traces agree;
- development replay/policy hashes reproduce;
- expanded-namespace allocator reports zero component collisions/failures;
- raw validation ledger SHA-256 and checksum manifest are retained;
- confirmation execution count remains zero unless every gate below passes.

## Validation gates

No gate may be tuned after seeing validation.

D is the primary treatment and must satisfy all of:

1. **distribution stability:** final policy and reached-state distribution reproduce exactly on an independent deterministic reroll; no unresolved policy-hash cycle;
2. **net utility:** positive net grounded utility after observation cost and strictly greater than A and B;
3. **observation economy:** observation/opportunity cost materially below B unless greater cost is more than repaid by net utility;
4. **known-case non-inferiority:** known success >= A and known wrong commits <= A;
5. **no-unique safety:** no-unique wrong commits < A, with material improvement rather than a single incidental case;
6. **every-cell analysis:** every populated no-unique cell is reported; the strict safety gate requires no wrong commitment in any populated no-unique cell;
7. **terminal reachability:** the E52A-basis joint terminal geometry must reduce the count of validation episodes with no reachable safe/correct terminal action relative to A;
8. **nontrivial continuation:** continuation occurs in a strict subset of feasible episodes rather than always-stop or always-continue collapse;
9. **integrity/allocator:** every native, determinism, provenance, and expanded-namespace gate passes.

If any gate fails, E53 is retained as a native negative and **confirmation remains sealed**. No validation-driven patch is permitted.

## Confirmation and R27 comparison

Only if all E53 validation gates pass:

1. execute the already allocated 5,400 sealed confirmation worlds once;
2. require the same qualitative and preregistered quantitative gates;
3. freeze E53;
4. only then run the broad R27 capability/regression battery.

R32 is not promoted merely for beating E52B. Promotion requires broad R27 non-inferiority/superiority across retained capability, safety, efficiency, persistence, and reproducibility gates.

## Explicitly prohibited follow-ups inside this experiment

- manually adding an ambiguity detector or confidence feature;
- giving UNKNOWN a positive target;
- choosing a fixed observation count;
- using evaluator mode/resource/time/horizon as cognition inputs;
- changing the E52A terminal pair identities after validation begins;
- opening confirmation because a subset of validation metrics looks promising;
- starting the dynamic-connectivity/structural-plasticity phase before E53 is resolved.

## Interpretation boundary

A pass would support the hypothesis that the R32 bottleneck was stable endogenous average-cost policy improvement rather than missing uncertainty representation. A failure should be localized by its native traces (utility, cost, reachability, oscillation, safety, approximation capacity) and followed by the smallest preregistered discriminator. It would not justify hand-authoring a task solution.
