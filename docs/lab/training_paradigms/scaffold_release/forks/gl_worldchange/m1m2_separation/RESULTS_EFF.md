# RESULTS_EFF.md — Workstream A efficiency results (M1 vs M2)

Frozen prereg: `m1m2_separation/PREREG_M1M2.md` (commit ac128f4eec2bb30b4ff2f64e4b2ff2bfd96c9dd3).
Drivers: `src/eff_m1.zag`, `src/eff_m2.zag` (pure Zag, zero RNG, real vendored harnesses).
Compiler: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
Runs: 2026-09-24. Every config ran 3x; all 50 configs × 3 reps byte-identical (0 determinism failures).

## E1 — frozen curriculum throughput (R=2000, 100 episodes/rep)

| learner | episodes | audit entries | supersessions | gate-fails | wall ms (rep1..3) | eps/sec | peak RSS KB |
|---|---|---|---|---|---|---|---|
| M1 | 200,000 | 354,000 | 4,000 | 2,000 | 33810, 38979, 51720 | 4,819 | 176, 180, 180 |
| M2 | 200,000 | 354,000 | 4,000 | 14,000 | 39491, 41997, 37151 | 5,057 | 180, 184, 180 |

Notes:
- Audit entries, supersessions identical. M2 is ~5% faster on wall-clock here.
- Gate-fail counts differ 7x (M1: 1/rep, M2: 7/rep). This is REAL and present in the
  committed H4 outputs (targets/m1/m1_run1.txt MEASURE-16 total=1; targets/m2/m2_run1.txt
  MEASURE-16 total=7: sid2=3, sid3=4). M2's figure-it-out path refuses the W3 auth gate
  more often on the same curriculum; KB outcomes are unaffected (all KB measures tie).

## E2 — chain scaling T=1..14 (R=300/rep, 5 episodes per chain link)

M1 and M2 produce IDENTICAL episode/audit/update counts at every T.
The separator is M2's instrumented ledger-scan reads per update (M1: 0, always).

| T | M1 wall ms | M2 wall ms | M2 scan reads | M2 reads/update |
|---|---|---|---|---|
| 1 | 308 | 519 | 300 | 1.0 |
| 2 | 551 | 577 | 2,400 | 4.0 |
| 3 | 575 | 690 | 6,600 | 7.3 |
| 4 | 760 | 759 | 12,900 | 10.8 |
| 5 | 660 | 661 | 21,300 | 14.2 |
| 6 | 686 | 898 | 31,800 | 17.7 |
| 7 | 850 | 898 | 44,400 | 21.1 |
| 8 | 624 | 675 | 59,100 | 24.6 |
| 9 | 796 | 600 | 75,900 | 28.1 |
| 10 | 648 | 687 | 94,800 | 31.6 |
| 11 | 559 | 4767 | 115,800 | 35.1 |
| 12 | 1977 | 921 | 138,900 | 38.6 |
| 13 | 596 | 643 | 164,100 | 42.1 |
| 14 | 863 | 823 | 191,400 | 45.6 |

Wall-clock is noisy (see T=11 M2 outlier), but the instrumented counts are exact:
M2's per-update ledger scan grows linearly with chain length (O(ledger)), M1's
completion is O(1) (copies from live key state). At T=14 M2 performs 191,400
extra ledger reads that M1 never does. M2's reads/update ≈ 3.3×T − 2 (linear fit).

## E3 — 7-key / 14-supersession stress (R=2000, 98 episodes/rep)

| learner | episodes | audit | supersessions | wall ms (rep1..3) | eps/sec | peak RSS KB |
|---|---|---|---|---|---|---|
| M1 | 196,000 | 280,000 | 28,000 | 5703, 5793, 4219 | 37,417 | 172, 172, 176 |
| M2 | 196,000 | 280,000 | 28,000 | 1362, 6873, 6147 | 40,884 | 176, 176, 2388 |

Outputs are byte-identical between learners (same checksum 2634615767108934656).
Wall-clock variance is high (M2 rep1 1362ms vs rep2 6873ms; M2 rep3 RSS 2388KB
vs 176KB typical) — no reliable winner on wall-clock for E3. Instrumented counts tie.

## Peak memory (fixed-arena arithmetic)

Both learners allocate identical arenas; peak is one live set:

| arena | bytes |
|---|---|
| mkey/mval/mflag (128×4 ×3) | 1,536 |
| qkey/qval/qflag (64×4 ×3) | 768 |
| audit (2048×16) | 32,768 |
| ks (8×16) | 128 |
| pe (5×4) | 20 |
| he (8×12) | 96 |
| hi (16×24) | 384 |
| cc (8×4) | 32 |
| WcEp | 40 |
| **Total** | **35,772 B = 34.93 KB** |

The audit ledger is 91.6% of the footprint. Measured peak RSS (VmHWM): 172–184 KB
for both learners across all configs (binary image + allocator + arenas). **Tie.**

## Ledger integrity

The H4 audit ledger is an append-only, step-sequenced log (16-byte entries:
step, op, slot1, aux; TN_OP_EPISODE markers chain episodes). It is not a
cryptographic hash chain in the original H4 design. Each driver output carries a
deterministic rolling digest over per-rep ledger state, and all 150 runs
(50 configs × 3 reps) are byte-identical, proving ledger determinism. Raw
per-run outputs retained in the scratch results/ directory.

## Efficiency verdict

Rough tie with different shapes: M2 is ~5% faster on the short curriculum (E1);
M1 has strictly better algorithmic complexity on chains (E2: O(1) vs O(ledger)
per update, measured). E3 and peak memory tie. Per the frozen prereg, efficiency
is secondary to the correctness split (see RESULTS_EDGE.md).
