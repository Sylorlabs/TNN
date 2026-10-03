# NAMECHECK: BELIEF-PROVENANCE 7 (d_self dynamics, bar meta-parameters, per-belief bars)

Lane: `docs/lab/research-lead/overnight-20260928/belief_provenance_7/`
Worker: BELIEF-PROVENANCE-7 subagent, 2026-10-03.
Parent: overnight priority 9, belief reasoning from
provenance/evidence. Experiment BP-7: the remaining
BP-6 open dynamics (d_self long trajectories, bar
meta-parameter sensitivity, per-belief bars). All 7
falsifiable predictions (FP1-FP7) stay sealed; this
lane does not re-open them. Non-ledger task; nothing
minted.

## Step 0: toolchain guard (recorded before any implementation)

- Safebin: `~/safebin` provisioned with the 36 allowed
  tools. `export PATH="$HOME/safebin"` held for the whole
  session.
- `which python3` returns NOTHING under the safebin PATH.
- `which python` returns NOTHING under the safebin PATH.
- znc: pinned toolchain
  `~/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1`
  (builds invoked by absolute path; verified present
  2026-10-03).
- Shell used only for: znc invocation, binary execution,
  git ops, file movement, sha256 checks. All scientific
  computation in pure Zag.
- No pre-prereg exploratory probes were needed: all
  predicted numbers are hand-derived from frozen forms
  (BP-4 R3-prime, BP-6 BA arm) plus block behaviors
  already probe-measured in BP-6 (/tmp/bp6probe notes
  in BP-6 NAMECHECK).
- Git discipline: explicit pathspecs only; commits local,
  never push; never `git reset`; never amend shared
  history; never modify other lanes. This worker touches
  only
  `docs/lab/research-lead/overnight-20260928/belief_provenance_7/`.
  If git writes fail with EPERM through the safebin
  symlink, retry via `/usr/bin/git` directly (per
  AGENTS.md lesson 2026-10-03); on index.lock
  contention, retry with sleep backoff, never remove the
  lock.
- Zag pitfalls honored: u8-backed belief state with
  direct index access (no `as *i32` + slice construction
  in functions); output through the frozen block's
  existing emit/e64 helpers; no reliance on `.len` of
  casts; `if` nesting at most 3; no `!(A && B)` in while
  conditions (De Morgan form); `[]u8 as *u8` never used.
- No em/en dashes in any lane file (byte-verified with
  grep before each commit).
- Frozen block reuse: `xf_block.zag` (the patched
  XHIER-COUNTMAP-FIX block) is concatenated VERBATIM as
  the base of `bp7_full.zag`; its SHA-256 is recorded in
  the prereg and re-verified before and after the build:
  172a2e7dbbaa4e60d662331965887327350068e0c13f25e438260ad08313c12a
- Belief layer reuse: BP-6's `bp6_learner.zag` is copied
  VERBATIM to `bp7_learner.zag` (hash re-verified):
  2de20f5a0ff87bc45140a161548b613b008e9c2adabf4da3fdda6d6d46040c5e
- R3-prime reuse: BP-4's `bp4_rules.zag` is reused
  VERBATIM in the build (hash re-verified):
  7392299309082836bf376bb445492ef8d9fd75b3d857ad425b8ca74d7399e4d9
  (exactly one function, bp4_disconf_learn; frozen FP4
  code, not new machinery).
- New learner machinery this lane: NONE (disclosed in
  PREREG Section 1). bp7_bar_param and per-belief bars
  (pb array, bp7_select_pbar) are driver-side
  experimental code, not belief-layer changes; R7 and
  bp2_bar_after stay frozen. Everything else new is
  test-harness code in bp7_driver.zag (world builders,
  bp7_absorb, bp7_kill_self_prov, commitment
  bookkeeping, in-driver bars).

## Step 1: prereg commit (this commit)

- PREREG.md written and frozen BEFORE any implementation
  file exists in this lane. This NAMECHECK.md Step 0/1
  recorded.
- Commit contains ONLY: PREREG.md, NAMECHECK.md (this
  file).
- Implementation (bp7_learner.zag, bp7_driver.zag,
  bp7_full.zag, runs, REPORT.md) comes in a LATER commit,
  strictly after this one.

## Step 2: implementation (pending)

## Step 3: runs + REPORT.md (pending)
