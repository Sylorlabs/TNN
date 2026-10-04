# B2 FIX REPORT — numeric guard on the endorse path (hell-hole V4)

## Change
File: `/home/hatch/workspace/scratch-hellhole/crews/b2/r12_con.zag` (copied fresh from `hellhole/r12_v3.zag`).
Binary: `/home/hatch/workspace/scratch-hellhole/crews/b2/r12_con` (built with pinned znc `--no-zagd`).

One new function block + two hook edits:
- `wnum()` — word-numbers one..thirty (single tokens).
- `umul()` — time-unit table: second(s)=1, minute(s)=60, hour(s)=3600, day(s)=86400, month(s)=2592000, year(s)=31536000.
- `is_demo()` — "one" after this/that/these/those/each/every/any is pronominal, not a quantity.
- `sp_grp()` — space-grouped thousands ("299 792 458" == 299792458).
- `ev_scan()` — extracts numeric entries (lo, hi, unit-class) from a text; ranges form on "to"/"and"/"-" ("22 and 33" -> [22,33]); i32 LE arenas, no `as []i32`.
- `numeric_guard(claim,title,snip)` — 0 allow AFFIRM / 1 force NEUTRAL / 2 force DENY.
  - No claim number, or no evidence number, or claim value equals / falls inside an evidence value/range of the same unit class -> 0.
  - Same unit class, no match -> 2 (contradiction).
  - Numbers on both sides but unit classes differ (e.g. unitless claim vs time evidence) -> 1 (not comparable).
- Hook in `r12_classify` after the deny scans: `ng==2 -> 16+7` (tag 2, new reason `numeric-mismatch`); on the endorse path `ng==1 -> 6` (neutral). Deny-lex/antonym/neg-scope/competing-subject still win (they return first).

## Seed verification
- S1 "Humans have exactly five senses." / "we actually have between 22 and 33 senses" -> **2 numeric-mismatch** (was 0 neutral)
- S2 "Goldfish have a three-second memory." / "goldfish have a spatial memory of at least six months" -> **2 numeric-mismatch** (was 1 endorse)
- Everest/Wikipedia -> **1 endorse** (unchanged); Everest/Mauna Kea -> **2 competing-subject** (unchanged)

## reg382 regression: 15 changed rows (diff | wc -l on '>' lines = 15), all -> 2 numeric-mismatch
- P2S-0-2 / P2H-0-2 (0 neutral -> 2): claim 100 degC boiling; evidence "32 degrees Fahrenheit" (freezing point). Different temperature figure; guard is quantity-blind.
- P2S-0-5 / P2H-0-5 (0 neutral -> 2): claim 100; evidence "14,000/15,000 times" (expansion ratio, unrelated quantity).
- P2S-0-0 / P2H-0-0 (1 endorse -> 2): claim 100; evidence "water boil at 212 degrees at sea level" (Quizlet). 212 degF == 100 degC semantically, but temperature-scale conversion is outside the frozen unit table -> treated as contradiction. Known limitation.
- P2S-3-3 / P2H-3-3 (1 endorse -> 2): claim "23 pairs of chromosomes"; evidence "four pairs" (fruit fly), "12" (rice plant). Other species' counts read as contradiction; guard is quantity-blind. Known limitation.
- P2S-4-0 / P2H-4-0 line 43/211 (0 neutral -> 2): claim "8 planets"; evidence title "Solar System 101" (course-number idiom 101 != 8).
- P2S-4-2 / P2H-4-2 (1 endorse -> 2): claim "8 planets"; evidence lists Mercury..Neptune "and then the possible Planet Nine" (nine != 8). Genuine contrastive catch.
- P2H-1-4 (1 endorse -> 2): claim "299,792,458 meters per second"; evidence "3 x 10^8 m/s ... 3600 seconds in an hour, 24 hours in a day". Scientific-notation approximation not expanded; 3/10/8 != claim. Known limitation.
- P2S-10-2 / P2H-10-2 (0 neutral -> 2): claim "5G ..." (number 5); evidence is a DOI URL "10.1080/19368623.2020.1788231" (numbers 10/1080/19368623/2020/1788231, no 5).

## Curated-18
`2,2,0,1,0,2,1,1,2,1,2,0,0,2,1,0,1,1` — exact match, all three runs.

## Determinism (3x reg382)
`69a0c5b93fd6a04eb91a3ba590a2ae4674a62e88edd75748fc0f0875c7cd7759` byte-identical on all three runs (run_1/2/3.txt).

