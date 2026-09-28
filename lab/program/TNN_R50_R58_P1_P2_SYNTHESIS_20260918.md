# R50–R58 P1/P2 bounded branch synthesis — 2026-09-18

This record preserves the fresh outcomes of the bounded language/tool/perception branch. Failed visual candidates remain negative evidence; none is relabeled as a pass.

## Successful bounded evidence

- R50 grounded compositional language: 100% fresh synthetic composition, 0% update-disabled. Evidence boundary: C4 synthetic grounding, not broad natural language.
- R50 acoustic motifs and held-out phrase compositions: 100% / 100%. Evidence boundary: C4 synthetic hearing, not natural connected speech.
- R50 cross-modal grounding: 100% on four randomized correspondences. Evidence boundary: bounded C4 synthetic.
- R50 object persistence interpolation: passed the frozen tracking gate.
- R51 learned tool-plan selection: 94.5% held-out instruction compositions vs 20% update-disabled. Evidence boundary: C4 bounded tool-sequence policy; tool arguments/execution are not a full coding agent.

## Visual lineage

- **R50_P1_P2_BOUNDED_MULTIMODAL_TOOLS_20260918** — PARTIAL: clean_accuracy=0.7708, occluded_accuracy=0.4542, active_accuracy=0.8375, second_view_fraction=0.8208
- **R51_P1_P2_TOOL_VISION_CORRECTION_20260918** — NO_GO: clean_accuracy=0.4281, occluded_accuracy=0.3750, active_accuracy=0.4875, second_view_fraction=0.6000
- **R52_LOCAL_VISUAL_GEOMETRY_20260918** — NO_GO: clean_accuracy=0.9025, occluded_accuracy=0.6325, active_accuracy=0.8900, second_view_fraction=0.6100
- **R53_OCCLUSION_MARGINAL_VISUAL_20260918** — NO_GO: clean_accuracy=0.8167, occluded_accuracy=0.6229, active_accuracy=0.8292, second_view_fraction=0.5042
- **R54_LEARNED_LOCAL_TEMPLATE_VISUAL_20260918** — NO_GO: clean_accuracy=0.8233, occluded_accuracy=0.5500, active_accuracy=0.8700, second_view_fraction=0.4333
- **R55_DENSE_LEARNED_VISUAL_20260918** — NO_GO: clean_accuracy=0.9444, occluded_accuracy=0.6733, noise_heavy_accuracy=0.5333, active_accuracy=0.8743, second_view_fraction=0.5386
- **R56_CONVOLUTIONAL_VISUAL_20260918** — NO_GO: clean_accuracy=0.9783, occluded_accuracy=0.8122, noise_heavy_accuracy=0.6689, active_accuracy=0.9629, second_view_fraction=0.5257
- **R57_SCANNED_LEARNED_TEMPLATE_VISUAL_20260918** — NO_GO: clean_accuracy=0.9433, occluded_accuracy=0.7994, noise_heavy_accuracy=0.5678, active_accuracy=0.8579, second_view_fraction=0.3979
- **R58_SUPPORT_CHANNEL_CONV_VISUAL_20260918** — NO_GO: clean_accuracy=0.9795, occluded_accuracy=0.8180, noise_heavy_accuracy=0.6645, active_accuracy=0.9607, second_view_fraction=0.5093

R55–R58 establish that learned dense/convolutional representations solve the clean translation panel and active reinspection strongly, but the frozen single-view corruption floors remain unmet. The best clean result is above 97%; active reinspection is above 96%; single-view occlusion remains around 82% and heavy sparse noise around 66–67% in the best learned branches.

## Claim boundary

- Natural video perception: **NOT EARNED**.
- Natural connected speech: **NOT EARNED**.
- Broad natural language: **NOT EARNED**.
- Bounded grounded language/tool/hearing/cross-modal synthetic evidence is retained at its stated C3/C4 scope.
- No visual failure was converted into a pass by changing a previously exposed threshold. Each correction used a new preregistered identity.
