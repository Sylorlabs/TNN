# NAMECHECK: Node 1 Efficacy Tester

## Step 0: Toolchain Guard
- Safebin activated: `$HOME/safebin` with allowed tools only.
- `which python3 python` returned nothing. Zero forbidden executables invoked.
- All computation in pure Zag via pinned `znc` (`src/tools/toolchain/znc_linux_x86_64_abed8aa1`).
- Shell used only for: invoking znc, running binaries, git operations, moving/copying files.

## Scope
- **UNFROZEN VARIANT ONLY.** This task tests H3-lite Node 1 on a variant.
- **PILOT ONLY.** This is not the sealed weak K-LT-5 test. Simple bias, unsealed world.
- Frozen TNN-2 source: `docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag`
- Frozen SHA-256: `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`
- H3-lite Node 1 variant: `docs/lab/research-lead/overnight-20260928/h3lite_node1/h3n1_variant.zag`
- Node 1 build commit: `45c55ed83`
- Variant files in `docs/lab/research-lead/overnight-20260928/node1_efficacy/`:
  - `n1e_driver.zag`: pilot driver source
  - `n1e_h3lite.zag`: variant + driver (H3-lite binary source)
  - `n1e_frozen.zag`: base + driver (frozen control binary source)
  - `n1e_h3lite_bin`, `n1e_frozen_bin`: compiled binaries
  - `h3lite_run1/2/3.txt`, `frozen_run1/2/3.txt`: 3/3 byte-identical transcripts

## Input Provenance
- H3-lite Node 1 implementation: commit `45c55ed83` (unfrozen variant, read-only for this task).
- Weak K-LT-5 prereg: `docs/lab/research-lead/overnight-20260928/weak_klt5/WEAK_KLT5_PREREG.md` (FROZEN, design reference only, not the sealed test).
- Consequence re-entry F2: commit `7eab34ff2` (falsifiability condition).

## Constraints Honored
- UNFROZEN VARIANT ONLY. Frozen source, binary, and build untouched.
- PILOT ONLY. Not the sealed weak K-LT-5. Simple unsealed bias.
- Pure Zag. Zero em dashes in deliverables (byte-verified).
- Paper untouched: `docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md` never modified.
- Nothing pushed. No sealed worlds opened.
