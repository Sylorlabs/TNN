# R51 tool-sequencing and visual-representation correction — preregistration

Date: 2026-09-18  
Status: **FROZEN BEFORE FRESH EXECUTION**

R50 exposed two bounded failures while grounded language, hearing, phrase recognition, tracking, and cross-modal grounding passed. R51 changes only the failed tracks.

## Tool-policy correction

R50 withheld vocabulary as well as sentence structure, making the small locally trained bag-of-words policy a lexical zero-shot test rather than the intended learned tool-sequencing test. R51 trains generic intent vocabulary across many randomized demonstrations and withholds *compositions and sentence structures* for evaluation. Character n-grams plus word features are learned by a multiclass perceptron. No tool word is hardcoded to an action in inference.

Pass: held-out-composition accuracy >= 0.90 and at least +0.50 over update-disabled.

## Vision correction

R50's row/column centroid representation was not translation/noise robust. R51 replaces it with generic translation-invariant geometry: centered second moments plus a histogram of pairwise relative offsets. Training includes generic pixel dropout/noise; evaluation uses unseen placements and fresh corruption. Active reinspection is triggered only by learned-distance margin uncertainty.

Pass: clean >= 0.90, occluded >= 0.75, active >= occluded + 0.05, and second-view fraction < 0.80.

Randomized category labels are generated after source freeze and must be absent from source. `learn_authority=0`; canonical R27 unchanged.

