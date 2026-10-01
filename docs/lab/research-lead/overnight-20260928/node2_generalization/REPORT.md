# Node2-v2 Generalization Report (Micah Q1)

**Verdict: NODE2-GEN-COMPLETE.**
**Date:** 2026-10-01
**Base:** `0988839a2` (K-H3 PASS), ablation `ab1bee9a6`
**All tests:** 3/3 byte-identical, pure Zag, safebin, no Python.

## Question

Can the learner generalize the lesson, not merely store 45?
I.e., does TNN learn HOW consequences should change future behavior,
or does it only execute a researcher-fixed update rule?

## Results Summary

| # | Question | Verdict | Mechanism |
|---|----------|---------|-----------|
| 1 | Threshold plasticity (3 -> 2?) | DOES-NOT-GENERALIZE | Threshold=3 hardcoded; 8x 45-pairs never trigger update |
| 2 | Multiple policies (3 contexts) | GENERALIZES* | Same rule updates 3 independent policies; *requires researcher-added context-keying |
| 3 | Context-dependent (competing) | GENERALIZES* | R1=45/60 coexists with R2=30; *requires context-keying |
| 4 | Revision (45->60->30) | GENERALIZES | Generic 3-consistent rule handles all revisions, no reversal case |
| 5 | Noisy evidence (45,45,46,45) | CONSECUTIVE-ONLY | 1 noise delays update by 3 revelations; requires 3 consecutive, not 3-of-N |

## Test 1: Threshold Plasticity - DOES-NOT-GENERALIZE

**World:** 12 cycles, pattern [45, 45, 99] x4. The correct action is always 45
(2 of 3 revelations agree). 99 is noise on every 3rd revelation.

**Result:** Default stayed 30. History ended (99,45,45). The 8 pairs of 45s
never triggered an update because the 3rd revelation (99) always broke
the 3-consecutive requirement.

**Interpretation:** The threshold=3 is researcher-fixed in
`resolve_uncertainty_v2`:
```
if(a1==a2 && a2==a3 && a1>=0 && a1!=def)
```
There is no mechanism for experience to change the evidence requirement.
The learner cannot discover that "2 consistent are sufficient in this world."
This is a hard architectural limitation, not a tunable parameter.

**To generalize:** Would require a meta-policy that tracks
"how many consistent revelations were actually needed" and adjusts
the threshold. That meta-policy does not exist.

## Test 2: Multiple Policies - GENERALIZES (with researcher modification)

**World:** 3 relations, each with different correct action.
R1 -> 45, R2 -> 60, R3 -> 75. Trained interleaved.

**Result:** All three policies updated independently.
R1=45, R2=60, R3=75. Guides carry context-appropriate actions.

**Modification required:** The original `n2v2_pol_get` finds a single
global policy (tag=40, subtype=2). I added `n2v2_pol_get_ctx(W,ctx)`
which keys policies by context (tag=40, field4=100+ctx), and modified
`miss_inquire` and `ev_observe_aw` to pass `r` (relation) as context.

**Interpretation:** The UPDATE RULE (3-consistent -> write) generalizes
across policies. But the SINGLE-GLOBAL-POLICY architecture is
researcher-fixed. The learner cannot spontaneously create a second
policy node for a new context; the researcher must add the keying.

**Learner-owned:** The three values (45,60,75). Not the keying scheme.

## Test 3: Context-Dependent Competing Policies - GENERALIZES (with modification)

**World:** R1 learns 45, then R2 confirms 30 (default), then R1 revises to 60.
Tests whether competing policies coexist or interfere.

**Result:** R1=60, R2=30. No interference. R2's 30-confirmations did not
affect R1. R1's revision to 60 did not affect R2.

**Interpretation:** With context-keying (from Test 2), the mechanism
maintains competing policies correctly. Without it (original single
policy), R1->45 then R1->60 would be a global replacement, and there
would be no way to have R1=60 while R2=30.

**This answers Micah's question:** "Can it maintain competing policies
when outcomes are context-dependent instead of globally replacing 30
with 45?" Answer: YES, but only after researcher adds context-keying.
The original cannot.

## Test 4: Revision - GENERALIZES

**World:** Phase 1: 3x45 -> 45. Phase 2: 3x60 -> 60. Phase 3: 3x30 -> 30.
Phase 4: new guide carries 30.

**Result:** All phases PASS. 45->60->30 via the generic 3-consistent rule.
No dedicated reversal case. The mechanism treats "revising 45 to 60"
identically to "learning 45 from 30": 3 consistent differing values
trigger the write.

