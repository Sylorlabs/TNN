# EXP-1 working note: the C7 metric arithmetic (adversarial-audit finding)

Date: 2026-09-20. Status: derived from source; numeric confirmation pending
the instrumented re-run.

## Code reality (verified in src0, and at baseline 5aa2fb13)

`met.hypotheses` is incremented at THREE sites (loop.zag):
- :82  `loop_claim_open` — proactive section-2 opens
- :161  refusal→abstain branch — FORCED opens
- :177  elected abstain branch — ELECTED opens

`tr.l1_opened` is incremented at ONE site (seam.zag:409, inside
`seam4_abstain` when the open succeeds): forced_ok + elected_ok.

Therefore:
- met.hypotheses  = proactive_ok + forced_ok + elected_ok
- tr.l1_opened    = forced_ok + elected_ok
- cap_old         = cok + ccon + met.hypotheses + tr.l1_opened
                  = cok + ccon + proactive_ok + 2*(forced_ok + elected_ok)

The code comment at `loop_capability` (loop.zag:466-473) says
"proactive O2 hypotheses (met.hypotheses) + L1 abstain-hypotheses
(tr.l1_opened)". That comment is STALE/WRONG: met.hypotheses includes all
L1 opens (true since the repair commit 5aa2fb13, verified in the baseline
blob). L1 opens are double-counted in cap_old; proactive opens single.

## Consequence for the DRAFT amendment

DRAFT §3 states the formula:
  cap = composites_ok + commits_constr + hypotheses_autonomy,
  hypotheses_autonomy = proactive O2 hypotheses + elected L1 abstain-hypotheses.

Taken literally with the code's counters, for redesigned DC-4
(cok=256, ccon=2, proactive_ok=622, elected_ok=0):
  cap = 256 + 2 + 622 + 0 = 880.

But DRAFT §3's "Expected re-score" says DC-4 = 914 − 17 = 897.
880 != 897. The draft's formula and its expected re-score are INCONSISTENT.

Root cause: the draft (like the rescore doc §1, like the code comment)
assumes met.hypotheses is proactive-only. It is not.

## Which number is correct for C7's purpose?

C7 asks: did teacher withdrawal collapse capability (DC-5 vs DC-4)? The C5
gate's forced hypotheses are a curriculum artifact (present in DC-4, absent
in DC-5), not a teacher effect. The correction must remove the artifact to
recover the fair comparison.

The artifact's measured size: cap_old(DC-4) − cap_old_baseline(DC-4)
= 914 − 897 = 17, entirely in tr.l1_opened (met.hypotheses is flat at 639
in both runs — the o2_cap=640 cid budget saturated, so the 17 forced
displaced 17 proactive 1:1; verified structurally, numeric re-confirmation
pending).

Removing the artifact: cap_new = cap_old − forced = 897. This recovers the
counterfactual DC-4 (what DC-4 scores without the gate artifact) and gives
897 → 897 → C7 ALIVE.

The literal formula (880) instead measures actual autonomous inquiry in the
confounded run. It additionally penalizes DC-4 for the 17 displaced
proactive hypotheses — a real consequence of the mandated mechanism, but
NOT a teacher effect, so it is the wrong correction for C7's question
(it answers "how autonomous was DC-4?" not "did the teacher matter?").

Both readings give C7 ALIVE (880→897: cap5 > cap4, no collapse; the in-code
bar fires iff cap5 < cap4). The operational re-score (897→897) is the
correct adoption target.

## Recommended adopted definition (fixes the defect, keeps the numbers)

  cap_new = composites_ok + commits_constr + met.hypotheses
            + (tr.l1_opened − forced)

i.e. cap_old with the forced hypotheses subtracted from the L1 term.
forced = number of complete ledger chains
  refusal(rc=311, b2=0) → abstain(rc=0, orc=0) → hyp_open(rc=0),
linked by (episode, need_id) then (episode, cid).

Scope condition (verified for this S10): the subtraction is exact because
o2_cap saturated in every stage (met.hypotheses = 639 = o2_cap − 1), so
forced hypotheses displaced proactive ones 1:1 and met.hypotheses carries
zero NET forced content vs the counterfactual. Without saturation the
arithmetic is not exact (a forced abstain would add +2 to cap_old); the
checker must assert mhyp == o2_cap − 1 per stage.

Also fix: the "met.hypotheses = proactive-only" language everywhere
(draft §3, rescore §1, and the stale code comment at loop_capability —
the comment is not a behavioral bar so correcting it is documentation,
but flag it as such).
