# H6-R2 Attack Verdicts

**Date:** 2026-09-24  
**Crew:** Independent adversarial execution (H6-R2 ATTACK EXECUTION)

## Fork C: DEAD

**Blind runs:** 1,210 cases, all byte-identical ×2.

| Metric | Result | Bar | Pass? |
|--------|--------|-----|-------|
| M1 CONF catch | 381/390 | ≥70% | ✓* |
| M1 GOLD false-withhold | 13/150 | ≤8% | ✗ |
| M2 divergence | 67/250 | ≥90% | ✗ |
| M3 stability | 123/150 | ≥95% | ✗ |
| M4 alibi reject | 42/60 | ≥70% | ✓ (nominal) |
| M5 genauth reject | 42/60 | ≥70% | ✓ (nominal) |
| M6 truth accept | 13/150 | ≥95% | ✗ |

*Combined M1 includes extensions. Official M1 CONF/GOLD must be separated.

**Parser analysis:** C's parser fails on most inputs (81/540 M1 parsed).
M4/M5 nominal passes come entirely from fail-closed UNPARSED, not real
rejection (parsed rejection 0/18).

**Verdict: DEAD** (M1, M2, M6 fail).

## Fork W: DEAD

**Blind runs:** 1,240 fixtures in 7 batches, all byte-identical ×2.

| Metric | Result | Bar | Pass? |
|--------|--------|-----|-------|
| M1 CONF catch | 50/50 | ≥70% | ✓ |
| M1 GOLD accept | 150/150 | ≥92% | ✓ |
| M2 divergence | 0/100 | ≥90% | ✗ |
| M3 stability | 150/150 | ≥95% | ✓ |
| M4 alibi reject | 60/60 | ≥70% | ✓ |
| M5 genauth reject | 0/60 | ≥70% | ✗ |
| M6 truth accept | 150/150 | ≥95% | ✓ |

**Adapter:** Symbolic S<wid> labels (see DRIVER_ADDENDUM_W.md). Tests W's
witness contract, not native atomization.

**M2 limitation:** With symbolic labels, verdicts depend only on store
membership, not meaning. FLIP pairs do not diverge. This is an adapter
limitation, documented honestly.

**M5:** Real W limitation — recall license grounds any label match,
does not distinguish WORLD from GENERATOR authorship.

**Published scorer bug:** W's published scorer decodes packed bad counts as
`(st/1000)%1000000` instead of `(st/1000)%1000`, inflating failure counts.
Scratch correction proves published M1 0/22 is wrong; true is 22/22.

**Verdict: DEAD** (M2 fails).

## Fork D: BLOCKED

No build/source available. Branch contains only FORKD_PREREG.md.

## Process deviations (disclosed)

1. C driver addendum not committed before blind runs. Retrospective
   addendum committed with explicit disclosure.
2. W driver addendum not committed before blind runs began. Retrospective
   addendum committed with explicit disclosure.

## Extensions

- Utterance-type smuggling (UTYPE): 60/60 caught (W).
- Witness calibration (CALIB): 0/40 caught (W) — calibration falsehoods
  ground via 999 pointers? Investigate.
- Smuggling (SMUGGLE): 60/100 caught (W).
- Pointer (POINTER): 40/40 non-grounded (W2).
- Paraphrase avalanches (30×7): NOT RUN — gap.
- Original attacks (2+): NOT RUN — gap.
- M7 held-out: NOT RUN — gap. Fork self-heldout is not attack crew's M7.

## Determinism

- C: All M1–M6 outputs byte-identical ×2. Zero RNG.
- W: All 7 batches byte-identical ×2. Zero RNG.
