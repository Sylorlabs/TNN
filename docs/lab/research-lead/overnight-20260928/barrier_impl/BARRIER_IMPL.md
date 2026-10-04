# BARRIER-1 BREAK IMPLEMENTATION

**Status:** EXPERIMENT COMPLETE. Unfrozen variant only. Not TNN-3.
**Date:** 2026-10-01 UTC. **Verdict:** BARRIER-IMPL-COMPLETE.
**Design:** `f0f223029` (BARRIER-BREAK-DESIGN-COMPLETE).

## 0. What was built

An unfrozen variant of the xfer variant (`cbd7bc803`), which itself is an
unfrozen variant of frozen TNN-2 (`f4de7ff46`). Per Micah: "try stuff
unfrozen as you go on." Frozen source and binary untouched.

**Base:** `../xfer_experiment/tnn2_xfer_variant.zag`
(SHA-256 `655d94bde41f1f2890a2b287f6bcf42db2123f6b9239caacbd93b22f360c3403`,
verified identical before modification.)
**Variant:** `tnn2_barrier_variant.zag` (base + barrier-1 machinery)
**Binary:** `tnn2_barrier_bin` (pinned `znc_linux_x86_64_abed8aa1`)
**Build file:** `tnn2_barrier_build.zag` (variant minus its test-battery
main, plus `barrier_probes.zag`)

### Change: barrier-1 break (visibility)

Per design `f0f223029`, barrier 1 is: "`t2_gather` reads only tag-1
FACTs, never tag-20 MAPs. Prior structures are invisible to
construction."

**1. New helper `gather_structures(W, out)`** (~15 code lines):
scans live tag-20 MAP nodes (`ng(W,m,36)==1 && ng(W,m,0)==20`); for
each, extracts a descriptor (node id, `t2_sig` cell count, provenance
s/r) into `out` and bumps the white-box visibility counter. Returns
visible structure count.

**2. Call site in `t2_gather`** (2 code lines): allocates a 256-byte
descriptor scratch buffer, calls `gather_structures`. Descriptors are
inert: no trial machinery reads them. Construction behavior unchanged.

**3. White-box counters** (2 lines in `tnn2_init`):
- `hg(W,56)`: increments per visible structure per construction event.
- `hg(W,60)`: increments on descriptor reference; no machinery
  references descriptors yet, so it stays 0.

### Implementation correction vs design

The design specified counters at `hg(W,53)` and `hg(W,54)`. During
testing, the visibility run showed `hg(W,52)` (the xfer MAP-branch
counter) corrupted to 256. Root cause: `hg(W,f)` is `get32(W,f)`,
byte offset f, and the header uses 4-byte aligned fields
(0,4,8,...,48,52). Offsets 53/54 overlap field 52's bytes 52-55.
The design's field numbers were corrected to the next free aligned
slots: **56 (visible) and 60 (referenced)**. Same intent, correct
memory layout. The xfer experiment's field audit ("fields in use:
0..48, 52 verified unused") is the authority here.

### Cognition delta (vs xfer variant)

- ~25 lines added (helper + call site + counter init + comments).
- 0 lines modified in existing logic.
- Zero new opcodes, modes, bridges, handlers, semantic cases.
- Zero hardcoded cross-domain mappings.
- Barriers 2/3/4 NOT touched.

## 1. Experimental design

Re-run the xfer A->B protocol (X1-X5, unchanged) plus three barrier
probes (B1-B3), 3/3 byte-identical runs.

**Domain A:** subjects 1-5, relation 11, query relation 40. Promotes a
4-link chain MAP (node 45).
**Domain B:** subjects 100-104, relation 61, query relation 60.
Isomorphic, disjoint namespace.

**Honest prediction** (from design): breaking barrier 1 alone enables
ZERO transfer. White-box should show A-MAP VISIBLE during B's
construction (counter > 0) yet never REFERENCED (counter = 0).

- **B1:** Is the A-MAP visible during B's construction? (counter 56 > 0)
- **B2:** Is any descriptor ever referenced? (counter 60 = 0 expected)
- **B3:** Trial-count comparison, control vs barrier variant. (identical
  expected; zero transfer)

## 2. Results (3/3 byte-identical)

### X1-X5: xfer protocol re-run, all match the xfer experiment

