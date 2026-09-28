# H1 ear brief — sol-H1: 10 ms natural-envelope dips

## What you are hearing

Three pairs of 30-second renders of the same B-β kids scene (children playing:
shouts, squeals, laughs, feet, thumps), all from captured field recordings.

In each pair, one clip is the **full mix** (foreground events + world bed) and
the other is the **bed only** (foreground events removed, bed alone).
The pairs are blinded: A/B assignment is in `KEY_H1.sealed.txt` — do not open
it before judging.

- `h1_pair1_A.wav` / `h1_pair1_B.wav`
- `h1_pair2_A.wav` / `h1_pair2_B.wav`
- `h1_pair3_A.wav` / `h1_pair3_B.wav`

## The question (answer per pair)

**Which clip CUTS OUT vs FLOWS?**

- "Cuts out": you hear moments where the sound seems to drop out, vanish, or
  stutter — brief gaps or holes in the texture, as if the world blinks.
- "Flows": the sound continues without such dropouts.

If you hear no difference on this dimension, say so — "no difference" is a
valid answer.

## Context (machine side, for after you judge)

The machine test found envelope dips (1 ms minima below the 5th-percentile
floor) lasting 100–990 ms in the full mixes, concentrated in dense-overlap and
sparse-gap regions — not at phrase boundaries. The bed alone also shows
100–280 ms dips. The machine verdict is SURVIVES (the dips are real by the
meter), but your ears outrank the meter: if the full mix flows and nothing
cuts out to you, the "defect" is inaudible and the hypothesis dies by ear.
