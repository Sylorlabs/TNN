# REPORT.md -- H-XIO-3: Third-Domain Pair Localizes the XIO Generality Boundary at Stage Assembly

## Verdict: XIO-THIRD-COMPLETE (S4 observed as predicted; H-XIO-3 rejected; boundary localized)

All 8 frozen kill bars (PREREG.md, commit c21e49503, committed before
any implementation existed) pass in their preregistered S4 form.
H-XIO-3, the claim that the XIO adapter generalizes unchanged to the
third pair sequence->aggregate (chain x sum), is REJECTED. The
rejection is clean and precisely localized: the learner-observed type
proxy classifies the third MAP family correctly (sum -> NUMBER), the
mismatch gate fires on all 8 cross-type pairs, but staged execution
fails because the oty-1 stage branch hardcodes count re-derivation
and produces count semantics (v2=1) for a sum MAP instead of the sum
(10). No adapter builds; Z1/Z2a/Z2b answer -2 in every arm. The
generality boundary of the XIO operator is at STAGE ASSEMBLY, not at
type observation and not at the mismatch gate.

## What was tested

The third pair uses the only trial-promoted MAP family structurally
different from both chain and count: SUM/aggregate. A sum MAP's graph
is unrolled INC cells only (no BRANCHEQ guards, no SETREG cells, no
cell-level DEP edges); its frame starts slot0 at 0 rather than the
query subject; its answer is a fixed total. X = CHAIN/sequence
(r=81, query r=91, oty 0), Y = SUM/aggregate (r=82, query r=92,
oty 1), Z = SUM(CHAIN(s)), query (41,93) -> 10 (chain 41->42->43->44,
sum of 44's values 3+7=10). The XIO core (xio_core.zag) is reused
byte-verbatim (sha256 4d4d2e0e932b6a472e3cd8456d7e1c633218e611ce5df51d03507218440a8a7f
before and after); the only new source is the driver (world, arms,
census, pair audit).

## Kill-bar scorecard (all from x3_run1/2/3.txt, 3/3 identical)

- K1 Z1 boundary: TREAT Z1 ans=-2, adapters=0, zero XIO-BUILD lines
  in the full output. PASS (the predicted S4 outcome).
- K2 oty observation: census shows exactly 2 chain MAPs (plen 4,
  oty 0, ids 27, 45) and 2 sum MAPs (plen -1, oty 1, all-INC graphs,
  ids 59, 91); no other MAPs. The INC-cell proxy classifies the third
  family correctly. S2 ruled out. PASS.
- K3 mismatch gate: the AUDIT pair audit on (41,93) reports
  PAIR-SUMMARY tried=8 (2 chain x 2 sum x 2 orders). Every cross-type
  pair is admitted. S3 ruled out. PASS.
- K4 stage diagnosis: the audit shows the 4 (chain, sum) pairs with
  v1=44 (correct chain endpoint) and v2=1 (count of the walk
  [44,3], not the sum 10), and the 4 (sum, chain) pairs with
  v1=-999999 (no (41,82,*) facts, walk length < 2); no pair yields
  v2=10. Representative lines:
  PAIR m1=27 o1=0 m2=59 o2=1 v1=44 v2=1
  PAIR m1=59 o1=1 m2=27 o2=0 v1=-999999 v2=-999999
  PASS.
- K5 ablations: TREAT Z2a=Z2b=-2; ABL-XIO, ABL-X, ABL-Y, FRESH:
  Z1=Z2a=Z2b=-2 in all four, adapters=0 throughout. The adapter is
  inert on this pair; the -2 is not an adapter-off artifact. PASS.
- K6 competence preserved: TREAT X1=14, X2=18, Y1=8, Y2=12. The sum
  MAPs are competent via trial (Y1/Y2 promote sum graphs with the
  correct totals); the adapter cannot stage them. PASS.
- K7 core unchanged: xio_core.zag sha256 identical before and after;
  grep finds no type-conversion table and no SUM_CHAIN / CHAIN_SUM
  template in x3_driver.zag. PASS.
- K8 determinism: 3/3 runs byte-identical, sha256
  d3ad77208ddc8771427a911a74bb80571ec2fd154ed1c7f78dfb452ad4a10220.
  PASS.
- Diagnostic signature: S4 observed; S1, S2, S3 not observed.

## The generality-boundary diagnosis (the key result)

XIO factors into three sub-mechanisms, and the third pair separates
them:

1. Type observation (xio_oty: INC-cell scan) GENERALIZES. It was
   designed against chain/count, but it classifies the unseen third
   family correctly: sum graphs start with an INC cell, so oty=1
   (NUMBER). The census (K2) is the white-box evidence. The proxy is
   not the boundary.

2. The mismatch gate (oty(m1) != oty(m2)) GENERALIZES. It admits all
   8 cross-type pairs (K3). The gate is purely a function of observed
   types; it has no chain/count specificity. The gate is not the
   boundary.

3. Staged execution DOES NOT GENERALIZE. xio_stage_exec dispatches on
   the 2-bucket oty: bucket 0 re-derives via t2_asm_chain, bucket 1
   re-derives via t2_chain + t2_asm_count. Trial, however, produces
   THREE MAP families, and bucket 1 conflates two of them (count and
   sum). The bucket-1 stage executor is count-specific: it walks a
   chain over the MAP's DEP relation and counts the links. Applied to
   a sum MAP, whose competency is totalling direct facts, it returns
   a link count (1), never the sum (10). K4 shows this exactly:
   v1=44 is right, v2=1 is count semantics where sum semantics were
   needed.

So the XIO operator is half-general: its typed pairing and gating
are domain-agnostic, but its stage executors are domain-specific to
the two families the researcher enumerated (chain, count). The
boundary is precise: XIO composes any pair whose MAPs are staged
correctly by the two fixed re-derivation branches, and no pair
involving a NUMBER MAP outside the count family. A third arithmetic
family breaks it at the stage level while passing type observation
and gating cleanly.

Architectural note: the stage executor re-derives rather than
re-executing the MAP's own graph because the MAP's literals are
input-specific (the sum graph bakes in the total as an INC count;
the chain graph bakes in node ids). Re-derivation therefore needs a
per-family assembler, but the 2-bucket oty cannot dispatch to three
or more assemblers. Fixing this boundary requires either a richer
learner-observed type signature that distinguishes count from sum
(and any future arithmetic family), or stage executors selected by
the MAP's own structural class rather than the binary oty. That fix
is NOT built here (it would be a core change, forbidden this wave);
it is recorded as the diagnosed next step.

## Ablation interpretation

- Adapters on vs off (TREAT vs ABL-XIO): identical -2 everywhere.
  The adapter contributes nothing on this pair, in either direction.
- Chain MAPs deleted (ABL-X): only same-type sum pairs exist; the
  mismatch gate admits none (tried would be 0); -2. Within-type
  pairs are never adapter candidates, by design.
- Sum MAPs deleted (ABL-Y): xio_has_typed fails; -2. The oty-1 stage
  is necessary for the gate to fire at all.
- FRESH: -2. Adapters compose learned MAPs; they are not a solver.
- Competence (K6) vs staging (K4): the sum MAPs answer Y1/Y2
  correctly via trial, so the failure is strictly in the adapter's
  re-derivation, not in the learner's sum competency.

## Why this matters for the composition program

C229 and the harder pair showed the SAME unmodified operator covering
chain->count and count->chain, which was evidence for generality.
This wave bounds that evidence: the operator's generality covers
pairing direction and value handoff across the two families its stage
executors implement, but it does not extend to a third MAP family,
even one the type proxy classifies correctly. The "typed" in typed
I/O adapters is currently a 2-bucket system; genuine generality needs
the type system and the stage executors to grow together. Any future
claim that XIO is a general typed-composition operator must first
pass a third-family test like this one.

## Honest boundaries

1. Only sequence->aggregate was run; aggregate->sequence hits the
   same stage-assembly boundary by symmetry (the sum stage is
   order-independent) and was not run.
2. The pair audit is driver-level observability built from the core's
   own xio_oty and xio_stage_exec; it modifies nothing and runs in a
   dedicated AUDIT arm.
3. The tag-8 combination node is a frozen trial precondition for sum
   candidates (internal t_p2); the driver creates one per world as
   world setup. It teaches no fact and promotes no MAP by itself.
4. Masked xio_try untested (inherited).
5. The em dashes in x3_compile.txt are znc's own warning text (also
   present in the sibling compile logs); all worker-authored docs,
   code, and run outputs are dash-free (byte-checked).

