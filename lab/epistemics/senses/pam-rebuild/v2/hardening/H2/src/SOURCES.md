# H2 sources

`vgate_h2.zag` — hardening fork H2 (authentication ablation), PREREG_V2-IE_AMEND1.

Derived from the landed V2-A gate
(`senses/pam-rebuild/v2/forks/V2-A/src/vgate_a.zag`):
- reads the G-channel attestation sidecar (`<records> <gatt> <ledger>`);
- recomputes `hex(sha256("PAMV2-REG-CHANNEL-2026-09-23|seq|fixture|jG|confG"))`
  per record in pure Zag and requires equality with the sidecar entry;
- the independent-evidence signal becomes
  `prog=PASS && jG==jcode && conf>=700 && confG>=700 && attested`.
The V2-A conflict-adjudication path is otherwise unchanged.

Generated deterministically by `hardening/tools/gen_h14.py`.
