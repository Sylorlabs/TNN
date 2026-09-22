# BLIND TEST-1 — judge ballot: b_gamma_judge1 (native critic, blind)

**Package:** B-GAMMA · **Judge role:** blind native critic (no listening; signal analysis only)
**Brief judged:** 30 s of children playing and laughing — ≥3 distinct child voices, overlapping play, running feet, laughter tumbling into each other. One clip real playground field recording, one synth control, one fork render (monster fork).
**Measurement source:** `measure_test1.py` run 2026-09-22, exit 0, 3/3 clips 30.0 s.

## 1. Per-clip fingerprints, S, A-NATIVE, labels

| clip | s1 (envelope periodicity) | s2 (stationarity) | s3 (loop score) | s4 (transient symmetry) | s5 (formant stability) | S (syntheticity) | key A-NATIVE notes | label | confidence | one-line evidence |
|---|---|---|---|---|---|---|---|---|---|---|
| judge_A | 0.6495 | 0.0000 | 0.1010 | 0.9344 | 0.0000 | **0.3370** | dc 3.0e-4, hiss 0.485, hf_flat 0.836, clips 0, clicks **6681** (!), transients 1.7/s (n=51) | **real recording** | LOW | lowest S; s2=0 and s5=0 = ambience breathes and resonances move; many messy impacts |
| judge_B | 0.8468 | 0.4622 | 0.0074 | 0.8274 | 0.4018 | **0.5091** | dc 5.1e-5, hiss 0.035, hf_flat 0.785, clips 0, clicks 2397, transients 0.1/s (n=3) | **synth control** | LOW | highest S; s1/s2/s5 all highest — periodic rhythm, stationary bed, fixed formants; only 3 transients in 30 s |
| judge_C | 0.8169 | 0.0000 | 0.0000 | 0.8512 | 0.3962 | **0.4129** | dc 7.2e-5, hiss 0.164, hf_flat 0.382, clips 0, clicks 1579, transients 0.5/s (n=15) | **fork render** | LOW | middle S; periodic envelope (attempting play rhythms) but breathing spectrum and zero exact repetition |

S gaps: B−C = 0.0962; C−A = 0.0759 (both ≥0.05, both <0.10).
Top-S clip B fingerprint ranks: s1 highest ✓, s2 highest ✓, s3 not highest (A=0.101) ✗, s4 not highest (A=0.9344) ✗, s5 highest ✓ → **2 dissents → LOW confidence** per preregistered rule.

A-NATIVE anomalies (quality notes only, not used for identity): judge_A has a very high click_count (6681) and the highest hiss_ratio (0.485) — digital clicks present; none of the three clips show hard clipping (clip_count 0 everywhere); judge_B is the cleanest on hiss/clicks, judge_C sits in between.

## 2. Forced ranking by "most likely to be a real field recording"

1. **judge_A** (most likely real)
2. **judge_C**
3. **judge_B** (least likely real)

## 3. Overrides

**None.** The baseline stands: highest S → synth control (B), lowest S → real recording (A), middle → fork render (C). The dissenting fingerprints (A leads on s3 and s4) are noted but do not form a coherent override case: B's top-S position is driven by s1, s2, and s5, which together paint the textbook synth-smell picture — a rhythmically periodic (0.85), stationary (0.46), fixed-formant (0.40) bed with essentially no distinct transient events (3 in 30 s). A's lowest-S position is driven by the reality-side fingerprints: s2=0 (spectral flux and RMS envelope vary maximally — the ambience breathes) and s5=0 (resonances move/collide), with 51 impacts at 1.7/s consistent with running feet and play collisions. A's elevated s3 (0.101, highest) and s4 (0.9344, highest) are the two reasons confidence is LOW rather than higher; they are consistent with repeated playground shouts/cries and symmetric impact transients, but the gap rule and dissent count require the LOW rating.

## 4. DISCLOSURE

- I opened **only** the three listed clip files (`judge_A.wav`, `judge_B.wav`, `judge_C.wav`) via the assigned measurement script. I did **not** open `ORDER_SEALED.md`, `clip_real.wav`, `clip_synth.wav`, or `clip_method.wav`.
- I did not recognize any clip (I have no audio access to any of these sources and no prior contact with these files).
- I used no web search and no non-signal information. My decision rests solely on the fingerprint numbers plus the preregistered scoring rules.
- **My ballot is NOT void.**
