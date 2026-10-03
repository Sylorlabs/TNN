# REPORT: H-FALLBACKFIX-1 Repair of R7/R4b/R4c Fallback Kills in Collapsed Composition

Date: 2026-10-02. Worker: H-FALLBACKFIX-1 completion worker (watchdog).
Branch: tnn-native-lab. Local only, never pushed.
Prereg: PREREG.md (frozen 9d1adc2f6) + PREREG_AMENDMENT1.md (03febc337)
+ PREREG_AMENDMENT2.md (22439e89f). Bars unchanged; no re-preregistration.
Pure Zag. Frozen read only.

## 0. Completion context (what this run did)

The orphan recovery commit 9bb1ace10 held PARTIAL EVIDENCE ONLY and no
verdict. This worker completed the battery under the already-frozen
prereg. Load-bearing findings during completion:

(a) STALE SOURCE: the committed ff_patch.zag (16:27) postdated all runs
and, worse, did NOT compile: its cl_build_cache addition passes
`cache+base+16` (i32) where []u8 is expected (znc E0203, typed
declaration check FAILED). The function is dead code (zero call sites)
and was never wired into cl_satisfy. Minimal fix applied: slice idiom
`cache[base+16..base+48]` (as used at cc_base.zag line 24). One line.
The function remains dead code. Behavioral path
(cl_extract/cl_walk/cl_satisfy/cl_candidates/cl_dfs/compose_try/
cb_couse_link) is byte-identical to the 16:12 embedded version that
produced the stale R7/R3/R6A passes. All completion builds and runs use
the fixed final patch.

(b) AMENDMENT-2 COMPLIANCE: ff_verify_driver.zag (16:10) predates the
frozen amendment 2 (16:21) and trained V-R4B/V-R4C via direct t2_trial.
New ff2_verify_driver.zag trains via ev_query per the frozen amendment
(ffv_train1 mirrors ff_driver.zag ff_train1). Worlds otherwise
identical. Per-test mains split out so the 600s K2 timeouts apply per
test.

## 1. Builds (all against the fixed final ff_patch.zag)

- ff2_fast_bin: cc_base + ff_patch + ff_driver_nomain + ff_fast_main
  (R7/R3/R6A)
- ff2_r4b_bin: cc_base + ff_patch + ff_driver_nomain + ff2_r4b_main
- ff2_r4c_bin: cc_base + ff_patch + ff_driver_nomain + ff2_r4c_main
- ff2_vr7_bin: cc_base + ff_cl_patch_orig + ff2_verify_driver
  + ff2_vr7_main (unfixed)
- ff2_vr4b_bin / ff2_vr4c_bin: cc_base + ff_cl_patch_orig
  + ff2_verify_driver + ff2_vr4b/vr4c_main (unfixed)
- ff2_c234_bin: cc_base + ff_patch + composition_collapse/cl_driver.zag
- All 7 compiled clean with the pinned znc (warnings only, A0102 class).

## 2. Per-bar verdicts against the EXACT frozen bars

### K1: V-R7 on UNFIXED mechanism reproduces the kill

PASS. ff2_vr7_run1/2/3.txt (3/3 byte-identical, sha256
7fe32b422fafe67799979ce8dc256a8e271fc3bb74d024011e52351a9981abd3):
Z ans=105 via COMP-SEGS n=2 [13 26] = [M,N] (misattributed; M=13, N=26,
P=39 from V-R7-IDS); LINK14 MAP_Z(119) -> M(13) present (false
provenance); type-15 N(26) -> M(13) aux=0 present (false co-use).
Matches the frozen kill signature exactly. Kill transfer confirmed.

### K2: V-R4B and V-R4C on UNFIXED mechanism do not terminate within 600s each

PASS. ff2_vr4b_run1.txt: `timeout 600` kill (exit 124); output shows
V-R4B training completed (28 facts+maps, zero FFV-TRAIN1-FAIL),
branch probe FFV-BRANCH-AT=9001 n=28 (every 1-link MAP fallback-admitted
at every node: the kill mechanism), V-R4B-Z-START, then no completion
in 600s. ff2_vr4c_run1.txt: `timeout 600` kill (exit 124); training
completed, V-R4C-Z-START, no completion in 600s. Kill transfer
confirmed for both.

### K3: R7 on REPAIRED mechanism

PASS. ff2_fast_run1/2/3.txt: Z ans=105; COMP-SEGS n=2 [26 39] = [N,P]
(the N and P MAP ids from R7-IDS); LINK14 from MAP_Z(119) only to 26
and 39 (no LINK14 119 -> M(13)); no type-15 N(26) -> M(13) aux=0;
R7-DUP15=0. R7-FALSE14=0 R7-FALSE15=0 R7-DUP15=0, R7-RESULT=PASS.

### K4: R4B on REPAIRED mechanism terminates within 300s, ans=-2

