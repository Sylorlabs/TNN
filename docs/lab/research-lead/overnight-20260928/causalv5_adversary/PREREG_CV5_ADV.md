# Preregistration: H-CAUSALV5 Red Team (CV5-ADV)

**Date:** 2026-09-29 (PDT)
**Status:** FROZEN (before any adversary fixture, build, or run)
**Researcher:** H-CAUSALV5 Red Team (subagent, independent)
**Branch:** tnn-native-lab
**Target:** H-CAUSALV5 SURVIVES (repair of H-CAUSALV4; R5 counter-evidence
retraction). Builder result: CV5_RESULT.md, causalv5.zag.

## Mission

Assume the H-CAUSALV5 claim is false. Attack the repair at the mechanism
level. The builder's load-bearing claims under test:

- C1: R5 "bounds the X-CV4-1 harm class by making every confirmation
  revisable" (PREREG_CAUSALV5.md).
- C2: R5 is "the general belief-revision requirement for defeasible
  causal claims ... not pattern-matching the attack" (CV5_RESULT.md 3).
- C3: "One counter-episode suffices because the rule is a universal
  claim" (CV5_RESULT.md 3).

Disclosed boundaries (NOT attackable as new findings; reproducing them
is a failed attack): R5 retracts on the FIRST counter-episode with no
graded confidence; the 8-episode X-CV4-1 confirmation remains
uncloseable by observation; re-confirmation uses the existing R4 path.

## Mechanism facts used (read from committed causalv5.zag)

- `dl_retract_check` demotes ACTIVE rules only, on ANY episode e with
  d>0, obs_action_at(seq(e)-d)==xa, ep_ns(e,v)!=nv. No other condition.
- Demotion sets st=PROVISIONAL and support=1. It does NOT reset dl_cs
  (the creation cause context). Re-confirmation therefore needs a
  support whose cause context differs from the ORIGINAL creation
  context.
- Refutation ignores the current action's own learned law for v.
- In prediction (`run_probe`), an ACTIVE delay rule OVERWRITES the
  entry prediction (out[v]=dl_fp), applied after predict_entry.

## Attack X-CV5-1: one-way ratchet (graded confidence + permanent degradation)

**Idea.** R5 erases all accumulated support on one counter-episode, but
re-confirmation demands cause-context novelty against the UNRESET
creation context. In a context-stable environment (the cause always
appears in the creation context), a refuted rule can NEVER re-confirm,
no matter how many honest demonstrations follow. Revision is one-way:
revisable down, not up. The builder disclosed "no graded confidence"
but not the one-way ratchet.

**Fixture** `cv5_adv_deg_obs.txt`: causal3/obs3d.txt (12 episodes; R0 =
(4,2,s2,1) ACTIVE at seq 11, support=2, creation ctx (0,0,0)) then:

- seq13 `T 0 0 0 | 4 | 0 0 0` (cause C_0)
- seq14 `T 0 0 0 | 3 | 0 0 0` (filler X)
- seq15 `T 0 0 0 | 1 | 0 0 0` (refuter R; a4 at seq13)
- seq16 `T 0 0 0 | 4 | 0 0 0` (C_1)
- seq17 `T 0 0 0 | 3 | 0 0 0` (F_1)
- seq18 `T 0 0 0 | 4 | 0 0 1` (E_1, honest re-demonstration)
- seq19 `T 0 0 0 | 4 | 0 0 0` (C_2)
- seq20 `T 0 0 0 | 3 | 0 0 0` (F_2)
- seq21 `T 0 0 0 | 4 | 0 0 1` (E_2)
- seq22 `T 0 0 0 | 4 | 0 0 0` (C_3)
- seq23 `T 0 0 0 | 3 | 0 0 0` (F_3)
- seq24 `T 0 0 0 | 4 | 0 0 1` (E_3)

**Hand derivation (frozen).**
- seq13: no contrad (a4 no-op consistent). No refute (obs_action_at(11)
  = a0 != 4).
- seq14: no contrad (a3 no-op consistent). No refute (obs_action_at(12)
  = a0 != 4).
- seq15: a1 first episode, no contrad. dl_retract_check: R0 ACTIVE,
  obs_action_at(13) = a4 == xa, ep_ns(s2) = 0 != 1. Exactly one
  `# delay rule R0 REFUTED at seq 15` line. st=PROV, support=1.
