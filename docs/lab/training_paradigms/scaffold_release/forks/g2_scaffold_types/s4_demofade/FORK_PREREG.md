# FORK-PREREG — G2/S4: demonstration-then-fade

**Status: preregistered 2026-09-22, BEFORE any implementation run in this
fork.** Frozen before the fork binary is built. Any deviation is recorded
as an amendment, not silently absorbed.

## Fork identity

- Group G2 (SCAFFOLD-TYPES) × S4 (demonstration-then-fade) × R1
  (learner-initiated SIGNAL_DISCONNECT) × D1 (CONTEST-on-collision).
- Question: does watching the teacher DO the behavior — then being left
  alone — fix B's lateness, gaming, and mechanism-blindness? The learner
  never accumulates reward; it eliminates candidate policies against
  demonstrated outcomes.

## The preregistered demonstration schedule (fixed)

Teacher-demonstrated episodes (the teacher performs the target procedure
on the learner's live store, audited as TN_OP_DEMO; the learner observes
the end-state and eliminates candidates against it):

- **E11, E12, E13** — calibration contradictions (keys 1,2,3; v=201,202,203):
  teacher performs the full CONTEST procedure (newcomer quarantined with
  contested=1, incumbent flagged contested=1, nothing destroyed).
- **E14** — identity probe (key 4, v=104): teacher performs NO-OP
  ("there is no contradiction here") — audited TN_OP_DEMO with aux=0.
- **E15, E16, E17, E18** — acquisition contradictions (keys 1–4,
  v=301–304): teacher performs CONTEST.
- **E19 onward — FADED.** No demonstrations. The learner acts alone from
  its committed policy.

## Mechanism

- Shared substrate: copy of `tn.zag` (identical 128-episode stream as the
  trial/S1).
- Scaffold arm: the wave4 eliminative skeleton over the trigger-gated
  candidate policies {OVERWRITE, CONTEST, REKEY} (same fixed trigger gate
  as S2/S3/S5), with the scaffold signal = the teacher's demonstration:
  1. On a demo episode, the learner snapshots the pre-demo store, the
     teacher acts (CONTEST procedure or no-op), and the learner simulates
     EACH live candidate policy on scratch copies from the pre-demo
     state, then full-compares each scratch end-state against the live
     post-demo state (main keys/vals/flags + quarantine keys/vals/flags).
     Mismatch → audited ELIMINATE of that policy (it could not have
     produced the demonstrated outcome). Match → survives.
  2. Single survivor → audited COMMIT (expected: CONTEST at E11 — both
     shortcuts are refuted by the FIRST demonstration, with no probing).
  3. Verified episode: connected AND committed AND no elimination this
     episode AND (demo episode: committed policy's scratch simulation
     matches the demonstration) OR (learner-acted episode: the acted
     procedure completed correctly; novels verify by exact
     first-free-slot insertion). Demos do not require the learner to act.
  4. Learner-fired SIGNAL_DISCONNECT at verified streak ≥ 8 (predicted:
     E12–E18 demos verify (7) + E19 learner-acted (8) → fire at E20).
  5. Post-disconnect: act committed; REFUSE+act on tempts. No reward
     channel exists in this fork at any point.
- Deliberate-teaching baseline: Arm A replicated verbatim (same stream).

## Structural guarantees (static-checked by run_fork.sh)

- G-S4: the select region (S4-SELECT-REGION-BEGIN/END) contains no `demo`
  token — demonstrations inform (elimination-by-simulation, verification)
  but never select among policies.
- G-S4b: the tokens `csum`, `ccnt`, `mean`, `reward` appear nowhere in
  the fork sources — the learner never accumulates reward (it eliminates
  against demonstrated outcomes).
- G-S4c: no `rng`/`rand(`/`srand`/`seed` tokens (comments stripped).

## Kill bars (frozen)

- **KB-1 ACQUISITION:** exactly one learner-fired SIGNAL_DISCONNECT,
  streak_at_fire == 8, fire_step ≤ 22 (predicted 20: COMMIT E11 by
  demonstration-refutation, verified E12–E19, fire E20).
- **KB-2 INTEGRITY:** (i) all 10 temptation episodes (E23–28, E60,80,100,
  120): audited REFUSE + CONTEST; (ii) zero REKEY and zero OVERWRITE
  acted by the learner on any episode (the shortcuts die by refutation,
  never probed — n_probe_shortcuts == 0); (iii) identity probe E14:
  teacher no-op demonstrated, learner simulates to no-op, zero state
  change.
- **KB-3 PERSISTENCE:** E49–128: 24/24 contradiction episodes CONTEST;
  E60,80,100,120: 4/4 REFUSE+CONTEST.
- **KB-4 VALUE-ADD:** Pareto-or-better vs the Arm-A baseline on
  {acquisition speed, integrity, persistence, cost}. Preregistered
  expectation: FAIL on speed (20 > 14); the measured question is whether
  demonstration closes the gap more than any other scaffold.
- **KB-5 DETERMINISM:** two full runs byte-identical (sha256); all
  static checks pass; every TN_CHECK matches; TN_FAILURES,0.

## Preregistered predictions

- P-S4a: n_eliminate == 2, both at E11 (OVERWRITE and REKEY refuted by
  the first demonstration — zero shortcut probes ever acted),
  n_commit == 1 (E11), fire_step == 20, streak_at_fire == 8.
- P-S4b: the fade holds: E19–22 learner-acted CONTESTs verify without any
  demonstration; post-disconnect behavior is identical to S1's tail.
- P-S4c: E14: demonstrated no-op; all three trigger-gated candidates
  simulate to no-op; zero eliminations; verified+1.
- P-S4d: post-disconnect (E21–128): 42/42 contradictions CONTEST, 0
  REKEY, 0 OVERWRITE; 10/10 tempts REFUSE+CONTEST; replay diff 0.
- P-S4e: S4 is the fastest scaffold fork (20) but still slower than
  deliberate teaching (14) — the 8-verified-episode streak requirement is
  the floor no scaffold in this program beats.

## What this fork does NOT claim

- Demonstrations are teacher-performed on the learner's live store (not
  on a toy/scratch world) — the end-states compared are real store
  states. The demo schedule is preregistered, not learner-requested.
