# H-REVISE7 RESULT

Date (UTC): 2026-09-29
Hypothesis: H-REVISE7 (second-order revision: revisions are hypotheses)
Parent: H-REVISE6 (SURVIVES 66/66; red team SURVIVES with confirmed residual)
Verdict: **H-REVISE7 SURVIVES** (98/98 checks, 3/3 deterministic)

## Commit lineage

- Prereg (frozen before implementation): `e78eec911`
  `docs/lab/research-lead/overnight-20260928/PREREG_REVISE7.md`
  (committed alone; no implementation existed at that commit)
- Implementation + raw evidence (this commit):
  `revise7.zag`, `REVISE7_RAW.txt`, `REVISE7_RAW_R2.txt`,
  `REVISE7_RAW_R3.txt`
- Result: this file, `REVISE7_RESULT.md`

## What was built (methodology)

`revise7.zag` is copied from `revise6.zag` with five repairs, all in pure Zag:

- R1: slot size 60 -> 64 bytes. Byte at so+60 holds revision STATUS:
  0=ROLLED_BACK (tombstone), 1=PROVISIONAL, 2=ACTIVE. Every appended
  revision enters as PROVISIONAL. `vs3_apply` and `vs3_firing_slot` skip
  status-0 slots. `vs3_dump` prints `st=RB/PROV/ACT`.
- R2: `diagnose_rollback_check(VS, inp, true_out)`. Caller contract: call only
  after `vs3_apply` mispredicted `true_out`. It finds the most-recent firing
  slot and runs the counterfactual skip-test: if the store WITHOUT that
  revision predicts the trusted label, the revision overrode a correct
  prediction. PROVISIONAL -> ROLLED_BACK (returns 1); ACTIVE -> PROVISIONAL
  (returns 2, demotion). Otherwise returns 0 and changes nothing.
- R3: `diagnose_confirm_check(VS, inp, true_out)`. Caller contract: call only
  after `vs3_apply` predicted correctly. If a PROVISIONAL revision fired and
  the P0 policy would have mispredicted, promote to ACTIVE (returns 1).
- R4: `vs3_revise` scans for a tombstoned slot with identical (cpos,cval)
  first and REACTIVATES it (status back to 1, program bytes overwritten)
  instead of appending a duplicate. vcount unchanged.
- R5: `diagnose_corroborate_v6` returns 0 with a clean WITHHOLD line on
  nn1<=0 (defense in depth against the red-team direct-call panic wart).

New main phases N1..N5 (32 named CHECKs) after the byte-preserved phases A..I.

Evidence method note: `znc --run` prints the compiler line
`znc: wrote native binary ...` to STDOUT, which would contaminate the raw.
The binary was therefore compiled once (`/tmp/revise7_bin`, not committed)
and executed directly three times; all three stdout captures are the raw
evidence files.

## Frozen kill bars and results

K-RV7-1 (X-RV5-1 replay with rollback bound): PASS 11/11.
  N1 propose==(0,122) PASS; N2 discover nn==3 (broadcast-first) PASS;
  N3 gate==1 on adversarial fail2 PASS (frozen expectation: detection is NOT
  claimed; the gate honestly appends); N4 revise rc==1 PASS;
  N5 status==PROVISIONAL PASS. On new labeled ("zbq"->"qqq") with VS
  mispredicting ("zzz"): N6 mispredict confirmed PASS; N7 rollback_check==1
  PASS; N8 status==ROLLED_BACK PASS; N9 exact restoration zbq->qqq PASS
  (vs3_apply returns "qqq", bit-identical to pre-revision behavior);
  N10 passing abc->ccc intact PASS; N11 P0 restoration zqy->yyy PASS (the
  honestly-labeled fail1 resurfaces as a genuine P0 failure, not silently
  absorbed).

K-RV7-2 (non-interference): PASS 4/4.
  Store: (0,120)->broadcast-first PROVISIONAL. ("yzb"->"yyy"): N12 VS
  mispredicts yzb->bbb (revision does not fire) PASS; N13 rollback_check==0
  PASS; N14 status stays PROVISIONAL PASS; N15 vcount==1 PASS.

K-RV7-3 (adversarial rollback is dual-use; re-admission bounds it): PASS 9/9.
  Forged ("xqw"->"www") (label crafted to equal P0 output): N16
  rollback_check==1 PASS; N17 status==ROLLED_BACK PASS. FROZEN DUAL-USE
  DISCLOSURE: the rule cannot distinguish this forged label from a genuine
  P0-consistent label, and the bar requires the honest behavior anyway.
  Genuine ("xqw"->"xxx"): N18 rollback_check==0 (nothing firing) PASS.
  Fresh pipeline: N19 re-propose==(0,120) PASS; N20 re-corroborate==1 PASS;
  N21 re-revise rc==1 PASS; N22 vcount==1 (REACTIVATE, no duplicate slot)
  PASS; N23 status==PROVISIONAL (reactivated) PASS; N24 re-admitted
  xqw->xxx PASS.

