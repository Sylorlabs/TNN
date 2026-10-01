# Wave record: wave-20261001-0821pdt

Coordinator: subagent 6fafe917 (parent: main agent, scheduler.cron).
Working copy: ~/workspace/tnn-rsi, branch tnn-native-lab.
Toolchain guard: safebin active at coordinator startup; `which python3`
resolves to nothing; recorded in NAMECHECK.md Step 0.

## Execution mode

Descendant workers were attempted (8 lanes). Coordinator fell back to
inline execution for lanes whose workers died at NAMECHECK (see per-lane
status below). This section is updated as the wave proceeds.

## Lane status

- exp2 (H-EXP2 v2 step 6 alternative-explanation attack): worker alive.
- fork-battery: worker alive.
- sensory: worker alive.
- freelunch: worker alive.
- ddes (ddes_followup re-freeze): worker alive.
- pi_rev2 (H-PI-REV2 step 5 baseline prereg): worker alive.
- adv_battery (TNN-2 post-freeze adversarial battery prereg): worker alive.
- actexp (F2 retry harder goal prereg): worker alive.

No em-dashes in this documentation.

## OUTCOME: INCOMPLETE

The wave died on the descendant-subagent runtime defect (thirteenth
kill). This wave tried a hybrid: descendant workers attempted (8
lanes), coordinator falling back to inline execution for lanes whose
workers died at NAMECHECK. The hybrid got further than pure
descendants but still died before any verdict or debate.

Partial evidence preserved (all committed):
- exp2 (H-EXP2 v2 step 6 alternative-explanation attack): the lane
  built altexp.zag (dumb baselines: enum/first/rnd/fixed probe
  choice; pruning machinery IDENTICAL to expseq, only probe choice
  differs; pure Zag, deterministic) and ran a 16-run sweep against
  the sealed worlds. 16/16 completed. Result pattern in
  sweep_out/sweep.tsv: 12/16 IDENTIFIED the law, but every w_X_2 run
  (4/4, one per seed group) STALLED at round=6. The stall is
  systematic on one law family and awaits a verdict next wave.
- Other lanes (adv_battery, ddes, fork_battery, freelunch, pi_rev2,
  sensory): NAMECHECK guard records only. actexp, redteam: empty.

Queued work rolls forward unchanged, with the step-6 STALLED pattern
now first in the exp2 queue (verdict: is the stall a law-family
property or a baseline artifact?).