## Notes / known limitations (kept minimal per brief)
- Guard is quantity-blind by design: any comparable-class numeric mismatch flips, even for unrelated quantities (expansion ratios, sub-counts, DOI numbers).
- No temperature-scale conversion (212 degF vs 100 degC reads as contradiction); no scientific-notation expansion ("3 x 10^8"); no approximate matching (exact integer compare only).
- Pronominal "one" excluded after this/that/these/those/each/every/any (protects CUR-10 "This one fruit..." -> stays 1 endorse).

---

# B2 ROUND-2 FIX REPORT — constrained numeric guard (contrastive fixer)

## Problem (round 1)
The numeric guard over-denied: 15 false DENYs on reg382, every one adjudicated
wrong. All were quantity-blind / unit-blind / entity-blind / name-blind hits.

## Changes (same file, `r12_con.zag`, rebuilt with pinned znc `--no-zagd`)
All changes are inside the numeric-guard block; the deny scans, endorse path,
and clause machinery are untouched.

1. **Unit-aware temperature (constraint 1).** New unit class 2 = temperature,
   canonical tenth-degree C. Parses `celsius/centigrade/fahrenheit/kelvin`,
   bare `degrees` + scale peek (`100 degrees Celsius`), `°C/°F/°K`, and
   compact suffixes `100C/212F/100°C/32°F` (parsed *before* the identifier
   filter, which otherwise reads the bare C as an identifier letter).
   Bare `degrees` with no scale tries both C and F readings at compare time.
   Unit mismatch (temp vs unitless/time) abstains via the existing
   not-comparable path (forces NEUTRAL on the endorse path, never DENY).
2. **Same-quantity gate (constraint 2).** Claim phenomenon class from
   boil-words vs freeze-words (`boil/boiling` vs
   `freeze/frozen/ice/melt/...`); evidence numbers in a ±60B window with the
   conflicting phenomenon and none of the claim's are skipped. Plus a
   quantity-noun hash for unitless entries (new 5th arena; trailing-`s`
   stripped, 1-letter nouns count as unmarked): a marked evidence noun
   differing from the claim's marked noun is a different quantity and is
   skipped (`10 percent` vs `twenty-thousandth decimal place`).
3. **Same-entity gate (constraint 3).** Claim entity class (human-words);
   evidence numbers whose *nearest* entity marker within ±60B is
   animal/plant are skipped (`four pairs` -> fruit fly, `12` -> rice plant).
4. **Name/identifier filter (constraint 4).** Skipped: digit runs with letters
   in the space-delimited token (`5G`, `COVID-19`); DOI/URL tokens
   (slash+dot or 2+ slashes); course numbers (small int after two capitalized
   words *followed by a title separator* `| ( : -` or end-of-text —
   the separator lookahead keeps title-case `Only Use 10 Percent` intact);
   capitalized number-words adjacent to a capitalized word (`Planet Nine`).
5. **Approximation tolerance (constraint 5).** New flags arena (bit0 =
   approximate). Scientific notation `N x 10^E` / `N × 10^E` / `N \times 10^E`
   is expanded (counts as approximate); approx words
   (`approximately/about/around/roughly/nearly/almost/circa/≈`) in the 30B
   before the number set the flag. Approximate comparisons use a 5% band
   (`3 x 10^8` ~= 299,792,458 -> no contradiction).
6. **Complement filter.** Evidence numbers preceded within 25B by
   `other/another/remaining` are complements, not competing values
   (`the other 90 percent` vs claim `10 percent`).

## Verification (all with the rebuilt `r12_con` binary)
- Seeds: S1 -> `2 numeric-mismatch`, S2 -> `2 numeric-mismatch`,
  Everest/Wikipedia -> `1 endorse`, Everest/Mauna Kea -> `2 competing-subject`.
- Curated-18 (reg382 rows 365-382): `2,2,0,1,0,2,1,1,2,1,2,0,0,2,1,0,1,1` exact.
- reg382 vs `hellhole/r12_v3` baseline output: **0 diffs** (382/382 identical).
  All 15 round-1 false DENYs return to baseline tags: lines 3,171 -> 0 neutral;
  6,174 -> 0 neutral; 7,175 -> 1 endorse (212F=100C via conversion);
  34,202 -> 1 endorse (entity gate); 43,211 -> 0 neutral (`101` filtered);
  51,219 -> 1 endorse (`Planet Nine` filtered); 99,267 -> 0 neutral
  (`5G`/`COVID-19`/DOI filtered); 191 -> 1 endorse (sci-notation + 5%).
