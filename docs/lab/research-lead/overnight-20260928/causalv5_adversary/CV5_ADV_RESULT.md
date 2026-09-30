# H-CAUSALV5 Red Team Result (CV5-ADV)

**Date:** 2026-09-29 (PDT)
**Researcher:** H-CAUSALV5 Red Team (subagent, independent)
**Branch:** tnn-native-lab
**Target:** H-CAUSALV5 SURVIVES (repair of H-CAUSALV4; R5 counter-evidence
retraction). Builder artifacts: causalv5_repair/PREREG_CAUSALV5.md,
causalv5_repair/CV5_RESULT.md, causalv5_repair/causalv5.zag.
**Verdict: H-CAUSALV5 DOWNGRADED.** Three of four attacks succeed. The
R5 refutation machinery stands (X-CV4-3 stays closed; regression is
byte-clean), but the builder's claims "bounds the X-CV4-1 harm class by
making every confirmation revisable" and "general belief-revision
requirement, not pattern-matching the attack" are narrowed as shown
below. Classification stays bounded L2; nothing here bears on L3.

## Preregistration and commit lineage

- Adversary prereg frozen ALONE at commit `f80720b3d` (1 file:
  causalv5_adversary/PREREG_CV5_ADV.md), BEFORE any fixture, build, or
  run. Verified: no attack file predates it.
- This result + fixtures + raws committed locally after execution (see
  commit at end). No push (Micah alone pushes).
- Frozen kill criteria per attack are quoted verbatim in the prereg.
  No criterion was weakened or altered after execution. All three
  successful attacks met their frozen criteria exactly as written.

## Method (exact)

1. Extracted the COMMITTED causalv5.zag from git HEAD (not the working
   tree) to /tmp/cv5adv. `cmp` confirmed it matches the working-tree
   copy; md5 = 1fc56329a2d6da52104050e3e83406b4 (matches the builder's
   recorded value).
2. Compiled with the repo znc binary
   (/home/hatch/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc
   --build) to /tmp/cv5adv/cv5. Binary in /tmp only, never committed.
3. Ran each attack fixture 3/3 through the binary; `cmp` across runs.
4. Checked traces with grep/cmp/md5sum only. Pure Zag. No Python at any
   stage (no fixtures, builds, runs, greps, hashes, or scratch used it).
5. Regression: built-from-HEAD binary on the committed fixtures; `cmp`
   against committed raws; `diff` of committed causalv5.zag vs
   committed causalv4.zag.

## X-CV5-1: one-way ratchet (graded confidence + permanent degradation)

**Fixture:** cv5_adv_deg_obs.txt (24 episodes): causal3/obs3d.txt's 12
(frozen; R0 = (4,2,s2,1) ACTIVE at seq 11, support=2, creation ctx
(0,0,0)) + refuter triple [C_0 a4 no-op @13, X a3 no-op @14, R a1
no-op @15] + three support blocks [C_k a4 no-op, F_k a3 no-op, E_k a4
s2 0->1] at 16-18, 19-21, 22-24.

**Result: SUCCEEDS (verdict DOWNGRADED).** Raw: CV5_ADV_DEG_RUN.txt,
md5 48e7892b8fa0135994619460af338f72, 3/3 byte-identical.

Exact trace (full, verbatim):

```
# PROVISIONAL-DELAY-RULE R0: cause a=4 d=2 -> s2 SET(1) support=1 (unconfirmed)
# delay-attributed var s2 of seq 7 to R0
# delay rule R0 CONFIRMED at seq 11 support=2 (provisional -> active)
# delay-attributed var s2 of seq 11 to R0
# opened contest C0 at seq 14
# delay rule R0 REFUTED at seq 15: cause a=4 at seq 13 not followed by s2=1 (observed 0); demoted to PROVISIONAL
# contest C0 resolved at seq 16 old=3 new=0 OLD-LAW-WINS
# opened contest C1 at seq 17
# delay rule R0 supported at seq 18 support=2
# delay rule R0 NOT CONFIRMED at seq 18: cause context identical to creation; remains PROVISIONAL
# delay-attributed var s2 of seq 18 to R0
# contest C1 resolved at seq 19 old=2 new=1 OLD-LAW-WINS
# opened contest C2 at seq 19
# opened contest C3 at seq 20
# contest C2 resolved at seq 21 old=2 new=1 OLD-LAW-WINS
# delay rule R0 supported at seq 21 support=3
# delay rule R0 NOT CONFIRMED at seq 21: cause context identical to creation; remains PROVISIONAL
# delay-attributed var s2 of seq 21 to R0
# contest C3 resolved at seq 22 old=2 new=1 OLD-LAW-WINS
# opened contest C4 at seq 22
# opened contest C5 at seq 23
# contest C4 resolved at seq 24 old=2 new=1 OLD-LAW-WINS
# delay rule R0 supported at seq 24 support=4
# delay rule R0 NOT CONFIRMED at seq 24: cause context identical to creation; remains PROVISIONAL
# delay-attributed var s2 of seq 24 to R0
# learned 24 episodes, 5 entries, 6 contests, 1 delay rules
# ENTRY 4 a=4 cond=[] st=1 fx=[UNCH,UNCH,UNCH] par=-1 ne=9
# DELAY RULES
# DL R0 cause=4 d=2 var=s2 fx=SET(1) st=PROV support=4
=== PROBES ===
Q (0 0 0) | 3 -> (0 0 0)
```

