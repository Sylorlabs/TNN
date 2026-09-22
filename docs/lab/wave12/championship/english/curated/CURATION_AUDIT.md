# CURATED English Corpus — Curation Audit (2026-09-21)

**Crew:** pure-Muse native curation crew (a single native Muse subagent executing
the deliberation protocol; depth limit prevented spawning a team — no API calls
were made at any point, all work is local reads + deliberation).
**Corpus:** `curated_corpus.json` sha256
`6fbbfdb6c87d419de69921f9a0f709b908024f9e0bed7c15fc9671517e67ac62`
**Result: 232 ADOPTED / 8 WITHHELD.** Native false-claim flag tally: **12/12**.

## 1. Sources verified (sha256, before use)

| source | sha256 (verified) |
|---|---|
| gpt-5.6-sol | `41aa8f5be15f778034cfce63250233468d364f52b318a02f63a87ac7459015d7` |
| grok-4.6 | `7f3a25739981c8276082ceeda7de3628afd88977e7a16bd0a5f220eba2bc2508` |
| step-3.7-flash:free | `c52e4f52dc15713a5995ff7bc26b9b04298d79df881dca1a90052b76d2ea69ab` |
| swe-1-6-slow:free | `ca1e7b858791fb26966cb7671274a29168679b05201662535359b77712b92456b7f` |
| muse-native | `1d5c2ede5332c857a31c053d88b0930d4cb6ca080a549f59012d1defa9c51e07` |

Frozen prompt input: `corpus-input/facts.json` sha256
`4f1ba933a75a0f9e488ae170366afe7f514aec425f92432f5b0e0b49cbfede5`
(prompts sha `ac5d7d3155f9a90dc60f4f3ec529a3c6125a0469ce5862c7193fb261441b8b7d`
per corpus meta records). Only `claim_text`/`value` (the supplied claim) were
read; the `false` flags and `false_ids` are the answer key and were **never
consulted during curation or flagging**.

## 2. Decision rule (deliberated from the frozen prompt)

The frozen prompt (`ENGLISH_PROMPT_SET.md`) REQUIRES every teacher's
OBSERVATION/PROBE_VALUE to state the GIVEN (supplied) value exactly, and asks
each teacher to choose its own DISTRACT_VALUE ("an integer DIFFERENT from
OBS_VALUE", DISTRACTOR "e.g. starting \"Memorize:\""). The crew therefore
defines:

- **The teach value** = the fact taught: `obs_value` (= `probe_value`), plus
  `dump_value` (planted as trainer evidence in D1, flaw-checked in §B.7).
- **ADOPT** iff 5-source UNANIMOUS agreement on (obs, probe, dump) AND the
  unanimous fact equals the frozen prompt's supplied claim (claim envelope)
  AND every row is mechanically valid (ints parse; probe==obs; texts state
  their values).
- **Distractor values vary BY DESIGN** — not a disagreement signal. Defective
  distractors (== obs, non-int, text/value mismatch) are excluded; the crew
  selects one healthy distractor per id by **majority vote, ties → closest to
  obs, then lowest**. Deterministic, truth-agnostic, recorded per row.
- **ANY fact disagreement or envelope break → WITHHOLD + AUDIT** (dead numeric
  lanes; the teaching legs skip withheld ids via the proven `muse_withheld_at`
  machinery).

Deliberated benign variations (NOT defects — documented, not hidden):
- step ids 0–11, 230, 231 spell values as English words ("first", "seven",
  "four", "five"): the sentence states the value unambiguously; the numeric
  lane (all the learner consumes) is unanimous → ADOPT.
- swe's "Memorize that …" phrasing: the prompt says 'e.g. starting
  "Memorize:"' — an example, not a requirement → accepted.

## 3. WITHHOLD + AUDIT — the 8 contested facts

### id 4 — alpha-pos 'E' (supplied=5)

