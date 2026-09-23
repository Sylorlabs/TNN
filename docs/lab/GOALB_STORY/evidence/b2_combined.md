# B2 combined two-judge table

Judge #1: gpt-5.6-sol (UnoRouter, blind). Judge #2: grok-4.7 (ExperientialLabs, blind).
Frozen prompt: evidence/b2_prompt.txt (same text, same blind TIDs for both judges).

| trial | set | variant | sol | grok-4.7 | mean | |diff| |
|---|---|---|---|---|---|---|
| T01 | S1 | POS | 2 | 1 | 1.5 | 1 |
| T02 | S1 | DEL | 3 | 2 | 2.5 | 1 |
| T03 | S2 | POS | 2 | 1 | 1.5 | 1 |
| T04 | S2 | DEL | 4 | 3 | 3.5 | 1 |
| T05 | S3 | POS | 2 | 1 | 1.5 | 1 |
| T06 | S3 | DEL | 3 | 2 | 2.5 | 1 |
| T07 | S4 | POS | 2 | 1 | 1.5 | 1 |
| T08 | S4 | DEL | 5 | 3 | 4.0 | 2 |
| T09 | S5 | POS | 2 | 1 | 1.5 | 1 |
| T10 | S5 | DEL | 4 | 2 | 3.0 | 2 |
| T11 | S6 | POS | 2 | 1 | 1.5 | 1 |
| T12 | S6 | DEL | 4 | 3 | 3.5 | 1 |
| T13 | S7 | POS | 2 | 1 | 1.5 | 1 |
| T14 | S7 | DEL | 4 | 2 | 3.0 | 2 |
| T15 | S8 | POS | 2 | 1 | 1.5 | 1 |
| T16 | S8 | DEL | 5 | 3 | 4.0 | 2 |
| T17 | CTRL | POS | 5 | 5 | 5.0 | 0 |

## Per-variant counts (mean >= 3.5)

- POS: 0/8 trials with two-judge mean >= 3.5 (bar: >=6/8)
- DEL: 4/8 trials with two-judge mean >= 3.5 (bar: >=6/8)

## Per-judge counts (single-judge reading, mean>=3.5 per judge)

- sol POS: 0/8
- sol DEL: 6/8
- grok-4.7 POS: 0/8
- grok-4.7 DEL: 0/8

## Head-to-head variant means

- sol: DEL 4.00, POS 2.00, gap 2.00
- grok-4.7: DEL 2.50, POS 1.00, gap 1.50
- combined: DEL 3.25, POS 1.50, gap 1.75

## Positive control T17: sol=5, grok=5 (bar: both >= 4.0)

## Inter-rater disagreements >2 points

- none

Max |diff| = 2
