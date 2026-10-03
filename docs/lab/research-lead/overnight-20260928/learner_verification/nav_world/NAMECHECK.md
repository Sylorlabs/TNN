# NAMECHECK.md - Learner-Owned Verification Worker (H-LVNAV-1)

## Step 0: Toolchain Guard

**Date:** 2026-10-02
**Worker:** Learner-Owned Verification Worker, H-LVNAV-1 (composition via
world execution)

### Safebin setup (executed)
```bash
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

**Result:** `guard-check-done` printed with NO python3/python path before it.
`which python3 python` returns nothing under the safebin PATH. Safebin holds
49 links; none match python, python3, or node (verified by grep).
**PATH:** `$HOME/safebin` only for all worker shell work.

### Verification
- `which python3` returns nothing: CONFIRMED
- `which python` returns nothing: CONFIRMED
- Pinned znc resolves via safebin (`znc 2026.07.0-dev`): CONFIRMED
- Pure Zag for all computation; shell used only for: invoking znc, running
  binaries, git ops, file moves, text audit greps: CONFIRMED
- Zag toolchain lessons from AGENTS.md applied: u8-backed cells with
  little-endian pack/unpack helpers (no `as *i32` slice construction);
  single preallocated output buffer with cursor-returning emit helpers and
  one `_zag_raw_syscall` write (no `_zag_print` for dynamic content).

**No forbidden executable invoked. Step 0 PASS.**

## Provenance
- Design: H-LVNAV-1 PREREG.md (commit 514e4ef6a, frozen before implementation).
- Lane: docs/lab/research-lead/overnight-20260928/learner_verification/nav_world/
  (subdirectory; the parent learner_verification/ lane holds C181, COMPLETE,
  and is left untouched).
- Base: standalone pure-Zag mechanism (composition_verify precedent: minimal
  white-box implementation keeps the learner/world information boundary
  structurally auditable). No TNN substrate code reused or modified.
- This work: new files only. No frozen source touched.

## Constraints
- Prereg frozen before implementation: YES (PREREG.md committed alone as
  514e4ef6a before any .zag file existed)
- Pure Zag: YES
- Zero em/en dashes in docs: YES (byte-verified before commit)
- Paper untouched: YES
- Nothing pushed: YES (local commits only)
- 0 modes/bridges/handlers: YES
- Explicit pathspecs on git add/commit: YES
