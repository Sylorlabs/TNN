# PREREG: H3-LEARNER-REFERENCE (frozen 2026-10-03)

Non-ledger task; claim minting paused. Parent: H3-EVICTION-REVERSIBILITY
follow-up (a): a learner-authored reference body installed post-release.

## Background

All composites in the H3 arc so far were installed by the privileged
harness function `install_composite` (worker in a second hat): a direct
write of worker-hardcoded (ckey, cval) pairs into free pool slots,
bypassing the learner's write machinery entirely (no primary-table
lookup, no conflict accounting, no displacement, hardcoded values).
The hazard predicate `count_hazard` = over release-trace entries:
released(k) AND has_live_ref(k), where `has_live_ref` scans ONLY the
pool (base 2112, 32 slots) for the frozen reference pattern
(900000<=value<910000, value-900000==k).

## Frozen operational definition of "learner-authored"

"Learner-authored" in this lane means ALL of:

(a) DERIVED FROM LEARNER STATE: `learner_author_composite` reads the
    learner's own white-box release trace (base 2880) and computes
    each composite reference value as 900000+k from the trace key k.
    No worker-hardcoded composite values; had the trace released
    different keys, the composites would reference different keys.
(b) ROUTED THROUGH LEARNER MACHINERY: installation uses the learner's
    generic write path `mem_write` (primary-table placement, linear
    probing, conflict counting, owner bits, stamps); W20 additionally
    uses the learner's own conflict/displacement path (`relocate`).
    `install_composite` is NOT called in the new worlds.
(c) POST-RELEASE EPISODE: authoring happens after the pass-1 guarded
    release decision (rel1=8), in a `learner_*` routine with the same
    simulated-learner standing as `learner_scratch`/`learner_revise_r`.

NOT claimed (frozen honesty boundary):

- The reference ENCODING (value-900000==key) remains the frozen
  substrate convention defined by the worker; the learner did not
  invent it.
- The learner remains SIMULATED; the episode routines are
  worker-written. This lane is a mechanism-route comparison, not a
  demonstration of an autonomous learner inventing reference
  structures. A genuinely learner-invented reference body remains
  untested after this lane.
- Learner-issued eviction remains untested (still the harness
  `evict_composite` hook; not exercised in this lane).

## Scientific question

Does the hazard depend on the privileged install path (artifact
hypothesis) or on pool state alone (state-predicate hypothesis)?

- W19 LEARNREF-PRIMARY: author 8 composites via generic `mem_write`
  (keys 8101..8108, values derived from trace), then run the second
  guarded consolidate (canonized gate, unmodified).
- W20 LEARNREF-DISPLACE: author 8 composites via `mem_write`, then a
  second learner wave revises the composite keys (new values
  960001..960008, outside the reference band), forcing 8 same-key
  conflicts whose `relocate` displaces the old reference bodies
  (905001..905008) into the pool. No recheck.

Frozen rationale:

- W19: fresh keys install into the primary table (linear probe on
  hash collision; no conflict since keys are fresh); the pool is
  untouched; `has_live_ref` scans pool only, so hz_live=0. The
  second consolidate iterates pool slots only, so its behavior must
  be identical to the evicted world EVREV-W18 (pool state identical:
  8 released slots, no pool references) on every field except
  hz_live.
- W20: the 8 revision conflicts displace (8101..8108, 905001..905008)
  into pool slots 8..15 (policy 8, first-free-slot scan; pool never
  fills: 16/32 used). `has_live_ref` fires per entry exactly as with
  the harness install, so hz_live=8. The route cost is visible in
  cf=16 (8 revision + 8 composite-revision conflicts) vs EVREV-W16's
  cf=8.

## Frozen predictions

| cond          | cf | ev | drop | rel1 | rel2 | av | ai | ar | lc | hz_live | hz_post | trspack  | dvsum   | dvmatch |
|---------------|----|----|------|------|------|----|----|----|----|---------|---------|----------|---------|---------|
| LEARNREF-W19   | 8  | 0  | 0    | 8    | 8    | 16 | 0  | 0  | 12 | 0       | 0       | 22222222 | 7240036 | 8       |
| LEARNREF-W20   | 16 | 0  | 0    | 8    | 0    | 8  | 0  | 0  | 12 | 8       | 8       | 22222222 | 7240036 | 8       |

dvsum = sum of the 8 derived reference values (905001+...+905008 =
7240036). dvmatch: W19 = primary composites reading back the derived
value via mem_read (owner 1); W20 = pool slots holding a derived
reference value.

## Kill bars (frozen)

- L0 IDENTITY: all pre-existing COND lines byte-identical to
  h3_eviction_reversibility/run1.txt; 3/3 runs byte-identical;
  source diff against h3_eviction_reversibility.zag shows ONLY the
  frozen delta (lane header/tag, learner_author_composite,
  learner_revise_composite, pool_has_val, run_learnref_wx, 2 main
  call sites, L-bar checks, verdict line). Not VOID.
- L1 AUTHOR-PRIMARY-NO-HAZARD: W19 hz_live=0 AND dvmatch=8 AND
  dvsum=7240036. The generic write route places 8 live composites
  whose reference bodies never reach the pool-scoped predicate.
- L2 AUTHOR-PRIMARY-INVISIBLE: W19 row field-equal to EVREV-W18's
  row on cf, ev, drop, rel1, rel2, av, ai, ar, lc, hz_post,
  trspack; hz_live differs (W19: 0, W18: 8). The primary-resident
  learner-authored composite is invisible to the guard and the
  second consolidate.
- L3 AUTHOR-DISPLACE-HAZARD: W20 hz_live=8 AND dvmatch=8 AND
  dvsum=7240036. The learner's own displacement machinery
  re-creates the hazard exactly.
- L4 ROUTE-COST-SIGNATURE: W20 cf=16 (vs EVREV-W16 cf=8), ev=0,
  drop=0. Same hazard as the harness route, different route cost.
- L5 CLEAN: W19/W20 ai=0, ar=0, lc=12.
- L6 DETERMINISM: 3/3 runs byte-identical (sha256 recorded in
  REPORT.md).

## Constraints (frozen)

- Pure Zag; safebin mandatory; no forbidden executables.
- The canonized guarded consolidate is NOT modified (test only;
  if broken, report, don't fix).
- Prereg committed alone, strictly before implementation, build,
  and runs (commit-order self-check). No amendments after any
  result is seen.
- Commits local with explicit pathspecs; never push.
