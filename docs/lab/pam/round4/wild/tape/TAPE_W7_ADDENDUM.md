# TAPE ADDENDUM W7 — FROZEN LAUNDERING FIXTURE SET

**Date:** 2026-09-24. **Crew:** WILD-B. **Status:** FROZEN — committed after
PREREG_W7 (8fdb5df1), before the W7 build. Parent: `wild/tape/TAPE.md` §4.

## Fixture set (extends the shared attack tape; the admission tape is untouched)

| Item | Value |
|---|---|
| Signals file (instrument reads) | `wild/w7/launder_signals.txt` |
| sha256 | `9024f08ebfaea55b3ace6689ada04697e998b550d4367b65d30fb04c3310ce2b` |
| Truth file (scorer only) | `wild/w7/launder_truth.txt` |
| sha256 | `5adc617c3e667d928c925b5b0c4468ec6338cf1eb799ab29241b1dcdcf43a34a` |
| Generator | `wild/w7/gen_launder.py` (deterministic, zero RNG) |

200 entries: ids 0..99 LAUNDERED (true GEN, claimed EXT); ids 100..199
GENUINE (true EXT, claimed EXT). Signals per PREREG_W7 §2:
`id|sig_c|sig_b|sig_a` — no label columns exist in the signals file
(label-blindness is structural, not a convention).

## H6 provenance

Built for the H6 laundering threat (GEN→EXT relabel defeats label-trust);
consumed only by the W7 battery. WILD-A may reuse it but must not modify it.
