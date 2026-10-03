# NAMECHECK.md -- Truncate Theorem Boundary Worker

## Step 0: toolchain guard (mandatory)

- Ran the safebin setup at startup: `$HOME/safebin` holds the
  allowed tools (git, znc, coreutils and standard shell
  utilities). `export PATH="$HOME/safebin"`.
- `which python3 python` returns nothing under the safebin
  PATH (verified 2026-10-02, guard-check-done).
- build.sh re-checks the guard first and aborts if
  python3/python resolve; the build printed
  "guard: python3/python absent, znc=/home/hatch/safebin/znc".
- All research logic is pure Zag (znc). Shell used only to
  invoke znc, run the binary, and do git/file operations.
- No forbidden executable was invoked during this wave.
- Step 0: PASS.

## Provenance

- The implementation sources (tt_patch.zag, tt_driver.zag,
  build.sh) were found in the working tree as untracked files
  from a prior incomplete wave (never committed, no REPORT
  produced). This worker read tt_patch.zag and tt_driver.zag
  in full, verified each construct against the PREREG plus
  Amendment 1, rebuilt tt_bin from source itself, and ran all
  three runs itself. Nothing from the prior wave was taken on
  trust.
- PREREG.md frozen at commit 49641f9c8, sha256
  5f297cb95a03b8bc11734e03cda96de336303d79a28b9355ab3772fe97f3bc5e
  (matches the frozen commit byte for byte). Not modified.
- PREREG_AMENDMENT1.md is committed in HEAD (committed alone
  before this worker's implementation commit; no result had
  been adopted by this worker). Its arm A correction was
  independently verified from the frozen substrate:
  ts_truncate_src and tt_nonprefix_src both require
  cc_satisfy(src, s) == L, and in arm A phase 2 the query
  source s = 32 cannot satisfy Z = [1,2,1] (rooted at 31, no
  live (32,1,*) fact), so the ev_query_tt fallback can never
  create the head-drop there. No kill bar weakened; K-A1
  strengthened with the nk = 1 determinism requirement.

## Commit-order self-check

- PREREG.md committed ALONE first: commit 49641f9c8,
  2026-10-02. No implementation in that commit.
- PREREG_AMENDMENT1.md committed alone in HEAD before any
  implementation commit by this worker.
- Implementation (tt_patch.zag, tt_driver.zag, build.sh,
  tt_full.zag, tt_bin, compile.txt, run outputs,
  sha256sums.txt, frozen source copies, NAMECHECK.md,
  REPORT.md) committed only after the prereg and the
  amendment, with explicit pathspecs.
- Nothing pushed to GitHub (local commits on
  tnn-native-lab only).
- Commit-order: PASS.

## Frozen vs unfrozen

- Unfrozen (this experiment only):
  `docs/lab/research-lead/overnight-20260928/truncate_theorem/`.
- Frozen, read-only (sha256-verified copies, not modified):
  - `adapt_revision_ops/cc_base.zag`
    (dc0e86d44db11390e6e7d2450e1b52d7fb8f8012b42346dc4d4739ef888d1ab6)
  - `adapt_revision_ops/un_patch.zag`
    (3e61056a3f46148393a386ee88fadb1328ab419ce627e77cb56a9aa6aa06eab2)
  - `adapt_revision_ops/adapt_patch.zag`
    (867bd6d96d9d4026c39d9bc5a9c6944f9ac0427722a3f6451c325c49f60c2ff0)
  - `adapt_revision_ops/revise_patch.zag`
    (5113000b1360bf3e978cb106f91f15a1e5956db113eb4b3c26a1ebde1fa7f6e3)
  - `adapt_revision_ops/ts_patch.zag`
    (07b7b3952db65b04d8bccf288d28ff0a2aaa899fefd75a1da0250baa7d22b451)

## Build records

- Pinned znc; compile exit 0; tt_bin 384548 bytes, sha256
  b42699fece7259cb9cbf1c2350b604dc857c053d1863097930a15568ae1f59ad.
- 3/3 byte-identical runs: sha256
  50d1fbf818b7b046f3587569afbe0fe568f7f071d1ec698d3ffca3fc29a0f8ff
  for run1.txt, run2.txt, run3.txt; cmp clean.
- Verdict lines: A-NONPREFIX-STALE=PASS,
  B-PREFIX-MID-REPLACE=PASS, C-PREFIX-ROOT-REPLACE=PASS,
  T-THEOREM-CONTROL=PASS.
- REVISE2-STALE emission count across all runs: 0.
- K-H1: no em/en dash bytes in PREREG.md, REPORT.md,
  NAMECHECK.md, tt_patch.zag, tt_driver.zag.
- K-H2: five frozen copies sha256-identical to originals;
  whole-word mode/bridge/handler grep on new sources = 0;
  no `as *i32` pattern; safebin guard enforced by build.sh.

## Architecture accounting

- Cognition lines added (unfrozen): tt_patch.zag
  (tt_nonprefix_src, adapt_nonprefix, ev_query_tt) and
  tt_driver.zag (4 arms plus local helpers).
- New hardcoded semantic cases: 0. New modes: 0. New
  bridges: 0. New handlers: 0. New opcodes: 0. New MAP
  types: 0. New edge types: 0.
