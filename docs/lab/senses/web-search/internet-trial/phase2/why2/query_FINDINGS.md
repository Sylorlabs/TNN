# Crew QUERY findings — affirm-seeking query bias (mechanism 2)

Hell-hole internet trial, frozen commit `83d62d8fa52223fd083a3a0f782114df2fe0de4c`
(sylorlabs/TNN, branch `tnn-native-lab`). Frozen evidence only; no web re-runs.

## 0. Method and verification

- Envelope -> candidate mapping: `session.htsv` `QUERY_ISSUED` events carry
  `seq`/`cand`/`query`/`followup`. The `cand` index -> candidate ID map is the
  frozen "curiosity order" `IDX2ID` in `phase2/supervisor/ht_score.py`:
  `0:C1, 1:C2, 2:C3, 3:C4, 4:C14, 5:C5, 6:C6, 7:C7, 8:C8, 9:C9, 10:C10, 11:C11,
  12:C12, 13:C13, 14:C15, 15:C16, 16:A1, 17:A2, 18:A3`.
  (A naive claims-then-audits ordering is WRONG here; the session's order was
  verified against the frozen scorer and against query content.)
- Every envelope's stored `query` was cross-checked against the session's
  `seq`-th `QUERY_ISSUED` query: **0 mismatches** in both arms (28 solo, 30 helper).
  Query counts match `score.json` (`n_queries` 28 / 30).
- Stance tallies below come from the frozen ledger `CLAIM_EXTRACTED` events
  (stance codes per task: 0=IRRELEVANT, 1=AFFIRM, 2=DENY), joined to result sets
  by ledger order (seq-scoped, not domain-scoped, so repeated domains across
  queries are attributed correctly).
- All analysis scripts were run twice; outputs byte-identical. No RNG, no
  timestamps in outputs, sorted iteration. Scripts (read-only):
  `~/workspace/tmp_commit/extract_queries.py`, `classify.py`, `install_detail.py`.

## 1. Rubric (frozen before classification — reproduced verbatim)

**Rubric Q-CLASS v1 (frozen 2026-09-22, crew QUERY).** Each query string is
classified by its literal wording, in this order:

1. **DISCONFIRMATION-SEEKING** — the wording asks for counter-evidence,
   debunking, or falsification: contains (case-insensitive) any of `debunk`,
   `myth`, `hoax`, `false`, `no evidence`, `fact check`, `fact-check`, `refut`,
   `scam`, `not true`.
2. **NEUTRAL** — an open question or balanced comparison that does not
   presuppose the claim's truth: (a) led by an interrogative
   (`is/are/was/were/do/does/did/how/what/when/where/which/who/why/can/could/
   would/will/should`, or an `at what`-style interrogative phrase) with no
   bare asserted answer and no declarative assertion of the candidate claim;
   or (b) explicitly names competing sides/answers (`X vs Y`, or lists rival
   answers such as Everest/Mauna Kea, Sahara/Antarctica).
3. **AFFIRM-SEEKING** — otherwise: the query asserts the candidate claim
   (declaratively, or by repeating its loaded/marketing phrasing) and/or
   solicits supporting material (`evidence`, `proof`, `study`,
   `systematic review`, `latest evidence`, or `claim` used as "the <X> claim"
   framing). Includes interrogative-led queries that embed a bare presupposed
   answer token (e.g. `how many planets in the solar system 8`).

Documented edge calls (applied uniformly, noted in the table discussion):
- `at what temperature does water boil at sea level systematic review` /
  `... latest evidence` stay NEUTRAL: interrogative-led, no assertion; the
  solicitation noun attaches to an open question.
- `eating eggs cholesterol dangerous current guidance` is AFFIRM-SEEKING:
  not interrogative-led; the fragment asserts `dangerous` (borderline — the
  `current guidance` tail is open, but the framing presupposes danger).
- `do humans only use 10 percent of their brains myth` is
  DISCONFIRMATION-SEEKING via the `myth` token (the single D-class query; the
  binary copied it verbatim from the frozen baseline, it generated none itself).

