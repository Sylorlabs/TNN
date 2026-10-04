# NAMECHECK: NT-CAPACITY-SWEEP

## Step 0: Toolchain guard (mandatory, Micah's 2026-09-30 ruling)

- Worker PATH: `$HOME/safebin` only (52 allowed tools: coreutils, git,
  pinned znc). Activated via `export PATH="$HOME/safebin"` at startup.
- `which python3` returns nothing under the worker PATH.
- `which python` returns nothing under the worker PATH.
- All computational research operations in pure Zag (znc). Shell only:
  invoke znc, run binaries, git ops, move/copy files, cmp/sha256.
- If a forbidden executable is invoked, this lane's wave is
  automatically PROCESS-FAIL and any result stays exploratory pending
  a clean re-freeze. Zero forbidden invocations to record.

## Lane identity

- Lane: `docs/lab/research-lead/overnight-20260928/nt_capacity_sweep/`
- Task: capacity sweep (CAP=20/22/24) of the NT-TEACHASSOC world to
  quantify the D6 assoc pin's opportunity-cost curve. Learner and
  oracles are NT-TEACHASSOC verbatim except capacity
  parameterization (`cl_new(ns)` allocates ns-relative layout).
  Three arms in one binary: R6-CAP20 (predicted COST-CONFIRMED:
  rescue holds, A-link 118 displaced, u=3, forget=1, nevict=30),
  R6-CAP22 (predicted REPRODUCED: byte-exact NT-TEACHASSOC
  regression), R6-CAP24 (predicted SLACK-CONFIRMED: rescue holds,
  zero opportunity cost, nevict=10, FP cost persists).
  Overall predicted verdict: CURVE-CONFIRMED.
- Non-ledger task (claim minting paused).

## Commit-order self-check

- Prereg commit (PREREG.md + NAMECHECK.md only) must strictly precede
  the implementation commit. Verified via `git log` before writing
  REPORT.md. No implementation file exists at prereg time.
- Commits go to `tnn-native-lab` (not a side branch) with explicit
  pathspecs, via git plumbing (separate index file, read-tree /
  write-tree / commit-tree / update-ref with old-value check),
  because the shared working tree is on a side branch with other
  workers' staged changes. The shared index is never touched.

## Provenance notes (filled as the lane proceeds)

- PREREG.md: frozen per-arm kill bars (S1-S5, R1-R7, T1-T5),
  hand-derived Section 5 traces for CAP=20 and CAP=24, CAP=22
  regression numbers from NT-TEACHASSOC (amended), verdict mapping
  (Section 8). Predicted verdict: CURVE-CONFIRMED.
- Prereg freeze: commit `<hash>` on `tnn-native-lab`
  (PREREG.md + NAMECHECK.md only), strictly before implementation.
- Implementation: `ntsweep_full.zag` (NT-TEACHASSOC source verbatim
  + CAP parameterization + 3-arm main + per-arm bars).
- Build `znc ntsweep_full.zag -o ntsweep_bin` under safebin-only
  PATH. 3/3 runs byte-identical, exit 0, zero stderr.
- Results: ARM20 COST-CONFIRMED (S1-S5 all 1: nevict=30, phev=1,
  118 displaced, u=3, forget=1, avail160=4, FP 50%);
  ARM22 REPRODUCED (R1-R7 all 1: byte-exact NT-TEACHASSOC numbers);
  ARM24 SLACK-CONFIRMED (T1-T5 all 1: nevict=10, u=4, forget=0,
  avail160=4, bprobe=2, FP 50%). Overall: CURVE-CONFIRMED.
  First-run exact match on all frozen hand-derived numbers.
- Digests: run
  `614e046b9d906a4e32ead8b6a05ce8225e6f03abfeae15fa566d4426eecda6a6`,
  bin
  `a25cb20ce53113c62c64ded35a621a1ed6671679cd4f4e25cbb096d245908415`,
  src
  `80cf0e57c6752c0fd9797aecff54d8a9834b51e52ac0f9ef7f76bae78762528a`.
- Commits local only, explicit pathspecs, never pushed.
  Non-ledger task (claim minting paused).
