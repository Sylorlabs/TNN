# NAMECHECK: H3-SEALED-B

Worker: H3-SEALED-B worker (non-ledger task; claim minting paused).
Lane: `docs/lab/research-lead/overnight-20260928/h3_sealed_b/`.
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
  diff, grep, awk, and git ops. All scientific computation in pure Zag.
- Git writes via `/usr/bin/git` directly (safebin git symlink EPERM lesson
  from AGENTS.md); explicit pathspecs; no `git reset`; local only, never
  pushed.

## Step 1: source-identity pre-check (before the prereg commit)

- `h3_sealed/unpin_h3sealed.zag` sha256:
  0b26c74d377d599fc0490cd41ed8611bca04c27b6f7eb9dbcf73c9ebde7250dc
  (recorded before the prereg commit; the copy target is fixed).
- The H3-SEALED binary sha256:
  38d5da296073687c9f6f8820d19a98bd0ba297e12713490314d34d3da44d1ade
  (deterministic-rebuild check target, recorded before the prereg commit).
- No implementation exists in this lane at prereg time: the lane directory
  contains only PREREG.md and NAMECHECK.md at this commit.

## Commit-order self-check

- This commit (PREREG.md + NAMECHECK.md, alone) strictly precedes the
  implementation commit (verbatim source copy + build) and all runs. The
  corrected W2 predictions (cf=85, drop=45, ev=8) are frozen here, before
  any build or run in this lane.
- Two-hat record (inherited from H3-SEALED): adversary designs (W1..W4,
  attack hypotheses) were fixed from the H3/H3B published reports and
  preregs before the .zag source was consulted; nothing is redesigned in
  this lane. The only new content is the corrected [B]-provenance W2
  derivation, whose arithmetic error the H3-SEALED worker owned and froze
  in its report.
