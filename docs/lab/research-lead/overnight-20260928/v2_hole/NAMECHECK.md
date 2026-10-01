# NAMECHECK.md - V2 Hole Prober

## Step 0: Toolchain Guard
- Date: 2026-10-01
- Safebin activated: `export PATH="$HOME/safebin"`
- `which python3 python` returns nothing (verified empty).
- Zero forbidden executables invoked.
- All computation in pure Zag via pinned `znc` (`src/tools/toolchain/znc_linux_x86_64_abed8aa1`).
- Shell used only for: invoking znc, running binaries, git operations, moving/copying files.

## Scope
- EXPERIMENTAL. Unfrozen variant only.
- Mission: empirically test whether `t2_revise_graph` accepts a repair that runs but computes something unrelated to the observation (new_o).

## Input Provenance
- Verification criterion analysis `c2a48bee6` (V2 finding): acceptance is `out != -999999`, never checks `out == new_o`.
- Frozen source: `docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag`
  - SHA-256 before copy: `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`
  - SHA-256 after copy (variant): identical (verified).
  - Frozen source, binary, and build `f4de7ff46` untouched (verified via git status).

## Variant Declaration
- UNFROZEN VARIANT: `tnn2_v2hole_variant.zag` (verbatim copy of frozen).
- Build file: `tnn2_v2hole_build.zag` (variant + driver appended, original main removed).
- Driver: `v2_driver.zag` (probe functions, no cognition changes).
- Binary: `tnn2_v2hole_bin`.
- No cognition code modified. Only the main function replaced with probe driver.

## Constraints
- UNFROZEN ONLY. Frozen TNN-2 untouched.
- Pure Zag. Zero em dashes (byte-verified).
- Paper untouched. Nothing pushed.
- Experiment, not TNN-3.
