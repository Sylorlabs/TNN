# REPRO.md — WE-09: exact mechanism of the miss

## The failing turn (frozen battery, commit `9263c90ec78d`)

- **Query:** `i'm curious about the birth year of the guy who wrote the martian`
- **Expected:** `Andy Weir was born in 1972.`
- **Got:** `Andy Weir wrote The Martian.`

## Stage-by-stage trace (confirmed by byte-exact Python mirror, `mirror.py`)

The turn takes the default path in `do_turn` (step 5: reference resolution +
v1 retrieval). `do_compose` does not trigger (no branch matches);
`extract_assert` is not reached (the turn has no `?`... actually the turn
DOES go to path 5 because `do_compose` returns 0 and the `?` check sends
questions to path 5).

### Stage 1 — keyword extraction (`proc_token` → `stem_inplace`)

Query tokens after stopword removal: `i, m, curious, about, birth, year,
guy, who, wrote, martian` (10 keywords; `curious`→`curiou` via the `s`-strip
rule; `the/of` are stopwords).

Relevant KB facts:
- fid 15 `Andy Weir wrote The Martian.` → `{andy, martian, weir, wrote}`
- fid 16 `Andy Weir was born in 1972.` → `{andy, born, weir}`
- fid 17 `The Martian was published in 2011.` → `{martian, publish}`

`stem_inplace` is a first-match-wins suffix stripper. It maps
`birth`→`birth` and `born`→`born`: **no rule bridges them** (the miss is
at the extraction stage — the morphology gap is real).

### Stage 2 — scoring (`retrieve`: best cross-multiplied Jaccard, tie → lower fid)

| fid | inter | union | score |
|---|---|---|---|
| 15 (WROTE) | {wrote, martian} = 2 | 12 | **0.1667 WINNER** |
| 17 (PUBLISHED) | {martian} = 1 | 11 | 0.0909 |
| 16 (BORN) | {} = 0 | 13 | 0.0000 |

The BORN fact scores **zero** — not low, zero. The WROTE fact wins on the
relative clause (`wrote the martian`) and is emitted verbatim.

### The verdict's root cause was incomplete

The trial verdict said: "The keyword core cannot bridge 'birth year' →
'born'." True, but insufficient. Simulating the bridge in the mirror
(birth→born, both sides):

| fid | inter | union | score |
|---|---|---|---|
| 15 (WROTE) | 2 | 12 | **0.1667 STILL WINS** |
| 16 (BORN) | {born} = 1 | 12 | 0.0833 |

**The bridge alone does not fix WE-09** (H2 confirmed). The query's
relative clause (`wrote the martian`, 2 overlaps) outscores the question
focus (`birth`, 1 overlap) under Jaccard. Worse: among BORN facts the
bridge creates a 4-way tie at 1/12, and tie→lower-fid would emit
*Herman Melville* (fid 1) — the wrong person entirely.

**WE-09 has two stacked causes:**
1. **Morphology gap** (extraction stage): `birth` ↛ `born`. Real, worth
   fixing on its own.
2. **Composition gap** (scoring stage): keyword Jaccard cannot distinguish
   the question focus ("birth year" — selects the relation) from the
   relative clause ("the guy who wrote the martian" — identifies the
   referent). No keyword-domain repair can fix this: every keyword the
   BORN fact shares with the query (`andy, weir, born`) is also shared by
   the WROTE fact, which additionally matches `wrote, martian`.

KB-M1: SATISFIED — the mirror reproduces the exact observed answer
(`Andy Weir wrote The Martian.`) via these two stages.
