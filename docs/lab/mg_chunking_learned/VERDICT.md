# Learned chunking chooser — VERDICT (Phase 2, 2026-09-26)

Plain-English verdict: **TNN's chunking is no longer hand-picked.** Nine candidate chunking
methods ran head-to-head on 57 questions; the intake now uses a policy table computed from
their measured scores — most correct first, then fewest fallbacks, then least work, then a
deterministic tie-break. The odd methods survived only where the numbers kept them.

## Bars

| Bar | Result |
|---|---|
| Correctness (learned live pass) | **57 / 57** |
| Native (no fallback) | **57 / 57** |
| Fallbacks | **0** |
| Every choice traced with its measured reason | yes |
| Every zoom traced | yes |
| Deterministic rerun | byte-identical (RUN_D1 == RUN_D2) |
| Rebuild from source | byte-identical to RUN_D1 |

RUN_D1.out SHA-256: `45780575f766cd28fc4805b076d43f445d1a68e4e99836b265562a7d622eadcb`

## How the chooser was learned

1. **Battery:** 57 questions — the 24 frozen Phase-1 questions plus 33 adversarial new ones
   (nested addressed-word operations, case traps, space/index traps, multi-token reversal).
2. **Candidates:** 9 chunking methods implemented as real Zag code, each emitting its answer,
   its measured operation count, and whether it stayed native or fell back.
3. **Derivation:** for every question-kind × text-shape class, all 9 candidates' totals were
   accumulated; the winner was selected by: most correct → most native → fewest operations →
   coarser chunking → lower candidate id. No candidate was ever selected on a single question
   it answered — the table is per-class.
4. **Live pass:** a separate run answered all 57 questions using ONLY the derived table, with
   the derived reason printed on every choice.

## The derived policy (question-kind × text-shape → chunking)

| Question kind | Single-word text | Multi-word text |
|---|---|---|
| letter count | WORD>CHAR (as CHAR) | CHAR |
| letter position | WORD>CHAR (as CHAR) | **WORD>CHAR (zoom)** |
| reverse | WORD>CHAR (as CHAR) | WORD>CHAR (as CHAR) |
| word count | WORD | WORD |
| length | WORD | CHAR |
| contains | **BOTH_ENDS** | WORD>CHAR |
| first word | — | CHAR |
| first letter | — | WORD>CHAR (as CHAR) |
| last letter | **END_DIRECT** | **END_DIRECT** |
| letter count in word | — | WORD>CHAR |
| length of word | — | WORD |
| letter position in word | — | WORD>CHAR |
| reverse a word | — | WORD>CHAR |
| first letter of word | — | WORD>CHAR |
| last letter of word | — | WORD>CHAR |
| last word | WORD | WORD |
| contains in word | — | WORD>CHAR |

("—" = no battery examples; the slot defaults to WORD>CHAR and will be filled by measurement
when examples arrive. "(as CHAR)" = the deliberative candidate chose character chunks —
the trace shows chunk=CHAR with the derived reason.)

## The weird candidates: who survived, who was cut

Two unusual methods earned their place **on measured numbers alone**:

| Candidate | Survived on | Measured gain |
|---|---|---|
| BOTH_ENDS (search inward from both ends) | contains / single-word | 8 ops vs 10 for CHAR and END_DIRECT — 20% less work |
| END_DIRECT (read the text edge directly) | last-letter / single+multi | 2 ops vs 14 (single), 1 op vs 11 (multi) — 7–11× less work than scanning |

Why END_DIRECT wins last-letter questions: the question names the edge, so reading the edge
directly is honest, native, and far cheaper than a full scan. It was the single biggest
measured win in the battery.

Cut, with reasons:

| Candidate | Fate | Reason |
|---|---|---|
| SPAN3 / SPAN5 (fixed 3/5-byte spans) | cut everywhere | correct on some classes but always fell back — never native |
| REV_WORD (address from the right) | cut everywhere | native on nested classes but always slower than WORD>CHAR; delegated elsewhere |
| WORD?CHARSCAN | never won | always tied or lost to WORD>CHAR; lost the deterministic tie-break |
| CHAR / WORD | won several classes outright | CHAR won 3 classes on fewest ops; WORD won 5 classes (word-scale questions) |

## Bugs found and fixed during this run (measured, then re-run)

1. **ws_locate(-1) returned the FIRST word, not the last.** The post-loop guard blocked the
   trailing-word update, so "last word of X" located X's first word for the CHAR, END_DIRECT,
   and SPAN candidates. Fixed; all measurements re-run from scratch.
2. **coarseness rank was inverted.** The tie-break table scored WORD as finest and SPAN as
   coarsest — exactly backwards. Fixed so lower = coarser chunking unit.
3. **Classifier gap:** digit ordinals ("1st letter of the X word of") weren't recognized —
   only spelled-out "first". Fixed before the live pass.

## What this is NOT

The learned chooser is derived from a **finite authored battery (57 questions)** and a
**finite implemented candidate set (9 methods)**, and it still depends on its
question parser/classifier. The learning is real — the table came from measured scores, not
from anyone's opinion — but it is not unconstrained runtime invention and not general
learning. New question forms extend the table by measurement, not by hand.
