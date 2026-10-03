# NAMECHECK: BELIEF-PROVENANCE 11 (cross-belief interaction beyond shared-fact scoping)

Lane: `docs/lab/research-lead/overnight-20260928/belief_provenance_11/`
Worker: BELIEF-PROVENANCE-11 subagent, 2026-10-03.
Parent: overnight priority 9, belief reasoning from
provenance/evidence. Experiment BP-11: cross-belief
interaction beyond shared-fact scoping (task option 3
from the BP-10 suggested nexts). Non-ledger task;
nothing minted. This lane does not presuppose the
pending governance decisions (#16 eviction-sync,
#17 per-belief bars, #18 d_self recovery): all worlds
use current frozen semantics only, no eviction
pressure, one fixed bar in selection calls, no d_self
manipulation.

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
- No pre-prereg exploratory probes this lane: every
  block behavior the prereg depends on is either read
  directly from the frozen source (activate/bid/
  ev_observe/ev_teach/promote_graph, with bid counts
  hand-derived from the driver's own edge writes) or
  was probe-measured in BP-10 (/tmp/bp10work:
  P-BP10a, P-BP10e, P-BP10f, P-BP10g). No probe
  result changed a frozen rule.
- Git discipline: explicit pathspecs only; commits
  local, never push; never `git reset`; never amend
  shared history; never modify other lanes. This worker
  touches only
  `docs/lab/research-lead/overnight-20260928/belief_provenance_11/`.
  Work is done in worktree `~/workspace/wt-bp11` on
  branch `lane-bp11-20261003` (forked from tnn-native-lab
  tip 4aa6b2680); final landing fast-forwards
  `tnn-native-lab` via plumbing (`update-ref` with
  old-value guard, per AGENTS.md), additive-only. If git
  writes fail with EPERM through the safebin symlink,
  retry via `/usr/bin/git` directly (per AGENTS.md
  lesson 2026-10-03); on index.lock contention, retry
  with sleep backoff, never remove the lock.
- Zag pitfalls honored: u8-backed belief state with
  direct index access (no `as *i32` + slice
  construction in functions); output through the
  frozen block's existing emit/e64 helpers; no
  reliance on `.len` of casts; `if` nesting at most
  3; no `!(A && B)` in while conditions (De Morgan
  form); `[]u8 as *u8` never used.
- No em/en dashes in any lane file (byte-verified
  with grep before each commit).
- Frozen block reuse: lines 1..2668 of BP-10's
  bp10_full.zag concatenated VERBATIM as the base of
  `bp11_full.zag`; its SHA-256 is recorded in the
  prereg and re-verified before and after the build:
  172a2e7dbbaa4e60d662331965887327350068e0c13f25e438260ad08313c12a
- Belief layer reuse: BP-10's `bp10_learner.zag` is
  copied VERBATIM to `bp11_learner.zag` (hash
  re-verified):
  2de20f5a0ff87bc45140a161548b613b008e9c2adabf4da3fdda6d6d46040c5e
- New learner machinery this lane: NONE (disclosed
  in PREREG Section 1). bp11_absorb (BP-10 absorb
  renamed, identical body), bp11_ck, bp11_bar,
  bp11_selfcnt, bp11_liclive are driver-side
  test-harness code, not belief-layer changes; the
  forgery actions (link_edge writes) are adversary
  actions in the driver, not belief-layer changes;
  the driver-written type-14 edges in PROP are test
  setup for the frozen R6 rule (same as BP-9 CHAIN),
  not belief-layer changes; direct driver calls to
  frozen learner functions (bp2_disconfirm,
  bp2_confirm, bp2_retire, bp2_form, bp2_propagate,
  bp2_kill_one_prov, bp2_relicense, bp2_select,
  bp2_eff, bp2_lic_live) are disclosed test actions
  invoking frozen operators, adding no rules.
  R2/R3/R5/R6/R7, eff(), bp2_retire, bp2_relicense
  stay frozen. 0 new edge types, 0 new node types,
  0 modes, 0 bridges, 0 handlers, 0 semantic cases
  (one-system accounting).

## Step 1: prereg commit (this commit)

- PREREG.md was written and frozen BEFORE any
  implementation file exists in this lane.
- The prereg commit contains ONLY: PREREG.md,
  NAMECHECK.md (Step 0/1 as then written).
