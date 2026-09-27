# De-synth atom calibration — 2026-09-27

Replaces the old FM-oscillator calibration. The planner no longer calibrates
FM indices; it calibrates two measured voice atoms (real source-derived
timbres) the way a musician learns an instrument: play fixed pitches, listen,
record where the pitch lands.

## Method

`cal_run` (in `plan_main_desynth.zag`) renders each atom FLAT (no contour) at
three probe pitches through the production renderer, re-hears each probe with
the organ, and records:

- **f0 bias** (ppm): `(heard_f0 − commanded_f0) / commanded_f0 × 10⁶`
- **CV yield** at 220 Hz: the atom's own measured pitch-variation (cv_pm)
- **voiced fraction** at 220 Hz

The planner's predictor then bias-corrects: `fpred = f + f × bias_ppm(f)/10⁶`
with linear interpolation between the 90/220/1010 Hz table entries.

## Measured values (deep battery run, /tmp/battery2)

| timbre | probe 90 Hz | probe 220 Hz | probe 1010 Hz | CV yield @220 | voiced frac @220 |
|---|---|---|---|---|---|
| atom0 (child voice) | heard 0 Hz — **organ cannot hear 90 Hz** (voiced_frac 0) | heard 220452 Hz → bias **+2054 ppm** (+0.21%) | heard 1009666 Hz → bias **−330 ppm** | 1 pm | 988/1000 |
| atom1 (speech voice) | heard 0 Hz — **organ cannot hear 90 Hz** (voiced_frac 0) | heard 221110 Hz → bias **+5045 ppm** (+0.50%) | heard 1010657 Hz → bias **+650 ppm** | 2 pm | 611/1000 |

## Honesty notes

1. **The 90 Hz calibration point is degenerate.** The organ hears nothing
   (f0 = 0, voiced fraction 0) for a 90 Hz flat render of either atom, so
   `bias90_ppm = 0` is a placeholder, not a measurement. The bias table
   effectively rests on the 220 Hz and 1010 Hz points. Low-pitch calibration
   is therefore unanchored — a known weakness (see BATTERY_VERDICT §5).
2. **The calibration measures the organ's hearing bias, not the renderer's.**
   `bias = heard − commanded` conflates renderer error with estimator error.
   For flat renders the two agree (renderer verified accurate: 220.472 Hz
   commanded → 220.5 Hz measured by independent analysis), so the table is
   valid for flat actions. For contour actions the planner re-uses the same
   table, but the organ's hearing of contour renders is separately biased
   (up to +45%, see BATTERY_VERDICT §5) — the table does not cover that.
3. Calibration is deterministic: identical atoms + identical organ → identical
   table, byte-identical across reruns (verified deep battery 1 vs 2).
