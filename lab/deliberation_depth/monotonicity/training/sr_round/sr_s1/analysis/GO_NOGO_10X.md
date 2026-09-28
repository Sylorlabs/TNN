# SR-S1 10× go/no-go — RESULT: FAIL (1 of 5), STOP per §5b

Final 10× state (epoch 59 of 60, A/B byte-identical):
  w1=23955 w2=-6465 w3=0 w4=0 w5=32886 w6=0 w7=535 w8=331 b=-24438
  mcC=0.884 mcW=0.190 mcA=0.828 | theater fired 29/60 epochs

| Criterion (§5b) | Result |
|---|---|
| weights ≠ init | PASS (all live coords moved) |
| w7 < 0 (separator moved) | **FAIL — w7 = +535** |
| w6 = 0 held | PASS (exact 0, all 60 epochs) |
| theater fired >0 epochs on unmasked indices | PASS (29 epochs v2>0; w2/w8 moved) |
| meanConfCorrect ≥ 0.30 | PASS (0.884) |

## Diagnosis

The w7<0 bar encodes grok's premise from Q1 §(c): "w7: ~30 wrong pin
presentations × (−50) ≈ −1500". The frozen data does not match that premise:

- Pin cells (f7=1000, released, train): **1990 total — 1985 correct, 5 wrong**
  (counted from frozen features.tsv, SHA 4682190c…).
- With 99.7% of pins correct, the ×5-boosted w7 channel is dominated by
  correct pins: whenever G-batch drags b down (b: 0 → −24438 over 10×),
  correct pins go underconfident (C<Y) and w7 is pushed UP — the pin
  absorber doing its designed job. The 5 wrong pins pull down at most
  −250/cell/epoch and only while fully wrong.
- w7 trajectory oscillates with ±3000 amplitude and is drifting DOWN late
  (epochs 57→59: 3035 → 1785 → 535): correct pins are saturating at C=1000
  (their residual → 0, pull → 0) while the 5 wrong pins remain fully wrong
  (steady ≈ −1250/epoch pull). The 10× cutoff caught a transient — one more
  epoch would plausibly flip w7 negative.

The mask's load-bearing behaviors ALL verify — this is a bar-premise
mismatch, not a mechanism failure:
- w6 ≡ 0 exactly (crush coordinate never touched by any update)
- w3 ≡ w4 ≡ 0 (dead/unused as designed)
- w5 = +32886: separator channel strongly moved, theater-detached
- w2 = −6465, w8 = +331: theater kept, fired 29/60 epochs
- w1 = 23955 via non-pin cells only (pin firewall verified in source:
  num=0 iff f7==1000)
- meanConfCorrect 0.884, meanConfWrong 0.190 — genuine separation, not
  degenerate (weights large but within the ±2M clamp; v2's own 10× reached
  w6=19963, so this magnitude regime is normal for the curriculum)

Grok telemetry scorecard (recorded, not bars): w7≈−1500 (got +535),
w2∈[−400,−100] (got −6465), w6≈0 ✓, w1≈1000 (got 23955). grok's single-step
arithmetic underpredicted 60-epoch × 4222-cell compounding by ~10–60× on
every live coordinate.

## Decision needed (parent/coordinator)

The literal §5b go/no-go fails on w7<0. Options:
  (a) Proceed to 100× anyway: the miss is a transient of a mispredicted
      data premise; late dynamics point w7 negative; all mechanism checks
      pass. Requires waiving/clarifying the literal bar (prereg note).
  (b) Kill SR-S1 at the gate on the literal bar.
  (c) Re-run 10× with a longer gate (e.g. 12×) — NOT prereg-literal; needs
      amendment, not recommended.
No 100× run launched. State committed incrementally; resume-ready.
