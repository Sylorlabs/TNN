# BLIND TEST-1 Ballot — package B-BETA, Judge 2 (native critic)

Blindness: I opened and measured ONLY the three listed blind clips. I did not open
KEY.sealed.txt, real_calib_30s.wav, or any other file in the directory. I have never
heard any of these clips and recognize none of them. No web search, no prior fork
knowledge was used — signal only.

## 1. Per-clip results

| clip | s1 (periodicity) | s2 (stationarity) | s3 (looping) | s4 (symmetry) | s5 (fixed ring) | S (syntheticity) | A-NATIVE notes | label | confidence | one-line evidence |
|---|---|---|---|---|---|---|---|---|---|---|
| blind_A | 0.7002 | 0.0000 | 0.0000 | 0.9206 | 0.2892 | **0.3820** | dc≈3.1e-5, clips 0, clicks 1297 (lowest), hiss 0.055, hf_flatness 0.474 (least flat), transients 1.0/s | fork render | LOW | lowest s1 of the three, zero exact repetition, moving formants — messy but assembled |
| blind_B | 0.7403 | 0.0000 | 0.0567 | 0.9148 | 0.0000 | **0.3424** | dc≈3.5e-5, clips 0, clicks 2708 (highest), hiss 0.064, hf_flatness 0.833, transients 0.8/s | real recording | LOW | lowest S; s2=0 and s5=0 (breathing ambience, moving resonances) |
| blind_C | 0.8468 | 0.4622 | 0.0074 | 0.8274 | 0.4018 | **0.5091** | dc≈5.1e-5, clips 0, clicks 2397, hiss 0.035 (lowest), transients 0.1/s (only 3 events in 30 s — event-starved) | synth control | LOW | only clip with nonzero stationarity + highest periodicity; 3 transients in 30 s of "children playing" is not a playground |

Preregistered baseline (highest S → synth, middle → fork, lowest → real) yields:
C = synth control, A = fork render, B = real recording.

## 2. Forced ranking by "most likely to be a real field recording"

1. **blind_B** (S = 0.3424 — least synth-like on the index)
2. **blind_A** (S = 0.3820 — middle; assembled from real captures, expected to be second-most real)
3. **blind_C** (S = 0.5091 — the synth tell is clear: a steady bed with almost no discrete events)

## 3. Overrides

**None. Baseline stands.** C's top-S rank is carried by three of five fingerprints —
highest envelope periodicity (s1 = 0.8468), the only nonzero stationarity
(s2 = 0.4622 vs 0.0000 for both A and B — exactly the "filtered-noise bed" signature
the theory predicts for a synth), and highest formant stability (s5 = 0.4018) —
plus the anomaly that a 30 s "children playing" clip contains only 3 transients
(0.1/s vs 1.0/s and 0.8/s), consistent with a stationary texture and nothing else.
There is no cited-fingerprint case for promoting A or B to the synth label:
B scores lowest on s2, s3 (low), s5 (0.0000), and A on s1, s3 (0.0000), s5.
The A↔B fork-vs-real assignment follows the frozen baseline mechanically.

## 4. Confidence rationale

Both S gaps: C−A = 0.1271, A−B = 0.0396. The A−B gap < 0.05 forces LOW per the
frozen rule ("LOW if any gap < 0.05"). Additionally two fingerprints (s3, s4) do not
rank C top, meeting the "≥2 fingerprints dissent" LOW criterion as well. All three
labels are therefore reported LOW. The single strongest leg of the ballot is C =
synth control (C−A gap ≥ 0.10 and the decisive s2 signature); the fork-vs-real
split between A and B is the weak leg.

## 5. DISCLOSURE

I opened ONLY the three listed clips (blind_A/B/C.wav) via the measurement script
and read its numeric output. I did NOT open KEY.sealed.txt, real_calib_30s.wav, or
anything else in that directory. I recognized none of the clips. I used no
non-signal information (no web, no fork knowledge, no prior exposure). Ballot is
valid on my side.
