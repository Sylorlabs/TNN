# F3 `onset_graft` — RUNLOG (build crew log)

Date: 2026-09-24 PDT. Prereg: `~/workspace/audio_round3/ROUND3_PREREG.md` (frozen).
Section 5 is the spec; §§0/2/7/8 are binding law. This log is the complete record.

## 0. Outcome

**FORK KILLED on G3 (shared analyzer gates) — HNR and HF fail, including after
the one permitted repair.** Killed at the integer-exact prototype stage;
no Zag build was attempted because the prototype proves the frozen design
cannot pass G3 (a Zag port would be bit-identical and equally dead).
Additionally the F3.3 (transient necessity) and F3.4 (HF necessity) claims die,
and F3.5 kills WSOLA-as-mechanism on its letter. Details below.

## 1. Source pins (all SHAs verified)

| Role | File | SHA-256 (prefix) | Offset | Length |
|------|------|------------------|--------|--------|
| Nucleus | `~/workspace/aud_v11/diag/vowel_real.wav` | `8ba3b42708a8bab2…` (full match to prereg §3 pin `8ba3b427…5d1d`) | samples [8820, 66150) = [0.2, 1.5) s | 57330 samples (1.3 s, ≥300 ms voiced ✓) |
| Onset | `~/workspace/v5work/kidc.wav` | `5a1b1f7b1f359f4f…` | t0 = sample 657055, cut [t0, t0+1323) = 30 ms | 1323 samples |
| Breath | `~/workspace/v5work/kidc.wav` | `5a1b1f7b1f359f4f…` | [1019592, 1023120) = [23.12, 23.20) s, 80 ms, REVERSED at render | 3528 samples |

Nucleus interval choice: [0.2, 1.5) s of `vowel_real.wav`; measured periodicity
0.983 on the interval (voiced ✓). Peak in interval = 23560.

## 2. Frozen hunt rules (fixed before seeing results, logged here)

**Onset rule:** scan `kidc.wav`, `kidd.wav`, `kide.wav` in order; in each, scan
consecutive non-overlapping 200 ms windows from t=0; select the FIRST window
with max|x[n+1]−x[n]| ≥ 4000 AND preceding-100 ms RMS < 0.3 × window RMS
(true attack from relative quiet, not mid-vowel). t0 = first argmax |slope|
in the window. Cut = [t0, t0+30 ms].
Result: `kidc.wav`, window [14.7, 14.9) s, t0 = 657055 (14.898 s),
max|slope| = 4507, pre-RMS 73.5 vs window RMS 3640.9. (Playground beds in
`audio_round2/shared/`: none exist — only scripts; documented. Field recording
`aporee_kids_play_area_30s.wav` scanned as fallback: no qualifying window.)

**Breath rule (original):** first 80 ms non-overlapping window, files
kidc→kidd→kide, periodicity < 0.3, RMS in [250, 1500], centroid in
[800, 6000] Hz.
Result: `kidc.wav` @ 430416 (9.76 s), RMS 1469, centroid 870 Hz.
→ REPAIRED (see §5): replaced by bright-breath rule.

**Breath rule (REPAIR-1, logged):** same scan, but centroid > 1500 Hz
(principled: the release is breath/air — broadband by nature; the 870 Hz
rumble was a poor breath candidate and carried no HF).
Result: `kidc.wav` @ 1019592 (23.12 s), RMS 1751, centroid 1902 Hz,
5.3% energy > 8 kHz, peak 7658, smooth swell onset (not a click), sustained
envelope. This is the frozen breath.

## 3. Frozen chain parameters

- WSOLA source-side only: L = 1024, Ha = 512, R = 128, T_corr = 256.
  Hs = round(512·T_target/T_source). T_target = round(1.15·57330) = 65929.
  Hs = 589. J = 110 frames. N_target_realized = 65225.
  Stretch realized = 65225/57330 = 1.1377 ∈ [0.85, 1.25] ✓.
- Correlation selector: for frame j ≥ 1, δ_j ∈ [−128, 128] maximizing
  integer covariance Σ(x−x̄)(y−ȳ) between tail-256 of frame j−1's source
  window and head-256 of candidate window; candidate starts clamped to
  [0, Slen−L]; ties → δ = 0 then lowest δ (deterministic scan order).
  δ_0 = 0.
