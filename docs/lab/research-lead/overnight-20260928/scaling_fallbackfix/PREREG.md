# PREREG: H-FALLBACKFIX-1 Scaling Analysis, Competing Sublinear Alternatives to the O(4096) Edge-Scan Pattern (FROZEN)

Status: FROZEN. This file is committed ALONE (with NAMECHECK.md) before
any implementation file is written. Commit-order self-check applies:
the prereg commit strictly precedes all implementation commits.

Worker: H-FALLBACKFIX-1 scaling-analysis worker (spawn 2026-10-02).
Date: 2026-10-02. Branch: lane-tnn3-20261002-1421pdt (local worktree;
task named tnn-native-lab but that branch is checked out and locked in
worktree ~/workspace/tnn-rsi-gpi3, so this work proceeds here; all
commits local, never pushed). Pure Zag for all research computation.
Frozen inputs read only, never modified.

## 1. Background and mandate

H-FALLBACKFIX-1 went BUILD-FAIL on performance (ledger C313): the
repair is CORRECT (R4b/R4c branching 28 per node down to 2 per node,
finite decline DFS, clean COMP-FAIL) but misses the frozen 300s wall.
Per the completion REPORT (composition_fallbackfix/REPORT.md section 4),
the decline DFS costs about 275s CPU from per-node O(4096) edge-store
scans that are unamortized across the about 511 DFS node visits.

Micah's ruling: treat this as SCALING EVIDENCE, not an edge-case patch
target. This prereg therefore does NOT optimize the failing case. It
freezes a competition between three structurally different sublinear
alternatives to the O(4096) edge-scan pattern, implemented in pure Zag
against the same repaired base, measured on the same workload that
failed.

## 2. The failing pattern (frozen analysis)

In the repaired patch (composition_fallbackfix/ff_patch.zag), each
cl_dfs node visit performs, per candidate fragment:

- cl_candidates: one full 4096 edge scan to enumerate FRAG marks.
- cl_extract: one 4096 mark-entry scan, plus per fragment step one
  4096 seq_nx scan and one 4096 dep_fact scan (len is 1 on this
  workload, so 3 scans of 4096 per extraction).
- cb_has_couse: nused times one 4096 scan (nused averages about 4 on
  the decline tree).
- cl_dfs revalidates every admitted candidate with a second full
  cl_satisfy, doubling the extraction cost.

Estimated total: about 511 visits times about 282k primitive
edge/node calls per visit, about 144M calls, about 275s CPU (lane
measurement C313). The pattern is: linear scans of a fixed 4096
store, repeated per node, per candidate, per step, with no reuse of
prior identical lookups.

## 3. The three designs (frozen)

All three keep every public signature used by drivers
(compose_try, ev_query, ev_cq, cl_mark, cb_couse_link), change no
world semantics, add no edge types, node tags, semantic cases,
modes, bridges, handlers, or routers. Each is a full replacement
patch file over the repaired ff_patch.zag (dead cl_build_cache
dropped; zero call sites).

### D1: substrate edge-and-fact index (general substrate mechanism)

A per compose_try index over the edge store and the fact nodes,
built once after the auto-mark loop, consulted by every lookup on
the DFS path. Analogous to the FACT/MAP index work.

Structures (z_alloc, per compose_try, discarded after):
- xft_head: 2048 by 16 i32 bucket heads keyed (from, type).
- xft_next: 4096 i32 chain links.
- xt_head/xt_next: 16 type heads plus 4096 links (type-15 chain for
  the candidate enumeration).
- xfr_head: 2048 i32 hash heads keyed (s, r) over live tag-1 fact
  nodes; xfr_next: 1024 links.

Build: single pass e = 4095 down to 0, head-insert, skipping empty
slots (from == -1); chains therefore ascend in edge-id order, which
is exactly the baseline scan visitation order. Fact pass n = 1023
down to 2 over live tag-1 nodes, same ordering guarantee for
t2_lu_first.

Rewritten lookups (same first-match, same existence, same order):
dep_fact, seq_nx, mark-entry find, cl_mark dedup is not needed
(auto-mark uses the baseline 4-arg cl_mark before the build),
cb_couse_link dedup (success path only), cb_has_couse, the
cl_candidates outer scan (type-15 chain), cl_walk's t2_lu_first
(fact hash).

Exactness argument: no edge writes or deletes occur during cl_dfs
(decay touches only type-9 edges and runs before compose_try inside
ev_query; t2_kill_edge is reachable only via ev_observe; pc_del_links
is driver-only; node eviction needs node allocation and z_alloc is
malloc-based, so none happens during the DFS). No node writes happen
during the DFS either. The index therefore reflects the store exactly
for the whole DFS, and every lookup returns exactly what the scan
returned, in the same order.

