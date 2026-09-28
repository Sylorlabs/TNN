# SR-S1 mask integers — PINNED (PREREG_SR.md §5b + §14 item 5)

Source of truth: `GROK_SR_DESIGN.md` Q1 (verbatim `grok_sr_Q1.txt`),
Scheme 1(a) "Pin firewall, theater reroute, separator boost".
Pinned BEFORE the first SR-S1 training run. Any change = prereg amendment.

Index convention: code index k (0-based) ↔ weight w_{k+1} ↔ feature f_{k+1}.
Pin flag f7 = feats slot 6.

Shared v2 update (DIV2 = 40000, tdiv = truncation toward zero):
  w_i ← w_i − tdiv(2(C−Y)f_i + 8·rise·f_i, 40000)
  b   ← b   − tdiv(2(C−Y)·1000 + 8·rise·1000, 40000)

## Stage 1 mask (mask ON) — exact integers

- k ∈ {4,6}  i.e. i ∈ {5,7} (evidence w5, pin w7):
    theater coefficient = 0 (no 8·rise·f_i term at all);
    calibration numerator × B with B = 5:
      num_i = 10(C−Y)f_i
    (verbatim grok: "calibration numerator multiplied by B=5: num_i=10(C−Y)f_i")
  Floor: |num_i| ≥ 40000 ⇒ |C−Y|·|f_i| ≥ 4000 (was 20000 unboosted).
  Check values (verbatim grok):
    f5=280 moves once |C−Y| ≥ 15  (40000/2800 = 14.29 → 15);
    full-error step tdiv(10·1000·280, 40000) = −70 (five times unboosted −14);
    f7=1000 moves once |C−Y| ≥ 4.
- k ∈ {1,7}  i.e. i ∈ {2,8} (w2, w8) and bias b:
    standard num, theater KEPT:
      num_i = 2(C−Y)f_i + 8·rise·f_i
      nb    = 2(C−Y)·1000 + 8·rise·1000
- k = 0      i.e. i = 1 (w1, margin channel):
    iff f7 == 1000 (pin cell): num_1 = 0  (pin firewall — pin error cannot
    touch the margin channel);
    else (non-pin cells): num_1 = 2(C−Y)f_1 + 8·rise·f_1  (ordinary v2).
- k ∈ {2,3,5}  i.e. i ∈ {3,4,6} (w3, w4, w6):
    num = 0 for the whole of Stage 1 (w3 dead, w4 unused, w6 crush coordinate
    held at 0).

Anti-saturation clamp unchanged: after each epoch w_i ∈ [−2000000, 2000000],
bindings counted. G-batch unchanged (v2 §5): after each epoch, per training
family F and adjacent depth pair, G in thousandths over M4-released training
cells (all phases): if G_F(d+1) > G_F(d): b ← b − tdiv(G_F(d+1) − G_F(d), 4).

Init (frozen): w1 = 1000, w2..w8 = 0, b = 0 (v2 §4, the killed M4-with-
harness-confidence configuration).

## Stage 2 (SIGNAL_DISCONNECT) — mask OFF

Hard cutoff at epoch boundary. Snapshot. Mask REMOVED: ordinary v2 update
rule on ALL indices (theater restored on every live coordinate, B = 1).
Unfreeze w1 (on pin cells), w4, w6. EXACTLY 2 ordinary v2 epochs, then FREEZE.
Zero gradient steps after freeze.

Epoch-unit reading (documented, literal): v2's frozen epoch unit is the
phase-pass (v2 prereg §5: "1× = 6 epochs (2 per phase in A→B→C order)"; the
train2 log increments `epoch` per phase-pass). "2 ordinary v2 epochs" =
2 phase-passes. After the 600-epoch (100-pass) Stage-1 boundary the ordinary
v2 cycle continues: Phase A ep0, Phase A ep1. G-batch stays on (all training
families); anti-saturation clamp stays on.

## Telemetry expectations (grok's predicted lock — NOT kill bars)

w7 ≈ −1500; w2 ∈ [−400,−100]; w6 = 0; w1 ≈ 1000; post-release
meanConfCorrect ≥ 0.60, meanConfWrong ≤ 0.25, logic meanConfCorrect drop
across disconnect ≤ 0.10. Adjudication uses B1–B9 + guards (§10) literally.
Crutch diagnostic (reported, not a kill bar): across the 2 Stage-2 epochs,
|Δw1| > 100 or w7 drifting toward 0 = mask was a crutch (report either way);
|Δw6| > 50 in those 2 epochs = theater reattachment reopened the crush.
