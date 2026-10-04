# PREREG: C1 Smallest-Consistent-K Revision Experiment (FROZEN)

Date: 2026-09-30. Worker: C1 Smallest-Consistent-K Revision Worker.
Status: PREREG-FROZEN. Committed alone before any implementation exists.

## Background

FE-FAMILY-CONFIRMED (6e03b2fa5): 24/24 R1 APPLICATION misses on the F-E family, all caused by periodic-demo key ambiguity. The rotation class in the frozen contestant (b8d38d9c8:contestant.zag, lines 792-822) takes the LARGEST matching k per demo: the inner loop `while(k<din.len)` assigns `found=k` on every match, so `found` ends as the largest k admitting the demo. For a period-2 demo under true key k=1 (e.g. "ahah" -> "haha"), both k=1 and k=3 match; the tie-break yields k=3 for that demo vs k=1 for a normal demo, the class finds inconsistency, collapses, and the query misses via fallback.

## The revision

Change exactly one line in the rotation class: the per-demo key selection from largest-match-k to smallest-consistent-k. In `contestant.zag` line 807:

BEFORE: `if(streq(rs,dout)==1){found=k;}`
AFTER:  `if(streq(rs,dout)==1 && found<0){found=k;}`

This makes `found` keep the FIRST (smallest) matching k instead of the last (largest). No other source line changes. The variant is a minimal, isolated revision, not a new capability.

## Frozen predictions

P-SK1: On the 8 sealed F-E worlds (reused byte-identical from 6e03b2fa5, 3 reps each = 24 runs), R1 (post-change rotation query) converts from 24/24 APPLICATION misses to 24/24 HITS. The smallest-consistent-k rule fires k=1 (the true key) for period-2 demos, the rotation class stays consistent, and the query hits.

P-SK2: R2 (revert) remains 24/24 hits (unchanged from FE-FAMILY-CONFIRMED).

P-SK3: R3 (pa control) remains 24/24 hits (unchanged).

P-SK4: H0-style reversal-ambiguity outcomes are unchanged: the F-A baseline of 0/24 R2 misses is preserved. The tie-break change affects only the rotation class, not reversal, char-map, duplication, or fallback.

P-SK5: Detection (D1) and diagnosis (D2) remain clean (0 failures) across all runs.

## Kill bars

K1: This prereg (commit alone) strictly precedes the implementation (frozen variant source+binary, commit alone), which strictly precedes the runs (results, commit alone). Verifiable via `git merge-base --is-ancestor` on the commit graph.

K2: The 8 F-E sealed worlds are reused byte-identical from 6e03b2fa5 (sha256 verified before running; no regeneration). 24 runs executed (8 worlds x 3 reps). All results recorded honestly against the frozen predictions above.

K3: Pure Zag + shell. Zero Python anywhere. No em dashes (shell-only `check_no_dash.sh`). Contaminated paper untouched. The ONLY source change vs the frozen contestant is the one-line tie-break (verified with `diff`).

## Verdict labels

SMALLK-REVISION-CONFIRMED if P-SK1 through P-SK5 all hold: smallest-consistent-k is the causal lever for the F-E misses.

SMALLK-REVISION-REFUTED if P-SK1 fails (misses do not convert to hits) or any of P-SK2 through P-SK5 fail: the tie-break is not the causal lever, or the change has unintended side effects.
