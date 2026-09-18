# R33-N15 preservation/additive stability-plasticity result

Status: **DEVELOPMENT GATE FAILED; EXPLORATORY VALIDATION COMPLETED; CONFIRMATION FORBIDDEN**.

R27 remains canonical at development step 60,423 with zero newborn restarts. N15 is synthetic native-Zag mechanism evidence only and is not promotion-eligible or a claim of original-R27 behavioral continuity.

## Execution accounting

- Development executed exactly once: 12 arms x 8 fresh populations = 96 arm-population exposures.
- Validation executed exactly once: fixed controls 0/1/4/8 plus frozen selected arm10 across 12 fresh populations = 60 arm-population exposures.
- Confirmation executed zero times because the frozen development gate was0.
- Total fresh N15 scientific arm-population exposures: 156.
- Development stdout SHA256: `15c7d41f2570ed649dc0ff7a5fff97aa8e7f0a58a3895ba0c6ab059546b0fe7a`.
- Validation stdout SHA256: `50708179e5aba619a219f1c30226e7d50734048062161482572cbe1c6c6b6085`.
- Selected BUILD_09 binary SHA256: `1f7b78d9f90153de1182887f813af70c884c6d59286e7c31e78fa62c936b4d3a`.
- Development runtime/RSS: 5.51 seconds / 5,799,936 bytes maximum RSS.
- Validation runtime/RSS: 3.12 seconds / 3,981,312 bytes maximum RSS.
- All observed resource use remained below frozen bounds.

## Development

Native development summaries have fields: arm, total pointwise old_lost, total new_gain, minimum population new_gain, maximum final-old deficit, eligible.

| Arm | Old lost | New gain | Min new gain | Max old deficit | Eligible |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 2905 | 2746 | 330 | 373 | 0 |
| 2 | 2805 | 2349 | 270 | 368 | 0 |
| 3 | 2912 | 2648 | 301 | 399 | 0 |
| 4 | 86 | 53 | -23 | 17 | 0 |
| 5 | 181 | 187 | -4 | 27 | 0 |
| 6 | 278 | 302 | 15 | 40 | 0 |
| 7 | 105 | 1139 | 134 | 15 | 0 |
| 8 | 293 | 2202 | 260 | 45 | 0 |
| 9 | 510 | 2436 | 270 | 87 | 0 |
| **10** | **49** | **1120** | **45** | **11** | **0** |
| 11 | 144 | 1779 | 187 | 30 | 0 |

Native selection: `N15_DEV_SELECTION,10,0`.

No arm met the preregistered development eligibility threshold. Arm10 was selected only by the frozen fallback rule: minimum total old loss among non-frozen arms with positive aggregate new gain. Its maximum final-old deficit was11, exceeding the required <=4, so development qualification failed. `DEV_SELECTION_FREEZE.json` SHA256 is `8fcf70430f46e3453766518fac8dade9a68dd540990d035ce7061093f21bb5a1`.

## Fresh exploratory validation

Validation used untouched namespace610000 and frozen invocation `validate 10 0`. Native aggregate fields are: arm, total old_lost, total old_rescued, total new_gain, minimum population new_gain, maximum final-old deficit, maximum pointwise old_lost, proposals, accepted, rejected, skipped, anchor_loss, populations.

| Arm | Old lost | Rescued | New gain | Min gain | Max deficit | Max loss | Accepted | Rejected | Anchor loss |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 frozen | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 1 shared rewrite | 4248 | 89 | 4031 | 283 | 380 | 390 | 1151 | 0 | 822 |
| 4 strict preservation | 182 | 78 | 72 | -19 | 24 | 28 | 42 | 12881 | 0 |
| 8 additive medium | 375 | 8 | 3312 | 262 | 33 | 35 | 630 | 3042 | 75 |
| **10 additive + preservation** | **131** | **3** | **1844** | **44** | **21** | **21** | **234** | **7458** | **0** |

Native validation gate: `N15_HOLDOUT_GATE,N15_VAL,10,0,0`.

The upstream development gate0 already forces validation qualification false. Independently, the native arm10 summary also violates three frozen validation thresholds: maximum final-old deficit21 >4, maximum pointwise old_lost21 >8, and total pointwise old_lost131 >48. `VALIDATION_DECISION_FREEZE.json` SHA256 is `b50519272285cdb70a5ce75a899665ad5d670611ab468cee72d4051f5f6ea0e6`.

## What changed scientifically

The failure is informative. Ordinary shared rewriting remains highly plastic but catastrophically disruptive. Strict preservation preserves much more but can suppress useful learning and even has a negative minimum-population new gain. Additive medium learns strongly but still loses substantial old behavior. Arm10 is the strongest observed stability/plasticity compromise in this campaign: on fresh validation it retains positive new gain in every population (`min_gain=44`), gains1844 aggregate new successes, and incurs131 pointwise old losses rather than arm8's375 or arm1's4248.

But arm10 still does not preserve old behavior tightly enough. The most diagnostic detail is that its training-anchor loss is **0** while unseen old probes still degrade. The preservation mechanism is therefore succeeding on the protected training anchors without generalizing that guarantee across the broader old-behavior distribution. Additive routing reduces interference, but the current input-prototype boundary plus fixed-anchor constraint does not define the old-behavior manifold tightly enough.

Within this synthetic N15 campaign, the observed results support a stability/plasticity tradeoff: shared rewriting caused substantial old-behavior loss, while stronger preservation constrained learning; arm10 showed a promising but still insufficient frontier. The next scientifically justified direction is not to weaken the gate or reuse these populations. It is to improve how old behavior is represented/protected or how specialist routing isolates updates, then test that as a new identity on new populations.

## Negative-result discipline

N15 development and validation are consumed. They must never be rerun, retuned, or relabeled as confirmation. Confirmation namespace710000 remains untouched and is forbidden for this identity. No threshold is relaxed after seeing the result, no arm is substituted, and no N15 population may become fresh evidence again.

Even the promising descriptive frontier shift does not establish an R27-dominating successor. Original R27 source/digest/verifier/runtime continuity remains unresolved, and N15 uses a synthetic parent. Canonical mutation, learner authority and promotion remain false.
