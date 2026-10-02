# H-CAUSALV6 Red Team Report (CV6-ADV)

**Date:** 2026-09-29 (PDT)
**Status:** COMPLETE (attacks executed, 3/3 deterministic)
**Researcher:** H-CAUSALV6 Red Team (subagent)
**Branch:** tnn-native-lab
**Target:** H-CAUSALV6 SURVIVES (commit 807d13042), R6 repair
**Assumption:** the H-CAUSALV6 claim is false. All attacks below tried to
kill or downgrade it.
**Prereg:** `PREREG_CV6_ADV.md` (frozen at 1e6bf7f80, before any attack
fixture was built or run).

## Verdicts

| Attack | Target | Result |
|--------|--------|--------|
| X-CV6-1 | R6b support-bar vs R4 diversity | DOWNGRADE |
| X-CV6-2 | R6c delayed-law intervener | DOWNGRADE |
| X-CV6-3 | Multi-refutation floor escalation | DOWNGRADE |
| X-CV6-4 | Regression (all builder bars) | HOLD |

Three of four attacks downgrade H-CAUSALV6. The regression claim stands.

## Method

- Attacker used ONLY the committed `causalv6.zag` blob from 807d13042
  (md5 7d579163a5299c2054e2080df3c3d198, verified byte-identical to the
  working tree file). No mechanism edits.
- Binary compiled from the committed blob with
  `/home/hatch/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc`
  (znc 2026.07.0-dev, edition 2026). Pure Zag. No Python at any stage.
- Attack fixtures are plain `T` observation files + probe files.
- Every attack run 3/3; determinism checked by cmp. All 3/3 byte-identical.
- /tmp was wiped by a VM restart mid-task; all fixtures were rebuilt from
  preserved designs and re-verified before this report. No results changed.

## X-CV6-1: R6b drops the R4 diversity guard (DOWNGRADE)

**Theory.** R6b replaces the R4 cause-context diversity check with a pure
support bar (`support > dl_rf`) for re-confirmation of refuted rules. A
refuted rule re-confirms by repetition alone, with zero context novelty.
A fresh rule with the same identical-context evidence shape is blocked by
R4 forever. This is a strict weakening of the positioned-confounder guard
on the re-confirmation path.

**Design.** The prereg specified Phase 0 (create + R4 confirm), Phase 1
(refute), Phase 2 (identical-context re-demonstrations), plus a fresh-rule
control. During analysis, the red team recognized that the builder's own
committed `cv6_trunc21` fixture (K-CV6-1c) already implements Phase 0/1/2
exactly. The attack therefore uses the builder's committed evidence for
the re-confirmation half, plus a custom control fixture for the R4-block
half. This is disclosed, not hidden: using the builder's own trace makes
the downgrade stronger, not weaker.

