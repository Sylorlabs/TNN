# PREREG.md -- XIO-IDFIX: generation-checked stage binding (A4c repair)

Frozen before implementation. Commit of this file strictly precedes the
implementation commit. Any deviation amends transparently and re-freezes.

## 1. Target

Repair the A4c KILL from XIO-REDTEAM-COMPLETE (commit 64d12b79f):
"id recycling silently rebinds a stage". When a MAP id is recycled
(deleted MAP's id reused by a new MAP via first-fit `alloc_node`), an
existing adapter's stage reference silently rebinds to the new MAP:
`xio_exec` checks only liveness (field 36) and tag (field 0 == 20),
both of which the new occupant passes. Recorded provenance
(o1=0, rel1=81) then describes a stage that is now (oty=1, rel=82).

A1 (type confusion) and A6 (oty vs sum) are out of scope: owned by the
XIO-generalization worker (H-XIO-4 prereg e08110f47).

## 2. Repair design (unfrozen xio_core only; frozen base byte-untouched)

Bind each stage by (id, generation-token), not bare id.

Token = (promotion-index << 10) | graph-root-id, where for a MAP node m:
- promotion-index = ng(W,m,24): written once by frozen `promote_graph`
  (= hg(W,24) at promotion). Verified never rewritten: `fr_set` touches
  only frame/register nodes (tag 902), never MAP nodes; no other
  field-24 write on tag-20 nodes exists in the base.
- graph-root-id = ng(W,m,20): written once at promotion, never
  rewritten. Old graph cells are never freed on MAP deletion
  (`rt_del_map_r` deactivates only the MAP node) or eviction
  (`rec_evict`/`evict_node` free no cells), so a recycled id's new
  graph always takes fresh cell ids.

Bounds: hg(W,24) is a live-edge count; all inc/dec sites audited
(link +1; decay/evict/edge-kill -1; init 0), so it stays in [0,4096].
Root id < 1024. Token < 2^23, fits i32, always >= 0.

Recording: the adapter already links one type-1 DEP edge per stage
(adapter -> m1, adapter -> m2) for provenance. The token is stored in
that edge's clk field (eg offset 12), which the base never reads or
writes for type-1 edges (decay touches type 9 only). No adapter node
layout change. XIO-BUILD emit line unchanged.

Check: in `xio_exec`, after the existing liveness+tag checks, compare
the recorded token (from the binding edge; -1 if the edge is missing)
against the live token (recomputed from the MAP node). On mismatch:
emit `XIO-INVALID id=<a> stage=<1|2>`, deactivate the adapter
(ns(W,a,36,0)), return -999999 (fail closed, `xio_adapt` returns -2).
A missing binding edge also fails closed (-1 never equals a live
token).

Specified semantics: STRICT identity. Any generation mismatch
invalidates the adapter, even if the replacement MAP is structurally
identical. A fresh promotion is a new evidentiary basis; the recorded
provenance refers to the original promotion event. The learner may
rebuild via verified `xio_try` if the composition still holds. There
is no silent rebind path, ever.

## 3. Exact source changes (xio_core.zag only, unfrozen)

New functions (inserted before `xio_build`):

```
fn xio_stage_tok(W:[]u8,m:i32)i32 {
  return ((ng(W,m,24))<<10)|(ng(W,m,20));
}
fn xio_bind_tok(W:[]u8,a:i32,m:i32)i32 {
  let e:i32=0;
  while(e<4096){
    if(eg(W,e,0)==a && eg(W,e,4)==1 && eg(W,e,8)==m){return eg(W,e,12);}
    e=e+1;
  }
  return -1;
}
```

`xio_build`: replace
```
  link_edge(W,a,1,m1,0);
  link_edge(W,a,1,m2,0);
```
with
```
  link_edge(W,a,1,m1,xio_stage_tok(W,m1));
  link_edge(W,a,1,m2,xio_stage_tok(W,m2));
```

`xio_exec`: after the liveness+tag checks, before stage execution,
insert
```
  if(xio_bind_tok(W,a,m1)!=xio_stage_tok(W,m1)){
    emit("XIO-INVALID id="); e64(a); emit(" stage=1\n");
    ns(W,a,36,0); return -999999;
  }
  if(xio_bind_tok(W,a,m2)!=xio_stage_tok(W,m2)){
    emit("XIO-INVALID id="); e64(a); emit(" stage=2\n");
    ns(W,a,36,0); return -999999;
  }
```

No other function changes. No signature changes. No new modes,
bridges, handlers, or core semantic cases. The frozen base
(xio_full.zag lines 1-1677) is not touched.

## 4. Assembly (all in xio_idfix/)

- xio_core_fixed.zag: repaired core (this prereg's section 3 applied
  to xio_adapters/xio_core.zag, sha256
  4d4d2e0e932b6a472e3cd8456d7e1c633218e611ce5df51d03507218440a8a7f).
- idfix_driver.zag: new driver with T1 (A4c retest), T4 (A4 bound),
  T5 (identical re-promotion); each test on a fresh learner.
- idfix_full.zag = xio_full.zag lines 1-1677 (frozen, byte-identical)
  + xio_core_fixed.zag + idfix_driver.zag.
- idfix_c229.zag = lines 1-1677 + xio_core_fixed.zag
  + xio_full.zag lines 1925+ (original C229 driver, verbatim).
- idfix_c235.zag = lines 1-1677 + xio_core_fixed.zag
  + xhio_full.zag lines 1925+ (original C235 driver, verbatim).

## 5. Tests and kill bars

T1 (A4c retest, K1): verbatim port of rt_a4c against the repaired
core, plus token probes (recorded vs live token per stage). The
pre-recycling output must match rt_run1.txt lines 109-121 exactly,
including `XIO-BUILD id=380 m1=27 m2=115 o1=0 o2=1 rel1=81 rel2=82
qr=93 mid=34 ans=2`, `A4c ad=380 m1=27 rec-o1=0 live-oty(m1)=0`, and
`A4c newmap=27 ad.m1=27 rec-o1=0 live-oty(ad.m1)=1
live-deprel(ad.m1)=81` (allocation order is unchanged by the repair).
Post-recycling, K1 PASS requires ALL of:
  (a) token probe shows recorded != live for stage 1;
  (b) the masked query emits `XIO-INVALID id=380 stage=1`;
  (c) no `XIO-REUSE id=380` line appears after recycling;
  (d) post-census shows adapters=0 (stale adapter deactivated).
The masked query's own return value is recorded, not a bar (it is
base-trial first-valid behavior, out of scope).