FAIL on the 300s wall-clock bar as literally specified. Two `timeout 300`
runs killed (exit 124) with the Z query incomplete. A completion run (no
wall timeout) confirmed the composition repair itself terminates:
compose_try finished with COMP-FAIL (clean decline), COMP-STAT tried=112
rejected=112, at ~275s CPU; the run then continued into t2_trial
(frozen base) which had consumed 300s+ CPU without finishing at last
check. The R4b blowup mechanism is fixed: branch probe on the repaired
build shows n=2 admitted at 9001 (PROBE-KIND1=2 KIND2=0) vs n=28 on
the unfixed build. The DFS is finite and complete; it is not a hang.
- The 275s CPU for the decline DFS comes from per-node 4096-edge scans
  (cl_candidates outer scan + per-mark cl_extract mark-entry scan +
  dep_fact scan + cb_has_couse scan). The author's cl_build_cache (scan
  once, not per node) was the intended fix for exactly this cost but was
  never wired into cl_satisfy and does not compile as committed.
  Amendment 1's "terminates in seconds" estimate was wrong by ~2 orders
  of magnitude.
- After composition declines, the standard ev_query pipeline continues
  (t2_trial, bootstrap_miss, miss_inquire); t2_trial on the dense
  layered graph is itself slow (frozen base code, not the repair).
- Machine contention: loadavg ~9-11 on 2 CPUs throughout; the process
  received ~10-14% CPU (36-41s user per 300s wall). Even at full CPU the
  composition DFS alone (~275s CPU) plus t2_trial exceeds the 300s wall
  bar.

Exact mechanism of the miss: per-node O(4096) edge-store scans in
cl_candidates/cl_extract/dep_fact/cb_has_couse, unamortized across the
~511 DFS node visits of the decline. No candidate was wrongly admitted
(branching is 2/node as designed); no bound failed to hold. The miss is
performance, not correctness: the repair terminates with the correct
decline, too slowly for the frozen 300s bar.

### K5: R4C on REPAIRED mechanism terminates within 300s, ans=9008

FAIL on the 300s wall-clock bar as literally specified. ff2_r4c_run1.txt:
`timeout 300` kill (exit 124); training completed (28 facts+maps, correct
path trained last, final hop 9601->9008), R4C-Z-START, no completion in
300s. Same cost structure as R4B (the R4C DFS explores in edge-id order
with the correct-path MAPs trained last, so it traverses nearly the full
decline tree before reaching the answer). The composition repair itself
is sound (R4B probe: branching 2/node, finite DFS, clean decline); the
miss is the per-node scan cost against the 300s wall bar.

### K6: R6A-DEDUP: zero duplicate type-15 triples

PASS. ff2_fast_run1/2/3.txt: R6A-WRITE w1=1 w2=0 w3=0 (double
cb_couse_link probe writes exactly one edge); R6A-Z ans=103;
R6A-DUP15=0; R6A-RESULT=PASS.

### K7: R3 still PASS (ans=306)

PASS. ff2_fast_run1/2/3.txt: R3-ZA ans=306, R3-RESULT=PASS.

### K8: C234 battery on REPAIRED mechanism

PASS. ff2_c234_run1/2/3.txt (3/3 byte-identical, sha256
4c898771fdaafe79a7bd0c0daa3faf247cbbde742fe7102a945e0e94e0b4ad5a):
byte-identical to the C234 baseline cl_run1/2/3.txt (same digest).
T1 ans=107 segs (13 26 39); T2A ans=109 segs (13 26 39 52);
T2B ans=111 segs (13 26 39 52 65); T3 ans=105 segs (27 42);
T4 ans=-2 terminates (matches C234: partial applicability fails with
no false positive); T5 ans=-2 terminates; T4B ans=106 segs (45 58).
Zero regression vs C234.

### K9: 3/3 runs byte-identical stdout per binary (SHA-256 recorded)

- ff2_fast_bin: 3/3 identical,
  3acef38e9281f8e77e0df04c1f953e5d5ae2d695ca235ebb3d72d13406072216. PASS.
- ff2_vr7_bin: 3/3 identical,
  7fe32b422fafe67799979ce8dc256a8e271fc3bb74d024011e52351a9981abd3. PASS.
- ff2_c234_bin: 3/3 identical,
  4c898771fdaafe79a7bd0c0daa3faf247cbbde742fe7102a945e0e94e0b4ad5a. PASS.
- ff2_r4b_bin / ff2_r4c_bin: timeout-300 runs killed (exit 124); no
  completions to compare. Determinism of the terminating binaries is
  established above.
- ff2_vr4b_bin / ff2_vr4c_bin: single 600s timeout demonstrations per
  K2 (the bar specifies one 600s non-termination demonstration each;
  pre-timeout output is deterministic).

### K10: architecture audit

