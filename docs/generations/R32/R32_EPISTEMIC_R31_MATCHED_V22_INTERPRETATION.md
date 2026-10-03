# R32 V22 — Common Utility Scale Ablation

Status: **REFERENCE_ONLY / REJECT GLOBAL INSPECT RESCALING**

The source-specific beneficial-INSPECT classifier validates strongly (ROC-AUC **0.8215**), but replacing the inherited INSPECT Q value with this globally calibrated expected utility makes the runtime over-conservative. No-unique UNKNOWN rises to **0.725** from V21 **0.620**, but resolvable success collapses to **0.1125** from **0.6425**. Stable-weak is 0.24, unstable-then-stable 0.16, replacement 0.03, reversal 0.02.

## Causal classification

The value-scale mismatch is real, but **global INSPECT replacement is the wrong repair**. It suppresses the already-useful source-specific evidence policy rather than correcting only states where its value is miscalibrated. This is a decision/action-value calibration failure, not evidence that persistent temporal hypotheses or active observation should be removed.

## Next

Retain the original V19 recursive INSPECT Q as baseline. Learn a **residual correction / advantage** from delayed realized inspect returns using current epistemic state, raw INSPECT Q, and V21 WAIT expected utility. This can down-correct overoptimistic INSPECT only where evidence supports it while preserving high-value resolvable inspections.
