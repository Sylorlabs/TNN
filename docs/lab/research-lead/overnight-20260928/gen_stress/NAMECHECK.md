# NAMECHECK: GEN-STRESS

## Step 0 -- Toolchain guard (worker instruction-level attestation)

- Date: 2026-10-03. Worker: gen-stress.
- `export PATH="$HOME/safebin"` active for all work in this lane.
- `which python3` -> NOTHING (exit 1). `which python` -> NOTHING (exit 1).
  Verified after PATH export, before any implementation.
- Safebin contents: 36 allowed tools (coreutils, git, pinned znc); no
  python3/python/perl/ruby/node.
- Pinned znc: ~/safebin/znc
  sha256 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
  (matches the C380-frozen pinned hash; verified by direct sha256sum in
  this lane).
- Git operations use /usr/bin/git directly (the safebin git symlink has the
  known EPERM defect on this host per AGENTS.md 2026-10-03; the resolved
  binary path works).
- Pure Zag for all scientific computation in this lane. Zero invocations of
  python3, python, or any other forbidden executable. If any occurs, this
  wave is automatically PROCESS-FAIL per the worker toolchain guard.

## Step 1 -- Frozen reference digests (mechanism under test, unmodified)

GEN and base are taken byte-identical from the C380 implementation commit
82732a9e8 (docs/lab/research-lead/overnight-20260928/compose_pair6_adv/),
via the C402-verified copies in
docs/lab/research-lead/overnight-20260928/gen_generality/
(ref_gg_base.zag, ref_gg_gen.zag):

- d6_base.zag @ 82732a9e8:
  sha256 a53cdf0126ab1501fb70d9b14c2f745e0ef1838209753df8a0c6d0daf484bbcb
- d6_gen.zag @ 82732a9e8:
  sha256 d6f1f9d8f4747293bb7a8e99474660347dc24693f62f3d25caaf1d83c19c9d9a

K1 requires ref_gs_base.zag / ref_gs_gen.zag in this lane to match these
digests exactly, and the assembled gs_full.zag regions to diff EMPTY
against them.

## Step 2 -- Commit order (prereg freeze)

- PREREG.md + this NAMECHECK.md (Steps 0-1) committed ALONE, strictly
  before any implementation file (gs_new.zag, gs_full.zag, binaries,
  run logs, REPORT.md).
- Lane branch: lane-genstress-20261003 (dedicated; explicit-pathspec
  commits only; local only, never pushed).
