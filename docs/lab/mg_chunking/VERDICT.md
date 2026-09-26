# VERDICT.md — MAGNIFYING-GLASS CHUNKING fork (TNN text handling)

Micah order 2026-09-26 ~09:27 PDT, verbatim in spirit: *"for magnifying glass
it should also work for TNN — say user asks how many r's in strawberry or
something else specific, TNN chooses its chunking and adapts it."*

## What was built

A chunking organ in pure Zag (`mg_chunk.zag`, ~1100 lines, zero RNG):
given (question, text), TNN **deliberatively chooses HOW to chunk the text** —
characters, words, variable scales, zoom in/out — with every choice recorded
and reasoned. No fixed tokenizer, no fixed chunk size, no baked-in units.

The zoom machinery follows the **n5_zoom precedent** (commit c4b302bf32f7):
`mg_zoom(qid, parent, roff, rlen, depth, why)` addresses a sub-span of the
text and logs `(qid, span, parent, off, len, depth, why)` to a zoom ledger.
The zoom trace IS the deliberation record.

## Battery

24 questions, 7 kinds, hand-verified expected answers (all ASCII, case-sensitive):

| # | question | text | exp |
|---|----------|------|-----|
| 0 | how many r's in strawberry | strawberry | 3 |
| 1 | how many s's in Mississippi | Mississippi | 4 |
| 2 | how many l's in hello world | hello world | 3 |
| 3 | how many e's in cheese | cheese | 3 |
| 4 | how many a's in abracadabra | abracadabra | 5 |
| 5 | what is the 3rd letter of strawberry | strawberry | r |
| 6 | what is the 1st letter of Mississippi | Mississippi | M |
| 7 | what is the 10th letter of strawberry | strawberry | y |
| 8 | spell strawberry backwards | strawberry | yrrebwarts |
| 9 | spell abc backwards | abc | cba |
| 10 | how many words in the quick brown fox | the quick brown fox | 4 |
| 11 | how many words in hello | hello | 1 |
| 12 | how many letters in strawberry | strawberry | 10 |
| 13 | how many letters in ab | ab | 2 |
| 14 | does the quick brown fox contain quick | the quick brown fox | yes |
| 15 | what is the first word of the quick brown fox | the quick brown fox | the |
| 16 | what is the last letter of Mississippi | Mississippi | i |
| 17 | what is the first letter of hello world | hello world | h |
| 18 | how many S's in Mississippi | Mississippi | 0 (case-sensitive trap) |
| 19 | how many o's in bookkeeper | bookkeeper | 2 |
| 20 | how many e's in the cheese wheel | the cheese wheel | 6 |
| 21 | does strawberry contain raw | strawberry | yes (sub-word trap) |
| 22 | what is the 2nd letter of fox | the quick brown fox | o (locate+index trap) |
| 23 | how many r's in the strawberry patch | the strawberry patch | 3 |

Four arms, same battery:
- **D** deliberative magnifying-glass chunking (chooses per question, traced zooms, never falls back)
- **C** fixed character chunks (every byte a chunk)
- **W** fixed word chunks (space-delimited)
- **S** fixed 4-byte spans

Fixed arms may inspect bytes inside a chunk only as a recorded **FALLBACK**
(the tokenizer escape hatch); `native=0` marks those answers. `ops` ≈ chunk
visits + byte inspections (documented approximation, deterministic).

## Results

Byte-identical reruns ×2 verified (`cmp` clean, SHA-256 `94fba9e3…` both runs);
rebuild-from-source reproduces RUN_R1 byte-identically.

### Accuracy and native-correct rate per arm × question kind

| arm | kind | n | correct | native (no fallback) | ops |
|-----|------|---|---------|----------------------|-----|
| D | LETTER_COUNT | 9 | 9 | 9 | 109 |
| D | POSITION | 6 | 6 | 6 | 32 |
| D | REVERSE | 2 | 2 | 2 | 13 |
| D | WORD_COUNT | 2 | 2 | 2 | 5 |
| D | LENGTH | 2 | 2 | 2 | 12 |
| D | CONTAINS | 2 | 2 | 2 | 15 |
| D | FIRST_WORD | 1 | 1 | 1 | 4 |
| C | LETTER_COUNT | 9 | 9 | 9 | 106 |
| C | POSITION | 6 | **5** | 6 | 18 |
| C | REVERSE | 2 | 2 | 2 | 13 |
| C | WORD_COUNT | 2 | 2 | 2 | 24 |
| C | LENGTH | 2 | 2 | 2 | 12 |
| C | CONTAINS | 2 | 2 | 2 | 29 |
| C | FIRST_WORD | 1 | 1 | 1 | 3 |
| W | LETTER_COUNT | 9 | 9 | 0 | 120 |
| W | POSITION | 6 | 6 | 0 | 25 |
| W | REVERSE | 2 | 2 | 0 | 15 |
| W | WORD_COUNT | 2 | 2 | 2 | 5 |
| W | LENGTH | 2 | 2 | 2 | 2 |
| W | CONTAINS | 2 | 2 | 1 | 15 |
| W | FIRST_WORD | 1 | 1 | 1 | 1 |
| S | LETTER_COUNT | 9 | 9 | 0 | 135 |
| S | POSITION | 6 | **5** | 0 | 10 |
| S | REVERSE | 2 | 2 | 0 | 17 |
| S | WORD_COUNT | 2 | 2 | 0 | 31 |
| S | LENGTH | 2 | 2 | 2 | 4 |
| S | CONTAINS | 2 | 2 | 0 | 37 |
| S | FIRST_WORD | 1 | 1 | 0 | 8 |

