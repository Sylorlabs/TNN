# NAMECHECK.md -- Clean Scaling Rerun Worker

## Step 0: Toolchain guard
- Date: 2026-10-01. Ran safebin setup: linked git, znc, sh, bash, ls, cp,
  mv, rm, mkdir, cat, grep, sed, awk, wc, cmp, sha256sum into
  $HOME/safebin.
- `export PATH="$HOME/safebin"` active for all work below.
- `which python3 python` returns nothing (verified: empty output before
  guard-check-done).
- Pinned compiler: src/tools/toolchain/znc_linux_x86_64_abed8aa1
  (via `znc` symlink in safebin).
- All research computation in pure Zag. Shell used only to invoke znc,
  run binaries, git operations, and move/copy files.
- Zero Python invocations this entire wave. Not one `python3`, not one
  `python`, not one accidental invocation. Every computation went
  through the pinned znc compiler or the compiled Zag binary itself.
  Any file assembly was done with sed/cat. This is a clean reproduction
  of commit 11adcb0ea, which carried a single accidental
  `python3 -c "print('skip')"` (output to /dev/null, computed nothing);
  that wave is PROCESS-FAIL for canonical promotion per the standing
  rule. This wave is PROCESS-PASS.

## Reproduction record
- Regenerated sc_base_expanded.zag from
  rebinding_hardening/hard_base.zag using the same sed expansion
  (1024->8192 nodes, 4096->16384 edges). Verified byte-identical to the
  prior wave's pre-fix backup (sc_base_expanded.zag.bak1000) via cmp.
- Applied the pre-existing 1000-threshold fix (11 line substitutions,
  1000->10000 in frame-slot encoding sites) via sed. Verified
  byte-identical to the prior wave's fixed sc_base_expanded.zag via cmp.
- Copied sc_patch.zag and sc_driver.zag from scaling_cont; verified
  byte-identical via sha256sum.
- Assembled sc_full.zag with the same sed/cat build steps; verified
  byte-identical to the prior wave's sc_full.zag via cmp.
- Compiled with pinned znc to sc_bin.
- Ran 3/3 runs; outputs byte-identical to each other AND to the prior
  wave's run hash eee373a21053b2a3a0005be8c1c83ed923f51b22c528b36cd9425d3052146d9d.

## Identity
- Worker: Clean Scaling Rerun Worker (Micah Priority 6).
- Reproducing: commit 11adcb0ea (Scaling continuation).
- Frozen source: read-only. Nothing pushed (local commits only).
