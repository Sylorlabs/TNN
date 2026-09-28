# R39 online latent factor experts — closeout

Status: **FRESH NO-GO**

R39 replaced frozen factor snapshots with separate bounded online success/cost expert banks. Delayed learner-visible evidence is assigned by posterior responsibility. Wave 3 selected `balanced_blend30` only after it passed all seven unchanged development gates; the fresh family had already been frozen before development aggregation.

## Development-selected candidate

`balanced_blend30` = 70% online factor experts + 30% retained R36 posterior predictions.

Development metrics:
- mean regret: 0.0319215694425855
- post-change regret: 0.044084946304708716
- return regret: 0.02565649578137607
- worst return ratio vs V2: 1.2534520436526426
- cost-cycle return regret: 0.020373663209549645
- unseen-recombine return regret: 0.026316966571513924
- factor-noise mean regret: 0.024712584957839387
- success/cost experts bounded at 5/5

All seven development gates passed.

## Frozen fresh result

Retained R38:
- mean regret: 0.03505475434528525
- post-change regret: 0.047732418790527184
- return regret: 0.028225906041811636
- worst return ratio vs V2: 1.4158308756671685
- cost-recurrence return regret: 0.018837856834295872
- unseen-pairing return regret: 0.03413711907002969
- cross-noise mean regret: 0.02628415842861355

R39 selected:
- mean regret: 0.03317528157467057
- post-change regret: 0.04313968665321289
- return regret: 0.026671769473236087
- worst return ratio vs V2: 1.3214803117665617
- cost-recurrence return regret: 0.01819799496469518
- unseen-pairing return regret: 0.03242134668390954
- cross-noise mean regret: 0.026606910756503344
- success/cost experts bounded at 5/5

Fresh gates passed: bounded, cross-noise, mean return, overall, post-change, unseen pairing, worst return.

Fresh gate failed: cost recurrence. The frozen requirement was <= 0.90 * retained R38; R39 improved cost recurrence only about 3.4%, below the required 10% improvement.

## Research conclusion

Online factor experts are materially better than frozen-factor routing and substantially reduce the worst recurrence failures seen in R38, but a fixed blend between factor experts and the stable monolithic posterior is still too coarse. The next architecture should arbitrate factor-vs-stable predictions independently for success and cost using learner-visible predictive reliability, so the system can prefer the stable cost model during cost recurrence while retaining factor experts where they demonstrably predict better.

`learn_authority = 0`. Phase 6 remains closed. No fresh-specific retuning of R39 is permitted.