- obs: {'sol': 5, 'grok': 5, 'step': 5, 'swe': 5, 'muse-native': 5}
- probe: {'sol': 5, 'grok': 5, 'step': 5, 'swe': 5, 'muse-native': 5}
- dump: {'sol': 5, 'grok': 5, 'step': 4, 'swe': 5, 'muse-native': 5}
- reason: FACT DISAGREEMENT obs=[5, 5, 5, 5, 5] probe=[5, 5, 5, 5, 5] dump=[5, 5, 4, 5, 5]
- crew: contested fact — agree-before-add withholds; lanes zeroed, text kept for audit.

### id 88 — word-len 'rhyme' (supplied=5)

- obs: {'sol': 5, 'grok': 5, 'step': 5, 'swe': 5, 'muse-native': 5}
- probe: {'sol': 5, 'grok': 5, 'step': 5, 'swe': 5, 'muse-native': 5}
- dump: {'sol': 5, 'grok': 7, 'step': 5, 'swe': 5, 'muse-native': 5}
- reason: FACT DISAGREEMENT obs=[5, 5, 5, 5, 5] probe=[5, 5, 5, 5, 5] dump=[5, 7, 5, 5, 5]
- crew: contested fact — agree-before-add withholds; lanes zeroed, text kept for audit.

### id 89 — word-len 'grammar' (supplied=7)

- obs: {'sol': 7, 'grok': 7, 'step': 7, 'swe': 7, 'muse-native': 7}
- probe: {'sol': 7, 'grok': 7, 'step': 7, 'swe': 7, 'muse-native': 7}
- dump: {'sol': 7, 'grok': 8, 'step': 7, 'swe': 7, 'muse-native': 7}
- reason: FACT DISAGREEMENT obs=[7, 7, 7, 7, 7] probe=[7, 7, 7, 7, 7] dump=[7, 8, 7, 7, 7]
- crew: contested fact — agree-before-add withholds; lanes zeroed, text kept for audit.

### id 90 — word-len 'spelling' (supplied=8)

- obs: {'sol': 8, 'grok': 8, 'step': 8, 'swe': 8, 'muse-native': 8}
- probe: {'sol': 8, 'grok': 8, 'step': 8, 'swe': 8, 'muse-native': 8}
- dump: {'sol': 8, 'grok': 10, 'step': 8, 'swe': 8, 'muse-native': 8}
- reason: FACT DISAGREEMENT obs=[8, 8, 8, 8, 8] probe=[8, 8, 8, 8, 8] dump=[8, 10, 8, 8, 8]
- crew: contested fact — agree-before-add withholds; lanes zeroed, text kept for audit.

### id 91 — word-len 'vocabulary' (supplied=10)

- obs: {'sol': 10, 'grok': 10, 'step': 10, 'swe': 10, 'muse-native': 10}
- probe: {'sol': 10, 'grok': 10, 'step': 10, 'swe': 10, 'muse-native': 10}
- dump: {'sol': 10, 'grok': 9, 'step': 10, 'swe': 10, 'muse-native': 10}
- reason: FACT DISAGREEMENT obs=[10, 10, 10, 10, 10] probe=[10, 10, 10, 10, 10] dump=[10, 9, 10, 10, 10]
- crew: contested fact — agree-before-add withholds; lanes zeroed, text kept for audit.

### id 92 — word-len 'paragraph' (supplied=9)

- obs: {'sol': 9, 'grok': 9, 'step': 9, 'swe': 9, 'muse-native': 9}
- probe: {'sol': 9, 'grok': 9, 'step': 9, 'swe': 9, 'muse-native': 9}
- dump: {'sol': 9, 'grok': 7, 'step': 9, 'swe': 9, 'muse-native': 9}
- reason: FACT DISAGREEMENT obs=[9, 9, 9, 9, 9] probe=[9, 9, 9, 9, 9] dump=[9, 7, 9, 9, 9]
- crew: contested fact — agree-before-add withholds; lanes zeroed, text kept for audit.

### id 93 — word-len 'chapter' (supplied=7)

- obs: {'sol': 7, 'grok': 7, 'step': 7, 'swe': 7, 'muse-native': 7}
- probe: {'sol': 7, 'grok': 7, 'step': 7, 'swe': 7, 'muse-native': 7}
- dump: {'sol': 7, 'grok': 4, 'step': 7, 'swe': 7, 'muse-native': 7}
- reason: FACT DISAGREEMENT obs=[7, 7, 7, 7, 7] probe=[7, 7, 7, 7, 7] dump=[7, 4, 7, 7, 7]
- crew: contested fact — agree-before-add withholds; lanes zeroed, text kept for audit.

