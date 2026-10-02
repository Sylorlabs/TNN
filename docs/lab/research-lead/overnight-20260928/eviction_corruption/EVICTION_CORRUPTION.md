# Eviction Corruption: Root Cause Analysis

**Status:** ANALYSIS-COMPLETE
**Verdict:** EVICTION-CORRUPTION-COMPLETE with classification: **DESIGN FLAW**
**Date:** 2026-10-01

## The Finding (from white-box inventory `b17fee225`)

During FW9's eviction churn, two intact MAPs were destroyed:
- **MAP 45** (FW1 chain graph): root now points at a TAG902 literal cell
- **MAP 82** (FW1 chain graph): root hijacked by a MOVE cell in MAP 74's graph
- **Policy root evicted**: its 5 MEM edges now emanate from an unrelated BEQ guard cell
- All 30 uncertainties and 9 guides orphaned

Both MAPs verified intact through the fw8 snapshot. The corruption occurred during FW9.

## Root Cause: The Mechanism

### How MAP roots are stored

In `promote_graph` (`tnn2.zag` line 533):
```
fn promote_graph(W:[]u8,root:i32,s:i32,r:i32,ans:i32,facts:[]u8,nf:i32)i32 {
  let m:i32=alloc_node(W); if(m<0){return -1;}
  ns(W,m,0,20); ns(W,m,4,r); ns(W,m,8,s); ns(W,m,12,-1); ns(W,m,16,-1);
  write_node(W,m,root,hg(W,24),ans,0);
  ...
}
```

`write_node` sets field 20 = root, field 24 = promo index, field 28 = answer, field 32 = 0.

**The MAP's graph root is stored as a plain integer in field 20, not as an edge.**

Confirmed by the frozen base comment (line 531): "field20=graph root".

### How evict_node works

```
fn evict_node(W:[]u8)i32 {
  let cur:i32=hg(W,8); let best:i32=-1; let bb:i32=1000000; let i:i32=0;
  while(i<1024){
    let n:i32=cur+i; if(n>=1024){n=n-1024;}
    if(n>=2 && ng(W,n,36)==1 && is_prot(W,n)==0){
      let b:i32=bid(W,n);
      if(b<bb){bb=b; best=n;}
    }
    i=i+1;
  }
  if(best<0){return -1;}
  rec_evict(W,best); ns(W,best,36,0); hs(W,20,hg(W,20)-1);
  let e:i32=0;
  while(e<4096){
    if(eg(W,e,0)!=-1 && (eg(W,e,0)==best || eg(W,e,8)==best)){
      es(W,e,0,-1); hs(W,24,hg(W,24)-1);
    }
    e=e+1;
  }
  let nc:i32=best+1; if(nc>=1024){nc=2;} hs(W,8,nc);
  return best;
}
```

**Victim selection:** Scans from rotating cursor `hg(W,8)`, picks the live (`field 36 == 1`), unprotected (`is_prot == 0`) node with the lowest `bid`.

**What is checked:** Node liveness, protection status (type-9 PRO edges only).

