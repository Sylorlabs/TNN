# ORACLE MANIFEST — native-authorship trial 1, fresh trap battery

- **Date sealed:** 2026-09-27
- **Prereg:** `docs/lab/native_authorship/PREREG.md` (frozen, commit `50fb8ff86e5a`)
- **Battery:** 26 fresh traps, authored by the independent battery-generator agent
  (P1a). The implementer (P1b) never saw the traps or oracles; it developed
  against the frozen 57-question production battery only.
- **Sealed oracle digest (SHA-256 of `oracles.txt` bytes): `57177f6e3f9772332bfe57ebeaf78dac27047d074dbe841da81afac52d4ad582`
- **Canonical per-trap bytes for the per-trap SHA-256 below:**
  `f"{idx:02d}|{tag}|{question}|{text}|{expected}"` encoded UTF-8 with REAL
  newlines (only trap E1 contains one, in question and text).

## Oracle-construction method

1. Each trap's expected answer was fixed by construction in the generator's
   authoring script from the question's plain reading (independent Python
   assertions, e.g. `"strawberry"[1] == "t"`, `"cheese".count("e") == 3`).
2. Validity was then checked MECHANICALLY: every trap was run through all 9
   production candidates (`cand_answer` c=1..9 from the frozen
   `docs/lab/mg_chunking_promote/intake.zag`) in isolated processes; a trap
   is valid iff >=1 candidate's answer equals the expected answer.
   Result: **26/26 valid** (see per-trap table). Oracle ceiling = 26.
3. No trap was selected, kept, or dropped on the basis of either arm's
   behavior. The frozen lookup (`tnn_intake`) was never executed on this
   battery during authoring.

## Oracle conventions (stated explicitly; both arms face the same oracle)

- **F6 strict indexing:** an index outside 1..len, or a question naming no
  ordinal at all, names no character. The strict candidates' `'?'` is
  correct; clampers that silently substitute an edge character are wrong.
  This is a genuine implemented difference between the 9 candidates.
- **E1 newline:** the machinery splits words on byte 32 only, so
  `"a\nb\nc"` is one word by machinery convention; oracle follows it.
- **D5 empty needle:** `find_sub(t, "")` returns 0 (vacuous presence),
  so `"does abc contain "` -> `yes` on every candidate.
- **D1 (W25 t[-1] class):** WORD, WORD>CHAR, WORD?CHARSCAN panic on empty
  text for kind 16 (negative word-table index); CHAR, REV_WORD, BOTH_ENDS,
  SPAN3, SPAN5, END_DIRECT refuse cleanly with `'?'`. The oracle is the
  clean refusal `'?'` — the trap tests exactly the prereg's
  'clean refusal, never a panic' requirement.

## Provenance

- `intake.zag` measured (frozen production, commit `e74271015`):
  SHA-256 `5a4e6789df98ba013dcaa06ff865604e93b887ed666827d82ec5db1db760b1bc`
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
- Harness: one Zag binary, `_zag_arg(1)`=trap idx, `_zag_arg(2)`=candidate,
  calling `cand_answer` directly; 26x9 isolated subprocess runs; the correct
  bit was read from the packed return (bit0 = answer == expected).
- Zero RNG anywhere in authoring or measurement. Deterministic.

## Per-trap oracles