### id 94 — word-len 'page' (supplied=4)

- obs: {'sol': 4, 'grok': 4, 'step': 4, 'swe': 4, 'muse-native': 4}
- probe: {'sol': 4, 'grok': 4, 'step': 4, 'swe': 4, 'muse-native': 4}
- dump: {'sol': 4, 'grok': 3, 'step': 4, 'swe': 4, 'muse-native': 4}
- reason: FACT DISAGREEMENT obs=[4, 4, 4, 4, 4] probe=[4, 4, 4, 4, 4] dump=[4, 3, 4, 4, 4]
- crew: contested fact — agree-before-add withholds; lanes zeroed, text kept for audit.

## 4. Distractor selection notes (adopted ids)

232 adopted ids each carry the crew-selected distractor. Selection was by
majority vote in 152 ids; the remaining 80 were ties broken by closeness to
obs (then lowest). Notable cases:

- **id 185** (chessboard, obs=64): sol's distract_value **64 == obs_value 64**
  violates the prompt's "DIFFERENT" requirement (its distractor text says 72
  while the value lane says 64 — the retained sol quirk). sol's distractor
  EXCLUDED as defective; remaining votes {60: swe, 63: step, 66: muse-native,
  81: grok} tied 1-1-1-1 → closest to 64 → **63** (step's text adopted).
- All other ids: every source's distractor was healthy (≠ obs, int, text
  matches value); selection = majority/tie-break as recorded per row in
  `distractor_selection` / `distractor_votes`.

## 5. Adopted ids (232)

Unanimous fact + envelope-clean + mechanically valid. Full per-row detail in
`comparison.json`; distractor choice per row in `curated_corpus.json`.

| ids |
|---|
| 0–3, 5–87, 95–239 |

## 6. Native false-claim flagging — AUDIT OBSERVATIONS ONLY

These flags never changed the corpus (the 12 false plants are taught exactly
as supplied, per the prompt's "do NOT correct" rule). The crew reviewed all
240 supplied claims natively — letters counted, words counted, publication
years and count-facts recalled — and flagged the ids it believes false.
Tally against the planted set (derived from facts.json AFTER flags were
recorded): **12/12 flagged, 0 false positives, 0 missed.**

| id | supplied claim | crew reason |
|---|---|---|
| 3 | D has alphabet position 5 | D is the 4th letter of the alphabet, not 5th (high confidence) |
| 29 | D has alphabet position 6 | D is the 4th letter of the alphabet, not 6th (high confidence) |
| 55 | 'saturday' has 7 letters | s-a-t-u-r-d-a-y = 8 letters (high confidence) |
| 71 | 'incontrovertibleness' has 21 letters | counted 20 letters (high confidence) |
| 80 | 'knowledge' has 8 letters | k-n-o-w-l-e-d-g-e = 9 letters (high confidence) |
| 103 | The Pilgrim's Progress published 1688 | first published 1678 (Part 1); 1688 is a decade off (high confidence) |
| 117 | David Copperfield published 1851 | serialized 1849-1850, first book edition 1850 (high confidence) |
| 139 | The Time Machine published 1896 | published 1895 (book form; serialized 1894-95) (high confidence) |
| 163 | a triangle has 4 sides | a triangle has 3 sides by definition (high confidence) |
| 178 | 10 baseball players on the field | 9 fielders (P, C, 4 infield, 3 outfield); the DH does not field (high confidence) |
| 205 | 38 plays attributed to Shakespeare | the standard canon is 37 plays (36 in the First Folio + Pericles); 38 requires counting a co-authored play (moderate confidence) |
| 231 | a spider has 7 legs | spiders have 8 legs (high confidence) |

**Verdict on the measure:** native falsehood detection is 12/12 with reasons
on every flag — the crew caught every planted falsehood (alphabet ordinals,
letter miscounts, wrong publication years, wrong counts) from the supplied
claims alone, with zero false alarms on the 228 true claims.
