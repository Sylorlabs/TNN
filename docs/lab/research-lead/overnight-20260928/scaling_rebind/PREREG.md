# PREREG: rebind_try Allocation/Eviction Storm - Characterization and Three Competing General Alternatives (FROZEN)

Status: FROZEN. This file is committed ALONE (with NAMECHECK.md) before
any implementation file is written. Commit-order self-check applies:
the prereg commit strictly precedes all implementation commits.

Worker: rebind_try scaling worker, replacement for the completed
H-FALLBACKFIX-1 worker (spawn 2026-10-02).
Date: 2026-10-02. Lane directory (new, own):
docs/lab/research-lead/overnight-20260928/scaling_rebind/
The scaling_fallbackfix lane is read-only and is never modified.
Pure Zag for all research computation. Frozen inputs read only, never
modified.

## 1. Background and mandate

H-FALLBACKFIX-1 scaling analysis (to be ledgered C342): three sublinear
alternatives to the O(4096) compose_try edge scans (D1 6.0x, D2 2.8x,
D3 2.9x, all CORRECT) still miss the 300s wall on the full R4B workload:
wall=1373.41s, cpu=214.78s, with rebind_try ~214.5s CPU vs compose_try
0.26s CPU (D1). The lane REPORT misattributed the cost to compose scans.

Micah's priority: treat this as SCALING EVIDENCE, not an edge-case
patch target. This prereg freezes (a) a measurement protocol that
characterizes where rebind_try spends its ~214.5s CPU, and (b) a
competition between three structurally different GENERAL alternatives
to the current rebind allocation path. Each design must be justifiable
as substrate, not as an R4B special case.

## 2. Frozen mechanism analysis (basis for predictions)

Read from scaling_fallbackfix/base_r4b_full.zag (frozen input):

- World arena: 1024 node slots (ids 2..1023), 4096 edge slots.
  alloc_node: linear scan for a free slot (ng(W,n,36)==0); at capacity
  calls evict_node.
- evict_node: full 1024-node scan from the hg(W,8) cursor; per live
  unprotected node computes bid() = five evcount scans plus one
  type-10 scan, each a full 4096 edge scan, about 7x4096 = 28.7K edge
  reads per candidate, about 29M primitive ops per eviction; then
  rec_evict plus a 4096 victim edge-kill sweep.
- Trial path: pc_try_one (per MAP per matching path) and t2_trial
  (per candidate: chains k=2..4, sums, counts, single-hops) assemble
  trial graphs IN THE WORLD ARENA via t2_asm_chain / t2_asm_count /
  t2_asm_sum (each cell = one alloc_node) plus t2_exec (one alloc_node
  for the frame). Rejected trials are NEVER freed: permanent debris.
- W-R4B: 28 training ev_queries (each: rebind_try over prior MAPs +
  t2_trial with dozens of candidates until the 1-hop verifies) plus
  one decline Z query scal_decline(W,9001,70,99999) (rebind_try over
  27 linked MAPs, every trial failing since expected=99999). Reported
  post-training state: 720 live nodes, 391 edges, 28 MAPs, 27
  type-14 links. The arena fills early in training; nearly every
  subsequent alloc_node then triggers evict_node.

## 3. Characterization protocol (instrumented baseline, frozen)

Build rb_char_full.zag = verbatim copy of
scaling_fallbackfix/base_r4b_full.zag plus counter hooks ONLY:

- alloc_node entry: hs(W,52,hg(W,52)+1) (header field 52 is free).
- evict_node entry: hs(W,60,hg(W,60)+1) (header field 60 is free).
- ev_query: emit CHAR-PHASE lines with alloc/evict/live deltas after
  rebind_try, after compose_try, and after mp_run.
- scal_r4b_train: emit per-training-query counter lines.
- scal_decline: emit Z-query counter lines.

No semantic change: the hooks only write two free header fields and
emit diagnostic lines. This build is diagnostic-only and is not
subject to the K-bars.

Frozen predictions: total alloc_node calls in the low thousands;
evict_node calls in the low hundreds; the rebind_try plus t2_trial
phases account for at least 95 percent of the about 215s CPU;
hg(W,20) reaches 1024 early in training and stays at cap for the
remainder of the run. If the measurements falsify this (for example
evict count near zero), the REPORT says so plainly and the designs
are re-ranked on measured rather than predicted mechanism.

## 4. The three designs (frozen)