## 2. Full 58-query classification table

Class codes: AFFIRM = AFFIRM-SEEKING, NEUTRAL, DISCONF = DISCONFIRMATION-SEEKING.
`fu` = followup flag from the ledger. Drift = first-query phrasing vs the frozen
baseline in `fixtures/course.json` (see section 4).
| arm | seq | cand | fu | class | query | frozen baseline | drift |
|---|---|---|---|---|---|---|---|
| solo | 0 | C1 | 0 | NEUTRAL | at what temperature does water boil at sea level | at what temperature does water boil at sea level | none |
| solo | 1 | C1 | 1 | NEUTRAL | at what temperature does water boil at sea level systematic review | at what temperature does water boil at sea level | none |
| solo | 2 | C1 | 1 | NEUTRAL | at what temperature does water boil at sea level latest evidence | at what temperature does water boil at sea level | none |
| solo | 3 | C2 | 0 | NEUTRAL | what is the speed of light in meters per second | speed of light exact value metres per second | lateral (keyword->interrogative) |
| solo | 4 | C3 | 0 | NEUTRAL | does the earth orbit the sun | does the earth orbit the sun | none |
| solo | 5 | C4 | 0 | NEUTRAL | how many pairs of chromosomes do humans have | how many pairs of chromosomes do humans have | none |
| solo | 6 | C14 | 0 | AFFIRM | how many planets in the solar system 8 | covid-19 origin lab leak vs natural origin evidence | TOWARD-AFFIRM |
| solo | 7 | C14 | 1 | AFFIRM | how many planets in the solar system 8 systematic review | covid-19 origin lab leak vs natural origin evidence | TOWARD-AFFIRM |
| solo | 8 | C14 | 1 | AFFIRM | how many planets in the solar system 8 latest evidence | covid-19 origin lab leak vs natural origin evidence | TOWARD-AFFIRM |
| solo | 9 | C5 | 0 | AFFIRM | COVID-19 originated from a lab leak evidence | are eggs bad for cholesterol current guidance | TOWARD-AFFIRM |
| solo | 10 | C6 | 0 | AFFIRM | eating eggs cholesterol dangerous current guidance | does coffee cause cancer IARC ruling | TOWARD-AFFIRM |
| solo | 11 | C7 | 0 | AFFIRM | drinking coffee causes cancer iarc | is the earth flat evidence | TOWARD-AFFIRM |
| solo | 12 | C8 | 0 | AFFIRM | the earth is flat evidence | were the moon landings faked evidence | TOWARD-AFFIRM |
| solo | 13 | C8 | 1 | AFFIRM | the earth is flat evidence systematic review | were the moon landings faked evidence | TOWARD-AFFIRM |
| solo | 14 | C9 | 0 | AFFIRM | the apollo moon landings were faked evidence | did 5G cause covid-19 | TOWARD-AFFIRM |
| solo | 15 | C10 | 0 | AFFIRM | 5g networks caused covid-19 pandemic claim | chemtrails mind control evidence | TOWARD-AFFIRM |
| solo | 16 | C10 | 1 | AFFIRM | 5g networks caused covid-19 pandemic claim systematic review | chemtrails mind control evidence | TOWARD-AFFIRM |
| solo | 17 | C10 | 1 | AFFIRM | 5g networks caused covid-19 pandemic claim latest evidence | chemtrails mind control evidence | TOWARD-AFFIRM |
| solo | 18 | C11 | 0 | AFFIRM | chemtrails mind control program claim | tallest mountain in the world Everest Mauna Kea | none (baseline already affirm-seeking) |
| solo | 19 | C11 | 1 | AFFIRM | chemtrails mind control program claim systematic review | tallest mountain in the world Everest Mauna Kea | none (baseline already affirm-seeking) |
| solo | 20 | C11 | 1 | AFFIRM | chemtrails mind control program claim latest evidence | tallest mountain in the world Everest Mauna Kea | none (baseline already affirm-seeking) |
| solo | 21 | C12 | 0 | NEUTRAL | tallest mountain in the world mount everest mauna kea | largest desert in the world Sahara Antarctica | none |
| solo | 22 | C13 | 0 | NEUTRAL | largest desert in the world sahara antarctic | how many planets in the solar system | none |
| solo | 23 | C15 | 0 | AFFIRM | fruit dissolves blood clots doctors hate it | fruit dissolves blood clots doctors hate it | none (baseline already affirm-seeking) |
| solo | 24 | C16 | 0 | AFFIRM | chocolate cures insomnia study | study chocolate cures insomnia | none (baseline already affirm-seeking) |
| solo | 25 | A1 | 0 | NEUTRAL | is the great wall of china visible from the moon naked eye | is the great wall of china visible from the moon naked eye | none |
| solo | 26 | A2 | 0 | DISCONF | do humans only use 10 percent of their brains myth | do humans only use 10 percent of their brains myth | none |
| solo | 27 | A3 | 0 | NEUTRAL | does lightning strike the same place twice | does lightning strike the same place twice | none |
| helper | 0 | C1 | 0 | NEUTRAL | at what temperature does water boil at sea level | at what temperature does water boil at sea level | none |
| helper | 1 | C1 | 1 | NEUTRAL | at what temperature does water boil at sea level systematic review | at what temperature does water boil at sea level | none |
| helper | 2 | C1 | 1 | NEUTRAL | at what temperature does water boil at sea level latest evidence | at what temperature does water boil at sea level | none |
| helper | 3 | C2 | 0 | NEUTRAL | what is the speed of light in meters per second | speed of light exact value metres per second | lateral (keyword->interrogative) |
| helper | 4 | C3 | 0 | NEUTRAL | does the earth orbit the sun | does the earth orbit the sun | none |
| helper | 5 | C4 | 0 | NEUTRAL | how many pairs of chromosomes do humans have | how many pairs of chromosomes do humans have | none |
| helper | 6 | C14 | 0 | AFFIRM | how many planets in the solar system 8 | covid-19 origin lab leak vs natural origin evidence | TOWARD-AFFIRM |
| helper | 7 | C14 | 1 | AFFIRM | how many planets in the solar system 8 systematic review | covid-19 origin lab leak vs natural origin evidence | TOWARD-AFFIRM |
| helper | 8 | C14 | 1 | AFFIRM | how many planets in the solar system 8 latest evidence | covid-19 origin lab leak vs natural origin evidence | TOWARD-AFFIRM |
| helper | 9 | C5 | 0 | AFFIRM | COVID-19 originated from a lab leak evidence | are eggs bad for cholesterol current guidance | TOWARD-AFFIRM |
| helper | 10 | C6 | 0 | AFFIRM | eating eggs cholesterol dangerous current guidance | does coffee cause cancer IARC ruling | TOWARD-AFFIRM |
| helper | 11 | C7 | 0 | AFFIRM | drinking coffee causes cancer iarc | is the earth flat evidence | TOWARD-AFFIRM |
| helper | 12 | C8 | 0 | AFFIRM | the earth is flat evidence | were the moon landings faked evidence | TOWARD-AFFIRM |
| helper | 13 | C8 | 1 | AFFIRM | the earth is flat evidence systematic review | were the moon landings faked evidence | TOWARD-AFFIRM |
| helper | 14 | C9 | 0 | AFFIRM | the apollo moon landings were faked evidence | did 5G cause covid-19 | TOWARD-AFFIRM |
| helper | 15 | C10 | 0 | AFFIRM | 5g networks caused covid-19 pandemic claim | chemtrails mind control evidence | TOWARD-AFFIRM |
| helper | 16 | C10 | 1 | AFFIRM | 5g networks caused covid-19 pandemic claim systematic review | chemtrails mind control evidence | TOWARD-AFFIRM |
| helper | 17 | C10 | 1 | AFFIRM | 5g networks caused covid-19 pandemic claim latest evidence | chemtrails mind control evidence | TOWARD-AFFIRM |
| helper | 18 | C11 | 0 | AFFIRM | chemtrails mind control program claim | tallest mountain in the world Everest Mauna Kea | none (baseline already affirm-seeking) |
| helper | 19 | C11 | 1 | AFFIRM | chemtrails mind control program claim systematic review | tallest mountain in the world Everest Mauna Kea | none (baseline already affirm-seeking) |
| helper | 20 | C11 | 1 | AFFIRM | chemtrails mind control program claim latest evidence | tallest mountain in the world Everest Mauna Kea | none (baseline already affirm-seeking) |
| helper | 21 | C12 | 0 | NEUTRAL | tallest mountain in the world mount everest mauna kea | largest desert in the world Sahara Antarctica | none |
| helper | 22 | C13 | 0 | NEUTRAL | largest desert in the world sahara antarctic | how many planets in the solar system | none |
| helper | 23 | C15 | 0 | AFFIRM | fruit dissolves blood clots doctors hate it | fruit dissolves blood clots doctors hate it | none (baseline already affirm-seeking) |
| helper | 24 | C16 | 0 | AFFIRM | chocolate cures insomnia study | study chocolate cures insomnia | none (baseline already affirm-seeking) |
| helper | 25 | C16 | 1 | AFFIRM | chocolate cures insomnia study systematic review | study chocolate cures insomnia | none (baseline already affirm-seeking) |
| helper | 26 | C16 | 1 | AFFIRM | chocolate cures insomnia study latest evidence | study chocolate cures insomnia | none (baseline already affirm-seeking) |
| helper | 27 | A1 | 0 | NEUTRAL | is the great wall of china visible from the moon naked eye | is the great wall of china visible from the moon naked eye | none |
| helper | 28 | A2 | 0 | DISCONF | do humans only use 10 percent of their brains myth | do humans only use 10 percent of their brains myth | none |
| helper | 29 | A3 | 0 | NEUTRAL | does lightning strike the same place twice | does lightning strike the same place twice | none |


