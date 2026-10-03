# NAMECHECK: RECLAMATION-H2 (exile, not destruction)

Worker: RECLAMATION-H2 worker (non-ledger task; claim minting paused).
Lane: docs/lab/research-lead/overnight-20260928/reclamation_h2/

## Step 0: Toolchain guard (recorded at lane startup)

- safebin at $HOME/safebin; PATH exported to $HOME/safebin for every
  build/run command.
- `which python3` and `which python` return nothing under that PATH
  (verified 2026-10-03 at lane startup; /usr/bin/python3 exists
  outside the safebin PATH and is never invoked).
- znc resolves inside safebin as the pinned compiler
  (znc 2026.07.0-dev (edition 2026)); build will cmp against
  src/tools/toolchain/znc_linux_x86_64_abed8aa1 (byte-identical
  check before the prereg commit).
- Shell use limited to: mkdir, znc invocation, binary execution,
  sha256sum, cmp, git ops, file reads/writes. No forbidden executable
  invoked. No PROCESS-FAIL condition triggered.
- Git writes via /usr/bin/git directly (safebin git symlink EPERM
  lesson, 2026-10-03); explicit pathspecs; no git reset; local only,
  never pushed.
- grep audit planned on the new code: no negated-conjunction while
  conditions (`grep -n 'while.*!('`); if-nesting at most 3; u8-backed
  cells with put32/ig helpers only; output via one preallocated
  buffer plus a single _zag_raw_syscall write.

## Conventions carried from the parent lanes

- Pure Zag for all scientific computation.
- Prereg committed alone before implementation (strict commit order);
  this prereg freezes all predicted values and kill bars.
- 3/3 byte-identical runs (sha256 equal) required; determinism bar is
  VOID-grade.
- Frozen kill bars are never weakened or reinterpreted after results.
- Build on LIVENESS-SIGNAL substrate; do not redesign the mechanism.
  New code: the cold tier (base 2752, 64 x 20 bytes), exile_victim,
  cold_lookup, the recovery path (mem_read_recov, test_A_recov), the
  drop-path exile, policy 0/1 branches (verbatim from
  EVICTION-POLICY-COMPARE) and policy 4 branch (verbatim from
  PINNING-RECLAMATION) for baseline reproduction, and the EXH2-OVF
  overflow driver (mode 2, w=51).
- Anchor conditions reproduce the frozen tables of all six baseline
  policies (FIFO, PART, PIN, PIN-LRU, PIN-CONSENT, PIN-LIVENESS) on
  the exile substrate; any drift is VOID.
- The discriminating rows are policy 6 (LRU) on the exile substrate:
  hot collapse bit-for-bit the frozen liveness rows (K6),
  recoverable retention 100 (K7), exact retrieval-cost ledger (K8),
  empty ledger under reread (K9), and the overflow recursion test
  (K10: cold_drop=74, retR=0).