```
X1 A_MAP=45, B_ans=104, B_MAP=89: PASS (both domains solved)
X2 control 3 tried/2 rejected; test 3 tried/2 rejected: identical, zero transfer
X3 ctr_delta=0: no MAP executed during B query
X4 maps 1->2, B_MAP=89, A-MAP byte-identical: fresh build, untouched
X5 B_ans=203, ctr_delta=0, B_MAP=71: short-B by fresh construction
```

Every X-probe output matches `cbd7bc803` exactly. The barrier-1 change
alters no existing behavior.

### B1: A-MAP VISIBLE during B construction

```
B1 A_MAP=45
B1 vis_before_B=0
B1 B_ans=104
B1 vis_after_B=1
B1 vis_delta=1
B1 RESULT: A-MAP VISIBLE during B construction (56 > 0)
```

During B's query, `t2_trial` calls `t2_gather`, which now enumerates
the live A-MAP (node 45, tag-20). One structure visible, counter
incremented once. Barrier 1 is broken: prior structures are now visible
to the construction path.

### B2: descriptors NEVER referenced

```
B2 B_ans=104
B2 ref_counter=0
B2 RESULT: descriptors NEVER referenced (60 = 0); visibility without usability
```

No construction machinery reads the descriptors. The visibility is
genuinely inert, as designed. This documents the gap: seeing is not
using.

### B3: transfer still zero

```
B3 control 3 tried/2 rejected; test 3 tried/2 rejected
B3 RESULT: identical trial counts, zero transfer (prediction holds)
```

## 3. Honest assessment

**The prediction holds exactly.** Breaking barrier 1 alone enables zero
transfer, and the white-box counters show why with precision:

- 56 > 0: the A-MAP was visible during B's construction.
- 60 = 0: nothing referenced it.
- Trial counts identical: visibility changed nothing about what was built.

**This validates the design as a diagnostic instrument.** The counters
separate "could not see" from "saw but could not use." Before this
change, barrier 1 made it impossible to even test whether barriers 3
(exact lookup) or 4 (baked literals) were the binding constraint. Now
the white box shows: the structure is seen, and still unused. The next
question is empirically accessible: if a descriptor WERE referenced,
would barrier 3 or 4 block first?

**What this does NOT establish:** No transfer, no SUF, no L3, no C0-D.
The change is researcher-owned infrastructure (1 researcher-owned
structural decision: make structures visible to gather). Learner-owned
structural decisions remain 0. This is a measurement instrument, not a
capability.

## 4. Standing architectural metric (variant delta vs xfer variant)

- RESEARCHER-OWNED STRUCTURAL DECISIONS: 1 (make structures visible)
- LEARNER-OWNED STRUCTURAL DECISIONS: 0
- SOURCE-ENUMERABLE FORMS: all (no new assemblers)
- SUF DECISIONS: 0
- LEARNER-INTERNAL CRITERIA: 0
- REUSE EVENTS: 0 cross-domain (visible but not used)
- REVISION EVENTS: 0 in this experiment
- COGNITION LINES: +25 added, 0 modified
- MODES: 0, BRIDGES: 0, HANDLERS: 0, SEMANTIC CASES: 0

## 5. Constraints honored

- UNFROZEN VARIANT ONLY. Frozen `tnn2.zag`, `tnn2_bin`, build `f4de7ff46`
  untouched (git status clean). Xfer variant source/binary untouched
  (SHA-256 unchanged).
- Barrier 1 ONLY. Barriers 2/3/4 not implemented.
- No hardcoded cross-domain mappings.
- 3/3 byte-identical runs. Zero em dashes (byte-verified). Paper
  untouched. Nothing pushed. Experiment only, not TNN-3 implementation.

## 6. Deliverables

- `NAMECHECK.md` (Step 0 guard + UNFROZEN VARIANT declaration)
- `BARRIER_IMPL.md` (this report)
- `tnn2_barrier_variant.zag` (variant source)
- `tnn2_barrier_build.zag` (build file: variant minus main + probes)
- `barrier_probes.zag` (X1-X5 + B1-B3 probes)
- `tnn2_barrier_bin` (compiled binary)
- `barrier_run1.txt`, `barrier_run2.txt`, `barrier_run3.txt`
  (3/3 byte-identical)
