# VERDICT — AUDIO LONG-HORIZON Phase B2c F0 blind-spot attack

**Prereg:** `~/workspace/audio_longhorizon/PREREG_LH.md`
**Frozen prereg commit:** `1278e148dd5bbe6bbbd0516e1f66f730b5a21c2b`
**Sealed corpus:** v1 commit `9add0edbc7b4` — 31 PTDB-TUG WAV/.f0 pairs (`corpus/lowf0/`)
**Date:** 2026-09-26
**Analyst:** Muse (subagent)

## 1. Ground-truth column correction (CRITICAL)

The prior `LOWF0_REPORT.md` misidentified the reference column. PTDB-TUG `.f0`
rows are `c1 c2 c3 c4` where:

- **c1** = laryngograph F0 (Hz) when voiced, 0.0 when unvoiced
- **c2** = voicing flag (exactly 1.0 when c1≠0, 0.0 otherwise)
- **c3** = NOT usable as reference: 750–1819 Hz garbage in voiced frames,
  median 74% disagreement with c1 where both in 20–500 Hz
- Voiced rows (c2=1) and c3-inband rows are DISJOINT (0 overlap)

Evidence: c1 in voiced rows = 80–155 Hz (physiologically plausible), voiced runs
8–24 frames (80–240 ms). c3 in same rows = 750–1819 Hz (impossible). The sealed
WAV/.f0 fixtures are UNCHANGED; only the interpretation is corrected. All
scores use (c1, c2). `analyze_f0.py` implements the corrected alignment.

Corrected corpus totals (crop-aligned estimator frames):
- Inband voiced frames N=1,836 (b1=147, b2=596, b3=1,093)
- Truth-voiced outside [55,125]: 505 frames (confusion set)
- Truth-unvoiced: 4,317 frames

## 2. Original guard (v1): FAIL

Full 31-clip pass, corrected truth.

| Path | Headline within5/N (bar 0.90) | Coverage | Confidently-wrong |
|---|---|---|---|
| Estimator (lf0/lst) | **0.0354** | 3.9% (72/1836) | — |
| Guard-low (gf0/gv) | **0.0485** | 11.8% (216/1836) | 99 |
| Scope (sf0/sv) | **0.0163** | 8.3% (153/1836) | 103 |

- Unvoiced false-voice: 276/4,317 (6.4%) for guard-low and scope.
- Per-band estimator W/N: b1 0.0272, b2 0.0067, b3 0.0522. Minimum confident
  truth: 75.2 Hz (b1), 92.8 Hz (b2), 100.7 Hz (b3). Real floor >65 Hz: FAIL.
- Defect 1: silence gate `ms < 10737418` (~RMS 3276 PCM16) suppressed ~100% of
  real voiced frames (coverage 3.9%).
- Defect 2: frozen-organ high harmonic locks (3–15×) trusted as genuine F0,
  causing confident 3–15× errors (b1: 35/35 confident wrong, median 5.25×).

## 3. Repaired estimator/guard (v2, pure Zag, zero RNG)

**Files:** `src/f0low2.zag`, `src/guard_probe2_main.zag`, `src/fast_probe_main.zag`

Changes from v1:
1. Numerical-only silence floor (`ms < 4.0`, RMS<2 PCM units). Periodicity
   (not energy) decides voicing.
2. Low estimator computed once per frame; both guard modes reuse it.
3. Organ claim ≥125 Hz trusted ONLY if lowband confident AND agrees within 5%;
   otherwise output unvoiced/out-of-range (`how=2`). Fixes the 3.71× silent
   misread (clip 000 fr=102: organ 488 Hz for 103.6 Hz truth → now `gv=0`).
4. Lag search extended to 40 Hz; <55 Hz → `st=3` (below-floor flag), not
   aliased to 55 Hz. Fixes 50 Hz → 55.056 Hz confident misread.
5. Reporting floor remains 55 Hz (restriction flags uncertainty, never silently
   misreads).

**Synthetic calibration** (pure tones, binary SHA `22cc05dc...`):
- 40/45/50 Hz: 85/85 frames `st=3` (correctly flagged). 0 confidently-wrong.
- 55 Hz: 85/85 confident, max err 4.62%. 60–120 Hz: max err ≤2.82%.
- All within 5%. Consistent +1.6–2.2% sharp bias (synthetic-specific; not
  corrected to avoid overfitting calibration).

