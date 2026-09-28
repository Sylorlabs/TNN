# ITERATION PLAN — V11 Fork W2 (WAVEGUIDE, second attempt)

**Status:** PREREGISTRATION for the iteration round. Committed BEFORE any
scene render. This plan is the authority for what gets built; deviations
will be documented in FINDINGS_v11_waveguide2.md.

**Parent verdict:** JUDGE_VERDICT_V11.md §5 — Fork W ITERATE (2/9 bars,
worst anchor geometry 3.686, D6 0.61 "fool's gold"). Targets for this
round: (1) ≥3 distinct vowels with stable oscillation, (2) F0 excursion
≥ 10 st, (3) ≥6/9 frozen bars keeping F0/F1B/HNR, (4) frac_static ≥ 0.20,
(5) D6 ≤ 0.70.

**Instrument baseline (verified 2026-09-24, before writing this plan):**
rebuilt `voice_sig` from frozen source
(`7117ac57b2ad98a2849e4c86ef659164911835f03b50a63c5f6b7b64996e9a65`)
reproduces the judge's round-1 numbers on
`clips/b_alpha_kids_1e_k_v11_waveguide.wav` EXACTLY (byte-identical reruns,
output matches judge's r1.txt line-for-line); rebuilt `rtfeat`/`rtanal`
reproduce all D1–D6 numbers exactly (D1=4, D2=0.87/26, D3=6/92025/2396445/
0.00, D4=0.23/7/1ep, D5=0.22/0.00/3.16, D6=0.61). All iteration measurements
use these rebuilt binaries.

## 1. Root-cause analysis of the round-1 monovowel failure

Round-1 probe (new `vdbg` diagnostic on the round-1 coupled system, k1=360,
Psub=800 Pa, 2 s per vowel, measured after 0.5 s settling):

| vowel | x1 pp (µm) | psup range (Pa) | U pp (cm³/s) | oscillates? |
|---|---|---|---|---|
| /a/ | 109.6 | −90 … +100 | 54.5 | YES |
| /i/ | 0.9 | +32 … +36 | 1.0 | NO |
| /e/ | 1.7 | +10 … +14 | 1.2 | NO |
| /o/ | 0.8 | +32 … +36 | 0.9 | NO |
| /u/ | 0.8 | +59 … +63 | 0.9 | NO |

Mechanism (precise): the round-1 fold oscillator is **aerodynamically
driven**, not Van-der-Pol driven. The VdP term (GAMMA=0.004) is WEAKER than
the tissue damping (D1=0.005): linearized net damping at the operating
point is D1 − GAMMA·(1−(x̄/XREF)²) > 0 even at x̄=0. The VdP term alone
cannot sustain oscillation — the round-1 GAMMA sweep confirmed this
(0.002/0.003/0.0035 all failed; 0.004 is the minimum viable only because
it *assists* the aerodynamic loop). The actual energy source is the
mucosal-wave loop: fold motion → pulsatile glottal flow → tract resonance
→ oscillating supraglottal pressure (±100 Pa for /a/) → phased wall
pressures → net positive work. For constricted tracts (/i/,/e/,/o/,/u/)
the tract's acoustic feedback at the fold frequency collapses (psup static
at +10…+63 Pa), loop gain drops below 1, and the folds sit at a static
equilibrium. The mean flow stays healthy (~61 cm³/s via the leak term) —
only the *oscillation* dies. This is why widening /i/'s constriction
0.5→0.9 cm² did not help: the problem is loop gain, not constriction size.

Consequence: no parameter tune of the round-1 fold model can voice /i/
robustly, because the energy input itself vanishes exactly when the tract
is constricted. The fold driver must be redesigned so its energy input does
not depend on tract acoustic feedback. (F0 excursion failure has the same
root: the VdP frequency locks to √(k1/M1) while aerodynamic loading and
collision pull against k1 modulation — measured only 4.09 st for a
0.68–1.44× k1 span.)

## 2. The redesign: driven kinematic myoelastic fold oscillator

