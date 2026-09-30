# OpScope 11-Step Pipeline: Status

Date: 2026-09-30. Worker: OpScope Pipeline Initiator.
Parent verdict ingested: OPSCOPE-REBUILD-PASS (837c02c59), F1-F5 all pass,
prereg 1fd2f0752 strictly precedes implementation (ancestry-verified).

## The 11 steps (frozen frontier promotion pipeline)

Only after all 11 may a frontier mechanism become SURVIVES.
Builders report BUILD-PASS/BUILD-FAIL only.

| # | Step | OpScope status |
|---|------|----------------|
| 1 | Committed preregistration | SATISFIED. 1fd2f0752, ancestry-verified before any implementation file existed. |
| 2 | Implementation | SATISFIED. 837c02c59. One-line K=2 change, frozen battery byte-identical, 3/3 deterministic (md5 767f289ef5732dde430c9f625c9b44a6), pure Zag. F1-F5 all PASS. |
| 3 | Sealed evaluation | NOT DONE. Initiated by this document set. Prereg frozen in SEALED_EVAL_PREREG.md. Awaits independent sealer. |
| 4 | Independent reproduction from committed source | NOT DONE. |
| 5 | Simple-baseline comparison | PARTIAL EVIDENCE ONLY. Prior wave f01c6b69d: UNION baseline scored 17/20 vs learner 20/20. No committed formal comparison against the K=2 rebuild. Not claimed. |
| 6 | Alternative-explanation attack | PARTIAL EVIDENCE ONLY. F3 source audit: 0 hits for "not", "negat", "is_negator" in the committed learner; routing references only OPREC.trigger_form id. No formal attack step. Not claimed. |
| 7 | OOD test | PARTIAL EVIDENCE ONLY. F2: novel negated "grn" (never negated in training) 3/3. The sealed evaluation is the formal OOD step. Not claimed until then. |
| 8 | Ablation | PARTIAL EVIDENCE ONLY. F4: operator table emptied, T1 3/3 -> 0/3, drop localized to negation items; 20-item 20/20 -> 17/20. No independent ablation protocol. Not claimed as step 8. |
| 9 | Transfer/reuse test | PARTIAL EVIDENCE ONLY. F2 scope-shift to a novel word is a reuse probe, not a formal transfer test. Not claimed. |
| 10 | Independent red team | NOT DONE. |
| 11 | Governance audit | NOT DONE. |

## Why the partial evidence does not satisfy steps 5-9

The rebuild's R4 falsifiers F1-F5 are in-wave evidence, executed by
the builder against a battery the builder knew. Steps 5-9 require
separate committed executions with their own frozen preregs:
baseline with a frozen simple control, attack with a frozen attack
hypothesis, OOD on sealer-held data, ablation by an independent
protocol, transfer on a new surface. Reusing F2-F5 as the formal
steps would double-count builder-known evidence. They are recorded
as partial evidence only.

## Next step

Step 3, sealed evaluation. The frozen prereg is
SEALED_EVAL_PREREG.md in this directory. It must be executed by an
independent sealer (a worker instance different from the rebuild
builder), in its own owned path
docs/lab/research-lead/overnight-20260928/opscope_sealed/.

A SEALED-PASS result completes step 3 and unlocks steps 4-11
(independent reproduction, then baseline, attack, OOD, ablation,
transfer, red team, governance audit, in pipeline order).

## Verdict of this task

PIPELINE-INITIATED. Status documented, step 3 identified and
preregistered. No SURVIVES claim: 8 of 11 steps remain (3 not done,
5 partial evidence only).