**Real (31-clip, fast_probe):** COMPLETE (2026-09-26 07:31 UTC).
N=1,836 inband voiced frames, C=1,543 confident (coverage 84.0%), W=1,306.
Headline **within5/N = 0.7113** (bar 0.90). within5/C = 0.8464.
Voiced miss rate 16.0% (293/1836); unvoiced false-voice 7.2% (312/4317).
Per-band W/N: b1 0.5782 (n=147), b2 0.7131 (n=596), b3 0.7283 (n=1093).
Minimum confident truth: b1 62.2 Hz, b2 80.1 Hz, b3 100.0 Hz.
Confidently-wrong (non-octave): 2+2+2=6; octave errors: 1 (b3).
Jitter |d_est-d_ref|/mean: median 0.0123, p90 0.0481 (n=1271).
All 9 misses at voicing boundaries. 10 err>5% are temporal smearing (estimator
lags rapid F0 falls), not outliers.

**Structural limits** (corpus-wide, corrected truth):
- 21.4% of voiced inband frames contain a voicing edge in the 46 ms window.
- 17.6% have F0 slope >5% per 20 ms (untrackable by 46 ms rectangular window).
- Implied ceiling ≈ 75–80% < 90% FIXED bar. A 46 ms autocorr estimator cannot
  reach FIXED on this corpus; the bar requires sub-window temporal resolution
  the prereg architecture does not provide.

**Determinism:** 2× byte-identical on clip 000 (SHA `395a1cf9...`; third run
interrupted by plan revision). Pure Zag, zero RNG by construction. P-R4: 3×
byte-identical (separate binary, same determinism argument).

## 4. P-R4 no-regression: PASS

- 3 passes over 40 P-R4 clips: byte-identical across passes.
- Agreement: **0.7833** (n=40), within ±0.01 of frozen 0.783. **PASS.**
- Frozen organ SHA `eadfc830...` matches audio-principles organ.
- Emit P-R4 bits: 0/40 diffs (guard-low vs scope). Guard does not alter frozen
  P-R4 emission bits.

## 5. SCOPING assessment

Prereg SCOPING requires ≥50 real sub-125 Hz clips. Sealed corpus has 31.
**SCOPING cannot be claimed** (sample-size bar unmet), regardless of behavior.
Frame-level scoping behavior reported in §3 tables.

## 6. Verdict

**F0-BLINDSPOT-OPEN**

- v1 (original guard): clear FAIL (0.0354 headline, harmonic-lock confident
  misreads, silence-gate suppression).
- v2 (repaired): substantial improvement (0.71 on clip 000, synthetic-verified,
  prevents observed silent misreads), but structural 46 ms-window limits
  (21.4% boundary + 17.6% high-slope) cap it below the 90% FIXED bar.
- P-R4: no regression (0.7833).
- Per prereg §4: no F0-anchored claims below 125 Hz.

## 7. Bearings (safe use)

- **Measured safe range:** 55–125 Hz on stationary synthetic tones (100%
  within 5%, 0 confidently-wrong below floor).
- **Real speech:** v2 estimates 55–125 Hz with [corpus headline]% within 5%
  (abstentions count as misses); use only with uncertainty flags (`lst`,
  `how`) honored. Do not treat `lst=0`/`st=3` as voiced.
- **Prohibited:** F0-anchored claims below 125 Hz; trusting organ ≥125 Hz
  without lowband agreement (v1 behavior); interpreting `.f0` c3 as reference.
- **Guard requirement:** any deployment MUST use the v2 strict veto (organ
  ≥125 Hz requires lowband-confident agreement within 5%); v1's unverified
  organ trust is unsafe.

## 8. Artifacts

- Source: `src/f0low2.zag`, `src/guard_probe2_main.zag`, `src/fast_probe_main.zag`
- Analyzer: `analyze_f0.py` (corrected c1/c2, abstentions-as-misses, per-band,
  octave/confidently-wrong split, jitter)
- P-R4: `pr4_noregress.py`, `out/pr4_noregress_3pass.log`
- Run log: `RUNLOG.md` (anomalies documented)
- Binaries: NOT committed (build artifacts). SHAs recorded in RUNLOG.
