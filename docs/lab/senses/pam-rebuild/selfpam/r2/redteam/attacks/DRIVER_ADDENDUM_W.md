# Fork W Driver Addendum (Retrospective)

**Status:** RETROSPECTIVE — committed after blind execution began. This
discloses a process deviation.

**Deviation:** The attack prereg requires fork-specific driver addenda to be
committed BEFORE blind execution. The W addendum was NOT committed before
W's blind runs began. This is a sequencing violation. It is disclosed here
retrospectively rather than concealed or backdated.

**Adapter actually used:** `~/workspace/selfpam_r2/attacks/adapt_w.py`

**Adapter representation (documented per task):**
W's ATOM parser accepts only a single token for labels, and its
canonicalizer (cn_text) splits on spaces for synonym replacement.
Full-sentence labels cannot work. This adapter uses deterministic symbolic
labels derived from exact sentence identity:

- Store labels: `S<wid>` (e.g., S1, S2, ..., S50).
- Grounded atom labels: `S<wid>` (exact match → recall license passes).
- Confabulated atom labels: `X<fid>_<span>` (no store match → license fails).

This tests W's externally supplied witness contract (exact label match in
vf_resolve/vf_license), NOT native semantic atomization. Sentence text is
preserved in TEXT for span/coverage.

**Paraphrase mappings:** GOLD, SM, and FLIP paraphrases are mapped to store
wids via deterministic synonym-aware Jaccard overlap (maps in
`w_attack/gold_map.tsv`, `w_attack/sm_map.tsv`, `w_attack/flip_map.tsv`).
For SM (SAME) pairs, the wid is propagated within the pair so both sides
share the label (paraphrase stability).

**Known limitations:**
- M2 (meaning-flip divergence): With symbolic labels, verdicts depend only
  on store membership, not meaning. Both FLIP sides map to the same wid (or
  both unmapped), so verdicts do not diverge. M2 is expected to FAIL. This
  is a limitation of the symbolic adapter, not a W mechanism failure.
- M5 (generator-authored rejection): W's recall license does not distinguish
  WORLD from GENERATOR authorship; it grounds any label match. M5 is
  expected to FAIL. This is a real W mechanism limitation.

**Determinism:** All 7 batches byte-identical ×2. Zero RNG.

**Date:** 2026-09-24
