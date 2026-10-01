# Shared Substrate: The Five Evaluation Tests (Design)

**Status:** DESIGN ONLY. No implementation proposed, no variant built.
**Date:** 2026-10-01
**Parent:** Shared retention substrate specification (`550fa268b`),
  section 9. This document expands those 5 test sketches into detailed
  test designs: setup, measurements, pass/fail criteria, controls, and
  what each test discriminates.

---

## Cross-cutting rules (all five tests)

1. **Unfrozen variants only.** Every test builds on an unfrozen variant
   of frozen TNN-2 implementing the substrate read/write paths under
   test. Frozen source, frozen preregs, and the paper are never touched.
2. **Determinism.** 3/3 byte-identical runs per test; a measure unstable
   across runs is reported as unstable, not as a result.
3. **Read-path-first.** A test passes only if a production read path
   fires on transcript and the decision identifiably changes (or
   identifiably does not change) because of what was read. Records
   written but never read are theater (T3/T4 pattern); gates that read
   but never change behavior fail the counterfactual.
4. **Scaffolded thresholds reported, not tuned.** The decline threshold,
   abandonment bound, record cap, and strategy minimum-attempts floor
   are researcher-set scaffolding initially (substrate spec section 8).
   Each test reports the values used. Thresholds are fixed before the
   run and never tuned to improve the result.
5. **No threshold tuning.** If a test fails because the scaffolded
   threshold was badly chosen, the finding is "mechanism unproven at
   this threshold," not an invitation to re-run at a better one.
6. **Prereg order.** A frozen prereg for the substrate implementation
   must precede any build; these designs feed that prereg. The tests
   are part of the prereg, not afterthoughts.

What would NOT show the substrate working (substrate spec section 9):
records written but never read; gates reading but never changing
behavior; R ratio improving because the world got easier (difficulty
control broken).

---

## T1. Decline gate test

**What it tests:** The decline read path (substrate spec 5.1): the
query path consults PURSUIT (s, r) `consec_fail` before the trial is
attempted, and returns a distinguished WITHHOLD instead of burning a
trial on a pursuit with an established failure record.

### Setup

- Variant A (gate): unfrozen variant implementing the substrate write
  paths (8-row table, spec 4.3) plus the decline gate in the query
  path, placed before the trial is attempted for a pursuit with an
  existing record.
- Variant B (no gate): the identical variant with the decline gate
  disabled by a flag (same binary, flag-controlled), so the comparison
  is mechanism-vs-mechanism on identical state.
- World: a contrived fail-world. Teach a set of (s, r) keys, then
  query each key repeatedly. The world is constructed so the trial
  always fails for these keys (e.g., no licensing facts exist for the
  trial families to assemble from; the trial exhausts, F2). Use 10
  distinct (s, r) keys, 8 queries each: the first 4 establish the
  failure record, the last 4 are the gate-evaluation queries.
- Scaffolded decline threshold: report the value used (suggest: withhold
  when `consec_fail` >= 3 and no success since). Fixed before the run.

### Measurements

- Per query on the last 4 queries per key: return value
  (WITHHOLD vs pipeline-exhaust -2 vs answer), trial-attempted flag,
  nodes/edges allocated for the query.
- WITHHOLD traces: each decline must name the pursuit key, the
  `consec_fail` value read, and the evidence consulted (source-class
  successes/failures excluding `src_self`), per spec 5.1 trace rule.
- Counterfactual sample: on a held-out subset (2 keys), run with the
  gate disabled (Variant B flag) through the full 8 queries; record
  whether the gate-enabled withholds correspond to attempts that fail
  under Variant B.
- Negative control: 10 fresh (s, r) keys with no record, and 5 keys
  with a recent success (reset-on-success exercised). The gate must
  NOT withhold on either.

### Pass criteria

1. The gate fires: WITHHOLD returned on a nonzero fraction of the
   gate-evaluation queries (the pursuits with established failure).
