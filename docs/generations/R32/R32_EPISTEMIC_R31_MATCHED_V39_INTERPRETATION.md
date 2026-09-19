# R32 V39 — Candidate-Specific Recurrent Temporal PAM

Status: **REFERENCE_ONLY / RECURRENT CAPACITY TEST REJECTED / HAZARD DECOMPOSITION NEXT**

V39 tested whether the remaining V38 positive-support gap was caused by summary-feature representation loss. A causal, unidirectional two-layer GRU received each candidate's retained ordered grounded evidence prefix plus the TNN-chosen physical action identity. A static learner-visible epistemic state branch was fused with the recurrent state. The PAM predicted repeated-continuation mean and variance from delayed outcomes. Generator mode, ambiguity labels, resource regime, future targets, final answer, and fixed probe counts were excluded.

The experiment used three episode-disjoint cross-fit folds plus one final model. Validation loss reached clear minima between epochs 14 and 23 before flattening or worsening, so the result is not classified as simple undertraining.

## Prediction

Compared with V38 ExtraTrees summaries:

- overall repeated-mean MAE: **0.14746 → 0.14598**;
- overall R²: **0.44923 → 0.38378**;
- decision-positive MAE: **0.23289 → 0.23560**;
- decision-nonpositive MAE: **0.14079 → 0.13898**.

The slight average MAE gain comes from easier nonpositive states. The target that matters—future support for the current hypothesis on actually beneficial INSPECT states—does not improve. At horizon 5 it remains approximately **0.346**, effectively unchanged.

The recurrent variance head is also weaker than the V38 tree-based uncertainty model:

- variance MAE: **0.01814 → 0.01879**;
- variance R²: **0.36059 → 0.21972**.

## Action value

Relative to V38 predicted mean+variance:

### Recurrent mean

- beneficial crossing: **+0.03521**;
- false-positive crossing: **+0.03557**;
- selected realized advantage: **-0.03436**.

### Recurrent mean + variance

- beneficial crossing: **-0.00235**;
- false-positive crossing: **+0.09314**;
- selected realized advantage: **-0.07726**.

### Hybrid ExtraTrees + recurrent

- beneficial crossing: **+0.03052**;
- false-positive crossing: **+0.00935**;
- selected realized advantage: **-0.00788**.

The hybrid has the least damage, but it still does not beat V38's realized evidence value.

## Causal classification

**Generic recurrent model capacity is not the missing mechanism.** The ordered raw prefix was available, the recurrent route trained and converged, and a modest recall increase was possible, but it broadened the action region rather than identifying the positive option-value boundary. This rejects the idea that replacing summaries with an opaque recurrent embedding is sufficient.

Retain:

- V38 repeated-continuation mean and variance;
- predicted continuation variance as unresolved-mass evidence;
- raw ordered evidence and action provenance;
- persistent multiple hypotheses.

Reject:

- the V39 GRU as a preferred epistemic repair;
- additional generic recurrent depth/epochs without a new causal target;
- using the hybrid's small recall gain while realized value falls.

## Next causal mechanism

The hidden dynamics that remain difficult are duration-structured: persistence, change, stabilization, and return. The next arm should decompose future support into explicit learned horizon-conditioned hazards rather than force one regressor or recurrent vector to predict all trajectories jointly.

Train from delayed observed outcomes only:

- probability current hypothesis persists to each horizon;
- probability a change occurs before each horizon;
- probability evidence returns to the prior hypothesis;
- expected dominant mass and unresolved variance by horizon.

These are live non-graph temporal hypotheses, not generator labels. Their weights and hazards must be learned from developmental histories. Compare against V38 with the same action-value learner. If horizon-conditioned hazard state improves positive support, retain it; otherwise the remaining boundary is observational identifiability rather than model organization.

R27 remains canonical. Native Zag reproduction remains mandatory before promotion.
