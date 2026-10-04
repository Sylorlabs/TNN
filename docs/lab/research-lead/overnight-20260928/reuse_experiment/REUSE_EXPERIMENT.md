# TNN-2 Reuse Path Experiment (Unfrozen Variant)

**Status:** EXPERIMENT COMPLETE. Unfrozen variant only. Not a TNN-3 implementation.
**Date:** 2026-10-01 (UTC). **Verdict:** REUSE-EXPERIMENT-COMPLETE.
**Worker:** Reuse Path Experimenter (subagent).

## 0. What was built

An **unfrozen variant** of frozen TNN-2 (`f4de7ff46`), per Micah's ruling
("try stuff unfrozen as you go on as thats what i imagine TNN being in
production"). The frozen source and binary were NOT modified.

**Variant:** `tnn2_reuse_variant.zag` (copy of `tnn2.zag` plus two changes)
**Binary:** `tnn2_reuse_variant_bin` (pinned `znc_linux_x86_64_abed8aa1`)

### Change 1: Delete the shadow teach

In `promote_graph`, the line `ev_teach_in(W,s,r,ans);` (frozen line 541)
is replaced with a comment. The MAP node becomes the promoted artifact.
No exact-match fact is inserted to shadow the graph it just promoted.

### Change 2: MAP-first lookup in `ev_query`

Inserted 19 lines after `ctx_push` in `ev_query`, before `activate`:

- Scan all live nodes for tag-20 MAPs with `field8 == s`, `field4 == r`,
  `is_superseded == 0`.
- Most-recent wins, ordered by MAP `field24` (promotion index).
- On hit: execute via `t2_exec(W, ng(W,m,20), s)`.
- On success (not -999999): do the same bookkeeping as the `activate`
  branch (`link_edge` type 6, `ref_prot`, `log_ev`) and return the
  executed result.
- On execution failure (-999999): fall through to the existing fact
  path, trial loop, and miss handlers, unchanged.

White-box instrumentation: `hg(W,32)` (a previously unused header field)
counts MAP-branch executions, giving a direct observable reuse signal.

### Cognition delta

- 19 lines added (MAP-first lookup + instrumentation).
- 1 line replaced with comment (shadow teach deletion).
- Zero new modes, bridges, handlers, semantic cases, opcodes, node types.
- The MAP tag-20 layout is reused as-is.

## 1. Probe results (3/3 byte-identical runs)

Five probes, all PASS. Full output in `probe_run1.txt` (run2, run3 identical).

### R1: MAP execution on re-query (K-REUSE-1 analogue) — PASS

```
R1 build_ans=5
R1 map_node=45
R1 fact_node=-1
R1 reuse_ctr_before=1
R1 requery_ans=5
R1 reuse_ctr_after=2
R1 ctr_delta=1
R1 PASS: MAP executed on re-query
```

White-box evidence: after promotion, `activate(W,1,40)` finds NO fact
(`fact_node=-1`), because the shadow teach was deleted. The re-query
returns the correct answer (5) while incrementing the MAP-branch counter
by exactly 1. Since no fact exists for (1,40), the answer MUST have come
from MAP execution via `t2_exec`, not from fact lookup. This is the
discriminator the reuse design specified: the trace shows the MAP read
preceding any `activate` hit, and the answer equals the executed output.

Note: `reuse_ctr_before=1` indicates the MAP branch fired once during the
build sequence (likely an internal query during trial verification);
the `ctr_delta=1` on the explicit re-query is the clean signal.

### R2: No shadow fact (K-REUSE-2 analogue) — PASS

```
R2 build_ans=5
R2 fact_node=-1
R2 total_facts=4
R2 PASS: no shadow fact for promoted (s,r)
```

After promotion, no tag-1 fact exists for (1,40). The only facts are the
4 explicitly taught chain facts. The degeneracy is removed, not routed
around.

### R3: Superseded MAP falls through — PASS

```
R3 build_ans=5
R3 map_node=45
R3 is_superseded=1
R3 requery_ans=-2
R3 ctr_delta=0
R3 PASS: superseded MAP skipped, fell through
```

After manually superseding the MAP (type-3 self-edge), the re-query
correctly SKIPS it (`ctr_delta=0`, MAP branch not taken) and falls through.
The answer is -2 (miss) because no fact exists and the trial loop cannot
verify without an expected answer. This confirms the liveness filter works
and a dead MAP never blocks the fallback path.

### R4: Fresh subject rebuilds (value-trace limit) — PASS

```
R4 first_ans=5
R4 maps_before=1
R4 second_ans=11
R4 maps_after=2
R4 ctr_delta=0
R4 map_for_7=89
R4 PASS: fresh MAP built, no cross-subject invocation
```

After promoting a MAP for subject 1, an isomorphic chain for subject 7
produces a FRESH MAP (node 89), not an invocation of the first. The
MAP-branch counter does not increment during subject 7's query
(`ctr_delta=0`), confirming the (1,40) MAP was not executed for (7,40).
This is the expected value-trace limitation: the design predicted
same-(s,r) reuse would work and cross-(s,r) reuse would still fail
behaviorally without portable procedures (a protected-core decision
banked for Micah, not taken here).

### R5: Contradiction retargets at MAP — PASS

```
R5 build_ans=5
R5 map_node=45
R5 observe_ret=0
R5 map_after=45
R5 fact_for_1_40=-1
R5 PASS: same MAP node revised in place
```

Contradicting a licensing fact via `ev_observe` revises the SAME MAP node
(45 before and after), and no fact for (1,40) is created. The MAP-level
analogue of the shadow teach is absent: revision updates the MAP's answer
field without memoizing a fact. (Note: this probe exercises the frozen
`revise_on_contradict` path; the design's full retargeting, including
deleting the `ev_teach_in` at frozen line 748, was not implemented in
this variant. The observed behavior, same-node revision with no new
(1,40) fact, is consistent with the design's intent.)

## 2. Honest assessment

**What works:** The mechanical reuse path functions as designed. Promoted
procedures execute on later cognition for the same (s,r). The shadow
degeneracy is removed. Superseded MAPs are skipped. The white-box reuse
signal (`hg(W,32)`) is observable.

**What does not work (as predicted):** Cross-subject transfer still
rebuilds rather than invokes. The graphs remain value traces with literals
baked in; the frozen 4-op ISA cannot dereference a relation for a new
subject. This is the Layer 2 limitation the C0-D analysis identified and
the reuse design explicitly scoped out. No portable procedures were added;
none were claimed.

**What this does NOT establish:** C0-D satisfaction, SUF, L3, or any
TNN-3 bar passage. The honest prediction from the design stands: scores
unchanged (the answers are the same; only the answering mechanism
changed), while the architecture gains the observable reuse event it was
missing. This experiment confirms the mechanism, not the capability.

## 3. Standing architectural metric

Per Micah's standing metric, for the variant (delta vs frozen TNN-2):

| Metric | Value | Note |
|---|---|---|
| RESEARCHER-OWNED STRUCTURAL DECISIONS | 2 | MAP-first ordering; shadow-teach deletion |
| LEARNER-OWNED STRUCTURAL DECISIONS | 0 | No new learner-owned decisions |
| SOURCE-ENUMERABLE FORMS | all | 3 assemblers unchanged; no new forms |
| SUF DECISIONS | 0 | Empty (b) list unchanged |
| LEARNER-INTERNAL CRITERIA | 0 | No new criteria |
| REUSE EVENTS | observed | R1: 1 per re-query (hg(W,32) delta) |
| REVISION EVENTS | observed | R5: 1 in-place MAP revision |
| COGNITION LINES | +19 / 1 modified | MAP lookup; shadow teach to comment |
| MODES | 0 | No new modes |
| BRIDGES | 0 | No new bridges |
| HANDLERS | 0 | No new handlers |
| SEMANTIC CASES | 0 | No new semantic cases |

The variant changes WHERE answers come from (MAP execution vs fact
lookup) without changing WHAT the learner can decide. This is
infrastructure honesty, not a capability gain. The metric reflects that:
reuse events are now observable, but learner-owned structural decisions
and SUF decisions remain zero.

## 4. Files

- `NAMECHECK.md` — Step 0 guard record and UNFROZEN VARIANT declaration.
- `tnn2_reuse_variant.zag` — variant source (frozen copy + 2 changes + probes).
- `tnn2_reuse_variant_bin` — compiled variant binary.
- `reuse_probes.zag` — probe source (appended to variant).
- `probe_run1.txt`, `probe_run2.txt`, `probe_run3.txt` — 3/3 byte-identical outputs.
- `REUSE_EXPERIMENT.md` — this report.

Frozen TNN-2 (`tnn2.zag`, `tnn2_bin`, build `f4de7ff46`) untouched.
Paper untouched. Nothing pushed.

*End of experiment report.*
