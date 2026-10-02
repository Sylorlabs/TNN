# PREREG.md: H-XIO-4: Generalized XIO Type System and Per-Class Stage Dispatch

Frozen: 2026-10-02 (this commit). Implementation does not exist yet at
freeze time. Any result obtained before this file's first commit is void.

## Hypothesis

H-XIO-4: XIO becomes a general typed-composition operator when its
type system and its stage executors grow together. A richer
learner-observed structural signature separates the three
trial-promoted MAP families (guard-only graphs, guard+INC graphs,
INC-only graphs) with no researcher domain labels, and stage
execution dispatches per structural class to the matching
re-derivation branch. Predicted outcome: the generalized operator
solves all three pairs (chain->count, count->chain, chain->sum) with
zero regression on the first two, where the frozen 2-bucket XIO
(C229, C235, XIO-THIRD) solved only the first two and failed the
third at stage assembly (signature S4, prereg c21e49503).

## The generality-boundary repair (frozen design)

The XIO-THIRD diagnosis: typed pairing and the mismatch gate are
domain-agnostic, but xio_stage_exec dispatches on the 2-bucket oty,
so bucket 1 conflates the count family and the sum family and the
bucket-1 executor hardcodes count re-derivation. This wave repairs
exactly that boundary. The repair has two coupled parts:

### Part 1: richer learner-observed structural signature

New function xio_sclass(W, m), computed at runtime by walking the
MAP's own executable graph from its root, following BRANCHEQ
true-targets (offset 12) for guard cells (tag 102) and SEQ edges
(type 12) otherwise, exactly the walk pattern of the existing
xio_oty. While walking it counts three structural features, all
directly observable from learner-built white-box state:

- g: cells with tag 102 (BRANCHEQ guards)
- ic: cells with tag 103 (INC cells of the frozen 4-op ISA)
- other: any other cell tag

Classification (integers only, no domain names anywhere in the
mechanism):

- g > 0 and ic > 0: class 1 (mixed guard+INC structure)
- g > 0 and ic == 0: class 0 (guard-only structure)
- g == 0 and ic > 0 and other == 0: class 2 (INC-only structure)
- otherwise: class -1 (unknown structure, fail-closed)

The existing xio_oty (INC-cell presence, 1 = NUMBER else 0 = NODE)
is kept verbatim as the coarse 2-bucket view; on all three
trial-promoted families oty == 1 iff sclass is 1 or 2. The mismatch
gate moves from oty-difference to sclass-difference: ordered pairs
(m1, m2), m1 != m2, are admitted iff sclass(m1) != sclass(m2). On the
three test pairs this admits exactly the same pair sets as the old
gate (chain/count, count/chain, chain/sum); it additionally admits
future cross-family pairs such as count/sum, which the 2-bucket gate
would wrongly reject (both oty 1). Same-class pairs are never
admitted. The adapter node records the structural class in its
signature slots (offsets 12/16, previously oty).

No researcher domain labels: the words chain, count, sum (or any
domain synonyms) appear nowhere in the new core source as type names,
table keys, or dispatch labels. Dispatch is on the integers 0/1/2/-1
produced by the structural walk.

### Part 2: per-structural-class stage dispatch

xio_stage_exec dispatches on xio_sclass, not on the 2-bucket oty:

- class 0: the existing chain re-derivation branch, verbatim
  (t2_gather + plen match + t2_asm_chain, verified masked with the
  stage input as frame subject).
- class 1: the existing count re-derivation branch, verbatim
  (DEP-provenance relation + t2_chain + t2_asm_count, verified masked
  with the stage input as frame subject).
- class 2: NEW sum re-derivation branch. It reads the licensing
  relation from the MAP's own DEP provenance edges (xio_dep_rel,
  unchanged), gathers the stage input's direct facts under exactly
  that relation (new xio_gather_direct, the relation-filtered analog
  of the existing t2_gather_sum), rebuilds the total with the
  learner's own t2_asm_sum, and verifies masked with frame slot0
  starting at 0. The s0=0 frame is not a researcher choice: it
  mirrors trial's own sum-candidate verification
  (t2_try_verify(W, root, 0, expected, masked, st) in t2_trial),
  exactly as the class-0/1 branches mirror trial's chain/count
  verification frames (s0 = subject). If no relation is observed, no
  direct facts exist, or the total is nonpositive/over budget, the
  stage returns -999999 (fail-closed, same sentinel as the old
  branches).
- class -1: return -999999 immediately.

Everything else (xio_build layout, xio_exec handoff, xio_adapt
lookup, xio_query pipeline order, xio_has_typed precondition, trial,
promotion, revision) is unchanged.

## Why the first two pairs cannot regress (frozen analysis)

On chain graphs the walk sees guards and no INC cells: class 0, the
identical branch the oty-0 path selected. On count graphs the walk
sees guards and INC cells: class 1, the identical branch the oty-1
path selected. The gate admits the same ordered pairs as before on
worlds containing only these two families (class 0 vs 1 is the same
partition as oty 0 vs 1). Trial, promotion, and all allocation
sequences are untouched, and the new functions perform no
allocations on the class-0/1 paths, so node ids, MAP ids, adapter
ids, and every emitted line for the first two pairs are predicted to
reproduce the C229 and C235 runs exactly (up to driver header text).

