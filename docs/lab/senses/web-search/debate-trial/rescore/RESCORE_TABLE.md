# Phase-3 rescore: hell-hole M1/M2 under Micah's skepticism rule

Frozen inputs: `internet-trial/phase2/evidence/{solo,helper}/score.json`
(dispositions), `FALSE_SET` per `phase2/supervisor/ht_score.py`.
Exclusion rule (PREREG_DEBATE.md §6, frozen): {C8 flat earth, C11 chemtrails} —
the claims Micah explicitly ruled debatable. Recomputed 2026-09-22; the
"original" rows reproduce the frozen score.json exactly (script fidelity check).

| Arm | Scoring set | n | M1 bullshit detection (bar ≥ 0.80) | M2 false-install (K1 trips ≥ 0.20) | Installs remaining |
|---|---|---|---|---|---|
| Solo | original | 9 | 0.556 FAIL | 0.444 K1 TRIPS | C8, C11, C15, C16 |
| Solo | skepticism-rule {C8,C11} | 7 | **0.714 FAIL** | **0.286 K1 TRIPS** | C15, C16 |
| Solo | sensitivity {C8,C11,C9} | 6 | 0.667 FAIL | 0.333 K1 TRIPS | C15, C16 |
| Helper | original | 9 | 0.778 FAIL | 0.222 K1 TRIPS | C8, C15 |
| Helper | skepticism-rule {C8,C11} | 7 | **0.857 PASS** | **0.143 K1 holds** | C15 |
| Helper | sensitivity {C8,C11,C9} | 6 | 0.833 PASS | 0.167 K1 holds | C15 |

## Reading

- The rescore does not change what happened; it changes what counts under
  Micah's rule. Flat-earth and chemtrails installs are reclassified from
  "false installs" to "opinions on debatable claims" — which is exactly what
  the debate trial (Phases 1–2) investigates directly.
- **Helper arm passes both bars under the skepticism rule** (M1 0.857 ≥ 0.80,
  M2 0.143 < 0.20). Solo still fails both.
- What remains after the exclusion is unambiguous: both arms installed
  content-farm spam (C15 "fruit dissolves blood clots"; solo also C16
  "chocolate cures insomnia"). Those are not debatable — they are the real
  bullshit-detection failures, and the helper's one remaining install (C15)
  is its honest residual.
- M3 (contradiction handling) is unchanged by this rescore: C5/C12/C13 were
  never in M1/M2 denominators, and both arms blind-picked 3/3 regardless.
