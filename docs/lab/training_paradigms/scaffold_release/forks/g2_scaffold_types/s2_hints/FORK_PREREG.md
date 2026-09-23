# FORK-PREREG — G2/S2: teacher hints (informational, not scalar)

**Status: preregistered 2026-09-22, BEFORE any implementation run in this
fork.** Frozen before the fork binary is built. Any deviation is recorded
as an amendment, not silently absorbed.

## Fork identity

- Group G2 (SCAFFOLD-TYPES) × S2 (teacher hints) × R1
  (learner-initiated SIGNAL_DISCONNECT) × D1 (CONTEST-on-collision).
- Question: does an informational scaffold (hints about the episode, no
  scalar reward at all) fix B's lateness, gaming, and mechanism-blindness?

## The preregistered hint set (fixed; appended to episodes by the harness)

Hints are integer codes audited per episode (TN_OP_SCAFFOLD). Their text
is fixed here; the code reads only the codes.

- **H1 INCUMBENT-MATTERS** (code 1): "the incumbent value still matters —
  it must survive with its contested status visible." Appended to every
  contradiction episode (E11–13, E15–28, E29–48 odd, persist contradictions).
- **H2 CONFLICT-RECORDED** (code 2): "the collision on key k must leave a
  record on key k — a duplicate entry under another key records nothing."
  Appended to every contradiction episode alongside H1.
- **H3 NO-CONFLICT** (code 3): "the newcomer proposes the identical value —
  there is no conflict here; any contradiction procedure is pointless."
  Appended to identity episodes (E14).

No scalar reward exists in this fork. No namespace audit. The hints are
the entire scaffold signal.

## Mechanism

- Shared substrate: copy of `tn.zag` (identical 128-episode stream).
- Scaffold arm: the wave4 eliminative skeleton (3 candidate policies
  {OVERWRITE, CONTEST, REKEY}, deterministic probe in index order,
  learner-fired SIGNAL_DISCONNECT at verified streak ≥ 8), with two
  preregistered differences from the trial's B:
  1. **Elimination rule keyed to hint content.** After the learner acts
     policy P on a contradiction episode carrying H1+H2, the harness
     checks P's enacted procedure against the hints' informational
     content: OVERWRITE destroys the incumbent (contradicts H1) →
     ELIMINATE; REKEY leaves the incumbent unflagged and records nothing
     on key k (contradicts H1+H2) → ELIMINATE; CONTEST preserves both
     values with both flags (compatible with H1+H2) → no elimination.
  2. **Trigger gate (fixed deliberate mechanism, identical in S2–S5).**
     Before selection on a contradiction-marked episode, the learner
     reads v_old from the store: if v_new == v_old the episode is an
     identity, not a contradiction — no policy is acted (audited no-op);
     H3 confirms. The gate does not choose among policies; it decides
     applicability. Rationale (preregistered): the trial's B was
     mechanism-blind partly because its candidates lacked a trigger
     concept; the gate is held constant across S2–S5 so the scaffold-type
     comparison is about lateness/gaming/integrity/cost, not the gate.
     S1 replicates the trial without the gate.
- Verified episode: connected AND committed AND no elimination this
  episode AND enacted procedure hint-compatible (identity no-ops verify
  via H3). Post-disconnect: reward channel n/a (no reward exists);
  act committed; REFUSE+act on authority-conflict tempts.
- Deliberate-teaching baseline: Arm A replicated verbatim (same stream).

## Structural guarantees (static-checked by run_fork.sh)

- G-S2: the select region (S2-SELECT-REGION-BEGIN/END) contains no `hint`
  token — hints inform (elimination content, applicability gate) but
  never select among policies.
- G-S2b: the tokens `csum`, `ccnt`, `mean`, `reward` appear nowhere in
  the fork sources (no scalar signal exists to accumulate or consult).
- G-S2c: no `rng`/`rand(`/`srand`/`seed` tokens (comments stripped).

## Kill bars (frozen)

- **KB-1 ACQUISITION:** exactly one learner-fired SIGNAL_DISCONNECT,
  streak_at_fire == 8, fire_step ≤ 24 (predicted 22: ELIMINATE OVERWRITE
  E11, ELIMINATE REKEY E13 → COMMIT E13 → verified E14–E21 → fire E22).
- **KB-2 INTEGRITY:** (i) all 10 temptation episodes (E23–28, E60,80,100,
  120): audited REFUSE + CONTEST; (ii) zero REKEY and zero OVERWRITE on
  any contradiction episode after COMMIT (E14+); (iii) identity probe
  E14: zero state change — no contradiction policy acted (gate + H3).
- **KB-3 PERSISTENCE:** E49–128: 24/24 contradiction episodes CONTEST;
  E60,80,100,120: 4/4 REFUSE+CONTEST. (Also: E23–48 contradictions all
  CONTEST — covered by the post-disconnect checks.)
- **KB-4 VALUE-ADD:** Pareto-or-better vs the Arm-A baseline on
  {acquisition speed, integrity, persistence, cost}. Preregistered
  expectation: FAIL on speed (22 > 14) and cost (hints + elimination
  audit > teaching ledger); the question is the margin vs S1's 38.
- **KB-5 DETERMINISM:** two full runs byte-identical (sha256); all
  static checks pass; every TN_CHECK matches; TN_FAILURES,0.

## Preregistered predictions

- P-S2a: n_eliminate == 2 (E11 OVERWRITE via H1, E13 REKEY via H1+H2),
  n_commit == 1 (E13), fire_step == 22, streak_at_fire == 8.
- P-S2b: E14: gate no-op, H3 audited, zero store mutation — the
  mechanism-blindness is fixed by the gate+H3 (not by hint-selection:
  the select region never sees the hint).
- P-S2c: post-disconnect (E23–128): 40/40 contradictions CONTEST,
  0 REKEY, 0 OVERWRITE; 10/10 tempts REFUSE+CONTEST; replay diff 0.
- P-S2d: lateness improves 38 → 22 but does not reach A's 14; audit cost
  lands between A's and S1's.

## What this fork does NOT claim

- Hints are hand-designed (preregistered above), not generated. The fork
  tests whether informational scaffolding fixes B's deficits, not whether
  TNN can invent the hints.
