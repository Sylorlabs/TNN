# RECOVERY: wall-time measurement for DEEP-TRIAL (K3 cost honesty)

Wave: wave-20260930-1421pdt recovery, run by the wave-20260930-1721pdt coordinator.
Reason: PREREG_TRADES.md K3 requires wall time reported; the 1421 worker's
three runs recorded trials and state bytes but no wall time. This file records
a recovery measurement on the FROZEN committed binary (deep_trial_bin,
committed in 02fcab591, unmodified). No science changed: the binary is
deterministic and the 4th run is byte-identical to run1.out.

Measurement (shell `time`, single run, 2026-09-30):
- real 0m0.007s, user 0m0.001s, sys 0m0.003s
- exit 0, zero stderr bytes
- stdout md5 999f204f2d44b7cadb4b76b4e4785f17 (matches run1.out, run2.out, run3.out)

Cost/capability summary (from the frozen run outputs):
- baseline trials 64, deep trials 170, ratio 2.66x (deep/baseline)
- baseline promotions 3 (F1, F2, F3), deep promotions 5 (F1, F2, F3, F4, F5)
- baseline novel accuracy 15/25, deep novel accuracy 25/25
- state bytes 12644 (fixed buffers, printed by the binary)
- trials per promoted rule: baseline 64/3 = 21.3, deep 170/5 = 34.0
- trials per correct novel prediction: baseline 64/15 = 4.27, deep 170/25 = 6.8

Note on the prereg's expected 70x ratio: the value-signature dedupe collapsed
the 418-candidate enumeration to 170 total EQ checks across all seven
families, so the realized cost is far below the prereg's rough estimate.
The estimate was a ceiling guess, not a kill bar; K3 requires measurement,
not a specific ratio. All cost figures are now measured and reported.

K3 status with this file: trials per family and totals printed (in the
binary output), ratio computed above, wall time and state bytes reported.
Whether this recovery measurement cures the worker's K3 gap is a debate
motion for the wave-20260930-1721pdt debate group.

No em-dashes in this documentation.
