# FACTSPEC.md — Frozen fact spec (SCALE corpus, 2026-09-21)

This document is FROZEN. Categories, id layout, vmin/vmax, and the falsehood
rule may not change without a dated amendment and full artifact regeneration.
Everything is integer-valued and deterministic; no randomness is used.

## 1. Fact id layout

For a scale parameter `M` (positive integer):

```
N = 24 * M                                  # total facts
id = c * M + i,   c in [0, 24), i in [0, M)
c = id // M,      i = id % M
```

**Word-level** categories (c = 0..15): `t = i % 10`, `k = (i // 10) % W_t`,
where `W_t` = word count of text `t`. The fact concerns `words_t[k]`.

**REQUIREMENT:** `M <= 10 * min_t(W_t)`. With `min_t(W_t) = 27439` (text 3,
Alice), the maximum feasible M is **274390**. The requirement guarantees
`(i // 10) < W_t` for all `i < M`, i.e. the `% W_t` never wraps and every
word-level id maps to a distinct `(t, k)` pair. `materialize.py` and
`verify_fact.py` assert this and refuse otherwise.

**Text-level** categories (c = 16..23): `t = i % 10`; `k` is unused and
recorded as `-1` in materialized rows.

## 2. Normalization reference

All word/sentence/paragraph notions are exactly those of `NORMALIZE.md`
(ASCII-only lowercase; words = maximal `[a-z]+` runs; sentences = maximal
spans terminated by `[.?!]` runs; paragraphs = maximal runs of non-blank
lines). Vowels are `aeiou` (ASCII, after lowercasing). `a=1 … z=26` is the
alphabetical index (`ord(c) - ord('a') + 1`).

## 3. Categories

| c | name | definition | vmin | vmax |
|---|------|------------|------|------|
| 0 | word_len | `len(word)` | 1 | 20 |
| 1 | alpha_first | alphabetical index of first letter | 1 | 26 |
| 2 | alpha_last | alphabetical index of last letter | 1 | 26 |
| 3 | vowel_count | # of `[aeiou]` chars in word | 0 | 20 |
| 4 | consonant_count | `len(word) - vowel_count` | 0 | 20 |
| 5 | vowel_groups | # of maximal `[aeiou]+` runs ("syllable estimate") | 0 | 20 |
| 6 | distinct_letters | # of distinct chars in word | 1 | 26 |
| 7 | word_mod97 | `H = Σ_{j=0}^{L-1} ord(word[j])·31^j`, value `H mod 97` (ord = ASCII code of the lowercase letter, j 0-based from first letter; exact big-int arithmetic) | 0 | 96 |
| 8 | sent_len_words | # words in the word's sentence | 0 | 401 |
| 9 | sent_pos_in_sentence | 0-based position of the word within its sentence | 0 | 400 |
| 10 | para_len_words | # words in the word's paragraph | 1 | 2687 |
| 11 | para_len_sents | # sentences attributed to the word's paragraph (`sent_para`; may be 0 — see NORMALIZE.md §5) | 0 | 134 |
| 12 | word_len_next | `len(words[k+1])`, or `0` if `k` is the last word | 0 | 20 |
| 13 | word_len_prev | `len(words[k-1])`, or `0` if `k == 0` | 0 | 20 |
| 14 | freq_in_text | occurrences of the exact spelling in text `t` | 1 | 14537 |
| 15 | is_long | `1` if `len(word) > 8` else `0` | 0 | 1 |
| 16 | text_words | `W_t` | 27439 | 219066 |
| 17 | text_sents | `S_t` | 1655 | 10831 |
| 18 | text_paras | `P_t` | 799 | 4117 |
| 19 | text_unique_words | # distinct word spellings in text `t` | 2579 | 16957 |
| 20 | text_longest_word | max word length in text `t` | 1 | 20 |
| 21 | text_avg100 | `floor(100 · total_letters_t / W_t)`, `total_letters_t = Σ len(word)` | 100 | 2000 |
| 22 | pub_year | publication year from `texts/meta.json` | 1600 | 2000 |
| 23 | title_words | # whitespace-separated tokens in the catalog title (`meta.json`) | 1 | 16 |

