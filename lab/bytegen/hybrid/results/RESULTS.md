# Hybrid v2 — results

**Build:** `src/render_hyb.zag` →
`toolchain/bin/znc_linux_x86_64_abed8aa1`
**Source SHA-256:** `73742f8fc3ceebe0d65884aea56e3182ee7861be942be676a0adfad8e1f054ba`
**Date:** 2026-09-24. Fixture: `bytegen/fixture/plan_v1.txt` (23 events, 30 s).
Reproduce: `tests/run_tests.sh` (builds, renders, diffs, prints this table).

## Determinism (zero RNG)

Three clean reruns + the clean render, all SHA-256 identical:

```
1823f8fa82af3aca23c598b902c53a0df072315c84e7c5509b26625299427ca4  rerun1.wav
1823f8fa82af3aca23c598b902c53a0df072315c84e7c5509b26625299427ca4  rerun2.wav
1823f8fa82af3aca23c598b902c53a0df072315c84e7c5509b26625299427ca4  rerun3.wav
1823f8fa82af3aca23c598b902c53a0df072315c84e7c5509b26625299427ca4  clean.wav
```

## Piece 1 — PAR motif path

- `clean.wav` is **byte-identical** (`cmp`) to
  `bytegen/fork_par/src/par_seq1.wav`. The default path IS PAR.
- Motif recurrence (2.0–5.15 s vs 24.0–27.15 s, zero-lag xcorr):
  **1.000000** (was 0.741083 under v1/unbounded AR; PAR baseline 1.000000).

## Piece 2 — exception detect-and-reassert

1292 blocks/render; trace `*_trace.txt` logs per-block
`(rms6, exp6, peak, fault, healed)`. Target calibration:
`K_PLAN = 49585` = median(measured/analytic) = 0.7566; spread min/med 0.57,
max/med 1.43, all inside the `[0.35, 2.5]` band. Zero false faults on all
clean renders.

| Attack | Detection | Healed output vs clean |
|--------|-----------|------------------------|
| 64-sample bit-flip @ 3.0 s | block 129: `fault=1` (peak edge) | **0 diffs** / 1,323,000 |
| Full-block dropout @ 3.0 s (1024 zeros) | block 129: `rms6=0`, `fault=1` (RMS lower edge) | **0 diffs** |
| Sustained: 64-sample bit-flip EVERY block | 1292/1292 `fault=1`, 1292 healed | **0 diffs** |

No-heal controls (raw damage the healing erases): bit-flip 64 diffs @
3.0000–3.0014 s; dropout 1023 diffs @ 2.9954–3.0186 s; sustained 82,688
diffs @ 0.000–29.978 s. No propagation in any control (pure synthesis
cannot cascade — damage is confined to corrupted samples).

Contractivity: the correction map `C(x) = plan_render(block)` is constant
in `x` → Lipschitz 0, idempotent, one-step convergence. Proven in
`HYBRID_SPEC.md` §2; empirically: the sustained attack is fully healed
with no oscillation across 1292 consecutive corrections.

## Piece 3 — RESPOND octave latch

Original RT-LONG (`tests/plan_long.txt`: 440 Hz cue, nominal 880, 27 s gap):
`nvoice=1 fm=456Hz nom=880Hz k=-1 → LATCHED f0=28835840` = **440·65536
exactly**. The latch corrects the plan's octave; it does not trust the
biased 456 Hz measurement. Rerun SHA identical
(`1027c5e24537199a33345ecfd4c1f08bbb0758cf38ee69bd1ccd7c5fca780dbe` ×2).

Multi-trap (`tests/plan_long_multi.txt`):

| Trap | Cue | Nominal | Result |
|------|-----|---------|--------|
| A polyphonic dyad 220+330 | 2 voices | 880 | `nvoice=2 → nominal` (abstain) |
| B single 440, wrong nominal | 1 voice, fm=456 | 880 | `k=-1 → LATCHED f0=440` exact |
| C single 523.25, correct nominal | 1 voice, fm=510 | 523 | `k=0 → nominal` (44¢ < 600¢ gate) |

The estimator's signal-dependent bias (±60¢ measured: 456 on the cue,
425.5 on the vibrato-less response) is why the gate is octave-scale
(600¢), not fine — the honest capability is octave-error detection.

## What the numbers say vs the old claims

- Recurrence: 0.741083 → **1.000000** (state carry eliminated, not clamped).
- Single-fault cascade: 6,217 post-window diffs (v1, "contained") →
  **0 diffs** (v2, healed). The v1 count is disclosed, not hidden: the old
  loop could only ride out corruption; re-assertion erases it.
- RT-LONG: "corrected 880→440" was really 880→465 (97¢ sharp). v2 latches
  880→**440 exactly** — by refusing to use the measurement as a pitch value.
- Sustained adversarial fault: v1 left 55,802 differing samples with 0
  after 4.8 s; v2 leaves **0 everywhere** (every block healed in place).
