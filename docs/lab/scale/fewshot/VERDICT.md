# FEW-SHOT / SCALE-DOWN verdict — 2026-09-21/22

Micah's question: the TNN learns shockingly fast (1.0 mastery at 240 facts and
at 6.58M). What happens below 240? Find the floor. Does one-shot learning work?

## Headline: there is no floor. One-shot learning works.

Clean mastery is **1.0000 at every N from 192 down to 1**. The smallest N with
mastery 1.0 is N=1, and it never breaks — a single fact taught once is held.
Absorption of planted falsehoods reproduces at minimal scale.

## Few-shot curve (P=1, single teaching pass, eval mode, 5/5 byte-identical reps)

| N | off | clean mastery | all-fact | absorption | flaw | ops/fact | B/fact | recall ns/probe (min of 5) |
|---|---|---|---|---|---|---|---|---|
| 192 | 0 | 179/179 = 1.0000 | 0.9323 | 13/13 | 96/96 | 4.005 | 92 | 205 |
| 128 | 0 | 119/119 = 1.0000 | 0.9297 | 9/9 | 96/96 | 4.007 | 92 | — |
| 96 | 0 | 91/91 = 1.0000 | 0.9479 | 5/5 | 96/96 | 4.010 | 92 | 412 |
| 64 | 0 | 60/60 = 1.0000 | 0.9375 | 4/4 | 96/96 | 4.015 | 93 | — |
| 48 | 0 | 45/45 = 1.0000 | 0.9375 | 3/3 | 96/96 | 4.020 | 93 | — |
| 32 | 0 | 29/29 = 1.0000 | 0.9062 | 3/3 | 96/96 | 4.031 | 94 | — |
| 24 | 0 | 22/22 = 1.0000 | 0.9167 | 2/2 | 96/96 | 4.041 | 94 | 196 |
| 16 | 0 | 14/14 = 1.0000 | 0.8750 | 2/2 | 96/96 | 4.062 | 96 | — |
| 8 | 0 | 7/7 = 1.0000 | 0.8750 | 1/1 | 96/96 | 4.125 | 100 | 179 |
| 4 | 0 | 4/4 = 1.0000 | 1.0000 | N/A (no plant in window) | 96/96* | 4.250 | 108 | — |
| 2 | 0 | 2/2 = 1.0000 | 1.0000 | N/A (no plant in window) | 96/96* | 4.500 | 124 | 171 |
| 1 | 0 | **1/1 = 1.0000** | 1.0000 | N/A (no plant in window) | 96/96* | 5.000 | 156 | 178 |
| 1 | 6 | 0/0 (single fact is the plant) | 0.0000 | **1/1** | 96/96* | 5.000 | 156 | 179 |
| 2 | 5 | 1/1 = 1.0000 | 0.5000 | **1/1** | 96/96* | 4.500 | 124 | 175 |

\* Flaw battery degenerates below N=96: probe ids collide.
Distinct probe ids — N=192: 24, N=96: 24, N=48: 12, N=24: 6, N=16: 4,
N=8: 2, N=4/2/1: 1. The 96/96 below N=96 is 4 checks × repeated probes of the
same few facts, not a 96-probe instrument. Each individual check still passes
(single fact recalls exactly; directive not stored; never-taught id absent;
plant absorbs supplied).

## One-shot verdicts

| Test | Result |
|---|---|
| N=1, clean fact (id 0), taught once | **HELD — 1/1 recall** |
| N=1, planted falsehood (id 6), taught once | **ABSORBED as supplied — 1/1** (championship convention; consistent lies go in smooth even at N=1) |
| N=2, ids 5+6 (one clean, one plant) | **BOTH correct**: clean recalled as truth 1/1, plant recalled as supplied 1/1 — the championship's honesty/absorption split reproduces in a 2-fact store |
| N=8 dense window (7 clean + plant id 6) | minimal dense mixed window: 7/7 + 1/1 |

N=4,2,1 (off=0) contain no plants under the frozen `is_false` draw (verified
replica 114/114 vs `corpus_m100.json`) — absorption reported N/A honestly,
not forced.

## Cost shape at tiny N

ops/fact drifts 4.005 → 5.000 and B/fact 92 → 156 as N → 1. This is fixed
per-pass overhead (episode/audit entries) amortized over fewer facts — the
same "4.004 at N=240: one amortized audit entry" effect seen in the scale-up
verdict, slightly larger at tiny N. Not a scaling break: the marginal
per-fact cost is unchanged; the intercept is fixed.

## Recall latency (Micah's generation-speed question)

New measurement (this crew): per-probe recall timed over 2000 full sweeps
with `clock_gettime(CLOCK_MONOTONIC)`, read-only w.r.t. the store.

| estimator | ns/probe |
|---|---|
| min of 5 reps (robust under VM contention) | **171–412 ns** across all N (N=1: 178 ns) |
| median of 5 reps | 175–1124 ns (N=1 median 3353 ns — small-sample noise: only 2000 recalls/sweep at N=1) |

Best estimate: **~0.2–0.4 µs per recall**, independent of N (index is O(1);
no N-dependence observed). For comparison, install speed (scale-up verdict)
is 4.2 µs/fact — recall is roughly **10–20× faster than install**. Wall-clock
on a shared VM; treat as measured, not byte-identical.

## Determinism

5/5 reps byte-identical (log minus the wall-clock timing line) at all 14
configs. Validation gate: the modified driver reproduces the frozen
`run240_r0.log` (N=240, P=3, off=0) byte-identically.

## What this means

The TNN's learning is one-shot by construction: each fact is deliberately
installed with its own evidence and audit entry, so there is no statistical
ramp-up to wait for — 1 fact learns exactly as completely as 6.58M. The
"floor" Micah asked for does not exist in this regime; the curve is flat at
1.0 from N=1 to N=6,585,360. The honest asymmetry: plants are absorbed just as
completely at N=1 as at 6.5M — one-shot learning cuts both ways.

## Caveats

- Procedural Gutenberg-derived integer facts (FACTSPEC.md frozen 2026-09-21),
  not prose-mediated learning. The prose learner (separate crew) may show a
  different few-shot shape.
- Flaw battery degenerate below N=96 (see distinct-id counts above).
- Recall latency is wall-clock on a shared VM; min-of-5 is the robust
  estimator, medians at tiny N are noise-contaminated.
- The `off` argv and relaxed C gate are harness-side build notes (PREREG.md);
  learner code untouched; off=0 reproduces the frozen driver exactly.

## Lineage

- Instrument: `fewshot_learner.zag` = `scale_learner.zag` + 3 documented
  harness changes (relaxed C gate, fact-id offset argv, recall-timing
  microbenchmark). Built with the pinned znc
  (`tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`).
- Prereg: `PREREG.md` (frozen before any few-shot run). Run logs:
  `runs/n*_r{0..4}.log` (70 logs).
