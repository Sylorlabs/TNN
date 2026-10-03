# NAMECHECK: RECLAMATION-H3 (learner-issued unpin)

Worker: RECLAMATION-H3 worker (non-ledger task; claim minting paused).
Lane: docs/lab/research-lead/overnight-20260928/reclamation_h3/

## Step 0: Toolchain guard (recorded at lane startup)

- safebin at $HOME/safebin; PATH exported to $HOME/safebin for every
  build and run command.
- `which python3` and `which python` return nothing under that PATH
  (verified 2026-10-03 at lane startup).
- znc resolves inside safebin as the pinned compiler
  (znc 2026.07.0-dev (edition 2026)); cmp against
  src/tools/toolchain/znc_linux_x86_64_abed8aa1: byte-identical
  (verified 2026-10-03 before the prereg commit).
- Pure Zag for all scientific computation (the frozen binary embodies
  the mechanism; shell used only for mkdir, znc invocation, binary
  execution, sha256sum, cmp, git ops, file reads/writes). No forbidden
  executable invoked. No PROCESS-FAIL condition triggered.
- Git writes via /usr/bin/git directly (safebin git symlink EPERM
  lesson, 2026-10-03); explicit pathspecs on every commit; no git
  reset; local only, never pushed.
- Commit order: PREREG.md + NAMECHECK.md commit strictly first, alone.
  Implementation (unpin_h3.zag), binary, runs, and REPORT.md only
  after. This prereg commit must strictly precede all of them.

## Conventions carried from the parent lanes

- Prereg freezes all predicted values and kill bars before any code is
  written; no bar may be weakened or reinterpreted after results.
- 3/3 byte-identical runs (sha256 equal) required; determinism bar is
  VOID-grade.
- Policies 0,1,3,4,5,6,7 and the full H1B 29-condition anchor protocol
  are carried verbatim so the H1B baseline reproduces exactly; new
  code is additive only (policy 8, policy 9 control, learner routines,
  trace/audit machinery).
- The znc defect workarounds from AGENTS.md apply to all new Zag code:
  u8-backed cells with put32/ig helpers; single-buffer output plus one
  _zag_raw_syscall write; if-nesting at most 3 with hoisted flags; no
  negated conjunctions in while conditions; no second-allocation
  number formatting.