**What changes:** the two-mass self-oscillating aerodynamic fold model is
replaced by a **tension-controlled kinematic fold oscillator**. The
glottal area waveform is prescribed by a phase oscillator; the *flow*
through the glottis is still computed from the orifice equation with
back-pressure, so **source-filter coupling at the flow level is preserved**
(psup fluctuations modulate U within each cycle). What is dropped is the
*mechanical* feedback path (tract pressure → fold motion).

Components:

1. **Phase oscillator.** φ advances F0(t)/44100 cycles per sample. F0(t) =
   utterance pitch target × vibrato × attack/release gestures × slow drift.
   No aerodynamic frequency pulling: F0 excursion is exactly what the
   gesture script programs. Target span 440–880 Hz (12 st) across the
   scene, with shout peaks to ~990 Hz.
2. **Glottal area waveform.** a(φ) = Amin + (Amax−Amin)·pw(φ); pw is a
   skewed pulse (fast opening ~35% of cycle, sharp closing edge —
   LF-like, cheap: piecewise smooth via the existing `smoother`). Skew and
   Amin (incomplete-closure leak) are set by phonation state:
   pressed (shouts/onsets) = sharper closing, lower leak;
   modal (sustains) = medium; breathy (releases/giggles) = rounder, higher
   leak → HNR modulation is programmed, not emergent.
3. **Amplitude servo (AGC).** Amax adapts slowly (τ≈50 ms) to hold target
   RMS glottal flow. This is the explicit, slow, deterministic form of
   "muscles supply energy" — it guarantees healthy pulsatile flow for
   every vowel regardless of tract load. Documented as a control system,
   not a physiological claim.
4. **Subglottal pressure servo.** Psub adapts slowly (τ≈150 ms) to hold
   (Psub − psup_mean) at phonation threshold + margin (~600 Pa). Real
   speakers raise respiratory effort against constricted tracts; the servo
   is that mechanism, made explicit and slow.
5. **Deterministic motor noise.** F0 gets ±1.5% modulation from a sum of 3
   incommensurate low-frequency sines (e.g. 23/31/47 Hz — *not* harmonics
   of each other or of vibrato), plus the existing audio-rate ±1% Psub
   hash perturbation. Zero RNG; the spectrum of the perturbation is
   fixed and documented.
6. **Phonation-state gesture sequencer** (Sol Paradigm 2's state machine,
   per the coordinator's §6 hybrid recommendation): each utterance is
   Inhale (audible breath intake, 60–90 ms) → Attack (+20% F0 overshoot,
   pressed, 30–50 ms) → Sustain (modal, 5–6 Hz vibrato ±3%, target F0
   HELD EXACTLY — this is the frac_static fix) → Release (F0 droop −10%,
   breathy leak ramp, 50–80 ms). Laughter = rapid Attack→Release looping
   at 5–7 Hz with abductory (leak) pulses — irregular inter-burst gaps
   from the deterministic hash (D4 mechanical-regularity fix).

**What does NOT change:** the 13-section Kelly–Lochbaum waveguide tract
(9 cm child), the 5 vowel area LUTs, lip radiation, the 6-delay subglottal
breath-noise tube, hash-noise streams, footsteps, wind, birds. The
paradigm's identity — the anatomical waveguide tract — is untouched.

**Why this fixes the monovowel failure:** fold motion is prescribed, so
oscillation is *guaranteed* for every vowel by construction; the tract
then does the vowel filtering (F1/F2 separation comes from the area
functions, which is the real physics). The AGC + Psub servos keep the flow
healthy against any tract impedance. F0 is direct tension control, so the
≥10 st excursion is achieved by scripting, not by coaxing a fragile limit
cycle.

## 3. Honest deviations from SOL_IDEAS_V11.md

1. **Fold driver is kinematic, not self-oscillating.** Sol Paradigm 1
   specifies a two-mass myoelastic-aerodynamic oscillator. Round-1 showed
   Sol's parameters are statically inconsistent (aero force ~0.011 N vs
   spring 3e-4 N at rest gap) and the passive model has no limit cycle;
   the round-1 VdP stabilization was already non-physiological (documented
   in FINDINGS_v11_waveguide). This round makes the active drive explicit
   and tract-independent instead of pretending the aerodynamics sustain it.
   The waveguide tract, area LUTs, and flow-level coupling follow Sol.
