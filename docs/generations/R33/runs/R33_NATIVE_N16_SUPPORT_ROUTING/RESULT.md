# R33-N16 support-routing stability/plasticity result

Status: **FULL PREREGISTERED SYNTHETIC N16 QUALIFICATION — INDEPENDENTLY CONFIRMED**.

R33-N16 is the strongest synthetic stability/plasticity mechanism result in this continuation. It does not load or emulate canonical R27 and therefore does not establish an R27-dominating successor, original-R27 behavioral continuity, canonical mutation, learner authority, or promotion.

## Mechanism selected

Native development selected arm19:

`additive_training_mean_projection_gate_75pct_dual512_preservation_tolerance1`

The arm uses a training-input mean-shift projection gate to localize specialist activation at the prospectively fixed 75% boundary, plus dual old-support preservation over 512 training-side support examples with tolerance1. Probe outcomes remain evaluator-only.

Native development selection was:

`N16_DEV_SELECTION,19,1`

## Execution accounting

- Development executed exactly once on namespace910000: 21 arms x10 fresh populations = **210** arm-population exposures.
- Validation executed exactly once on namespace1010000: fixed controls0/1/3/4/6/8/14/17 plus selected arm19 x16 fresh populations = **144** exposures.
- Confirmation executed exactly once on namespace1110000 with the same nine-arm matrix x16 fresh populations = **144** exposures.
- Total fresh N16 scientific exposure: **498** arm-population runs.
- No stage was rerun, retuned, substituted, threshold-relaxed, or reused after exposure.
- Selected BUILD_11 binary SHA256: `6135e70986c3402e368836ef24b253e30a2be190f21f8aaa723ab3cd2c45a7ee`.
- Development stdout SHA256: `b1a60003311bd7d337c3f89db7471440d5163e83c1bfd3f13290b50cde28548c`.
- Validation stdout SHA256: `86853328f4c63d0df8e4ec86632dd8c22b63064060da7d563e14de6670ab9e3d`.
- Confirmation stdout SHA256: `ba9a2e0035dab0216a8ab4f673b6c2bcdc3df3d9663d6a3147e245957e69b7ff`.
- Immutable post-run evidence manifest: `Research/R33_NATIVE_N16_POSTRUN_EVIDENCE.sha256`, 28/28 entries verified, SHA256 `4e628153112903cb9a06bb5b0fa6ab2de293a61645b505bae2d823b4533f294a`.

Observed stage resources remained below frozen bounds:

| Stage | Wall seconds | Maximum RSS bytes | Exit | Terminal marker |
| --- | ---: | ---: | ---: | --- |
| Development | 49.50 | 19,693,568 | 0 | `R33_N16_DEV_COMPLETE` |
| Validation | 15.61 | 7,585,792 | 0 | `R33_N16_VALIDATION_COMPLETE` |
| Confirmation | 14.04 | 7,749,632 | 0 | `R33_N16_CONFIRMATION_COMPLETE` |

## Development tournament

Native development summary fields are: arm, total pointwise old_lost, total new_gain, minimum population new_gain, maximum final-old deficit, maximum pointwise old_lost, old routing hits, new routing hits, eligible.

| Arm | Old lost | New gain | Min gain | Max deficit | Max loss | Old hits | New hits | Eligible |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 3546 | 3505 | 318 | 357 | 367 | 0 | 0 | 0 |
| 2 | 5 | 16 | -15 | 1 | 1 | 0 | 0 | 0 |
| 3 | 347 | 2817 | 259 | 41 | 43 | 788 | 3966 | 0 |
| 4 | 75 | 1509 | 44 | 12 | 12 | 788 | 3966 | 0 |
| 5 | 18 | 630 | 21 | 4 | 6 | 788 | 3966 | 0 |
| 6 | 8 | 477 | 8 | 3 | 3 | 788 | 3966 | 0 |
| 7 | 15 | 838 | 36 | 3 | 3 | 788 | 3966 | 1 |
| 8 | 394 | 2986 | 224 | 52 | 52 | 604 | 4233 | 0 |
| 9 | 126 | 575 | -6 | 33 | 33 | 604 | 4233 | 0 |
| 10 | 17 | 435 | -4 | 5 | 5 | 604 | 4233 | 0 |
| 11 | 5 | 365 | -4 | 1 | 2 | 604 | 4233 | 0 |
| 12 | 20 | 422 | 12 | 6 | 6 | 604 | 4233 | 0 |
| 13 | 302 | 2828 | 201 | 48 | 48 | 458 | 3964 | 0 |
| 14 | 315 | 2894 | 201 | 48 | 48 | 482 | 4057 | 0 |
| 15 | 115 | 1416 | 19 | 29 | 29 | 482 | 4057 | 0 |
| 16 | 399 | 3421 | 320 | 49 | 50 | 741 | 4655 | 0 |
| 17 | 150 | 2808 | 257 | 19 | 19 | 234 | 3837 | 0 |
| 18 | 52 | 2457 | 196 | 15 | 15 | 234 | 3837 | 0 |
| **19** | **4** | **2327** | **194** | **2** | **2** | **234** | **3837** | **1** |
| 20 | 84 | 2444 | 210 | 12 | 12 | 121 | 3375 | 0 |

Arm7 and arm19 were eligible; the frozen native selector chose arm19 because it had the smaller total old loss. Arm19 then remained fixed for all holdout stages.

## Fresh validation

Validation aggregate fields below are the native rows: total old_lost, old_rescued, total new_gain, minimum population new_gain, maximum final-old deficit, maximum pointwise old_lost, old/new routing hits, proposals, accepted, rejected, skipped, anchor_loss, populations.

