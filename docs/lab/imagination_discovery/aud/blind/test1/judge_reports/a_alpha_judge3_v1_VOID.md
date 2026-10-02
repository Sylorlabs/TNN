# BLIND TEST-1 — Package A-ALPHA — Native Critic Judge 3

**Judge:** blind native critic (judge 3). I did not build any clips and had no prior exposure to them. I cannot hear; this ballot is signal-only, from the output of `measure_test1.py` plus the project's synth-smell fingerprint theory.

**Brief being judged:** 30 s of children playing and laughing — ≥3 distinct child voices, overlapping play, running feet, laughter tumbling into each other.

---

## 1. Per-clip table

| clip | s1 | s2 | s3 | s4 | s5 | S | key A-NATIVE notes | identity | confidence | one-line evidence |
|---|---|---|---|---|---|---|---|---|---|---|
| clip_1.wav | 0.6264 | 0.2975 | 0.0123 | 0.8216 | 0.0000 | 0.3516 | dc 1.6e-07; hiss 0.033; hf_flat 0.17; clicks 1978; **clip 0**; 0.47 trans/s (14) | **REAL recording** (forced choice) | LOW | No near-exact repetition anywhere (s3=0.012), moving formants (s5=0), natural-range envelope variability, clean sample hygiene |
| clip_2.wav | 0.5796 | 0.0000 | 0.5025 | 0.7719 | 0.0000 | 0.3708 | dc 1.6e-05; hiss 0.033; hf_flat 0.90; **clicks 10414**; **clip 723**; 1.13 trans/s (34) | **FORK RENDER** (forced choice) | LOW | Half of all distant 1-s chunk pairs are near-bit-identical (s3=0.503) with 10,414 digital clicks and 723 clipped samples — a looped/spliced assembly, not a continuous capture |
| calib_real.wav | 0.0584 | 0.8960 | 1.0000 | 0.5000 (n=0) | 0.9543 | 0.6817 | dc 2.1e-08; hiss 1.48; hf_flat 0.85; clicks 0; clip 0; 0 trans/s | LABELED real anchor | n/a (labeled) | Label trusted; fingerprint profile (s3=1.0, zero transients, stationary) reads as a real distant-ambience bed looped to 30 s |
| calib_synth.wav | 0.8744 | 0.0000 | 0.0714 | 0.7759 | 0.6261 | 0.4696 | dc 5.6e-06; hiss 0.317; hf_flat 0.80; clicks 5790; clip 0; 0.97 trans/s (29) | LABELED synth anchor | n/a (labeled) | Label trusted; highly periodic envelope rhythm (s1=0.874) marks it as generated/structured |

s1 = envelope periodicity | s2 = stationarity | s3 = near-exact repetition | s4 = transient symmetry | s5 = formant stability | S = mean(s1..s5), higher = more synth-like.

---

## 2. Forced choice

**The real recording is clip_1. The fork render is clip_2.**

### Anchor-margin reasoning (preregistered rule) and why I override it

The preregistered rule says: the unlabeled clip whose S is nearer calib_real's S (0.6817) is the real recording.

- |S(clip_1) − S(calib_real)| = **0.3301**
- |S(clip_2) − S(calib_real)| = **0.3109**

Strictly, clip_2 is nearer — by a margin of **0.0192**, far below the 0.05 LOW-confidence floor. The rule's verdict here is essentially a coin flip, and worse: **both** unlabeled clips are far nearer the *synth* anchor (|0.1180| and |0.0988| respectively) than the real anchor. The S anchors are degenerate in this package: **calib_real has the highest S of all four clips (0.6817)** — the labeled real recording is the most "synthetic" by the project's own index. This is driven by s3 = 1.0000 (every distant 1-s chunk pair near-identical), s5 = 0.9543 (static formants), s2 = 0.8960 (stationary), and zero detected transients. That is the profile of a real distant-playground ambience bed **looped to fill 30 s**, not of synthetic generation — the loop artifact inflates the repetition/stationarity/formant-stability fingerprints. The anchor labels are trusted, but S-distance to this anchor carries almost no information about which active, transient-rich scene (both unlabeled clips have real transients and fully moving formants, s5 = 0) is the continuous real capture. The preregistration explicitly permits overriding on individual fingerprints with written justification. Here it is:

1. **s3 (near-exact repetition) — the decisive fingerprint.** clip_2: 0.5025 — roughly half of all distant 1-s chunk pairs are cosine > 0.999 identical. Per the agreed theory ("reality: no voice repeats exactly"), this is the single strongest assembly/loop signature in the set. clip_1: 0.0123 — effectively no repetition at all. A real continuous 30-s playground capture cannot repeat half its chunks bit-near-exactly; an assembled render built from repeated event grains can.
2. **Digital hygiene (A-NATIVE).** The labeled real anchor has 0 clicks, 0 clipped samples. clip_2 has **10,414 clicks and 723 clipped samples** — a pervasive artifact texture (splice/resample/granualr stitching noise), incompatible with a clean field recording. clip_1 has 0 clipped samples and a click count (1978) consistent with transient-rich play (hand-claps, footfalls, mouth sounds). clip_2's extreme envelope variability (flux_cv 3.55, rms_cv 3.89, s2 = 0.0) is artifact-driven, not natural dynamics; clip_1's (flux_cv 0.47, rms_cv 0.65, s2 = 0.30) sits in a natural range.
3. **Converging transient profile.** clip_2's transient density (1.13/s, 34 events) matches the labeled synth anchor (0.97/s, 29); clip_1's (0.47/s, 14) does not. clip_2 is additionally the more hf-flat of the two (0.90 vs 0.17) — its little HF energy is noise-like rather than structured.

**Confidence: LOW.** The strict S-anchor rule nominally pointed at clip_2 (margin 0.0192 < 0.05 ⇒ LOW under the rule anyway), and both clips are closer in S to the synth anchor than to the real anchor — the anchors do not support my choice at all. I am overriding the anchor verdict on fingerprints alone, so per the prereg I drop to LOW and state it plainly. The single fact that would most raise my confidence: a listening oracle confirming clip_2's clicks sound like splice artifacts and clip_1's like real transient play.

---

## 3. Forced ranking of all four by realness (most → least likely to be a real field recording)

1. **calib_real.wav** — labeled real; its odd fingerprints are explained by 30-s looping of a real ambience bed, and its digital hygiene is perfect (0 clicks, 0 clipping).
2. **clip_1.wav** — my forced-choice real: zero near-exact repetition, fully moving formants, natural-range dynamics, no clipping.
3. **clip_2.wav** — my forced-choice fork render: looped/spliced construction signature (s3 = 0.50 + 10k clicks + clipping), though with real-like moving formants and non-stationarity underneath.
4. **calib_synth.wav** — labeled synth control; the most rhythmically periodic envelope in the set (s1 = 0.874) is the most artificial trait measured.

---

## 4. Disclosure

- I opened **only** the four listed files, and only via the measurement tool (`measure_test1.py` reading the WAVs) — I did not play, view, or inspect them in any other way, and I have no audio-hearing capability.
- I did **not** open anything under `…/blind/test1/keys/` or any other package, log, README, or fork material.
- I did **not** recognize any clip and had no prior knowledge of the forks; I used no web search and no information beyond the tool's numbers and the fingerprint theory supplied in the task.
- My ballot is **not void**: no blindness rule was violated. My override of the S-anchor rule is exercised under the preregistration's explicit "unless individual fingerprints tell a different story" clause, with the written justification above, and confidence dropped to LOW as required.
