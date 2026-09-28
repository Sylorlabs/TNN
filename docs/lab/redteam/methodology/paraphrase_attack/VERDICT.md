# VERDICT — adversarial paraphrase attack on prose v1 (Sol #1)

**Date:** 2026-09-21/22. Prereg: `PREREG.md` (frozen pre-score; battery sha256
`f6189f4b…22fad` recorded pre-score).
**Target claim:** prose-learning PREREG.md — "test measures generalization
across wordings, not template memorization."
**Method:** 48 clean facts × 3 probe tiers (original / mild / adversarial),
scored through the EXISTING 0-diff-verified oracle pipeline
(`prose-learning/src/oracle.py::pipeline`) — the mechanism under test is
byte-identical to the v1 verdict's. The v1 pipeline predates this battery, so
Sol's "tests unknown to authors until model frozen" demand is satisfied.
Battery hand-written by the redteam analyst: no RNG, no LLM.

## Results

| Source | Original (generator probe) | Mild (novel syntax, same vocab) | Adversarial (disjoint vocab) |
|---|---|---|---|
| sol | 45/48 = 0.9375 | 45/48 = 0.9375 | 33/48 = 0.6875 |
| grok | 38/48 = 0.7917 | 38/48 = 0.7917 | 27/48 = 0.5625 |

Per-family adversarial mastery:

| Family | sol adv | grok adv | Mechanism of failure/success |
|---|---|---|---|
| alpha-pos | 0.917 | 0.917 | entity letter token is near-unique; overlap+tiebreak luck |
| letter-count | 0.667 | 0.500 | unique entity word usually disambiguates; stemmer conflations (`misunderstandings`/`misunderstanding`) merge facts |
| pub-year | 1.000 | 0.583 | entity name (Hamlet, Moby-Dick) unique across all 240 facts → single shared token wins outright (Jaccard 1/7 beats 240 zeros) |
| misc-count | 0.167 | 0.250 | **collapse**: no unique entity token, concept vocabulary replaced → 0-overlap tie soup → lowest-id winner |

## Kill bars

| Bar | Outcome |
|---|---|
| KB-MILD (≥0.90) | sol 0.9375 HOLD; grok 0.7917 TRIP on the absolute bar — **but Δ(mild−original) = 0.000 on both sources, every family**. No syntax fragility exists; the trip is inherited from grok's baseline, not caused by syntax novelty. The bar's intent is satisfied. |
| KB-ADV | sol 0.6875 → **PARTIAL**; grok 0.5625 → **PARTIAL** (band was 0.50–0.80). |

## What this proves and what it doesn't

**Proves:** the v1 pipeline is a word-overlap matcher whose "generalization"
is vocabulary-coupled. Novel syntax costs nothing (mild == original exactly);
novel concept vocabulary costs 23–25pp overall and collapses retrieval to
~0.2 where disambiguation depends on concept words rather than a unique entity
token. The prereg's "generalization across wordings" claim is weakened to:
generalization across *the generator's template inventory*, which shares
vocabulary by construction. This is consistent with the program's own v2 PARA
result (0.26–0.63 single-exposure) — brittleness to phrasing is real and
measured twice now.

**Doesn't prove:** that TNN-the-architecture can't comprehend (v2/v3 are the
admittedly-shallow-pipeline's successors); that the quality refutation is
wrong *within* the generator's distribution (Q=+0.0022 used the same coupled
probes for all sources, so the comparison was fair); or that average-case
natural paraphrase would be this bad (this battery is ADVERSARIAL by design —
worst-case vocabulary fragility, not a natural-paraphrase estimate).

## Artifacts

- `PREREG.md` (frozen pre-score), `paraphrases.py` (hand-written table),
  `paraphrase_battery.jsonl` (sha256 `f6189f4b…22fad`), `score_paraphrase.py`,
  `results.json` (per-fact table).
- Scoring reuses `prose-learning/src/oracle.py` unmodified; no new learner build.
