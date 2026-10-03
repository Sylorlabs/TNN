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

## Step 2: implementation (pending)

## Step 3: runs + REPORT.md (pending)
