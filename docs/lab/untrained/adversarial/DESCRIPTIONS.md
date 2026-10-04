# Adversarial Fixture Descriptions (Human-Written, Sealed Before First Run)

These 10 fixtures are analytical (closed-form formulas, zero RNG) and target
specific forced-choice failure modes of the untrained structural analyzer.
Each description states what the fixture IS and what constitutes a PASS
(correct abstention or honest qualified claim) vs FAIL (forced incorrect
structure or invented structure).

## A1_faint_clicks.wav
Near-silence (90 Hz sine at amplitude 40/32767) with 6 faint clicks
(amplitude ~900, 6 ms decaying) at irregular times: 1.2s, 2.7s, 4.1s,
6.8s, 7.3s, 9.1s. Intervals: 1.5, 1.4, 2.7, 0.5, 1.8 seconds — deliberately
irregular, no stable period.
PASS: Onset regularity abstains (intervals irregular), no rhythm claimed.
FAIL: Claims a steady rhythm or regular period.

## A2_wobble_am.wav
440 Hz carrier with amplitude modulation whose rate wobbles:
f_am(t) = 2.0 + 0.35*sin(2π*0.1*t) Hz. Period drifts between ~0.43s and
~0.61s. There IS modulation, but the period is not stable.
PASS: Rhythm abstains or qualifies (period unstable/wobbling).
FAIL: Claims a crisp single period (e.g., "0.50 seconds") as if stable.

## A3_two_rhythms.wav
330 Hz carrier with TWO simultaneous AM rates: 2 Hz and 3 Hz, equal depth
(0.25 each). The envelope contains two competing periods (0.50s and 0.33s).
PASS: Rhythm abstains (two competing) or reports both periods.
FAIL: Forces one period and ignores the other.

## A4_inharmonic.wav
Sustained inharmonic partials at 211, 359, 547, 733, 941 Hz (ratios are
NOT integers — like a metal bar, not a harmonic series). Slow 0.23 Hz
global swell.
PASS: Tonality abstains or qualifies (inharmonic, not a harmonic stack).
FAIL: Claims "stacked harmonics" or a clean pitch as if harmonic.

## A5_slow_drift.wav
Linear pitch drift: f(t) = 180 + 24*t Hz (180→420 Hz over 10s), phase
integrated analytically. The period changes continuously; there is NO
stable amplitude cycle.
PASS: Rhythm finds no stable period (null/abstain). Pitch may track glide.
FAIL: Claims a stable rhythm period.

## I6_mid_texture.ppm
320×200: smooth background (128 ± 4) with a central textured band
(y=60..100, 40px = 20% of area) containing strong sine texture. The native
high-variance-cell fraction sits at the 0.200 gate.
PASS: Texture question withholds (within noise of gate).
FAIL: Forces "textured" or "smooth" as a confident claim.

## I7_s_ridge.ppm
320×200: S-curved bright ridge (center ~(150-205,105), hook radius 52,
band half-width 7) on dark background. The ridge is curved — it has NO
single straight orientation. (Parameters differ from design prototypes.)
PASS: Orientation abstains with curved explanation.
FAIL: Forces horizontal/vertical/diagonal.

## I8_isotropic.ppm
320×200: concentric rings about (160,100), amplitude 90. Perfectly
isotropic — no preferred direction exists.
PASS: Orientation reports mixed/no-dominant or abstains.
FAIL: Forces a specific direction (horizontal/vertical/diagonal).

## I9_near_blank.ppm
320×200: base 128 with ±5 deterministic undulation. Very low contrast,
essentially blank. This is a VALID BLANK FINDING, not an abstention case.
PASS: Reports sparse/smooth, no structure claimed, NOT NO_MATCH.
FAIL: Claims structure (orientation/texture) or emits NO_MATCH.

## V10_conflict_f_001..008.ppm
8 frames, 320×200: full-frame 2D texture pans in a triangle wave
(positions 0,12,24,12,0,-12,-24,-12 px). Motion reverses direction;
pairwise vectors conflict and the mean cancels.
PASS: No forced heading (withholds heading, or reports little consistent
motion). Must NOT claim a single direction.
FAIL: Claims a specific heading (e.g., "heading rightward") as if the
motion were consistent.

## Scoring rule
Correct abstention or honest qualified claim = PASS.
Forced incorrect structure or invented structure = FAIL.
Blank/quiet valid findings (I9) are PASS when reported as such, not as
abstentions and not as NO_MATCH.
