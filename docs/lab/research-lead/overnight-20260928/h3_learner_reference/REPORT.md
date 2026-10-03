# REPORT: H3-LEARNER-REFERENCE (learner-authored reference body probe)

Date: 2026-10-03. Worker: H3-LEARNER-REFERENCE worker
(non-ledger task; claim minting paused).
Prereg: committed alone as 5216c07e0 (strictly before
implementation, build, and runs). No amendments.

## Verdict: LEARNER-REFERENCE-PASS (L0..L6 all hold)

3/3 runs byte-identical (sha256
937790f23d648f86d8f244f4ccaf3a0be700b7138064be55697edf17b5a52439).
Binary sha256
abb6d70acc6e37efb7e90acdbdd51b360e8c9081b316949152b1f9f74ff88cf9.
Source sha256
e0e48f6b271403b3d13e5a8f4c92adbf24ea1f266a5029c82c5c1227fa86c3a4.

The parent's remaining open follow-up (a) is EXECUTED. What it
establishes -- and what it does not -- is stated first, because the
learner/harness distinction is the whole point of this lane.

## What "learner-authored" means here (read this before the verdict)

In this lane "learner-authored" means all of, and only:

(a) DERIVED FROM LEARNER STATE: `learner_author_composite` reads the
    learner's own white-box release trace and computes each composite
    reference value as 900000+k from the trace key k. No
    worker-hardcoded composite values; dvsum=7240036 and dvmatch=8
    confirm the bodies reference exactly the released keys.
(b) ROUTED THROUGH LEARNER MACHINERY: installation goes through the
    learner's generic write path (`mem_write`: primary-table
    placement, linear probing, conflict counting, owner bits,
    stamps); W20 additionally through the learner's own
    conflict/displacement path (`relocate`). `install_composite`
    is NOT called in the new worlds.
(c) POST-RELEASE EPISODE: authoring happens after the pass-1 guarded
    release decision, in a `learner_*` routine with the same
    simulated-learner standing as `learner_scratch`/`learner_revise_r`.

What is NOT established, and must not be claimed:

- The reference ENCODING (value-900000==key) remains the frozen
  substrate convention defined by the worker. The learner did not
  invent it.
- The learner remains SIMULATED; the episode routines are
  worker-written code in a third hat. This lane is a
  mechanism-route comparison, not a demonstration of an autonomous
  learner inventing reference structures. A genuinely
  learner-invented reference body -- created by a real learner that
  was never told the encoding -- remains UNTESTED after this lane.
  Nothing in this report should be cited as "the learner authored a
  reference body" without that qualification.
- Learner-issued eviction remains untested.

## Results (identical across run1/run2/run3)

| cond        | cf | ev | drop | rel1 | rel2 | av | ai | ar | lc | hz_live | hz_post | dvsum   | dvmatch | trs              |
|-------------|----|----|------|------|------|----|----|----|----|---------|---------|---------|---------|------------------|
| LEARNREF-W19 | 8  | 0  | 0    | 8    | 8    | 16 | 0  | 0  | 12 | 0       | 0       | 7240036 | 8       | 2222222222222222 |
| LEARNREF-W20 | 16 | 0  | 0    | 8    | 0    | 8  | 0  | 0  | 12 | 8       | 8       | 7240036 | 8       | 22222222         |

Every measured row matches the frozen prereg predictions exactly.
The 60 pre-existing COND lines are byte-identical to
h3_eviction_reversibility/run1.txt, and the in-band
GUARDED-SEALED-VERDICT=PASS, CHURN-INTERACTION-VERDICT=PASS,
RELEASE-CHURN-VERDICT=PASS, POSTREL-COMPOSITE-VERDICT=PASS,
SECOND-CONSOLIDATE-VERDICT=PASS, and
EVICTION-REVERSIBILITY-VERDICT=PASS still hold, so the new worlds
caused no regression. The guarded consolidate was NOT modified.

Kill bars (in-band + external, all 3 runs):
- L0 IDENTITY: HOLD. diff of run1.txt against
  h3_eviction_reversibility/run1.txt shows ONLY the expected
  differences: the LANE= tag line, the 2 new COND=LEARNREF-W19/W20
  lines, the 5 new L1..L5 in-band check lines, and the
  LEARNER-REFERENCE-VERDICT= line (9 diff lines, all in the expected
  categories). 3/3 runs byte-identical. diff of
  h3_learner_reference.zag against
  h3_eviction_reversibility/h3_eviction_reversibility.zag shows only
  the frozen delta: lane header comment, LANE= tag, the
  learner_author_composite / learner_revise_composite /
  pool_has_val routines, the run_learnref_wx runner, 2 main call
  sites, L-bar checks, verdict line. Every mechanism function body
  byte-identical. Not VOID.
- L1 W19-AUTHOR-PRIMARY-NO-HAZARD: HOLD (rel1=8, hz_live=0,
  dvsum=7240036, dvmatch=8, cf=8, rel2=8, av=16, hz_post=0). Eight
  live composites authored by the learner's own machinery, with
  reference bodies derived from its own trace, do NOT re-create the
  hazard -- because the generic write path installs fresh keys into
  the PRIMARY table, and the reference leg of the hazard predicate
  (has_live_ref) scans the pool only. The difference from the
  harness-written route is the installation LOCATION, not a
  sanitizing property of authorship.
- L2 W19-INVISIBLE-TO-GUARD: HOLD. Programmatic field-by-field
  comparison confirms W19's row equals EVREV-W18's row on every
  shared field (cf, ev, drop, rel1, rel2, av, ai, ar, lc, hz_post,
  trspack); only hz_live differs (W19: 0, W18: 8). The
  primary-resident learner-authored composite is invisible to the
  guard and to the second consolidate: the gate's statelessness
  re-fires all 8 releases (rel2=8) exactly as in the evicted world.
