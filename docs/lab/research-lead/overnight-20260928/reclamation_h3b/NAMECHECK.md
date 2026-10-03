# NAMECHECK: RECLAMATION-H3B (fresh K20 derivation, unchanged mechanism)

Worker: RECLAMATION-H3B worker (non-ledger task; claim minting paused).
Lane: docs/lab/research-lead/overnight-20260928/reclamation_h3b/

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
  the mechanism; shell used only for binary execution, sha256sum,
  cmp, git ops, file reads/writes). No forbidden executable invoked.
  No PROCESS-FAIL condition triggered.
- Git writes via /usr/bin/git directly (safebin git symlink EPERM
  lesson, 2026-10-03); explicit pathspecs on every commit; no git
  reset; local only, never pushed.
- Commit order: PREREG.md + NAMECHECK.md commit strictly first,
  alone. No implementation in this lane: the mechanism is the frozen
  H3 binary (unpin_h3_bin, sha256
  a9759f7c4bd71b944a6e0e2da69264c6f2f192ba4edef4835c8ee9fdf747223c),
  copied byte-identical from reclamation_h3 into this lane and
  verified by sha256 before the prereg commit. The source copy
  unpin_h3.zag (sha256
  14ad232b4967f3e06725905577aef219136778bbb1c1d552cf4b90835082d32e)
  is held for provenance and is NOT modified.
- Note: the binary's in-band K1..K22 self-check lines and VERDICT
  line encode the H3 frozen values (including the superseded
  post=7/ret=20 for K20), so they will print K20 FAIL and
  VERDICT=FAIL even when the corrected H3B bars pass. The governing
  verdict is the external worker check of the COND columns against
  the H3B PREREG.md; this reading is frozen in the prereg.

## Conventions carried from the parent lanes

- Prereg freezes all predicted values and kill bars before any run;
  no bar may be weakened or reinterpreted after results.
- 3/3 byte-identical runs (sha256 equal) required; determinism bar is
  VOID-grade.
- H3B delta is the K20 derivation only: UNPINSTALE-A20 ret==17,
  post==6, rawA==19, ev==16, drop==0, cf==48, bacc==20. All other
  21 bars carried verbatim from the H3 prereg.
