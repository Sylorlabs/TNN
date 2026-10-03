# NAMECHECK: Discount Builder (discount_impl)

## Step 0: Toolchain guard

Executed at startup (2026-10-01):

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `guard-check-done` with no python3/python paths printed.
Safebin active for all subsequent commands. Pure Zag via the pinned
znc (`src/tools/toolchain/znc_linux_x86_64_abed8aa1`). Zero forbidden
executables invoked. Shell used only to invoke znc, run the binary,
do git operations, and move/copy files.

## Scope declaration

UNFROZEN VARIANT ONLY. Pilot implementation of the minimal discount
subset (D1+D2+W3+R1) per specification `62fa77192` (DISCOUNT.md).
Frozen TNN-2 source is never modified; the variant is built from a
verbatim frozen copy with `bootstrap_miss` replaced.

## Input provenance

- Discount spec: `62fa77192` (`docs/lab/research-lead/overnight-20260928/discount/DISCOUNT.md`)
- Contradiction-break battery: `510b6cb42` (driver replicated)
- Frozen base: `cb_base.zag` (SHA-256 `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`), copied to `di_base.zag`, hash re-verified
- Genuine-state field census: field 12 free on tag-1 FACT nodes (verified by grep; all other field-12 uses are graph cells tag 101/102, MAP tag 20, allocator zeroing)

## Build note

First splice attempt cut the base at line 1356 (before the test
helpers), which broke compilation (`run_all` references `t_r_pact*`
defined later). Fixed by keeping the full base minus only the
original `fn main` line, with `bootstrap_miss` (lines 763-788)
replaced by the pilot version. The dead test code compiles but is
unreachable (`main` calls `di_main`).

## Constraints honored

- UNFROZEN ONLY. Frozen source untouched (hash verified before and after).
- Minimal subset ONLY: D1 (field 12, allocator-zeroed, no init change),
  D2 (T=2 hardcoded), W3 (minority discount on strict-majority
  non-unanimity), R1 (skip discount > 2). No W1/W2, no R2/R3, no floor D3.
- Pure Zag. Zero em dashes (byte-verified).
- Paper untouched. Nothing pushed. No sealed worlds.
- Commit with explicit pathspecs on both `git add` and `git commit`.
