# Characterization — candidate (b): compound-bool→i32 cast

**Status:** NOT REPRODUCED on lab toolchain. Raw evidence: RAW_B_bool_cast.txt.
**Verdict:** NOT-REPRODUCED (honest negative).

## What was tried
Two minimal pure-Zag reproducers, no arrays, no allocations, no syscalls, no
imports (single file), compiled with znc_linux_x86_64_abed8aa1 (SHA-256
498abcb5…e58ef) for x86-64 and `--target arm64` (run under qemu-aarch64-static).

Shapes covered (all preregistered expected-vs-actual, 24 case-lines total):
1. `return (v>=2001 && v<=2008) as i32;` — the exact reported shape (also the
   `cl_is_status` shape in shipped common.zag).
2. Single-comparison control: `return (v==5) as i32;`.
3. `||` compound: `return (a<0 || b<0) as i32;`.
4. Negated compound: `return !(v>=2001 && v<=2008) as i32;`.
5. Let-bound variant: `let ok:i32=(v>=2001 && v<=2008) as i32; return ok;`.
6. "Range branches": nested `if(v>=2001){ if(v<=2008){ return (...) as i32; } }`.
7. Triple-AND, i32 operands, mixed `&&`/`||` precedence.

Inputs covered below-range, both edges, inside, above-range, negatives.

## Result
Every line matched its preregistered expected value on both backends; all
exits 0; all run-pairs byte-identical (deterministic). The reported failure
("did not produce the required 1 for valid scalars") did not occur in any
of the 4 binaries × 2 runs.

## Why it may not reproduce here (hypotheses, not claims)
- The doc-sweep source (V92 V4_PATCH_NOTES) says "the local Zag compiler used
  by this lane" — the R27 continuity lane likely used the pinned macOS ARM64
  compiler `znc_macos_arm64_7cacbfc0`, which is not available in this lab.
- The defect may have been fixed between that lane's compiler and abed8aa1.
- The trigger may need a shape not tried (e.g. specific register pressure in
  a larger function, or a comparison form not covered).
- Independent corroboration of health: the shipped R34 v3 harness uses the
  exact `(v>=2001 && v<=2008) as i32` shape and passes 24/24 checks on this
  toolchain (ZAG_PLAYBOOK §6).

## Reconciliation note
Nothing reproduced, so there is no manifestation to attribute to a known bug.
Had it reproduced with no arrays in the repro, ZNC-2026-09-19-001 (array-store
miscompile) would have been structurally inapplicable — recorded here so a
future reproducer can reuse the disambiguation.

## Suggested follow-up (not a filing)
Keep the V4 patch-notes report as unreplicated historical evidence. If the
macOS ARM64 pinned compiler becomes available, re-run repro/kbool_main.zag
and repro/kbool_main2.zag against it before writing a bug ID. No ZNC ID
assigned — a NOT-REPRODUCED candidate must not consume a bug number.
