# A4 MISTAG REPORT — hell-hole V4 extra-families hunt (crew A4)

Binary: `/home/hatch/workspace/scratch-hellhole/hellhole/r12_v3` (frozen)
Source studied: `/home/hatch/workspace/scratch-hellhole/hellhole/r12_v3.zag` (990 lines)
Work dir: `/home/hatch/workspace/scratch-hellhole/crews/a4/`
Date: 2026-09-23. No fixes applied (hunt only).

## Method (per corpus, identical for all five)

1. I hand-authored each corpus row as `idx \t claim \t title \t snippet \t oracle_tag`
   and assigned `oracle_tag` **by my own reading of the claim/snippet pair alone**,
   using the entailment rules stated in the subtype tables below.
2. Oracles were frozen in the corpus files **before the classifier was executed once**.
3. After freezing, I projected columns 1–4 to `in_<fam>.tsv`, ran the frozen binary
   3× per corpus, verified the 3 outputs byte-identical (SHA-256), then scored
   run 1 against the frozen oracles.
4. **No oracle was revised after seeing classifier output.** Two rows surprised me
   (C7 passes via the 3-char-verb blind spot; T6 "passes" via a spurious
   competing-subject DENY) — both are documented below as wrong-reason outcomes,
   oracles untouched.

## Frozen corpora

| corpus file | rows | SHA-256 |
|---|---|---|
| `corpus_cond.tsv` | 13 | `d546f07f05fae74f8967518d00c83603667be0c8e820b93d6b62504c899ef154` |
| `corpus_qnt.tsv` | 12 | `9be8e691e67a913a07a6bb19e0341fbd54195afca2901cb50d3326e3b283ff5a` |
| `corpus_hedge.tsv` | 12 | `2f77be04a336719477b4c7cb1f1d9d69091b44f11d3d18fa10ef25dd38f31b56` |
| `corpus_tmp.tsv` | 12 | `b4c191792347b732ca4341cfa873717d29a93b75e813aa12662a5043282fbb07` |
| `corpus_cmp.tsv` | 10 | `e37f674f34a20d1c01d2db47f19a606b574467f73dc8c26faf7ba7c76c03bb3b` |

## Determinism: 3 runs byte-identical per corpus

| output file (run1 = run2 = run3) | SHA-256 |
|---|---|
| `out_cond_run{1,2,3}.txt` | `9d221dfc306ad933c3beb673bd5a165b3fcbb29b550cb8446157f140a277520c` |
| `out_qnt_run{1,2,3}.txt` | `5f034aefd8ae1524a1c4f9a9df69a55525099b6ddb24092e5d704f309cec7772` |
| `out_hedge_run{1,2,3}.txt` | `c6646ebbcc3a343d4890e4b823bc25ad7855b91d0837476ba9d159d3b7fb51c8` |
| `out_tmp_run{1,2,3}.txt` | `a100f9d4207f17f20db7eafa9773f73095312d7fd4adb2519458804f24d4f0d9` |
| `out_cmp_run{1,2,3}.txt` | `9ff3311ba6fdf4cc5162e31244ebd2a480e6d472c1892cac294a723c7f4e2743` |

## Headline accuracies

| family | file | correct | accuracy |
|---|---|---|---|
| conditionals | `corpus_cond.tsv` | 6/13 | 46.2% |
| quantifiers | `corpus_qnt.tsv` | 4/12 | 33.3% |
| hedging | `corpus_hedge.tsv` | 1/12 | 8.3% |
| temporal order | `corpus_tmp.tsv` | 3/12 | 25.0% |
| comparatives (5th family) | `corpus_cmp.tsv` | 1/10 | 10.0% |
| **total** | | **15/59** | **25.4%** |

---

## 1. Conditionals — 6/13 (46.2%)

Oracle rule: bare "If X, Y" / "Y if X" / counterfactual evidence asserts only the
conditional → NEUTRAL on the factual claim; conditional + satisfied antecedent in
the same snippet → AFFIRM; conditional + negated consequent → DENY.

