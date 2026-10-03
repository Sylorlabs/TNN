# REDTEAM DP-1 DOPPLER FLYBY - wave-20260925-1721pdt (self-review, adversarial)

## 1. Novelty

Repo-wide grep (recorded in prereg): doppler 0 hits, flyby 0, variable-delay
0, fractional-delay 0, in runs and imagination_discovery. No loop candidate
has used source motion. The runs/ hits for chorus/formant/transient/detune
are D-AUD-3 score content words, not mechanisms. Genuinely new.

## 2. S11-AUD mechanism-class challenge (strongest objection)

S11-AUD is "physical-space propagation" (QUEUED-UNJUDGED): static early
reflections plus Schroeder late reverb, fixed geometry. DP-1 is also
physical acoustics. Is DP-1 a re-freeze of that class?
Counter: S11-AUD's mechanism is time-INVARIANT filtering (fixed taps, fixed
RT60). DP-1's mechanism is a time-VARYING delay from source motion; it
produces pitch shift, which no static filter can produce. No shared code,
no shared parameter, no shared measurement. The theme overlaps; the
mechanism does not. Held as [NEW], disclosed honestly.

## 3. ST-1 (DEAD) replay check

ST-1 died on KB7 crest (+1.61 dB over a 1.5 dB bar) with static panning.
DP-1 pans one moving source analytically. Different mechanism, and DP-1's
KB4 passes at 0.994 (essentially no crest change). Not a replay.

## 4. Substrate vibrato collision

render_struck already implements periodic vibrato (vibd/vibr), used by
D-AUD-1 glass tones. DP-1 is a one-way trajectory pitch shift from
propagation delay, not oscillation. Different mechanism. The D-AUD-3 bed
itself uses vibd=0.0 everywhere, so there is no interaction.

## 5. Bar integrity

- KB3 tolerance +/-3%: measurement quantization under 1% (3 s windows,
  ~150 cycles). No gaming; the analytic ratio is recomputed from frozen
  params, not hardcoded.
- KB4/KB5: the flyby is calibrated to 8000 int16 peak (0.37x bed peak);
  ratios 0.994/1.007 show the mechanism barely perturbs mix statistics,
  which is the honest result, not a tuned pass.
- KB7 1.867x: under the 2.0x bar with margin, but the closest bar. The
  cost is the 22 s engine render plus the resampling pass; both linear.
- KB8: 210/210 checkpoints match the identical op sequence within 1 ulp
  of the 1e-9 scale. No transcription drift.

## 6. Calibration honesty

The runtime CAL normalizes the engine to TARGET_FLYBY_PEAK. This is gain
staging, disclosed in the prereg before implementation. It does not touch
pitch (KB3), determinism (KB1), or the mix-statistic bars (KB4/KB5
measured post-hoc). The same CAL results every run (deterministic source).

## 7. What could still be wrong

- The flyby is a new world event (a lifter), not a transformation of an
  existing voice. It is content-adjacent. The mechanism (doppler
  propagation) is the candidate; the lifter is its carrier. Flagged.
- Thematic overlap with S11-AUD (finding 2) is the real judgment call and
  belongs to the owner alongside the queued items.
- Audibility was not ear-checked by the worker (no listening possible);
  levels were set analytically (flyby peak ~10 dB above bed RMS at
  closest approach). His ears decide.

## 8. Verdict on the red team

No padding, no re-freeze, no bar movement, no frontier contact. DP-1
stands as [NEW] with all bars passing. READY-FOR-JUDGE.