2. Counterfactual accuracy: on the held-out disabled-gate sample, the
   attempts the gate would have declined in fact fail (>= 80% of
   declined queries would have failed if attempted; the bar is a
   design choice but must be preregistered).
3. WITHHOLD is distinguished from -2 pipeline exhaust in the return
   value and in the log (decline-signal analysis: -2 is exhaust, not
   a choice).
4. No false withholds: zero WITHHOLD on fresh keys and zero on
   recently-succeeded keys (reset-on-success works).
5. Declined attempts do NOT increment `attempts` or `consec_fail`
   (spec 5.1 conservative rule); verify in the substrate snapshot.

### What it discriminates

Whether the decline read path fires in normal production operation
and changes behavior (trial skipped, resources saved), versus theater
(records written, never read). The counterfactual is the load-bearing
part: a gate that withholds on queries that would have succeeded is
worse than no gate.

### Falsification of the gate

If the gate fires but the counterfactual shows withheld queries would
have succeeded (false-withhold rate above the bar), the gate's
criterion is unsound: it is declining for the wrong reason, which is
the C5 failure mode (confident maladaptation), not evidence of
working adaptation.

---

## T2. Abandonment test

**What it tests:** The abandonment read path (substrate spec 5.2):
pursuits whose `consec_fail` exceeds the abandonment bound are marked
ABANDONED and stop consuming trial/revision resources; the minimal
re-engagement (a successful observation for the pursuit's key resets
state to RE-ENGAGED and `consec_fail` to zero) provides the exit from
the stop.

### Setup

- Variant: unfrozen variant with substrate write paths, the decline
  gate, and the abandonment gate. Abandonment applies in two paths:
  the miss path (before re-firing the trial on a repeated (s, r)
  miss) and the contradiction path (before re-firing revision on a
  MAP whose campaign has failed).
- World: 5 (s, r) keys queried 25 times each with no teach events that
  would make them answerable (trial always fails, F2; or revision
  always returns 0, F3 sub-mode). Then, for 3 of the 5 keys, teach a
  successful observation (making the key answerable); the remaining
  2 stay unanswerable. Then query all 5 keys 5 more times.
- Scaffolded abandonment bound: report the value (suggest: mark
  ABANDONED when `consec_fail` >= 10, a strictly deeper bound than the
  decline threshold). Fixed before the run.

### Measurements

- Substrate record snapshots per key after every 5 queries: `state`
  (ACTIVE/ABANDONED/RE-ENGAGED), `consec_fail`, `attempts`.
- Trial-firing count and revision-firing count per key per 5-query
  block.
- Node/edge allocation per key per block (resource consumption).
- Control: identical run with the abandonment gate disabled; expect
  continued re-attempt and continued allocation growth (the current
  accreting behavior documented in `ae76a60a7`).

### Pass criteria

1. ABANDONED transitions occur on transcript for the unanswerable
   keys, with the trace naming the bound crossed.
2. After abandonment, trial and revision do not fire for those keys:
   resource consumption per abandoned pursuit drops to zero in
   subsequent blocks (allocation flatlines).
3. Control comparison: the gate-disabled run shows continued
   re-attempt and continued allocation growth on the same keys.
4. Re-engagement: after the successful observation, the 3 taught keys
   transition to RE-ENGAGED with `consec_fail` reset to zero, and the
   trial fires again on the next query (the stop has an exit; contrast
   with the permanent bootstrap break in `510b6cb42`).
5. The 2 never-taught keys remain ABANDONED (no spurious re-engagement).
6. Decline and abandonment do not double-count: decline's withholds
   did not advance `consec_fail` toward the abandonment bound
   (spec 5.2 ordering note; verify in snapshots).

### What it discriminates

Whether the abandonment lifecycle actually stops resource consumption
(the middle stop working as designed) and whether re-engagement
provides a learner-owned path from "stop" to "resume." The three-stops
synthesis requires all three stops to be exits, not traps.

### Falsification of the gate

