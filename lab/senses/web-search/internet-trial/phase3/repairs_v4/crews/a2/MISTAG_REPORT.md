# A2 MISTAG REPORT — contrastive/comparative hunt vs frozen r12_v3

Crew: A2 (CONTRASTIVE/COMPARATIVE HUNTER), hell-hole V4 campaign.
Classifier: `/home/hatch/workspace/scratch-hellhole/hellhole/r12_v3` (frozen).
Corpus: `/home/hatch/workspace/scratch-hellhole/crews/a2/corpus_con.tsv`
SHA-256: `bf9e61a26ee9b652966d2ead17bf8888380a4870a8d5d8319e5dd3610d7e905d`
Runs: 3× byte-identical (`run_1.txt`/`run_2.txt`/`run_3.txt`, sha `7af02240d58507d9f9493f6d7b8736467d76d9712c7abdba3f3348912a163982`).

## Method (oracle-before-output)

All 50 rows were hand-authored with `oracle_tag` fixed from my own reading
BEFORE the classifier was ever run on the corpus. After scoring, oracle tags
were NOT changed. 7 of my 50 hand-predictions of classifier behavior were
wrong (C01, C02, C11, C19, C22, C26, C33); each was resolved by re-reading
the source (`competitor()`, gate `need`, capitalization paths) — oracle
values were left untouched throughout. The corpus is frozen: any future
re-run scores against the SHA above.

## Corpus composition (50 rows, ≥3 per subtype)

| Subtype | Rows | Oracle mix |
|---|---|---|
| range vs exact number | C01–C03 | 3× DENY (C01, C13 are the two required seeds: senses, goldfish) |
| "more than X" vs "exactly X" | C04–C06 | 3× DENY |
| "less than X" | C07–C09 | 3× DENY |
| "at least X" / "at most X" | C10–C13 | 4× DENY |
| differing quantities, same units (+unit conversion) | C14–C18 | 5× DENY |
| superlatives of a different entity | C19–C23 | 4× DENY, 1× AFFIRM |
| X-vs-Y comparatives | C24–C27 | 3× DENY, 1× AFFIRM |
| "whereas/while" contrasts | C28–C31 | 3× DENY, 1× AFFIRM |
| "unlike X, Y …" contrasts | C32–C36 | 2× DENY, 2× NEUTRAL, 1× AFFIRM |
| "not X but Y" value contrasts | C37–C40 | 3× DENY, 1× AFFIRM |
| affirm controls (same value) | C41–C44 | 4× AFFIRM |
| neutral controls (unrelated aspect) | C45–C47 | 3× NEUTRAL |
| deny-mechanism positives | C48–C50 | 3× DENY |

## Score: 13/50 correct (0.26). 37 mistags.

### Per-subtype accuracy

| Subtype | n | correct | mistag | acc | mistag outcomes |
|---|---|---|---|---|---|
| range vs exact | 3 | 0 | 3 | 0.00 | 2 NEUTRAL, 1 AFFIRM |
| more than vs exactly | 3 | 0 | 3 | 0.00 | 3 AFFIRM |
| less than | 3 | 0 | 3 | 0.00 | 2 AFFIRM, 1 NEUTRAL |
| at least / at most | 4 | 0 | 4 | 0.00 | 2 AFFIRM, 2 NEUTRAL |
| differing quantities | 5 | 0 | 5 | 0.00 | 5 NEUTRAL |
| superlatives | 5 | 1 | 4 | 0.20 | 3 AFFIRM, 1 NEUTRAL |
| X-vs-Y comparatives | 4 | 0 | 4 | 0.00 | 2 AFFIRM, 2 NEUTRAL |
| whereas / while | 4 | 1 | 3 | 0.25 | 1 AFFIRM, 2 NEUTRAL |
| unlike | 5 | 3 | 2 | 0.60 | 2 AFFIRM |
| not X but Y | 4 | 1 | 3 | 0.25 | 2 AFFIRM, 1 NEUTRAL |
| affirm controls | 4 | 3 | 1 | 0.75 | 1 NEUTRAL |
| neutral controls | 3 | 1 | 2 | 0.33 | 2 AFFIRM |
| deny-mechanism positives | 3 | 3 | 0 | 1.00 | — |

### Full mistag list (idx, oracle → got, reason)

