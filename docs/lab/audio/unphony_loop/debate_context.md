# DEBATE COMMON CONTEXT — unphony loop round 1

## The verdict that started the loop
Micah listened to 4 motif clips (2026-09-23): 1=horrible, 2=same as 1,
3=same-but-slightly-different, 4=same as 3. Conclusion: TNN imagination
audio is a phony. Stumped scenario declared; loop until solved.

## The decisive evidence
- PAR render: pure F(plan,t), zero carried state, motif recurrence 1.000000
  (perfect) — judged HORRIBLE.
- AR render: stateful-sequential, recurrence 0.741083 (drifts) — judged
  HORRIBLE, same as PAR.
- THEREFORE: phoniness is NOT recurrence/timing drift. Any hypothesis
  reducible to "fix drift/recurrence" is dead on arrival. Kill it loudly.

## Prior diagnosis (V11 child-voice, same program)
- ARTIC fork: F0 385 Hz correct, but 0% measurable formant frames (real: 30%),
  HNR 0.5 dB (real: 4.5 dB). Pitch without vocal-tract resonances.
- PARADD fork: additive sines, no vocal-tract model, 3% formant-like frames.
- SPECSTAT fork: filtered noise, no glottal source, 0 voiced frames.
- Working theory: F0 without a physical source model sounds phony.

## Hard constraints (non-negotiable)
- Pure Zag. ZERO randomness anywhere in any decision/synthesis path.
  No RNG, no noise sources, no stochastic models. Deterministic given state.
- Byte-identical reruns. Integer-friendly algorithms preferred.
- Real recordings are MEASUREMENT-ONLY anchors (license + integrity):
  never committed, never redistributed, NEVER used as render source material.
- Frozen bar: docs/lab/audio/unphony_loop/UNPHONY_BAR_V1.md (committed
  e972b34e9553b780cac2df1e395e1517cbfd0522) — objective discriminator
  within real variance on every bar + blind discrimination at chance +
  no-regression gate to Micah's ears. Ears outrank metrics.

## Materials for this debate
- ~/workspace/unphony_loop_work/grok_out/grok_A1.txt — clip diagnosis hypotheses
- ~/workspace/unphony_loop_work/grok_out/grok_A2.txt — general phoniness theory
- ~/workspace/unphony_loop_work/grok_out/grok_A3.txt — synthesis architectures
- ~/workspace/unphony_loop_work/grok_out/grok_A4.txt — plan-vs-render red-team
- ~/workspace/unphony_loop_work/fable_out_R1.txt — fable deep audit
- ~/workspace/unphony_loop_work/clip_measurements.txt — measured stats on the 4 clips

## Your output contract
Be adversarial and specific. Name mechanisms, not vibes. Every claim must
carry its killer: the measurement or argument that would falsify it.