- Hann OLA, Q15 table; output = acc·32768/W rounded, W = 0 → 0.
- Gains (frozen, from nucleus input peak only): headroom target 29200
  (−1.001 dBFS). G_n = (29200·32768)//23560 = 40612 (Q15).
  G_t = (2·G_n)//10 = 8122 (0.2·G_n). G_b = (35·G_n)//100 = 14214 (0.35·G_n).
- Assembly: transient·G_t at samples [0, 441); 10 ms equal-power crossfade
  [441, 882) between transient tail and nucleus head (Q15 cos/sin tables);
  nucleus·G_n from 882; reversed breath·G_b added at
  [441+65225−1764, +3528) = [63902, 67430). Total 67430 samples (1.529 s).
- No compressor/saturator/EQ/denoise/normalization. All integer, zero RNG.

## 4. Prototype measurements (integer-exact Python mirror of the Zag spec)

Analyzer: `audio_round2/shared/analyze.py`. Full mix SHA-256 (2 runs):
`3ddba86b26d95cdf345375004396fe0428e2338ab51341b44f4482d3be5fe4f7`
(byte-identical ✓).

| Metric | Full mix | Gate | Verdict |
|--------|----------|------|---------|
| frac_static | 0.9868 | ≥ 0.25 | PASS |
| HNR | **7.82 dB** | [0.7, 6.7] | **FAIL** (+1.1 dB over) |
| periodicity | 0.8584 | ≥ 0.5 | PASS |
| HF rolloff | **−48.24 dB** (after REPAIR-1; was −51.53) | [−40, −12] | **FAIL** (−8.2 dB under) |
| prosody CV | 1.249% | [0.3%, 3%] | PASS |
| transient crest (med) | 7.14 dB | [3, 20] | PASS |
| peak | −1.03 dBFS | < −1 | PASS |

## 5. The one repair (REPAIR-1, logged)

Failed bar: G3 HF (−51.53 dB, need ≥ −40).
Repair: replaced dark breath (centroid 870 Hz) with bright breath
(kidc @ 23.12 s, centroid 1902 Hz, 5.3% > 8 kHz) under the revised
breath rule (§2). Principled: breath/air is broadband; selection was for
breath-likeness, and the rule is frozen and logged.
Result: HF −51.53 → −48.24 dB (+3.3 dB). Still 8.2 dB short of −40.
HNR unchanged (7.82 dB). **Repair did not bring the bar into range.**
No second repair attempted (one per bar max).

Why it can't work: the nucleus is 1.48 s of loud (−1 dBFS) clean vowel;
the layers total 110 ms at 0.2/0.35 gain. The vowel's max-500 Hz band
(HF denominator) is ~4e12; the layers cannot supply 1e-4 of it in >8 kHz.
The source vowel (`vowel_real.wav`) is uniformly clean (HNR ~17.5 dB) and
dark (HF −43 to −66 dB) across its full 2 s — no interval selection can fix
this within the frozen chain.

## 6. Kill-bar verdicts

- **F3.1** stretch 1.1377 ∈ [0.85, 1.25] ✓; repeated-block fraction 0.0
  (110/110 unique starts) < 0.5 ✓ → **PASS**.
- **F3.2** min frame-boundary Pearson r = 0.9941 (worst j=31) ≥ 0.98 → **PASS**.
  (The WSOLA alignment itself works excellently.)
- **F3.3 TRANSIENT NECESSITY** → **FAIL — claim DIES.**
  Full mix onset crest 7.14 dB (in [3,20] ✓); G_t=0 ablation 7.15 dB
  (NOT < 3 dB ✗). The 20 ms crest window is dominated by the loud vowel
  nucleus; the transient (0.2 gain, peak 2193 vs nucleus 29116) is
  invisible to the crest metric. The ablation is 0.01 dB different from
  full — the transient contributes nothing measurable to onset crest.
  No repair can fix this within the frozen chain (the nucleus will always
  dominate). Per prereg: "the graft claim dies."
