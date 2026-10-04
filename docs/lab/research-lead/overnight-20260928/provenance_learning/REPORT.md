# Provenance Policy Learning: Report

**Verdict: PROVENANCE-LEARNING-COMPLETE.**

**Date:** 2026-10-01
**Worker:** Provenance Policy Learning Worker (Micah Priority 4)
**Prior:** `9e9a2e372` (PROVENANCE-TREATMENT-COMPLETE; RESEARCHER-OWNED 9, LEARNER-OWNED 0)

## Summary

TNN learns source reliability from experienced consequences and uses the
learned ranking to resolve disagreements. No hardcoded source rank exists
in the treatment arm. When teacher B degrades, the learner demotes B from
experience; when B recovers and A degrades, the learner switches allegiance
to B. A hardcoded-rank control cannot switch and answers 4/4 probes wrong
in the final phase.

## 1. Method

### 1.1 Design

Two external teachers (source tags 7=SRC_A, 8=SRC_B in field 16, extending
the provenance treatment). Each round: both teachers claim a value for
(1,50), the learner predicts via `src_query` BEFORE the outcome is known,
then `ev_observe_src` reveals the world outcome and scores BOTH teachers'
latest claims (the learner heard both, so both reliabilities update).

Reliability store: tag-61 records (storage infrastructure only), one per
source: correct claims / total claims. Disagreement rule: prefer the higher
correct/total ratio (integer cross-multiplication, no floats). Exact ties
and no-data cases fall back to fact recency, which is source-neutral.

Treatment (`rank_fixed()=0`): ranking emerges from experienced accuracy.
Control (`rank_fixed()=1`, one-line sed diff, verified): hardcoded "A
always wins disagreements". Same scoring, same phases.

### 1.2 Phases

- P1 (6 rounds): A=42, B=42, outcome 42. Both reliabilities climb.
- P2 (6 rounds): A=42, B=99 (B degrades), outcome 42.
- P3 (4 probes): disagreement only, no outcome, no scoring. Pure preference.
- P4 (7 rounds): A=99 (A degrades), B=42 (B recovers), outcome 42.
- P5 (4 probes): disagreement only. Pure preference.

3/3 byte-identical per arm. Pure Zag, safebin, pinned znc.

## 2. Results

### 2.1 Treatment: reliability trajectories (learner-owned values)

| Phase | relA | relB | Behavior |
|-------|------|------|----------|
| P1 end | 6/6 | 6/6 | agreement, both credited |
| P2 k=1 | 7/7 | 6/7 | first disagreement: exact tie, neutral recency tiebreak picks B (wrong, honest) |
| P2 end | 12/12 | 6/12 | A preferred 5/5 after the tiebreak loss |
| P3 | - | - | 4/4 probes prefer A (1.0 > 0.5), all correct |
| P4 k=1..6 | 12/13 .. 12/18 | 7/13 .. 12/18 | keeps picking A (wrong) while A still outranks B; each wrong pick demotes A |
| P4 k=7 | 12/19 | 13/19 | tie broken by recency, picks B (correct); B now strictly ahead |
| P5 | - | - | 4/4 probes prefer B (13/19 > 12/19), all correct |

The switch from A to B at P4 k=7 is the key event: no researcher changed
any rank. Six consecutive wrong consequences demoted A from 12/12 to
12/18 while B's correct claims accumulated to 12/18, and the learner
followed the evidence.

### 2.2 Control: hardcoded rank cannot switch

Identical reliability records (A=12/19, B=13/19 at P4 end; the control
tracks the same evidence) but the choice is overridden to A always:

- P3: 4/4 prefer A (correct only because A happens to be right).
- P4: 7/7 picks A=99, all wrong, while B=13/19 sits in the records unused.
- P5: 4/4 probes pick A=99, all wrong. preferB=0.

The control demonstrates the cost of a permanent rank: the evidence for
switching is present in learner state, but the fixed policy cannot use it.

### 2.3 Answers to the mission questions

1. Confidence in A stays high while A is correct (12/12); drops after
   degradation (12/19). Yes, tracked per source from consequences.
2. On A/B disagreement the learner prefers the higher-reliability source:
   4/4 for A in P3, 4/4 for B in P5. The ranking is experienced, not coded.
3. Recovery is revisable: B recovers from 6/12 to 13/19 and wins the
   ranking back. Nothing is permanent.
4. No hardcoded OBSERVED > INFERRED or A > B rank exists in the treatment
   arm. The only source-neutral tiebreak is fact recency.

## 3. Honest accounting (Micah's standing question)

- RESEARCHER-OWNED: the reliability record layout, the count-correct/total
  update rule, the disagreement rule "prefer higher reliability", the
  recency tiebreak, the prediction-before-outcome protocol, the phase
  design, the teacher schedules.
- LEARNER-OWNED: the reliability VALUES (6/6, 12/12, 6/12, 12/19, 13/19),
  which source wins each disagreement, the switch point (P4 k=7), the
  recovery of B's standing. No per-case success rules; no source identity
  appears in any decision except as a record key.
- The update rule is bookkeeping; the RANKING is learned. This moves the
  provenance result from 9/0 toward learner-owned policy, but the
  disagreement rule itself is still researcher-set. Full learner ownership
  would require the learner to invent the reliability concept; that is
  future work.

## 4. Limitations and attacks

- The learner is scored on both teachers' claims each round ("hears both").
  A stricter bandit variant (score only the chosen source) would switch
  more slowly; not run.
- The switch required 6 wrong rounds because A started at 12/12. Strong
  priors are slow to overturn; this is honest Bayesian-like behavior, but
  the rate is set by the counting rule, not learned.
- Only two sources, one relation, one value pair (42/99). No test of
  graded reliability (e.g., 70% vs 90% teachers) or of reliability
  transferring across relations.
- Compiler fault: the first control build miscompiled the skipped-else
  form (pred=-2 on all disagreements). Worked around by running identical
  ranking code in both arms with a post-hoc override; treatment output
  byte-identical before/after, confirming the workaround preserves
  behavior. Filed in NAMECHECK.md.

## 5. Artifacts

`docs/lab/research-lead/overnight-20260928/provenance_learning/`:
`pl_nomain.zag` (frozen base minus main), `pl_patch.zag` (machinery),
`pl_patch_ctl.zag` (one-line control), `pl_driver.zag`, `build.sh`,
`pl_full_trt.zag`, `pl_full_ctl.zag`, `pl_trt_bin`, `pl_ctl_bin`,
`pl_trt_run{1,2,3}.txt`, `pl_ctl_run{1,2,3}.txt`, NAMECHECK.md, REPORT.md.
