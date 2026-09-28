# CREW A — §6 VERDICT: Contender A (pure-PAR) vs NATIVE. 2026-09-24.

## Per-axis scorecard (frozen battery, fresh builds, pinned toolchain)

| Axis | A | NATIVE | Winner |
|---|---|---|---|
| DET (mix-level, 2 renders) | byte-identical | byte-identical | TIE |
| QUALITY (9 V10 bars) | 9/9 PASS | 9/9 PASS (dive) | TIE |
| COHERENCE (motif recurrence) | 1.0000000000, byte-identical windows | 0.736557 (dive) | **A** |
| RT-LONG (RESPOND trap) | 440.00 Hz, +0.01¢ | 454.38 Hz, +55.69¢ | **A** |
| RT-CASCADE (4 fault models) | 0 post-fault diffs (all) | 5,854 post-fault diffs | **A** |
| RT-EDGE (truncation) | legitimate-only diffs | — | PASS |
| §5 red team | survives (6/6 probes) | — | PASS |
| COST (CPU, wait4, contention-free) | 0.92 s | 0.80 s → **1.15×** | **NATIVE** |
| Memory (peak RSS) | 15.3 MB | 15.4 MB | TIE |
| Dense polyphony (A-poly fork) | clips from N=2 (0.037→0.707), no adaptation | servo halves RMS, darkens, AGC 0.5 floor | **NATIVE** (tradeoff) |

## Fork scorecard

| Fork | Prereg claim | Result |
|---|---|---|
| A-fmt (parallel formation) | byte-identical shards + speedup_form ≥ 0.7×S @ S=8 | **Identity PASS, speedup FAIL** — mechanism proven, no measured speedup in this implementation/environment; E2E impact nil |
| A-long (600 s drift) | zero drift ≥5 min, motif recurrence exact | **PASS** — 600 s byte-identical reruns, motif @590 s byte-identical, bed ±1.65 ppm both horizons |
| A-poly (dense polyphony) | document failure mode vs AR | **Confirmed regression** — A clips, no output-adaptive behavior; native servo self-limits at 4.79 FS plan-deviation |

## §6 overthrow test

Overthrow requires: all quality bars pass ✓, coherence ≥ NATIVE ✓,
improvement on ≥1 target axis ✓ (coherence, RT-LONG, RT-CASCADE),
determinism ✓, §5 red-team survival ✓, **and no regression elsewhere** ✗.

**A regresses on COST (1.15× single-threaded CPU — the architectural price
of per-sample integer-division phase recompute) and on dense-polyphony
headroom (no output-adaptive behavior; the servo-AR's is a genuine win for
the native side, at 4.79 FS plan-deviation cost).** The regression clause
fails. Additionally, A-fmt failed its preregistered speedup bar — the
scaling axis delivers no demonstrated improvement.

## VERDICT: PARTIAL WIN / NO OVERTHROW.

A is strictly better on statelessness-derived properties (exact coherence,
RESPOND resolution, fault containment, 600 s drift-free recurrence) and
ties quality/determinism/memory. It loses on single-threaded cost and
dense-sum headroom. Per the frozen rule — tie keeps NATIVE, and two
regressions are not a tie — **NATIVE keeps the throne.**

A's wins are all consequences of one architectural property: the
generation path never reads the mix (pure f(plan,t)). That property is
proven exactly (0/1,190,699 post-fault, byte-identical 600 s reruns,
max|Σ(solos)−chord| = 0). The losses are the price of that property: no
feedback loop means no cost amortization and no self-limiting. The
tournament should treat this as a characterized tradeoff, not a bug —
the characterization's framing stands: neither side is "wrong"; they
optimize different things.
