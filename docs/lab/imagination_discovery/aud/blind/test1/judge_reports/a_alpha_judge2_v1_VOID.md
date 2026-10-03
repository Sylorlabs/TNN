# BLIND TEST-1 Judge Ballot — Package A-ALPHA

**Judge 2** — blind native critic, signal-only analysis.
Tool: `measure_test1.py` run once on the four listed files (30.0 s each, exit 0).
Brief (all clips): 30 s of children playing and laughing — ≥3 distinct child voices,
overlapping play, running feet, laughter tumbling into each other.

## 1. Per-clip table

| clip | s1 periodicity | s2 stationarity | s3 loop/repeat | s4 transient symmetry | s5 formant stability | S | key A-NATIVE notes | identity | confidence | one-line evidence |
|---|---|---|---|---|---|---|---|---|---|---|
| `clip_1.wav` | 0.6264 | 0.2975 | **0.0123** | 0.8216 | 0.0000 | 0.3516 | dc≈1.6e-7; clip_count 0; clicks 1978; hiss_ratio 0.033 (clean); hf_flatness 0.17 (peaky); 14 transients (0.47/s) | **REAL** (forced choice) | MEDIUM | s3≈0.01: no near-exact repetition; zero clipped samples; natural HF — the only clip with no loop signature. |
| `clip_2.wav` | 0.5796 | 0.0000 | **0.5025** | 0.7719 | 0.0000 | 0.3708 | dc≈1.6e-5; clip_count **723**; clicks **10414**; hiss_ratio 0.033; hf_flatness 0.90 (flat); 34 transients (1.13/s) | **FORK RENDER** (forced choice) | MEDIUM | s3=0.50: over half of distant 1 s chunk pairs near-identical — looped/duplicated material; 723 clipped samples + 10,414 clicks = digital-render signature. |
| `calib_real.wav` | 0.0584 | 0.8960 | **1.0000** | 0.5000 | 0.9543 | **0.6817** | dc≈2.1e-8; clip_count 0; clicks 0; hiss_ratio **1.484** (SEVERE — A-NATIVE violation); hf_flatness 0.85; **0 transients in 30 s** | LABELED real anchor ⚠ | N/A (labeled) | Anchor compromised: s3=1.0 (perfect loop), s2=0.90 (stationary bed), static formants, zero transients, hiss 1.48 — reads as a looped ambience texture, not children playing. Its S **exceeds** the synth anchor's. |
| `calib_synth.wav` | 0.8744 | 0.0000 | 0.0714 | 0.7759 | 0.6261 | 0.4696 | dc≈5.6e-6; clip_count 0; clicks 5790; hiss_ratio 0.317; hf_flatness 0.80; 29 transients (0.97/s) | LABELED synth anchor | N/A (labeled) | Rhythmic (s1=0.87), symmetric transients, moderately stable formants — eventful but periodic; scores LESS synthetic than the labeled-real anchor. |

All five fingerprints are synth-smell metrics (higher = more synth-like); S = mean(s1..s5).
Arithmetic verified: e.g. clip_1 (0.6264+0.2975+0.0123+0.8216+0.0)/5 = 0.3516 ✓.

## 2. Forced choice

**Mechanical anchor rule** (nearer to calib_real S = 0.6817 is the real recording):
- |clip_1 S − 0.6817| = |0.3516 − 0.6817| = **0.3301**
- |clip_2 S − 0.6817| = |0.3708 − 0.6817| = **0.3109**
- Mechanical verdict: **clip_2 = real**. Margin 0.0192 → **LOW** confidence per prereg (< 0.05).

Note: both unlabeled clips are actually nearer the *synth* anchor (|clip_1−0.4696|=0.1180,
|clip_2−0.4696|=0.0988) — the calibration bracket does not behave as designed.

**Override (prereg escape clause — individual fingerprints contradict the anchor verdict):**

1. **The anchors are inverted.** The labeled-real anchor's composite S (0.6817) *exceeds* the
   labeled-synth anchor's (0.4696). The prereg's anchor rule was written on the assumption
   calib_real S < calib_synth S; that assumption fails, so S-proximity cannot be trusted.
2. **Decisive fingerprint: s3.** The theory's headline reality diagnostic ("no voice repeats
   exactly"): clip_1 = 0.0123 vs clip_2 = 0.5025, a gap of ≈0.49 — the largest inter-clip
   fingerprint difference by far. Over half of clip_2's distant 1 s chunk pairs are
   near-identical: looped or copy-pasted material. clip_1 shows no loop signature.
3. **Corroborating digital evidence.** clip_2: 723 clipped samples, 10,414 detected clicks,
   hf_flatness 0.90 (flat, noise-like HF). clip_1: 0 clips, 1,978 clicks, hf_flatness 0.17
   (peaky, event-like). Both comply with the A-NATIVE no-hiss law (hiss ≈ 0.033 each);
   the labeled-real anchor grossly violates it (hiss 1.48).
4. **Explaining clip_1's weak spots.** clip_1's s1 (0.626, periodic envelope) is explicable by
   the brief's *running feet* — periodic impact rhythm is genuinely rhythmic. Its s4 (0.822,
   symmetric transients) is high but s4 is weakly discriminating here (clip_2 = 0.772, synth
   anchor = 0.776 — all three nearly equal).

**VERDICT: clip_1 = real recording; clip_2 = fork render.**
The mechanical anchor verdict (clip_2 = real) carried LOW confidence; per prereg I drop it
a level — it is void. My independent fingerprint verdict stands at **MEDIUM** confidence:
grounded in the decisive s3 gap and corroborated by the digital-artifact disparity, but
capped because the compromised anchors remove my calibration reference.

## 3. Forced ranking — most → least likely to be a real field recording

1. **clip_1.wav** — no loop signature (s3≈0.01), moving formants (s5=0), zero clipped
   samples, natural HF profile, A-NATIVE-clean.
2. **clip_2.wav** — looped material (s3=0.50), digital-render artifacts (723 clips,
   10,414 clicks); eventful but synthetic-leaning.
3. **calib_synth.wav** (labeled synth control) — periodic rhythm (s1=0.87), symmetric
   transients, rhythmic synth-control profile.
4. **calib_real.wav** (labeled real anchor) — ranked last *on signal*: perfect loop
   (s3=1.0), near-stationary bed (s2=0.90), static formants (s5=0.95), zero transients in
   30 s, severe hiss (1.48). Inconsistent with the children-playing brief; consistent with
   a looped ambience texture. **The anchor should be investigated (mislabeled/misfiled)
   before this package's scores are used.**

## 4. Disclosure

I analyzed **only** the four listed WAV files, via the single specified `measure_test1.py`
run. I did not open anything under `keys/`, did not open any other judge's ballot, did not
web-search, recognized none of the clips, and used no non-signal information.
**My ballot is not void.**
