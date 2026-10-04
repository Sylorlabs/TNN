# REPORT.md: H-XIO-4: Generalized XIO Type System and Per-Class Stage Dispatch

## Verdict: XIO-GENERAL-COMPLETE (with 3-pair battery)

All 8 frozen kill bars (PREREG.md, commit e08110f47, committed before
any implementation existed) pass. The repaired XIO operator solves all
three pairs: chain->count (C229 values reproduced exactly, adapter
ids 380/467 identical to the historical run), count->chain (C235
values reproduced exactly, adapter ids 214/313 identical), and the
previously failing chain->sum (Z=SUM(CHAIN(s))=10 on all three probes,
the XIO-THIRD S4 failure signature gone). The generality boundary
localized by XIO-THIRD is repaired by growing the type system and the
stage executors together: a learner-observed structural signature
(xio_sclass: guard presence, INC-only vs mixed cells, integers only,
zero researcher domain labels) plus per-structural-class stage
dispatch (class 0/1 branches verbatim, new class-2 total
re-derivation). Runs are 3/3 byte-identical.

## What was built

Two new files in xio_general/ (unfrozen); the frozen
composition_A/cx_core.zag is referenced verbatim in assembly, never
copied or edited (sha256 dc0e86d44db11390e6e7d2450e1b52d7fb8f8012b42346dc4d4739ef888d1ab6
before and after):

