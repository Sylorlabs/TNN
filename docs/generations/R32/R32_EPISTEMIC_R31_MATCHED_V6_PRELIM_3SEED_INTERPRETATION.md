# R32 V6 Preliminary Multi-Seed Read

Status: **REFERENCE_ONLY / HARD_FRONTIER_CONFIRMED / AMBIGUITY_GAIN_NOT_CONFIRMED**

Across seeds 9710-9712, D preserves the difficult resolvable frontier: core hard correctness **0.9874** versus A **0.9833**, and expanded resolvable correctness improves **0.9168 -> 0.9707**. Wrong commitment falls **0.1075 -> 0.0488**, and replacement correctness improves **0.5900 -> 0.9700**.

The primary R32 target is **not met yet**. Genuine-ambiguity UNKNOWN averages only **0.5575** versus A **0.5433**; the seed-9710 gain did not replicate on 9711/9712. This is insufficient improvement over the ~0.57 R31 boundary.

## Causal classification

The V6 residual action-value formulation is retained because hard correctness is stable across seeds. The remaining ambiguity failure is most consistent with **representation/evidence-instability loss**: D stores posterior history but its Q features largely summarize current/global/recent mass and cross-modal aggregate agreement. Contradictory repeated physical evidence can cancel in accumulated scores without exposing the within-modality temporal instability pattern strongly enough.

## Next mechanism

Keep V6 residual Q control. Add generic temporal-instability features from the persistent hypothesis trajectory (top-switch rate, posterior movement, entropy/margin variance and trend, global-vs-recent divergence) plus within-modality/source disagreement. No ambiguity label, condition ID, confidence threshold, or fixed probe count. Then rerun the matched seed panel.