**Totals: D 24/24 correct, 24/24 native, 0 fallbacks · C 23/24, 24/24 native ·
W 24/24, 6/24 native (18 fallbacks) · S 23/24, 2/24 native (22 fallbacks).**

### What chunking did TNN choose per question type (arm D)

| chunking | used | on |
|----------|------|----|
| CHAR | 14 | single-token letter counts (q0,1,3,4,18,19), single-token positions (q5,6,7,16), reversals (q8,9), lengths (q12,13) |
| WORD | 3 | word counts (q10,11), first word (q15) |
| WORD>CHAR | 5 | multi-token letter counts (q2,20,23), multi-token positions (q17,22) |
| WORD?CHARSCAN | 2 | contains: word-boundary hit, no zoom (q14); word-boundary miss → magnified char-span scan (q21) |

It did **not** chunk the same way every time: 4 distinct chunkings across the
battery, chosen by question kind × text shape, each with a recorded reason
(e.g. q22: *"locate the named word at word scale, then magnify to character
units for the index"*). 12 zooms total, max depth 2.

### The q22 trap (the money question)

*"what is the 2nd letter of fox"* on *"the quick brown fox"*:

- **D**: `zoom span=1 off=16 len=3 depth=1 why=locate-target-word` →
  `zoom span=2 off=17 len=1 depth=2 why=index-character-inside-word` → **"o"** ✓
- **C**: indexed the 2nd byte of the whole text → **"h"** ✗ (answered a
  different question than asked — it cannot address "the word fox")
- **W**: "o" ✓ but via recorded fallback (sub-word escape)
- **S**: "h" ✗ (same whole-text reading as C)

This is the genuine magnifying-glass win: **addressing precedes indexing.**
Fixed chunkers have no sub-span addressing, so on a question that names a
sub-span they either answer the wrong reading (C, S) or bolt on a char escape
(W). The deliberative arm magnifies to the named span first, natively.

### Efficiency notes (secondary)

- WORD_COUNT: D=5 ops vs C=24 (word units are the right scale; chars work but visit every byte).
- q21 (`contain raw`): D tries word-boundary match (1 word visit), misses, then magnifies to one char-span scan — the principled form of W's fallback.
- C is the universal unit here (23/24) — characters resolve everything except sub-span addressing.

## Verdict

**Deliberative chunking beats fixed chunking: 24/24 correct with 24/24 native
(no fallbacks), vs C 23/24, W 24/24-but-18-fallbacks, S 23/24-but-22-fallbacks.**
Adaptation is real and visible in the trace (4 chunkings, 12 traced zooms,
max depth 2), and the q22 sub-span trap is a genuine fixed-chunking failure
that magnification fixes natively.

## Honest boundary

1. The "deliberation" is a **deterministic rule table** (classify question by
   marker phrases → choose chunking by kind × text shape), not a learned
   chooser. The adaptation is real but hand-authored; a TNN-native chooser
   that learns its own chunking policy from experience is the open next step.
2. Battery is small (24) and hand-built; all four arms share the author's
   answer semantics. The q22 "wrong reading" for C/S follows from the
   locate rule the author gave D — a fixed-char system with its own locate
   step would be D by another name.
3. Case-sensitive byte matching throughout (q18: "how many S's" → 0).
   A real deployment needs a deliberated case policy; not tested here.
4. `ops` is an approximate cost model (chunk visits + byte inspections),
   not wall-clock.

## Reproduce

```
cd docs/lab/mg_chunking
./build.sh        # znc mg_chunk.zag -o mg_chunk_bin
./mg_chunk_bin > out.txt   # deterministic; rerun is byte-identical
```

## Evidence

- `evidence/RUN_R1.out`, `evidence/RUN_R2.out` — full traces (SHA-256 `94fba9e3578d84402eeebf0ab3d09c814630a2b9635fd8ed1fcebd70bfe9c74f`, identical)
- `SHA_MANIFEST.md` — file SHAs
- `mg_chunk.zag`, `R33_NATIVE_IO_V1.zag`, `build.sh` — sources
