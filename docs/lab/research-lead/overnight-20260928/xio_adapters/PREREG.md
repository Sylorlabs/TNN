# PREREG.md -- H-XIO-1: Learner-Built Typed I/O Adapters for Cross-Domain Composition

Frozen: 2026-10-02 (this commit). Implementation does not exist yet at
freeze time. Any result obtained before this file's first commit is void.

## Hypothesis

H-XIO-1: cross-domain composition (chain navigation x count aggregation,
ledger C215, commit 0c91d9b3f) fails because all three mechanisms compose
by navigation concatenation and have no typed value handoff. A
learner-built typed I/O adapter rescues it: when the learner observes a
type mismatch between a competent MAP's output type and what the
chain composer expects, it attempts typed function composition over
ordered MAP pairs, and on verification success builds a persistent
adapter structure that performs the value-level handoff.

## Background (from C215, not re-argued here)

- X MAPs: chain graphs (guard/set only), output is a walked node.
- Y MAPs: count graphs (guard/set + INC cells + MOV epilogue), output is
  a computed number. plen = -1, contract = -1, relseq = []: invisible to
  all three admission filters, though competent (Y1=3, Y2=4 via trial).
- Z = chain-then-count, query (31,93) -> 2: needs X-walk to 34, then
  Y-count of 34. All mechanisms return -2 in all arms.

## Mechanism design (frozen)

### Typed signatures (learner-observed, not researcher labels)

For each MAP m, the learner computes oty(m) by scanning m's own
executable graph (white-box learner state): oty = 1 (NUMBER) if any cell
has tag 103 (INC); else oty = 0 (NODE). Input type is always NODE
(the query subject). The 103-means-arithmetic fact belongs to the frozen
protected ISA; the classification is computed at runtime over
learner-built graphs. There is no researcher-written table mapping MAPs
or relations to types.

### Mismatch trigger

The typed-composition attempt (xio_try) runs only when:
1. direct lookup and structural rebind both failed for the query, and
2. at least one active MAP has oty = 1 (a competent non-chain MAP the
   chain composer cannot see), and
3. the query is unmasked (expected answer supplied as post-hoc feedback,
   same E-ruling as trial).

xio_try attempts ordered pairs (m1, m2), m1 != m2, with
oty(m1) != oty(m2) ONLY. Same-type pairs are the within-domain
composers' job and are never adapter candidates. This is the literal
"type mismatch triggers adapter construction" gate.

### Staged execution (value-level handoff, not path concatenation)

xio_stage_exec(m, x) re-derives the stage for input x using the same
procedures trial uses to build MAPs, then executes:
- oty 0 (chain): gather BFS paths from x (t2_gather), take paths whose
  length equals rb_chain_plen of m's graph, rebuild via t2_asm_chain,
  execute via t2_exec semantics (masked verify: first valid output).
- oty 1 (count): read the stage's input relation from m's own DEP
  provenance edges (xio_dep_rel), walk the value chain from x
  (t2_chain), rebuild via t2_asm_count, execute (masked verify).

Composition: v1 = stage(m1, s); v2 = stage(m2, v1). If v2 is valid and
v2 == expected, build the adapter and return v2.

### Adapter structure (learner-built persistent state)

On success, xio_build allocates a node with tag 40 (T_ADAPT) holding:
field4 = m1, field8 = m2, field12 = oty(m1), field16 = oty(m2),
field20 = rel1 (from m1's DEP edges), field24 = rel2 (from m2's DEP
edges), field28 = answer, field32 = query relation served.
Plus DEP (type 1) edges adapter -> m1 and adapter -> m2 (provenance).
The adapter does NOT teach an answer fact: it is procedural, executed
on demand, so reuse must go through the adapter itself.

Adapter execution (xio_exec): v1 = stage(m1, s); v2 = stage(m2, v1);
return v2. The type conversion (node->count: m1's output node fed as
m2's count subject, m2's numeric output returned; count->node symmetric)
is performed by this handoff, recorded in the (o1, o2) signature.

### Query pipeline (driver-level, unfrozen; frozen base untouched)

xio_query: activate -> adapter lookup (xio_adapt, relation-keyed) ->
rebind_try -> xio_try -> mp_run (trial) -> bootstrap_miss ->
miss_inquire. This is not a mode: xio_try is attempted uniformly on any
query reaching it, keyed only by learner state, with no task label
routing. Zero modes, zero bridges, zero handlers, zero new semantic
cases, zero core changes.

