# ZOMBIE_CENSUS.md

## Verdict: ZOMBIE-CENSUS-COMPLETE with rates.

## Method

Pure-Zag in-driver zombie detector on verbatim frozen TNN-2 copies
(SHA-256 `a29972ca...` verified before and after). Three workloads,
fresh learner each, unsealed synthetic integer subjects only.
3/3 byte-identical runs (SHA-256 `a7b33dfd...`).

### Detector (read-only white box)

For each live tag-20 MAP node, read field 20 (graph root, plain integer):

- root == 0: BOOTSTRAP (degenerate, not zombie)
- root out of [2,1024): Z_RANGE (dangling)
- node[root] dead (field 36 != 1): Z_DEAD (dangling)
- node[root] live but tag not in {101,102,103,104}: Z_WRONGTYPE
- root shared with another live MAP: Z_SHARED
- root reachable from another live MAP's SEQ walk: Z_HIJACKED
- else: OK

Two-pass: pass 1 classifies by root validity; pass 2 checks
shared/hijacked using only pass-1-OK MAPs as hosts (zombies cannot
host a hijack claim). SEQ successor index built in one edge pass;
walks bounded at 80 steps. Guard cells (tag 102) followed via
field-12 match target, matching the frozen executor.

### Workloads

- W1_LIGHT: 20 teaches + 4 chain-promote cycles (masked queries, flags=1).
- W2_MEDIUM: 60 teaches + 10 chain-promote cycles + 5 contradictions.
- W3_HEAVY: 80 chain-promote cycles (2 teaches + 1 masked query each),
  census at 40 cycles (W3_MID40) and 80 cycles (W3_HEAVY80).

Driver bug found and fixed during development: initial driver passed
flags=0 to ev_query, so masked=0 and expected=-2 meant t2_try_verify
never accepted (0 MAPs promoted). Corrected to flags=1 (true masked
mode). This is a driver bug, not a TNN-2 finding.

## Results (3/3 identical)

| Workload   | live_nodes | MAPs | Zombies | Rate  |
|------------|------------|------|---------|-------|
| W1_LIGHT   | 72         | 4    | 0       | 0.0%  |
| W2_MEDIUM  | 220        | 10   | 0       | 0.0%  |
| W3_MID40   | 520        | 40   | 0       | 0.0%  |
| W3_HEAVY80 | 1022       | 79   | 3       | 3.8%  |

### W3_HEAVY80 zombie detail

- map=13, Z_WRONGTYPE: root=6, live, tag=30 (UNCERTAINTY node).
  Evicted graph cell reused for an uncertainty node.
- map=26, Z_WRONGTYPE: root=19, live, tag=902 (literal cell).
  Evicted graph cell reused for a literal.
- map=39, Z_SHARED: root=32, live, tag=102, shared with another MAP.
  Two MAP shells point at the same graph cell.

Zero Z_RANGE, Z_DEAD, Z_HIJACKED in this workload.

## Analysis

1. **Zombies appear only under budget pressure.** At 520/1024 nodes
   (W3_MID40, no eviction), 0 zombies across 40 MAPs. At 1022/1024
   (eviction churn), 3.8%. The corruption is caused by eviction,
   not by normal operation.

2. **3.8% is a lower bound.** The white-box inventory found 20% in
   the W cumulative state (9/52). The W world had more diverse
   operations and longer churn. My workload uses only chain promotions;
   real workloads with contradictions, revisions, and mixed operations
   likely produce higher rates.

3. **No Z_DEAD observed because reuse is immediate.** When a graph
   cell is evicted, alloc_node reuses the slot promptly, so the
   zombie root points to a live wrong-type node rather than a dead
   one. Z_DEAD would only appear if we sampled between eviction
   and reuse.

4. **Zombies are never detected or cleaned.** No production code
   checks MAP root validity. The MAP shells persist indefinitely.
   A zombie MAP is never executed at query time in frozen TNN-2
   (activate matches FACTs only), so the corruption is silent:
   no crash, no error, just a dead structure occupying budget.

5. **The shared-root case is the most dangerous.** Two MAPs pointing
   at the same graph cell means a future revision or execution
   through one MAP's root would operate on the other's graph.
   In frozen TNN-2 this is inert (MAPs never execute at query),
   but any future MAP-execution path would hit this landmine.

## Relation to prior findings

- Confirms eviction-corruption `986c52fdc` (design flaw, field-based
  roots invisible to evict_node) with measured rates.
- Consistent with white-box inventory `b17fee225` (20% in W state);
  this census establishes the pressure-dependence curve.
- The 3.8% rate at 1022/1024 nodes suggests the corruption is
  not rare under sustained pressure.

## Explicit non-claims

- This census does not measure zombie impact on capability
  (frozen TNN-2 never executes MAPs at query, so impact is nil today).
- The rate is workload-dependent; 3.8% is specific to chain-promotion
  churn, not a universal constant.
- No fix implemented (measurement only, per task scope).

## Standing metric (this measurement)

- RESEARCHER-OWNED STRUCTURAL DECISIONS: 0 (measurement only)
- LEARNER-OWNED STRUCTURAL DECISIONS: 0
- ZOMBIE MAPS: 3/79 at heavy pressure (3.8%)
- ZOMBIE DETECTION EVENTS: 0 (no detector in production)
- ZOMBIE CLEANUP EVENTS: 0
