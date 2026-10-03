# LISTENING INSTRUCTION - DP-1 DOPPLER FLYBY

Candidate: DP-1 DOPPLER FLYBY [NEW], wave-20260925-1721pdt.
Status: READY-FOR-JUDGE. Not adopted, not queued. Your verdict decides.

## Files

- Baseline: docs/lab/rsi/runs/wave-20260925-1721pdt/sensory/dp1/dp1_baseline.wav
  (D-AUD-3 bed, stereo, 21 s)
- Variant: docs/lab/rsi/runs/wave-20260925-1721pdt/sensory/dp1/dp1_variant_r1.wav
  (same bed plus the flyby, stereo, 21 s)

Both at the same fixed level. No normalization tricks between them.

## What to listen for

A heavy lifter crosses the basalt plain mic at constant speed, closest at
t = 10.5 s. Listen on stereo speakers or headphones:

1. Motion: the source enters far left, swings through center at 10.5 s,
   exits far right.
2. Pitch: the engine tone falls in pitch as it passes (about a 1.2x drop
   from approach to recession, measured 52.5 Hz to 43.5 Hz on the stem).
3. Loudness: a long swell peaking at closest approach, then receding.

## The question for your ears

Does the flyby make the planetvoice scene feel like a real place with
something moving through it, or does it read as a synth effect pasted on?
Compare against the baseline. There is no metric behind this; your ears
are the kill bar.

## Provenance

Mechanism: time-varying propagation delay (doppler) from a frozen
trajectory, inverse-distance gain, constant-power pan. Pure Zag,
deterministic, all 8 frozen kill bars pass (see EVIDENCE_DP1_1721.md).
Does not stack S11-AUD. Does not touch your frontier work.
