# H2 Determinism

## Method
Three full P0-F episodes (F-0, 120 ticks) through the real harness protocol
(teaching + cards + OBS loop), comparing the learner's action traces:
- Run 1 vs Run 2 (same binary, same inputs)
- Run 1 vs Run 3 with `MALLOC_PERTURB_=165` (adversarial allocator)

## Results
- Run 1 trace SHA-256 (first 16 hex): `1227bc8a36f69a4a`
- Run 2 byte-identical to Run 1: **True**
- MALLOC_PERTURB_=165 byte-identical to Run 1: **True**

## Why deterministic
- Pure Zag; zero RNG in decision paths (no random exploration, no stochastic tie-breaks).
- All arenas explicitly zero-initialized at allocation (`z_alloc`); no uninitialized reads.
- Planner ties broken by lowest candidate index (strict-greater replacement).
- BFS ties broken by fixed neighbor order (LEFT then RIGHT).
- Estimator updates are pure functions of OBS history.

## Binary
- SHA-256: `432c836b6c32832072bfebb60ec143147959e6dc6dbad81f59fe437ae92a84d5`
