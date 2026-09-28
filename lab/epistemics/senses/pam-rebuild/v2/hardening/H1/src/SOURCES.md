# H1 sources

`vgate_h1.zag` — hardening fork H1 (prog-requirement ablation), PREREG_V2-IE_AMEND1.

Derived from the landed V2-D gate
(`senses/pam-rebuild/v2/forks/V2-D/src/vgate_d.zag`) by a single-rule change:
the independent-evidence signal additionally requires `prog=PASS`
(`pr == 0`). All other V2-D logic (confidence separation, revision policy)
unchanged. The third CLI arg (gatt sidecar) is accepted and ignored.

Generated deterministically by `hardening/tools/gen_h14.py`.