Common constraints for all three: pure Zag; 0 new edge types; 0 new
node tags; 0 new semantic cases; 0 modes, bridges, handlers, or
routers; no task labels; no workload-specific constants or
thresholds. Each design is documented in REPORT.md as a substrate
mechanism with its generality argument.

### E1: trial-scoped bulk reclamation

Mechanism: rejected proposals in a generate-and-test loop are garbage
by construction. Reclaim them at trial scope instead of letting them
permanently occupy the arena.

- New functions: tb_new / tb_push / tb_count (trial buffer: driver
  z_alloc, 2048 i32 slots, slot 0 = count) and trial_free(W,tb)
  (marks listed nodes free, decrements hg(W,20), then ONE 4096 edge
  sweep killing edges touching a freed slot) and
  trial_free_from(W,tb,keep) (frees only ids at index >= keep).
- New _tb variants of t2_asm_chain, t2_asm_count, t2_asm_sum,
  t2_exec, t2_try_verify: identical logic plus a tb:[]u8 parameter;
  every allocated node id (cells, literals, exec frame) is pushed.
  Originals are kept for non-trial callers (revision path, tests).
- pc_try_one and t2_trial (all four candidate sites: chain, sum,
  count, single-hop) use the _tb variants with a per-attempt trial
  buffer. On verify reject: trial_free(W,tb) (whole trial including
  frame). On verify accept: trial_free_from(W,tb,checkpoint) where
  checkpoint is the tb count before t2_exec (frees only the frame);
  promote_graph is unchanged and keeps the verified graph.
- The edge sweep preserves the baseline invariant that no live edge
  touches a free slot (evict_node maintains the same invariant), so
  later allocations cannot inherit stale SEQ/DEP edges.

Frozen prediction: evict_node calls go to 0 on W-R4B; rebind+trial
CPU 2-8s (at least 25x reduction vs baseline); full timed wall
under 300s.

### E2: scratch-arena transactional trials

Mechanism: transactional speculation. Trial graphs are assembled and
executed in an isolated driver-side scratch arena and committed to
the world arena only on verification success; the world arena is
never polluted by rejected hypotheses.

- t2_scratch(): z_alloc(110656) zeroed arena with edge slots
  initialized to empty (es(S,e,0,-1) for e in 0..4095); node live
  flags are zero from z_alloc.
- pc_try_one and t2_trial: per attempt, allocate one scratch S and
  run t2_asm_* and t2_try_verify against S (signatures unchanged;
  the W parameter receives S). Gather/read helpers (t2_gather,
  t2_chain, rb_chain_plen) still read the real W. On reject: drop S.
  On accept: promote_copy(W,S,rootS,s,r,ans,facts,nf).
- promote_copy: walks the S graph in t2_sig order (SEQ links plus
  guard true-targets), mirrors cells into W in walk order with an
  id-remap table (literals copied by value; scalar fields copied
  verbatim; SEQ edges mirrored; DEP edges mirrored with fact ids,
  which are already real-W ids), then runs the standard promote
  tail (MAP node, type-13/2/6 edges, DEP edges to facts,
  ev_teach_in). promote_graph itself is unchanged.

Frozen prediction: evict_node calls go to 0 on W-R4B; rebind+trial
CPU 2-8s (at least 25x reduction); full timed wall under 300s.

### E3: bounded-scan (CLOCK-style) approximate eviction

Mechanism: bounded-scan approximate eviction, the CLOCK family from
OS page replacement. Attacks the per-eviction cost, not the
eviction count.

- evict_node ONLY is changed: starting from the hg(W,8) cursor,
  probe up to 64 live unprotected nodes, compute bid() for the
  probed nodes only, evict the minimum-bid node among them (ties go
  to the first probed). If no unprotected node is found within 64
  probes, fall back to the full 1024 scan (preserves the -1
  no-victim contract exactly). rec_evict and the victim edge-kill
  sweep are unchanged.
- The bound 64 is a tuning constant, not workload-specific.
- Approximation disclosed: the victim may differ from the exact
  argmin. On W-R4B the victims are bid-0 trial debris under both
  policies; debris nodes are invisible to every read path (tags
  101/102/103/902, never tag 1; DEP edges run debris->fact so they
  do not affect debris bids), so victim choice among debris is
  unobservable. The REPORT states the approximation and its safety
  condition honestly.

