# NAMECHECK: BELIEF-PROVENANCE 6 (open dynamics, continued)

Lane: `docs/lab/research-lead/overnight-20260928/belief_provenance_6/`
Worker: BELIEF-PROVENANCE-6 subagent, 2026-10-03.
Parent: overnight priority 9, belief reasoning from
provenance/evidence. Experiment BP-6: the remaining BP-5
open dynamics (bar-adjustment trajectories, combiner
alternatives, eviction interaction, larger/nested cycles).
All 7 falsifiable predictions (FP1-FP7) stay sealed; this
lane does not re-open them. Non-ledger task; nothing
minted.

## Step 0: toolchain guard (recorded before any implementation)

- Safebin: `~/safebin` provisioned with the 36 allowed
  tools. `export PATH="$HOME/safebin"` held for the whole
  session.
- `which python3` returns NOTHING under the safebin PATH.
- `which python` returns NOTHING under the safebin PATH.
- znc resolves via the safebin symlink to the pinned
  toolchain
  `~/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1`
  (builds invoked by absolute path; verified present
  2026-10-03).
- Shell used only for: znc invocation, binary execution,
  git ops, file movement, sha256 checks. All scientific
  computation in pure Zag.
- Pre-prereg exploratory probes ran in /tmp/bp6probe
  (ephemeral, never committed): evict_node deterministic
  victim targeting via type-9 protection (returned the
  target id, target dead, rec_evict tombstone live tag-3
  on the hg(12) chain); repeated matching ev_observe
  writes one type-7 per call (t7cnt 2/2); mixed
  contradict-then-match sequence on two facts of one MAP
  (t3==1 on the contradicted fact, t7==1 on the matched
  fact, MAP field28 unchanged); bp2_bar_after(50,1,100)
  ==51. Probes established what is testable; all
  predicted numbers in PREREG.md are hand-derived from
  the frozen R1-R7 forms plus these probe measurements.
- Git discipline: explicit pathspecs only; commits local,
  never push; never `git reset`; never amend shared
  history; never modify other lanes. This worker touches
  only
  `docs/lab/research-lead/overnight-20260928/belief_provenance_6/`.
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
  the base of `bp6_full.zag`; its SHA-256 is recorded in
  the prereg and re-verified before and after the build:
  172a2e7dbbaa4e60d662331965887327350068e0c13f25e438260ad08313c12a
- Belief layer reuse: BP-5's `bp5_learner.zag` is copied
  VERBATIM to `bp6_learner.zag` (hash re-verified):
  2de20f5a0ff87bc45140a161548b613b008e9c2adabf4da3fdda6d6d46040c5e
- New learner machinery this lane: NONE (disclosed in
  PREREG Section 1). bp2_bar_after is existing dormant
  belief-layer code, now triggered in a closed loop.
  Combiner variants (bp6_cmax/bp6_cavg/bp6_cwavg) are
  driver-side experimental code, not belief-layer
  changes; R6 (min) stays frozen. Everything else new is
  test-harness code in bp6_driver.zag (world builders,
  bp6_absorb, commitment bookkeeping, in-driver bars).

## Step 1: prereg commit (this commit)

- PREREG.md written and frozen BEFORE any implementation
  file exists in this lane. This NAMECHECK.md Step 0/1
  recorded.
- Commit contains ONLY: PREREG.md, NAMECHECK.md (this
  file).
- Implementation (bp6_learner.zag, bp6_driver.zag,
  bp6_full.zag, runs, REPORT.md) comes in a LATER commit,
  strictly after this one.

## Step 2: implementation (pending)

## Step 3: runs + REPORT.md (pending)
