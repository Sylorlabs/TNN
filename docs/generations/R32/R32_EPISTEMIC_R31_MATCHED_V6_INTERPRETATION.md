# R32 Epistemic Qualification V6 — Development Result

Status: **REFERENCE_ONLY / PROMISING_RESIDUAL_Q / MULTI_SEED_REQUIRED**

On seed 9710, the residual action-value formulation restores the R31 hard frontier while improving several epistemic cases. A reaches core hard **0.9917**, expanded resolvable **0.9092**, and genuine ambiguity UNKNOWN **0.5500**. D reaches core hard **0.9937**, expanded resolvable **0.9733**, and genuine ambiguity UNKNOWN **0.6125**. Mean wrong commitment falls from **0.1243** to **0.0471**.

Entity-replacement correctness improves **0.3000 -> 0.9500**, delayed-distinguishing correctness improves 0.4500 -> 0.7000, and correlated-wrong correctness improves 0.9375 -> 0.9875. D does this by preserving `KEEP_R31` as one available action rather than making R31 absolute authority; `COMMIT_CURRENT`, `INSPECT(source)`, and `UNKNOWN` can win whenever their learned delayed-regret value is higher. There is no fixed confidence threshold or probe count in D.

## Causal classification

The V5 collapse was a **decision-policy formulation** failure, not an uncertainty-representation failure. Residual Q learning is retained provisionally because it recovers hard correctness and reduces wrong commitment without removing persistent hypotheses/provenance/temporal state.

## Remaining weakness

The cost-too-high condition is not yet good enough: D improves correctness there but rational abstention falls from 0.1500 to 0.0375 and mean evidence cost rises. Observation cost is already in the INSPECT target, so this is currently a learned value/curriculum calibration issue rather than a missing cost mechanism. Do not promote until multi-seed confirmation and a harder cost frontier test.

All results are REFERENCE_ONLY. Native Zag reproduction remains mandatory; R27 remains canonical.
