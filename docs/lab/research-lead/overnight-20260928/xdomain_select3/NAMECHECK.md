# NAMECHECK: XP-SELECT-3

## Step 0: toolchain guard (recorded before any research computation)

- Safebin created at $HOME/safebin with allowed tools only
  (git, znc, sh, bash, ls, cp, mv, rm, mkdir, cat, grep, sed, awk,
  wc, cmp, sha256sum, git-receive-pack, git-upload-pack).
- `export PATH="$HOME/safebin"` active for all work below.
- `which python3` returns NOTHING (rc=1). `which python` returns
  NOTHING (rc=1). Verified 2026-10-02.
- `which znc` resolves to the pinned compiler
  src/tools/toolchain/znc_linux_x86_64_abed8aa1. All Zag compiled
  with the pinned build only.
- Any forbidden-executable invocation is PROCESS-FAIL. None occurred.

## Reading disclosures (API only; implementation built from PREREG)

- Read via git show (other branch, not copied):
  xdomain_select2/PREREG.md (7d2239f50), xs2_patch.zag and
  xs2_driver.zag (33fa210dd), for API surface and driver assertion
  patterns.
- Read in-checkout: composition_C/cc_base.zag,
  composition_unified/un_patch.zag, xdomain_l2_adapt/trunc_patch.zag,
  xdomain_l2_adapt/PREREG_AMENDMENT1.md, xdomain_causal_interv/PREREG.md.
- The XS3 selector, driver, and battery below are designed from this
  prereg, not copied from any prior implementation.

## Environment note

- /tmp is a 512M tmpfs at 100% (dominated by another worker's
  /tmp/arena-c8-wt, untouched). The pre-freeze well-formedness
  prototype therefore ran in ~/workspace/_scratch_xs3 (outside the
  repo, never committed, deleted after the run). No other worker
  files touched.

## Steps

- [x] Step 0: toolchain guard (above).
- [x] Step 1: PREREG.md frozen, committed ALONE (commit ea6f894df).
- [x] Step 2: implementation (xs3_patch.zag, drivers, binaries).
  One pre-report fix: A8 driver query corrected 106 -> 107 to match
  the frozen battery; rebuilt and re-ran 3/3 (disclosed in
  REPORT.md). No frozen bar changed.
- [x] Step 3: 3/3 runs, REPORT.md. Verdict XP-SELECT-3-PASS
  (K1-K13). Run shas: main
  52a63054a86eaf9ce571a6d51d3f2dce0a7d7a924280a68eef05d45bbdc6ef11,
  noadapt
  08d7a7a7caf184422e53ae9859a289c6f667e0eae000a089ea7413f4f9b8c896.
- [x] Scratch ~/workspace/_scratch_xs3 deleted after the run.
