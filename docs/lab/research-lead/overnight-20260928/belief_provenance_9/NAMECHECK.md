# NAMECHECK: BELIEF-PROVENANCE 9 (provenance chain integrity)

Lane: `docs/lab/research-lead/overnight-20260928/belief_provenance_9/`
Worker: BELIEF-PROVENANCE-9 subagent, 2026-10-03.
Parent: overnight priority 9, belief reasoning from
provenance/evidence. Experiment BP-9: provenance chain
integrity under adversarial corruption (task option 1).
All 7 falsifiable predictions (FP1-FP7) stay sealed;
this lane does not re-open them. Non-ledger task;
nothing minted. This lane does not presuppose the
pending governance decisions (#16 eviction-sync, #17
per-belief bars, #18 d_self recovery): all worlds use
current frozen semantics only.

## Step 0: toolchain guard (recorded before any implementation)

- Safebin: `~/safebin` active from session start.
  `export PATH="$HOME/safebin"` held for the whole
  session.
- `which python3` returns NOTHING under the safebin PATH.
- `which python` returns NOTHING under the safebin PATH.
- znc: safebin `znc` is a symlink to the pinned
  toolchain
  `~/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1`
  (SHA-256
  498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef;
  builds invoked by absolute path).
- Shell used only for: znc invocation, binary
  execution, git ops, file movement, sha256 checks.
  All scientific computation in pure Zag.
- Pre-prereg exploratory probe: one probe binary in
  /tmp/bp9probe (ephemeral, NOT lane-committed),
  pure Zag under safebin, measuring block behaviors
  the prereg depends on: P1a (two promote_graph
  calls on one shared fact give distinct MAP ids
  mP=3 mQ=5, one type-1 licensing edge each), P1b
  (ev_observe match on shared fact: ret 1, +1
  type-7), P1c (link_edge type-7 self-edge on a
  fact is counted by the census), P1d (link_edge
  kind-3 self-edge with field12=9 is found by the
  reason-code query). No probe result changed a
  frozen rule; they fixed the prereg's block
  assumptions.
- Git discipline: explicit pathspecs only; commits
  local, never push; never `git reset`; never amend
  shared history; never modify other lanes. This
  worker touches only
  `docs/lab/research-lead/overnight-20260928/belief_provenance_9/`.
  Worktree branch is tnn-native-lab (verified
  `git branch --show-current`). If git writes fail
  with EPERM through the safebin symlink, retry via
  `/usr/bin/git` directly (per AGENTS.md lesson
  2026-10-03); on index.lock contention, retry with
  sleep backoff, never remove the lock.
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
  1..2668 of BP-8's bp8_full.zag) is concatenated
  VERBATIM as the base of `bp9_full.zag`; its
  SHA-256 is recorded in the prereg and re-verified
  before and after the build:
  172a2e7dbbaa4e60d662331965887327350068e0c13f25e438260ad08313c12a
- Belief layer reuse: BP-8's `bp8_learner.zag` is
  copied VERBATIM to `bp9_learner.zag` (hash
  re-verified):
  2de20f5a0ff87bc45140a161548b613b008e9c2adabf4da3fdda6d6d46040c5e
- New learner machinery this lane: NONE (disclosed
  in PREREG Section 1). bp9_absorb (BP-8 absorb
  renamed, identical body), bp9_ck, bp9_bar,
  bp9_selfcnt, bp9_allsup, bp9_liclive are
  driver-side test-harness code, not belief-layer
  changes; the forgery actions (link_edge writes,
  direct bt[] writes) are adversary actions in the
  driver, not belief-layer changes. R2/R3/R5/R6/R7,
  eff(), bp2_retire, bp2_relicense stay frozen.
  0 new edge types, 0 new node types, 0 modes,
  0 bridges, 0 handlers, 0 semantic cases
  (one-system accounting). Reason code 9 is a
  novel field12 VALUE used only as the forgery
  marker, not a new edge type or semantic case.

## Step 1: prereg commit (done, commit 0742f9cea)

- PREREG.md was written and frozen BEFORE any
  implementation file existed in this lane.
- The prereg commit contained ONLY: PREREG.md,
  NAMECHECK.md (Step 0/1 as then written).
- Implementation came in a LATER commit,
  strictly after the prereg commit
  (commit-order self-check holds).

## Step 2: implementation (done)

- Files: bp9_learner.zag (verbatim copy of BP-8's
  bp8_learner.zag, SHA-256
  2de20f5a0ff87bc45140a161548b613b008e9c2adabf4da3fdda6d6d46040c5e
  on both, `cmp` clean), bp9_driver.zag (new: two
  world arms FORGE/CHAIN, bp9_absorb with the
  identical body of bp8_absorb, bp9_ck/bp9_bar/
  bp9_selfcnt/bp9_allsup/bp9_liclive test helpers,
  world builders, in-driver bars). Zero new learner
  functions this lane; the forgery actions are
  adversary actions in the driver, not belief-layer
  changes.
- Built: `sed -n '1,2668p'
  ../belief_provenance_8/bp8_full.zag` (the patched
  block, verbatim) + bp9_learner.zag + bp9_driver.zag
  > bp9_full.zag; pinned znc by absolute path,
  build exit 0 -> bp9_bin (383428 bytes; log:
  bp9_compile.txt; 322 A0102 warnings are the benign
  ignored-return-value pattern pervasive in the
  frozen block itself, same as BP-4 through BP-8).
- Block SHA-256 re-verified before AND after the
  build: 172a2e7dbbaa4e60d662331965887327350068e0c13f25e438260ad08313c12a
  (unchanged).
- No amendment round: the first implementation run
  went 17/17 against the frozen prereg, so PREREG.md
  Section 5b stays empty. No frozen rule changed to
  chase a bar.
- No Python/C/JS/Rust invoked at any point. Safebin
  PATH held for the whole session. `which python3` /
  `which python` still empty at build and run.
- No em/en dashes in any authored lane file or run
  output (byte-verified with grep).
- 0 new edge types (1/3/7/14 all pre-existing in the
  block; kind-3 self-edges pre-exist via bp2_retire),
  0 new node types (tags 1/3/20 pre-existing),
  0 modes, 0 bridges, 0 handlers, 0 semantic cases
  (one-system accounting). Reason code 9 is a novel
  field12 VALUE used only as the forgery marker,
  not a new edge type or semantic case.

## Step 3: runs + REPORT.md (done)

- 3/3 runs byte-identical: sha256
  55de4ccfa05f33d22e477d670a67abdbb8b33560f8523a9f7b9e6f41d1125a18
  for bp9_run1/2/3.txt (K-DET PASS).
- In-driver bars: 17/17 PASS (2 PCs + 15 K bars).
  FORGE: forged match 110/2 (n7==1,
  undetectable); forged contradict 80/0/1
  (n3==1, undetectable); forged match on
  contradicted fact absorbed 90/1/0 (n7==1,
  bypasses block one-shot protection,
  forgery-unique signature); 3 forged type-7s
  saturate to one R2 (n7==3, 110/2);
  stale-watermark replay 120/3 (no replay
  protection); shared-fact genuine match 110/110
  (non-rivalrous); one forged shared-fact edge
  120/120 (blast radius 2). CHAIN: propagated
  weakening 40 and snap-up 80 leave no trace on
  the composite's record (disc 0, conf 1, no k3);
  forged reason-9 queryable, coexists with
  genuine reason-2 retire (ambiguous record);
  table tamper to 100 accepted (eff 100, retired
  belief selected at bar 50 with reason-2 edge
  present); fact death leaves b_ext stale (1 vs
  live 0); explicit relicense retires reason-2.
  BP9-SUMMARY 17/17; 19/19 with K-DET/K-HYG.
- REPORT.md written with verdict BP-9-PASS. The 7
  sealed predictions stay sealed; this lane adds
  adversarial-integrity evidence only.
- Committed with explicit pathspecs, local only,
  never pushed.
- Ledger: non-ledger task, nothing minted; ledger
  file untouched.
