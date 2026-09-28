# COST — wall-clock comparison (contender A vs native AR)

**Method:** interleaved runs on the same machine, same fixture plan
(`plans/pv_seq.txt`, 30 s / 44.1 kHz), equivalent s32-mix output
(`seq+mix` vs native `seqmix`; both write 5,292,000-byte mix dumps).
Python `time.time()` around subprocess; `/usr/bin/time` absent on VM.
Peak RSS inconclusive (`RUSAGE_CHILDREN` cumulative on this VM).

## Mix-level (synthesis work only; architecturally honest per §2 DET note)

6 interleaved runs, 2026-09-24:

| run | A (s) | Native (s) |
|---|---|---|
| 0 | 7.96 | 4.58 |
| 1 | 6.38 | 4.35 |
| 2 | 6.42 | 5.09 |
| 3 | 5.13 | 4.04 |
| 4 | 6.15 | 4.41 |
| 5 | 6.67 | 3.92 |
| **median** | **6.40** | **4.38** |

Every A run slower than every native run. Gap is consistent, not noise.

## WAV-level (includes mastering/writer)

4 interleaved runs: A median 6.01 s, native median 4.74 s. Same direction.

## Formation cost (for completeness)

`form_par`: 0.03–0.04 s (negligible vs render).

## Root cause

Architectural, not a bug: pure `f(plan,t)` recomputes oscillator phase per
sample per voice via integer division (`(f0q*tr)/SR`, mod 2^32 wrap);
native's carried phase is a single addition per sample per voice. This is the
fundamental price of statelessness. PAR's multi-core dividend is not
demonstrated by this single-threaded Zag binary.

## Verdict on COST axis

**Native wins.** ~46% gap at mix level. This is the regression that blocks a
clean §6 overthrow (see VERDICT_AUDIO.md).
