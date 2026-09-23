# NORMALIZE.md — Frozen normalization spec (SCALE corpus, 2026-09-21)

This document is FROZEN. Any change requires a dated amendment and re-derivation
of every downstream artifact (indexes, corpora, manifests). All steps are
deterministic; no randomness is used anywhere.

## 0. Input

- Raw bytes of each text file `texts/text_<t>.txt` (t = 0..9), exactly as
  downloaded from Project Gutenberg (no header/footer stripping — the PG
  license header and footer are part of the bytes).
- Decode: UTF-8, strict. (All 10 source files are UTF-8; a decode failure is a
  build error, not a fallback case.)
- Let `S` be the resulting Unicode string of length `N` code points.
  **Char offsets** below are 0-based indices into `S` (Python `str` indexing).

## 1. Lowercasing (ASCII-only)

`low[i] = chr(ord(S[i]) + 32)` if `'A' <= S[i] <= 'Z'`, else `S[i]`.

Rationale: a full Unicode `lower()` can change string length
(e.g. U+0130 → two code points), which would move char offsets. The ASCII-only
mapping is a 1:1 code-point mapping, so offsets are identical before and after.
Non-ASCII letters (é, ß, …) are NOT lowercased and act as word separators.

## 2. Words

A **word** is a maximal run of characters in `[a-z]` in the ASCII-lowercased
string. "Maximal" = cannot be extended left or right while staying in `[a-z]`.

- `words[0..W)` in document order; `W` = word count of the text.
- `word_start[k]` = char offset of the first character of `words[k]`.
- Word text is recovered as the maximal `[a-z]+` run starting at
  `word_start[k]` (equivalently `re.findall(r'[a-z]+', low)` in order).

Words have length ≥ 1 by construction.

## 3. Sentences

A **sentence** is a maximal span of text terminated by a sentence terminator.
Terminators are exactly the characters `.`, `?`, `!`.

Algorithm (single left-to-right pass over `S`, 0-based):

```
sents = []          # list of [start, end) char spans
start = 0
i = 0
while i < N:
    if S[i] in '.?!':
        j = i
        while j < N and S[j] in '.?!':
            j += 1
        sents.append([start, j])   # span includes the terminator run
        start = j
        i = j
    else:
        i += 1
if start < N:
    sents.append([start, N])      # trailing text with no terminator
```

Notes:
- A maximal run of terminators (e.g. `...`, `?!`) ends exactly one sentence;
  the run belongs to the sentence it terminates.
- Text before the first terminator is the first sentence.
- A sentence may contain zero words (e.g. a span consisting only of
  punctuation/whitespace). Its `sent_len_words` is then 0.
- Sentence spans partition `[0, N)`: every char offset, hence every word
  start, lies in exactly one sentence.

## 4. Paragraphs

- Split `S` on `'\n'` into lines (line `L` covers a char span; the `'\n'`
  itself belongs to no paragraph).
- A line is **blank** iff `line.strip() == ''` (empty or whitespace-only;
  a trailing `'\r'` therefore counts as blank — PG files use `\n`).
- A **paragraph** is a maximal run of ≥1 consecutive non-blank lines.
- `para_start[p]` = char offset of the first character of the first line;
  `para_end[p]` = char offset one past the last character of the last line
  (excluding the terminating newline).
- Every word start lies inside exactly one paragraph (a word cannot start on
  a blank line, and inter-paragraph newlines contain no letters).

## 5. Derived maps (stored per text in `index_<t>.tnix`)

- `word_sent[k]` = index of the sentence containing `word_start[k]`.
- `word_para[k]` = index of the paragraph containing `word_start[k]`.
- `sent_para[s]` = index of the paragraph containing `sent_start[s]`
  (a sentence may span paragraphs; it is attributed to the paragraph where
  it *starts*).
- `para_len_words[p]` = `count(k : word_para[k] == p)`.
- `para_len_sents[p]` = `count(s : sent_para[s] == p)` (may be 0: a paragraph
  can sit in the middle of a sentence that started in an earlier paragraph).
- `sent_len_words[s]` = `count(k : word_sent[k] == s)`.
- `sent_pos_in_sentence[k]` = `k - min{k' : word_sent[k'] == word_sent[k]}`
  (0-based position of the word within its sentence).

## 6. Binary index format (`index_<t>.tnix`, little-endian)

```
offset  size  field
0       8     magic = b'TNIX0001'
8       8     n_words  (u64)
16      8     n_sents  (u64)
24      8     n_paras  (u64)
32      4*n_words  word_start  (u32 each)
..      4*n_words  word_sent   (u32 each)
..      4*n_words  word_para   (u32 each)
..      4*n_sents  sent_start  (u32 each)
..      4*n_sents  sent_end    (u32 each)
..      4*n_sents  sent_para   (u32 each)
..      4*n_paras  para_start  (u32 each)
..      4*n_paras  para_end    (u32 each)
```

All offsets are char offsets into the decoded text `S`. A pure-Python reader
is `index_reader.py`; an independent re-derivation (regex-based) is
`indep_impl.py`. Both must agree byte-for-byte on every array (checked by
`sanity_check.py`).

## 7. Worked miniature example

Input (chars): `Hi!\n\nOk, go.\n` (N=11)

- Lowercased: `hi!\n\nok, go.\n`
- Words: `hi` @0, `ok` @5, `go` @9 → W=3
- Sentences: `[0,3)` = `hi!`, `[3,11)` = `\n\nok, go.\n`
  (terminator run `!` at 2..3 ends sentence 0; `.` at 10..11 ends sentence 1)
- Paragraphs: line 0 `hi!` [0,3), line 1 `` blank, line 2 `ok, go.` [5,10),
  line 3 `` blank → paragraphs `[0,3)`, `[5,10)` → P=2
- `word_sent` = [0,1,1]; `word_para` = [0,1,1]; `sent_para` = [0,1]
  (sentence 1 starts at char 3, which is the blank line — wait, char 3 is
  `\n`, the line boundary...)

Correction of the example: `sent_start[1] = 3`. Char 3 is `'\n'` (end of
line 0). Line 0 spans chars [0,3); char 3 is the newline itself, which belongs
to no paragraph per §4. **Refinement (frozen):** `sent_para[s]` = paragraph
containing `sent_start[s]`; if `sent_start[s]` falls on a newline or blank
line (belongs to no paragraph), scan forward to the first char that belongs
to a paragraph and use that paragraph; if none exists (trailing whitespace),
use the last paragraph. In the example, scanning forward from 3 reaches char 5
(`o`, paragraph 1) → `sent_para[1] = 1`.

## 8. Rebuild recipe

1. Fetch the 10 files from the exact URLs recorded in `texts/meta.json`
   (`source_url` per text); verify SHA-256 against `SHA256SUMS.txt`.
2. Run `python3 build_index.py` → regenerates `index_<t>.tnix` (byte-identical).
3. `python3 materialize.py --M 10` / `--M 100` → regenerates the corpora.
4. `python3 sanity_check.py` → 2000/2000 independent agreement required.
