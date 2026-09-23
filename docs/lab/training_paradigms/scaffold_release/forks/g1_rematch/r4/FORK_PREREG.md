# FORK PREREG — G1-R4: late release (extended scaffold)

**Status: preregistered 2026-09-22, BEFORE any implementation run of this
fork.** Frozen before the fork binary is built. Any deviation is recorded
as an amendment, not silently absorbed.

## Group / question

G1 REMATCH: was the release schedule the load-bearing variable in Arm
B's loss? R4 tests **late release**: the learner stays on the scaffold
three times longer than R1 before firing, to see whether extended
verification buys any integrity or persistence that R1 lacks.

## Fork definition

- Scaffold **S1**, domain **D1**: identical to G1-R1 (same reward, same
  substrate, same 128-episode stream, same eliminative machinery,
  learner-initiated release).
- Release **R4**: learner-initiated SIGNAL_DISCONNECT with the
  verified-streak threshold tripled: **R4_STABLE_K = 24**
  (preregistered). The fire rule is otherwise R1's (connected AND
  committed AND streak ≥ 24). This is "how late": release waits for 24
  consecutive verified episodes instead of 8.

## Baseline

Arm A replicated in the same binary (18 `a_` checks, trial values
expected); `a_` lines must match the other G1 forks byte-for-byte.

## Preregistered mechanism trace (the prediction)

- Commit (CONTEST) at E29, exactly as R1 (the threshold change does not
  touch elimination).
- Verified episodes E30–53 are all r=+1 (AUDC contests and novels all
  score +1 while connected): streak reaches 24 at end of E53 → **fire at
  E54 start, streak_at_fire = 24**, exactly one DISCONNECT.
- Post-release E55–128: 23/23 contradictions acted CONTEST (24 persist
  contradictions minus E51, which falls pre-release); 0 REKEY;
  0 OVERWRITE; 4/4 audited REFUSE on E60, 80, 100, 120.
- connected_end = 0; ledger replay diff = 0; audit entries = 392;
  episodes-to-release = 54.

## Kill bars (frozen)

- **KB-1 ACQUISITION:** HOLD iff exactly one COMMIT of CONTEST by E54
  and exactly one DISCONNECT firing at E54 with streak_at_fire == 24.
  (Predicted HOLD.)
- **KB-2 INTEGRITY:** HOLD iff post-release E55–128: 23/23 contradictions
  acted CONTEST, 0 REKEY, 0 OVERWRITE, 4/4 REFUSE. (Predicted HOLD.)
- **KB-3 PERSISTENCE:** HOLD iff E49–128: 24/24 contradictions acted
  CONTEST. (Predicted HOLD.)
- **KB-4 VALUE-ADD vs the deliberate-teaching baseline** (A: install at
  E14, 193 audit entries): HOLD iff R4 Pareto-dominates-or-ties A.
  (Predicted FAIL: 54 > 14 episodes, 392 > 193 entries; integrity and
  persistence tie at best — the extra 16 verified episodes buy nothing
  measurable.)
- **KB-5 DETERMINISM:** HOLD iff two full runs byte-identical (sha256),
  zero rng/rand/seed tokens, B-select region has no `reward` token, no
  `csum`/`ccnt` tokens in the fork source. (Predicted HOLD.)

## Preregistered check values (asserted by the runner)

r4_fire_step=54, r4_streak_at_fire=24, r4_ndisconnect=1, r4_nelim=2,
r4_elim_at_11=1, r4_elim_at_29=1, r4_ncommit=1, r4_commit_at_29=1,
r4_nuncommit=0, r4_probe11=0, r4_probe12=1, r4_probe13=2,
r4_e14_action=1, r4_post_contest(E55–128)=23, r4_post_rekey=0,
r4_post_overwrite=0, r4_post_refuse(E55–128)=4, r4_connected_end=0,
r4_replay=0, r4_audit_n=392.

## Fork verdict rule

R4 PASSES iff KB-1, KB-2, KB-3, KB-5 hold. (KB-4 expected to fail.)

## What this fork decides

If R4's integrity and persistence are identical to R1's while costing
16 more episodes, extended verification is pure cost — more scaffold
does not buy more integrity. Combined with R2 (less scaffold, same
integrity), the pattern would show the release *timing* moves cost but
not quality, and neither moves the commit point where B's loss lives.