- seq16: no contrad (no prior E). No attribution. R0 PROV, unchecked.
- seq17: no contrad. Nothing.
- seq18 (E_1): contrad on s2 vs seq5/C_0/C_1 no-ops. delay_attribution:
  d=1 fails for all xa (xa=3 passes pre-check but the global check hits
  frozen seq9: an a4 episode with ns(s2)=0 that had a3 at seq 8).
  d=2, xa=4 passes the global check (all a4 negatives lack a4 at s-2:
  seq5 via a0 at seq3, seq9 via a3 at seq7, C_0 via a0 at seq11, C_1
  via a3 at seq14; positives E_1 have a4 at seq16). dl_add_or_support
  matches R0: support 1->2, PROV, diversity check: cause ctx (0,0,0)
  == creation (0,0,0), div=0: `# delay rule R0 ... NOT CONFIRMED at
  seq 18 ... remains PROVISIONAL`.
- seq19 (C_2): contrad vs E_1 (same state, ns differs). Attribution
  finds no (d,xa) (d=1,xa=3 killed by frozen seq5 positive with a0 at
  s-1; d=2 pre-check fails). Contest opens (diagnostic only; contest
  wins are never consumed by the mechanism). entry_add_ep keeps a4 s2
  law UNCH (E_1 excluded from fx_codes as delay-explained).
- seq20: no contrad. seq21 (E_2): same as E_1: support 2->3, NOT
  CONFIRMED, remains PROVISIONAL.
- seq22: same as C_2 (contest opens, benign). seq23: nothing.
  seq24 (E_3): support 3->4, NOT CONFIRMED, remains PROVISIONAL.

**KILL CRITERION X-CV5-1.** SUCCEEDS (verdict DOWNGRADED) iff the raw
output contains exactly one `R0 REFUTED at seq 15` line, three
`NOT CONFIRMED at seq 18|21|24` + `remains PROVISIONAL` lines, and the
final dump reads `# DL R0 cause=4 d=2 var=s2 fx=SET(1) st=PROV
support=4`. FAILS (defense holds) if R0 re-confirms at any point or the
trace deviates from the derivation for mechanism reasons rather than
fixture bugs (fixture bugs must be fixed and the attack re-run; a fix
that changes the criterion requires a prereg amendment note, and the
original criterion stays on record).

