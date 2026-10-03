# VENDORING — phase-2 harness sources

All mechanism sources are vendored (copied, not moved) from the phase-1
skeleton so this harness builds standalone. Canonical phase-1 hashes
(recorded 2026-09-20, before any edit):

| File | Canonical sha256 (phase 1) | Vendored sha256 (this dir) |
|---|---|---|
| `se_ingress.zag` | `9da289fb9da657d1917de586acbd74adb2e89716ce50353f6c1b72d6e8ef7043` | identical (unchanged) |
| `se_memif.zag` | `3bd7e2cddf8af133d499e83f37671285468e9ccfa39892910dd473f7826890f2` | differs by ONE preregistered delta (below) |
| `substrate/cl/common.zag` | `8aec83cb4feb83a20bc91c8179d7055d691c155414a359f7014386271aa6168b` | identical (unchanged) |
| `substrate/R33_NATIVE_SHA256_V2.zag` | `9824f6db66a943917dbc7cd5e6862ab0967b7ea83161cfc357bb7d17ca683bcf` | identical (unchanged) |
| `substrate/R33_NATIVE_IO_V1.zag` | `e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8` | identical (unchanged) |

(Note: the vendored `substrate/` tree is the canonical layout — `cl/`
sits beside the two `R33_*` files — so `cl/common.zag`'s bare
`@import("../R33_NATIVE_SHA256_V2.zag")` resolves.)

## Delta vs phase 1 (preregistered in PREREG_SENSES_PHASE2_HARNESS.md §6)

- `se_memif.zag`: `MI_AUDIT_CAP`: 256 → 2048. Rationale: §H runs 1,000
  OBSERVE/KILL cycles (1,990 audited ops); the 256-cap audit silently stops
  recording when full, making the literal §H bar ("entry count equals ops
  issued") unreachable. Op table, refusal codes (-7201..-7210), judgment
  gate, strength-is-declared, slot semantics, PIN/KILL/RECALL preconditions
  — all unchanged. Header comment in the vendored file records the delta.
- Everything else: byte-identical to the canonical copies.

## New in this dir (not vendored)

- `se2_main.zag` — harness driver (modes `harness`, `verify`). New code,
  pure Zag, no RNG/clock/threads/floats.
- `run_phase2_harness.sh` — §F/§G runner script (harness, not mechanism).
- `count_phase2.sh` — counting reporter (harness, not mechanism).
