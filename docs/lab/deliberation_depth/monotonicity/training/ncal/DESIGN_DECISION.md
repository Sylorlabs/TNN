# Native Calibration: Design Decision (2026-09-25)

## Finding
A systematic exploration of the design space found:

1. **Stateless (no GT, no history, pure function of current features)**:
   - Best attempt: conf = (f1 + 0.5*f5 - 0.5*f4 - 500*f3 + 500*f7 - 0.3*f8)/1000
   - Result: b3=10, b13=3, v2=260 (without ceiling); b3=3, b13=19 (with ceiling)
   - VERDICT: FAILS. Hand-designed stateless functions cannot achieve calibration.
     The empirical mapping (margin 500 → 100% correct for honest, 50% for ceiling)
     is not derivable from first principles.

2. **Online empirical ledger + per-item ceiling (uses GT of past judgments)**:
   - Config: K=2, p0=0.95, mbw=150, cbw=250, full per-item ceiling
   - Result: b3=0, b13=0, b4=0.973, b5=0.668, v1=0, v2=0
   - VERDICT: PASSES ALL BARS.

3. **V2=0 requires per-item confidence continuity**:
   - Without the ceiling (min over previous conf), v2=260.
   - The ceiling uses the machine's OWN past confidence (not GT correctness).
   - This is deliberation continuity, not test-order dependence.

## Interpretation
"Native calibration" is interpreted as:
- NO separate training phase (no scaffold-and-release procedure).
- NO frozen trained head (params not learned via gradient descent).
- YES to online empirical tracking (the machine learns from its experience).
- YES to deliberation continuity (the machine remembers its confidence along a path).
- Params (K, p0, bin widths) selected via pre-prereg exploratory grid search
  (design phase, explicitly documented, not presented as confirmatory).

## Acknowledged limitations
- The ledger uses ground-truth correctness of PAST judgments to update.
  This is online learning, not pure native calibration.
- The bin widths and prior were tuned via grid search (not derived from principle).
- A truly "born calibrated" machine (zero GT, zero tuning) was not achieved.
- This result SUGGESTS that native calibration may require either
  (a) online GT feedback, or (b) arbitrary priors — a finding for Micah.

## Architecture: NEC (Native Epistemic Calibration)
1. Reference class: (margin_bin, consumed_bin), 7x5=35 classes. No depth, no family.
2. Ledger: Laplace (c + 2*0.95)/(t + 2), online, GT-updated.
3. Ceiling: conf(d) = min(ledger_conf(d), conf(d_prev)). Nonincreasing along path.
4. M4 skeleton: release/correctness frozen (B9).
