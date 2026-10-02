# R32 E51M — Calibration Training-Dose × Boundary-Capacity Curve

Date frozen: 2026-08-30
Branch: `r32-agent-sequential-frontier`
Canonical status: R27 remains canonical.

## Causal basis

E51K showed that rank-preserving scalar calibration errors are already present on development worlds, so the current bottleneck is not primarily fresh-world transfer. E51L showed that top-commit sign supervision moves the frontier strongly toward valid commitment but still cannot fit the harmful-commit side well enough; four learner-selected hinge bases recover some negative-side discrimination without solving the tradeoff.

Before introducing a qualitatively different calibration mechanism or connection topology, E51M follows the training-first protocol and measures whether the same scalar decision system improves with **more development worlds** and **more learner-owned generic boundary capacity**.

## Constraints

- Native Zag v2 only.
- Same primary 32-feature learner-visible terminal state.
- Same frozen base terminal action-ordering head for every arm. It is trained only on the first 1× development subset so calibration dose is isolated from action-ranking dose.
- UNKNOWN is fixed at score 0; no UNKNOWN classifier or positive UNKNOWN target.
- Scalar sign target is the E51L consequence-derived target of the frozen learner-selected top commit: +1000 if its grounded utility is positive, -1000 if negative, 0 if neutral.
- One scalar shift applies equally to KEEP/CURRENT/RESTORE, preserving their ordering exactly.
- Evaluator truth, ambiguity membership, seed/stage identity, validation membership, and audit margins are never learner inputs.
- No graph/topology rewrite, hand-selected feature, confidence threshold, or ambiguity detector.
- Validation is common and untouched across all arms.
- Confirmation is sealed unless an exact validation gate passes.

## Fresh partitions and nested dose

Allocate one maximum development population using stage 52:

- 1× dose: first 3,240 episodes / 55,080 states;
- 2× dose: first 6,480 episodes / 110,160 states;
- 4× dose: all 12,960 episodes / 220,320 states.

The smaller doses are strict prefixes of the larger dose, so the curve changes training exposure rather than world identity.

Use stage 53 for one common untouched validation population of 5,400 episodes / 91,800 states.
Use stage 54 for 10,800 confirmation episodes allocated and sealed.

## Capacity curve

For each dose independently:

1. fit one deterministic linear scalar sign calibrator;
2. run one learner-owned greedy data-mean hinge residual search with a maximum of 16 accepted terms;
3. evaluate the same learned sequence at prefixes of 0, 4, 8, and 16 accepted terms.

Thus the full calibration grid is:

- doses: 1×, 2×, 4×;
- hinge capacities: 0, 4, 8, 16;
- 12 calibrated arms total, plus one uncalibrated frozen-base control.

Feature identity, hinge direction, data-derived mean, coefficient, and stopping point are selected only from the corresponding development prefix by strict squared-loss improvement. A capacity prefix cannot use later terms.

Resource ceilings are experimental ceilings, not cognitive knowledge.

## Deterministic variable-dose fitter

Because existing E50/E51G batch helpers are fixed to 55,080 records, E51M may implement an equivalent generic scalar coordinate-descent fitter whose sample count is an explicit argument. It must:

- use only the same scalar sign targets and learner-visible features;
- start from zero parameters;
- traverse every supplied record for every accepted sweep;
- clamp bias/weight parameters to the existing E50 bounds;
- accept only strictly lower full training squared error;
- reproduce identical final parameters, accepted sweeps, stop reason, and loss trace under forward/reverse record traversal for every dose.

The same requirement applies to the variable-dose hinge search: means, selected term sequence, coefficients, accepted count, final loss, and trace must be forward/reverse identical.

## Required measurements

For each of the 12 calibrated arms report:

- development positive/negative decision-side sign accuracy;
- common validation positive/negative decision-side sign accuracy;
- validation known episode reachability;
- validation no-unique UNKNOWN reachability;
- actual accepted hinge count available at the requested prefix.

Also report the uncalibrated base validation reachability.

Decision-side convention remains: beneficial commit prediction `>= 0` is commit-side; harmful commit prediction must be `< 0` to expose UNKNOWN.

## Integrity gates

Before interpretation require:

1. E50 parent integrity passes;
2. maximum-development + validation + confirmation seed allocation has zero failures;
3. exact counts: 12,960 max development, 5,400 validation, 10,800 confirmation allocated / 0 executed;
4. base UNKNOWN targets/parameters remain zero;
5. every dose has both positive and negative sign targets;
6. every dose's scalar fit is forward/reverse identical;
7. every dose's hinge sequence is forward/reverse identical;
8. at least one dose recruits more than four hinge terms if strict improvement remains available; if not, the earlier stop itself is the capacity result;
9. no evaluator-only quantity becomes a learner input.

## Validation gates

Exact rescue: any calibrated arm reaches **4,200 / 4,200 known** and **1,200 / 1,200 no-unique UNKNOWN** with all integrity gates passing.

A monotonic-training signal requires increasing dose at a fixed capacity to weakly preserve known reachability and improve no-unique reachability, or vice versa without worsening the other dimension. A monotonic-capacity signal is defined analogously at fixed dose.

## Frozen outcomes

- `CALIBRATION_DOSE_CAPACITY_RESCUE`: an arm reaches the exact gate.
- `CALIBRATION_DOSE_SIGNAL`: increased training dose produces a reproducible Pareto improvement even without exact rescue.
- `CALIBRATION_CAPACITY_SIGNAL`: increased hinge capacity produces a reproducible Pareto improvement even without exact rescue.
- `CALIBRATION_DOSE_CAPACITY_PLATEAU`: no tested increase in dose or capacity gives a meaningful Pareto movement toward exact reachability.
- integrity failure: invalid experiment.

If the grid plateaus while development sign error remains substantial, a qualitatively richer **learner-owned local/prototype calibration memory** becomes justified on the same state before any broader connection-topology rewrite. If dose produces a clear Pareto trajectory, continue training/curriculum diagnosis before changing mechanism.

No E51M result can promote R32 or establish AGI.
