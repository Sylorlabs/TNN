# One-Brain Round 3 — Measurement (v6, frozen)

- v6: `~/workspace/onebrain3/prereg/v6.tsv`, SHA-256
  `42d215ecebc9302141aaec93cc067a78effba79541059d2e60f6e165fe1139d0`
- Implementation: `~/workspace/onebrain3/impl/onebrain_v3.zag` (pure Zag).
- Each mode run 3×; all 9 modes byte-identical across reruns (K5″).
- Single-mode output byte-identical to v2 on v4 and v5 (pinned GEN→ELIM→ARGMAX).
- No RNG in source (grep for rand/srand/random: zero hits; K6″).

## Aggregate accuracy (44 items)

| mode     | correct | pct   |
|----------|---------|-------|
| single   | 20      | 45.5% |
| onebrain | 23      | 52.3% |
| ablate   | 21      | 47.7% |
| poison   | 4       | 9.1%  |
| min      | 23      | 52.3% |
| nF       | 22      | 50.0% |
| nS       | 22      | 50.0% |
| nA       | 22      | 50.0% |
| nG       | 23      | 52.3% |

## Per-problem winners (expected | single onebrain ablate poison min nF nS nA nG; ✓=correct)

| id  | exp | s  | ob | ab | po | mn | nF | nS | nA | nG |
|-----|-----|----|----|----|----|----|----|----|----|----|
| q01 | 18 | 16 | 18✓| 16 | -1 | 18✓| 16 | 16 | 16 | 18✓|
| q02 | 18 | 17 | 18✓| 17 | -1 | 18✓| 17 | 17 | 17 | 18✓|
| q03 | 20 | 19 | 20✓| 20✓| -1 | 20✓| 19 | 19 | 19 | 20✓|
| q04 | 14 | 13 | 14✓| 13 | -1 | 14✓| 13 | 13 | 13 | 14✓|
| q05 | 17 | 16 | 17✓| 17✓| -1 | 17✓| 16 | 16 | 16 | 17✓|
| q06 | 15 | 14 | 15✓| 14 | -1 | 15✓| 14 | 14 | 14 | 15✓|
| q07 | 15 | 13 | 15✓| 15✓| -1 | 15✓| 15✓| 15✓| 15✓| 15✓|
| q08 | 19 | 19✓| 19✓| 19✓| -1 | 19✓| 19✓| 19✓| 19✓| 19✓|
| q09 | 16 | 16✓| 16✓| 16✓| -1 | 16✓| 16✓| 16✓| 16✓| 16✓|
| q10 | 14 | 13 | 14✓| 14✓| -1 | 14✓| 14✓| 14✓| 14✓| 14✓|
| q11 | 17 | 17✓| 17✓| 17✓| -1 | 17✓| 17✓| 17✓| 17✓| 17✓|
| q12 | 20 | 20✓| 20✓| 20✓| -1 | 20✓| 20✓| 20✓| 20✓| 20✓|
| q13 | 15 | 13 | 15✓| 15✓| -1 | 15✓| 15✓| 15✓| 15✓| 15✓|
| q14 | 15 | 13 | 15✓| 15✓| -1 | 15✓| 15✓| 15✓| 15✓| 15✓|
| q15 | 15 | 13 | 15✓| 15✓| -1 | 15✓| 15✓| 15✓| 15✓| 15✓|
| q16 | 15 | 13 | 15✓| 15✓| -1 | 15✓| 15✓| 15✓| 15✓| 15✓|
| q17 | 16 | 16✓| 19 | 19 | -1 | 19 | 19 | 19 | 19 | 19 |
| q18 | 16 | 16✓| 19 | 19 | -1 | 19 | 19 | 19 | 19 | 19 |
| q19 | 16 | 16✓| 19 | 19 | -1 | 19 | 16✓| 16✓| 16✓| 19 |
| q20 | 16 | 16✓| 19 | 19 | -1 | 19 | 19 | 19 | 19 | 19 |
| q21 | 15 | 15✓| 19 | 15✓| -1 | 19 | 15✓| 15✓| 15✓| 19 |
| q22 | 15 | 15✓| 19 | 19 | -1 | 19 | 19 | 19 | 19 | 19 |
| q23 | 15 | 15✓| 19 | 19 | -1 | 19 | 15✓| 15✓| 15✓| 19 |
| q24 | 15 | 15✓| 19 | 19 | -1 | 19 | 15✓| 15✓| 15✓| 19 |
| q25 | 22 | 13 | 13 | 13 | 14 | 13 | 13 | 13 | 13 | 13 |
| q26 | 20 | 19 | 19 | 19 | -1 | 19 | 19 | 19 | 19 | 19 |
| q27 | 23 | 19 | 19 | 19 | -1 | 19 | 19 | 19 | 19 | 19 |
| q28 | 23 | 19 | 19 | 19 | 19 | 19 | 19 | 19 | 19 | 19 |
| q29 | 18 | 16 | 16 | 16 | -1 | 16 | 16 | 16 | 16 | 16 |
| q30 | 17 | 13 | 13 | 13 | -1 | 13 | 13 | 13 | 13 | 13 |
| q31 | 14 | 14✓| 15 | 14✓| -1 | 15 | 14✓| 14✓| 14✓| 15 |
| q32 | 15 | 13 | 13 | 13 | -1 | 13 | 13 | 13 | 13 | 13 |
| q33 | 21 | 21✓| 21✓| 21✓| -1 | 21✓| 21✓| 21✓| 21✓| 21✓|
| q34 | 21 | 21✓| 21✓| 21✓| -1 | 21✓| 21✓| 21✓| 21✓| 21✓|
| q35 | 14 | 13 | 13 | 13 | -1 | 13 | 13 | 13 | 13 | 13 |
| q36 | 18 | 17 | 17 | 17 | -1 | 17 | 17 | 17 | 17 | 17 |
| q37 | 13 | 13✓| 13✓| 13✓| 13✓| 13✓| 13✓| 13✓| 13✓| 13✓|
| q38 | 13 | 13✓| 13✓| 13✓| 13✓| 13✓| 13✓| 13✓| 13✓| 13✓|
| q39 | 13 | 13✓| 13✓| 13✓| 13✓| 13✓| 13✓| 13✓| 13✓| 13✓|
| q40 | 16 | 16✓| 16✓| 16✓| 16✓| 16✓| 16✓| 16✓| 16✓| 16✓|
| q41 | 23 | 19 | 19 | 19 | -1 | 19 | 19 | 19 | 19 | 19 |
| q42 | 23 | 19 | 19 | 19 | 19 | 19 | 19 | 19 | 19 | 19 |
| q43 | 23 | 19 | 19 | 19 | -1 | 19 | 19 | 19 | 19 | 19 |
| q44 | 19 | 19✓| 19✓| 19✓| -1 | 19✓| 19✓| 19✓| 19✓| 19✓|

