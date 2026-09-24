# CREW A — fork A-fmt: deterministic parallel formation. Results 2026-09-24.

## Mechanism
New file `src/form_pfmt.zag` (pure Zag, pinned toolchain), same deterministic
formation algorithm as `form_par`, three modes:
- `seq <theme> <out>` — reference sequential formation
- `shard <theme> <shard-out> <k> <S>` — formation over directive-shard k of S
  (each shard owns a contiguous block; RESPOND resolution consults the full
  spec with immutable semantics; each comment is assigned to the shard of its
  following directive — a same-comment-on-every-shard bug was caught and fixed)
- `assemble <out> <S> <shard...>` — order-preserving concatenation
Limits raised to 8,192 directives/specs/slots + larger buffers (no spec change
to the algorithm).

## Identity (prereg §2.1)
- `theme_v1` seq == original `form_par` output: byte-identical.
- Generated `bigtheme` (4,000 directives + headers/STRUCT/INST, 571 RESPONDs):
  seq == S=8 assembled → SHA-256
  `31ceb5f91289f66a6eb0e5e8aa55d88441274d0794a6b393b9f4150df714386b`,
  byte-identical. Also S=1, S=2, S=64, and `theme_v1` S=4 — all exact.

## Performance (honest, this implementation, this environment)
- Sequential formation, bigtheme: CPU min-of-5 **0.174 s**.
- One S=8 shard: CPU min-of-5 **0.098 s**.
- 8 shards on a loaded 2-CPU VM: **1.612 s wall** (concurrent) / 8.451 s
  (sequential launch, same loaded VM); observed ≈0.07× sequential on one
  batch — every shard reparses the whole theme and a pass-2 assembles
  serially, so the replicated-parse serial fraction dominates at this
  theme size, and the VM (load avg 14.5–17.5 on 2 CPUs) penalizes the
  parallel launch.
- The dive prototype's projected 1.67–8.65× formation speedups are for a
  different implementation's regime; **this real implementation shows NO
  measured formation speedup and a wall regression on the loaded VM.**
  Do not claim a speedup. Rendering dominates E2E anyway (~1.03–1.06×
  projected E2E from the prototype; unverified and not claimed here).

## Fork verdict: mechanism PROVEN (exactness at all S), speedup NOT
## demonstrated. A-fmt is a determinism result, not a performance result.