Frozen complexity claim: per compose_try O(4096 + 1024) build;
per node visit O(type-15 chain + candidates times bucket walks).
Predicted 300x to 1000x CPU reduction on W-R4B (about 275s down to
under 2s). This design also removes the t2_lu_first 1024 node scans
that bound the other two designs.

### D2: lazy per-query memoization of pure subcomputations

No upfront build. Two small memo tables (z_alloc, per compose_try,
threaded through cl_dfs, cl_candidates, cl_satisfy):

- Memo E: 64 slots keyed (m, start, len), caching cl_extract
  results (ex status plus rels). Extraction is cur-independent, so
  one fill serves all satisfy queries for that fragment (all cur
  values, candidates pass plus cl_dfs revalidation). Filled lazily
  on first miss via the scan path.
- Memo P: 64 slots keyed (m), caching co-use presence: whether any
  aux == 0 type-15 edge leaves m. Filled lazily via one 4096 scan
  per m. cb_has_couse with presence 0 returns 0 in O(1); the R4B
  decline world has no co-use edges, so all 28 fills hit the fast
  path.

The cur-dependent fallback (t2_gather plen) is deliberately NOT
memoized. The cl_candidates outer 4096 scan is unchanged.

Exactness argument: within one compose_try the store is unmutated
(same no-write/delete case as D1), so a cached pure subcomputation
equals its recomputation.

Frozen complexity claim: per compose_try O(F times S) fills with
F about 28 fragments and S = 4096, plus the unchanged per-visit
outer scans and walks. Predicted 8x to 15x CPU reduction on W-R4B
(about 275s down to about 15 to 30s). The remaining dominant cost
is the per-visit outer mark scan and the t2_lu_first walks, which
this design intentionally does not address.

### D3: mechanism-maintained fragment summary (write-through,
verify-and-repair, session-persistent)

The composition mechanism maintains its own summary of its
experience as learner state (in driver-allocated buffers, never in
the world store): a mark inventory plus per-fragment extraction
summaries plus per-MAP co-use presence/targets.

- Write-through: D3's summary-aware cl_mark_s (used by the
  auto-mark loop) extracts each fragment once at mark time via the
  scan path and stores (mark edge, entry cell, per step: guard
  cell, set cell, fact id, rel, seq edge to next step). D3's
  cb_couse_link_s maintains per-MAP co-use presence and target
  lists at write time. The baseline 4-arg cl_mark and cb_couse_link
  keep their exact behavior for external callers (cl_driver t4b,
  R6A probe, ev_cq).
- Inventory as the candidate source: cl_candidates iterates the
  summary inventory (sorted by mark-edge id after reconcile, which
  equals the baseline scan visitation order) instead of scanning
  4096 per visit. A once-per-compose_try reconcile pass (one 4096
  scan) picks up marks written outside the summary path (cl_driver
  t4b direct cl_mark calls) so the inventory is complete.
- Verify-and-repair reads: cl_extract on a summary hit re-checks
  every predicate the scan path checks (mark edge from/type/aux,
  entry linkage, per-step guard tag 102, guard to set linkage, set
  tag 101, seq-edge linkage, fact tag 1 and live, rel equality),
  all O(len) node reads, zero scans. Mismatch falls back to the
  scan path and refreshes the entry (self-repair). Co-use presence
  is lazy-filled by one scan per m on first need, then
  write-through maintained.
- Session persistence: the driver allocates one summary per
  session and threads it through compose_try_s for two back to
  back decline queries with no world mutation between them.
  Plain compose_try allocates a fresh per-call summary (same
  per-call benefit, no cross-call state); ev_query is unchanged.

Exactness argument: within a compose_try, and across the two
session queries (nothing runs between them by construction), no
edge writes or deletes occur on the read path; the only type-15
writers in base plus patch are cl_mark variants and cb_couse_link
variants, all tracked; node recycling is caught by the verify
predicates (tag, live, rel equality). Verify pass therefore implies
the scan would return identical rels.

Frozen complexity claim: Q1 O(F times len times S) mark-time plus
O(visits times candidates times len) verify; Q2 O(visits times
candidates times len) only. Predicted Q1 10x to 20x, Q2 12x to 25x
CPU reduction on W-R4B. The session test's structural point is the
verify hit rate (expected 100 percent, zero rescans), demonstrating
cross-query amortization; absolute Q2 time stays walk-bound like D2.

## 4. Workload W-R4B (frozen definition)

