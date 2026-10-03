# COST_LEDGER: WIDE-EIG-10 (wave-20261002-0521pdt, lane TRADES)

Zero em-dashes in this file. All costs measured on the sealed 8-world
set, binaries built from the frozen sources with the pinned znc.
Deliberation cost is the honest currency; wall clock reported with its
confounds.

## Deliberation cost (the 10x)

| Variant | EIG searches/world | Total forward sims (8 worlds) | Ratio vs SINGLE |
|---|---|---|---|
| WIDE | 30 (10 traces x 3 rounds) | 12288 | 11.01x |
| F_CM | 30 | 11548 | 10.35x (0.94x of WIDE) |
| SINGLE | 3 (1 trace x 3 rounds) | 1116 | 1.00x |

Per-world sim ratios (WIDE/SINGLE): 8.92, 14.50, 8.93, 13.93, 9.42,
13.96, 8.98, 15.96. Sims per search scale with hypothesis-set size,
which is world-dependent; the aggregate 11.01x is inside the frozen
[8,12] band.

## Wall clock

| Variant | ms/run (mean, 8 worlds) | Ratio vs SINGLE |
|---|---|---|
| WIDE | 7647.75 | 4.77x |
| F_CM | 8783 | 5.48x |
| SINGLE | 1603.5 | 1.00x |

Wall is compressed by fixed per-turn process-spawn overhead (75 vs 21
binary invocations per run); the 10x is in deliberation steps and
forward sims, which is the budgeted currency.

## Bytes

- Contestant binaries: 189855 bytes each (all three variants; the
  one-line flag delta changes no size).
- Learner state: 16384 bytes fixed allocation (W region 14000..16384
  holds the 10 per-trace hypothesis sets plus the pooled verdict set).
- World files per world: pre.jsonl (13 turns) + int_table.tsv
  (60 precomputed outcomes).

## Intelligence purchased

- WIDE 8/8 sealed chain identification vs SINGLE 5/8: +3 worlds bought
  at 11.01x forward sims. The gain is ensemble-plus-pooling reliability,
  not EIG choice superiority (F_CM 8/8 at 0.94x of WIDE's sims).
- No regression: 68-item arena battery stripped reply stream
  byte-identical to the INQ sealed run (58/68; C9 stays 0.000 by design).
- Determinism: 3/3 byte-identical runs on all 8 worlds; zero randomness
  in WIDE decision paths; F_CM uses a frozen-seed LCG.

Efficiency was not traded for speed anywhere: no cheap-only variant is
promoted; the 10x budget was spent and measured.