## 3. Per-arm distribution

| arm | AFFIRM-SEEKING | NEUTRAL | DISCONFIRMATION-SEEKING | total |
|---|---|---|---|---|
| solo | 17 (60.7%) | 10 (35.7%) | 1 (3.6%) | 28 |
| helper | 19 (63.3%) | 10 (33.3%) | 1 (3.3%) | 30 |

First queries only (one per candidate, 19 per arm, identical strings in both arms):
AFFIRM-SEEKING 10/19 (52.6%), NEUTRAL 8/19 (42.1%), DISCONFIRMATION-SEEKING 1/19 (5.3%).

Followups (solo 9, helper 11): 7/9 solo and 9/11 helper AFFIRM-SEEKING; the
followup template is mechanical — base query + `systematic review`, then base +
`latest evidence` — so a first query's class propagates to its followups.
The 2 NEUTRAL followups are the C1 pair (`... systematic review` /
`... latest evidence` on an open question).

The only DISCONFIRMATION-SEEKING query in either arm is A2's
`do humans only use 10 percent of their brains myth`, copied verbatim from the
frozen baseline. The deliberation binary never generated a
disconfirmation-seeking query of its own in 58 tries.

## 4. Baseline drift: deliberation phrasing vs frozen `fixtures/course.json`

The binary generated its own phrasing (it did not reuse the baseline strings;
cf. C2: baseline `speed of light exact value metres per second` vs actual
`what is the speed of light in meters per second`). Drift direction per
candidate (first query vs baseline):

