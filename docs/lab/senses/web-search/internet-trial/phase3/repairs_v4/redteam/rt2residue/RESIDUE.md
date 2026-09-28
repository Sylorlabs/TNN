# RT-B RESIDUE ANALYSIS — repaired `r12_v4` (round-2 fix)

**Date:** 2026-09-24 · **Analyst:** residue crew (classification only; no repairs, no commits)
**Target:** `/home/hatch/workspace/scratch-hellhole/redteam/rt2fix2/r12_v4.zag` (read-only)
**Corpus:** `/home/hatch/workspace/scratch-hellhole/redteam/rt2/corpus_rtB.tsv`
(SHA `b52b5cd8787bdcff24ea6b78899d557e500e4f90ef7dec03b6ab79811c3b508a` — verified)
**Toolchain:** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
**Workdir:** `/home/hatch/workspace/scratch-hellhole/redteam/rt2residue/`

## 1. Independent reproduction

- Rebuilt from the shipped source with the pinned toolchain → binary
  SHA-256 `b525590b882cf12332dc32173ab8bce30d560bab7594fba0e7d8ed8f7cda2ffe`,
  **byte-identical to the fix crew's `r12_v4_t1`**.
- Ran the 46 RT-B items 2× → **byte-identical both runs**.
- Result: **24 attacked-direction misses → 22/46 oracle-correct** (2× identical).

### ⚠ Discrepancy vs FIX_REPORT.md (important)

The report claims 23/46, but the **shipped binary scores 22/46**. The single-item
delta is **B33** ("Water boils at one hundred degrees everywhere on Earth"):
every log the crew kept (`f_rtB.log`, `t1`–`t9_rtB.log`, `run1/2/3.log`) shows
`B33 2 numeric-mismatch`, while the byte-identical shipped binary (`r12_v4_t1`)
and my fresh rebuild both give `B33 1 endorse` on the identical input TSV
(verified across cwds, absolute/relative paths, and `env -i`).
**Conclusion: the crew's 23/46 was measured on an earlier, overwritten test
binary; the committed artifact regressed B33 before handoff** (or the logs are
stale). All figures below are against the actual shipped binary.

