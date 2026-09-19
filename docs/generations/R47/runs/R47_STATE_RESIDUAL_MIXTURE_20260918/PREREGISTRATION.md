# R47 state-conditioned residual mixture — preregistration

Date: 2026-09-18  
Status: **FROZEN BEFORE DEVELOPMENT RESULTS**

## Parent result

R46 rejected one continuously learned residual surface despite strong exercise. The retained R39 70/30 factor/stable predictor remains the immutable base. R47 tests the direct next hypothesis named by the R46 closeout: multiple locally valid residual corrections selected from learner-visible state, with explicit anti-interference and noise abstention.

## Learner-visible mechanism

Each strategy owns at most three residual experts. Experts are seeded only from distinct encountered online-state feature vectors. Routing uses centroid similarity, learned recent residual reliability, and a small generic under-use bonus. Delayed feedback updates the selected expert strongly and other active experts weakly. The final correction is attenuated toward zero when experts disagree, recent residual error is high, or the gate is diffuse.

No scenario label, latent context identifier, evaluator state, future outcome, oracle competence, or counterfactual result enters the model.

## Development family

The already-exposed paired R39 family remains the development family: seeds `36501, 36507, 36513, 36519`; scenarios `staggered_return`, `cost_recurrence`, `unseen_pairing`, `double_recombine`, `cross_noise`; 4,800 steps per life. Frozen V2/R36/R39 rows from R41 remain controls.

Candidates are `mix_cautious`, `mix_balanced`, and `mix_fast`; their numeric parameters are frozen in `r47_state_residual_mixture.py`.

## Development admission gates

A candidate must pass every gate against paired R39: cost-recurrence return regret `<=0.95×`; worst paired return ratio vs V2 better than R39; mean return no worse; overall mean regret `<=1.01×`; post-change no worse; unseen-pairing return `<=1.02×`; cross-noise mean `<=1.02×`; residual and R39 expert counts stay bounded; every row receives at least 100 delayed residual updates; mean absolute utility correction is at least `0.0015`; multi-expert routing occurs in at least 10% of decisions.

No fresh family may run unless a candidate passes all development gates. `learn_authority=0`; Phase 6 remains closed.
