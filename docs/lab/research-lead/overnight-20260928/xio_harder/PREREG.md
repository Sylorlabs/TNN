# PREREG.md -- H-XIO-2: Typed I/O Adapters on the Harder Cross-Domain Pair

Frozen: 2026-10-02 (this commit). Implementation does not exist yet at
freeze time. Any result obtained before this file's first commit is void.

## Hypothesis

H-XIO-2: the typed I/O adapter mechanism that rescued chain-then-count
(H-XIO-1, prereg 12e7bc301, ledger C229) generalizes UNCHANGED to the
harder pair (transform-then-navigate, prereg 23266dc1c, results
d09995951), where the handoff direction is reversed: X = COUNT
(node -> number, oty 1) then Y = CHAIN on numeric subjects
(number -> node, oty 0), Z = Y(X(s)) with a COMPUTED intermediate k=4.

The xdomain-harder worker's shared diagnosis was that cross-domain
needs typed function composition with a computed-value to subject
handoff, which no chain-bound mechanism performs. H-XIO-2 claims the
adapter's staged execution v2 = stage(m2, stage(m1, s)) already
performs exactly this handoff, because the chain stage assembler
(t2_gather) treats any i32 subject id uniformly: a computed number is
re-subjected with no type barrier. The port changes NOTHING in the
adapter machinery; only the world (driver) is new.

## Mechanism (frozen, reused byte-verbatim)

