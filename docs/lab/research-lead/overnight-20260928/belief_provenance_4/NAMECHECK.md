# NAMECHECK: BELIEF-PROVENANCE 4 (FP1 + FP4 + FP5)

Lane: `docs/lab/research-lead/overnight-20260928/belief_provenance_4/`
Worker: BELIEF-PROVENANCE-4 subagent, 2026-10-03.
Parent: overnight priority 9, belief reasoning from
provenance/evidence. Experiment BP-4: test the three
remaining falsifiable predictions of the BELIEF-PROVENANCE
DESIGN.md Section 10: FP1 (graded flip point), FP4 (learned
source discount), FP5 (independence discount). This
completes all 7 falsifiable predictions (FP2/FP3 sealed by
BP-2, FP6/FP7 sealed by BP-3). Non-ledger task; nothing
minted.

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
  (builds invoked by absolute path; verified present
  2026-10-03).
- Shell used only for: znc invocation, binary execution, git
  ops, file movement, sha256 checks. All scientific
  computation in pure Zag.
- Git discipline: explicit pathspecs only; commits local,
  never push; never `git reset`; never amend shared history;
  never modify other lanes. This worker touches only
  `docs/lab/research-lead/overnight-20260928/belief_provenance_4/`.
  If git writes fail with EPERM through the safebin symlink,
  retry via `/usr/bin/git` directly (per AGENTS.md lesson
  2026-10-03); on index.lock contention, retry with sleep
  backoff, never remove the lock.
- Zag pitfalls honored: u8-backed belief state with direct
  index access (no `as *i32` + slice construction in
  functions); output through the frozen block's existing
  emit/e64 helpers (already validated 3/3 byte-identical by
  the XF, BP-2 and BP-3 lanes); no reliance on `.len` of
  casts; `if` nesting at most 3; no `!(A && B)` in while
  conditions (De Morgan form); `[]u8 as *u8` never used.
- No em/en dashes in any lane file (byte-verified with grep
  before each commit).
- Frozen block reuse: `xf_block.zag` (the patched
  XHIER-COUNTMAP-FIX block, verdict XHIER-COUNTMAP-FIX-PASS)
  is concatenated VERBATIM as the base of `bp4_full.zag`;
  its SHA-256 is recorded in the prereg and re-verified
  before and after the build:
  172a2e7dbbaa4e60d662331965887327350068e0c13f25e438260ad08313c12a
- Belief layer reuse: BP-3's `bp3_learner.zag` is copied
  VERBATIM to `bp4_learner.zag` (hash re-verified):
  2de20f5a0ff87bc45140a161548b613b008e9c2adabf4da3fdda6d6d46040c5e
- New learner machinery this lane (disclosed in PREREG
  Section 1): exactly one function, `bp4_disconf_learn`
  (the FP4 d_self learning rule), in `bp4_rules.zag`.
  Everything else new is test-harness code in
  `bp4_driver.zag` (world replay, source-tag scripting,
  experience sequences, in-driver bars). Build on BP-3, no
  redesign of the belief layer.

## Step 1: prereg commit (this commit)

- PREREG.md written and frozen BEFORE any implementation file
  exists in this lane. This NAMECHECK.md Step 0/1 recorded.
- Commit contains ONLY: PREREG.md, NAMECHECK.md (this file).
- Implementation (bp4_learner.zag, bp4_rules.zag,
  bp4_driver.zag, bp4_full.zag, runs, REPORT.md) comes in a
  LATER commit, strictly after this one.

## Step 2: implementation (pending)

## Step 3: runs + REPORT.md (pending)
