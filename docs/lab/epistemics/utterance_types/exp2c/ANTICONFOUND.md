# Anti-confound report — exp2c Stage-2 item files

Verifier: `stage2/check.py` (deterministic, no RNG). Corpus of forbidden
substrings: every 16-byte substring of every utterance text (lowercased) in
the frozen curriculum (`crew2/curriculum/*.txt`: ex/tr/pa/no/sinc/facts/calib/
fhyp/nest/supp/paraphrases/types) plus the original 48-item calibration corpus
(`broaderfix/crew2/calibration_corpus_items.txt`). 17,641 forbidden substrings.

## Files

- `cal_vol.txt` — 96 items: families A (`if the`), B (`do we`), C (`it is`),
  16 ENDORSE + 16 WITHHOLD each. W-items: A/B → hypothetical (ti=2),
  C → joke (ti=1, joke absurdities per the corpus proposal's family-C design).
- `cal_de.txt` — 32 items: new family D (`what if`) 8E+8W, new family E
  (`where do`) 8E+8W. W-items → hypothetical (ti=2). Families derived from the
  learner's own live hypothetical marker set (base MDUMP): `what if`,
  `where do` are live status-1 hypothetical UTT markers; A/B/C bigrams excluded.

## Checks (all pass)

1. **Zero ≥16-byte overlap with frozen utterances or the original 48-item
   corpus**: 0 violating items (after 4 rewrite iterations; initial draft had
   28, all rewritten — e.g. hypothetical phrasings echoing fhyp.txt/ex3.txt
   probes like "the moon were made", "the sea turned to", "where do we buy
   bread" from cc32).
2. **Zero ≥16-byte overlap among new items**: 0 pairwise collisions (initial
   draft had 44, mostly repeated frames like "how do we cross", "where do we
   find"; fixed by varying frames, verbs, and punctuation).
3. **Target bigram present** (case-insensitive substring, matching the
   learner's `has_sub` on lowered text): asserted for all 128 items.
4. **Six-speaker rotation**: cal_vol.txt 16 per speaker; cal_de.txt 5–6 per
   speaker (Mara/Theo/Priya/June/Sam/Dev).
5. **Sincere contexts on both polarities**: `says evenly` / `says plainly`
   alternate on BOTH E and W items (mirrors the original corpus: 12/12 each),
   so context carries no polarity signal.
6. **No type labels**: item files carry only the numeric concept index `ti`
   on W rows (2=hypothetical, 1=joke), ignored for E rows (`x`); no
   type-name strings.

## Generation note

`stage2/author.py` → `stage2/items_data.py` (utterance lists) →
`stage2/gen_stage2.py` (adds IDs/speakers/contexts). The verifier runs on the
final utterance bytes. `cal_ab.txt` / `cal_c.txt` / `cal_abc.txt` /
`cal_ab_rev.txt` (Stage-1) are verbatim transforms of the frozen 48-item
corpus (6-field rows with appended `ti`); no authoring, no overlap risk
beyond the frozen source itself.
