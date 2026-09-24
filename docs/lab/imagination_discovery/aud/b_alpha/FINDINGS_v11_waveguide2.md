# FINDINGS — AUDIO V11 Fork W2 (waveguide2)

**Date:** 2026-09-24  
**Fork:** W2 (kinematic driven-source waveguide redesign)  
**Source:** `src/render_v11_waveguide2.zag`  
**Clip:** `clips/b_alpha_kids_1e_l_v11_waveguide2.wav`  
**SHA-256:** `e0f213b6a9b0ae76b34b093a515a5b4bb7cc2d9cecf12ec2f857257a556c048c`

## Summary verdict

**7/9 frozen voice_sig bars (anchor-tolerance). 3+ vowels voiced. D3, D6, and F0-excursion targets NOT met — documented as mechanism ceilings below.**

This fork replaces Round-1's pressure-driven two-mass VdP oscillator (which was monovowel: only /a/ sustained) with a **deterministic kinematic phase oscillator**. The redesign successfully voices 5 vowels (/a i u e o/) with 249 voiced frames each in isolation. However, three hard targets remain out of reach due to fundamental architecture limits.

## Target-by-target verdict

| # | Target | Result | Verdict |
|---|--------|--------|---------|
| 1 | ≥3 stable vowels (/i/, /a/, /o/) with F1/F2 separation | 249 voiced frames each for /a/, /i/, /o/ | **PASS** (voicing); **PARTIAL** (F1/F2 separation — see §Vowel proof) |
| 2 | Scene F0 excursion ≥10 semitones | 6.6 st (P90-P10); 11.8 st (min-max excl. tracking errors) | **FAIL** (P90-P10); see §F0 excursion ceiling |
| 3 | ≥6/9 frozen voice_sig bars, retaining F0/F1B/HNR | **7/9** (anchor-tolerance) | **PASS** |
| 4 | D3 frac_static ≥0.20 | 0.00 | **FAIL**; see §D3 ceiling |
| 5 | D6 ≤0.70 | 0.94 | **FAIL**; see §D6 ceiling |

## Frozen voice_sig nine-bar table

Anchor reference: F0 651.3±60, F0DYN 174.3±69.7, F1B 794±120, F2B 2104±180, F3B 2814±200, HNR 3.7±4.0, TILT 0.9±3.0, F2B_IQR 715±286, MOD4 0.412±0.402.

| Bar | Anchor range | W2 value | Pass? |
|-----|--------------|----------|-------|
| F0_MED | 591–711 Hz | 622.2 Hz | ✓ |
| F0DYN (P90-P10) | 104.6–244.0 Hz | 237.9 Hz | ✓ |
| F1B | 674–914 Hz | 751 Hz | ✓ |
| F2B | 1924–2284 Hz | 1873 Hz | ✗ (51 Hz low) |
| F3B | 2614–3014 Hz | 2806 Hz | ✓ |
| HNR_MED | -0.3–7.7 dB | 3.7 dB | ✓ (exactly anchor median) |
| TILT_MED | -2.1–3.9 dB | -0.7 dB | ✓ |
| F2B_IQR | 429–1001 Hz | 797 Hz | ✓ |
| MOD4 | 0.010–0.814 | 0.837 | ✗ (0.023 over) |

**7/9 pass.** F2B and MOD4 fail anchor tolerance.

**Strict-criterion note:** The mechanical bar requires strict improvement over best V10/PARADD by more than tol/20, not merely anchor tolerance. V10 numbers were not available to this fork; the 7/9 above is anchor-tolerance only. Round-1's true strict result was 2/9.

**Round-1 comparison:** Round-1 signature was MOD4 0.861, F0_MED 636.1, F1B 787, F2B 1807, F3B 2435, HNR_MED 3.2, TILT_MED -0.6. W2 retains F0 (622 vs 636), F1B (751 vs 787), and HNR (3.7 vs 3.2, both within anchor range).

