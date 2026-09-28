# PREREG_v11_waveguide — AUDIO V11 FORK W (child-scale digital-waveguide vocal tract)

**Status:** FROZEN 2026-09-23, BEFORE any render. Committed alone per task.
**Fork:** W (Sol Paradigm 1, CS-DWGVT — step-3.7-flash). Coordinator: audio V11.
**Work dir:** `~/workspace/aud_v11/fork_w/` (scratch; binaries never committed).

## 1. Claim

A 30 s playground scene rendered through a child-scale (9 cm) 1D digital-waveguide
vocal tract driven by a child two-mass vocal-fold oscillator — with source-filter
back-pressure coupling — will produce a voice signature nearer the frozen real-child
anchor than any V10 render, passing all 9 frozen bars (JUDGE_PROTOCOL_V11.md §3)
and the self-check bars below. Child-likeness is to emerge from anatomy (short
tract, light folds, coupled physics), not from hand-tuned formant numbers.

## 2. Frozen ground truth

- Instrument: `docs/lab/imagination_discovery/aud/b_alpha/voice_sig_frozen.zag`
  (SHA-256 `7117ac57b2ad98a2849e4c86ef659164911835f03b50a63c5f6b7b64996e9a65`),
  built per protocol §8.
- Anchor signature: F0 651.3 | F0DYN 174.3 | F1B 794 | F2B 2104 | F3B 2814 |
  HNR 3.7 | TILT 0.9 | MOD4 0.412 | 36 clean frames.
- V10 wrong-target baseline: PARADD 52 frames (F0 766.6/F0DYN 384.3/F1B 740/
  F2B 2329/F3B 2968/HNR 4.0/TILT 0.0/MOD4 0.551); ARTIC and SPECSTAT VS_OK 0.

## 3. Architecture (from SOL_IDEAS_V11.md Paradigm 1)

### 3.1 Vocal tract — 13-section Kelly–Lochbaum digital waveguide
- 13 sections, Δx = 0.714 cm, 9 cm total (average 5-year-old tract).
- One-sample-per-section delay (≈0.79 cm at 44.1 kHz; slight tract stretch, documented).
- Junction scattering with r_j = (A[j]−A[j+1])/(A[j]+A[j+1]).
- Distributed damping per section (child tissue: wider formant bandwidths emerge).
- Glottis boundary (junction 0): reflection + glottal-flow injection.
- Lip boundary (junction 13): open-end reflection rL ≈ −0.65; radiated output
  = 1-zero FIR high-pass of lip pressure (child lip radiation).
- Subglottal tract: 2-section waveguide (1.4 cm) behind the glottis; shapes
  glottal leakage noise, returns supraglottal back-pressure to the folds.

