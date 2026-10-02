# RESULTS: C1 Smallest-Consistent-K Revision Experiment

Date: 2026-09-30. Worker: C1 Smallest-Consistent-K Revision Worker.
Status: SMALLK-REVISION-CONFIRMED.

## Commits

- Prereg: 22e2554b8 (FROZEN; committed alone before implementation)
- Freeze: 13efc8f86 (variant source+binary; one-line change; committed alone)
- Results: this commit (committed alone)

Ordering verified: 22e2554b8 < 13efc8f86 < this commit via `git merge-base --is-ancestor`.

## Method

The 8 sealed F-E worlds from 6e03b2fa5 were reused byte-identical
(sha256 verified: all 8 E0-E7 turns.jsonl match the sealed commit).
The diag and agg instruments were reused byte-identical from the F-E
freeze (0d8bdc111). Only the contestant binary was swapped to the
smallest-consistent-k variant (13efc8f86:contestant_smallk_bin).

24 runs executed (8 worlds x 3 reps). All reps byte-identical per world
(cmp on replies.jsonl, scores.jsonl, state.txt).

## Results vs frozen predictions

| Prediction | Observed | Verdict |
|---|---|---|
| P-SK1: 24/24 R1 HITS | 24/24 correct (scores.jsonl) | PASS |
| P-SK2: 24/24 R2 hits | 24/24 correct | PASS |
| P-SK3: 24/24 R3 hits | 24/24 correct | PASS |
| P-SK4: H0 reversal-ambiguity unchanged | 0 det_fail, 0 diag_fail; no reversal class regressions | PASS |
| P-SK5: D1/D2 clean | 0 det_fail, 0 diag_fail across 24 runs | PASS |

## The diag UNCLASSIFIED artifact (explained)

The diag output shows R1 as `loc=UNCLASSIFIED` (24/24) rather than
`loc=HIT-OK`. This is a classification artifact, not a miss. The diag's
internal model predicts the contestant's output based on the OLD
largest-k behavior: for E0 it predicts `haha` (the rotation-by-3 fallback
output). The revised contestant outputs `tqoq`, which the world key
(`key.json`) confirms is the CORRECT R1 answer for E0.

The diag classifies as HIT-OK only when its prediction matches the
actual AND the answer is correct. Here the diag's prediction is stale
(it models the old tie-break), so pred != actual, yielding UNCLASSIFIED.
The ground-truth scores (`scores.jsonl`, from `run_race.sh` comparing
against `key.json`) show `correct:1` for all 24 R1.

In short: the 24/24 R1 are HITS. The diag needs its rotation model
updated to reflect smallest-consistent-k; its current UNCLASSIFIED
reflects model staleness, not contestant failure.

## Mechanism (confirmed)

The one-line change (line 807: `found=k` to `found=k` only if `found<0`)
makes the rotation class select the smallest consistent k per demo.
For period-2 demos under true key k=1, both k=1 and k=3 match; the
revised tie-break selects k=1. The class now finds consistency across
demos (1 vs 1, instead of 3 vs 1), does not collapse, and the query hits
via the rotation class (not fallback).

## Interpretation

SMALLK-REVISION-CONFIRMED. The smallest-consistent-k tie-break is the
causal lever for the F-E family misses. The 24/24 misses convert to
24/24 hits with no change to R2, R3, detection, diagnosis, or
reversal-ambiguity behavior. The change is minimal (one line) and
isolated (only the rotation class tie-break).

## Kill bars

K1: Prereg (22e2554b8) strictly precedes freeze (13efc8f86) strictly
precedes results (this commit). Verified via merge-base.

K2: The 8 F-E worlds reused byte-identical (sha256 verified). 24 runs
executed. All results recorded honestly against the frozen predictions.

K3: Pure Zag + shell. Zero Python. No em dashes (shell-only
check_no_dash.sh). Contaminated paper untouched. The ONLY source change
vs the frozen contestant is the one-line tie-break (verified with diff).

## Architecture

0 new cognition source lines (one line modified, not added). 0 new
semantic cases/modes/bridges/handlers. This is a revision experiment,
not a new capability.
