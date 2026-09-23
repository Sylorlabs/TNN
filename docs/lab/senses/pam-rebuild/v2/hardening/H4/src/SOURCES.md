# H4 sources

`vgate_h4.zag` — hardening fork H4 (corroboration-only revision),
PREREG_V2-IE_AMEND1.

Derived from the landed V2-A gate:
- the V2-A adjudication rule is replaced by R4(a) alone: a conflicting
  challenger supersedes the permanent slot only with historical corroboration
  (prior PASS same-class trial within tolerance). No channel authentication,
  no challenger margin — isolates the corroboration mechanism.
- the sidecar is read but not consulted (uniform CLI).

Generated deterministically by `hardening/tools/gen_h14.py`.