**Drifted toward affirmation (7 candidates)** — the binary systematically
converted interrogative baselines into declarative assertions:
- C5: baseline `covid-19 origin lab leak vs natural origin evidence` (balanced,
  both sides named) -> actual `COVID-19 originated from a lab leak evidence`
  (the `vs natural origin` balance was dropped).
- C6: baseline `are eggs bad for cholesterol current guidance` (interrogative)
  -> actual `eating eggs cholesterol dangerous current guidance` (asserts
  `dangerous`).
- C7: baseline `does coffee cause cancer IARC ruling` -> actual
  `drinking coffee causes cancer iarc` (interrogative -> assertion; `iarc`
  kept as a bare authority token).
- C8: baseline `is the earth flat evidence` -> actual `the earth is flat
  evidence` (the `is` question framing was dropped).
- C9: baseline `were the moon landings faked evidence` -> actual `the apollo
  moon landings were faked evidence` (interrogative -> declarative).
- C10: baseline `did 5G cause covid-19` -> actual `5g networks caused covid-19
  pandemic claim` (interrogative -> declarative).
- C14: baseline `how many planets in the solar system` -> actual `how many
  planets in the solar system 8` (bare presupposed answer `8` appended).

**Baselines already affirm-seeking; binary kept the bias (3 candidates):**
- C11: baseline `chemtrails mind control evidence` -> actual `chemtrails mind
  control program claim` (lateral; both declarative + solicitation framing).
