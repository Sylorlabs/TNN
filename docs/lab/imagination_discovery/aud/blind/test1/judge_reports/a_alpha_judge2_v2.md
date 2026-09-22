# BLIND TEST-1 — Package A-ALPHA — Judge 2 ballot (blind native critic)

**Judge role:** blind native critic. I have never encountered these clips, did not build any
fork, and cannot hear. Analysis is signal-only, from the numbers returned by
`measure_test1.py` plus the project's agreed synth-smell fingerprint theory.

**Anomalies in the anchors (noted before scoring):** the labeled anchors are only
0.0393 apart in S (calib_real S=0.5089, calib_synth S=0.4696), and both UNLABELED
clips score BELOW both anchors (0.3516, 0.3708). The S-anchor distance rule alone
therefore calls both unlabeled clips "closer to synth" — an impossible split for a
one-real/one-render pair. Scoring below follows the preregistered escape clause:
individual fingerprints arbitrate, in writing.

## 1. Per-clip table

| clip | s1 | s2 | s3 | s4 | s5 | S | key A-NATIVE notes | identity | confidence | one-line evidence |
|---|---|---|---|---|---|---|---|---|---|---|
| clip_1 | 0.6264 | 0.2975 | 0.0123 | 0.8216 | 0.0 | 0.3516 | dc=1.6e-7 (cleanest); clip_count=0; clicks=1978 (< calib_real's 2400); hiss=0.0325 ≈ calib_real's 0.0354; hf_flatness=0.17 (strongly non-flat HF, natural) | **FORCED CHOICE: the real recording** | MEDIUM | s3 and s4 match the real anchor almost exactly; no digital-assembly artifacts; HF spectrum natural |
| clip_2 | 0.5796 | 0.0 | 0.5025 | 0.7719 | 0.0 | 0.3708 | dc=1.6e-5 (100x clip_1); **clip_count=723**; **clicks=10414**; hiss=0.0329; hf_flatness=0.90 ≈ synth control; transients/s=1.13 ≈ synth's 0.97 | **FORCED CHOICE: the fork render** | MEDIUM | s3 = 0.50: half of all distant 1 s chunk pairs are near-identical (loop/paste fingerprint); 723 hard clips + 10k clicks = splice/synthesis assembly scars |
| calib_real | 0.8468 | 0.4611 | 0.0074 | 0.8274 | 0.402 | 0.5089 | LABELED: known real playground field recording. dc=6e-8; clips=0; clicks=2400; hiss=0.0354; hf_flatness=0.79 | anchor (known real) | n/a | — |
| calib_synth | 0.8744 | 0.0 | 0.0714 | 0.7759 | 0.6261 | 0.4696 | LABELED: known synth control. dc=5.6e-6; clips=0; clicks=5790; **hiss=0.317 (10x all others)** — a prominent noise bed; hf_flatness=0.80 | anchor (known synth) | n/a | — |

## 2. Forced choice

**clip_1 is the real recording. clip_2 is the fork render.**

Anchor-margin reasoning (why I overrode the naive S rule):
- S-distances: clip_1 is 0.1180 from the synth anchor / 0.1573 from the real anchor;
  clip_2 is 0.0988 from synth / 0.1381 from real. The S-only rule labels BOTH as synth
  (both nearer the synth anchor), which is impossible for a one-real/one-render pair,
  and the anchors themselves differ by only 0.0393. S is saturated here; the individual
  fingerprints decide, and they point one way, unanimously:
- **REGULARITY/repetition (s3):** clip_2 = 0.5025 — half of distant 1 s chunk pairs are
  >0.999 cosine-identical. The real anchor is 0.0074, the synth control 0.0714; clip_1
  is 0.0123. A real playground never repeats half its material exactly; clip_2 carries a
  loop/paste signature 68x the real-anchor level. This single fingerprint is nearly decisive.
- **SYMMETRY (s4):** clip_1 = 0.8216 vs real anchor 0.8274 (near-exact match);
  clip_2 = 0.7719 vs synth control 0.7759 (near-exact match). Transients pair off the same way.
- **A-NATIVE assembly scars:** clip_2 has 723 hard clips and 10,414 clicks — digital
  splice/paste artifacts absent from both anchors (0 and 0 clip counts). clip_1 has 0 clips
  and fewer clicks than the real anchor.
- **High-frequency character:** clip_1 hf_flatness=0.17 (strongly non-flat, natural
  playground HF); clip_2 = 0.90, matching the synth control (0.80); hiss beds also match
  (clip_1 0.0325 ≈ real 0.0354; the synth control's 0.317 is the outlier noise bed).
- **Transients/s:** clip_2 (1.13) ≈ synth control (0.97); clip_1 (0.47) is between, closer
  to the real anchor (0.10).

Counter-notes (why not HIGH): s1, s2, s5 are ambiguous or favor the anchors over BOTH
unlabeled clips (both unlabeled score s5=0.0, i.e. MORE formant motion than the real
anchor; s1 is high in both anchors). These likely reflect the real anchor's periodic
ambient component rather than vocality, but they keep me from claiming full separation.

**Confidence: MEDIUM.** The fingerprint story is internally consistent across s3, s4,
hiss, HF flatness, clip/clack counts, and transient rate — but the individual
fingerprints contradict the S-anchor distances, which per the prereg drops confidence
one level (and the anchor pair itself is only 0.0393 apart).

## 3. Forced ranking (most → least likely a real field recording)

1. **calib_real** — labeled anchor, known genuine.
2. **clip_1** — forced choice: the real recording.
3. **calib_synth** — labeled anchor, known synth control (outranks clip_2 because it is
   at least an honestly-labeled control; clip_2's loop fingerprint + assembly scars are
   worse than the control's noise bed).
4. **clip_2** — forced choice: the fork render.

## 4. DISCLOSURE

- I opened NOTHING beyond the four listed clips, and only through the measurement tool
  (its output is quoted in the table above). I did not open anything under
  `.../aud/blind/test1/keys/` or any other file in the blind-test tree.
- I have never encountered any of these clips before, built no fork, and (being a
  text-only critic) did not listen to or otherwise "recognize" any of them.
- I used no web search, no prior knowledge of the forks, and no information beyond
  the tool's numbers and the stated fingerprint theory.

**My ballot is not void.**
