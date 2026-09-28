# Amendment: Adoption of Design β for Sincere-Discourse Calibration

**Date:** 2026-09-27
**Amends:** `docs/lab/epistemics/utterance_types/exp2c/EXP_PREREG.md` (frozen; this is a separate adoption record, not an edit)
**Sign-off:** Micah, 2026-09-27

## Decision

Design β is ADOPTED for the sincere-discourse calibration delivery.

## Basis

exp2c results (committed):
- A+B (32 items): hypothetical LK 3/10 → 9/10 at zero additional bar failures.
- β+C (48 items): 10/10 LK with other bars passing.
- Prereg-compliant vol2 β (96 items): LK 10/10.

Design β is the configuration that achieved these results. The α design (abc-a) failed and is NOT adopted.

## Caveats (to be addressed in exp2d)

1. **C1:** cc40 is a near-template copy of si3_15. Must dedupe and scan all corpus/probe near-duplicates.
2. **C2:** D/E (`what if`, `where do`) mechanism engaged, but old probes contained zero matching lookalikes. Must extend probes.
3. **C3:** Three n-gram collisions lower DP (the clock → si3_03, is out → si5_01, at night → si4_05/si5_09). Must white-box and fix or bound.

## Scope

This adoption covers the sincere-calibration delivery only. It does not adopt:
- The two-heads split, content-only lock, or unscored-question rule (remain on hold).
- Any source changes (exp2d uses the v3 source plus the X2C probe block; no mechanism changes).

---

**Micah's sign-off (2026-09-27):** Design β adopted for sincere-calibration delivery, with the three caveats to be fixed in exp2d.
