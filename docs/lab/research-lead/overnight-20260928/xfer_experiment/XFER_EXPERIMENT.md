# TNN-2 Cross-Domain Transfer Experiment (Unfrozen Variant)

**Status:** EXPERIMENT COMPLETE. Unfrozen variant only. Not a TNN-3 implementation.
**Date:** 2026-10-01 (UTC). **Verdict:** XFER-EXPERIMENT-COMPLETE.
**Worker:** Cross-Domain Transfer Experimenter (subagent).

## 0. What was built

An **unfrozen variant** of frozen TNN-2 (`f4de7ff46`), per Micah's ruling
("try stuff unfrozen as you go on as thats what i imagine TNN being in
production" and "TNN should stay a white box architecture if you need to
find something use the white box"). The frozen source and binary were NOT
modified.

**Variant:** `tnn2_xfer_variant.zag` (copy of `tnn2.zag`, SHA-256 verified
identical before modification, plus two changes)
**Binary:** `tnn2_xfer_bin` (pinned `znc_linux_x86_64_abed8aa1`)
**Build file:** `tnn2_xfer_build.zag` (variant minus its test-battery main,
plus `xfer_probes.zag`)

### Change 1: Delete the shadow teach

In `promote_graph`, the line `ev_teach_in(W,s,r,ans);` is replaced with a
comment. The MAP node becomes the promoted artifact. No exact-match fact
is inserted to shadow the graph it just promoted. (Same as reuse
experiment `ea8fc0ac1`.)

### Change 2: MAP-first lookup in `ev_query`

Inserted 19 lines after `ctx_push` in `ev_query`, before `activate`:
scan all live tag-20 MAPs for exact (s,r), most-recent wins by field24,
execute via `t2_exec`, do activate-equivalent bookkeeping on success,
fall through on -999999.

White-box instrumentation: `hg(W,52)` counts MAP-branch executions.
Field 52 was verified unused by frozen TNN-2 (fields in use: 0, 4, 8,
12, 16, 20, 24, 28, 32, 36, 40, 44, 48). This avoids the ctx ring buffer
at 32/36/40/44 that the reuse experiment's field-32 counter collided
with. Initialized `hs(W,52,0)` in `tnn2_init`.

### Cognition delta

- 19 lines added (MAP-first lookup + instrumentation).
- 1 line replaced with comment (shadow teach deletion).
- 1 line added (`hs(W,52,0)` init).
- Zero new modes, bridges, handlers, semantic cases, opcodes, node types.
- Zero hardcoded cross-domain mappings (task constraint).

## 1. Experimental design

Micah's major target (2026-10-01): "learn structure in context A,
recognize applicability in context B, adapt/invoke it, require fewer
experiences than a fresh learner. Do not hardcode cross-domain mappings
to make this happen."

**Domain A** (subjects 1-5, relation 11, query relation 40):
teach (1,11,2), (2,11,3), (3,11,4), (4,11,5); query (1,40) expects 5.
Promotes a 4-link chain MAP.

**Domain B** (subjects 100-104, relation 61, query relation 60):
teach (100,61,101), (101,61,102), (102,61,103), (103,61,104);
query (100,60) expects 104. Isomorphic to A, disjoint namespace.

**Control:** fresh learner, B facts only, query (100,60).
**Test:** A learned first (MAP promoted), then B facts, query (100,60).

**Measures:** examples-to-criterion proxied by trial counts
(`hg(W,16)` = tried*1024+rejected for the last `t2_trial` call);
white-box MAP-branch counter `hg(W,52)`; MAP census before/after.

Five probes (X1-X5), 3/3 byte-identical runs. Full output in
`xfer_run1.txt` (run2, run3 identical).

## 2. Results

### X1: Baseline, both domains solvable

```
X1 A_MAP=45
X1 B_ans=104
X1 B_MAP=89
X1 PASS: both domains solved, both MAPs exist
```

Both domains solve independently. Two distinct MAPs (nodes 45 and 89).

### X2: Trial counts, control vs transfer learner

```
X2 control_ans=104
X2 control_tried=3
X2 control_rejected=2
X2 test_A_MAP=45
X2 test_ans=104
X2 test_tried=3
X2 test_rejected=2
X2 RESULT: identical trial counts, zero transfer
```

The transfer learner (A then B) used **exactly** the same number of
trials (3 tried, 2 rejected) as the fresh control (B only). Prior
learning of the isomorphic A-structure reduced B's construction cost
by zero.

### X3: White-box, was the A-MAP invoked during B's query?

```
X3 A_MAP=45
X3 ctr_before_B=0
X3 B_ans=104
X3 ctr_after_B=0
X3 ctr_delta=0
X3 RESULT: no MAP executed during B query; A-MAP not invoked
```

The MAP-branch counter did not increment during B's query. The A-MAP
was never executed, consulted, or adapted. B's answer came entirely
from fresh trial construction.

### X4: MAP census, fresh build, A-MAP untouched

```
X4 A_MAP=45
X4 maps_before_B=1
X4 B_ans=104
X4 maps_after_B=2
X4 B_MAP=89
X4 RESULT: exactly one new MAP built; A-MAP byte-identical, untouched
```

B's query created exactly one new MAP (node 89, distinct from 45).
The A-MAP's identifying fields (s=1, r=40, root) are unchanged.
No adaptation, no reference, no link between the two structures.

### X5: Short-B, 3-link chain after 4-link A

```
X5 A_MAP=45
X5 B_ans=203
X5 ctr_delta=0
X5 tried=2
X5 rejected=1
X5 B_MAP=71
X5 RESULT: short-B solved by fresh construction; A-MAP not involved
```

A shorter B chain (3 links, subjects 200-203) is solved by fresh
construction (new MAP node 71). The A-MAP is not involved even where
structural reuse would most visibly help.

## 3. Mechanistic explanation (white box)

Transfer is not merely absent; it is **architecturally impossible** in
the current design. Four independent barriers, each verified by reading
the frozen source:

1. **Trial construction reads only facts.** `t2_gather` (frozen line
   442) scans for `ng(W,n,0)==1` (tag-1 FACT nodes). It never reads
   tag-20 MAPs. Prior structures are invisible to the construction path.

2. **Trial search order is source-fixed.** `t2_trial` tries chains
   k=2..4, then sums, then counts, then single hops, in hardcoded order.
   No learner-state value influences which assembler family is tried
   first. (Adaptive trial order is H3-lite Node 1 territory, not TNN-2.)

3. **MAP lookup is exact (s,r).** The variant's MAP-first scan matches
   `field8==s && field4==r`. A query for (100,60) can never match the
   (1,40) MAP. There is no similarity-based retrieval.

4. **MAPs have literals baked in.** The A-MAP's graph cells contain the
   specific values 1,2,3,4,5. Even if retrieved, it could not execute
   for subject 100 without a rebinding mechanism, which does not exist.

Any one of these barriers alone suffices to guarantee zero transfer.
All four are present.

## 4. What this means

**The honest result:** ZERO cross-domain transfer. Not a little, not
partial. Zero. The transfer learner behaves bit-for-bit identically to
a fresh learner on the new domain (X2 trial counts identical, X3
counter delta zero, X4 A-MAP untouched).

**This is not a bug to patch.** It is a structural fact about the
architecture: TNN-2 has no machinery by which a learned structure in
one namespace could influence construction in another. The reuse-path
fix (MAP-first lookup, no shadow teach) solves same-(s,r) invocation
but is orthogonal to cross-domain recognition.

**Implication for TNN-3:** Cross-domain transfer requires new
architectural machinery, at minimum:
- a retrieval path keyed by structural similarity rather than (s,r);
- a rebinding/adaptation mechanism for baked literals;
- trial construction that consults prior structures.
None of these exist in TNN-2, and none are implied by the reuse fix.
This experiment bounds what the reuse infrastructure can and cannot do.

**Relation to prior results:** Consistent with the transfer analysis
`475c57e23` (C0-D not met; rebuild not invocation) and the reuse
experiment `ea8fc0ac1` (R4: fresh subject rebuilds). This experiment
extends R4's finding from "different subject, same relation shape" to
"different domain entirely" and adds the trial-count identity proof.

## 5. Standing architectural metric (variant delta vs frozen TNN-2)

- RESEARCHER-OWNED STRUCTURAL DECISIONS: 2 (MAP-first ordering;
  shadow-teach deletion)
- LEARNER-OWNED STRUCTURAL DECISIONS: 0
- SOURCE-ENUMERABLE FORMS: all (3 assemblers unchanged)
- SUF DECISIONS: 0
- LEARNER-INTERNAL CRITERIA: 0
- REUSE EVENTS: observed within-domain only (MAP-branch counter);
  cross-domain: 0
- REVISION EVENTS: 0 in this experiment
- COGNITION LINES: +20 added, 1 modified
- MODES: 0, BRIDGES: 0, HANDLERS: 0, SEMANTIC CASES: 0

## 6. Constraints honored

- UNFROZEN VARIANT ONLY. Frozen `tnn2.zag`, `tnn2_bin`, build `f4de7ff46`
  untouched (verified by diff: frozen file has zero modifications).
- No hardcoded cross-domain mappings. The probe namespaces (A: 1-5/11/40,
  B: 100-104/61/60, X5: 200-203/61/60) are arbitrary; the variant contains
  no knowledge of them.
- Honest reporting: the negative result is reported as the result. No
  patching to force transfer.
- 3/3 byte-identical runs. Zero em dashes (byte-verified). Paper
  untouched. Nothing pushed. Experiment only, not TNN-3 implementation.