If ABANDONED marks appear but trials still fire (the gate is consulted
but does not gate), or if abandonment fires so early that answerable
keys are abandoned (bound too aggressive, no recovery path exercised),
the lifecycle is theater.

---

## T3. Trial reorder test (substrate-backed vs field-32)

**What it tests:** The trial-reorder read path (substrate spec 5.4):
family dispatch order derived from shared STRATEGY records (success
rate over non-self attempts, descending) improves trial efficiency as
well as, or better than, the built H3-lite Node 1 (field-32 Hebbian
swap, `45c55ed83`), and does so from auditable evidence rather than
the executability confound.

### Setup

- Variant C (substrate reorder): unfrozen variant implementing the
  substrate write paths and the 5.4 dispatch (all six STRATEGY family
  records read; order = descending success rate over
  `(attempts - src_self)`; minimum-attempts floor so untried families
  are not buried).
- Variant D (field-32): the built H3-lite Node 1 variant (`45c55ed83`)
  unchanged.
- Variant E (frozen): frozen TNN-2, fixed order (discrimination
  control).
- World: the weak K-LT-5 discrimination world (same prereg, same bar).
  Phase A: 20 misses with count-family bias. Phase B: 20 misses, same
  bias. Use the sealed world if available (evaluator-run), or an
  equivalently biased world for the mechanism comparison. The trial
  must be forced (no direct (s, r) facts; the H2 lesson).
- Metric: E(X) = total `t2_try_verify` invocations per phase;
  R = E(A)/E(B).

### Measurements

- E(A), E(B), R for each variant, 3/3 byte-identical runs.
- Per-family STRATEGY records after Phase A and Phase B for Variant C:
  attempts, successes, `src_self` counts, computed success rates, the
  resulting dispatch order. This is the audit trail the field-32
  mechanism lacks.
- For Variant D: the field-32 counter and resulting order (for the
  head-to-head comparison).

### Pass criteria

1. Variant C: R > 1.15 (same bar as the weak K-LT-5 prereg).
2. Variant E (frozen): R ~= 1.00 (discrimination control; the
   improvement is caused by the reorder mechanism, not the world).
3. Mechanism comparison: report R_C vs R_D. The substrate mechanism
   passes if R_C >= R_D (it matches or beats the narrow counter) AND
   the improvement is auditable (the per-family records show the
   promoted family genuinely succeeded more, excluding self-generated
   confirmations).
4. Difficulty control: the fresh-B control from the weak K-LT-5 prereg
   must hold (B solved with no retained state takes the same examples
   as A solved fresh); otherwise the R ratio is void.
5. Source-exclusion check: recompute the Variant C order including
   `src_self` attempts; if including self-generated attempts changes
   the winning family, report it as a C6 near-miss and the primary
   result stands on the excluding computation.

### What it discriminates

Whether the shared-substrate evidence base (successes and failures,
per-pursuit attribution, source-excluded rates) drives reorder as well
as the narrow private counter, and whether the learned order reflects
genuine success rather than the executability-order confound the
success-criteria analysis identified in masked mode (Node 1 learning
"runnable first" rather than "correct first").

### Falsification of the reorder path

If Variant C fails R > 1.15 while Variant D passes on the same world,
the substrate-backed reorder is not yet a working replacement: the
convergence (spec 5.4) loses the diagnostic. Report which half is
missing (write paths not attributing per family? rate computation
excluding too much? floor burying the good family?).

---

## T4. Falsifiability S2: do narrow counters suffice?

**What it tests:** Learning machinery S2 (spec section 5): "if three
narrow per-decision counters prove sufficient for decline,
abandonment, and forgetting with no composition problems and no
counter proliferation as decisions are added, the shared-substrate
requirement is overstated; narrow counters suffice." This test is
deliberately adversarial to the substrate. The substrate must earn
its keep.

### Setup

