# Decline-Gate Adversary Report

## Verdict

**DECLINE-ADV-COMPLETE: SURVIVES with NEEDS-FIX items.**

The decline gate survives adversarial attack on its core claim (DYN-1 bending
via allocation suppression) but has three specific weaknesses requiring fixes:
1. Total-not-consecutive tally over-declines after intermittent success.
2. No trial-based re-engagement path (teaching works, but trial discovery
   after decline is structurally blocked).
3. N=3 is arbitrary; sensitivity shows linear tradeoff with no principled
   optimum.

The gate does NOT inappropriately transfer declines across domains. Re-engagement
via teaching works immediately (1 teach unsticks).

## Method

Unfrozen variants built from verbatim frozen base (`adv_base.zag`, SHA-256
`a29972ca...` verified). Gate spliced with configurable N (1,2,3,4,5).
Four adversarial drivers, 3/3 byte-identical runs each.

All in `docs/lab/research-lead/overnight-20260928/decline_adversary/`:
- `NAMECHECK.md` (Step 0 guard, scope, provenance)
- `adv_base.zag` (verbatim frozen copy)
- `adv_gate_template.zag`, `adv_gate_N{1,2,3,4,5}.zag` (parameterized gates)
- `adv_driver_{reengage,intermittent,nsens,transfer}.zag` (adversarial drivers)
- `adv_full_*.zag` (spliced variants), `adv_full_*.bin` (binaries)
- `adv_*_run{1,2,3}.txt` (3/3 byte-identical outputs)
- `build_adv.sh` (splice script)

## Adversary 1: N Sensitivity

**Question:** Which N balances robustness vs false-decline? Is N=3 principled?

**Method:** 30 misses (3 keys x 10) with N=0 (no gate),1,2,3,4,5.

**Results (3/3 identical):**

| N | totdn | declines | fullmiss | nodes saved vs N=0 |
|---|-------|----------|----------|-------------------|
| 0 | 61 | 0 | 30 | 0 (baseline) |
| 1 | 7 | 27 | 3 | 54 |
| 2 | 13 | 24 | 6 | 48 |
| 3 | 19 | 21 | 9 | 42 |
| 4 | 25 | 18 | 12 | 36 |
| 5 | 31 | 15 | 15 | 30 |

**Finding:** Perfectly linear tradeoff. Each N increment allows 6 more nodes
(2 per key x 3 keys). N=1 is most aggressive (saves 54, declines 27/30).
N=5 is most conservative (saves 30, declines 15/30).

**No principled optimum.** Without a late-success world to measure false-decline
rate, N cannot be optimized. N=3 is arbitrary. The choice is a robustness vs
savings tradeoff with no learner-internal criterion.

**Status:** NEEDS-FIX. N must either become learner-set (not researcher-set)
or be justified by false-decline measurements in a world with late successes.

## Adversary 2: Re-engagement

**Question:** After declines, does teaching unstick the gate? How many teaches?

**Method:** 10 misses on (501,99) to trigger gate. Teach (501,99,4242).
Query 5 times.

**Results (3/3 identical):**
```
PHASE1: Q0 ret=-2 dn=3, Q1 ret=-2 dn=2, Q2 ret=-2 dn=2,
        Q3-9 ret=-3 dn=0 (7 declines, gate fired after 3)
PHASE2: TEACH ret=9 dn=1
PHASE3: Q0-4 ret=4242 dn=0 (all 5 hit via activate, gate bypassed)
```

**Finding:** Re-engagement WORKS. One teach unsticks immediately. The gate
checks AFTER activate, so taught facts bypass via activate hit. The "implicit
reset" claimed in the decline-gate report is confirmed.

**Cost:** 1 teach. Zero queries lost after teaching.

**Status:** SURVIVES. The narrow exit (teaching) functions as designed.

## Adversary 3: Intermittent Failures (Total vs Consecutive)

**Question:** The tally counts TOTAL failures, not consecutive. Does this
over-decline after intermittent success?

**Method:**
1. 2 failures on (601,99). uncert=2.
2. Teach (601,99,7777), query (success via activate). Check uncert.
3. 2 failures on new key (602,99). Check separate tally.
4. Observe (601,99,8888) to contradict, query.

**Results (3/3 identical):**
```
STEP1: Q0 ret=-2 uncert=1, Q1 ret=-2 uncert=2
STEP2: TEACH, Q ret=7777 uncert=2 (NOT reset to 0)
STEP3: (602,99) Q0 uncert=1, Q1 uncert=2 (separate key, correct)
STEP4: OBSERVE, Q ret=8888 uncert=2
```

**Finding:** CONFIRMED: tally is total, not consecutive. UNCERTAINTY nodes
persist after success. After 2 failures + success, the tally stays at 2.
One more failure would trigger the gate (3 total), even though it was only
1 consecutive failure after the success.

**Implication:** The gate is more aggressive than a "3 consecutive failures"
rule. A key that fails twice, succeeds once, then fails once more is declined.
Whether this is correct depends on semantics:
- If UNCERTAINTY = "cumulative confusion about this key", then total is right.
- If UNCERTAINTY = "consecutive failures", then it should reset on success.

The current design implements cumulative confusion, not consecutive failure.
This is undocumented in the gate report (which says "consecutive" but the
code counts total).

**Status:** NEEDS-FIX. Either:
(a) Document as cumulative-confusion semantics (not consecutive), OR
(b) Implement true consecutive tally by clearing UNCERTAINTY on success.
The report claims "consecutive" but the mechanism is total. This is a
spec-vs-implementation mismatch.

