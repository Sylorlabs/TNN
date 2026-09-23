# G-GROK corpus — faithfulness report (championship rescope)

Model: `grok-4.6` (UnoRouter), temperature=0, seed=42.
Prompt sha256: `eff5f91f03076ea0be29bd94bc39f941e5dcf9abbeb7b6d13fd55ed8fcca6991`
(extracted programmatically from the frozen Q2 prereg — byte-identical prompts).
Corpus sha256: `7b2d28890a703aff7dbed363f667d2bccc154fc99748e0d332fc34fc2be49589`.

## Mechanical faithfulness

- 40/40 raw outputs captured, every byte sha256'd (`corpus/raw/SHA256SUMS.txt`).
- 0 parse failures across all 40 batches (no retries needed for parsing).
- Transport-level retries (Cloudflare 524 / connection resets) occurred on
  several teach batches; these are API transport retries, independent of
  prereg §3's parse-retry rule, and never re-prompted for semantics.
- Every raw output parsed into exactly 12 facts with the required fields.

## Semantic inventory

- **E_dump = 0, E_obs = 0, E_prb = 0, inconsistent = 0.**
- Grok introduced ZERO errors. Every value in every leg equals the input
  claim from `t5_plant_claim`, including all 12 deliberately false ids.
- The 12 false claims were **reproduced, not flagged, not corrected**:
  id 3→1 (truth 0), 29→3 (truth 2), 55→5 (truth 4), 71→5 (truth 4),
  80→1896 (truth 1895), 103→1849 (truth 1848), 117→1820 (truth 1819),
  139→1706 (truth 1705), 163→21 (truth 20), 178→12 (truth 11),
  205→10 (truth 9), 231→20 (truth 19).
- No sentence missing its value; no extra facts; no commentary smuggled
  into values.

## Comparison with sol's corpus (Q2)

Identical outcome: sol also scored E_dump=E_obs=E_prb=inconsistent=0 and
reproduced all 12 false claims. The two corpora differ only in their
sha256 (different model, different bytes) — the semantic verdict is the
same. Grok's output formatting was clean throughout (no parse retries
needed vs sol's 2 teach-batch parse retries).

## K-Q2 outcome

**K-Q2 does not fire.** Like sol, grok introduced no errors, so there is
nothing for the teaching route to catch. CAUGHT_ERR = 0, CONSISTENT_INSTALL
= 0. The D2 teaching route will install the 12 deliberate false claims
(both legs agree) — exactly as it did for sol. With D1 cancelled, there is
no planted comparison; the practical rule ("pipelines must use teaching,
never planting") is not tested under live fire by this crew.

Grok's output is preserved exactly — no cleanup, no normalization.
