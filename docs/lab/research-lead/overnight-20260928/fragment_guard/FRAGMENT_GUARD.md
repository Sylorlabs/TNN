# Fragment Guard Verification

Status: VERIFICATION-COMPLETE. Read-only inspection of the frozen
base. No implementation. No source modified.

Frozen base: `bootstrap_loop/bl_base.zag`
SHA-256: `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`

## 1. The spec's guard requirement

FRAGMENT_RECORD.md section 1.2 states:

> Every production scan that enumerates tag-20 nodes must skip fragment
> records unless it explicitly intends to read the fragment store. In
> particular:
>
> - The query path (`activate`, `ev_query`) must not treat a fragment
>   record as an answerable MAP. Guard: `ng(W,m,24) != -2` before any
>   MAP-shaped read.
> - `revise_on_contradict` dispatches on prov edges to MAPs; fragment
>   records carry no prov edges as targets (they are patterns, not
>   instantiated queries), so no guard is needed there, but the build
>   must verify this by inspection.

## 2. Census of tag-20 enumeration in the frozen base

Complete grep for tag-20 node scans in production code:

| Location | Function | Code | Field-24 check | Production? |
|----------|----------|------|----------------|-------------|
| bl_base.zag:690 | `revise_on_contradict` | `ng(W,m,36)==1 && ng(W,m,0)==20` | NO | YES |
| bl_base.zag:1281 | `t_t2_revise` (test) | `ng(W,n,0)==20 && ng(W,n,4)==40` | NO | NO (test) |

That is the entire census. Two locations. One is test code.

### 2.1 `activate` (line 140) does NOT enumerate MAPs

```zag
fn activate(W:[]u8,s:i32,r:i32)i32 {
  let best:i32=-1; let bb:i32=-1; let n:i32=2;
  while(n<1024){
    if(ng(W,n,36)==1 && ng(W,n,0)==1 && is_superseded(W,n)==0){
```

The scan condition is `ng(W,n,0)==1` (FACT nodes only). It never
examines a tag-20 node. A fragment record (tag 20) cannot be
returned by `activate` under any input.

### 2.2 `ev_query` (line 813) does NOT enumerate MAPs

`ev_query` calls, in order:
1. `activate` (tag-1 only, per 2.1)
2. `mp_run` -> `t2_trial` -> `t2_gather` (tag-1 only; line 453:
   `ng(W,n,0)==1`)
3. `bootstrap_miss` (tag-1 only; line 766: `ng(W,n,0)==1`)
4. `miss_inquire` (creates UNCERTAINTY + guide; no MAP scan)

None of these enumerate tag-20 nodes. `ev_query` cannot mistake a
fragment for a MAP because it never looks at MAPs.

### 2.3 `bootstrap_miss` CREATES a tag-20 node (line 777)

```zag
ns(W,m,0,20); write_node(W,m,0,hg(W,24),0,0);
```

This is the bootstrap-inference MAP. Field 24 is set to `hg(W,24)`
(the edge counter, always >= 0). It is NOT -2. The fragment marker
does not collide with this creation path.

### 2.4 `promote_graph` (line 533) CREATES tag-20 nodes

```zag
ns(W,m,0,20); ns(W,m,4,r); ns(W,m,8,s); ns(W,m,12,-1); ns(W,m,16,-1);
write_node(W,m,root,hg(W,24),ans,0);
```

Field 24 = `hg(W,24)` >= 0. Not -2. No collision.

## 3. The actual vulnerable location: `revise_on_contradict`

```zag
fn revise_on_contradict(W:[]u8,factn:i32,new_o:i32)void {
  let old_o:i32=ng(W,factn,28);
  if(old_o==new_o){return;}
  let m:i32=2;
  while(m<1024){
    if(ng(W,m,36)==1 && ng(W,m,0)==20){       // <-- NO field-24 check
      let e:i32=0; let hit:i32=0;
      while(e<4096){
        if(eg(W,e,0)!=-1 && eg(W,e,0)==m && eg(W,e,4)==1 && eg(W,e,8)==factn){hit=1;}
        e=e+1;
      }
      if(hit==1){t2_revise_graph(W,m,factn,old_o,new_o);}
    }
    m=m+1;
  }
  return;
}
```

This is the ONLY production function that enumerates tag-20 nodes.
It has NO field-24 guard.

### 3.1 Why fragments are currently safe here (by construction)

The inner check requires a type-1 (prov) edge FROM the MAP node TO
the contradicted fact:

```
eg(W,e,0)==m && eg(W,e,4)==1 && eg(W,e,8)==factn
```

Per the fragment spec, fragments carry:
- ET_FRAGUSE (type 14): FROM composite TO fragment (inbound, not
  outbound from the fragment)
- ET_FRAGSLOT (type 15): FROM fragment TO literal-holder
- ET_FRAGHIST (type 16): FROM fragment TO fact (read-only, not
  type 1)

