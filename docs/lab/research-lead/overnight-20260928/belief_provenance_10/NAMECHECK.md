# NAMECHECK: BELIEF-PROVENANCE 10 (belief revision under contradiction)

Lane: `docs/lab/research-lead/overnight-20260928/belief_provenance_10/`
Worker: BELIEF-PROVENANCE-10 subagent, 2026-10-03.
Parent: overnight priority 9, belief reasoning from
provenance/evidence. Experiment BP-10: belief revision
under contradiction (task option 2 from the BP-9
suggested nexts). Non-ledger task; nothing minted. This
lane does not presuppose the pending governance decisions
(#16 eviction-sync, #17 per-belief bars, #18 d_self
recovery): all worlds use current frozen semantics only.

## Step 0: toolchain guard (recorded before any implementation)

- Safebin: `~/safebin` active from session start.
  `export PATH="$HOME/safebin"` held for the whole
  session.
- `which python3` returns NOTHING under the safebin PATH.
- `which python` returns NOTHING under the safebin PATH.
- znc: safebin `znc` is a symlink to the pinned
  toolchain
  `~/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1`
  (builds invoked by absolute path).
- Shell used only for: znc invocation, binary
  execution, git ops, file movement, sha256 checks.
  All scientific computation in pure Zag.
- Pre-prereg exploratory probes: four probe binaries in
  /tmp/bp10work (ephemeral, NOT lane-committed), pure Zag
  under safebin, measuring block behaviors the prereg
  depends on: P-BP10a (post-contradict observations route
  to the newest fact node; the original fact sees no new
  type-7/type-3), P-BP10b (contradict one-shot per value;
  repeat matches on the newest node), P-BP10c
  (promote_graph with 2 facts writes 2 type-1 edges; a
  genuine match on the fresh fact lands on the ev_teach'd
  node), P-BP10d (fresh fact n7=n3=0), P-BP10e (match ret
  1, contradict ret 0), P-BP10f (one genuine contradict
  writes exactly one type-3 on the original fact with a
  promote_graph belief; revise_on_contradict surgery
  no-ops), P-BP10g (bid subtracts evcount(type-3); two
  forged type-3s route a later genuine match away from
  the forged fact). No probe result changed a frozen
  rule; they fixed the prereg's block assumptions. Source
  facts S1 (bp2_revise has zero callers), S2
  (confirm/disconfirm check no retirement state), S3
  (retire keeps hasb; form resets fields) read from the
  frozen code.
- Git discipline: explicit pathspecs only; commits
  local, never push; never `git reset`; never amend
  shared history; never modify other lanes. This worker
  touches only
  `docs/lab/research-lead/overnight-20260928/belief_provenance_10/`.
  Work is done in worktree `~/workspace/wt-bp10` on
  branch `lane-bp10-20261003` (forked from tnn-native-lab
  tip); final landing fast-forwards `tnn-native-lab`
  via plumbing (`update-ref` with old-value guard, per
  AGENTS.md), additive-only. If git writes fail with
  EPERM through the safebin symlink, retry via
  `/usr/bin/git` directly (per AGENTS.md lesson
  2026-10-03); on index.lock contention, retry with
  sleep backoff, never remove the lock. One stray
  `core.sparsecheckout=true` (worktree-level) was set on
  the main worktree by an aborted sparse-checkout
  attempt and immediately reverted; the main worktree
  is untouched otherwise.
- Zag pitfalls honored: u8-backed belief state with
  direct index access (no `as *i32` + slice
  construction in functions); output through the
  frozen block's existing emit/e64 helpers; no
  reliance on `.len` of casts; `if` nesting at most
  3; no `!(A && B)` in while conditions (De Morgan
  form); `[]u8 as *u8` never used.
- No em/en dashes in any lane file (byte-verified
  with grep before each commit).
- Frozen block reuse: `xf_block.zag` (lines 1..2668 of
  BP-8's bp8_full.zag) is concatenated VERBATIM as the
  base of `bp10_full.zag`; its SHA-256 is recorded in
  the prereg and re-verified before and after the build:
  172a2e7dbbaa4e60d662331965887327350068e0c13f25e438260ad08313c12a
- Belief layer reuse: BP-9's `bp9_learner.zag` is
  copied VERBATIM to `bp10_learner.zag` (hash
  re-verified):
  2de20f5a0ff87bc45140a161548b613b008e9c2adabf4da3fdda6d6d46040c5e
- New learner machinery this lane: NONE (disclosed
  in PREREG Section 1). bp10_absorb (BP-9 absorb
  renamed, identical body), bp10_ck, bp10_bar,
  bp10_selfcnt are driver-side test-harness code, not
  belief-layer changes; the forgery actions (link_edge
  writes) are adversary actions in the driver, not
  belief-layer changes; direct driver calls to frozen
  learner functions (bp2_disconfirm, bp2_confirm,
  bp2_revise, bp2_retire, bp2_form) are disclosed test
  actions invoking frozen operators, adding no rules.
  R2/R3/R5/R6/R7, eff(), bp2_retire, bp2_relicense
  stay frozen. 0 new edge types, 0 new node types,
  0 modes, 0 bridges, 0 handlers, 0 semantic cases
  (one-system accounting).

## Step 1: prereg commit (done, commit 3d3c450ca)

- PREREG.md was written and frozen BEFORE any
  implementation file exists in this lane.
- The prereg commit contained ONLY: PREREG.md,
  NAMECHECK.md (Step 0/1 as then written).

## Step 2: implementation + report (done)

- bp10_learner.zag: byte-copy of bp9_learner.zag
  (SHA-256 re-verified:
  2de20f5a0ff87bc45140a161548b613b008e9c2adabf4da3fdda6d6d46040c5e).
- bp10_driver.zag: the CON/REC/REV/AMB battery (new
  file, driver-side only, zero new learner
  machinery).
- bp10_full.zag: xf_block.zag (SHA-256 re-verified
  172a2e7dbbaa4e60d662331965887327350068e0c13f25e438260ad08313c12a)
  + bp10_learner.zag + bp10_driver.zag.
- Build: pinned znc by absolute path, exit 0,
  bp10_bin (417194 bytes); 322 A0102 warnings
  (benign, same pattern as BP-4 through BP-9).
- Runs: 3/3 byte-identical, SHA-256
  5c682624b9e8cca5cdd7bd70cea666a8241f3a4b17e0938bd2abd565cc018419.
- Result: 19/19 in-driver bars PASS on the first
  run; K-DET PASS; K-HYG PASS (compile-log em
  dashes are znc's own warning prose, disclosed in
  REPORT.md); F-VOID not triggered.
- Verdict: BP-10-PASS. REPORT.md written.
- PREREG Section 5b holds the R1 mechanistic
  refinement (no bar or number changed).
