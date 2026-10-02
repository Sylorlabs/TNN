# PREREG AMENDMENT 2 (FROZEN)

**Date:** 2026-09-30 (PDT). **Status:** FROZEN. Committed after Amendment 1
(428c00e23), before any implementation. Transparent correction.

**Reason:** The base prereg (Step 3) says the (i) probe is synthesized from
"the first v in V containing w at p*". For Family B3, w="not" has p*=0
(training "not tak <color>"), but V (episodes 100..119) contains "not" only
at position 1 (ep 109..111 "tak not grn"). There is NO V episode with "not"
at p*=0, so the probe cannot be constructed from V as specified.

**Correction:** The (i) probe base is the first TRAINING episode (0..99)
containing w at p* (which exists by definition of p* as the most frequent
training position). The probe moves w to p', keeps the training episode's
target object fixed, recomputes T' via the world oracle, and checks the
tentative operator. All B3/P1 predictions stand: the position-0-trained
operator is probed at p'=1 and passes.

No prediction values change. K2 is evaluated against the amended prereg.
