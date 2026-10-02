# Preregistration: H-CAUSALV2 Red Team (CV2-ADV)

**Date:** 2026-09-29 (PDT)
**Status:** FROZEN (before any attack code, fixture, or execution)
**Researcher:** H-CAUSALV2 Red Team (subagent)
**Branch:** tnn-native-lab
**Target:** H-CAUSALV2 SURVIVES (4/4), causalv2.zag
  (docs/lab/research-lead/overnight-20260928/causalv2_repair/)
**Mission:** Assume the H-CAUSALV2 repair claim is false. Attack it.

## Background

H-CAUSALV2 repaired two H-CAUSALV red-team findings:
- R1 (X-CV-2): two-tier delay rules; new rules start PROVISIONAL (inert),
  promoted to ACTIVE only at support=2. Rationale (frozen):
  "Genuine delays repeat; confounders do not."
- R2 (X-CV-3): new world 3i2 where THR wins 2-vs-3 genuinely; the
  amendment tie-break (THR enumerated before EQ, first-added wins ties)
  is retained in code but claimed "provably idle" on 3i2 and "honest
  representational preference" elsewhere.

## Attack X-CV2-1: spurious confirmation via two positioned confounders

**Hypothesis:** The R1 rationale ("confounders do not repeat") is false
under adversarial stream control. Two positioned confounders with the
same (cause, delay, var) and the same outcome value both pass
delay_clean (the cross-check requires same-outcome episodes to share
the cause action, which they do by construction), so the second
confirms the first's PROVISIONAL rule to ACTIVE. The spurious rule
then fires and corrupts predictions.

**Frozen fixture** (cv2_adv_double_obs.txt), 8 episodes:
```
T 0 0 0 | 0 | 0 0 1
T 0 0 0 | 0 | 0 0 1
T 0 0 0 | 1 | 0 0 0
T 0 0 0 | 0 | 0 0 0
T 0 0 0 | 2 | 0 0 1
T 0 0 0 | 2 | 0 0 1
T 0 0 0 | 1 | 0 0 0
T 0 0 0 | 2 | 0 0 0
```
Design: seq1-2 teach a0: s2:=1. seq3 positions action 1 (no-op).
seq4 is the law-change flip (a0, s2 stays 0), contradicting the a0
entry; delay_clean(d=1,xa=1) passes (action at seq3 is 1; same-action
a0 episodes seq1-2 have outcome s2=1 != 0 with preceding actions 0/-1,
both != 1); PROVISIONAL (a=1,d=1,s2) SET(0) support=1 is recorded;
entry 0 goes CONFLICTED (no resolving split). seq5-6 teach a2:
s2:=1 in a separate entry. seq7 positions action 1 again. seq8 is the
second law-change flip (a2, s2 stays 0), contradicting the a2 entry;
delay_clean(d=1,xa=1) passes (action at seq7 is 1; same-action a2
episodes seq5-6 have outcome s2=1 != 0 with preceding actions 0,2,
both != 1); dl_add_or_support matches the existing PROVISIONAL rule
on (cause=1,d=1,var=s2) and promotes it to ACTIVE at support=2.

**Frozen harm probe** (cv2_adv_double_probe.txt):
```
H 0 0 0 | 1
Q 0 0 1 | 1
```
Truth: action 1 is a no-op in this fixture (seq3, seq7 show s2
unchanged), so the correct prediction is (0,0,1).

**KILL CRITERION (downgrade):** The attack SUCCEEDS iff, after running
the frozen fixture through the unmodified committed causalv2.zag,
both hold: (a) the delay-rule dump shows an ACTIVE rule
`cause=1 d=1 var=s2 fx=SET(0)` with `support=2` (the spurious
correlation confirmed), AND (b) the harm probe predicts
`Q (0 0 1) | 1 -> (0 0 0)` (WRONG; the spurious ACTIVE rule fired).
If both hold, the R1 rationale is falsified: positioned confounders
CAN be repeated, and the two-tier system still produces a harmful
ACTIVE spurious rule. Verdict impact: H-CAUSALV2 DOWNGRADED (the
single-confounder fix is real, but the repair claim is narrowed).
If the rule stays PROVISIONAL or the probe predicts (0,0,1) or
WITHHOLD, the attack FAILS.

## Attack X-CV2-2: threshold fiat between t=0 and t=1

**Hypothesis:** The amendment tie-break is still load-bearing with
observable harm. With s0 values {0,2} observed (never 1), both
THR t=0 ({<=0}|{>0}) and THR t=1 ({<=1}|{>1}) resolve with 2 cells, as
does EQ (2 cells). Enumeration order (t=0, t=1, then EQ; first-added
wins ties via strict `<`) selects t=0 arbitrarily. The two thresholds
generalize DIFFERENTLY to the unseen value s0=1 (t=0: {>0}; t=1:
{<=1}), so the fiat choice has predictive consequences, refuting the
code comment's "tied candidates are behaviorally identical" framing
(which holds only on observed cells, while the learner predicts on
unseen cells too).

