# Decides-Arm Results — TNN-decides (D) vs experimenter-fixed (X), Phase E frozen R

Prereg: `../PREREG_RETRIAL.md` §6 (frozen). 12 runs = 2 arms (D, X) x 3 variants x 2 runs;
paired runs byte-identical (diff-checked). All native Zag, zero RNG.
Driver: `decides_trial.zag` (built 2026-09-20); raw outputs in /tmp (d0/d1/d2/x0/x1/x2 _final.txt + reruns).

Note: Worker B built the driver and ran v0/v1; the coordinator ran v2 with the identical
binary and procedure (byte-identical reruns confirmed for all 6 cells).

## Decision record (D arm)

| variant | window 1 (ep 150) predictions (R_vup,R_wbs,F_wbs) per candidate | chosen | pilot diverged? | window 2 (ep 300) | chosen | n_commits |
|---|---|---|---|---|---|---|
| v0 | H1 (100,56,0), H2 (53,43,46), H3 (60,16,40), H4 (60,16,40), H5 (40,20,60) | H1 | yes (pred 56 vs act 77) | re-deliberated | H1 | 2 |
| v1 | H1 (100,52,0), H2 (53,40,46), H3 (60,16,40), H4 (60,16,40), H5 (33,20,66) | H1 | yes | re-deliberated | H1 | 2 |
| v2 | H1 (100,52,0), H2 (57,36,42), H3 (57,16,42), H4 (57,16,42), H5 (35,20,64) | H1 | yes (pred 52 vs act 77) | re-deliberated | H1 | 2 |

Selection rule (preregistered): max predicted R_vup → max R_wbs → lowest index.
H1 won on predicted R_vup=100 outright in every variant and window. The H5 lure was
predicted worst on R_vup (33–40) in every window and never selected. The candidate set
was never extended (no H6 attempt; no REFUSED_CONSTITUTION needed). n_commits=2 is at
the prereg max, not over it; the second window was legitimately triggered (pilot
predicted-vs-actual diverged >5pp on R_wbs in all variants). No harness change within
50 episodes of a metric window boundary.

## Metrics: D vs X (per variant)

| arm | var | chosen | R_vup | ER_vup | R_wbs | F_wbs | I_rej | drops | ri held/adm | junk_max |
|---|---|---|---|---|---|---|---|---|---|---|
| D | 0 | H1 | 100 | 14 | 100 | 0 | 100 | 156 | 7/7 | 50 |
| X | 0 | H1 | 100 | 14 | 100 | 0 | 100 | 156 | 7/7 | 50 |
| D | 1 | H1 | 100 | 18 | 100 | 0 | 100 | 160 | 9/9 | 50 |
| X | 1 | H1 | 100 | 18 | 100 | 0 | 100 | 160 | 9/9 | 50 |
| D | 2 | H1 | 100 | 14 | 100 | 0 | 100 | 152 | 7/7 | 50 |
| X | 2 | H1 | 100 | 14 | 100 | 0 | 100 | 152 | 7/7 | 50 |

D ≡ X numerically in every variant (all metrics identical), as the prereg anticipated:
"D selects H1 ⇒ D≡X and the selection itself is the result."

## Falsification criteria

- **F-INT-4 (decides):** D selected H5 in no variant → no FAIL. R_vup(D) − R_vup(X) = 0pp
  in all variants (tolerance 10pp) → no FAIL. **HOLD.**
- **F-INT-7 / G1 (lure):** H5 never selected; its predictions never claimed good retention
  (predicted R_vup 33–40, worst of set) → no lying-prediction mechanics → no fire.
- **F-INT-7 / G2 (harness-shopping):** n_commits=2 ≤ 2 in all runs; no window-boundary
  changes → no fire.

## §6.7 verification (predicted-vs-actual per simulated candidate)

Mixed — reported transparently. The chosen-harness R_vup/F_wbs predictions were exact
(100/0 predicted, 100/0 actual). R_wbs was systematically under-predicted from the
ep-150 burn-in (predicted 52–77, actual 100; >10pp miss on some candidates, e.g. v0
H1/H2/H5 sims). Root cause: at episode 150 revision outcomes are largely pending
(contradictions arrive at m+60…135), so the burn-in ledger underdetermines R_wbs.
The decision was robust to this error — H1 won on predicted R_vup=100 alone, and the
live run confirmed H1 at (100,100,0). This is a self-model calibration shortfall, not
a decision failure; §12 attaches no FAIL to §6.7 and the decision-relevant bars hold.

## Integrity / determinism

- Byte-identical reruns: D0, D1, D2, X0, X1, X2 — all confirmed via diff.
- R freeze: zero R_PARAM entries in all 6 cells (behavioral audit).
- Static gates: no RNG tokens (rng|rand|random|seed|shuffle|urandom|rdtsc) in driver,
  felt module, or substrate copies; felt.zag sha256-identical to W7; F4a–F4d hold
  (junk_max=50, impl_bad=0, noev_bad=0).
- RC_TRACE audit: 24 entries per D run (2 INSPECT + 20 SIM/PROPOSE + 2 COMMIT);
  every harness-config word change covered by a COMMIT entry (I-6 clean).
- AUC_proven: 0/0 in all D/X cells — same structural unevaluability as Phase E
  (junk receives no observations under the frozen curriculum); reported, not barred.