1. xio_core2.zag, the generalized XIO core. Changes relative to the
   C229 xio_core.zag, exactly as frozen in the prereg:
   - NEW xio_sclass(W, m): walks the MAP's own executable graph
     (BRANCHEQ true-targets for tag-102 cells, SEQ edges otherwise,
     the xio_oty walk pattern) counting guards (tag 102), INC cells
     (tag 103), and other cells. Returns 0 (guard-only), 1
     (guard+INC mixed), 2 (INC-only), or -1 (unknown, fail-closed).
     Integers only; no domain type names, no type-conversion table,
     no pair templates (grep-verified).
   - xio_oty kept verbatim as the coarse 2-bucket view (1 iff the
     graph contains an INC cell). On all three trial-promoted
     families, oty == 1 iff sclass is 1 or 2.
   - The mismatch gate moved from oty-difference to
     sclass-difference: ordered pairs (m1, m2), m1 != m2, are
     admitted iff sclass(m1) != sclass(m2). On the three test pairs
     this admits exactly the same pair sets as the old gate; it
     additionally admits future cross-family pairs (e.g. class 1/2)
     that the 2-bucket gate would wrongly reject. Same-class pairs
     are never candidates.
   - xio_stage_exec dispatches on xio_sclass: class 0 runs the
     existing chain re-derivation branch verbatim; class 1 runs the
     existing count re-derivation branch verbatim; class 2 runs the
     NEW xio_stage_c2 (relation from the MAP's own DEP provenance
     edges, the stage input's direct facts under exactly that
     relation via xio_gather_direct, rebuild with the learner's own
     t2_asm_sum, masked verify with frame slot0 = 0, mirroring
     trial's own class-2 candidate frame); class -1 returns -999999.
   - The adapter node layout is unchanged; signature slots 12/16
     now hold the structural class (emitted as c1=/c2=).
   - Everything else (xio_build, xio_exec, xio_adapt, xio_query
     pipeline order, xio_has_typed, trial, promotion) is unchanged.
2. xg_driver.zag, the 3-pair battery driver. PAIR-A replicates the
   C229 world, PAIR-B the C235 world, PAIR-C the XIO-THIRD world
   (facts and queries copied from the three source drivers). Arms:
   TREAT + ABL-XIO for A and B; TREAT, ABL-XIO, ABL-X, ABL-Y, FRESH,
   AUDIT for C. The census reports oty, sclass, and a driver-side
   class label (observability only, not part of the type system).

## Kill-bar scorecard (all from xg_run1/2/3.txt, 3/3 identical)

- K1 PAIR-A no-regression: TREAT Z1=2 via
  `XIO-BUILD id=380 m1=27 m2=115 c1=0 c2=1 rel1=81 rel2=82 qr=93
  mid=34 ans=2` (tried=1 rejected=0); Z2a=2 via `XIO-REUSE id=380`
  (adapters stay 1); Z2b=2 via a second adapter `id=467 ... qr=94
  mid=74 ans=2` (adapters=2). X1=14, X2=18, Y1=3, Y2=4. ABL-XIO:
  Z1=Z2a=Z2b=-2, adapters=0. Every id, mid, and answer matches the
  C229 run exactly. PASS.
- K2 PAIR-B no-regression: TREAT Z1=52 via
  `XIO-BUILD id=214 m1=44 m2=96 c1=1 c2=0 rel1=81 rel2=82 qr=93
  mid=4 ans=52` (tried=1 rejected=0); Z2a=52 via `XIO-REUSE id=214`;
  Z2b=32 via a second adapter `id=313 ... qr=94 mid=3 ans=32`.
  X1=3, X2=2, Y1=32, Y2=42. ABL-XIO: all -2, adapters=0. Every id,
  mid, and answer matches the C235 run exactly. PASS.
- K3 PAIR-C solves: TREAT Z1=10 via
  `XIO-BUILD id=190 m1=27 m2=59 c1=0 c2=2 rel1=81 rel2=82 qr=93
  mid=44 ans=10` (tried=1 rejected=0); Z2a=10 via `XIO-REUSE id=190`
  (adapters stay 1); Z2b=10 via a second adapter
  `id=275 ... qr=94 mid=74 ans=10` (adapters=2). The first
  mismatched pair tried builds the adapter, as in C229/C235. PASS.
- K4 Structural signature: PAIR-A census shows 2 MAPs sclass 0 and
  2 sclass 1; PAIR-B shows 2 sclass 1 and 2 sclass 0; PAIR-C shows
  2 sclass 0 and 2 sclass 2; no other MAPs in any world. oty agrees
  in all 12 MAPs (1 iff sclass in {1,2}). grep over xio_core2.zag
  finds no domain type names (remaining matches are inherited
  frozen-trial identifiers t2_asm_chain/t2_asm_count/t2_asm_sum and
  the common noun "count" in "fact count"/xio_count), no
  type-conversion table, no pair templates. PASS.
- K5 Gate and stage diagnosis: PAIR-C AUDIT reports tried=8
  cross-class pairs and gate_rejected=4 same-class pairs. The 4
  (class 0, class 2) pairs show v1=44 v2=10; the 4 (class 2,
  class 0) pairs show v1=-999999 v2=-999999. White-box proof the
  stage boundary moved: v2=10 (total semantics) where XIO-THIRD
  measured v2=1 (link-count semantics) on the same world. PASS.
- K6 Ablation causality: PAIR-C ABL-XIO, ABL-X, ABL-Y, FRESH all
  give Z1=Z2a=Z2b=-2 with adapters=0 throughout and zero XIO-BUILD
  lines; PAIR-A and PAIR-B ABL-XIO give -2 with adapters=0. The
  adapters cause the TREAT successes; they are not solvers and need
  both stage families. PASS.
- K7 Competence preserved: PAIR-C TREAT X1=14, X2=18, Y1=8, Y2=12,
  matching XIO-THIRD K6. The repair changes staging, not the
  learner's sum competency. PASS.
- K8 Determinism: 3/3 runs byte-identical, sha256
  a7cf8b524b20e50906d21cb3d58e88cf8ba63e12276ee3cb2337ccfeee4b63ae.
  PASS.

## Why the repair is general, not a third branch bolted on

The failure XIO-THIRD localized was a type-system/stage-executor
mismatch: the signature could not name the third family, so no
executor could be selected for it. The repair does not add a
"sum branch" keyed to a researcher label; it adds a structural
discriminator (guard presence, INC-only vs mixed) that the learner
computes from each MAP's own graph, and the executor is selected by
that observed structure. Three facts make this a type-system repair
rather than a domain patch:

1. The discriminators are total over graph structure, not over an
   enumerated family list: any future trial-promoted family with
   guards+INC, guard-only, or INC-only graphs is classified without
   researcher involvement, and unknown structures fail closed
   (class -1) instead of being mis-staged.
2. The gate now partitions on the same signature the dispatch uses,
   so pairing and staging cannot disagree about what a MAP is. The
   2-bucket gate would admit (class 1, class 2) pairs only to
   mis-stage them; the sclass gate admits them to the correct
   executors.
3. The class-2 stage re-derives from the MAP's own provenance
   (relation off its DEP edges) and the learner's own assembler and
   verification frame (t2_asm_sum, slot0=0), exactly the pattern the
   class-0/1 branches already used. No new researcher knowledge
   enters at stage time.

## Ablation interpretation

- Adapters off -> -2 on all three pairs (K6): the generalized
  stages are causally necessary, including the new class-2 stage.
- Either stage family missing -> -2, no adapter built (PAIR-C
  ABL-X/ABL-Y): the operator composes learned competencies; it is
  not a Z-specific solver.
- Adapter present, new subject, same relation -> reuse without
  rebuild (Z2a on all three pairs): the adapter is procedural, and
  each stage re-derives for the new input through its
  class-selected executor.
- The PAIR-A/B TREAT outputs reproduce the historical adapter ids
  (380/467, 214/313) and handoff values (mid=34, mid=4), confirming
  the class-0/1 paths are allocation-identical to the frozen core.

## Honest boundaries

1. Only sequence->aggregate was run for the new class;
   aggregate->sequence exercises the same dispatch symmetrically
   and was not separately run.
2. The class-2 stage sums the stage input's direct facts under the
   MAP-observed licensing relation. Worlds where a subject carries
   same-relation facts outside the intended aggregate set are not
   tested; the trial-promoted sum family has no such noise.
3. Masked xio_try untested (inherited from C229).
4. Class -1 (unknown structure) is fail-closed, not handled.
5. The second sum MAP promotes at id 103 here vs 91 in XIO-THIRD:
   during the Y2 probe, xio_try now stages the first sum MAP
   through the class-2 branch (different allocation sequence than
   the old count branch) before trial promotes the second MAP.
   This id shift is itself evidence the dispatch changed; no kill
   bar depends on it.
6. The pair audit is driver-level observability built from the
   core's own xio_sclass and xio_stage_exec; it modifies nothing
   and runs in a dedicated AUDIT arm.

## Standing metrics

- Cognition lines added: ~90 new mechanism lines in xio_core2.zag
  (xio_sclass, xio_gather_direct, xio_stage_c2, dispatch/gate
  changes); the class-0/1 stage branches and all of trial/promotion
  are reused verbatim from the frozen base.
- Modes / bridges / handlers / new core semantic cases: 0 / 0 / 0 / 0.
- Hardcoded pair templates / type-conversion table: 0
  (grep-verified).
- Researcher-owned: world facts, queries, arm definitions, driver
  census/audit layout, tag-8 world setup (PAIR-C). The structural
  signature, the mismatch gate, stage dispatch, stage relations,
  and adapter layout are learner-observed or learner-built.
- Learner-owned: all 12 MAP graphs, oty/sclass labels (computed),
  stage relations (provenance-read), all admitted pairs
  (gate-computed), all stage values, all 7 adapters built.
- Capability-source delta: one repaired generality boundary; the
  third pair is newly solvable, the first two provably unregressed.

## Deliverables (all in xio_general/)

- PREREG.md (frozen e08110f47, before implementation)
- NAMECHECK.md (toolchain guard Step 0, commit-order self-check,
  build/run log, scorecard)
- REPORT.md (this file)
- xio_core2.zag (new, unfrozen: generalized XIO core)
- xg_driver.zag (new, unfrozen: 3-pair battery driver)
- xg_full.zag (assembled: ../composition_A/cx_core.zag verbatim +
  xio_core2.zag + xg_driver.zag)
- xg_bin (pinned znc build), xg_compile.txt (warnings only)
- xg_run1.txt, xg_run2.txt, xg_run3.txt (3/3 byte-identical)

Pure Zag, safebin PATH, zero em/en dashes in worker-authored content
(byte-verified), paper untouched, committed locally, nothing pushed.
