# NAMECHECK: BELIEF-PROVENANCE 2 (provenance-death + propagation)

Lane: `docs/lab/research-lead/overnight-20260928/belief_provenance_2/`
Worker: BELIEF-PROVENANCE-2 subagent, 2026-10-03.
Parent: overnight priority 9, belief reasoning from
provenance/evidence. Experiment BP-2: implement the
BELIEF-PROVENANCE DESIGN.md belief layer (records R1-R7) and
test FP2 (provenance-death) and FP3 (propagation) as sealed
arms replaying the frozen XHIER-COUNTMAP-FIX world, plus the
design's kill criterion (R7 vs plain liveness-gating).
Non-ledger task; nothing minted.

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
  `docs/lab/research-lead/overnight-20260928/belief_provenance_2/`.
  If git writes fail with EPERM through the safebin symlink,
  retry via `/usr/bin/git` directly (per AGENTS.md lesson
  2026-10-03).
- Zag pitfalls honored: u8-backed belief state with direct
  index access (no `as *i32` + slice construction in
  functions); output through the frozen block's existing
  emit/e64 helpers (already validated 3/3 byte-identical by
  the XF lane); no reliance on `.len` of casts; `if` nesting
  at most 3; no `!(A && B)` in while conditions (De Morgan
  form); `[]u8 as *u8` never used.
- No em/en dashes in any lane file (byte-verified with grep
  before each commit).
- Frozen block reuse: `xf_block.zag` (the patched
  XHIER-COUNTMAP-FIX block, verdict XHIER-COUNTMAP-FIX-PASS)
  is concatenated VERBATIM as the base of `bp2_full.zag`;
  its SHA-256 is recorded in the prereg and re-verified
  before and after the build. The belief layer
  (`bp2_learner.zag`) and the battery driver
  (`bp2_driver.zag`) are the only new code.

## Step 1: prereg commit (this commit)

- PREREG.md written and frozen BEFORE any implementation file
  exists in this lane. This NAMECHECK.md Step 0/1 recorded.
- Commit contains ONLY: PREREG.md, NAMECHECK.md (this file).
- Implementation (bp2_learner.zag, bp2_driver.zag) comes in a
  LATER commit, strictly after this one.

## Step 2: implementation (done, commit follows prereg commit 5912fb0eb)

- Files: bp2_learner.zag (249 lines: belief table, R1/R2/R3/
  R4/R5/R6/R7, eff(), b_retire with kind-3 reason edges,
  lg() liveness-gating baseline, bp2_kill_one_prov,
  bp2_census, bp2_bar_after), bp2_driver.zag (314 lines:
  bp2_build world replay + W2 FP2 arm + W3 FP3 arm +
  in-driver bars PC/K-FP2/K-FP3).
- Built: `cat ../xhier_countmap_fix/xf_block.zag
  bp2_learner.zag bp2_driver.zag > bp2_full.zag`; pinned
  znc by absolute path, build exit 0 -> bp2_bin (372750
  bytes; log: bp2_compile.txt; 199 A0102 warnings, all the
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
  9318027e43ecdabf4eb4ce11e87f27bcb475b50324c3ae8c544a63f1096c65a8
  for bp2_run1/2/3.txt (K-DET PASS).
- In-driver bars: 7/7 preconditions PASS; FP2: G1/G2/G3
  (75,37,9 graded), D1 (kind-3 reason-2 on MAP_V3 and
  MAP_Z2), D2 (persist -3,-3,-3), D3 (lg=299 vs R7=-3),
  C1 (EXEC 4,4,4,-2 vs R7 Z2,Z2,-3,-3,-3) all PASS;
  FP3: S1 (120/100, R7=Z2), F1 (flip to Z3 at first
  tombstone), F2 (census 5/5, no k3 on Z2), F3
  (lg=Z2 vs R7=Z3) all PASS. BP2-SUMMARY 18/18.
- REPORT.md written with verdict BP-2-PASS.
- Committed with explicit pathspecs, local only, never
  pushed.
- Ledger: non-ledger task, nothing minted; ledger file
  untouched.
