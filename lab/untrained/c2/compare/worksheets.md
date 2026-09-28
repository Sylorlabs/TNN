# Claim worksheets — c2 confirmatory run (2026-09-26)
Human descriptions sealed 2026-09-26 18:29:57 UTC, BEFORE any analyzer run.
TNN outputs: `out/T-B*_r1.txt` (r2 byte-identical for all six).
Analyzer: frozen c2 (source SHA 826ff003..., binary SHA d4ed41c4...).

Scoring: MATCH / MISS / WEAK MISS / PARTIAL / HALLUCINATION.
A hallucination is a FALSE POSITIVE: TNN asserts structure that is not there.
False positives fail the bar; withholding does not.

---

## B1 — Surf (H-B1 vs T-B1)

| # | TNN claim | Human | Score |
|---|-----------|-------|-------|
| 1 | DURATION ~91 s | 91.0 s | MATCH |
| 2 | DYNAMICS large swings | ~20-30 dB swell vs quiet | MATCH |
| 3 | PITCH none; inharmonic/noise-like (withheld) | No tonal content | MATCH |
| 4 | ONSETS 57 distinct transient events | ~12-15 slow AM swells, not transients | MISS |
| 5 | ONSETS irregular intervals | Irregular swell spacing | MATCH |
| 6 | SPECTRUM broadband low/mid/high | Broadband, thin to 8 kHz | MATCH |
| 7 | SPECTRUM few tonal components | No tonal | MATCH |
| 8 | RHYTHM 0.100 s cycle | True cycle ~5 s (wave swells) | HALLUCINATION |
| 9 | LAYERS transients over noise-like bed | Single AM process; no separate transient layer | HALLUCINATION |

B1: 5 MATCH / 1 MISS / 2 HALLUCINATION.
H-8: the 0.100 s rhythm is the envelope-autocorr lag-2 artifact (same mechanism
as exploratory H1/H2). H-9: phantom transient layer (same as exploratory H3).

---

## B2 — Hoot owl (H-B2 vs T-B2)

| # | TNN claim | Human | Score |
|---|-----------|-------|-------|
| 1 | DURATION ~34 s | 34.9 s | MATCH |
| 2 | DYNAMICS large swings | Phrases vs silence | MATCH |
| 3 | PITCH none; inharmonic/noise-like (withheld) | STRONGLY TONAL, harmonic stacks <2 kHz | MISS |
| 4 | ONSETS 64 distinct transient events | Soft hoots, no sharp transients; 5 phrases | MISS |
| 5 | ONSETS irregular intervals | Irregular phrase gaps | MATCH |
| 6 | SPECTRUM mid (400 Hz-2 kHz) | Low fundamental + harmonics to 2 kHz | PARTIAL |
| 7 | SPECTRUM few tonal; noise-like | Strongly tonal | MISS |
| 8 | RHYTHM 0.100 s cycle | Irregular phrases; no fast rhythm | HALLUCINATION |
| 9 | LAYERS transients over noise-like bed | Single tonal process; quiet (not noisy) between | HALLUCINATION |

B2: 3 MATCH / 3 MISS / 1 PARTIAL / 2 HALLUCINATION.
H-8: lag-2 artifact again. H-9: "noise-like bed" is false (background is quiet);
hoot onsets mischaracterized as transients.

---

## B3 — Helicopter (H-B3 vs T-B3)

| # | TNN claim | Human | Score |
|---|-----------|-------|-------|
| 1 | DURATION ~72 s | 72.4 s | MATCH |
| 2 | DYNAMICS large swings | ~20+ dB approach-departure | MATCH |
| 3 | PITCH none (withheld) | 5 kHz tonal whine + low rotor | MISS |
| 4 | ONSETS 15 distinct transient events | NO discrete events; continuous | HALLUCINATION |
| 5 | ONSETS irregular intervals | (spurious; not scored separately) | — |
| 6 | SPECTRUM below ~400 Hz | Strong low-frequency rotor | MATCH |
| 7 | SPECTRUM few tonal; noise-like | 5 kHz whine is tonal | MISS |
| 8 | RHYTHM 0.140 s cycle | Fast blade-pass AM ripple | PARTIAL |
| 9 | LAYERS transients over noise-like bed | One passing source; no transients | MISS |

