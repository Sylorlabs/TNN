# AUDIO PRE-DELIVERY WAVEFORM GATE (standing policy, effective 2026-09-24)

**Authority:** Micah, 2026-09-24, after the 4-motif-clip ears verdict.
**Cause:** Agents cannot hear audio. Claims of audio progress were made without
measuring the delivered waveforms (par_motif_fixed.wav and
par_motif_recur_fixed.wav shipped BYTE-IDENTICAL under two names; the "hum"
was never measured).

## The gate

No audio clip reaches Micah's ears unless ALL of the following hold:

1. **Waveform analysis FIRST.** Every audio hypothesis is tested against
   measured waveform data BEFORE any render is presented: HNR, spectra,
   envelope stationarity, spectral drift, loop-periodicity, transient
   regularity, hum/tonal detection (incl. 50/60 Hz and harmonics).
2. **Measured delta vs the previous version.** The delivery note states the
   metric, the old value, the new value, and the measurement method.
   "Sounds better" is not a metric. No delta, no delivery.
3. **Identity check.** SHA-256 of every delivered file is recorded; two files
   with the same hash are ONE file and are labeled as such. Never ship the
   same bytes under two names again.
4. **No ear claims by agents.** Agents describe measurements, never how
   something "sounds." Micah's ears are the final oracle; the brief attached
   to a clip states what was changed and what the meters say.

## Artifact labels (mandatory)

- `NEW` — never presented before.
- `PREVIOUSLY SHOWN` — presented before, unchanged or re-presented.
- `REFERENCE` — calibration / anchor material, not a deliverable.

## Delivery format

**M4A1 APPROVED (2026-09-24):** all future ear-judgment clips are delivered
in M4A (AAC). WAV masters stay in the work dirs for measurement.

## Engineering rules

- Pure Zag for instruments and synthesis. Deterministic: byte-identical reruns.
- Race-free commits to `sylorlabs/TNN`, branch `tnn-native-lab`.
- Never commit binaries or `.zagd` files.
- Frozen fixtures are never edited in place; judgment variants are labeled
  copies with the exact parameter delta recorded.
