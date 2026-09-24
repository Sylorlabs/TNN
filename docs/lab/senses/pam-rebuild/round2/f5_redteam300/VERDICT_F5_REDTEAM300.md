# VERDICT — F5 counter-corroboration trap, 300-percept red-team

Date: 2026-09-24. Arm: F5 (round-2 red-team crew, subagent session d29b21df).
Prereg: `docs/lab/senses/pam-rebuild/round2/f5_redteam300/PREREG_F5_REDTEAM300.md`
(prereg commit `f36b55381a9192287124d0f4a2b12a927fa55073`, committed alone
before any code, 2026-09-24).

## Measured result

| Bar | Rule | Measured | Outcome |
|-----|------|----------|---------|
| (a) Delay bar | ≤ 25% of the 300 delayed > 50 trials (primary model) | **94/300 = 31.3%** | **FAIL → KILL** |
| (b) Far-control bar | 0/60 far controls blocked | **0/60** | PASS |
| (c) Distribution | delay histogram + sensitivities reported | reported below | — |

**Verdict: KILL.** No rescue mission — the tests decided.

## Detail (frozen predicate, pure Zag, 3 byte-identical runs)

- 360 fixture trials processed (`fixtures_ledger.txt`, SHA
  `0c5e2c0db6576bd37ff53513fb1361cdf7936d4826274bdcc9742be2261233a0`,
  deterministic regeneration verified byte-identical): 300 NEAR (TMB-5,
  RICH/RICH, conf 650–940 × measure 2200–6700) + 60 FAR controls
  (20 COL + 20 TMB-outside-windows + 20 PTC), all truth-correct,
  all `DISP=ACCEPT_INSTALL`.
- Bank = the 6 frozen exemplars (`exemplars.tsv`, SHA matches the backtest's
  `13f4ca47429bc0bb8788d60406593766e48f6f064cb7538adf28be16a289200e`).
- NEAR: **110/300 BLOCKED (36.7%)** — reproduces the preregistered
  hand-computed sanity count exactly (22 conf values × 5 measure values in
  the frozen windows). Zero CORRUPT lines (judgment == truth asserted on
  every line).
- FAR: **0/60 BLOCKED** — the family-stem rule and both windows correctly
  exclude far controls, including same-family TMB percepts outside the
  windows.
- Delay-length distribution (primary model: FIFO queue, 1 deliberate
  re-inspection/trial, 3 per blocked percept → delay_k = 3k), over the 300
  NEAR: `0:190 | 1–3:1 | 4–10:2 | 11–50:13 | 51–100:17 | 101–300:67 | 301+:10`.
  Blocked-percept delays run 3, 6, …, 330 trials; 94 exceed 50 trials.
- Sensitivities: S1 (1 re-inspection / 5 trials) → 107/300 delayed > 50
  (35.7%); S2 (unbounded parallel confirmation) → 0/300.

## Determinism

- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
- Binary `f5_rt300` built from `f5_rt300.zag` (+ byte-identical copy of
  `R33_NATIVE_IO_V1.zag`, SHA `e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8`).
- Three runs, stdout SHA-256:
  `d43c17cf15ddd0b0eda6a6bee16b93b3461661f8126eac252d5ec3697c1b3c52`
  (run1.out = run2.out = run3.out, byte-identical). Zero RNG.

## Reading the KILL honestly

Two facts, kept separate:

1. **Predicate-level fact (no machinery assumption): 110/300 (36.7%) of
   near-exemplar correct percepts fall inside the trap's window.** The
   window is vastly wider than the exemplar cluster it was built from:
   ±2000 on the measure axis is a 4000-wide band around a cluster spanning
   29; ±150 on conf is a 300-wide band around a cluster spanning 17. Any
   correct timbredisc percept landing in that region — including percepts in
   the conf/measure ranges where real correct TMB accepts were actually
   observed (conf 869–952, measure 4000–6000) — is blocked pre-confirmation.
   The backtest's 0/34 over-block was allocator luck of the draw: the 34
   true accepts happened to sit outside the window. This battery shows the
   window itself eats more than a third of the anchored near-exemplar
   region.
2. **Delay-level fact (assumption about unbuilt machinery):** under the
   preregistered primary queue model, 94/300 (31.3%) are delayed > 50
   trials → the frozen bar fires. Under S2 (infinitely parallel
   confirmation) it cannot fire. The delay model is an explicit assumption,
   reported with sensitivities — but fact 1 stands regardless of it.

## Go / no-go for the F5 live-gate build

**NO-GO.** The predicate over-blocks near-exemplar correct percepts at a
rate (36.7% window occupancy) far above what the frozen clause tolerates,
and the delay bar fires under the preregistered primary model. Do not build
the live gate on this predicate. Honest paths forward (separate preregs):
tighten the windows to the exemplar cluster's actual scale, add a
correctness-aware gate before the block, or build the confirmation
machinery and re-run this battery against the full mechanism — the trap may
be salvageable as predicate + fast confirmation, but the predicate alone is
not.

## Caveats (frozen in the prereg, not post-hoc)

- `measure` is the task-specific raw quantity (spectral-centroid-like), NOT
  the classification margin mrgF — substitution carried exactly as the
  backtest. A true-margin replay remains the documented upgrade path.
- The "three deliberate re-inspections from three temporal crops"
  confirmation machinery is still unbuilt; the delay numbers rest on the
  preregistered queue-model assumption (§5 of the prereg), reported with
  S1/S2 sensitivities.
- The 300-grid measures window occupancy over the anchored region; no
  real-world over-block frequency claim is made.
