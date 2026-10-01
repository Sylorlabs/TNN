# USABILITY GAP ANALYSIS

**Status:** DRAFT-NOT-FROZEN. Analysis only; no implementation proposed or built.

**Parent result:** Barrier implementation `d7a62ea34` broke barrier 1
(structure visibility). The A-MAP is VISIBLE during B's construction
(`hg(W,56) > 0`) but NEVER referenced (`hg(W,60) = 0`). Zero transfer
preserved. This document characterizes what stands between visibility
and usability.

## 1. Trace: where the descriptors exist, and where they die

### 1.1 The descriptor lifecycle (source: `tnn2_barrier_variant.zag`)

`gather_structures` (line 446) scans live tag-20 MAPs. For each, it writes
a 16-byte descriptor into the caller-supplied buffer:

- bytes 0-3: MAP node id
- bytes 4-7: `t2_sig` cell count (`nc`)
- bytes 8-11: provenance s (`ng(W,m,8)`)
- bytes 12-15: provenance r (`ng(W,m,4)`)

It bumps `hg(W,56)` per structure and returns the visible count.

The single call site is `t2_gather` (line 473):

```
let sdesc:[]u8=z_alloc(256);
let nvis:i32=gather_structures(W,sdesc);
```

`sdesc` is function-local. `t2_gather` returns `np` (the FACT-path count).
`sdesc` is never copied into `paths`, never returned, never passed to
`t2_trial`. The descriptors are allocated, filled, counted, and dropped.
They are dead on arrival. This is the plumbing gap, and it is the EASY
part of the problem.

### 1.2 The descriptor is impoverished relative to the design

The barrier-break design (`f0f223029`) specified descriptors containing a
"structural signature (via frozen `t2_sig`)" plus a "literal vector (the
baked-in constants)". The implementation stores NEITHER:

- It stores `nc`, the cell COUNT returned by `t2_sig`, and discards the
  256-byte `sig` buffer that `t2_sig` actually filled.
- It stores no literal vector at all.

A cell count is nearly useless as a retrieval key: many MAPs share the
same count, and count carries no topological information. Even the
discarded signature would have been weak: the frozen `t2_sig`
implementation records `(tag, literal)` per cell INCLUDING literals for
tags 101/102 (this is the literal-recording behavior that voided the H2
calibration in `72173fe11`). A literal-contaminated signature cannot
match across disjoint namespaces by construction. The one field that
could support cross-domain matching (pure topology) is the one field
the frozen implementation does not produce.

### 1.3 Where descriptors COULD be consulted

Two plumbing options, both trivial:

- (a) `t2_gather` returns descriptors alongside paths (needs a second
  output channel; the 12-slot path layout is fixed).
- (b) `t2_trial` calls `gather_structures` directly before the fixed
  trial loops (simplest; ~5 lines).

And one execution primitive that already exists: `t2_try_verify`
(line 527) accepts an arbitrary `root` and runs it via `t2_exec`
(line 412), which seeds a fresh frame with `s0` and calls
`execute(W,root,fr)`. So the machinery to ATTEMPT a visible MAP exists
today. The naive composition, about 10 lines, would be: for each
visible descriptor, call `t2_try_verify` on its MAP root.

It would achieve exactly nothing. In the xfer case: the A-MAP (node 45)
is a 4-link chain with literals 1-5 baked into SETREG cells. Executing
it on a frame seeded with B's subject (100) computes a function of the
baked literals, not of the new subject. Verification against B's
`expected` fails. The attempt fails safely (verification rejects it)
but uselessly. Plumbing is not usability. The three sub-problems below
are what block the naive attempt from ever succeeding.

## 2. Decomposition of the usability gap

### 2.1 Retrieval: finding the RIGHT structure

**Current state:** The descriptor carries provenance (s, r). The A-MAP's
provenance is domain A's namespace (subjects 1-5, relation 40). The B
query is (subject 100+, relation 60). Exact (s,r) matching, the only
lookup TNN-2 has, fails by construction on disjoint namespaces. This is
barrier 3, now empirically accessible.

**What is needed:** A similarity key that is invariant to namespace but
sensitive to structure. Candidates:

- Pure topological signature (cell count is insufficient; the discarded
  `t2_sig` bytes are literal-contaminated; a literal-free topology hash
  does not exist in the codebase).
- Behavioral signature (what the MAP computes, not how; requires
  executing candidates, which is expensive and needs sandboxing).
- Provenance-role abstraction (relation 40 in A plays the role that
  relation 60 plays in B; requires learning role mappings, which is
  itself a transfer problem).

**Treadmill assessment: HIGH RISK.** Defining "similar" is exactly where
researcher judgment smuggles in. A structural-similarity metric tuned to
match "4-link chain" across these two domains is one step from a
chain-detector, the class of protected-core semantic operations Micah's
ISA ruling forbids (cf. FIND_POLYNOMIAL_ORDER). The honest version of
retrieval is LEARNED similarity: the learner discovers which structural
features predict reuse success. No machinery for that exists, and
building it is a research program, not a patch. Any fixed metric should
be treated as a benchmark-specific handler until proven otherwise.

### 2.2 Applicability: determining the structure fits (s,r)

