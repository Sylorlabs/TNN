# NAMECHECK.md -- L2 Revision Mid-Iteration Worker (L2-EXTENDN-2)

## Step 0: Toolchain Guard
- Date: 2026-10-02
- Safebin setup: ran
  `docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`
  from ~/workspace/tnn-rsi; SAFEBIN-READY, 36 tools linked;
  `export PATH="$HOME/safebin"`.
- `which python3` under worker PATH: (empty, rc=1) -- GUARD PASS
- `which python` under worker PATH: (empty, rc=1) -- GUARD PASS
- No forbidden executables invoked at any point in this session.
- Pinned znc: src/tools/toolchain/znc_linux_x86_64_abed8aa1
- Pure Zag for all computation. Shell only for pinned znc, built
  binaries, git, and file moves.

## Step 1: Provenance
- Worker: L2 Revision Mid-Iteration Worker (subagent, 2026-10-02)
- Parent mandate: L2-EXTENDN-2 REVISION MID-ITERATION. Fuses the
  C301 iterative-extension operator with revision machinery;
  exercises the EXECFAIL stop C301 left untested. Fresh
  preregistration, not salvage of the old lane.
- Branch: tnn-native-lab, local only, nothing pushed.

## Step 2: Commit order self-check
- Prereg commit a259f0a2d contains only PREREG.md and
  NAMECHECK.md (Step 0 guard); `git show --stat` verified
  2 files, 265 insertions, no implementation.
- Implementation (rv_patch.zag, rv_driver.zag, build.sh,
  frozen copies, runs, REPORT.md) written only after.
- Prereg freeze ordering: PASS.

## Step 3: Build records
- Frozen copies sha256 (verified identical to C301 origins):
  - cc_base.zag dc0e86d44db11390e6e7d2450e1b52d7fb8f8012b42346dc4d4739ef888d1ab6
  - un_patch.zag 3e61056a3f46148393a386ee88fadb1328ab419ce627e77cb56a9aa6aa06eab2
  - adapt_patch.zag 867bd6d96d9d4026c39d9bc5a9c6944f9ac0427722a3f6451c325c49f60c2ff0
- Build: cat cc_base.zag un_patch.zag adapt_patch.zag rv_patch.zag
  rv_driver.zag > rv_full.zag; compile with pinned znc to rv_bin.
  rv_full.zag 23fc9ce8ac629cf8a3f7b41b1975fb1f23f28bd3dce822ded555f70e79ea7687
  rv_bin c4738ff5eb65ab3c9b89be2155a86e58efe07e0f176ef6d03a59cbdfc3c571e4
- Runs: 3x ./rv_bin > rv_runN.txt; sha256
  10fb3633f4dac33e7c913ddde9ac88a56a5786769da3552abe69bc2e60e5847d (all three),
  pairwise cmp clean, exit 0.
- Audits: dash check clean on all deliverables; frozen-source
  sha256 audit clean; origins unmodified; 0-new-machinery grep
  audit clean (link_edge in new code: type-16 operator
  provenance x2, type-3 world-kill self-loop x1; no new node
  tags); negated-conjunction while grep clean.

## Step 4: Constraints
- Pure Zag. Zero em/en dashes in all loop docs. Paper untouched.
- Nothing pushed (commits carry "Local only, never pushed.").
- 0 new edge types, 0 new opcodes, 0 modes, 0 bridges, 0 handlers,
  0 new semantic cases. Type-16 adapted-from reuse only, plus the
  disclosed world-kill type-3 self-loop reusing the frozen
  supersede semantic.