- Determinism: 3x reg382 runs byte-identical
  (`c1bcfacfa00c20e8e7edaec337aa4792c27a6ccf8dc777111a861dcf0dfe65a7`).

## Residual limitations
- Bare `degrees` tries C and F only (not K); ambiguous-scale matches are
  lenient by design (abstain-from-deny direction).
- Quantity-noun matching is unitless-only; genuinely cross-unit genuine
  contradictions (feet vs meters) abstain rather than convert.
- Complement/entity/phenomenon word lists are small and English-specific.

# B2 ROUND-3 FIX REPORT — contrastive fixer, real-row failures (hell-hole V4)

## Failures (found testing the REAL v3 seed rows, not simplifications)
- F1: V3-07-q0-r1 ("Humans have exactly five senses." / "Humans have five primary senses: ...") went 1->0. Root cause: the numbers agree (5=5) but the quantity-noun hash reads the adjective "primary" ("five primary senses") as a different quantity, so the guard abstained (old ng=1), and abstain vetoed the endorse path to NEUTRAL.
- F2: V3-07-q0-r2 ("...just five senses. But modern neuroscience tells us that we actually have between 22 and 33 senses.") stayed 1 AFFIRM. Root cause: the guard saw the conceded "five" match the claim and stopped, never weighing the asserted "22 to 33".

## Changes (same file, `r12_con.zag`, rebuilt with pinned znc `--no-zagd`)
1. **Abstain is pass-through (F1).** `numeric_guard` contract is now binary: 2 = genuine detected mismatch (DENY veto), 0 = everything else (match, no numbers, or abstention). The old ng=1 force-NEUTRAL is gone; `r12_classify` drops the `ng==1 -> neutral` branch. The guard only ever VETOES; an abstain never vetoes an endorse. New helpers: `cmp_entry()` (factored compare: 0 not-comparable / 1 match / 2 contradict -- byte-identical logic to the old inline loop).
2. **Concession rule (F2).** New `scan_ev_text()`: per evidence text, find the earliest whole-word pivot (`find_pivot`: but/however/actually/now/"tells us"); if the pre-pivot part carries a concession marker (`has_marker`: just / "learned that" / "traditional answer" / "used to think") AND the claim's number (pre-scan match via `cmp_entry`) AND the post-pivot part carries a different comparable number, only the asserted post-pivot part is scanned -- the asserted number wins. Marker/pivot/value checks run on a lowercased copy; `ev_scan` always sees original-case slices (capitalization filters need it; `lower_copy` is length-preserving so positions align). Scratch arenas (320B) reused for the pre/post pattern scans.

## Verification (installed `r12_con` binary, real rows)
- V3-07-q0-r0->2, q0-r1->1, q0-r2->2, q1-r3->2; V3-05-q0-r2->2; A2 C01->2, C13->2. Seeds: S1->2 numeric-mismatch, S2->2 numeric-mismatch, E1->1 endorse, E2->2 competing-subject, C12->2 competing-subject.
- V3-07-q0-r3 stays 1 endorse -- DOCUMENTED, not flipped: "dozens" is an indefinite quantifier, not a cardinal; the word-number table (one..thirty) covers exact cardinals only, so the guard cannot quantify it. The pre-pivot "five senses" (Aristotle clause) is a genuine value match and carries no listed concession marker, so no concession drop fires either. Flipping it would need a fabricated dozens->N mapping plus a broader concession rule -- both rejected as unjustified.
- reg382 vs `hellhole/reg382_tags.txt`: **0 diffs** (382/382). Curated-18 (lines 365-382): `2,2,0,1,0,2,1,1,2,1,2,0,0,2,1,0,1,1` exact.
- Full ev_r12 (72 rows) old-vs-new: 3 changed rows -- the 2 intended fixes plus V3-01-q0-r3 0->1, which is JUSTIFIED by the F1 directive: the evidence ("two upper and two lower chambers") genuinely affirms the claim ("four chambers"); the old abstain was vetoing a legitimate endorse, the same pathology as F1.
- Adversarial probes: boil-vs-freeze ("...but it freezes at 0") stays 1 endorse (phenomenon gate intact); marker with no pivot, and marker+pivot with no asserted number, both stay 1 endorse (no trigger-happy drops).
- Determinism: 3x reg382 byte-identical (`c1bcfacfa00c20e8e7edaec337aa4792c27a6ccf8dc777111a861dcf0dfe65a7` -- same bytes as round-2, consistent with 0 diffs).
- Pure Zag, zero RNG. No commit (per brief).