- C01 2→0 neutral — range vs exact (seed a)
- C02 2→0 neutral — range vs exact
- C03 2→1 endorse — range vs exact
- C04 2→1 endorse — more than vs exactly
- C05 2→1 endorse — more than vs exactly
- C06 2→1 endorse — more than vs exactly
- C07 2→1 endorse — less than
- C08 2→1 endorse — less than
- C09 2→0 neutral — less than
- C10 2→1 endorse — at most
- C11 2→0 neutral — at least
- C12 2→0 neutral — at most
- C13 2→1 endorse — at least (seed b; reproduces V3-07)
- C14 2→0 neutral — differing quantities
- C15 2→0 neutral — differing quantities
- C16 2→0 gate — differing quantities (unit conversion)
- C17 2→0 neutral — differing quantities (unit conversion)
- C18 2→0 neutral — differing quantities
- C19 2→1 endorse — superlative, different entity
- C20 2→1 endorse — superlative, different entity
- C21 2→1 endorse — superlative, different entity
- C22 2→0 neutral — superlative, different entity
- C24 2→1 endorse — X-vs-Y comparative
- C25 2→1 endorse — X-vs-Y comparative
- C26 2→0 neutral — X-vs-Y comparative
- C27 1→0 neutral — X-vs-Y comparative (AFFIRM control mistagged)
- C28 2→0 neutral — whereas
- C29 2→1 endorse — while
- C30 2→0 neutral — whereas
- C32 2→1 endorse — unlike
- C33 2→1 endorse — unlike
- C37 2→1 endorse — not X but Y
- C38 2→0 neutral — not X but Y
- C39 2→1 endorse — not X but Y
- C44 1→0 neutral — AFFIRM control ("stands" not recognized)
- C45 0→1 endorse — NEUTRAL control (aspect confusion)
- C47 0→1 endorse — NEUTRAL control (aspect confusion)

Correct: C23, C31, C36, C40, C41, C42, C43 (endorse); C34, C35, C46 (neutral);
C48 (deny-lex), C49 (neg-scope), C50 (antonym).

## Mechanism diagnosis (citing classifier functions)

### 1. The endorse path has no value check at all (19 AFFIRM mistags)

`scan_text()`'s AFFIRM branch requires `nclm>=need`, anchor, `ns==0`,
not-interrogative, not-framed, `comp==0`. That is pure topic overlap plus an
un-negated predicate match. `has_claim_value()` — the ONLY numeric guard —
is called exclusively inside the competing-subject DENY branch; the endorse
path never consults it. So "exactly 300" vs "more than 300" (C04),
"exactly 22" vs "less than 22" (C07), "at most 40,000" vs "exactly 50,000"
(C10), "at least six months" vs "three-second" (C13), reversed comparatives
(C24, C25), and "not five but seven" (C37) all AFFIRM: the claim's stems
co-occur with a predicate, and nothing compares the values. This is the R1
failure from the V3 trial, reproduced systematically: **19 of 50 rows**.

### 2. `has_claim_value()` is digit-only and deny-branch-only

`claim_numbers()` extracts `\d[\d,]*` runs; word-numbers ("five", "seven",
"three", "ten") are invisible, so `nnums==0` → guard returns 0 and can never
fire (C01, C13, C14, C15, C17, C18, C37–C40). Even where digits exist, the
guard is a comma/space-stripped *substring* test with no range, bound, or
unit semantics: "between 22 and 33" vs claim "five" cannot be compared by
design. No unit conversion exists anywhere ("three hours" vs "120 minutes",
C16; "seven pounds" vs "3,000 grams", C17).

### 3. `competitor()` fires on the wrong things and `deny-4` almost never fires

The competing-subject DENY (reason 4) fired **zero times** in 50 rows. It
requires `comp==1 && nclm>=1 && firstA-in-clause && (pred=="be" ||
superlative) && !interrog && has_claim_value==0`. Failure modes observed:

