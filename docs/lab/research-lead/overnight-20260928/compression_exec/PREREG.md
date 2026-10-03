# PREREG: E10.1 TRIAL-UNIFY (compression_exec)

**Status:** PREREG-FROZEN. Frozen before any implementation artifact
exists. No unified source, build, or run may precede the commit of
this file (see section 7).

**Date:** 2026-10-03. Lane:
`docs/lab/research-lead/overnight-20260928/compression_exec/`

**Grounding:** FRONTIER-AUDIT proposal E10.1 TRIAL-UNIFY
(frontier_audit/FRONTIER_AUDIT.md section 3, PRIORITY 10), grounded in
compression_audit/COMPRESSION_AUDIT.md section 3, Rank 1: "Trial
4-phase loop -> generic candidate-source iterator." The audit records
that the `assemble -> t2_try_verify -> promote_graph` triple repeats 4
times verbatim inside the 81-line t2_trial, and that the search ORDER
(chains before sums before counts before single-hops) is hardcoded
researcher-owned control flow.

## 1. Hypothesis

Rewriting t2_trial's four phases as ONE generic candidate-source
iterator (a phase table of (gather, assemble) pairs driven by a single
loop) strictly compresses the trial/search region with ZERO behavior
change: one general mechanism subsumes the four hardcoded phase
bodies. A compression PASS proves the audit's highest-ratio candidate
is real and gives the template for Ranks 2-8. A FAIL (behavior changes
or lines do not shrink) falsifies the candidate honestly.

## 2. Frozen references (hashes verified at extraction)

- Frozen TNN-2 base: `tnn2.zag` from commit f4de7ff46,
  SHA-256 `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`
  (1591 lines). NEVER edited in this lane.
- Freeze shim driver: `shim_driver2.zag` from commit 23c2c0206 (part
  of freeze_shim2.zag, SHA-256
  `33795c19c9f7ecd8e4c0c9a180293bf577b53ba7aae6f6a5557c972fe372ace8`).
  Zero-cognition transport per SHIM_REPORT.md; concatenated verbatim
  after the base for both arms (pre = frozen base + driver,
  post = unified base + driver). The driver file is identical in both
  arms (sha256-checked by the build script).
- FW1-FW9 sealed worlds: 16 world files from commit 396895595
  (`freeze_worlds_v2/worlds/`). Used as a no-regression battery ONLY
  (blind runs, byte-compare outputs; no tuning to world content).

## 3. Design (fixed before implementation)

- New file `tnn2_unify.zag`: byte-copy of the frozen base EXCEPT the
  t2_trial region (plus a marked delta note at the single edit
  site). The four phase bodies become entries in a phase table:
  each entry is a (kind, gather inputs, assemble selector, ablation
  gate) row; ONE loop walks the table and performs
  gather -> assemble -> t2_try_verify -> promote_graph per entry.
- The default phase order in the table is chains k=2..4, sums,
  counts, single-hops: identical to the frozen order.
- The dc/di ablation gates move from code to per-entry gate
  attributes (chains gated on dc==0, counts on di==0), as the audit
  requires.
- `mp_run` is untouched (still unpacks flags, calls t2_trial).
- No new node types, no new edge types, no new modes, no bridges, no
  handlers. The trial-stats accounting (tried/rejected packed into
  header field 16) is preserved exactly.

## 4. Kill bars (frozen; all must pass for BUILD-PASS)

- **K1 (no regression):** FW1-FW9 battery (all 16 sealed world
  files, run via the freeze shim with fresh state per world) yields
  9/9 world verdicts IDENTICAL pre/post: the shim stdout for each
  world must be byte-identical between the frozen-base shim and the
  unified-base shim. Any differing byte = FAIL.
- **K2 (compression real):** cognition lines in the trial/search
  region strictly reduced: count lines from `fn t2_trial` through the
  end of the four-phase body (exclusive of unchanged helpers) in the
  frozen base vs the unified file. Unified must have >= 20 percent
  fewer lines in that region. Measured by `wc -l` on the extracted
  regions recorded in REPORT.md.
- **K3 (no new machinery):** zero new modes/bridges/handlers: the
  unified file introduces no mode flags, no subsystem bridges, no new
  handler functions relative to the frozen base. Verified by a
  name-diff of top-level function definitions plus a grep audit for
  mode-like branching on new globals; recorded in REPORT.md.
- **K4 (determinism):** 3/3 byte-identical: three consecutive builds
  of the unified shim produce byte-identical binaries
  (sha256sum equal), and three consecutive runs of the FW battery on
  the unified shim produce byte-identical concatenated outputs.
- **K5 (order is data):** white-box check: in the unified file the
  phase ORDER exists only in the phase table. Demonstrated by a
  table-only edit (swap two phase rows, no code change) that changes
  which candidate family wins on a probe query. The probe is a
  synthetic world (not FW-sealed), built in pure Zag, and the
  behavior delta must be attributable to the table edit alone.

## 5. Verdict rules

- BUILD-PASS iff K1..K5 all pass as frozen above.
- BUILD-FAIL if any kill bar fails. A behavior difference (K1) is a
  FAIL of the compression candidate, not a signal to tune the unified
  code toward the worlds: no world-content inspection may drive an
  implementation change.
- VOID conditions: frozen-base SHA mismatch at extraction; driver
  SHA mismatch between arms; any forbidden-executable invocation
  (PROCESS-FAIL per governance); prereg commit not strictly before
  implementation commit.

## 6. Predicted information gain

MEDIUM-HIGH (per E10.1): the compression audit is analysis-only; this
is the first EXECUTED compression. PASS proves Rank 1 is real and
gives the template for Ranks 2-8. FAIL falsifies the candidate
honestly. Either way the #10 backlog gets its first executed datum.

## 7. Commit-order self-check

- This PREREG.md and NAMECHECK.md are committed alone in the first
  lane commit. `git log` must show the prereg commit strictly before
  any commit containing implementation artifacts (unified source,
  builds, runs, REPORT.md). The worker records the prereg commit
  hash here after committing: PREREG_COMMIT=________ (filled at
  commit time in the commit message; REPORT.md re-verifies ordering).
