# VERDICT — F20 USD (Unearned-Stability Discount), mech 20

- **Date:** 2026-09-24
- **Authority:** PREREG_FORKROUND.md §3 (F20) + ideas/native1_forks.md Fork 1
  (authoritative on discrepancies). Coordinator sign-off 2026-09-25.
- **Verdict: KILLED** — falsification (c) w9 fits to 0 (feature is dead
  weight, not a mechanism); falsification (b) B4 < 0.50 on honest legs
  also fires. Kill is honest per the fork's own spec and the build brief
  ("a clamp attractor or dead w9 is a kill, not a tune-up").

## Kill-bar table (frozen analyzer defs; B8 amended §4b)

| Bar | F20 (m20) | NEC m9 (yardstick) | Δ vs NEC | Threshold | Result |
|-----|-----------|-------------------|----------|-----------|--------|
| B1 (1→0) | 0 | 0 | 0 | =0 | PASS |
| B2 (V1,V2) | 0, 0 | 0, 0 | 0 | =0,=0 | PASS* |
| B3 (strict Gviol) | 2 (redteam, n=3→2→1→1) | 6 | −4 | =0 every family | FAIL |
| B4 (meanConfCorrect) | 0.0000 (n=4005) | 0.972 | −0.972 | ≥0.50 | FAIL → kill (b) |
| B4b (honest floors) | 0.0000 all 4 | ≥0.984 | ≈−0.984 | ≥0.50 | FAIL → kill (b) |
| B5 (separation) | 0.0000 | 0.668 | −0.668 | ≥0.20 | FAIL |
| B6 (recall) | 1.00 (P/trap vacuous) | 1.00 | 0 | ≥0.95 | PASS |
| B7 (abstention) | 0.1475 | 0.148 | −0.0005 | ≤0.30 | PASS |
| B8 (amended §4b) | admit/cost/logic/revoke/O VACUOUS-fail; D pass; P pass (perfect-cal); redteam/trap VOID | — | — | per §4b | FAIL |
| B9 (identity vs M4) | 5240/5240 = 100% | 100% | 0 | 100% | PASS |
| B12 (recorded) | 0 G>0 crossings | — | — | recorded | — |
| B13 (underconf) | 33 (F,d) < −0.100 | 6 | +27 | =0 | FAIL |
| B3pi (recorded) | 0 / 3467 pairs | — | — | recorded | — |

\* B2 "passes" only via the clamp attractor (constant conf ⇒ no rises) —
degenerate compliance, named here, does not count toward support.

## Falsification triggers (ideas file, authoritative)
- **(a)** trap/redteam strict G(d+1)>G(d) with n_rel≥16 at both rungs:
  **0 hits — clear** (the 2 redteam B3 violations are n=3→2→1→1 tiny-n
  noise, below the n_rel≥16 gate; trap G flat at +0.000).
- **(b)** B4 < 0.50 on any honest leg: **4 hits — KILL.**
  admit/cost/logic/revoke all 0.0000.
- **(c)** w9 fits to 0 on a majority of legs: **fitted w9 = 0 — KILL.**
  The discount is identically zero on all 37 legs.

## Why w9 died (mechanistic autopsy, not a tune-up)
1. Fitted weights: w1=1000, w2..w8=0, w9=0, b=−100387 — the w1..w8/b
   trajectory reproduces the frozen base trainer bit-for-bit, so the F20
   trainer is a faithful §5 extension; w9 is the only new degree of
   freedom and it never moved.
2. Independent exact-integer re-simulation of pass 0 (b held at full
   height, i.e. WITHOUT the G-batch collapse): max per-cell w9 gradient
   numerator = 2,567,604 < DIV=4,000,000 → **w9 could never move by ±1 on
   any training cell**; 0 up-steps, 0 down-steps over the full pass.
   The w9 signal is SUB-QUANTAL under the frozen DIV — structural, not a
   transient, not the projection, not the b-race.
3. Note the feature itself fires broadly on the frozen data (admit-correct
   50.9% fire, cost-correct 46.4%, O-correct 77.8%), so even absent the
   quantization problem the "trap signature" premise is empirically
   shaky — evidence does NOT track stability on this harness.

## The clamp attractor
C = clamp(f1 − 100387, 0, 1000) = 0 on every released cell. All B4/B4b/B5
failures and all 33 B13 failures are this attractor, not USD working. The
fork's mechanistic claim (G flat "by construction of the population the
metric scores") is not tested — the head never learned the discount.

## What was NOT the cause
- Not an implementation bug: shared-weight trajectory bit-identical to
  the frozen base trainer; A/B byte-identical builds, runs, params.
- Not under-training: passes=100 (600 epochs), the deepest precedent.
- Not the projection: w9 never went positive to be projected.

## Commits
- `c0ec3328397c9b050e0eae9116a2ff4f74e3faf9` — sources, optimizer choice
  (pre-run), build log, analysis script.
- (batch 2: params, training logs, 37-leg results, analysis output, this
  verdict — SHA on completion.)

## Residual notes
- PREREG_FORKROUND.md §2 transcribes the features.tsv SHA256 as
  `...e65e897d`; on-disk file is `...e65a897d`, matching prior rounds'
  records — one-char transcription typo in the prereg, file is genuine.
- Per-item B3pi = 0/3467 and B12 = 0 crossings recorded for the Q5
  unsatisfiability-thesis evidence pool (constant-conf policy).
