# NAMECHECK: GEN-GENERALITY

## Step 0 -- Toolchain guard (worker instruction-level attestation)

- Date: 2026-10-03. Worker: gen-generality.
- `export PATH="$HOME/safebin"` active for all work in this lane.
- `which python3` -> NOTHING (exit 1). `which python` -> NOTHING (exit 1).
  Verified after PATH export, before any implementation.
- Safebin contents: 36 allowed tools (coreutils, git, pinned znc); no
  python3/python/perl/ruby/node.
- Pinned znc: ~/safebin/znc -> 
  /home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1
  sha256 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
  (matches the C380-frozen pinned hash).
- Git operations use /usr/bin/git directly (the safebin git symlink has the
  known EPERM defect on this host per AGENTS.md 2026-10-03; the resolved
  binary path works).
- Pure Zag for all scientific computation in this lane. Zero invocations of
  python3, python, or any other forbidden executable. If any occurs, this
  wave is automatically PROCESS-FAIL per the worker toolchain guard.

## Step 1 -- Frozen reference digests (mechanism under test, unmodified)

GEN and base are taken byte-identical from the C380 implementation commit
82732a9e8 (docs/lab/research-lead/overnight-20260928/compose_pair6_adv/):

- d6_base.zag @ 82732a9e8:
  sha256 a53cdf0126ab1501fb70d9b14c2f745e0ef1838209753df8a0c6d0daf484bbcb
- d6_gen.zag @ 82732a9e8:
  sha256 d6f1f9d8f4747293bb7a8e99474660347dc24693f62f3d25caaf1d83c19c9d9a

K1 requires ref_gg_base.zag / ref_gg_gen.zag in this lane to match these
digests exactly, and the assembled gg_full.zag regions to diff EMPTY
against them.

## Step 2 -- Commit order (prereg freeze)

- PREREG.md + this NAMECHECK.md (Steps 0-1) committed ALONE, strictly
  before any implementation file (gg_new.zag, gg_full.zag, binaries,
  run logs, REPORT.md).
- Prereg commit: 484fe6aad (2026-10-03).
- PREREG_AMEND1.md (transparent Q4a/Q4b derivation correction; no
  implementation change): committed 4e57ab950, BEFORE the official runs
  it governs. The 3 pre-amendment runs are retained as gg_expl1/2/3.txt
  (exploratory, reported).
- Implementation: gg_new.zag (setups + driver only); gg_full.zag =
  ref_gg_base.zag + (ref_gg_gen.zag minus main, stripped via
  sed '/^fn main()i32 {/,$d') + gg_new.zag; region diffs EMPTY (verified).
- Binary gg_bin sha256:
  5e48732a94ddd4a55e6bbc91c91a393f71c80bdbd34e45421ae5010c2d75350a
- Official runs gg_run1/2/3.txt: 3/3 byte-identical, sha256
  4b81226d665735820fec1ec4c0dc3e0447b9947b8069f8618b8ad59e87740752
  (identical to the exploratory bytes: the amendment changed only
  prediction text, not the implementation; determinism holds).
- stderr empty on all runs.
