# REDTEAM prereg — adversarial paraphrase attack on prose v1 (Sol #1)

**Frozen:** 2026-09-21, before battery scoring. Redteam methodology-skeptic crew.
**Target claim (prose-learning PREREG.md):** "Train and test use DIFFERENT
sentence templates (dump vs probe wordings), so the test measures
generalization across wordings, not template memorization."
**Attack (Sol #1 — benchmark leakage / test-generation coupling):** both
templates come from the SAME generator; the shared vocabulary, stemmer rules,
and derivation templates make "held-out" meaningless. A deterministic
bag-of-stemmed-words pipeline scores 0.83–0.96 on generator-coupled probes
while failing on paraphrases a human would answer trivially.

## Battery

- 48 clean facts per source (fact ids aligned across sources; none in the 12
  false ids), 4 families × 12:
  - alpha-pos: {0,5,8,12,17,21,25,31,35,40,44,47}
  - letter-count: {48,52,56,60,64,68,72,76,84,88,92,94}
  - publication-year: {96,99,104,105,110,111,118,121,124,130,136,142}
  - misc-count: {144,147,151,155,160,200,204,210,216,217,220,224}
- Sources: sol (v1 best, 0.9649) and grok (v1 worst, 0.8289).
- Per fact, THREE probes: (a) ORIGINAL (from frozen test_{source}.txt);
  (b) MILD — hand-written, same content vocabulary as the generator, novel
  syntax the generator never produced (isolates syntax fragility);
  (c) ADVERSARIAL — hand-written, same meaning, content words deliberately
  disjoint from train+test vocabulary where a human synonym exists
  (isolates vocabulary coupling).
- Paraphrases are hand-written by the redteam author (no RNG, no LLM),
  frozen in `paraphrase_battery.jsonl` (sha256 recorded below, pre-score).
  Correctness criterion: answer == probe_value from the frozen test set.

## Scoring

The EXISTING independent oracle pipeline (`prose-learning/src/oracle.py`,
`pipeline()` + Jaccard argmax + lowest-id tiebreak — the 0-diff-verified
implementation of the frozen v1 mechanism) installs all 240 train sentences
per source and scores the three probe tiers. No new learner build; the
mechanism under test is byte-identical to the v1 verdict's. Scoring script:
`score_paraphrase.py`. Deterministic, zero RNG.

## Kill bars (set pre-score)

| Bar | Rule | Reading |
|---|---|---|
| KB-MILD | mild mastery ≥ 0.90 | Syntax-only novelty must not break retrieval |
| KB-ADV-CONFIRM | adversarial mastery < 0.50 | → test-generation-coupling attack **CONFIRMED** (evidence) |
| KB-ADV-PARTIAL | 0.50 ≤ adversarial < 0.80 | → attack **PARTIAL** |
| KB-ADV-REFUTE | adversarial mastery ≥ 0.80 | → attack **REFUTED** on v1 |

Interpretation guardrail (preregistered): an ADV collapse proves the v1
pipeline is a word-overlap matcher, not a comprehender. It does NOT prove
TNN-the-architecture cannot comprehend — v2/v3 exist precisely because v1's
pipeline was admittedly shallow. The attack targets the HEADLINE ("prose path
viable at 0.83–0.96 / quality refuted in prose"), not the architecture's ceiling.

## Battery sha256 (recorded pre-score)

`paraphrase_battery.jsonl` sha256:
`f6189f4b76b6b17848a865d35ba356c91d386160e0179771581ad94f92322fad`
(48 items; hand-written paraphrases frozen before any scoring run.)
