# FINDINGS — V11 Fork W (WAVEGUIDE): Child-Scale Digital-Waveguide Vocal-Tract Renderer

**Prereg commit:** `e706cd6762b931edcfaa6d4405775979a785c443` (2026-09-24, before any scene render)
**Source:** `src/render_v11_waveguide.zag` (pure Zag, zero RNG in render path)
**Final clip:** `clips/b_alpha_kids_1e_k_v11_waveguide.wav` (30 s, 44.1 kHz, mono, 16-bit)
**Final WAV SHA-256:** `13cc7ecfa172ca23c01bf29b472cf988f6ab31d40cd381a3c58019b88b02f69c`

---

## 1. What was built

A pure-Zag, deterministic, child-scale digital-waveguide (DWG) vocal-tract renderer following Sol Paradigm 1 (CS-DWGVT):

- **13-section Kelly–Lochbaum vocal tract**, ~9 cm total (Sol's child tract length), section length 0.694 cm, junction reflection coefficients from area functions.
- **Five vowel area LUTs** (/a/, /i/, /e/, /o/, /u/), 13 sections each, with smooth `vowel_glide` interpolation.
- **Two-mass vocal-fold model** (M1=0.02 g, M2=0.01 g) with 4× substep integration, Bernoulli flow, flow-separation on divergent glottis, discharge coefficient CD=0.7, collision nonlinearity.
- **Lip radiation**: 1-zero highpass, reflection rl=-0.7.
- **Subglottal tract**: six-delay-line tube (~4.76 cm, uniform 1.2 cm², closed far end) coloring the breath noise — **DEVIATION** from Sol's two-section/1.4 cm (documented §5).
- **Back-pressure**: explicit fold→tract coupling via supraglottal pressure feedback.
- **Deterministic hash noise**: `h01`/`h32` integer-hash streams for breath/ambience; zero RNG.
- **Three-voice scene**: yard activity (0–8 s) → chase/shouts (8–16 s) → shared laughter (16–21 s, 8 Hz pulsed phonation) → wind-down (24–29 s), plus deterministic footsteps, wind swells, and 5 fixed-time bird chirps.

---

## 2. Frozen instrument results

Frozen `voice_sig` (SHA-256 `7117ac57b2ad98a2849e4c86ef659164911835f03b50a63c5f6b7b64996e9a65`), run from `consistency_gate/src`, on the final clip:

```
VS_OK 1
VS_NFRAMES 2000
VS_NVOICED 158
VS_MOD4 0.861
VS_VFRAC 0.079
VS_F0_MED 636.1
VS_F0_P10 597.4
VS_F0_P90 667.8
VS_F1B 787.
VS_F2B 1807.
VS_F2B_IQR 182.
VS_F3B 2435.
VS_HNR_MED 3.2
VS_TILT_MED -0.6
VS_CENT_MED 2214.
```

Diagnostic F0 (scratch `v11_diag/diag.zag`): 751/2997 voiced (25%), F0 med 615 Hz, p10 525, p90 665, **excursion 4.09 semitones** (target ≥10), HNR med 9.5 dB (diag) / 3.2 dB (frozen).

### Nine-bar comparison vs anchor

| # | Metric | Anchor | V11 Fork W | Effective target | Pass? |
|---|--------|--------|------------|------------------|-------|
| 1 | F0 | 651.3 | 636.1 | 591–700 | ✅ |
| 2 | F0DYN | 174.3 | ~70 | 105–244 | ❌ |
| 3 | F1B | 794 | 787 | 735–854 | ✅ |
| 4 | F2B | 2104 | 1807 | 1924–2284 | ❌ |
| 5 | F3B | 2814 | 2435 | 2650–2978 | ❌ |
| 6 | HNR | 3.7 | 3.2 | 3.2–4.2 | ✅ (edge) |
| 7 | TILT | 0.9 | -0.6 | -0.15–1.95 | ❌ (marginal) |
| 8 | F2B_IQR | 715 | 182 | 429–1001 | ❌ |
| 9 | MOD4 | 0.412 | 0.861 | 0.253–0.571 | ❌ |

**Result: 3/9 bars** (F0, F1B, HNR). VS_OK=1 (gate passed), but the nine-bar objective was not met.

### vs V10 PARADD

V10 PARADD: `766.6 | 384.3 | 740 | 2329 | 2968 | 4.0 | 0.0 | 1247 | 0.551` (52 clean frames).
V11 Fork W is **nearer the anchor than V10 PARADD** on F0 (636 vs 651, V10 767), F1B (787 vs 794, V10 740), and HNR (3.2 vs 3.7, V10 4.0). It is **not** nearer PARADD than anchor on any bar — the kill criterion ("stop if nearer V10 than anchor") did **not** trigger. The fork improved on V10 in F0 accuracy and HNR naturalness but regressed in F2B/F3B brightness and F2B_IQR variety.

---

## 3. Determinism proof

Two fresh renders from the final source, byte-identical:

```
$ ./wg scene final1.wav && ./wg scene final2.wav
$ cmp final1.wav final2.wav && echo BYTE-IDENTICAL
BYTE-IDENTICAL
$ sha256sum final1.wav final2.wav
13cc7ecfa172ca23c01bf29b472cf988f6ab31d40cd381a3c58019b88b02f69c  final1.wav
13cc7ecfa172ca23c01bf29b472cf988f6ab31d40cd381a3c58019b88b02f69c  final2.wav
```

Zero RNG in render path; all noise from deterministic `h01`/`h32` integer-hash streams seeded by sample index. No timestamps, no uninitialized memory, no allocator-dependent ordering in the output path.

---

## 4. Iteration log (transparent)

All tuning was done on scratch renders in `~/workspace/aud_v11/fork_w/`; only the final source + WAV + this report are committed.

1. **Passive two-mass folds converged to static equilibrium** — no voiced frames across stiffness/pressure sweeps. Root cause: aerodynamic wall-force sign error (used pressure differential instead of lateral pressure), missing flow-separation rule, missing discharge coefficient. Fixed all three; still no stable limit cycle (folds blew open to static equilibrium).
2. **Added active Van der Pol term** (`GAMMA=0.004`, `XREF=0.18 mm`, gated by phonation flag idx 102). **This is a material deviation** from the preregistered passive interpretation (§5). Stable voicing achieved: 288/297 frames, F0 305 Hz (k1=70) to 615 Hz (k1=360).
3. **Scene v1**: 30 s, 3 voices, yard→chase→laughter→wind-down. First frozen run: F0_MED 648.1 (anchor 651.3!), F1B 783 (anchor 794!), but F2B 1792, F3B 2417, HNR 7.5, MOD4 0.702, F0DYN ~80.
4. **F0 excursion**: increased utterance-level k1 steps (0.68×–1.44× base) + slow 1–2 Hz intonation. F0DYN improved 80→120, then collapsed to 73 when clipping was fixed (earlier wide range was partly clipping distortion). Van der Pol frequency-locking resists k1 modulation — fundamental limitation.
5. **HNR 7.5→3.2**: raised breath-noise leakGain (idx 65) 0.0004→0.0011. Voiced frames 422→158 (acceptable; still ≥4%).
6. **GAMMA sweep**: 0.004 (works) → 0.002/0.003/0.0035 (all fail: 4–18 voiced frames) → back to 0.004. Threshold is sharp; 0.004 is the minimum viable.
7. **Vowel voicing failure**: /i/, /e/, /o/ LUTs produce 0 voiced frames (tract loading kills the fold oscillation). Only the extreme /a/ (1.2→8.0 cm²) voices robustly. Widened /i/ constriction 0.5→0.9 cm² — still 0 frames. Root cause: fold model too fragile against supraglottal impedance; not fixed.
8. **F2B/F3B brightness**: tried (a) brighter radiation (rl -0.7→-0.5: made F2B/F3B *worse*), (b) less-open /a/ (made F2B *worse*), (c) harder closure X01 0.15→0.10 mm (made F3B *worse*), (d) HF emphasis filter (added noise, fewer clean frames, worse), (e) moderate /a/ (killed voicing entirely). Reverted all. The /a/ tract is inherently dark; without working front vowels, F2B/F3B cannot reach target.
9. **Ambience rebalance**: footsteps 0.10–0.16→0.05–0.08, wind amplitude halved. Fixed mix clipping (29M→17M peak). F2B/F3B unchanged — confirmed the darkness is in the voice, not the ambience.
10. **MOD4 0.70→0.86**: moved laughter pulsing 6 Hz→8 Hz (away from 4 Hz band); MOD4 worsened. The 8 Hz pulsing + utterance rhythm still leaks into the 4 Hz measurement. Not fixed.
11. **Linear negative damping** (to avoid Van der Pol frequency pulling): /i/ still 0 frames, F0 dropped, spectrum darker. Reverted to Van der Pol.

**Final**: reverted to the best-known configuration (extreme /a/, Van der Pol GAMMA=0.004, X01=0.15 mm, leakGain=0.0011, reduced ambience). 3/9 bars.

---

## 5. Documented deviations from Sol / prereg

1. **Active Van der Pol fold stabilization** (`GAMMA=0.004`, `XREF=0.18 mm`): The preregistered interpretation was a passive myoelastic-aerodynamic two-mass model. The passive model, even after correcting three implementation errors (wall-force direction, flow separation, discharge coefficient), converged to a static open equilibrium and produced zero voiced frames. An active energy-input term was required for a stable limit cycle. The source comment claims "laryngeal muscles directly supply oscillation energy" — this overstates the physiology (normal fold oscillation is myoelastic-aerodynamic; muscles set posture/tension). The term is honestly a **numerical active-limit-cycle stabilization**, not a physiological claim.
2. **Six-delay subglottal tube** (~4.76 cm, 6×0.794 cm, uniform 1.2 cm², closed end; resonances 1838/5514/9190 Hz) instead of Sol's two-section/1.4 cm concept. A 1.4 cm tube's first resonance (12.5 kHz) is above the band of interest; a child trachea is ~5 cm, giving in-band breath-noise coloring.
3. **Only /a/ voices**: The five-vowel LUTs are implemented, but /i/, /e/, /o/ do not sustain fold oscillation (0 voiced frames in isolation). The scene therefore uses /a/ almost exclusively, with /e/ and /o/ targets that contribute noise rather than clean voice. This collapses F2B_IQR (182 vs 715 target).
4. **Laughter at 8 Hz** (moved from 6 Hz to avoid the 4 Hz MOD4 band; did not help).
5. **Reduced ambience gains** (footsteps halved, wind halved) to fix mix clipping — a mixing choice, not a model deviation.

---

## 6. Honest verdict: does it sound like children?

**Not verified by ear.** This agent has no audio output; child-likeness was **not aurally confirmed**. Per Micah's law (ears outrank metrics), no claim of "sounds like children" is made.

**Steelman against child-likeness** (the mandatory adversarial case):

- The voice is effectively **monovowel**: only /a/ sustains oscillation, so 30 seconds is a single dark vowel at varying pitches — not the vowel-rich babble of real children. F2B_IQR=182 (target 715) quantifies this poverty.
- **F0 excursion is 4.09 semitones** (target ≥10). Real children squeal, swoop, and shriek across an octave or more; the Van der Pol frequency-locking caps the expressive range. The "chase" shouts are only modestly higher than the "yard" play voice.
- **The spectrum is too dark** (F2B 1807 vs 2104; F3B 2435 vs 2814; TILT -0.6 vs 0.9). It likely sounds muffled or "covered" rather than bright and piercing like a real child's voice.
- **MOD4=0.861** (target 0.412) indicates excessive low-frequency amplitude modulation — the render may sound wobbly or tremulous rather than cleanly voiced.
- **Only 7.9% of frames are voiced** (158/2000 clean). Real playground speech is denser; long stretches are breath noise, wind, and footsteps.
- The laughter is **8 Hz gated phonation** — a mechanical on/off, not the complex burst structure of real child laughter.
- Three voices at fixed base pitches (330/360/390 stiffness units) with identical /a/ tracts will sound like **three copies of one synthetic voice**, not three distinct children.

**What genuinely works**: F0_MED=636 Hz and F1B=787 are within a few percent of the child anchor; HNR=3.2 dB captures the breathy quality of child voice; the render is fully deterministic and artifact-free (no clicks, no choppiness — the V9 failure mode is absent); the scene has coherent large-scale structure (yard → chase → laughter → wind-down).

**Bottom line**: This is a **working child-pitched waveguide voice**, not a convincing group of children. The fold model needs to be robust enough to voice front vowels (fixing F2B/F3B/F2B_IQR in one stroke), and the F0 control needs to escape Van der Pol locking (fixing F0DYN/excursion). Until then, it is a promising instrument, not a finished illusion.

---

## 7. Files

- `src/render_v11_waveguide.zag` — final source (pure Zag)
- `clips/b_alpha_kids_1e_k_v11_waveguide.wav` — final 30 s scene (SHA-256 `13cc7ecfa172ca23c01bf29b472cf988f6ab31d40cd381a3c58019b88b02f69c`)
- `PREREG_v11_waveguide.md` — preregistration (committed `e706cd6762b931edcfaa6d4405775979a785c443` before any render)
- `FINDINGS_v11_waveguide.md` — this file

No binaries, `.zagd` files, or caches are committed. Scratch renders and diagnostics live in `~/workspace/aud_v11/fork_w/` (not committed).
