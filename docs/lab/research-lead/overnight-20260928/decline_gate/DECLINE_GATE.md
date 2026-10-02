# Decline Gate: DYN-1 Bending Test

## Verdict

**DECLINE-GATE-COMPLETE: BENDS.**

The first mechanism tested that bends DYN-1. Per-event node cost for a
repeatedly-failing pursuit drops from +2 to +0 after 3 consecutive failures.
H3-lite Node 1 (policy reorder) was FLAT; the decline gate bends because it
suppresses structure creation, not just reorders attempts.

## Method

Unfrozen variant `dg_full.zag`: verbatim frozen TNN-2 (`dg_base.zag`,
SHA-256 `a29972ca...` verified) with `ev_query` replaced by the gated
version (see `dg_gate.zag`), test `main` removed, measurement driver
appended. Cognition diff verified: only the gate helpers and gate check
differ; all other functions byte-identical to frozen.

Gate design (minimal, one-system):
- Counter: live UNCERTAINTY (tag 30) nodes keyed (s,r). Each failed miss
  reifies exactly one, so the count is the consecutive-failure tally.
  No new node types, fields, modes, bridges, handlers, or storage.
- Rule: in `ev_query`, after `activate` fails, if the tally >= 3, return
  WITHHOLD (-3, distinguished from -2 exhaust), skip trial, bootstrap,
  and `miss_inquire`. Event preamble (clock/decay/ctx) still runs.
- Reset is implicit: any success path returns before the gate is
  consulted; a later taught fact makes `activate` hit first.
- Researcher-set: N=3 fixed. Sensitivity not run in this pilot.

Same 250-event DYN-1 battery as `003767553` (80 teach, 50 qhit, 50 miss,
50 observe, 20 miss2). 3/3 byte-identical runs (SHA-256
`68b5167b8a8d5a0dec0f9997f6c15e6f4feba64bf2443e9494f40cd4faf920e5`).

## Results

### The bend: repeated-miss cost goes 2 -> 0

Key 101 trace (representative of all 10 miss keys):

| Event | Miss # | ret | dn | de |
|-------|--------|-----|----|----|
| E130 | 1 | -2 | 3 | 3 |
| E140 | 2 | -2 | 2 | 3 |
| E150 | 3 | -2 | 2 | 2 |
| E160 | 4 | -3 | 0 | 0 |
| E170 | 5 | -3 | 0 | 0 |
| E230 | 6 | -3 | 0 | -1 |
| E240 | 7 | -3 | 0 | -1 |

(E130 dn=3 is the first-ever miss creating the policy anchor. E230/E240
de=-1 is clockwork decay TTL expiry, not gate-related.)

### Phase totals vs frozen baseline

| Phase | Baseline totdn | Gate totdn | Declines | Saved |
|-------|---------------|------------|----------|-------|
| A teach (80) | 80 | 80 | 0 | 0 |
| B qhit (50) | 0 | 0 | 0 | 0 |
| C miss (50) | 101 | 61 | 20 | 40 |
| D observe (50) | 100 | 100 | 0 | 0 |
| E miss2 (20) | 40 | 0 | 20 | 40 |

- Phase C: 30 full misses (29 x dn=2, 1 x dn=3) + 20 declines (dn=0).
- Phase E: 20/20 declined, all dn=0.
- No declines outside miss phases (0 in A/B/D).
- UNCERTAINTY census: 30 total, exactly 3 per key (baseline: 70, 7 per key).
- Final: 241 live nodes vs 321 baseline (80 fewer = 40 declined x 2).

### Why it bends where Node 1 did not

Node 1 changed which trial families are attempted; allocation sites are
structural, not policy-gated, so per-event cost stayed flat. The decline
gate suppresses the allocation sites themselves (`miss_inquire` never
runs for declined pursuits). To bend DYN-1, a mechanism must reduce
structures written per event with experience. This one does.

## Counterfactual check (learning-machinery definition)

- (a) Behavioral difference across histories on the same probe: yes.
  Query (101,99) at E130 runs full inquiry; the identical query at E160
  returns WITHHOLD.
- (b) Mediated by learner-state difference: yes, the UNCERTAINTY tally.
- (c) Causally attributable to a production write path: yes,
  `miss_inquire` writes the tally; the gate reads it.

The decline criterion (N=3) is researcher-authored. Bounded L2, not L3,
not a learner-internal criterion.

## Honest limits

1. N=3 is a researcher magic number (fixed; no sensitivity run).
2. The tally counts total failures per key, not strictly consecutive;
   identical in this battery (miss keys never succeed).
3. No re-engagement path: decline is sticky until UNCERTAINTY nodes are
   evicted (forgetting re-opens inquiry).
4. False-decline risk: a trial that would have succeeded on attempt 4+
   is declined. Cannot fire in this battery (r=99 trials never succeed).
5. Novel misses still cost +2 each; the gate bends repeated ignorance,
   not novel ignorance.
6. Decline is a stop with a narrow exit (eviction-driven forgetting);
   richer re-engagement (e.g. successful observation) is future work.

## Standing metrics

- RESEARCHER-OWNED STRUCTURAL DECISIONS: 2 (gate rule, N=3 threshold)
- LEARNER-OWNED STRUCTURAL DECISIONS: 0 (tally values are learner-state
  but the decline criterion is researcher-authored)
- SOURCE-ENUMERABLE FORMS: 0
- SUF DECISIONS: 0
- LEARNER-INTERNAL CRITERIA: 0
- REUSE EVENTS: 0
- REVISION EVENTS: 0
- COGNITION LINES: ~40 added (helpers + gate check + comments)
- MODES: 0, BRIDGES: 0, HANDLERS: 0, SEMANTIC CASES: 0

## Constraints honored

UNFROZEN variant only; frozen source untouched (hash verified before/after).
Pure Zag, safebin, `which python3 python` empty. Zero em dashes
byte-verified. Paper untouched. Nothing pushed. No sealed worlds.

## Deliverables

All in `docs/lab/research-lead/overnight-20260928/decline_gate/`:
- `NAMECHECK.md` (Step 0 toolchain guard, scope, constraints)
- `DECLINE_GATE.md` (this report)
- `dg_base.zag` (verbatim frozen copy, SHA-256 verified)
- `dg_gate.zag` (gate cognition patch: helpers + new ev_query)
- `dg_driver.zag` (DYN-1 driver + decline counters)
- `dg_full.zag` (variant: base minus test main, gate spliced in, driver)
- `dg_bin` (compiled binary)
- `dg_run1.txt`, `dg_run2.txt`, `dg_run3.txt` (3/3 byte-identical)
