# Decline Gate Builder: NAMECHECK

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

UNFROZEN VARIANT ONLY. This is a pilot mechanism test, not TNN-3.
The frozen TNN-2 source (`dyn1_base.zag`, SHA-256
`a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`)
is copied verbatim as `dg_base.zag` (hash re-verified) and is never modified.
The variant `dg_full.zag` replaces only `ev_query` (base lines 813-835) with
the gated version, adds three helper functions, removes the test `main`
(base line 1357), and appends the measurement driver. Diff-verified: the only
cognition changes are the gate helpers and the gate check.

## Task

Implement a minimal decline gate and test whether DYN-1 bends: after N=3
consecutive failed pursuits of the same (s,r), further queries return
WITHHOLD (-3) instead of re-attempting trial/bootstrap and reifying another
UNCERTAINTY node + guide. Run the 250-event DYN-1 battery, 3/3 byte-identical.

## Constraints honored

- UNFROZEN variant only. Frozen source read-only, never modified.
- Pure Zag. No Python, no other interpreters.
- Zero em dashes in all deliverables (byte-verified).
- Paper untouched (`TNN_RESEARCH_PAPER_20260929.md` never opened for edit).
- Nothing pushed. Local commits only.
- No sealed worlds opened or inspected.
- Explicit pathspecs on both `git add` and `git commit`.

## Verdict target

DECLINE-GATE-COMPLETE with verdict BENDS or FLAT.
