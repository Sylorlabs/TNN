# DIALOGUE — multi-turn conversation trial (PREREG, frozen 2026-09-21)

**Question (Micah):** can the TNN hold a conversation — follow-ups, weird styles,
weird wording? Does it repeat what it knows, or understand what's happening?

**Status:** nothing like this has been tested. The prose learners answer single
probes. This is the first multi-turn test.

## Base mechanism (frozen choice)

The pinned **v1 prose learner** (commit `d4c151c7e39c`) — Micah's 2026-09-21
decision: v1 stays the prose path; v2 did not ship; v3 is in flight and is not
a dependency. Its pipeline (tokenize → vocab → frozen stopwords → frozen
stemmer → key sets → Jaccard retrieval) is copied verbatim into `dialogue.zag`.
No v2 machinery is used.

## What is under test

`dialogue.zag`: a **deterministic dialogue-state manager** wrapped around the
frozen v1 retrieval core. The manager is the mechanism being measured. It is
explicitly a state machine, not a learned conversationalist — the experiment
asks whether *this architecture* tracks conversation state, and where it fails.

### Knowledge base (frozen, authored, 38 real-world-true facts)

IDs 0–37 (full text in `KB.md`; generated into the binary by `gen_dialogue.py`):

| IDs | Content |
|---|---|
| 0–3 | Melville / Moby Dick (wrote + novel, born 1819, published 1851, passive duplicate) |
| 4–7 | Austen / Pride and Prejudice (wrote + novel, born 1775, published 1813, passive duplicate) |
| 8–11 | Darwin / Origin of Species (wrote, born 1809, published 1859, passive duplicate) |
| 12–14 | Curie (discovered radium, born 1867, Nobel Prize 1903) |
| 15–17 | Weir / The Martian (wrote, born 1972, published 2011) |
| 18–20 | Eiffel Tower (in Paris, built 1889, 330 m) |
| 21–23 | Montparnasse Tower (in Paris, built 1973, 210 m) |
| 24–25 | Louvre (in Paris, opened as museum 1793) |
| 26–28 | Statue of Liberty (landmark in New York, dedicated 1886, 93 m) |
| 29–30 | Big Ben (landmark in London, 96 m) |
| 31–32 | Colosseum (in Rome, completed 80 AD) |
| 33–34 | Paris / Berlin capitals |
| 35–37 | water boils 100 °C, Everest 8849 m, Amazon 6400 km |

### Gazetteer (frozen, deterministic tie-break = lowest entity id)

Persons: Herman Melville, Jane Austen, Charles Darwin, Marie Curie, Andy Weir.
Non-persons: Moby Dick, Pride and Prejudice, On the Origin of Species,
The Martian, radium, Nobel Prize, Eiffel Tower, Montparnasse Tower, Louvre,
Statue of Liberty, Big Ben, Colosseum, Paris, Berlin, France, Germany,
New York, London, Rome, water, Mount Everest, Amazon River.
Honest limitation: entity recognition is a frozen gazetteer, not learned NER.

### Dialogue state

- `sal`: salience stack of entity ids, most-recent-first, cap 8, dedup.
- `topic`: topic stack of entity ids (push on topic change, pop on resume).
- `uclaims`: user assertions: (subject_eid, relation, value, turn_no), cap 16.
- `prev_ans`: fact id of the last TNN answer; `prev_q`: last resolved query.

### Turn processing (fixed order, deterministic)

1. **Correction markers** — utterance starts with "no" (followed by comma/space),
   or contains "i meant" / "not that" / "the other" / "wrong":
   exclude `prev_ans` from retrieval, re-run `prev_q`, return next-best fact.
   Updates salience and `prev_ans`.
2. **Resume markers** — contains "back to" or "anyway":
   "back to X" with entity X on the topic stack → pop down to X;
   otherwise pop one level. Respond with the resumed topic's general fact
   (lowest KB id mentioning the entity).
3. **Compose probes** — matches one of the frozen templates (§Compose):
   run the compose mechanism, return "yes" / "no" / entity name.
4. **User assertions** — no "?" in the utterance AND matches a frozen template
   (§Assertions): store the claim; on (subject, relation) conflict with a stored
   claim → `CONTRADICTION: turn {n} said {old}.`; else `NOTED.`
5. **Default** — resolve references (§Resolution), retrieve via v1 Jaccard
   (tie → lowest fact id, ties counted), respond with the retrieved fact's
   verbatim text.

### Reference resolution (pre-pipeline)

