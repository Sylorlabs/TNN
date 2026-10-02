# C1-CLEAN RESULTS

Wave: C1-CLEAN
Date: 2026-09-30
Status: COMPLETE

## TNN CLEAN SCORE

**63/63** (mean over 3 fresh unseen canonical worlds, 3 reps each, 9/9 perfect)

## LLM BASELINE

**PENDING**

## Canonical Worlds (W0-W2)

All 3 canonical worlds scored 63/63 on all 3 repetitions.
All repetitions byte-identical within each world (3/3 determinism).

| World | Rep 1 | Rep 2 | Rep 3 | Determinism |
|-------|-------|-------|-------|-------------|
| W0 | 63/63 | 63/63 | 63/63 | 3/3 identical |
| W1 | 63/63 | 63/63 | 63/63 | 3/3 identical |
| W2 | 63/63 | 63/63 | 63/63 | 3/3 identical |

Stage scores (all canonical reps): A 20/20, B 8/8, C 6/6, D 6/6, E 8/8,
F 3/3, G 2/2, H 4/4, T 2/2, K 2/2, L 2/2.

## Exploratory Hard Worlds (H0-H1)

Scored separately. NOT part of TNN CLEAN SCORE.

Actual hard-world denominator: 67 queries (prereg said 64; see discrepancy note).

| World | Rep 1 | Rep 2 | Rep 3 | Determinism |
|-------|-------|-------|-------|-------------|
| H0 | 66/67 | 66/67 | 66/67 | 3/3 identical |
| H1 | 67/67 | 67/67 | 67/67 | 3/3 identical |

### H0 finding: systematic L3 law-revert miss

H0 missed L3 on all 3 reps (expected "ttxy", got "tyxt"). This is the
law-revert query (pb under the original rotation after a change and revert).
The miss is deterministic and world-dependent: H1 scored L 4/4 including its
own law-revert query.

Interpretation: the contestant handles a single law change (canonical L 2/2)
but its revision mechanism does not reliably handle a law revert. This is a
genuine boundary worth a future v2 hypothesis, not a canonical failure.

## Prereg Denominator Discrepancy

The prereg proposed a hard-world denominator of 64. The actual frozen hard
generator produces 67 scored query turns. This document reports raw X/67.
The prereg is preserved as-is; the discrepancy is disclosed here.

## Costs (canonical, representative W0 rep 1)

- Queries: 63
- Observations: 2078
- Tools: 4 (ASK: 3, INTERVENE: 1)
- Wall time: 329,598 ms
- Persistent state: 1,659 bytes
- Peak RSS: 14,536 kB
- Ledger: facts=32 rels=23 hyps=6 demos=8 vocab=6

## Verdict

**C1-CLEAN-PASS**

TNN CLEAN SCORE 63/63 on 3 fresh unseen canonical worlds with 3/3
byte-identical determinism. Governance clean. LLM BASELINE: PENDING.
