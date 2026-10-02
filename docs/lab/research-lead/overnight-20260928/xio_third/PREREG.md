# PREREG.md -- H-XIO-3: Typed I/O Adapters on the Third Domain Pair (Sequence x Aggregate)

Frozen: 2026-10-02 (this commit). Implementation does not exist yet at
freeze time. Any result obtained before this file's first commit is void.

## Hypothesis

H-XIO-3: the typed I/O adapter mechanism (H-XIO-1, C229; H-XIO-2,
harder pair) generalizes UNCHANGED to a third domain pair whose MAP
types are structurally different from both chain and count:
sequence-then-aggregate. X = CHAIN/sequence (node -> node, oty 0,
guard/set cells), Y = SUM/aggregate (direct facts -> number, oty 1,
unrolled INC cells only, no guards, frame slot0 starts at 0).
Z = Y(X(s)): walk a chain, then sum the endpoint's values. The port
changes NOTHING in the adapter machinery; only the world (driver) is
new.

## Why this pair

The frozen XIO core classifies MAP output type by INC-cell presence
(oty 1 = NUMBER iff the graph contains a tag-103 cell, else 0 = NODE)
and stages oty 0 through the chain re-derivation branch
(t2_gather + plen match + t2_asm_chain) and oty 1 through the count
re-derivation branch (DEP-provenance relation + t2_chain +
t2_asm_count). Trial promotes exactly three MAP families: chain
(oty 0), count (oty 1), sum (oty 1). Sum is the only family whose cell
types and output semantics are structurally different from both chain
and count: its graph is unrolled INC cells only (no BRANCHEQ guards,
no SETREG cells, hence no cell-level DEP edges), its execution frame
starts slot0 at 0 instead of the query subject, and its answer is a
fixed total rather than a walked node or a link count. A sum MAP is
therefore the strongest available third-domain probe of whether XIO
is a genuinely general typed-composition operator or a chain/count
trick. The tested order is sequence->aggregate: Z = SUM(CHAIN(s)).

## White-box prediction (frozen analysis of the byte-identical core)

H-XIO-3 is PREDICTED TO FAIL, with the failure localized to STAGE
ASSEMBLY. Step by step over the frozen code:

1. oty observation: sum graphs begin with an INC cell (tag 103), so
   xio_oty returns 1 (NUMBER) on the first cell visited. Chain graphs
   contain no INC cells, so oty 0. The INC-cell proxy classifies the
   third family correctly; the MAP census will show it.

2. Mismatch gate: xio_try admits ordered MAP pairs (m1, m2),
   m1 != m2, with oty(m1) != oty(m2) only. (chain, sum) pairs have
   (0, 1) and (sum, chain) pairs have (1, 0), so the gate fires.
   With 2 chain MAPs and 2 sum MAPs, tried = 8.

3. Stage assembly: the oty 1 stage branch is count-specific. It reads
   the stage input relation from the MAP's own DEP edges (82 for the
   sum MAPs, whose licensing facts are the summed direct facts),
   walks t2_chain from the stage input over that relation, and
   rebuilds with t2_asm_count. For Z1 = (41, 93) -> 10: a
   (chain, sum) pair yields v1 = 44 (the chain endpoint, correct),
   then v2 = stage(sum, 44) = count of the walk [44, 3] = 1, not the
   sum 10. A (sum, chain) pair yields v1 = -999999 (no (41, 82, *)
   facts, so the chain walk has length < 2). Every pair is rejected;
   no XIO-BUILD is emitted; Z1 answers -2.

Predicted signature: oty correct, gate fires, stages produce count
semantics for a sum MAP. The generality boundary is at STAGE
ASSEMBLY: the NUMBER bucket's stage executor hardcodes count
re-derivation and cannot re-derive sum graphs. The pairing and gating
logic generalizes to the third pair; the staged execution does not.

## Mechanism (frozen, reused byte-verbatim)

xio_core.zag from H-XIO-1 is reused UNMODIFIED (sha256 recorded in
NAMECHECK.md Step 2; the assembly recipe references the sibling file
directly, no copy, no edit). All of the following are frozen claims
about existing, already-tested code, not new design:

