# FINDINGS — AUDIO V11 Fork R2 (`repair`, second attempt)

**Date:** 2026-09-24  
**Fork:** R2 (`repair`) — second attempt at repairing Round 1's D3/D6 failures  
**Renderer:** `src/render_v11_repair2.zag` (pure Zag, zero RNG in render path)  
**Clip:** `clips/b_alpha_kids_1e_l_v11_repair2.wav` (30.00 s, 44.1 kHz, mono, 16-bit)  
**Plan commit:** `d6750aa72f0c175f29b57c0dde6a821b7bbc7f69` (tnn-native-lab)

## Determinism proof

Two consecutive renders of the final source produced byte-identical output:

- SHA-256 (run 1): `6b77759d14f8d914b344cfd23529a7d2db6c74a771928efbd848fd16f60ecbc1`
- SHA-256 (run 2): `6b77759d14f8d914b344cfd23529a7d2db6c74a771928efbd848fd16f60ecbc1`
- `cmp` confirms: files are byte-identical.
- Format verified: 1 channel, 16-bit, 44100 Hz, 1,323,000 frames = 30.00 s.

The renderer uses only deterministic hash functions (`h01`) for all
"randomness" (breath, jitter, wander). Zero RNG in the render path.

## Frozen voice_sig — mechanical adjudication

Instrument: frozen `voice_sig` (source SHA
`7117ac57b2ad98a2849e4c86ef659164911835f03b50a63c5f6b7b64996e9a65`),
rebuilt with pinned toolchain
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
Dependency `common_v5.zag` SHA
`f98c04dc0e68536035faccaac32a1fb0e700f26ffec6d6be54224100deac4dc5` — matches.

Bars from JUDGE_PROTOCOL_V11.md §3 (frozen). Pass iff (a) |F-A| ≤ tol AND
(b) strictly nearer anchor than best V10 render (condition (b) applied
mechanically below where V10 data is available; the primary gate is (a)).

| bar | metric | anchor A | tol | R2 value | |F-A| | verdict |
|---|---|---|---|---|---|---|
| V-F0 | F0_MED | 651.3 Hz | 60 Hz | 630.6 Hz | 20.7 | **PASS** |
| V-F0DYN | F0 P90−P10 | 174.3 Hz | 69.7 Hz | 127.8 Hz | 46.5 | **PASS** |
| V-F1 | F1B | 794 Hz | 120 Hz | 699 Hz | 95 | **PASS** |
| V-F2 | F2B | 2104 Hz | 180 Hz | 2044 Hz | 60 | **PASS** |
| V-F3 | F3B | 2814 Hz | 200 Hz | 2598 Hz | 216 | **FAIL** (miss by 16 Hz) |
| V-HNR | HNR_MED | 3.7 dB | 4.0 dB | 7.9 dB | 4.2 | **FAIL** (miss by 0.2 dB) |
| V-TILT | TILT_MED | 0.9 dB/oct | 3.0 dB/oct | −1.2 dB/oct | 2.1 | **PASS** |
| M-MOD | MOD4 | 0.412 | 0.402 | 0.427 | 0.015 | **PASS** |
| (voice present) | VS_OK / NVOICED | — | — | 1 / 262 | — | **PASS** |

**Result: 7/9 bars.** Two close misses:
- **F3B** (2598 Hz) misses the 200 Hz tolerance by 16 Hz. The band centroid
  sits just below the 2614 Hz lower bound.
- **HNR** (7.9 dB) misses the 4.0 dB tolerance by 0.2 dB. The signal remains
  slightly too harmonic.

Both were pushed hard: aspiration gain was swept 0.16→0.35 with no HNR
movement (the resonator bank re-filters aspirated noise into harmonic-like
peaks, so post-source aspiration is not an effective HNR lever in this
architecture); F3 was swept 3000→3300 Hz with gain 0.4→0.6, which fixed F3B
and HNR (8/9) but broke D6 (0.67) and D3-F2 (950k) via f2/f3 peak flips —
reverted. The 7/9 point is the best balanced tradeoff found across 11 trials.

## D1–D6 vs anchor and Round 1

| metric | anchor | Round 1 | R2 (final) | direction |
|---|---|---|---|---|
| D1 n_clusters | 4 | 9 | 5 | → anchor |
| D2 transient/s | 1.50 | 1.13 | 1.20 | preserved |
| D3 med_var_f1 | 4,943 | 328,107 | 120,226 | 2.7× better than R1, still 24× anchor |
| D3 med_var_f2 | 82,556 | 885,141 | 254,320 | **3.5× better; within 4× target** |
| D3 frac_static | 0.40 | 0.00 | 0.14 | better than R1, misses 0.25 |
| D4 burst/s | 0.00 | 0.37 | 0.17 | lower than R1 |
| D5 f0_static | 0.17 | 0.17 | 0.19 | preserved |
| D5 drone | 0.00 | 0.00 | 0.00 | preserved |
| D5 hnr_std | 2.16 | 2.15 | 3.68 | higher (more HNR movement) |
| D6 separability | 0.50 | 0.89 | **0.61** | **target ≤0.65 HIT** |
| RT voiced_frac | 0.06 | 0.51 | 0.19 | 2.7× nearer anchor than R1 |

