# NAMECHECK: NT-NONLOCAL

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

- Lane: `docs/lab/research-lead/overnight-20260928/nt_nonlocal/`
- Task: non-entry-local relevance signal for eviction (D5:
  revision-target pinning layered on D4's evict-least-read) on the
  NT-LOWVALUE-BOUNDARY workload in BOTH teach orders (RARE-last
  liability case and RARE-first mirror case), K=1,2,3,6 (8 arms).
  Tests the recommended follow-up from NT-USEFUL-EVICT: does a
  forward-looking, non-entry-local signal pin 148 at last-order K=6,
  the case D2, D3, and D4 all fail? New rule = new lane;
  D1/D2/D3/D4 and their lanes untouched.
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

- PREREG.md: frozen kill bars K1-K7, hand-derived predictions for
  all 8 arms (Section 5), verdict mapping (Section 8). No
  implementation yet.
