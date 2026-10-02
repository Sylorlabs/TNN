# NAMECHECK.md -- Composition Integration Worker (H-COMPINTEG-1)

## Step 0: Toolchain Guard
- Date: 2026-10-02
- Safebin setup: `mkdir -p $HOME/safebin`, symlinked allowed tools
  (git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp
  sha256sum git-receive-pack git-upload-pack); `export PATH="$HOME/safebin"`
- `which python3 python` under worker PATH: (empty, no output) -- GUARD PASS
- No forbidden executables invoked at any point.
- Pinned znc: src/tools/toolchain/znc_linux_x86_64_abed8aa1

## Step 1: Provenance
- Worker: Composition Integration Worker (subagent, 2026-10-02)
- Parent mandate: integrate C278/C279/C280/C289/C290/C291; report
  where integration breaks.
- Branch: tnn-native-lab, local only, nothing pushed.

## Step 2: Commit order self-check
- PREREG.md committed ALONE first: 05d1b7a28 (this file was the only
  pathspec in that commit). Implementation (integ_patch.zag,
  integ_driver.zag, build.sh, frozen copies) written only after.
- Prereg freeze ordering: PASS.

## Step 3: Build records
- Frozen copies sha256 (verified identical to origins at copy time):
  - cc_base.zag dc0e86d44db11390e6e7d2450e1b52d7fb8f8012b42346dc4d4739ef888d1ab6
  - un_patch.zag 3e61056a3f46148393a386ee88fadb1328ab419ce627e77cb56a9aa6aa06eab2
  - adapt_patch.zag 867bd6d96d9d4026c39d9bc5a9c6944f9ac0427722a3f6451c325c49f60c2ff0
  - revise_patch.zag 5113000b1360bf3e978cb106f91f15a1e5956db113eb4b3c26a1ebde1fa7f6e3
  - ts_patch.zag 07b7b3952db65b04d8bccf288d28ff0a2aaa899fefd75a1da0250baa7d22b451
  - lvcomp_patch.zag ea833de28d21657b6cb6dcf2ad8c378b6cf604ccbe81680b6acfdcc68e24c302
- Build: cat cc_base un_patch adapt_patch revise_patch ts_patch
  lvcomp_patch integ_patch integ_driver > integ_full.zag; compile
  with pinned znc to integ_bin.
- Runs: 3x ./integ_bin > integ_runN.txt; sha256 + pairwise cmp.
- Audits: grep for `expected` in integ_patch.zag (must be absent);
  byte-check for em/en dashes in all deliverables.

## Step 4: Constraints
- Pure Zag. Zero em/en dashes. Paper untouched. Nothing pushed.
- 0 modes, 0 bridges, 0 handlers, 0 new semantic cases, 0 new
  opcodes, 0 new MAP/edge types.

## Step 5: Verification session (2026-10-02, second worker session)

- Step 0 re-verified: safebin_setup/setup_safebin.sh run fresh;
  36 tools linked, `which python3` and `which python` return
  nothing under worker PATH. Pinned znc confirmed at
  src/tools/toolchain/znc_linux_x86_64_abed8aa1. No forbidden
  executable invoked in this session. GUARD PASS.
- K8 re-verified: all six frozen copies sha256-identical to
  origins (hashes match the Step 3 record; un_patch.zag matches
  the prereg record 3e61056a...); origins unmodified
  (`git diff --stat` on all origin dirs empty).
- K7 audit correction: the token `expected` was present 3x in
  integ_patch.zag comments (lines 11, 23, 171). Reworded to
  researcher-provided/answer; code semantics untouched. grep now
  returns 0. Dash audit: check_no_dash.sh exit 0 on
  integ_patch.zag, integ_driver.zag, NAMECHECK.md, build.sh,
  REPORT.md.
- Fresh rebuild: build.sh, compile exit 0. integ_full.zag
  047bd54e070aaedc10d800209e0e70d0064b126ba866efc8901d8919001e13ce
  (byte-identical to cat of the 8 sources in build order, cmp
  clean). integ_bin
  a44e696642dd6e38a9d3696b6393ced1880030519e92549d4a1a813d2c7ffc7c.
- Runs: 3x ./integ_bin > integ_runN.txt, exit 0 each; sha256
  d0ec18fd37dbe43b8122251ca0a8d083fec7a8b56d0fed42319103cd6fc0d1bc
  all three; pairwise cmp clean. K6 PASS.
- Cognition lines (integ_patch.zag, non-comment non-blank): 157.
- Commit order re-verified: `git show --stat 05d1b7a28` shows
  PREREG.md as the sole file. Freeze ordering: PASS.

## Final battery build record (amended design, Amendments 1-3)

- Amendments 1/2/3 each committed before the redesigned
  implementation was run (6bdfb7216 amends 1+2 and 3; the final
  driver edits and Amendment 3 are included here).
- Rebuild: build.sh, compile exit 0 (warnings only, A0102 class).
  integ_full.zag is the cat of the 8 sources in build order.
- Runs: 3x ./integ_bin > integ_runN.txt, exit 0 each; sha256
  8e73222767a21f5a89e5d35b13a7730e261ee47aabd281e5dacf2784f05797f1
  all three; pairwise cmp clean. K6 PASS.
- K7: `expected` absent from integ_patch.zag (grep 0); zero
  em/en dashes byte-verified across all deliverables; 0
  modes/bridges/handlers (single comment declaration only).
- K8: frozen copies sha256-verified against origins at copy
  time; origins unmodified.
- Cognition lines: integ_patch.zag 157, integ_driver.zag 335
  (harness).
- Verdict: COMPOSITION-INTEGRATION-COMPLETE. K1-K5 PASS (arms),
  K6-K8 PASS. I5 diagnostic PASS (non-gating).
