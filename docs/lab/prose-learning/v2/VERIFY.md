# VERIFY.md — inputs2 construction verification (Worker A, 2026-09-21/22)

Battery built by `~/workspace/richcomp/build_inputs2.py`, checked by
`~/workspace/richcomp/verify_inputs2.py`. **No RNG used anywhere** — all fact
selections are hand-picked fixed lists, all templates fixed. Re-running the
builder reproduces the files byte-identically (verified: sha256 before/after
rebuild identical).

## Verification coverage (all pass, 0 open fixes)

1. **Format**: every train line = exactly `{"id","text"}` with sequential ids
   from 0; every test line = exactly `{"id","probe","probe_value","expect"}`
   with `expect` in {value, contradiction, hedged, unknown}; non-value expects
   carry `probe_value: null`; value expects carry an int.
2. **SUB-PARA truth**: every train line's last number and every probe value
   checked against hand-computed truth (alpha = ord−64; word length = len(word);
   pub-year/count vs championship sol test probes). All 48 facts × 5 wordings
   consistent. No train wording duplicates any championship sol train sentence;
   the 5 wordings per fact are pairwise distinct.
3. **SUB-CONTR**: each item is exactly 2 sentences asserting different values
   (v1≠v2 verified); probes expect contradiction with null value.
4. **SUB-HEDGE**: asserted+hedged items verified asserted value ≠ hedged value
   and probe expects the asserted value; hedged-only probes expect hedged/null.
   All 12 hedge markers attested in the battery: think, believe, probably,
   maybe, perhaps, might, could, seems, allegedly, reportedly, possibly, likely.
5. **SUB-NEG**: neg-only items contain a standalone negation marker and probe
   unknown/null; neg+asserted items verified the asserted sentence's value
   equals the probe value (negation does not poison truth in either order).
6. **SUB-MULTI**: all 24 chains hand-checked — anchor value equals the true
   alphabet position, derived value = anchor±1 equals the true position of the
   queried letter, probe expects the derived value.
7. **SUB-CORE**: every item has a quoted entity in sentence 1 and a pronoun /
   "the word" / "the letter" coref phrase in sentence 2; sentence 2's last
   number equals the probe value (24/24).
8. **SUB-DISTR**: train ids 0–239 byte-equal to championship sol train
   (sentence→text conversion); test probes equal championship sol probes with
   expect=value. Distractors (240) verified: no frozen relation phrase, no
   negation word, no hedge word, no quotes; 48 distinct entities, each
   internally value-consistent across its 5 templates; entities disjoint from
   all championship entities.

## Championship-truth consistency

Constructed asserted values were cross-checked against the championship sol
test probes (the corpus teaching authority). Planted-falsehood entities
(D, saturday, incontrovertibleness, knowledge, Pilgrim's Progress,
David Copperfield, The Time Machine, triangle, baseball team,
Shakespeare-plays, spider-legs) are **never used as asserted-truth entities**
in any constructed item. CORE sentence-2 facts (years, counts, ranks) are
invented trivia, hand-verified as internally consistent (e.g. "K" occurs
2 times in "bookkeeping" — counted by hand).

## Items fixed during verification

1. **core id 19** (train): sentence 2 originally read
   `That letter appears twice in the word "letter".` — "twice" is a word, not
   a digit, so the v1 last-number value rule would find no value. Changed to
   `That letter appears 2 times in the word "letter".`
   (fix applied in `build_inputs2.py`; battery rebuilt; verifier re-run clean.)

No other items required fixes. One verifier-script typo (dropped "Q" from the
verifier's own alphabet string) was fixed in the verifier, not the battery.