Identical construction to H-FALLBACKFIX-1 K4 (ff_driver.zag
ff_r4b_test, copied verbatim into this lane's timed driver):
2-wide depth-8 layered graph, nodes 9000+g*100+a, relations
300+g*4+(a-1)*2+(b-1), 28 facts via ev_teach, 28 one-link MAPs via
ff_train1 (ev_query per MAP), then the Z query (9001, 70, 99999,
expected 99999).

Timed measurement replicates ev_query's exact prefix (header bump,
decay, ctx_push, activate, rebind_try with the shared rbs buffer)
then calls compose_try directly and stops, isolating the scan
pattern. This is the same workload that failed K4: same world,
same query, same preconditions at compose_try entry; only the
post-decline pipeline (mp_run, bootstrap_miss, miss_inquire, all
frozen base) is excluded from the primary timing and measured
separately as P2.

W-R4C (success variant, ff_r4c_test verbatim, Z = (9001, 70, 9008))
is the secondary workload for the C6 bar.

## 5. Frozen bars

Correctness (each design; must equal the repaired baseline):
- C1 R7: ans=105, COMP-SEGS n=2 [26 39], R7-FALSE14=0 R7-FALSE15=0
  R7-DUP15=0, R7-RESULT=PASS; per-design fast binary stdout
  byte-identical to the baseline fast binary.
- C2 R3: ans=306, R3-RESULT=PASS (same byte-identity rule).
- C3 R6A: w1=1 w2=0 w3=0, R6A-Z ans=103, R6A-DUP15=0,
  R6A-RESULT=PASS (same byte-identity rule).
- C4 C234 battery: per-design c234 binary stdout byte-identical
  to the lane's ff2_c234_run1.txt (SHA-256
  4c898771fdaafe79a7bd0c0daa3faf247cbbde742fe7102a945e0e94e0b4ad5a);
  the baseline c234 binary must reproduce that digest first.
- C5 R4B decline: timed compose_try returns -2 with COMP-FAIL;
  TIMED-DECLINE output (RB-STAT, COMP-STAT, ans) byte-identical
  across baseline and designs.
- C6 R4C: timed compose_try returns 9008; output byte-identical
  across designs (baseline R4C run best-effort reference).

Performance:
- P1 (primary, per design): W-R4B timed decline completes within
  300s wall-clock. "Beats the wall" means P1 passes with C5 held.
- P2 (secondary, reported not pass/fail): full ev_query W-R4B
  within 300s wall (K4 parity). Expected to still miss because the
  post-decline pipeline is frozen base code outside this
  experiment's scope; either outcome is reported as scaling
  evidence.

Determinism:
- D0: 3 runs per binary, byte-identical stdout, SHA-256 recorded.
  Applies to all corr, timed, session, and c234 binaries.

Architecture:
- A0: 0 new edge types, 0 new node tags, 0 new semantic cases,
  0 modes/bridges/handlers/routers in all three designs (grep
  audited). D1's index and D2's memo are general substrate/query
  mechanisms; D3's summary is mechanism-maintained learner state.

## 6. Method (frozen)

- Toolchain guard in NAMECHECK.md Step 0 before any work; pure
  Zag for all research computation; shell only for znc invocation,
  binary execution, git ops, file movement.
- Frozen inputs (read only): composition_C/cc_base.zag,
  composition_fallbackfix/ff_patch.zag (copied to this lane as
  ff_patch_base.zag, cmp-verified), composition_fallbackfix/
  ff_driver_nomain.zag, composition_collapse/cl_driver.zag.
- Build recipe: cat cc_base.zag <patch> [ff_driver_nomain.zag]
  [timed driver] [main] > <full>.zag; compile with the pinned
  znc src/tools/toolchain/znc_linux_x86_64_abed8aa1. C234 builds
  use cl_driver.zag (own main) instead of the timed driver.
- Timing protocol: `time -p` for CPU (user+sys), wall from
  date +%s.%N around the run, /proc/loadavg before and after,
  sha256sum of stdout. Runs sequential per binary (no
  self-contention). Generous timeout guards (3600s); P1 is judged
  on measured wall under 300s, not on the guard.
- Commit order: this prereg (+ NAMECHECK.md) commits ALONE first.
  Then implementation files. Then runs plus REPORT.md. Explicit
  pathspecs on every commit. Never git reset. Never amend shared
  history. Local only, never push.
- New dynamic output in this lane reuses the existing proven
  emit/e64 helpers (no new _zag_print wrappers); the D0 3/3
  byte-identity bar empirically guards every binary against the
  pinned compiler's layout-dependent print defect.
- Zero em/en dashes in all lane documents (byte-verified before
  commit).

## 7. Verdict rule

Per design: CORRECT iff C1 through C6 and D0 and A0 all pass.
BEATS-WALL iff CORRECT and P1 passes. Designs ranked by median
timed-decline CPU seconds. A design that is correct but misses P1
is reported as scaling evidence with its measured reduction
factor, not as a failure of honesty. If no design beats the wall,
that is a finding about the pattern, reported plainly.