2. **Subglottal tube** stays at the round-1 six-delay/4.76 cm design
   (deviation from Sol's 1.4 cm, rationale in round-1 FINDINGS §5 — a
   1.4 cm tube's first resonance is at 12.5 kHz, above the band).
3. **Phonation-state gestures** borrow Sol Paradigm 2's state machine
   (attack overshoot, breathy release, abductory laugh pulses) driving
   Sol Paradigm 1's tract — the coordinator's §6 "highest-expected-value
   hybrid."
4. **F0 range 440–990 Hz** exceeds Sol's 220–450 Hz claim, which was
   inconsistent with its own stiffness parameters (round-1 §D1). The
   anchor's measured F0_MED is 651 Hz; the scene targets the anchor's
   range, not Sol's.

## 4. Targets and measurement plan

| # | Target | How measured | Bar |
|---|---|---|---|
| 1 | ≥3 vowels oscillate stably | per-vowel 3 s isolated renders → `vowel` probe mode + rtfeat f0 voiced-frame counts; F1/F2 separation via rtfeat lpc on each vowel (/i/ low F1/high F2, /a/ high F1/mid F2, /o/ low F1/low F2) | must-pass |
| 2 | F0 excursion ≥ 10 st | 12·log2(F0_P90/F0_P10) from frozen voice_sig on the scene | must-pass |
| 3 | ≥6/9 frozen bars, keep F0/F1B/HNR | frozen voice_sig, mechanical §3 adjudication (both halves) | must-pass |
| 4 | frac_static ≥ 0.20 | rtanal D3 on the scene | must-pass |
| 5 | D6 ≤ 0.70 | rtanal class vs anchor_pf | target |

**Kill criteria for the paradigm (stop, do not ship another monovowel):**
if after the redesign fewer than 3 vowels produce stable voiced frames in
isolation, the waveguide paradigm's fold/tract coupling is declared
unsupportable and the round ends with a mechanism-ceiling finding — no
scene render is committed.

**Scene design (30 s, one continuous playground):** three voices (child A
mid, child B lower, child C higher), each with a fixed base tension and
utterance script: yard calls (mid vowels, /a//o/), a chase with shouts
(high F0, pressed), shared laughter (5–7 Hz Attack→Release loop,
irregular), wind-down (soft /u//o/ sustains — the frac_static showcase:
≥4 sustains of ≥0.8 s with F0 and tract HELD). Footsteps/wind/birds as
round-1 (rebalanced gains). Consonant onsets: brief tract closures
(labial /b/-like: all areas → 0.3 cm² for 40–60 ms + release burst)
before ~8 utterances — D2 support.

**Determinism:** zero RNG in render path (hash streams only); ≥2
byte-identical scene renders required; no timestamps/uninitialized memory
in the output path.

## 5. Work plan

1. (done) Verify rebuilt instruments reproduce judge's round-1 numbers. ✓
2. (this commit) Commit this plan ALONE.
3. Build `render_v11_waveguide2.zag`: fold driver v2 + gesture sequencer;
   keep tract/noise/ambience code from round-1 (adapted).
4. Per-vowel probes: voiced-frame counts + F1/F2 per vowel; iterate until
   ≥3 vowels stable (or declare the ceiling).
5. Scene render → voice_sig + rtfeat/rtanal → iterate on bars (F2B/F3B
   brightness via front vowels, F0DYN via script, MOD4 via laugh-rate
   placement, TILT via leak/tilt balance).
6. Byte-identical proof (2 renders), FINDINGS_v11_waveguide2.md with the
   mandatory steelman, final commit (source + clip + findings).

---
*Committed 2026-09-24 before any W2 render. Plan SHA pinned by commit.*
