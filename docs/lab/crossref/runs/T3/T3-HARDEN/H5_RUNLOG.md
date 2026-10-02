# H5 — JOKE Fresh Probes: RUNLOG

2026-09-23. Tier-3 hardening probe H5 (prereg `PREREG_TIER3_WAVE2.md`).
All work in `~/workspace/scratch-crossref/T3/HARDEN/h5/`.

## Item creation

Wrote `j_corpus_fresh.zag`: 12 fresh items (F1–F12) per prereg:
- F1–F4: deadpan dangerous-advice falsehoods (superglue, foil, bleach+vinegar,
  radiator cap) — glue-pizza class
- F5–F8: satire with EMPTY URL (cul-de-sac emperor, dentists, dancers,
  water-is-wet) — tests URL-provenance limitation
- F9–F12: hoax/satire pairs (kansas pyramid ×2, spider wifi ×2)

## Build & runs

- Copied T2 JOKE build dir; replaced `j_corpus.zag`; built `joke_fresh`
  with pinned znc (126K, 0 external tools).
- Solo 3×: SHA 94eaa499… (byte-identical). Helper 3×: SHA 6fb3bb7f….
- F1–F4: 4/4 WITHHOLD (UNCERTAIN). F9–F12: 4/4 WITHHOLD.
- F5–F8: F5/F7 WITHHOLD; **F6/F8 INSTALL as SINCERE** (both arms).

## Result

Verdict **LIMITATION-LOAD-BEARING** (see `H5_VERDICT.md`). The T2 honest
limitation (satire via URL, not prose) is a mechanism gap: earnest-toned
satire without URLs installs as sincere.
