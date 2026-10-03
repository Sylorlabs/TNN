# NAMECHECK: COMPRESSION-EXEC (E10.1 TRIAL-UNIFY)

Worker: COMPRESSION-EXEC subagent, 2026-10-03.
Lane: `docs/lab/research-lead/overnight-20260928/compression_exec/`
Task: Execute FRONTIER-AUDIT proposal E10.1 TRIAL-UNIFY, the audit's
Rank-1 compression candidate (compression_audit/COMPRESSION_AUDIT.md
section 3, Rank 1): rewrite t2_trial's four-phase loop as ONE generic
candidate-source iterator (phase table of (gather, assemble) pairs
driven by a single loop) on the frozen TNN-2 base.
Non-ledger task (claim minting paused); nothing minted.

## Step 0: toolchain guard (safebin mandatory)

- safebin present at /home/hatch/safebin (51 tools, znc included).
- Verified 2026-10-03 (this worker, before any work): with
  PATH="$HOME/safebin": `which python3` -> empty; `which python` ->
  empty; `which znc` -> /home/hatch/safebin/znc, znc 2026.07.0-dev
  (edition 2026).
- All research computation in this lane is pure Zag, compiled with
  the pinned safebin znc. Shell is used only for znc/binary/git/
  byte-verification (diff, cmp, sha256sum, grep).
- If any forbidden executable is invoked, the wave is PROCESS-FAIL
  per standing governance.
- Git note: $HOME/safebin/git is a symlink to /usr/bin/git with a
  known EPERM-on-write failure mode on this shared worktree; all git
  writes in this lane use /usr/bin/git directly, with explicit
  pathspecs, never bare `git commit`, never `git reset`.

## Step 1: identity

- Lane name matches the assigned lane exactly.
- No prior lane with this name exists in tnn-rsi-gpi3.

## Step 2: scope

- Read-only references (extracted from frozen git commits, hashes
  verified at extraction): frozen TNN-2 base tnn2.zag
  (f4de7ff46, SHA-256 a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd);
  freeze shim driver shim_driver2.zag (23c2c0206, part of source with
  SHA-256 33795c19c9f7ecd8e4c0c9a180293bf577b53ba7aae6f6a5557c972fe372ace8);
  FW1-FW9 sealed worlds (396895595, freeze_worlds_v2/worlds/).
- Writes only inside compression_exec/ (PREREG.md, this file,
  unified sources, build/run artifacts, REPORT.md).
- The frozen base is NEVER edited: the unified variant is a separate
  file. No behavior change is intended; this is a compression test.

## Step 3: commit order

- PREREG.md + this NAMECHECK.md are committed alone strictly before
  any implementation artifact (unified source, builds, runs,
  REPORT.md). Self-check recorded in PREREG.md section 7.

## Step 4: sealed-world blindness

- FW1-FW9 are sealed evaluator assets. This lane runs them as a
  no-regression check ONLY: world outputs are compared
  pre/post byte-for-byte; no world content is inspected to tune the
  implementation. The implementation is a pure refactor of t2_trial;
  no world-specific logic may be added.
