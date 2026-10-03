# BLIND TEST-1 — Native Critic Ballot (package B-ALPHA, judge3_v2)

## 0. Method
Ran the sanctioned measurement tool once on exactly the three listed clips. No other
files were opened (in particular nothing under `keys/`), no web search, no prior
exposure to any fork output. All numbers below are signal-only tool output.

## 1. Per-clip results

| clip | s1 periodicity | s2 stationarity | s3 loop | s4 symmetry | s5 formant-stab | S | A-NATIVE notes | label | confidence | one-line evidence |
|---|---|---|---|---|---|---|---|---|---|---|
| clip_1 | 0.8744 | 0.0000 | 0.0714 | 0.7759 | 0.6261 | **0.4696** | hiss_ratio 0.317 (highest), hf_flatness 0.796 (highest/flattest high band), 5790 clicks, 0.97 transients/s, dc ~5.6e-6, no clipping | **synth control** | LOW | Strong envelope periodicity (0.8744, top rank) + flat high-band hiss bed + most symmetric transients; reads as a looped/bedded construct |
| clip_2 | 0.6323 | 0.1877 | 0.0764 | 0.7273 | 0.3421 | **0.3932** | hiss_ratio 0.071, hf_flatness 0.534, 1437 clicks, only 0.17 transients/s (5 transients), dc ~4.2e-7, no clipping | **fork render** | LOW | Middle S by baseline; mild stationarity and modest periodicity, neither texture of the bed nor the chaos of the wild |
| clip_3 | 0.6929 | 0.0000 | 0.0000 | 0.7231 | 0.3387 | **0.3509** | hiss_ratio 0.050 (lowest), hf_flatness 0.559, 872 clicks (fewest), 0.13 transients/s (4 transients), highest spectral variability (flux_cv 1.73, centroid_cv 0.231), no clipping | **real recording** | LOW | Zero near-exact repetition, lowest formant stability, highest flux/centroid variability — messy, breathing, non-repeating signal |

Notes on the fingerprints:
- s2 hits its 0.0 clip for both clip_1 and clip_3 (tie): neither has a stationary
  spectral-flux bed. clip_2 is the most stationary (0.1877) but only mildly so.
- s3: clip_2 is top (0.0764) vs clip_1 0.0714 — the single dissenting fingerprint
  for the top-S clip. Both values are small; this is a weak dissent, not a strong
  repetition signature anywhere.
- s4 is near-flat across clips (0.72–0.78); discriminative weight is low.
- s1 and s5 drive clip_1's top-S rank: envelope periodicity 0.8744 (far the
  highest) and formant stability 0.6261 (far the highest).

## 2. Forced ranking by "most likely to be a real field recording"

1. **clip_3** (lowest syntheticity, S = 0.3509)
2. **clip_2** (middle, S = 0.3932)
3. **clip_1** (highest syntheticity, S = 0.4696)

## 3. Overrides

**No override.** I considered one: clip_1's top-S rank is driven mainly by
s1/s4/s5 while s3 dissents (clip_2 edges it 0.0764 vs 0.0714). I keep clip_1 as
the synth control because the dissent is quantitatively weak (both s3 values are
tiny and the gap is 0.005) and the corroborating evidence is strong: clip_1 has
by far the highest envelope periodicity (0.8744 — rhythmic regularity, the
classic loop fingerprint), the flattest/most energetic high-band hiss
(hiss_ratio 0.317, hf_flatness 0.796 — a stationary hiss bed under the
envelope, which is exactly how one games flatness bars), the most symmetric
transients, and the most stable centroid on high-energy frames. No fingerprint
constellation in clip_2 or clip_3 reads more synth-like than that combination.
Baseline stands.

Confidence note: gaps are top−middle = 0.0764 and middle−bottom = 0.0423.
One gap is below 0.05, and one fingerprint dissents, so per the preregistered
rule this is **LOW confidence** on every label despite a coherent overall
picture. The middle clip (fork) and bottom clip (real) are only 0.0423 apart —
this ballot is an educated guess on clip_2 vs clip_3, while the clip_1 =
synth-control call is the comparatively firm one.

## 4. DISCLOSURE

- I opened exactly the three listed `.wav` files via the sanctioned measurement
  tool. I opened nothing under `.../blind/test1/keys/`, nothing else in the
  test tree, and no other audio anywhere.
- I recognized none of the clips — I have never heard, measured, or seen any of
  these signals before, and I did not build any of the forks.
- I used no web search and no information beyond the tool's numbers and the
  fingerprint theory stated in the task.
- **My ballot is not void.** (Had any of the above been violated, I would have
  said so here.)
