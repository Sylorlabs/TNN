# Collection log — held-out set (64 items, all real web)

Collector: crew agent, 2026-09-22. Frozen BEFORE any training-corpus work.
SHA-256: `corpus/HELDOUT_SHA256.txt` (heldout.json), `corpus/HELPER_SHA256.txt` (helper.json).
Disjoint from: the training corpus (does not exist yet at freeze time) and the
joke-lie-trial 30-item corpus.

## Label policy (from GATE_SPEC.md, frozen)

| Class | N | Label |
|---|---|---|
| D-A | 24 | JOKING — deadpan advice jokes, glue-on-pizza class |
| D-B | 16 | JOKING — absurd-premise flat jokes stated sincerely |
| SAT | 8 | SATIRE — theonion.com week-in-review headlines |
| HOAX | 8 | DECEPTIVE — documented deliberate fabrications |
| SINC | 8 | SINCERE — 4 true-weird + 4 sincerely-held common false beliefs |

All item texts are verbatim excerpts from the cited public-web pages, copied
character-for-character from the fetched page text on 2026-09-22.

## Sources by class

**D-A (24).** 12 pre-existing + 12 new from the same two joke threads:
- https://www.boredpanda.com/funny-bad-advice/ — page header frames items as
  "pure entertainment"/"tongue-in-cheek", "should not be taken seriously":
  uncontested JOKING intent. 19 of the 24 D-A items.
- https://www.thepoke.com/2022/09/13/15-terrible-life-tips/ — explicitly
  identifies r/ShittyLifeProTips as mocking pro-tips, "don't try these": hda08, hda09.
- https://knowyourmeme.com/memes/delete-system32 — documented troll advice: hda10.
- https://www.techspot.com/community/... — documented fake microwave-charging ad: hda11.

**D-B (16).** Joke listicles / joke threads: boredpanda (11), thepoke (3),
humorliving.com (hdb07), christianforums.com dumbest-jokes thread (hdb08, hdb09).

**SAT (8).** https://theonion.com/the-week-in-review-1819580587/ — satire
outlet, uncontested SATIRE.

**HOAX (8).** Deliberate fabrications, each with a documented-fabrication basis:
- hhx01 AFDB (zapatopi.net/afdb) — parody hoax site.
- hhx02 Bonsai Kitten (pcworld.com) — FBI-investigated fabrication; item text is
  PCWorld's factual reporting of the hoax site's copy (sincere reporting OF a hoax).
- hhx03 DHMO Research Division (diigo.com hoax-websites list) — documented gimmick site.
- hhx04 Apple Wave (bustle.com) — documented 4chan fabrication.
- hhx05 All About Explorers (en.paperblog.com) — "web site developed by a group
  of teachers with fake information to show students that not everything that
  they read on the internet is true"; Columbus pitch quoted verbatim.
- hhx06 Dog Island (annarbor.com) — site called "an obvious tongue-in-cheek
  urban myth"; pitch quoted verbatim.
- hhx07 Dehydrated Water (hoaxes.org) — "an old joke/gag product"; instructions
  quoted verbatim from the site copy.
- hhx08 Pacific Northwest Tree Octopus (truthorfiction.com) — Lyle Zapato's
  1998 internet hoax, "intentionally humorous and fictitious"; site pitch quoted verbatim.
  (Replaces the weaker Jackalope excerpt; archive fetch for the Jackalope
  Conspiracy page failed and was not retried.)

**SINC (8).** Sincere intent + no joke markers.
- True-weird (content factual): hsi01 sharks older than trees
  (discoverwildlife.com); hsi02 banana equivalent dose (scienceabc.com);
  hsi03 Shannon number vs atoms (chess.com); hsi04 Mpemba effect
  (science.howstuffworks.com).
- Believed-false (intent sincere; the asserted/embedded factual claim is false —
  these test that a sincere false belief is NOT dismissed as a joke):
  hsi05 "lightning never strikes twice" (sincerely-used proverb,
  idioms.thefreedictionary.com); hsi06 "as blind as a bat"
  (sincerely-used idiom, idioms.thefreedictionary.com); hsi07 "I have the
  memory of a goldfish" (sincerely-used common phrase, westeamahead.org);
  hsi08 daddy-longlegs venom legend (widely-repeated playground legend
  sincerely asserted by repeaters, livescience.com).

## Exclusions applied

- No flat-earth / chemtrails / Epstein-class items (Micah's skepticism rule).
- No items from the joke-lie-trial 30-item corpus (freshness).
- No items with ambiguous authorial intent (e.g. real MMS bleach "cures" —
  sincere conspiracy belief, NOT a joke; excluded).
- No tide-pod / cinnamon-challenge items (real harmful behavior; intent ambiguous).
- The Mpemba item is stated in its standard observed form
  ("when hot water and cold water are placed in the identical freezing
  environment, the hot water will freeze faster"), not the over-broad form.

## Blind helper judgments (corpus/helper.json)

Crew-authored intent judgments from item TEXT ALONE, before any training —
per GATE_SPEC the helper is an untrusted observer and the combination rule is
asymmetric (helper SINCERE can never manufacture SINCERE; final SINCERE
requires the classifier's own SINCERE). Judgments: 24 JOKING (all D-A),
16 JOKING (all D-B), 5 SATIRE + 3 UNCERTAIN (SAT), 4 DECEPTIVE + 2 JOKING +
1 SINCERE + 1 UNCERTAIN (HOAX), 8 SINCERE (SINC). Every cited phrase was
machine-checked to be a substring of the folded item text.

## Caveats (honest)

- The helper judgments are CREW judgments (one agent), not an independent
  system. They are frozen as untrusted observations by design.
- Held-out text is crew-selected real-web material; the "uncontested" claim
  rests on the cited page framing (joke-thread headers, satire outlet,
  documented-hoax writeups), documented per item in the `basis` field.
- Items hhx02, hhx06, hhx07, hhx08 sit at the joke/hoax boundary; the corpus
  labels them DECEPTIVE on the documented-fabrication basis. This is a crew
  judgment call, disclosed here.
