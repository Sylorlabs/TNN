# H5 sources

`vgate_h5.zag` — hardening fork H5 (R1–R4 composite), PREREG_V2-IE_AMEND1.

Derived from the generated H3 gate by replacing the whole decision block:
- R1: the independent-evidence signal requires `prog=PASS`.
- R2: G-channel attestation (as H2/H3).
- R3: EVERY install path (provisional, permanent, revision) requires
  `prog=PASS && pred=1 && conf>=700 && jG==jcode && confG>=700 && attested`;
  anything weaker is WITHHELD (`no-attested-agreement`) or SUPPRESSED.
- R4: revision of a permanent slot needs historical corroboration AND
  challenger margin >= 100 (as H3), decided inline; the old V2-A
  adjudication block is removed.
- FAIL/UNRESOLVED handling unchanged from V2-A.

Generated deterministically by `hardening/tools/gen_h56.py` from H3.
