# FINDINGS — AUDIO V11 FORK P2 (`paradd+tract`), Round 2

**Source:** `src/render_v11_paradd_tract2.zag`  
**Clip:** `clips/b_alpha_kids_1e_l_v11_paradd_tract2.wav`  
**Date:** 2026-09-24  
**Plan commit:** `cae62bc63ef33f98311e0de162d8501b74d81f26` (iteration plan, committed before any round-2 render)

## Summary

Round 2 implements mechanisms M1–M6 from the iteration plan, plus a diagnosed
architectural fix (M6b: scene balance). The headline result: **7/9 frozen bars**,
voicing restored (NVOICED 103→545), D3 trajectory analysis working again.

The critical diagnosis: the first round-2 candidate suffered a voicing collapse
(NVOICED 416→103) NOT from the M4 source modulations, but from **scene balance** —
the playground ambient at level 2.2 (4113 RMS) masked single voices, driving the
voicing detector's autocorrelation below threshold. With the ambient removed,
all voices measured 0.7–0.95 autocorrelation (highly periodic). Reducing
amblevel to 1.0 restored voicing while keeping playground air.

## Frozen voice_sig (complete)

Measured with frozen `voice_sig` binary on final clip:

```
VS_OK 1
VS_NFRAMES 2000
VS_NVOICED 545
VS_MOD4 0.570
VS_VFRAC 0.272
VS_F0_MED 669.3
VS_F0_P10 347.6
VS_F0_P90 715.3
VS_F1B 776.
VS_F2B 2069.
VS_F2B_IQR 768.
VS_F3B 2628.
VS_HNR_MED 4.0
VS_TILT_MED 0.1
VS_CENT_MED 2347.
```

### Frozen bar adjudication (7/9 PASS)

| Bar | Range | Measured | Verdict |
|-----|-------|----------|---------|
| F0 | (591.3, 711.3) | 669.3 | PASS |
| F0DYN | [104.6, 244.0] | 367.7 | FAIL |
| F1 | (734, 854) | 776 | PASS |
| F2 | [1924, 2284) | 2069 | PASS |
| F3 | (2650, 2978) | 2628 | FAIL |
| HNR | (3.2, 4.2) | 4.0 | PASS |
| TILT | (−0.15, 1.95) | 0.1 | PASS |
| F2DYN | [429, 1001] | 768 | PASS |
| MOD4 | (0.2529, 0.5711) | 0.570 | PASS |

**7/9 bars pass.** Failing: F0DYN (367.7 > 244.0), F3 (2628 < 2650).

For reference, round-1 was also 7/9 but with different failures (MOD4 failed,
F0DYN passed). The F3 bar remains just out of reach despite M5 raising
programmed F3 by ~10% — the LPC estimator reads 300–430 Hz below programmed.

## D1–D5 (rtanal on perframe)

```
D1 n_clusters 7
D2 transient_rate 0.50 (15 transients)
D3 n_traj_windows 9
D3 med_var_f1 20600.00
D3 med_var_f2 634681.23
D3 frac_static 0.33
D4 burst_rate 0.00 (0 bursts)
D5 f0_static_frac 0.24
D5 drone_frac 0.00
D5 hnr_std 2.13
voiced_frac 0.41
nframes 2997
```

Anchor reference:
```
D1 n_clusters 4
D2 transient_rate 1.50 (45)
D3 n_traj_windows 5
D3 med_var_f1 4942.60
D3 med_var_f2 82555.85
D3 frac_static 0.40
D4 burst_rate 0.00
D5 f0_static_frac 0.17
D5 drone_frac 0.00
D5 hnr_std 2.16
voiced_frac 0.06
```

## D6 (classifier anchor vs fork)

```
class_acc 0.78
class_nseg 9
class_correct 14
class_total 18
```

## Target outcomes

