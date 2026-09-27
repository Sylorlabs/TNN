# Novelty Audit (EXP1b)

## Method

Text search of the committed training mass (kb/kb.txt, kb/kb_p.txt) for
each A1 sketch's composed steps (the composition, not just the words).

## Training mass

kb/kb.txt contains H1..H8 (taught single-step heuristics):
- H1: mote on cell -> EAT
- H2: move toward nearest mote
- H3: storm flee
- H4: (not used)
- H5: critical energy -> seek mote
- H6: WAIT when nothing visible
- H7/H8: (not used)

kb/kb_p.txt contains P's phased strategy (gather, combine, ward, survive).

## A1 sketches

All 5 sketches describe the same behavior:
- Execute primitive plans in index order
- EAT on cell (H1)
- Flee storm (H3)
- Seek mote when energy < 25 (H5)
- WAIT (H6, and via plan WAIT tokens)

## Findings

Every "step" in the A1 sketches is either:
1. A taught single-step heuristic (H1, H3, H5, H6), found verbatim in kb.txt, or
2. A random primitive action (L, R, W, T, D, C) from the plan enumeration,
   which is not a "composition" but a single token.

There is no composed multi-step sequence in the sketches that is not
found in the training mass. The "strategy" is a trivial recombination.

## Verdict

K4 FIRES. The winning strategy is a trivial recombination of taught
heuristics and random actions (per EXP1 PREREG section 2). The invention
claim is killed.
