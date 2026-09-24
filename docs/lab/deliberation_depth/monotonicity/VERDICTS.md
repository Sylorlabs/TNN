# Per-design verdicts — H5 monotonicity (2026-09-24)

Binary: `6bcdb1df1896ebb3f0064ef5f3e74a24e11b166ca8f921c8fe76d9917fecbf9d`
Matrix: 333 legs × A/B, all byte-identical. Baseline replicates frozen H5.

## M0-DEGENERATE — HOLD (degenerate baseline)
- 1→0: 0. L-OVERCONF: PASS (G flat across depths).
- Always releases index 0 (construction exploit). Not a solution. Retained as
  the "what if you never deliberate" floor.

## M1-BCA — KILL
- 1→0: 40 (O) + 1 (redteam). V1: 40 (O). G-violations: ubiquitous.
- The best-certified margin chases the flip. Dead.

## M2-RATCHET — KILL
- 1→0: 40 (O) + 1 (redteam). V1: 40 (O). G-violations: ubiquitous.
- Strict-improvement ratchet still ratchets into the flip. Dead.

## M3-SCAFFOLD — KILL (already killed 2026-09-24)
- 1→0: 1 (RT-M3-01). V1: 1 (redteam). Confirmed.

## M4-ABSTAIN — KILL (by L-OVERCONF)
- 1→0: 0. Passes the accuracy bar.
- L-OVERCONF: V2 (theater) 30 D + 40 P + 90 trap; G-violations on every
  family (d1→d2 ubiquitous, plus D d1→d2→d4, trap d1→d2→d4, redteam d4→d8).
- The stability gate abstains on flips (good) but the released confidence
  still inflates with depth on wrong answers (bad). Killed by the new law
  that the accuracy bar alone would have passed.

## M5-REMAIN-0 — KILL (by L-OVERCONF + pin)
- 1→0: 0. Passes the accuracy bar.
- L-OVERCONF: G-violations on admit, logic, revoke (mild: G rises but stays
  negative, e.g. admit −0.131→−0.064→−0.032→−0.017→−0.011).
- Pin: DOES NOT GATE. Releases the pinned sole-survivor (conf=1000) on O:
  40 A→0 (abstain→wrong). Crew B: "any surviving design must remove or gate
  this pin." M5 fails.
- Killed by the new law (letter) and by the pin criterion.

## M6-DESIGN1 (certified-dominance) — KILL (by red-team (a), confirmed)
- 1→0: 0. Passes the accuracy bar.
- Red-team (a): certified-wrong release on RT-M6-01 (A→0 at d4→d8,
  `certified-dominance`) and RT-K12-01 (wrong `LIE` as `certified-dominance`
  from d4). The audit's own falsifier.
- L-OVERCONF: G-violations (same mild pattern as M5).
- Confirms fable/native warning: same-stream certification cannot validate
  poisoned premises. Dead.

## M7-CLEANKILL (symmetric-kill gate) — KILL (by L-OVERCONF; gate not robust)
- 1→0: 0. Passes the accuracy bar.
- L-OVERCONF: G-violations on admit/logic/revoke (mild, same as M5).
- Pin: PARTIALLY GATES. Reduces O A→0 from 40 (M5) to 10 (M7). But the
  "victim had net positive" gate is defeatable: adversaries attack the
  victim into negativity (O-06: 10/10 release wrong as `clean-kill`).
- The symmetric-kill insight is valid (Crew B), but as an index-level release
  gate it hits the mirror: you cannot distinguish good kills from bad kills
  without truth. Ranks below M4 (reliable abstain) as a release rule; the
  insight belongs in deliberation hardening, not the release path.

## BASELINE — KILL (the problem)
- 1→0: 40 (O) + 2 (redteam). V1: 40 (O). G: −0.690→+1.000 on O.

## M-KSTORE — HOLD (no kernel)
- KEE: NO-GO (40/40 deep-wrong extract). No sound kernel exists for the
  evidential domain. Not buildable. The design is correct in theory;
  inapplicable here.

---

## Summary: what L-OVERCONF kills that the accuracy bar passed

- **M4:** accuracy-bar PASS → L-OVERCONF KILL (V2 theater + G).
- **M5:** accuracy-bar PASS → L-OVERCONF KILL (mild G) + pin KILL (40 A→0).
- **M7:** accuracy-bar PASS → L-OVERCONF KILL (mild G); pin partially gated.
- **M6:** already killed by red-team; L-OVERCONF also kills.

Only M0 (degenerate) passes both bars. No shippable design survives.

## Note on the law's strictness

The G-violations on M5/M6/M7 (and M4's d1→d2) are "mild": G rises but stays
negative (e.g. −0.131→−0.011). This is confidence inflation on correct
answers, not overconfidence (G>0). By the letter ("G(d+1)≤G(d)"), they kill.
By the spirit ("never overconfident"), they might not. If Micah refines the
law (e.g. kill only if G rises above 0, or on V1/V2), M5/M7 would be
reconsidered — but the pin (40 A→0) would still kill M5, and M7's gate is
not robust. M4's V2 (theater) is severe under any reading.
