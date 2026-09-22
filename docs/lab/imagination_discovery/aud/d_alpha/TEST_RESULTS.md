# TEST_RESULTS.md — FORK D-α (direct waveform dreaming)

All renders: pinned toolchain `znc_linux_x86_64_abed8aa1`, 44.1 kHz mono
16-bit. Dates: 2026-09-22.

## 1. Deliverables and hashes

| file | subject | dur | size (bytes) | SHA-256 |
|---|---|---|---|---|
| `d_alpha_kids.wav` | Test 1: kids playing/laughing | 30.00 s | 2,646,044 | `54a85d469a4b49b8d789fb4baea5213909b3af1cd44b100c71fc54981a71446d` |
| `d_alpha_kethra.wav` | Test 2: Kethra planet voice (anti-v2) | 21.00 s | 1,852,244 | `b64b8d94a46410dafa6785a7b93f4f92e6a2da08dc32110413eac3f0d8bcfcf8` |
| `d_alpha_ocean.wav` | Test 3: alien ocean surf at dawn | 30.00 s | 2,646,044 | `e9756ad66727c8ee05265bac948f1cbd644a3580f432889505749a0be46703af` |
| `d_alpha_monster.wav` | monster objection | 21.00 s | 1,852,244 | `40d11a4bf710d0efdc104f1f56f7af0c601dcba89347133186fb92fd8ff4c059` |
| `synth_control_kids.wav` | K2 control (banned paradigm) | 30.00 s | 2,646,044 | (rendered; labeled CONTROL) |

Source: `dream.zag` (deliberation + expansion). Control source:
`synth_control.zag` (banned toolkit, kept only as control).

## 2. Test 1 — kids benchmark (30 s, ≥3 child voices, overlapping play, running feet, tumbling laugh)

### Mechanical / audit gates

| gate | bar | result |
|---|---|---|
| A-NATIVE | all sub-bars | **PASS** (floor NATURAL FALL; ZCR 0.039; hiss 0.000 CLEAN; DC −0.0002; peak 0.679 / 3.4 dB headroom; clicks within nature) |
| Uniqueness (no two pulses alike) | max pairwise xcorr < 0.90 | **PASS** (0.670, 58 pulses) |
| Resonances move | pulse centroid SD > 250 Hz | **PASS** (mean 1839, SD 516 Hz) |
| Non-repetition | 2 s self-similarity < 0.90 | **PASS** (0.781) |
| Determinism | byte-identical 3/3 by SHA-256 | **PASS** (4/4 incl. committed file) |
| Expansion audit (K4) | opinionless arithmetic | **PASS** — 4 defects found and fixed during audit (see EXPANSION_AUDIT.md §3.6); no hidden oscillators/resonators/filters/chirps/beds |
| Study grounding | pulse stats vs public-domain laughter | PASS — pulse durs 30–160 ms, F0 298–580 (+shriek lifts), centroids 1231–3084 Hz vs studied 1700–4200 |

### Oracle gates (kill bars)

| gate | bar | result |
|---|---|---|
| K1 | one "sounds like a synth" from Micah kills the claim | **PENDING** — Micah has not listened |
| K2 | beat synth control in forced choice, ≥4/5 fresh native critics | **PENDING** — control built and ready (`synth_control_kids.wav`); critics not yet run |
| K3 | nondeterminism | **CLEAR** — 3/3 byte-identical |
| K4 | expansion-code audit trip | **CLEAR** — audit committed (EXPANSION_AUDIT.md) |

### The synth control (for K2)

Built from the banned paradigm in good faith (struck harmonic partials +
vibrato LFO + struck envelopes + filtered-noise feet + sine-voice chirps).
It exhibits the synth smells D-α was designed to avoid: 2 s self-similarity
**0.919** (FAILS the <0.90 non-repetition bar — phrase-level repetition),
digital-silence floor (−300 dB — no air). Pulse-level uniqueness 0.512
(passes — pitch wander varies pulses). This is the correct control: it
should lose on exactly the bars D-α passes.

## 3. Test 2 — anti-v2 (Kethra planet voice, rebuilt from scratch)

| gate | result |
|---|---|
| A-NATIVE | **PASS** (ZCR 0.052; hiss CLEAN; DC −0.0000; headroom 3.4 dB) |
| Determinism 3/3 | **PASS** |
| Expansion audit | **PASS** (same audited expansion) |
| Blind A/B vs `d_aud3_planetvoice_v2.wav` ("unrecognizable as the same synth paradigm, retains alien planet voice meaning") | **PENDING** — clips ready; listeners not yet run |

