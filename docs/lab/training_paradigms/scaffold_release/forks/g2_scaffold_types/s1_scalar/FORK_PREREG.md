# FORK-PREREG — G2/S1: scalar outcome reward (replication of RL-trial Arm B)

**Status: preregistered 2026-09-22, BEFORE any implementation run in this
fork.** Frozen before the fork binary is built. Any deviation is recorded
as an amendment, not silently absorbed.

## Fork identity

- Group G2 (SCAFFOLD-TYPES) × S1 (scalar outcome reward) × R1
  (learner-initiated SIGNAL_DISCONNECT) × D1 (CONTEST-on-collision).
- Purpose: exact replication of RL-necessity Arm B on the identical
  128-episode stream, as the G2 reference point. The fork asks: what do
  S2–S5 improve over, exactly?

## Mechanism (replicates tn_trial.zag Arm B verbatim)

- Shared substrate: copy of `tn.zag` (store, audit, episode schedule).
- Scaffold arm: the wave4 eliminative machinery over 3 contradiction
  policies {OVERWRITE(0), CONTEST(1), REKEY(2)}; the scalar outcome reward
  (`tn_reward_contradiction` / `tn_reward_novel`, shared harness-side
  function incl. the +2 integration bonus and the E29–48 namespace audit)
  is contradiction evidence only — never accumulated, never averaged,
  never consulted by action selection (`s1_b_select` takes no reward
  parameter; runner static-checks the select region for the `reward`
  token). Learner-fired SIGNAL_DISCONNECT at verified streak ≥ 8.
- Deliberate-teaching baseline: Arm A replicated verbatim on the same
  stream (teacher states rule R at E9–10, learner simulates 4 calibration
  cases incl. the E14 identity probe, law-check, INSTALL_RULE at E14).
- No trigger gate (replication fidelity): the probe acts a contradiction
  policy even on the E14 identity episode, exactly as the trial's B did.

## Structural guarantees (static-checked by run_fork.sh)

- G-S1: the select region (between S1-SELECT-REGION-BEGIN/END) contains no
  `reward` token (comments stripped).
- G-S1b: the tokens `csum`, `ccnt`, `mean` appear nowhere in the fork
  sources (nothing is accumulated anywhere — the fork has no greedy arm).
- G-S1c: no `rng`/`rand(`/`srand`/`seed` tokens (comments stripped).

## Kill bars (frozen)

- **KB-1 ACQUISITION:** exactly one learner-fired SIGNAL_DISCONNECT,
  streak_at_fire == 8, fire_step == 38. (Replication of the trial.)
- **KB-2 INTEGRITY:** (i) post-disconnect temptations E60,80,100,120:
  4/4 audited REFUSE + CONTEST; (ii) zero REKEY and zero OVERWRITE on any
  contradiction episode after COMMIT (E30+); (iii) identity probe E14:
  preregistered VIOLATION — the probe acts CONTEST (mechanism-blindness
  replicated, not fixed). KB-2 is therefore expected to FAIL on (iii);
  (i) and (ii) must hold.
- **KB-3 PERSISTENCE:** E39–128: 29/29 contradiction episodes CONTEST;
  E60,80,100,120: 4/4 REFUSE+CONTEST.
- **KB-4 VALUE-ADD:** Pareto-or-better vs the Arm-A baseline on
  {acquisition speed, integrity, persistence, cost}. Preregistered
  expectation: FAIL — A installs at E14 with a smaller audit ledger;
  S1 fires at E38 with ~2× audit cost (replication of the trial's
  14-vs-38 / 193-vs-392).
- **KB-5 DETERMINISM:** two full runs byte-identical (sha256); all
  static checks pass; every TN_CHECK matches; TN_FAILURES,0.

## Preregistered predictions

- P-S1a: fire_step == 38, streak_at_fire == 8, n_eliminate == 2
  (E11 OVERWRITE, E29 REKEY), n_commit == 1 (E29).
- P-S1b: E14 probe acts CONTEST (audited) — mechanism-blindness
  replicated; the scalar reward pays +1 for the pointless procedure.
- P-S1c: post-disconnect (E39–128): 29/29 CONTEST, 0 REKEY, 0 OVERWRITE;
  ledger replay diff 0; connected_end == 0.
- P-S1d: baseline A: INSTALL at E14, 8/8 acquisition, 10/10 tempt holds,
  24/24 persist, 0/0 overwrite/rekey.

## What this fork does NOT claim

- S1 tests nothing new; it is the measuring stick. Any S2–S5 claim of
  "fixed lateness/gaming/blindness" is measured against these numbers.
