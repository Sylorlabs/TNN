# GOAL-B trial table

B5: 3 fresh-process reruns byte-identical (cmp rep1/rep2/rep3). B4: kb.txt sha256 unchanged; 0/16 stories share a >=16-byte substring with kb.txt; composer source has no write path to kb.txt (O_RDONLY reads only).

B2 two-judge bar (prereg): mean of the two judges' scores >= 3.5 on >=6/8 trials per variant.

| trial | set | variant | B1 words | B2 sol | B2 grok-4.7 | B2 two-judge mean | B3 novel |
|---|---|---|---|---|---|---|---|
| T01 | S1 | POS | PASS | 2 | 1 | 1.5 | PASS |
| T02 | S1 | DEL | PASS | 3 | 2 | 2.5 | PASS |
| T03 | S2 | POS | PASS | 2 | 1 | 1.5 | PASS |
| T04 | S2 | DEL | PASS | 4 | 3 | 3.5 | PASS |
| T05 | S3 | POS | PASS | 2 | 1 | 1.5 | PASS |
| T06 | S3 | DEL | PASS | 3 | 2 | 2.5 | PASS |
| T07 | S4 | POS | PASS | 2 | 1 | 1.5 | PASS |
| T08 | S4 | DEL | PASS | 5 | 3 | 4.0 | PASS |
| T09 | S5 | POS | PASS | 2 | 1 | 1.5 | PASS |
| T10 | S5 | DEL | PASS | 4 | 2 | 3.0 | PASS |
| T11 | S6 | POS | PASS | 2 | 1 | 1.5 | PASS |
| T12 | S6 | DEL | PASS | 4 | 3 | 3.5 | PASS |
| T13 | S7 | POS | PASS | 2 | 1 | 1.5 | PASS |
| T14 | S7 | DEL | PASS | 4 | 2 | 3.0 | PASS |
| T15 | S8 | POS | PASS | 2 | 1 | 1.5 | PASS |
| T16 | S8 | DEL | PASS | 5 | 3 | 4.0 | PASS |

B2 two-judge verdict: POS 0/8 >=3.5 (FAIL), DEL 4/8 >=3.5 (FAIL). Bar not met.
Per-judge: sol POS 0/8, sol DEL 6/8; grok-4.7 POS 0/8, grok-4.7 DEL 0/8.
Head-to-head means: sol DEL 4.00 vs POS 2.00 (gap 2.00); grok-4.7 DEL 2.50 vs POS 1.00 (gap 1.50); combined DEL 3.25 vs POS 1.50 (gap 1.75).
Inter-rater |diff| max 2; no disagreements >2 points (prereg flag threshold).
Positive control T17: sol=5, grok-4.7=5 (bar >=4.0 both judges — PASS, apparatus valid).

Judge #1: gpt-5.6-sol via UnoRouter, blind, frozen prompt evidence/b2_prompt.txt.
Judge #2: grok-4.7 via ExperientialLabs, blind, the SAME frozen prompt text and blind TIDs (A1 said grok-4.6 via UnoRouter; substitution documented in VERDICT.md).
Full combined table: evidence/b2_combined.md.
