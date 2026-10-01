# NAMECHECK.md - L2L2 Repair Worker

## Step 0: Toolchain Guard

- Safebin activated: `mkdir -p $HOME/safebin`, symlinked 36 allowed tools, `export PATH="$HOME/safebin"`.
- `which python3 python` returns nothing. Zero forbidden executables invoked.
- All computation in pure Zag via pinned `znc_linux_x86_64_abed8aa1`.
- Shell used only for: invoking znc, running binaries, git operations, moving/copying files.
- Guard check recorded: 2026-10-01.

## Scope

- Repair worker for L2L2 causal ablation (P3) per audit `af9a9765a`.
- Prereg amendment committed BEFORE implementation (Micah's prereg commit-order rule).
- UNFROZEN VARIANT: `l2l2.zag` copied to this directory as `l2l2_repair.zag`; mode 2 added.
  Original `learntolearn2/l2l2.zag` (commit `b7047b6e6`) untouched.
- Lineage: copy of `b7047b6e6:l2l2.zag`, SHA-256 verified before modification.

## Input provenance

- Audit: `af9a9765a` (L2L2_AUDIT.md)
- Original prereg: `4b4c8c345` (PREREG_L2L2.md)
- Original implementation: `b7047b6e6` (l2l2.zag)
- This amendment does not modify the original prereg; it extends it.

## Constraints

- Prereg amendment commit strictly precedes implementation commit.
- Pure Zag. Zero em dashes. Paper untouched. Nothing pushed.