**Interpretation:** This is genuine generalization. The learner does not
need a special "undo" or "reverse" operation. The same consequence-driven
update handles both initial learning and revision. The history-reset
on write ensures clean transitions.

**This is the strongest positive result:** The mechanism learns HOW
consequences change behavior (3 consistent -> update), and this HOW
applies to revision without modification.

## Test 5: Noisy Evidence - CONSECUTIVE-ONLY

**World:** Sequence 45,45,46,45,45,45,45. One noise (46) at position 3.

**Result:** Update fired on cycle 5 (the 3rd consecutive 45 after noise),
not cycle 3. Timeline:
- Cycle 0: a_w=45, default=30 (h=(45,-1,-1))
- Cycle 1: a_w=45, default=30 (h=(45,45,-1))
- Cycle 2: a_w=46, default=30 (h=(46,45,45), not equal)
- Cycle 3: a_w=45, default=30 (h=(45,46,45), not equal)
- Cycle 4: a_w=45, default=30 (h=(45,45,46), not equal)
- Cycle 5: a_w=45, default=45 (h=(45,45,45), UPDATE)
- Cycle 6: a_w=45, default=45 (stable)

**Interpretation:** The mechanism requires 3 CONSECUTIVE consistent
revelations, not 3-of-N. One noise delays the update by 3 extra
revelations (must rebuild the 3-run from scratch).

**Limitation:** In noisy worlds, this is fragile. A 10% noise rate
means the expected wait for 3 consecutive is much longer than 3.
The learner cannot adapt to "3 of 5" or "majority of recent."
This is another researcher-fixed aspect (the equality check).

## Standing Metrics: Researcher vs Learner

### Test 1 (Threshold)
- RESEARCHER-OWNED: Threshold=3, equality check, history length=3, shift-register logic.
- LEARNER-OWNED: 0 (no adaptation occurred; default stayed 30).
- Verdict: Learner column did NOT grow.

### Test 2 (Multiple)
- RESEARCHER-OWNED: Context-keying scheme (field4=100+ctx), 3-revelation rule, policy layout.
- LEARNER-OWNED: 3 (values 45, 60, 75 set by experience).
- Verdict: Learner column grew by 3, but researcher added the keying.

### Test 3 (Context-dependent)
- RESEARCHER-OWNED: Context-keying, update rule.
- LEARNER-OWNED: 2 (R1=60, R2=30; R1 revised from 45 to 60 by experience).
- Verdict: Learner column grew, but on researcher-built foundation.

### Test 4 (Revision)
- RESEARCHER-OWNED: 3-revelation rule, write logic, history reset.
- LEARNER-OWNED: 3 (45, then 60, then 30; each set by experience via generic rule).
- Verdict: Learner column grew by 3 on UNMODIFIED mechanism. Strongest result.

### Test 5 (Noise)
- RESEARCHER-OWNED: Consecutive requirement, equality check.
- LEARNER-OWNED: 1 (45, set after noise delay).
- Verdict: Learner column grew by 1, but mechanism is brittle to noise.

## Overall Assessment

**What generalizes:**
- The 3-consistent update RULE applies to revision (Test 4). The learner
  does not need separate learn vs revise machinery. This is "learning
  how consequences change behavior" at the rule level.

**What does NOT generalize:**
- The threshold (3) cannot be changed by experience (Test 1).
- The single-policy architecture cannot spawn context-specific policies
  without researcher intervention (Tests 2, 3).
- The consecutive requirement cannot relax to majority-of-recent
  in noisy worlds (Test 5).

**Micah's Q1 answer:** TNN learns THAT consequences change behavior
(via the 3-consistent rule), but it does NOT learn HOW MUCH evidence
is needed, WHEN to create new policies, or HOW to handle noise.
Those remain researcher-fixed. The "how" is partially learned
(revision works), but the meta-how (threshold, policy creation,
noise tolerance) is not.

**Learner column growth:** Tests 2-5 added 9 learner-owned values
(45,60,75,60,30,45,45,60,30). But Tests 2-3 required researcher-added
context-keying. Only Tests 4-5 show learner growth on the unmodified
mechanism.

## Artifacts

- `gen_base.zag`: copy of `0988839a2` source (unfrozen)
- `gen_multi.zag`: with context-keyed policies (tag=40, field4=100+ctx)
- `gen_test1_threshold.zag` .. `gen_test5_noise.zag`: drivers
- `gen_test1_bin` .. `gen_test5_bin`: binaries
- `run_t1_r1.txt` .. `run_t5_r3.txt`: 3/3 outputs per test
- `build.sh`: build script

All commits local, explicit pathspecs, nothing pushed.
Zero em/en dashes in documentation (byte-verified).
Paper untouched.
