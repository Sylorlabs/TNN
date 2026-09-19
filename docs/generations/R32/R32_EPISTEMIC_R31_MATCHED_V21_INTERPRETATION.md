# R32 V21 — Beneficial-WAIT Objective

Status: **REFERENCE_ONLY / TRAINING TARGET VALIDATED / RUNTIME SCALE MISMATCH**

V21 holds V20 architecture and epistemic state fixed and changes only the WAIT learning target from raw continuous return to delayed beneficial-wait classification. Validation improves materially: ROC-AUC **0.7942** versus V20 **0.6229**. Expected utility is also directionally separated on held-out rows (actual-beneficial mean **+0.0419**, non-beneficial **-0.2426**).

On the unchanged forced reusable-probe hardening battery, however, no-unique UNKNOWN is **0.620** (V20 **0.620**) and resolvable success is **0.6425** (V20 **0.6625**). Wrong commitment is **0.1300** and mean trials **7.701**. The new WAIT option is selected for only **0.0071** trials/episode on average, while the inherited direct INSPECT value selects **7.694**.

## Causal classification

**Action-value scale / option-comparison failure.** The training objective is substantially more predictive, but its expected-utility output lives on a narrower scale (conditional positive return mean 0.411, nonpositive -0.696) than the recursively trained source-specific INSPECT Q values. Therefore the WAIT signal usually cannot influence action selection even when it predicts future benefit. This is not evidence for replacing persistent hypotheses, temporal change-point state, or the WAIT concept.

## Next

Keep the V21 classifier and V20 architecture. Train/derive **WAIT advantage relative to the best currently available action** from delayed realized outcomes, or calibrate all competing option values onto a common held-out utility scale. Do not add a confidence threshold or fixed probe count.

R27 remains canonical; native Zag qualification remains mandatory.
