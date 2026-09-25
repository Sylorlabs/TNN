# SR-S1 gate-extension — RESULT: GATE NOT CLEARED, STOP per coordinator ruling

Extension run: passes=11 (66 epochs, epochs 0–65), A/B byte-identical, from
frozen init via the deterministic-forward method (build log 2026-09-24).
- Epochs 0–59 byte-identical to committed log_10x_a.tsv (determinism proven);
  epoch-59 row = committed params_10x_a.txt. Extension epochs are exactly
  what a resume-from-epoch-60-snapshot would produce.
- Logs open with prereg SHA f55d1dbbe1a609f69301ce8f537282a0372880b51fdec6b51d0f588b9fd96d30.

## Gate reading (ruling window: epochs 60–64)

| epoch | phase | w7 | b | mcC |
|---|---|---|---|---|
| 60 | A ep0 | **1833** | −18111 | 0.974 |
| 61 | A ep1 | **1833** | −17784 | 0.977 |
| 62 | B ep0 | **1833** | −26644 | 0.882 |
| 63 | B ep1 | **3083** | −31275 | 0.829 |
| 64 | C ep0 | **1833** | −29047 | 0.872 |
| 65 | C ep1 | 583 | −27401 | 0.884 |

w7 ≥ 0 at every epoch in the window (min 1833; window min incl. ep65 is 583).
**The literal §5b go/no-go (w7<0) is NOT satisfied. Per the coordinator
ruling: STOP, report back — the dynamics differ from the diagnosis.**
No 100× run launched. No Stage-2 run launched. train_sr2.zag is written and
§5b-verified (build log) but HELD — not built, not run.

## The dynamics differ from the diagnosis — characterization

The 10× diagnosis (and the ruling's premise) read epochs 57→59
(3035→1785→535) as clean −1250/epoch steps of the 5-wrong-pin pull and
predicted w7<0 at epoch 60 (≈−715; build log recorded this prediction —
it was wrong: actual +1833). The full 66-epoch series shows those steps
are **phase-local, not secular**:

- w7's feature IS the pin indicator (k3==6 ↔ w7 ↔ f7; feats slot 6), so w7
  moves ONLY on pin cells, with the ×10 boost (num=10·err·f7).
- Pin cells (f7=1000, released, train; counted from frozen features.tsv):
  **Phase A: 1950 correct / 0 wrong; Phase B: 35 correct / 0 wrong;
  Phase C: 0 correct / 5 wrong.**
- Within each pass: Phase A ep0 pushes w7 UP (+1298 at the pass 9→10
  boundary: 535→1833), Phase B ep1 pushes UP (+1250), Phase C ep0/ep1 pull
  DOWN (−1250 each — the "diagnosed" steps). Net per pass ≈ +48.
- Pass-end w7 (Phase C ep1): −629, −830, −608, −312, **+314, +371, +262,
  +348, +451, +535, +583** (epochs 5–65). w7 crossed zero UPWARD at pass 4
  and has risen monotonically for 7 consecutive passes. The 10× cutoff
  (epoch 59) caught the oscillation TROUGH, not a transient crossing.

Mechanism (why the drift is positive, not negative): the G-batch ratchet
drags b down secularly (−965 → −27401). Deeply negative b makes the 1985
correct pins underconfident (mcC=0.884, NOT saturating at C=1000 — the
diagnosis's saturation premise is refuted), so their ×10-boosted upward
push on w7 GROWS as |b| grows, while the 5-wrong-pin downward pull is
constant. There is no mechanism for trend reversal: continued Stage-1
training drives w7's pass-end mean further positive, not negative.

## Bar-premise vs mechanism verdict (unchanged, strengthened)

- The bar's INTENT (separator channel live and responsive) is satisfied:
  w7 moves ±1300 within a pass and ranged −830 → +3083 across training;
  w5=+36811 theater-detached; w6≡0; theater fired; mcC=0.884.
- The bar's LITERAL directional premise (w7<0) encoded grok's ~30-wrong-pin
  estimate; the frozen data has 5 wrong pins (all Phase C) vs 1985 correct
  pins (Phases A/B) pushing the other way. The miss is STRUCTURAL under the
  frozen Stage-1 dynamics, not a transient — extending Stage 1 cannot clear
  it. This is a bar-premise failure, not a mechanism failure.

## Coordinator decision needed

Options:
  (a) Waive/clarify the literal w7<0 bar (premise refuted by frozen data;
      intent satisfied) and green-light 100× + Stage 2 — needs a prereg
      note, not a silent waiver.
  (b) Kill SR-S1 at the gate on the literal bar.
  (c) Amend the Stage-1 design (e.g. rebalance the pin-phase structure) —
      NOT recommended without a prereg amendment; changes the tested
      hypothesis.
The crew makes no move until the ruling lands. Kill bars B1–B13 and §11
are untouched by this gate outcome (no post-freeze eval exists to
adjudicate them).

## Artifacts (this commit)

- logs/log_11x_a.tsv (66 epochs; B byte-identical, not committed)
- params/params_11x_a.zag + .txt (epoch-65 snapshot; B byte-identical)
- src/train_sr2.zag (Stage-2 driver, §5b-verified, HELD — unbuilt/unrun)
- build/BUILD_LOG.md (extension run record)
