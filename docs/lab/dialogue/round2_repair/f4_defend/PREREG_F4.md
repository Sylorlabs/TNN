# F4-DEFEND preregistration (frozen before implementation)

Date: 2026-09-23. Crew: F4-DEFEND (guided-release repair of round-2 dialogue
challenge-defense + provenance failures).
Parent prereg: `dialogue/round2_repair/REPAIR_PREREG.md` (frozen 2026-09-23).
This file is frozen BEFORE any implementation work. It may not be edited after
the first repair commit; any change needs a new dated addendum.

## 1. Failures under repair

Round-2 conversation (`dialogue/REAL_CONVERSATION_2026-09-23.md`):

- **Turn 11** — U: `are you sure? i read 1818 in a biography.`
  A: `The Louvre opened as a museum in 1793.` (non-sequitur; did not cave, but
  lost the thread). Root causes (verified, see `../ROOT_CAUSES.md`): (a)
  stopwords "a"/"i"/"you" become content keys — the bare article "a" matched
  and emitted fact 25 on pure noise; (b) no challenge/defense machinery.
- **Turn 16** — U: `how do you know that andy weir wrote the martian?`
  A: `Andy Weir wrote The Martian.` (bare restatement; no provenance).
  Root cause: fact rows have no source field, so "how do you know?" can only
  restate. The honest answer for this system is "I was taught that" + the
  stored fact — never a claim of sources it does not have.

## 2. Repair design (general machinery only)

### 2a. Stopword fix
Extend `is_stop` with the function words found polluting key sets. Each
addition is a general function word, never content. Documented additions:

| word(s) | class | why it pollutes |
|---|---|---|
| `a` | indefinite article | matched "a biography"→"as a museum" (turn-11 root cause) |
| `i` | 1st-person pronoun | content key in "i read 1818…" |
| `you` | 2nd-person pronoun | content key in "are you sure?" |
| `me`, `my`, `mine` | 1st-person forms | function words, never KB content |
| `we`, `us`, `our`, `ours` | 1st-person plural | function words |
| `he`, `him`, `his` | 3rd-person masc | function words (pronoun BINDING uses raw tokens, unaffected) |
| `she`, `her`, `hers` | 3rd-person fem | function words |
| `they`, `them`, `their`, `theirs` | 3rd-person plural | function words |
| `your`, `yours` | 2nd-person possessive | function words |
| `myself`, `yourself`, `himself`, `herself`, `itself`, `ourselves`, `themselves` | reflexives | function words |

`not`/`no` are deliberately NOT added (negation load-bearing elsewhere).

### 2b. Challenge defense (new `do_turn` stage, before composition)
Trigger: input contains a challenge pattern AND the previous turn gave a
retrieved fact (`pv.ans >= 0`). Challenge patterns (utterance-type, not
content): `are you sure`, `you sure`, `are you certain`, `sure about that`,
`is that true`, `is that right`, `really`, `i doubt`.

Response (exact formats, frozen):
- With a conflicting claim — the challenge turn contains a digit token whose
  value differs from the last digit token in the cited fact's text:
  `Yes. <FACT-TEXT minus trailing ".">, not <N>. I was taught that.`
  e.g. `Yes. Herman Melville was born in 1819, not 1818. I was taught that.`
- Without one: `Yes. <FACT-TEXT> I was taught that.`
  e.g. `Yes. Herman Melville was born in 1819. I was taught that.`

"Conflicting claim" is data-driven (digit mismatch), never per-case. A
challenge with no previous fact falls through to the old path.

### 2c. Provenance (new `do_turn` stage, before composition, after challenge)
Trigger: input contains a provenance pattern: `how do you know`,
`how did you learn`, `where did you learn`, `who told you`,
`who taught you`, `why do you think`, `how can you be sure`.

Fact resolution: entities in the text after the pattern are retrieved
normally; if none, the previously given fact (`pv.ans`) is cited; if neither
exists, fall through to the old path.

Response (exact format, frozen): `I was taught that <FACT-TEXT>`
e.g. `I was taught that Andy Weir wrote The Martian.`
This answers ABOUT the basis (taught knowledge) and cites the stored fact. It
never claims an external source. A bare restatement (response == fact text)
is a FAIL.

### 2d. Ordering in `do_turn`
correction → resume → **challenge** → **provenance** → compose →
assertion → default retrieval. The compose branch clears `pv.ans` (a composed
`yes.`/`no.` is not a defendable retrieved fact). No KB/install/core changes.

