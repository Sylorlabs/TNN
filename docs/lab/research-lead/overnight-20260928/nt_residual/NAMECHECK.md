# NAMECHECK: NT-RESIDUAL

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

- Lane: `docs/lab/research-lead/overnight-20260928/nt_residual/`
- Task: the residual case from NT-NONLOCAL's recommended follow-up
  #1: a rare-but-useful link (160->161->162) that is NEVER a
  revision target. Single arm R6 (K=6, LAST). Learner is the NTNL
  D5 learner verbatim; only the workload gains two keys and one
  per-pass probe (q(160) vs 162). Tests: does D5 protect the
  residual link (predicted NO), does it still protect 148 in the
  same run (dissociation), and is any learner-available signal
  available that could predict the residual link's usefulness
  (predicted: fundamentally impossible in this workload).
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

- PREREG.md: frozen kill bars K1-K7, hand-derived Section 5
  predictions (single arm R6), verdict mapping (Section 8).
  Predicted verdict: RESIDUAL-CONFIRMED.
- Prereg freeze: commit `8dc808fb4e839c3f3404b7f7304986db2345d1cc`
  on `tnn-native-lab` (PREREG.md + NAMECHECK.md only), strictly
  before implementation.
- Implementation: `ntres_full.zag` (NTNL D5 learner verbatim;
  workload adds RESIDUAL keys 160/161 + q(160) probe; layout
  extended to subjs 100..165). Build `znc ntres_full.zag -o
  ntres_bin` exit 0 (benign zagd warning). 3/3 runs
  byte-identical, exit 0, zero stderr. Digests: run
  `6be7bc39438cf53b2980a4605deb4ab1b1f3aee4505dbae8f028163532ac2bf4`,
  bin
  `c07bb48e70ba568190ebe3936d483452cc1558cd678d9eabee0b28cdbcfd4e03`,
  src
  `25f935daa65c269475cec795c5a8bc10b5e57c9f0a4ab85fa52f7cbae5d28a2e`.
- Results: K1-K7 all 1, VERDICT=RESIDUAL-CONFIRMED. REPORT.md
  written.
- Commits local only, explicit pathspecs, never pushed.
  Non-ledger task (claim minting paused).