- Variant F (narrow): unfrozen variant implementing three narrow
  per-decision counters, added one at a time in three stages:
  - Stage 1 (decline): a per-pursuit failure counter stored on the
    pursuit node itself; the decline gate reads it.
  - Stage 2 (abandonment): a per-pursuit re-attempt counter, separate
    from Stage 1's counter; the abandonment gate reads it.
  - Stage 3 (forgetting): a per-structure idle-since counter;
    eviction consults it.
- Each stage reuses the T1, T2, and retention-input test worlds
  respectively, so the narrow counters face the same behavioral bars
  as the substrate gates.
- The narrow counters must implement the same read-path-first
  discipline (gates that actually fire); otherwise the comparison is
  confounded by implementation quality rather than architecture.

### Measurements

- Stage-by-stage: total counters added, lines of counter-management
  code added, counter-related fields added per node type.
- Composition audit at each stage:
  a. Can abandonment read decline's counter, or must the failure be
     counted twice (the consult-vs-advance double-counting problem
     the substrate solves by design)?
  b. When Stage 2 is added, does Stage 1's behavior change
     (regression from shared mutable state)?
  c. Does any counter's write path need evidence another counter
     already holds (write duplication)?
- Counter proliferation: total counters after all three stages vs
  one counter per decision (linear) or worse.

### Pass criteria (for the substrate claim; i.e., S2 NOT triggered)

At least one of the following is demonstrated on transcript:

1. A composition problem: e.g., decline's withholds inflate
   abandonment's re-attempt count (double-counting), requiring an ad
   hoc exclusion rule that duplicates the substrate's consult/advance
   separation.
2. Counter proliferation worse than linear: adding the third decision
   requires more than one new counter (e.g., a cross-counter
   coordination field).
3. Write duplication: the same outcome event must be recorded in two
   counters with different semantics, and the two can diverge.

### S2 triggered (substrate requirement overstated)

If all three stages pass their behavioral bars (T1/T2/retention
equivalents) with exactly three counters, no composition problems,
no write duplication, and no regression when stages are added, then
S2 is triggered: narrow counters suffice, and the shared-substrate
requirement is overstated. This is a clean kill of the substrate's
architectural-compression argument, and must be reported as such.

### What it discriminates

Whether the shared substrate is a genuine architectural requirement
(composition demands it) or an over-engineered generalization of
three counters that compose fine. The test is symmetric: it can kill
the substrate claim.

### Honesty constraint

The narrow-counter implementer must be genuinely trying to make
narrow counters work, not building a strawman. The fairest version
of this test uses the same engineer for both implementations. If
only one implementation exists, the S2 verdict is provisional.

---

## T5. Cost feasibility test

**What it tests:** Substrate spec 6.4 and learning machinery 3.4:
"the learning machinery hastens saturation. Every retained
consequence consumes budget. Boundedness is a feasibility condition,
not an optimization." A substrate that is cognitively sound but
breaks the budget fails.

### Setup

- Variant G: unfrozen variant implementing the minimal viable set
  (learning machinery 3.3): substrate write paths, decline gate,
  trial reorder. (Abandonment may be included; report which gates are
  active.)
- Baseline: frozen TNN-2 on the same workload.
- Workload: a DYN-1-style lifetime sequence of 200-300 events (mixed
  teaches, queries, misses), sized to stay pre-saturation for the
  baseline so the comparison is about overhead, not about the wall.
- Substrate record cap: report the value used (researcher-set
  scaffolding, spec section 8).

### Measurements (all required by spec 6.4)

1. Substrate records created (total, by key_type).
2. Substrate records reclaimed (total; stalest-first with
   ABANDONED-first tiebreak exercised or not).
3. Substrate node/field cost as a fraction of total state growth
   (nodes + fields attributable to the substrate vs total
   nodes + fields added).
4. Per-experience cost: nodes and edges added per event, Variant G
   vs baseline (the DYN-1 comparison).
5. Events to saturation: at what event count does each variant hit
   the node-budget wall (if within the workload; otherwise report
   projected from the per-experience rate).
