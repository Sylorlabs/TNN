# FINDINGS_v9 — "one scene" rebuild (NEW clip for Micah's ears)

**Date:** 2026-09-23
**Clip (NEW):** `clips/b_alpha_kids_1e_i_v9_onescene.wav`
**SHA-256:** `2fbcac7b3f0d3bc05418fdc0d5e303a4d632e583f8c94d5c81843f45a0a85a89`
**Source:** `src/render_v9.zag` (pure Zag; Python only for forensic measurement)
**Determinism:** two renders byte-identical (`cmp` clean)

Micah's verdict on v8: "Sounds like someone tried to fuse a bunch of clips
together but it's not a consistent sound of children playing."
His creative law: never fuse/force clips together — imagine ONE consistent
scene: the mood, the type of children, the age, one consistent sound in the
head. Default: little kids in a playground.

## Diagnosis: why v8 felt fused (measured, not guessed)

v8's 131-atom catalog spans FIVE source recordings, and the score drew from
all of them in sequence:

| fno | file | material | atoms used in v8 |
|---|---|---|---|
| 0 | w1.wav | Berlin playground | voices |
| 1 | w2.wav | dozen children, playground | laugh/footsteps/voices |
| 2 | w3.wav | single 4-year-old laughing | laughter |
| 3 | w4.wav | children in park | laughter/voices |
| 4 | w5.wav | children playing janken (Tokyo) | laughter |

Different continents, different mics, different rooms, different children,
different ages — pasted in sequence. The bed was worse: a granular wash of
textures from catalog3 (ocean material) + catalog.bin tx4. The "air" itself
changed rooms every few seconds. The score was honest collage; the ear heard
every seam. Additionally v8 time-stretched atoms 0.90–1.14×, shifting
formants so one child sounded like several.

## Rebuild: scene-first (v9)

- **ONE WORLD:** every atom and every bed chunk comes from w2.wav ("dozen
  children on playground", 48.8 s, one mic, one place). fno==1 filter:
  12 laugh + 7 voice + 25 footstep atoms, all from the same recording.
- **CAST, not salad:** laughter cluster 2 (9 atoms) and cluster 0 (3) recur
  as the same laughing kids; voice clusters 0/1/2 (4/1/2 atoms) recur as
  the same calling kids. Round-robin reuse = the same child heard twice,
  which reads as one continuous kid, not a parade of strangers.
- **ONE MOMENT, fully composed (no hash-walk):** 0–6.5 s the yard is
  already alive (running feet, two kids calling); 6.5–12.5 s a chase game;
  12.5–16.5 s one trips (stumble, thud, gasp, a held breath of bed);
  16.5–23 s everyone laughs it off; 23–30 s steps slow and recede, last
  calls, the air breathes out. A continuous footstep line runs under the
  whole scene (gap 0.24–0.70 s by phase) — locomotion as continuum.
- **NATURAL RATE:** ratio = 1.0 on every event. One child keeps one voice.
- **Bed = the world's own air:** the 8 quietest 1.5 s windows of w2
  (≥2 s apart, deterministic greedy pick), joined into a seamless
  equal-power ring, traversed contiguously with v8's rare-reseed
  (mean ~9 s) + zero-phase macro-envelope machinery, two-pass scaled
  to the same −37 dBFS target.

Kept from v8: seamless ring technique, rare deterministic reseeds,
macro-envelope follower, 8 ms attack / 500 ms release staging,
class-median levels, EVENT_TRIM 0.5, transparent limiter-only mastering
(0 samples limited), deterministic streams, byte-identical reruns, no RNG.

## Measurements

Frozen nine-bar gate (gate.zag, unchanged bars) — full mix:

| bar | v9 | bar limit | v8 | real anchors |
|---|---|---|---|---|
| G-PER | **0.177** PASS | ≤ 0.35 | 0.204 | 0.104–0.261 |
| G-STA | **1.756** PASS | ≤ 3.0 dB | 2.68 | 0.73–1.93 |
| G-LURCH | 4.675 PASS | ≤ 5.0 dB | 4.59 | 2.03–3.65 |
| G-DRIFT | 291.8 PASS | ≤ 800 Hz | 585 | 418–522 |
| G-FLUXm | 245.4 PASS | ≤ 350 | 271 | 148–220 |
| G-SIL1 | 0.000 PASS | ≤ 0.02 | 0.000 | 0.000 |
| G-SIL2 | 0.000 PASS | ≤ 0.5 s | 0.000 | 0 |
| G-CLIP | 0.127 PASS | ≤ 0.95 | 0.149 | 0.084–0.133 |
| G-CREST | 7.05 PASS | ≤ 14 | 7.96 | 4.19–4.98 |
| WARN | none tripped | | | |

G-STA 1.756 dB now sits INSIDE the real-anchor envelope (0.73–1.93) —
the dynamics read like a real playground recording, not a montage.
W-DENSE max 5 onsets/2 s (no warn); W-ENDS/W-DYN ok.

Modulation spectrum (forensic, not a frozen bar):

| material | 0.5–2 Hz | 2–5 Hz | note |
|---|---|---|---|
| v9 bed-only | 8.65% | 31.97% | |
| raw w2 chunks (no processing) | 9.98% | 33.20% | the source itself |
| full w2.wav | 12.33% | 10.76% | |
| v9 full mix | 21.84% | 19.18% | footsteps 3–4 Hz + laugh phrasing ~1 Hz |
| v8 full mix | 9.2% | — | sparser events |
| v8 bed / aporee anchor | 3.0% / 1.9% | — | |

The bed's modulation is inherited verbatim from w2's own quiet air
(rendered bed ≡ raw chunks to within 1.5 points) — distant playground
rhythm at ~3.5 Hz, not processing wander. The ring/junction/flatten
machinery adds nothing measurable. The full-mix 0.5–2 Hz is the composed
event rhythm (chase footsteps, laugh phrasing), i.e. the scene itself.

No dips (no near-silent gaps ≥150 ms outside the 30 ms end fades), no
cutouts, zero hard discontinuities, zero clipped samples, limiter engaged
on 0 samples. Peak −17.9 dBFS (natural scene levels, same as v8).

## Honest self-assessment (for the record)

What v9 fixes by construction: single acoustic space, single mic,
recurring cast, natural rates, one composed moment, bed from the same
air. The fused-clips mechanism is gone — there is nothing left to fuse.

What I cannot verify without ears: (1) the cluster proxies are
descriptor-based, not human-verified identities — cluster 2's 9 laugh
atoms may be several similar-sounding kids, not one; (2) I cannot hear
whether the composed chase/trip/laugh arc reads as a real moment or as
a well-behaved montage; (3) the bed's inherited 2–5 Hz distant-play
rhythm could read as life or as restlessness — Micah's ears decide.

New kill bar (single-scene coherence): a blind listener should hear one
continuous real moment, not a montage. The gate passes; the ears judge.

## Files

- `src/render_v9.zag` — the renderer (committed)
- `clips/b_alpha_kids_1e_i_v9_onescene.wav` — NEW clip (committed)
- `FINDINGS_v9.md` — this file (committed)
- `measure_tremolo.py` — forensic measurement only (not committed; Python)