Frozen prediction: per-eviction cost about 29M to about 1.9M
primitive ops (about 15x); eviction COUNT unchanged; rebind+trial
CPU about 12-20s (10-20x reduction); full timed wall likely under
300s but this is the closest of the three, uncertainty recorded.

## 5. Workload W-R4B (frozen, by reference)

Identical to the scaling_fallbackfix W-R4B definition: scal_r4b_train
(28 facts via ev_teach, 28 one-link MAPs via ff_train1 with
ev_query(W,s,800+idx,o,0)) then scal_decline(W,9001,70,99999),
expected decline ans=-2 with COMP-FAIL. The frozen reference is
scaling_fallbackfix/base_r4b_bin; this lane rebuilds the baseline
from base_r4b_full.zag + main_r4b.zag with the pinned compiler and
confirms the reference digests before comparing designs.

## 6. Frozen bars

Correctness (per design; baseline = rebuilt baseline binary):
- K1 R4B decline: ans=-2 with COMP-FAIL; RB-STAT and COMP-STAT
  tried/rejected counts EXACTLY equal baseline; the lines
  TIMED-DECLINE-START, RB-STAT, COMP-STAT, TIMED-DECLINE-END,
  R4B-Z ans=, R4B-RESULT= byte-identical to baseline. (Design-local
  CHAR- diagnostic lines are excluded from the line set.)
- K2 R4C success: ans=9008; TIMED lines byte-identical to baseline.
- K3 CORR battery (R7/R3/R6A via main_corr): stdout byte-identical
  to baseline.
- K4 C234 battery (t1,t2a,t2b,t3,t4,t5,t4b): stdout byte-identical
  to the baseline digest (baseline reproduced first).
- K5 D0: 3 runs per timed binary, byte-identical stdout within the
  design, SHA-256 recorded.
Performance:
- P1 (primary): rebind+trial-phase CPU, measured by time -p on the
  timed binary with the phase attribution from the characterization
  build, reduced by at least 10x vs the baseline median.
- P2 (secondary, reported): full timed R4B (train + Z) wall under
  300s.
Architecture:
- A0: 0 new edge types, 0 new node tags, 0 new semantic cases,
  0 modes/bridges/handlers/routers (grep audited); no task labels;
  each design documented as a substrate mechanism with no
  workload-specific constants.

## 7. Method (frozen)

- Toolchain guard Step 0 in NAMECHECK.md, executed before any other
  work this session.
- Frozen inputs (read only): scaling_fallbackfix/base_r4b_full.zag,
  scaling_fallbackfix/base_c234_full.zag,
  scaling_fallbackfix/main_r4b.zag,
  scaling_fallbackfix/main_corr.zag. Copied into this lane as
  rb_base_full.zag, rb_c234_base_full.zag, rb_main_r4b.zag,
  rb_main_corr.zag and cmp-verified before use.
- Variant construction: cp the frozen copy, then surgical function
  edits with file tools (no sweeping rewrites). Compile with the
  pinned compiler src/tools/toolchain/znc_linux_x86_64_abed8aa1.
  Mains appended with cat.
- New dynamic output reuses the proven emit/e64 helpers only (no new
  _zag_print wrappers); the K5 3/3 byte-identity bar empirically
  guards every binary against the pinned compiler's
  layout-dependent print defect.
- Timing protocol: time -p for CPU (user+sys), wall from
  date +%s.%N around the run, /proc/loadavg before and after,
  sha256sum of stdout. Runs sequential per binary. Timeout guard
  3600s; P2 is judged on measured wall under 300s, not the guard.
- Commit order: this prereg (+ NAMECHECK.md) commits ALONE first.
  Then frozen input copies. Then characterization build+run. Then
  E1/E2/E3 implementations. Then runs plus REPORT.md. Explicit
  pathspecs on every commit. Never git reset. Never amend shared
  history. Local only, never push.
- Zero em/en dashes in all lane documents (byte-verified before
  commit).

## 8. Verdict rule

Per design: CORRECT iff K1 through K5 and A0 all pass. REBIND-PASS
iff CORRECT and P1 passes. Designs are ranked by median
rebind+trial-phase CPU seconds. A design that is correct but misses
P1 or P2 is reported as scaling evidence with its measured
reduction factor, not as a failure of honesty. If no design beats
the storm, that is a finding about the rebind path, reported
plainly. VOID is terminal: a broken prereg is amended transparently
and re-frozen, never silently fixed.
