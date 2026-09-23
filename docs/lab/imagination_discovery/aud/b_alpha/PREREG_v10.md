# V10 PREREG — synthesize from understanding (frozen 2026-09-23)

Micah's verdict on V9: one scene now (WIN), but choppy like chunks cut out of
a constant recording (LOSS). Directive: TNN must combine its UNDERSTANDING of
audio and SYNTHESIZE, not play/cut one clip. Try something other than gates.
Ask Sol for inspiration. Fork multiple synthesis approaches.

## Paradigm shift (non-negotiable)

ABANDON concatenative chunk assembly: no recorded atoms, no splicing, no
gating pre-cut chunks on/off. The renderer must generate the playground from
an internal generative model of the sound — its understanding of voice
production, laugh structure, footstep physics, spatial air. Continuous
internal state; smooth parameter trajectories. Choppiness must be impossible
BY CONSTRUCTION, not fixed in post.

## Frozen constraints (all forks)

- Pure Zag (pinned znc `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`).
  Python for glue/analysis/forensics only.
- Zero RNG in the render path. Deterministic hash streams allowed.
  Byte-identical reruns (prove with `cmp` across two renders).
- 30 s mono 44.1 kHz 16-bit WAV.
- Creative law: ONE consistent imagined scene — little kids (ages ~3-6) in a
  playground, age-consistent, mood-consistent. The composed moment from V9
  (yard alive -> chase -> trip -> laugh -> wind down) may be reused as the
  scene script or replaced by an equally coherent one.
- Nine frozen bars (consistency_gate/src/gate.zag) must PASS: G-PER, G-STA,
  G-LURCH, G-DRIFT, G-FLUXm, G-SIL1, G-SIL2, G-CLIP, G-CREST. No WARN tripped.
- Technical wins kept: no tremolo/wandering (0.5-2 Hz modulation within the
  real-anchor envelope), no dips, no cutouts, no clipping, no DC offset.

## New kill bar: CHOP — no choppiness

A blind listener must not hear chunk boundaries or random dropouts of the
scene. Instrument (forensic, Python):

- CHOP-1: zero sample-level hard discontinuities (jump > 12000 counts in one
  sample with smooth neighbors). HARD bound.
- CHOP-2: no near-silent gaps >= 150 ms outside the 30 ms end fades.
- CHOP-3: spectral-flux spike audit — count flux spikes above the natural-
  transient threshold; EVERY spike must correspond to a scene-scripted event
  timestamp (footstep strike, laugh onset, shout). Unexplained spikes =
  hidden chunk boundaries = FAIL.
- CHOP-4 (structural): the fork's design doc must state WHY choppiness is
  impossible by construction (continuous state / smooth trajectories), and
  the implementation must contain no atom-placement, no gated on/off event
  triggering, no chunk ring/buffer splicing. Code audit.

Micah's ears are the final judge. The gate is necessary, not sufficient.

## Fork designs (FROZEN 2026-09-23 — Sol divergent round informed, convergent
round attempted twice, provider declined; designs frozen on Sol + analyst judgment)

### Fork A — ARTIC (articulatory/physical; from Sol's proposal)
Voice = phase-integrated glottal-pulse oscillator (F0 250–500 Hz, smooth
vibrato + pitch glides, differentiated rounded glottal pulse + aspiration
noise) through 3–4 formant resonators (~700/1800/2800/4000 Hz, child
bandwidths). Laughter = repeated smooth pitch rises/falls + breath bursts
through the SAME vocal model (not a separate effect). Footsteps = damped
2nd-order contact oscillator driven by a smooth half-sine force profile
(x''+2ζωx'+ω²x = a(t)u(t)), step rate gliding 2–4 Hz. Air = filtered hash
noise + weak resonant playground reflections, bounded away from silence.
Control: deterministic scene script, every parameter on cubic Hermite / C²
bump trajectories (20–80 ms attacks, 100–500 ms releases). No-chop argument:
persistent phase/filter/envelope state everywhere; no buffers, atoms, or
gates exist in the design.

### Fork B — PARADD (parallel parametric additive; from Grok's proposal)
3 voice channels = sine-LUT oscillators + 2–4 harmonic partials (detuned by
fixed hash offsets) under smooth exponential/cubic envelopes; laughter =
hash noise through a time-varying 2nd-order bandpass (800–1800 Hz, Q 3–6)
with a slow bursty gain trajectory (0.4–1.2 s sigmoid swells); footsteps =
damped sinusoids (2.5–6 kHz) with smooth exponential decay + impact boost;
ambience = hash noise through a slowly-varying 4-pole lowpass (cutoff
trajectory 0.3–2 Hz). Control: hash-chain scene script (40–60 events),
parameters linearly blended per sample. No-chop argument: every output
sample is a combination of continuous phase accumulators and memory-bearing
IIR filters; all parameters C¹ in time; no parameter ever jumps.

### Fork C — SPECSTAT (spectral-statistical resynthesis; analyst design)
One-time analysis of a real playground recording into slowly-varying
band-energy statistics via a hand-built filter bank (no FFT, no atoms kept).
Resynthesize NEW audio by driving a bank of resonant filters with ONE
continuous noise-excitation stream whose per-band energies follow a composed
30 s scene trajectory derived from those statistics. The "understanding" is
the statistical spectral model of real play; the scene script composes new
trajectories through it. No-chop argument: the excitation never stops or
restarts, band gains are smooth trajectories — nothing is cut, spliced, or
gated at any point.

All three are genuinely different paradigms (physical production model vs
parametric additive vs statistical resynthesis). Shared risk to guard:
voices sounding synthetic (mitigate with aspiration, formant motion, pitch
instability, several independently-controlled children) and ambience
sounding looped (G-PER bar guards this).

## Head-to-head test

Every fork renders its clip, passes the nine bars + CHOP instrument, and is
ranked by: (1) CHOP-3 unexplained-spike count, (2) nine-bar margins,
(3) structural purity audit. Winner = fewest unexplained spikes with all
bars passed. Ears decide the final cut among the top two.

## Commits

Prereg (this file) committed BEFORE any fork render. Each fork: renderer
source + clip + findings doc. Winner documented in FINDINGS_v10.md.
All to branch tnn-native-lab via the racefree script, lab-relative paths.
