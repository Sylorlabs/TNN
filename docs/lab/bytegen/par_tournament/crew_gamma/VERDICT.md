# CREW GAMMA — VERDICT
**Question:** after removing the output-derived normalizer, which absolute-level strategy wins — H1 (re-stage plan energies for gain 1) or H2 (one fixed, output-independent mastering gain)? Control = old output-derived peak normalizer.
**Method:** pinned toolchain, zero RNG, 3 byte-identical reruns (84 SHA comparisons, 0 mismatches), analyzer-driven only. 7 variants × 4 hifi fixtures.

## 1. Clipping (rail samples = ±32767, exact counts)

| variant | song | happy | scary | calm |
|---|---|---|---|---|
| ctl (gain-1) | 6825 = 5.896% | 5257 = 4.059% | 23338 = 16.936% | 0 |
| **h1** (re-staged) | **0** | **0** | **0** | **0** |
| h2a (G=32767/124074, hottest@FS) | 0 | **1 sample** (0.0008%) | 0 | 0 |
| h2b (G=32767/104680, scary@FS) | 23 (0.020%) | 20 (0.015%) | 1 sample | 0 |
| h2c (G=32767/248148, half) | 0 | 0 | 0 | 0 |
| h2d (G=32767/27441, calm@FS) | 11987 = 10.356% | 7765 = 5.995% | 32993 = 23.943% | 0 |
| revert (old normalizer) | 0 | 0 | 0 | 0 |

Peaks: ctl 32768/32768/32768/27441 · h1 8726/7577/11645/14608 · h2a 31092/32767/27645/7246 · h2c = h2a/2 · revert 24000 on all four.

## 2. Plan-dynamics preservation (per-1 s-window RMS ratio vs control; max deviation in dB — 0.000 = bit-exact scaling)

| variant | song | happy | scary | calm |
|---|---|---|---|---|
| h1 | 0.08346 / 0.003 dB | 0.06940 / 0.042 dB | 0.13374 / **0.170 dB** | 0.53172 / 0.016 dB |
| h2a–d | 0.027–0.153 dB (pure gain; residual = clipping/rounding only) | | | |
| revert | intra-file 0.027–0.153 dB, but **inter-file ratios destroyed**: 0.2265/0.2172/0.2773/**0.8746** — every file pinned to 24000 peak; the quiet calm is scaled **UP** ×0.8746 |

H1 preserves relative dynamics to ≤0.17 dB (integer energy-rounding noise; worst on scary's small energies). H2 is a pure gain — dynamics bit-exact. The old normalizer is linear within a file but erases all inter-render level relationships.

## 3. Gamma proof (R3 retention)

Shared-prefix diffs, hifi [0,107484) + 8 kHz [0,20000): **ctl, h1, h2a, h2b, h2c, h2d = 0 diffs** on both paths. Revert hifi = **107,428 diffs** — the disease returns exactly as the repair recorded (107,428), validating the revert reconstruction.

## 4. Consistency gate (9 bars; fixture clips 2.6–3.1 s, so G-LURCH/G-SIL1 fail on the short ruler for ALL variants including control — measurement limitation, not a strategy difference)

- Level-invariant bars (G-PER, G-STA, G-DRIFT, G-FLUXm, G-CREST): **identical values across all variants per fixture** — empirical level-invariance confirmed.
- G-CLIP fails exactly where rail% > 0 (ctl song/happy/scary, h2a happy by 1 sample, h2b song/happy, h2d song/happy/scary).
- No variant introduces a new silence/density failure vs control.
- Crest: ctl song 2.110 (clipping squashes it) → h1 6.707, h2a 6.808, revert 6.808. H1's crest differs slightly from H2's (6.707 vs 6.808): re-staging rounds each voice's energy, so the H1 mix is not a bit-exact scaled copy of the control mix — dynamics preserved to 0.17 dB, not to the bit.

## 5. Cost
- H1: one-time per-fixture census (mechanical source analysis) + integer multiply baked into plan authorship; **zero runtime cost**; but it mutates the plan (mix-level result changes) and every new plan needs its bound computed.
- H2: one integer multiply per sample at emit (same as the old normalizer's per-sample cost, minus the two-pass peak scan); plan and mix untouched.
- Revert: two-pass (scan + scale) — most expensive, and diseased.

## 6. Tournament interaction
- Frozen `plan_v1.txt` already satisfies the H1 discipline (24 voices, max 2 simultaneous, authored worst-case **0.950 FS**): H1 correctly requires **no** re-staging — the rule must not mutate frozen plans.
- Stock tournament renderer vs H2-style fixed-gain variant: raw `seq+mix` dumps **byte-identical**; WAVs differ (peak 27852 vs 21668) → mastering is strictly downstream of mix generation.
- **Surfaced:** the tournament's own `render_par.zag` `wav_write` carries an output-derived 0.85-FS peak normalizer (`(mix*27852)/peak`) — the tournament's own gamma-disease instance, same class as the one just repaired.

## 7. Recommendation (what the tests decide)

**H2 wins**, with a safety margin. H1 achieves 0% clipping by construction but is 2.8–3.6× over-conservative (song RMS −21.6 dB vs control), mutates plans (mix-level result changes), perturbs inter-voice ratios by integer rounding (0.17 dB), and needs a per-plan census for every new fixture. H2 keeps mixes byte-identical, preserves dynamics exactly, kills the gamma disease (0 diffs), and costs one multiply per sample.

- Tested h2a (hottest fixture at exactly full scale) lands **1 sample on the rail** — fails a strict zero-rail bar. Back the gain off:
- **Recommended: G = 32767/124074 × 0.95 ≈ 0.25089** (integer form `v*31128/124074`), calibrated once on the four-fixture corpus, fixed for all renders. Expected: 0 rail samples on the measured corpus with ~0.45 dB headroom, gamma-clean, bit-exact dynamics.
- Conservative alternative: h2c's half gain (G = 32767/248148 ≈ 0.13206), 0 rail samples with 6 dB headroom, quieter.
- Honest limit of H2: the constant is calibrated on the fixture corpus; a future fixture hotter than happy would touch the rail (graceful clipping, no disease). H1 is the choice only if per-plan zero-rail guarantees without corpus calibration are required.

## 8. Broken governance bars (need Micah-signed amendments before altered bars govern reruns)

1. `imagination/HIFI-PREREG.md` H3 — says zero rail samples and peak ≤24000+1. Broken by the repair: gain-1 renders hit 32768 peak with 5.896%/4.059%/16.936% at rail (song/happy/scary).
2. `imagination/MOOD2-RESULTS.md` H3 — says zero rail samples and peak exactly 24000. Broken the same way.

## 9. UNSIGNED-DRAFT amendments (not law until Micah signs)

### UNSIGNED-DRAFT — HIFI H3 amendment
> H3 (post-repair): zero rail samples (±32767) on all hifi fixtures; mastering is one fixed, output-independent gain G declared in the prereg (value, calibration corpus, safety margin), applied identically to every render; no output-derived rescaling at any stage. Inter-render peak/RMS relationships must be preserved to measurement precision (per-1 s-window RMS ratio vs the unmastered mix constant to ≤0.2 dB). The old "peak ≤24000+1" normalized bar is retired.

### UNSIGNED-DRAFT — MOOD2 H3 amendment
> H3 (post-repair): zero rail samples (±32767) on all mood fixtures; mastering is the same fixed gain G declared for HIFI; no per-file peak normalization — the old "peak exactly 24000" bar is retired and replaced by the fixed-gain policy plus a declared headroom criterion (peak ≤ 0.95 FS on the calibration corpus).
