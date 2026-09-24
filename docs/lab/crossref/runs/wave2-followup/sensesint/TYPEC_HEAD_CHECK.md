# SENSESINT HEAD Type-C check — 2026-09-24

**HEAD:** `7478e5a0b4c53266c73f6dfc4f78462142d5ebbe` (tnn-native-lab)
**Manifest:** `docs/lab/GROK47_OVERNIGHT/senses-integrity/ITEMS_DONE.tsv` (140 rows, frozen)
**Method:** `typec_head_check.py` — parsed the 140-row manifest, fetched the
`docs/lab` subtree recursively at HEAD via the GitHub API, compared all 140
paths by presence + byte size. (Whole-repo recursive tree is API-truncated;
the docs/lab subtree is complete and untruncated.)

## Result: 140/140 paths present at HEAD — zero missing

- **139/140** manifest-exact sizes.
- **`docs/lab/redteam/bar-audit/PROPOSED_BARS.md`** — present, 11846 B vs
  manifest 11587 B (+259). Cause: legitimate post-freeze crew edit
  `1e1080dc57a4` (2026-09-22, "N9 reword fix: pin tier-3-attributable delta,
  flag judgment-call threshold") — single-row reword, diff verified benign.
  The manifest size predates the edit; the evidence path is not missing.
- **`docs/lab/senses/rematch/code/kb5.py`** (2731 B) and
  **`docs/lab/senses/rematch/code/run_all.py`** (5801 B) — present at
  committed sizes; manifest sizes (2189/4302) are stale pre-final drafts,
  established by the recovery crew (committed bytes byte-identical to the
  worker's final local copies).

## Disposition

The old PARTIAL was historically correct at frozen pin
`7b2100d09911c5c10252c5756c7def288e70bd1f` (10 evidence paths absent from
the freeze tree). At HEAD the evidence gap is fully remediated: all 140
paths present, the 10 recovered items byte-identical to independently
rebuilt originals, and the GK trial results re-derived byte-identically
(H1/H2/H3 all SUSTAINED re-derivable). Per Micah's directive not to freeze
SENSESINT as PARTIAL, the current disposition at HEAD is **REPRODUCED**
(140/140 evidenced; the 130/130 verdicts on the originally verifiable items
stand, and the 10 recovered items' claims re-derive).