Corpus-derived constants (from `texts/index_stats.json`, frozen with this
spec): `W_MAXLEN=20`, `S_MAXLEN=401`, `P_WORDMAX=2687`, `P_SENTMAX=134`,
`FREQMAX=14537`, `WTEXTMAX=219066`, `STEXTMAX=10831`, `PTEXTMAX=4117`,
`UMAX=16957`, `MIN_W=27439`. Every `vmax` above is ≥ every truth in the
corpus; every `vmin` is ≤ every truth. All categories satisfy `vmax > vmin`
(required by the distractor rule).

Notes:
- Categories 0–21 are mechanically recomputable from the text bytes alone
  (bytes → NORMALIZE.md → index → formula).
- Categories 22–23 additionally depend on `texts/meta.json`
  (title/author/year from the Project Gutenberg catalog — see meta.json
  `title_source`). This is the spec's one non-bytes input, recorded
  explicitly.
- c8 `vmin=0`: a sentence may contain zero words (punctuation-only span).
- c9 `vmax=400 = S_MAXLEN − 1`: `sent_pos ≤ sent_len_words − 1 ≤ 400`.
- c11 `vmin=0`: a paragraph can sit mid-sentence (see NORMALIZE.md §5).
- c14 counts exact spellings (already lowercased words), including the PG
  header/footer text, which is part of the bytes.

## 4. Planted falsehoods (championship convention)

Learners train on **supplied** values; evaluation scores against **truth**.
Exactly the false ids (deterministic, ~5%) carry a wrong-but-in-range
supplied value.

splitmix64 (standard, 64-bit), used as a **seeded stream**:

```
MASK64 = 2^64 − 1
GOLDEN = 0x9E3779B97F4A7C15
mix(state):                              # one mixing round
    x = (state + GOLDEN) mod 2^64
    z = x
    z = ((z xor (z >> 30)) · 0xBF58476D1CE4E5B9) mod 2^64
    z = ((z xor (z >> 27)) · 0x94D049BB133111EB) mod 2^64
    return (z xor (z >> 31))              # in [0, 2^64)
draw(seed, idx):                         # idx-th output, 0-based
    return mix((seed + (idx + 1)·GOLDEN) mod 2^64)
```

i.e. the standard splitmix64 generator semantics (`state = seed`; each draw
increments the state by GOLDEN, then mixes). `draw(20260921, id)` is the
frozen meaning of "splitmix64(seed=20260921, id)" in this spec.

- `is_false(id)` ⟺ `draw(20260921, id) mod 100 < 5`.
- For false ids, with `R = vmax − vmin` (per the fact's category, `R ≥ 1`):
  ```
  r        = draw(20260921, id xor 0x9E37)     # independent stream position
  supplied = vmin + ((truth − vmin + 1 + (r mod R)) mod (R + 1))
  ```
  For true ids, `supplied = truth`.
- Guarantee: `supplied ∈ [vmin, vmax]` and `supplied ≠ truth` for false ids,
  because the added offset `1 + (r mod R)` lies in `[1, R]`, so
  `(truth − vmin + offset) mod (R+1) ≠ (truth − vmin)`.

Design note (frozen): the naive state choice `mix(seed + id)` yields a
4.125% false rate over the M=100 id range (a ~2σ low draw), violating the
mandated 5% ± 0.3pp gate (§7). The stream-draw reading above uses the same
seed (20260921), the same `< 5` rule, and the canonical splitmix64 stream
semantics; it yields 114/2400 = 4.750% at M=100 (inside the gate) and
5.015% at M=10000. The seed, rule, and gate are all satisfied
simultaneously only under this reading, which is therefore the frozen one.

## 5. Materialization policy

- `corpus_m10.json` (N=240) and `corpus_m100.json` (N=2,400): full
  truth+supplied tables. Row: `{id, c, i, t, k, truth, supplied, is_false}`.
  Top-level `false_ids`: sorted list of false ids.
- M = 1000 / 10000 / larger: NOT materialized (would be GBs at the top end:
  M=274390 → 6.58M facts). Any single id at any feasible M is recomputable on
  demand with `python3 verify_fact.py --id ID --M M`.