## Standing metrics

- Cognition lines added: 0 to the adapter mechanism (byte-verbatim
  reuse); 276 new driver lines (world/arms/census/pair audit,
  unfrozen).
- Modes / bridges / handlers / new core semantic cases: 0 / 0 / 0 / 0.
- Hardcoded pair templates: 0 (grep-verified).
- Researcher-owned: world facts, queries, arm definitions, driver
  census/audit layout, tag-8 world setup. (Stage re-derivation,
  adapter layout, and the oty-difference gate remain C229's
  researcher-owned list, unchanged.)
- Learner-owned: all MAP graphs (including the 2 sum graphs), oty
  labels (computed), stage relations (provenance-read), the 8
  admitted pairs (gate-computed), the rejected stage values.
- Capability-source delta: zero new capability (the predicted and
  observed outcome); the wave's product is the localized boundary,
  not a mechanism change.

## Deliverables (all in xio_third/)

- PREREG.md (frozen c21e49503, before implementation)
- NAMECHECK.md (toolchain guard Step 0, commit-order self-check,
  build/run log, scorecard)
- REPORT.md (this file)
- x3_driver.zag (new, unfrozen: third-pair world, arms, census,
  pair audit; the ONLY new source)
- x3_full.zag (assembled: composition_A/cx_core.zag verbatim +
  xio_adapters/xio_core.zag verbatim + x3_driver.zag)
- x3_bin (pinned znc build), x3_compile.txt (warnings only)
- x3_run1.txt, x3_run2.txt, x3_run3.txt (3/3 byte-identical)

Pure Zag, safebin PATH, zero em/en dashes in worker-authored content
(byte-verified), paper untouched, committed locally, nothing pushed.