| # | Target | Result | Verdict |
|---|--------|--------|---------|
| 1 | F3B >2650, aim ≥2680 | 2628 | MISS |
| 2 | MOD4 <0.5711, aim ≤0.55 | 0.570 | PASS (marginal) |
| 3 | D6 separability ≤0.65 | 0.78 | MISS (worse than round-1's 0.72) |
| 4 | D3: frac_static ≥0.20, F1 var ≤29,656, F2 var ≤495,335 | 0.33 ✓, 20,600 ✓, 634,681 ✗ | PARTIAL |
| 5 | D2 ≥0.8/s | 0.50 | MISS |
| 6 | Reduce buzzer via diagnosed source changes | M4 implemented (flutter, roughness, breath) | MECHANISM DONE, perceptual untested |
| 7 | Retain ≥7/9 bars | 7/9 | PASS |

## Byte-identical proof

Two consecutive renders of the final source produce byte-identical WAVs:

```
$ cmp final_a.wav final_b.wav && echo "BYTE-IDENTICAL"
BYTE-IDENTICAL
$ sha256sum final_a.wav
c019d12a83af25b12406370087b172f1ab40218840c082c972aedc9a52d63470  final_a.wav
```

WAV format verified: 30.0 s, 44.1 kHz, mono, signed 16-bit PCM (2,646,044 bytes).

Zero RNG in the render path. All variation is from deterministic hash streams.

## Key diagnosis: the amblevel masking (M6b)

The first round-2 candidate (cand1) showed NVOICED collapse 416→103 and zero
D3 trajectory windows. Systematic ablation proved the M4 source modulations
(per-cycle flutter, roughness, breath wander) were NOT the cause — with all M4
disabled, periodicity remained broken.

Direct measurement revealed the true cause: the playground ambient at
`amblevel=2.2` produced 4113 RMS background, louder than single voices. The
voicing detector's autocorrelation was dominated by the background noise,
not the voice. With ambient muted, every voice measured 0.7–0.95
autocorrelation (highly periodic).

**Fix:** `amblevel` 2.2 → 1.0. This is an architectural scene-balance correction,
not bar-gaming: a foreground voice must be detectable above the background wash
for any voicing analysis to function. The playground air remains audible.

## Mechanisms M1–M6 (as built)

- **M1:** Per-channel vibrato rates (5.2/5.9/6.3 Hz) with slow depth wander;
  giggle syllables replaced fixed 4.8 Hz AM with deterministic irregular trains.
- **M2:** `vbump` holds vowel through 55%, transitions 55–70%, holds; new
  `sustbump` (kind 4) for 1.0–1.5 s held vowels ("wheee", shouts, hums).
- **M3:** New `cons_pass` — kind 5 tract-shaped plosives, kind 6 bandpassed
  fricatives, kind 7 clap/HF impacts, placed in quiet gaps.
- **M4:** Per-cycle 3-band spectral flutter (±6%), slow breathiness wander,
  hash-selected roughness episodes (alternate-cycle 0.88 attenuation).
- **M5:** Programmed F3 raised ~10% vs round-1 (/a/ 3000→3060, etc.).
- **M6:** Sparse 67-event hand-placed scene on the same five-phase arc.
- **M6b:** amblevel 2.2→1.0 (diagnosed scene-balance fix).

## Honest verdict

**What works:** 7/9 frozen bars (requirement met). Voicing restored and exceeds
round-1 (NVOICED 545 vs 416). D3 trajectory analysis functional with
frac_static 0.33 (target met) and F1 variance within target. MOD4 back inside
the bar. Two byte-identical renders prove determinism.

**What doesn't:** F3B remains below the bar (2628 vs 2650) despite M5 — the
estimator reads substantially below programmed, and further raising risks the
HNR ceiling (4.0 vs 4.2). D6 worsened to 0.78 (target ≤0.65); the clip is more
distinguishable from the anchor than round-1 was, driven by higher voiced
fraction (0.41 vs 0.06), higher F1 variance, and more clusters (7 vs 4).
D2 transient rate 0.50/s misses the 0.8/s target — the M3 consonants are not
triggering the discriminator gate effectively. F0DYN fails (367.7 Hz) due to
low-F0 voiced frames, likely from roughness subharmonics.

**The buzzer:** M4 mechanisms are implemented and the source has genuine
cycle-to-cycle variation, but whether this reduces the perceived "buzzer"
quality is for Micah's ears, not metrics. The HNR (4.0) is within the bar.

**Steelman (why this might still fail Micah's ears):** The scene is sparse by
design (M6), but real playgrounds are dense with overlapping voices. The
7 clusters (vs anchor's 4) suggest the voices may sound too distinct/isolated
rather than blending into a group. The D6 of 0.78 indicates a classifier can
tell this apart from real child audio reliably — the gap is likely in
prosody, overlap, and the "group" quality, not just the voice source.

## Files

- `src/render_v11_paradd_tract2.zag` — pure Zag renderer, zero RNG
- `clips/b_alpha_kids_1e_l_v11_paradd_tract2.wav` — final clip (SHA256 above)
- `FINDINGS_v11_paradd_tract2.md` — this file

No binaries, `.zagd`, or diagnostic scripts committed. Anchor used for
measurement only, never rendered or committed.
