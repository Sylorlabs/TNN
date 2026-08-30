# R32 E53A — Learner-Owned Meta-Control Pressure Test

Date: 2026-08-30  
Status: `PREREGISTERED NATIVE DIAGNOSTIC — FROZEN BEFORE EXECUTION`  
Canonical: R27 step 60,423  
Parent: E53 conservative-policy core; E52B on-policy instability

## Why this test exists

The E53 core exposes conservative update primitives, but several consequential inputs remain caller supplied: update rate, replay mass, residual clip, and value bounds. Calling these values "learner-owned" is not sufficient unless a native learner actually selects them from its own experience.

E53A is a bounded ownership-pressure test. It asks whether TNN can select among generic policy-update geometries from delayed grounded objective and then change the selected geometry online as learner-visible state changes, without an evaluator regime label entering the selector.

This is **not** the full E53 behavioral discriminator and cannot promote R32.

## Fixed meta-action vocabulary

The protected test substrate exposes six generic candidate update geometries. Each candidate specifies only:

- update rate;
- replay mass;
- residual/trust-region clip.

The six candidates span slow/high-replay through fast/no-replay behavior. The candidate vocabulary itself remains researcher supplied and is therefore only a partial ownership transfer. TNN owns **which candidate is valued and selected in a learner-visible state**.

## Learner-visible meta-state

The selector receives only a generic endogenous discrepancy derived from the learner's current policy value and its retained replay anchor. It does not receive:

- evaluator family/regime ID;
- truth label;
- ambiguity/no-unique label;
- seed identity;
- tape time or remaining horizon;
- benchmark target class;
- graph/topology identity.

The discrepancy is discretized into three generic magnitude regions solely for this bounded diagnostic. Representation ownership is not claimed.

## Development

Development experience deterministically visits all six meta-actions with equal exposure. For each reached learner-visible meta-state, TNN accumulates delayed objective for the chosen candidate and stores value as grounded utility per visit.

No validation record updates the learned values.

## Validation

A fresh deterministic validation sequence alternates among learner-visible low, medium, and large discrepancy states. The evaluator changes latent target/noise conditions, but those family identities are never passed to the selector.

The learned arm chooses the highest learned meta-action value for the current learner-visible meta-state. It is compared with all six fixed meta-actions on the exact same validation records.

## Delayed objective

For a proposed scalar policy update:

`objective = 3 * reduction_in_grounded_absolute_error - parameter_churn`

This rewards useful correction while charging the magnitude of the internal modification. The learner sees only the realized scalar objective after its candidate is exercised.

## Required outputs and success gate

The native test must emit:

- learned value for every meta-state × meta-action;
- selected action for every meta-state;
- selected rate/replay/clip for every meta-state;
- adaptive validation cumulative objective;
- cumulative objective for all six fixed controls;
- best fixed-control objective;
- adaptive action diversity and action-switch count;
- UNKNOWN protected-zero check;
- evaluator-label-absent and graph-not-required checks;
- two-build byte identity and source hash in CI.

The diagnostic passes only if:

1. development exposure is balanced and every meta-state/action has nonzero grounded experience;
2. at least three distinct meta-actions are selected across learner-visible states;
3. the learned selector changes meta-action when state changes;
4. adaptive validation objective is strictly greater than the best of all six fixed controls;
5. UNKNOWN remains zero;
6. evaluator family/regime identity is absent from the selector call graph;
7. no graph substrate is required.

A pass means only that **meta-control selection can be transferred from a caller schedule into learner-valued state in this bounded native diagnostic**. It does not prove full self-modification, representation ownership, arbitrary connection rewriting, or AGI.