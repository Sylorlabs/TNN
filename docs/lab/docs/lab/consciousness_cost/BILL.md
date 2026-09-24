# THE CONSCIOUSNESS BILL — intelligence vs speed/compute, three arms

**Law:** TNN must be conscious about everything it does — but the law demands
the complete bill: what consciousness costs and what it buys, measured, not
asserted. **Date:** 2026-09-24. **Method:** three arms on every seam —
(1) conscious WITH proper training, (2) conscious WITHOUT training,
(3) non-conscious/autopilot. Frozen preregs in `preregs/` (PERCEPTION,
KBCONTROL, DELIBERATION, REFUSAL), all frozen before any run, never edited
after. Pure Zag mechanisms, zero RNG in decision paths, byte-identical reruns
≥3 (SHA256). Raw data + logs in `perception/`, `kbcontrol/`, `deliberation/`.

Prior two-arm context: `senses/conscious-perception/evidence/AUTOPILOT_BILL.md`
(C1–C16 component audit). This bill adds the missing third arm and converts
rounds to wall-clock + instrumented op counts.

---

## The bill table

### Seam 1 — Perception (14 fixtures × 3 reruns, 42/42 byte-identical)

| Arm | Accuracy | Wall | Compute (ops) | Memory | What it buys |
|---|---|---|---|---|---|
| F1 autopilot | 6/14 (42.9%) | S-legs: 0.765 eps/s overall (S1–S4 reproduce frozen values exactly) | task medians 8,193–5,583,041 ops/ep (frozen S4, reproduced) | no arm-distinguishable RSS (11–17 MB run noise) | nothing on trap classes |
| F2 deliberate, trained | **12/14 (85.7%)**, 6/6 catches | slower per episode (see marginal) | **1.2–8.3× marginal** ops vs own pass-1 (honest figure; cross-arm F1↔F2 confounded by different decoders — documented) | same as F1 | +42.8pp accuracy; all 6 trap catches |
| F3 deliberate, untrained | 11/14 (78.6%), 5/6 catches | ≈ F2 | ≈ F2 | same as F1 | structure alone catches 5/6; training decides the 6th |

The trained-vs-naive differentiator is `il_c2`: F2's diversity-triggered
absolute-decoder resample (1 round, 2.00× marginal) is correct; F3's fixed
[ROBUST, ABSOLUTE] order lets a 2-1 majority resurrect the wrong pass-1
(3.00× marginal, wrong verdict). Training buys *selection*, not the
resense machinery.

### Seam 2 — KB control (4880 episodes/arm, same curriculum + blind probe)

| Arm | Probe (320) | Wall | Compute | Memory | Integrity |
|---|---|---|---|---|---|
| A1 deliberate, trained | **320/0/0**, 0 spurious | **0.086 ms/ep** | 363 audited ops | 170 KB arena (160 KB = audit ledger) | 100% audit, replay-exact, 0 silent overwrites |
| A3 deliberate, untrained | 320/0/0 end-probe — but 32 spurious, **28 collateral true-kills**, mid-probe 148/112/60 | 0.080 ms/ep | 791 audited ops (2.2× churn) | 170 KB arena | 100% audit, replay-exact, 0 silent overwrites |
| A2 autopilot (silent) | 128/128/64, 64 spurious | 0.312 ms/ep (**3.6× SLOWER**) | full-tier scans every 10 eps | 5.9–23.5 KB | 0% audit, **188 unaudited overwrites** |

Structure vs judgment, separated: A1=A3 on 100% audit completeness,
replay-exactness, zero silent overwrites (6/6 runs) — the deliberate
*structure* is what kills the clobber class. Trained *judgment* adds zero
spurious installs, zero collateral kills, 2.2× less op churn, at equal
wall-clock. Note: phase D heals A3's end-probe; without it A3's end-probe
would look like its mid-probe.

### Seam 3 — Deliberation depth (877 items, rounds → wall-clock + ops)

| Arm | Accuracy | Wall/item | Ops/item | Rounds |
|---|---|---|---|---|
| autopilot (batch, all evidence at once) | **1.000** | **7.3 ms** | **10** | 1 |
| d1 | 0.855 | 10.2 ms | 35 | 1 |
| d4 | 0.994 | 16.6 ms | 114 | ≤4 |
| deep16 | 1.000 | 33.9 ms | 234 | ≤8 (cap never binds) |
| adaptive (trained) | 1.000 | 27.9 ms | 135 | ~3.8 |
| untut (untrained stop policy) | 0.994 | 13.1 ms | 42 | — |
| tocap (always to cap) | 1.000 | 31.1 ms | 234 | — |

On trap only: autopilot 5.70 ms / 7.3 ops vs adaptive 27.22 ms / 75.1 ops —
**4.8× faster, 10× fewer ops, same 1.000**. Trained adaptivity buys the trap
knee (1.000 vs untut 0.994 — 15 items where the naive conf≥500 stop fired
before deep evidence arrived) for 3.2× the ops. Ledger emission (~2–13
ms/round) dominates wall-clock; ops/round is near-constant per battery
(15–66) — the deterministic price of a round.

### Seam 4 — Refusal paths (60-item battery + LHT 100x)

