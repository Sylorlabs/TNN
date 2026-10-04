# REPORT.md -- H-XIO-1: Learner-Built Typed I/O Adapters Rescue Cross-Domain Composition

## Verdict: XIO-ADAPTERS-COMPLETE

All 8 frozen kill bars (PREREG.md, commit 12e7bc301, committed before
any implementation existed) pass. With adapters enabled, the C215
cross-domain pair (chain-then-count) composes successfully; with
adapters disabled the exact C215 negative reproduces; the adapter is
reused on a second pair with the same type mismatch and a second
adapter is built for a new composite relation; no-MAP controls fail as
required; runs are 3/3 byte-identical.

## What was built

A typed I/O adapter is a persistent learner-built structure (node tag
40) that performs function composition over typed MAP outputs. The
mechanism, in xio_core.zag (unfrozen, new):

1. Learner-observed typed signatures: oty(m) = 1 (NUMBER) if the MAP's
   own executable graph contains an INC cell (tag 103 of the frozen
   4-op ISA), else 0 (NODE). Computed at runtime over learner-built
   graphs. No researcher type table.
2. Mismatch trigger: xio_try runs only after lookup and rebind fail,
   only when a competent oty=1 MAP exists, and only over ordered pairs
   with oty(m1) != oty(m2). Same-type pairs are never candidates.
3. Staged execution (value-level handoff, not path concatenation):
   v1 = stage(m1, s), v2 = stage(m2, v1), where each stage re-derives
   its graph for the new input with the learner's own trial assemblers
   (t2_gather + t2_asm_chain for oty 0; DEP-provenance relation +
   t2_chain + t2_asm_count for oty 1) and executes it.
4. On v2 == expected, xio_build allocates the adapter node
   (m1, m2, oty1, oty2, rel1, rel2, answer, query relation) with DEP
   edges to both stages. The adapter teaches no answer fact: it is
   procedural and must re-execute on reuse.
5. Query pipeline: activate -> adapter lookup (relation-keyed) ->
   rebind_try -> xio_try -> mp_run (trial) -> bootstrap_miss ->
   miss_inquire. Uniform miss-policy stage, no task-label routing.

## Kill-bar scorecard (all from xio_run1/2/3.txt, 3/3 identical)

- K1 Z success: TREAT Z1 ans=2. Exactly one adapter built, first
  mismatched pair tried (tried=1 rejected=0):
  `XIO-BUILD id=380 m1=27 m2=115 o1=0 o2=1 rel1=81 rel2=82 qr=93
  mid=34 ans=2`
  m1=27 is the learner-promoted chain MAP (r=91 s=11), m2=115 the
  learner-promoted count MAP (r=92 s=50). mid=34 is the exact
  predicted handoff value (X-walk endpoint, Y-count subject).
- K2 Reuse: TREAT Z2a (41,93) ans=2 via `XIO-REUSE id=380 ans=2`;
  adapter count stays 1. No rebuild: the same adapter re-derived
  both stages for the new subject (41->44->2).
- K3 Generalization: TREAT Z2b (71,94) ans=2 via a second adapter
  `XIO-BUILD id=467 ... qr=94 mid=74 ans=2` (mid=74 = 71+3, correct);
  adapter count becomes 2. Same stage MAPs (27, 115) reused under a
  new composite relation.
- K4 Ablation causality: ABL-XIO (adapters disabled) Z1=Z2a=Z2b=-2,
  adapters=0 throughout. The C215 negative reproduces exactly when
  the adapter stages are off, so the adapters cause the TREAT
  success.
- K5 No-MAP controls: ABL-X (chain MAPs deleted), ABL-Y (count MAPs
  deleted), FRESH (no training): Z1=Z2a=Z2b=-2 in all three,
  adapters=0. Adapters compose learned MAPs; they are not a hardcoded
  Z solver (without both stage types, xio_try admits no pair).