**Current state:** MAPs carry no input/output contract. The MAP layout
(field 20 = graph root, field 28 = answer, fields 4/8 = r/s provenance)
says what the MAP WAS (provenance), not what it DOES (contract). The
graph executes on a frame seeded with `s0`, but nothing records which
frame slots are inputs, which literals are parameters vs constants, or
what relation the graph computes.

**What is needed:** Given a retrieved candidate and a query (s, r), a
decision procedure for "this structure applies here." The minimal
general form is try-and-verify: bind, execute, check. But:

- "Bind" requires rebinding (2.3).
- "Check" requires verification. The only verifier available is
  `t2_try_verify`, which checks against harness-supplied `expected`
  (unmasked) or accepts any non-degenerate value (masked). In a genuine
  transfer setting there is no `expected`. Learner-internal verification
  does not exist (see verification-criterion analysis, in progress).
  Try-and-verify with a harness oracle is not transfer; it is
  researcher-supervised reuse.

**Treadmill assessment: MEDIUM RISK.** Try-and-verify is the right SHAPE
(it is general, not domain-specific), but it is currently unfillable:
both halves (bind, verify) depend on missing machinery. A "verify
against expected" shortcut would convert the transfer experiment into a
supervised demo. The applicability decision cannot be built before the
verification criterion exists.

### 2.3 Rebinding: adapting baked-in literals

**Current state:** The A-MAP's graph cells reference literal nodes for
values 1-5 via field 8 (tags 101/102). These are baked at promotion
time. There is no indirection, no parameter slot, no substitution map.
This is barrier 4.

**What is needed:** A variable-binding mechanism that preserves graph
topology while replacing the literal layer. Three shapes, in increasing
order of generality:

- (a) Copy-and-rebind: copy the graph cells, swap literal references.
  Requires an ALIGNMENT: which old literal corresponds to which new
  value? In the xfer worlds, positional alignment works (chain order
  preserved) because the worlds are isomorphic BY CONSTRUCTION. In
  general, alignment is the hard part, and positional alignment is a
  one-world trick.
- (b) Parameterized execution: execute with a substitution map from old
  literals to new values. Requires the ISA or the executor to support
  indirection on literal reads. The frozen 4-op ISA has no such
  operation; adding one is a protected-core change (Micah escalation).
- (c) Template-guided re-derivation: use the old MAP as a template for
  fresh construction (the assembler takes a topology hint). Requires
  the assembler to accept structural input, which it currently cannot;
  assemblers take FACT paths only.

**Treadmill assessment: HIGH RISK.** Option (a) with positional
alignment solves exactly the xfer experiment and nothing else. The
general problem, learned variable binding (which parts of a procedure
are parameters, which are constants, and how they map to a new
domain), is arguably the core of what "procedure" MEANS. It is not a
missing feature; it is a missing cognitive capability. Any rebinding
rule that works on the xfer pair should be assumed benchmark-specific
until it survives a second, independently designed domain pair.

## 3. Dependency ordering

The three sub-problems are not independent. They form a chain:

```
retrieval -> applicability -> rebinding -> verification
   (3)          (3.5)           (4)          (missing)
```

- Retrieval without applicability yields candidate spam.
- Applicability without rebinding yields visible-but-unusable (today).
- Rebinding without verification yields silent wrong answers (worse
  than useless; the H2 void showed TNN returning confidently wrong
  values when verification is bypassed).
- All of it without learner-internal verification is
  researcher-supervised reuse, not transfer.

The barrier-break design correctly identified barrier 1 as the
bottleneck to break FIRST (visibility makes the rest empirically
accessible). The next bottleneck is NOT obvious: breaking retrieval
(barrier 3) without rebinding (barrier 4) produces the same
visible-but-unusable outcome at one level up. The honest next step is
probably retrieval AND rebinding together on a second domain pair, with
verification held fixed (harness `expected`) as a control, so that the
only new variables are the two barriers under test.

## 4. What the counters now separate

The white-box counters introduced by the barrier implementation give
the vocabulary for future work:

- `hg(W,56)` (visible): "could the construction see it?"
- `hg(W,60)` (referenced): "did any machinery consult it?"

Today: 56 > 0, 60 = 0. A future retrieval mechanism moves 60 > 0 while
transfer stays zero (retrieved but unusable). A future rebinding
mechanism is the one that can move transfer above zero. The counters
separate "saw but could not use" from "used but could not adapt" from
"adapted." That separation is the diagnostic value of the barrier-1
break, and it is fully realized: the instrument works as designed.

## 5. Explicit non-claims

- This analysis does not design a retrieval, applicability, or
  rebinding mechanism.
- It does not claim any of the three sub-problems is easy or nearly
  solved. Two of three carry HIGH treadmill risk.
- It does not obsolete the barrier-break design's honesty analysis;
  it extends it one level down.
- No SUF, no L3, no C0-D implications. Researcher-owned structural
  decisions for this analysis: 0 (analysis only). Learner-owned: 0.

## Verdict

**USABILITY-GAP-COMPLETE.** The gap is characterized as one plumbing
gap (trivial, ~10 lines, achieves nothing alone) plus three
substantive sub-problems (retrieval, applicability, rebinding) in
dependency order, each with a treadmill-risk assessment. The
visibility counters provide the diagnostic vocabulary for measuring
future progress through the chain.