- oty(m): 1 (NUMBER) iff m's executable graph contains an INC cell
  (tag 103 of the frozen 4-op ISA), else 0 (NODE). Computed at runtime
  over learner-built graphs.
- xio_try: ordered MAP pairs (m1, m2), m1 != m2, with oty(m1) !=
  oty(m2) only; v1 = stage(m1, s), v2 = stage(m2, v1); on
  v2 == expected, xio_build persists the adapter (tag 40) with DEP
  edges to both stages.
- xio_stage_exec: oty 0 re-derives a chain via t2_gather from the
  input subject + plen match + t2_asm_chain; oty 1 reads the input
  relation from the MAP's own DEP provenance + t2_chain +
  t2_asm_count. Masked verify (expected = -2 inside stages).
- xio_query pipeline: activate -> xio_adapt (relation-keyed adapter
  lookup) -> rebind_try -> xio_try -> mp_run (trial) ->
  bootstrap_miss -> miss_inquire. Not a mode; uniform miss policy.

The new work in this wave is ONLY the driver (world facts, queries,
arms, census, pair audit): x3_driver.zag. The pair audit is
driver-level observability built from the core's own xio_oty and
xio_stage_exec; it modifies nothing.

## World design (sequence->aggregate)

- X (CHAIN/sequence, r=81 facts, query r=91):
  teach (11,81,12),(12,81,13),(13,81,14); query (11,91) -> 14;
  teach (15,81,16),(16,81,17),(17,81,18); query (15,91) -> 18.
- Y (SUM/aggregate, r=82 facts, query r=92; driver creates the tag-8
  combination node that frozen trial requires for sum candidates,
  cf. internal t_p2; documented as world setup in Honest boundaries):
  teach (20,82,3),(20,82,5); query (20,92) -> 8;
  teach (30,82,4),(30,82,6),(30,82,2); query (30,92) -> 12.
- 30-fact interference gap (subjects 5000+, relations 60-69).
- Z1: teach (41,81,42),(42,81,43),(43,81,44);
  teach (44,82,3),(44,82,7);
  query (41,93) -> 10. Requires CHAIN(41)=44, then SUM(44)=10.
- Z2a (same composite relation 93):
  teach (51,81,52),(52,81,53),(53,81,54);
  teach (54,82,2),(54,82,8);
  query (51,93) -> 10.
- Z2b (new composite relation 94):
  teach (71,81,72),(72,81,73),(73,81,74);
  teach (74,82,1),(74,82,9);
  query (71,94) -> 10.

Arms (separate worlds, one binary):
- TREAT: full training, adapters enabled (xio_on=1).
- ABL-XIO: full training, adapters disabled (xio_on=0). Expect -2
  throughout (same as TREAT; the adapter is inert on this pair).
- ABL-X: full training, r=91 (chain) MAPs deleted before Z, adapters
  enabled. Expect -2, adapters 0 (only same-type sum pairs exist;
  the mismatch gate admits none).
- ABL-Y: full training, r=92 (sum) MAPs deleted before Z, adapters
  enabled. Expect -2, adapters 0 (xio_has_typed fails: no oty-1 MAP).
- FRESH: no X/Y training, adapters disabled. Expect -2, adapters 0.
- AUDIT: full training, Z1 facts only; runs the driver pair audit on
  (41,93) BEFORE the Z1 query, then the Z1 query. The audit reports
  every differing-oty pair with its stage outputs (v1, v2) via the
  core's own xio_stage_exec, making the stage-assembly diagnosis
  white-box observable.

## Kill bars (frozen; the S4 set must pass as preregistered)

- K1 Z1 boundary: TREAT Z1 ans=-2, adapters=0, no XIO-BUILD line
  emitted. (This is the predicted S4 outcome; an XIO-BUILD with
  ans=10 would be S1 instead.)
- K2 oty observation: MAP census shows exactly 2 chain MAPs
  (plen 4, oty 0) and 2 sum MAPs (plen -1, oty 1, all-INC graphs);
  no other MAPs. Rules out S2.
- K3 mismatch gate: the AUDIT pair audit on (41,93) reports
  tried=8 differing-oty pairs (2 chain x 2 sum x 2 orders).
  Rules out S3.
