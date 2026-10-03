# PREREG DP-1 DOPPLER FLYBY [NEW] - wave-20260925-1721pdt

Date: 2026-09-25. Worker: sensory headspace, depth-2.
Status: FROZEN pre-implementation. Kill bars below are frozen and will not move.

## Provenance header (machine-checkable)

RENDER_SHA: <sha256 of dp1_variant_r1.wav, filled at render time in EVIDENCE>
FIRST_RENDERED_WAVE: wave-20260925-1721pdt
COMPONENT_LINEAGE: D-AUD-3-substrate(synth.zag f76293f6061812aaaedeac59ae67440bf949b23c1bf9ebc7e60211df1c58f055, vendored byte-identical as sub/synth_base.zag); R9:QUEUED-UNJUDGED; C1:QUEUED-UNJUDGED; C2v3:QUEUED-UNJUDGED; S11-IMG:QUEUED-UNJUDGED; S11-AUD:QUEUED-UNJUDGED; S12:DEAD; S12b:DEAD; S13:QUEUED-UNJUDGED; S14:QUEUED-UNJUDGED; whirlpool-planform:QUEUED-UNJUDGED; B1:DEAD; DF-1:DEAD; C-D19:DEAD; G1:STOOD-DOWN; ST-1:DEAD; D-VID-1:STOOD-DOWN
NEW_KNOWLEDGE_CLAIM: A frozen constant-velocity flyby rendered through a time-varying propagation delay adds motion-based realism to the D-AUD-3 bed via doppler pitch fall, inverse-distance loudness swell, and lateral pan at linear resampling cost.
Tag: [NEW]. Not a re-certification. Queue items are listed only as lineage.

## Mechanism (new)

DP-1 renders a single heavy lifter flying past the Kethra mic on a frozen
straight-line trajectory and propagates its engine tone through a
time-varying delay line. Per output sample at time t (seconds):

  x(t)   = V * (t - T_CA)                 lateral position, V = 30 m/s
  d(t)   = sqrt(DMIN^2 + x(t)^2)          slant range, DMIN = 15 m
  tau(t) = d(t) / C                       propagation delay, C = 319 m/s (argon, Kethra; same constant S11-AUD used)
  g(t)   = D_REF / d(t)                   inverse-distance gain, D_REF = 25 m
  u(t)   = x(t) / d(t)                    lateral unit (-1..1)
  gL(t)  = sqrt((1 - u)/2), gR(t) = sqrt((1 + u)/2)   constant-power pan

Output y[n] = g(t) * CAL * src((t - tau(t) + PREROLL) * SR), linear
interpolation on the fractional source index, then panned by gL/gR.
T_CA = 10.5 s (closest approach mid-piece), PREROLL = 1.0 s, SR = 44100.

The engine source is rendered from substrate-style primitives (my own new
function, deterministic): 6 inharmonic partials, f0 = 48 Hz, stiff-bar
B = 0.0008, amplitudes 1/(1+0.5*(k-1)), 0.4 Hz throb at depth 0.25,
2 s rise / 1 s fall envelope, 22.0 s span. No samples, no RNG, no IR.

Calibration (disclosed, deterministic): the implementation renders the
source, measures its Q24 peak, and sets CAL = TARGET_FLYBY_PEAK /
(src_peak_q24 / 512 * GMAX) with GMAX = D_REF/DMIN = 1.6667 and
TARGET_FLYBY_PEAK = 8000 int16 units at DP_SCALE. Same value every run.
This is gain staging, not bar gaming: all bars are measured post-hoc.

Variant = D-AUD-3 bed (score_aud3, untouched calls) dual-mono plus the
stereo flyby. Baseline = bed dual-mono, same writer, same scale.
Does not stack S11-AUD. Does not touch b_alpha or audio_principles.

## Metric moved and cost

Moves perceived source-motion realism of the D-AUD-3 bed: a static scene
gains an approaching/receding pitched source (doppler fall about
1.2x across the pass, 26 dB loudness swell, left-to-right pan). No prior
loop metric covers this; KB3 certifies the physical cue is present at
analytic strength; final judgment is his ears. Cost: one linear
resampling pass over 21 s stereo plus a 22 s source render; KB7 caps
variant wall at 2.0x baseline wall.

## Frozen kill bars

KB1 determinism: variant stereo WAV sha256 identical across 3
  independent runs; trace file sha256 identical across 3 runs. PASS iff all match.
KB2 no clipping: peak int16 magnitude < 32767 in baseline and variant.
  PASS iff true.
KB3 doppler correctness: verifier measures zero-crossing frequency of the
  isolated probe stem in approach window [3.0, 6.0] s and recession window
  [15.0, 18.0] s; ratio approach/recession within +/-3 percent of the
  analytic window-center ratio 1.20694 recomputed from frozen C, V, DMIN,
  T_CA. PASS iff within.
