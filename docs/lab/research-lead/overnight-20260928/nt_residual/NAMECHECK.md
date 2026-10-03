# NAMECHECK: NT-RESIDUAL

## Step 0: Toolchain guard (mandatory, Micah's 2026-09-30 ruling)

- Worker PATH: `$HOME/safebin` only (36 allowed tools: coreutils, git,
  pinned znc). Activated via `export PATH="$HOME/safebin"` at startup.
- `which python3` returns nothing under the worker PATH.
- `which python` returns nothing under the worker PATH.
- All computational research operations in pure Zag (znc). Shell only:
  invoke znc, run binaries, git ops, move/copy files, cmp/sha256.
- If a forbidden executable is invoked, this lane's wave is
  automatically PROCESS-FAIL and any result stays exploratory pending
  a clean re-freeze. Zero forbidden invocations to record.

## Lane identity

- Lane: `docs/lab/research-lead/overnight-20260928/nt_residual/`
- Task: the residual case from NT-NONLOCAL's recommended follow-up
  #1: a rare-but-useful link (160->161->162) that is NEVER a
  revision target. Single arm R6 (K=6, LAST). Learner is the NTNL
  D5 learner verbatim; only the workload gains two keys and one
  per-pass probe (q(160) vs 162). Tests: does D5 protect the
  residual link (predicted NO), does it still protect 148 in the
  same run (dissociation), and is any learner-available signal
  available that could predict the residual link's usefulness
  (predicted: fundamentally impossible in this workload).
- Non-ledger task (claim minting paused).

## Commit-order self-check

- Prereg commit (PREREG.md + NAMECHECK.md only) must strictly precede
  the implementation commit. Verified via `git log` before writing
  REPORT.md. No implementation file exists at prereg time.
- Commits go to `tnn-native-lab` (not a side branch) with explicit
  pathspecs, via git plumbing (separate index file, read-tree /
  write-tree / commit-tree / update-ref with old-value check), because
  the shared working tree is on a side branch with other workers'
  staged changes. The shared index is never touched.

## Provenance notes (filled as the lane proceeds)

- PREREG.md: frozen kill bars K1-K7, hand-derived Section 5
  predictions (single arm R6), verdict mapping (Section 8).
  Predicted verdict: RESIDUAL-CONFIRMED.
