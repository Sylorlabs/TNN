# NAMECHECK: Node 2 Reachability Prober

## Step 0: Toolchain Guard
- Safebin activated: `mkdir -p $HOME/safebin`, symlinked 19 allowed tools (git, znc, sh, bash, ls, cp, mv, rm, mkdir, cat, grep, sed, awk, wc, cmp, sha256sum, git-receive-pack, git-upload-pack).
- `export PATH="$HOME/safebin"`
- `which python3 python` returned nothing. Guard check done.
- Zero forbidden executables invoked. All computation in pure Zag via pinned znc.

## Scope
UNFROZEN VARIANT ONLY. Analysis/experiment, not TNN-3.

## Input Provenance
- Frozen H3-lite prereg: commit `9084a7760` (H3LITE-PREREG-FROZEN). Read-only. Node 2 spec from Section 3.
- Frozen TNN-2 source: `tnn2_build/tnn2.zag` at commit `f4de7ff46`. SHA-256 `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`. Verified before copying. Frozen source never modified.
- Success criteria analysis: commit `04af42736` (majority-of-three unreachability claim).

## Variant Declaration
- `tnn2_base.zag`: verbatim copy of frozen source. SHA-256 verified `a29972ca...`.
- `tnn2_node2.zag`: UNFROZEN VARIANT. Implements H3-lite Node 2 ONLY (guide template policy) per frozen prereg Section 3, minimal. Changes:
  1. New `n2_pol_get`: finds/creates policy node (tag 40, subtype 2).
  2. Modified `miss_inquire`: reads action/content from policy node fields 20/24 instead of literals 30/-999. Increments miss count (field 32).
  3. New `resolve_uncertainty`: called from `ev_observe` no-fact branch. Supersedes open uncertainty and its guide, increments resolution count (field 28), records guide's action in 3-slot history (fields 8/12/16), applies majority-of-three rule.
  4. New `main`: probe driver (replaces test battery).
- Cognition (frozen functions) otherwise untouched. Frozen source, binary, build `f4de7ff46` verified unmodified at end.

## Constraints
- UNFROZEN ONLY. Node 2 ONLY. Prereg `9084a7760` frozen, not modified.
- Pure Zag. Zero em dashes in deliverables (byte-verified).
- Paper untouched. Nothing pushed. No sealed worlds.
