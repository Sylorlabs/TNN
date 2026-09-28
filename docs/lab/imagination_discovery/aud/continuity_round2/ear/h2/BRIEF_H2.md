# H2 ear brief — sol-H2: bridge_world source/room/texture seams

## What you are hearing

Three pairs of 2-second excerpts from the B-γ kids scene (children playing,
all captured field recordings), each centered on a transition.

In each pair, one excerpt is centered on a **bridge edge** — the moment the
`bridge_world` texture (wash/wind/feet/distant-play) enters or exits — and the
other is centered on a **matched ordinary transition** (a regular foreground
event onset at the same local loudness, not at any bridge edge).
Blinded: A/B assignment is in `KEY_H2.sealed.txt` — do not open it before
judging.

- `h2_pair1_A.wav` / `h2_pair1_B.wav` (scene s5: bridge entry 14.4 s)
- `h2_pair2_A.wav` / `h2_pair2_B.wav` (scene s30: bridge entry 24.8 s)
- `h2_pair3_A.wav` / `h2_pair3_B.wav` (scene s2: bridge exit 26.8 s)

## The question (answer per pair)

**Which excerpt has the discontinuity?**

- A discontinuity: a sudden change of room, source, or texture at the center
  of the excerpt — as if the world cuts to a different recording, the air
  changes, or a seam shows.
- If neither or both sound continuous, say so — "no difference" is valid.

## Context (machine side, for after you judge)

The machine test (300 bridge edges vs 299 loudness-matched ordinary
transitions, one-sided Mann–Whitney U) found no significant seam signature:
1 ms slope, spectral flux, and 50 ms spectral distance are all *lower* at
bridge edges than at ordinary transitions (n.s.); only the 2–20 Hz modulation
change is slightly higher at bridges (median 0.87 vs 0.75, p=0.40, n.s.).
The machine could not kill the hypothesis only because that one median runs
the wrong way. Your ears decide: if the bridge excerpts sound as continuous
as the ordinary ones, the seam is inaudible and the hypothesis dies by ear.
