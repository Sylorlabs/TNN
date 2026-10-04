# Preregistration: H-CAUSALV6 (Causal Vocabulary Repair, Round 6)

**Date:** 2026-09-29 (PDT)
**Status:** FROZEN (before any H-CAUSALV6 implementation)
**Researcher:** H-CAUSALV6 Frontier Researcher (subagent)
**Branch:** tnn-native-lab
**Target:** H-CAUSALV5 DOWNGRADED (red team CV5-ADV, CV5_ADV_RESULT.md).
This hypothesis repairs the downgrade findings at the mechanism level.

## Background and failures being repaired

H-CAUSALV5 (R5: counter-evidence retraction) was DOWNGRADED by
independent red team. Three attacks succeeded:

- **X-CV5-1 (one-way ratchet):** SUCCEEDED. One counter-episode
  permanently demotes a genuine ACTIVE delay rule in a
  context-stable environment. Three honest re-demonstrations
  (support 2->3->4) cannot restore it because R5 does not reset
  the creation context dl_cs, so the R4 diversity check can never
  pass when the cause always appears in the creation context
  (0,0,0). Revision is one-way: revisable down, never up without
  context novelty. Narrows C1 ("bounds the harm class by making
  every confirmation revisable").

- **X-CV5-2 (masking games the refutation threshold):** SUCCEEDED.
  The refuting observation (seq16: a1 sets s2 0->2) was fully
  explained by the learner's own immediate law for a1 (learned at
  seq13: s2:=SET(2), reproduced in the probe), yet R5 demoted the
  genuine delay rule (a4,d=2,s2:=1). The refutation condition
  ignores the current action's own learned law for v, so it cannot
  distinguish falsification from masking. Narrows C2 ("principled
  belief-revision") and C3 ("one counter-episode suffices because
  the rule is a universal claim").

- **X-CV5-3 (zero-marginal-cost re-arm):** SUCCEEDED. A persistent
  adversary re-arms the refuted SPURIOUS rule (1,1,s2,2) with a
  SINGLE episode (seq11). Refutation resets support to 1 and keeps
  dl_cs at the original creation context, so one support in any
  fresh context re-confirms (support=2). R5 adds zero marginal cost
  to re-attack. Narrows C1 to one-shot adversaries.

- **X-CV5-4 (regression):** FAILED (defense held). All CV5 raws
  byte-identical; diff causalv5 vs causalv4 is exactly the R5
  change set.

## Repair (frozen mechanism specification)

causalv6.zag = byte-copy of frozen causalv5.zag (committed in
causalv5_repair/, md5 1fc56329a2d6da52104050e3e83406b4) plus ONLY
the R6 changes below. No other mechanism change. In particular,
rule creation (R1a/R1b), delay_clean, the R4 diversity check for
FIRST confirmation, contest behavior, and prediction are untouched.

### New memory

- `O_DL_RF() = 8932`: i32 per delay rule (16 rules max, 64 bytes).
  The refutation floor: the support count the rule had when it was
  last refuted. 0 = never refuted.
- All offsets from O_CD_N onward shift by +64:
  O_CD_N=8996, O_CD_KIND=9000, O_CD_V1=9008, O_CD_P2=9016,
  O_CD_CELLS=9024, O_NEP=9032, O_NENT=9036, O_NCT=9040,
  O_NDL=9044, WSZ=9048.
- New accessors: `dl_rf(W,r)` returns get32(W,O_DL_RF()+r*4).
- Rule creation initializes dl_rf to 0.

### R6a: Refutation records the support floor

In `dl_retract_check`, when an ACTIVE rule is refuted: before
resetting support to 1, save the pre-refutation support into
dl_rf. The emit line is unchanged (still says "REFUTED ...
demoted to PROVISIONAL"). dl_cs is left untouched.

Rationale: the refutation floor is the graded-confidence bar. A
rule that was confirmed with high support must re-earn MORE
support than it had, not just repeat the original 2-support
confirmation. This is the general belief-revision requirement:
a refuted hypothesis needs stronger evidence to be re-adopted.

### R6b: Graded re-confirmation (closes X-CV5-1 and X-CV5-3)

In `dl_add_or_support`, the promotion branch is split:

- If `dl_rf(W,r) == 0` (never refuted): the original R4 logic is
  used unchanged (support>=2 AND cause-context diversity vs
  dl_cs).
- If `dl_rf(W,r) > 0` (previously refuted): the rule is promoted
  to ACTIVE iff `s+1 > dl_rf(W,r)` (support strictly exceeds the
  pre-refutation support). The R4 diversity check is NOT applied;
  the higher support bar replaces it. Rationale: the diversity
  check already vetted the initial confirmation; post-refutation,
  the question is whether new evidence outweighs the refutation,
  which is a quantity question, not a context-diversity question.
  In a context-stable environment, repetition IS the only available
  evidence, and the ratchet must not make it useless.
  - On promotion: clear dl_rf to 0 (the rule is forgiven; a future
    refutation sets a fresh floor). Emit the standard
    `# delay rule R<r> CONFIRMED at seq <s> support=<s+1>
    (provisional -> active)` line.
  - If `s+1 <= dl_rf`: emit
    `# delay rule R<r> supported at seq <s> support=<s+1>`
    followed by
    `# delay rule R<r> NOT RE-CONFIRMED at seq <s>: support
    <s+1> does not exceed pre-refutation <rf>; remains
    PROVISIONAL`.

This closes X-CV5-1: the genuine rule (refuted with support=2,
dl_rf=2) re-confirms when support reaches 3 (two honest
re-demonstrations), without needing context diversity.

This raises the X-CV5-3 re-arm cost: the spurious rule (refuted
with support=2, dl_rf=2) needs support>=3 to re-confirm. A single
adversarial episode (support=2) no longer suffices. The marginal
cost of re-arm is now proportional to the rule's prior support.

### R6c: Masking check (closes X-CV5-2)

In `dl_retract_check`, before demoting an ACTIVE rule R
(cause xa, delay d, var v := nv) at episode e: check whether the
CURRENT action's learned immediate law explains the observation.

New helper `dl_masked(W,e,v,obs)`:
- Let `a_cur = ep_a(W,e)` (the action at the current episode).
- Let `(s0,s1,s2)` be the pre-state `ep_s(W,e,0..2)`.
- Find the best matching ST_ACT entry for `(a_cur, s0,s1,s2)`
  using the same specificity logic as `predict_entry` (highest
  condition-bit count; ST_ACT only, not ST_AMB).
- If no entry matches, return 0 (not masked).
- Let `fx = en_fx(W,best,v)`. If `fx == 0` (UNCH), return 0:
  a passive "unchanged" law is not active masking.
- Compute the predicted value: if `fx_is_set(fx)` then
  `pred = fx_c(fx)`; else if `fx_is_add(fx)` then
  `pred = boundv(sv + fx_d(fx), v)` where `sv = svar(s0,s1,s2,v)`;
  else return 0.
- If `pred == obs`, return 1 (masked). Else return 0.

If `dl_masked` returns 1: do NOT demote. Emit
`# delay rule R<r> NOT REFUTED at seq <s>: cause a=<xa> at seq
<s-d> not followed by s<v>=<nv> (observed <obs>); masked by
a=<a_cur> immediate law; remains ACTIVE`.
The rule's support and status are untouched.

Rationale: the delay rule is a ceteris-paribus claim ("xa at
seq-d causes v:=nv when nothing else intervenes"). If the current
action's own learned law actively predicts the observed outcome,
the ceteris-paribus condition is violated; the observation does
not test the delay rule. Refuting on masked observations is the
X-CV5-2 error. Note: the check runs BEFORE `entry_add_ep` for the
current episode (dl_retract_check is called before entry_add_ep
in learn_episode), so the law used is learned from PRIOR episodes
only, not the current one. This prevents the current episode from
masking itself.

## Frozen kill bars

All fixtures are the red team's frozen attack fixtures, run with
the red team's frozen probe files. Every run is 3/3 byte-identical.

### K-CV6-1: X-CV5-1 ratchet closed (deg fixture)

Fixture: causalv5_adversary/cv5_adv_deg_obs.txt (24 episodes).
Probe: causalv5_adversary/cv5_adv_deg_probe.txt.

Hand-derived expectations:
- Exactly one `# delay rule R0 REFUTED at seq 15` line. (The
  refuter is genuine; a1 has no prior entry at seq15, so no
  masking. dl_rf is set to 2.)
- `# delay rule R0 CONFIRMED at seq 21 support=3 (provisional
  -> active)`. (At seq18: support=2, not > 2, so NOT
  RE-CONFIRMED. At seq21: support=3 > 2, CONFIRMED.)
- Zero `# delay rule R0 NOT CONFIRMED` lines after seq15. (The
  R4 diversity path is not taken for the refuted rule.)
- Final dump: `# DL R0 cause=4 d=2 var=s2 fx=SET(1) st=ACT
  support=4`.
- Probe: `Q (0 0 0) | 3 -> (0 0 1)`. (R0 is ACTIVE; with H=[a4,a3],
  the d=2 delay fires and sets s2:=1.)

KILL if: R0 is not ACTIVE by the end of the fixture, or the probe
does not show the restored delay effect.

### K-CV6-2: X-CV5-2 masking closed (mask fixture)

Fixture: causalv5_adversary/cv5_adv_mask_obs.txt (16 episodes).
Probe: causalv5_adversary/cv5_adv_mask_probe.txt.

Hand-derived expectations:
- Zero `# delay rule R0 REFUTED` lines. (At seq16, the current
  action a1 has a learned ST_ACT law s2:=SET(2) from seq13, which
  predicts obs=2. Masked.)
- One `# delay rule R0 NOT REFUTED at seq 16` line mentioning
  masking by a=1.
- Final dump: `# DL R0 cause=4 d=2 var=s2 fx=SET(1) st=ACT
  support=2`. (Support unchanged from the seq11 confirmation.)
- Probe: `Q (0 0 0) | 1 -> (0 0 2)`. (From the a1 immediate law;
  the delay rule does not fire because nh=1 < d=2. Same as CV5.)

KILL if: R0 is refuted (any REFUTED line), or the final status is
not ACTIVE.

### K-CV6-3: X-CV5-3 re-arm cost raised (rearm fixture)

Fixture: causalv5_adversary/cv5_adv_rearm_obs.txt (11 episodes).
Probe: causalv5_adversary/cv5_adv_rearm_probe.txt.

Hand-derived expectations:
- `# delay rule R0 REFUTED at seq 10` (1 line). (The refuter is
  genuine; a1's law for s2 is UNCH, not an active SET/ADD, so no
  masking. dl_rf is set to 2.)
- At seq11: `# delay rule R0 supported at seq 11 support=2`
  followed by `# delay rule R0 NOT RE-CONFIRMED at seq 11`.
  (support=2 is not > dl_rf=2.)
- Zero `# delay rule R0 CONFIRMED at seq 11` lines.
- Final dump: `# DL R0 cause=1 d=1 var=s2 fx=SET(2) st=PROV
  support=2`.
- Probe: `Q (0 0 1) | 1 -> (0 0 1)`. (R0 is PROV so the delay does
  not fire; the a1 immediate law predicts identity. Not the
  corrupted (0,0,2).)

KILL if: R0 is CONFIRMED at seq11 (re-arm at unit cost still
works), or the probe shows (0,0,2).

### K-CV6-4: Regression (no silent changes)

- The 10 frozen CV4 fixtures (double, thr, mask, 3i2, 3c, 3d, 3i,
  B2, C2, double2): output byte-identical (cmp) to the committed
  CV5 raws. Rationale: no refutations occur in these fixtures
  under CV5, so dl_rf stays 0 and the masking check never fires.
- CV5_PERM_RUN (X-CV4-3): byte-identical to committed
  CV5_PERM_RUN.txt. Rationale: the seq10 refutation is not masked
  (a1's law for s2 is UNCH at seq10; the masking check requires an
  active SET/ADD). dl_rf is set internally but not emitted.
- CV5_VARY_RUN (X-CV4-1): byte-identical to committed
  CV5_VARY_RUN.txt. Rationale: R0 confirms at seq8 via the R4
  path (dl_rf==0); no refutation occurs in the 8-episode fixture.
- Determinism: 3/3 byte-identical on all runs.

KILL if: any regression output differs from the committed CV5
raw, or any run is non-deterministic.

## Classification

Bounded L2 (defeasible causal revision with graded confidence).
Not L3. The repair makes revision symmetric and masking-aware;
it does not advance the learning level.

## Governance

- Pure Zag only. No Python at any stage.
- This prereg is committed alone before any implementation, build,
  or run.
- Only H-CAUSALV6-owned paths will be staged/committed
  (docs/lab/research-lead/overnight-20260928/causalv6_repair/).
- No em dashes in loop documentation.
- Commits stay local; no push.
