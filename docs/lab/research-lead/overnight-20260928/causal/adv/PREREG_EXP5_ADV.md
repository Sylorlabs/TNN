# Preregistration: H-EXP5 Red Team (Adversary)

Date: 2026-09-29. Pure Zag. This prereg is frozen BEFORE any
adversarial fixture is executed against exp_invent5. No Python at
any stage. Mechanism: exp_invent5.zag (H-EXP5, SURVIVES 6/6).
Adversary assumes the H-EXP5 claim is false.

## Target claim

H-EXP5 "half-closed" the H-EXP4 gap "(which action sets which
value...)" by reporting per-(action,variable,value)
observed-outcome achievability. The result doc presents K-E5-2
(S1: "lamp==1 demonstrated by {2} (1 ep)" coexisting with the
NEEDS-EXTERNAL-SETUP flag for lamp) as "the sharpest honesty
property of H-EXP5: demonstrated-as-outcome does not clear the
change-based hazard flag."

## Attack X-E5-1: flag-silent carryover demonstration

**Setup.** Fixture F1 (new file, derived from S1/cum_B.txt):
lamp changes 1->0 once via action 0 (so ctrl[lamp]==1 and the
per-variable NEEDS-EXTERNAL-SETUP flag is SILENT for lamp), while
lamp==1 is observed ONLY as no-change carryover (start lamp==1,
outcome lamp==1) via action 2. temp and pressure remain
controllable as in S1.

**Rationale.** K-E5-2's honesty property was demonstrated in the
flag-FIRES case. Here the backstop is silent. If the top pick (or
any ranked pick) requires lamp==1, the ACHIEVABILITY line will
read "lamp==1 demonstrated by action(s) {2} (N eps)" with no
hazard flag for lamp and no per-line carryover signal, although
no action ever produced lamp==1 as a change.

**Kill criterion (DOWNGRADE, not kill).** The attack SUCCEEDS if:
(1) some ranked pick requires lamp==1; (2) every action-2
episode with outcome lamp==1 has start lamp==1 (verified from
the fixture: all carryover, zero changes to lamp==1 by any
action); (3) the REACHABILITY line for that pick does NOT flag
lamp; (4) the ACHIEVABILITY line reports "demonstrated by"
for lamp==1 with no per-line indication that the demonstrations
are carryover-only. Success narrows the K-E5-2 honesty property:
it holds only when the per-variable change flag fires, and the
flag's granularity (per-variable) is coarser than the
achievability claim (per-(variable,value)).

## Attack X-E5-2: lumped change-action and carryover-action

**Setup.** Uses the FROZEN S1 fixture (cum_B.txt), ranked state
[2] (2 0 0), which requires temp==2. From the S1 episodes:
action 0 yields temp==2 twice (T 1 0 0 | 0 | 2 0 0 is a
1->2 change; T 2 0 0 | 0 | 2 0 0 is 2->2 carryover);
action 2 yields temp==2 twice (T 2 1 0 | 2 | 2 1 0 and
T 2 0 1 | 2 | 2 0 1, both 2->2 carryover, zero changes).

**Rationale.** The ACHIEVABILITY line for [2] reads "temp==2
demonstrated by action(s) {0,2} (4 eps)", lumping an action
with change-evidence and an action with carryover-only
evidence, with no per-action change signal. A setup planner
choosing between actions 0 and 2 gets no machine-readable
indication that action 2 never changed temp to 2.

**Kill criterion (DOWNGRADE).** The attack SUCCEEDS if the
reproduced S1 output contains the lumped line for a pick
requiring temp==2 AND per-episode verification confirms
action 2's temp==2 outcomes are all carryover (start==outcome)
while action 0 has at least one genuine change to temp==2.
Success shows the "which action" half of the closed gap does
not distinguish change-evidence from carryover-evidence at
the granularity the line is consumed.

## Attack X-E5-3: regression and reproduction

**Setup.** Rebuild exp_invent5.zag with znc 2026.07.0-dev in
/tmp (no repo binaries committed). Run the four frozen
fixtures (S1=cum_B.txt, S2=exp_obs2.txt, S0=exp_null.txt,
A1=x_e3_a1.txt). Compare md5 against the committed evidence
in EXP5_RESULT.md (S1 ae8d42e417f38228de6aa707350bf5bd,
S2 cd949065b4ad6ed4f33dbbd47bdacf2e,
S0 64fc5fde5f36107e2889ccf2703bef42,
A1 4c4e9954fe4fcbd64470e777f934515c).
Diff exp5 vs exp4 outputs to confirm only added lines differ.

**Kill criterion (KILL of the 6/6 if failed).** The attack
SUCCEEDS (as a kill) if any reproduced md5 differs from the
committed evidence, or if the exp5-vs-exp4 diff shows any
change outside the four preregistered additions (ACHV table,
ACHIEVABILITY lines, replaced legend). If all match, X-E5-3
FAILS (regression holds).

## Attack X-E5-4: source audit

**Setup.** Static inspection of exp_invent5.zag against
PREREG_EXP5.md: (a) compute_achievability uses 36 i32 cells,
index ((a*3)+v)*3+x, counts EP_ACT episodes only, outcome
values from ep_ns, clamped to 0..2, actions guarded to 0..3;
(b) emit_achv_table and emit_achievability formats match the
frozen format strings exactly; (c) legend text matches the
frozen legend exactly; (d) no test-answer literals (fixture
values, expected counts) in mechanism code; (e) diff
exp_invent4.zag vs exp_invent5.zag shows ONLY the four
preregistered additions.

**Kill criterion (KILL/DOWNGRADE).** SUCCEEDS if any check
fails: wrong counts, format deviation, legend deviation,
test literals, or undeclared logic changes. Any success is
reported with exact line numbers.

## Governance

Prereg frozen before any adversarial execution. Pure Zag.
Only adversary-owned files staged/committed. No em dashes.
Determinism: 3/3 byte-identical runs for new fixtures.
