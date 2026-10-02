# BLIND TEST-1 — Native Critic Report (b_alpha, judge1)

Package: B-ALPHA. Method: signal-only analysis of the three WAV files via
`measure_test1.py`. No listening, no keys, no other files opened.

## 1. Per-clip results

| clip | s1 (periodicity) | s2 (stationarity) | s3 (loops) | s4 (symmetry) | s5 (fixed ring) | S | key A-NATIVE notes | label | conf | one-line evidence |
|---|---|---|---|---|---|---|---|---|---|---|
| clip_1.wav | 0.8744 | 0.0000 | 0.0714 | 0.7759 | 0.6261 | **0.4696** | dc ~0, 0 clips, **5790 clicks**, hiss_ratio 0.317, hf_flatness 0.796, 29 transients @0.97/s | **synth control** | LOW | Highest S by clear margin; extreme envelope periodicity (s1=0.8744) + symmetric transients + fixed formants |
| clip_2.wav | 0.6323 | 0.1877 | 0.0764 | 0.7273 | 0.3421 | 0.3932 | dc ~0, 0 clips, 1437 clicks, hiss_ratio 0.071, hf_flatness 0.534, 5 transients @0.17/s | **fork render** | LOW | Middle S; S-gap to real < 0.05 |
| clip_3.wav | 0.6929 | 0.0000 | 0.0000 | 0.7231 | 0.3387 | **0.3509** | dc ~0, 0 clips, 872 clicks, hiss_ratio 0.050, hf_flatness 0.559, 4 transients @0.13/s | **real recording** | LOW | Lowest S; zero near-exact repetitions (s3=0.0), most mobile formants (s5=0.3387), lowest hiss |

S ranking: clip_1 (0.4696) > clip_2 (0.3932) > clip_3 (0.3509).
Gaps: top−mid = 0.0764, mid−low = 0.0423.

Fingerprint top-S agreement check (who is "most synth-like" per fingerprint):
- s1: clip_1 (0.8744) — agrees
- s2: clip_2 (0.1877) — dissents (all values near zero)
- s3: clip_2 (0.0764 vs 0.0714) — dissents (absolute spread tiny)
- s4: clip_1 (0.7759) — agrees
- s5: clip_1 (0.6261) — agrees

## 2. Forced ranking by "most likely a real field recording"

1. **clip_3** — lowest S; zero loop signatures, moving formants, least high-band hiss
2. **clip_2** — middle S; close to clip_3 (gap 0.0423)
3. **clip_1** — least likely; periodic envelope, symmetric transients, fixed rings, 5790 digital clicks

## 3. Overrides

**None.** The baseline stands (highest S → synth control, lowest S → real,
middle → fork render). Notes on why no override was taken:

- clip_1's lead is driven by the three structurally most diagnostic
  fingerprints: s1 envelope periodicity at 0.8744 (nearly locked-in rhythm —
  the strongest synth tell in the set), s4 transient symmetry 0.7759, and
  s5 formant stability 0.6261 (nearly double the other two).
- The two dissenting fingerprints carry weak evidence: s2's maximum across
  all clips is 0.1877 (all three are effectively non-stationary on this
  metric) and s3's spread is 0.0764 vs 0.0714 vs 0.0000 — near-tied at the
  top, so clip_2's "win" there is negligible.
- A-NATIVE corroborates rather than contradicts: clip_1 has 5790 detected
  clicks (digital artifact signature inconsistent with a clean field
  recording) plus the highest high-band hiss energy (hiss_ratio 0.317,
  hf_flatness 0.796 — a stationary high-band noise component, i.e. filtered-noise bed).

## 4. Confidence

Per the frozen rule: HIGH needs both gaps ≥ 0.10 AND all five fingerprints
agreeing on the top-S clip. Here top−mid = 0.0764 (< 0.10), mid−low = 0.0423
(< 0.05), and two fingerprints (s2, s3) dissent on the top-S rank.

**Confidence: LOW for all three labels.** The synth-control call (clip_1) is
the most secure of the three — its S margin (0.0764) and three of five
fingerprints, plus the click artifact, all point the same way. The real-vs-fork
call (clip_3 vs clip_2) is genuinely uncertain: the gap is 0.0423 and both
are plausible renders.

## 5. DISCLOSURE

- I opened NOTHING beyond the three listed clip files and the measurement
  script output. I did not open anything under `.../blind/test1/keys/`,
  did not visit any other package, doc, or directory, and did not run any
  other tool.
- I recognized none of the clips and have no prior knowledge of the forks
  (b_alpha label only).
- No web search was used. All judgments come solely from the five
  fingerprint numbers plus the A-NATIVE anomaly notes per the preregistered
  theory.
- **Ballot is valid** (no blindness rule violated).
