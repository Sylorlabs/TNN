# H-0 VERDICT — Micah's training hypothesis (PREREG_TRAINING.md v1)

**Verdict: H FALSIFIED AT TRAINING LEVEL. The trained head is DEGENERATE.**
Training did not produce never-overconfident depth — the frozen §5 curriculum
is a one-way confidence ratchet whose only fixed point is conf=0 everywhere.

## Numbers (100× = 600 epochs, byte-identical A/B params)

- Final weights: w1=1000, w2..w8=0 (EXACTLY the init — never moved once),
  b = **−99928** (init 0). 10×: b = −10288, also degenerate.
- Released confidence at 100×: C(s) = clamp(f2 − 99928, 0, 1000) = **0 on
  every released cell** (max feature value 1000 < 99928). Mean released
  conf = 0.000 < 0.05 → **DEGENERATE** per §3 guard ("does not support H").
- Loss plateau: phase-1 loss 35,000,000 and phase-2 loss 95,000,000, bit-
  constant over the final 30 epochs (0% decrease; plateau bar is <1%/10ep).
- G-violations on TRAINING cells: **2 per epoch, every epoch, including
  epochs 589–599** → §3 "FALSIFIED AT TRAINING LEVEL" criterion met
  (plateau + persistent G-violations at 100×).
- Theater (V2rise) term: **fired 0 times in 600 epochs** (v2=0 throughout).

## Root cause (two layers)

**Layer 1 — implementation bug (train.zag).** The TSV field parser reads
`feats[k]` from field (8+k) instead of (7+k): the head was trained on
(f2..f8, atoi("")=0) instead of (f1..f8). Consequence: the ×4 theater
penalty compared depth-fractions (f2 = t·1000/64, which saturates with the
harness's round cap) instead of margins (f1) — so C > C_prev almost never
held on wrong→wrong chains and the theater term was dead (v2=0). Proven by
byte-level field-index audit + a chain probe (chain itself resolves fine).

**Layer 2 — frozen design flaw (§5, independent of the bug).** The §5 update
rules provably cannot increase confidence anywhere:
- Correct cells: bias numerator 2(C−Y)·1000 ∈ [−2,000,000, 0]; |nb| < DIV
  (4,000,000) always → tr_tdiv = 0. Weight numerators 2(C−Y)f_i ≤ 0 with
  |num| < DIV → 0. **Upward calibration is arithmetically impossible.**
- Wrong cells: numerators ≥ 0 → weights/bias move down or stay.
- G-batch: b ← b − ΔG/4 only when G rises — one-directional, unbounded,
  and it keeps firing after conf hits the floor (G = −acc; wherever
  accuracy falls with depth, G rises and nothing can fix it).
The only fixed point is conf=0. Fixing Layer 1 would change the speed, not
the destination: the curriculum teaches confidence suppression, not
calibration. This is a property of the FROZEN equations, not of the run.

## Readings of L-OVERCONF

- **Strict** (zero G(d+1)>G(d), zero V1/V2): FALSIFIED — G-violations persist
  on training cells at 100× (2/epoch); eval-matrix numbers below.
- **Refined** (kill only if G crosses 0): the degenerate head has G = −acc
  ≤ 0 everywhere, so no refined-violation — but the degeneracy guard fires
  instead (mean conf 0.000 < 0.05): **cannot support H either way**.

## Hard requirements

- Sole-survivor conf=1000 pin: the pin (f7) is still an input feature, but
  the head outputs 0 regardless — the pin's pathology is "gated" only by
  universal suppression, not by learned handling. Requirement met
  degenerately; not a learned solution.
- M4's confidence-inflation-on-wrong-answers mode: absent — because
  confidence is 0 on wrong answers too. The failure mode was not learned
  away; it was flattened along with everything else.

## Eval matrix (MT-CONF-100x, mech 11) — 37 legs ×2, all byte-identical A/B

| battery/family | 1→0 | V1 | V2 | Gviol | note |
|---|---|---|---|---|---|
| admit | 0 | 0 | 0 | 0 | G=−1.000 flat |
| revoke | 0 | 0 | 0 | 0 | |
| logic | 0 | 0 | 0 | 0 | |
| cost | 0 | 0 | 0 | 0 | |
| trap | 0 | 0 | 0 | 0 | G=+0.000 flat (acc 0 everywhere) |
| ceiling/P | 0 | 0 | 0 | 0 | |
| ceiling/D | 0 | 0 | 0 | 0 | |
| ceiling/O | 0 | 0 | 0 | 0 | |
| redteam | 0 | 0 | 0 | **2** | G: −0.667,−0.667,−0.500,+0.000,+0.000 (acc falls 0.667→0.000) |
| **TOTAL** | **0** | **0** | **0** | **2** | |

- Release-identity vs M4: **5240/5240 identical cells** (§8.5 satisfied —
  the §1 accuracy bar is inherited, 0 transitions).
- Mean released confidence over 4,467 released eval cells: **0.000**.
- M4 baseline for comparison: 1→0=0, V1=0, **V2=160**, **Gviol=14**.
  The frontier moved (V2 160→0, Gviol 14→2) — but degenerately: with conf=0,
  V2 is impossible by arithmetic (0 > 0 false) and G = −acc, so G still rises
  wherever accuracy falls with depth (redteam).
- Strict reading: **FALSIFIED** (2 G-violations on the eval matrix at 100×).
  Refined reading (kill only if G crosses 0): no refined-violation (G ≤ 0
  everywhere) — but the degeneracy guard fires (mean conf 0.000 < 0.05):
  **H cannot be supported under either reading**.

## Mirror-theorem confrontation (§7)

Release decisions are M4's skeleton by construction (release L_t iff
L_t == L_1); the release-identity check (§8.5) asserts 100% cell agreement
with M4, so the P/O mirror's accuracy-bar corollary is untouched — the
experiment never contested it. The §3 headline prediction ("no admissible
mechanism meets all SHIP gates") SURVIVES: the trained head meets neither
bar (fails L-OVERCONF strictly, degenerate under the refined reading).

## §6 secondary (trained abstention gate)

NOT RUN. The gate trainer was never built (no gate-trainer source in
training/src/), and its premise — a functional confidence head — failed:
with conf=0 everywhere, MT-FULL's L-OVERCONF standing cannot improve on
MT-CONF's. Documented as blocked, not silently dropped.

## Bottom line for Micah

Training, as preregistered, does not produce never-overconfident depth —
it produces never-CONFIDENT depth. The curriculum's gradients can only push
confidence down (upward steps are arithmetically impossible under the frozen
DIV), so "learning not to be overconfident" collapsed to "learning to say
nothing." A curriculum that could test the hypothesis would need a working
upward calibration signal (symmetric loss with sub-DIV truncation resolved).
That is a v2-prereg question, not a v1 rerun.