| idx | tag | family | kind | question | text | expected | SHA-256 | correct candidates | panics |
|---|---|---|---|---|---|---|---|---|---|---|
| 00 | N1 | F1-novel-vocab | 1 | how many .'s in the cat sat. the dog ran. | the cat sat. the dog ran. | 2 | `38aee4e4787e34b9…` | BOTH_ENDS, CHAR, END_DIRECT, REV_WORD, SPAN3, SPAN5, WORD, WORD>CHAR, WORD?CHARSCAN | — |
| 01 | N2 | F1-novel-vocab | 2 | what is the 2nd (second) letter of strawberry | strawberry | t | `ac87c534892015cf…` | BOTH_ENDS, CHAR, END_DIRECT, REV_WORD, SPAN3, SPAN5, WORD, WORD>CHAR, WORD?CHARSCAN | — |
| 02 | N3 | F1-novel-vocab | 4 | how many words in the second sentence of the cat sat. the dog ran. | the cat sat. the dog ran. | 6 | `58c731424f515f25…` | BOTH_ENDS, CHAR, END_DIRECT, REV_WORD, SPAN3, SPAN5, WORD, WORD>CHAR, WORD?CHARSCAN | — |
| 03 | N4 | F1-novel-vocab | 1 | how many 0's in 101010 | 101010 | 3 | `428137f9d5a9fc52…` | BOTH_ENDS, CHAR, END_DIRECT, REV_WORD, SPAN3, SPAN5, WORD, WORD>CHAR, WORD?CHARSCAN | — |
| 04 | N5 | F1-novel-vocab | 1 | how many s's in APPLES | APPLES | 0 | `f6334a7836ff7665…` | BOTH_ENDS, CHAR, END_DIRECT, REV_WORD, SPAN3, SPAN5, WORD, WORD>CHAR, WORD?CHARSCAN | — |
| 05 | M1 | F2-multilevel | 12 | what is the 3rd letter of the 2nd word of alpha beta gamma delta | alpha beta gamma delta | t | `dd089e1199b07569…` | BOTH_ENDS, CHAR, END_DIRECT, REV_WORD, SPAN3, SPAN5, WORD, WORD>CHAR, WORD?CHARSCAN | — |
| 06 | M2 | F2-multilevel | 10 | how many e's in the 2nd word of the cheese wheel | the cheese wheel | 3 | `97a5013b7f1a4224…` | BOTH_ENDS, CHAR, END_DIRECT, REV_WORD, SPAN3, SPAN5, WORD, WORD>CHAR, WORD?CHARSCAN | — |
| 07 | M3 | F2-multilevel | 17 | does the 2nd word of abc def contain bcd | abc def | no | `a38e2820faa3f0b7…` | BOTH_ENDS, CHAR, END_DIRECT, REV_WORD, SPAN3, SPAN5, WORD, WORD>CHAR, WORD?CHARSCAN | — |
| 08 | M4 | F2-multilevel | 13 | spell the 2nd word of abc def backwards | abc def | fed | `23f77146226edc38…` | BOTH_ENDS, CHAR, END_DIRECT, REV_WORD, SPAN3, SPAN5, WORD, WORD>CHAR, WORD?CHARSCAN | — |
| 09 | M5 | F2-multilevel | 14 | what is the 1st letter of the last word of alpha beta gamma | alpha beta gamma | g | `685bc10b5491af42…` | BOTH_ENDS, CHAR, END_DIRECT, REV_WORD, SPAN3, SPAN5, WORD, WORD>CHAR, WORD?CHARSCAN | — |
| 10 | L1 | F3-longer-text | 4 | how many words in w0 w1 w2 w3 w4 w5 w6 w7 w8 w9 w10 w11 w12 w13 w14 w15 w16 w17 w18 w19 w20 w21 w22 w23 w24 w25 w26 w27 w28 w29 w30 w31 w32 w33 w34 w35 w36 w37 w38 w39 w40 w41 w42 w43 w44 w45 w46 w47 w48 w49 w50 w51 w52 w53 w54 w55 w56 w57 w58 w59 w60 w61 w62 w63 w64 w65 w66 w67 w68 w69 w70 w71 w72 w73 w74 w75 w76 w77 w78 w79 w80 w81 w82 w83 w84 w85 w86 w87 w88 w89 w90 w91 w92 w93 w94 w95 w96 w97 w98 w99 w100 w101 w102 w103 w104 w105 w106 w107 w108 w109 w110 w111 w112 w113 w114 w115 w116 w117 w118 w119 | w0 w1 w2 w3 w4 w5 w6 w7 w8 w9 w10 w11 w12 w13 w14 w15 w16 w17 w18 w19 w20 w21 w22 w23 w24 w25 w26 w27 w28 w29 w30 w31 w32 w33 w34 w35 w36 w37 w38 w39 w40 w41 w42 w43 w44 w45 w46 w47 w48 w49 w50 w51 w52 w53 w54 w55 w56 w57 w58 w59 w60 w61 w62 w63 w64 w65 w66 w67 w68 w69 w70 w71 w72 w73 w74 w75 w76 w77 w78 w79 w80 w81 w82 w83 w84 w85 w86 w87 w88 w89 w90 w91 w92 w93 w94 w95 w96 w97 w98 w99 w100 w101 w102 w103 w104 w105 w106 w107 w108 w109 w110 w111 w112 w113 w114 w115 w116 w117 w118 w119 | 120 | `263b2624827ceea1…` | BOTH_ENDS, CHAR, END_DIRECT, REV_WORD, SPAN3, SPAN5, WORD, WORD>CHAR, WORD?CHARSCAN | — |
| 11 | E1 | F4-edge-shape | 4 | how many words in a\nb\nc | a\nb\nc | 1 | `b6fec2741172f735…` | BOTH_ENDS, CHAR, END_DIRECT, REV_WORD, SPAN3, SPAN5, WORD, WORD>CHAR, WORD?CHARSCAN | — |
| 12 | E2 | F4-edge-shape | 5 | how many letters in abc  | abc  | 4 | `71d7ffa7f3e38be3…` | BOTH_ENDS, CHAR, END_DIRECT, SPAN3, SPAN5, WORD>CHAR, WORD?CHARSCAN | — |
| 13 | E3 | F4-edge-shape | 2 | what is the 2nd letter of the  quick | the  quick | h | `bae1b9932cd0f4d5…` | BOTH_ENDS, CHAR, END_DIRECT, REV_WORD, SPAN3, SPAN5, WORD, WORD>CHAR, WORD?CHARSCAN | — |
| 14 | D1 | F5-degenerate | 16 | what is the last word of  |  | ? | `11354a65f4103c58…` | BOTH_ENDS, CHAR, END_DIRECT, REV_WORD, SPAN3, SPAN5 | WORD, WORD>CHAR, WORD?CHARSCAN |
| 15 | D2 | F5-degenerate | 4 | how many words in  |  | 0 | `3395457922b90288…` | BOTH_ENDS, CHAR, END_DIRECT, REV_WORD, SPAN3, SPAN5, WORD, WORD>CHAR, WORD?CHARSCAN | — |
| 16 | D3 | F5-degenerate | 1 | how many z's in  |  | 0 | `b8576d436c4bfd44…` | BOTH_ENDS, CHAR, END_DIRECT, REV_WORD, SPAN3, SPAN5, WORD, WORD>CHAR, WORD?CHARSCAN | — |
| 17 | D4 | F5-degenerate | 2 | what is the 1st letter of  |  | ? | `58dac972600f7f89…` | BOTH_ENDS, CHAR, END_DIRECT, REV_WORD, SPAN3, SPAN5, WORD, WORD>CHAR, WORD?CHARSCAN | — |
| 18 | D5 | F5-degenerate | 6 | does abc contain  | abc | yes | `af08fb9ec75a6dcf…` | BOTH_ENDS, CHAR, END_DIRECT, REV_WORD, SPAN3, SPAN5, WORD, WORD>CHAR, WORD?CHARSCAN | — |
| 19 | S1 | F6-strict-index | 2 | what is the 0th letter of abc | abc | ? | `94f99f06b257612f…` | REV_WORD, SPAN3, SPAN5, WORD | — |
| 20 | S2 | F6-strict-index | 12 | what is the 9th letter of the 1st word of abc def | abc def | ? | `e6d9b738038c21ca…` | REV_WORD, WORD | — |
| 21 | S3 | F6-strict-index | 2 | what is the 4th letter of fox | the quick brown fox | ? | `ec31ebf4423d1ce0…` | REV_WORD, WORD | — |
| 22 | S4 | F6-strict-index | 12 | what is the 0th letter of the 2nd word of abc def | abc def | ? | `6f875f57c7d37fc1…` | REV_WORD, WORD | — |
| 23 | S5 | F6-strict-index | 2 | what is the 9th letter of abc | abc | ? | `609de246cf8dbdfe…` | REV_WORD, SPAN3, SPAN5, WORD | — |
| 24 | O1 | F6-strict-index | 12 | what is the letter of the 2nd word of abc def | abc def | ? | `660709de33464c28…` | REV_WORD, WORD | — |
| 25 | O2 | F6-strict-index | 12 | what is the letter of the 3rd word of alpha beta gamma | alpha beta gamma | ? | `2440f2529269780f…` | REV_WORD, WORD | — |

