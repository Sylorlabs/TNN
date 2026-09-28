# NOVELTY AUDIT (K4): Experiment 1

Question: is the I arm's strategy novel, or a trivial recombination?

## What the I arm does

The I arm generates candidate plans from six schemas:
seek-crystal, seek-mote, COMBINE, DROP, void-seek, and wait.
It scores candidates with hand-authored bonuses favoring productive
compositions (e.g., crystal-seeking before COMBINE, mote-seeking for energy).
It selects the best candidate deterministically and executes it open-loop
for up to six schema steps, then replans.

## Findings

1. The schemas themselves (seek-crystal, seek-mote, COMBINE, DROP) are
   the same primitives taught to P and available in the shared KB.
   No new primitive was invented.

2. The candidate ordering and scoring bonuses were authored by the
   implementer to favor compositions known to be productive.
   This encodes the solution rather than discovering it.

3. The resulting behavior (gather crystals, build, forage) is a
   recombination of taught elements, not a novel composition.

4. K1 already killed H1 (I-survive 574 did not beat R 600), so the
   invention claim fails on performance regardless of novelty.

## Verdict

K4: the strategy is a trivial recombination with authored cuing.
Even if H1 had passed K1, K4 would kill the invention claim.
