# TASTE PROBE — is the "simplicity bias" a genuine aesthetic opinion or an artifact?

Date: 2026-09-22. Authority: Micah's direct order ("TNN needs its own opinion;
if simplicity is its opinion then thats the result"; no debiasing installed).
This probe does NOT change any frozen bar, taste function, or Q3 verdict.

## Method

(a) **Justifications in TNN's own terms.** The frozen taste functions ARE TNN's
operationalized aesthetics (written before any Q3 outcome). An independent
Python port of both visual taste functions was verified **16/16 exact** against
the logged Q3 scores, then each of the 8 pair-decisions was decomposed into
sub-score margins to name the decisive criterion — what TNN's aesthetic
actually cited for each pick.

(b) **Consistency.** Decisive-criterion distribution across all decisions;
how often the simpler side won; how often SIMPLICITY was decisive.

(c) **Novel-pair probe.** 4 NEW pairs (never seen by any trial code), each with
a DOCUMENTED human preference for the MORE COMPLEX design, encoded in both
modes under the same care rules as the Q3 rebuild (1–6 elements from documented
visual facts, machine coords round multiples of 50, nearest human handles, no
outcome tuning, no iteration — encoded once, scored once):

| # | Pair | Simple side (0) | Complex side (1) | Documented human pref | Evidence tier |
|---|---|---|---|---|---|
| N1 | Pringles 2021 vs 2009 | 2021: floating brows, flat black mustache, no hair | 2009: brown hair, glinting eyes, textured mustache, bow tie | 2009 (complex) | STRONG — "unanimously hated", "huge backlash", generally negative (Mascotpedia, Logopedia, packaging-gateway, press) |
| N2 | Gmail 2020 vs 2013 | 2020: 4-color M mark | 2013: white envelope + red M accent | 2013 (complex) | STRONG — "pinnacle of useless minimalism", users "furious", "the red envelope stuck out much better" (TechCrunch, Android Police, ScreenRant, Creative Bloq) |
| N3 | Slack 2019 vs 2013 | 2019: 4-color pinwheel | 2013: 11-color plaid hashtag | 2013 (complex) | STRONG — "legions of commentators tearing strips off", "much-loved plaid hashtag", "simply awful" (Creative Bloq, Fast Company, WebDesignerDepot) |
| N4 | Firefox 2019 vs 2017 | 2019: abstract gradient swoosh | 2017: detailed fox + globe | 2017 (complex) | MODERATE — genuine criticism ("lost its paw", "too abstract", Mudspike forums); caveat: the viral 2021 "killed the fox" backlash was a misunderstanding of the parent-brand mark, not the browser icon |

## (a) Justifications — what TNN's aesthetic cited for each Q3 pick

### Machine mode (ALIGNMENT / SYMMETRY / CONTRAST)

| Pair | Score | Pick | Human | Decisive term | Justification in its own terms |
|---|---|---|---|---|---|
| Gap | 592–630 | classic | classic ✓ | SYMMETRY −50 | Classic's navy box + white text mirror-match; 2010's contrast edge (+12) not enough |
| Tropicana | 462–619 | original | original ✓ | SYMMETRY −200 | Original's orange/straw/leaf arrangement far more mirror-matched |
| New Coke | 666–766 | classic | classic ✓ | SYMMETRY −100 | The "NEW!" starburst breaks the 2010 side's symmetry |
| UC | 414–778 | seal | seal ✓ | SYMMETRY −300 | Seal's disc/book/text arrangement dominates on symmetry and contrast |
| Cracker Barrel | 700–539 | 2025 wordmark | original ✗ | SYMMETRY +200 | **Artifact:** a single centered element is trivially self-mirrored (300 vs 100); the original's contrast advantage (−39) loses |
| Starbucks | 775–794 | 1992 | 2011 ✗ | CONTRAST −19 | Near-tie (align 400–400, sym 300–300); the black inner field adds 19 points of tonal range — a 2.4% margin, noise-level |
| Mastercard | 545–439 | 2016 | 2016 ✓ | ALIGNMENT +100 | 2016's round coordinates |
| Apple | 446–289 | mono | mono ✓ | SYMMETRY +150 | Mono's elements self-mirror; rainbow's stripes only partly match |

### Human mode (HARMONY / BALANCE / SIMPLICITY)

