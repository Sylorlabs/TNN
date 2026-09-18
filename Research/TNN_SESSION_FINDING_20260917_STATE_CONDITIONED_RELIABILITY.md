# TNN Session Finding — State-Conditioned Reliability

Date: 2026-09-17  
Status: **locally restored and metric-verified through R46**  
Authority boundary: `learn_authority = 0`; Phase 6 remains closed

## Verified finding

The recovered R36–R41 campaign supports the session's original narrowing:

- reusable self-context memory is useful for recurrence;
- online success/cost factor experts add useful structure;
- global channel-level scalar reliability is too coarse (R40);
- strategy-specific scalar reliability is still too coarse (R41).

R42 then tested the next hypothesis directly: condition factor-vs-stable reliability on learner-visible operating state and recent feature/error trajectory while preserving the R36 stable posterior and R39 factor experts.

R42 was also a development NO-GO. R46 then tested a richer interaction: a continuous factorized learner-visible state drove bounded additive success/cost residuals on top of the unchanged R39 predictor. R46 was also a development NO-GO. The stronger verified conclusion is now:

> The remaining problem is not solved by progressively finer scalar reliability memories or by one continuously learned additive residual surface. R46 could strongly improve specific recurrence behavior, but those gains interfered with broader post-change, recombination, and noise performance. The next hypothesis needs multiple locally valid predictive corrections with explicit interference control rather than one shared correction.

## Local recovery and provenance

The exact R36–R41 archives were restored to this Mac under `TNN/Research`. Every recovered `MANIFEST.sha256` passed before R42 execution.

R42 was frozen before its new candidate results were aggregated. Its source freeze, inherited R41 fresh freeze, inherited R41 paired-control rows, and inherited R40 historical-control rows all verified before execution. The R41 fresh family remained unopened because no R42 candidate passed development.

The R42 Mac runtime used CPython 3.13.12 and NumPy 2.3.5. A recovered R39 control replay matched all non-floating fields exactly; the only differences were floating roundoff below `4e-15`.

## Evidence chain

### R39 — online factor experts

R39 retained a fixed 70% online-factor / 30% stable-memory blend after the factor experts materially improved recurrence behavior. Its fresh challenge still exposed a cost-recurrence weakness, motivating learned reliability arbitration rather than another fixed blend.

### R40 — channel-specific reliability

R40 completed all 120 preregistered development jobs with zero harness errors and selected no candidate. The retained R39 control had mean regret `0.0345137075`, return regret `0.0255295429`, and cost-recurrence return regret `0.0185357451`. The learned success/cost weights stayed close to 0.5, and no candidate cleared all eight gates. R40 fresh remained unopened.

### R41 — strategy-specific reliability

R41 completed all 120 preregistered development jobs with zero harness errors and selected no candidate. `strat_slow` improved cost recurrence to `0.0187826233` but failed post-change and unseen-pairing gates. Strategy-specific factor/stable weights still averaged near 0.5. R41 fresh remained unopened.

### R42 — state-conditioned scalar blend correction

R42 reused the immutable paired R41 V2/R36/R39 rows and ran 60 new state-conditioned candidate jobs across four seeds and five worlds. All 60 completed.

The retained paired R39 baseline was:

- mean regret: `0.03487726965606639`
- post-change regret: `0.045077940544996836`
- return regret: `0.028278379573013348`
- cost-recurrence return regret: `0.02411182269582512`
- unseen-pairing return regret: `0.028115905475791743`
- cross-noise mean regret: `0.02878717511583586`
- worst return-regret ratio vs V2: `1.4684404504268764`

No R42 candidate passed all eight frozen gates:

- `state_cautious`: failed cost recurrence, unseen pairing, and behavioral exercise.
- `state_balanced`: failed cost recurrence, mean return, unseen pairing, and behavioral exercise.
- `state_fast`: failed cost recurrence, worst-world return ratio, and behavioral exercise.

The state correction was updated at least 4,792 times per row, yet mean absolute factor-weight deviation from the fixed 0.70 baseline was only `0.0012–0.0028`, below the preregistered `0.01` floor. Faster adaptation did not rescue the cost-recurrence gate and worsened the worst-world return ratio.

`selected_for_fresh = null`. R41 fresh remains sealed.

### R46 — factorized predictive latent residual

R46 kept the R39 70% factor / 30% stable-memory predictor unchanged and added bounded additive success/cost residuals driven by continuous learner-visible state. The complete eight-file development source boundary and four-file fresh boundary were hash-frozen before any R46 result. Sixty inherited R41 controls and sixty R42 historical controls also verified before execution.

All 60 preregistered R46 development jobs completed. No candidate passed all eight gates:

- `latent_cautious`: mean regret `0.0367401734`, return regret `0.0311393303`, cost-recurrence return `0.0232100684`; passed worst-return, cross-noise, and bounded/exercised gates.
- `latent_balanced`: mean regret `0.0381966086`, return regret `0.0302399408`, cost-recurrence return `0.0203951096`; passed cost-recurrence, worst-return, and bounded/exercised gates.
- `latent_fast`: mean regret `0.0393752777`, return regret `0.0300382687`, cost-recurrence return `0.0247283041`; passed worst-return and bounded/exercised gates.

The mechanism was strongly exercised: aggregate mean absolute utility correction ranged from about `0.041` to `0.072`, with at least 4,792 delayed residual updates per row. `latent_balanced` materially improved cost recurrence and the worst paired return ratio, but simultaneously worsened overall regret, post-change regret, unseen pairing, and cross-noise. This local-gain/global-interference pattern is the central R46 result.

`selected_for_fresh = null`. The frozen R46 fresh family remained completely unopened.

## Architectural consequence

The evidence now argues against both a single scalar routing correction and a single shared additive residual. The next mechanism should preserve R39 memory/factor predictors but allow multiple bounded corrections to coexist and be selected from learner-visible state, with explicit protection against cross-state interference and noisy feedback. The most direct next test is a state-conditioned mixture of residual experts or expert-selection layer with:

- fixed bounded expert capacity;
- delayed causal credit using action-time cached state;
- a noise-abstention / update-suppression control;
- R39, R42, and R46 retained as frozen baselines;
- a fresh family preregistered and sealed before development.

This is a narrower hypothesis than simply increasing model capacity: the experiment must test whether separating locally valid corrections fixes the interference pattern exposed by R46.

## Authority boundary

`learn_authority = 0`. Phase 6 remains closed. No R42 fresh challenge was exposed and no native promotion claim is made.