### What is researcher-supplied (honest list)

World facts, queries, arm definitions, the two stage re-derivation
procedures (which reuse the learner's own trial assemblers
t2_asm_chain / t2_asm_count), the adapter field layout, the
oty-difference gate. The researcher does NOT supply: which MAPs pair,
the type labels (computed), the stage relations (read from provenance),
the intermediate value, or the adapter instance itself.

## World design (identical facts to C215, plus two reuse probes)

- X: teach (11,81,12),(12,81,13),(13,81,14); query (11,91)->14;
  teach (15,81,16),(16,81,17),(17,81,18); query (15,91)->18.
- Y: teach (50,82,51),(51,82,52),(52,82,53); query (50,92)->3;
  teach (60,82,61),(61,82,62),(62,82,63),(63,82,64); query (60,92)->4.
- 30-fact interference gap (subjects 5000+, relations 60-69).
- Z1: teach (31,81,32),(32,81,33),(33,81,34),(34,82,35),(35,82,36);
  query (31,93)->2.
- Z2a (reuse probe, same composite relation): teach
  (41,81,42),(42,81,43),(43,81,44),(44,82,45),(45,82,46);
  query (41,93)->2.
- Z2b (generalization probe, new composite relation): teach
  (71,81,72),(72,81,73),(73,81,74),(74,82,75),(75,82,76);
  query (71,94)->2.

Arms (separate worlds, one binary):
- TREAT: full training, adapters enabled.
- ABL-XIO: full training, adapters disabled (xio_on=0: adapter lookup
  and xio_try skipped). Expect full C215 negative reproduction.
- ABL-X: full training, r=91 MAPs deleted before Z, adapters enabled.
- ABL-Y: full training, r=92 MAPs deleted before Z, adapters enabled.
- FRESH: no X/Y training, adapters enabled.

## Kill bars (frozen; ALL must pass)

- K1 Z success: TREAT Z1 ans=2, exactly one adapter built, with
  o1=0, o2=1 (node->count), m1/m2 = the learner-promoted chain/count
  MAP ids, rel1=81, rel2=82, qr=93.
- K2 Reuse: TREAT Z2a ans=2 via XIO-REUSE of the Z1 adapter; adapter
  count stays 1 (no rebuild).
- K3 Generalization: TREAT Z2b ans=2 via a second adapter (qr=94);
  adapter count becomes 2.
- K4 Ablation causality: ABL-XIO Z1=Z2a=Z2b=-2 (C215 negative
  reproduced with adapters off).
- K5 No-MAP controls: ABL-X, ABL-Y, FRESH: Z1=Z2a=Z2b=-2 in all three
  (adapters compose learned MAPs; they are not a hardcoded Z solver).
- K6 Competence preserved: TREAT X1=14, X2=18, Y1=3, Y2=4 (matches C215).
- K7 Learner-built evidence: MAP census shows 2 chain MAPs
  (plen 4, oty 0) and 2 count MAPs (plen -1, oty 1); adapter fields
  reference learner-promoted MAP ids; no type-conversion table and no
  CHAIN_COUNT template anywhere in the new source (grep-verified).
- K8 Determinism: 3/3 runs byte-identical stdout (sha256 recorded).

## Verdict rule

XIO-ADAPTERS-COMPLETE iff K1 through K8 all pass as frozen above.
Any single kill-bar failure, or any implementation existing before this
file's first commit, voids the verdict (fresh prereg required).

## Honest boundaries (frozen)

1. Only chain (oty 0) and count (oty 1) stage types are implemented;
   sum MAPs are excluded from pairs (documented, not tested).
2. Masked xio_try (expected=-2) is not implemented; returns -2.
3. One cross-domain family (navigation x aggregation); audio/program
   domains out of scope.
4. Adapters are relation-keyed procedural structures; they do not teach
   answer facts (deliberate, required by K2).
5. The oty-difference gate means same-type pairs never build adapters;
   within-domain composition remains A/B/C's problem.

## Deliverables

docs/lab/research-lead/overnight-20260928/xio_adapters/: PREREG.md
(this file, frozen first), NAMECHECK.md, REPORT.md, xio_core.zag,
xio_driver.zag, xio_full.zag, xio_bin, xio_run1/2/3.txt,
xio_compile.txt. Pure Zag, safebin PATH, committed locally, never
pushed. Frozen base (composition_A/cx_core.zag) included verbatim,
read-only, unmodified.