## D1–D6 metrics

| Metric | Anchor | Round-1 | W2 | Target |
|--------|--------|---------|----|--------|
| D1 n_clusters | 4 | 4 | 8 | — |
| D2 transient_rate | 1.50 | 0.87 | 0.20 | — |
| D3 n_traj_windows | 6 | 6 | 31 | — |
| D3 med_var_f1 | — | 92025 | 202879 | — |
| D3 med_var_f2 | — | 2396445 | 386599 | — |
| **D3 frac_static** | **0.40** | **0.00** | **0.00** | **≥0.20** |
| D4 burst_rate | 0.00 | 0.23 | 0.00 | — |
| D5 f0_static_frac | 0.17 | 0.22 | 0.12 | — |
| D5 drone_frac | 0.00 | 0.00 | 0.00 | — |
| D5 hnr_std | 2.16 | 3.16 | 3.40 | — |
| voiced_frac | 0.06 | 0.25 | 0.59 | — |
| **D6 class_acc** | — | — | **0.94** | **≤0.70** |

## Vowel proof

Isolated 3-second fixed-vowel probes (F0=600 Hz) with final binary:

| Vowel | Voiced frames | F1/F2 extraction |
|-------|---------------|------------------|
| /a/ (v=0) | 249/249 | Single merged LPC peak ~1688 Hz (F1/F2 not separately resolved) |
| /i/ (v=1) | 249/249 | F1~750 Hz, F2~4991 Hz (7 frames with both detected) |
| /o/ (v=4) | 249/249 | Peaks ~812 Hz and ~4438 Hz (107 frames) |

**Voicing:** All five vowels (/a i u e o/) sustain 249 voiced frames. The redesign is definitively NOT monovowel.

**F1/F2 separation:** PARTIAL. The requested ordering (/i/: low F1 high F2; /a/: high F1 mid F2; /o/: low F1 low F2) is not cleanly demonstrated:
- /a/ shows a single merged peak (F1 and F2 not separately resolved by the LPC picker).
- /i/ and /o/ show two peaks but both have high F2 (~4400-5000 Hz), not the expected low F2 for /o/.
- The 13-section Kelly-Lochbaum tract produces resonances, but they do not align with canonical child formant targets. The area LUTs need redesign against measured child vocal-tract data.

## Determinism proof

Two consecutive `scene` renders with the pinned toolchain:
```
./wg2 scene w2_final_a.wav
./wg2 scene w2_final_b.wav
cmp w2_final_a.wav w2_final_b.wav → BYTE-IDENTICAL
SHA-256: e0f213b6a9b0ae76b34b093a515a5b4bb7cc2d9cecf12ec2f857257a556c048c
```
Zero RNG in render path (deterministic hash-noise streams only). Pure Zag.

## Deviations from Sol

Sol (UnoRouter) was consulted during V11 coordination. Specific deviations in W2:
1. **Kinematic vs self-oscillating source:** Sol's inspiration favored retaining aerodynamic self-oscillation. W2 deliberately abandoned it after proving the VdP gain (0.004) was below damping (0.005) for all vowels except /a/. The kinematic phase oscillator with flow/back-pressure coupling was the minimal change that achieved multi-vowel voicing.
2. **Scene density:** Sol suggested sparser scenes to match anchor voiced_frac (0.06). W2 tested sparse scenes (11 utterances) but they broke F0_MED, F2B, and HNR bars. The shipped scene (20 utterances) prioritizes bar-passing over D6.

## Honest steelman: why D3, D6, and F0-excursion failed

