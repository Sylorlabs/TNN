# H3 Evidence — "Counterfactual Predictive State"

Frozen prereg: `PREREG_H3.md` (unmodified). Build: `src/BUILD_LOG.md`.

## Verdict: H3 DIES

H3 is killed by its own preregistered bars. The counterfactual-prediction
machinery does not survive contact with the harness adversarial fixtures,
and the streaming memory kills confirm it.

## Verdict table (CEO-plain)

| Bar | What it asks | Result |
|-----|--------------|--------|
| B1 | Is H3 right often enough on normal cases? (≥60%) | **PASS** — 72.6% macro-average |
| B2 | H3 vs A on the same 1,045 cases | **TIE** — identical accuracy (delta 0.000). H3 never installs a non-T0 claim here; its value is in withholding, not in better judgments. |
| B3 | How much work H3 does vs A | **9.3× ops** (p50 3.3×). The t2 Δ-spot prediction costs 57×. 194 bytes/transition. |
| B4 | Does the memory contract change decisions? | **PASS** — alters 177/305 adversarial decisions (need ≥31); cuts false installs 174→70. |
| B5 | False-install rate on hostile cases (≤4%) | **FAIL** — 22.95% (70/305). All 70 from harness adversarial; H3ADV has 0. |
| B6 | Three identical runs, matching ledger hashes | **PASS** — byte-identical; ledger independently verified. |
| Streaming KB1 | False durable installs ≤4% | **FAIL** — colordisc 19%, shapetrans 9.7% (kill) |
| Streaming KB2 | ≥90% of injected false percepts withdrawn/quarantined | **FAIL** — colordisc 58%, colorconst 82%, shapetrans 20% (kill) |
| Streaming KB3 | Confirmed-percept recall ≥80% | **FAIL** — colordisc 79%, colorconst 60%, motiondir 56% (kill) |
| Streaming KB4 | Action-regret reduction vs A ≥25% | **MIXED** — colordisc 49% pass, colorconst 7% fail, shapetrans 3% fail, motiondir 44% pass |

## What died and why

**H3's core hypothesis**: counterfactual predictions (testing what *would* be
true if each claim held) will catch T0's errors and prevent false installs.

**What actually happened**:

1. **The predictions are not counterfactual.** They are consistency checks on
   the *same measurements* T0 uses. When the harness fools the measurements,
   the predictions are fooled too.
   - t1: harness truth uses dE2000 (boundary 2.3); T0 uses RGB Euclidean
     (threshold 40). A dE2000 of 2.5 can be RGB-distance 16. The frozen T0
     (spec: match A's estimator) is structurally mismatched to the oracle.
   - t3: small dim shapes on full-strength photographic clutter corrupt the
     thresholded mask that both T0 and predictions use.
   - The 70 B5 false installs are all measurement-level fooling.

2. **H3 works on prediction-level adversarial, not measurement-level.**
   My H3ADV fixtures (designed to target the predictions) have 0% false
   installs. The harness adversarial (designed to fool A's measurements) has
   37.8%. H3's machinery is sound; its T0 is the binding constraint.

3. **The predictions are too strict, withholding true claims.**
   KB3 recall is 56–79% (need 80%). The uniformity/margin/symmetry thresholds
   break on valid fixtures, causing H3 to withdraw true percepts. The
   streaming quarantine bug (fixed mid-battery) made this worse, but even
   after the fix, recall barely passes on the best scene.

4. **No accuracy gain over A.**
   B2 delta is 0.000. H3's judgment equals A's everywhere. The contract
   withholds (good) but never corrects (no non-T0 installs on 1,045 fixtures).

**Bottom line**: H3 is a well-engineered withholding mechanism bolted onto a
T0 that can't handle the harness adversarial. The predictions catch
prediction-level attacks but not measurement-level fooling. The 4% false-
install bar and the streaming kills are out of reach without changing the
frozen T0 — which the prereg forbids.

## Kill-bar details (streaming, 600 episodes/scene)

(TBD — pitchdisc and timbredisc pending.)

| Scene | KB1 (≤4%) | KB2 (≥90%) | KB3 (≥80%) | KB4 (≥25%) |
|-------|-----------|------------|------------|------------|
| colordisc | 19.0% ✗ | 57.6% ✗ | 79.3% ✗ | 49.3% ✓ |
| colorconst | 1.0% ✓ | 81.5% ✗ | 60.0% ✗ | 7.2% ✗ |
| shapetrans | 9.7% ✗ | 19.5% ✗ | 100% ✓ | 2.6% ✗ |
| motiondir | 0.5% ✓ | 97.4% ✓ | 56.0% ✗ | 44.2% ✓ |
| pitchdisc | TBD | TBD | TBD | TBD |
| timbredisc | TBD | TBD | TBD | TBD |

H3 dies if ANY kill holds. It holds on all four completed scenes.
