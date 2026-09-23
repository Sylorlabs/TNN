# H6 sources

`vgate_h6.zag` — hardening fork H6 (R1–R4, no provisional installs),
PREREG_V2-IE_AMEND1.

Derived from the generated H5 gate:
- provisional installs are removed. The first r3-satisfying observation of a
  judgment is WITHHELD as an unconfirmed candidate (`uc_*` per task); only a
  second r3-satisfying observation with the same jcode and |measure| within
  tolerance promotes it to PERMANENT_INSTALL (`corroborated-second`).
- a non-matching later observation replaces the candidate (latest wins).
- conflict-vs-permanent adjudication identical to H5 (R4 inline).

Generated deterministically by `hardening/tools/gen_h56.py` from H3.