**Phase 0/1/2 (builder's cv6_trunc21_obs.txt, 21 episodes, committed).**
R0=(a4,d=2,s2:=1). Created from seq 7 (support=1).
dl_cs (creation cause context) = state at seq 5 = (0,0,0).
CONFIRMED at seq 11 (support=2) via R4: cause context at seq 9 = (2,0,0),
diverse from (0,0,0). R0 ACTIVE.
REFUTED at seq 15: cause a=4 at seq 13 not followed by s2=1 (observed 0).
dl_rf=2, support reset to 1, PROVISIONAL.
Support at seq 18 (support=2): cause context = state at seq 16 = (0,0,0)
== dl_cs. IDENTICAL. R6b: 2 > 2 false. NOT RE-CONFIRMED.
Support at seq 21 (support=3): cause context = state at seq 19 = (0,0,0)
== dl_cs. IDENTICAL. R6b: 3 > 2 true. CONFIRMED. R0 ACTIVE, support=3.

The re-confirming supports (seq 18, seq 21) both carry cause context
(0,0,0), exactly equal to the creation context. Under R4 (the fresh-rule
path), a support with identical cause context can NEVER confirm, no matter
how many repetitions. Under R6b, it confirmed at support=3.

**Control (xcv61_ctrl_obs.txt, 10 episodes, custom).**
Fresh rule R0=(a1,d=1,s2:=1), created seq 4, dl_cs=(0,0,0).
Support seq 7 (support=2): `# delay rule R0 NOT CONFIRMED at seq 7:
cause context identical to creation; remains PROVISIONAL`.
Support seq 10 (support=3): `# delay rule R0 NOT CONFIRMED at seq 10:
cause context identical to creation; remains PROVISIONAL`.
Final: `DL R0 cause=1 d=1 var=s2 fx=SET(1) st=PROV support=3`.
Three identical-context supports; R4 blocks every one. The rule never
activates.

**Verdict: DOWNGRADE.** The frozen criterion is met: R0 re-confirms and
ends ACTIVE (st=ACT, support=3) using only identical-context supports
after refutation, while the fresh-rule control shows R4 blocking the same
identical-context shape as PROVISIONAL. R6b strictly weakens the R4
positioned-confounder guard on re-confirmation. A confounder that was
refuted once can re-establish itself by pure repetition in the exact
original context, which the pre-R6 mechanism forbade.

**Raw:** `XCV61_CTRL_RUN.txt` (md5 d5e3db8f99e290db8361a408ff35eb83).
Builder Phase 0/1/2 raw: committed `CV6_TRUNC21_RUN.txt` (reproduced
byte-identical in X-CV6-4).

## X-CV6-2: Delayed-law intervener falsely refutes (DOWNGRADE)

**Theory.** R6c (`dl_masked`) withholds refutation only when the CURRENT
episode action's learned ACTIVE immediate law predicts the observation. It
scans ST_ACT immediate entries for the current action. A delayed law of
another action that fully explains the observation does not mask. The
X-CV5-2 failure class (falsification vs masking) recurs for delayed
interveners. (The disclosed ST_AMB non-masking boundary was verified by
code inspection: `dl_masked` requires `en_st==ST_ACT`. No fixture spent.)

**Fixture (xcv62_obs.txt, 19 episodes, custom).**
Phase A (seq 1-9): R0=(a4,d=2,s2:=1) established ACTIVE (support=2) via
the x2p1b pattern (creation seq 6, R4 confirmation seq 9 with diverse
cause context (0,0,1)).
Phase B (seq 10-16): R1=(a2,d=1,s2:=2) established ACTIVE (support=2).
Creation seq 13 (contradiction s2 1->2 under a=3, preceded by a=2,
dl_cs=(0,0,1)). R4 confirmation seq 16 (diverse cause context (0,0,0)).
Building R1 required firming the (0,0,1) UNCH pattern first (seq 10-11);
otherwise the a=3 entry splits instead of contradicting.
Phase C trap (seq 17-19):
`T 0 0 2 | 4 | 0 0 2` (a4 at t),
`T 0 0 2 | 2 | 0 0 2` (a2 at t+1),
`T 0 0 2 | 1 | 0 0 2` (a1 at t+2, observed s2=2).
At seq 19: R0's check sees cause a=4 at seq 17, expects s2=1, observes 2.
R1 (ACTIVE) fully explains s2=2 via its own learned delayed law
(a2 at seq 18, d=1). a1's immediate law is UNCH (passive); `dl_masked`
requires SET/ADD, so no masking.

**Result.**
`# delay rule R0 REFUTED at seq 19: cause a=4 at seq 17 not followed by
s2=1 (observed 2); demoted to PROVISIONAL`
Final dump:
`# DL R0 cause=4 d=2 var=s2 fx=SET(1) st=PROV support=1`
`# DL R1 cause=2 d=1 var=s2 fx=SET(2) st=ACT support=2`
R0 (victim) refuted. R1 (intervener) still ACTIVE. The observation is
fully explained by the learner's own delayed law, but refutation was not
withheld because R6c only checks immediate laws of the current action.

**Verdict: DOWNGRADE.** The frozen criterion is met: R1/victim is REFUTED
at the trap while R2/intervener is ACTIVE in the final dump. C-R6c is
narrowed to immediate-law interveners only. A delayed intervener that the
learner itself has confirmed does not protect a victim rule from false
refutation. (Prereg named victim R1 and intervener R2; creation order in
the fixture made them R0 and R1. Roles are as specified.)

**Raw:** `XCV62_RUN.txt` (md5 b5d542503b84e60d137bcd0cdaac5071).

## X-CV6-3: Persistent-adversary floor escalation (DOWNGRADE)

**Theory.** R6a sets `dl_rf` to the pre-refutation support on EVERY
refutation; R6b clears it only on promotion. A persistent adversary
injecting one counter-episode per cycle refutes at the current peak
support, so the floor ratchets up each cycle while the adversary's
per-cycle cost stays at 1. Honest recovery cost grows without bound.
The X-CV5-1 one-way ratchet is closed for one-shot adversaries only.

**Fixture (xcv63_obs.txt, 77 episodes, custom).**
R0=(a4,d=2,s2:=1), established ACTIVE (support=2) via x2p1b (seq 1-9).
Each cycle: adversary block (reset a=0, cause a=4, filler a=1, observation
a=2 with s2=0) refutes in ONE counter-episode (the observation; reset/
cause/filler are setup). The observation uses a=2 (not the a=3 effect
action) so it does not poison `delay_clean` for future a=3 supports.
Honest recovery: repeated (cause a=4, filler a=1, effect a=3 s2->1) with
a=0 resets, until support > dl_rf.

**Cycle table.**

| Cycle | Refuted at | dl_rf (floor) | Recovery supports | Re-confirmed at | Support | PROV episodes |
|-------|-----------|---------------|-------------------|-----------------|---------|---------------|
| 1 | seq 13 | 2 | 2 (seq 16, 20) | seq 20 | 3 | 7 (13-19) |
| 2 | seq 24 | 3 | 3 (seq 27, 31, 35) | seq 35 | 4 | 11 (24-34) |
| 3 | seq 39 | 4 | 4 (seq 42, 46, 50, 54) | seq 54 | 5 | 15 (39-53) |
| 4 | seq 58 | 5 | 5 (seq 61, 65, 69, 73, 77) | seq 77 | 6 | 19 (58-76) |

Floors escalate 2->3->4->5. Honest recovery costs grow 2, 3, 4, 5
support episodes (prereg listed "2, 3, 4"; the 4th cycle costs 5,
continuing the pattern). Adversary pays exactly 1 counter-episode per
refutation (seq 13, 24, 39, 58). R0's PROVISIONAL/inert duration grows
7, 11, 15, 19 episodes. Final: R0 ACTIVE, support=6.

**Verdict: DOWNGRADE.** The frozen criterion is met: floors escalate
2->3->4->5 across 4 cycles, honest re-confirmation costs grow, adversary
pays 1 counter-episode per cycle, and R0 spends a growing duration
PROVISIONAL/inert. C-R6b is narrowed: the X-CV5-1 ratchet is closed for
one-shot adversaries only; a persistent 1-episode-per-cycle adversary
wins the cost race without bound. Each refutation makes the NEXT
recovery strictly more expensive, while the adversary's cost is constant.

**Raw:** `XCV63_RUN.txt` (md5 d7610cf8fdce9e02600ff0f6b7ae9db4).

## X-CV6-4: Regression (HOLD)

**Rebuild.** Binary compiled from the committed 807d13042 blob
(md5 7d579163a5299c2054e2080df3c3d198, re-verified after /tmp wipe).
All runs below use this binary.

**Attack bars (3/3, cmp against committed raws).**
- K-CV6-1c (cv6_trunc21_obs/probe vs CV6_TRUNC21_RUN.txt): IDENTICAL.
- K-CV6-2 (cv5_adv_mask_obs/probe vs CV6_MASK_RUN.txt): IDENTICAL.
  (Committed raw is named CV6_MASK_RUN.txt; the result doc records its
  md5 as d3ef918e9ea1c418f86259c0bf90c890, matching this rerun.)
- K-CV6-3 (cv5_adv_rearm_obs/probe vs CV6_REARM_RUN.txt): IDENTICAL.

**12 regressions (each 3/3 byte-identical, cmp against committed
CV6_REG_*.txt).** Fixture map recovered from committed preregs:
double, thr (causalv2_adversary/cv2_adv_*), mask
(causalv_adversary/cv_adv_mask_obs + cv_adv_harm_probe), 3i2
(causalv2_repair/obs3i2+probe3i2), 3c/3d/3i (causal3/obs+probe),
B2/C2 (causal/obs+probe), double2
(causalv3_adversary/cv3_adv_double2_*), perm/vary
(causalv4_adversary/cv4_adv_perm/vary_*). Result: 12/12 IDENTICAL,
0 nondeterministic.

**v5->v6 diff audit.** `diff` of committed causalv5.zag vs committed
causalv6.zag (both from 807d13042) yields exactly 10 hunks, all R6:
(1) header comment, (2) R6 doc comment, (3) O_DL_RF offset + shifted
workspace offsets (mechanical), (4) dl_rf accessor, (5) R6b
re-confirmation branch in dl_add_or_support, (6) its closing brace,
(7) dl_rf init on rule creation, (8) dl_masked function (R6c),
(9) dl_retract_check comment, (10) masking branch + dl_rf recording on
refutation. No changes to learn_episode, delay_clean, attribution,
entry machinery, or any other mechanism. No silent changes.

**Verdict: HOLD.** The regression claim stands: 15/15 outputs
byte-identical, 3/3 deterministic, diff contains only the R6 change set.

## Causal interpretation

R6a (floor) is sound as a one-shot defense: it forces re-confirmation to
exceed the refuted support, closing the X-CV5-1 free re-arm. But R6a+R6b
compose into a ratchet under a persistent adversary (X-CV6-3): every
refutation raises the floor to the current peak, so honest recovery cost
grows linearly while adversary cost stays constant. This is not a bug in
R6a alone; it is the predictable composition of "floor = peak support"
with "adversary chooses when to refute."

R6b (graded re-confirmation) is the weakest link. It discards the R4
diversity evidence entirely on the re-confirmation path, replacing a
qualitative guard (context novelty) with a quantitative one (repetition
count). X-CV6-1 shows the guard was load-bearing: the exact evidence
shape R4 was built to block (positioned confounder, identical context)
re-confirms under R6b. A sound R6b would require BOTH support > dl_rf AND
the R4 diversity check, not one or the other.

R6c (masking) is scoped too narrowly. It checks only the current action's
immediate laws, ignoring the learner's own delayed laws (X-CV6-2) and
ambiguous laws (disclosed ST_AMB boundary). The ceteris-paribus clause in
the delay rule's meaning ("when nothing else intervenes") is operationally
checked against immediate interveners only.

## Governance disclosures

1. The assignment prompt stated "H-CAUSALV6 SURVIVES (K-CV6-1c/2/3/4)" and
   "All bars pass." The builder report records K-CV6-1: FAIL, K-CV6-1b:
   FAIL, K-CV6-1c: PASS, K-CV6-2/3/4: PASS. The "all bars pass" phrasing
   is corrected here; sequential amendments (745b831b1, e6cbd2a3c,
   51cf2b3d2) require governance adjudication (already flagged by parent).
2. Before this prereg was frozen, the red team reproduced the committed
   K-CV6-1c run from the committed source (byte-identical, md5
   35433be9e9ac3d2271e1519e6db2fc3c). This was reproduction of committed
   builder evidence, not an attack; no attack fixture existed before the
   prereg commit (1e6bf7f80).
3. X-CV6-1's attack half reuses the builder's committed trunc21 fixture
   rather than a custom-built Phase 0/1/2. The fixture implements the
   prereg's design exactly; the red team recognized this during analysis.
   The control half is custom-built.
4. X-CV6-3's prereg listed recovery costs as "2, 3, 4"; observed costs
   are 2, 3, 4, 5 (the 4th cycle continues the linear pattern).
5. Pure Zag throughout. No Python at any stage (fixtures via shell
   heredocs, analysis via grep/cmp/md5). /tmp wipe forced a rebuild;
   all results re-verified.
6. No em dashes in this documentation (byte-verified before commit).
7. These are subagent findings, not canonical; they require independent
   verification before being treated as canonical.

## Commit lineage

- 745b831b1: PREREG_CAUSALV6 (original)
- e6cbd2a3c: PREREG_CAUSALV6_AMENDMENT (K-CV6-1b)
- 51cf2b3d2: PREREG_CAUSALV6_AMENDMENT2 (K-CV6-1c)
- 807d13042: H-CAUSALV6 implementation + evidence + result
- 1e6bf7f80: CV6-ADV prereg (this red team, frozen before attacks)
- (this commit): CV6-ADV fixtures + raw evidence + report

## Files (docs/lab/research-lead/overnight-20260928/cv6_adversary/)

- PREREG_CV6_ADV.md (frozen prereg)
- CV6_ADV_REPORT.md (this report)
- xcv61_ctrl_obs.txt, xcv61_ctrl_probe.txt, XCV61_CTRL_RUN.txt
- xcv62_obs.txt, xcv62_probe.txt, XCV62_RUN.txt
- xcv63_obs.txt, xcv63_probe.txt, XCV63_RUN.txt
