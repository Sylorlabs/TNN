# Experiment A Analysis

## Method
- Arms: C=choice (10), D=delete-only (11), M=misuse (12). B2 curriculum.
- Scales: S1 (500 episodes, 6 variants), S10 (5000 episodes, 3 variants).
- Every run byte-identical x2 (battery verifies).
- Metrics: time series (`ST_TS` every h/20 + t=0/h) and endpoints.

## S1 Results (mean of 6 variants)

### VUP (value update, no wrongness)

| Metric | C | D | M | C vs D |
|--------|---|---|---|--------|
| Drops | 0 | 470 | 0 | C wins (infinite) |
| Abandons | 0 | 3792 | 0 | C wins |
| Important held | 29/150 | 9/150 | 29/150 | C 3.2× |
| Recycles | 475 | 0 | 475 | — |
| Deletes | 0 | 0 | 0 | — |
| Cites saved | 1631 | 0 | 1631 | C wins |
| Ledger entries | 589 | 3844 | 589 | C 6.5× smaller |
| Ledger bytes | 49,476 | 322,896 | 49,476 | C 6.5× smaller |

### WBS (wrongness, tests revision)

| Metric | C | D | M | Note |
|--------|---|---|---|------|
| Honest revisions | 50/50 | 36/36 | 0/50 | D smaller cohort |
| Revision rate | 100% | 100% | 0% | M wound |
| Latency (mean) | 50 | 50 | — | Identical |
| Drops | 0 | 434 | 0 | D admission collapse |
| Abandons | 0 | 3472 | 0 | D ledger bloat |
| Important held | 28.3/150 | 15/150 | 29/150 | C 1.9× D |
| Deletes | 50 | 36 | 0 | C revises more |
| Recycles | 420 | 0 | 524.5 | M recycles most |
| Dodges | 0 | 0 | 54.5 | M misuse |
| Cites spent | 200 | 144 | 0 | C pays for revisions |
| Cites saved | 1200 | 0 | 1984 | M dodges most |

### JI (implants)

| Metric | C | D | M |
|--------|---|---|---|
| Drops | 0 | 469 | 0 |
| Abandons | 0 | 3752 | 0 |
| Important held | 29/150 | 9.2/150 | 29/150 |
| Recycles | 470 | 0 | 470 |

## S10 Results (mean of 3 variants) — battery complete 2026-09-26 ~11:00 UTC

The S1 pattern is structural and WIDENS at S10. All 27 cells ×2 byte-identical, all ST_INVALID 0.

### VUP (mean of 3 variants)

| Metric | C | D | M | C vs D |
|--------|---|---|---|--------|
| Drops | 0 | 4682 | 0 | C wins |
| Abandons | 0 | 37848 | 0 | C wins |
| Important held | 317/1500 | 95/1500 | 317/1500 | C 3.3× |
| Recycles | 4742 | 0 | 4742 | — |
| Cites saved | 16599 | 0 | 16599 | C wins |
| Ledger entries | 5950 | 38367 | 5950 | C 6.4× smaller |
| Ledger bytes | 499,828 | 3,222,800 | 499,828 | C 6.4× smaller |

### WBS (mean of 3 variants)

| Metric | C | D | M | Note |
|--------|---|---|---|------|
| Honest revisions | 677/677 | 1470/1470 | 0/668 | both 100% — see nuance |
| Revision rate | 100% | 100% | 0% | M wound |
| Latency (mean) | 50 | 50 | — | Identical |
| Drops | 0 | 3212 | 0 | D admission collapse |
| Abandons | 0 | 25696 | 0 | D ledger bloat |
| Important held | 317/1500 | 103/1500 | 317/1500 | C 3.1× |
| Deletes | 677 | 1470 | 0 | D pays for more rot |
| Recycles | 4005 | 0 | 5353 | — |
| Dodges | 0 | 0 | 671 | M misuse |
| Cites spent | 2708 | 5880 | 0 | D 2.2× cite spend |
| Cites saved | 10577 | 0 | 19956 | M dodges most |
| Ledger entries | 10682 | 38304 | 8622 | C 3.6× smaller |

**Revision-count nuance (important):** D's higher raw revision count (1470 vs
677) is NOT a win — it is a symptom. C recycles stale/superseded memories
BEFORE they rot into contradiction (reasons 2/3/4), so fewer reach the
contradicted state; the 677 contradicted ones are honestly deleted (reason 1).
D cannot preempt, so 1470 memories rot into contradiction and must be deleted
at 4 cites each. Same 100% honest rate; D's path costs 2.2× the cites and
25,696 abandons. Report the rate WITH the cost, not the count.

### JI (mean of 3 variants)

| Metric | C | D | M |
|--------|---|---|---|
| Drops | 0 | 4681 | 0 |
| Abandons | 0 | 37448 | 0 |
| Important held | 317/1500 | 96/1500 | 317/1500 |
| Recycles | 4680 | 0 | 4684 |
| Dodges | 0 | 0 | 2 |

## Time series
`ST_TS` lines show:
- C: live slots stay at 32 (full), important held climbs to 29, zero drops/abandons throughout.
- D: live slots at 32, but drops accumulate from t≈150 (saturation), abandons from t≈150, important held plateaus at 9.
- The divergence starts at saturation (~150 episodes for S1) and widens.

## Misuse white-box
M arm deliberations (WBS):
- 54.5 dodges (mean), all reason 9, all trigger=contradiction.
- 0 honest revisions (vs 50 for C).
- The deliberation trace shows: contradicted memory → choice=RECYCLE (not DELETE)
  → reason=9 → no kill_ep → rev_kill=0.
- This is the "wound": TNN deliberately avoids the destruction price by
  recycling a false memory into a placeholder, destroying its ability to
  revise.

## Statistical notes
- 6 variants (S1) × 2 runs byte-identical. 3 variants (S10).
- No RNG. All deterministic.
- Effect sizes are 3× to 6.5×, far beyond noise.
- D's WBS 100% revision rate is misleading without the cohort size (36 vs 50).
