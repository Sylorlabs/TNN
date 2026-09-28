# B.6 FORCE-PIN LIVE WIRING REPORT

**Date:** 2026-09-21 | **Crew:** force-pin wiring | **Decision:** Micah — WIRE IT LIVE

## What was done

Applied `forcepin/patch/delib_forcepin.patch` to the live
`units/teachers/learner/delib.zag`, with one path correction:
`@import("forcepin.zag")` → `@import("forcepin/forcepin.zag")`
(the module stays in its `forcepin/` subdirectory; no duplicate copy).

The patch is strictly additive:
- `DLB.fpins: *FPStore` field + `fp_init` in the constructor
- Force-pin state folded into `dlb_digest` (state commitment)
- ELIMINATE consults `fp_check` → §L R2 (CONFLICTS_PINNED) with audited refusal
- `dlb_retract` refuses to kill a force-pinned unit (V_REJECT / R2)
- Scratch arena 16384 → 24576 (force-pin tables)

The old learner-side `Pins` is untouched (parked item 1 from the verdict —
whether to deprecate/route it is still Micah's call).

## Test results (all against the LIVE wired delib.zag, not scratch)

| Suite | Result |
|---|---|
| Module contract (test_forcepin.zag) | **34/34 PASS** |
| Live wired end-to-end (17 checks) | **17/17 PASS** |
| Determinism N=5 | byte-identical both binaries |
| MALLOC_PERTURB_ {0,165,17} | byte-identical all |
| Static path audit (updated for post-wiring) | **PASS** |
| Existing learner tests (driver, determinism, pins, retract, tripwire) | all PASS — **no regressions** |

Determinism SHAs match the pre-wiring validation exactly:
- wired: `b5551d6884e2d64e6b42921867667035bd48466b4d0b3e5d29b62a0a02cda35a`
- module: `754f10db3b8d34598c8e9b9d448d47cbbb5c88ab6631fe89d5ce06a304c7deac`

## Static audit update

`static_audit.sh` claim B was written for the pre-wiring state ("zero fp_
symbols in the live tree"). Updated to the post-wiring invariant that
matters: **zero calls to the fp_pin/fp_unpin mutators** in the live tree.
The wiring calls only read-side symbols (fp_init ×1, fp_check ×1,
fp_gate ×1, fp_gate_kill ×1). Claim C now checks the live delib.zag.

## ZNC-007 check

The patch contains no `as []i32`/`as []u32`/`as []u16` consecutive-cast
patterns. The force-pin tables are `[]i64` (ZNC-007-clean). No conversion
needed.

## Files changed

- `units/teachers/learner/delib.zag` — wiring patch applied (live)
- `units/teachers/learner/forcepin/static_audit.sh` — claims B/C updated
  for post-wiring state
- `units/teachers/learner/forcepin/WIRING_REPORT.md` — this file