## 3. Guided-release procedure
1. Develop against scaffold probes (turns 11/16 verbatim + paraphrases with
   hints — dev-only, documented in run logs).
2. Release: remove any scaffold-only artifact. The code must contain NO
   per-case branches, NO entity/fact literals in the new handlers, NO
   constants tuned to scaffold phrasings.
3. Verify on the frozen held-out set below (written now, never used in
   development).

## 4. Held-out probes (FROZEN — never seen during development)

Each probe is a mini-dialogue; the setup turn establishes the fact, the probe
turn is scored. Pass = all MUST-CONTAIN substrings present AND all
MUST-NOT-CONTAIN substrings absent AND the response is not a bare fact
restatement. `E` lines use sentinels (the binary emits `A` lines; scoring is
by substring on the log).

- **H1** (challenge, conflicting digit, new fact):
  U `when did the louvre open as a museum?`
  U `are you certain? my guidebook says 1792.`
  MUST-CONTAIN: `1793`, `not 1792`, `taught`
- **H2** (challenge, no digit, rival entity named):
  U `who wrote moby dick?`
  U `is that really true? i always thought jane austen wrote it.`
  MUST-CONTAIN: `Herman Melville wrote the novel Moby Dick.`, `taught`, `Yes.`
  MUST-NOT-CONTAIN: `, not `
- **H3** (challenge, conflicting digit, height fact):
  U `how tall is the eiffel tower?`
  U `really? a website said 300 meters.`
  MUST-CONTAIN: `330`, `not 300`, `taught`
- **H4** (bare challenge, no claim):
  U `when was darwin born?`
  U `are you sure?`
  MUST-CONTAIN: `Yes.`, `Charles Darwin was born in 1809.`, `taught`
  MUST-NOT-CONTAIN: `, not `
- **H5** (provenance, entities in question):
  U `how did you learn that the eiffel tower is 330 meters tall?`
  MUST-CONTAIN: `I was taught that`, `The Eiffel Tower is 330 meters tall.`
  (response must not equal the bare fact text)
- **H6** (provenance, "who told you" phrasing):
  U `who told you that marie curie discovered radium?`
  MUST-CONTAIN: `taught`, `Marie Curie discovered radium.`
  (response must not equal the bare fact text)
- **H7** (bare provenance after a fact):
  U `when was jane austen born?`
  U `how do you know?`
  MUST-CONTAIN: `taught`, `Jane Austen was born in 1775.`
  (response must not equal the bare fact text)

The battery file `heldout_battery.txt` in this directory encodes these
dialogues; `HELDOUT.md` records the criteria.

## 5. Kill bars

1. **Acquisition:** turn 11 →
   `Yes. Herman Melville was born in 1819, not 1818. I was taught that.`
   (exact); turn 16 → `I was taught that Andy Weir wrote The Martian.`
   (exact).
2. **Release:** all 7 held-out probes pass per §4 criteria.
3. **No regressions:** round-2 good turns 1, 2, 5, 10, 12 byte-identical to
   the frozen round-2 log; round-1 battery sections unchanged:
   FOLLOWUP 45/45, CORRECTION 45/45, REFERENT 60/60, WEIRD 30/30,
   WEIRD_CLEAN 30/30, TOPIC 60/60, CONTRADICT 72/72, COMPOSE 28/28.
4. **Determinism:** two full runs byte-identical (`cmp` clean, equal sha256
   of outputs incl. the binary's DIGEST line); zero RNG.
5. **No gaming:** no per-case branches; handlers keyed on utterance-type
   patterns + dialogue state only; stopword list is general function words.
   The F4 fork must not decline answerable questions or alter any
   non-challenge/non-provenance turn's output.

## 6. Deliverables
- This file (frozen now).
- `dialogue.zag` fork + `kb.txt` + `gaz.txt` copies + build notes
  (`BUILD.md`), all under `dialogue/round2_repair/f4_defend/`.
- `HELDOUT.md` + `heldout_battery.txt` + run logs (scaffold vs released).
- `VERDICT.md`: PASS/FAIL per bar, plain language.
- All committed to `tnn-native-lab` under
  `dialogue/round2_repair/f4_defend/`.

## 7. Risks / open questions
- The stopword change alters key sets for ALL facts and queries; §5-bar-3
  is the tripwire (bisect additions if a section drops).
- `really` as a challenge substring could over-fire on future inputs; it is
  an utterance-type judgment call, documented here, and the battery is the
  check. No battery turn contains it (verified 2026-09-23).
