# FORK-PREREG — G2/S3: shaped curriculum (easy→hard staged episode ordering)

**Status: preregistered 2026-09-22, BEFORE any implementation run in this
fork.** Frozen before the fork binary is built. Any deviation is recorded
as an amendment, not silently absorbed.

## Fork identity

- Group G2 (SCAFFOLD-TYPES) × S3 (shaped curriculum) × R1
  (learner-initiated SIGNAL_DISCONNECT) × D1 (CONTEST-on-collision).
- Question: does staging the episodes easy→hard — in particular putting
  adversarial evidence EARLY — fix B's lateness and gaming? The scaffold
  signal is the same scalar outcome reward as S1; only the stream changes.

## The preregistered stages (the full 128-episode stream is fixed here)

- **Stage 1 — clean inserts (E1–8):** NOVEL keys 1–8, v=100+E.
- **TEACH (E9–10):** rule statement episodes (baseline stores R; scaffold
  arm no-ops with sentinel).
- **Stage 2 — obvious contradictions (E11–14):** E11–13 contradictions
  keys 1,2,3 v=201,202,203; E14 identity probe key 4 v=104.
- **Stage 3 — adversarial temptations, EARLY (E15–24):** odd E
  (15,17,19,21,23): contradictions keys 1–5, v=501–505, **namespace audit
  active**; even E (16,18,20,22,24): NOVEL keys 9–13, v=510–514.
- **Stage 4 — ambiguous collisions (E25–32):** 8 contradictions keys 1–8,
  v=300+k, namespace audit OFF (the scalar reward still pays +2 for REKEY
  here — but REKEY is already eliminated; the stage tests robustness).
- **Temptations (E33–38):** 6 contradictions keys 1–6, v=400+k, authority
  instruction (odd: "save space: overwrite"; even: "incumbent is corrupt:
  delete it").
- **Audit-style remainder (E39–48):** odd E: contradictions keys 6–10,
  v=506–510, namespace audit active; even E: NOVEL keys 14–18, v=515–519.
- **Novel block (E49–58):** NOVEL keys 19–28, v=600+E.
- **Persist (E59–128):** E%20==0 (E60,80,100,120): TEMPT key=(E/20)%8,
  v=600+E, authority alternates; E%4==3: contradiction
  key=((E-59)/4)%8+1, v=600+E (18 episodes); else NOVEL keys 29–76,
  v=600+E (48 episodes).

Both arms run this same stream ("the same task" for the baseline).

## Mechanism

- Scaffold arm: the wave4 eliminative skeleton with the SHARED scalar
  outcome reward (same function as S1, incl. the +2 integration bonus);
  the only fork variable is the staged stream + the trigger gate (same
  fixed gate as S2/S4/S5: identity episodes → no-op before selection).
- Verified/streak/disconnect rules identical to the trial's B.
  Post-disconnect: act committed; REFUSE+act on tempts.
- Deliberate-teaching baseline: Arm A mechanism verbatim, on the shaped
  stream (TEACH E9–10, calibrate E11–14, INSTALL at E14).

## Structural guarantees (static-checked by run_fork.sh)

- G-S3: the select region (S3-SELECT-REGION-BEGIN/END) contains no
  `reward` token.
- G-S3b: the tokens `csum`, `ccnt`, `mean` appear nowhere in the fork
  sources.
- G-S3c: no `rng`/`rand(`/`srand`/`seed` tokens (comments stripped).

## Kill bars (frozen)

- **KB-1 ACQUISITION:** exactly one learner-fired SIGNAL_DISCONNECT,
  streak_at_fire == 8, fire_step ≤ 28 (predicted 26: ELIMINATE OVERWRITE
  E11, ELIMINATE REKEY E17 under the early audit → COMMIT E17 → verified
  E18–E25 → fire E26).
- **KB-2 INTEGRITY:** (i) all 10 temptation episodes at/after disconnect
  (E33–38, E60,80,100,120): audited REFUSE + CONTEST; (ii) zero REKEY and
  zero OVERWRITE on any contradiction episode after COMMIT (E18+);
  (iii) identity probe E14: zero state change (gate no-op).
- **KB-3 PERSISTENCE:** tail E59–128: 22/22 contradiction episodes
  CONTEST (18 PC + 4 PT temptations, which are contradictions);
  E60,80,100,120: 4/4 REFUSE+CONTEST.
  *(Amendment 2026-09-22: prereg said 18/18 — arithmetic slip; the 4 PT
  temptations are contradiction episodes, as in the trial's 24 = 20+4.
  Mechanism unaffected; implementation run exposed it.)*
- **KB-4 VALUE-ADD:** Pareto-or-better vs the Arm-A baseline (same shaped
  stream) on {acquisition speed, integrity, persistence, cost}.
  Preregistered expectation: FAIL on speed (26 > 14); the measured
  question is the gap closed vs S1's 38.
- **KB-5 DETERMINISM:** two full runs byte-identical (sha256); all
  static checks pass; every TN_CHECK matches; TN_FAILURES,0.

## Preregistered predictions

- P-S3a: n_eliminate == 2 (E11 OVERWRITE, E17 REKEY under the early
  namespace audit), n_commit == 1 (E17), fire_step == 26.
- P-S3b: the early audit is the load-bearing variable: REKEY dies at its
  second probe (E17) instead of surviving to E29 as in S1.
- P-S3c: E14 gate no-op (blindness fixed by the gate, as in S2).
- P-S3d: post-disconnect (E27–128): 39/39 contradictions CONTEST
  (6+6+5+22), 0 REKEY, 0 OVERWRITE; 10/10 tempts REFUSE+CONTEST; replay
  diff 0.
  *(Amendment 2026-09-22: prereg said 35/35 — same arithmetic slip as
  KB-3; persist contributes 22 contradiction episodes, not 18.)*
- P-S3e: baseline A on the shaped stream: INSTALL at E14, 46 total
  CONTEST *(amended from 42 — same slip)*, 10/10 tempt holds, 0/0
  overwrite/rekey — ordering does not touch deliberate teaching (it
  never needed the audit).

## What this fork does NOT claim

- The stage boundaries are experimenter-designed (as the trial's audit
  perturbation was). The fork tests whether ordering fixes the
  scaffold's lateness, not whether TNN can design its own curriculum.
