# HUM DIAGNOSIS — 4 motif clips (ar/par × fixed/recur)

**Date:** 2026-09-24. **Analyst:** audio coordinator (waveform-first).
**Trigger:** Micah's ears verdict — "consistent hum behind" all four clips,
clips 3+4 "the same damn thing," zero improvement heard.

## 1. What the hum is

The hum is the **frozen fixture's continuous 110 Hz bed**:
`BED 0.0 30.0 110.0 250` in `fixture/plan_v1.txt` — 110 Hz at 25% FS,
running 0–30 s under every note. It is not a synthesis bug and not mains
hum; it is composed content, and it dominates every delivered excerpt.

Whole-excerpt spectral measurement (Hann-windowed FFT, tonal peak vs median
2–8 kHz floor):

| clip | 110 Hz strength | next tonals |
|---|---|---|
| ar_motif_fixed | **63.7 dB** | 220, 330, 554, 440, 659 Hz |
| ar_motif_recur_fixed | **64.8 dB** | same stack |
| par_motif_fixed | **67.4 dB** | same stack |
| par_motif_recur_fixed | **67.4 dB** | same stack |

The full stack (110/220/330/440/554/659 Hz) is the bed's harmonic series
**fused with the motif pitches**: 110×4=440, 110×5=550≈554.37,
110×6=660≈659.25. The bed's harmonics land on/near the motif notes, so the
whole clip reads as one static harmonic drone — "the same damn thing."

## 2. Why clips 3 and 4 are identical (legitimate, never communicated)

`par_motif_fixed.wav` and `par_motif_recur_fixed.wav` are **SHA-256 identical**
(`fef400e3…`). This is by construction, documented in `build0_rerender.txt`
but never told to Micah: PAR is pure F(plan,t), deterministic, and the 110 Hz
bed completes exactly 2420 integer cycles between the 1.5 s and 23.5 s cut
points (22 s × 110 Hz). AR's recur differs slightly (5.41 dB spectral diff)
because AR carries state. The identical pair looked like fraud; it was an
uncommunicated determinism property.

## 3. Was the vibrato fix real?

Yes — but masked. Note pitch centers in the fixed renders sit at plan
+1.43…+1.60 Hz (uniform +0.36% vibrato smear, proven a peak-picker artifact
also present in ideal float synthesis), vs +3.2…+6.7% sharp before the fix.
Carrier/lobe ratio 0.30 → 1.75. The fix is in the audio; the bed buries its
audibility, and nobody measured what ears would hear.

## 4. The kill test (2026-09-24)

Re-rendered the fixed PAR and AR binaries against plan copies with the bed
at −12 dB (amp 63) and off (amp 0). Frozen fixture untouched. Excerpts cut
at the verified byte offsets (66150 / 1036350, 4.0 s).

| variant | 110 Hz hum | Δhum | note HNR | ΔHNR | pitch err |
|---|---|---|---|---|---|
| par bed250 (as delivered) | 70.8 dB | — | 8.16 dB | — | 1.69±0.38 Hz |
| par bed63 (−12 dB) | 58.8 dB | **−12.0** | 12.59 dB | **+4.4** | 1.69±0.38 Hz |
| par bed0 (off) | 20.2 dB | **−50.6** | 15.36 dB | **+7.2** | 1.69±0.38 Hz |
| ar bed250 (as delivered) | 68.8/69.7 dB | — | — | — | — |
| ar bed63 (−12 dB) | 55.0 dB | **−13.8** | — | — | — |
| ar bed0 (off) | 14.5 dB | **−54.3** | — | — | — |

The hum scales exactly with the bed gain (−12.0 dB measured for a −12 dB bed
change) → the bed is the sole hum source. Pitch centers are unchanged across
mixes → the vibrato fix survives independent of the bed. Note HNR rises
+4.4/+7.2 dB as the masking bed is removed.

## 5. Judgment mixes (NEW, M4A per M4A1)

In `~/workspace/audio_humkill/` (workspace only; not committed — audio
binaries stay out of the repo):

- `par_bed0_off_motif.m4a` / `par_bed0_off_recur.m4a` — NEW, hum −50.6 dB
- `par_bed63_-12dB_motif.m4a` / `par_bed63_-12dB_recur.m4a` — NEW, hum −12 dB
- `ar_bed0_motif.m4a`, `ar_bed63_motif.m4a` — NEW, hum −54.3 / −13.8 dB

WAV masters + full 30 s renders alongside. Plan variants
(`plan_bedlow.txt`, `plan_bedoff.txt`) record the exact parameter deltas.

## 6. Recommendation

Ship judgment mixes with the bed attenuated or off for all future ear panels
on this material; keep the frozen fixture for measurement. The bed is
composed content, so any permanent mix change is a composition decision for
Micah — the variants above are the head-to-head test, not a decision.
