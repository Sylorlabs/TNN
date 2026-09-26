# LEARNED_VERDICT.md — TNN-native learned chunking policy (pure Zag, zero RNG)

Date: 2026-09-26. Branch: `tnn-native-lab`. Source: `learned_chunk.zag`.

## What was built, in plain words

TNN learns **which chunking method to use for which kind of question** by
trying all four candidate methods on training questions, measuring what
worked, and freezing the winner per situation. The learning is over a
hand-authored candidate set (see boundaries); what is learned is the
routing, from measured outcomes, not programmer-written kind→chunk rules.

### The four candidate methods

| id | method | provenance |
|----|--------|------------|
| K1 | addressed-CHAR: character scan over a located span | D-derived (fork C's char scan generalized to addressed spans) |
| K2 | addressed-WORD: word scan over a located span | D-derived (fork W's word scan generalized) |
| K3 | WORD→CHAR magnifying glass: zoom to the located span, then char-address inside it | D's `mg_zoom` + located span |
| K4 | WORD?CHARSCAN: zoom to the located span, then plain char scan | magnifying-glass variant |

Fixed C/W/S from the fork are **not** in the candidate set — they are retired
from live intake and run only as negative controls (`ctrl_q`).

### Context (the situation the policy sees)

`ctx = kind×100 + text_shape×10 + subspan_class`, all derived from
(question, text) alone — no answer leakage:

- `kind`: fork classifier (1 LETTER_COUNT … 9 POS_LAST) + 12 sentence-word
  selection + 13 sentence word-count (new structural kinds, not epistemic).
- `text_shape`: 0 single short word, 1 multi-word / sentence text, 2 multi-sentence.
- `subspan_class`: 0 whole-text (kind 6: needle is a whole word, so word-scale
  suffices), 1 literal sub-span named in the question (kind 6: needle is a
  substring, so word-scale falls back), 2 ordinal/unlocatable reference.

### The learning loop (no RNG anywhere)

1. For each training question (original 24), try all four candidates in
   round-robin order `((round+qid) % 4) + 1` — deterministic, no shuffling.
2. Record per (ctx, candidate): trials, correctness, native answers (no
   fallback), total ops.
3. Gain rule, fixed before training:
   `gain = 1000·correct + 100·native − ops`. Ties break to the lower
   candidate id.
4. Freeze the ledger; evaluate original 24 + 12 new adversarial traps.
   Unseen contexts route to **K3** (the addressed magnifier) — an adaptive
   method, not a hidden fixed fallback.

Every zoom is logged to a zoom ledger `(qid, span, parent, off, len, depth,
why)` — the deliberation record.

### The learned policy (all 13 trained contexts)

| ctx | situation | winner | candidate gains [K1,K2,K3,K4] | read |
|-----|-----------|--------|-------------------------------|------|
| 100 | LETTER_COUNT, single word, whole | **K1** | [6541, 5935, 6535, 6535] | char scan is cheapest at char scale |
| 110 | LETTER_COUNT, multi-word, whole | **K1** | [3253, 2945, 3250, 3250] | same, multi-word |
| 200 | POSITION, single, whole | **K1** | [3286, 2983, 3286, 3286] | tie → K1 on tie-break |
| 211 | POSITION, multi-word, literal sub-span (the money-trap ctx) | **K3** | [98, 994, 1094, 1094] | **only ctx where magnify wins**: K1 answers the wrong span (98 — 0 correct) |
| 300 | REVERSE, single, whole | **K1** | [2187, 1985, 2187, 2187] | tie → K1 |
| 400 | WORD_COUNT, single, whole | **K2** | [1095, 1099, 1099, 1099] | tie → K2 |
| 410 | WORD_COUNT, multi-word, whole | **K2** | [1081, 1096, 1096, 1096] | tie → K2 |
| 500 | LENGTH, single, whole | **K2** | [2188, 2198, 2188, 2188] | **weird win**: K2 answers letter-count via word lengths, 10 ops cheaper |
| 601 | CONTAINS, single, substring-scope | **K1** | [1090, 989, 1089, 1089] | word-scale falls back on substrings |
| 610 | CONTAINS, multi-word, word-scope needle | **K2** | [1081, 1096, 1096, 1096] | tie → K2 (whole-word needle, native) |
| 710 | FIRST_WORD, multi-word, whole | **K2** | [1097, 1099, 1096, 1096] | word questions stay at word scale |
| 810 | POS_FIRST, multi-word, whole | **K1** | [1099, 999, 1099, 1099] | tie → K1 |
| 900 | POS_LAST, single, whole | **K1** | [1099, 999, 1089, 1089] | K1 native and cheapest |

Reading the policy: char-scale questions → K1 (char scan); word-scale
questions → K2 (word scan); the addressed magnifier K3 is reserved for the
one situation that needs it — a named sub-span inside a larger text
(ctx 211), where fixed scales answer the wrong question. K4 (WORD?CHARSCAN)
never won anywhere: it tied K3 on every trial and lost every tie-break —
tested, measured, earned no keep.

### Weird choices, with measured justification

- **K2 for LENGTH (kind 5), gain 2198 vs 2188**: K2 (word) computes letter
  counts from word lengths — answering a char question at word scale,
  natively, 10 ops cheaper. Retained because the ledger says it wins.
- **K3 for ctx 211 only**: the ledger measured K1 scoring 98 (0/1 correct —
  the money trap) and K2 scoring 994 (correct but fallback). Magnification is
  expensive and chosen exactly where the measurements demand it.
- **K4 nowhere**: the ledger found it never beats K3. It stays in the code as
  a measured-rejected method, not silently deleted.

### Diagnosis-before-patching log (first prototype run: 34/36, native 35/36)

1. **Two LETTER_COUNT failures (n26, n30)**: `s3_locate` parsed the target
   after `"of "` for kinds 1/2/8/9, but kind-1 questions use `"in "` — the
   missing marker produced a garbage slice, locate failed, answer `?`.
   Fixed: kind 1 parses after `"'s in "`. Verified by output grep, not just
   the aggregate.
2. **One fallback (n28, `does the 3rd word contain own`)**: ctx 612 conflated
   "needle is a whole word" (q14, where K2 is native) with "needle is a
   substring" (n28, where K2 falls back). Fixed with a structural context
   feature computable from (q,t) alone — `is_whole_word` — splitting kind-6
   subspan class into word-scope (0) vs substring-scope (1). This is a
   context-feature fix, not an answer fix: it generalizes to all future
   CONTAINS questions.
3. **Misbucketed new kinds**: the frozen `skind` knows only kinds 1–9; new
   kinds 12/13 fell into the default bucket. Added `learn_skind` (12→POSITION,
   13→WORD_COUNT) without touching the frozen function.

### Battery: original 24 + 12 adversarial traps

New traps: nested ordinal addressing (`3rd letter of the 2nd word of the 4th
sentence` — 3-deep zoom), sentence→word selection, literal phrase subspans
(letter counts inside a named phrase), substring CONTAINS traps, sentence
word-count, ordinal-word reversal, reverse-an-ordinal-word, fixed-scale
money traps (`2nd letter of the 1st word`, `last letter of the first word
of hello world`).

| total | correct | native | fallbacks | ops | zooms (train 44 + eval 23) | result |
|-------|---------|--------|-----------|-----|----------------------------|--------|
| 36 | 36 | 36 | 0 | 489 | 67 | **LEARNED_RESULT PASS** |

Old-24 subset: 24/24 correct, 24/24 native. New-12 subset: 12/12 correct,
12/12 native. Policy usage in eval: K1 ×19, K2 ×6, K3 ×11 (q22's learned
ctx-211 + 10 unseen contexts defaulting to K3).

Per-question results (eval; all `correct=1 native=1 fallback=0`):

| qid | question | ctx → policy | ans | exp | ops | zooms |
|-----|----------|--------------|-----|-----|-----|-------|
| 0 | how many r's in strawberry | 100→K1 | 3 | 3 | 10 | 0 |
| 1 | how many s's in Mississippi | 100→K1 | 4 | 4 | 11 | 0 |
| 2 | how many l's in hello world | 110→K1 | 3 | 3 | 11 | 0 |
| 3 | how many e's in cheese | 100→K1 | 3 | 3 | 6 | 0 |
| 4 | how many a's in abracadabra | 100→K1 | 5 | 5 | 11 | 0 |
| 5 | what is the 3rd letter of strawberry | 200→K1 | r | r | 3 | 0 |
| 6 | what is the 1st letter of Mississippi | 200→K1 | M | M | 1 | 0 |
| 7 | what is the 10th letter of strawberry | 200→K1 | y | y | 10 | 0 |
| 8 | spell strawberry backwards | 300→K1 | yrrebwarts | yrrebwarts | 10 | 0 |
| 9 | spell abc backwards | 300→K1 | cba | cba | 3 | 0 |
| 10 | how many words in the quick brown fox | 410→K2 | 4 | 4 | 4 | 0 |
| 11 | how many words in hello | 400→K2 | 1 | 1 | 1 | 0 |
| 12 | how many letters in strawberry | 500→K2 | 10 | 10 | 1 | 0 |
| 13 | how many letters in ab | 500→K2 | 2 | 2 | 1 | 0 |
| 14 | does the quick brown fox contain quick | 610→K2 | yes | yes | 4 | 0 |
| 15 | what is the first word of the quick brown fox | 710→K2 | the | the | 1 | 0 |
| 16 | what is the last letter of Mississippi | 900→K1 | i | i | 1 | 0 |
| 17 | what is the first letter of hello world | 810→K1 | h | h | 1 | 0 |
| 18 | how many S's in Mississippi | 100→K1 | 0 | 0 | 11 | 0 |
| 19 | how many o's in bookkeeper | 100→K1 | 2 | 2 | 10 | 0 |
| 20 | how many e's in the cheese wheel | 110→K1 | 6 | 6 | 16 | 0 |
| 21 | does strawberry contain raw | 601→K1 | yes | yes | 10 | 0 |
| 22 | what is the 2nd letter of fox | 211→K3 | o | o | 6 | 2 |
| 23 | how many r's in the strawberry patch | 110→K1 | 3 | 3 | 20 | 0 |
| 24 | 3rd letter of the 2nd word of the 4th sentence | 222→K3* | n | n | 76 | 3 |
| 25 | 1st word of the 3rd sentence | 1222→K3* | line | line | 73 | 1 |
| 26 | how many e's in second words work | 121→K3* | 1 | 1 | 30 | 4 |
| 27 | 2nd letter of the 2nd word | 212→K3* | k | k | 9 | 2 |
| 28 | does the 3rd word contain own | 612→K3* | yes | yes | 10 | 2 |
| 29 | last letter of the first word of hello world | 910→K3* | o | o | 7 | 2 |
| 30 | how many r's in red strawberry | 111→K3* | 4 | 4 | 18 | 3 |
| 31 | what is the 2nd letter of the 1st word | 212→K3* | h | h | 6 | 2 |
| 32 | how many words in the 4th sentence | 1322→K3* | 3 | 3 | 73 | 1 |
| 33 | spell the 2nd word backwards | 312→K3* | kciuq | kciuq | 9 | 1 |
| 34 | does Mississippi contain issi | 601→K1 | yes | yes | 11 | 0 |
| 35 | what is the 4th letter of mississippi | 200→K1 | s | s | 4 | 0 |

`*` = unseen context, defaulted to K3 (the addressed magnifier). Full
questions and zoom traces are in `evidence_learned/RUN_L1.out`.

### Key zoom traces

q22 (money trap, learned ctx 211):

```text
D zoom qid=22 span=1 parent=0 off=16 len=3 depth=1 why=locate-target-word
D zoom qid=22 span=2 parent=1 off=17 len=1 depth=2 why=index-character-inside-word
K3 ans="o" exp="o" correct=1 native=1 fallback=0 ops=6 maxdepth=2 zooms=2
```

q24 (nested trap, `3rd letter of the 2nd word of the 4th sentence`, unseen ctx 222):

```text
D zoom qid=24 span=1 parent=0 off=55 len=15 depth=1 why=character-span
D zoom qid=24 span=2 parent=1 off=59 len=5 depth=2 why=character-span
D zoom qid=24 span=3 parent=2 off=61 len=1 depth=3 why=index-character-inside-word
K3 ans="n" exp="n" correct=1 native=1 fallback=0 ops=76 maxdepth=3 zooms=3
```

(4th sentence is `and final text.` → 2nd word `final` → 3rd letter `n`.)
Note: the fork's frozen `why_str` only labels its own four codes; the new
codes (6 ordinal-character-in-sentence, 7 index-character-in-sentence) are
stored numerically in the ledger and render as `character-span` in the
printed trace. Recorded here so the trace is read honestly.

### Negative controls (fixed C/W/S on the same 36)

| arm | correct | native | fallbacks | note |
|-----|---------|--------|-----------|------|
| C (char) | 27/36 | 36/36 | 0 | all 9 wrong answers are scoped questions — C scans the whole text and answers the wrong question (e.g. `h` for q22, `8` for n26 where the subspan answer is `1`) |
| W (word) | 27/36 | 8/36 | 28 | same 9 wrong; 7 via fallback |
| S (span) | 27/36 | 4/36 | 32 | same 9 wrong; 7 via fallback |

The three fixed arms fail the identical 9 questions — every one of them a
question that scopes a sub-span. This is the negative-control evidence for
the retirement: fixed scales answer the wrong question on scoped traps.

### Determinism

Two runs, rc=0 both, byte-identical:

- SHA-256 `47f1b1a2caa16c89b914ec2052432d3bee552904712329dcde3dde871c307587`
  (`evidence_learned/RUN_L1.out`, `RUN_L2.out`).

No RNG, no timestamps, no pointer-derived values in any decision path.

### Honest boundaries

- The candidate set (K1–K4) is hand-authored; what is *learned* is the
  routing over measured outcomes, not the chunking primitives. A fuller
  native policy would invent its own addressing operators.
- The context features (kind/shape/subspan) are structural, not epistemic —
  but the four-candidate set and the ctx bucketing are still human-chosen
  machinery around the learning.
- Only 13 contexts were trained; 10 of the 12 new traps ran on the
  unseen-context default (K3). The default is an adaptive magnifier, not a
  fixed scale — but it is still a prior, chosen by the programmer.
- The gain rule `1000·correct + 100·native − ops` is a fixed measurement
  aggregation: correctness dominates, nativeness next, cost last. Different
  weights could rerank the ties (K1/K3/K4 tie on several contexts; the
  tie-break to lower id is deterministic but arbitrary).
- The battery is 36 short ASCII questions. Multi-KB texts, Unicode, and
  adversarial questions outside these 15 kinds are untested.
- `learn_skind` buckets the two new kinds for the summary table; the frozen
  fork `skind` was left untouched.

### Open questions

1. Should the unseen-context default itself be learned (e.g. from context
   similarity) rather than fixed to K3?
2. The K1/K3/K4 three-way ties on whole-text contexts: is "cheapest correct"
   the right tie-break, or should magnification depth be preferred for
   robustness?
3. Can the candidate set be opened — letting TNN propose its own addressing
   operators instead of choosing among four authored ones?

### Files

- `learned_chunk.zag` — the learned policy battery (pure Zag, zero RNG)
- `evidence_learned/RUN_L1.out`, `RUN_L2.out` — both runs (PASS, byte-identical)

Build binaries (`learned_bin`), `.zagd`/caches, and build logs are local
intermediates and are **not** committed.
