# RUNLOG — Phase B2c: F0 blind-spot attack on real material

## Prereg bars (PREREG_LH §4)
- **FIXED** iff, on real low-F0 material (55–125 Hz, voiced per the frozen
  analyzer): resolution floor ≤ 65 Hz; |f0_meas − f0_ref|/f0_ref ≤ 5% on
  ≥ 90% of voiced frames; per-band error bounds reported (55–80, 80–100,
  100–125 Hz); 3× byte-identical determinism retained; NO regression —
  the P-R4 anchor re-run within ±0.01 of the frozen baseline (0.783).
- **SCOPING WORKS** iff: the organ contract is amended to state the measured
  125 Hz effective floor; on a probe battery of ≥ 50 sub-125 Hz real clips,
  ≥ 95% are reported unvoiced or f0 = 0, and 0% are confidently-wrong
  (voiced = 1 with f0 in [80,1200] Hz). Any confident-wrong = SCOPING-FAIL.
- Neither → **F0-BLINDSPOT-OPEN**: no F0-anchored gate or loop may claim
  validity below 125 Hz, recorded as a standing restriction.

## Method
- Sealed corpus: 31 PTDB-TUG mic+laryngograph pairs (corpus/lowf0/),
  manifest commit 9add0edbc7b4. Wiring crew's guard: wiring/src/f0low.zag.
- New probe binary (pure Zag, zero RNG): src/guard_probe_main.zag =
  organ_lib.zag + f0low.zag + per-frame dump (organ f0/voiced, lowband
  estimator lf0/lst, guard-low gf0/gv/ghow, guard-scope sf0/sv/show).
  Build: build/guard_probe_full.zag, binary build/guard_probe.
- Alignment: 5.0 s WAV window at manifest window_start_s into the original
  PTDB utterance; .f0 = 10 ms frames over the original. Estimator frame f
  centers at (f*1024+1024)/44100 s clip-time → ref frame k =
  round((t + window_start)/0.01 − 0.5). Alignment verified by offset sweep
  (see evidence).
- "Voiced" ground truth = laryngograph F0 in [55,125] Hz (inband), per
  corpus/LOWF0_REPORT.md banding.
- Offline analyzer (examiner): analyze_f0.py. Zag produces, Python scores.

## Anomalies
(none yet)

## Runs
- R1: guard_probe over 31 pairs, pass 1 (byte-identity set 1).

## 2026-09-26 ~05:30 UTC — Ground-truth column correction (CRITICAL)

**The LOWF0_REPORT.md column identification was wrong.** PTDB-TUG .f0 rows are
`c1 c2 c3 c4` where:
- c2 = laryngograph voicing flag (1.0 = voiced, 0.0 = unvoiced)
- c1 = laryngograph F0 (Hz) when voiced, 0.0 when unvoiced
- c3 = NOT the reference F0: garbage (750–1819 Hz) exactly in voiced frames,
  median 74% disagreement with c1 where both present
- Voiced rows (c2=1) and c3-inband rows are DISJOINT (0 overlap in 2/3 clips)

Evidence: c1 in voiced rows = 80–155 Hz (physiologically plausible), voiced
runs 8–24 frames (80–240 ms, plausible segments). c3 in the same rows =
750–1819 Hz (impossible). The sealed WAV/.f0 fixtures are unchanged; only the
interpretation is corrected. `analyze_f0.py` now uses (c1, c2).

Corrected corpus totals: 4,312 voiced+inband reference frames (was "5,743"
under the wrong column). Bands: b1=362, b2=1396, b3=2554. Plus 1,158
truth-voiced frames with F0 outside [55,125] (unvoiced/confusion test set).

## 2026-09-26 ~05:35 UTC — Original guard scored on correct truth: FAIL

- Estimator headline within5/N = 0.0354 (bar 0.90). Coverage 3.9% (silence gate).
- Guard-low headline = 0.0485; 99 confidently-wrong on inband truth (b1: 35/35
  wrong, median err 5.25x; b2: 17/23; b3: 51/158). Unvoiced false-voice 6.4%.
- Scope headline = 0.0163; 103 confidently-wrong. Not scoping.
- Both paths fail -> v2 (repaired estimator + strict guard) is the candidate.

## 2026-09-26 ~05:40 UTC — v2 defects found and fixed on clip 000

1. Below-floor aliasing: 50 Hz synth tone confidently reported as 55.056 Hz
   (10% err). Fixed by extending lag search to 40 Hz; <55 Hz now -> st=3.
   Verified: 50 Hz -> 85/85 lst=3.
2. Unverified organ trust: guard trusted organ >=125 Hz when lowband abstained
   (fr=102: 488 Hz reported for 103.6 Hz truth, 3.71x err). Fixed: organ >=125
   trusted ONLY if lowband confident AND agrees within 5%; else out-of-range.
   Applies to guard-low and scope modes.

## 2026-09-26 ~05:45 UTC — Accuracy challenge quantified

Clip 000 v2: N=66, within5/N=0.7121 (bar 0.90). All 9 misses and 5/10 err>5%
are at voicing boundaries. Corpus-wide: 21.4% of voiced inband frames have a
voicing edge within the 46 ms estimator window (ceiling 78.6% if all fail).
The 46 ms window vs 10 ms reference mismatch is the fundamental limit.
P-R4 no-regression: PROVEN (3 passes byte-identical, 0.7833 in [0.773,0.793]).
Emit P-R4 bits: 0/40 diffs low-vs-scope (guard doesn't touch frozen bits).

## 2026-09-26 ~06:00 UTC — v2 synthetic calibration complete

Pure tones via latest fast_probe (SHA 22cc05dc):
- 40/45/50 Hz: 85/85 frames lst=3 (below-floor, correctly flagged). 0 confident.
- 55 Hz: 85/85 lst=1, max err 4.62% (within 5%).
- 60–120 Hz: 100% lst=1, max err ≤2.82% (60 Hz) down to ≤1.41% (105+ Hz).
- Consistent +1.6–2.2% sharp bias on synthetic (matches wiring crew's F0_CHAR
  note). Not corrected: bias appears synthetic-specific (real-material errors
  are scatter, mean +0.7% on clip 000), correcting it would overfit calibration.

## 2026-09-26 ~06:00 UTC — Estimator improvement attempts

- 32 ms window (centered): WORSE (0.6515 vs 0.7121 on clip 000). Shorter window
  increases autocorr mis-selection more than it helps boundaries.
- Hann-tapered 46 ms: ABANDONED (too slow: fcosr per sample, 9+ min/clip).
- Root causes quantified:
  - 21.4% of voiced inband frames contain a voicing edge in the 46 ms window.
  - 17.6% have F0 slope >5%/20 ms (untrackable by 46 ms rectangular window).
  - Real-material err>5% are TEMPORAL SMEARING (estimator lags rapid F0 falls),
    not isolated outliers. Median filter would not help.

## 2026-09-26 ~06:10 UTC — Run plan revised

Original 3×31 sequential run killed (load avg 24 on 2 cores → 15+ hr).
Revised: 3× determinism on clips 000/001/002 (9 runs, proves binary
determinism) + 1× full 31-clip pass (headline number). The 31-clip headline
inherits determinism from the proven binary (pure Zag, zero RNG).