**What is NOT checked:**
- Whether the node is a MAP root (referenced by any MAP's field 20)
- Whether the node is a graph cell belonging to a live MAP's structure
- Whether any non-edge field references this node

**Edge cleanup:** All edges where the victim is source OR target are deleted. This is correct for edge-based references.

**The gap:** MAP roots are field-based references, not edges. Edge cleanup does not touch them. There is no code anywhere in the retention system that scans MAP root fields.

### The corruption sequence

1. MAP 45 created with field 20 = R (a graph cell, e.g., a MOVE or chain node)
2. Under budget pressure, cell R is evaluated by `evict_node`
3. R's bid is 0 (graph cells have no incoming type-1,2,6,7 edges; SEQ type-12 edges don't count)
4. R is unprotected (no type-9 PRO edge)
5. R is selected as victim, its slot freed, its edges cleaned up
6. **MAP 45's field 20 still equals R.** No edge existed, so nothing updated it.
7. Later, `alloc_node` reuses slot R for a new node (zeroes all fields, sets new type)
8. Slot R is now a TAG902 literal cell (or part of another MAP's graph)
9. MAP 45's field 20 = R now points to the wrong node type
10. MAP 45 is corrupted

### Why graph cells are always first

The `bid` function:
```
fn bid(W:[]u8,n:i32)i32 {
  let c:i32=evcount(W,n,1)+evcount(W,n,2)+evcount(W,n,6)+evcount(W,n,7)-evcount(W,n,3);
  ...
}
```

- **MAP node:** Has type-2 and type-6 self-edges (from `promote_graph`). Bid = 0 + 1 + 1 + 0 - 0 = **2**.
- **Graph cell:** Connected via SEQ (type-12) edges, which are not in the bid formula. Bid = **0**.
- **Fact node:** May have DEP/USE/OBS edges. Bid varies, typically >= 0.

Graph cells are the lowest-bid nodes in the entire system. Under any budget pressure, they are evicted first. This is not a rare edge case; it is the guaranteed output of the bid function.

## Classification: DESIGN FLAW (not implementation bug)

### Why not a bug

A bug is "implementation does not match intended policy." There is no evidence of an intended policy that protects MAP roots:

1. `evict_node` faithfully implements its specified behavior: lowest-bid unprotected node, edge cleanup.
2. `is_prot` faithfully checks type-9 PRO edges; the spec never mentions MAP roots.
3. `bid` faithfully counts the specified edge types; the spec never mentions structural membership.
4. Nowhere in the 1591-line source is there any mechanism for tracking field-based references.

The implementation is correct. The design is incomplete.

### The design gap

The retention system reasons about **nodes and edges**. But TNN-2 has **field-based references** (MAP root in field 20) that are invisible to the retention system. This is an architectural blind spot: the system cannot maintain invariants over references it cannot see.

More deeply: the bid function is **per-node** while utility is **per-structure**. A graph cell has zero individual utility (bid 0) but is essential as part of a MAP. The forgetting analysis (`2726baf74`) identified this as the root cause of fossilization: "retention bids are per-node and fixed while utility is per-structure and experiential."

## What the Minimal Fix Would Be (if treated as bug)

**Option A: Protect MAP-referenced nodes.**
In `evict_node`, before selecting victim, check if any live MAP (tag 20) has field 20 == n. If so, skip n.
Cost: O(MAPs) per candidate, O(1024 * MAPs) per eviction. Expensive but correct.

**Option B: Tombstone on eviction.**
When evicting n, scan all MAPs. If any MAP has root == n, mark that MAP as dead (e.g., set a tombstone flag or supersede it) so it doesn't point to garbage.
Cost: Prevents corruption but loses the MAP. Better than a zombie, worse than protection.

**Option C: Store root as edge.**
Change `promote_graph` to store the root as a typed edge (e.g., type-14 ROOT edge from MAP to root cell) instead of field 20. Then `evict_node`'s edge cleanup automatically severs the reference, and the MAP can detect the missing root.
Cost: Requires changing all root readers (lines 707, 1285). Changes the data model.

All three are **bugfixes** in the sense that they patch the specific corruption. None addresses the deeper per-node vs per-structure bid problem.

## What the Design Change Would Be

**Structure-level retention.** The bid of a node should reflect the utility of the structure it belongs to, not just its individual edge counts.

Concretely: when computing `bid(n)`, if n is a graph cell referenced (transitively) by a live MAP's root, n should inherit some function of the MAP's bid. Or: MAPs should PROTECT their entire graph (via type-9 PRO edges or a structural protection mechanism).

This is the same class of move as the H3-lite policy nodes: replacing a researcher-fixed constant (per-node bid weights) with a mechanism that respects structural relationships. It does not require learner-owned decisions, but it does require the architecture to model "this cell is part of that structure."

## Implications for "Structures Die First"

**CONFIRMED, and worse than predicted.**

The forgetting analysis predicted: "structures die first, MAPs fossilize, answers catastrophically forgotten."

The white-box inventory shows the actual failure mode is more insidious:

1. **Structures don't just die; they are corrupted while their shells survive.** MAP 45 and MAP 82 still exist as MAP nodes (tag 20, bid 2). They look alive in a node census. But their roots point to garbage. They are **zombie MAPs**.

2. **A cleanly deleted structure is gone. A corrupted structure is a landmine.** If the system ever tries to execute a zombie MAP (currently it doesn't at query time, but revision or future machinery might), it will read a literal cell as a graph root, producing undefined behavior.

3. **The corruption is silent.** Nothing logs it. Nothing detects it. The `rec_evict` history (itself write-only theater, per `e0423538a`) doesn't record that a MAP was structurally destroyed. The white-box inspector only caught it by comparing snapshots.

4. **The policy root was evicted.** The node coordinating retention policy was itself a victim of the policy. This is a self-undermining failure: the system destroyed its own control structure because the control structure had a low bid.

### Prediction refinement

Original P4 prediction: "structures die first"
Refined: "structures are **corrupted** first (via field-reference invalidation), while their MAP shells survive as zombies; the corruption is silent and undetectable by the system itself."

This strengthens the case for structure-level retention: it's not just about preserving useful structures, it's about preventing the system from silently corrupting its own knowledge.

## Standing Metric Implications

- **RESEARCHER-OWNED STRUCTURAL DECISIONS:** The eviction policy (bid weights, protection criteria, victim selection) is entirely researcher-owned. The corruption is a consequence of researcher-owned design, not learner behavior.
- **LEARNER-OWNED STRUCTURAL DECISIONS:** 0 (unchanged). The learner has no input to retention.
- **REVISION EVENTS:** The corruption is not a revision; it's destruction. It should not be counted as a revision event.
- **New category needed:** CORRUPTION EVENTS (silent structural destruction). MAP 45 and MAP 82 are 2 corruption events. The policy root eviction is a 3rd.

## Open Questions

1. How many other field-based references exist that the retention system cannot see? (MAP root is one; are there others?)
2. If a zombie MAP is revised (contradiction arrives), does the revision machinery detect the corruption, or does it operate on garbage?
3. The budget pressure experimenter (`0208769e`) may independently observe this corruption. If so, that is a replication.