| Arm | Old lost | Rescued | New gain | Min gain | Max deficit | Max loss | Old hits | New hits | Accepted | Rejected | Anchor loss |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 1 | 5678 | 209 | 5524 | 316 | 378 | 384 | 0 | 0 | 1550 | 0 | 0 |
| 3 | 537 | 19 | 4525 | 264 | 42 | 43 | 1226 | 6339 | 844 | 3852 | 0 |
| 4 | 119 | 13 | 2020 | 71 | 18 | 18 | 1226 | 6339 | 303 | 11328 | 0 |
| 6 | 23 | 16 | 987 | 25 | 3 | 4 | 1226 | 6339 | 158 | 14491 | 0 |
| 8 | 598 | 0 | 4814 | 235 | 56 | 56 | 889 | 6766 | 1055 | 2748 | 0 |
| 14 | 413 | 0 | 4657 | 224 | 44 | 44 | 661 | 6453 | 1008 | 3120 | 0 |
| 17 | 211 | 0 | 4551 | 262 | 21 | 21 | 366 | 6173 | 845 | 3786 | 0 |
| **19** | **12** | **3** | **3767** | **194** | **4** | **4** | **366** | **6173** | **550** | **6314** | **9** |

Native validation gate:

`N16_HOLDOUT_GATE,N16_VAL,19,1,1`

The selected summary is frozen exactly as:

`N16_HOLDOUT_ARM,N16_VAL,19,12,3,3767,194,4,4,366,6173,6864,550,6314,17712,9,16`

`VALIDATION_DECISION_FREEZE.json` SHA256 is `8a36c74be84f4bd1c8f44cbf053592018d854a5763c88486745bb6f55bf0476c`.

## Fresh confirmation

| Arm | Old lost | Rescued | New gain | Min gain | Max deficit | Max loss | Old hits | New hits | Accepted | Rejected | Anchor loss |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 1 | 5666 | 116 | 5479 | 319 | 369 | 371 | 0 | 0 | 1540 | 0 | 0 |
| 3 | 577 | 10 | 4421 | 252 | 52 | 59 | 1226 | 6357 | 806 | 4008 | 0 |
| 4 | 157 | 10 | 1964 | 6 | 17 | 17 | 1226 | 6357 | 304 | 11472 | 0 |
| 6 | 14 | 8 | 685 | 11 | 9 | 9 | 1226 | 6357 | 133 | 15272 | 0 |
| 8 | 627 | 1 | 4830 | 278 | 49 | 49 | 915 | 6877 | 949 | 2658 | 0 |
| 14 | 472 | 1 | 4748 | 272 | 49 | 49 | 714 | 6661 | 915 | 2808 | 0 |
| 17 | 209 | 0 | 4450 | 245 | 21 | 21 | 375 | 6197 | 803 | 3948 | 0 |
| **19** | **7** | **0** | **3603** | **179** | **2** | **2** | **375** | **6197** | **489** | **6584** | **3** |

Native confirmation gate:

`N16_HOLDOUT_GATE,N16_CONF,19,1,1`

The selected summary is frozen exactly as:

`N16_HOLDOUT_ARM,N16_CONF,19,7,0,3603,179,2,2,375,6197,7073,489,6584,17503,3,16`

`CONFIRMATION_DECISION_FREEZE.json` SHA256 is `fb7af94b916031e496099d5fc2f8e02bfa69a60ca5e80332a434d0a20abe87eb`.

## Scientific interpretation

The synthetic mechanism result is qualitatively different from N15. N15 found a promising preservation/additive frontier but failed its frozen development and validation gates because unseen old behavior still degraded substantially even while protected anchors remained intact. N16 broadened support and tightened routing. Arm19 then passed native development, untouched validation, and untouched confirmation gates without threshold relaxation.

The key repeated pattern is that the 75%-projection route without preservation (arm17) retains strong new learning but still loses substantial old behavior, whereas arm19 retains useful new learning while reducing old loss to 12 in validation and 7 in confirmation. The N15-like arm4 similarly preserves more than unconstrained routing but has materially weaker holdout preservation than arm19. These comparisons are already encoded in the preregistered native holdout gate; the native gate lines, not an external re-scoring, are the scientific authority.

This supports the bounded conclusion that broader training-side old-support preservation plus a localized specialist routing boundary can materially improve the synthetic stability/plasticity frontier and that the effect replicated across two disjoint holdout namespaces.

## Why this still does not “beat R27”

N16 answers a mechanism question, not the unresolved canonical-continuity question. The N16 parent and populations are synthetic. The campaign never loaded the accepted R27 runtime state, never recomputed the original semantic digest, and never ran the original 33-check verifier against a mutated R27-continuous descendant. The original R27 source/digest/verifier/runtime closure is still unresolved.

Therefore the correct statement is: **N16 has full native gate1 evidence for its preregistered synthetic campaign, but it has not been placed into an admissible R27-continuous head-to-head promotion test.** This is a major reason a promising mechanism can exist without yet “beating R27” canonically.

## Governance and next boundary

All N16 scientific namespaces are consumed. N16 must never be rerun, retuned, or relabeled as new evidence. Any follow-on mechanism experiment requires a new identity and fresh populations.

Independent post-run review returned terminal disposition `CONFIRM_FULL_PREREGISTERED_SYNTHETIC_N16_QUALIFICATION` with no requested correction. The final review is preserved in `POSTRUN_INDEPENDENT_REVIEW.md`. Two earlier reviewer transports failed before returning a scientific disposition; those infrastructure failures remain preserved separately in `POSTRUN_REVIEW_TRANSPORT_HISTORY.md` and did not alter scientific receipts.

Canonical R27 remains step60,423 with zero newborn restarts. Canonical mutation=false. Learner authority=false. Promotion=false.
