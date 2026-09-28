# JUDGE PROTOCOL V11 — frozen judging protocol for AUDIO V11 forks

Status: **FROZEN** — this document was committed before any V11 fork was
inspected or judged. No bar, tolerance, procedure, or kill rule below may be
changed after the first V11 fork is seen. Amendments require Micah's explicit
sign-off and a new version number (V11.1); the frozen copy stays in git
history.

## 0. Why this protocol exists

V10's ARTIC, PARADD, and SPECSTAT passed all nine consistency bars, yet
Micah's ears judged that none of them sounded like little children. The old
gate measured general waveform consistency, not child-likeness. This protocol
replaces it with a two-pronged child-likeness test:

- **Prong 1 (objective):** voice-signature bars measured by a frozen pure-Zag
  instrument against the real-child anchor. Every bar cites the anchor's
  measured value and a tolerance derived from real-child variance —
  never from renders.
- **Prong 2 (subjective):** blind structured listening by ear judges with
  written justifications, a mandatory steelman against child-likeness, and
  red-team calibration traps.

A fork reaches Micah's ears only if it passes **both** prongs. Ears outrank
metrics: any unanimous ear rejection kills the fork even with a perfect
objective score (this is what V10 taught us).

## 1. The anchor (the only ground truth)

- File: `consistency_gate/calibration/aporee_kids_play_area_30s.wav`
  (Pingtung Park children's play area, Wu Tsan-cheng, CC BY-NC-ND 3.0).
- SHA-256:
  `6adafbf0143df1c1721377cd8eaa7f25aa6305fb4be6d12c6268d28281738960`
- The anchor WAV is **measurement-only**: never committed, never
  redistributed (license). Judges work from derived measurements and from
  blinded listening copies prepared by the administrator.
- Why this anchor: it is a real recording of real children at play. It is
  distant and quiet (-35.9 dBFS median) — that is a feature, not a bug: the
  instrument was built to find real voices inside a real scene rather than
  demanding studio conditions.

## 2. The instrument (frozen)

- Source: `voice_sig.zag` (pure Zag, zero RNG, deterministic), developed
  in the working tree at
  `imagination_discovery/aud/b_alpha/consistency_gate/src/voice_sig.zag`.
  The source is not committed with this protocol; the frozen measurement
  values in §8 are the protocol's ground truth. Binary built with the
  pinned toolchain; the binary is a build artifact and is never committed.
- What it does (frozen with the source):
  1. Rumble removal: `y = x - MA441(x)` (~100 Hz high-pass). Without this,
     autocorrelation locks onto playground rumble instead of voices.
  2. 30 ms frames, 15 ms hop. Screen: frame RMS(y) >= median + 1 dB
     (floor -55 dBFS), ZCR in [0.020, 0.500].
  3. Periodicity: normalized autocorrelation of mean-removed y, lags
     55..735 (60..801 Hz). The peak must be a **local maximum** (never the
     range edge) with parabolic interpolation. **Clean voice frame** iff
     peak >= 0.60 and 150 <= F0 <= 800 Hz.
  4. On clean frames only: F0, HNR = 10*log10(peak/(1-peak)), LPC(12)
     (Levinson-Durbin, Hamming, pre-emphasis 0.97) envelope over 0..6 kHz,
     formant-band energy centroids, spectral tilt (octave regression of
     envelope dB at 250/500/1000/2000/4000 Hz), envelope centroid.
  5. MOD4 (mix-level, always computed): max normalized autocorrelation of
     the 25 ms RMS(y) envelope over lags 5..20 windows (2..8 Hz) — the
     syllabic-modulation signature of real vocal activity.
  6. `VS_OK 1` requires >= 25 clean voice frames. Fewer → `VS_OK 0`: **no
     measurable voice signature**. A children's playground scene with no
     measurable voices fails the objective prong outright — that is a
     finding, not a missing value.
- Formant measurement (read this before citing "formants"): the anchor's
  clean play voices sit at F0 ~ 600-800 Hz, so harmonic spacing exceeds
  formant bandwidths and peak-picking is unreliable (the known
  child-formant-tracking problem; cf. Lee et al. on F2/F3 difficulty in
  children). The instrument therefore reports LPC-envelope **energy
  centroids** in the F1/F2/F3 bands (VS_F1B 200-1250 Hz, VS_F2B 700-3400
  Hz, VS_F3B 1500-4600 Hz). They are always defined, deterministic, and
  sensitive to vocal-tract size (short child tracts push resonance energy
  up). They are not textbook formant frequencies; treat them as
  resonance-distribution measurements.
- Determinism: the instrument was run twice on the anchor; output is
  byte-identical (see §8).

## 3. The objective bars (frozen)

Nine bars. A fork passes a bar iff **both**:

- (a) `|F - A| <= tol` — within real-child tolerance of the anchor, AND
- (b) `|F - A| < min over V10 renders of |R - A| + tol/20` — strictly nearer
  the anchor than the best V10 render on that bar, up to a
  measurement-resolution tie epsilon of `tol/20` (renders missing the metric
  are skipped; if no V10 render has the metric, (b) is vacuous).

The tie epsilon exists because a V10 render can land essentially on the
anchor by luck (PARADD's tilt matches the anchor to the printed digit);
without it, "strictly nearer" would make such a bar impassable. Differences
below `tol/20` are not resolvable as "nearer" at the tolerance scale. The
requirement stays teeth-first everywhere else: on 8 of 9 bars the V10 best
is well outside the epsilon, so the fork must genuinely beat V10.

A fork missing a metric (VS_OK 0) **fails** every voice bar. An anchor-side
missing metric voids the bar (excluded from the pass count, noted).

Tolerance rule (frozen): `tol = max(literature_floor, split_half_diff)`,
where `split_half_diff = |anchor_half1 - anchor_half2|` (deterministic
15 s / 15 s split, same instrument), and the literature floors are:

| bar | metric | anchor A | lit floor | tol = max(lit, split) |
|---|---|---|---|---|
| V-F0 | VS_F0_MED | 651.3 Hz | 60 Hz | 60 Hz (split n/a) |
| V-F0DYN | F0 P90-P10 | 174.3 Hz | 0.40 x A | 69.7 Hz (split n/a) |
| V-F1 | VS_F1B | 794 Hz | 120 Hz | 120 Hz (split n/a) |
| V-F2 | VS_F2B | 2104 Hz | 180 Hz | 180 Hz (split n/a) |
| V-F3 | VS_F3B | 2814 Hz | 200 Hz | 200 Hz (split n/a) |
| V-HNR | VS_HNR_MED | 3.7 dB | 4.0 dB | 4.0 dB (split n/a) |
| V-TILT | VS_TILT_MED | 0.9 dB/oct | 3.0 dB/oct | 3.0 dB/oct (split n/a) |
| V-F2DYN | VS_F2B_IQR | 715 Hz | 0.40 x A | 286 Hz (split n/a) |
| M-MOD | VS_MOD4 | 0.412 | 0.10 | 0.402 (split 0.402) |

Literature basis for floors (sanity context, not bar values): Sydney Voice
Lab norms (age 4-8 mean F0 255-277 Hz, SD 24-32; play/shout ranges wider —
floor 60 Hz ~ 2x conversational SD); Iseli et al. child corner vowels
(/a/ F1 1030 / F2 1370 / F3 3170; /i/ 370/3200/3730; /u/ 430/1170/3260)
showing child resonances far above adult norms — floors 120/180/200 Hz are
conservative against these spreads. HNR/tilt/MOD4 floors are judgment calls
documented here as such.

The mechanical judge (`judge/judge_v11.py` in the crew workdir; logic
frozen here) applies the table. **Objective PASS requires 9/9 bars**
(no partial credit; 8/9 is reported as MARGINAL, which is still a FAIL for
gate purposes).

## 4. Kill rules (frozen)

- **(a) Wrong-target convergence.** Signature distance: z-scored Euclidean
  over the nine bars, `z_i = (x_i - A_i)/tol_i`. If the fork's signature is
  strictly nearer to ANY V10 render's signature than to the anchor's
  (`min_render D < D_anchor`), the fork is KILLED — it is converging on the
  machinery that produced V10, not on children. (V10 renders missing voice
  metrics are excluded from the render set for the voice bars; the distance
  uses metrics present in both signatures, minimum 5 shared.)
- **(b) Unanimous ears.** If every ear judge rates the fork "not children"
  (S1 <= 3/10, see §5) with written justification, the fork is KILLED even
  with a 9/9 objective score. Micah's ears outrank the instrument — V10 is
  the precedent.
- **(c) Both-prongs gate.** Nothing reaches Micah without passing BOTH
  prongs. Objective PASS + subjective PASS (mean S1 >= 6/10, no unanimous
  rejection, ranks above the puppet and all V10 renders — §5) is required.

## 5. Subjective prong (frozen procedure)

- **Blinding:** the administrator (who does not judge) renames all clips
  (anchor, forks, puppet, V10 renders, controls) to random IDs and orders
  them by SHA-256 digest (deterministic, blind). The anchor is always
  included blind as the ceiling reference. Judges never learn identities
  until scores are locked.
- **Independent scoring first:** each judge scores every clip alone:
  - S1 child-likeness 0-10 ("does this sound like real little children at
    play?")
  - S2 toy/machine quality 0-10 ("does this sound like a toy, robot, or
    machine?")
  - Written justification (>= 2 sentences) per clip, then a **steelman
    against child-likeness**: the strongest case that this clip is NOT
    children, written BEFORE seeing other judges' scores.
  - Scores lock before any discussion.
- **Ranking:** each judge rank-orders all clips by child-likeness.
- **Pass criteria:** mean S1 >= 6/10 AND mean rank strictly better than the
  puppet's AND strictly better than the best V10 render's AND no judge
  writes an "obviously not children" justification that survives discussion.
- **Anti-self-deception rules:**
  1. The against-case is written before the for-case may be revised.
  2. The R1 puppet (a metric-matching non-child, §6) is in every session
     as a calibration trap: any judge ranking the puppet above the blind
     anchor has their session flagged and the session is re-run.
  3. Judges are told a puppet exists but not which clip it is.
  4. Discussion happens only after locked scores; discussion may change a
     score only with a written reason, and changes are logged.
- **Controls in every session:** blind anchor (ceiling), R1 puppet (trap),
  best V10 render by objective distance (the wrong-target reference).

## 6. Red-team / protocol-attack battery (frozen)

The protocol must survive its own attacks. Each attack is built
deterministically (no RNG) and run through the full judge:

- **R1 — the metric puppet.** A synthetic "voice" engineered to hit the
  objective bars: F0 at the anchor's F0_MED with wander, harmonic stack at
  the anchor's tilt, resonators at F1B/F2B/F3B, noise for the anchor's HNR,
  4 Hz syllabic AM for MOD4 — but with static formants, no phonemes, no
  prosody, robotic timing. **Measured:** passes 6/9 bars (V-F0, V-F0DYN,
  V-F1, V-F2, V-TILT, V-F2DYN); fails V-F3, V-HNR (nearer-than-V10), M-MOD.
  **Interpretation:** a naive 30-minute synthetic games two-thirds of the
  objective prong; a determined attacker could likely reach 9/9. This is
  WHY the subjective prong exists — the puppet would be destroyed by the
  ear panel. If the panel does NOT reject it, the protocol is broken and
  judging halts. The 6/9 result is the gameability baseline (§8).
- **R2 — ambience mask.** Anchor + loud playground wash (+6 dB) burying the
  clean voices. **Expected:** VS_OK 0 → objective FAIL. (A scene whose
  voices can't be measured can't be judged child-like.)
- **R3 — level shift.** Anchor x4 linear gain (no clipping). **Expected:**
  9/9 PASS, D = 0 — the instrument must be level-invariant. If not, the
  instrument is broken and judging halts.
- **R4 — identity.** Anchor vs itself. **Expected:** 9/9, D = 0. Sanity.
- **Toy-vs-child forced choice:** each fork is paired blind against (i) the
  anchor, (ii) the R1 puppet, (iii) the best V10 render; judges pick the
  more child-like. A fork losing to the puppet fails the session.
- **Blind ordering:** judges rank anchor/candidate/puppet/V10 without
  identities (§5).

Attack results are committed with the protocol (§8) as the baseline the
protocol survived.

## 7. Judging workflow (frozen)

1. Fork clips arrive; the administrator verifies 44.1 kHz mono 16-bit,
   >= 10 s, logs SHA-256, assigns blind IDs.
2. The objective judge runs `voice_sig` + `judge_v11.py` on each fork
   (anchor halves and V10 references are frozen inputs, re-measured only
   with the frozen binary).
3. Objective FAIL or kill (a) → fork dead, reported, never reaches ears.
4. Objective PASS → blind listening session per §5 with attacks from §6.
5. Kill (b) → fork dead. Both prongs pass → fork advances to Micah with
   the full verdict file (objective table, ear scores, justifications,
   attack results).

## 8. Frozen measurements

Instrument: `voice_sig.zag` (pure-Zag source; binary built 2026-09-24
with the pinned toolchain, reruns byte-identical). The instrument source
is not part of this protocol commit; the frozen measurement values below
are the protocol's ground truth. All values below were produced by the
frozen binary.

Anchor (full 30 s), VS_OK 1, 36 clean voice frames:
`F0_MED 651.3 | F0_P10 598.0 | F0_P90 772.3 | F1B 794 | F2B 2104 |
F2B_IQR 715 | F3B 2814 | HNR_MED 3.7 | TILT_MED 0.9 | MOD4 0.412`

Tolerances (frozen): `tol = max(literature_floor, split_half_diff)`.
Split-half (15 s / 15 s) was unmeasurable for voice metrics — both halves
fall below the 25-clean-frame gate (21 and 14 frames) under the corrected
R(0) normalization, which is itself informative about how sparse real
playground voices are. Voice-metric tolerances therefore rest on the
literature floors alone (documented as such); MOD4 uses the true
split-half diff (|0.483 - 0.081| = 0.402).

| bar | anchor A | tol |
|---|---|---|
| V-F0 | 651.3 Hz | 60 Hz |
| V-F0DYN | 174.3 Hz | 69.7 Hz |
| V-F1 | 794 Hz | 120 Hz |
| V-F2 | 2104 Hz | 180 Hz |
| V-F3 | 2814 Hz | 200 Hz |
| V-HNR | 3.7 dB | 4.0 dB |
| V-TILT | 0.9 dB/oct | 3.0 dB/oct |
| V-F2DYN | 715 Hz | 286 Hz |
| M-MOD | 0.412 | 0.402 |

V10 reference signatures (the wrong-target baseline; measured, never tuned).
ARTIC and SPECSTAT have **no measurable voice signature** (0 clean frames
under the corrected instrument — their "voices" were R(55)-normalization
artifacts; this is itself a finding about V10):

- PARADD (VS_OK 1, 52 frames): `F0 766.6 | F0DYN 384.3 | F1B 740 |
  F2B 2329 | F2B_IQR 1247 | F3B 2968 | HNR 4.0 | TILT 0.0 | MOD4 0.551`
- ARTIC: VS_OK 0 (0 clean frames; max peak 0.398) — fails objective prong.
- SPECSTAT: VS_OK 0 (0 clean frames) — fails objective prong.

Attack battery results (frozen binary):
- R1 (metric puppet, iteration 2): VS_OK 1, 721 frames.
  `F0 637.9 | F0DYN 163.1 | F1B 798 | F2B 2063 | F2B_IQR 658 |
  F3B 2407 | HNR 6.0 | TILT 0.6 | MOD4 0.842`.
  Passes 6/9 (V-F0, V-F0DYN, V-F1, V-F2, V-TILT, V-F2DYN).
  Fails V-F3 (off 407 Hz), V-HNR (not nearer than PARADD), M-MOD
  (off 0.43 vs tol 0.402). The puppet WAV is NOT committed (attack
  artifact, workdir only).
- R2 (anchor + 6 dB wash): VS_OK 0 (1 clean frame) — objective FAIL, as
  designed. A scene whose voices are buried cannot be judged child-like.
- R3 (anchor x4 level): 9/9-equivalent, signature identical to anchor
  (F2B 2100 vs 2104, else byte-comparable) — level invariance confirmed.
- R4 (identity): anchor vs itself — 9/9, D = 0 (by construction).

## 9. What this protocol does not claim

- It does not define "child-likeness" in full; it operationalizes a
  measurable, attack-tested approximation. The ear panel is load-bearing.
- The anchor is one playground, one afternoon. Tolerances come from
  literature + within-anchor variance, not from a population of
  playgrounds. A fork that sounds like children from a different
  playground but misses a bar is a protocol limitation, to be argued to
  Micah with evidence — not silently waived.
- The instrument cannot hear. It measures. The day the instrument and the
  ears disagree, the ears win and the instrument gets rebuilt. That is
  what happened to the nine V10 bars, and this protocol is built to let it
  happen again.