**Interpretation on success.** One counter-episode permanently demotes
a genuine ACTIVE rule in a context-stable environment: three honest
re-demonstrations cannot restore it because R5 does not reset the
creation context. C1 ("bounds the harm class by making every
confirmation revisable") is narrowed: revision is one-way without
context novelty. This goes beyond the disclosed "no graded confidence"
boundary.

## Attack X-CV5-2: masking games the refutation threshold

**Idea.** R5's refutation condition ignores the current action's own
learned law for v. A TRUE delay rule is refuted by an observation fully
explained by the system's own immediate causal knowledge (masking),
which does not falsify the ceteris-paribus delay claim. This attacks C2
("principled belief-revision, not pattern-matching"): the criterion
cannot distinguish falsification from masking.

**Fixture** `cv5_adv_mask_obs.txt`: obs3d.txt (12) then:

- seq13 `T 0 0 0 | 1 | 0 0 2` (a1 first episode; learns immediate law
  s2:=SET(2) directly, no contrad possible)
- seq14 `T 0 0 0 | 4 | 0 0 0` (a4 cause, no contrad)
- seq15 `T 0 0 0 | 3 | 0 0 0` (a3 filler, no contrad)
- seq16 `T 0 0 0 | 1 | 0 0 2` (mask: a1 s2 0->2, consistent with its
  learned law; a4 at seq14)

**Probe** `cv5_adv_mask_probe.txt`:
- `H 0 0 0 | 1`
- `Q 0 0 0 | 1`

**Hand derivation (frozen).** seq13: a1 learns SET(2) (single-episode
law). seq14/15: clean no-ops, no refute (wrong actions at s-2). seq16:
no contrad (prior a1 (0,0,0) has ns(s2)=2). dl_retract_check: R0
ACTIVE, d=2>0, obs_action_at(14)=a4==xa, ep_ns(s2)=2 != 1: `# delay
rule R0 REFUTED at seq 16`. The ENTRY dump shows a1
fx=[UNCH,UNCH,SET(2)]. Probe: entry predicts (0 0 2), R0 PROV inert,
so `Q (0 0 0) | 1 -> (0 0 2)`.

**KILL CRITERION X-CV5-2.** SUCCEEDS (verdict DOWNGRADED) iff the raw
shows `R0 REFUTED at seq 16`, the ENTRY dump shows a1 with
fx=[UNCH,UNCH,SET(2)], and the probe predicts `Q (0 0 0) | 1 ->
(0 0 2)`. FAILS if no refutation occurs. On success: the refuted
observation was fully explained by the learner's own immediate law,
yet the delay rule was demoted. C2/C3 are narrowed: the "universal
claim" test fires on masked observations.

## Attack X-CV5-3: zero-marginal-cost re-arm (re-confirmation abuse)

**Idea.** After refutation, support resets to 1 and the creation
context is NOT reset, so a persistent adversary re-confirms the
SPURIOUS X-CV4-1 rule with a SINGLE episode in any fresh context.
R5 adds zero marginal cost to re-attack: the "harm bound" holds only
against one-shot adversaries.

**Fixture** `cv5_adv_rearm_obs.txt`:
causalv4_adversary/cv4_adv_vary_obs.txt (8 episodes; R0 = (1,1,s2,2)
CONFIRMED at seq 8, creation ctx (1,0,0)) then:

- seq9  `T 0 0 0 | 1 | 0 0 0` (a1 no-op in new state; no same-state
  prior, no contrad; no refute: obs_action_at(8) = a2 != 1)
- seq10 `T 0 0 0 | 1 | 0 0 0` (a1 no-op; no contrad vs seq9;
  dl_retract_check: obs_action_at(9) = a1 == xa, ns(s2) = 0 != 2:
  `# delay rule R0 REFUTED at seq 10`; st=PROV, support=1)
- seq11 `T 0 0 0 | 0 | 0 0 2` (a0 s2 0->2; contrad vs seq1/seq2 SET(1);
  delay_attribution d=1,xa=1: global check over a0 episodes passes
  (positives seq4, seq11 have a1 at s-1; negatives seq2 has a0 at s-1);
  dl_add_or_support matches R0 PROV: support 1->2; diversity:
  cause ctx (0,0,0) != creation (1,0,0): `# delay rule R0 CONFIRMED
  at seq 11`. dl_retract_check after: obs_action_at(10) = a1 == xa
  but ep_ns(s2) = 2 == nv: no refute.)

**Probe** `cv5_adv_rearm_probe.txt` (== vary probe):
- `H 0 0 0 | 1`
- `Q 0 0 1 | 1`

**KILL CRITERION X-CV5-3.** SUCCEEDS (verdict DOWNGRADED) iff the raw
shows `R0 CONFIRMED at seq 8`, `R0 REFUTED at seq 10`, `R0 CONFIRMED
at seq 11`, the final dump shows st=ACT, and the probe shows
`Q (0 0 1) | 1 -> (0 0 2)` (corruption returns). FAILS if
re-confirmation does not occur. On success: C1 is narrowed to
one-shot adversaries; a persistent adversary re-arms at unit cost.

## Attack X-CV5-4: regression (no silent changes)

**Procedure.** Build the COMMITTED causalv5.zag (from git HEAD, not the
working tree) and run:
- (a) cv4_adv_perm_obs/probe vs committed CV5_PERM_RUN.txt (cmp).
- (b) cv4_adv_vary_obs/probe vs committed CV5_VARY_RUN.txt (cmp).
- (c) 3d / double / double2 fixtures vs committed CV4_3D_RUN.txt,
  CV4_DOUBLE_RUN.txt, CV4_DOUBLE2_RUN.txt (cmp).
- (d) diff committed causalv5.zag vs committed causalv4.zag: must be
  exactly the R5 change set (dl_retract_check, the learn_episode
  hook, and associated comments).

**KILL CRITERION X-CV5-4.** SUCCEEDS (regression failure) iff any cmp
differs or (d) shows undeclared mechanism changes. Verdict then per
the failing bar (KILLED only if K-CV5-1/2/3 do not reproduce).
Otherwise the attack FAILS (defense holds).

## Verdict rule

- H-CAUSALV5 SURVIVES iff X-CV5-1, X-CV5-2, X-CV5-3, X-CV5-4 all FAIL
  (defenses hold; findings at most reproduce disclosed boundaries).
- Any of X-CV5-1/2/3 SUCCEEDS: H-CAUSALV5 DOWNGRADED (the R5
  refutation machinery stands and X-CV4-3 stays closed, but the
  "bounds the harm class" / "principled revision" claims are
  narrowed as demonstrated).
- X-CV5-4 mismatch: verdict per the failing bar.

## Governance

- Pure Zag. No Python at any stage (fixtures, builds, runs, greps,
  hashes, cmp). Binaries in /tmp only, never committed.
- This prereg is committed ALONE before any fixture, build, or run.
- Only cv5_adv_* owned paths staged/committed
  (docs/lab/research-lead/overnight-20260928/causalv5_adversary/).
  Concurrent workers' files untouched. No broad git add.
- No em dashes in loop documentation. Commits local only; no push.
