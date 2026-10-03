# NAMECHECK: NT-TEACHASSOC-CTRL

## Step 0: Toolchain guard (mandatory, Micah's 2026-09-30 ruling)

- Worker PATH: `$HOME/safebin` only (coreutils, git, pinned znc
  2026.07.0-dev). Activated via `export PATH="$HOME/safebin"` at
  startup and in every exec call that builds or runs.
- `which python3` returns nothing under the worker PATH.
- `which python` returns nothing under the worker PATH.
- All computational research operations in pure Zag (znc). Shell only:
  invoke znc, run binaries, git ops, move/copy files, cmp/sha256.
- If a forbidden executable is invoked, this lane's wave is
  automatically PROCESS-FAIL and any result stays exploratory pending
  a clean re-freeze. Zero forbidden invocations to record.

## Lane identity

- Lane: `docs/lab/research-lead/overnight-20260928/nt_teachassoc_ctrl/`
- Task: the recommended follow-up from NT-TEACHASSOC (ASSOC-CONFIRMED):
  the no-exploratory control arm. Identical world to NT-TEACHASSOC
  (D1-D6 learner incl. D6 code, CAP=22, decoy chain taught, per-pass
  q(100)/q(160) probes, retest, bprobe, resprobe) MINUS the four
  exploratory query events (q(160),q(161),q(170),q(171) post-phase-1).
  Tests: (a) D6 provably inert with no exploratory queries
  (apin=0); (b) the residual chain NOT rescued (avail160=0,
  resprobe=0, evh(161)=1 -- mechanism-level reproduction of
  NT-RESIDUAL's headline); (c) D5 still covers 148, retention
  intact. Predicted verdict: CTRL-CONFIRMED.
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
- Git writes go through /usr/bin/git directly (AGENTS.md lesson:
  the $HOME/safebin/git symlink can fail object/index writes with
  EPERM); the worker PATH stays safebin-only (no python).

## Provenance notes (filled as the lane proceeds)

- PREREG.md: frozen kill bars K1-K7, hand-derived Section 4 trace
  (single arm R6), verdict mapping (Section 7). Predicted verdict:
  CTRL-CONFIRMED.
- Prereg freeze: commit `<hash>` on `tnn-native-lab`
  (PREREG.md + NAMECHECK.md only), strictly before implementation.
- Implementation: `ntctrl_full.zag` (NT-TEACHASSOC's ntteach_full.zag
  verbatim except: exploratory episode deleted; tag NTTCTRL; fprate
  guarded against apin=0; kill bars / verdict codes per PREREG
  Section 6-7). No learner rule touched.
- Build `znc ntctrl_full.zag -o ntctrl_bin` under safebin-only PATH.
  3/3 runs byte-identical, exit 0, zero stderr.
- Results: K1-K7 all 1, VERDICT=CTRL-CONFIRMED.
- Commits local only, explicit pathspecs, never pushed.
  Non-ledger task (claim minting paused).