- L3 W20-AUTHOR-DISPLACE-HAZARD: HOLD (rel1=8, hz_live=8,
  dvsum=7240036, dvmatch=8, rel2=0, av=8, hz_post=8, cf=16). When
  the learner's own revision/displacement machinery places the
  authored reference bodies in the pool (8 same-key conflicts,
  relocate into pool slots 8..15, pool never fills), the hazard
  re-creates EXACTLY as with the harness install (hz_live=8).
- L4 W20-ROUTE-COST-SIGNATURE: HOLD (W20 cf=16 vs EVREV-W16 cf=8;
  ev=0, drop=0). Same hazard as the harness route, different route
  cost: the 8 extra conflicts are the observable signature of the
  learner-machinery route (8 revision + 8 composite-revision).
- L5 CLEAN: HOLD (ai=0, ar=0, lc=12 in W19/W20).
- L6 DETERMINISM: HOLD (3/3 byte-identical).

In-band LEARNER-REFERENCE-VERDICT=PASS in all 3 runs; the governing
verdict is this external check.

## What this establishes

1. The hazard is a STATE predicate, not a route artifact. Before
   this lane, every hazard observation in the H3 arc used the
   privileged `install_composite`; a skeptic could argue the hazard
   was an artifact of that privileged path. W20 kills that: the
   learner's own write/displacement machinery reproduces the hazard
   exactly (hz_live=8, per-entry pattern match confirmed by
   dvmatch=8), with no privileged install anywhere in the world.
2. The route determines REACHABILITY, not the predicate. W19 shows
   the learner's generic write path alone cannot place reference
   bodies where the predicate scans: composites land in primary,
   the pool is untouched, hz_live=0, and the guard behaves exactly
   as in the evicted world. Authorship through learner machinery is
   not inherently "safe"; placement is what matters, and on this
   substrate only displacement (or privileged install) reaches the
   pool.
3. The sealed ordering/decision/reversibility matrix is now closed
   on the authorship axis too: harness-written post-release
   composites re-create the hazard (POSTCOMP); learner-machinery
   post-release composites re-create it identically once pooled
   (W20); learner-machinery composites that never reach the pool do
   not (W19); eviction reverses the pooled hazard per entry (EVREV).

## Honest caveats

- "Learner-authored" here = trace-derived + learner-machinery-routed
  (see the definition section above). The learner remains simulated;
  the reference encoding is worker-defined; the episode is
  worker-written. A genuinely learner-invented reference body
  remains untested -- this is the residual open item, and it cannot
  be closed on this simulation substrate, only on a substrate with a
  real learner.
- The adversary/author is the worker in a third hat (same
  procedural seal as the parent lanes). W19/W20 were specified in
  the prereg before implementation.
- The guarded consolidate was NOT modified in this lane (test
  only, per the task constraint).
- The eviction in this arc remains harness-issued; whether the
  learner itself would ever evict its composite is not tested.
- Non-ledger task: no claims minted.

## Toolchain guard

Safebin active for the whole lane; `which python3` and `which
python` return nothing under that PATH (verified 2026-10-03
before the prereg commit); no forbidden executable invoked at any
point (shell used only for mkdir, file writes, znc invocation,
binary execution, sha256sum, cmp, diff, grep, git ops). No
PROCESS-FAIL condition triggered. Pinned znc verified
byte-identical to src/tools/toolchain/znc_linux_x86_64_abed8aa1
before the prereg commit (sha256
498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef).
Build ran in foreground (zagd unavailable warning only), first
try, no defect symptoms; `-o h3_learner_reference_bin` used for
the output name. New-code audit: no negated-conjunction while
conditions, no `as *i32` slice construction, no `[]u8 as *u8`
casts, zero `!(` in new code, if-nesting at most 2 in new code
(L2 rewritten from a loop to explicit comparisons during
implementation, before any build). Git writes via /usr/bin/git
directly (safebin git symlink EPERM lesson); explicit pathspecs;
no git reset; local only, never pushed.

## Commits

- 5216c07e0: frozen prereg (PREREG.md + NAMECHECK.md), alone,
  strictly before implementation, build, and runs.
- This commit: h3_learner_reference.zag (source sha256
  e0e48f6b271403b3d13e5a8f4c92adbf24ea1f266a5029c82c5c1227fa86c3a4;
  diff against h3_eviction_reversibility/h3_eviction_reversibility.zag
  shows only the frozen delta), h3_learner_reference_bin (sha256
  abb6d70acc6e37efb7e90acdbdd51b360e8c9081b316949152b1f9f74ff88cf9),
  build.err, run1/2/3.txt, run1/2/3.err, REPORT.md. Local only,
  never pushed.

## Follow-ups for the parent

- Follow-up (a) is EXECUTED and CLOSED as a route comparison:
  LEARNER-REFERENCE-PASS (L0..L6). A learner-machinery-authored
  reference body re-creates the hazard exactly once its bodies
  reach the pool (W20: hz_live=8); the generic write path alone
  does not reach the pool and leaves the guard landscape identical
  to the evicted world (W19 == W18 except hz_live).
- Residual open item (honest, cannot be closed on this substrate):
  a GENUINELY learner-invented reference body -- a real learner
  inventing the reference encoding itself, never told
  value-900000==key. The H3 simulation substrate has no autonomous
  learner; this stays open by construction.
- Untouched by this lane: learner-issued eviction (still the
  harness evict_composite hook).
