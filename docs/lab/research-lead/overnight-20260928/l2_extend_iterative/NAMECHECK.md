# NAMECHECK.md -- L2 Iterative Extension Worker (L2-EXTENDN-1)

## Step 0: Toolchain Guard
- Date: 2026-10-02
- Safebin setup: ran
  `docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`;
  36 tools linked; `export PATH="$HOME/safebin"`.
- `which python3` under worker PATH: (empty, rc=1) -- GUARD PASS
- `which python` under worker PATH: (empty, rc=1) -- GUARD PASS
- No forbidden executables invoked at any point in this session.
- Pinned znc: src/tools/toolchain/znc_linux_x86_64_abed8aa1
- Pure Zag for all computation. Shell only for pinned znc, built
  binaries, git, and file moves.

## Step 1: Provenance
- Worker: L2 Iterative Extension Worker (subagent, 2026-10-02)
- Parent mandate: L2 ITERATIVE EXTENSION (EXTEND-N). Carry-forward
  from H-COMPINTEG-1 ledger C295: frozen EXTEND-ONE cannot
  accumulate multi-link chains; fresh prereg for iterative
  multi-link extension, not salvage of the old one.
- Branch: tnn-native-lab, local only, nothing pushed.

## Step 2: Commit order self-check
- PREREG.md committed first together with this NAMECHECK.md
  (Step 0 guard only): 800a9558a (the only two pathspecs in that
  commit; `git show --stat` verified 2 files, no implementation).
- Implementation (extn_patch.zag, extn_driver.zag, build.sh,
  frozen copies, runs, REPORT.md) written only after.
- Prereg freeze ordering: PASS.

## Step 3: Build records
- Frozen copies sha256 (verified identical to origins at copy time):
  - cc_base.zag dc0e86d44db11390e6e7d2450e1b52d7fb8f8012b42346dc4d4739ef888d1ab6
  - un_patch.zag 3e61056a3f46148393a386ee88fadb1328ab419ce627e77cb56a9aa6aa06eab2
  - adapt_patch.zag 867bd6d96d9d4026c39d9bc5a9c6944f9ac0427722a3f6451c325c49f60c2ff0
- Build: cat cc_base.zag un_patch.zag adapt_patch.zag extn_patch.zag
  extn_driver.zag > extn_full.zag; compile with pinned znc to extn_bin.
  extn_full.zag d835d2d605c1fd1015d645c236d7b27fcbfb8e108da7c5b9d6441ff7ab709e65
  extn_bin d6a20a0537745d4d564bc744b3eafa6ef8af837c5c0bf5d876aa281260f1b016
- Runs: 3x ./extn_bin > extn_runN.txt; sha256
  355a059fd987f78f96b5f0ccaaeae83dbe640e96adfd1d2a908fa63a7eedd59a (all three),
  pairwise cmp clean, exit 0.
- Audits: dash check clean on all deliverables; frozen-source
  sha256 audit clean; origins unmodified; 0-new-machinery grep
  audit clean (one link_edge in new code: type-16 only).
- One driver assertion bug fixed pre-report (A1 7-link relseq
  compared against a 6-slot buffer); operator output already
  matched the frozen prereg; no bar touched.

## Step 4: Constraints
- Pure Zag. Zero em/en dashes in all loop docs. Paper untouched.
- Nothing pushed (commits carry "Local only, never pushed.").
- 0 new edge types, 0 new opcodes, 0 modes, 0 bridges, 0 handlers,
  0 new semantic cases. Type-16 adapted-from reuse only.
