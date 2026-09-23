# H3 sources

`vgate_h3.zag` — hardening fork H3 (auth + conflict adjudication),
PREREG_V2-IE_AMEND1.

Derived from the landed V2-A gate, as H2 (R1+R2 attested agreement), plus:
- the V2-A adjudication rule ("independent evidence revises on conflict") is
  replaced by R4: a conflicting challenger supersedes the permanent slot only
  with (a) historical corroboration — at least one PRIOR stream trial with the
  same task, same jcode, prog=PASS, |measure| within the task tolerance — AND
  (b) challenger margin `conf_challenger - conf_incumbent >= 100` (T3).
- the incumbent's install confidence is stored (`perm_c`) at promotion and at
  revision for the margin computation.

Generated deterministically by `hardening/tools/gen_h14.py`.