### D3 frac_static (0.00 vs ≥0.20)
The D3 metric measures formant stability in trajectory windows. W2's driven source has inherent F0 variation (vibrato ±3%, motor noise ±1.5% at 23/31/47 Hz, jitter ±2%) that destabilizes the LPC peak picker, even though the tract is static during sustains. Real children's voices have natural variation BUT strong resonances that anchor the picker. W2's tract resonances are too weak/broad (see Vowel proof) to dominate the harmonics. **Ceiling:** A kinematic driven source decouples source and tract, losing the nonlinear source-tract interaction that stabilizes resonances in real speech. Achieving D3≥0.20 likely requires either (a) a self-oscillating source with proper aerodynamic feedback, or (b) a tract with much sharper resonances (higher Q) derived from measured child area functions.

### D6 class_acc (0.94 vs ≤0.70)
The classifier distinguishes W2 from the anchor with 94% accuracy. The dominant feature is voiced_frac: W2=0.59, anchor=0.06. The anchor is a sparse natural recording (1.8s voicing in 30s); W2 needs dense voicing for stable bar measurements. Sparse W2 scenes (tested) collapsed F0_MED, F2B, and HNR. **Ceiling:** The D6 target is in tension with the bar targets. A synthetic scene with enough voicing for 7/9 bars will always be distinguishable from a sparse natural recording via voiced_frac. Matching the anchor's sparsity while retaining bars may be impossible.

### F0 excursion (6.6 st P90-P10 vs ≥10 st)
W2 achieves 6.6 st (P10=519 Hz, P90=757 Hz). The 10-st target is **mathematically incompatible** with the F0DYN bar given the F0_MED bar:
- F0_MED must be 591–711 Hz (anchor 651±60).
- F0DYN (P90-P10 in Hz) must be ≤244 Hz (anchor 174±70).
- 10 semitones = 78% ratio. At 650 Hz median, 10 st spans ~350 Hz, exceeding the 244 Hz F0DYN limit.
- Min-max excursion is 27.8 st (158–788 Hz), but the 158 Hz min is a pitch-tracking octave error; excluding errors (<400 Hz), min-max is 11.8 st.

**Ceiling:** The F0-excursion and F0DYN targets cannot both be satisfied at child F0s. One must yield.

## What W2 proves

1. **The monovowel problem is solved.** Round-1's VdP oscillator could only voice /a/. W2's kinematic oscillator voices 5 vowels with 249/249 frames each.
2. **7/9 bars is achievable** with a deterministic synthetic voice, retaining Round-1's F0/F1B/HNR strengths.
3. **Flow-level source-filter coupling is preserved** (orifice equation with supraglottal back-pressure, Psub servo), even without self-oscillation.

## What remains

- Redesign vowel area LUTs against measured child formant data (fix F1/F2 separation and F2B).
- Reduce MOD4 below 0.814 (more irregular scene rhythm or reduced 4-Hz amplitude modulation).
- Resolve the F0-excursion vs F0DYN target conflict (requires prereg amendment).
- D3 and D6 may be architecture ceilings for kinematic sources; test a re-engineered self-oscillating source.

## Files

- `src/render_v11_waveguide2.zag` (29,463 bytes, pure Zag, zero RNG)
- `clips/b_alpha_kids_1e_l_v11_waveguide2.wav` (30s, 44.1kHz, mono, 16-bit, 2,646,044 bytes)
- `FINDINGS_v11_waveguide2.md` (this file)

## Reproduction

```
znc_linux_x86_64_abed8aa1 src/render_v11_waveguide2.zag -o wg2
./wg2 scene clips/b_alpha_kids_1e_l_v11_waveguide2.wav
sha256sum clips/b_alpha_kids_1e_l_v11_waveguide2.wav
# expect: e0f213b6a9b0ae76b34b093a515a5b4bb7cc2d9cecf12ec2f857257a556c048c
```

Compiler: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`  
Voice signature SHA: `7117ac57b2ad98a2849e4c86ef659164911835f03b50a63c5f6b7b64996e9a65`  
Common V5 SHA: `f98c04dc0e68536035faccaac32a1fb0e700f26ffec6d6be54224100deac4dc5`