A fragment has no outbound type-1 edges. The inner check
`eg(W,e,4)==1` will not match a fragment's type-15 or type-16
edges. Therefore `t2_revise_graph` will not be called on a
fragment, PROVIDED the build never creates a type-1 edge from a
fragment record.

### 3.2 Why the spec's "no guard needed" is fragile

The safety in 3.1 depends on a BUILD-TIME INVARIANT (fragments
never get type-1 edges), not on a production check. If any future
code path (extraction bug, splice bug, edge-rewiring bug) creates
a type-1 edge from a fragment to a fact, then on contradiction of
that fact:

1. `revise_on_contradict` would call `t2_revise_graph` on the
   fragment.
2. `t2_revise_graph` reads `ng(W,m,20)` as graph root (actually
   the fragment's topology root), `ng(W,m,8)` as s (actually -1),
   `ng(W,m,4)` as r (actually -1), `ng(W,m,28)` as answer
   (actually the F-shape signature).
3. It would then tombstone cells, insert a corrected step, and
   re-execute the FRAGMENT'S topology as if it were a live
   inference graph, then `ns(W,m,28,out)` would OVERWRITE the
   F-shape signature with the revision output.

This would corrupt the fragment store silently. The failure mode
is not a crash; it is silent corruption of F-shape signatures,
which would break the W6 dedupe (section 6.2 of the spec) by
making distinct fragments appear identical or identical
fragments appear distinct.

### 3.3 Recommended guard (1 line, defense in depth)

In `revise_on_contradict`, line 690:

```zag
// current:
if(ng(W,m,36)==1 && ng(W,m,0)==20){
// guarded:
if(ng(W,m,36)==1 && ng(W,m,0)==20 && ng(W,m,24)!=-2){
```

This makes the protection explicit and robust against any future
edge-type bug. Cost: one field read per live tag-20 node per
contradiction event. Contradictions are rare relative to queries
(DYN-1: 50 observes per 250 events). The cost is negligible.

This is a RECOMMENDATION for the future build's preregistration,
not a change to the frozen base.

## 4. Other paths that touch MAP-shaped data

### 4.1 `map_standing` (line 568): TEST ONLY

Callers at lines 1160, 1210, 1286, 1301 are all in test functions
(`t_p7`, `t_xcap`, `t_t2_revise`). Zero production callers.
`map_standing` reads field 24 as the promotion index; on a
fragment (field 24 = -2) it would count all type-2 minus type-3
edges (since `e >= -2` is always true). Semantically wrong, but
unreachable in production. If the future build calls
`map_standing` in production, it needs the guard.

### 4.2 `ev_act` (line 862): TAG-AGNOSTIC, latent risk

`ev_act` enumerates candidates via edges from POLICY_ROOT without
filtering by tag. It reads `ng(W,cand,4)` as the relation and
`ng(W,cand,20)` as the answer value. If a fragment were ever
linked to/from POLICY_ROOT:

- field 4 = -1 (would fail the ctx relation match, likely
  harmless)
- field 20 = graph root cell id (would be returned as an "action"
  value if selected, which is wrong)

The fragment design does not link fragments to POLICY_ROOT.
This is a LATENT RISK, not a current vulnerability. The build
should verify by inspection that no path links a fragment to
POLICY_ROOT, or add a tag check to `ev_act`.

### 4.3 `evict_node` (line 254): TAG-AGNOSTIC, no guard needed

Eviction selects by lowest `bid`, regardless of tag. Per the
fragment spec section 6.5, fragments are subject to the same
general eviction policy. No guard needed. `rec_evict` records
`(ng(W,n,20), ng(W,n,24), ng(W,n,28))` in the tombstone; for a
fragment this records (root, -2, signature), which is harmless
and arguably useful for audit.

### 4.4 `bid` (line 237): TAG-AGNOSTIC, safe

Counts event edges only. No MAP field reads. Safe for fragments.

### 4.5 `execute` / `t2_exec`: EXPLICIT ROOTS ONLY

These take an explicit graph root and walk cells (tags 101-104).
They never enumerate MAPs. A fragment's topology cells are valid
executable cells (copied from a walked trace), so `execute` would
technically run on a fragment root, but no production path passes
a fragment root to `execute`. The fragment selection path (future
build) reads fragments directly and splices their cells; it does
not `execute` the fragment in place.

### 4.6 `fr_set` field-24 writes (line 175): NO COLLISION

`fr_set` writes to field 24 of graph CELLS during execution
(frame slot 1). Cells are tags 101-104, not tag 20. The fragment
marker is only meaningful on tag-20 nodes. The guard
`ng(W,m,24)!=-2` must only be applied where `ng(W,m,0)==20` is
already established, which is the case at line 690.

## 5. Field-24 = -2 ambiguity check

Verified: in the frozen base, no tag-20 node ever has field 24
= -2.

- `promote_graph`: field 24 = `hg(W,24)` (edge count) >= 0.
- `bootstrap_miss`: field 24 = `hg(W,24)` >= 0.
- Test code (lines 1157, 1202): field 24 = `hg(W,24)` >= 0.
- Alloc zeroing (lines 93, 102, 111): field 24 = 0.

The marker is unambiguous. Any tag-20 node with field 24 = -2
is a fragment record (in the future build) and nothing else.

## 6. Verdict on the spec's guard requirement

### 6.1 The spec's stated location is incorrect

FRAGMENT_RECORD.md section 1.2 says:

> The query path (`activate`, `ev_query`) must not treat a fragment
> record as an answerable MAP. Guard: `ng(W,m,24) != -2` before any
> MAP-shaped read.

VERIFICATION RESULT: `activate` and `ev_query` never enumerate
tag-20 nodes. They scan tag-1 (FACT) nodes exclusively. The guard
is not needed in the query path because the query path never
looks at MAPs. The spec's stated guard location would be dead
code if implemented as described.

This is not a safety problem (an unnecessary guard is harmless),
but it indicates the spec author did not perform the census in
section 2 of this report. The build's preregistration should
correct the guard location.

### 6.2 The actual required guard location

`revise_on_contradict` (bl_base.zag:690) is the ONLY production
function that enumerates tag-20 nodes. It needs:

```zag
if(ng(W,m,36)==1 && ng(W,m,0)==20 && ng(W,m,24)!=-2){
```

The spec's claim that "no guard is needed there" (section 1.2,
second bullet) is TRUE only under the build-time invariant that
fragments never carry outbound type-1 edges. The guard is
recommended as defense in depth because the failure mode of a
violated invariant is silent fragment-store corruption (F-shape
overwrite), not a crash.

