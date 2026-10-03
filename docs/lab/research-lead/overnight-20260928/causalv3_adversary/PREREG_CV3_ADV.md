# Preregistration: H-CAUSALV3 Independent Red Team (CV3-ADV)

**Date:** 2026-09-29 (PDT)
**Status:** FROZEN (before any attack fixture, code, or execution)
**Researcher:** H-CAUSALV3 Red Team (subagent)
**Branch:** tnn-native-lab
**Target:** H-CAUSALV3 SURVIVES (9/9), causalv3.zag (committed)
**Mandate:** Assume the claim is false. Attack the repairs.

## Background

H-CAUSALV3 repairs two H-CAUSALV2 red-team downgrades:
- R1a: delay_clean returns 0 on stasis (ep_ns==ep_s). Closes X-CV2-1 (stasis confounder).
- R1b: dl_add_or_support match key is (cause, delay, var, outcome). Coherence hygiene.
- R2: within-variable ties become ST_AMB over all tied minima. Closes X-CV2-2 (threshold fiat).
- AMEND1: non-covering candidates abstain in agreed-under-ambiguity.

## Attack X-CV3-1: Genuine-change double confounder

**Theory:** R1a blocks stasis confounders (ns==s). But a positioned
confounder can coincide with GENUINE CHANGE. R1a assumes
"genuine change = not a confounder." This is false: if the law
changes to a different genuine outcome, and action 1 (no-op) is
positioned before the flip, delay_clean passes (genuine change,
clean cross-check) and dl_add_or_support confirms (same outcome).
R1b does not help because both confounders share the outcome.

**Fixture** (cv3_adv_double2_obs.txt, frozen verbatim below):
seq1-2 teach a0: s2:=1. seq3 positions action 1 (no-op). seq4 is a
law-change flip (a0, s2 0->2, GENUINE CHANGE). seq5-6 teach a2:
s2:=1 in a separate entry. seq7 positions action 1 again. seq8 is
the second law-change flip (a2, s2 0->2, GENUINE CHANGE).

```
T 0 0 0 | 0 | 0 0 1
T 0 0 0 | 0 | 0 0 1
T 0 0 0 | 1 | 0 0 0
T 0 0 0 | 0 | 0 0 2
T 0 0 0 | 2 | 0 0 1
T 0 0 0 | 2 | 0 0 1
T 0 0 0 | 1 | 0 0 0
T 0 0 0 | 2 | 0 0 2
```

**Probe** (cv3_adv_double2_probe.txt, frozen verbatim below):
```
H 0 0 0 | 1
Q 0 0 1 | 1
```

**Truth:** Action 1 is a no-op throughout (seq3, seq7 leave state
unchanged). The s2:=2 outcomes are law changes. Truth for
Q (0 0 1) | 1 is (0,0,1).

**Kill criteria (both must hold for SUCCEED):**
(a) The dump shows a delay rule `cause=1 d=1 var=s2 fx=SET(2)
st=ACT support=2` (spurious correlation CONFIRMED to ACTIVE).
(b) The harm probe predicts `Q (0 0 1) | 1 -> (0 0 2)` (WRONG;
truth (0,0,1)). The ACTIVE spurious rule fired and corrupted
the prediction.

**Interpretation if SUCCEEDS:** DOWNGRADE. R1a closes the stasis
confounder subclass but not the genuine-change confounder
subclass. Positioned confounders with genuine change still
confirm to ACTIVE. The "confounders do not repeat" rationale
remains false under adversarial stream control.

## Attack X-CV3-2: Two covering candidates agree wrong

**Theory:** Agreed-under-ambiguity predicts on unanimous agreement
among covering candidates. I attempt to force a confident-wrong
prediction with TWO covering candidates agreeing.

**Analysis (preregistered):** For two THR candidates on the same
variable to both cover an unseen probe value and agree, their
cells must have identical fx. But if the cells have identical fx,
no split would have triggered (no UNRES). Therefore two
same-variable THR candidates CANNOT agree-wrong on an unseen
value while maintaining the ambiguity. This attack is expected
to FAIL (defense holds by construction).

**Fixture** (cv3_adv_twothr_obs.txt, frozen verbatim below):
Attempt to construct the impossible case. Observed s0 in {0,2}
with s2 conflict to trigger split.
```
T 0 1 0 | 3 | 0 0 1
T 2 1 0 | 3 | 2 0 0
```

**Probe** (cv3_adv_twothr_probe.txt):
```
Q 1 1 0 | 3
```

**Kill criteria (for SUCCEED):** The probe predicts confidently
(non-WITHHOLD) and WRONG, with >=2 covering candidates agreeing.
**Expected:** FAIL (withhold or correct). If FAILS, this is a
positive finding: the ambiguity machinery is robust against
multi-candidate agreement-wrong.

## Attack X-CV3-3: Vacuous unanimity via abstention

**Theory:** AMEND1: non-covering candidates abstain. If only ONE
candidate covers the probe, its prediction is "unanimous" by
definition. An adversary can choose a probe value where the
cautious candidate (EQ) abstains but the generalizing candidate
(THR) covers and is wrong. Pre-AMEND1 (veto), this would withhold.

**Fixture** (cv3_adv_vac_obs.txt, frozen verbatim below):
s0 in {0,1}. s0=0 works, s0=1 blocked. Tie between THR s0<=0
(2 cells) and EQ s0 (2 cells). THR s0<=1 does not resolve
(only 1 nonempty cell).
```
T 0 1 0 | 3 | 0 0 1
T 1 1 0 | 3 | 1 1 0
```

**Probe** (cv3_adv_vac_probe.txt, frozen verbatim below):
```
Q 2 1 0 | 3
```

**Truth (adversary-defined):** At s0=2, action 3 works: (2,0,1).
(THR s0<=0 generalizes "s0>0 -> blocked" which is wrong at s0=2.)

**Kill criteria (both must hold for SUCCEED):**
(a) The entry is ST_AMB over 2 tied candidates (THR s0<=0, EQ s0).
(b) The probe predicts `Q (2 1 0) | 3 -> (2,1,0)` (confident,
WRONG; truth (2,0,1)). EQ abstains (no s0=2 episodes), THR s0<=0
covers alone and is wrong.

**Interpretation if SUCCEEDS:** BOUNDARY (not downgrade). This
confirms the documented limitation: "a single opinionated
candidate predicts alone when all others abstain." AMEND1 trades
B2's veto-technicality withhold for vacuous-unanimity confident
predictions. The behavior is disclosed, but now empirically
demonstrated as wrong.

## Attack X-CV3-4: Regression on frozen bars

**Theory:** Verify the 9/9 H-CAUSALV3 kill bars reproduce from the
committed source. Any silent change is a finding.

**Method:** Rebuild causalv3.zag from the committed source.
Run all 9 frozen fixtures. Compare to committed CV3_*_RUN.txt
via cmp. Verify K-CV3-1 (0 delay rules, probe correct), K-CV3-2
(3 tied candidates, withhold), K-CV3-3 (regressions), K-CV3-4
(3/3 deterministic).

**Kill criteria (for SUCCEED = regression FAILS):** Any of the
9 fixtures produces output differing from committed CV3_*_RUN.txt,
or any K-CV3 bar fails to reproduce.

**Expected:** FAIL (regression holds).

## Governance

- Prereg committed alone before any attack fixture, code, or execution.
- Pure Zag. No Python in fixtures, execution, or analysis.
- Only adversary-owned files staged/committed.
- No em dashes in documentation.
- 3/3 byte-identical runs for all empirical claims.
