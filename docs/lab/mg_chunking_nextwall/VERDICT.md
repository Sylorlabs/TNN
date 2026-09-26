# NEXT-WALL VERDICT — frozen policy vs 26 never-seen traps (2026-09-26)

Plain-English verdict: **the frozen policy holds on everything inside its
derivation world and breaks, honestly, outside it.** 13 of 25 answered traps
correct, 12 missed, 1 trap crashed the binary. Every break traces to a named
mechanism below — none required re-derivation to explain.

## Score

| | n |
|---|---:|
| Traps | 26 |
| Answered | 25 |
| Correct | **13** |
| Missed | 12 |
| Crashed (panic, deterministic) | 1 (W25) |

WALL1.out / WALL2.out SHA-256 (byte-identical reruns, panic included):
`791f5e95ccc0b3da44df0d41bcacb4b0ead3712f6515585bbcdb7b2ddeb234ad`
stderr (the panic) likewise byte-identical:
`1c5a18d5dca549602929ec030d23bbe0735c7d97c7caee2f36bc28a27c1e94f0`

## Where it holds (13)

| Trap | What held |
|---|---|
| W09 (cross-word "ick bro") | **Adaptation worked**: word-boundary match failed, the WORD?CHARSCAN candidate magnified to a character-span scan and found "ick bro" across "quick brown", with a real zoom trace. The flagship adaptation case. |
| W10, W11, W13 | Clean "no" on misses, needle-longer-than-text, text-shorter-than-needle. |
| W12, W14 | Degenerate inputs: empty-text word count = 0, zero-count letter = 0. |
| W15 | Case sensitivity: 's' in "MISSISSIPPI" = 0. |
| W16 | Whole-word matching: "issi" is not a word in "mississippi" -> "no". |
| W20 | Doubled spaces / padded text: word count 3. |
| W21 | Leading-space text + clamp: 3rd letter of " ab" = 'b' (whole-text match path). |
| W22 | Digit target: three 7's counted. |
| W23, W24 | Clamp edges follow the code's own convention (0th -> last char, 10th of 3 -> last char). |

## Where it breaks (12 + 1 crash), by cause

### Parser / classifier failures (question never understood)

| Trap | Mechanism |
|---|---|
| W00, W01, W02 | "sentences"/"lines" -> kind 0 (unclassified). The classifier has no sentence or line concept; defaulted to WORD and answered empty. |
| W19 | "2nd word of the 1st sentence" -> kind 0. Sentence->word hybrid addressing doesn't exist. |
| W07 | "the **second** letter" -> kind POSITION ok, but `parse_pos_n` only reads digits; "second" parsed as 0, clamped to index 0 -> 's' instead of 't'. Spelled ordinals outside parser vocabulary. |
| W08 | "the **third** word" -> kind LENGTH_WORD ok, but the word reference "third" parsed as 0 -> no word -> '?'. Same vocabulary gap. |
| W05 | "the word **before** fox" -> kind FIRST_LETTER_WORD, but `parse_wordref` only understands "the Nth/last word of"; no "word of" present -> '?'. Relative word addressing unsupported. |
| W04 | "e's in the word **after** the" -> kind LETTER_COUNT, no relative addressing, so it counted over the whole text (6) instead of "cheese" (3). Same gap as W05. |
| W03 | "the letter **after** the 2nd letter of fox" -> kind POSITION; `zoom_locate` takes everything after "of " literally ("fox in the quick brown fox") and finds nothing -> '?'. Two-hop relative addressing unsupported. |

### Addressing / nesting failures (parsed, resolved wrong)

| Trap | Mechanism |
|---|---|
| W17 | "2nd letter of **the**" with "the" x3 in text. `zoom_locate` takes the whole tail after "of " ("the in the quick brown the fox") as one literal and matches nothing -> '?'. No occurrence selection among repeats. |
| W18 | "1st letter of the 2nd word of the last word of ..." (designed unanswerable). `parse_wordref` resolves exactly ONE "word of" level ("worldly" = 2nd word) and silently drops the deeper nesting -> answered 'w' instead of abstaining. Single-level addressing. |
| W06 | "spell the word after quick **backwards**" -> kind REVERSE, but the only reverse machinery is whole-text reversal -> reversed the whole string. No word-scoped reverse candidate was ever derived (derivation battery had none). Finite candidate set + addressing. |

### Robustness break (crash)

| Trap | Mechanism |
|---|---|
| W25 | "1st letter of" over EMPTY text -> kind POSITION, `zoom_locate` returns a zero-length span, index clamps to -1, `t[-1]` -> **panic: slice index out of bounds**. Deterministic, byte-identical across runs. The position path has no degenerate-input guard (the WORD>CHAR kind-12 path has one; kind 2/8/9 do not). |

## The honest conclusion

The policy is a **measured winner inside its derivation world** — 57/57 there,
13/13 here on every trap that stays inside that world (degenerate inputs, case,
clamps, cross-word adaptation). Outside it, the breaks are all in the
hand-designed parts the derivation never touched: the parser's vocabulary
(sentences, lines, spelled ordinals, relative addressing), the single-level
addressing, and the finite candidate set. **Nothing here shows the system
inventing its own chunking or structure at runtime** — when the question leaves
the authored world, the system applies the frozen machinery and fails in
exactly the ways the frozen machinery predicts. The wall stands; the next work
is the parser/addressing layer, per the alignment direction that TNN should one
day invent its own structure.

## Files

- `battery2.zag` — frozen 26-trap battery (runs through the committed production intake).
- `gen_wall.py` — generator; oracles asserted before the first run (see PREREG.md).
- `PREREG.md` — preregistered traps, oracles, and reporting duties.
- `build.sh` — repo-relative build + verification.
- `evidence/WALL1.out`, `evidence/WALL2.out` — the two byte-identical runs (W25 panic included).
- `SHA_MANIFEST.md` — checksums.
