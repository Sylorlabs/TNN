# VERDICTS — wave12 workstream 3: compiler-bug candidates

**Date:** 2026-09-20. **Toolchain:** znc_linux_x86_64_abed8aa1
(SHA-256 `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`),
flags `--no-zagd --no-analyze --no-foreground-cache`; arm64 via `--target arm64`
+ `toolchain/bin/qemu-aarch64-static`. Preregs frozen in commit `ab002188d838`
BEFORE any compiler run. All runs deterministic (two runs per binary,
byte-identical stdout/exit).

## Candidate (a): imported top-level const lowering — NEW BUG: ZNC-2026-09-20-001

Reproduced on the lab toolchain's **arm64 backend**; clean on x86-64.
Imported top-level `const` references lower to address-like function values
(e.g. authored `42` → `8383760`; authored `610473` → `365080603896`); the
defining module's own references, the importer's own consts, and imported
*functions* are all correct. Deterministic per binary.
Trigger: imported-module const ref + arm64 codegen (both this compiler's
`--target arm64` and, per doc evidence, the pinned macOS ARM64 `7cacbfc0`).
Reconciliation: distinct from ZNC-2026-09-19-001 (no arrays in repro; x86-64
clean), from the wasm breakage (different target), and from the arm64
syscall-lowering bug (no syscalls; any imported const triggers it).
Full write-up: CHAR_A_const_import.md (repro, trigger matrix, filing note).
Raw logs: RAW_A_const_import.txt. Sources: repro/kconst_defs.zag,
repro/kconst_main.zag, repro/kconst_main2.zag.

## Candidate (b): compound-bool→i32 cast not returning 1 — NOT-REPRODUCED

24 preregistered case-lines across 7 shapes (direct return of
`(v>=2001 && v<=2008) as i32`, single-comparison control, `||`, negation,
let-bound, nested if-branch "range branches", triple-AND, i32 operands,
mixed precedence), on x86-64 AND arm64: every value exact, every exit 0,
every run-pair byte-identical. The shipped R34 harness's identical
`cl_is_status` shape passing 24/24 on this toolchain independently corroborates.
The V4 patch-notes report stands as unreplicated historical evidence —
possibly specific to the unavailable macOS ARM64 pinned compiler, or already
fixed. No bug ID assigned (a negative must not consume one). If that compiler
becomes available, re-run the repros before filing.
Full write-up: CHAR_B_bool_cast.md. Raw logs: RAW_B_bool_cast.txt.
Sources: repro/kbool_main.zag, repro/kbool_main2.zag.

## Net change to the znc bug inventory
- ZNC-2026-09-19-001 — hot-path (array-store) miscompile — unchanged.
- wasm codegen breakage — unchanged.
- arm64 syscall-lowering (dropped syscall number) — unchanged.
- **ZNC-2026-09-20-001 — NEW: arm64 backend mislowers imported top-level const
  references as function values** (this workstream).
- Compound-bool→i32 cast — NOT-REPRODUCED on lab toolchain; no ID; historical
  report retained, not promoted.

## Files committed (this workstream, docs/lab/wave12/compiler-bugs/)
PREREG_A_const_import.md, PREREG_B_bool_cast.md (frozen pre-run),
repro/{kconst_defs,kconst_main,kconst_main2,kbool_main,kbool_main2}.zag,
RAW_A_const_import.txt, RAW_B_bool_cast.txt,
CHAR_A_const_import.md, CHAR_B_bool_cast.md, VERDICTS.md.
No binaries, .zagd.semantic-ready, or .zag-cache committed.
