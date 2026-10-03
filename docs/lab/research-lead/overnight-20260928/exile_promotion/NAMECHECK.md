# NAMECHECK: EXILE-PROMOTION (promotion / reheat dynamics)

Worker: EXILE-PROMOTION worker (non-ledger task; claim minting
paused). Lane:
docs/lab/research-lead/overnight-20260928/exile_promotion/

## Step 0: Toolchain guard (recorded at lane startup)

- safebin at $HOME/safebin; PATH exported to $HOME/safebin for every
  build/run command.
- `which python3` and `which python` return nothing under that PATH
  (verified 2026-10-03 at lane startup; /usr/bin/python3 exists
  outside the safebin PATH and is never invoked).
- znc resolves inside safebin as the pinned compiler
  (znc 2026.07.0-dev (edition 2026)); cmp-verified byte-identical
  to src/tools/toolchain/znc_linux_x86_64_abed8aa1 before the prereg
  commit.
- Shell use limited to: mkdir, znc invocation, binary execution,
  sha256sum, cmp, git ops, file reads/writes. No forbidden
  executable invoked. No PROCESS-FAIL condition triggered.
- Git writes via /usr/bin/git directly (safebin git symlink EPERM
  lesson, 2026-10-03); explicit pathspecs; no git reset; local only,
  never pushed. A stale cherry-pick is in progress repo-wide from
  another worker; this lane does not touch it (no --continue,
  --skip, --abort, no reset).
- grep audit planned on the new code: no negated-conjunction while
  conditions (`grep -n 'while.*!('`); if-nesting at most 3; u8-backed
  cells with put32/ig helpers only; output via one preallocated
  buffer plus a single _zag_raw_syscall write.

## Conventions carried from RECLAMATION-H2

- Pure Zag for all scientific computation.
- Prereg committed alone before implementation (strict commit
  order); the prereg freezes all predicted values and kill bars.
- 3/3 byte-identical runs (sha256 equal) required; determinism bar
  is VOID-grade.
- Frozen kill bars are never weakened or reinterpreted after
  results. H2's erratum process (dated, transparent, derivation
  errors only) is the sole correction path.
- Build on H2; do not redesign. New code is additive: header
  offset 60 (promote counter), cold recovery-count side table at
  base 4032 (64 x u8), rcount reset in exile_victim, promotion
  trigger in cold_lookup at frozen threshold T=2, promote_slot
  (move-not-copy; first free pool slot else min last-touch victim
  re-exiled), pm threaded through mem_read_recov / test_A_recov,
  anchor run_cond with pm, and the run_promo driver (3 recovery
  passes + optional second churn + R4).
- Five pm=0 anchors must reproduce H2's frozen rows bit-for-bit
  (EXH2-B0, EXH2-A32, EXH2-M2, EXH2-OVF, EXCON-M2); any drift is
  FAIL.
- The discriminating conditions are pm=1: PXP-B0 (promotion inert),
  PXP-M2 (amortization + hot restoration), PXP-M2C2 (reheat after
  partial rechurn), PXP-OVF (promotion cannot resurrect cold-FIFO
  destruction).
- znc's && short-circuits: test reads that must execute are
  let-bound, as in H2.