| subtype | rows | correct |
|---|---|---|
| bare "If X then Y" (NEUTRAL oracle) | C1, C3, C6, C9 | 0/4 |
| trailing "Y if X" (NEUTRAL oracle) | C7 | 1/1* |
| counterfactual "would have" (NEUTRAL oracle) | C5 | 0/1 |
| subjunctive "would … if" (NEUTRAL oracle) | C10 | 0/1 |
| conditional + satisfied antecedent (AFFIRM oracle) | C2, C4, C8, C11 | 3/4 |
| concessive "whether or not" (AFFIRM oracle) | C12 | 1/1 |
| conditional + negated consequent (DENY oracle) | C13 | 1/1 |

\* C7 passes for the wrong reason (see mechanism M3).

Mistags:
- C1 `Water boils at 100C.` / `If water reaches 100C it boils.` → oracle NEUTRAL, pred AFFIRM (endorse)
- C3 `Smoke causes cancer.` / `If people smoke, it causes cancer.` → NEUTRAL → AFFIRM (endorse)
- C5 `The tower was struck by lightning.` / `If the storm had come, lightning would have struck the tower.` → NEUTRAL → AFFIRM (endorse)
- C6 `Lightning strikes the tower.` / `If a storm comes, lightning will strike the tower.` → NEUTRAL → AFFIRM (endorse)
- C8 `Birds use tools.` / `Birds use tools; sticks were available to the crows.` → oracle AFFIRM, pred NEUTRAL (neutral)
- C9 `Honey cures coughs.` / `If honey is taken, it cures coughs.` → NEUTRAL → AFFIRM (endorse)
- C10 `Water boils at 100C.` / `Water would boil at 100C if heated.` → NEUTRAL → AFFIRM (endorse)

## 2. Quantifiers — 4/12 (33.3%)

Oracle rule: standard first-order reading. "Some X are not Y" contradicts "All X
are Y" → DENY; "One X is Y" contradicts "No X are Y" → DENY; "Some X are Y" does
not entail "All X are Y" → NEUTRAL; "All X are Y" entails "Some X are Y" → AFFIRM;
bare plurals read generically.

| subtype | rows | correct |
|---|---|---|
| all vs some-not (DENY oracle) | Q1, Q7 | 0/2 |
| no vs one-is (DENY oracle) | Q2, Q6 | 0/2 |
| most vs most-not (DENY oracle) | Q3 | 0/1 |
| bare plural vs some-not (DENY oracle) | Q8 | 0/1 |
| few vs most (DENY oracle) | Q10 | 0/1 |
| all-claim vs some-evidence (NEUTRAL oracle) | Q5 | 0/1 |
| some-claim vs all-evidence (AFFIRM oracle) | Q4 | 1/1 |
| bare-claim vs all-evidence (AFFIRM oracle) | Q9 | 1/1 |
| many-claim vs no-evidence (DENY oracle) | Q11 | 1/1 |
| some-claim vs no-evidence (DENY oracle) | Q12 | 1/1 |

Mistags:
- Q1 `All cats are indoors.` / `Some cats are not indoors.` → DENY → AFFIRM (endorse)
- Q2 `No cats are indoors.` / `One cat is indoors.` → DENY → AFFIRM (endorse)
- Q3 `Most cats are indoors.` / `Most cats are not indoors.` → DENY → AFFIRM (endorse)
- Q5 `All cats are indoors.` / `Some cats are indoors.` → NEUTRAL → AFFIRM (endorse)
- Q6 `No birds use tools.` / `One bird uses tools.` → DENY → NEUTRAL (neutral)
- Q7 `All dogs are loud.` / `Some dogs are not loud.` → DENY → AFFIRM (endorse)
- Q8 `Cats are indoors.` / `Some cats are not indoors.` → DENY → AFFIRM (endorse)
- Q10 `Few cats are indoors.` / `Most cats are indoors.` → DENY → AFFIRM (endorse)