## Test battery (frozen worlds)

Three pair-worlds in one driver, each with a fresh learner state:

- PAIR-A replicates the C229 world byte-for-byte in facts and
  queries (chain->count; Z1=(31,93)->2, Z2a=(41,93)->2,
  Z2b=(71,94)->2). Arms: TREAT, ABL-XIO.
- PAIR-B replicates the C235 world (count->chain; Z1=(21,93)->52,
  Z2a=(41,93)->52, Z2b=(71,94)->32). Arms: TREAT, ABL-XIO.
- PAIR-C replicates the XIO-THIRD world (chain->sum;
  Z = SUM(CHAIN(s)); Z1=(41,93)->10, Z2a=(51,93)->10,
  Z2b=(71,94)->10). Arms: TREAT, ABL-XIO, ABL-X, ABL-Y, FRESH,
  AUDIT (structural-class pair audit on Z1).

The driver census reports, per MAP, the learner-observed oty and
sclass and a driver-side class label for readability (driver
observability only, not part of the type system).

## Kill bars (all must pass; verdict requires 8/8)

- K1 PAIR-A no-regression: TREAT Z1=2 with exactly one XIO-BUILD
  (signature c1=0 c2=1, mid=34, ans=2, tried=1 rejected=0);
  Z2a=2 via XIO-REUSE (adapter count stays 1); Z2b=2 via a second
  adapter (qr=94, mid=74, ans=2); X1=14, X2=18, Y1=3, Y2=4.
  ABL-XIO: Z1=Z2a=Z2b=-2, adapters=0. All values match C229.
- K2 PAIR-B no-regression: TREAT Z1=52 with exactly one XIO-BUILD
  (signature c1=1 c2=0, mid=4, ans=52, tried=1 rejected=0);
  Z2a=52 via XIO-REUSE; Z2b=32 via a second adapter (qr=94, mid=3,
  ans=32); X1=3, X2=2, Y1=32, Y2=42. ABL-XIO: all -2, adapters=0.
  All values match C235.
- K3 PAIR-C solves: TREAT Z1=10 with exactly one XIO-BUILD
  (signature c1=0 c2=2, mid=44, ans=10); Z2a=10 via XIO-REUSE
  (adapter count stays 1); Z2b=10 via a second adapter (qr=94,
  mid=74, ans=10). The XIO-THIRD S4 failure signature is gone:
  no (chain,sum) pair yields count semantics.
- K4 Structural signature: the PAIR-C census shows exactly 2 MAPs
  with sclass 0 and 2 MAPs with sclass 2 (no other MAPs); PAIR-A
  shows 2 with sclass 0 and 2 with sclass 1; PAIR-B shows 2 with
  sclass 1 and 2 with sclass 0. oty agrees (1 iff sclass in {1,2}).
  grep over xio_core2.zag finds no domain type names, no
  type-conversion table, no pair templates.
- K5 Gate and stage diagnosis: the PAIR-C AUDIT arm reports
  tried=8 cross-class pairs; the 4 (class 0, class 2) pairs show
  v1=44 v2=10; the 4 (class 2, class 0) pairs show v1=-999999
  v2=-999999. Same-class pairs are never tried. This is the
  white-box proof that the stage boundary moved: v2=10 (sum
  semantics) where XIO-THIRD measured v2=1 (count semantics).
- K6 Ablation causality: PAIR-C ABL-XIO, ABL-X, ABL-Y, FRESH all
  give Z1=Z2a=Z2b=-2 with adapters=0 throughout; PAIR-A and PAIR-B
  ABL-XIO give -2 with adapters=0. The adapters cause the TREAT
  successes; they are not solvers (FRESH) and need both stage
  families (ABL-X/ABL-Y).
- K7 Competence preserved: PAIR-C TREAT X1=14, X2=18, Y1=8, Y2=12
  (matches XIO-THIRD K6: the sum MAPs are competent via trial; the
  repair changes staging, not competency).
- K8 Determinism: 3/3 runs byte-identical (sha256 recorded in
  NAMECHECK.md).

## Out of scope (honest boundaries)

- Only sequence->aggregate was re-run for the new class;
  aggregate->sequence hits the same stage dispatch symmetrically and
  is not separately run.
- The class-2 stage sums the stage input's direct facts under the
  MAP-observed licensing relation; worlds where a subject carries
  same-relation facts outside the intended aggregate set are not
  tested (the trial-promoted sum family has no such noise).
- Masked xio_try untested (inherited from C229).
- A fourth MAP family (class -1) is fail-closed, not handled.

## Verdict rule

XIO-GENERAL-COMPLETE iff all 8 kill bars pass on the frozen design
above with 3/3 byte-identical runs. Any implementation existing at
or before this file's first commit voids the wave.