Against the frozen criterion: exactly one `R0 REFUTED at seq 15` line
(PASS); three `NOT CONFIRMED at seq 18|21|24` + `remains PROVISIONAL`
lines (PASS); final dump `st=PROV support=4` (PASS).

**Causal interpretation.** One counter-episode permanently demotes a
genuine ACTIVE delay rule in a context-stable environment. Three
honest re-demonstrations (support 2->3->4) cannot restore it because
R5 does not reset the creation context `dl_cs`, so the diversity check
can never pass when the cause always appears in the creation context.
Revision is one-way: revisable down, never up without context novelty.
The builder disclosed "no graded confidence" but not the one-way
ratchet. This narrows C1 ("bounds the harm class by making every
confirmation revisable"): the revisability is conditional on context
diversity the mechanism does not itself seek. Note the opened contests
(C0..C5, all resolved OLD-LAW-WINS) are diagnostic only; contest wins
are never consumed by the delay-rule logic, so they are not part of
this attack.

**Failures/boundaries of this attack.** It does not dispute that the
single refuter was genuine counter-evidence under the mechanism's
definition; it disputes that the revision is symmetric. A defender
could argue the environment should supply diverse contexts; the attack
shows the mechanism has no way to obtain or demand them, so in
context-stable environments degradation is permanent.

## X-CV5-2: masking games the refutation threshold

**Fixture:** cv5_adv_mask_obs.txt (16 episodes): obs3d.txt's 12 + seq13
`T 0 0 0 | 1 | 0 0 2` (a1 first episode; learns immediate law
s2:=SET(2)), seq14 `T 0 0 0 | 4 | 0 0 0` (a4 cause), seq15
`T 0 0 0 | 3 | 0 0 0` (a3 filler), seq16 `T 0 0 0 | 1 | 0 0 2`
(mask: a1 s2 0->2, consistent with its learned law; a4 at seq14).

**Result: SUCCEEDS (verdict DOWNGRADED).** Raw: CV5_ADV_MASK_RUN.txt,
md5 f34dc68476760cf4241251d894d76c0c, 3/3 byte-identical.

Exact trace (verbatim):

```
# PROVISIONAL-DELAY-RULE R0: cause a=4 d=2 -> s2 SET(1) support=1 (unconfirmed)
# delay-attributed var s2 of seq 7 to R0
# delay rule R0 CONFIRMED at seq 11 support=2 (provisional -> active)
# delay-attributed var s2 of seq 11 to R0
# opened contest C0 at seq 15
# delay rule R0 REFUTED at seq 16: cause a=4 at seq 14 not followed by s2=1 (observed 2); demoted to PROVISIONAL
# learned 16 episodes, 5 entries, 1 contests, 1 delay rules
# ENTRY 1 a=1 cond=[] st=1 fx=[UNCH,UNCH,SET(2)] par=-1 ne=2
# DELAY RULES
# DL R0 cause=4 d=2 var=s2 fx=SET(1) st=PROV support=1
=== PROBES ===
Q (0 0 0) | 1 -> (0 0 2)
```

Against the frozen criterion: `R0 REFUTED at seq 16` (PASS); ENTRY 1
a=1 fx=[UNCH,UNCH,SET(2)] (PASS); probe `Q (0 0 0) | 1 -> (0 0 2)`
(PASS).

**Causal interpretation.** The refuting observation (seq16) was fully
explained by the learner's own immediate law for a1 (learned at
seq13, reproduced in the probe), yet R5 demoted the genuine delay
rule. The refutation condition ignores the current action's own
learned law for v, so it cannot distinguish falsification from
masking: the ceteris-paribus delay claim ("a4 at s-2 causes s2:=1 when
nothing else intervenes") is not what was tested. This narrows C2
("principled belief-revision") and C3 ("one counter-episode suffices
because the rule is a universal claim"): the criterion fires on
masked observations, not only on genuine universal-claim violations.

**Failures/boundaries.** The attack does not show the refuter was
unreasonable under a strict reading of the universal claim; it shows
the universal-claim reading is itself too crude, because the mechanism
has no masking/consistency check against its own immediate laws.

## X-CV5-3: zero-marginal-cost re-arm (re-confirmation abuse)

**Fixture:** cv5_adv_rearm_obs.txt (11 episodes):
causalv4_adversary/cv4_adv_vary_obs.txt's 8 (frozen; SPURIOUS R0 =
(1,1,s2,2) CONFIRMED at seq 8, creation ctx (1,0,0)) + seq9
`T 0 0 0 | 1 | 0 0 0` (a1 no-op, new state) + seq10
`T 0 0 0 | 1 | 0 0 0` (refuter: a1 at seq9, ns(s2)=0 != 2) + seq11
`T 0 0 0 | 0 | 0 0 2` (re-arm: a0 s2 0->2, a1 at seq10).

**Result: SUCCEEDS (verdict DOWNGRADED).** Raw: CV5_ADV_REARM_RUN.txt,
md5 bd96c019254a3d485af1f2a07fdf183a, 3/3 byte-identical.

Exact trace (verbatim):

```
# PROVISIONAL-DELAY-RULE R0: cause a=1 d=1 -> s2 SET(2) support=1 (unconfirmed)
# delay-attributed var s2 of seq 4 to R0
# delay rule R0 CONFIRMED at seq 8 support=2 (provisional -> active)
# delay-attributed var s2 of seq 8 to R0
# delay rule R0 REFUTED at seq 10: cause a=1 at seq 9 not followed by s2=2 (observed 0); demoted to PROVISIONAL
# delay rule R0 CONFIRMED at seq 11 support=2 (provisional -> active)
# delay-attributed var s2 of seq 11 to R0
# learned 11 episodes, 5 entries, 0 contests, 1 delay rules
# DELAY RULES
# DL R0 cause=1 d=1 var=s2 fx=SET(2) st=ACT support=2
=== PROBES ===
Q (0 0 1) | 1 -> (0 0 2)
```

Against the frozen criterion: `CONFIRMED at seq 8` (PASS); `REFUTED
at seq 10` (PASS); `CONFIRMED at seq 11` (PASS); final st=ACT (PASS);
probe `Q (0 0 1) | 1 -> (0 0 2)` (PASS).

**Causal interpretation.** A persistent adversary re-arms the refuted
SPURIOUS rule with a SINGLE episode (seq11). Refutation resets support
to 1 and keeps dl_cs at the original creation context, so one support
in any fresh context re-confirms. R5 adds zero marginal cost to
re-attack. This narrows C1 to one-shot adversaries: the "harm class"
is bounded only if the adversary stops attacking after refutation.

**Failures/boundaries.** The builder disclosed that re-confirmation
uses the existing R4 path; what they did not consider is adversarial
re-arm of a spurious rule at unit cost. The attack does not dispute
that the mechanism behaved as designed; it disputes that the design
bounds the harm class against persistent adversaries.

## X-CV5-4: regression (no silent changes)

**Result: attack FAILS (defense holds).** Built-from-HEAD binary; all
`cmp` byte-identical:

- perm fixture -> CV5_PERM_RUN.txt: IDENTICAL
  (CV5_ADV_REGPERM_RUN.txt, md5 2f9466445079f24da5f1265ad7c8cd76)
- vary fixture -> CV5_VARY_RUN.txt: IDENTICAL
  (CV5_ADV_REGVARY_RUN.txt, md5 d32d0c76230278c094ba81953f0cbbd8)
- 3d -> CV4_3D_RUN.txt: IDENTICAL (md5 77b0fcb0bd24135b280433ce391aac43)
- double -> CV4_DOUBLE_RUN.txt: IDENTICAL (md5 ef64c15c62371489a783e3efbfda7529)
- double2 -> CV4_DOUBLE2_RUN.txt: IDENTICAL (md5 69496cc52890a42bfb35929499cc900e)
- diff committed causalv5.zag vs committed causalv4.zag: 42 lines,
  exactly the R5 change set (header comment, dl_retract_check, the
  learn_episode hook, associated comments). No undeclared changes.

## Verdict

**H-CAUSALV5 DOWNGRADED.** Per the frozen verdict rule (any of
X-CV5-1/2/3 succeeding), the hypothesis is downgraded, not killed:
the R5 refutation machinery functions as specified, X-CV4-3 stays
closed (K-CV5-1 reproduces byte-identically), and no regression was
found. What falls:

1. "Bounds the X-CV4-1 harm class by making every confirmation
   revisable" narrows to: revision is one-way in context-stable
   environments (X-CV5-1) and zero-cost reversible by a persistent
   adversary (X-CV5-3). The bound holds against one-shot adversaries
   with context-diverse environments only.
2. "General belief-revision, not pattern-matching the attack" narrows:
   the criterion fires on masked observations it cannot distinguish
   from falsification (X-CV5-2).

Classification remains bounded L2. Nothing here bears on L3.

## Governance disclosures

- Pure Zag throughout: fixtures, builds, runs, greps, hashes, cmp.
  No Python at any stage.
- Adversary prereg (f80720b3d) committed alone before any fixture,
  build, or run. Strict prereg-before-execution order observed.
- No frozen kill bar weakened or retroactively altered.
- Staged/committed only owned paths
  (docs/lab/research-lead/overnight-20260928/causalv5_adversary/).
  Concurrent workers' files untouched; no broad git add.
- No em dashes in loop documentation.
- Commits local only; no push.
- /tmp/cv5adv build artifacts excluded from the commit.
- Negative evidence preserved: X-CV5-4 failed (defense held); the
  contest subsystem was examined and found inert with respect to the
  delay-rule logic (contest wins are emitted but never consumed).

## Files committed (this report's commit)

- causalv5_adversary/PREREG_CV5_ADV.md (prereg, committed alone at
  f80720b3d; re-listed for lineage)
- causalv5_adversary/CV5_ADV_RESULT.md (this file)
- causalv5_adversary/cv5_adv_deg_obs.txt / cv5_adv_deg_probe.txt
- causalv5_adversary/cv5_adv_mask_obs.txt / cv5_adv_mask_probe.txt
- causalv5_adversary/cv5_adv_rearm_obs.txt / cv5_adv_rearm_probe.txt
- causalv5_adversary/CV5_ADV_DEG_RUN.txt (md5
  48e7892b8fa0135994619460af338f72)
- causalv5_adversary/CV5_ADV_MASK_RUN.txt (md5
  f34dc68476760cf4241251d894d76c0c)
- causalv5_adversary/CV5_ADV_REARM_RUN.txt (md5
  bd96c019254a3d485af1f2a07fdf183a)
- causalv5_adversary/CV5_ADV_REGPERM_RUN.txt (md5
  2f9466445079f24da5f1265ad7c8cd76)
- causalv5_adversary/CV5_ADV_REGVARY_RUN.txt (md5
  d32d0c76230278c094ba81953f0cbbd8)
- causalv5_adversary/CV5_ADV_REG3D_RUN.txt (md5
  77b0fcb0bd24135b280433ce391aac43)
- causalv5_adversary/CV5_ADV_REGDOUBLE_RUN.txt (md5
  ef64c15c62371489a783e3efbfda7529)
- causalv5_adversary/CV5_ADV_REGDOUBLE2_RUN.txt (md5
  69496cc52890a42bfb35929499cc900e)

All runs 3/3 byte-identical (cmp). Source built from git HEAD
causalv5.zag, md5 1fc56329a2d6da52104050e3e83406b4.

## Recommended follow-ups for the builder (not executed)

- Reset or re-derive dl_cs on refutation, or require post-refutation
  supports to exceed the pre-refutation support count, to close the
  X-CV5-1 ratchet.
- Check the current action's learned law for v before demoting, to
  close the X-CV5-2 masking hole.
- Require re-confirmation supports to be earned under adversarial
  pressure (or raise the post-refutation bar), to raise the X-CV5-3
  re-arm cost.
