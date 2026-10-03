# ADDENDUM to COMMITORDER_1421.md (recovery correction)

Written by the wave-20260930-1721pdt coordinator during recovery of the
INCOMPLETE wave-20260930-1421pdt. COMMITORDER_1421.md is a mid-wave draft
and is NOT edited (historical record preserved); this addendum corrects
it on the record.

## Correction 1: ORDER.txt files DO exist

COMMITORDER_1421.md's lane table states "ORDER.txt present: NO" for all
lanes. That was true when the gov worker wrote the draft, but the lane
dirs in the committed record (02fcab591) contain:
- ddes/ORDER.txt (creation order: NAMECHECK, DIAGNOSIS, PREREG_DDESREPAIR3,
  ORDER.txt, ddesr3.zag planned, build/run evidence planned, RESULT planned)
- trades/ORDER.txt (NAMECHECK, PREREG_TRADES, ORDER.txt, deep_trial.zag,
  deep_trial_bin, build_trades.log, RESULTS_TRADES.md planned)
- integration/ORDER.txt (NAMECHECK, PREREG_UEXEC, ORDER.txt, uexec.zag
  planned, RUN_UEXEC.txt planned, RESULT_UEXEC.md planned)

The file-creation order in every lane is prereg-before-implementation.
However, the COMMIT record does not preserve this separation: preregs and
implementations were committed together in the single recovery commit
02fcab591. Per the standing prereg commit-order rule (2026-09-23), what
matters is the commit record: a prereg whose first commit does not strictly
precede its implementation's first commit is UNVERIFIABLE ORDERING.

## Correction 2: ordering status per lane (commit record)

- ddes (R3): PREREG_DDESREPAIR3.md and ddesr3.zag share first commit
  02fcab591. UNVERIFIABLE ORDERING. Additionally the implementation was
  never built or run. Status: INCOMPLETE, re-queue with proper
  commit-order (prereg committed alone first).
- trades: PREREG_TRADES.md and deep_trial.zag share first commit
  02fcab591. UNVERIFIABLE ORDERING, even though the science is complete
  (3/3 byte-identical runs, K1/K2/K4/K5 verified, K3 wall-time recovered).
  Status: cannot be adopted this wave; re-freeze and re-run queued.
- integration: PREREG_UEXEC.md committed in 02fcab591; no implementation
  file exists. Ordering preserved for a future implementation commit as
  strict descendant. Status: prereg frozen, implementation pending.
- freeze_analysis: design document, not a mechanism implementation.
  No ordering constraint applies.
- gov docs: governance records, not mechanism implementations.

## Correction 3: false output claim in gov NAMECHECK.md

The gov worker's NAMECHECK.md lists DEBATE_MOTIONS_1421.md and
LOOPSTATE_DRAFT_1421.md as produced outputs. Neither file exists in the
gov lane or anywhere in the run dir (verified by the recovery
coordinator). The debate and the LOOP_STATE draft were NOT done. The
claim is false and is recorded here as a process incident: outputs must
not be claimed before they exist on disk. No verdicts were held for
1421pdt; the mandatory debate is being held by the recovering wave.

No em-dashes in this documentation.
