# NAMECHECK: Cross-Domain Transfer Experiment

## Step 0: Toolchain guard (mandatory)

- Safebin activated: `mkdir -p $HOME/safebin`, symlinked 16 allowed tools
  (git, znc, sh, bash, ls, cp, mv, rm, mkdir, cat, grep, sed, awk, wc,
  cmp, sha256sum, git-receive-pack, git-upload-pack).
- `export PATH="$HOME/safebin"` set before all work.
- `which python3 python` returned NOTHING. Zero forbidden executables
  invoked during this task.
- All computation in Zag (pinned `znc_linux_x86_64_abed8aa1`).
- Shell used only for: invoking znc, running binaries, git operations,
  moving/copying files.

## UNFROZEN VARIANT DECLARATION

This experiment uses an **UNFROZEN VARIANT** of TNN-2.

- Frozen source: `docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag`
  (SHA-256 `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`)
- Variant: `tnn2_xfer_variant.zag` (copy verified SHA-256 identical BEFORE
  modification).
- Frozen `tnn2.zag`, `tnn2_bin`, build `f4de7ff46`: NOT modified (verified
  by diff after variant creation).
- Per Micah 2026-10-01: "try stuff unfrozen as you go on as thats what i
  imagine TNN being in production" and "TNN should stay a white box
  architecture if you need to find something use the white box".

## Variant changes (2, same as reuse experiment plus counter fix)

1. **Shadow teach deleted** in `promote_graph`: the MAP node is the
   promoted artifact; no exact-match fact shadows it.
2. **MAP-first lookup** in `ev_query`: scan live tag-20 MAPs for exact
   (s,r); most-recent wins; execute via `t2_exec`; fall through on
   -999999. White-box counter at `hg(W,52)` (field 52 verified unused by
   frozen TNN-2; avoids the ctx ring buffer at 32/36/40/44 that the reuse
   experiment's field-32 counter collided with).
3. `hs(W,52,0)` initialized in `tnn2_init`.

Zero new modes, bridges, handlers, semantic cases, opcodes, node types.
No cross-domain mappings hardcoded (task constraint).

## Scope

- Cross-domain transfer test ONLY.
- This is an experiment, NOT TNN-3 implementation.
- Honest reporting: transfer failure is a result, not a bug to patch.

## Input provenance

- Frozen `tnn2.zag` read from `tnn2_build/` (read-only).
- Reuse experiment (`ea8fc0ac1`) consulted for probe patterns and API
  surface; its variant NOT copied (fresh copy from frozen source).
- Trial-loop analysis done by reading frozen source directly (white box).

## Constraints honored

- UNFROZEN VARIANT ONLY. Frozen TNN-2 untouched.
- No hardcoded cross-domain mappings.
- Zero em dashes in deliverables (byte-verified before commit).
- Paper untouched. Nothing pushed. Local commits only.
