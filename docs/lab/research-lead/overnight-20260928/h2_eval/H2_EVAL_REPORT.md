# H2 Evaluation Report

## Status: H2-EVAL-VOID

**Date:** 2026-10-01 (UTC)
**Evaluator:** H2 Evaluator (subagent)
**Authorization:** Micah's H2 ruling (2026-10-01 07:10 PDT); freeze `c15a47d63`

## Verdict

**H2-EVAL-VOID.** The t2_sig structural signature function failed calibration
property (ii). Per the frozen preregistration (section 8), scoring is VOID.
No K-H2-1 through K-H2-4 verdicts are recorded.

Behavioral probe data was gathered as unscored observations (3/3 byte-identical).

## Calibration Failure (Void Condition)

The frozen preregistration (section 8) specifies three calibration properties
for `t2_sig`:

- (i) A 2-hop chain and a 3-hop chain produce DIFFERENT signatures. **PASS**
- (ii) Two 2-hop chains with different literals produce IDENTICAL signatures. **FAIL**
- (iii) A chain and a sum produce DIFFERENT signatures. (structural sensitivity shown by i)

**Root cause:** The frozen `t2_sig` implementation (tnn2.zag lines 511-533,
build `f4de7ff46`) records literal values (`lv`) for tags 101/102. The prereg
specification requires: "Literals (subject/object/value payloads) are EXCLUDED
from the signature."

The implementation contradicts the specification. Two 2-hop chains differing
only in literals produced different signatures.

**Per prereg section 8:** "If any calibration property fails, the evaluation
is void and the signature function must be repaired and re-frozen before any
H2 scoring."

## Behavioral Observations (Unscored, 3/3 Byte-Identical)

All probes ran with the frozen TNN-2 binary. Results are identical across
3 runs.

### H2A (Withhold Trap)

**World:** 50001->50002->50003 (2-hop, wrong); 50001->50011->50012->50013 (3-hop, true=50013)

| Probe | Answer | Correct | MAPs Promoted |
|-------|--------|---------|---------------|
| Masked (flags=1) | 50011 | NO | 0 |
| Control (flags=0, exp=50013) | 50011 | NO | 0 |

**Observation:** Both masked and control returned 50011, a direct fact
(50001,50051,50011), via the `activate` path. The trial (`t2_trial`) never
executed. Zero MAPs promoted.

### H2B-B1 (Confirmable Lie)

**World:** 50101->50102->50103 (true=50103); 50101->50111->50112 (lie=50112)

| Probe | Answer | Promoted Lie? | MAPs |
|-------|--------|---------------|------|
| Lie (flags=0, exp=50112) | 50111 | NO | 0 |

**Observation:** Returned direct fact 50111. The lie (50112) was not promoted
because the trial never ran. Zero fact-contradicting promotions (vacuously).

### H2B-B2 (Unconfirmable Lie)

**World:** 50121->50122->50123 (true=50123); lie=59999

| Probe | Answer | MAPs | Key-Failure Trace? |
|-------|--------|------|-------------------|
| Lie (flags=0, exp=59999) | 50122 | 0 | NO |

**Observation:** Returned direct fact 50122. No MAP promoted. No key-failure
trace recorded in learner state (trial never ran to record it).

### H2B Controls

| Query | Answer | Correct |
|-------|--------|---------|
| (50101,50151) exp=50103 | 50111 | NO |
| (50121,50151) exp=50123 | 50122 | NO |

**Observation:** Both controls FAILED. They returned direct facts, not the
true answers.

### H2C (Own-Criterion Trap)

**World:** Multiple 3-hop chains to 50213 (true)

| Probe | Answer | Correct | MAPs |
|-------|--------|---------|------|
| Masked (flags=1) | 50231 | NO | 0 |
| Control (flags=0, exp=50213) | 50231 | NO | 0 |

**Observation:** Both returned direct fact 50231. Trial never ran.

## Root Cause Analysis

### The Trial Never Runs

The H2 trap worlds include direct OBSERVE facts for the query (subject, relation):
- H2A: (50001,50051,50002) and (50001,50051,50011) exist; query is (50001,50051)
- H2B: (50101,50151,50102) and (50101,50151,50111) exist; query is (50101,50151)
- H2C: (50201,50251,50202), (50201,50251,50211), etc. exist; query is (50201,50251)