- **F3.4 HF NECESSITY** → **FAIL — claim DIES.**
  Full-mix HF −48.24 dB is NOT in [−40, −12] (first condition fails).
  Nucleus-only HF −52.17 dB; drop vs full only 0.64 dB (need ≥ 6 dB).
  Honest write-up: the breath is not the HF story — the layers contribute
  negligible HF; the "air" does not materialize in the measurement.
  Per prereg, claiming otherwise would kill the claim; I admit it: the
  breath layer is not the HF story.
- **F3.5 NAIVE-SPLICE CONTROL** → **FAIL — WSOLA dies as the mechanism
  on the letter of the bar.**
  Naive (δ*=0) boundary-sample discontinuity vs aligned: median flux
  differs by 0.3 dB (NOT ≥ 6 dB worse ✗). (Note: Hann OLA smooths both;
  the real naive-vs-aligned difference appears in HNR/HF, where — perversely —
  the naive version scores BETTER: HNR 6.59 vs 7.82, HF −42.52 vs −51.53.
  The shared gates reward the naive splice's broadband artifacts.)
- **G1 provenance:** 100% of output samples map to the three pinned files
  (nucleus intervals, transient cut, reversed breath cut, gains logged).
  Spot-checkable from the frozen parameters above. (Would be PASS.)
- **G2 determinism:** 2/2 prototype runs byte-identical
  (`3ddba86b…5fe4f7`). (Would be PASS; third run not done — fork dead.)
- **G4 no-static audit:** (a) boundary raw sample-diffs at graft points are
  −21.5/−21.8 dB rel peak — dominated by NATURAL vowel slope
  (404 Hz × 29116 amplitude ⇒ ~1700/sample natural), not artifactual clicks;
  the crossfade is mathematically continuous (equal-power). No isolated
  click exceeds 4× local median slope. (b) no 50 ms frame with crest > 20 dB
  (max 7.5 dB) ✓. (c) voiced 8–16 kHz −54.2 dB rel peak ✓ (≤ −30).
  G4 would PASS under the natural-slope interpretation.
- **G5 silence:** not run (fork dead on G3; prototype divides by peak=0 —
  would need the Gn=0-when-peak=0 rule; moot).

## 7. What died and why

1. **The fork** dies on **G3**: HNR 7.82 dB (> 6.7) and HF −48.24 dB
   (< −40), after the one permitted repair. Root cause: the frozen design
   (clean WSOLA vowel at −1 dBFS for 1.48 s + 110 ms of low-gain layers)
   is structurally incompatible with gates that demand a moderately noisy
   signal. The only available nucleus source (`vowel_real.wav`) is too
   clean (HNR ~17.5) and too dark (HF ≤ −43) everywhere; the layers are too
   small and too quiet to move the medians.
2. **The transient-necessity claim** (F3.3) dies: the crest metric cannot see
   the transient under the nucleus.
3. **The HF-necessity / breath-as-air claim** (F3.4) dies: the breath
   contributes ~0.6 dB of HF; it is not the HF story.
4. **WSOLA-as-mechanism** (F3.5) dies on the bar's letter: naive splicing is
   not ≥6 dB worse in boundary flux — and the shared gates perversely prefer
   the naive version's artifacts.

The mechanism itself (source-side WSOLA with covariance search) works
correctly (F3.2: r ≥ 0.9941 on all 110 frames; F3.1: stretch/budget clean;
deterministic). What fails is the fit between the design's output and the
measurement framework — a design-level incompatibility, not an
implementation bug. No Zag build was produced (nothing valid to build).

## 8. Artifacts in this workdir

- `RUNLOG.md` (this file)
- `proto.py` — integer-exact prototype (design exploration tool, not deliverable)
- `abl.py` — full / noT / nuc / naive render modes
- (No WAV master: fork killed before render-for-delivery. Prototype WAVs in
  /tmp only: `/tmp/f3_full.wav` etc., SHA `3ddba86b…5fe4f7`.)

## 9. Note for the parent

Do NOT stage anything for ears. There is no surviving audio. The honest
deliverable is this kill record. If Micah wants F3 re-attempted, the design
needs a prereg amendment (noisier nucleus source class, or gates recalibrated
for clean-vowel WSOLA) — that needs his word.