- K4 stage diagnosis: the audit shows the 4 (chain, sum) pairs with
  v1=44 and v2=1 (count semantics, not the sum 10), and the 4
  (sum, chain) pairs with v1=-999999; no pair yields v2=10.
- K5 ablations: TREAT Z2a=Z2b=-2; ABL-XIO, ABL-X, ABL-Y, FRESH:
  Z1=Z2a=Z2b=-2 in all four, adapters=0 throughout.
- K6 competence preserved: TREAT X1=14, X2=18, Y1=8, Y2=12. The sum
  MAPs are competent via trial; the adapter cannot stage them.
- K7 core unchanged: xio_adapters/xio_core.zag sha256 equals
  4d4d2e0e932b6a472e3cd8456d7e1c633218e611ce5df51d03507218440a8a7f
  before and after; grep confirms no type-conversion table and no
  SUM_CHAIN / CHAIN_SUM pair template in x3_driver.zag.
- K8 determinism: 3/3 runs byte-identical stdout (sha256 recorded).

## Diagnostic signatures (frozen)

- S1 (generality): XIO-BUILD on Z1 with o1=0, o2=1, mid=44, ans=10.
  Predicted NOT observed; would support H-XIO-3.
- S2 (oty observation failure): census does not show sum MAPs at
  oty 1 / chain MAPs at oty 0. Predicted NOT observed.
- S3 (mismatch gate failure): audit tried=0 on (41,93) despite K2.
  Predicted NOT observed.
- S4 (stage assembly boundary): K1, K2, K3, K4 as above: oty correct,
  gate fires (tried=8), every pair rejected at the stage level
  (count semantics from the oty-1 branch, -999999 from empty walks),
  no adapter built. PREDICTED.

## Verdict rule

XIO-THIRD-COMPLETE iff: (i) this PREREG's first commit strictly
precedes any implementation commit (verified in NAMECHECK.md Step 3);
(ii) the adapter core is byte-identical (K7); (iii) 3/3 runs are
byte-identical (K8); and (iv) EITHER S1 is observed (Z1=10 via
XIO-BUILD: H-XIO-3 supported, generality confirmed) OR S4 is observed
cleanly (K1 through K6 pass as preregistered: H-XIO-3 rejected, and
the generality boundary is localized at stage assembly with the
oty proxy (S2) and the mismatch gate (S3) ruled out). Any S2 or S3
observation, any non-determinism, or any adapter-mechanism edit
before or during this wave voids the verdict (fresh prereg required).
The driver (world + audit) is the only new source this wave.

## Honest boundaries (frozen)

1. The frozen core's stage machinery has exactly two buckets
   (chain/count re-derivation); a sum stage executor would require a
   core change, which this wave forbids. This wave therefore tests
   the generality boundary; it does not fix it.
2. Only the sequence->aggregate order is run; aggregate->sequence
   hits the same stage-assembly boundary by symmetry (the sum stage
   is order-independent) and is noted, not run.
3. Masked xio_try (expected=-2) returns -2, untested (inherited).
4. The pair audit is driver-level observability using the core's own
   xio_oty and xio_stage_exec. It allocates nodes like any driver
   code; it runs in a dedicated AUDIT arm so TREAT stays a clean
   mirror of the C229/HARDER arms.
5. The tag-8 combination node is a frozen trial precondition for sum
   candidates (see internal t_p2 in cx_core.zag). The driver creates
   one per world as world setup, exactly as the frozen test does.
   It teaches no fact and promotes no MAP by itself.
6. oty via INC-cell scan remains the inherited structural proxy; this
   wave shows it classifies the third family correctly and is not the
   boundary.

## Deliverables

docs/lab/research-lead/overnight-20260928/xio_third/: PREREG.md
(this file, frozen first), NAMECHECK.md, REPORT.md, x3_driver.zag
(new, unfrozen: third-pair world, arms, census, pair audit),
x3_full.zag (assembled: composition_A/cx_core.zag verbatim +
xio_adapters/xio_core.zag verbatim + x3_driver.zag), x3_bin,
x3_run1.txt, x3_run2.txt, x3_run3.txt, x3_compile.txt. Pure Zag,
safebin PATH, committed locally, never pushed. No new
adapter-mechanism source: the C229 core is referenced, not copied or
edited.
