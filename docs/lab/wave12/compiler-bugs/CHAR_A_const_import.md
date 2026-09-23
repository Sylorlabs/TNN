# Characterization — candidate (a): imported top-level const lowering

**Status:** REPRODUCED on lab toolchain (arm64 backend). Raw evidence: RAW_A_const_import.txt.
**Verdict:** NEW BUG → **ZNC-2026-09-20-001**.

## Exact trigger conditions
1. A top-level `const` declared in module M (e.g. `const K_I32:i32=42;`).
2. Module N does `@import("M")` and references the const — directly in `main`,
   inside N's own function, in arithmetic, or cast — any use site.
3. Compile with the **arm64 backend** (`--target arm64` on znc_linux_x86_64_abed8aa1;
   historical report: pinned macOS ARM64 `znc_macos_arm64_7cacbfc0`).

All three must hold. Dropping any one removes the failure:
- Same reference compiled for x86-64 → authored value, exit 0 (A1, A3).
- Reference inside the *defining* module M → correct on arm64 (defs_val()=42, A2).
- Importer's *own* top-level const → correct on arm64 (LOCAL_C=7, A3).
- Imported *functions* → correct on arm64 (A2 control).

## Minimal failing shape
`defs.zag`: `const K:i32=42;` — `main.zag`: `@import("defs.zag")`
`fn main()i32 { let v:i32=K; ... }` → arm64 binary prints `8383760`, not `42`.

## Observed failure mode
The imported const reference lowers to what behaves like a **function/fat-function
address**: the observed values (8383760, 365080603896, 8383720, 16765744, 8383360)
are address-like, stable across runs (deterministic per binary), and arithmetic
on them operates on the wrong base (K_I32+8 → 8383720 = base−40, not 50).
Consistent with the doc-sweep's source pointer: top-level consts are "represented
as annotated nullary functions" and the arm64 backend lacks the handling that
resolves them to their values at import boundaries (cf. `selfhost/parse.zag`
per-Parser `consts` list not inherited by the importing parser — a front-end
resolution defect surfacing only in the arm64 lowering path).

## What correct behavior would be
The x86-64 backend's behavior: the reference resolves to the authored constant
value (42 / 610473), in all positions, with exit 0.

## Reconciliation vs the three known bugs (adversarial, per prereg)
- **vs ZNC-2026-09-19-001 (hot-path array-store miscompile):** 001 corrupts
  *array stores* in multi-store contexts on x86-64. This repro contains zero
  arrays, zero stores; the symptom is a name-resolution/lowering failure
  (function-address values), and the x86-64 backend — where 001 lives — is
  *clean*. Cannot be 001. DISTINCT.
- **vs wasm codegen breakage:** different target entirely; the wasm backend
  cannot even compile this program shape (`_zag_println` → `call to unknown
  function`). DISTINCT.
- **vs arm64 syscall-lowering (dropped syscall number):** that bug is in the
  lowering of the `_zag_clock_monotonic_ms` helper (Darwin 169 vs 116). This
  repro issues zero syscalls and the defect fires for *any* imported const.
  Same backend family (arm64), but different trigger (any imported const vs one
  intrinsic) and different mechanism (const resolution vs syscall-number
  emission). DISTINCT.

## Suggested filing note
Title: `ZNC-2026-09-20-001: arm64 backend mislowers imported top-level const
references as function values`. Include: repro pair (kconst_defs.zag /
kconst_main.zag), trigger matrix (A1–A3), x86-64-clean control, note that the
defect reproduces on both the historical macOS ARM64 pinned compiler
(doc evidence) and this Linux compiler's `--target arm64` backend —
suggesting a shared front-end/import-resolution root cause with an
arm64-only lowering gap. Suggested owner action: resolve imported const refs
to their values in the arm64 backend (or in shared lowering before backend
split), matching x86-64 behavior.
