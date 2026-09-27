# TABLES.md — Attempt 3 parser tables (frozen 2026-09-27)

Every table below is **general linguistic knowledge — no label exposure**.
The implementer has never seen train labels. All tables were built from
dictionaries, grammar rules, and the blind (label-free) input texts' vocabulary
only. No table was tuned against labels, scores, or verdicts.

## Table 1: WORDNUM — word-number map
`zero`→0 … `ninety`→90, `hundred`→100, `thousand`→1000, `million`→10⁶,
`billion`→10⁹, `dozen`→12. General English number words.

## Table 2: DIM_OF_ADJ — evaluative dimension lexicon
Adjective → dimension. Dimensions: physical (`size,time,temp,weight,
distance,countdim,sense`) and evaluative (`taste,aesthetic,value,fun,moral,
general,feeling`). EVAL_DIMS = {taste,aesthetic,value,fun,moral,general,feeling}.
Dimension words, not topic words. Includes: "deaf/blind/mute"→sense (physical),
"respect"→value, "horned"→stem via noun-vocab check.

## Table 3: ANTONYMS — antonym pairs (91 pairs)
General-knowledge adjective antonyms (hot/cold, big/small, …), expanded beyond
attempt 2 to cover rank/size/time dimensions (long/short, early/late, …).
Coded to integer pairs in `antonym.tsv`.

## Table 4: verb tables
- **IRREG**: irregular + regular -ed past mapping (general English morphology),
  incl. corpus-attested regular pasts (ended→end, …).
- **LEX_VERBS**: verb form inventory (general English; corpus-attested forms
  added: separate/taste/circle/erase/offer/deliver/deserve/shed/drop/modify/title).
- **VERB_LEMMA/AUX**: auxiliaries and be/have/do lemmas.
- **lemma_verb**: deterministic lemmatizer; -es sibilant rule
  (passes→pass vs rises→rise), -ies→-y.
- **CAUSAL_VERBS** (cause, make, lead, generate, produce, …), **ORIGIN_VERBS**
  (invent, discover, write, compose, …), **DEONTIC_MODALS** (should/ought/must),
  **EXPERIENCER** (think/feel/believe/would), **SENSE_VERBS** (sound/taste/smell/
  feel/look → sensory dimension coercion).
- **VERB_DIM**: matter→value.

## Table 5: syntactic tables
- **ROLE_NOUNS**: closed class for "The <role> of <E> is <V>"
  (capital, inventor, discoverer, author, founder, composer, …).
- **COMPARATIVES**: -er/-est/more/most/less/least forms + irregular
  (better/best/worse/worst), with MORE/LESS direction per base.
- **ABSTRACT_NOUNS** (form/kind/way/type/…), **DET/STOP** (determiners,
  prepositions, possessive handling), **DEGREE_ADV** (too/so/very/…),
  **NEGWORDS** (not/never/no/unable/can't/…), **QUANT_CLASSES** (count/date),
  **STATIVE_PLACE_HEADS** (be/lie/stand/sit — functional location) vs
  **NONFUNC_PLACE_HEADS** (live/grow/occur/…).
- **NOUN_VOCAB**: label-blind noun inventory from the blind texts, used only
  for the -ed adjective→noun stem check ("horned"→"horn").

## Table 6: NOUN_VOCAB (see above)

## Output schema
- `frames.tsv`: `iid pidx nent e0..e5 ahead aclass adim vkind vcode vnum vdir
  vcmp vadj vent neg type itype func` — all categorical fields integer-coded
  via `vocab.tsv`. `vkind`: 0=NUM,1=CMP,2=ADJ,3=ENT,4=PHR. `type/itype`:
  0=FACTUAL,1=EVALUATIVE,2=DEONTIC,3=CAUSAL. `func`=1 iff the attribute is
  functional for the contradiction rule (role/origin/naming, or stative
  location). Count values carry the counted noun (`13:dozen`).
- `address.tsv`: per-premise addressing — 15 columns:
  `owner_iid owner_pidx addr_iid addr_pidx ahead aclass adim vkind vcode vnum
  vdir vcmp vadj vent neg` (the addressing item's premise values plus its
  premise index, for the prereg §4.3.4 standing check; comparison is
  deliberation, not build).
- `vocab.tsv`: `namespace code text` decode table.
- `idmap.tsv`: `iid opaque_id` (T0001–T0448 train, H0001–H0192 held-out).
- `classmeta.tsv`: `aclass_code quant _` (quant=1 for count/date).
- `antonym.tsv`: `adj_code adj_code` pairs.
- `massaddr.tsv`: mass-addressability audit (train-only): rank premises with a
  non-evaluative dimension are FACTUAL iff ≥1 *train* item carries that
  dimension; else re-typed EVALUATIVE (prereg §4.3.5).

## Label-blind build statistics (2026-09-27, frozen)
- items=640, well-formed items=640 (fraction 1.0000 ≥ 0.90 bar)
- premises=684, addressing rows=1006 (train+heldout index)
- items with ≥1 non-self address: 214/640
- item types: EVALUATIVE 171, FACTUAL 438, CAUSAL 25, DEONTIC 6
- build is byte-deterministic across reruns (sha256 verified)

No labels were consulted. No scores were computed.