Note: Q11/Q12 pass only because the evidence-initial "No" lands within 4 tokens
*before* the predicate, tripping neg-scope — positional luck, not quantifier logic.

## 3. Hedging — 1/12 (8.3%)

Oracle rule: hedged evidence ("may/might/could/suggests/possibly/appears/seems/is
thought to/believe") is not endorsement → NEUTRAL; hedged denial ("may not be X")
is not a denial → NEUTRAL; the unhedged twin → AFFIRM.

| subtype | rows | correct |
|---|---|---|
| modal hedge may/might/could (NEUTRAL oracle) | H1, H2, H3 | 0/3 |
| lexical hedge suggests/possibly/appears/seems/is-thought-to/believe (NEUTRAL) | H4, H5, H6, H7, H8, H12 | 0/6 |
| hedged denial (NEUTRAL oracle) | H9, H11 | 0/2 |
| unhedged control (AFFIRM oracle) | H10 | 1/1 |

Mistags:
- H1 `Coffee cures colds.` / `Coffee may cure colds.` → NEUTRAL → AFFIRM (endorse)
- H2 … / `Coffee might cure colds.` → NEUTRAL → AFFIRM (endorse)
- H3 … / `Coffee could cure colds.` → NEUTRAL → AFFIRM (endorse)
- H4 … / `A study suggests coffee cures colds.` → NEUTRAL → AFFIRM (endorse)
- H5 … / `Coffee possibly cures colds.` → NEUTRAL → AFFIRM (endorse)
- H6 … / `Coffee appears to cure colds.` → NEUTRAL → AFFIRM (endorse)
- H7 … / `Coffee seems to cure colds.` → NEUTRAL → AFFIRM (endorse)
- H8 … / `Coffee is thought to cure colds.` → NEUTRAL → AFFIRM (endorse)
- H9 … / `Coffee may not cure colds.` → NEUTRAL → DENY (neg-scope)
- H11 `Coffee does not cure colds.` / `Coffee may not cure colds.` → NEUTRAL → DENY (neg-scope)
- H12 `Coffee cures colds.` / `Researchers believe coffee cures colds.` → NEUTRAL → AFFIRM (endorse)

## 4. Temporal order — 3/12 (25.0%)

Oracle rule: swapped before/after with same entities → DENY; same order → AFFIRM;
co-occurrence with no order stated → NEUTRAL; date pairs evaluated arithmetically
(1990 < 1995 ⇒ flood-before-drought true; 1985 < 1990 ⇒ false).

| subtype | rows | correct |
|---|---|---|
| before/after swap (DENY oracle) | T1, T7, T8, T9 | 0/4 |
| identical order (AFFIRM oracle) | T2 | 1/1 |
| co-occurrence, no order (NEUTRAL oracle) | T3, T11 | 0/2 |
| date arithmetic (AFFIRM / DENY oracle) | T4, T5 | 1/2 |
| 3-event chain swap (DENY oracle) | T10 | 0/1 |
| date mismatch on claim date (DENY oracle) | T12 | 0/1 |
| before/after swap, pronoun subject (DENY oracle) | T6 | 1/1* |

\* T6 is a correct tag via a **wrong reason** (see mechanism M7): pred DENY
(competing-subject), triggered spuriously by the capitalized pronoun "She".

Mistags:
- T1 `The flood was before the drought.` / `The flood was after the drought.` → DENY → AFFIRM (endorse)
- T3 … / `The flood was bad and the drought was worse.` → NEUTRAL → AFFIRM (endorse)
- T5 `The flood was in 1990, before the drought.` / `The drought was in 1985 and the flood was in 1990.` → DENY → AFFIRM (endorse)
- T7 `The meeting was before lunch.` / `The meeting was after lunch.` → DENY → AFFIRM (endorse)
- T8 `The drought was after the flood.` / `The drought was before the flood.` → DENY → AFFIRM (endorse)
- T9 `The flood was before the drought.` / `The drought was before the flood.` → DENY → AFFIRM (endorse)
- T10 `The quake was before the flood, which was before the fire.` / `The quake was before the fire, which was before the flood.` → DENY → AFFIRM (endorse)
- T11 `Dawn was before noon.` / `Dawn was early and noon was late.` → NEUTRAL → AFFIRM (endorse)
- T12 `The flood was in 1990, before the drought.` / `The flood was in 2001, before the drought.` → DENY → AFFIRM (endorse)

## 5. Comparatives (fifth family — discovered during the hunt) — 1/10 (10.0%)

Rationale for adding: while building the temporal corpus I noticed the antonym
gate in `scan_text` only handles the hardcoded `flat/spherical` pair; gradable
antonyms (faster/slower, bigger/smaller, more/fewer) are distinct stems that sail
through the overlap gate into `endorse`. Oracle rule: swapping a gradable
comparative for its antonym, or swapping the compared entities, contradicts the
claim → DENY; identical → AFFIRM.

| subtype | rows | correct |
|---|---|---|
| gradable-antonym swap (DENY oracle) | P1, P3, P4, P5, P6, P7 | 0/6 |
| entity role swap (DENY oracle) | P8, P10 | 0/2 |
| more/fewer swap (DENY oracle) | P9 | 0/1 |
| identical (AFFIRM oracle) | P2 | 1/1 |

Mistags (all oracle DENY → pred AFFIRM (endorse)):
- P1 `The cheetah is faster than the lion.` / `The cheetah is slower than the lion.`
- P3 `The whale is bigger than the shark.` / `The whale is smaller than the shark.`
- P4 `The mountain is taller than the hill.` / `The mountain is shorter than the hill.`
- P5 `Steel is hotter than copper.` / `Steel is colder than copper.`
- P6 `Mary is older than John.` / `Mary is younger than John.`
- P7 `The lion is slower than the cheetah.` / `The lion is faster than the cheetah.`
- P8 `The cheetah is faster than the lion.` / `The lion is faster than the cheetah.`
- P9 `The box has more apples than the bag.` / `The box has fewer apples than the bag.`
- P10 `The box has more apples than the bag.` / `The bag has more apples than the box.`

---

## Mechanism diagnoses (all cite `r12_v3.zag`)

**M1 — No conditional / modality representation (C1, C3, C5, C6, C9, C10).**
The AFFIRM rule in `scan_text` ("AFFIRM: positive endorsement evidence only")
requires only: `nclm>=need`, anchor present, `ns==0`, not interrogative, not
framed, `comp==0`. There is no conditional lexicon and no hedge lexicon anywhere
in the source. Worse, `if` is in both `lex_stop` and `lex_conjskip`, so the
conditional marker is actively erased before scoring. Any "If X then Y" sentence
sharing ≥2 claim stems endorses the bare claim.

**M2 — Negation scope is pre-predicate only (Q1, Q3, Q7, Q8).**
`neg_scope()` checks only the 4 tokens *before* the predicate index `pi`.
Post-copula negation ("are not indoors") sits *after* `pi` and is invisible, so
"Some cats are not indoors" endorses "All cats are indoors". The 4-token window
is positional, not syntactic.

**M3 — 3-code-point content-word drop (C7, C8, Q6; also Q5, Q10).**
`r12_classify` keeps only claim tokens with `z_cplen(tok)>3`. "use", "all",
"few" are dropped. Consequences: (a) if the claim's only verb is 3 chars
("use"), `pred` falls back to be/have or `""`; with `pred=""`, `pi` is never
found and AFFIRM is unreachable — C8's satisfied-antecedent AFFIRM degrades to
NEUTRAL, and Q6's DENY degrades to NEUTRAL; (b) the quantifiers "all"/"few"
vanish, so "All cats…"/"Few cats…" are scored as bare "Cats…". (C7 passes as
NEUTRAL only because of (a), not because the trailing conditional was
understood.)

**M4 — Claim-side "no"/"not" erased as stopwords (Q2, Q6, H11).**
`lex_stop` contains `no` and `not`, so the claim's own universal negation is
dropped from content words: "No cats are indoors" ≡ "Cats are indoors" to the
classifier, and "Coffee does not cure colds" ≡ "Coffee cures colds". The
classifier cannot represent a negated claim at all.

**M5 — Quantifiers are stems or nothing (Q1–Q12, Q5, Q10).**
"some"/"most"/"many" (len ≥4, not stopwords) are kept as *ordinary content
stems* — "some" can even become the `firstA` anchor — with zero quantifier
logic: no all/some entailment direction (Q5 over-affirms), no contradiction
between "all" and "some-not" (Q1). Combined with M3/M4, quantifier words are
either dropped ("all", "few", "no") or inert ("some", "most").

**M6 — Temporal order invisible (T1, T3, T5, T7–T12).**
`before`/`after` are both in `lex_stop` → dropped from claim content words; no
order representation exists anywhere in the pipeline. Same-entity before/after
swaps, 3-event chain swaps, and date contradictions all reduce to entity
co-occurrence → `endorse`. T3/T11 show the residual M1b shape: bare
co-occurrence ("The flood was bad and the drought was worse") endorses an order
claim. Numbers ("1990") survive as content words but are compared by stem
identity, never arithmetically (T5, T12).

**M7 — T6: right tag, wrong reason (flag, oracle unchanged).**
T6 `She was here before noon.` / `She was here after noon.` scores DENY via
`competing-subject`, not via order understanding: `competitor()` treats the
capitalized pronoun "She" as a competing proper noun because "she" was
stopword-dropped from the claim's stem set (`in_stems` fails), satisfying the
`comp==1` + `pred=="be"` + anchor-present conditions. A differently-cased or
unpronouned variant would AFFIRM.

**M8 — Hedged denial over-denies (H9, H11).**
`neg_scope` fires on "not" in "may not cure" (within 4 tokens before `pi`) →
DENY (neg-scope), but a hedged denial is NEUTRAL, not a denial. There is no
distinction between "not" under a modal and bare "not".

**M9 — Gradable antonyms unhandled (P1, P3–P10).**
The DENY-(d) antonym gate in `scan_text` hardcodes exactly one pair
(`flat`↔`spherical`/`sphere`/`round`/`globe`/`oblate`). "faster"/"slower",
"bigger"/"smaller", "hotter"/"colder", "more"/"fewer" are distinct stems that
pass the overlap gate (need counts only the shared stems) → `endorse`. Entity
role swaps (P8, P10) likewise reduce to bag-of-stems overlap.

## Cross-family pattern

44 of 59 rows mistagged (74.6%). The dominant failure is **over-affirmation on
stem overlap**: 38 of 44 mistags are oracle NEUTRAL/DENY → pred AFFIRM
(endorse). The R1 repair ("no fallthrough-to-AFFIRM; AFFIRM requires positive
endorsement") narrowed *what counts* as endorsement to predicate-level
assertion, but the endorsement test is still bag-of-stems + positional
negation — it cannot see conditionals, hedging/modality, quantifier scope,
temporal order, or gradable antonymy. The four hunted families plus
comparatives are all instances of one underlying gap: **the classifier has no
representation of logical/grammatical operators** (if, not-after-copula,
all/some/no, before/after, -er/than antonyms); they are stopword-dropped or
stem-inert, leaving bare entity overlap to drive `endorse`.

## Files

- Corpora (5-col, frozen oracles): `corpus_cond.tsv`, `corpus_qnt.tsv`, `corpus_hedge.tsv`, `corpus_tmp.tsv`, `corpus_cmp.tsv`
- Classifier inputs (4-col projections): `in_cond.tsv`, `in_qnt.tsv`, `in_hedge.tsv`, `in_tmp.tsv`, `in_cmp.tsv`
- Raw outputs (3 runs each, byte-identical): `out_<fam>_run{1,2,3}.txt`
- Build/score scripts: `write_corpora.py`, `score.py`
- This report: `MISTAG_REPORT.md`