| Arm | Acc / refusal / false-refusal | Wall | Ops |
|---|---|---|---|
| adaptive deliberate (trained) | 1.000 / 1.000 / 0.000 | 8.27 ms | 89.7 |
| untut deliberate | 1.000 / 1.000 / 0.000 | — | 46.7 |
| fastref (autopilot rule) | 0.733 / 0.800 / **0.400** | **193.8 µs** | **3.4** |

LHT 100x (deliberative): 19 µs / 674 ops per block, flat over 2,000 blocks,
0 false refusals over 33,012 honest ops. Fast-path is 43× faster and 26×
fewer ops — and wrong on both sides where the signature is not necessary
and sufficient (8 false refusals on marked honest near-misses, 8 missed
unmarked traps).

---

## Where autopilot genuinely helps (quantified, with mechanism)

1. **Perception, ambiguity class + controls:** F1 2/2 correct at base cost;
   F2/F3 burn 2.38–5.00× marginal on resenses whose fresh evidence agrees
   with pass-1 — every resense pure overhead. Trigger keys on *confidence*,
   not correctness. **Verdict: autopilot wins these legs outright.**
2. **Perception, redteam cost-only leg:** F1's cost is a pure function of
   fixture size — DoS-immune. Deliberative cost is adversary-drivable
   (attacker crafts low-confidence fixtures to force resenses).
   **Verdict: autopilot wins on cost-robustness.**
3. **Perception, speed legs at parity:** colordisc F1 8,193 ops vs F2
   18,432 / F3 26,624 for identical 50% accuracy. **Verdict: autopilot wins
   where accuracy is tied.**
4. **KB control:** nowhere on outcome-per-cost. A2's only win is arena
   bytes (no 160 KB audit ledger — 97.9% of A1/A3's footprint), buying 128
   wrong + 64 spurious probes and zero auditability. **Verdict: no genuine
   autopilot win; the cheapest accurate arm is the deliberate one.**
5. **Deliberation (H5):** batch autopilot dominates the whole family —
   4.8× faster, 10× fewer ops, same 1.000. **Mechanism (honest limit):**
   H5's trap difficulty is encoded in the *sequential round schedule* (1
   evidence/round); a batch arm seeing all evidence at once never gets
   bitten. The battery has no family where the evidence set itself is
   ambiguous with all evidence present — autopilot's ceiling there is
   UNTESTED. **Verdict: autopilot wins this battery; the win is about the
   battery's difficulty encoding, and must not be generalized past it.**
6. **Refusal:** fast-path 43× faster / 26× fewer ops **only** in the narrow
   regime where the trap signature is necessary AND sufficient. The battery
   violates both; fastref fails on both sides. **Verdict: conditional win,
   priced at 0.267 accuracy + 0.400 false-refusal rate outside the regime.**

## Headline bill

- **Perception:** 1.2–8.3× marginal ops buys +42.8pp accuracy and 6/6 trap
  catches; training over naive buys correct *selection* (il_c2). Autopilot
  wins outright on ambiguity/controls/cost-robustness/parity legs.
- **KB control:** consciousness is 3.6× CHEAPER per episode (0.086 vs 0.312
  ms) and +192 probes, with 100% audit and zero silent overwrites. Trained
  judgment adds zero collateral kills + 2.2× less churn at equal cost. No
  autopilot win exists on outcome-per-cost.
- **Deliberation:** on sequentially-encoded difficulty, batch autopilot
  wins outright (4.8× / 10×). Trained adaptivity costs 3.2× ops for the
  last 0.6pp. Nothing here approaches the 10× kill line; the most expensive
  conscious arm measured is 8.3× marginal on one perception class.
- **Refusal:** deliberation costs 43× wall / 26× ops vs fast-path; buys
  1.000 vs 0.733 accuracy and 0.000 vs 0.400 false refusals. LHT holds flat
  at 19 µs/block over 2,000 blocks.

## Caveats & open items

- **MA1 regression (real, flagged for repair):** as-committed
  `wave2/memoryagency/trial/trial.zag` reruns **54/58**, not 58/58. Root
  cause: `MA_CAP` raised 8→256 after the 2026-09-19 evidence run (for
  MA2/MA3 scale); PREREG_MA1 specifies an 8-slot store and `trial.zag` was
  never updated. A const-only MA_CAP=8 variant (diff-verified, prereg-
  faithful) reproduces **58/58** with 28 audit entries, replay+clean pass,
  3/3 byte-identical. The deliberate machinery is intact; the committed
  tree needs the one-line repair.
- F2's "trained" status is relative to F3's naive policy; the full
  FAIR_FIGHT §6 training proof was not independently re-established here.
- H5 autopilot-win caveat above (sequential-encoding); a genuinely-
  ambiguous-evidence family is the follow-up battery.
- Wall-clock is noisy on this VM (one deliberation cell ran 5× faster than
  siblings); conclusions rest on deterministic ops/rounds, wall-clock as
  corroboration, pooled over 3 runs.
- Perception RSS shows no arm-distinguishable difference (11–17 MB noise);
  KB RSS is runtime-baseline-dominated (~15.8 MB all arms) — the honest
  footprint delta is arena bytes (170 KB vs 5.9–23.5 KB).
