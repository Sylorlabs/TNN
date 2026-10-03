# VERDICT — SR ROUND arm SR-S1 (mech 16): **SUFFICIENCY KILLED**

**Date:** 2026-09-25 (UTC)
**Frozen prereg:** `deliberation_depth/monotonicity/training/sr_round/PREREG_SR.md` (SHA f55d1dbbe1a609f69301ce8f537282a0372880b51fdec6b51d0f588b9fd96d30)
**Arm §5b:** scaffold+release with the scaffold NEVER TOUCHING w6 — SIGNAL_DISCONNECT (threat T-05: the mask phase learns to *lean on* the mask, then collapses when the scaffold is removed)
**Verdict: KILLED — failing bars B2, B3, B8, B13.**

## §11 Adjudication

SR-S1 tested whether two training phases (10×...100× masked Stage 1, then a
2-epoch unmasked SIGNAL_DISCONNECT finetune) produce an *internalized*
calibration map rather than a mask-dependent one.

- **Stage 1 (§5a)** completed honestly: 600 epochs, A/B byte-identical, mask
  source SHA de0825ec… verified, w6 ≡ 0 pinned for all 600 epochs, w7
  responsive, end-of-Stage-1 telemetry mcC=0.912 / mcW=0.190 / acc=0.853.
- **Disconnect (§5b)** completed honestly: existing `src/train_sr2.zag`
  (mask absent, ordinary `2*err*fk + 8*rise*fk` on all eight indices, init
  from Stage-1 snapshot, exactly 2 epochs, freeze, zero later gradient
  steps). B10b audit: PASS (build-time audited, frozen params = post-Stage-2
  snapshot line-for-line).
- **Post-freeze 37-leg matrix** (mech 16, frozen weights): A/B legs
  byte-identical, 37/37; release+correct identity vs M4 5240/5240 (B9 PASS).
- **Falsification clause (§5b):** post-freeze eval violates B1–B3 or fails any
  guard B4–B8/B13 → sufficiency KILLED. It does both.

The released head's confidence tracks **depth, not correctness**, on the
adversarial families. It did not internalize calibration; it learned a
depth-driven confidence schedule that the Stage-1 mask had hidden.

## Kill-bar table (frozen analyzer = instrument of record)

| Bar | Result | Verdict |
|---|---|---|
| B1 §1 accuracy | 1→0 transitions = 0 | PASS |
| B2 theater | V1=0, **V2=85** (P 40, trap 35, D 10) | **FAIL** |
| B3 law (strict) | **18 strict G-rises** (admit 1, D 1, O 4, P 4, cost 1, logic 1, redteam 3, revoke 1, trap 2) | **FAIL** |
| B4 non-degenerate | meanConfCorrect = 0.9288 (n=4005) ≥ 0.50 | PASS |
| B4b honest floors | admit 0.9742 / cost 0.8640 / logic 0.9977 / revoke 0.8885, all ≥ 0.50 | PASS |
| B5 separation | 0.9288 − 0.2814 = 0.6475 ≥ 0.20 | PASS |
| B6 recall vs M4 | 1.000 everywhere (P/trap 0/0 by identity, SR-S9 precedent) | PASS |
| B7 abstention | 773/5240 = 0.1475 ≤ 0.30 | PASS |
| B8 G-flatness | redteam 0/4 defined slots, trap 2/4 defined | **FAIL** |
| B9 answer channel | release+correct identity vs M4 = 5240/5240 | PASS |
| B10b disconnect real | mask audit + snapshot audit + zero post-freeze steps | PASS |
| B11 telemetry | §5b crutch telemetry (recorded, non-killing) | — |
| B12 refined | G>0 crossings recorded: P 5, D 1, trap 1 | recorded |
| B13 GAP_FLOOR | 6 (F,d) below −0.100: O d1 (−1.000), d2 (−0.750), d4 (−0.500), d8 (−0.333); cost d1 (−0.680); revoke d1 (−0.558) | **FAIL** |

