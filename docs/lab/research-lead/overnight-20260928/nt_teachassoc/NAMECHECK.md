# NAMECHECK: NT-TEACHASSOC

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

- Lane: `docs/lab/research-lead/overnight-20260928/nt_teachassoc/`
- Task: the flagged follow-up from NT-RESIDUAL: test a teaching-stream
  association signal -- protect keys taught adjacent (in time) to
  observed query starts -- in a world where the teaching stream
  carries the dependence. New rule D6 (association pin, W=20,
  same-subject, tick-stamped teach/query events) added to the
  NT-RESIDUAL D5 learner; workload gains an exploratory query episode
  (q(160),q(161),q(170),q(171) post-phase-1) and a decoy chain
  (170,1)->171,(171,1)->172 taught with identical stream-adjacency
  but never probed (false-positive control). CAP=22 (25 keys, 1.14x).
  Single arm R6 (K=6). Tests: (a) D6 rescues the residual chain
  (avail160=4, evh(160)=evh(161)=0); (b) learner-availability (by
  construction); (c) FP rate via the decoy (predicted 2/4 useless);
  (d) D5 still covers 148 in the same run (dissociation).
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

- PREREG.md: frozen kill bars K1-K7, hand-derived Section 5 trace
  (single arm R6), verdict mapping (Section 8). Predicted verdict:
  ASSOC-CONFIRMED.
- Prereg freeze: commit `4aa6b2680f1aa725f94b2c453a5148ea0ba6d57c`
  on `tnn-native-lab` (PREREG.md + NAMECHECK.md only), strictly
  before implementation.
- AMENDMENT 1 (2026-10-03): transparent correction of a
  hand-derivation error in PREREG Section 5 (passes 3-6 each have
  4 evictions, not 3: the first restore evicts 144, making its
  later teach a fourth restore). Corrected: nevict=22 (was 18);
  EVHIST 140=5,141=6,143=6,144=5 (was 140=5,141=6,143=4,144=3).
  Rules, workload, protocol, and all other frozen numbers
  unchanged; K5 remains exact (not weakened). Original numbers
  preserved in git history for audit. Amendment committed to
  `tnn-native-lab` as `<hash>` before any verdict was recorded;
  the implementation's K5 check was updated to the corrected
  bar and the binary rebuilt + rerun 3x after the amendment.
  Amendment commit: `5351f79ecc053006fe4d38f62f5edbdb6bd86a97`.
- Implementation: `ntteach_full.zag` (NT-RESIDUAL D5 learner verbatim
  + D6; oracles add exploratory episode + decoy chain; CAP=22).
- Build `znc ntteach_full.zag -o ntteach_bin` exit 0 (benign
  zagd-unavailable warning + 4 benign A0102 ignored-return warnings
  on the exploratory h_query calls, whose results are intentionally
  discarded). 3/3 runs byte-identical, exit 0, zero stderr.
- Results: K1-K7 all 1, VERDICT=ASSOC-CONFIRMED.
- Digests: run
  `aec8cfc5ef734399c7e326d136bf35545a903cdc9e1bc122a5bccfa3939acfc1`,
  bin
  `63eb84da13666916ee9f3bde9ce666c39d2313966d5d14f77ba1d23bb8e2cdae`,
  src
  `57b7a91f7be1d0a0f33d3c8a950e150cfe01195a40486d2a0bcdf470113bb9a2`.
- Amendment 1: see above. The implementation commit below contains
  the amended PREREG.md + NAMECHECK.md (already frozen as
  5351f79e), ntteach_full.zag, ntteach_bin, 3 run logs, REPORT.md.
- Commits local only, explicit pathspecs, never pushed.
  Non-ledger task (claim minting paused).
