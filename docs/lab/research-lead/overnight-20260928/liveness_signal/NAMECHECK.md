# NAMECHECK: LIVENESS-SIGNAL

Worker: LIVENESS-SIGNAL worker (non-ledger task; claim minting paused).
Lane: docs/lab/research-lead/overnight-20260928/liveness_signal/

## Step 0: Toolchain guard (recorded at lane startup)

- safebin at $HOME/safebin; PATH exported to $HOME/safebin for every
  build/run command.
- `which python3` and `which python` return nothing under that PATH
  (verified 2026-10-03 at lane startup).
- znc resolves inside safebin as the pinned compiler
  (znc 2026.07.0-dev (edition 2026)); build will cmp against
  src/tools/toolchain/znc_linux_x86_64_abed8aa1 (verified
  byte-identical 2026-10-03 before the prereg commit).
- Shell use limited to: mkdir, znc invocation, binary execution,
  sha256sum, cmp, git ops, file reads/writes. No forbidden executable
  invoked. No PROCESS-FAIL condition triggered.
- Git writes via /usr/bin/git directly (safebin git symlink EPERM
  lesson, 2026-10-03); explicit pathspecs; no git reset; local only,
  never pushed.
- grep audit planned on the new code: no negated-conjunction while
  conditions; if-nesting at most 3.

## Conventions carried from the parent lanes

- Pure Zag for all scientific computation.
- Prereg committed alone before implementation (strict commit order);
  this prereg freezes all predicted values and kill bars.
- 3/3 byte-identical runs (sha256 equal) required; determinism bar is
  VOID-grade.
- Frozen kill bars are never weakened or reinterpreted after results.
- Build on CONSENT-MULTIOWNER; do not redesign the substrate. The only
  new code is the policy-6 reclamation rule plus the LIVR-M2 re-read
  driver.
- Anchor conditions reproduce the full frozen CONSENT-MULTIOWNER table
  (policies 3 and 5, all 9 rows); any drift is VOID.
