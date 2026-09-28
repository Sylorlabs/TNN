# KNOWLEDGE STORE SPEC — hell-hole V5 joke-knowledge experiment (2026-09-24)

## Purpose
Test Micah's ruling: the V4 joke classifier's "comprehension ceiling" (~83% of
misses need semantic comprehension) is KNOWLEDGE, not architecture. We teach
the classifier joke knowledge at volume as deliberately-managed memory
partitions, then measure whether recall on the ceiling classes rises while the
deadpan-install bar (zero) holds.

## The architectural discipline (NON-NEGOTIABLE)
Knowledge NEVER fires on shape alone. Every knowledge-backed rule keeps the
V4 shape+incongruity-turn discipline: the knowledge supplies the SEMANTIC
CONTENT (what the two meanings are, what the fact is), and a general
mechanism still verifies a genuine INCONGRUITY TURN in the text (sense
collision, literal/figurative clash, fact violation). A store entry present
in sincere text with no turn must NOT install. This is what separates
knowledge from lexicon-stuffing.

## The four stores (plain TSV, one record per line, TAB-separated fields)

### 1. pun.tsv — dual-meaning words/phrases (~200 entries)
Format: `word \t senseA_cues \t senseB_cues \t gloss`
- `word`: the dual-meaning unit, lowercase (may be multi-word: "put down").
- `senseA_cues` / `senseB_cues`: comma-separated single words/short phrases
  that evoke each sense in surrounding text.
- `gloss`: `A=<sense A>; B=<sense B>` for audit.
- Example: `interest \t lost,keep,curious \t bank,banker,rate,loan \t
  A=curiosity/attention; B=financial charge`
- Breadth: the common dual-meaning words jokes actually use (bank, break,
  date, note, sole, bark, right, left, put down, make up, run, etc.). MUST
  include the RT3e ceiling words: interest, put down, working on, uplift,
  problems (math-problems vs difficulties), break (rest vs KitKat slogan).

### 2. idiom.tsv — idioms with literal-play cues (~200 entries)
Format: `phrase \t literal_play_cues \t gloss`
- `phrase`: the idiom, lowercase.
- `literal_play_cues`: comma-separated words that, appearing alongside the
  idiom, signal the text is PLAYING ON the literal meaning (the clash).
- `gloss`: `fig=<figurative meaning>; lit=<literal reading>`.
- Example: `play by ear \t piano,hands,hear,listen \t fig=improvise;
  lit=using the ear as a body part`
- MUST include RT3e ceiling idioms: play by ear, makes my day, days were
  numbered, dying to leave.

### 3. world.tsv — world facts with violation cues (~200 entries)
Format: `entity \t fact_cues \t violation_cues \t gloss`
- `entity`: the thing the fact is about, lowercase.
- `fact_cues`: comma-separated words evoking the fact.
- `violation_cues`: comma-separated words/phrases whose presence alongside
  the entity signals the text CONTRADICTS or plays against the fact.
- `gloss`: `fact=<the fact>`.
- Example: `parachute \t skydive,survive,safe \t don't need,without,no parachute
  \t fact=a parachute is needed to survive a skydive`
- MUST include RT3e ceiling facts: parachute/skydive, gazpacho served cold,
  KitKat "have a break" slogan, Siri/front camera, utility companies send
  bills, thesaurus = book of synonyms.

### 4. phon.tsv — homophones / sound-alikes (~150 entries)
Format: `written \t alternate \t alt_meaning_cues \t gloss`
- `written`: the word as written in text. `alternate`: what it sounds like.
- `alt_meaning_cues`: comma-separated words evoking the ALTERNATE reading's
  meaning in context.
- `gloss`: `sounds like "<alternate>"`.
- Example: `seafood \t see food \t see,eat,diet \t sounds like "see food"`
- MUST include RT3e ceiling pairs: seafood/see food, lettuce/let us,
  tearable/terrible, impasta/impostor.

## Authoring constraints
- All lowercase, plain ASCII. No smart quotes, no emojis.
- Cue lists: 2-8 cues each, words/phrases that would plausibly appear in real
  text (not joke-specific phrasing).
- BREADTH OVER DEPTH: cover the space of joke knowledge, not just the RT3e
  items. The test corpora will be NOVEL jokes; the stores must generalize.
- NO joke texts in the stores. Knowledge only.
- Deduplicate within each store (one record per word/phrase/entity).
- Sort each file alphabetically by the first field (deterministic; enables
  clean volume-tier subsetting by interleave).
- Provenance: a header comment line (`#`) per file stating authoring method
  and date; per-entry provenance is the gloss field.

## Output
Four files: `~/workspace/hh-v5-jokeknow/stores/pun.tsv`, `idiom.tsv`,
`world.tsv`, `phon.tsv`. Plus a one-page `STORES_README.md` with counts and
any authoring judgment calls.

## What this is NOT
- Not a joke corpus. Not trigger lists for firing on shape.
- Not an attempt to memorize the RT3e items. The RT3e items' knowledge is
  legitimately included (it's real knowledge), but the stores must stand
  alone as general joke knowledge.
