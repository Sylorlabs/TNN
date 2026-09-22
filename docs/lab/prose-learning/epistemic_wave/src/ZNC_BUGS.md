# znc Compiler Bugs Found (2026-09-22)

## ZNC-2026-09-22-001: Multiple structs with slice fields fail
**Status:** CONFIRMED with minimal reproducer

**Reproducer:** `tstruct3.zag` — 3 structs (Lin, Idx, Idx) with `[]u8` fields.
Allocate structs, then assign slice fields. Fields read back as empty (len=0).

**Workaround:** Use a SINGLE struct with all slice fields (World pattern).
Proven in `tbone.zag` — single World struct with 20+ slice fields works.

**Also:** Fields must be assigned IMMEDIATELY after struct allocation.
Pattern that works:
```zag
let s:*T=nio_alloc(64) as *T;
s.*.field=nio_alloc(N);  // immediately, no intervening allocs
```
Pattern that fails:
```zag
let s1:*T=nio_alloc(64) as *T;
let s2:*T=nio_alloc(64) as *T;
s1.*.field=nio_alloc(N);  // fails, reads as empty
```

## ZNC-2026-09-22-002: Large nio_alloc causes segfault on program exit
**Status:** CONFIRMED with minimal reproducer

**Reproducer:** `texit2.zag` — allocate 8MB + 7.68MB via nio_alloc.
Program logic completes, prints output, then segfaults (exit=139) during exit cleanup.

With small allocations (100 bytes), exits cleanly (exit=0).

**Impact:** Programs requiring large buffers (100k corpus needs ~21MB) will
segfault on exit. Output is correct before the segfault. Workaround: runner
must capture stdout and ignore exit code, or check output content.

## ZNC-2026-09-22-003: Struct size must account for 16-byte slices
**Status:** CONFIRMED (from AGENTS.md, verified)

Slice-typed struct fields (`[]u8`) occupy 16 bytes (ptr+len), not 8.
Undersized `nio_alloc(N) as *Struct` silently corrupts heap.

## Summary
The single-World-struct pattern with immediate field assignment is the
reliable way to manage state in znc. Large allocations work for program
logic but cause exit-time segfaults (output remains valid).