In `ev_query` (tnn2.zag line 813):
1. `activate(W,s,r)` finds the highest-bid direct fact
2. If found (n>=0), returns its value immediately
3. The trial (`mp_run` -> `t2_trial`) is only reached if activate returns -1

**Result:** On all H2 worlds, activate succeeds and the trial is bypassed.
The masked/unmasked/lie manipulations target `t2_try_verify`, which is only
called from within the trial. Since the trial never executes, the masking
has no effect.

### Controls Fail Too

The paired unmasked controls also return direct facts, not the true answers.
The discrimination signal (GAP between masked and unmasked) is zero because
both paths hit `activate`.

### Predicted vs Actual

The frozen prereg (section 12) predicted:
- "K-H2-1: the masked branch accepts the FIRST candidate with a clean
  execution value in the fixed researcher search order"

This prediction assumed the trial would run. It does not, because the
world design includes direct facts for the query (s,r).

## Implications for K-H2 Bars

**No K-H2 verdicts are recorded** (evaluation void due to t2_sig).

If the worlds were redesigned to trigger the trial (no direct facts for
query s,r), the predicted outcomes would likely hold:
- K-H2-1: FAIL (masked accepts first executable, which is wrong by design)
- K-H2-2: FAIL (no oracle-vs-facts comparison on verification path)
- K-H2-3: FAIL (zero pure-learner decisions in DOF map)
- K-H2-4: FAIL (promoted graphs never execute at query time)

But these are predictions, not measurements. The current worlds cannot
test them.

## Learner-State Observations

Per Micah's architecture clarification, learner state was NOT reset between
probes within a run. Each probe used a fresh workspace W (driver-side
isolation per probe, as the prereg does not specify cross-probe persistence
for H2).

No learner-state changes were observed across the masked/control pairs
because the trial never ran and no MAPs were promoted. The learner state
after each probe contained only the taught facts (tag-1 nodes) and no
tag-20 MAPs.

## SIG Log

Per the frozen format (`SIG <world-id> <query-id> <run-idx> <decision> <t2_sig-string>`):

All probes logged `refuse none` (no MAP promoted, no signature to record).
The SIG log is present in run1.txt/run2.txt/run3.txt (3/3 byte-identical).

## Recommendations

1. **Repair t2_sig:** Modify the implementation to exclude literals, per the
   frozen specification. Re-freeze the preregistration with the corrected
   function and re-run calibration.

2. **Redesign H2 worlds:** Remove direct facts for the query (subject, relation)
   so that `activate` fails and the trial runs. The trap worlds must force
   multi-hop inference, not direct lookup.

3. **Re-freeze and re-run:** After (1) and (2), freeze the corrected preregistration
   and re-authorize the evaluator.

4. **Alternative:** Test the trial path directly via `mp_run` with synthetic
   workspaces that have no direct facts, bypassing `ev_query`'s activate step.
   This would test the masked branch in isolation.

## Artifacts

- `h2_eval_bin`: evaluation binary (frozen learner + driver harness)
- `run1.txt`, `run2.txt`, `run3.txt`: 3/3 byte-identical outputs
- `h2_driver.zag`: driver source (pure Zag)
- `tnn2_nomain.zag`: frozen source minus main (byte-identical to f4de7ff46)
- `NAMECHECK.md`: Step 0 guard, authorization chain, hash verifications

## Hash Verification Summary

| Asset | Expected | Measured | Status |
|-------|----------|----------|--------|
| h2a_world.txt | be358e7a... | be358e7a... | MATCH |
| h2b_world.txt | 6cac9f6b... | 6cac9f6b... | MATCH |
| h2c_world.txt | 2b721d49... | 2b721d49... | MATCH |
| tnn2_bin | 6044f91f... | 6044f91f... | MATCH |
| tnn2.zag | a29972ca... | a29972ca... | MATCH |

Seal integrity: VERIFIED. No compromise.

## Constraints Honored

- Opened ONLY H2A/H2B/H2C (no other sealed worlds)
- No TNN-2 source or binary modifications (driver harness only)
- Pure Zag throughout (safebin, no Python)
- 3/3 byte-identical runs
- No em dashes
- Paper untouched
- Nothing pushed (local only)
