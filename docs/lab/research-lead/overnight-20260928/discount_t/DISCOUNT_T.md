# Discount Threshold Sensitivity (T=1, 2, 3)

**Verdict: DISCOUNT-T-COMPLETE.** 3/3 byte-identical runs per threshold.
Committed locally on `tnn-native-lab`. Nothing pushed.

## Method

Three unfrozen variants of the discount pilot (`0daaa2ed4`), differing
only in the R1 exclusion threshold literal (`dt_boot_tN.zag`).
`dt_variant_t2.zag` is byte-identical to the pilot variant, so T=2 is a
true control. Each variant replays the contradiction-break battery
(`510b6cb42`) Phases 1-5 identically, then adds Phase 6: a second
contradiction `(6001,50,99)` on a fresh subject followed by 8 queries,
measuring exclusion latency of the new fact.

## Results (3/3 byte-identical per T)

Phase 2 identical across all T (q0..q3 = 42; discount untouched while
evidence is unanimous). All non-42 answers are -2; the unanimity gate
stays intact at every T.

### First incident (Phase 4, contra `(3001,50,99)`)

| T | b0 | b1 | b2 | b3 | b4 | b5 | failed bootstraps before recovery |
|---|----|----|----|----|----|----|-------------------------------------|
| 1 | -2 (d1) | -2 (d2) | 42 | 42 | 42 | 42 | 2 |
| 2 | -2 (d1) | -2 (d2) | -2 (d3) | 42 | 42 | 42 | 3 |
| 3 | -2 (d1) | -2 (d2) | -2 (d3) | -2 (d4) | 42 | 42 | 4 |

### Second incident (Phase 6, contra `(6001,50,99)`)

| T | f0 | f1 | f2 | f3 | f4 | f5..f7 | failed bootstraps before recovery |
|---|----|----|----|----|----|--------|-------------------------------------|
| 1 | -2 (d1) | -2 (d2) | 42 | 42 | 42 | 42 | 2 |
| 2 | -2 (d1) | -2 (d2) | -2 (d3) | 42 | 42 | 42 | 3 |
| 3 | -2 (d1) | -2 (d2) | -2 (d3) | -2 (d4) | 42 | 42 | 4 |

The predicted **T+1 bound holds exactly for both incidents at all T**:
recovery after T+1 failed bootstraps, first success at b_{T+1} / f_{T+1}.
Phase 6 confirms the mechanism is not a one-shot: a novel contradiction
is handled with the same latency, and the previously excluded fact
stays excluded without interfering.

Window spot-checks at each recovery boundary show the contra fact
absent from the R1-filtered scan (only d0 42s present) when the first
42 fires. Discount counters freeze once the fact is excluded (no
runaway increment: final discounts 2, 3, 4 for T=1, 2, 3).

## Sensitivity reading

- **Speed:** T=1 recovers fastest (2 wasted queries per incident),
  T=3 slowest (4 wasted queries). The cost is linear in T, exactly as
  the spec predicted.
- **False-positive exposure:** T only moves the speed/robustness point.
  At T=1 a fact is excluded after 2 minority appearances; at T=3 after
  4. The spec's stated risk ("W3's majority heuristic punishes truth
  when the majority is wrong") is T-independent: the mechanism is
  source-blind at every T, and excluding the only genuine evidence to
  preserve a self-referential loop happens at all three thresholds.
  Lower T shortens the paralysis window but also silences a
  transiently-disagreeing fact sooner.
- **No T fixes the epistemic problem.** Source provenance (spec C6)
  remains the actual fix. This test reports sensitivity; per the spec
  it does not select a T ("fix once, report T=1/2/3 sensitivity, never
  tune").

## Honest limits

- The battery is the same 5-vs-1 majority shape in both incidents;
  weaker majorities, ties, and multi-fact disagreements were not
  sensitivity-tested.
- W1/W2 (observe path) and Phase 7 not replayed at any T.
- Bounded L2 at all T, not L3, not a learner-internal criterion.

## Standing metrics (this measurement)

- RESEARCHER-OWNED STRUCTURAL DECISIONS: 0 new (threshold literal is a
  parameter of the pilot's 7; variants are measurement scaffolding).
- LEARNER-OWNED STRUCTURAL DECISIONS: 0 new (per-fact discount values
  as in the pilot).
- SOURCE-ENUMERABLE FORMS: 0. SUF DECISIONS: 0.
- LEARNER-INTERNAL CRITERIA: 0. REUSE EVENTS: 0. REVISION EVENTS: 0.
- COGNITION LINES: 0 added. MODES: 0. BRIDGES: 0. HANDLERS: 0.
- SEMANTIC CASES: 0.
