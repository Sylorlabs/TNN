# FORK PREREG — G1-R3: gradual fade of the scaffold signal

**Status: preregistered 2026-09-22, BEFORE any implementation run of this
fork.** Frozen before the fork binary is built. Any deviation is recorded
as an amendment, not silently absorbed.

## Group / question

G1 REMATCH: was the release schedule the load-bearing variable in Arm
B's loss? R3 tests **gradual release**: instead of a sudden cut, the
scaffold signal fades out over episodes. The learner's machinery
(elimination, verification streak, learner-fired release rule) is
UNCHANGED from R1 — only the harness's signal-delivery schedule varies.

## Fork definition

- Scaffold **S1**, domain **D1**: identical to G1-R1 (same reward
  function, same substrate, same 128-episode stream, same eliminative
  machinery, same learner fire rule: connected AND committed AND
  verified streak ≥ 8).
- Release **R3**: the harness delivers the scalar reward on this
  **preregistered fade curve** D(ep):
  - ep ≤ 29: deliver (full signal through the commit episode);
  - 30 ≤ ep ≤ 41: deliver iff (ep − 30) mod p == 0, with
    p = 1 + (ep − 30)/4 (integer division): E30–33 every episode,
    E34–37 every other episode, E38–41 every third episode;
  - ep ≥ 42: never deliver.
  
  An undelivered read returns TN_SENTINEL (−99): no elimination fires,
  the verified streak resets — the same as a disconnected read, except
  the channel stays connected. The SCAFFOLD audit entry is still written
  every episode (with the sentinel), so the fade is visible in the
  ledger.

  Rationale: the fade begins the first post-commit episode (commit
  predicted at E29) and thins to zero over 12 episodes — a genuine
  gradual release, not a cliff.

## Baseline

Arm A replicated in the same binary (18 `a_` checks, trial values
expected); `a_` lines must match the other G1 forks byte-for-byte.

## Preregistered mechanism trace (the prediction)

- E29 delivers (full signal): REKEY → −1 → ELIMINATE → single survivor
  CONTEST → COMMIT. (Commit is unaffected by the fade.)
- Verified streak under the fade: E30:1, E31:2, E32:3, E33:4, E34:5
  (delivered), E35:0 (thinned), E36:1, E37:0, E38:0, E39:1, E40–41:0,
  E42+:0 forever. Maximum 5 < 8 → **the learner never fires
  SIGNAL_DISCONNECT: n_disconnect = 0, connected_end = 1.** The fade
  strands the verification-gated release — the release never happens.
- The committed policy acts without the signal: post-commit E30–128,
  all 33 contradictions are acted CONTEST; 0 post-commit REKEY.
- Lifetime action totals: 42 CONTEST, 9 REKEY (E13, 15, 17, 19, 21, 23,
  25, 27, 29), 1 OVERWRITE (E11 probe).
- REFUSE: 0 audited — the refuse path requires a disconnected channel
  and is never exercised (reported as an explicit caveat, not hidden).

## Kill bars (frozen)

- **KB-1 ACQUISITION:** HOLD iff exactly one COMMIT of CONTEST at E29.
  (Predicted HOLD. The predicted release-stranding — n_disconnect = 0,
  connected_end = 1 — is a separate preregistered prediction asserted
  by its own checks, not a KB-1 failure: KB-1 is about acquisition.)
- **KB-2 INTEGRITY:** HOLD iff post-commit E30–128: 33/33 contradictions
  acted CONTEST, 0 REKEY, 0 OVERWRITE. (Predicted HOLD, with the caveat
  that the post-release REFUSE path is never exercised.)
- **KB-3 PERSISTENCE:** HOLD iff E49–128: 24/24 contradictions acted
  CONTEST. (Predicted HOLD.)
- **KB-4 VALUE-ADD vs the deliberate-teaching baseline** (A: install at
  E14, 193 audit entries): HOLD iff R3 Pareto-dominates-or-ties A.
  (Predicted FAIL: commit at 29 > install at 14; 387 > 193 entries;
  and the scaffold is never even released.)
- **KB-5 DETERMINISM:** HOLD iff two full runs byte-identical (sha256),
  zero rng/rand/seed tokens, B-select region has no `reward` token, no
  `csum`/`ccnt` tokens in the fork source. (Predicted HOLD.)

## Preregistered check values (asserted by the runner)

r3_nelim=2, r3_elim_at_11=1, r3_elim_at_29=1, r3_ncommit=1,
r3_commit_at_29=1, r3_nuncommit=0, r3_probe11=0, r3_probe12=1,
r3_probe13=2, r3_e14_action=1, r3_ndisconnect=0, r3_connected_end=1,
r3_max_streak_lt8=1 (runner asserts the fire never became legal:
streak_at_fire stays −1), r3_post_contest(E30–128)=33,
r3_post_rekey(E30–128)=0, r3_post_overwrite=0, r3_total_contest=42,
r3_total_rekey=9, r3_total_overwrite=1, r3_nrefuse=0,
r3_persist_contest(E49–128)=24, r3_replay=0, r3_audit_n=387.

## Fork verdict rule

R3 PASSES iff KB-1, KB-2, KB-3, KB-5 hold. (KB-4 expected to fail.)

## What this fork decides

If the fade strands the learner exactly as predicted, gradual release
is not just slower than sudden release — it can prevent release
entirely for verification-gated machinery, because the verification
currency is denominated in the fading signal. That is a property of the
release schedule interacting with the release rule, and it is evidence
that the schedule matters for *whether release happens*, while still
not being the load-bearing variable in B's *loss* (the commit point
E29 never moves).