- K6 Competence preserved: TREAT X1=14 (trial 2/1), X2=18 (rebind
  1/0), Y1=3 (trial 3/2), Y2=4 (trial 4/3). Matches C215 exactly.
- K7 Learner-built evidence: census shows 2 chain MAPs (plen 4,
  oty 0) and 2 count MAPs (plen -1, oty 1, invisible to chain
  admission as in C215). Adapter fields reference learner-promoted
  MAP ids; rel1/rel2 read from the MAPs' own DEP provenance edges;
  grep confirms no type-conversion table and no CHAIN_COUNT template
  in the new source (only a comment stating their absence).
- K8 Determinism: 3/3 runs byte-identical, sha256
  `3b10e33ebdbb99d6826b945cd6ffbcb35c99ed17a6f4da3a84fb26d0325c9e98`.

## Why this is the missing substrate piece (C215 diagnosis, confirmed)

C215 found every mechanism composing by navigation concatenation with
count MAPs invisible to admission. The adapter fixes exactly this:
the count MAP stays invisible to chain admission (plen=-1, untouched),
but the typed-composition path does not need it to look like a chain.
It needs a typed signature (oty=1, observed) and a value handoff
(stage 2 applied to stage 1's output value). The XIO-BUILD line is the
white-box trace: chain MAP 27's node output 34 fed as count MAP 115's
subject, count 2 returned, composite typed node->count.

## Ablation interpretation

- Adapters off -> -2 (K4): the adapter stages are causally necessary.
- Either stage type missing -> -2, no adapter built (K5): the adapter
  is not a Z-specific hack; it needs both learned competencies.
- Adapter present, new subject, same relation -> reuse, no rebuild
  (K2): the adapter is a general procedure, not a memorized answer.
  (It teaches no fact; Z2a could not have been answered by lookup.)

## Honest boundaries

1. Only chain/count stage types; sum MAPs excluded from pairs.
2. Masked xio_try (expected=-2) returns -2, untested.
3. One cross-domain family (navigation x aggregation).
4. Pair search is brute-force over ordered MAP pairs (8 here);
   scaling to large MAP stores needs indexing (future work).
5. oty via INC-cell scan is a structural proxy grounded in the frozen
   ISA, not a learned classifier; a noisier alternative (output-value
   observation) was not needed here.
6. The adapter does not invent new stage procedures; it reuses the
   learner's own trial assemblers. The invention is the composition:
   which MAPs pair, the typed handoff, and the persistent structure.

## Standing metrics

- Cognition lines added: ~290 (xio_core.zag) + ~150 (xio_driver.zag),
  all unfrozen driver-level; frozen base (cx_core.zag) byte-untouched.
- Modes / bridges / handlers / new core semantic cases: 0 / 0 / 0 / 0.
- Researcher-owned: world, arms, stage re-derivation procedures (the
  learner's own trial assemblers), adapter field layout, oty-difference
  gate.
- Learner-owned: all MAP graphs, oty labels (computed), stage
  relations (provenance-read), paired MAPs (27, 115), intermediate
  values (34, 74), both adapter nodes and their DEP edges.
- Capability-source delta: the Z capability comes from new learner
  state (2 adapter nodes + 4 DEP edges), not new researcher machinery.

## Deliverables (all in xio_adapters/)

- PREREG.md (frozen 12e7bc301, before implementation)
- NAMECHECK.md (toolchain guard Step 0, commit-order self-check)
- REPORT.md (this file)
- xio_core.zag, xio_driver.zag (new, unfrozen)
- xio_full.zag (assembly: cx_core.zag verbatim + xio_core + driver)
- xio_bin (pinned znc build), xio_compile.txt (warnings only)
- xio_run1.txt, xio_run2.txt, xio_run3.txt (3/3 byte-identical)

Pure Zag, safebin PATH, zero em/en dashes (byte-verified), paper
untouched, committed locally, nothing pushed. The base's internal
test battery references ev_query; this worker provides it as
xio_query(...,xio_on=1) in the driver (cx_patch.zag deliberately not
included; the battery is never invoked).