T2 (C229 regression, K2): idfix_c229 run stdout byte-identical to the
committed xio_adapters/xio_run1.txt
(sha256 3b10e33ebdbb99d6826b945cd6ffbcb35c99ed17a6f4da3a84fb26d0325c9e98).

T3 (C235 regression, K3): idfix_c235 run stdout byte-identical to the
committed xio_harder/xhio_run1.txt
(sha256 6909ba0c576b3204c110e259411cbb71970f3caa39912f812a2d7761188ab51a).

T4 (A4 bound preserved, K4): verbatim port of rt_a4. K4 PASS requires
the red-team BOUND behavior unchanged: 4a `revised-serve=3`,
`rec-ans-now=2`, `old-answer=-2`; 4b `del-m2 old-ans=-2`,
`adapters=1` (orphan persists, serves nothing), `relearn=3`.
(The 4b path fails the liveness check before the generation check,
so orphan behavior is exactly preserved.)

T5 (identical re-promotion, K5): build adapter as in T1, deactivate
only m1, rebuild a chain graph over the same facts (31,81,32..34) and
`promote_graph` it so first-fit reuses id 27 with the same
(oty=0, rel=81) signature the old code would silently rebind. K5 PASS
requires `XIO-INVALID id=<ad> stage=1`, no `XIO-REUSE` on the stale
adapter, post-census adapters=0. This pins the strict-identity
semantics: structural identity does not rebind.

K6 (hygiene): frozen base lines 1-1677 byte-identical before/after
(cmp); 0 modes/bridges/handlers/new core semantic cases; pure Zag
under safebin PATH (guard recorded in NAMECHECK.md Step 0); 3/3
byte-identical runs for idfix_full (sha256 recorded), and the
regression assemblies each run 3/3 with stdout matching the
committed hashes above.

Verdict XIO-IDFIX-COMPLETE iff K1-K6 all PASS. Any kill-bar failure
yields XIO-IDFIX-FAIL (no bar weakening; amend and re-freeze instead).

## 6. Out of scope (residual bounds, recorded not repaired)

- Stale DEP edges shadowing `xio_dep_rel` (red-team candidate repair
  #3): unchanged. With the adapter invalidated on recycling, stale
  edges no longer affect adapter execution.
- First-fit id recycling in frozen `alloc_node`: unchanged.
- Masked-trial first-valid teaching poisoning the query relation
  (A4c root cause #3): base-trial behavior, unchanged.
- Token collision analysis: a missed rebinding needs a simultaneous
  (promotion-index, graph-root) collision on the recycled id; the
  old graph cells are never freed, so the root-id half cannot
  collide through the deletion/eviction paths. Documented in REPORT.

No em dashes were used in this prereg (verified).
