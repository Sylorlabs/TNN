# R49 meta-autonomy correction — closeout

Date: 2026-09-18  
Status: **PASS**

R49 was preregistered after R48 exposed two failures. It changed only curiosity scoring and self-model exploration, generated fresh randomized test identities after source freeze, and retained update-disabled controls.

## Curiosity

- learnable-process tail allocation: `1.0`
- constant-process tail allocation: `0.0`
- unpredictable-noise tail allocation: `0.0`
- update-disabled learnable allocation: `0.3333333333333333`

The corrected policy uses transition predictability, outcome entropy, non-overlapping rolling learning progress, and decaying novelty. Region names are randomized and carry no policy meaning.

## Self-model

- fresh best-strategy identification: `1.0`
- update-disabled identification: `0.28125`

The learner uses outcome histories and generic uncertainty exploration. Evaluator competence tables are not exposed to it.

`learn_authority = 0`; canonical R27 remains unchanged.

