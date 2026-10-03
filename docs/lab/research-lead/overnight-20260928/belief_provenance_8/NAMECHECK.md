# NAMECHECK: BELIEF-PROVENANCE 8 (multi-channel absorption, large/heterogeneous cycles)

Lane: `docs/lab/research-lead/overnight-20260928/belief_provenance_8/`
Worker: BELIEF-PROVENANCE-8 subagent, 2026-10-03.
Parent: overnight priority 9, belief reasoning from
provenance/evidence. Experiment BP-8: the two open
dynamics suggested by BP-7 (multi-channel absorption;
cycles larger than 5 with heterogeneous edges). All 7
falsifiable predictions (FP1-FP7) stay sealed; this
lane does not re-open them. Non-ledger task; nothing
minted.

## Step 0: toolchain guard (recorded before any implementation)

- Safebin: `~/safebin` (49 tools) active from session
  start. `export PATH="$HOME/safebin"` held for the
  whole session.
- `which python3` returns NOTHING under the safebin PATH.
- `which python` returns NOTHING under the safebin PATH.
- znc: safebin `znc` is a symlink to the pinned
  toolchain
  `~/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1`
  (identical SHA-256
  498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef;
  builds invoked by absolute path).
- Shell used only for: znc invocation, binary
  execution, git ops, file movement, sha256 checks.
  All scientific computation in pure Zag.
- Pre-prereg exploratory probes: three probe binaries
  in /tmp/bp8probe (ephemeral, NOT lane-committed),
  all pure Zag under safebin, measuring block
  behaviors the prereg depends on: P1/P2/P3 (match/
  contradict sequencing on graph-less facts), P6/P7
  (same on graph-licensed facts; P7 showed the
  contradict-then-match ret is 1 graph-licensed vs 0
  graph-less, so the ret is emitted not barred),
  P8 (absorb net 90/0/1), P5 (12-ring converge/
  fixpoint/raise), P4+P3b (heterogeneous ring: R6
  no-op ret 255 across type-1/type-3, weakening
  reabsorbed). No probe result changed a frozen
  rule; they fixed the prereg's block assumptions.
- Git discipline: explicit pathspecs only; commits
  local, never push; never `git reset`; never amend
  shared history; never modify other lanes. This
  worker touches only
  `docs/lab/research-lead/overnight-20260928/belief_provenance_8/`.
  If git writes fail with EPERM through the safebin
  symlink, retry via `/usr/bin/git` directly (per
  AGENTS.md lesson 2026-10-03); on index.lock
  contention, retry with sleep backoff, never remove
  the lock.
- Zag pitfalls honored: u8-backed belief state with
  direct index access (no `as *i32` + slice
  construction in functions); output through the
  frozen block's existing emit/e64 helpers; no
  reliance on `.len` of casts; `if` nesting at most
  3; no `!(A && B)` in while conditions (De Morgan
  form); `[]u8 as *u8` never used.
- No em/en dashes in any lane file (byte-verified
  with grep before each commit).
- Frozen block reuse: `xf_block.zag` (the patched
  XHIER-COUNTMAP-FIX block, extracted as lines
  1..2668 of BP-7's bp7_full.zag) is concatenated
  VERBATIM as the base of `bp8_full.zag`; its
  SHA-256 is recorded in the prereg and re-verified
  before and after the build:
  172a2e7dbbaa4e60d662331965887327350068e0c13f25e438260ad08313c12a
- Belief layer reuse: BP-7's `bp7_learner.zag` is
  copied VERBATIM to `bp8_learner.zag` (hash
  re-verified):
  2de20f5a0ff87bc45140a161548b613b008e9c2adabf4da3fdda6d6d46040c5e
- New learner machinery this lane: NONE (disclosed
  in PREREG Section 1). bp8_absorb (BP-7 absorb
  renamed, identical body) and bp8_allsup are
  driver-side test-harness code, not belief-layer
  changes; R6/R7 and bp2_bar_after stay frozen.
  0 new edge types, 0 new node types, 0 modes,
  0 bridges, 0 handlers (one-system accounting).

## Step 1: prereg commit (this commit)

- PREREG.md written and frozen BEFORE any
  implementation file exists in this lane. This
  NAMECHECK.md Step 0/1 recorded.
- Commit contains ONLY: PREREG.md, NAMECHECK.md
  (this file).
- Implementation (bp8_learner.zag, bp8_driver.zag,
  bp8_full.zag, runs, REPORT.md) comes in a LATER
  commit, strictly after this one.

## Step 2: implementation (pending)

## Step 3: runs + REPORT.md (pending)