Design note: the rebuild shares NO code path with v2's paradigm — no
resonators, no beds, no chorus stack. Kethra's voice is slow geology:
tidal breathing swells, vent exhalations (breath grain), cryo-cracks
(drawn impacts at 2–3× rate), magnetospheric chorus (wandering high voices).

## 4. Test 3 — alien ocean ("an alien ocean's surf at dawn, under a sky that hums")

| gate | result |
|---|---|
| A-NATIVE | **PASS** (ZCR 0.022; hiss CLEAN; DC ≤ 0.005; headroom 3.4 dB) |
| Determinism 3/3 | **PASS** |
| Expansion audit | **PASS** |
| Blind evaluation (Micah + 2 native critics): kills on "synth," "Earth pastiche," or audit trip | **PENDING** — clip ready; listeners not yet run |

Design note: breakers are DRAWN 3 s tables (slow rise, ragged crest,
heavy fall), not filtered noise; the sky hum is a low voiced drone with
wandering F0; the alien color is deliberated inharmonic partials
(1, 1.71, 2.63…).

## 5. Monster objection

| item | result |
|---|---|
| Committed description first | **DONE** (MONSTER.md §2, written before rendering) |
| Render (`d_alpha_monster.wav`) | 21 s, A-NATIVE **PASS**, deterministic 3/3 |
| Knowledge-stretch vs noise/synth collapse | **PENDING Micah's ears** — honest assessment in MONSTER.md §4: the attempt is specific enough to be wrong; whether it reads as imagination or "big animal"/synth drone is for the oracle |

## 6. Head-to-head vs b-family

**No b-family results were available to this fork.** No comparison is
invented here. The only head-to-heads this fork can report are internal:
D-α vs its own synth control (K2, pending listeners) and D-α Kethra vs
`d_aud3_planetvoice_v2.wav` (Test 2, pending listeners).

## 7. Did the expansion stay opinionless?

Yes, with four defects found and fixed (audit §3.6) — all four were
rendering-math bugs (clamped impact tails, positive-only breaker wash,
double-applied ratios, shared-phase inharmonic DC), none were hidden
opinions. The audit faces the "oscillator in a wig" charge directly
(§3.1–3.3): the mechanism is Fourier summation, but every frequency,
weight, trajectory, and timing is deliberated per gesture; the expansion
integrates and adds. The ear (K1) remains the final judge.

## 8. What remains open (for the parent/coordinator)

1. **K1**: Micah listens to `d_alpha_kids.wav` (brief: 30 s, three children
   playing and laughing, running feet, tumbling laugh). One "synth" kills
   the Test 1 claim.
2. **K2**: 5 fresh native critics (did not build clips), blind order,
   forced choice D-α kids vs `synth_control_kids.wav`. Two questions per
   clip: "could this be a real recording of the described event?" and
   "does this sound like a synth?" Bar: ≥4/5 for D-α.
3. **Test 2**: blind A/B `d_alpha_kethra.wav` vs `d_aud3_planetvoice_v2.wav`.
4. **Test 3**: blind ocean evaluation, Micah + 2 native critics.
5. **Monster**: Micah's verdict on `d_alpha_monster.wav`.
6. Real-playground calibration recording: not obtained by this fork (the
   public-domain pool recording is children ambience, not a playground —
   not mislabeled as such).

## 9. Pre-verdict (honest, before the oracle)

- **Mechanical position: strong.** All four clips pass A-NATIVE, all
  determinism checks, all forensics bars. The audit is committed with
  defects owned.
- **Likeliest K1 risk:** the monster (low inharmonic drone — the highest
  synth-adjacent risk in the set) and, for the kids, any residual
  "sung" quality if the jitter/envelope raggedness under-delivers on a
  couple of pulses. The kids' best defense is the measured irregularity
  (centroid SD 516 Hz, 58 unique pulses, no phrase repetition).
- **K2 outlook:** the control is audibly a synth by construction
  (regular 0.16 s "ha" rhythm, LFO vibrato, struck envelopes). If critics
  are honest and the brief is clear, D-α should win — but that is a
  prediction, not a result.
- **What would change my mind:** a single "synth" from Micah on any clip
  kills that clip's claim per the debate's rules. The position accepts
  this in advance.
