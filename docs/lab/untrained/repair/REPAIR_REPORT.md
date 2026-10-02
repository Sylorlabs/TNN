# UNTRAINED-ANALYSIS REPAIR — Diagnosis and Repair Report

**Fork:** UNTRAINED-ANALYSIS REPAIR  
**Branch:** `tnn-native-lab` (never `main`)  
**Date:** 2026-09-26  
**Workdir:** `~/workspace/untrained_repair/`  
**Toolchain:** `znc 2026.07.0-dev (edition 2026)`  
**Source:** `repair/uanalyze.zag`  
**Binary:** `repair/uanalyze_repaired` (pure Zag, zero RNG, byte-identical reruns)

## 1. Binding c2 result (inherited, verified 2026-09-26)

| Score | Count |
|---|---:|
| MATCH | 23 |
| MISS | 8 |
| WEAK MISS | 4 |
| PARTIAL | 3 |
| HALLUCINATION | 6 |

**Verdict: FAIL** — any hallucination fails.

The six hallucinations:
1. B1 false `RHYTHM 0.100 s` (envelope-autocorr lag-2 artifact).
2. B1 false separate transient layer over noise bed (onset shredding).
3. B2 false `RHYTHM 0.100 s` (same lag-2 artifact).
4. B2 false transient layer over noise bed (hoot onsets mischaracterized; bed is quiet, not noisy).
5. B3 false 15 distinct transient events (continuous helicopter chopped into "transients").
6. B4 false "mostly smooth, little fine detail" (80×45 downscale destroyed texture).

## 2. Root causes and repairs

### Audio

