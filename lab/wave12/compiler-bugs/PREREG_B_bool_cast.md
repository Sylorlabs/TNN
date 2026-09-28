# Preregistration — compiler-bug candidate (b): compound-bool→i32 cast

**ID:** CB-B-PREREG-2026-09-20 (wave12 workstream 3)
**Frozen:** 2026-09-20, BEFORE any znc run for this candidate.
**Toolchain:** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
(znc 2026.07.0-dev), flags `--no-zagd --no-analyze --no-foreground-cache`,
default target Linux x86-64. (arm64 probe only if x86-64 is inconclusive.)

## Background claim under test
Doc-sweep (tier1_batch7 finding [16], V92 V4_PATCH_NOTES): "range branches in
`r27s4_count_valid` returning compound boolean expressions cast directly to
`i32` did not produce the required `1` for valid scalars under the local Zag
compiler" — patch replaced casts with explicit `return 1` / `return 0` branches.
"No R27 values changed."

## Reproducer (pure Zag, minimal, NO arrays/allocations — see reconciliation)
`repro/kbool_main.zag`, single file, `fn main()i32`:
- `fn in_range(v:i64)i32 { return (v>=2001 && v<=2008) as i32; }`
  (the exact reported shape; also mirrors `cl_is_status` in common.zag)
- `fn eq5(v:i64)i32 { return (v==5) as i32; }` (single-comparison control)
- `fn or_case(a:i64,b:i64)i32 { return (a<0 || b<0) as i32; }` (`||` compound)
- `fn not_case(v:i64)i32 { return !(v>=2001 && v<=2008) as i32; }` (negated compound)
- `fn let_case(v:i64)i32 { let ok:i32=(v>=2001 && v<=2008) as i32; return ok; }`
  (let-bound variant)
- main prints one line per case over below/edge/inside/edge/above inputs, and
  returns 0 iff every line matches its expected value.

## Expected-vs-actual criterion (frozen)
- EXPECTED: `in_range` → 0,1,1,1,0 for inputs 2000,2001,2005,2008,2009;
  `eq5` → 0,1,0 for 4,5,6; `or_case` → 1,1,0 for (-1,0),(0,-2),(1,2);
  `not_case` → 1,0 for 2000,2005; `let_case` → 0,1 for 2000,2005.
  Exit 0 and stdout byte-exact.
- BUG REPRODUCED: any true compound expression yields a value ≠ 1
  (e.g. 0, 256, garbage, address-like), while the single-comparison control
  yields correct results. That shape = the reported bool-cast defect.
- NOT REPRODUCED: all lines exact on two runs (byte-identical output/exit).

## Decision rules
- If reproduced: disambiguation check — the repro contains zero array stores,
  zero allocations, zero syscalls, single file (no imports). ZNC-2026-09-19-001
  is an array-store miscompile; it cannot explain a no-array bool-cast failure.
- If NOT reproduced: honest verdict NOT-REPRODUCED on the lab toolchain; doc
  evidence (V4 patch notes) stands as unreplicated historical evidence.

## Pre-registered reconciliation (adversarial; must be attempted before NEW verdict)
- vs ZNC-2026-09-19-001: repro deliberately contains no arrays → 001's mechanism
  (array-store corruption, phantom stores) is structurally inapplicable.
  Predict: distinct.
- vs wasm codegen breakage: repro runs on native x86-64, no wasm involved.
  Predict: distinct.
- vs arm64 syscall-lowering: no syscalls, no `_zag_*` helpers in repro.
  Predict: distinct.
- NEW-BUG bar: reproduced here AND unexplained by all three known bugs.

## Kill/validity notes
- Deterministic: two runs per binary must be byte-identical in output/exit.
- No binaries committed (lab law).
- Verdict options: NEW BUG (write ZNC-2026-09-20-00X) / FACET OF KNOWN BUG
  (name it + evidence) / NOT-REPRODUCED (report what was tried).