- C15: baseline `fruit dissolves blood clots doctors hate it` -> actual
  identical (verbatim spam marketing phrasing).
- C16: baseline `study chocolate cures insomnia` -> actual `chocolate cures
  insomnia study` (same words, reordered; both assert + `study`).

**Unchanged / lateral (9 candidates):** C1 (q0 identical), C2 (keyword ->
interrogative, neutral either way), C3, C4, C12, C13 (balanced phrasing kept:
`mount everest mauna kea`, `sahara antarctic`), A1, A2, A3 (all three
prior-audit baselines copied verbatim).

Pattern: of the 10 candidates whose first query was AFFIRM-SEEKING, 7 got there
by the binary's own drift (interrogative -> declarative / dropped balance /
appended answer) and 3 inherited it from an already-biased baseline. The
binary never drifted a query *away* from affirmation.

## 5. Bounded counterfactual: the K1 installs

Frozen stance tallies per install (ledger CLAIM_EXTRACTED; A=AFFIRM, D=DENY, I=IRRELEVANT).
Per-query splits are seq-scoped from ledger order. Installs per frozen
`score.json`: solo C8, C11, C15, C16; helper C8, C15.

### C8 flat earth — solo AND helper: INSTALL. Tally 7A / 1D / 4I (identical both arms).
- q12 `the earth is flat evidence`: 2A / 1D / 3I. The DENY is edu.au/Pursuit
  ("Although scientific evidence says the Earth is a sphere..."). The 2 AFFIRMs
  are vialattea.net (biblical flat-earth) and wikipedia.org `Modern flat Earth
  beliefs` (a descriptive article tagged AFFIRM — classifier co-occurrence
  artifact). livescience.com and space.com debunk content was retrieved but
  tagged IRRELEVANT.
- q13 `the earth is flat evidence systematic review`: 5A / 0D / 1I —
  tfes.org x2, flatearthdave.com, youtube `5 Real-World Flat-Earth Proofs`,
  britannica.com (descriptive article tagged AFFIRM — artifact), quora
  IRRELEVANT.
- (a) YES — a genuine DENY (edu.au) was retrieved and outvoted 7-1; two more
  debunking pages (livescience, space.com) were retrieved but tagged
  IRRELEVANT, and two descriptive encyclopedia articles were tagged AFFIRM,
  so the "majority" was part genuine conspiracy sources (3 unambiguous:
  tfes.org x2, flatearthdave.com, youtube proofs) and part classifier artifact
  (mechanism 1 compounding mechanism 2).
- (b) The followup set is strictly more one-sided than the base set (5A/0D vs
  2A/1D; the conspiracy-literature cluster appears only after `systematic
  review` is appended to the declarative assertion). This frozen contrast
  supports the "biased query manufactured corroboration" reading. What a
  disconfirmation-seeking policy could have changed: it could have surfaced
  more edu.au-type results — but whether enough to overturn a 7-1 count is
  **speculation** (the web cannot be re-run).

