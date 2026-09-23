# F4-DEFEND run log — 2026-09-23

## Baselines (before repair)

Round-1 battery on canonical source, pinned compiler:
FOLLOWUP 45/45, CORRECTION 45/45, REFERENT 60/60, WEIRD 30/30,
WEIRD_CLEAN 30/30, TOPIC 60/60, CONTRADICT 72/72, COMPOSE 28/28.
DIGEST `35aaae8ac1bbf764d1f710403a9302ad1f4f9b5327c9b13793cd90299834474b`.

Round-2 conversation baseline captured (`conv2_run1.log`).

## Repair development (scaffold probes only)

Implemented in the F4 fork `dialogue.zag` (canonical untouched):
stopwords (`a i you` + pronoun/function-word family), challenge-defense
patterns, provenance patterns, challenge-before-composition dispatch,
stale-fact guard on composed turns.

Scaffold acquisition (dev-only inputs, never committed as behavior):
- turn 11: `Yes. Herman Melville was born in 1819, not 1818. I was taught that.`
- turn 16: `I was taught that Andy Weir wrote The Martian.`
- Louvre 1792 challenge: `Yes. The Louvre opened as a museum in 1793, not 1792. I was taught that.`
- "Who told you the Martian was written by Andy Weir?":
  `I was taught that Andy Weir wrote The Martian.`

Round-2 conv diff vs baseline: only turns 11 and 16 changed; good turns
1, 2, 5, 10, 12 byte-identical.

## Stopword regression investigation

1. With required stopwords (`a i you`) only: REFERENT dropped to 57/60.
   Three repeated failures: `What about Big Ben?` → `Big Ben is a landmark
   in London.` instead of `Big Ben is 96 meters tall.` Root cause: removing
   `a` exposed a Jaccard tie (2/5 vs 2/5) between the landmark and height
   facts; the old `a` pollution had accidentally broken the tie in the
   height fact's favor.
2. Added `about` as a stopword (documented as a general preposition/function
   word). This made `What about X?` content-free, which activated the
   existing entity-swap ellipsis machinery: REFERENT back to 60/60, but
   TOPIC dropped to 57/60 — `What about Pride and Prejudice?` after
   `Who wrote Moby Dick?` now carried the "who wrote" shape and answered
   `Jane Austen wrote the novel Pride and Prejudice.` instead of
   `Pride and Prejudice was published in 1813.`
3. Resolution: the ellipsis now requires the previous turn to have used
   pronoun binding (`pv[32] > 0`, a new prev-state field set in every
   `do_turn` branch). A `What about X?` after a complete question is a topic
   shift (direct retrieval); after a follow-up (`How tall is it?`) it
   continues the follow-up. General mechanism, no per-case code.

Final round-1 battery: 45/45, 45/45, 60/60, 30/30, 30/30, 60/60, 72/72,
28/28 — and the DIGEST is byte-identical to the pre-repair baseline
(`35aaae8a...`), i.e. every round-1 A-line is unchanged.

## Held-out release test (frozen probes, first examined at release)

All 7 held-outs pass against the frozen `HELDOUT.md` criteria:

- H1: `Yes. The Louvre opened as a museum in 1793, not 1792. I was taught that.`
- H2: `Yes. Herman Melville wrote the novel Moby Dick. I was taught that.`
- H3: `Yes. The Eiffel Tower is 330 meters tall, not 300. I was taught that.`
- H4: `Yes. Charles Darwin was born in 1809. I was taught that.`
- H5: `I was taught that The Eiffel Tower is 330 meters tall.`
- H6: `I was taught that Marie Curie discovered radium.`
- H7: `I was taught that Jane Austen was born in 1775.`

Setup turns all retrieved the correct facts. H2/H4 have no conflicting
number and correctly omit the `, not N` clause; H5/H6/H7 give the
`I was taught that` form with the fact, no invented source.

## Determinism

Every final artifact was produced twice and byte-compared:
- battery log: `33743aead2f6457dce48653df1eff28e91cbf165208839ab86fad0e8c4bbb372`
- held-out log: `6942704ce00556d624d149dd5e2e8f01e84e396149b902ed16bbc7f727a1156d`
- conv log: stable across rebuilds; turns 11/16 exact targets shown above.

Code scan of all new repair code: zero RNG references, zero entity names,
zero fact texts, zero digits (challenge/provenance dispatch is purely on
utterance-type patterns + generic numeric extraction).
