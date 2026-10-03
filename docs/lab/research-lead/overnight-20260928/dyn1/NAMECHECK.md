# DYN-1 Measurer: NAMECHECK

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

UNFROZEN VARIANT ONLY. This is a measurement experiment, not TNN-3.
The frozen TNN-2 source (`tnn2_build/tnn2.zag`, SHA-256
`a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`)
is copied verbatim as `dyn1_base.zag` (hash re-verified) and is never modified.
The variant `dyn1_full.zag` is the verbatim copy with the original test `main`
removed and a measurement driver appended. Cognition code is byte-identical
to frozen; only the driver (harness-side, not cognition) differs.

## Task

Measure DYN-1: per-experience state deltas (nodes and edges added per teach,
per query hit, per miss, per observe) across a 250-event lifetime-like
sequence. Test whether per-event cost is constant ("write-mostly, not living"
signature) and count duplicate structures from repeated identical misses.

## Constraints honored

- UNFROZEN variant only. Frozen source read-only, never modified.
- Pure Zag. No Python, no other interpreters.
- Zero em dashes in all deliverables.
- Paper untouched (`TNN_RESEARCH_PAPER_20260929.md` never opened for edit).
- Nothing pushed. Local commits only.
- No sealed worlds opened or inspected.
- Explicit pathspecs on both `git add` and `git commit`.

## Verdict target

DYN1-COMPLETE with the measured DYN-1 profile.
