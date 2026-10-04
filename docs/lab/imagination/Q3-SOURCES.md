# Q3 — Human-preference pair sources (verified 2026-09-22)

All 8 pairs from the frozen `PREREG.md` §Q3 were re-verified against
public web sources on 2026-09-22. The documented human preference for
each pair is confirmed below. Search was via public web; no paywalled or
private sources.

| # | Pair | Documented human preference | Evidence | Tier |
|---|---|---|---|---|
| 1 | Gap 2010 redesign vs classic blue box | CLASSIC (old) | 2010 redesign reverted after 6 days following backlash; 2000+ protest comments, parody account 5000+ followers (prereg sources: BBC/Branding Journal via press) | STRONG |
| 2 | Tropicana 2009 vs straw-in-orange | ORIGINAL (old) | Sales fell 20%; original packaging restored after ~46 days; $35M campaign scrapped (prereg sources: SEC filings via Medill) | STRONG |
| 3 | New Coke 1985 vs Coca-Cola Classic | CLASSIC (old) | Original returned after 79 days amid high complaint volume (8,000 calls/day, 40,000 letters); reverted 1985-07-11 (prereg sources: HISTORY.com; Coca-Cola Company) | STRONG |
| 4 | UC 2012 monogram vs century-old seal | SEAL (old) | 50,000+ petition signatures; new mark use suspended Dec 2012 (prereg sources: Higher Ed Dive; UC statement) | STRONG |
| 5 | Cracker Barrel 2025 rebrand vs old-timer logo | ORIGINAL (old) | 2025 minimalist wordmark (dropped "Uncle Herschel") met backlash; stock dropped ~7–11%; company announced Aug 26, 2025 it would keep the original logo (sources: The Branding Journal, USA Today/Beacon Journal, Brandfetch, Jukebox Print — all accessed 2026-09-22) | STRONG |
| 6 | Starbucks 2011 wordless siren vs 1992 logo | NEW (2011) | 2011 redesign (siren alone, no words/ring, by in-house + Lippincott) won 1st place 2011 Brand New Awards; still in use 2011–present, 15 years (sources: Logopedia/Starbucks logo history, Creative Bloq, Medium/TradeFlock, SecureYourTrademark — all accessed 2026-09-22) | MODERATE |
| 7 | Mastercard 2016 flat circles vs prior logo | NEW (2016) | Pentagram (Michael Bierut, Luke Hayman) redesign: flat interlocking red/amber circles, solid orange overlap; won "Logo of the Decade" (Creative Bloq awards, 25.45% vote); >80% spontaneous recognition without wordmark (sources: Creative Bloq, Fast Company, Dezeen, InvestorPlace — all accessed 2026-09-22) | MODERATE |
| 8 | Apple 1998 monochrome vs rainbow | NEW (mono) | Rainbow (1977–1998/99) replaced by single-color mark with the 1998 iMac G3; "one of the most recognizable logos in the world"; rainbow seen as dated/"toy" brand, mono aligned with Think Different turnaround (sources: Cult of Mac, SlashGear, Logopedia/Apple, WeAndTheColor, CGain — all accessed 2026-09-22) | MODERATE |

## Encoding notes

Encodings (`ig_pair` in `imagination/src/imagine.zag`) were rebuilt on
2026-09-22 from the factual references above (same facts, two codecs).
Prior encodings were degenerate (single-element ties, pair 7 identical on
both sides, pair 8 encoded as audio for a logo pair) and are replaced.
Rebuild rules, to honor the circularity guard (taste functions frozen
before encodings; encodings faithful, not outcome-tuned):

1. Each design is 1–6 elements stating documented visual facts (field
   color, mark color, layout position, extra/missing elements).
2. Same encoding care for both sides: machine coordinates are round
   multiples of 50 throughout; human colors are the nearest fixed-vocab
   handles. No side-specific tweaks.
3. No attribute was chosen to push a score toward the known outcome;
   scores are whatever the frozen taste functions compute.
4. Pair order (side 0 / side 1) is as listed in the frozen prereg table.
   Ties predict the first-listed design per the frozen rule, and ties are
   reported as ties, not as discrimination.