xio_core.zag from H-XIO-1 is reused UNMODIFIED (sha256 recorded in
NAMECHECK.md Step 2; assembly recipe cats the sibling file verbatim,
no copy, no edit). All of the following are therefore frozen claims
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
arms, census): xhio_driver.zag. Prediction: the first differing pair
tried on Z1 is (count MAP, chain MAP) with o1=1, o2=0 (reversed from
C229's o1=0, o2=1), mid=4, ans=52.

## World design (harder-pair facts from d09995951, plus reuse probes)

- X (COUNT, r=81 facts, query r=91):
  teach (11,81,12),(12,81,13),(13,81,14); query (11,91) -> 3;
  teach (15,81,16),(16,81,17); query (15,91) -> 2.
- Y (CHAIN on numeric subjects, r=82 facts, query r=92):
  teach (3,82,30),(30,82,31),(31,82,32); query (3,92) -> 32;
  teach (2,82,40),(40,82,41),(41,82,42); query (2,92) -> 42.
- 30-fact interference gap (subjects 5000+, relations 60-69).
- Z1: teach (21,81,22),(22,81,23),(23,81,24),(24,81,25);
  teach (4,82,50),(50,82,51),(51,82,52);
  query (21,93) -> 52. Requires count(21)=4, then chain from 4.
- Z2a (reuse probe, same composite relation 93):
  teach (41,81,42),(42,81,43),(43,81,44),(44,81,45);
  query (41,93) -> 52. Requires count(41)=4, then chain from 4
  (82-chain from 4 already taught in Z1).
- Z2b (generalization probe, new composite relation 94):
  teach (71,81,72),(72,81,73),(73,81,74);
  query (71,94) -> 32. Requires count(71)=3, then chain from 3
  (82-chain from 3 taught in Y training).

Arms (separate worlds, one binary):
- TREAT: full training, adapters enabled (xio_on=1).
- ABL-XIO: full training, adapters disabled (xio_on=0: adapter lookup
  and xio_try skipped). Expect the d09995951 negative reproduced.
- ABL-X: full training, r=91 (count) MAPs deleted before Z, adapters
  enabled. Expect -2, adapters 0 (xio_has_typed fails: no oty-1 MAP).
- ABL-Y: full training, r=92 (chain) MAPs deleted before Z, adapters
  enabled. Expect -2, adapters 0 (only same-type count pairs exist;
  the mismatch gate admits none).
- FRESH: no X/Y training, adapters enabled. Expect -2, adapters 0.

## Kill bars (frozen; ALL must pass)

- K1 Z success: TREAT Z1 ans=52, exactly one adapter built on Z1,
  with o1=1, o2=0 (count -> chain), rel1=81, rel2=82, qr=93, mid=4
  (the computed handoff value), ans=52, and the pair scan showing
  tried=1 rejected=0 (first differing pair tried is count, chain).
- K2 Reuse: TREAT Z2a ans=52 via XIO-REUSE of the Z1 adapter; adapter
  count stays 1 (no rebuild; the adapter re-derives both stages for
  the new subject 41).
- K3 Generalization: TREAT Z2b ans=32 via a second adapter (qr=94,
  mid=3, ans=32); adapter count becomes 2. Same stage MAPs reused
  under a new composite relation with a different intermediate.
- K4 Ablation causality: ABL-XIO Z1=Z2a=Z2b=-2, adapters=0 throughout
  (the d09995951 harder negative reproduces with adapters off).
- K5 No-MAP controls: ABL-X, ABL-Y, FRESH: Z1=Z2a=Z2b=-2 in all three,
  adapters=0 (adapters compose learned MAPs; not a hardcoded solver).
- K6 Competence preserved: TREAT X1=3, X2=2, Y1=32, Y2=42 (matches
  d09995951; via path is pipeline-dependent and not bar-relevant).
- K7 Learner-built evidence: MAP census shows 2 count MAPs (plen -1,
  oty 1) and 2 chain MAPs (plen 4, oty 0); adapter fields reference
  learner-promoted MAP ids; xio_core.zag sha256 matches the C229
  committed file (zero mechanism changes); grep confirms no
  type-conversion table and no COUNT_CHAIN / CHAIN_COUNT pair template
  in the new driver source.
- K8 Determinism: 3/3 runs byte-identical stdout (sha256 recorded).

## Handoff analysis (frozen diagnostic signatures)

The verdict requires XIO-HARDER-COMPLETE to include the handoff
analysis. Preregistered signatures:

- S1 (handoff works): XIO-BUILD with o1=1 o2=0 mid=4 ans=52,
  tried=1 rejected=0. The computed number 4 is re-subjected into
  t2_gather and the chain stage assembles (4,50,51,52). This is the
  K1 pass signature.
- S2 (adapter gate fine, chain stage fails on computed subject):
  tried>=1 rejected>=1 on Z1, no XIO-BUILD, ans=-2, mid never
  emitted. Localizes the failure to the STAGE ASSEMBLER
  (t2_gather/t2_asm_chain refusing subject 4), not the adapter logic.
- S3 (count stage fails): v1 never valid. Excluded as a separate
  signature by K6: the count stage is the same code path as X1/X2
  trial competence, so K6 passing rules S3 out.
- S4 (adapter gate never fires): tried=0 on Z1 despite census (K7)
  showing oty-1 and oty-0 MAPs. Localizes to oty misclassification
  or the pair scan, not the handoff.

If K1 fails, the observed signature (S2/S3/S4) determines whether the
failure is in the adapter or in the stage assemblers, per the table.

## Verdict rule

XIO-HARDER-COMPLETE iff K1 through K8 all pass as frozen above, with
the handoff analysis reporting which signature (S1-S4) was observed.
Any single kill-bar failure, or any adapter-mechanism edit before or
during this wave, voids the verdict (fresh prereg required). The
driver (world) is the only new source this wave.

## Honest boundaries (frozen)

1. Only chain (oty 0) and count (oty 1) stage types; the core is
   unchanged from C229, so the same boundary applies.
2. Masked xio_try (expected=-2) returns -2, untested (inherited).
3. One harder pair (count x chain-on-numbers); the adapter's
   generality across further pairs is not claimed here.
4. Pair search is brute-force over ordered MAP pairs (inherited).
5. oty via INC-cell scan is the inherited structural proxy.
6. The adapter reuses the learner's own trial assemblers; the
   invention is the pairing and the typed handoff (inherited).

## Deliverables

docs/lab/research-lead/overnight-20260928/xio_harder/: PREREG.md
(this file, frozen first), NAMECHECK.md, REPORT.md, xhio_driver.zag
(new, unfrozen: world/arms/census), xhio_full.zag (assembled:
composition_A/cx_core.zag verbatim + xio_adapters/xio_core.zag
verbatim + xhio_driver.zag), xhio_bin, xhio_run1/2/3.txt,
xhio_compile.txt. Pure Zag, safebin PATH, committed locally, never
pushed. No new adapter-mechanism source: the C229 core is referenced,
not copied or edited.
