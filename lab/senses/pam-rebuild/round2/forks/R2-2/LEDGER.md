# R2-2 Build Ledger

**Date:** 2026-09-23
**Branch:** tnn-native-lab
**Toolchain:** ~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1

## Sources (committed under src/)

- `r2gen.py` — fixture generator (MASTER seed 20260923, zero RNG)
- `sense2.zag` — pure-Zag percept pipeline + memory contract
- `enroll2.py` — exemplar/bank enrollment generator
- `exemplars.zag` — 370 frozen noise-fixture exemplars (generated)
- `falsebank.zag` — 7 frozen known-false collision signatures (generated)
- `R33_NATIVE_IO_V1.zag`, `R33_NATIVE_SHA256_V2.zag` — runtime imports
- `run_eval.py`, `score2.py`, `verify_chain.py`, `probe_bank.py` — evaluation harness

## Compiler workarounds (not prereg changes)

1. **Chunked builders:** znc hangs/crashes on SHA256 + single 3700-write builder. Split into 40-record chunks (10 for exemplars, 1 for bank). Proven safe at 400 puts/chunk.
2. **Stride fix:** `(i*10+w*4)` → `(i*40+w*4)` in EX_get/FB_get (records are 10 words = 40 bytes).
3. **Differentiated helpers:** FB helpers textually distinct from EX to avoid `__clos_cap` clash.
4. **Unrolled FB_fill:** while-loop fill miscompiled when two identical fills imported together.

## Bank (7 entries, PREREG-faithful)

Per PREREG_R2-2.md §1: G3's harmonic-boost ×1.15 (1, deduplicated from 3 identical), G3's occlusion-bar (2), reversed-video (2), H1's flicker/metamer (2).

See `src/BANK_MANIFEST.txt` for SHAs and sources.

## Exemplars (370)

All frozen harness noise fixtures (t1-t6), enumerated by enroll2.py. See `src/EXEMPLAR_LEDGER.txt`.

## Binary

`sense2` built from `sense2.zag` + generated tables. NOT committed (binaries excluded).

## Evaluation

Three byte-identical runs over 11,285 fixtures (370 primary + 5,100 normal + 5,815 adversarial), 8 shards each, hash-chained ledgers. See `evidence/run1/`, `run2/`, `run3/`.
