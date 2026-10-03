# NAMECHECK: H3-SEALED

Worker: H3-SEALED worker (non-ledger task; claim minting paused).
Lane: `docs/lab/research-lead/overnight-20260928/h3_sealed/`.
Date: 2026-10-03.

## Step 0: toolchain guard (safebin mandatory)

- Safebin activated at worker startup: `export PATH="$HOME/safebin"`.
- `which python3` returns nothing; `which python` returns nothing (verified
  2026-10-03, before the prereg commit).
- `~/safebin/znc` is byte-identical (sha256
  498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef) to the
  pinned compiler
  `~/workspace/tnn-rsi-gpi3/src/tools/toolchain/znc_linux_x86_64_abed8aa1`
  (`znc 2026.07.0-dev (edition 2026)`); verified before the prereg commit.
- Shell used only for mkdir, file writes, binary execution, sha256sum, cmp,
  diff, grep, and git ops. All scientific computation in pure Zag.
- Git writes via `/usr/bin/git` directly (safebin git symlink EPERM lesson
  from AGENTS.md); explicit pathspecs; no `git reset`; local only, never
  pushed.

## Commit-order self-check

- This commit (PREREG.md + NAMECHECK.md, alone) strictly precedes the
  implementation commit and all runs. No implementation exists in this lane
  at prereg time. The sealed worlds' predictions are frozen here.
- Two-hat record: adversary designs (W1..W4, attack hypotheses) were fixed
  from the H3/H3B published reports and preregs before the .zag source was
  consulted; the source was read before this prereg only to validate
  interface assumptions A1..A5 (recorded in PREREG.md). No world design
  changed as a result.
