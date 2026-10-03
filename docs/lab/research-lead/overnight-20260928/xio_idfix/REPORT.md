# REPORT.md -- XIO-IDFIX: generation-checked stage binding (A4c repair)

## Verdict: XIO-IDFIX-COMPLETE

The A4c KILL from XIO-REDTEAM-COMPLETE (commit 64d12b79f) is repaired.
All six preregistered kill bars (PREREG.md, committed 53bb4e9ae
before implementation) PASS. No bar was weakened or moved.

## Repair

Adapter stages are now bound by (id, generation-token), not bare id.

- Token = (promotion-index << 10) | graph-root-id, computed from the
  stage MAP node's write-once fields: ng(W,m,24) (frozen promotion
  index, written once by `promote_graph`) and ng(W,m,20) (executable
  graph root, never rewritten; old graph cells are never freed on
  MAP deletion or eviction, so a recycled id's new graph always takes
  fresh cell ids). hg(W,24) is a live-edge count audited to stay in
  [0,4096]; root < 1024; token < 2^23, always >= 0.
- Recorded per stage in the adapter->stage type-1 DEP binding edge's
  clk field at `xio_build` time. No adapter node layout change; the
  XIO-BUILD emit line is unchanged.
- `xio_exec` compares the recorded token against the live MAP's token
  after the existing liveness+tag checks. On mismatch it emits
  `XIO-INVALID id=<a> stage=<1|2>`, deactivates the adapter, and
  returns -999999 (fail closed). A missing binding edge also fails
  closed. Specified semantics: STRICT identity, even a structurally
  identical re-promotion invalidates; the learner rebuilds via
  verified `xio_try` if the composition still holds.

Source delta: xio_core.zag (unfrozen) only, +2 functions, +2 changed
`link_edge` calls, +1 check block in `xio_exec`. Frozen base
(xio_full.zag lines 1-1677) byte-untouched (cmp verified). 0 modes /
0 bridges / 0 handlers / 0 new core semantic cases. Pure Zag under
safebin PATH (guard in NAMECHECK.md Step 0; `which python3 python`
empty). Zero em/en dashes.

## Test results

T1 A4c retest (K1: PASS). Pre-recycling output is line-for-line
identical to rt_run1.txt (same XIO-BUILD id=380 m1=27, same probes),
proving the repair changes nothing on the happy path. Post-recycling:
token probe 13328 (recorded) vs 261513 (live), `XIO-INVALID id=380
stage=1`, no XIO-REUSE on the stale adapter, post-census adapters=0.
The silent rebinding is now a loud invalidation. The base trial's
own post-recycling behavior (masked/unmasked 70 via trial paths) is
byte-identical to the red-team run: unchanged, out of scope per
prereg (root cause #3, first-valid masked teaching).

T2 C229 regression (K2: PASS). Repaired core + verbatim original
xio_driver: 3/3 runs byte-identical to the committed
xio_adapters/xio_run1.txt (sha256
3b10e33ebdbb99d6826b945cd6ffbcb35c99ed17a6f4da3a84fb26d0325c9e98).

T3 C235 regression (K3: PASS). Repaired core + verbatim original
xhio_driver: 3/3 runs byte-identical to the committed
xio_harder/xhio_run1.txt (sha256
6909ba0c576b3204c110e259411cbb71970f3caa39912f812a2d7761188ab51a).

T4 A4 bound preserved (K4: PASS). Verbatim rt_a4 port: 4a
revised-serve=3, rec-ans-now=2 (stale audit field), old-answer=-2;
4b del-m2 old-ans=-2, orphan persists (adapters=1) serving nothing,
relearn=3. The 4b path fails the liveness check before the
generation check, so orphan behavior is exactly preserved.

T5 identical re-promotion (K5: PASS). Targeted deletion of m1 only,
then a structurally identical chain MAP re-promoted onto id 27 with
the same (oty=0, rel=81) signature the old code would have silently
rebound: tokens 13328 vs 234879, `XIO-INVALID id=380 stage=1`, no
XIO-REUSE, census adapters=0. Pins the strict-identity semantics.
(The trial correctly re-derives 34 via rebind using the legitimate
new MAP; only the stale adapter is dead.)

K6 hygiene (PASS). Frozen base cmp-identical in all three
assemblies; no em/en dashes; no new modes/bridges/handlers; 3/3
byte-identical idfix runs (sha256
b6a1dce5557b6cdbb1075de95641e5f1e2d46c63761610a9dbcbaa07186d9c90).

## Residual bounds (not repaired, per prereg)

- Stale DEP edges shadowing `xio_dep_rel` (red-team candidate #3):
  unchanged; with the adapter invalidated on recycling, stale edges
  no longer affect adapter execution.
- First-fit id recycling in frozen `alloc_node`: unchanged.
- Masked-trial first-valid teaching poisoning the query relation
  (A4c root cause #3): base-trial behavior, unchanged.
- Token collision: a missed rebinding needs a simultaneous
  (promotion-index, graph-root) collision on the recycled id; the
  root-id half cannot collide through the deletion/eviction paths
  because old graph cells are never freed.

## Deliverables (all in xio_idfix/)

- PREREG.md (frozen, committed 53bb4e9ae before implementation)
- NAMECHECK.md (toolchain guard Step 0, scope, Zag notes)
- REPORT.md (this file)
- xio_core_fixed.zag (repaired core; diff vs xio_core.zag is the
  repair and nothing else)
- idfix_driver.zag (T1/T4/T5 driver, unfrozen, new)
- idfix_full.zag, idfix_c229.zag, idfix_c235.zag (assemblies:
  frozen base lines 1-1677 + repaired core + driver)
- idfix_bin, idfix_c229_bin, idfix_c235_bin (pinned znc builds)
- idfix_compile.txt, idfix_c229_compile.txt, idfix_c235_compile.txt
- idfix_run1/2/3.txt (3/3 byte-identical), idfix_c229_run1/2/3.txt,
  idfix_c235_run1/2/3.txt (3/3 each, matching committed hashes)

Committed locally with explicit pathspecs. Nothing pushed. The
original xio_adapters/ and xio_harder/ trees are untouched; promotion
of the repaired core into them is a parent-orchestrator decision.

No em dashes were used in this report (verified).
