# R32 V26 — Candidate-Selected Conditional INSPECT Advantage

Status: **REFERENCE_ONLY / DISTRIBUTION REPAIR CONFIRMED / ABSOLUTE UTILITY GATE REJECTED**

V26 implemented the exact V25 follow-up. Development was restricted to high-uncertainty states where the reusable grounded consequence apparatus (source 7) was the sole optional evidence action. The learner received only persistent epistemic state, provenance/lineage repetition, action identity, and experienced cost. Generator regimes and delayed evaluator state were excluded from model inputs.

The candidate distribution changed materially: positive realized INSPECT advantage rose from V25's **1.7036%** to **5.4545%**. The sign classifier retained useful ranking (**ROC-AUC 0.8716**, AP 0.2241). Conditional magnitude models also predicted positive outcomes at a positive mean component of **0.4546**.

The runtime gate nevertheless fails. Learned expected advantage remains **-0.2569** even on truly beneficial actions, and only **1.5464%** of beneficial test actions cross zero. False-positive crossings are **0.3141%**. Restricting analysis further to actions that the inherited policy itself ranks above every terminal action raises positive prevalence to **7.0013%**, but their realized mean advantage is still **-0.3401** while inherited predicted advantage is +0.2027.

## Causal classification

**Developmental action-distribution mismatch was real but not sufficient.** V26 removes the V25 1.7% random-action scarcity, yet the conditional expected utility remains negative. This rejects the proposed global two-part calibration as a runtime repair under the current regret/cost scale.

The remaining failure is now narrowed to one of two causes:

1. **utility/evaluator scale mismatch** — ordinary consequence-probe costs may be too large relative to the +1 correct / 0 UNKNOWN / -2 wrong terminal regret scale, making multi-observation resolution economically negative even when the behavioral evaluator expects resolution; or
2. **future-dynamics state aliasing** — current epistemic features do not contain enough evidence to distinguish worlds where another trial will resolve from worlds where it will not.

## Decision

- Retain persistent temporal/provenance uncertainty and pairwise advantage ranking.
- Retain candidate-selected developmental data.
- Reject V26 expected-advantage sign as a runtime gate.
- Do not run a behavioral hardening pass with a model that almost never selects a truly beneficial observation.
- Next run is a matched utility-envelope audit: hold trajectories and representation fixed, vary only cost-to-regret normalization, and test whether any single scale preserves no-unique/costly abstention while making resolvable evidence acquisition rational. If no feasible envelope exists, the residual is representation/future-dynamics aliasing rather than cost calibration.

R27 remains canonical. Native Zag qualification remains blocked and no reference result can promote the TNN.
