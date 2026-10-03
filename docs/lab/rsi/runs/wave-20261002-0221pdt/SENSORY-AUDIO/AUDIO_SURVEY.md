# AUDIO SURVEY - SENSORY-AUDIO lane, wave-20261002-0221pdt

Survey date: 2026-10-02. Method: read the verdict/status docs under
docs/lab/audio*, docs/lab/audio_intake, docs/lab/audio_longhorizon,
docs/lab/audio_principles, plus recent commit history. No audio worker ran
this wave before this lane; the SENSORY image line (H3) runs separately.

## Standing laws (bind this lane)

- AUDIO_PREDELIVERY_GATE.md (Micah 2026-09-24): waveform analysis FIRST,
  measured delta vs previous version, SHA identity check, NO ear claims by
  agents (Micah's ears are the final oracle), artifact labels NEW /
  PREVIOUSLY SHOWN / REFERENCE, M4A for ear-judgment clips, pure Zag,
  deterministic byte-identical reruns, never commit binaries or .zagd,
  frozen fixtures never edited in place.
- Round-3 no-synth law: no oscillators, no parametric excitation, no
  synthetic noise; every output sample traces to a recorded sample through
  a documented transform. STATIC IS THE KILLER (hard gate for ears).
- Fidelity bar: output must sound like real life. Human ears outrank any
  audio metric (report both).

## Line 1: long-memory intake (v5 -> v6)

- VERDICT_INTAKE.md (2026-09-26): intake is sample-exact at parse; F0 intake
  essentially perfect (<=0.2 Hz); spectral gaps are downstream (imagine
  walk) EXCEPT the cry peak overshoot (1.92x), which was intake: two
  machinery bugs, L1 fabricated 64-sample head and L2 plm half-period phase
  mismatch.
- REPAIR_HEAD64.md (2026-09-26): both fixed, RBLMEMv5 -> RBLMEMv6 (true head
  samples stored). Cry: peak 23834 -> 12406, corr 0.89618 -> 0.99827,
  matching the ablation exactly. Honest representation floor now corr
  ~0.998 on the hardest clip (64-prototype quantization, by design).
- State: CLOSED. No known intake-adjacent items remaining.

## Line 2: audio_longhorizon semantic model (phase 3)

- phase3/VERDICT.md (2026-09-26): semantic excitation
  s[j] = proto[q[j]] + amp[per]*plm[hb] + impulse[j] on 359 sealed clips.
- H1 transient-event channel (THE BIG ONE): top M = max(16, nr/500)
  residual-error samples as deterministic (position, amplitude) impulses.
  Residual RMS shrank 91-94% per class; semantic RMS improved 26-40% per
  class. No clip regressed. This is the largest measured fidelity effect
  in the audio line's history.
- H2 joint per-period amplitude: strictly better than phase 2, no clip
  regresses (min gain +10.1%).
- H4 selective refused-harmonic acceptance (r^2 > 0.10): 14/14 accepted
  clips improved 23-65%.
- Killed by measurement: H3 (extra tail levels, redundant), H5 (HF shaping,
  ratio artifact, energetically negligible).
- Exactness layer untouched: 359/359 bit-identical (mode 10).
- State: COMPLETE, gate green. The transient channel exists ONLY in the
  hear/re-emit (analysis) path.

## Line 3: de-synth measured-timbre renderer + planner (latest render work)

- 2026-09-27: synthetic renderer (oscillator + FM + exp10) replaced by
  measured-timbre renderer: measured harmonic stack + measured per-period
  amplitude (time-warped, no exp10) + measured texture (pitch-synchronous).
  Zero oscillators/FM/synth primitives in the planner production path.
- Transients: HONESTLY DISABLED. The atom stores NIMP (pos, amp) events,
  but desynth_render.zag skips them. Reason (source comment, P2 #8):
  the peaks were extracted from the period-synchronous residual, which
  does not isolate valid transients (residual RMS exceeds the source due
  to harmonic leakage; speech peaks measured ~170x harmonic RMS).
  Rendering them as impulses broke voicing detection. The comment names
  the required future work: "Transient rendering needs a fixed residual
  isolator (future work); do NOT re-enable without a separate valid
  extraction mechanism."
- Round 3 (2026-09-27): MP3 32kHz honest kill (no discrepancy); planner D2
  contour KILLED (error redistribution); planner residual narrowed to a
  spike-statistic problem; t17 octaves unfixable at planner level.
- Round 4: V-D directional rule held-out test (frozen prereg).
- Closure (2026-09-27, three-wall integration, CLOSED): Wall 1 trig-free
  hearing; Wall 2 low-F0 mis-hearing repair (t20: 890.2 -> 96.9 Hz);
  Wall 3 envelope vocabulary (4 measured atoms: 2 rise, 2 decay;
  level-normalized). Final battery 20 targets: mean err_pm 775 -> 425
  (-45%), 11 improved / 4 regressed / 5 flat, 20/20 WAVs byte-identical.
- Honest residuals post-closure: envelope/F0 tradeoff on t8/t12/t14; t17
  hearing octave outliers; t19/t20 low-F0 floor; renderer D2 (commanded
  contour mean renders at ~0.59x); Wall-3 extractor crash for source F0
  below ~172 Hz.
- Waveform symptom (closure evidence/waveform_battery_final.tsv, t1):
  reference has 21 onsets / 5 s; the render has 1 onset / 2 s. The
  imagination renders are nearly onset-free: the transient structure of
  real audio is missing from every render.

## Line 4: round2/round3 forks, unphony loop, audio_principles

- Round 2 ear verdicts (Micah 2026-09-24): glottal_formant BEST (no
  static), skeleton_refine middle, prosody_ab WORST (static). Static is
  the killer.
- Unphony loop: vibrato-depth bug found and fixed (2pi too large);
  BUILD 0 re-render PREDICTION-HELD.
- audio_principles crews P/C/L: dither, chance baselines, sealed targets;
  crew P organ.zag is the standing forward sense (pure Zag WAV parse).

## Current state of the audio line (2026-10-02)

- Intake: solved (v6, honest floor corr ~0.998).
- Analysis (hear/re-emit): strong (phase-3 semantic model, transient
  channel dominant, 359/359 exact).
- Imagination (planner + renderer): functional but not quality-passing.
  The renderer has TWO measured channels (harmonic stack, texture) and is
  missing the THIRD (transients): the dominant fidelity mechanism from
  phase 3 is at ZERO on the render path, blocked only by the invalid
  legacy extractor. Renders are onset-free vs onset-rich references.
- No audio work since 2026-09-27. Nothing in this lane is currently
  queued for Micah's ears.

## The gap SA1 attacks

Phase-3 H1 proved the transient-event channel is the dominant fidelity
mechanism (91-94% residual shrinkage), but it lives only in the
analysis path. The imagination renderer disables it because the legacy
extraction was invalid (harmonic leakage). The renderer's own source code
names the unblocking work: a fixed residual isolator. SA1 builds that
isolator in pure Zag, adds the measured transient channel to the render
structure, and tests it against frozen bars. This is a structural
synthesis change, not a re-enable of the killed path: the killed path
used invalid (leakage) peaks; SA1 uses a new valid extraction mechanism,
exactly as the source comment requires.
