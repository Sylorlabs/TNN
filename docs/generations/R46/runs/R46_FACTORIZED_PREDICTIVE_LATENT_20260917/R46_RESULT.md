# R46 factorized predictive latent residual — closeout

Date: 2026-09-17  
Status: **DEVELOPMENT NO-GO / FRESH UNOPENED**

R46 tested the richer state interaction identified after R42. The retained R39 predictor stayed fixed at 70% online factor experts / 30% stable memory, while learner-visible operating state drove bounded additive success and cost residuals. This moved state from a scalar routing weight into prediction itself without exposing latent context IDs, scenario labels, evaluator state, future outcomes, or oracle competence.

## Provenance and execution

- `PREREGISTRATION.md` and the complete eight-file R46 source boundary were frozen before development results.
- The four-file fresh boundary was frozen separately before development results.
- All 60 inherited paired R41 V2/R36/R39 control rows verified against `INHERITED_R41_CONTROL_ROWS.sha256`.
- All 60 completed R42 state-conditioned scalar rows verified against `INHERITED_R42_CONTROL_ROWS.sha256` and were historical controls only.
- Development ran exactly 60 new jobs: 3 candidates × 4 seeds × 5 preregistered worlds.
- All 60 development jobs completed successfully.
- Runtime: CPython 3.13.12 with NumPy 2.3.5 on macOS arm64.
- `selected_for_fresh = null`; no fresh directory or fresh result was created.

`learn_authority = 0`. Phase 6 remains closed.

## Paired retained R39 control

- mean regret: `0.03487726965606639`
- post-change regret: `0.045077940544996836`
- return regret: `0.028278379573013348`
- cost-recurrence return regret: `0.02411182269582512`
- unseen-pairing return regret: `0.028115905475791743`
- cross-noise mean regret: `0.02878717511583586`
- worst return-regret ratio vs paired V2: `1.4684404504268764`

## Candidate results

| candidate | mean regret | post-change | return regret | cost recurrence | unseen pairing | cross noise | worst / V2 | mean abs utility correction | result |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `latent_cautious` | 0.036740173 | 0.048289368 | 0.031139330 | 0.023210068 | 0.032646208 | 0.029053851 | 1.287574 | 0.040621206 | NO-GO |
| `latent_balanced` | 0.038196609 | 0.049532071 | 0.030239941 | 0.020395110 | 0.034232042 | 0.031919356 | 1.268499 | 0.056695703 | NO-GO |
| `latent_fast` | 0.039375278 | 0.052048686 | 0.030038269 | 0.024728304 | 0.028771214 | 0.034105887 | 1.291451 | 0.072396218 | NO-GO |

Every candidate remained within five success and five cost experts, received at least 4,792 delayed residual updates in every row, and exceeded the preregistered behavioral-exercise floor of `0.003` mean absolute utility correction.

## Frozen gate outcomes

- `latent_cautious` passed worst-return, cross-noise, and bounded/exercised gates. It failed cost recurrence, mean return, overall, post-change, and unseen-pairing gates.
- `latent_balanced` passed cost-recurrence, worst-return, and bounded/exercised gates. It failed mean return, overall, post-change, unseen-pairing, and cross-noise gates.
- `latent_fast` passed worst-return and bounded/exercised gates. It failed cost recurrence, mean return, overall, post-change, unseen-pairing, and cross-noise gates.

No candidate cleared all eight gates. The frozen R46 fresh family therefore remained unopened.

## Research conclusion

R46 falsifies this specific factorized additive-residual hypothesis as a general solution under the frozen development battery.

The mechanism was strongly exercised, unlike R42: mean absolute utility corrections ranged from about `0.041` to `0.072`. It could produce large local gains. In particular, `latent_balanced` improved cost-recurrence return regret from `0.024111823` to `0.020395110` and improved the worst paired return ratio from `1.46844` to `1.26850`. Those gains did not generalize. The same mechanism increased overall regret, post-change regret, and unseen-pairing regret, with additional cross-noise degradation at the balanced and fast settings.

The accumulated evidence now rules out both of the obvious low-dimensional fixes:

1. progressively finer scalar arbitration (R40–R42), and
2. a single continuously learned additive residual driven by the same delayed learner-visible state (R46).

The next experiment should preserve R39 memory/factor predictors while adding a mechanism that can represent multiple locally valid predictive corrections without forcing one residual surface to serve incompatible recurrence, recombination, and noise states. A bounded state-conditioned expert-selection or mixture-of-residuals model is the most direct next hypothesis, with explicit anti-interference and noise-abstention controls.

## Authority boundary

`learn_authority = 0`. Phase 6 remains closed. No R46 fresh challenge was exposed and no native promotion claim is made.
