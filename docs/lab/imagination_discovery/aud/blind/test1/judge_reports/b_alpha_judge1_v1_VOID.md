# BLIND TEST-1 — Package B-ALPHA — Judge 1 (native critic)

Ballot for: children playing + laughing brief (30 s, ≥3 child voices, overlapping play, running feet, laughter tumbling).
Method: signal-only analysis via `measure_test1.py`. Judge is a non-hearing native critic; no other material was consulted.

## 1. Per-clip results

| clip | s1 (periodicity) | s2 (stationarity) | s3 (loop) | s4 (symmetry) | s5 (fixed ring) | S | A-NATIVE notes | label | confidence | one-line evidence |
|---|---|---|---|---|---|---|---|---|---|---|
| clip_1.wav | 0.8744 | 0.0000 | 0.0714 | 0.7759 | 0.6261 | **0.4696** | dc≈5.6e-06, clip 0, **click 5790**, hiss 0.317, hf_flat 0.796, 29 transients (0.97/s) | **fork render** | MEDIUM | Middle S; near-exact loop low (s3=0.07, no verbatim repeats), strong envelope periodicity (s1=0.87) with nonstationary texture (s2=0) — rhythmic event assembly, not a filtered-noise bed; very high click count consistent with event-grain boundaries |
| clip_2.wav | 0.6929 | 0.0000 | 0.0000 | 0.7231 | 0.3387 | **0.3509** | dc≈3.9e-07, clip 0, click 872, hiss 0.050, hf_flat 0.559, 4 transients (0.13/s) | **real recording** | MEDIUM | Lowest S; s3=0 (nothing repeats exactly), s5=0.34 (resonances move), s2=0 (flux CV 1.73 — ambience breathes), natural HF rolloff (hiss 0.05, flatness 0.56) |
| clip_3.wav | 0.7084 | 0.7871 | 0.9212 | 0.9868 | 0.9289 | **0.8665** | dc≈3.3e-08, clip 0, click 0, **hiss 1.464**, hf_flat 0.844, 1 transient (0.03/s) | **synth control** | MEDIUM | Highest S by a wide margin; full synth signature — stationary bed (s2=0.79), near-exact repetition (s3=0.92), symmetric transient (s4=0.99), static formants (s5=0.93), high-band-dominant flat hiss (1.46), only 1 detected transient in 30 s |

S gaps: clip_3 − clip_1 = 0.3969; clip_1 − clip_2 = 0.1187 (both ≥ 0.10).

## 2. Forced ranking by "most likely to be a real field recording"

1. **clip_2.wav** (S = 0.3509)
2. **clip_1.wav** (S = 0.4696)
3. **clip_3.wav** (S = 0.8665)

## 3. Overrides

**None.** The preregistered baseline stands: clip_3 → synth control, clip_2 → real recording, clip_1 → fork render.

Notes on why no override was warranted despite dissent:
- The single dissenting fingerprint is **s1** (envelope periodicity), where clip_1 (0.8744) outranks clip_3 (0.7084). I do not read this as exonerating clip_3: its other four fingerprints are decisive (s2/s3/s4/s5 all rank clip_3 top by large margins, and its A-NATIVE profile is the classic filtered-noise bed — flat, high-band-dominant hiss, zero clicks, one transient in 30 s). The s1 dissent is instead read as evidence *about* clip_1: a fork render built from assembled events can impose a regular placement rhythm (high s1) while still being nonstationary (s2=0) and repetition-free at the 1 s chunk level (s3=0.07). That profile matches the fork-render hypothesis for the middle clip, which is already what the baseline assigns. No cited evidence justified moving any label.

## 4. Confidence rationale

Per the frozen rule: both S gaps ≥ 0.10, but one fingerprint (s1) dissents on the top-S clip's rank → **MEDIUM** confidence for all three labels. Without the s1 dissent the synth-control call on clip_3 would be HIGH; the real-recording call on clip_2 rests on s3=0, s5=0.34, and natural HF rolloff, and the fork call on clip_1 rests on middle-S plus rhythmic-but-nonstationary structure.

## 5. DISCLOSURE

- I opened **only** the three listed files: `clip_1.wav`, `clip_2.wav`, `clip_3.wav` under `packages/b_alpha/`. Nothing under `keys/` (or anywhere else in the test tree) was opened.
- I have never heard or encountered any of these clips; they were analyzed as raw signal only (no playback, no prior knowledge of the forks, no web search, no external references).
- No non-signal information was used. Judgments rest solely on the measurement tool's numbers and the published synth-smell fingerprint theory.
- This ballot is **not void**.
