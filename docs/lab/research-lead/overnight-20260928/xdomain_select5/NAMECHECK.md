# NAMECHECK: XP-SELECT-5

## Step 0: toolchain guard (recorded before any research computation)

- Safebin created at $HOME/safebin with allowed tools only
  (git, znc, sh, bash, ls, cp, mv, rm, mkdir, cat, grep, sed, awk,
  wc, cmp, sha256sum, git-receive-pack, git-upload-pack, plus
  standard coreutils symlinks).
- `export PATH="$HOME/safebin"` active for all work below.
- `which python3` returns NOTHING (rc=1). `which python` returns
  NOTHING (rc=1). Verified 2026-10-02 at worker startup.
- `which znc` resolves via safebin symlink to the pinned compiler
  src/tools/toolchain/znc_linux_x86_64_abed8aa1. All Zag compiled
  with the pinned build only.
- Any forbidden-executable invocation is PROCESS-FAIL. None occurred.

## Reading disclosures (API only; implementation built from PREREG)

- Read in-checkout: xdomain_select4/PREREG.md, xdomain_select4/REPORT.md,
  xdomain_select4/NAMECHECK.md (XP-SELECT line methodology, kill-bar
  structure K1-K13, battery well-formedness precedent, assertion patterns).
- Read in-checkout: composition_xdomain/REPORT.md (navigation x aggregation
  L1 pair design: chain X with r81/r91, count Y with r82/r92, INC-cell
  count graphs, Z query (s,93)->count).
- Read in-checkout: xdomain_value/REPORT.md, xdomain_value/vc_patch.zag
  (H2 value-level function composition: (CHAIN,COUNT) ordered pairs,
  vc_has_count_map INC scan, count template execution; modes are
  researcher-defined there, this worker derives function types from
  learner state instead).
- Read in-checkout (frozen, verbatim use):
  composition_C/cc_base.zag, composition_unified/un_patch.zag.
- The XS5 selector, exact value-level composition, driver, and battery
  below are designed from the frozen PREREG.md in this lane, not copied
  from any prior implementation. Function names use the xs5_ prefix;
  trace tags use XS5-.

## Environment note

- Pre-freeze well-formedness prototype ran in ~/workspace/_scratch_xs5
  (outside the repo, never committed, deleted after the run). It used
  only the frozen shared machinery (cc_base.zag + un_patch.zag) plus a
  minimal exact value-level composition (nav via cc_satisfy, agg via
  count template, NO selector code): confirmed TRAIN-X/TRAIN-Y MAPs,
  P-AGGREL=82 from Y provenance, A4 shape ans=2, A1/A2/A3 shapes ans=-2
  across rebind/compose/trial/bootstrap. The prototype also caught two
  design bugs pre-freeze: Y must be taught as an 82-CHAIN (t2_chain
  follows one chain per relation; a star teaches only 1 link) and A2's
  expected must avoid coinciding with the trial's route-link count.
  No selector/orchestration code was prototyped. Disclosed in REPORT.md.

## Steps

- [x] Step 0: toolchain guard (above).
- [ ] Step 1: PREREG.md frozen, committed ALONE (this file + PREREG.md).
- [ ] Step 2: implementation (xs5_patch.zag, xs5_patch_noadapt.zag,
  xs5_driver.zag, xs5_driver_noadapt.zag, binaries).
- [ ] Step 3: 3/3 runs, REPORT.md. Verdict TBD.
- [ ] Scratch ~/workspace/_scratch_xs5 deleted after the run.
