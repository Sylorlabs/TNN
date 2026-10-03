# SPEC-EPOCHTAG: NAMECHECK

**Lane:** docs/lab/research-lead/overnight-20260928/spec_epochtag/
**Date:** 2026-10-03

## Step 0: Toolchain guard (mandatory)

- Worker activated safebin: `export PATH="$HOME/safebin"` before any build.
- `which python3` returns nothing; `which python` returns nothing.
- Pinned compiler: `$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1`
  (same pinned znc as the disagreement_attribution and spec_relationblind lanes).
- All research logic in pure Zag. No Python, C, JS, or Rust in verifiers,
  scorers, harnesses, or analysis. Output analysis via grep/awk/cmp only.
- znc defect workarounds observed: no `as *i32` slice construction; dynamic
  output via single-buffer `o_app`/`o_i64` + one `_zag_raw_syscall` (never
  `_zag_print`); `if` nesting kept at 3 or fewer with hoisted flags; no
  `!(A && B)` in while conditions.
- Memory-layout verification (source inspection, 2026-10-03): world arena
  A[772] is free (facts occupy 4..772; arena is 4096 bytes); L tag slots at
  13300/13364/13428 (+bi*4, 16 slots each) are free (highest L offset used by
  da_learn.zag is 13296, telemetry cells).

## Steps 1..n: reserved for build/run verification records
