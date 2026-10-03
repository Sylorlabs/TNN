# NAMECHECK: BELIEF-PROVENANCE 3 (domain-blindness + abstention)

Lane: `docs/lab/research-lead/overnight-20260928/belief_provenance_3/`
Worker: BELIEF-PROVENANCE-3 subagent, 2026-10-03.
Parent: overnight priority 9, belief reasoning from
provenance/evidence. Experiment BP-3: test the two remaining
falsifiable predictions of the BELIEF-PROVENANCE DESIGN.md,
FP6 (domain-blindness permutation) and FP7 (abstention),
plus the "does abstention help" policy comparison, as
sealed arms on the frozen BP-2 belief machinery. Non-ledger
task; nothing minted.

## Step 0: toolchain guard (recorded before any implementation)

- Safebin: `~/safebin` provisioned with the 36 allowed tools
  (awk basename bash cat chmod cmp comm cp cut date diff
  dirname echo file find git git-receive-pack git-upload-pack
  grep head join ln ls mkdir mktemp mv nl od paste printf rm
  sed sh sha256sum sleep sort stat strings tail tee timeout
  touch tr uname uniq wc which xargs znc).
  `export PATH="$HOME/safebin"` held for the whole session.
- `which python3` returns NOTHING under the safebin PATH.
- `which python` returns NOTHING under the safebin PATH.
- znc resolves via the safebin symlink to the pinned toolchain
  `~/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1`
  (builds invoked by absolute path).
- Shell used only for: znc invocation, binary execution, git
  ops, file movement, sha256 checks. All scientific
  computation in pure Zag.
- Git discipline: explicit pathspecs only; commits local,
  never push; never `git reset`; never amend shared history;
  never modify other lanes. This worker touches only
  `docs/lab/research-lead/overnight-20260928/belief_provenance_3/`.
  If git writes fail with EPERM through the safebin symlink,
  retry via `/usr/bin/git` directly (per AGENTS.md lesson
  2026-10-03).
- Zag pitfalls honored: u8-backed belief state with direct
  index access (no `as *i32` + slice construction in
  functions); output through the frozen block's existing
  emit/e64 helpers (already validated 3/3 byte-identical by
  the XF and BP-2 lanes); no reliance on `.len` of casts;
  `if` nesting at most 3; no `!(A && B)` in while
  conditions (De Morgan form); `[]u8 as *u8` never used.
- No em/en dashes in any lane file (byte-verified with grep
  before each commit).
- Frozen block reuse: `xf_block.zag` (the patched
  XHIER-COUNTMAP-FIX block, verdict XHIER-COUNTMAP-FIX-PASS)
  is concatenated VERBATIM as the base of `bp3_full.zag`;
  its SHA-256 is recorded in the prereg and re-verified
  before and after the build.
- Belief layer reuse: BP-2's `bp2_learner.zag` is copied
  VERBATIM to `bp3_learner.zag` (hash re-verified); the only
  new code is the battery driver `bp3_driver.zag` (permuted
  world builds, FP6/FP7 arms, in-driver bars, the forced-
  argmax baseline policy). Build on BP-2, no redesign.

## Step 1: prereg commit (this commit)

- PREREG.md written and frozen BEFORE any implementation file
  exists in this lane. This NAMECHECK.md Step 0/1 recorded.
- Commit contains ONLY: PREREG.md, NAMECHECK.md (this file).
- Implementation (bp3_learner.zag, bp3_driver.zag) comes in a
  LATER commit, strictly after this one.

## Step 2: implementation (done)

- Files: bp3_learner.zag (verbatim copy of BP-2's
  bp2_learner.zag, SHA-256
  2de20f5a0ff87bc45140a161548b613b008e9c2adabf4da3fdda6d6d46040c5e
  on both), bp3_driver.zag (new: bp3_perm relabeling
  bijection, bp3_build parameterized world replay,
  bp3_force forced-argmax baseline policy, bp3_fp6_run
  step runner with snapshot/compare modes, bp3_degrade,
  FP6/FP7a/FP7b arms, in-driver bars).
- One driver bug found and fixed before the scored runs:
  bp3_fp6_run mode=1 compared pm=1/pm=2 traces against a
  fresh zeroed buffer instead of the pm=0 reference trace
  (K-FP6-TAB/TRC failed spuriously); fixed to pass the
  reference trace and to report table vs trace equality as
  separate bitmask bits. The fix aligns the driver with the
  frozen prereg; no bar or prediction was changed.
- Built: `cat ../xhier_countmap_fix/xf_block.zag
  bp3_learner.zag bp3_driver.zag > bp3_full.zag`; pinned
  znc by absolute path, build exit 0 -> bp3_bin (406001
  bytes; log: bp3_compile.txt; A0102 warnings are the
  benign ignored-return-value pattern pervasive in the
  frozen block itself).
- xf_block.zag SHA-256 re-verified before AND after the
  build: 172a2e7dbbaa4e60d662331965887327350068e0c13f25e438260ad08313c12a
  (unchanged; the patched XHIER-COUNTMAP-FIX block).
- No Python/C/JS/Rust invoked at any point. Safebin PATH
  held for the whole session. `which python3` /
  `which python` still empty at build and run.
- No em/en dashes in any lane file (byte-verified with
  grep).
- 0 new edge types (1/14/3 only), 0 new node types,
  0 modes, 0 bridges, 0 handlers (one-system accounting).

## Step 3: runs + REPORT.md (done)

- 3/3 runs byte-identical: sha256
  e1f5fb137a4b29b8d28d415ca5ac131afe806a7f7a22032c66a0018a262c6043
  for bp3_run1/2/3.txt (K-DET PASS).
- In-driver bars: 31/31 PASS. FP6: 9/9 PCs, K-FP6-VAL
  (pm=0 reproduces BP-2 values), K-FP6-IDX (node ids
  27/194/274/299 identical across identity/offset/
  reflection), K-FP6-TAB (8192-B bt + 1024-B hasb
  byte-identical at t0..t4), K-FP6-TRC (per-step belief
  trace identical). FP7a: 4/4 PCs, K-FP7-A1 (37/37/37/37),
  A2 (pair -3), A3 (singles -3/-3), A5 (empty/recordless
  -3), A4 (bt unchanged, no kind-3). FP7b: 4/4 PCs,
  K-FP7-B1 (37/9, R7 -3, forced 299), K-FP7-B3 (bar=30
  picks 299 pre-evidence), K-FP7-B2 (17/29, R7 -3),
  K-FP7-B0 (W7c setup 37/9, R7 -3), K-FP7-B4 (57/0,
  R7=299). BP3-SUMMARY 31/31.
- REPORT.md written with verdict BP-3-PASS.
- Committed with explicit pathspecs, local only, never
  pushed.
- Ledger: non-ledger task, nothing minted; ledger file
  untouched.
