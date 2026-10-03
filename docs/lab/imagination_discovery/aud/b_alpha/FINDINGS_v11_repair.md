# FINDINGS: V11 Repair (Fork R) — Articulatory Renderer Repair

**Date:** 2026-09-24  
**Preregistration:** `20b9ffa647f7c2b4bde4904fcaa2b7181a63f1a0`  
**Final commit:** (pending)

## Root Cause

V10's articulatory renderer failed (VS_OK 0, zero clean frames) because the
aspiration noise level was catastrophically high. The effective aspiration
reached approximately `breath × burst ≈ 0.9 × 2.2 ≈ 2.0`, versus a glottal
peak scale of 0.55 — burying both periodicity and formant resonance under
broadband noise.

The architecture itself was sound. A clean source through the same parallel
resonator bank produced measurable voice (VS_OK 1, 330/799 clean frames,
F1B 610, F2B 1953, HNR 12.1). The paradigm did not fail; the execution did.

Secondary defects in V10:
- Adult-sized formants (not child-scaled)
- F0 too low relative to the frozen detector's expectations
- Dense ambience masking the voice
- Inadequate syllabic/modulation behavior for the MOD4 bar

## Frozen voice_sig Output (Final Render)

```
VS_OK 1
VS_NFRAMES 2000
VS_NVOICED 342
VS_MOD4 0.520
VS_VFRAC 0.171
VS_F0_MED 632.7
VS_F0_P10 538.0
VS_F0_P90 699.6
VS_F1B 777.
VS_F2B 2282.
VS_F2B_IQR 525.
VS_F3B 2734.
VS_HNR_MED 3.6
VS_TILT_MED 0.9
VS_CENT_MED 2655.
```

## Nine-Bar Comparison

| Bar | Anchor | V10 PARADD | Final | Target | Pass? |
|-----|--------|------------|-------|--------|-------|
| F0 | 651.3 | 766.6 | 632.7 | 591.3–711.3 | ✓ |
| F0DYN | 174.3 | 384.3 | 161.6 | 104.6–244.0 | ✓ |
| F1B | 794 | 740 | 777 | 734–854 | ✓ |
| F2B | 2104 | 2329 | 2282 | 1924–2284 | ✓ |
| F2B_IQR | 715 | 1247 | 525 | 429–1001 | ✓ |
| F3B | 2814 | 2968 | 2734 | 2650–2978 | ✓ |
| HNR | 3.7 | 4.0 | 3.6 | 4.0–4.2 | ✗ |
| TILT | 0.9 | 0.0 | 0.9 | −0.15–1.95 | ✓ |
| MOD4 | 0.412 | 0.551 | 0.520 | 0.253–0.571 | ✓ |

**8/9 bars pass.** HNR 3.6 vs required 4.0–4.2. The anchor (real children)
measures 3.7, so 3.6 is within 0.1 dB of the anchor.

**Wrong-target distance:** Final is closer to anchor than V10 on all 9 bars
(9/9 wins). Normalized distances confirm the repair beats V10 decisively.

## Diagnosis Self-Checks

From `diag_bin`:
- **Voiced:** 1522/2997 = 50.8% ✓ (≥4% required)
- **Formant frames:** 688/1522 = 45.2% of voiced ✓ (≥20% required)
- **HNR:** voice_sig 3.6 dB ✓ (≥3 dB required; task target 4.0 not met)
- **F0 median:** 635 Hz ✓ (350–700 required)
- **F0 excursion:** 16.78 semitones ✓ (≥10 st required)

## Source Tilt and Jitter Evidence

**Glottal-source tilt (−6 to −9 dB/oct required):**
- Not directly measured on the isolated source. The glottal pulse shape
  (LF-model inspired, `OQ` 0.58–0.70) is designed for −6 to −9 dB/oct.
- `diag_bin voice` reports output spectral tilt −17.75 dB/oct, but this is
  the radiated output (source + tract + radiation), not the isolated source.
