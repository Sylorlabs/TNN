# R32 V41 — Live Fresh-Stream Horizon-Hazard Qualification

Status: **REFERENCE_ONLY / OFFLINE GAIN PARTIALLY REPLICATED / LIVE RESOLUTION STILL REJECTED**

V41 deployed the retained V40 `horizon_hazard_variance` INSPECT-value model into a live sequential policy on fresh episode streams. It held the V19 delayed-trained COMMIT / UNKNOWN terminal controller fixed and compared:

1. terminal controller with no extra evidence;
2. V38 repeated-mean/variance evidence acquisition;
3. V40 horizon-hazard/variance evidence acquisition.

Evaluation used seven epistemic modes × five fresh resource contexts × 40 episodes per cell. The evaluator safety loop was not a learner input and no fixed runtime probe count was used.

## Deployment integrity

The reconstructed live feature path exactly reproduced a held-out persisted trajectory:

- V32/V33 action-state maximum delta: **5.96e-08**
- V38 repeated mean/variance delta: **0.0**
- V40 horizon pair/hazard delta: **0.0**

Therefore the behavioral result is not caused by a serialization or feature-serving mismatch.

## Fresh-stream result

| Policy | No-unique UNKNOWN | Resolvable success | Wrong commitment | Mean trials | Costly UNKNOWN | Runaway |
|---|---:|---:|---:|---:|---:|---:|
| terminal only | 1.0000 | 0.0000 | 0.0007 | 0.0000 | 0.9950 | 0.0000 |
| V38 reusable | 0.9025 | 0.0300 | 0.0557 | 0.3143 | 0.9950 | 0.0000 |
| **V40 reusable** | **0.8850** | **0.0500** | 0.0621 | 0.3614 | **0.9950** | **0.0000** |

Relative to V38, V40:

- raises resolvable success by **+0.0200**;
- doubles unstable-then-stable success **0.0700 → 0.1350**;
- leaves reversal at **0.0050** and replacement near zero (**0.0050**);
- lowers no-unique UNKNOWN by **0.0175**;
- raises wrong commitment by **0.0064**;
- adds only **0.0471** trials and **0.0109** mean opportunity loss;
- causes no runaway evidence acquisition.

The primary R32 target is not met. The live controller usually stops before enough grounded consequences exist to reveal replacement or reversal.

## Causal classification

**Early multi-step option-credit / deployment-state distribution failure.** The explicit V40 horizon state remains useful: its offline action ranking improved and its live deployment produces a real but small gain. However, the global action-value model underprices early trials whose benefit arrives only after several initially non-distinguishing consequences. The retained terminal controller is appropriately conservative at those initial ambiguous states, so failure to propagate multi-step evidence value leaves resolvable cases UNKNOWN.

This is not:

- feature-serving corruption (exact replay passed);
- runaway probing;
- cost-too-high failure (0.995 costly UNKNOWN);
- generic recurrent undercapacity (V39 already converged and failed);
- justification for a fixed minimum probe count.

## Decision

- Retain V40 horizon-conditioned temporal state as an action-value feature.
- Reject the current global V40 action-value policy as a live R32 solution.
- Keep the terminal UNKNOWN controller unchanged.
- Next causal arm: train a **stage-conditioned action-value population** keyed only by learner-visible evidence count / remaining learned horizon. Hold trajectories, targets, shadow price, V40 state, zero-utility action boundary, and terminal policy fixed. Test whether early-stage specialists propagate delayed evidence value without increasing late/no-unique false acquisition.

R27 remains canonical. Native Zag reproduction remains mandatory before promotion.
