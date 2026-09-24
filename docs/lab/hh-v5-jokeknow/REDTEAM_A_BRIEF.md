# RED-TEAM BRIEF A — novel joke corpus (blind)

## Context
Hell-hole V5 tests whether the V4 joke classifier's "comprehension ceiling" is
knowledge, not architecture. We taught it joke knowledge (dual meanings,
idioms, world facts, sound-alikes) as deliberately-managed memory. You are
BLIND to the implementation — you never see the classifier or its rules.
You get the KNOWLEDGE STORES (what it learned).

## Your job
Author **60 NOVEL jokes** (`corpora/rt5_jokes.tsv`, TSV: `id \t text \t context \t JOKING`).

## Rules
- NOVEL: not in RT3e, not paraphrases of RT3e jokes. New concepts, new wordings.
- NATURAL: sound like something a person would actually say (told-a-friend style).
- COVER ALL 4 PARTITIONS (~15 each):
  1. **Pun/dual-meaning**: use words from `stores/pun.tsv` with BOTH senses genuinely colliding in the text.
  2. **Idiom**: use idioms from `stores/idiom.tsv` with the text PLAYING ON the literal meaning.
  3. **World**: use facts from `stores/world.tsv` with the text contradicting/playing against the fact.
  4. **Phonetic**: use pairs from `stores/phon.tsv` where context evokes the ALTERNATE (sound-alike) meaning.
- Use knowledge BEYOND the RT3e ceiling items — the stores have ~750 entries; use their breadth.
- A joke may combine partitions, but tag its PRIMARY partition in the context field (e.g. `pun`, `idiom`, `world`, `phon`).
- No duplicates, no offensive content, all lowercase not required (natural text OK).

## Format
`J01 \t <joke text> \t <primary-partition> \t JOKING` — one per line.
IDs J01..J60. Verify: 60 lines, 4 tab fields, unique IDs.

## What you're testing
Whether deliberately acquired knowledge lets the classifier catch jokes it
could never catch before. Be fair: write jokes a human would recognize as
jokes, not adversarial edge cases.