KB4 crest: |20*log10(crest_variant / crest_baseline)| <= 1.5 dB,
  crest = peak/RMS on int16 WAV. PASS iff true.
KB5 energy: |20*log10(rms_variant / rms_baseline)| <= 2.0 dB. PASS iff true.
KB6 pure Zag: pinned znc sha256 prefix 498abcb5; token grep over all
  DP-1-authored .zag finds zero hits for rand, srand, random, time, clock,
  python (comment hits for none). PASS iff clean.
KB7 cost: variant wall time <= 2.0 * baseline wall time. PASS iff true.
KB8 trace audit: verifier recomputes tau, g, gL, gR at every trace
  checkpoint from frozen params; 0 mismatches at 1e-9 relative epsilon.
  PASS iff 0.

DP_SCALE = 0.09 frozen for the fixed-scale WAV writer (no normalization,
no soft clip; fades 30 ms in / 0.8 s out identical for baseline and
variant). Baseline bed measured pre-prereg (disclosed characterization):
bed_q24_peak = 123529294 (int16 241268 at scale 1.0), bed_rms_q24 =
13791633.770. At DP_SCALE 0.09 the bed peaks at 21714 with headroom for
the calibrated flyby (worst-case coincident peak 29714 < 32767).

## Consistency check (pre-implementation; standing governance)

Mechanism and bars jointly satisfiable:

KB1: every input is a frozen constant; noise from h32; trig from the
substrate LUT; f64 IEEE ops in fixed order. No RNG anywhere. Satisfiable.
KB2: TARGET_FLYBY_PEAK = 8000 and DP_SCALE = 0.09 put the worst-case
coincident peak at 29714, margin 3053. Satisfiable by construction.
KB3: analytic ratio derives from the same frozen params the renderer
uses; zero-crossing quantization over 3 s windows at ~48-53 Hz is under
1 percent against a 3 percent tolerance. Satisfiable.
KB4/KB5: flyby peak is 0.37x bed peak and its energy is concentrated in
about 3 s of 21 s; estimated crest shift under +0.6 dB and energy shift
under +1.4 dB, both inside bars. Satisfiable; if measurement disagrees
the candidate is DISCARDED, bars do not move.
KB6: pure Zag by construction; verifier greps. Satisfiable.
KB7: resampling is O(N) with a small constant; the bed render dominates
wall time. Satisfiable.
KB8: verifier replays the identical f64 op sequence. Satisfiable.

No bar contradicts the mechanism. No narrowing needed. Proceeding.

## Prior-art verification (greps recorded)

Repo-wide grep over docs/lab/rsi/runs and docs/lab/imagination_discovery
(excluding .zag-cache), 2026-09-25:

  vibrato: runs=0 imag=22 | chorus: runs=14 imag=19 | formant: runs=2 imag=77
  transient: runs=2 imag=74 | detune: runs=2 imag=8
  doppler: 0 | flyby: 0 | variable-delay: 0 | fractional-delay: 0
  humaniz: 0 | sub-harmonic: 0 | glissando: 0

The runs/ hits for chorus/formant/transient/detune are D-AUD-3 score
content words (EM chorus group, formant resonators, glass-strike
transients, detuned sub partials), not candidate mechanisms. No loop
candidate has ever used doppler, variable-delay propagation, or a moving
source. S11-AUD used static geometry (early reflections plus Schroeder
late reverb); DP-1 uses time-varying delay from source motion, a
different mechanism in the broader physical-acoustics space.

## Red-team self-review (novelty)

1. vs S11-AUD (physical-space propagation, QUEUED-UNJUDGED): S11-AUD is a
   static room (fixed taps, fixed RT60). DP-1 is source motion
   (time-varying tau, doppler shift). No shared code path, no shared
   parameter, opposite ends of the propagation static/dynamic axis.
   Not a re-freeze.
2. vs ST-1 (stereo panning, DEAD): ST-1 panned static stems with a frozen
   table. DP-1 pans one moving source analytically from its trajectory.
   Different mechanism; and ST-1's death was a crest miss, not a concept
   this replays.
3. vs substrate vibrato (render_struck vibd/vibr): periodic pitch wobble
   already exists in the substrate for some tones. DP-1 is a one-way
   trajectory pitch shift from propagation delay, not oscillation.
   Different mechanism.
4. Honest weakness: doppler shares the physical-acoustics theme with
   S11-AUD. The distinction (static room vs moving source) is real but
   thematic overlap is disclosed for the judge.

## Timeline

Prereg frozen here, pre-implementation, committed alone. RENDER_SHA to be
filled at render time. Implementation and evidence commits follow.
