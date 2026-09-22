# Calibration report — intent classifier (2026-09-22, pre-freeze)

Dev set: `calibration/dev.json` — 10 hand-written items from general knowledge,
disjoint from the test corpus by construction (the test corpus is real web items
collected independently; these are synthetic). Run with the calibration driver
(`src/j_calib.zag` + generated `src/c_calib.zag`), pure Zag, zero RNG.

## Per-item results

| ID | Expected | Observed | Verdict |
|---|---|---|---|
| c1 | SATIRE | 3 SATIRE — R_SATIRE_STYLE (area man, sources confirm, at press time) | ✓ |
| c2 | JOKING | 2 JOKING — R_ABSURD (glue) | ✓ |
| c3 | UNCERTAIN-or-SINCERE | 5 UNCERTAIN — R_NO_MARKERS | ✓ (gap documented below) |
| c4 | SINCERE | 1 SINCERE — R_EARNEST (according to, researchers, scientists, studies) | ✓ |
| c5 | SINCERE-or-UNCERTAIN, not DECEPTIVE | 5 UNCERTAIN — R_NO_MARKERS | ✓ |
| c6 | JOKING | 2 JOKING — R_EXPLICIT_JOKE (lol, /s) | ✓ |
| c7 | DECEPTIVE | 4 DECEPTIVE — R_FABRICATION (forward this, before they delete, copy and paste, send this to, they don't want you to know) | ✓ |
| c8 | SATIRE | 3 SATIRE — R_SATIRE_SOURCE (theonion.com) + style | ✓ |
| c9 | UNCERTAIN | 5 UNCERTAIN — R_NO_MARKERS | ✓ |
| c10 | JOKING | 2 JOKING — R_ABSURD (bleach) + R_EARNEST (rule 3 decides before conflict) | ✓ |

**10/10.** No marker-list changes were needed; the lists are frozen as drafted.

## Known gaps (frozen into the design, not tuned away)

1. **Earnest-presented absurdity (c3, the DHMO class).** An absurd claim written
   in a flat earnest tone with no joke/absurd/style/fabrication markers lands
   UNCERTAIN. Detecting it would require world knowledge (DHMO = water), which a
   marker reader does not have. Any "chemical scare" marker would be
   item-specific, so it stays out. System behavior is still safe: UNCERTAIN →
   WITHHOLD on the install gate.
2. **Marker-free sincere claims (c5).** Short sincere folk claims with no earnest
   markers land UNCERTAIN rather than SINCERE. This is honest abstention; the
   install gate withholds, and (e)-category install dispositions are descriptive
   only per the prereg.

## Determinism

Two consecutive runs of the calibration binary: byte-identical output.
