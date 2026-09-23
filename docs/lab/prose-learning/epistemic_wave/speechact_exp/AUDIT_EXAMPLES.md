# Example Quality/Diversity Audit

**Date:** 2026-09-22 · **Prereg:** PREREG_DECLINE.md, Audit section (frozen, committed e1f2d2c642e0)
**Question (Micah):** "Are they good examples? Examples shouldn't be the same thing — they should all be different in their own ways."
**Method:** Pure Python analysis of the 224 example utterances (32/concept). The Zag engine was not touched.
**Feature definition (byte-faithful to `delib_vol.zag`'s front-end):** lowercase; words = `[a-z]+`
runs; unigrams (word length ≥ 3, deduped within utterance); adjacent bigrams (ANY word
length, joined `_`, deduped within utterance); one `first_<firstword>` marker; `qmark` if
the line contains `?`; `exclam` if it contains `!`.

## Headline

Micah's charge lands — on **three of the seven concepts**. Hypothetical, counterfactual,
and analogy are template-redundant **in the frame, not the content**: identical
grammatical openers carry most of the feature mass, so later examples add fewer and fewer
new features (novelty drops 21–33% from r1–2 to r3–32). Sarcasm and joke have rigid frames
too but stay content-diverse (sarcasm's novelty is *flat* at 20.5 → 20.2 — its examples
genuinely are "all different in their own ways" in content). Poetry and implicature are
formally varied. Meanwhile cross-concept feature overlap explodes with N
(8 → 61 → 291 shared features at N = 2, 8, 32) — the frame repetitions are exactly the
features that get shared, which is the dilution mechanism H-D3 suspects.

## 1. Distinct-token ratios

| Concept | Uni ratio | Uni (distinct/total) | Bi ratio | Bi (distinct/total) |
|---|---|---|---|---|
| sarcasm | 0.830 | 263 / 317 | 0.968 | 362 / 374 |
| joke | 0.811 | 232 / 286 | 0.964 | 347 / 360 |
| analogy | 0.772 | 179 / 232 | 0.905 | 257 / 284 |
| poetry | 0.741 | 186 / 251 | 0.941 | 241 / 256 |
| implicature | 0.674 | 178 / 264 | 0.934 | 282 / 302 |
| counterfactual | 0.633 | 191 / 302 | 0.827 | 316 / 382 |
| hypothetical | 0.623 | 218 / 350 | 0.886 | 335 / 378 |

Ratios = distinct / total tokens (deduped within utterance, per the engine). Hypothetical
and counterfactual recycle the most content words; sarcasm and joke recycle the least.

## 2. Template adherence

Template rules defined after reading the files (documented below). Score = fraction of
the 32 lines matching.

| Concept | Rule | Hits | Interpretation |
|---|---|---|---|
| sarcasm | First word ∈ praise set {superb, tremendous, marvelous, lovely, brilliant, fantastic, terrific, peachy, admirable, awesome, amazing, ideal, outstanding, best, delightful, swell, stellar, great, charming, genius, thoughtful, beautiful, grand, exquisite, dandy, wonderful, remarkable, perfect, splendid, incredible, classic} (allowing a leading "oh, ") | **30/32** | Rigid frame |
| hypothetical | First word ∈ {suppose, what, imagine, let, pretend, hypothetically, consider, picture, say} | **32/32** | Fully templated opener |
| counterfactual | Starts with if/had, or contains would've/could've/might've/should've/'d have (all conditional-past markers) | **32/32** | Fully templated frame (27/32 under the strict no-'d-have rule; the 5 misses are "I'd have…/She'd have…" — the same construction) |
| analogy | Copula-centered: contains " is "/" was "/" are "/" were " (29/32 under strict " is a/was a/like" — the 3 misses are copula metaphors without the article, e.g. "was two radios", "is molasses poured") | **32/32** | Fully templated frame |
| poetry | Probe: starts with "the" → 16/32. No dominant template found. | — | Form varies (predicates differ) |
| implicature | Probe: contains "has/have been" or "since" → 9/32. No dominant template found. | — | Form varies; genre-narrow (all domestic "something needs doing" observations) |
| joke | First word ∈ {my, the, i} | **32/32** | Frame-templated ("X does incongruous human thing") but content-maximally diverse |

Top repeated frame bigrams (evidence of template mass): counterfactual `had_the` ×12,
`might_ve` ×9, `would_ve` ×9, `i_d` ×7; hypothetical `would_you` ×7, `how_would` ×5,
`let_s` ×4, `pretend_you` ×4; analogy `is_a` ×20 (twenty of 32 lines), `was_a` ×4;
sarcasm `oh` as first word ×11; joke `my` ×15 / `the` ×15 as first word.

