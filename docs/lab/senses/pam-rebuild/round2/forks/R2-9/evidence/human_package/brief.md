# R2-9 Human Judge Brief (KB-E3/E4)

You are judging whether R2-9's sensory emissions are faithful and beautiful.
This package contains 151 VISUAL trials in randomized double-blind order.

## What to do
For each trial J###:
1. Look at `source` (the original stimulus) and `emission` (R2-9's output).
2. Read `claim.txt` (what R2-9 claims it perceived).
3. Judge:
   - KB-E3 (fidelity): Does the emission faithfully represent the source?
   - KB-E4 (beauty): Is the emission beautiful / does it show imagination?
4. Record your verdict per trial.

## Audio trials: GATE-BLOCKED
49 audio trials (pitchdisc, timbredisc) are NOT included in this package.
Reason: The frozen protocol requires audio to pass a full waveform gate
(envelope stationarity, spectral drift, loop periodicity, transient regularity,
THD) calibrated against real field recordings. That gate is not implemented;
only a partial gate (peak/clipping, DC, envelope stationarity) exists,
calibrated against human-produced references, not field recordings.
Per the protocol: do not fake it. Audio is withheld until a compliant gate passes.
The 49 blocked trials are listed in `audio_gate_blocked.tsv`.

## Blinding
- Trial order is randomized. `manifest.tsv` (sealed) maps judge IDs back to
  sample indices; do not open it until judging is complete.
- `claim.txt` contains the fork's claim but NOT the ground truth.
- Clean/adversarial status and attack family are not revealed.