- compose_try: exactly 1 definition (ff_patch.zag), exactly 1 call site
  (ev_query, line 414). PASS.
- COMPOSE_MODE: 0 occurrences in patch and full builds. PASS.
- modes/bridges/handlers: 0 (only the header comment stating zero).
  PASS.
- New semantic cases: 0. New edge types: 0 (uses 15/14/6/8, all
  pre-existing). New node tags: 0 (20/101/102/1, all pre-existing).
  PASS.
- Whole MAP DFS remnants: 0; cl_dfs is fragment DFS only; whole MAPs
  enter only as (m,0,L) marks. PASS.
- Candidate enumeration consults only type-15 FRAG marks (aux != 0);
  co-use discrimination only on aux == 0 edges (cb_has_couse checks
  eg(...,12)==0). PASS.
- `expected` token: used only as the query target (compose_try
  expected<0 decline; cl_dfs nv==expected termination;
  t2_try_verify). Never as learning supervision. PASS.
- Dash audit: PREREG.md, both amendments, NAMECHECK.md, REPORT.md clean
  per worker_snippets/check_no_dash.sh. PASS.

### K11: process

PASS. Safebin toolchain guard recorded in NAMECHECK.md Step 0 (fresh
guard by this worker); `which python3 python` empty; pure Zag for all
research computation. One accidental `python3 -c` probe failed to
resolve (no interpreter in safebin PATH; nothing executed); disclosed
in NAMECHECK.md.

## 3. Final patch vs embedded build: behavioral identity

The final ff_patch.zag differs from the 16:12 embedded version by
exactly one hunk: the dead cl_build_cache function (plus the
one-line type fix). The function has zero call sites; the executable
path is byte-identical. Empirically: R7/R3/R6A on the final patch
reproduce the embedded build's passes exactly (same answers, same
segment MAP ids, same edge tables), and the C234 battery is
byte-identical to the C234 baseline.

## 4. R4B/R4C termination analysis

The R4b/R4c kill is the composition DFS branching blowup: unfixed,
every 1-link MAP is fallback-admitted at every node (branch probe:
n=28 at 9001), 28^8 paths, non-terminating (K2: 600s timeouts).
Repaired, admission is relation-relevant: branch probe shows n=2
(KIND1=2, KIND2=0), 2^8 = 256 paths, finite DFS. The repaired
compose_try terminates with a clean decline (COMP-FAIL, tried=112
rejected=112). Termination is proven by construction (iterative DFS
over a finite tree, bounded depth 8, bounded candidates) and observed.

The 300s bars are missed on performance, not termination: the decline
DFS costs ~275s CPU from unamortized per-node O(4096) edge-store scans,
and the post-composition t2_trial (frozen base) adds 300s+ CPU on the
dense layered graph. The bars measure wall-clock on a shared VM at
load ~10; the mechanism needs a scan-amortization fix (the unwired
cl_build_cache) to meet them.

## 5. Verdict

BUILD-FAIL (INCOMPLETE). Per the frozen prereg, any bar missed is
BUILD-FAIL.

Passing: K1 (V-R7 kill transfer reproduced), K2 (V-R4B/V-R4C 600s
non-termination), K3 (R7 repaired: ans=105 via [N,P], no false LINK14/
type-15, zero dup15), K6 (R6A-DEDUP: zero duplicates, single write),
K7 (R3 ans=306), K8 (C234 battery byte-identical to baseline, zero
regression), K10 (architecture audit: 1 compose_try, 0 modes/bridges/
handlers, 0 new edge types/tags/semantic cases, expected-as-target
only, dash-clean), K11 (pure Zag, safebin guard).

Failing: K4 (R4B did not terminate within 300s wall; composition DFS
takes ~275s CPU, full query slower), K5 (R4C did not terminate within
300s wall; same cost structure). K9 partially: 3/3 byte-identical for
ff2_fast_bin, ff2_vr7_bin, ff2_c234_bin with SHA-256 recorded; single
demonstrations for the timeout binaries per K2's spec.

The repair is CORRECT but too SLOW for the frozen performance bars:
(a) R7's false-provenance kill is fixed (gated fallback); (b) R4b/R4c
branching is bounded (2/node walk-admitted, 0 fallback-admitted;
28^8 becomes 2^8, finite DFS, clean decline); (c) type-15 dedup holds.
What fails is wall-clock: per-node O(4096) edge-store scans
(cl_candidates/cl_extract/dep_fact/cb_has_couse) unamortized across the
decline DFS, plus t2_trial costs in the frozen base, plus VM contention
(load ~10 on 2 CPUs). The author's cl_build_cache (scan-once cache) was
the intended performance fix but was never wired in and did not compile
as committed.

Recommended next step (not taken here; would be new work): wire the
mark/rels cache into cl_satisfy per the frozen design's performance
intent, re-verify K4/K5 against the unchanged 300s bars. Do not weaken
the bars.