### 3.2 Vocal folds — child two-mass oscillator (Ishizaka–Flanagan form)
- m1 = 0.02 g, m2 = 0.01 g; k1 = 2 N/m, k2 = 4 N/m, kc = 1 N/m;
  d1 = 0.005 Ns/m, d2 = 0.003 Ns/m (Sol's values, modal baseline).
- Subglottal pressure Ps = 0.5–2 kPa, scheduled by utterance effort.
- Bernoulli flow: U = A_min·√(2·|Ps−Psupra|/ρ)·sign, collision nonlinearity,
  supraglottal pressure Psupra taken from tract junction 0 each sample
  (the source-filter back-pressure coupling).
- Glottal flow injected as volume-velocity source into junction 0.

### 3.3 Noise (zero RNG in render path — seeded hash streams only)
- Breath noise: deterministic h01(seed, counter) white stream (the established
  common_v5.zag hash; Sol explicitly allows "seeded hash streams only"),
  amplitude ∝ glottal leakage area, shaped by the subglottal waveguide.
- Cycle-to-cycle jitter: hash-seeded tension perturbation, 2–4% of period.
- Footstep timing jitter: separate hash stream, CV ≈ 0.3.

### 3.4 Child vowel area-function LUTs (13 areas, cm², glottis→lips)
Sol gives only max/min areas (/a/ max 10, /i/ min 0.5, /u/ 2, /e/ 3, /o/ 4 cm²),
not full tube shapes. Full 13-section shapes are designed for child formant
targets (F1 ≈ 950 Hz, F4 ≈ 6000 Hz for mid vowels; 9 cm uniform tube gives
972/2917/4861/6806 Hz) and then TUNED EMPIRICALLY against the frozen
instrument's band centroids (see §3.6). All final LUTs committed in source.

### 3.5 Scene (30 s, 44.1 kHz mono 16-bit)
One continuous playground scene, three kid voices (A/B/C, different base
tension → different F0 registers):
- 0–8 s: yard activity — chant-like utterances, running footsteps.
- 8–18 s: chase — shouts, faster utterances, footstep bursts.
- 18–25 s: shared laughter — giggle episodes per Sol: 4 Hz AM on Ps,
  12 Hz FM on fold stiffness, 10 ms abductory damping pulses, +3 dB
  leakage noise during open phases.
- 25–30 s: wind-down — softer calls, breaths, receding footsteps.
- Utterances: vowel sequences (/a i u e o/) with attack overshoot (+20% pitch),
  effort-scheduled Ps, breathy releases; consonant-ish onsets via abrupt
  pressure onsets + brief noise bursts. No real words (honest limitation).
- Ambience: low playground wash (distant voice fragments + soft wind/bird-ish
  hash noise), kept below the voice screen so it cannot dominate clean frames.

### 3.6 Tuning loop (preregistered, honest)
The vowel LUTs, damping, leakage-noise gain, and tension schedule will be
iterated against the FROZEN instrument (never a modified one). Tuning targets
are the 9 frozen bars; each iteration is logged in the findings file with the
changed parameter and the resulting signature. This is open, documented
parameter fitting against the frozen judge — not silent overfitting: the
final FINDINGS file reports the full iteration log.

## 4. Deviations from Sol's sketch (written justification, preregistered)

- **D1 — tension-scaled stiffness.** Sol's k1=2/k2=4 N/m with Ps 0.5–2 kPa is
  a MODAL baseline (Sol: "F0 220–450 Hz for mid vowels"). The frozen anchor's
  clean play voices sit at F0 598–772 Hz (median 651.3). Hitting V-F0 requires
  play/shout F0, which in two-mass models comes from the standard longitudinal
  tension parameter (cricothyroid activation): k1,k2 × tension T ∈ [1, 5],
  scheduled by utterance effort (shouts T≈4–5, chant T≈2–3, wind-down T≈1–2).
  This is the model's own tension knob, not a hand-tuned F0 number.
- **D2 — f64 arithmetic, not Q15.** IEEE-754 double ops are deterministic on
  this VM (all prior V10/V11 instruments use f64; byte-identical verified).
  Q15 buys nothing for judging and risks overflow bugs. The physics is
  unchanged; only the number format differs.
- **D3 — footstep engine.** Sol: reuse the waveguide as a 20-section mechanical
  impact model. Preregistered simplification: per-step deterministic 1 ms
  impulse (scaled to ~20 kg child) → 200 Hz low-pass (sole compliance) →
  two fixed resonant modes (80–250 Hz, the light high-pitched thud). Justified:
  footsteps are scene dressing, not voice-signature relevant; the two-mode
  model preserves Sol's acoustic target (light, high-pitched thud) at 1/20th
  the compute, leaving budget for the three coupled voice renders.
- **D4 — hash streams instead of literal LFSR.** common_v5.zag h01(seed,k) is
  the established deterministic primitive; Sol explicitly permits "seeded
  hash streams only". Not a real deviation; recorded for audit clarity.
- **D5 — vowel LUT shapes.** Sol gives extrema only; full shapes are designed
  (§3.4) and tuned against the frozen instrument (§3.6).

## 5. Bars and kill rules (frozen; from task + JUDGE_PROTOCOL_V11.md)

- **Self-check:** VS_OK 1 with ≥25 clean frames; voiced fraction ≥4% under the
  diagnosis instrument is indicative, not gating; HNR ≥3 dB; F0 med 350–700 Hz;
  excursion ≥10 st; formant-band energy present on voiced frames.
- **Objective:** 9/9 frozen bars vs anchor, each also strictly nearer the
  anchor than PARADD (the only V10 render with a voice signature).
- **KILL RULE (a):** if the fork's z-scored signature distance is nearer ANY
  V10 render than the anchor (min_render D < D_anchor, ≥5 shared metrics),
  the fork is dead — report honestly and stop. No silent bar-shopping.
- **KILL RULE (b):** subjective prong is the parent's job; this fork's
  deliverable includes the MANDATORY honest steelman in FINDINGS.
- **Determinism:** ≥2 byte-identical renders (cmp-verified), zero RNG.

## 6. Deliverables

1. `src/render_v11_waveguide.zag` — the renderer (pure Zag, imports only
   `src/common_v5.zag` helpers).
2. `clips/b_alpha_kids_1e_k_v11_waveguide.wav` — the 30 s clip.
3. `FINDINGS_v11_waveguide.md` — full voice_sig output, 9-bar table vs anchor
   vs V10, byte-identical proof, iteration log, and the MANDATORY honest
   steelman arguing why the clip does NOT sound like children.

## 7. Honesty commitments

- The anchor WAV is measurement-only (CC BY-NC-ND): never a render source,
  never committed. (This prereg uses no audio at all.)
- If the signature lands nearer V10 than the anchor, I report it and stop —
  no metric-hacking, no bar-shopping, no "close enough".
- If the steelman cannot be written convincingly, I say why.
- Commits: branch tnn-native-lab ONLY; commit_racefree.py with
  TMPDIR=~/workspace/tmp_commit; no binaries, no .zagd.
