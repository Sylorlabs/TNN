# PREREG_AMENDMENT1 (pre-verdict, transparent)

Date: 2026-10-03. Corrects a derivation error in
PREREG.md section 5a/5b. No counting-rule change, no
learner-code change (the learner is frozen and reused
byte-identical), no world-fact change.

## The error

PREREG section 5a (build A) and 5b (build B) predict
adapted-Z MAP ids 4,5,6 (build A) and 4,5 (build B).
Both builds teach exactly THREE MAPs (mD' id 0,
mA' id 1, mB' id 2; no pattern MAP), so `map_create`
assigns the first adapted Z id 3, not 4. The id-4 base
was carried over from the builder's world (which
teaches four MAPs). The MAP lists in PREREG section
4a/4b (three MAPs) are authoritative and match the
implemented world files; the Z-id derivation was
wrong.

## Corrections

- Build A: Z1 id 4 -> 3, Z2 id 5 -> 4, Z3 id 6 -> 5.
  All Z row CONTENTS (live, rl, start, end, dom, cap,
  de, dr1, dr2, dnf, dvr, dir, rels, facts) are
  unchanged. K4' via expectations become 3,4,5;
  K8' t16 edges become (3,1,16),(3,2,16),
  (4,1,16),(5,1,16) with LINK14 to 3,4,5;
  t16 count stays 4.
- Build B: Z4a id 4 -> 3, Z4b id 5 -> 4. Row
  contents unchanged. K4' via expectations become
  3,4; K8' edges become (3,1,16),(4,1,16) with
  LINK14 to 3,4; t16 count stays 2.
- Builds C, X1-X4 are unaffected (C teaches four
  MAPs; X builds predict no adapted Z).
- Ablation-arm t16 COUNTS in section 5 are
  unchanged (they never referenced Z ids).

## Evidence

Build A run 1 (pre-amendment driver with the wrong
ids): 3/3 byte-identical; K1'=K2'=K3'=K5'=1; the only
falsifiers fired were the id-dependent ones
(F-NO-GROUND-Q1/2/3, F-WRONG-Z1/2/3,
F-NO-T16-42, F-NO-T16-61, F-NO-LINK14-6,
F-RE-Q1/2/3-VIA), and the MR-ZBUILD/ANS trace shows
the predicted rels, facts, answers, ops, and tries
at ids 3,4,5. The mechanism behaved exactly as
designed; only the prereg's id derivation was off
by one.
