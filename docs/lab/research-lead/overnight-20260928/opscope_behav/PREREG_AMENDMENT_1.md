# PREREG AMENDMENT 1 (FROZEN)

**Date:** 2026-09-30 (PDT). **Status:** FROZEN. Committed after the base prereg
(82e0e94fd), before any implementation. Transparent correction; no code exists.

**Reason:** The base prereg misdescribed the test episodes for Families B2/B3.
`gen_episodes_fam` overwrites only training blocks (24..35, 88..91) and appends
attack probes (120+); the frozen test set (episodes 100..119) is IDENTICAL
across all families (from the original `gen_episodes`). The validation set V
is episodes 100..119 only; the attack probe episodes (120+) are NOT used.

**Corrections:**

1. **B3/P2:** T1 is ep 109..111 = "tak not grn" (not "not tak grn" as the base
   prereg parenthetical said). Prediction unchanged: 3/3. Rationale: the
   position-0-trained "not" operator installs with posmask=0 (unrestricted,
   via strict (i)); on test "tak not grn" ("not" at position 1) it fires and
   predicts or_default(tak)|op_k(grn) = {tak}|{tak} = {tak} = T. The
   PROBE_D1/PROBE_D2 lines (referring to attack probe episodes 120+) are
   STRUCK; the (i) cross-position probe is synthesized by the harness, not
   drawn from ep 120+.

2. **B2/P4:** The PROBE_CONF_NEG / PROBE_HARM_DIRECT lines (referring to
   gate-stress probe episodes 120+) are STRUCK. The confound's behavioral
   harm is measured on the frozen V set: ep 100..102 ("tak grn cub", DIRECT
   novel) and ep 106..108 ("tak grn sph", SYN novel). Prediction: with the
   grn-operator tentatively installed, these score 0/3 each (as in
   GATE-STRESS-FAIL); with it rejected, 3/3 each. The (ii) acc_with=5/20 vs
   acc_base=20/20 comparison is on V=100..119.

3. **B1/P4:** Unchanged (T1 ep 109..111 = "tak not grn", 3/3). Confirmed.

No frozen prediction VALUE changes; only the episode references are corrected.
K2 is evaluated against this amended prereg.
