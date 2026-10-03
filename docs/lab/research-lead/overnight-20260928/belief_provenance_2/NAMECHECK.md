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

## Step 2: implementation (pending)

## Step 3: runs + REPORT.md (pending)