## Adversary 4: Novel-Domain Transfer

**Question:** After declining on domain A, does domain B inherit decline
inappropriately?

**Method:** 30 misses on A (701,702,703). Then 9 misses on B (801,802,803).

**Results (3/3 identical):**
```
PHASE1: Domain A declined. uncert(701)=3, uncert(702)=3, uncert(703)=3.
PHASE2: Domain B NOT declined.
  Q s=801 ret=-2 dn=2 uncert=1 (full inquiry, not withheld)
  Q s=802 ret=-2 dn=2 uncert=1
  Q s=803 ret=-2 dn=2 uncert=1
  ... builds to uncert=3 independently
```

**Finding:** NO inappropriate transfer. The gate is correctly keyed by (s,r).
Domain B runs full inquiry for its first 3 misses, independent of A's declines.

**Status:** SURVIVES. Keying is correct.

## Adversary 5: Late-Success (Structural Analysis)

**Question:** If trial would succeed on attempt 4+, does the gate block it?

**Method:** Structural analysis (not run; trial success after 3 failures
requires engineering a pattern that trial can infer, which is complex).

**Finding:** The gate is checked BEFORE trial in `ev_query`:
```
let n:i32=activate(W,s,r);
if(n>=0){ ... return ...; }  // activate hit bypasses gate
if(dg_uncert_count(W,s,r)>=dg_n()){ ... return -3; }  // GATE HERE
let ans:i32=mp_run(W,s,r,expected,flags);  // trial AFTER gate
```

Any trial that would succeed after N failures is structurally blocked.
Teaching bypasses via activate, but trial-based discovery does not.

In the DYN-1 battery, r=99 trials never succeed, so this cannot fire there.
But in any world where trial COULD succeed late (e.g., after observing
enough data to infer a pattern), the gate would cause a false-decline.

**This is the fundamental false-decline risk.** The gate cannot distinguish:
- "This pursuit is hopeless, stop trying" (correct decline)
- "This pursuit needs one more data point, then trial will succeed"
  (false decline)

**Status:** NEEDS-FIX. The gate needs a re-engagement path for trial-based
learning, not just teaching-based. Options:
(a) Allow periodic "probe" trials after decline (e.g., every 10th query
    runs trial despite gate).
(b) Clear decline on observation (not just teaching), since observations
    can enable trial success.
(c) Make N learner-adaptive based on trial success history.

## Summary of Failures

| Adversary | Result | Severity |
|-----------|--------|----------|
| N sensitivity | N=3 arbitrary, linear tradeoff, no optimum | Medium: needs principled N or learner-set threshold |
| Re-engagement | WORKS (1 teach unsticks) | None: survives |
| Intermittent | Total-not-consecutive confirmed; spec says "consecutive" | Medium: spec-vs-code mismatch, over-declines |
| Transfer | NO inappropriate transfer | None: survives |
| Late-success | Structurally blocked; no trial re-engagement path | High: fundamental false-decline risk |

## Does the Gate Survive?

**Core claim (DYN-1 bending):** YES. The gate bends DYN-1 by suppressing
allocation sites. This survives all adversaries.

**Robustness:** PARTIAL. Three fixes needed:
1. **Clarify tally semantics.** The code counts total failures; the report
   says "consecutive". Either fix the code to reset on success, or fix the
   spec to say "cumulative". Current state is a spec-vs-implementation bug.
2. **Trial re-engagement path.** Teaching unsticks, but trial discovery
   after decline is blocked. Add probe trials or observation-triggered
   reset.
3. **Principled N.** N=3 is arbitrary. Either make it learner-set or measure
   false-decline rate in a late-success world to justify the tradeoff.

**One-System Rule:** HOLDS. Zero new types, fields, modes, bridges, handlers.
The gate reads existing UNCERTAINTY nodes. All fixes can be implemented
within the same substrate (no new machinery required).

## Standing Metrics

- RESEARCHER-OWNED STRUCTURAL DECISIONS: 3 (gate rule, N threshold, tally semantics)
- LEARNER-OWNED STRUCTURAL DECISIONS: 0
- SOURCE-ENUMERABLE FORMS: 0
- SUF DECISIONS: 0
- LEARNER-INTERNAL CRITERIA: 0
- REUSE EVENTS: 0
- REVISION EVENTS: 0
- COGNITION LINES: ~40 (gate) + ~150 (adversarial drivers)
- MODES: 0, BRIDGES: 0, HANDLERS: 0, SEMANTIC CASES: 0

## Constraints Honored

Unfrozen variant only. Frozen source untouched (hash `a29972ca...` verified).
Pure Zag via pinned znc. Safebin active, `which python3 python` empty.
Zero em dashes and zero en dashes byte-verified. Paper untouched.
No sealed worlds. Nothing pushed. All runs 3/3 byte-identical.

## Deliverables

All in `docs/lab/research-lead/overnight-20260928/decline_adversary/`:
- `NAMECHECK.md` (Step 0, scope, provenance)
- `DECLINE_ADVERSARY.md` (this report)
- `adv_base.zag` (verbatim frozen, SHA-256 verified)
- `adv_gate_template.zag`, `adv_gate_N{1,2,3,4,5}.zag`
- `adv_driver_{reengage,intermittent,nsens,transfer}.zag`
- `adv_full_*.zag` (8 spliced variants), `adv_full_*.bin` (8 binaries)
- `adv_*_run{1,2,3}.txt` (all 3/3 byte-identical)
- `build_adv.sh` (splice script)