- Gazetteer scan, longest-match-first, left to right.
- Pronouns → salience: he/him/his/she/her → most recent person;
  it/its → most recent non-person; they/them → most recent entity (any).
  Pronoun tokens are *replaced* by the entity name before the v1 pipeline
  (necessary: v1's frozen stopwords delete "it"; "he"/"she" would be junk keys).
- No entity and no pronoun → keyword fallback: score entities by number of
  their name-words present as utterance tokens; take max > 0, tie → lowest eid.
- **Ellipsis**: if the resolved utterance has zero content tokens (no
  non-stopword token outside entity names), reuse the previous resolved query
  with the previous entity's name substituted for the new entity's
  ("And Germany?" after "What is the capital of France?").
- Both user and TNN turns update salience.

### Assertions (frozen templates, lowercased input)

- `{person} wrote {work}` / `{work} was written by {person}` → WROTE(work→person)
- `{entity} is {N} meters tall` → TALL(entity→N)
- `{entity} was built in {N}` → BUILT(entity→N)
- `{person} was born in {N}` → BORN(person→N)
- `{city} is the capital of {country}` → CAPITAL(country→city)
- `{entity} is in {place}` → LOCATED(entity→place)

Scope: only user-vs-user consistency is checked. KB-vs-user-assertion is the
principle-detection trial's territory (already proven), not this trial's.

### Compose (frozen templates)

- C1: "was the author of {work} born before {entity} was built?"
  AUTHOR_OF(work) = person in the lowest-id KB fact containing the work's name,
  a person entity, and key "wrote". Birth year / build year via the number
  lexicon on the matching born/built facts. `before` → year1 < year2.
- C2: "which is taller, {E1} or {E2}?" → heights from "{E} is {N} meters tall"
  facts → name of the taller (tie → lowest eid; preregistered, no ties in battery).
- C3: "did {person} write {work}?" / "did the author of {work1} write {work2}?"
  → "yes" if a KB fact contains the person, the work, and key "wrote", else "no".
- **Novelty control**: the binary asserts the compose response is not a
  substring of any KB fact text or any prior turn text, and prints
  `COMPOSE-NOVEL=1` per compose turn. A composed answer must be synthesis,
  not repetition.

### Battery (`battery.txt`, generated by `gen_dialogue.py`, frozen at build)

| Section | Dialogues | Turns each | What it measures |
|---|---|---|---|
| FOLLOWUP | 15 | 3–4 | anaphora + ellipsis chains (he/she/it, "And Germany?") |
| CORRECTION | 15 | 3 | revise-not-repeat (exclude prev answer, take next-best) |
| REFERENT | 15 | 4 | "it" rebinding across referent switches |
| WEIRD | 15 | 2–3 | typos, fragments, slang, indirect, passive |
| WEIRD_CLEAN | 15 | 2–3 | clean twins of WEIRD (style-gap control) |
| TOPIC | 15 | 4 | push / push / pop ("back to", "anyway") |
| CONTRADICT | 15 | 4–5 | user asserts X at turn 2, denies at turn 4–5 (12 true contradictions + 3 consistent restatements as false-alarm controls) |
| COMPOSE | 10 | 3 | C1 ×4, C2 ×3, C3 ×3 — synthesis across turns |

Total ≈ 115 dialogues, ≈ 390 turns. Every turn has an expected response:
a KB fact's verbatim text, `NOTED.`, `CONTRADICTION: turn {n} said {old}.`,
"yes" / "no", or an entity name. Expectations are set by authorial intent
(the semantically correct answer), never by running the binary.

### Scoring

Per turn: PASS = exact match with expected. Per-type rate = passes / turns.
Style gap = WEIRD rate − WEIRD_CLEAN rate (percentage points).

## Kill bars

- **KB-DLG-TRACK**: per-type state-tracking rate ≥ 0.70 for FOLLOWUP,
  CORRECTION, REFERENT, TOPIC, CONTRADICT. Reported per type; any type
  below 0.70 = FAIL for that type (no averaging away weakness).
- **KB-DLG-STYLE**: |WEIRD − WEIRD_CLEAN| ≤ 30pp, else FAIL.
- **KB-DLG-DET**: 5/5 byte-identical run logs (output has no timestamps;
  determinism is verified by the oracle on full logs).
- **KB-DLG-COMPOSE** (measurement): report compose success rate and the
  novelty-control result. If compose is 0% and analysis shows repeat-only
  behavior, the verdict states that plainly — a finding, not a hidden failure.

## Determinism and verification

- Pure Zag, zero RNG in any decision path. Static scan of new sources required.
- 5 repetitions; oracle `verify_dialogue.py` independently replays
  `battery.txt`, recomputes every turn's PASS/FAIL from the run log, checks
  per-type counts and the final sha256 digest of all responses.
- Calibration: the author may reword turns that are broken by construction
  (no KB fact can answer them); expectations stay fixed to the semantically
  correct fact. All rewordings are documented in VERDICT.md.

## Honest limitations (preregistered)

1. Gazetteer entity recognition, not learned NER.
2. Authored 38-fact KB, not a broad corpus.
3. Responses are retrieved fact texts (or computed short answers) — no fluent
   generation; the trial measures state tracking, not eloquence.
4. Assertion/possessive handling is template-based.
5. WEIRD covers wording variation, not speech errors at scale.

## Deliverables

`dialogue.zag`, `gen_dialogue.py`, `battery.txt`, `KB.md`, `oracle`
(`verify_dialogue.py`), 5 md5-verified run logs, `SHA256SUMS`, `VERDICT.md`,
committed to `tnn-native-lab` under `docs/lab/dialogue/`; night-run log entry.