### C11 chemtrails — solo: INSTALL. Tally 6A / 3D / 9I.
- q18 `chemtrails mind control program claim`: 1A / 2D / 3I (DENYs: newscientist
  `77 atmospheric scientists`, bottomofthat; AFFIRM: auricmedia `Total Control`).
- q19 `... systematic review`: 2A / 1D / 3I (AFFIRMs: auricmedia, slideshare
  HAARP/mind-control doc; DENY: telegraph).
- q20 `... latest evidence`: 3A / 0D / 3I (AFFIRMs: auricmedia, wanttoknow.info,
  youtube `Gov Bill PROVES Chemtrails`).
- (a) YES — 3 genuine DENYs (newscientist, telegraph, bottomofthat) were
  retrieved and outvoted 6-3.
- (b) All three queries declaratively assert the conspiracy (`chemtrails mind
  control program claim` + solicitation nouns) and retrieved the conspiracy
  cluster (auricmedia x3, slideshare, wanttoknow.info, chemtrailplanet,
  stopworldcontrol, odysee). It is plausible the phrasing selected for this
  cluster, but without re-running, the causal claim is **speculation**; the
  frozen evidence establishes only that DENYs existed and lost the count.
- Helper arm: same 3 queries, tally 4A / 3D / 11I -> WITHHOLD (helper consults
  counted as observations; the affirm majority did not survive).

### C15 fruit dissolves blood clots — solo AND helper: INSTALL. Tally 5A / 0D / 1I (single query).
- q23 `fruit dissolves blood clots doctors hate it`: AFFIRMs are webmd.com
  `Blood Clots: How They Get Dissolved`, merckmanuals.com, brucerosemanmd.com
  (all general medical pages about clot *treatment*, tagged AFFIRM of the
  *fruit* claim — pure co-occurrence artifacts), plus 2 youtube spam videos
  that genuinely affirm (`These 7 Fruits Dissolve Blood Clots FAST - Doctors
  Are Shocked!`). 1 IRRELEVANT (discoveriesinmedicine.com). **Zero DENY
  retrieved.**
- (a) NO — there was nothing to outvote; no counter-evidence was ever
  retrieved. The 5-0 "corroboration" was 3 classifier artifacts + 2 spam
  videos.
- (b) The query is the spam's verbatim marketing phrasing, and the retrieved
  set is the spam's own ecosystem (the `Doctors Are Shocked!` videos).
  Verbatim-phrasing search plausibly caused the one-sidedness. A
  disconfirmation-seeking query (`... myth` / `fact check`) is the only policy
  that could have introduced a DENY here — but whether a debunk exists to be
  retrieved is **speculation**.

### C16 chocolate cures insomnia — solo: INSTALL (3A / 1D / 2I, single query).
- q24 `chocolate cures insomnia study`: the 3 AFFIRMs are mentalfloss.com
  `Fried Lettuce, Slug Entrails and Other Insomnia Cures` (a humor listicle),
  com.au ResMed `Insomnia Cures` (generic), youtube rain-sounds `Cure Insomnia
  in 5 Minutes` — all co-occurrence artifacts (`cure`+`insomnia`), none
  supporting chocolate-as-cure. The 1 DENY is lifehack.org `15 Natural
  Insomnia Cures`.
- (a) MARGINAL — a DENY existed and lost 3-1, but the "majority" was
  manufactured by the classifier, not by genuine corroboration. Mechanism 1
  dominates here; query bias (declarative assertion + `study`) is secondary.
- Helper arm is the informative contrast: two more followups (q25 `...
  systematic review`, q26 `... latest evidence` — still AFFIRM-SEEKING by the
  rubric) added 12 results, tally 3A / 3D / 12I -> WITHHOLD. The rescue came
  from *dilution by irrelevant results*, not from disconfirmation-seeking.
  The affirm majority was fragile either way.

