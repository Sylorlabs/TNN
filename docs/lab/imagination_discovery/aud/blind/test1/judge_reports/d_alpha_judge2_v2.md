# BLIND TEST-1 ballot — package D-ALPHA — judge2 (v2)

**Role:** blind native critic. Did not build any clip, never encountered them, cannot hear — signal numbers only.
**Method:** `measure_test1.py` output + synth-smell fingerprint theory + the preregistered baseline/override/confidence rules. S = mean(s1..s5), verified by recomputation (0.3698 / 0.2861 / 0.5061).
**S gaps:** top−mid = 0.1363, mid−bot = 0.0837.

## 1. Per-clip table

| clip | s1 (rhythm periodicity) | s2 (stationarity) | s3 (near-exact repeats) | s4 (transient symmetry) | s5 (formant stability) | S | key A-NATIVE notes | label | confidence | one-line evidence |
|---|---|---|---|---|---|---|---|---|---|---|
| clip_1 | 0.6171 | 0.0000 (flux_cv 3.76, rms_cv 1.89) | 0.3374 | 0.8945 (43 events, 1.43/s) | 0.0000 (centroid_cv 0.78) | 0.3698 | dc 9.5e-6; hiss_ratio 0.496 (prominent HF bed); hf_flatness 0.88 (flat, white-noise-like HF); clips 0; **clicks 7409 (~247/s)**; most transients of any clip | fork render | LOW | Periodic event rhythm (highest s1) + 33.7% near-exact 1-s chunk reuse (highest s3) say *constructed*; breathing envelope (s2=0) and moving formants (s5=0) rule out the stationary-bed synth signature |
| clip_2 | 0.4454 | 0.0000 (flux_cv 1.39, rms_cv 1.37) | 0.0246 | 0.9606 (12 events, 0.40/s) | 0.0000 (centroid_cv 0.66) | 0.2861 | dc 2.2e-6; hiss_ratio 0.019 (no artificial HF bed, lowest); hf_flatness 0.79; clips 0; **clicks 9219 (~307/s — anomaly, noted below)**; few soft transients | real recording | MEDIUM | Lowest periodicity, near-zero repeats (s3 0.02), breathing ambience, moving formants; lone blot is s4 computed on only 12 transients |
| clip_3 | 0.5012 | **0.4399** (flux_cv 0.52, rms_cv 0.38 — only stationary texture) | 0.1232 | 0.8794 (17 events, 0.57/s) | **0.5868** (centroid_cv 0.14 — static formants) | 0.5061 | dc 1.0e-7 (lowest); hiss_ratio 0.067; hf_flatness 0.53 (least noise-like); clips 0; clicks 551 (fewest); lowest transient density | synth control | LOW | Only clip with a stationary texture (s2) and static formants (s5) = filtered-noise-bed + fixed-resonator synth signature |

## 2. Forced ranking by realness

1. **clip_2** — most likely a real field recording
2. **clip_1** — constructed, but lively (breathing envelope, moving formants, dense discrete events)
3. **clip_3** — least likely real (stationary texture, static formants)

## 3. Overrides

**None. The preregistered baseline stands:** highest S → synth control (clip_3, 0.5061); lowest S → real recording (clip_2, 0.2861); middle S → fork render (clip_1, 0.3698).

**Why no override despite dissenting fingerprints:** the three dissents on the top-S clip's rank are spikes on *other* clips, not weaknesses in clip_3's own synth evidence — clip_1 owns s1 (0.6171 periodicity) and s3 (0.3374 looping); clip_2 owns s4 (0.9606, on only 12 transients). clip_3's s2 (0.4399, the only nonzero stationarity; rms_cv 0.38 vs 1.89/1.37) and s5 (0.5868, the only nonzero formant stability; centroid_cv 0.14 vs 0.78/0.66) are exactly the filtered-noise-bed + fixed-resonator fingerprints the agreed theory defines for synth; it also has the lowest transient density (0.57/s) and the fewest clicks. An override would require fingerprint evidence that clip_3 is *less* synth-like than another clip on the synth-defining dimensions — the evidence runs the other way. clip_1's construction markers (periodic rhythm, 33.7% chunk reuse, 7409 clicks, flat HF bed at hiss_ratio 0.50) combined with its breathing envelope and moving formants read as an assembled-but-lively construction — consistent with the fork render, not with the steady-bed synth architecture, and its near-exact repetition rules out the real recording. clip_2 owns the real-leaning fingerprints (lowest s1, lowest s3 by far, s2=0, s5=0, no HF bed).

**A-NATIVE anomalies noted (not identity evidence, per the frozen rule):** clip_1 and clip_2 carry very high click counts (7409 / 9219 ≈ 247–307/s) — consistent with hard-edged concatenation artifacts rather than anything about the brief; clip_1 carries a prominent flat high-frequency bed (hiss_ratio 0.496, hf_flatness 0.88). Neither anomaly changes the fingerprint-based identities.

## 4. Confidence accounting (frozen rule, applied mechanically)

- **clip_3 "synth control":** both gaps ≥ 0.05 (0.1363, 0.0837), but 3 fingerprints dissent on the top-S rank (s1→clip_1, s3→clip_1, s4→clip_2) → **LOW**. (MEDIUM's conditions are also met, but LOW's "≥2 fingerprints dissent" clause is written as a disqualifier — it takes precedence, otherwise it could never fire when gaps ≥ 0.05.)
- **clip_2 "real recording"** (symmetric analog of the rule): both gaps ≥ 0.05; 1 clean dissent (s4), with s2/s5 tied at 0.0 with clip_1 → **MEDIUM**.
- **clip_1 "fork render":** residual label assigned by elimination; bounded by the weaker of the other two → **LOW**.

## 5. DISCLOSURE

- I opened **only** the three listed clip files (reads performed by the measurement tool) — nothing else. I did **not** open anything under `.../blind/test1/keys/` (sealed mappings), no other files, no script internals.
- I recognized **none** of the clips; I had never encountered them. I cannot hear; I analyzed signal numbers only.
- I used **no web search** and **no prior knowledge of the forks** — the verdict was reached from the tool numbers, the fingerprint theory, and the preregistered baseline/override/confidence rules alone.
- **This ballot is VALID (not void).**
