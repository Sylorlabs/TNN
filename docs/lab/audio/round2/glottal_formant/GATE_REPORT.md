# FORK 1 (glottal_formant) — GATE REPORT (2026-09-24)

## Verdict: PASS — all shared gates + kill bar.

## Engine
LF-model glottal flow derivative (simplified: sin hump + sharp
closure spike) driving 6 PARALLEL formant resonators (800/1200/2800/
3500/4500/6000 Hz). Phrase: /ba/ (196 Hz), /da/ (247 Hz), /ga/
(294 Hz). 0.5 s/note, 20ms consonant bursts (bypass formants for
sharp transient). Deterministic breath + 5.5 Hz vibrato.

Note: formants are PARALLEL (summed, normalized), not series. Series
connection multiplies resonant gains (175^6 = blowup). Documented as
an implementation correction.

## Final metrics (gf_full.wav)
- frac_static: 0.7079 [PASS ≥0.25]
- HNR: 6.62 dB [PASS 0.7–6.7]
- periodicity: 0.8211 [PASS ≥0.5]
- HF rolloff: −17.85 dB [PASS −40 to −12]
- prosody: 0.546% [PASS 0.3–3%]
- onset crest: 8.51 dB [PASS 3–20]
- peak: −1.17 dBFS [PASS < −1]
- centroid: 965.8 Hz

## Kill experiment: LF→sine swap
- LF (full): HF rolloff −17.85 dB
- Sine: HF rolloff −24.63 dB
- Difference: 6.78 dB (≥6 dB). KILL PASSES.
The LF glottal model contributes 6.78 dB of high-frequency energy
vs a pure sine. The source (not just the filter) is load-bearing.

## Determinism
3× reruns byte-identical.
WAV SHA-256: 27a9247f0f0dbcd736a2f596aeef25cf488e8c2665d6957fb4927e1b5c02d785
NEW M4A SHA-256: 60337ba844eeef7a1b251382ca30480e6645eb2364b98d023cbe79a446c11de4

## Files
- `gf.zag` (source: prelude + fork1_body.txt)
- `gf_full.wav` (also r1/r2/r3 byte-identical)
- `gf_sine.wav` (kill control)
- `glottal_formant_NEW.m4a` (staged for ear)
