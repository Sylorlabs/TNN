# K4 trace audit — native-authorship trial 1 (broker)

**Bar (frozen):** "≥90% of trap questions show ≥2 candidates with input-specific
evidence in the trace; independent audit of 10 random traces finds none reducible
to a kind→candidate mapping."

**Result: FAIL on the coverage prong (21/26 = 80.8% < 90%).** The audit prong was
still performed; findings below.

## Coverage: 21/26

Every non-crashed, non-refused trap (21) emits all 9 `D-EV` candidate evidence
lines with input-specific content (this text's byte/word/span counts, needle-hit
on this text, edge vocabulary, addressing depths). Method: count `D-EV` lines with
quoted evidence ≥8 chars per trap; all 21 have 9/9.

The 5 without candidate evidence:
- q10 (L1): deliberation **crashes** (exit 1) — no trace at all.
- q14–q17 (D1–D4): **clean pre-deliberation refusals** (`# D-REFUSE`, empty text).
  The D0 degenerate guard fires before `d_features`/`d_deliberate` run, so no
  candidate evidence exists by design.

21/26 = 80.8% < 90% → K4 fails as written. (If refusals were excluded from the
denominator, 21/22 = 95.5%; the prereg does not exclude them.)

## Deterministic 10-trace audit (qids 0–9; declared in advance, no RNG)

| qid | kind → winner | #D-EV | non-kind features doing work in this trace | reducible? |
|---|---|---|---|---|
| 0 | LETTER_COUNT → CHAR (F52) | 9 | span counts "4 vs 7 spans over 19B"; addr_depth | no |
| 1 | POSITION → CHAR (F10) | 9 | S1-shape-single fires (spaceless "strawberry"); byte counts | no |
| 2 | WORD_COUNT → WORD (F51) | 9 | count_unit=word; word-table evidence | no |
| 3 | LETTER_COUNT → CHAR (F52) | 9 | same rule, different text counts | no |
| 4 | LETTER_COUNT → CHAR (F52) | 9 | same rule, different text counts | no |
| 5 | POSITION_WORD → WORD>CHAR (F2) | 9 | addr_depth=2 addressing levels over 4 words | no |
| 6 | POSITION_WORD → WORD>CHAR (F2) | 9 | addr_depth; word-locate evidence | no |
| 7 | CONTAINS_WORD → WORD>CHAR (F2) | 9 | needle word-hit on this text | no |
| 8 | POSITION_WORD → WORD>CHAR (F2) | 9 | addr_depth; reversal evidence | no |
| 9 | FIRST_LETTER_WORD → END_DIRECT (F1) | 9 | edge= NAMED edge vocabulary; direct edge read | no |

**Why "not reducible" (mechanistic):**
1. Elimination paths differ by non-kind input properties. Same-kind pair
   q1/q13/q19/q23 (all POSITION→CHAR/F10): S1-shape-single fires for the
   spaceless texts (q1 "strawberry", q19 "abc") and not for q13/q21 (spaced).
   A kind→candidate lookup would emit identical traces; these differ by input.
2. Terminal rules are stated in non-kind features: F10 (ans_unit=LETTER +
   addr_depth=1), F2 (addr_depth), F52/F51 (count_unit), F1 (named edge +
   LETTER), F33 (needle_hit + lenclass). No kind-0 rule fired on this battery.
3. P-feat (constant-fold all features incl. kind) flips 21/26 choices —
   choices are feature-sensitive, not kind-memorized.

**Honest caveat (observational):** on this 26-trap battery the winner is perfectly
predicted by kind alone — no two traps share a kind with different winners, so
the battery contains no proving pair where a non-kind feature flips the choice
holding kind fixed. The DESIGN.md claims such divergence exists (F31 vs F32 for
CONTAINS by needle word-hit); the mechanism supports it (rules keyed on
needle_hit/addr_depth/edge), and the traces demonstrably process those features —
but this battery cannot exhibit the flip. A future battery should include
same-kind, different-winner pairs to test this directly.

## Refusal-path note

q14–q17 refuse before deliberation. The refusal is the prereg-mandated clean
refusal for degenerate inputs (§4: "empty text must refuse cleanly"), and the
oracle blesses `?` for D1/D4. The arm's refusal path hardcodes `correct=0` in
its self-report; the broker scores oracle-grounded (ans == exp), crediting q14
and q17. See VERDICT.md.
