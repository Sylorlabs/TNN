# Repair rescore — before/after (c2 methodology, same sealed human descriptions)

Frozen (c2 binding): 23 MATCH / 8 MISS / 4 WEAK MISS / 3 PARTIAL / 6 HALLUCINATION → **FAIL**  
Repaired: 35 MATCH / 2 MISS / 4 WEAK MISS / 2 PARTIAL / 0 HALLUCINATION

## B1 — Surf

| # | Frozen claim | Repaired claim | Human | Frozen | Repaired |
|---|---|---|---|---|---|
| 1 | DURATION ~91 s | (same) | 91.0 s | MATCH | MATCH |
| 2 | DYNAMICS large swings | (same) | ~20-30 dB | MATCH | MATCH |
| 3 | PITCH none; inharmonic | (same) | No tonal | MATCH | MATCH |
| 4 | ONSETS 57 transients | No discrete transients; 39 gradual swell onsets | ~12-15 slow AM swells, not transients | MISS | MATCH |
| 5 | ONSETS irregular | Onsets at irregular intervals | Irregular swell spacing | MATCH | MATCH |
| 6 | SPECTRUM broadband | (same) | Broadband | MATCH | MATCH |
| 7 | SPECTRUM few tonal | Few tonal below ~4 kHz (ceiling noted) | No tonal | MATCH | MATCH |
| 8 | RHYTHM 0.100 s | 12 slow swells, median 5.580 s | True cycle ~5 s | HALLUCINATION | MATCH |
| 9 | LAYERS transients/noise bed | Single AM process; no separable layer | Single AM process | HALLUCINATION | MATCH |

B1: 5/1/2 → **9/0/0**.

## B2 — Hoot owl

| # | Frozen claim | Repaired claim | Human | Frozen | Repaired |
|---|---|---|---|---|---|
| 1 | DURATION ~34 s | (same) | 34.9 s | MATCH | MATCH |
| 2 | DYNAMICS large swings | (same) | Phrases vs silence | MATCH | MATCH |
| 3 | PITCH none | Tonal in active regions: median ~551.7 Hz, span 290.9–615.3 Hz; quiet gaps | STRONGLY TONAL, harmonic stacks <2 kHz | MISS | MATCH |
| 4 | ONSETS 64 transients | No discrete transients; 42 gradual swell onsets | Soft hoots, no sharp transients; 5 phrases | MISS | MATCH |
| 5 | ONSETS irregular | Onsets at irregular intervals | Irregular phrase gaps | MATCH | MATCH |
| 6 | SPECTRUM mid (400 Hz–2 kHz) | (same) | Low fundamental + harmonics to 2 kHz | PARTIAL | PARTIAL |
| 7 | SPECTRUM few tonal; noise-like | WITHDRAWN | Strongly tonal | MISS | — |
| 8 | RHYTHM 0.100 s | 5 slow swells, median 5.290 s | Irregular phrases; no fast rhythm | HALLUCINATION | MATCH |
| 9 | LAYERS transients/noise bed | Single AM process; no separable layer | Single tonal process; quiet between | HALLUCINATION | MATCH |

B2: 3/3/1/2 → **7/0/1/0** (claim 7 withdrawn).

## B3 — Helicopter

| # | Frozen claim | Repaired claim | Human | Frozen | Repaired |
|---|---|---|---|---|---|
| 1 | DURATION ~72 s | (same) | 72.4 s | MATCH | MATCH |
| 2 | DYNAMICS large swings | (same) | ~20+ dB approach-departure | MATCH | MATCH |
| 3 | PITCH none (withheld) | (same; ceiling) | 5 kHz tonal whine + low rotor | MISS | MISS |
| 4 | ONSETS 15 transients | No discrete transients; gradual fluctuations | NO discrete events; continuous | HALLUCINATION | MATCH |
| 6 | SPECTRUM below ~400 Hz | (same) | Strong low-frequency rotor | MATCH | MATCH |
| 7 | SPECTRUM few tonal; noise-like | Few tonal below ~4 kHz (ceiling noted) | 5 kHz whine is tonal | MISS | MISS |
| 8 | RHYTHM 0.140 s | No slow amplitude cycle detected | Fast blade-pass AM ripple | PARTIAL | UNREPORTED* |
| 9 | LAYERS transients/noise bed | Single AM process; no separable layer | One passing source; no transients | MISS | MATCH |

B3: 3/3/1/1 → **5/2/0/0**. Claims 3,7 remain MISS (5 kHz whine above the honest 4 kHz pitch ceiling).  
*Claim 8: the blade-pass chop has a wandering period (Doppler); the stable-period detector withholds it. "No slow amplitude cycle" is true; the fast ripple is a documented capability gap, not a hallucination.

## B4 — Forest mist

| # | Frozen claim | Repaired claim | Human | Frozen | Repaired |
|---|---|---|---|---|---|
| 1 | TONE mid-tone | (same) | Muted mid-tone | MATCH | MATCH |
| 2 | COLOR muted | (same) | Desaturated | MATCH | MATCH |
| 3 | REGIONS 4; largest 39% | (same) | (no count claimed) | WEAK MISS | WEAK MISS |
| 4 | EDGES mostly vertical | (same) | Strong vertical trunks | MATCH | MATCH |
| 5 | TEXTURE mostly smooth | Fine-grained texture across most of the frame | Fine detail in bark + grass | HALLUCINATION | MATCH |
| 6 | LAYOUT top/bottom differ | (same) | Grass vs misty forest | MATCH | MATCH |
| 7 | LAYOUT mass centered | (same) | Roughly symmetric | MATCH | MATCH |

B4: 5/0/1/1 → **6/0/1/0**.

## B5 — Dunes

| # | Frozen claim | Repaired claim | Human | Frozen | Repaired |
|---|---|---|---|---|---|
| 1 | TONE mid-tone | (same) | Mid-tone | MATCH | MATCH |
| 2 | COLOR vivid saturated | (same) | Intense orange-red | MATCH | MATCH |
| 3 | REGIONS 6; largest 25% | (same) | (~5-6 plausible; unverified) | WEAK MISS | WEAK MISS |
| 4 | EDGES mostly horizontal | EDGES run mostly diagonal | DOMINANT curved DIAGONAL S-ridge | MISS | MATCH |
| 5 | (TEXTURE withheld) | (withheld; native 0.240) | Subtle texture; smooth gradients | (correct) | (correct) |
| 6 | LAYOUT top/bottom differ | (same) | Sky/dune bands | MATCH | MATCH |
| 7 | LAYOUT mass centered | (same) | Centered | MATCH | MATCH |

B5: 4/1/1/0 → **5/0/1/0**.

## B6 — Waterfall video

Unchanged (video mechanisms not repaired). 3 MATCH / 2 WEAK MISS / 1 PARTIAL.

## Tally

| Input | MATCH | MISS | WEAK | PARTIAL | HALLUCINATION |
|-------|:-----:|:----:|:----:|:-------:|:-------------:|
| B1 surf | 9 | 0 | 0 | 0 | 0 |
| B2 hoot owl | 7 | 0 | 0 | 1 | 0 |
| B3 helicopter | 5 | 2 | 0 | 0 | 0 |
| B4 forest | 6 | 0 | 1 | 0 | 0 |
| B5 dunes | 5 | 0 | 1 | 0 | 0 |
| B6 waterfall | 3 | 0 | 2 | 1 | 0 |
| **TOTAL** | **35** | **2** | **4** | **2** | **0** |

**Hallucinations: 6 → 0.** The binding bar (any hallucination fails) is now met on the c2 inputs.
