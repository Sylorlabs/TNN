# F1 epoch_graft — Final Analyzer/G4 Report
Date: 2026-09-25
Prereg: ~/workspace/audio_round3/ROUND3_PREREG.md (frozen 2026-09-24)

## Source SHAs
- vowel_real.wav: 8ba3b42708a8bab2bb8152d392d4425c5c248591d545f3bd1b24070e264e5d1d
- kidb.wav: 13285a0da02de5a830e289924ba4c9e5b831ac86bbd7de0002f033d7046682a3
- All 44.1 kHz mono 16-bit PCM.

## Plan
- plan.bin SHA: 1551226008b2f3ebd106926c34fd05a8ffade6ef8aa0d85313f66231f189de86
- Fossil: frames 0-392 (393 frames), 785 marks, slice 773-87345, peak 23560
- Donor: kidb frames 2573-2618 (46 frames), CV 1.2424008155672617%, median F0 493.71903047640404 Hz
- Donor marks: 113/113 used, 0 truncated
- Mapping: linear, unique 1.0, max reuse 1
- G: 1.0 (G_x1e12=1000000000000)

## Render SHAs (3x byte-identical)
| Variant | WAV SHA | Peak | Provenance SHA |
|---------|---------|------|----------------|
| a | 14c7f43f40b51ec8ab2f12f521798bc704314b0e2e95f9b5c4e46e037905008f | 22133 | de0e5f5eeaef72830379d6c152dfc3e2a002f7703c3536f1da23eb64b80d8c41 |
| b | 3bea9096bc24632d76319193e6eb3e68ffce137b251f57afc4a511fc5dddf630 | 23350 | 4a1a3aae34304cd91c4486bb2d744bbd11ea44505a47b7a25032b1c82d04e48b |
| c | 32150962a1ea0f9fcffe7ed9211f371c74e048687260a0bcffda765aef702f36 | 23389 | e97eb4adf51efbb99084eb221710220da3733ab648b5f1959a570effe59cb8bb |
| freeze | dfdce5d8e8ca985e824193b721f6286085009a9459fd1dff3543772fe30065d4 | 21520 | 072fa7aa39e09e511dc919fc0b847eadb6f785ee40e6d39d72fbc9a87c7c5430 |
| control | 43ded64586e705085c675d0df32bb35607cc300df8fbeba4e57b6ecb24059fad | 23560 | 1068727d7bb9e053cc91539b97407630c3db659a74008ee52295ee415864b14c |

Renderer: epochgraft (SHA ebeca0f6402233d78a40c830b8d6b8b7a6e1dcc04527e7979e77e41fefb11b1b)
Source: epochgraft.zag (SHA afdb8c9afa8f60c0d0f268f4d5ffe80f980d08a1615432930bfd554a708d958c)
Toolchain: ~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 (pinned)

## G4 No-Static Audit

### Variant (a) — copied cycles, Hann OLA
- G4a boundary: -19.12 dB @ 9786, ratio 1.02x [PASS] (not a click; signal slew)
- G4b 50ms crest>20dB: 0 frames [PASS]
- G4c voiced 8-16kHz: -73.46 dB (21 voiced frames) [PASS]
- G4d sub-period: grains are 2*tf (~218 samples), periods ~89-110 [PASS]
- Hum: -29.74 dB @ 300 Hz [NOT CLEAN] (300 Hz present in source at -38.89 dB; amplified by processing)
- Flux: std=1.15644, mean=5.64981
- F0 median: 491.1 Hz
- G1 full re-render: EXACT (0 LSB diff)
- F1.2: byte-identical True, isolated corr 1.0 [PASS]

### Variant (b) — windowed-sinc resampling
- G4a boundary: -18.37 dB @ 7811, ratio 1.02x [PASS]
- G4b 50ms crest>20dB: 0 frames [PASS]
- G4c voiced 8-16kHz: -53.93 dB (21 voiced frames) [PASS]
- G4d sub-period: [PASS]
- Hum: -38.66 dB @ 250 Hz [NOT CLEAN]
- Flux: std=0.65796, mean=5.83341
- F0 median: 492.3 Hz
- G1b sinc spot: 1200 spots, 0 uncovered, 0 bad, maxdiff 0 [PASS]

### Variant (c) — SUTURE butt-splice control
- G4a boundary: 2.45 dB @ 6727, ratio 30.43x [FAIL] (real clicks)
- G4b 50ms crest>20dB: 0 frames [PASS]
- G4c voiced 8-16kHz: -1.27 dB [FAIL] (click HF energy)
- G4d sub-period: [FAIL] (cp=min(tf,dtj); when dtj<tf, grain is sub-period)
- Hum: -24.57 dB @ 50 Hz [NOT CLEAN]
- Flux: std=0.48895
- F0 median: 494.4 Hz
- G1 full re-render: EXACT (0 LSB diff)

### Freeze control (i(j)=i(0))
- G4a: -25.28 dB, ratio 0.43x [PASS]
- G4b: 0 frames [PASS]
- G4c: -72.08 dB [PASS]
- G4d: [PASS]
- Flux: std=0.89198
- F0 median: 495.6 Hz
- G1: EXACT

### LF control (synthetic pulse train)
- HNR: 12.31 dB (leaves HNR box [0.7, 6.7]) [F1.5 PASS]
- Real (fossil) HNR: 11.57 dB; diff 0.74 dB (<3 dB, but box-leave suffices)
- F0 median: 495.4 Hz

## F1 Bar Verdicts

| Bar | (a) | (b) | (c) |
|-----|-----|-----|-----|
| F1.1 unique>=0.5, reuse<=2 | 1.0/1 PASS | 1.0/1 PASS | 1.0/1 PASS |
| F1.2 byte-identical, corr>=0.999 | True/1.0 PASS | N/A | N/A |
| F1.3 F0 within 3% of 493.72 Hz | 0.53% PASS | 0.29% PASS | 0.14% PASS |
| F1.4 not wavetable | FAIL (0.892>=0.578) | FAIL (0.892>=0.329) | N/A |
| G4 all pass | YES | YES | NO |

## Final Verdict
- **(a)**: Best-on-gates. Passes all G4, F1.1, F1.2, F1.3. FAILS F1.4 → KILLED as wavetable.
- **(b)**: Passes all G4, F1.1, F1.3. FAILS F1.4 → KILLED as wavetable.
- **(c)**: Fails G4a/G4c/G4d → KILLED. No repair possible (butt-splice clicks inherent to design).
- **Fork F1**: KILLED per F1.4. Freeze passes all G-bars with flux-std 0.892, which is ≥0.5× the real variants' flux (0.578 for a, 0.329 for b). The epoch_graft method does not produce sufficient spectral variation beyond a static wavetable.
- **No variant staged for ears.** Coordinator stages neutral CLIP_X; none qualified.