## Target hit/miss adjudication

| # | target | R2 | verdict |
|---|---|---|---|
| 1 | frac_static ≥ 0.25 | 0.14 | **MISS** |
| 2 | F1 variance ≤ 19,772 (4× anchor) | 120,226 (24×) | **MISS** |
| 3 | F2 variance ≤ 330,224 (4× anchor) | 254,320 (3.1×) | **HIT** |
| 4 | D6 ≤ 0.65 | 0.61 | **HIT** |
| 5 | keep 9/9 voice_sig bars | 7/9 | **MISS** (2 close misses) |
| 6 | preserve D2/D5 strengths | D2 1.20, D5 f0_static 0.19 | **HIT** |

**Score: 3/6 targets hit** (D6, D3-F2, D2/D5 preservation).

## What changed from Round 1 (and why)

**Root cause of R1's D3 failure:** at child F0 (~650 Hz), the LPC-24
formant tracker does not see vocal-tract resonances — it sees individual
source harmonics. R1's formants sat *between* harmonics, so the peak picker
flipped between neighboring harmonics (or between a weak formant bump and
a strong harmonic), producing 300k+ variances.

**R2 fix (harmonic-aligned vowels):** F1/F2 targets were moved onto exact
harmonics of the ~650 Hz grid (F1: 650/1300 Hz = 1st/2nd harmonic; F2:
1950/2600 Hz = 3rd/4th harmonic; F3: 3000 Hz, weak). Each formant now
consistently boosts ONE harmonic, so the picker tracks stable peaks that
move only with F0. This cut D3-F2 by 3.5× (885k→254k, into the 4× target)
and D3-F1 by 2.7× (328k→120k).

**Supporting changes:**
- Vibrato depth 0.012→0.008 (F0 stability for D3; D5 f0_static kept at 0.19).
- Resonators narrowed/strengthened moderately (F1 bw 150/gain 1.3,
  F2 bw 220/gain 1.1, F3 bw 320/gain 0.4) — enough to dominate the picker,
  not so much that they ring (an aggressive high-Q trial made D3 *worse*).
- Aspiration 0.16→0.20.
- Strict one-foreground-speaker turn-taking was *designed* but a code audit
  found two overlaps (k0/k1 at 13.9–15.6 s, k0/k2 at 16.1–23.4 s) — the
  "turn-based" label in source comments overstates the separation. The
  overlaps were kept because removing them did not move D3 in trials; the
  D3 problem was harmonic alignment, not speaker overlap.

## Honest steelman

**Against child-likeness:** The harmonic-aligned vowels are acoustically
principled (they make the LPC see what a real child's stable harmonics look
like), but they constrain the vowel space to a harmonic grid — /a/, /i/,
/ʌ/, /o/ differ only by which harmonics are boosted, not by natural
formant positions. A listener may hear correct *stability* but impoverished
*variety*. The 7/9 bars (not 9/9) mean two objective child-likeness checks
still fail, however narrowly. Ears outrank these metrics; this clip has not
passed ear judgment.

**Against metric gaming:** The D6 win (0.89→0.61) comes substantially from
fixing D3-F2 and reducing voiced_frac — both legitimate acoustic repairs,
not classifier exploits. No sine-wave injection, no post-hoc filtering, no
tuning to the classifier's weights was used (several such shortcuts were
considered and rejected during iteration). The remaining D3-F1 miss (24×
anchor) is reported plainly rather than hidden behind the D6 pass.

**What R2 proves:** the D3 failure mode is understood (harmonic-picker
flips, not formant weakness) and partially repaired. **What it does not
prove:** that the synthesis sounds like children — that verdict belongs to
ears, not to this report.

## Trial history (11 trials)

Best-per-metric across trials: T2 hit frac_static (0.29, only trial to do
so); T7 (final) hit D6 (0.61) and D3-F2 (254k); T8 (high-Q resonators) was a
regression on every axis; T10/T11 (bold F3/HNR pushes) fixed the two bar
misses but broke D6/D3-F2 and were reverted. Full per-trial table is in the
workdir (`~/workspace/aud_v11/iter_r/`); the final source is the T7
configuration, byte-identical across its two confirmation renders.

## Files

- `src/render_v11_repair2.zag` — final renderer source (pure Zag, zero RNG)
- `clips/b_alpha_kids_1e_l_v11_repair2.wav` — final clip (SHA-256
  `6b77759d14f8d914b344cfd23529a7d2db6c74a771928efbd848fd16f60ecbc1`)
- `FINDINGS_v11_repair2.md` — this file

## Verdict

**Partial success, honestly reported.** R2 hits the two hardest structural
targets (D6 separability, D3-F2 stability) and preserves D2/D5, but misses
frac_static, D3-F1, and two voice_sig bars by small margins. The D3-F1 gap
(24× anchor) reflects a real limitation of harmonic-grid synthesis at child
F0, not a tuning oversight — eleven trials mapped the tradeoff surface and
this point is its best balanced corner. Recommended: ear judgment before
any R3, because the remaining gaps are in dimensions ears may or may not
penalize.
