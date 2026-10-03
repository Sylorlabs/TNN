# NAMECHECK: NT-USEFUL-EVICT

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

- Lane: `docs/lab/research-lead/overnight-20260928/nt_useful_evict/`
- Task: usefulness-aware eviction rule (D4: evict-least-read, where
  "read" = the entry contributed an answer to a query; max-ins
  tie-break) on the NT-LOWVALUE-BOUNDARY workload in BOTH teach
  orders (RARE-last liability case and RARE-first mirror case),
  K=1,2,3,6 (8 arms). Tests NTFQ's recommended follow-up: does a
  learner-available relevance signal pin 148 in both orders and at
  K=6? New rule = new lane; D1/D2/D3 lanes untouched.
- Non-ledger task (claim minting paused).

## Commit-order self-check

- Prereg commit (PREREG.md + NAMECHECK.md only) must strictly precede
  the implementation commit. Verified via `git log` before writing
  REPORT.md. No implementation file exists at prereg time.
- Commits go to `tnn-native-lab` (not a side branch) with explicit
  pathspecs, via a git worktree (the shared working tree stays on
  its branch with other workers' staged changes untouched).

## Provenance notes (filled as the lane proceeds)

- PREREG.md: frozen kill bars K1-K7, hand-derived predictions for
  all 8 arms (Section 5), verdict mapping (Section 8). No
  implementation yet.
- znc: pinned 2026.07.0-dev (same build as NT1/NT-D2/NT-PORT/
  NT-PRESSURE/NT-PORT-PRESSURE/NT-LOWVALUE-BOUNDARY/NT-ORDER-
  MIRROR/NT-FREQ-EVICT).
- Build: `znc ntue_full.zag -o ntue_bin` under safebin-only PATH.
- Runs: 3/3 byte-identical (cmp), exit 0, zero stderr.
- Commits local only, explicit pathspecs, never pushed.
