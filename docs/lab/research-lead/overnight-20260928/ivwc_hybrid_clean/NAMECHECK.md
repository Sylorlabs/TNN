# NAMECHECK.md -- IVWC-HYBRID-CLEAN (clean reproduction of IVWC-HYBRID-VERDICT)

## Purpose

IVWC-HYBRID-VERDICT reached BUILD-PASS (K1-K10) but PROCESS-FAIL on
the invocation-based guard (one accidental `python3 -c "print('skip')"`
during the K1 audit, after all builds/runs; it computed/read/wrote
nothing). This lane is the clean reproduction that lifts the
PROCESS-FAIL: rebuild of the committed source plus 3x re-runs with
**zero python3/python invocations anywhere in the session**.

This lane changes NO source and NO predictions. The frozen
preregistration is `ivwc_hybrid_verdict/PREREG.md` (commit
`99c5691da`); the implementation is `ivwc_hybrid_verdict/`
(commit `5ad68a24e`). Everything here is a byte-verifiable
reproduction of that committed work.

## Step 0: Toolchain guard (mandatory)

- Lane: `docs/lab/research-lead/overnight-20260928/ivwc_hybrid_clean/`
  (fresh lane; `ivwc_hybrid_verdict/` and all other lanes untouched --
  the verdict lane's files were only READ, never modified).
- Safebin: ran
  `docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`
  at startup, then `export PATH="$HOME/safebin"` for every build /
  run / audit command. Verified: `command -v python3` returns
  nothing, `command -v python` returns nothing under the safebin
  PATH. Pinned znc at `$HOME/safebin/znc` (symlink to
  `src/tools/toolchain/znc_linux_x86_64_abed8aa1`), version
  `znc 2026.07.0-dev (edition 2026)`.
- **Zero python3/python invocations in this session.** No python3,
  no python, no C, no JS, no Rust in build, runs, scoring, or
  analysis. Pure Zag only. The only non-safebin executable used is
  `/usr/bin/git` for worktree/commit/push operations (the safebin
  `git` symlink is known-broken for writes per AGENTS.md); git is
  version control, not research logic.
- Source identity: the rebuilt source is the committed blob
  `5ad68a24e:docs/lab/research-lead/overnight-20260928/ivwc_hybrid_verdict/src/ivwc_hybrid_verdict.zag`,
  sha256
  `2af399624ced0da22ce5d6744efc43b565200a8ecaddeaefdc08de561464c8e8`
  (1216 lines). Extracted via `git cat-file -p`; byte-verified.
- Rebuilt binary sha256:
  `6773ffab36b990abe780bb099ed2f1e477173830fd2509d81bb97ea23d6c523a`
  -- byte-identical to the binary committed in `5ad68a24e`
  (same sha256, verified via `git cat-file -p`).
- Build stderr: only the standard zagd-unavailable informational
  notice (`znc: warning: zagd unavailable; foreground compilation
  continues without background planning`). Run stderr: empty
  (0 bytes) on all 3 runs.
- Commits: explicit pathspecs confined to `ivwc_hybrid_clean/`
  (plumbing: read-tree + hash-object/update-index + write-tree +
  commit-tree + update-ref, per the shared-workspace git
  discipline; no worktree used after the first `git worktree add`
  failed at index-write time and cleaned itself up).
  The reproducible build artifact (`bin/`) is deliberately NOT
  committed, per Micah's 2026-10-03 guidance (everything except
  reproducible cache/build artifacts).
- Non-ledger task (claim minting paused).

## Step 1: What was reproduced

`src/ivwc_hybrid_verdict.zag` (pure Zag, single file, pinned znc):
train COMMIT / PREFF / CONSEQ, learner BAR (T_fixed=12,
C=15), sealed BARS (ThyA=13/20/6, ThyB=13/20/13 @15/30/45),
verdicts A1..A6 (V_T/V_N anchors) + A7a/A7b/A8a/A8b/A9a/A9b
(V_HA/V_HB hybrids), fenced SCORING (WC-FINAL=60). Rebuilt with
`znc src/ivwc_hybrid_verdict.zag -o <scratch>/ivwc_hybrid_clean_bin`
under the safebin PATH; run 3x; stdout captured to
`runs/ivwc_hybrid_clean-run{1,2,3}.txt`.

## Step 2: Frozen predictions re-verified (summary; full table in REPORT.md)

All twelve arm accuracies and all five error sets confirmed
byte-identical to the verdict run (stdout sha256
`eee1fcd97432078ce9945552222cd580cdc06dedc32294a21a5976bae73d95f4`,
3/3 identical, and `cmp`-equal to the committed
`ivwc_hybrid_verdict-run1.txt`):
- K5: A8a @15 = 11/12, errors exactly {s=5} (K5he=1, K5hs=5).
- K7: A7a @15 = 11/12, errors exactly {s=3} (K7he=1, K7hs=3).
- K9: A8a @30 = 12/12 (K9he=0).
- K10: A7a @45 = 9/12, errors exactly {s=0,s=4,s=5}
  (K10he=3, K10hs=5) -- the preregistered limit.
- K1 diet audits re-run on the source: A1 phase order
  671<684<701<769<827<854<923; A2 0 world_buf/world_off in learner
  fns; A3 0; A4 0; A5 `world_execute(` x3; A6 WC-FINAL=60;
  A7 0 learner_/belief_ after SCORING marker; A8 0 oracle.