6. Read-path cost: substrate lookups per query (the decline lookup
   and the six-family STRATEGY read) measured as scan steps, so the
   per-experience cost includes the read overhead, not just the
   writes.

### Pass criteria

1. All six measurements reported (visibility, not hidden cost).
2. Substrate cost fraction below a preregistered ceiling (suggest:
   <= 20% of total state growth on this workload; the exact number is
   a design choice but must be fixed before the run).
3. The substrate does not bring the saturation wall substantially
   earlier: events-to-saturation for Variant G within 80% of baseline
   (suggest; preregister the exact bar).
4. Reclamation fires under pressure if the record cap is reached in
   the workload; if the cap is never reached, report that the
   reclamation path is untested (not that it works).

### What it discriminates

Feasibility. The cognitive tests (T1-T4) can all pass while the
substrate fails here: a mechanism that doubles state growth to save
a few trials is not viable under the scaling wall (the node budget
fills in hundreds of events; spec 6). This test is the gate between
"the substrate works" and "the substrate can ship."

### Falsification of feasibility

If the substrate's bookkeeping costs exceed the decisions it informs
(e.g., the read-path scan cost per query exceeds the trial cost the
decline gate saves), the substrate fails feasibility even if every
cognitive test passes. Report the ratio explicitly: cost of the
substrate's decisions vs cost of the decisions without it.

---

## Test dependency ordering

The five tests have a natural order, because later tests assume
earlier machinery:

1. T1 (decline) and T2 (abandonment) can run in either order; both
   exercise the PURSUIT write paths and the `consec_fail` lifecycle.
   Run T1 first (shallower gate), then T2.
2. T3 (reorder) requires the STRATEGY write paths and an audited trial
   success criterion (C5). If the success criterion is corrupt
   (V2-style: wrong-but-running counts as success), T3 records garbage
   and its pass would be confident maladaptation. The criterion audit
   precedes T3.
3. T4 (S2) requires working narrow-counter implementations of the T1,
   T2, and retention behaviors. It is the most expensive test
   (three implementation stages) and should run after the substrate's
   own gates are validated, so the behavioral bars are known-good.
4. T5 (cost) should run alongside or immediately after each cognitive
   test's implementation, because cost numbers are only meaningful for
   the exact code under test. At minimum, run T5 on the final
   minimal-viable-set variant.

## What the five tests jointly establish

- T1+T2: the two stopping gates work (decline = reversible shallow,
  abandonment = resumable middle), each with an exit.
- T3: the selection gate (trial reorder) works from shared evidence
  and the evidence is auditable.
- T4: the shared store is architecturally required, not just
  convenient (or: S2 kills it, honestly).
- T5: the whole thing fits in the budget (or: it does not, honestly).

If all five pass, the substrate has earned its place as specified
infrastructure. If any fail, the failure localizes: which gate, which
read path, which assumption (composition? cost? criterion?).

---

## Standing architectural metric (this design)

- RESEARCHER-OWNED STRUCTURAL DECISIONS: 0 added (design only).
- LEARNER-OWNED STRUCTURAL DECISIONS: 0.
- SOURCE-ENUMERABLE FORMS: 0.
- SUF DECISIONS: 0.
- LEARNER-INTERNAL CRITERIA: 0.
- REUSE EVENTS: 0.
- REVISION EVENTS: 0.
- COGNITION LINES: 0.
- MODES: 0. BRIDGES: 0. HANDLERS: 0. SEMANTIC CASES: 0.

Test designs: 5 (T1 decline, T2 abandonment, T3 reorder, T4 S2,
T5 cost). Falsifiability: S2 fully designed (T4); S1/S3/S4/S5
referenced as the surrounding falsifiability context. Explicit
scaffold values: 4 named (decline threshold, abandonment bound,
record cap, strategy floor), all to be fixed in prereg, never tuned.

---

**Verdict: SUBSTRATE-TESTS-COMPLETE.**
