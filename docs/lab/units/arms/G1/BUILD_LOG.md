# G1 BUILD_LOG

**Arm:** G1 — Pressure-driven coarsening  
**Date:** 2026-09-21  
**Compiler:** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` (frozen)

## Build commands

```
cd ~/workspace/tnn-lab/units/arms/G1
~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 cl/arm.zag -o work/build/g1
```

Single binary; mode selected via `argv[1]` (e.g. `./g1 m1-1x-prose <corpus-root>`).

## Corrections during build (2026-09-21)

1. **Struct init:** Replaced invalid `let s:G1; g_init(...)` with `let s:G1=g_new(...)` (struct-returning constructor).
2. **Local struct field access:** `s.*.field` invalid on local struct values; use `s.field`. Pointer params still use `s.*.field`.
3. **Flags zero-init:** Explicitly zero every `flags` entry in `g_init`; allocator does NOT zero.
4. **Variable order:** Moved M3 freeze-check variable definitions after `surv_t`/`fresh_t`.
5. **JSON helper:** Fixed malformed METRIC_JSON (missing comma after mode field).
6. **Ledger clamp:** `g_init` clamps ledger to ≤2^25 bytes (524288 entries); znc panics indexing a single slice past 2^25. M2's `50*n` ledger hit 222MB for t2-prose. LEDGER-BOUND truncation documented.
7. **Eviction fallback:** Declared FIFO oldest-unpinned eviction (audited policy_code=1) for full-store ingest; never pins, never random.
8. **M8 store image:** Hashes full slot arrays + insertion queue + dedup + counters (not just slots).

## znc issues encountered

- ZNC-2026-09-21-002: `slice as *u8` does NOT yield data pointer; use word→byte decomposition.
- ZNC-2026-09-21-003: slice struct fields are 16 bytes (ptr+len); size accordingly.
- ZNC-2026-09-21-004: annotated slice-let aliasing local struct field rejected; route through pointer.
- ZNC-2026-09-21-005: `nio_alloc(N) as *Struct` fails for large structs; use globals/handles.
- ZNC-2026-09-21-006: free through nested value fields corrupts heap; use flat structs.
- Bare `return` in void fn fails; use `return;`.
- Never name a function `zalloc` (builtin collision); use `z_alloc`.
- `_zag_raw_syscall` takes exactly 7 args; paths must be NUL-terminated via `z_cstr`.
- `_zag_arg(n)` is non-owned; never `nio_free` it.
- `_zag_strcmp` returns 1 on equality.
- `[]u8` `==` is not content identity; use integer selectors.
- Uninitialized heap arrays NOT reliably zeroed; initialize all sentinel arrays.

## Test runs

- `m2-t1-prose`: 2.5s, 100.0/100.0.
- `m1-1x-prose`: 100.0/100.0, 84731 units.
- `m1-1x-code`: 100.0/100.0, 148678 units.
- `m3-1x`: 39s, survival 100.0, fresh 94.6, K3 FIRES (see DEATH_CERTIFICATE.md).

## Artifacts (not committed)

- `work/build/g1` (binary), `work/build/smoke1/` (smoke outputs), `cl/*_test*`, `cl/dbg*` — all removed or excluded.
- Only source (`cl/arm.zag`), docs (`ARM_SPEC.md`, `BUILD_LOG.md`, `DEATH_CERTIFICATE.md`), and text evidence committed.
