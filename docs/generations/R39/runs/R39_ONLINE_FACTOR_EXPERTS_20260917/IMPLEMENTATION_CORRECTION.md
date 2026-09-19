# R39 pre-tournament implementation correction

The first single development probe revealed that factor creation could never occur from the initial one-expert state because posterior max is identically 1.0 with one expert, while the spawn rule required posterior max < 0.78.

This contradicted the preregistered architecture, which explicitly requires persistent learner-visible predictive surprise to be able to create a new factor.

Before any tournament aggregation, the spawn rule was corrected so the first new expert may be created from persistent surprise when only one expert exists; later factor creation still requires posterior ambiguity. The partial pre-correction probe is preserved under `invalid_pre_freeze_probe/` and is not scored.

## Pre-tournament scale calibration

After fixing first-factor creation, diagnostic-only probes showed success and cost surprise live on materially different scales. Using one shared threshold would make success factors spawn while cost factors almost never could (except during synthetic noise). Because R39 is explicitly a factorized architecture, success and cost factor-creation thresholds were separated before the scored tournament.

The scored source uses:
- strict: success 1.00 / cost 0.25
- balanced: success 0.75 / cost 0.18
- fast: success 0.55 / cost 0.12

The surprise baseline in the leaky evidence accumulator is 0.12. These settings were frozen before tournament aggregation. Diagnostic probes remain under `invalid_pre_freeze_probe/` and are excluded from scoring.
