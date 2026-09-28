# FORK 5 (transient_first) — KILLED (2026-09-24)

## Verdict: KILL — fails the prosody shared gate; mechanism incompatible.

## What works (kill experiments PASS)
- Burst-removed: crest 13.72 → 10.07 dB (drop 3.65 dB ≥ 3 dB).
  The 3 ms burst is load-bearing for the transient. PASS.
- Fastdecay (damp 0.992): sustain 3.0 s → 0.5 s (< 3 s).
  The damping controls sustain. PASS.
- HNR 6.8, HF −12.05, crest 13.7 dB, peak −7.0 dBFS all pass.

## What fails
- PROSODY: 6.5% (bar [0.3%, 3%]). FAIL.

## Root cause (honest negative)
The Karplus-Strong pluck DECAYS. As the amplitude decays, the F0
tracker's autocorr peak weakens and it jumps between lags, inflating
measured prosody to 6.5%. The true pitch is static (531 Hz measured
on the loud attack). 

The fork is caught in a bind:
- Static pitch → true prosody ~0% → fails the ≥0.3% floor.
- Decaying amplitude → tracker artifact 6.5% → fails the ≤3% ceiling.
- The HNR bar forces enough noise to worsen tracker instability.

A plucked string (decaying) is fundamentally incompatible with a
prosody gate designed for sustained voiced tones. This is a
mechanism/gate mismatch, not a bug. The KS engine itself is sound
(kills pass).

## Per the task rules
"A failed per-fork kill bar kills the fork" — the kills PASSED, but
"Each surviving fork must pass [shared gates]" — prosody FAILED.
Fork 5 does not survive. No clip shipped.

## Artifacts (committed for the record, not for the ear)
- `tf.zag` (source), `pluck_full.wav`, `pluck_noburst.wav`,
  `pluck_fast.wav` + SHAs in manifest.
