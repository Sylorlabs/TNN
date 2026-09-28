# Preregistration — compiler-bug candidate (a): imported top-level const lowering

**ID:** CB-A-PREREG-2026-09-20 (wave12 workstream 3)
**Frozen:** 2026-09-20, BEFORE any znc run for this candidate.
**Toolchain:** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
(znc 2026.07.0-dev), flags `--no-zagd --no-analyze --no-foreground-cache`.
Default target Linux x86-64; secondary probe `--target arm64` (Linux AArch64 ELF)
executed under `toolchain/bin/qemu-aarch64-static`.

## Background claim under test
Doc-sweep (tier1_batch1 finding [3], tier1_batch2 file 38, tier1_batch5, tier1_batch6)
reports a fourth znc defect: top-level Zag `const` decls are "represented as
annotated nullary functions", and imported references materialize as
function/fat-function values — imported i64 expected values arrived as
address-like `610473...`. Root-cause pointer: `selfhost/parse.zag` registers
const names in each Parser's separate `consts` list; an imported caller does not
inherit that parser-local list. Observed on pinned macOS ARM64 compiler
`znc_macos_arm64_7cacbfc0` (not available in this lab).

## Reproducer (pure Zag, minimal)
- `repro/kconst_defs.zag`: top-level `const K_I32:i32=42;` and
  `const K_I64:i64=610473;`, plus `fn defs_val()i32 { return K_I32; }`
  (same-module control).
- `repro/kconst_main.zag`: `@import("kconst_defs.zag")`; `fn main()i32`
  prints (a) `K_I32` referenced directly, (b) `K_I64` referenced directly,
  (c) `K_I32+8` (imported const in arithmetic), (d) `defs_val()` (same-module
  control); exit code = 0 iff all four match authored values, nonzero otherwise.

## Expected-vs-actual criterion (frozen)
- EXPECTED: stdout exactly `42 610473 50 42` (whitespace-normalized), exit 0.
- BUG REPRODUCED: any imported-module reference yields a non-authored value
  (e.g. an address-like large integer such as `610473xxxx`, or 0) while the
  same-module control yields 42. That shape = the reported defect.
- NOT REPRODUCED: stdout/exit exactly as expected on both targets.

## Decision rules
- If reproduced on x86-64: confirm on arm64 target; trigger is backend-independent
  (front-end), supporting a NEW BUG verdict.
- If NOT reproduced on x86-64 but reproduced on arm64: trigger is backend-specific;
  still a candidate NEW BUG (distinct from known arm64 syscall bug — see below).
- If NOT reproduced on either: honest verdict NOT-REPRODUCED on the lab toolchain;
  the macOS-ARM64 doc evidence stands as unreplicated historical evidence only.

## Pre-registered reconciliation (adversarial; must be attempted before NEW verdict)
- vs ZNC-2026-09-19-001 (hot-path miscompile): 001 is native array-store codegen
  corruption in multi-store contexts. This repro contains no arrays/stores; a
  const-resolution failure cannot be 001's mechanism. Predict: distinct.
- vs wasm codegen breakage: wasm bug is a whole-backend limitation (`call to
  unknown function` for `_zag_println`, host-import requirement). Candidate (a)
  was reported on native ARM64. Predict: distinct.
- vs arm64 syscall-lowering: that bug drops the syscall number when lowering the
  `_zag_clock_monotonic_ms` helper (169 vs 116). Candidate (a) would fire for ANY
  imported const reference, no syscalls involved. Predict: distinct.
- NEW-BUG bar: reproduced here AND unexplained by all three known bugs above.

## Kill/validity notes
- Deterministic: two runs per binary must be byte-identical in output/exit.
- No binaries, `.zagd.semantic-ready`, or `.zag-cache` committed (lab law).
- Verdict options: NEW BUG (write ZNC-2026-09-20-00X) / FACET OF KNOWN BUG
  (name it + evidence) / NOT-REPRODUCED (report what was tried).
