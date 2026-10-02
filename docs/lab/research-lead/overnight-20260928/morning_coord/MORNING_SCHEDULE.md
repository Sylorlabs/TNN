# Morning Schedule: 2026-10-01 (PDT)

**Prepared:** ~00:05 PDT (07:05 UTC), 2026-10-01.
**Status:** The freeze evaluator is alive and mid-run (FW run 3 on FW9b at last check). Reconciled report expected ~09:00 UTC central (01:40-02:50 PDT window). Bundle v16 stays gated on that report.

## 1. What Micah can do while waiting (no dependencies)

**Read, in priority order** (`reading_guide/READING_GUIDE.md`):

- 10 minutes: `session_summary/SESSION_SUMMARY.md`, then `gw_eval/GW_EVAL_REPORT.md` (2/8 WORLD-PASS), then `protected_core_decision/PROTECTED_CORE_BRIEF.md` (Alt C recommended, NOT DECIDED).
- 30 more minutes: red-team synthesis, degree-of-freedom map (0 pure learner decisions), prereg compliance audit (5/9 draft error corrected to 4/9), re-clustering draft, TNN-3 roadmap.
- 1 more hour: the three detailed red-team reports, C0-D structural analysis, H2 probe design, kill-bar draft plus review, morning report.

**Review the 4 banked decisions** (`morning_checklist/MORNING_CHECKLIST.md`):

1. Protected-core structural ops: Alt C recommended (H3-lite only, defer the structural question); asked to approve the H3-lite prereg path, keep the structural question banked, and reject Alt A (permanent prohibition).
2. Six kill-bar open questions (draft `76231baa8`, review `eb354e3a2` with recommendations); 24 bars total on record (`1722884ad`), all DRAFT-NOT-FROZEN.
3. K-H3 DRAFT-NOT-FROZEN needs a separate review.
4. Full TNN-3 preregistration, pending decisions 1-3; roadmap order is fixed (H2 probes, then H3-lite, then repair/inquiry, H1 only after H2).

**Review H2 readiness** (`h2_readiness/H2_READINESS.md`): probe design (`4631c5918`) and three sealed trap worlds (`86389b108`, H2A/H2B/H2C, NOT run) are ready. Two decisions needed from Micah: freeze K-H2-1..K-H2-4 in a preregistration (currently DRAFT-NOT-FROZEN), then authorize the evaluator.

**Skim for context:** `final_tally/FINAL_TALLY.md` (21 workers, 70 commits, 159 ledger claims, zero SURVIVES, L3 zero).

## 2. What happens when the reconciled freeze report lands

The evaluator must commit `core_freeze_tnn2_eval/` with a report that satisfies all six reconciliation steps from the prereg compliance audit (`8959a7c14`):

1. 5/9 corrected to 4/9 (the draft's arithmetic error; do not quote or ledger 5/9 anywhere).
2. K-FZ2-4 determinism resolved (3/3 byte-identical runs per world).
3. W1-W9 battery complete.
4. Per-cluster analysis against the five TNN-1 failure clusters.
5. Post-run hashes re-verified under K-FZ2-2.
6. Re-clustering incorporated; verdict no longer the premature FREEZE-EVAL-COMPLETE.

Any report that still claims 5/9 while listing four passes, leaves determinism pending, omits W1-W9, omits post-run hashes, or omits re-clustering must be rejected and sent back.

On acceptance, in order:

1. Independently verify the report (spot-check scores, hashes, determinism artifacts).
2. Ledger C160: record the verified freeze score in the canonical ledger (currently 159 claims; C160 is reserved for this).
3. Confirm `tnn2_transfer/` landed (boundary `8d763d766` and `h2_trapworlds` `86389b108` are already committed).
4. Bundle v16 per the 13-item checklist (`bundle_v16_prep/BUNDLE_V16_INVENTORY.md`, commit `801dc071d`): re-verify frozen hashes (`tnn2.zag`, `tnn2_bin`), seal spot-check, confirm the paper untouched, `git bundle create`, verify, record SHA-256 and size. Do NOT push.

## 3. Schedule (all times PDT)

| Window | Activity |
|---|---|
| 00:00-01:40 PDT | Reading window: 10-minute guide, then the 4 banked decisions, then H2 readiness. Evaluator still running; do not disturb. |
| 01:40-02:50 PDT | Freeze report expected window (central ~02:00 PDT / 09:00 UTC). If it lands early, start independent verification immediately. If it runs past 02:50, the risk is pace, not rework (machinery verified sound). |
| On report arrival | Verification against the six steps above. Estimated 20-40 min. |
| After verification passes | Ledger C160, then bundle v16 creation per checklist. Estimated 30-60 min including clone-check. |
| After bundle logged | Unblocked: H2 bar freeze decision, evaluator authorization, and the protected-core/K-H3/TNN-3 preregistration decisions are all in Micah's hands. |

## 4. Standing cautions

- Do NOT quote the draft 5/9 score; the audit-corrected figure is 4/9, and the reconciled report has not landed.
- Do NOT run the H2 trap worlds; they await Micah's freeze of K-H2-1..K-H2-4 and evaluator authorization.
- Do NOT push anything; commits stay local on `tnn-native-lab`.
- The evaluator is not stuck; it is actively executing. Check mtime evidence, never its internals, and never edit its draft.
