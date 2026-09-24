# RUNLOG — T2-PROSEV3 (independent re-verification)

**Date:** 2026-09-23 PDT
**Re-verifier:** replacement coordinator (Wave-2 crossref)
**Frozen prereg:** 7b2100d09911c5c10252c5756c7def288e70bd1f

See VERIFY.md for the full verification report.

## RV2 — Resumed challenge forks (2026-09-24, replacement re-verifier)

**CHAL-P1 deviationectomy:**
- Built `learn3_devectomy.zag` (narrowed coreference trigger).
- Sub-core: 16/24 (narrow) vs 11/24 (wide); 5 registered items confirmed.
- Championship: 4 sources × 5 reps = 20 logs, byte-identical within source.
- Scores (external verify3.zag): grok 183, sol 204, step 208, muse-native 227.
- Log digests: see `work/forks/runs/digests/RV2_DIGESTS.md`.

**CHAL-P3 wrong-value analysis:**
- From deviationectomy logs: grok max 185 < 189; sol max 204 (no gain).
- Cannot flip. Kill bar unreachable.

**QUOTE-FIX fork:**
- Built `learn3_quotefix.zag` (curly-quote recognition in rule 2a + quote
  stripping in ent_finalize).
- sol: 204 → 215/228 (3 reps byte-identical, sha256 ac181523…).
- grok/step/muse-native: unchanged (byte-identical logs to devectomy).
- 2/4 FAIL stands.

**CHAL-P2:** Not executed (cannot affect RV-BROKE kill bar; documented in
VERIFY.md as limitation).

**Binaries:** `learn3_devectomy`, `learn3_quotefix`, `verify3_bin` built and
tested locally; NOT committed (binary exclusion rule). Sources committed.
