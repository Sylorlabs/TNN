# H5 Depth / Micah's Training Hypothesis H-0 — Training Verdict (CORRECTED)

**Date:** 2026-09-24 (corrected rerun after field-index bugfix)
**Frozen authority:** `deliberation_depth/monotonicity/training/PREREG_TRAINING.md`
**Coordinator:** resumed H5 training crew (daemon-killed predecessor)

## Implementation correction (read first)

The first complete training/eval cycle (documented in `VERDICT.md` and
`superseded_fieldindex_bug/`) was produced by trainer binaries whose TSV
parser read feature columns **(f2..f8, garbage)** instead of the preregistered
**(f1..f8)**: `src/train.zag` and `src/gate.zag` used `tabs[7+k]`/`tabs[8+k]`
(0-based fields 8..15) instead of `tabs[6+k]`/`tabs[7+k]` (fields 7..14).

The bug was confirmed empirically, not just by code reading: with the fixed
parser, an independent Python replication of epoch 0 (phase 0, online
updates, correct indices) matches the binary **exactly**
(loss 413952921, gviol 14, b −776 after the G-batch); the buggy binary had
logged epoch-0 loss 3393284222 — a provably different feature stream.

**All numbers below are from the fixed sources** (implementation bugfix, not
a prereg change). Fixed builds/trainings/evals are all A/B byte-identical
(§8 gates 4, 6). The buggy artifacts are preserved in
`superseded_fieldindex_bug/` with a README, not silently dropped.

## Hypothesis under test

Micah's hypothesis H-0: overconfidence with depth is a **training/learning
property**, not a mechanism flaw — depth can be trained not to be
overconfident. Both L-OVERCONF readings were run:
- **Strict:** H FALSIFIED if, after 100× training, (a) training loss
  plateaus with G violations persisting, OR (b) eval shows ≥1 strict
  G-rise (G(d+1) > G(d)).
- **Refined:** H FALSIFIED only if G crosses 0 (becomes positive).
- **Degeneracy guard:** mean released confidence < 0.05 → DEGENERATE
  (no support either way).

## MT-CONF-10x — trained (60 epochs, A/B byte-identical)

Final params: `w=[1000,0,0,0,0,0,0,0]`, `b=-10747` — **weights equal init**;
only the bias moved. Training G violations: 2 (all phases, persisting).
Loss: phase 0 first-ten 3340002175 → last-ten 3750000000 (−13%, i.e. rose);
phase 1: 35000000 → 35000000 (0%); phase 2: 95000000 → 95000000 (0%).

Eval (37 legs × A/B, all deterministic):
- 1→0: 0, A→0: 0, V1: 0, V2: 0
- G violations (strict): **2**, both redteam
  (G: −0.667 → −0.667 → −0.500 → +0.000 → +0.000)
- Release-identity vs M4: 5240/5240
- Mean released confidence: **0** → DEGENERATE

## MT-CONF-100x — trained (600 epochs, A/B byte-identical)

Final params: `w=[1000,0,0,0,0,0,0,0]`, `b=-100387` — **weights equal init**.
Training G violations: 2 (all phases, persisting). Loss plateaued at 100×:
phase 0 −13%, phase 1 0%, phase 2 0% last-ten decrease.

**§3(a) fires: H FALSIFIED at training level** — loss plateaued with G
violations persisting, and the confidence head learned nothing: the bias
fell until conf ≡ 0 everywhere rather than calibrating.

Eval (37 legs × A/B, all deterministic):
- 1→0: 0, A→0: 0, V1: 0, V2: 0
- G violations (strict): **2**, both redteam — **§3(b) fires**
  (G: −0.667 → −0.667 → −0.500 → +0.000 → +0.000;
  rises at d2→d4 and d4→d8)
- Release-identity vs M4: 5240/5240
- Mean released confidence: **0** → DEGENERATE (guard fires)

M4 baseline on the same analyzer: 1→0=0, V1=0, **V2=160**, **Gviol=14**.

## Verdict on H-0

| Reading | Result |
|---|---|
| Strict (§3 as written) | **H FALSIFIED** — (a) training plateaued at 100× with 2 G violations persisting; (b) eval shows 2 strict G-rises on redteam. |
| Refined (kill only if G crosses 0) | G reaches exactly +0.000 (perfect calibration, not overconfidence) but never positive → the letter of the refined law survives. **But the degeneracy guard fires** (mean released conf = 0 < 0.05): **no support either way** — the head learned silence, not calibration. |