## 3. Marginal novelty curves (file order)

New features each example adds beyond the union of all previous examples, k = 1..32.

| k | sarcasm | joke | poetry | implicature | analogy | counterfactual | hypothetical |
|---|---|---|---|---|---|---|---|
| 1 | 20 | 23 | 18 | 19 | 19 | 24 | 27 |
| 2 | 21 | 24 | 15 | 19 | 17 | 19 | 24 |
| 3 | 20 | 22 | 15 | 19 | 19 | 20 | 22 |
| 4 | 20 | 19 | 15 | 13 | 14 | 22 | 25 |
| 5 | 28 | 13 | 13 | 18 | 19 | 18 | 18 |
| 6 | 28 | 20 | 16 | 17 | 13 | 15 | 18 |
| 7 | 21 | 15 | 13 | 12 | 18 | 18 | 21 |
| 8 | 19 | 23 | 13 | 19 | 16 | 18 | 25 |
| 9 | 20 | 21 | 14 | 16 | 12 | 22 | 18 |
| 10 | 19 | 16 | 13 | 16 | 14 | 18 | 18 |
| 11 | 18 | 15 | 15 | 17 | 12 | 16 | 16 |
| 12 | 23 | 19 | 13 | 13 | 14 | 14 | 20 |
| 13 | 21 | 18 | 14 | 15 | 11 | 17 | 18 |
| 14 | 15 | 23 | 14 | 14 | 16 | 15 | 15 |
| 15 | 22 | 18 | 13 | 14 | 17 | 13 | 14 |
| 16 | 24 | 16 | 16 | 14 | 14 | 15 | 17 |
| 17 | 20 | 19 | 15 | 15 | 14 | 16 | 16 |
| 18 | 22 | 21 | 14 | 11 | 11 | 14 | 17 |
| 19 | 22 | 21 | 11 | 21 | 13 | 15 | 17 |
| 20 | 21 | 21 | 14 | 13 | 14 | 12 | 15 |
| 21 | 21 | 15 | 13 | 13 | 12 | 14 | 17 |
| 22 | 22 | 16 | 16 | 15 | 11 | 15 | 15 |
| 23 | 17 | 19 | 12 | 13 | 10 | 15 | 10 |
| 24 | 19 | 16 | 12 | 17 | 12 | 14 | 15 |
| 25 | 18 | 17 | 12 | 11 | 12 | 13 | 17 |
| 26 | 17 | 15 | 11 | 13 | 14 | 11 | 14 |
| 27 | 18 | 15 | 13 | 12 | 12 | 19 | 14 |
| 28 | 18 | 16 | 14 | 9 | 13 | 14 | 19 |
| 29 | 19 | 15 | 15 | 11 | 8 | 17 | 20 |
| 30 | 16 | 14 | 14 | 17 | 13 | 14 | 14 |
| 31 | 22 | 21 | 15 | 15 | 16 | 14 | 14 |
| 32 | 17 | 16 | 13 | 13 | 12 | 12 | 13 |

| Concept | Mean novelty k=1–2 | Mean novelty k=3–32 | Drop |
|---|---|---|---|
| sarcasm | 20.5 | 20.2 | **−1% (flat)** |
| joke | 23.5 | 17.8 | −24% |
| poetry | 16.5 | 13.7 | −17% |
| implicature | 19.0 | 14.5 | −24% |
| analogy | 18.0 | 13.5 | −25% |
| counterfactual | 21.5 | 15.7 | −27% |
| hypothetical | 25.5 | 17.1 | **−33%** |

Sarcasm is the standout: its novelty never declines — each new example keeps adding ~20
fresh features. The three template-redundant concepts drop 25–33%. Joke starts highest
(23.5) and stays highest (17.8).

## 4. Cross-concept overlap growth

Features appearing in ≥2 concepts' profiles, computed on the same first-N subsets the
experiment used:

| N | Total features | Shared across ≥2 concepts | Share |
|---|---|---|---|
| 2 | 289 | 8 | 2.8% |
| 8 | 1,059 | 61 | 5.8% |
| 32 | 3,666 | 291 | 7.9% |

Shared-feature count grows **36×** from N=2 to N=32 while total features grow 12.7×.
The shared features are exactly the frame vocabulary (the/the_, of_the, had_the, is_a,
would_you, has_been…) — the mechanism H-D3 describes (DISC_BAR starvation) is being
fed by the template frames documented above.

## 5. Verdicts

