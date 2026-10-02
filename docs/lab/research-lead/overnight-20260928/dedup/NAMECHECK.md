# Deduplication Investigator: NAMECHECK

## Step 0: Toolchain Guard (mandatory, recorded)

Activation performed 2026-10-01:
```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```
Result: `which python3 python` returned nothing. Guard check done.
Zero forbidden executables invoked. All computation in pure Zag via the pinned
compiler `src/tools/toolchain/znc_linux_x86_64_abed8aa1`.

## Scope

UNFROZEN VARIANT ONLY. This is a DYN-1 bending experiment, not TNN-3.
The frozen TNN-2 source (`tnn2_build/tnn2.zag`, SHA-256
`a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`)
is never modified. The starting point is `dyn1_full.zag` (the verbatim DYN-1
measurement variant from `003767553`: frozen cognition, base test main
removed, DYN-1 driver appended). The only cognition change in this wave is
the dedup pre-scan inside `miss_inquire`, documented in DEDUP.md. The driver
is harness-side and verbatim.

## Task

Investigate deduplication as a DYN-1 bending mechanism: analyze why 70
duplicate UNCERTAINTY nodes are created, design a content-addressed reuse
mechanism at the allocation site, implement on the unfrozen variant, and
measure whether the DYN-1 curve bends.

## Constraints honored

- UNFROZEN variant only. Frozen source read-only, never modified.
- Pure Zag. No Python, no other interpreters.
- Zero em dashes in all deliverables (byte-verified before commit).
- Paper untouched (`TNN_RESEARCH_PAPER_20260929.md` never opened for edit).
- Nothing pushed. Local commits only.
- No sealed worlds opened or inspected.
- Explicit pathspecs on both `git add` and `git commit`.
- No `as *i32` plus slice construction in Zag; u8-backed cells with
  little-endian helpers only (compiler workaround, AGENTS.md).

## Verdict target

DEDUP-COMPLETE with BENT or FLAT.
