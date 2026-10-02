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
  (Step 0 guard only); commit contains no implementation files.
- Implementation (.zag sources, build.sh, runs, REPORT.md) written
  only after the prereg commit.
- Prereg freeze ordering: PASS (record hashes below after commit).

## Step 3: Build records
(to be filled after implementation)
- Frozen copies sha256 (verified identical to origins at copy time):
  - cc_base.zag: (pending)
  - un_patch.zag: (pending)
  - adapt_patch.zag: (pending)
- Build: cat cc_base.zag un_patch.zag adapt_patch.zag extn_patch.zag
  extn_driver.zag > extn_full.zag; compile with pinned znc to extn_bin.
- Runs: 3x ./extn_bin > extn_runN.txt; sha256 + pairwise cmp.
- Audits: dash check on all deliverables; frozen-source sha256 audit;
  0-new-machinery grep audit.

## Step 4: Constraints
- Pure Zag. Zero em/en dashes in all loop docs. Paper untouched.
- Nothing pushed (commits carry "Local only, never pushed.").
- 0 new edge types, 0 new opcodes, 0 modes, 0 bridges, 0 handlers,
  0 new semantic cases. Type-16 adapted-from reuse only.
