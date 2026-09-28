# Corpus Samples (real extracted facts)

## WordNet (kind 4) — wn.bin

- `wn:3.1:n:00001740` | that which is perceived or known or inferred to have its own distinct existence (living or nonliving)
- `wn:3.1:n:00001930` | an entity that has physical existence
- `wn:3.1:n:00002137` | a general concept formed by extracting common features from specific examples
- `wn:3.1:n:00002684` | a tangible and visible entity; an entity that can cast a shadow; "it was full of rackets, balls and other objects"

## Simple Wikipedia (kind 3) — wiki.bin

- `wiki:simple:april:sent000000` | April (Apr.) is the fourth month of the year in the Julian and Gregorian calendars, and comes between March and May.
- `wiki:simple:april:sent000001` | It is one of four months to have 30 days.
- `wiki:simple:april:sent000002` | April always begins on the same day of the week as July, and additionally, January in leap years.

Raw wikitext (same article) before cleaning:
`'''April''' (Apr.) is the fourth [[month]] of the [[year]] in the [[Julian calendar|Julian]] and [[Gregorian calendar]]s, and comes between [[March]] and [[May]].`

## Wiktionary (kind 1) — wikt.bin (parser validated on real pages)

- `wikt:en:dictionary:noun:001` | A reference work listing words or names from one or more languages, usually ordered alphabetically, explaining each term's meanings or senses, often also containing information on its etymology, pronunciation, usage, semantic relations, translations, as well as other relevant information.
- `wikt:en:dictionary:noun:002` | A synchronic dictionary of a standardised language held to only contain words that are properly part of the language.
- `wikt:en:dictionary:noun:004` | The collection of words used or understood by a particular individual.

## Negative control (frozen) — bad.bin

1,200 synthetic records: 200 dupes of the last real key (expect G2), 250 empty-text
(expect G1), 250 NUL-in-key (expect G1), 250 circular dict definitions (expect G3),
250 sentences without terminal punctuation (expect G3). Expected: g1=500, g2=200,
g3=500, installed=0.