B3: 3 MATCH / 3 MISS / 1 PARTIAL / 1 HALLUCINATION.
Notes: the 5 kHz whine is ABOVE the analyzer's 4 kHz pitch ceiling (honest
boundary, documented in tests/boundary_report.txt). Claim 8 (0.140 s) may be
a genuine blade-pass detection (7.1 Hz = "many per second"), but the true
blade frequency is unverified from the plots; scored PARTIAL, not MATCH.

---

## B4 — Forest mist (H-B4 vs T-B4)

| # | TNN claim | Human | Score |
|---|-----------|-------|-------|
| 1 | TONE mid-tone | Muted mid-tone | MATCH |
| 2 | COLOR muted, near-monochrome | Desaturated; fog-washed | MATCH |
| 3 | REGIONS 4; largest 39% | (no region count claimed) | WEAK MISS |
| 4 | EDGES mostly vertical | Strong vertical trunks | MATCH |
| 5 | TEXTURE mostly smooth, little fine detail | Fine detail in bark + grass (foreground) | HALLUCINATION |
| 6 | LAYOUT top/bottom differ strongly | Grass foreground vs misty forest | MATCH |
| 7 | LAYOUT mass centered | Roughly symmetric, no focal object | MATCH |

B4: 5 MATCH / 1 WEAK MISS / 1 HALLUCINATION.
H-5: the "smooth" falsehood recurs (same 80x45-downscale mechanism as
exploratory H4/H5). The human explicitly noted foreground fine detail.

---

## B5 — Dune 45 (H-B5 vs T-B5)

| # | TNN claim | Human | Score |
|---|-----------|-------|-------|
| 1 | TONE mid-tone | Mid-tone | MATCH |
| 2 | COLOR vivid, strongly saturated | Intense orange-red; saturated | MATCH |
| 3 | REGIONS 6; largest 25% | (~5-6 plausible; unverified) | WEAK MISS |
| 4 | EDGES mostly horizontal | DOMINANT is the curved DIAGONAL S-ridge | MISS |
| 5 | (TEXTURE withheld; frac 0.433) | Subtle texture; smooth gradients | (correct withholding) |
| 6 | LAYOUT top/bottom differ strongly | Sky/dune vs plain bands | MATCH |
| 7 | LAYOUT mass centered | Centered | MATCH |

B5: 4 MATCH / 1 MISS / 1 WEAK MISS.
Note: the analyzer correctly WITHHELD the "smooth" texture claim here
(texture_frac 0.433 above threshold) — a genuine improvement over the
exploratory behavior, but it still missed the dominant diagonal ridge.

---

## B6 — Waterfall video (H-B6 vs T-B6)

| # | TNN claim | Human | Score |
|---|-----------|-------|-------|
| 1 | DURATION 14 frames @2 fps (~7 s) | 6.8 s, 14 frames | MATCH |
| 2 | MOTION little consistent; near-static or chaotic | Static camera (yes) BUT localized water motion (missed) | PARTIAL |
| 3 | CUTS none; one continuous shot | One static shot, no cuts | MATCH |
| 4 | BRIGHTNESS darkens over time | (not noted; 110->104, small) | WEAK MISS |
| 5 | COVERAGE motion toward bottom | Water moves (fall left-center, sea right); "bottom" imprecise | WEAK MISS |

B6: 3 MATCH / 1 PARTIAL / 2 WEAK MISS.

---

## Tally

| Input | MATCH | MISS | WEAK | PARTIAL | HALLUCINATION |
|-------|:-----:|:----:|:----:|:-------:|:-------------:|
| B1 surf | 5 | 1 | 0 | 0 | 2 |
| B2 hoot owl | 3 | 3 | 0 | 1 | 2 |
| B3 helicopter | 3 | 3 | 0 | 1 | 1 |
| B4 forest | 5 | 0 | 1 | 0 | 1 |
| B5 dunes | 4 | 1 | 1 | 0 | 0 |
| B6 waterfall | 3 | 0 | 2 | 1 | 0 |
| **TOTAL** | **23** | **8** | **4** | **3** | **6** |

44 scored claims. The bar FAILS: 6 hallucinations (any >0 fails).
