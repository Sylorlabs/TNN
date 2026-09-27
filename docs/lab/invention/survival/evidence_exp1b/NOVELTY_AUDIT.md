# Novelty Audit (EXP1b)

## Method

Text search of the committed training mass (kb/kb.txt, kb/kb_p.txt) for
each A1 sketch's composed steps (the composition, not just the words).

## Training mass

kb/kb.txt contains H1..H8 (taught single-step heuristics):
- H1: energy below 40 and a mote within 3 cells -> move toward nearest mote
- H2: storm starts within 20 ticks and you are in the zone -> move toward
  nearest cell outside the zone
- H3: storm active and you are in the zone without shelter -> move toward
  nearest safe cell
- H4: energy below 25 -> move toward nearest active mote (EAT if a mote
  shares the cell)
- H5: a mote shares your cell -> EAT it
- H6: hold two or more items and you are safe -> you may try COMBINE
- H7: otherwise -> move toward nearest active mote
- H8: keep energy above 0

Correction (2026-09-27, independent red-team review): an earlier version
of this file mislabeled the heuristics (H1 as "mote on cell -> EAT",
H5 as "critical energy -> seek mote", H6 as a WAIT rule). The labels
above match kb.txt verbatim. The mislabeling did not affect the verdict:
no composed multi-step sequence in the sketches appears in the training
mass under either labeling.

kb/kb_p.txt contains P's phased strategy (gather, combine, ward, survive).

## A1 sketches

All 5 sketches describe the same behavior:
- Execute primitive plans in index order
- Move toward mote when energy low (H1), EAT on cell (H5)
- Flee storm (H2/H3)
- Emergency seek when energy below 25 (H4)
- WAIT (via plan WAIT tokens; no WAIT rule is taught)

## Findings

Every "step" in the A1 sketches is either:
1. A taught single-step heuristic (H1, H2, H3, H4, H5), found verbatim in kb.txt, or
2. A random primitive action (L, R, W, T, D, C) from the plan enumeration,
   which is not a "composition" but a single token.

There is no composed multi-step sequence in the sketches that is not
found in the training mass. The "strategy" is a trivial recombination.

## Verdict

K4 FIRES. The winning strategy is a trivial recombination of taught
heuristics and random actions (per EXP1 PREREG section 2). The invention
claim is killed.
