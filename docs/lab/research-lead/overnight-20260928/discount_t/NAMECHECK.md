# NAMECHECK: Discount T-Sensitivity Tester (discount_t)

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
executables invoked. Shell used only to invoke znc, run the binaries,
do git operations, and move/copy files.

## Scope declaration

MEASUREMENT ONLY. Threshold-sensitivity test of the discount pilot
(`0daaa2ed4`, D1+D2+W3+R1) at T=1, 2, 3. UNFROZEN VARIANTS ONLY.
Frozen TNN-2 source is never modified.

## Input provenance

- Discount spec: `62fa77192` (`docs/lab/research-lead/overnight-20260928/discount/DISCOUNT.md`)
- Discount pilot: `0daaa2ed4` (`docs/lab/research-lead/overnight-20260928/discount_impl/`)
- Contradiction-break battery: `510b6cb42`
- Frozen base: `di_base.zag` copied to `dt_base.zag`, SHA-256 re-verified
  `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`

## Build method

- `dt_boot_t2.zag` is a verbatim copy of the pilot `di_boot.zag`
  (diff-verified). `dt_boot_t1.zag` / `dt_boot_t3.zag` differ only in
  the R1 threshold literal (`ng(W,n,12)<=1` / `<=3`) and comments.
- Variants assembled exactly as the pilot: full base minus the original
  `fn main` line, `bootstrap_miss` (lines 763-788) replaced.
  `dt_variant_t2.zag` is byte-identical to the pilot `di_variant.zag`
  (`cmp` clean), so T=2 is a true control of the published pilot.
- Driver: `dt_driver_tpl.zag` replicates the pilot driver Phases 1-5
  verbatim (subjects, flags, query counts), adds Phase 6 (second
  contradiction on a fresh subject, 8 queries). Instantiated per T by
  sed on the `@@TH@@` / `@@TAG@@` markers.
- Compiled with the pinned znc; same A0102 lint warnings as the frozen
  base (pre-existing, also present in the pilot build).

## Constraints honored

- MEASUREMENT ONLY. Unfrozen variants. Frozen source untouched
  (hash verified before and after).
- Pure Zag. Zero em dashes (byte-verified).
- Paper untouched. Nothing pushed. No sealed worlds.
- Commit with explicit pathspecs on both `git add` and `git commit`.