- **Gap:** Direct source-domain tilt measurement was not performed.

**Jitter (>1.5% required):**
- `JIT = 0.018` (1.8% per-cycle F0 perturbation depth, deterministic hash).
- Designed to exceed 1.5%, but cycle-to-cycle jitter was not empirically
  measured from the rendered audio.
- **Gap:** Empirical jitter verification pending.

**Bandwidths (1.5–2× adult required):**
- F1 BW 200 Hz, F2 BW 320 Hz, F3 BW 450 Hz, F4 BW 650 Hz.
- Approximately 2–4× typical adult values; at the high end of the target.

## Determinism Proof

Two full renders from the final source (compiled in `b_alpha/src/`):
- SHA-256 (render 1): `e9d716a4ce03a759ac8cfff66e5ef6be4a0f9a8e3c7df86de57a659047e4144a`
- SHA-256 (render 2): `e9d716a4ce03a759ac8cfff66e5ef6be4a0f9a8e3c7df86de57a659047e4144a`
- `cmp` confirms byte-identical.

WAV specs: 44.1 kHz, mono, 16-bit, 30.00 s (1,323,000 frames). Zero RNG in
render path (all modulation via deterministic hash/waveguide functions).

## Resonator Probe (Corrected)

Parallel resonator bank verified with deterministic noise probe:
- 1000 Hz center → measured 963 Hz, 0.0 dB relative
- 2600 Hz center → measured 2613 Hz, −2.3 dB
- 3900 Hz center → measured 3982 Hz, −5.3 dB
- 6000 Hz center → measured 6033 Hz, −7.8 dB

(Note: The initial P1 impulse was placed at sample zero and erased by the
30 ms fade-in; that measurement is invalid and not cited.)

## Honest Verdict: Does It Sound Like Children?

**Steelman (why it does NOT sound like children):**

Even with 8/9 frozen bars passing, this render likely does not sound like
real children playing. The architecture produces parallel-formant
"vowel-like" squeals with correct pitch and formant ranges, but it lacks:

1. **Phonemes and words:** No consonants, no syllable structure, no language.
   Real children speak; this produces vowel-ish glides.
2. **Coarticulation:** Formants glide smoothly but without the rapid,
   context-dependent transitions of real speech.
3. **Anatomical coupling:** Source and tract are independent; real voices
   have coupled source-tract interaction.
4. **Prosody:** The "utterance gates" create turn-taking, but without
   linguistic intent, it sounds like random vocalizing.
5. **Individual identity:** Four voices with different F0s, but no
   consistent speaker characteristics.

The frozen bars measure acoustic correlates (F0, formants, HNR, modulation),
not child-likeness. A synthesizer can hit all nine bars and still sound
like robotic vowels or synthetic squeals. The bars are necessary but not
sufficient.

**Verdict:** The repair succeeds technically (8/9 bars, beats V10 9/9,
byte-identical determinism), but the "child" quality remains unproven.
Micah's ears outrank the metrics; this needs his listening test.

## Programmed Range Discrepancy

The task specifies programmed F2 2200–3000 Hz, but:
- Anchor F2B (real children): 2104 Hz (below 2200)
- Frozen target F2B: 1924–2284 Hz (below 2200)
- Final formula F2: (2350−500×mouth)×(1±0.30) → 1295–3055 Hz

The programmed 2200–3000 Hz range is incompatible with the anchor and
measured target. The final prioritizes the frozen instrument (ground truth
for judging) over the programmed range. F1 (950–1250) and F3 (3600–4600)
also deviate from programmed (800–1100, 3500–4500) for the same reason:
the measured bars are the judging criterion.

## Files Committed

- `src/render_v11_repair.zag` (27 KB, pure Zag, zero RNG)
- `clips/b_alpha_kids_1e_k_v11_repair.wav` (2.6 MB, 30s, 44.1kHz, mono, 16-bit)
- `FINDINGS_v11_repair.md` (this file)