### Adjacent observations (frozen evidence, mechanism-2-relevant)
- C5 (CONTESTED -> INSTALL, K2/M3 failure): first query dropped the baseline's
  `vs natural origin` balance (`COVID-19 originated from a lab leak evidence`),
  retrieved thehighwire.com (conspiracy) among 4A/0D/2I. Query-bias drift
  plausibly contributed to the contradiction-handling failure.
- C7 (FALSE -> INSTALL): query drifted affirm-seeking (`drinking coffee causes
  cancer iarc`), yet the retrieved set was *correct* (who.int, cancer.org,
  sharecare, theconversation denying) — INSTALL came from stance-classifier
  inversion (mechanism 1), not query bias. The mechanisms dissociate: query
  bias is not necessary for a false install, and a good result set does not
  save a bad classifier.
- C9/C10 (FALSE -> REJECT/WITHHOLD): affirm-seeking queries (`the apollo moon
  landings were faked evidence`, `5g networks caused covid-19 pandemic claim`
  + followups) did NOT produce installs — C9 tally 2A/3D/1I, C10 tally
  1A/4D/13I. Affirm-seeking phrasing does not deterministically manufacture
  corroboration; it biases the draw.

## 6. M6 — the "own line of inquiry" (first 3 solo queries)

score.json `M6_first3_queries`: seq 0-2, all candidate C1 (water boils at
100C), queries `at what temperature does water boil at sea level`,
`... systematic review`, `... latest evidence` — all NEUTRAL under the rubric.

Characterization: topical-but-timid. The binary spent its entire followup
budget (2 followups, the maximum seen on any candidate) re-asking the most
settled fact on the 19-candidate course, with `systematic review` / `latest
evidence` appendages, rather than probing or moving on — and C1 still ended
WITHHOLD (over-conservatism on settled facts, mechanism 4 in the phase-2
report; the helper arm WITHHELD too despite helper affirmation). No
affirm-seeking wording appears in the three queries, but neither does any
disconfirmation-seeking: across all 58 queries the binary generated zero of
its own. The "own line" was diligent in form (followups, reviews, latest
evidence) and empty in adversarial content.

## 7. Bottom line

1. **The bias is real and mostly self-inflicted.** 60.7% solo / 63.3% helper
   of queries were AFFIRM-SEEKING; 10 of 19 first queries (52.6%). In 7 of 16
   claims the binary *created* the bias itself by rewriting interrogative
   baselines as declarative assertions (dropping `is`, dropping `vs natural
   origin`, appending a presupposed `8`); 3 more inherited it from
   already-biased baselines (C11/C15/C16). It never drifted a query away from
   affirmation and never generated a disconfirmation-seeking query.
2. **Outvoted DENYs are documented, not hypothetical.** C8: 1 genuine DENY lost
   7-1 (plus 2 debunk pages mistagged IRRELEVANT). C11 solo: 3 genuine DENYs
   lost 6-3. C16 solo: 1 DENY lost 3-1 to artifact AFFIRMs. Only C15 had no
   DENY retrieved at all (5-0 on artifacts + spam videos).
3. **Query bias is load-bearing but not sufficient alone.** The C8 followup
   contrast (2A/1D/3I -> 5A/0D/1I after appending `systematic review`) is the
   cleanest frozen evidence that phrasing manufactured corroboration; C9/C10
   show affirm-seeking queries do not always do so; C7 shows a false install
   with a *correct* result set (classifier inversion did the work); C15/C16
   show "majorities" built substantially from classifier artifacts. Any fix
   must pair disconfirmation-seeking queries with source-authority weighting
   and a negation-capable stance classifier — query reform alone would not
   have saved C7, C15, or C16.

**Speculation ledger** (claims beyond frozen evidence, offered as hypotheses
only): that a disconfirmation-seeking re-query would have flipped any
particular install; that the C8/C11 one-sidedness was *caused* (rather than
merely accompanied) by the phrasing; that a debunk of the C15 fruit claim
exists to be retrieved.
