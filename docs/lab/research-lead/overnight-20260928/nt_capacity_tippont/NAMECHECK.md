# NAMECHECK: NT-CAPACITY-TIPPOINT

## Step 0: Toolchain guard (mandatory, Micah's 2026-09-30 ruling)

- Worker PATH: `$HOME/safebin` only (allowed tools: coreutils, git,
  pinned znc; `python3`/`python` do not resolve). Activated via
  `export PATH="$HOME/safebin"` at startup.
- `which python3` returns nothing under the worker PATH.
- `which python` returns nothing under the worker PATH.
- All computational research operations in pure Zag (znc 2026.07.0-dev).
  Shell only: invoke znc, run binaries, git ops, move/copy files,
  cmp/sha256.
- If a forbidden executable is invoked, this lane's wave is
  automatically PROCESS-FAIL and any result stays exploratory pending
  a clean re-freeze. Zero forbidden invocations to record.

## Lane identity

- Lane: `docs/lab/research-lead/overnight-20260928/nt_capacity_tippont/`
- Task: locate the exact integer tipping point of the D6 assoc pin's
  opportunity-cost curve found by NT-CAPACITY-SWEEP (CURVE-CONFIRMED:
  cost YES at CAP=20, clean at CAP=22/24). Run CAP=21 (predicted CLEAN:
  u=4, forget=0, phev=0, nevict=28, EVHIST 131=5,140=6,141=6,143=6,
  144=5) plus a CAP=22 regression arm in one binary. Predicted overall
  verdict: TIPPOINT-LOCATED-AT-20 (cost iff CAP <= 20, clean iff
  CAP >= 21 on the tested slice).
- Learner and oracles are NT-CAPACITY-SWEEP verbatim except the arm
  list (R6-CAP21 + R6-CAP22). Non-ledger task (claim minting paused).

## Commit-order self-check

- Prereg commit (PREREG.md + NAMECHECK.md only) must strictly precede
  the implementation commit. Verified via `git log` before writing
  REPORT.md. No implementation file exists at prereg time.
- Commits go to `tnn-native-lab` (not a side branch) with explicit
  pathspecs, via git plumbing (separate index file, read-tree /
  write-tree / commit-tree / update-ref with old-value check),
  because the shared working tree is on a side branch with other
  workers' staged changes. The shared index is never touched.
- Git writes go through `/usr/bin/git` directly (safebin `git` symlink
  EPERM lesson, AGENTS.md 2026-10-03); index.lock contention is retried
  with sleep backoff, never by removing the lock.

## Provenance notes (filled as the lane proceeds)

- PREREG.md: frozen CAP=21 hand-derived trace (Section 5.1), frozen
  kill bars U1-U5 (CAP=21) and R1-R7 (CAP=22 regression), verdict
  mapping (Section 8). Predicted verdict: TIPPOINT-LOCATED-AT-20.
- Prereg freeze: commit `<hash>` on `tnn-native-lab`
  (PREREG.md + NAMECHECK.md only), strictly before implementation.
- Implementation: `nttip_full.zag` (NT-CAPACITY-SWEEP source verbatim
  + 2-arm main + per-arm bars).
- Build `znc nttip_full.zag -o nttip_bin` under safebin-only PATH.
  3/3 runs byte-identical, exit 0, zero stderr.
- Results: (filled after runs)
- Digests: run `<sha>`, bin `<sha>`, src `<sha>`.
- Commits local only, explicit pathspecs, never pushed.
  Non-ledger task (claim minting paused).
