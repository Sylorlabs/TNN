# R47 state-conditioned residual mixture — closeout

Date: 2026-09-18  
Status: **DEVELOPMENT NO-GO / FRESH UNOPENED**

R47 tested the direct next hypothesis from the R46 closeout: preserve the retained R39 70/30 factor/stable predictor and let learner-visible state route among multiple bounded local residual experts, with weak cross-expert updates and abstention toward R39 under uncertainty/noise.

## Provenance and execution

- `PREREGISTRATION.md`, `FRESH_CONTRACT.md`, and the R47 development/fresh source boundary were hashed before development execution.
- Development used the already-exposed R39 paired family: 4 seeds × 5 scenarios × 3 candidates = 60 new jobs.
- All 60 jobs completed successfully under CPython 3.13.12 + NumPy 2.3.5.
- Frozen V2/R36/R39 rows from R41 remained immutable controls.
- `selected_for_fresh = null`; the frozen R47 fresh family was not executed.
- `learn_authority = 0`; Phase 6 remains closed.

## Retained R39 control

- mean regret: `0.03487726965606639`
- post-change regret: `0.045077940544996836`
- return regret: `0.028278379573013348`
- cost-recurrence return regret: `0.02411182269582512`
- unseen-pairing return regret: `0.028115905475791743`
- cross-noise mean regret: `0.02878717511583586`
- worst paired return-regret ratio vs V2: `1.4684404504268764`

## Candidate results

| candidate | mean regret | post-change | return | cost recurrence | unseen pairing | cross noise | worst / V2 | utility correction | result |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `mix_cautious` | 0.034439662 | 0.045105049 | 0.026752194 | 0.020877614 | 0.030035401 | 0.029496652 | 1.118438 | 0.016636714 | NO-GO |
| `mix_balanced` | 0.034049083 | 0.044531887 | 0.025682205 | 0.019378662 | 0.027909503 | 0.029399209 | 1.092808 | 0.027383000 | NO-GO |
| `mix_fast` | 0.034623112 | 0.045169044 | 0.024789115 | 0.019503581 | 0.030885247 | 0.028959213 | 1.198064 | 0.038399301 | NO-GO |

All candidates stayed within the frozen 5 success / 5 cost / 3 residual-expert caps. Every row received at least 4,793 delayed residual updates, and multi-expert routing occurred in >99.8% of decisions.

## Gate outcomes

- `mix_cautious` failed post-change, unseen-pairing, and cross-noise gates.
- `mix_balanced` passed every gate except cross-noise.
- `mix_fast` failed post-change and unseen-pairing while passing cross-noise.

No candidate passed all frozen development gates, so fresh remains unopened.

## Research conclusion

R47 shows that local residual specialization materially improves the R46 tradeoff, especially recurrence, return, and worst-case paired behavior. The failure pattern is now narrower: `mix_balanced` satisfies seven of eight gates and misses only cross-noise by a small margin, while `mix_fast` satisfies the noise gate but over-adapts after changes and on unseen pairings.

The next bounded discriminator should preserve local specialization but make noise abstention itself learned from delayed reliability rather than a fixed scalar penalty. That change is justified by the split R47 result: the balanced model has the desired transfer profile but insufficient noise suppression; the fast model suppresses the aggregate noise metric but sacrifices post-change/unseen-pairing stability.

This result does not authorize fresh exposure, architecture promotion, canonical mutation, or Phase-6 learning authority.