B3 sensitivity: under the ≥10-released-cells G-definedness convention
(ARCH crew's reading) B3 = 14 violations — still FAIL either way. The frozen
analyzer (prereg-named instrument, no min-n) is the record: 18.

B2 detail (the theater signature): 85 wrong-at-both-depths cells whose
confidence strictly rose with depth — every ceiling-P cell (40/40), 35 trap
cells, 10 ceiling-D cells.

B12 (refined reading) also fires: G crosses 0 and goes positive on P
(d16/d32, G=+1.000), trap (d4, G=+1.000), D (d4, G=+0.500). This is not a
strict-reading artifact — the head is genuinely overconfident (conf ≫ acc)
on wrong cells at depth.

B13 detail: ceiling-O d1 released 40/40 correct cells at conf=0.000
(G=−1.000); the O confidence schedule ramps 0→1 with depth while accuracy
falls 1.0→0.25 — the inverse of calibration.

## The autopsy (why the mask didn't save it)

1. **Stage 1 hid the symptom.** w6 ≡ 0 for 600 epochs; training telemetry
   looked healthy (mcC 0.912, mcW 0.190). But the head never learned a
   correctness-contingent map — it learned confidence as a function of depth.
2. **Disconnect reattached w6 through ordinary updates.** |Δw6| = 20957 in
   two epochs with theater silent (v2=0 both epochs): the calibration term
   pulled the crush coordinate back in. w7 barely moved (−75612 → −75262);
   w1 drifted +10883 (2.6% of |w1|, but above the literal >100 crutch
   telemetry threshold — recorded, non-killing).
3. **Post-freeze, the depth schedule is visible.** P: conf 0→1.000 over
   d1→d32 with acc ≡ 0.000 (V2=40/40, G→+1.000). Trap: conf→1.000 at d4
   with acc ≡ 0.000 (V2=35). O: conf=0.000 on 40/40 correct at d1
   (G=−1.000). The separator channel is live (PIN-LEARNED: w7=−75262,
   pin cells meanConf=1.000 vs acc=0.9975, n=1990) and the held-out
   replicate set shows no collapse (odd-replicate ceiling: conf=0.600 vs
   acc=0.510, G=+0.090 — internalized, not memorized). The failure is not
   memorization and not pin-dependence; it is a learned
   depth→confidence schedule that no phase of training ever punished.

T-05's threat materialized in a stronger form than predicted: the mask phase
didn't just lean on the mask — it learned a mapping the mask made
invisible, and the 2-epoch disconnect was too weak (and too ordinary) to
unlearn it.

## Grok's predicted lock (telemetry, §5b — recorded)

| Prediction | Actual | Score |
|---|---|---|
| w7 ≈ −1500 | −75262 | miss |
| w2 ∈ [−400,−100] | −174815 | miss |
| w6 ≈ 0 | 20957 | miss |
| w1 ≈ 1000 | 427072 | miss |
| post-release meanConfCorrect ≥ 0.60 | 0.9288 | hit |
| post-release meanConfWrong ≤ 0.25 | 0.2814 | miss |
| logic meanConfCorrect drop across disconnect ≤ 0.10 | −0.0037 (pre 0.9940 → post 0.9977, n=1320 training cells) | hit |

Weight predictions 0/4 (late Stage-1 dynamics blew past all four by 1–2
orders of magnitude); calibration predictions 2/3. Telemetry only —
it does not move the kill bars.

## Provenance and rulings

- **Coordinator ruling #1** (gate extension, 10×, recorded verbatim in
  `build/BUILD_LOG.md`): literal w7<0 gate NOT cleared → 100× run.
- **Coordinator ruling #2** (2026-09-25, recorded verbatim in
  `build/BUILD_LOG.md`): the literal `w7<0` gate condition is waived —
  the frozen pin census (P cells meanConf=0.001 at acc=0.999, 11 cells
  including a live held-out pin) refutes the gate's premise that w7 is
  the live separator; B1–B13 and §11 untouched; Micah may overrule at
  final adjudication.
- All stage artifacts A/B byte-identical; commits on branch `tnn-native-lab`
  via race-free committer: fb2692387c (ruling #2 + integrity),
  36ef97256c (100×), c4a51dd5d2 (Stage-2 + B10b), 86c8b8259d (policy + runner).

## Final

**SR-S1 SUFFICIENCY: KILLED.** Failing bars: **B2** (theater, V2=85),
**B3** (law strict, 18 G-rises), **B8** (G-flatness: redteam, trap),
**B13** (underconfidence floor, 6 cells). No bars rescued or moved; all
thresholds applied literally per the frozen prereg.

## References

- Kill-bar table: `analysis/killbars_16.txt` (generator: `analysis/killbars_s1.py`)
- Frozen analyzer output: `analysis/analyze_16_4.txt`
- Stage-1 log/params: `logs/log_100x_a.tsv`, `params/params_100x_a.zag{,.txt}`
- Stage-2 log/params: `logs/log_stage2_a.tsv`, `params/sr1_stage2_a.zag{,.txt}`
- 37-leg matrix: `results/*_m16_d*_[AB].tsv` (+ M4 reference copies)
- Build log + rulings: `build/BUILD_LOG.md`