## Category attribution

- **Cat A q01–q06 (duel helps): 6/6.** Trace-verified: q01
  `DUEL_DELIB kill=0(correction) by=7(assertion) evclass=1 trighits=1
  topicc=3 corr=0` — killed the spurious correction reading; compose 18 wins.
  Old conflict direction preserved; victim = least-evidenced threatened target.
- **Cat B q07–q12 (guard must abstain): 6/6.** Trace-verified: q07
  `kill=4(joke) by=7` then
  `DUEL_ABSTAIN victim=6(forget) by=7 why=annihilation-guard(alive_fired=1)` —
  the guard saved the operative forget reading. Winner 15.
- **Cat C q13–q24 (V4 denial binds): 4/12.** α items q13–q16 all correct
  (denial helps, as designed). β/γ items q17–q24: V4 denial removes the
  expected bid's support → 19 wins (wrong). This is the prereg's honest mix:
  the denial mechanism binds and hurts on 8/12. Single (no V4) gets q17–q24
  right; the loss is the mechanism's, reported honestly.
- **Cat D q25–q36 (reintegration room): 2/12** (q33, q34 only). The
  reintegration deliberates (full ledger-cited trace) but does not find the
  contestable winners (22/23/20/18/17/14/15). Honest: the room was there,
  the mechanism didn't take it.
- **Cat E q37–q40 (anchors): 4/4.** Unchanged by fork machinery.
- **Cat F q41–q44 (withhold/challenge): 1/4.** q44 correct; q41–q43 give 19
  (challenge) instead of 23 (withhold) — pre-existing v2 GEN limitation
  (single also 19), not a round-3 regression.

## Neuter deltas vs onebrain (K4″ causality)

| neuter | deltas | items |
|--------|--------|-------|
| nF (fork→0) | 11 | q01,q02,q03,q04,q05,q06,q19,q21,q23,q24,q31 |
| nS (subpass→null) | 11 | same 11 |
| nA (audit→null) | 11 | same 11 |
| nG (reint→lowest-hid) | 0 | — |
| ablate (no shared) | 6 | q01,q02,q04,q06,q21,q31 |
| poison | 38 | (see table; mostly NO_VERDICT) |
| min | 0 | identical to onebrain (machinery fans out on its own) |

## Kill-bar verdicts

- **K1″ (Accuracy benefit, conjunctive): PASS.** onebrain 23/44 > single
  20/44, and ablate 21/44 < onebrain 23/44. The +3 rides the shared channel:
  +12 (Cat A 6, Cat B q07+q10, Cat C α 4), −9 (Cat C β/γ 8 via honest V4
  hurt, q31 via duel). Ablate loses 6 deltas, net −2.
- **K2″ (Causal cross-talk): PASS.** Poison changes 38/44 problems (mostly
  to NO_VERDICT); cross-talk is massive, not zero.
- **K3″ (TNN's own decision): NOT VOIDED.** min (bare driver, no scaffold)
  fans out via the machinery's own ledger fork flag (fork=1 in verdicts) and
  matches onebrain 23/44 exactly.
- **K4″ (Per-stage causality): MIXED.** Fork (11 deltas), subpass (11),
  audit (11) all causal — their "conscious" claims survive. **Reintegration:
  KILLED on v6** — nG is behaviorally identical to onebrain on all 44 items
  (0 deltas). The reintegration genuinely deliberates (full trace; on the v5
  dev set it overruled both branches correctly on q19, and nG changed q19
  there), but on v6 its verdicts coincide with the lowest-hid null. Honest
  kill per the preregistered bar.
- **K5″ (Determinism): PASS.** All 9 modes byte-identical across 3 reruns.
- **K6″ (No RNG): PASS.** Zero rand/srand/random hits in source; all
  tie-breaks pinned (hid order).