- (a) Genuine superlative refutations don't mention the claim's subject, so
  the `firstA`-in-clause requirement blocks the deny: C22 ("The Amazon is
  the longest river…") → competitor detected ("Amazon" capitalized) but
  deny-4 blocked → NEUTRAL (oracle DENY).
- (b) The `pred=="be"` requirement blocks non-copular refutations: C26
  ("Tea has more caffeine than coffee") → `competitor()` fired on
  capitalized "Tea", AFFIRM vetoed, but pred is "have" → no deny → NEUTRAL.
- (c) `competitor()` is capitalization-gated (≥3 chars immediate, ≥4
  far-field): lowercase genuine competitors are invisible → AFFIRM mistags
  (C19 "colossal squid", C21 "pronghorn", C24 "giraffes", C25 "lions";
  verified: capitalizing "Colossal" flips C19's analog to NEUTRAL).
- (d) `competitor()` treats capitalized SHORT claim words as competitors:
  the claim-stem set only contains words with `z_cplen>3`, so "Tea" (in the
  claim, 3 chars) and "There"/"K2" count as foreign entities. C26's "Tea"
  vetoed a correct AFFIRM-path and, via (b), produced NEUTRAL; C11's
  sentence-initial "There" vetoed AFFIRM → NEUTRAL. Lowercase "tea" gives
  the (wrong) AFFIRM — the tag flips on capitalization alone.

Net effect of the competitor machinery: it converts some would-be AFFIRM
mistags into NEUTRAL mistags (C01, C11, C22, C26) — still wrong (oracle
DENY), just quieter — and never once produces the DENY it was built for.

### 4. Predicate-coverage gaps → NEUTRAL mistags (no-predicate = no verdict)

Every deny/affirm rule below the lexicon checks requires `pi>=0` (a
predicate match). Refutations phrased with verbs outside `lex_verb` or
without a copula are unscored: "place" (C02), "weighs" (C12, C14),
"lasts" (C15), "arrived" (C38), "helped"→"help" (C28), "migrate" (C30),
"finished" vs pred "took" (C16, psyn table has no took↔finish). The whole
"differing quantities" subtype (0/5) died here. This also mistags AFFIRM
controls: C44 ("stands" not a `psyn` of "be") and C27 ("contains" not a
`psyn` of "have") → NEUTRAL.

### 5. `neg_scope()` only looks BACKWARD

Negation must occur within 4 tokens *before* the predicate. "not X but Y"
places "not" after the copula ("is not five but seven", C37; "was not red
but green", C39) → `ns==0` → AFFIRM mistag. The construction is invisible to
every deny branch (deny-lex has no "not…but" pattern).

### 6. Contrast markers are absent from all lexicons

"whereas", "while" (contrastive), "unlike", "between", "more/less than",
"at least/most" appear in no lexicon (`lex_strong`, `lex_weak`,
`lex_conjskip` — which has "while" but only uses it to *exempt* tokens in
the far-field competitor scan). C29 is the sharpest case: "lowers blood
pressure in men, while in women it raises it" AFFIRMs because the first
conjunct endorses and the "while"-clause is never segmented (clause
splitting is only on `[.!?;—]`, never commas) or weighed.

### 7. Short-claim gate (`need=1` when `nw<3`)

C33 ("The restaurant is excellent.", oracle DENY): 2 content words → `need=1`
→ title "Restaurant review" alone satisfies the overlap gate → AFFIRM on a
refutation. C32 similar. Short claims are one shared word away from
endorsement.

### 8. Endorse-on-different-aspect (NEUTRAL→AFFIRM)

C45 ("was completed in 1889" matches be-predicate → AFFIRM on a height
claim), C47 ("have eight senses" → AFFIRM on a no-bones claim). Predicate
match ≠ proposition match — the R1 gap in its pure form.

### 9. What works

All three deny mechanisms fire correctly on their home turf: deny-lex
(C48 "The myth says…", via the ana rule), neg-scope (C49 "does not
contain", negation before predicate), antonym (C50 flat↔oblate). The
classifier's deny side is a set of narrow tripwires; contrastive refutation
— the common case in retrieval — trips none of them.

## Severity read

- 37/50 mistag (0.26 accuracy). Every contrastive subtype scores ≤0.25
  except "unlike" (0.60, and both mistags were AFFIRM false-installs).
- Of the 37 mistags, 19 are AFFIRM (false installs — the dangerous
  direction) and 18 are NEUTRAL (missed refutations).
- The two V3 seeds reproduce: C01 (senses) → NEUTRAL, C13 (goldfish) →
  AFFIRM.

## Files

- Corpus (frozen): `corpus_con.tsv` (50 rows, SHA-256
  `bf9e61a26ee9b652966d2ead17bf8888380a4870a8d5d8319e5dd3610d7e905d`)
- Classifier input projection: `corpus_con_input.tsv`
- Determinism: `run_1.txt`, `run_2.txt`, `run_3.txt` — byte-identical,
  sha256 `7af02240d58507d9f9493f6d7b8736467d76d9712c7abdba3f3348912a163982`
- SHA record: `corpus_con.sha256`
- This report: `MISTAG_REPORT.md`

No fixes attempted (per task). No commits made.