| # | Root cause | Repair | Mechanism |
|---|---|---|---|
| M1 | Envelope autocorrelation accepted the lag-2 bin (0.100 s) as a "cycle" — a continuity artifact, not periodicity. | Fast-rhythm gate | Accept only interior local maxima with absolute strength ≥0.30, topographic prominence ≥0.08, and ≥3 above-mean window pairs aligned at the winning lag (cycle support). Rejects chance sparse-event coincidences. |
| M2 | Raw threshold crossings counted as "transients" — shredded slow swells (B1: 57, B2: 64) into discrete events. | Onset taxonomy | Each 20 ms energy window carries low/mid/high one-pole spectral fractions. Crossings classified as slow swells, notes, soft onsets, same-process fluctuations, or true transients. |
| M3 | Onsets from near-silence always called "transient". | Silence-origin rule | An onset from near-silence is transient only if attack is fast AND energy falls below half the onset energy within two windows; sustained bursts are note-like. |
| M4 | "Transient layer over noise bed" asserted without separability evidence. | Layer separability | A separate transient layer requires a real nonquiet bed AND event/bed spectral separation. Same-spectrum events described as one process. |
| M5 | Silence between phrases vetoed pitch (B2's hoots missed). | Active-region pitch | Pitch estimated in active regions; quiet gaps no longer veto. Median 551.7 Hz, range 290.9–615.3 Hz recovered for B2. |
| M6 | Octave test checked one exact integer lag (missed B2's lag-28 maximum when strongest was lag-58). | Octave ±2 | Half-lag correction searches ±2 around the divisor for a nearby local maximum. |
| M7 | Content above 4 kHz (B3's 5 kHz whine) silently invisible; analyzer claimed "noise-like". | 4 kHz ceiling honesty | `band_vhi` metric; dominant high-band energy suppresses subharmonic pitch claims and emits an explicit ceiling statement. "Noise-like" qualified as "below ~4 kHz (tonality above ~4 kHz not assessed)". |
| M8 | Slow swells (B1's ~5 s waves) had no detector — the gap M1's artifact filled. | Slow-swell detector | 2 s smoothing, ≥3 s peak separation, ≥2× valley prominence; reports count, median interval, CV. B1: 12 swells, median 5.580 s (human: ~12–15, ~5 s). B2: 5 swells, median 5.290 s (human: 5 phrases). |

### Image

| # | Root cause | Repair | Mechanism |
|---|---|---|---|
| T1 | Texture measured on the 80×45 downscale; fine detail averaged away (B4 called "smooth"). | Native-resolution texture | Full-resolution grayscale retained; texture measured in native 8×8 cells (absolute variance >100). "Mostly smooth" now requires native fraction <0.15 AND downsampled fraction <0.20. B4: native 0.645 → "fine-grained texture". |
| T2 | Orientation from local Sobel-gradient votes; curved structures misclassified (B5's S-ridge called "horizontal"). | Component orientation | Strong edges grouped by mark-at-push flood fill; top components vote via covariance/principal-axis. B5: "mostly diagonal". New "mostly diagonal" output class. |

### Video

Unchanged. B6 output byte-identical to frozen (no regression).

## 3. Before/after rescoring (c2 methodology, same human descriptions)

| Input | Frozen | Repaired |
|---|---|---|
| B1 surf | 5 MATCH / 1 MISS / 2 HALLUC | **9 MATCH / 0 / 0** |
| B2 hoot owl | 3 / 3 / 1 PARTIAL / 2 HALLUC | **7 MATCH / 1 PARTIAL / 0 / 0** (false "noise-like" claim withdrawn) |
| B3 helicopter | 3 / 3 / 1 PARTIAL / 1 HALLUC | **5 MATCH / 2 MISS / 0 / 0** |
| B4 forest | 5 / 1 WEAK / 1 HALLUC | **6 MATCH / 1 WEAK / 0** |
| B5 dunes | 4 / 1 / 1 WEAK / 0 | **5 MATCH / 1 WEAK / 0** |
| B6 waterfall | 3 / 0 / 2 WEAK / 1 PARTIAL | 3 / 0 / 2 WEAK / 1 PARTIAL (unchanged) |
| **TOTAL** | **23 / 8 / 4 / 3 / 6** | **35 / 2 / 4 / 2 / 0** |

**Hallucinations: 6 → 0.** Misses: 8 → 2 (both are B3's 5 kHz whine, above the honest 4 kHz pitch ceiling).

## 4. Surviving limitations (named precisely)

1. **4 kHz pitch ceiling.** Tonal content above ~4 kHz (B3's 5 kHz whine) is not pitch-estimated and not assessed for tonality. The analyzer now says so explicitly instead of claiming "noise-like". Extending the pitch search to shorter lags risks octave errors; not attempted.
2. **Wandering-period fast modulation unreported.** B3's blade-pass chop (~7 Hz, period drifting with Doppler) does not produce a stable fixed-lag autocorrelation peak. The detector requires a stable period; the chop is withheld ("no slow amplitude cycle detected" — true, but the fast ripple goes unmentioned). A high-passed-envelope ripple detector was prototyped and REJECTED: its gates were too lax (false positives on slow-drift fixtures) or too strict (missed B3 anyway). Documented as a capability gap, not a silent behavior.
3. **Curved-ridge orientation imperfect.** Synthetic S-curves can classify as "mostly horizontal" when component curvature conflicts. The conservative fallback (withhold on conflict) is not yet implemented.
4. **Format barrier.** Modes parse WAV, PPM, and a PPM-frame prefix directly. This does not satisfy the long-term "no format barrier" requirement. A format-independent intake layer is future work.
5. **Connected-component allocations** are proportional to image size; bounds audited but large images use significant memory.

## 5. Boundary battery (deterministic fixtures, pre-freeze)

| Fixture | Result |
|---|---|
| True 7 Hz AM | `env_period_ms 140` ✓ |
| Slow monotonic/drifting shoulder | Rhythm withheld ✓ |
| True 5 s AM | Fast withheld; 3 slow swells, median 5.000 s ✓ |
| Sparse irregular impulses | Rhythm withheld ✓ |
| Periodic tonal bursts | 2.000 s rhythm ✓ |
| Continuous 3 Hz AM | 0.340 s rhythm ✓ |
| Irregular tonal phrases | Fast withheld ✓ |
| 6 kHz-dominant tone | Pitch withheld with explicit ceiling; no false "noise-like" ✓ |
| 2 px checkerboard | Native texture 1.000; fine-grained ✓ |
| Smooth gradient | Native texture 0.000; mostly smooth ✓ |
| Diagonal ridge | Mostly diagonal ✓ |
| B4 forest | Mostly vertical; native texture 0.645; fine-grained ✓ |
| B5 dunes | Mostly diagonal; native 0.240; texture correctly withheld ✓ |

## 6. Freeze record

- Source SHA-256: `bca267201da64c1e2f3a618e28bdb3a6436d5ed202691e05f4a873bf29f57a30`
- Binary SHA-256: `53caf89911b80d99e7a70b3b0e52638af3fd5e72de25c5bb729554693b194eae`
- Toolchain: `znc 2026.07.0-dev (edition 2026)`
- Determinism: every output run twice, byte-identical (verified 2026-09-26).

## 7. Confirmatory protocol (to be executed post-freeze)

Per the binding order: (1) freeze, (2) acquire fresh novel inputs, (3) `git hash-object` audit every original against the repo object store (all must 404), (4) independently prepare and SHA-256-seal human descriptions BEFORE analyzer execution, (5) run every input twice requiring byte identity, (6) c2-format worksheets, (7) binding verdict. **Any hallucination fails.**