### 6.3 Completeness

All production paths that could mistake a fragment for a regular
MAP have been enumerated:

| Path | Enumerates tag-20? | Guard needed? | Status |
|------|-------------------|---------------|--------|
| `activate` | No (tag-1 only) | No | Safe |
| `ev_query` | No (via activate/trial/bootstrap) | No | Safe |
| `t2_trial` / `t2_gather` | No (tag-1 only) | No | Safe |
| `bootstrap_miss` | No (tag-1 only; creates MAPs) | No | Safe |
| `miss_inquire` | No | No | Safe |
| `revise_on_contradict` | YES | YES (defense in depth) | GUARD RECOMMENDED |
| `t2_revise_graph` | No (called with explicit m) | No (protected by caller) | Safe if caller guarded |
| `promote_graph` | No (creates MAPs) | No | Safe |
| `map_standing` | N/A (test only) | If made production | Flagged |
| `ev_act` | Tag-agnostic (no tag filter) | Latent risk | FLAGGED |
| `evict_node` / `bid` | Tag-agnostic | No (by design) | Safe |
| `execute` / `t2_exec` | No (explicit roots) | No | Safe |

## 7. Gaps and recommendations for the build preregistration

1. CORRECT the guard location: `revise_on_contradict:690`, not
   the query path. The query path needs no guard.
2. ADD `ng(W,m,24)!=-2` to `revise_on_contradict` as defense in
   depth (1 line, negligible cost).
3. VERIFY by inspection that no fragment creation path emits
   outbound type-1 edges (the load-bearing invariant for the
   unguarded inner check).
4. VERIFY by inspection that no path links a fragment to
   POLICY_ROOT (the `ev_act` latent risk), or add a tag check to
   `ev_act`.
5. If `map_standing` is called in production in the future build,
   add the guard there.
6. The Q1 correction (FRAGMENT_RECORD.md section 0) is confirmed:
   fields 40-68 do not exist in the frozen 40-byte layout. Any
   guard or layout code must account for the node enlargement.

## 8. Standing architectural metrics

- RESEARCHER-OWNED STRUCTURAL DECISIONS: 0 (verification only).
- LEARNER-OWNED STRUCTURAL DECISIONS: 0.
- SUF DECISIONS: 0. LEARNER-INTERNAL CRITERIA: 0.
- REUSE EVENTS: 0. REVISION EVENTS: 0.
- COGNITION LINES: 0. MODES: 0. BRIDGES: 0. HANDLERS: 0.
- SEMANTIC CASES: 0.
- SOURCE-ENUMERABLE FORMS: 0.

## 9. Explicit non-claims

1. This verification covers the frozen base only. It does not
   verify the future composition-memory build (which does not
   exist yet).
2. It does not authorize implementation of the guard. The guard
   is a recommendation for the build's preregistration.
3. The "safe by construction" findings in 3.1 depend on the
   fragment spec's edge-type assignments (14, 15, 16) being
   honored by the build. If the build uses different edge types,
   this verification must be redone.
4. No capability, SUF, L3, or utility claim is made or implied.

No em dashes were used in this document.