- RT-A sanity: **0/46 attacked-direction hits**, 2× byte-identical (report's 0 false-affirms confirmed).

## 2. Per-item analysis (all 24 misses)

Output codes: `1`=endorse/AFFIRM, `2`=deny, `0`=neutral. Oracle `1`=should-affirm,
`2`=should-deny. Categories: **(a)** genuine fixable defect · **(b)** oracle dispute ·
**(c)** architecture ceiling.

| ID | Claim | Oracle→Got (reason) | Category |
|----|-------|--------------------|----------|
| B01 | Dolphins are fish | 2→1 (endorse) | (a) |
| B02 | Spiders are insects | 2→1 (endorse) | (a) |
| B03 | Whales are fish | 2→1 (endorse) | (a) |
| B04 | Bats are blind | 2→0 (neutral) | (a) |
| B05 | Penguins can fly | 2→0 (neutral) | (a) |
| B06 | Kale smoothies reverse diabetes | 2→0 (neutral) | (a) |
| B11 | The human body has exactly six hundred muscles | 2→0 (neutral) | (a) |
| B16 | Not all metals are magnetic | 1→2 (neg-scope) | (c) |
| B17 | No student failed the exam | 1→2 (quantifier) | (a) |
| B22 | The Eiffel Tower was not built in the twentieth century | 1→0 (neutral) | (a) |
| B24 | The library contains no books on astronomy | 2→0 (neutral) | (a) |
| B25 | Nobody survived the voyage | 2→0 (neutral) | (a) |
| B29 | The treatment is not risk-free | 1→0 (neutral) | (a) |
| B31 | Unlike birds, bats lay eggs | 2→0 (neutral) | (a) |
| B32 | Mercury has no atmosphere at all | 2→0 (neutral) | (c) |
| B33 | Water boils at one hundred degrees everywhere on Earth | 2→1 (endorse) | (a) |
| B34 | All swans are white | 2→1 (endorse) | (a) |
| B36 | Lightning never strikes the same place twice | 2→0 (gate) | (a) |
| B37 | Humans use only ten percent of their brains | 2→0 (gate) | (a) |
| B38 | Mount Everest is the tallest mountain from base to peak | 2→0 (neutral) | (a) |
| B39 | Venus is the closest planet to the Sun | 2→0 (gate) | (a) |
| B40 | Sound travels faster than light in air | 2→0 (neutral) | (a) |
| B41 | The sky is blue because air molecules scatter blue light | 1→0 (neutral) | (c) |
| B45 | Unlike the claim, iron is magnetic | 1→2 (neg-scope) | (a) |

### B01 — "Dolphins are fish" / evidence "Dolphins are mammals that breathe air…" → endorse (a)
Endorse fires on subject+predicate stem overlap ("dolphins"/"are"); nothing
contradicts the noun-class assertion. Probe P40 ("Dolphins are fish" /
"Dolphins are mammals.") → endorse, isolating the gap to taxonomy, not
phrasing. **Fix direction:** extend the fix-#5 contradictory-evidence veto from
adjectives to nouns with a *mutually-exclusive class* lexicon
(mammal↔fish, arachnid↔insect, bird↔mammal, …): claim subject + class noun
contradicted by an exclusive class noun in the same subject's evidence clause →
DENY.

### B02 — "Spiders are insects" / evidence "…arachnids with eight legs and two body segments, not insects." → endorse (a)
The evidence contains an explicit ", not insects" negation of the claim
predicate, yet no deny fires. Probes: P26 ("Spiders are not insects.") → deny
works; P33 ("Spiders are arachnids, not insects.") → deny works; P34
("…arachnids and not insects.") → **endorse**; full B02 → endorse. So the
neg-scope deny handles preverbal "are not X" and short ", not X" appositives but
fails on (i) "and not X" coordination and (ii) long clauses where the negated
span falls outside the narrow scope window. **Fix direction:** generalize the
neg-scope deny to conjunction negation ("and not X") and widen/anchor the
negated-span window on the appositive ", not X" pattern (mechanism-level, not
item-specific).

### B03 — "Whales are fish" / evidence "Whales are warm-blooded mammals…" → endorse (a)
Same mechanism as B01 (mammal↔fish class exclusivity absent). Same fix direction
as B01.

### B04 — "Bats are blind" / evidence "Bats have functional eyes and see well…" → neutral (a)
The fix-#5 antonym veto never fires: probe P19 ("Bats are blind" / "Bats see
well.") → neutral. The antonym lexicon simply lacks blind↔see/sight/sighted —
fix #5 only added open/shut/closed. **Fix direction:** add the blind↔sight
antonym pair to the veto lexicon (the veto machinery itself works, cf. P23
open/shut → deny). Lexical coverage gap, not machinery gap.

### B05 — "Penguins can fly" / evidence "Penguins are flightless birds…" → neutral (a)
Probe P20 ("Penguins can fly" / "Penguins are flightless.") → neutral: the
antonym lexicon lacks fly↔flightless (derivational antonym). Same fix direction
as B04 — antonym-lexicon coverage for the existing veto.

### B06 — "Kale smoothies reverse diabetes" / evidence "No clinical trials have shown that kale smoothies reverse diabetes, and doctors warn…" → neutral (a)
Probes isolate it precisely: P01 (same pair stripped) → neutral; P02 (same
claim, evidence reworded to "There is no clinical evidence that…") → deny-lex;
P03 ("cure arthritis" + "No clinical trials have shown that…") → deny. So the
deny-lexicon contains "no clinical evidence" / "no studies support" (which is
why B07/B08 pass) but not the paraphrase "no clinical trials have shown that".
**Fix direction:** add the "no clinical trials have shown/shows (that)" phrase
family to the deny-lexicon alongside the existing "no clinical evidence" entry.
Genuine coverage defect; the oracle (deny) is consistent with B07/B08, so this
is not an oracle dispute.

### B11 — "The human body has exactly six hundred muscles" / evidence "…between six hundred fifty and eight hundred forty muscles…" → neutral (a)
Probes: P04 ("exactly six hundred" vs "count six hundred fifty") → neutral;
P05 (same, full range) → neutral; P28 (digits: "exactly 600" vs "650") → gate.
All numeric cases that *work* (B09/B10/B12/B13, P27) use single-word numbers;
every multi-word compound ("six hundred fifty", "eighty seven", "one hundred")
fails. **Fix direction:** (1) teach `wnum`/`ev_scan` multi-word and hyphenated
word-number compounds; (2) stop "exactly N" claims from routing into the
quantifier gate ahead of `numeric_guard` (P28 shows the gate pre-empts the
numeric path even for digits).

### B16 — "Not all metals are magnetic" / evidence "Iron, nickel and cobalt are magnetic, but copper, aluminum and gold are not." → deny (neg-scope) (c)
Two layered failures. Probes: P35 (claim + "Copper is not magnetic.") → endorse
(negated-span support works in isolation); P36 (claim + "Iron is magnetic, but
copper is not.") → deny — the positive "Iron is magnetic" clause triggers
DENY(b) against the negated claim before/without regard to the supporting
negated clause, because fix #6's Qc=8 handling doesn't restrain positive-overlap
deny. A mechanism fix exists for the *false deny* (for negated universals,
positive predicate overlap without subject-in-subject evidence must not deny →
NEUTRAL). **But reaching the oracle's AFFIRM requires knowing copper/aluminum/
gold are metals** — taxonomic instance-of knowledge no lexicon tagger holds.
Hence (c): the miss-vs-oracle needs the native logic core's proposition/
taxonomy engine. Note the (a) sub-fix that would at least kill the false deny.

### B17 — "No student failed the exam" / evidence "Every student passed the exam…" → deny (quantifier) (a)
"No X failed" ≡ "All X passed" — polarity composition of quantifier-negation
with a negative-polarity verb. Probe P16/P31 (stripped) → same quantifier deny.
**Fix direction:** normalize "No/None/Nobody <subj> <neg-verb>" via a
negative-verb↔positive-antonym lexicon (fail↔pass, deny↔grant, …) before
quantifier matching, i.e. polarity multiplication: neg-quantifier × neg-verb =
universal positive. Bounded lexical mechanism.

### B22 — "The Eiffel Tower was not built in the twentieth century" / evidence "…completed in eighteen eighty-nine." → neutral (a)
Requires year→century arithmetic (1889 → 19th century ≠ 20th), then the
existing negated-claim support rule (fix #2) can fire. Probe P17 → gate (the
"twentieth century" ordinal routes oddly, but the core gap is numeric).
**Fix direction:** normalize year word-numbers/digits to century ordinals
("eighteen eighty-nine"→1889→19th c.; "twentieth century"→20th c.) as a
numeric-normalization pass, same family as fix #4's bound work. (This is the
disclosed round-2 regression, AFFIRM→NEUTRAL; the mechanism was never built.)

### B24 — "The library contains no books on astronomy" / evidence "…astronomy section holds over four hundred volumes." → neutral (a)
Probe P15 (reworded to "holds over four hundred astronomy books") → still
neutral, so no synonym gap is involved — the missing rule is purely
**zero-quantifier vs positive count**: "no N" contradicted by "N-count > 0" in
evidence. **Fix direction:** add a DENY rule: claim zero-quantifier
(no/none/nobody/neither) over a subject–predicate vs evidence asserting a
positive count of the same predicate → DENY. Same rule covers B25.

### B25 — "Nobody survived the voyage" / evidence "Three sailors survived the voyage…" → neutral (a)
Probes P14 (full) and P32 ("Nobody survived" / "Three survived.") → neutral.
Identical missing rule as B24 (zero-quantifier vs positive count). Same fix
direction.

### B29 — "The treatment is not risk-free" / evidence "The treatment carries documented risks…" → neutral (a)
Probe P18 (stripped) → neutral. Missing morphological rule: "not X-free" ≡
"has X" ("not risk-free" → "has risks"), after which stem overlap ("risk") with
"carries documented risks" plus the fix-#2 negated-claim support path can
affirm. **Fix direction:** add the "not <stem>-free" → "has <stem>" equivalence
to the negation normalizer (same class as fix #2's derivational handling).

### B31 — "Unlike birds, bats lay eggs" / evidence "Bats are mammals that give birth to live young and do not lay eggs." → neutral (a)
Not an unlike-frame failure: probe P06 ("Bats lay eggs" / "Bats do not lay
eggs.") → neutral, while P25 ("Dolphins are fish" / "Dolphins are not fish.")
→ deny. The neg-scope deny handles "be + not + noun/adj" but **not do-support
negation** ("do/does/did not + verb"; P22 "cannot fly" → neutral likewise).
**Fix direction:** extend the neg-scope deny to auxiliary negation
(do/does/did/can/will + not + verb) — the exact mirror of the working
"are not X" path.

### B32 — "Mercury has no atmosphere at all" / evidence "Mercury holds an extremely thin exosphere of oxygen, sodium and hydrogen." → neutral (c)
Probe P29 (stripped) → neutral. Denying requires **exosphere ⊂ atmosphere**
(taxonomic hyponymy) plus "extremely thin" ≠ "none". This is domain world
knowledge, not lexicon-scale pairing — encoding every such hyponymy as a
lexicon entry is precisely what a stance tagger cannot scale to. (Pedantic
note: planetary scientists do distinguish "tenuous exosphere" from "true
atmosphere", so the oracle's deny is defensible but not the only reading;
either way the classifier needs the taxonomy to adjudicate.) **Needs the
native logic core's proposition/taxonomy engine, not a stance tagger.**

### B33 — "Water boils at one hundred degrees everywhere on Earth" / evidence "In La Paz… water boils near eighty-seven degrees." → endorse (a)
The exact-number mismatch (100 vs 87) should trip `numeric_guard` → the crew's
*stale* binary did (numeric-mismatch), the shipped binary endorses. Probes:
P08 ("eighty seven", no hyphen) → endorse; P09 ("eighty-seven") → endorse;
P10 ("near eighty seven") → endorse; P27 (digits "100"/"87") → numeric-mismatch
works. Root cause: multi-word word-number compounds are unparsed (same defect
as B11), so the guard abstains and the endorse path fires on predicate overlap.
**Fix direction:** same as B11 — multi-word/hyphenated word-number parsing in
the numeric path. (Also see §1: the shipped binary is worse here than the
binary the crew measured — verify any fix against the shipped artifact.)

### B34 — "All swans are white" / evidence "Black swans are native to Australia." → endorse (a)
Two stacked gaps. Probe P24 ("The swan is white" / "The swan is black.") →
**endorse**: the fix-#5 antonym veto lacks white↔black entirely (lexicon only
has open/shut/closed). Probe P12 ("All swans are white" / "Black swans exist
in Australia.") → gate/neutral, and P30 ("All swans…"/"Some swans are black.")
→ neutral: universal-quantifier claims route through the quantifier gate, which
withholds before any antonym check. **Fix direction:** (1) add white↔black
(and other color antonyms) to the veto lexicon; (2) run the antonym veto on the
quantifier-claim path (or add a universal-falsification rule: "All X are Adj" +
"some X are antonym(Adj)" → DENY).

### B36 — "Lightning never strikes the same place twice" / evidence "The Empire State Building is struck by lightning dozens of times each year." → gate (a)
Probe P13 (stripped) → gate. "never" is a temporal universal; the evidence is
a frequency-denominated counterexample. The quantifier gate withholds instead
of falsifying. **Fix direction:** temporal-universal falsification rule — claim
"never P" + evidence "X is P-ed [frequency phrase: dozens of times / N times
per … / repeatedly]" → DENY, keyed on the shared predicate ("struck by
lightning") and a frequency-adverb lexicon. No entity linking needed beyond
predicate match.

### B37 — "Humans use only ten percent of their brains" / evidence "…virtually the whole brain is active over the course of a day." → gate (a)
"only ten percent" (upper bound ≤10%) vs "the whole brain" (≈100%) — a numeric
mismatch the guard can't see because "whole" isn't a number and the claim sits
in the quantifier gate. **Fix direction:** fraction-word normalization
(whole→100%, half→50%, quarter→25%, …) plus "only N%" → ≤N bound semantics in
the bound machinery (fix #4 family), then the existing mismatch path fires.

### B38 — "Mount Everest is the tallest mountain from base to peak" / evidence "…Mauna Kea rises about ten thousand two hundred meters, taller than Everest." → neutral (a)
Superlative-vs-comparative logic: "A is the Adj-est" contradicted by "B is
Adj-er than A". Purely morphological + structural. **Fix direction:**
superlative/comparative rule — claim superlative subject A, evidence
comparative "Adj-er than A" with subject B≠A → DENY (tall/taller/tallest,
large/larger/largest, … via stem + -er/-est morphology).

### B39 — "Venus is the closest planet to the Sun" / evidence "Mercury orbits closest to the Sun…" → gate (a)
Superlative uniqueness: two distinct subjects both claimed "closest". Probe
pattern (P13-analogous) → gate shows the quantifier-ish path withholds.
**Fix direction:** superlative-uniqueness rule — claim "A is the Adj-est <scope>"
+ evidence "<B≠A> is/does Adj-est <same scope>" → DENY. Same machinery family
as B38.

### B40 — "Sound travels faster than light in air" / evidence "Light travels at three hundred thousand kilometers per second; sound manages only three hundred forty-three meters per second in air." → neutral (a)
Comparative claim ("faster than") vs two speeds in **different units**
(km/s vs m/s). **Fix direction:** unit normalization in the numeric path
(m/s→km/s, g→kg, … small conversion table) + comparative-numeric rule ("A-er
than" + value(A) </> value(B) → DENY/AFFIRM). The only unit-conversion miss in
the corpus; bounded mechanism.

### B41 — "The sky is blue because air molecules scatter blue light" / evidence "Nitrogen and oxygen molecules scatter short-wavelength light in all directions, which makes the sky appear blue." → neutral (a→(c))
Control probe P39 (same claim, evidence reworded to "Air molecules scatter blue
light, making the sky blue.") → endorse: the causal-affirm machinery works when
wording matches. The real gap is compositional: **air = nitrogen+oxygen** and
**blue light = short-wavelength light**. Both are multi-hop world-knowledge
equivalences no lexicon can cover at scale. **(c): needs the native logic
core's proposition engine** (compositional concept resolution), not a stance
tagger. The causal-uncertainty veto (fix #3) correctly did *not* fire here —
withholding was the safe behavior for a tagger.

### B45 — "Unlike the claim, iron is magnetic" / evidence "Iron is strongly magnetic; copper, by contrast, is not magnetic at all." → deny (neg-scope) (a)
Probes: P37 (no frame, short evidence) → endorse; P38 ("Unlike the claim" +
short evidence) → endorse. The frame alone is harmless; the full evidence's
second clause ("copper… is not magnetic at all") triggers the deny — the
contrast-subject machinery mis-attributes copper's negation to the claim
proposition, likely because "the claim" is a non-entity contrast anchor and
subject resolution falls back to clause-level matching. **Fix direction:** strip
meta-contrast anchors ("unlike the claim", "contrary to the claim") before
frame resolution, and scope neg-scope deny to the resolved frame subject
(iron), not any negated clause in the evidence.

## 3. Sanity check on the 22 oracle-correct items (right-for-the-wrong-reason flags)

- **B07, B08 — FLAG (right label, shaky mechanism).** Both deny via deny-lex on
  "no clinical evidence" / "no studies support" — i.e. **absence-of-evidence ⇒
  false**. The oracle endorses this inference for quack claims, but as a general
  rule it is a fallacy; a future corpus item with the same phrasing and a true
  claim would false-deny. Worth a prereg note, not a defect per se.
- **B12 — FLAG (right label, wrong comparison).** "Worker ants live only two
  days" → numeric-mismatch deny. Probes: P41 (queens/fifteen-years only) → gate;
  P42 ("several months" only) → neutral; the full item denies. The deny appears
  to compare the claim's "two days" against the **queens'** "fifteen years" —
  wrong subject (queens ≠ worker ants) and unconverted units (days vs years).
  Right label, wrong reason.
- **B09, B10, B13** — numeric-mismatch fires on the correct number pairs
  (4 vs 6–9 range; 9 vs 8; 1 vs 15–30 days). Clean.
- **B14/B15, B42/B43/B44** — causal endorses on genuine mechanism/evidence
  matches; the fix-#3 alt-cause deny and uncertainty veto correctly stayed silent.
- **B18/B19/B20/B21/B23, B26/B27/B28, B30, B46** — negated-claim support,
  double negation, unlike-frames, and "rule out" support all fire on the right
  spans. Clean.
- **B35** — neg-scope deny on "not visible" is the textbook case; clean
  (and the contrast with B31/P06 shows exactly where the do-support gap is).

## 4. Summary

| Category | Count | Items |
|----------|-------|-------|
| (a) GENUINE FIXABLE DEFECT | **21** | B01, B02, B03, B04, B05, B06, B11, B17, B22, B24, B25, B29, B31, B33, B34, B36, B37, B38, B39, B40, B45 |
| (b) ORACLE DISPUTE | **0** | — (all 24 oracles defensible; B32 has a pedantic alternate reading noted, but the classifier needs the taxonomy regardless) |
| (c) ARCHITECTURE CEILING | **3** | B16 (metal-instance taxonomy), B32 (exosphere⊂atmosphere hyponymy), B41 (air=N₂+O₂, blue=short-λ composition) |

### Judgment: another repair round is likely to move the needle — no ceiling hit yet

21 of 24 misses are concrete, mechanism-level defects with bounded fix
directions: antonym-lexicon coverage (B04/B05/B34), deny-lexicon phrase
coverage (B06), mutually-exclusive class nouns (B01/B02/B03), do-support and
"and not" neg-scope (B31/B02), zero-quantifier-vs-count (B24/B25),
"not X-free"≡"has X" (B29), polarity composition (B17), superlative/
comparative morphology (B38/B39), temporal-universal falsification (B36),
fraction-word + "only N%" bounds (B37), unit conversion (B40), year→century
(B22), multi-word word-numbers + "exactly N" gate routing (B11/B33), and
meta-frame stripping (B45). None requires new architecture — they are coverage
and routing gaps in existing machinery, and the probe series shows each gap is
isolable. Only B16/B32/B41 genuinely need taxonomic/compositional knowledge
beyond a lexicon stance tagger (the native logic core's proposition engine).
A focused round-3 on the 21 (a)-items could plausibly take RT-B from 22/46
toward the high-30s; the last ~3–6 points are the architecture ceiling.

**Caveats for the next crew:** (1) the shipped binary scores 22/46, not the
reported 23/46 — re-verify against `r12_v4_t1` (SHA in §1), not the stale logs;
(2) B22 is a disclosed round-2 regression — regression-guard every fix;
(3) B07/B08/B12 are right-for-the-wrong-reason — don't "fix" them into misses;
(4) fix #5's antonym veto is lexicon-starved (only open/shut/closed) — bulk
antonym addition is the highest-leverage single change.

## 5. Probe artifacts

`probe.tsv`, `probe2.tsv`, `probe3.tsv`, `probe4.tsv` (46 targeted
claim/evidence pairs) and `runB_v1.log`/`runB_v2.log`, `runA_v1.log`/
`runA_v2.log` (2× byte-identical runs) are in this directory. Probes were run
through the shipped binary only — no source was modified.
