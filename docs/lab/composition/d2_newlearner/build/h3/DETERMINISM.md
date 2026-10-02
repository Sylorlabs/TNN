# H3 Determinism Notes

**Binary SHA-256:** `2357e86844e75041f9ce3423f600c0e15560a6806a3abfc6590b50ef6b4a4e43`
**Date:** 2026-09-28

## Design for determinism

- Zero RNG anywhere in decision paths (Micah's law). No timestamps, no
  pointer-derived values, no hash iteration in any decision.
- All tie-breaks are positional/index-based (nearest target, lowest cell on
  ties, lowest OBS index on ties).
- Fixed-size arenas allocated once at startup; explicitly zeroed. No
  allocator-dependent iteration order (no maps/sets).
- One reusable input buffer; no history accumulation.

## Test results

| Test | Result |
|---|---|
| FW-48 deliberative, 3 consecutive runs | byte-identical action traces + RESULT lines (200 ticks) |
| FWF-64 deliberative, 3 consecutive runs | byte-identical (320 ticks) |
| FW-48 deliberative, 2 runs under `MALLOC_PERTURB_=165` | byte-identical to each other AND to the unperturbed runs |
| FW-48 fixed-order, 2 runs under `MALLOC_PERTURB_=165` | byte-identical |

Repeated traces are byte-identical, including under allocator perturbation.
The uninitialized-heap hazard (AGENTS.md znc lesson) is addressed by explicit
zeroing of all arenas at startup (`z_alloc` zeroes; `card_reset` re-zeroes
card state; OBS state zeroed at startup and fully overwritten per parse).