- **sarcasm — MIXED.** The frame is rigid (30/32 praise-opener; 11/32 begin "oh, "), but
  the content answers Micah's charge: uni ratio 0.830, bigram ratio 0.968 (nearly every
  bigram unique), and marginal novelty is FLAT (20.5 → 20.2) across all 32. Each
  misfortune is genuinely different. Evidence: *"Superb — the plumber cancelled an hour
  before the appointment. Really classy."* vs *"I love how my alarm chose today, of all
  days, to oversleep. Truly reliable."* vs *"Genius move, phone — autocorrecting the
  client's name into a vegetable. Seamless."*
- **hypothetical — TEMPLATE-REDUNDANT.** 32/32 opener template with a manufactured 8×4
  balance of openers (suppose/what/imagine/let/pretend/hypothetically/consider/picture+say
  each ×4 — suspiciously even, looks generated to pattern). Lowest uni ratio (0.623);
  novelty drops 33%. Evidence: *"Suppose the ocean tides rose six feet higher. Where
  would the coastline end up?"* / *"Suppose your dog could read your thoughts. Would it
  judge your cooking?"* / *"Suppose bread grew on trees like fruit. Which bakery would
  survive?"* — four of 32 start "suppose", and `would_you` recurs ×7.
- **counterfactual — TEMPLATE-REDUNDANT.** 32/32 conditional-past frame; `had_the` ×12,
  `might_ve` ×9, `would_ve` ×9, `i_d` ×7. Lowest bigram ratio (0.827); novelty drops
  27%. Evidence: *"Had the bakery opened Sundays, fresh rolls would've been ours to
  grab."* vs *"Had the landlord fixed that pipe, the basement would've stayed dry."* vs
  *"Had I learned to swim, last summer's lake trip would've been different."*
- **analogy — TEMPLATE-REDUNDANT.** 32/32 copula-centered; `is_a` alone covers 20/32
  lines. Content (the vehicles) is fairly diverse (uni 0.772), but the frame dominates
  the profile as N grows. Evidence: *"That old delivery van is a shopping cart with a
  hood."* / *"Her patience is a well that never runs dry."* / *"That song is a warm
  blanket on a freezing night."*
- **poetry — GOOD.** No dominant template (16/32 start with "the", but every predicate
  differs); uni 0.741, bigram 0.941; novelty decline is mild (−17%), consistent with
  natural saturation rather than templating. Evidence: *"The streetlamps blink awake,
  one by one, like tired commuters."* vs *"Fog tiptoes through the harbor, counting every
  mast."* vs *"Clouds drift like spilled flour across the blue table."*
- **implicature — MIXED.** No dominant template (probe features only 9/32) — formally it
  satisfies Micah's "all different in their own ways". But the genre is narrow: all 32
  are domestic "state of affairs implying someone should act" observations, and uni
  ratio (0.674) is middling. Evidence: *"The window over the sink has been open all
  morning."* vs *"My coffee cup's been empty since the waitress last came by."* vs
  *"These bags aren't going to carry themselves upstairs."*
- **joke — MIXED.** 32/32 my/the/i opener, but the highest sustained content novelty
  (23.5 → 17.8) and uni 0.811: the frame is the joke's delivery mechanism, not
  redundancy. Evidence: *"My hamster runs a tiny accounting firm and files my taxes
  every April."* vs *"The spaghetti in my pantry formed a string quartet. The acoustics
  are awful."* vs *"I challenged a hurricane to a staring contest. It blinked first."*

## 6. Answer to the lead's charge

**Are they good examples?** 3 of 7 concepts are not good *in the way Micah means* —
hypothetical, counterfactual, and analogy repeat the same grammatical frame 32 times,
so their later examples mostly re-contribute `had_the`, `is_a`, `would_you` instead of
new content. Those frames are also the shared cross-concept vocabulary that grows 36×
with N, directly feeding the distinctiveness-dilution mechanism (H-D3). **But quality
already have the audit of their novelty in file order (AUDIT_EXAMPLES.md §3). **But quality
alone cannot explain the whole decline**: sarcasm's examples are the most
content-diverse set in the batch (flat novelty, 0.83 uni ratio) and sarcasm still
collapses — 6/10 at r2 → 0–1/10 by r16, "the profile dissolves" (VOLUME_CURVE.md §5). The ordered workdirs
(`ord_diverse`, `ord_redundant`, `ord_proto`, `ord_outlier` — see ORDERS.md) now let
H-D2 test the quality direction head-on; the bar-artifact (H-D1) and dilution (H-D3)
tests will tell whether fixing the examples is enough.