## Construction notes (why each trap)

- **00 [N1]** punctuation as letter target: '.' counts as the target letter via "'s in" parse
- **01 [N2]** spelled ordinal '(second)' is inert decoration; digit ordinal governs parse_pos_n
- **02 [N3]** sentence/ordinal words are inert: kind WORD_COUNT answers whole-text count
- **03 [N4]** digit as letter target
- **04 [N5]** case-sensitive scan: lowercase 's' absent in all-caps text
- **05 [M1]** word-level locate (2nd word='beta') then char index 3 -> 't'
- **06 [M2]** locate 2nd word then count letters inside it
- **07 [M3]** kind CONTAINS_WORD: locate word then substring-scan inside it -> miss
- **08 [M4]** locate 2nd word then reverse it
- **09 [M5]** relative addressing via 'last': last word='gamma' -> 'g'
- **10 [L1]** 120-word text; word count must survive scale
- **11 [E1]** newline is not a word separator in the machinery: whole text is one word
- **12 [E2]** trailing space: byte length counts it
- **13 [E3]** double space inside text; whole-text char index 2 -> 'h'
- **14 [D1]** W25 t[-1] class: empty text on last-word question must refuse cleanly, never panic
- **15 [D2]** empty text word count
- **16 [D3]** empty text letter count
- **17 [D4]** empty text position question -> clean '?' refusal
- **18 [D5]** empty needle: find_sub returns 0 (vacuous presence) -> yes
- **19 [S1]** index 0 is out of range: strict candidates refuse with '?'
- **20 [S2]** index 9 exceeds word length 3: strict candidates refuse with '?'
- **21 [S3]** 'fox' has no 4th letter: strict candidates refuse with '?'
- **22 [S4]** index 0 with word-level addressing: strict candidates refuse with '?'
- **23 [S5]** index 9 exceeds text length 3: strict candidates refuse with '?'
- **24 [O1]** no ordinal names no position: strict candidates refuse with '?'
- **25 [O2]** no ordinal names no position: strict candidates refuse with '?'
