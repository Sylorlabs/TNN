# BLIND TEST-1 Ballot — Package D-ALPHA — Judge 3 (native critic, signal-only)

- **Brief:** 30 s, children playing and laughing: ≥3 distinct child voices, overlapping play, running feet, laughter tumbling into each other.
- **Method:** measurement tool only (`measure_test1.py`), synth-smell fingerprint theory. I cannot hear; this ballot is signal-only.
- **No overrides.** The preregistered S-ranking baseline stands as assigned below. Rationale in §3.

## 1. Per-clip table

| clip | s1 | s2 | s3 | s4 | s5 | S | key A-NATIVE notes | label | confidence | one-line evidence |
|---|---|---|---|---|---|---|---|---|---|---|
| clip_1 | 0.0478 | 0.8947 | 1.0000 | 0.5000* | 0.9514 | **0.6788** | dc 1.9e-08, 0 clips, **0 clicks**, **hiss_ratio 1.4739** (HF louder than mid band — a hiss bed), hf_flatness 0.8456, **0 transients/s** | **synth control** | LOW | Exact loop: s3=1.0 (every distant 1-s chunk pair near-identical), frozen centroid (s5=0.95), stationary texture (s2=0.89) — a looped bed, not a scene. |
| clip_2 | 0.6171 | 0.0000 | 0.3374 | 0.8945 | 0.0000 | **0.3698** | dc 9.5e-06, 0 clips, **7409 clicks**, hiss_ratio 0.4955, hf_flatness 0.8815, **1.43 transients/s** (n=43) | **fork render** | LOW | Strongly periodic envelope (s1=0.62, highest) + symmetric impacts (s4=0.89, 43 of them) — repeated drawn gestures; variable spectrum (s5=0), moderate repetition (s3=0.34). |
| clip_3 | 0.4454 | 0.0000 | 0.0246 | 0.9606 | 0.0000 | **0.2861** | dc 2.2e-06, 0 clips, **9219 clicks**, **hiss_ratio 0.0194** (very dark HF), hf_flatness 0.7877, 0.40 transients/s (n=12) | **real recording** | LOW | Breathing ambience (s2=0), moving resonances (s5=0), near-zero repetition (s3=0.02) — the most alive profile of the three. |

\* s4=0.5 for clip_1 is the tool's default: n_transients=0, so no attack/decay symmetry was measurable. It is a non-measurement, not evidence of medium symmetry.

## 2. Forced ranking by "most likely to be a real field recording"

1. **clip_3** — lowest syntheticity (S=0.2861); ambience breathes (s2=0), resonances move/couple (s5=0), nothing repeats (s3=0.02). The single most alive signal in the battery.
2. **clip_2** — variable spectrum and moving resonances (s2=s5=0) but a strongly periodic envelope (s1=0.62) and symmetric impacts (s4=0.89) are not how messy real play behaves; reads as repeated dreamed gestures.
3. **clip_1** — s3=1.0 (literally every distant 1-s chunk near-identical) is impossible for a real field recording; frozen centroid (s5=0.95) and a stationary hiss bed (hiss_ratio 1.47) seal it. Dead last, by a large margin.

## 3. Overrides

**None.** The baseline stands.

Considered and rejected: clip_2's s1 (0.6171) is the strongest single periodicity in the battery, which could argue for calling it the synth. But clip_1's top-S status is not a one-fingerprint fluke — three fingerprints rank it highest (s2=0.8947, s3=1.0000, s5=0.9514), and s3=1.0 is the single most synthetic measurement in the whole package: an exact loop of content. A real playground cannot repeat 1-s chunks at log-mel cosine > 0.999 across the whole clip; no voice repeats exactly, ever. The evidence for clip_1 = synthetic control is decisive under the theory, and clip_2's gesture-repetition profile (periodic envelope + symmetric impacts, but variable spectrum and low repetition) is exactly the fork-vs-synth middle ground the middle-S label occupies.

## 4. Confidence rationale (preregistered rule, applied literally)

- S gaps: clip_1 − clip_2 = **0.3090**; clip_2 − clip_3 = **0.0837**. Both ≥ 0.05, so HIGH-vs-MEDIUM-vs-LOW turns on fingerprint agreement.
- Fingerprint rank agreement on the top-S clip (clip_1): s2, s3, s5 agree (rank 3/3). s1 dissents (ranks clip_1 1/3). s4 dissents by rank — **caveat:** s4=0.5 is a default from zero detected transients, i.e. a non-measurement, not a measurement of symmetry.
- **Ballot confidence: LOW.** Literal rule: ≥2 fingerprints dissent on clip_1's rank (s1 + s4-by-rank). The genuine dissent is s1; s4 is a non-measurement. If s4 is excluded, the dissent count is 1 and this would read MEDIUM — the evidence is mixed, the rule is what it is, so LOW stands.

## 5. A-NATIVE anomalies (noted, not deciding — per brief, identity is decided on fingerprints)

- clip_1: hiss_ratio 1.4739 — HF band energy exceeds the 0.3–8 kHz band. This is a hiss texture, a direct A-NATIVE violation (no static/hiss), consistent with a synthetic bed, not a field recording.
- clip_2: 7409 clicks in 30 s; clip_3: 9219 clicks in 30 s. For the real-recording candidate (clip_3) that click count is anomalous for clean native field-recording quality — flagged for the record; the click detector may be flagging natural transient grains (hand claps, footfalls), and I did not let it move the identity call.
- clip_3: hiss_ratio 0.0194 — extremely dark high end; a dull mic or heavy lowpass character.
- All clips: clip_count = 0 (no digital clipping anywhere), DC offsets negligible (largest: clip_2 at 9.5e-06).

## 6. DISCLOSURE

- I analyzed **only** the three listed files: `d_alpha/clip_1.wav`, `d_alpha/clip_2.wav`, `d_alpha/clip_3.wav`, via the measurement tool's numeric output plus one arithmetic-verification script of my own.
- I did **not** open anything under `keys/` (or any sealed mapping), opened no other files in the test1 tree, and listened to nothing.
- I recognized no clip — I have never encountered these files and used no prior knowledge of the forks; the only fork knowledge I hold is the generic position label "D-ALPHA" from the task text, which informed no measurement.
- I used no web search and no non-signal information.
- **This ballot is valid** (no disclosure failure).
