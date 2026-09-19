# R32 V23 — Residual INSPECT/WAIT Fusion Gate

Status: **REFERENCE_ONLY / REJECT BEFORE HARDENING**

V23 keeps the inherited recursive INSPECT Q and trains only a residual correction from current epistemic state, inherited INSPECT Q, and V21 WAIT expected utility. The residual target is delayed realized source-specific inspect return minus inherited INSPECT Q.

Held-out validation rejects the repair: inherited INSPECT MSE is **0.1441** versus fused **0.1501**; inherited benefit AUC is **0.8272** versus fused **0.8220**. The mean residual target is approximately zero (-0.0022), indicating the direct INSPECT model is already well-scaled for its own target.

## Causal classification

The V21 WAIT signal is **not merely a missing residual correction to source-specific INSPECT Q**. Forcing it into that role does not improve held-out action-value prediction. Combined with V21/V22, this points to a distinct temporal decision variable: expected future resolvability/horizon, not another estimate of immediate source-action utility.

## Decision

Reject V23 without hardening because its matched validation gate fails. Retain V19 INSPECT Q, V18 unresolved hypothesis, V21 beneficial-WAIT classifier as diagnostic evidence. Next construct an explicit time-to-resolution / convergence-hazard process from delayed grounded trajectories; use it to decide WAIT versus terminal action without replacing INSPECT values.
