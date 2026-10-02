# NAMECHECK: H3-lite Node 1 Builder

## Step 0: Toolchain Guard
- Safebin activated: `$HOME/safebin` with 36 allowed tools.
- `which python3 python` returned nothing. Zero forbidden executables invoked.
- All computation in pure Zag via pinned `znc` (`src/tools/toolchain/znc_linux_x86_64_abed8aa1`).
- Shell used only for: invoking znc, running binaries, git operations, moving/copying files.

## Scope
- **UNFROZEN VARIANT ONLY.** This task implements H3-lite Node 1 on a variant.
- Frozen TNN-2 source: `docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag`
- Frozen SHA-256: `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`
- Verified identical before and after variant creation. Frozen never modified.
- Variant files in `docs/lab/research-lead/overnight-20260928/h3lite_node1/`:
  - `h3n1_base.zag`: verbatim frozen copy (SHA-256 verified)
  - `h3n1_funcs.zag`: H3-lite Node 1 functions (new code)
  - `h3n1_variant.zag`: base + funcs (t2_trial replaced)
  - `h3n1_build.zag`: variant + test driver
  - `h3n1_driver.zag`: test driver source
  - `h3n1_bin`: compiled binary
  - `run1.txt`, `run2.txt`, `run3.txt`: 3/3 byte-identical transcripts

## Input Provenance
- H3-lite prereg: commit `9084a7760` (FROZEN, read-only, never modified).
- Prereg path: `docs/lab/research-lead/overnight-20260928/h3lite_prereg/H3LITE_PREREG_FROZEN.md`
- Weak K-LT-5 design: `docs/lab/research-lead/overnight-20260928/weak_klt5/` (test design, not yet run).

## Constraints Honored
- UNFROZEN VARIANT ONLY. Frozen source, binary, and build untouched.
- Node 1 ONLY. Nodes 2 and 3 NOT implemented.
- Prereg `9084a7760` is frozen; not modified.
- Pure Zag. Zero em dashes in deliverables (byte-verified).
- Paper untouched: `docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md` never modified.
- Nothing pushed. No sealed worlds opened.
- Alternative C boundary: no new opcodes, modes, bridges, or handlers. All policy writes use existing `ns` field writes. Verified by architecture accounting in H3LITE_NODE1.md.