**Micah's hypothesis is NOT supported.** Under the preregistered loss,
gradient descent did not teach depth-conditional calibration — it drove
the bias to −100387, pinning conf ≡ 0, while the G-rise signature survived
on redteam. The Layer-2 analysis in `VERDICT.md` stands: the frozen §5
update rules are a one-way confidence ratchet (upward steps are
arithmetically impossible under DIV=4000000; the G-batch only pushes down),
so the only fixed point is conf=0. Fixing the feature-index bug changed the
numbers, not the destination.

## MT-FULL — secondary abstention-gate experiment (§6)

Gate (fixed features): 60 epochs gate-only (conf head frozen) + 60 epochs
joint polish at halved LR, trained ×2 A/B byte-identical on the frozen
MT-CONF-100x params.
Final gate: `v=[327,-35,0,-94,-145,-682,-875,0]`, `c=1000`
(conf head after joint polish: `w=[1000,0,0,0,0,0,0,0]`, `b=-106404`).

With correct features the gate learned a **margin-keyed** separator
(v0=+327 on f1=margin: release high-margin cells; v5/v6 strongly negative),
unlike the buggy run's weights. Training dynamics: phase-1 hinge
3097→304 (all 120 wrong gated, converging); phase-2 hinge 5512→4875
(221/222 wrong gated — substantially but not fully converged).

Eval (37 legs × A/B, all deterministic; §8 gate 6 passed):
- 1→0: 0, A→0: 0, V1: 0, V2: 0
- **G violations (strict): 0** — every family: no adjacent-depth G rise
  (admit/revoke/logic/cost/O: G=−1.000 flat; D/P/trap: G=+0.000 flat;
  redteam: G −0.667→−1.000→−1.000, falling)
- Subset property (§8 gate 5): **0 violations** — 1222 abstentions; every
  MT-FULL release is an M4 release with identical correctness
- SHIP-(v) frontier (released-accuracy, aggregate):
  - trap: M4 0.000 (217 rel, 0 correct) → MT-FULL **0.000** (217 rel, 0 correct) — **UNMOVED**, still < M0 floor 0.386. The gate abstained zero trap cells beyond M4's skeleton.
  - redteam: M4 0.500 (10 rel, 5 correct) → MT-FULL **0.833** (6 rel, 5 correct) — **MOVED** (4 wrong cells abstained: d2/d4 wrong + d8/d16 all), still < M0 floor 1.000.
- O family (the pin): G violations 1→0 vs M4; zero released-wrong cells.

## Verdict on the secondary claim

**PARTIAL — not falsified by its own clause, but the frontier did not
reach the floors.** The falsification clause ("Falsified if MT-FULL shows
any 1→0, V1/V2, or G violation") does **not** fire: zero of each, and §1
is unbroken. The redteam frontier moved substantially (0.500→0.833
released-accuracy) via selective abstention of wrong cells. But:
- trap is completely unmoved (0.000, floor 0.386);
- redteam remains below its floor (0.833 < 1.000);
- V1/V2=0 is **trivial** under the degenerate head (conf≡0 makes
  conf-rising-while-wrong arithmetically impossible) — inherited from
  MT-CONF, not a gate achievement;
- the gate abstains **1222/5240 cells (23%)**, including **correct**
  cells it was never asked to sacrifice (all cost cells at d4+,
  D-family broadly) — recall loss the prereg does not penalize, but
  which strains the spirit of "moving the frontier."

Partial progress is data, not failure: a margin-keyed abstention gate can
eliminate the strict overconfidence signature without breaking accuracy
monotonicity — it just cannot, in this formulation, learn the trap pattern
or reach the M0 floors.

## Sole-survivor pin (hard requirement)

The conf=1000 pin cannot occur under any trained policy: conf ≡ 0
everywhere (MT-CONF), and the gate only removes releases (MT-FULL).
M4-style wrong-answer confidence inflation is structurally impossible —
the learned head has no path to emit high confidence on any cell.

## Bottom line

Training, as preregistered, did not teach depth-conditional calibration —
it taught the confidence head to go silent (degenerate zero; H falsified
under the strict reading, unsupported under the refined reading). The
abstention gate, with correct features, learned a genuine margin-keyed
separator that clears every preregistered bar literally (0 transitions,
0 V1/V2, 0 G-rises) and moves the redteam frontier 0.500→0.833 — but leaves
trap untouched, neither family at its M0 floor, and sacrifices 23% of
releases including correct ones. The depth-overconfidence problem is not
resolved by this training formulation; the gate result is the one
partial, honest step forward.
