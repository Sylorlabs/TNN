# R42 state-conditioned reliability — closeout

Status: **DEVELOPMENT NO-GO / FRESH UNOPENED**

R42 tested the hypothesis left by R40 and R41: whether learner-visible operating state and recent feature/error trajectory can improve arbitration between the retained R36 stable posterior and R39 online factor experts. The retained R39 predictor remains a 70% factor / 30% stable blend; R42 only adds a bounded state-conditioned correction to that factor weight.

## Provenance and execution

- The recovered R36, R37, R38, R39, R40, and R41 archives were restored locally and every archive `MANIFEST.sha256` passed before R42 execution.
- R42 freeze revision 2 was verified before execution. Its five frozen source files match `SOURCE_FREEZE_DEV.sha256`.
- The inherited R41 fresh family remained hash-bound by `INHERITED_FRESH_FREEZE.sha256` and was not opened.
- The immutable R41 paired-control rows and R40 historical-control rows match their inherited SHA-256 ledgers.
- Development used the preregistered 60 new candidate jobs: 3 state-conditioned candidates × 4 seeds × 5 scenarios. All 60 jobs completed successfully.
- Runtime: CPython 3.13.12 on macOS arm64 with NumPy 2.3.5. A recovered R39 control row replay matched all non-floating fields exactly; floating differences were limited to platform-level roundoff below `4e-15`.

`learn_authority = 0`. Phase 6 remains closed.

## Paired retained R39 control

- mean regret: `0.03487726965606639`
- post-change regret: `0.045077940544996836`
- return regret: `0.028278379573013348`
- cost-recurrence return regret: `0.02411182269582512`
- unseen-pairing return regret: `0.028115905475791743`
- cross-noise mean regret: `0.02878717511583586`
- worst return-regret ratio vs paired V2: `1.4684404504268764`

The frozen cost-recurrence gate required `<= 0.022906231561033864` (5% better than R39). The behavioral-exercise gate required mean absolute factor-weight deviation from 0.70 of at least `0.01`.

## Candidate results

| candidate | mean regret | post-change | return regret | cost recurrence | unseen pairing | cross noise | worst / V2 | mean weight deviation | result |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `state_cautious` | 0.034763108 | 0.044786736 | 0.028200407 | 0.023782731 | 0.028887212 | 0.028685577 | 1.454656 | 0.001165 | NO-GO |
| `state_balanced` | 0.035215649 | 0.045133389 | 0.028975806 | 0.025425792 | 0.030009339 | 0.028549116 | 1.416795 | 0.001948 | NO-GO |
| `state_fast` | 0.034493751 | 0.044428093 | 0.027881243 | 0.023636368 | 0.028394255 | 0.028351908 | 1.520558 | 0.002750 | NO-GO |

All candidates remained within five success and five cost experts and received at least 4,792 delayed arbitration updates per row.

### Frozen gate outcomes

- `state_cautious` passed worst-return, mean-return, overall, post-change, and cross-noise gates. It failed cost-recurrence, unseen-pairing, and behavioral-exercise gates.
- `state_balanced` passed worst-return, overall, post-change, and cross-noise gates. It failed cost-recurrence, mean-return, unseen-pairing, and behavioral-exercise gates.
- `state_fast` passed mean-return, overall, post-change, unseen-pairing, and cross-noise gates. It failed cost-recurrence, worst-return, and behavioral-exercise gates.

No candidate cleared all eight development gates. `selected_for_fresh = null`; the inherited R41 fresh family remains unopened.

## Research conclusion

R40 ruled out global channel-level scalar reliability, R41 ruled out strategy-specific scalar reliability, and R42 now rules out this bounded state-conditioned **scalar blend correction** as an adequate solution under the frozen development battery.

The R42 state signal updated thousands of times but changed the retained 70/30 blend only slightly: mean absolute weight deviation was about 0.0012–0.0028, below the preregistered 0.01 behavioral floor. Increasing adaptation speed improved some average metrics but produced a worse worst-world return ratio and still did not clear the cost-recurrence gate.

This does not establish that learner-visible state is useless. It shows that using state only to perturb one factor-vs-stable mixture coefficient is still too restrictive. The next defensible architecture should preserve the retained memory/factor predictors and let learner-visible state affect prediction at a richer level, such as a bounded state-conditioned residual or expert-selection correction, with scalar blend routing retained as a baseline.

