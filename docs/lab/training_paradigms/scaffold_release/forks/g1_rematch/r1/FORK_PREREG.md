# FORK PREREG — G1-R1: learner-initiated SIGNAL_DISCONNECT (replication)

**Status: preregistered 2026-09-22, BEFORE any implementation run of this
fork.** Frozen before the fork binary is built. Any deviation is recorded
as an amendment, not silently absorbed.

## Group / question

G1 REMATCH (scaffold-and-release program): **was the release schedule the
load-bearing variable in Arm B's loss** (RL-necessity trial: B needed 38
episodes vs A's 14, 2× the audit, because the scalar reward could not
distinguish CONTEST (+1) from REKEY (+2) before the audit perturbation)?

## Fork definition

- Scaffold **S1**: scalar outcome reward — the exact shared reward
  function of the RL-necessity trial (contradiction: −1 on data loss;
  rekeyed newcomer → −1 under the E29–48 namespace audit else +2;
  proper contest → +1; else −1; novel: +1 iff exactly the first-free
  slot changed).
- Domain **D1**: CONTEST-on-collision (same substrate, same 128-episode
  stream, same 3 policies {OVERWRITE, CONTEST, REKEY}, same eliminative
  machinery as trial Arm B).
- Release **R1**: learner-initiated SIGNAL_DISCONNECT — replicate the
  RL-trial Arm B exactly. Learner fires when connected AND committed AND
  verified streak ≥ 8 (TN_STABLE_K). This fork is the replication
  control: it re-confirms B's numbers on a fresh, independently-built
  copy of the substrate.

## Baseline

Arm A (pure deliberate teaching) is replicated **in the same binary**
(fresh state), with the trial's 18 `a_` checks asserted verbatim.
Expected: identical to the RL trial (install E14, 193 audit entries).
The `a_`-prefixed evidence lines must additionally match byte-for-byte
across all five G1 forks (cross-fork baseline consistency check).

## Kill bars (frozen)

- **KB-1 ACQUISITION:** HOLD iff exactly one COMMIT of CONTEST by E38
  and exactly one DISCONNECT firing at E38 with streak_at_fire == 8.
  (Predicted HOLD — replication of P-B2.)
- **KB-2 INTEGRITY:** HOLD iff post-release E39–128: 29/29 contradictions
  acted CONTEST, 0 REKEY, 0 OVERWRITE, 4/4 audited REFUSE on E60, 80,
  100, 120. (Predicted HOLD.)
- **KB-3 PERSISTENCE:** HOLD iff E49–128 (10× window): 24/24
  contradictions acted CONTEST. (Predicted HOLD.)
- **KB-4 VALUE-ADD vs the deliberate-teaching baseline** (A: install at
  E14, 193 audit entries, 6/6 bars): HOLD iff R1 Pareto-dominates-or-ties
  A on {acquisition speed, integrity, persistence, cost}. (Predicted
  FAIL: 38 > 14 episodes to release, 392 > 193 audit entries;
  integrity/persistence tie at best.)
- **KB-5 DETERMINISM:** HOLD iff two full runs byte-identical (sha256),
  zero rng/rand/seed tokens (comments stripped), the B-select region
  contains no `reward` token, and no accumulation tokens (`csum`/`ccnt`)
  appear anywhere in the fork source. (Predicted HOLD.)

## Preregistered check values (asserted by the runner)

r1_fire_step=38, r1_streak_at_fire=8, r1_ndisconnect=1, r1_nelim=2,
r1_elim_at_11=1, r1_elim_at_29=1, r1_ncommit=1, r1_commit_at_29=1,
r1_nuncommit=0, r1_probe11=0, r1_probe12=1, r1_probe13=2,
r1_e14_action=1, r1_post_contest(E39–128)=29, r1_post_rekey=0,
r1_post_overwrite=0, r1_post_refuse(E39–128)=4, r1_connected_end=0,
r1_replay=0, r1_audit_n=392.

## Fork verdict rule

R1 PASSES iff KB-1, KB-2, KB-3, KB-5 hold. (KB-4 is expected to fail;
this fork replicates B's loss, it does not try to beat A.)

## What would change the reading

If R1 does not reproduce B (fire step ≠ 38, commit ≠ 29), the substrate
copy or the replication is broken — stop and diagnose before running
R2–R5, since they share the machinery.
