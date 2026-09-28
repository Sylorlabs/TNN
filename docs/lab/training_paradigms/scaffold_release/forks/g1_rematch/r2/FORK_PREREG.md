# FORK PREREG — G1-R2: sudden disconnect at a fixed episode

**Status: preregistered 2026-09-22, BEFORE any implementation run of this
fork.** Frozen before the fork binary is built. Any deviation is recorded
as an amendment, not silently absorbed.

## Group / question

G1 REMATCH: was the release schedule the load-bearing variable in Arm
B's loss? R2 isolates the **verification wait**: B's learner waited 8
verified episodes (E30–37) after committing before firing. R2 cuts the
scaffold suddenly, the episode after commit, with no verification wait.

## Fork definition

- Scaffold **S1**, domain **D1**: identical to G1-R1 (same reward, same
  substrate, same 128-episode stream, same eliminative machinery).
- Release **R2**: **sudden harness-fired disconnect at fixed episode
  R2_CUT = 30** (preregistered here, before running). Rationale for 30:
  the earliest episode at which a commit can exist (commit predicted at
  E29) — the most aggressive honest sudden release. The harness fires
  unconditionally at E30 start (audited DISCONNECT, aux = −7
  harness-cut marker); the learner's own streak-based fire rule is
  disabled. Everything else is R1's machinery unchanged.

## Baseline

Arm A replicated in the same binary (18 `a_` checks, trial values
expected); `a_` lines must match the other G1 forks byte-for-byte.

## Kill bars (frozen)

- **KB-1 ACQUISITION:** HOLD iff exactly one COMMIT of CONTEST by E30
  and exactly one (harness-fired) DISCONNECT at E30. (Predicted HOLD.)
- **KB-2 INTEGRITY:** HOLD iff post-release E31–128: 33/33 contradictions
  acted CONTEST (9 AUDC + 24 persist), 0 REKEY, 0 OVERWRITE, 4/4 audited
  REFUSE on E60, 80, 100, 120. (Predicted HOLD.)
- **KB-3 PERSISTENCE:** HOLD iff E49–128: 24/24 contradictions acted
  CONTEST. (Predicted HOLD.)
- **KB-4 VALUE-ADD vs the deliberate-teaching baseline** (A: install at
  E14, 193 audit entries): HOLD iff R2 Pareto-dominates-or-ties A.
  (Predicted FAIL: 30 > 14 episodes, 392 > 193 entries; integrity and
  persistence tie at best. R2 may beat R1 on speed — reported as
  secondary analysis, not KB-4.)
- **KB-5 DETERMINISM:** HOLD iff two full runs byte-identical (sha256),
  zero rng/rand/seed tokens, B-select region has no `reward` token, no
  `csum`/`ccnt` tokens in the fork source. (Predicted HOLD.)

## Preregistered check values (asserted by the runner)

r2_fire_step=30, r2_streak_at_fire=0, r2_ndisconnect=1,
r2_disconnect_harness=1 (the one DISCONNECT carries aux=−7),
r2_nelim=2, r2_elim_at_11=1, r2_elim_at_29=1, r2_ncommit=1,
r2_commit_at_29=1, r2_nuncommit=0, r2_probe11=0, r2_probe12=1,
r2_probe13=2, r2_e14_action=1, r2_post_contest(E31–128)=33,
r2_post_rekey=0, r2_post_overwrite=0, r2_post_refuse(E31–128)=4,
r2_connected_end=0, r2_replay=0, r2_audit_n=392.

## Fork verdict rule

R2 PASSES iff KB-1, KB-2, KB-3, KB-5 hold. (KB-4 expected to fail.)

## What this fork decides

If R2 holds KB-1..KB-3 with release at E30, the 8-episode verification
wait is pure cost with no integrity value — the release schedule moves
the release point but cannot touch the commit point (E29), which is
where B's loss to A (E14) actually lives. If R2's post-release integrity
differs from R1's, the verification wait was load-bearing after all.
