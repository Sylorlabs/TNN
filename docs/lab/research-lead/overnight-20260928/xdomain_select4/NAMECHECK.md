# NAMECHECK: XP-SELECT-4

## Step 0: toolchain guard (recorded before any research computation)

- Safebin created at $HOME/safebin with allowed tools only
  (git, znc, sh, bash, ls, cp, mv, rm, mkdir, cat, grep, sed, awk,
  wc, cmp, sha256sum, git-receive-pack, git-upload-pack).
- `export PATH="$HOME/safebin"` active for all work below.
- `which python3` returns NOTHING (rc=1). `which python` returns
  NOTHING (rc=1). Verified 2026-10-02 at worker startup.
- `which znc` resolves to the pinned compiler
  src/tools/toolchain/znc_linux_x86_64_abed8aa1. All Zag compiled
  with the pinned build only.
- Any forbidden-executable invocation is PROCESS-FAIL. None occurred.

## Reading disclosures (API only; implementation built from PREREG)

- Read in-checkout: xdomain_select3/PREREG.md, xdomain_select3/REPORT.md,
  xdomain_select3/xs3_patch.zag, xdomain_select3/xs3_driver.zag
  (API surface, selector architecture, driver assertion patterns).
- Read in-checkout: xdomain_grammar_construct/PREREG.md,
  xdomain_grammar_construct/REPORT.md (grammar to construction L1
  pair design, the exact-reuse baseline this probe adds mismatch to).
- Read in-checkout (frozen, verbatim use):
  composition_C/cc_base.zag, composition_unified/un_patch.zag.
- The XS4 selector, driver, and battery below are designed from the
  frozen PREREG.md in this lane, not copied from any prior
  implementation. Function names use the xs4_ prefix; trace tags use
  XS4-.

## Environment note

- Pre-freeze well-formedness prototype ran in ~/workspace/_scratch_xs4
  (outside the repo, never committed, deleted after the run). It used
  only the frozen shared machinery (cc_base.zag + un_patch.zag, plain
  ev_query): no selector code was prototyped. Disclosed in REPORT.md.

## Steps

- [x] Step 0: toolchain guard (above).
- [ ] Step 1: PREREG.md frozen, committed ALONE (commit-order self-check).
- [ ] Step 2: implementation (xs4_patch.zag, drivers, binaries).
- [ ] Step 3: 3/3 runs, REPORT.md.
- [ ] Scratch ~/workspace/_scratch_xs4 deleted after the run.