K-RV7-4 (promotion and graded contradiction): PASS 7/7.
  Confirming ("xqp"->"xxx") (VS correct via revision; P0 gives "ppp"):
  N25 VS correct PASS; N26 confirm_check==1 PASS; N27 status==ACTIVE PASS.
  Forged ("xqw"->"www"): N28 demote returns 2 PASS; N29 status==PROVISIONAL
  (demoted, not rolled back) PASS. Forged ("xab"->"bbb"): N30 second
  contradiction rollback==1 PASS; N31 status==ROLLED_BACK PASS.
  Bound demonstrated: 1 contradiction fells a provisional revision,
  2 fell a confirmed one.

K-RV7-5 (nn<=0 defense in depth): PASS.
  N32 nn<=0 withholds cleanly PASS, exercised in all 3 runs, no panic.

K-RV7-6 (regression): PASS.
  All 50 inherited named CHECK lines byte-identical between REVISE6_RAW.txt
  and REVISE7_RAW.txt (md5 bcbe69a4fe6f776e613011890d769b37 on the extracted
  CHECK lines, both files). Full raw diff contains ONLY the pre-declared
  categories: banner rename H-REVISE6->H-REVISE7; vs3_revise EVIDENCE lines
  (8: Phase C x1, Phase G x1, Phase H x1, Phase I x1, chained-revision phase
  x4); vs3_dump " st=PROV" fields; the new Phase N block; final verdict
  rename. Zero other differences. Total 98/98 in the RESULT line.

K-RV7-7 (determinism): PASS.
  3/3 runs byte-identical, cmp-verified and md5-verified
  (6b783965c82d1b5483808a36ed4f78e7 x3).

## Prereg inaccuracies (owned, do not change the verdict)

1. K-RV7-6 estimated "vs3_revise EVIDENCE lines (exactly 4, in Phases C, G,
   H, I)". The actual count is 8 (C:1, G:1, H:1, I:1, chained phase:4). All
   are the same pre-declared category (every vs3_revise call now emits one
   EVIDENCE line); the estimate missed the chained-revision phase's four
   appends. No undocumented raw difference exists.
2. The prereg said "66 existing named CHECK lines". The exact composition is
   50 named CHECK lines plus 16 unnamed counter increments (extract/discover
   successes in phases A/C/G/H/I), totaling 66. All 50 named lines are
   byte-identical; the grand total is 98/98 as frozen.

Both corrections are recorded here; no frozen bar was weakened and the
verdict stands on the corrected reading.

## What is still NOT solved (frozen boundaries)

- X-RV5-1/X-RV6-1 remains a CONFIRMED RESIDUAL: still undetectable at append
  time by any observation-only gate. H-REVISE7 bounds the aftermath; it does
  not remove the residual.
- Forged-label rollback is dual-use (K-RV7-3 disclosure): anyone holding the
  label channel can roll back any revision at will. The protocol weights
  evidence; it does not authenticate labels.
- Duplicate-append detection when propose re-derives an ACTIVE revision's
  (cpos,cval) is not implemented (known gap, still open).
- Adversarial confirmation-forgery (flooding confirming labels to promote a
  wrong revision) is not defended; promotion is evidence-weighting, not
  authentication.
- Tombstones still occupy capacity: 4 tombstoned slots refuse further
  appends with VS3FULL even though no live revision exists.

## Causal interpretation

The rollback is a genuine counterfactual, not a heuristic: vs3_apply_skip
answers "what would the store have predicted without this revision" by
running the identical dispatch with one slot ignored. Exact restoration
holds because rollback flips exactly one status byte and the apply path
skips status-0 slots, so every downstream firing decision is unchanged.
The graded bound (1 contradiction for provisional, 2 for confirmed) follows
from the evidence asymmetry frozen in the prereg: a revision enters on
minimum evidence, so one contradiction suffices; a confirmed revision has
survived a confirming trial, so it costs two. The re-admission result (N3)
shows the protocol is self-healing under honest labels: a wrongly rolled
back revision is re-derived by the unchanged diagnosis pipeline and
reactivated without duplicating state.

## Classification

Bounded L2+ revision with a self-correction protocol. NOT L3: no new
representation was invented (the provisional/active/rolled-back status
machine and the rollback/confirm rules were designed by the researcher, not
invented by the learner after experience). It is, however, a concrete step
toward the Level E correction/revision requirement at the meta level: the
learner now revises its own revisions instead of only its base policy.

## Governance disclosures

- Pure Zag throughout: implementation, fixtures, evidence, analysis, and all
  file edits. No Python anywhere in this work.
- Prereg committed alone at e78eec911 before any implementation existed.
- No em dashes in this documentation.
- Owned paths only: PREREG_REVISE7.md, revise7.zag, REVISE7_RAW*.txt,
  REVISE7_RESULT.md under docs/lab/research-lead/overnight-20260928/.
- The compiled test binary lived in /tmp and was not committed.
- No worker-count claims are made in this report.

## Next

H-REVISE7 requires an independent red team before it can be called
established: suggested attacks are forged-confirmation flooding, rapid
rollback/re-admit oscillation, multi-slot interference (rollback skip-test
with two firing revisions), duplicate-append of an ACTIVE revision, and
capacity interplay between tombstones and VS3FULL.
