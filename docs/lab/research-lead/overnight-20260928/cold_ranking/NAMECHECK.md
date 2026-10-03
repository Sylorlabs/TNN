# NAMECHECK: COLD-RANKING (LRU/importance ranking within cold)

Worker: COLD-RANKING worker (non-ledger task; claim minting
paused). Lane:
docs/lab/research-lead/overnight-20260928/cold_ranking/

## Step 0: Toolchain guard (recorded at lane startup)

- safebin at $HOME/safebin; PATH exported to $HOME/safebin for every
  build/run command.
- `command -v python3` and `command -v python` return nothing under
  that PATH (verified 2026-10-03 at lane startup; /usr/bin/python3
  exists outside the safebin PATH and is never invoked).
- znc resolves inside safebin as the pinned compiler
  (znc 2026.07.0-dev (edition 2026)); cmp-verified byte-identical
  to src/tools/toolchain/znc_linux_x86_64_abed8aa1 before the prereg
  commit.
- Shell use limited to: mkdir, znc invocation, binary execution,
  sha256sum, cmp, git ops, file reads/writes. No forbidden
  executable invoked. No PROCESS-FAIL condition triggered.
- Git writes via /usr/bin/git directly (safebin git symlink EPERM
  lesson, 2026-10-03); explicit pathspecs; no git reset; local only,
  never pushed. Another worker's stale cherry-pick is in progress
  repo-wide; this lane does not touch it (no --continue, --skip,
  --abort, no reset).
- grep audit planned on the new code: no negated-conjunction while
  conditions (`grep -n 'while.*!('`); if-nesting at most 3; u8-backed
  cells with put32/ig helpers only; output via one preallocated
  buffer plus a single _zag_raw_syscall write.

## Conventions carried from EXILE-PROMOTION

- Pure Zag for all scientific computation.
- Prereg committed alone before implementation (strict commit
  order); the prereg freezes all predicted values and kill bars.
- 3/3 byte-identical runs (sha256 equal) required; determinism bar
  is VOID-grade.
- Frozen kill bars are never weakened or reinterpreted after
  results. The erratum process (dated, transparent, derivation
  errors only) is the sole correction path.
- Build on EXILE-PROMOTION; do not redesign. New code is additive:
  header offsets 64 (rank_cost) and 68 (rank_moves); rk threaded
  through mem_read_recov / test_A_recov / cold_lookup; rank move on
  every cold hit after the rc increment and before the promotion
  check (move-then-promote); rc byte moves with its slot; rk=1 is
  move-to-front (recency), rk=2 is bubble-up while rc(s) >
  rc(s-1) (importance); rk=0 leaves cold_lookup behavior-identical
  to EXILE-PROMOTION.
- The anchor is rk=0, pm=1, M2C2: must reproduce EXILE-PROMOTION's
  published PXP-M2C2 row bit-for-bit (cc4=712, ccT=1132, rkT=0).
  Any drift is FAIL.
- znc's && short-circuits: test reads that must execute are
  let-bound, as in EXILE-PROMOTION.