**Frozen fixture** (cv2_adv_thr_obs.txt), true world law (environment):
depressurize (action 3) is blocked iff temp (s0) >= 2; training shows
only temp 0 and 2:
```
T 0 1 0 | 3 | 0 0 1
T 2 1 0 | 3 | 2 1 0
```
seq2 contradicts the a3 entry on pressure (expected SET(0), observed
UNCH). split_search: s0 values {0,2}. THR t=0: {0}->SET(0),
{2}->UNCH, 2 cells, resolves. THR t=1: {0}->SET(0), {2}->UNCH,
2 cells, resolves. EQ: 2 cells, resolves. Predicted winner by code
inspection: THR t=0 (enumerated first).

**Frozen probe** (cv2_adv_thr_probe.txt):
```
Q 1 1 0 | 3
```
Under the true law (blocked iff s0>=2), s0=1 (warm) works: truth is
(1,0,0). Under the fiat t=0 split, s0=1 falls in {s0>0} -> UNCH ->
(1,1,0), WRONG. (Under t=1 it would fall in {s0<=1} -> SET(0) ->
(1,0,0), correct by luck of the draw; under EQ it would match no
child.)

**KILL CRITERION (downgrade):** The attack SUCCEEDS iff the run shows
`# SPLIT-THR entry 3 by s0 threshold 0 into 2` AND the probe predicts
`Q (1 1 0) | 3 -> (1,1,0)` (WRONG under the frozen true law). If both
hold, the tie-break fiat demonstrably causes a confident wrong
prediction on an unseen value where the alternative fiat choice (t=1)
would be correct and EQ would withhold. Verdict impact: H-CAUSALV2
DOWNGRADED (the R2 "genuinely data-driven" claim does not cover tie
cases; the amendment tie-break remains harm-capable). If threshold 1
is selected, or the probe withholds or predicts (1,0,0), the attack
FAILS. (A spurious PROVISIONAL delay rule may also appear for the
seq2 contradiction; it is inert and does not affect this criterion.)

## Attack X-CV2-3: regression on the frozen K-CV2 bars

**Method:** Re-run the four K-CV2 worlds through the unmodified
committed causalv2.zag: cv_adv_mask_obs.txt + harm probe (K-CV2-1),
obs3i2.txt + probe3i2.txt (K-CV2-2), obs3c/obs3d/obs3i/obs_B2/obs_C2
with their probes (K-CV2-3), each twice for determinism (K-CV2-4).
Compare stdout SHA-256 against the committed raw evidence
(CV2_MASK_RUN.txt, CV2_3I2_RUN.txt, CV2_3D_RUN.txt, CV2_3C_RUN.txt,
CV2_3I_RUN.txt, CV2_B2_RUN.txt, CV2_C2_RUN.txt).

**KILL CRITERION:** Any byte difference from committed evidence, or
any frozen bar failing to reproduce, triggers investigation. A
confirmed frozen-bar failure KILLS or DOWNGRAEDS H-CAUSALV2 per the
bar's own terms. Exact reproduction means the attack FAILS (regression
holds).

## Attack X-CV2-4: source audit

**Method:** Read causalv2.zag directly and verify: (a) the R1 changes
match the frozen prereg spec point for point (ST_PROV=5, provisional
start, support-2 promotion, inert-on-probe via the unchanged
dl_st==ST_ACT gate, emit labels); (b) the probe runner fires only
ST_ACT rules; (c) no test-answer literals (fixture values such as
the 3i2 probe expectations) appear in mechanism code; (d) the
dl_add_or_support match key and its nv-blindness; (e) the split-search
enumeration order and tie-break.

**KILL CRITERION:** If the implementation deviates from the frozen
spec in a way that invalidates a verdict (e.g., provisional rules
can fire, confirmation threshold is not 2, hardcoded fixture
answers), H-CAUSALV2 is DOWNGRADED or KILLED per severity. Full
spec fidelity means the attack FAILS.

## Verdict rule

H-CAUSALV2 is DOWNGRADED iff X-CV2-1 or X-CV2-2 succeeds under its
frozen kill criterion. It is KILLED iff X-CV2-3 shows a frozen bar no
longer passing. If all four attacks fail, H-CAUSALV2 SURVIVES this
red team.

## Governance

- This prereg is committed ALONE before any attack fixture, attack
  code, or execution. No attack run exists at commit time.
- Attack fixtures are frozen above; any deviation is documented as
  an amendment before use.
- Pure Zag. No Python anywhere (fixtures, execution, analysis).
  Shell text tools (grep, sed, sha256sum, cmp) only for inspection.
- No em dashes in loop documentation.
- Only adversary-owned files staged/committed. Concurrent agents'
  files untouched. Binaries in /tmp only.
