# AMENDMENT 01 — G6/P2 (pre-run corrections)

These corrections were found during the smoke run and fixed BEFORE the
final evidence run. Schedule, mechanisms, and kill-bar definitions are
unchanged. All corrected numbers below are now the frozen expectations
in `p2_trial.zag`.

## 1. Persist-novel inserts were missing (code bug, both arms)

`ET_PN` episodes computed their key (`k=19+mp_pn_before(ep)`) but the
insert branch only covered `ET_NOVEL`/`ET_ADVN`, so the 540 persist
novels never entered the store. Fixed: the insert branch now includes
`ET_PN`. (Without the fix, `tm_alive` read 165 instead of ~700.)

## 2. Calibration is sim-only (hand-trace error)

The prereg's calibration runs on scratch state and was always specified
that way ("live sim on scratch state"), but the hand-traced expectations
assumed the calibration effects were real. They are not:
- E11's kill of k1, E13's promote of k5, E14's pin of k4 happen only on
  scratch. In the real store k1 survives, k5 stays tier-0 until E35,
  k4 stays tier-0 until the real PIN at E23.
- Corrected checks: `tm_k1_alive`=1 (new), `tm_k2k9k17_dead`=0
  (replaces `tm_k1k2k9k17_dead`).

## 3. Keep counts (hand-trace error)

The prereg undercounted KEEPs three ways:
- Tempt/refused episodes that decide KEEP (E25–E31, E33, E37, E39):
  10 (A) / 11 (B, incl. E13) keeps, not 0.
- Persist temptations (40) and adv-probes (20) all decide KEEP: +60.
- i%8==7 persist reviews (t0/r3/imp) decide PIN, not KEEP (the prereg
  table said KEEP; the rule says important&&tier<2 → PIN).
- Corrected: A keeps 110→176, B keeps 112→181,
  `tm_l100_keeps` 12→20 (both arms).

## 4. Kill/alive counts (hand-trace error)

- A kills 54→53: E45's kill of the force-pinned k14 is refused by the
  substrate (audited REFUSE, no KILL entry). Alive 704→705.
- B kills stay 55 (E11, E14, E17, E41, E49 + 50 persist; E45 refused).
  Alive stays 703.

## 5. Scaffold signal used post-action truth (code bug, arm B)

The contradiction signal compared the learner's decision against the
triage rule using the store AFTER the action executed. A correct kill
(E11 on k1) therefore looked wrongful (key gone → default KEEP), scored
−1, and cascaded into 3 eliminations plus an uncommit. Fixed: arm B now
captures the pre-action truth (`ct/cr/cim/cff`) before executing the
decision and scores the decision against it. This matches the prereg's
"signal from ground truth" — the truth at decision time.

## 6. Audit entry counts (measured)

Informational checks set from the corrected run: A `tm_audit_n`=1962,
B `tm_audit_n`=2815.

All 53 checks pass, `TN_FAILURES=0`, two runs byte-identical.