| Pair | Score | Pick | Human | Decisive term | Justification in its own terms |
|---|---|---|---|---|---|
| Gap | 491–662 | classic | classic ✓ | BALANCE −200 | Classic's elements sit in mirror zones with matching colors |
| Tropicana | 591–625 | original | original ✓ | HARMONY −34 | Original's orange/red/green closer on the hue wheel (small margin) |
| New Coke | 591–712 | classic | classic ✓ | BALANCE −100 | (simplicity +37 voted for New Coke, lost) |
| UC | 562–641 | seal | seal ✓ | BALANCE −150 | (simplicity +37 voted for the monogram, lost) |
| Cracker Barrel | 1000–725 | 2025 wordmark | original ✗ | HARMONY +100 (all agree) | **Artifact:** one element → vacuous harmony 400 + trivial self-mirror balance 300 + max simplicity 300 = perfect 1000, unbeatable by construction |
| Starbucks | 662–691 | 1992 | 2011 ✗ | HARMONY −66 | **Simplicity voted WITH humans** (+37 for the simpler 2011) and was overridden by harmony |
| Mastercard | 508–528 | old | 2016 ✗ | BALANCE −50 | **Simplicity voted WITH humans** (+38 for 2016), overridden by balance |
| Apple | 612–642 | rainbow | mono ✗ | HARMONY −30 | Balance −150 and simplicity +150 cancel exactly; harmony breaks the tie for rainbow. **Simplicity voted WITH humans** and lost |

## (b) Consistency analysis

24 decisions total (8 Q3 + 4 novel pairs × 2 modes):

| Stat | Value |
|---|---|
| Simpler side won | 14/24 (58.3%) — barely above chance, not a stable preference |
| Agreement with documented human preference | 14/24 (58.3%) |
| Human-mode decisive terms | BALANCE 7, HARMONY 4, **SIMPLICITY 1** |
| Machine-mode decisive terms | SYMMETRY 8, ALIGNMENT 3, CONTRAST 1 (no simplicity term exists) |
| Human-mode misses where SIMPLICITY voted with humans | 3 of 4 (Starbucks, Mastercard, Apple) |

The "simplicity bias" label is **backwards** for three of the four human-mode
misses: TNN's simplicity instinct agreed with the documented human preference
and was outvoted by its harmony/balance instincts. SIMPLICITY was the decisive
term in only 1 of 12 human-mode decisions.

## (c) Novel probe results

| Pair | Machine pick | Decisive | Human pick | Decisive | Documented human pref |
|---|---|---|---|---|---|
| N1 Pringles | simple (688–581) | ALIGN +100 | simple (695–608) | SIMPLICITY +75 | complex ✗✗ |
| N2 Gmail | complex (324–756) | SYM −300 | complex (512–741) | BALANCE −150 | complex ✓✓ |
| N3 Slack | complex (424–569) | SYM −150 | complex (362–653) | BALANCE −300 | complex ✓✓ |
| N4 Firefox | simple (717–580) | ALIGN +100 | simple (862–620) | HARMONY +92 | complex ✗✗ |

2/4 complex picks per mode. No uniform simplicity preference. Where the simple
side won it was via alignment/harmony/simplicity margins on the specific
encodings — not a stable principle. Note N2: the complex (human-preferred) side
had FEWER elements, so SIMPLICITY voted for the complex side (−38) — the
simplicity term is a pure element-count term with no aesthetic content beyond
"fewer elements".

## Verdict

1. **Cracker Barrel (both modes): representation/scoring artifact, NOT a
   genuine aesthetic judgment.** A single-element design gets degenerate
   perfect scores by construction — human mode: vacuous harmony (400, no pairs)
   + trivial self-mirror balance (300) + maximal simplicity (300) = 1000, the
   maximum possible, unbeatable by any multi-element design; machine mode: a
   centered single element is trivially self-symmetric. The frozen functions
   cannot distinguish a good single element from a bad one. This is a flaw in
   the operationalized aesthetic (frozen before outcomes — recorded, not
   retro-fixed, per Micah's no-debiasing order).
2. **Starbucks / Mastercard / Apple (human mode): genuine criterion conflicts,
   and simplicity was on the humans' side.** No correction needed or made.
3. **Starbucks (machine mode): a 19-point contrast margin on a near-tie** —
   noise-level, not a principle.
4. **Novel probe: 2/4 per mode.** There is no stable simplicity opinion to
   record as "its taste". What IS stable: the degenerate single-element
   perfect score (a math property of the frozen functions) and TNN's
   harmony/balance instincts, which outvote its simplicity instinct 11-to-1.

**Bottom line for Micah:** TNN does not have a simplicity preference. It has a
degenerate-scoring bug that LOOKS like one in exactly one configuration
(single-element vs multi-element), and everywhere else its criteria fight it
out with simplicity usually losing. The Cracker Barrel miss is the bug, not
the taste.
