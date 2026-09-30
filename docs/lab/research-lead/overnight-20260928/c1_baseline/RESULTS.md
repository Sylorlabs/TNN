# C1 simple baseline: RESULTS (frozen)

- Prereg: commit 26937cb55 (committed alone before implementation)
- Freeze: commit 11b957715 (sources, binaries, hashes, committed alone)
- Runs: 45 total (3 baselines x 5 worlds x 3 reps), frozen driver run_race.sh
  (sha256 4cd7bec75915fb93dc8e874d25f9ec6428ee604beadff79b9357ea1c092850a9),
  worlds byte-identical to e0a30377f blobs, fresh state dir per run.
- Verdict rule from prereg: any baseline reaching 60/63 or more on any
  canonical world yields C1-BASELINE-WORLD-PROPERTY; otherwise
  C1-BASELINE-LEARNING-PROPERTY.

## Totals (reps byte-identical, shown once per world)

| baseline | w0 (63) | w1 (63) | w2 (63) | h0 (67) | h1 (67) |
|----------|---------|---------|---------|---------|---------|
| MEM      | 27      | 27      | 27      | 29      | 29      |
| FREQ     | 6       | 6       | 3       | 7       | 5       |
| RAND     | 5       | 5       | 5       | 6       | 6       |

C1-CLEAN contestant for reference: 63/63 on W0/W1/W2, 66/67 on H0, 67/67 on H1.

## Stage breakdowns (rep 1; reps 2 and 3 byte-identical)

MEM w0/w1/w2: A 20/20, B 0/8, C 6/6, D 0/6, E 0/8, F 0/3, G 0/2,
H 0/4, T 0/2, K 1/2, L 0/2. Sum 27/63.
MEM h0/h1: A 20/20, B 0/8, C 8/8, D 0/6, E 0/8, F 0/3, G 0/2,
H 0/4, T 0/2, K 1/2, L 0/4. Sum 29/67.

FREQ w0: A 5/20, B 0/8, C 0/6, D 0/6, E 0/8, F 0/3, G 0/2,
H 0/4, T 0/2, K 1/2, L 0/2. Sum 6/63.
FREQ w1: A 4/20, B 0/8, C 1/6, D 0/6, E 0/8, F 0/3, G 0/2,
H 0/4, T 0/2, K 1/2, L 0/2. Sum 6/63.
FREQ w2: A 2/20, B 0/8, C 0/6, D 0/6, E 0/8, F 1/3, G 0/2,
H 0/4, T 0/2, K 0/2, L 0/2. Sum 3/63.
FREQ h0: A 3/20, B 0/8, C 3/8, D 0/6, E 0/8, F 0/3, G 0/2,
H 0/4, T 0/2, K 1/2, L 0/4. Sum 7/67.
FREQ h1: A 4/20, B 0/8, C 0/8, D 0/6, E 0/8, F 0/3, G 0/2,
H 0/4, T 0/2, K 1/2, L 0/4. Sum 5/67.

RAND w0/w1/w2: A 5/20, B 0/8, C 0/6, D 0/6, E 0/8, F 0/3, G 0/2,
H 0/4, T 0/2, K 0/2, L 0/2. Sum 5/63.
RAND h0/h1: A 5/20, B 0/8, C 1/8, D 0/6, E 0/8, F 0/3, G 0/2,
H 0/4, T 0/2, K 0/2, L 0/4. Sum 6/67.

## Frozen prediction outcomes

- P-MEM1 (MEM under 35/63 on every canonical world): PASS. Observed 27/63.
- P-MEM2 (MEM 20/20 on stage A every canonical rep): PASS.
- P-FREQ1 (FREQ under 12/63 on every canonical world): PASS. Observed 6, 6, 3.
- P-RAND1 (RAND under 8/63 on every canonical world): PASS. Observed 5/63.
- P-DET1 (3/3 reps byte-identical per baseline/world on replies.jsonl and
  scores.jsonl): PASS. All 15 (baseline, world) pairs byte-identical.
  costs.txt differs only on the wall_ms line, as anticipated.

## Kill-bar outcomes

- K1 ordering: prereg commit 26937cb55 strictly precedes freeze commit
  11b957715 (verified with git merge-base --is-ancestor). This results commit
  follows the freeze. Ordering clean.
- K2 worlds plus honest recording: worlds byte-identical to the frozen
  e0a30377f blobs; scores recorded as measured, including the MEM K stage
  1/2 rather than the predicted 2/2.
- K3 purity: all analysis with shell byte tools (sha256sum, grep, wc); no
  Python anywhere; no em dashes in this document (checked).

## Verdict

The highest score by any baseline on any canonical world is MEM 27/63,
far below the 60/63 rule. No baseline approaches the C1-CLEAN contestant
score of 63/63.

**C1-BASELINE-LEARNING-PROPERTY**

The 63/63 scores are a learning property of the contestant, not a world
property. The strongest trivial control (MEM: persistent last-write-wins
memory of taught facts) captures the taught-fact stages (A and C) exactly
as predicted and nothing else: every inferential stage (B, D through H,
T, L) scores zero, and it misses one of two retention probes. FREQ and
RAND score at or near chance as predicted.
