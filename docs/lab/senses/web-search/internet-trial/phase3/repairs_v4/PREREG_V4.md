# HELL-HOLE V4 PREREG — stance/logic repair campaign

**Date:** 2026-09-23
**Status:** FROZEN (committed before any v4 scoring run)
**Parent trial:** v3 (commit `51e944390624942c167596c3feb1e46b2b003872`) — PASS but
borderline (M1 0.818, K1 0.182); systematic classifier failures: negation
("bats are NOT blind" → AFFIRM), unsupported-claim affirmation
("No clinical evidence supports celery juice cures" → AFFIRM), contrastive
refutation ("22–33 senses" vs "exactly five" → AFFIRM; goldfish "six months"
vs "three seconds" → AFFIRM), causal "because" (8/8 ice-float rows → NEUTRAL).
Two false installs (V3-05, V3-07), one miss (V3-03).

**New directive (Micah, 2026-09-23):** the v3 verifier REJECTED good logic, and
depending on online/external logic is bad — rebuild verification so every logic
judgment comes from TNN's own native logic machinery, nothing external.

## Track L — lexicon front-end repair (r12.zag family fixes, pure Zag)

Repairs the R1/R2 stance tagger's systematic families without breaking what
works. Each family gets a hunter-built corpus (blind oracle tags: oracle
written BEFORE running the classifier) and a fixer crew.

### Families (minimum)
- L-NEG: negation & scope (not/never/no/none/n't/"no evidence", double
  negation, negation outside predicate scope, "not X but Y")
- L-CON: contrastive refutation & comparatives (ranges vs exact numbers,
  more/less than, at-least/most, superlatives, X-vs-Y, whereas/while)
- L-CAU: causal structure (because/causes/leads to/due to/results in,
  mechanism explanations, causal chains, prevented-cause)
- L-COND: conditionals (if-then consequent not asserted)
- L-QNT: quantifiers (all/some/most/no/none)
- L-HEDGE: hedging (may/might/could/suggests/possibly/appears)
- L-TMP: temporal order (before/after)

### Bars (Track L)
- **M-FAM:** per-family accuracy on its frozen hunter corpus ≥ **0.85**,
  AND no other family's accuracy decreases vs the frozen-r12 baseline on
  that family's corpus (no robbing Peter to pay Paul).
- **M-V3SEED:** the 5 known v3 failure rows flip to correct tags:
  "bats are NOT blind"→DENY, "No clinical evidence supports celery juice
  cures"→DENY, "22–33 senses"→DENY, "goldfish six months"→DENY, and ≥6/8 of
  the ice-float "because" rows →AFFIRM.
- **K-REG382:** 382-row frozen regression diff vs `r12.zag@a867c3be` must
  contain ONLY justified rows; every diff row documented with (idx, old
  tag/reason, new tag/reason, why intended). Curated-18 (oracle behavior
  specs) must remain 18/18.
- **K-DET:** 3 runs byte-identical SHA-256 on every corpus.
- **K-PURE:** pure Zag, zero RNG, no web, no Python in the verdict path.

### Regression gates (must hold, else track FAILS)
- Joke classifier: fresh UNSEEN joke set (new jokes, blind intent labels),
  accuracy ≥ 0.90 AND zero deadpan installs (K-JOKE < 0.25 as in v3).
- R3 gate: 6/6 v3 gated candidates (V3-10,11,12,13,18,19) → WITHHOLD.
- R6 precedence: 6/6 seeded CONTRADICTS (V3-14,20–24) → REJECT.

## Track G — native logic rebuild (Micah's directive)

### Audit (first)
Audit the v3 verifier for external/online dependence. Every point where a
logic or stance judgment depends on something outside TNN's own machinery
gets listed: live browser_search evidence collection, hand-normalized TSVs,
hand-seeded R6 verdicts, hand tiering, hand helper texts. Classified as
EXTERNAL-SOURCE (evidence provenance) or EXTERNAL-JUDGMENT (a human/external
tool decided instead of TNN). The rebuild must eliminate all of them from
the judgment path.

### LOGIC-CORE (native Zag logic engine)
Pure-Zag engine: (claim proposition, evidence propositions) →
{AFFIRM, DENY, NEUTRAL} via native logical rules, emitting a proof trace
(rule IDs fired). No lexicon heuristics, no web, no seeded verdicts, zero
RNG. Proposition batteries are frozen TSVs
`id \t claim_prop \t evidence_props \t oracle`; battery SHAs frozen BEFORE
engine scoring runs. Numeric comparison ("22–33" vs "five") is implemented
natively inside the engine (number parsing + integer comparison in Zag) —
it is logic machinery, not an external engine.

### Families + bars (Track G, per-family accuracy on frozen battery)
- G-NEG negation (20 items): ≥ 18/20 (0.90)
- G-CON contrastive refutation incl. numeric ranges (20): ≥ 18/20 (0.90)
- G-CAU causal because/causes (20): ≥ 18/20 (0.90)
- G-QNT quantifiers (20): ≥ 17/20 (0.85)
- G-COND conditionals (20): ≥ 17/20 (0.85)
- G-HEDGE hedging (20): ≥ 17/20 (0.85)
- G-TMP temporal order (20): ≥ 17/20 (0.85)
- G-CMP comparatives (20): ≥ 17/20 (0.85)

### Kill bars (Track G)
- **K-V3PROOF:** the v3-rejected cases as propositions — V3-03 (ice floats,
  TRUE, causal evidence), V3-05 (goldfish memory, FALSE, contrastive
  evidence), V3-07 (five senses, FALSE, contrastive evidence) — 3/3 correct
  (AFFIRM where TRUE, DENY where FALSE). Else HALT.
- **K-MLOGIC:** the 5 v3 logic seeds (R6 CONTRADICTS cases) re-expressed as
  propositions must still yield contradiction, 5/5. Else HALT.
- **K-DET:** 3 runs byte-identical SHA-256. Else HALT.
- **K-PURE:** any web fetch, RNG, or non-Zag judgment in the verdict path →
  HALT.
- **K-FAM50:** any family below 0.50 → HALT (systematic, not noise).

## Determinism & purity (both tracks)
Zero randomness anywhere. 3 consecutive runs, byte-identical SHA-256,
recorded. Pure Zag for mechanisms and verdicts; Python only for
harnessing/analysis (never in the decision path).

## Amendments
Any change to families, bars, batteries, or kill criteria needs Micah's
re-approval. A PARTIAL never ends a track.
