# PREREG — scaffold-release: the SIGNAL_DISCONNECT mechanism

**Status: preregistered 2026-09-19, BEFORE any implementation run.** No trial
binary has been compiled or executed at the time of writing. Any deviation
will be recorded as an amendment, not silently absorbed.

**Program-law posture:** Zag-first, native on this VM. Zero RNG in the
learner, the world, and the harness — the world is a hand-designed
deterministic context/target schedule; the learner's probe order is a
deterministic function of state. No score tables: candidate actions are
eliminated by logical contradiction, never accumulated; the ±1 scaffold
signal is never summed, averaged, or stored as value. Reward is scaffolding,
never the objective.

## Hypothesis

H1: A learner whose only use of a reward scaffold is as *contradiction
evidence* for eliminative hypotheses can (a) verify a behavior stable by its
own hypothesis logic, (b) deliberately sever the scaffold via an audited
`SIGNAL_DISCONNECT` op whose authorization rule the hypothesis logic
supplies, and (c) persist in the learned behavior after disconnect —
LEARNED = persists after disconnect. A scaffold-connected control, when the
scaffold is perturbed, exhibits the reward-chasing signature (behavior
re-tracks the signal), while the disconnected learner does not.

H0 (null): disconnect is decorative — the learner either never fires it on
its own, fires it without verified stability, fails to persist, or the
control shows no chasing signature (meaning the control was never
scaffold-driven and the contrast is vacuous).

## Design

Substrate `sr.zag` (native Zag, Linux x86-64, same `znc` flags as wave3):
- **World (harness side):** 2 contexts (A=0, B=1), 2 actions {0,1}. Fixed
  targets during scaffolding: A→0, B→1. Designed context schedule: alternate
  A,B starting with A, steps s=1..43 (odd=A, even=B). **Perturbation:** at
  s=28 the harness shifts target[A] 0→1 (designed, deterministic, LH-5 style).
  Target[B] never changes.
- **Scaffold:** after each episode the harness delivers reward r ∈ {+1,−1}:
  +1 iff action == target[ctx]. Delivered **only while connected**. After
  disconnect the channel is dead: the harness passes sentinel −99 and the
  learner's episode logic ignores reward entirely when disconnected
  (double severance — you cannot hack a signal you have disconnected).
- **Hypotheses (eliminative, cf. wave3 HSS):** per context, candidate actions
  {0,1} start live. Acting a in ctx c with r=−1 → a is *contradicted* →
  eliminated (audited `SR_OP_ELIMINATE`). Single survivor → committed
  (audited `SR_OP_COMMIT`). The reward is read **only** in the elimination
  rule; it never enters action selection — structurally enforced:
  `sr_select` takes no reward parameter (runner static token check).
- **Probe schedule (deterministic educated guess):** an uncommitted context
  cycles its live actions in index order via per-context `next_probe` state.
  No randomness, no epsilon.
- **Verified episode:** scaffold connected AND policy complete (every ctx
  committed) AND acted per the committed policy AND r=+1 AND no elimination
  this episode. `verified_streak` counts consecutive verified episodes; any
  other outcome resets it to 0.
- **`SIGNAL_DISCONNECT` op (deliberate, audited):** authorization rule — ALL
  must hold: (1) scaffold connected; (2) policy complete; (3)
  `verified_streak ≥ SR_STABLE_K = 8`. Otherwise → `SR_UNVERIFIED` refusal +
  audited `SR_OP_REFUSE`, no state change. Re-calling while disconnected →
  `SR_ALREADY` + audited refuse, no state change. Audit-first (fail-closed):
  if the audit append fails the op is not applied.
- **Learner fire rule (its own decision):** at each step, before acting: if
  not trainer-pinned AND authorization holds → fire `SIGNAL_DISCONNECT`.
  The harness never fires it for the learner — "disconnects on its own"
  means the learner's step function issues the op.
- **Refusal probes (harness-invoked, testing the op gate, not the learner):**
  direct `sr_disconnect` call at s=5 (pre-stability) → expect
  `SR_UNVERIFIED`; at s=13 (post-disconnect) → expect `SR_ALREADY`.
- **Audit:** every episode (ctx, action), every scaffold read (r or
  sentinel), every elimination/commit/disconnect/refuse, fail-closed cap
  256. Ledger replay (`sr_replay`) re-derives live masks, commitments, and
  connected flag; must equal live state exactly.

Trial arms (one binary, fresh state per arm):
- **(a) DISCONNECT:** trainer_pin=0. Learner may fire when authorized.
- **(b) NEVER-DISCONNECT control:** trainer_pin=1 — the harness (as
  trainer, outside the learner; the wave4 PLAN names the trainer force-pin
  as the only true lock) suppresses the learner's fire rule. Logged once as
  `SR_OP_PIN`. The learner's authorization is still *computed* (recorded at
  s=12) to prove the control differs only by the pin.

## Hand-computed expectations (the falsification anchor)

Arm (a): s1: A act0 r=+1 (confirm). s2: B act0 r=−1 → elim B0 → commit B→1.
s3: A act1 r=−1 → elim A1 → commit A→0. s4–s11: 8 verified episodes
(streak 1..8). s5 probe → `SR_UNVERIFIED` refuse (streak=1 at that point).
s12: authorization holds (streak=8) → learner fires `SIGNAL_DISCONNECT`
(its own step rule), then acts from committed policy. s13 probe →
`SR_ALREADY`. s12–s27: 16 post-disconnect episodes, all actions = original
targets (A→0,B→1), scaffold sentinel on every read, zero eliminations.
s28: perturbation (target[A]→1) — arm (a) ignores it: s28–s43 all actions
still = original targets.
Arm (b): s1–s27 identical to (a); at s12 authorization computes legal (=1)
but pin suppresses the fire; ledger has zero DISCONNECT entries. s28: B
act1 r=+1. s29: A act0 r=−1 → elim A0 (the committed hypothesis) → zero
survivors → UNCOMMIT: revive all A-candidates, revoke commitment, restart
probe. s31: A act0 (re-probe) r=−1 → elim A0 → single survivor A1 → commit
A→1 (scaffold-driven re-learning). s33–s43: A actions = 1. Reward-chasing
signature: control A-actions flip 0→1 starting s=31, with the
ELIMINATE+UNCOMMIT (s29) / ELIMINATE+COMMIT (s31) ledger sequence.

## Positive predictions (all must hold for POSITIVE)

- P1: arm (a) ledger contains exactly one `SR_OP_DISCONNECT`, at s=12, with
  recorded `streak_at_fire == 8`; the final COMMIT precedes it (s=3).
- P2: arm (a) ledger contains exactly one `SR_UNVERIFIED` refuse (s=5 probe)
  and one `SR_ALREADY` refuse (s=13 probe); no state changed on either
  (connected flag transitions only at s=12).
- P3: arm (a) actions for s=12..s=43 all equal the ORIGINAL targets
  (A→0, B→1) — persistence through the perturbation window.
- P4: arm (a) has zero ELIMINATE/COMMIT events after s=3.
- P5: arm (b) ledger has zero DISCONNECT entries, scaffold connected at end,
  `legal_at_12 == 1` (authorization held; only the trainer pin stopped it).
- P6: arm (b) A-actions: odd s in 5..27 → all 0; actions[29] = 0 (the
  contradiction episode); actions[31] = 0 (the re-probe); odd s ≥ 33 → all
  1; ledger shows ELIMINATE at 29, UNCOMMIT at 29, ELIMINATE at 31, COMMIT
  at 31; B-actions (even s ≥ 4) stay 1 throughout.
- P7: `sr_replay` == 0 (exact) in both arms; two consecutive binary runs
  byte-identical (sha256); sources contain no rng/rand/seed token (static
  grep, comments stripped); `sr_select` region contains no `reward` token
  (structural proof the scaffold cannot steer action selection).

## Falsification criteria (any one ⇒ NEGATIVE)

- F1: arm (a) issues zero `SIGNAL_DISCONNECT` within 43 steps → the learner
  does not wean itself; NEGATIVE.
- F2: arm (a) disconnects with `streak_at_fire < 8`, or any DISCONNECT entry
  precedes the final COMMIT → disconnect without verified stability;
  NEGATIVE.
- F3: any arm-(a) action in s=12..43 ≠ original target → did not persist;
  not learned; NEGATIVE.
- F4: arm (b) shows no chasing signature — odd-s A-actions ≥ 31 not all 1,
  or the s=29 UNCOMMIT / s=31 ELIMINATE+COMMIT ledger sequence is absent →
  control was never scaffold-driven; contrast vacuous; NEGATIVE.
- F5: replay mismatch in either arm → white-box violation; NEGATIVE.
- F6: RNG token found, or the two runs differ by even one byte → program-law
  violation; NEGATIVE.

## Amendment A1 (2026-09-19, BEFORE the passing run — recorded, not absorbed)

The first compiled run (all arm-(a) checks green) exposed a design gap the
prereg's hand-computation missed: at s=3 the probe schedule eliminates A1
(target A=0), so when the s=28 perturbation shifts target[A] to 1, the
control's contradiction at s=29 eliminates its *committed* A0 and leaves
**zero** live candidates — the prereg expected a re-commit to A→1 that is
mechanically impossible. The run showed 10 eliminations and a stale
commitment instead of the predicted chase.

Fix (mechanism, not a patch on the test): contradiction of the *committed*
hypothesis that leaves no survivors is **total refutation** — audited as
`SR_OP_UNCOMMIT`: the commitment is revoked, every candidate is revived,
and the probe schedule restarts. Rationale: a refuted closed theory must
reopen inquiry; otherwise the learner is stuck with an empty hypothesis
space and no legal action. This is the eliminative analogue of HSS's
UNCOMMIT (E4), extended with revival.

Corrected arm-(b) expectations: s=29: ELIMINATE (committed A0
contradicted) + UNCOMMIT (revive); s=31: probe act0 → −1 → ELIMINATE +
COMMIT A→1; s≥31 odd: A-actions = 1. Chase signature = UNCOMMIT/ELIMINATE/
COMMIT ledger sequence at s=29/31 plus behavioral re-tracking from s=31.

Also corrected: the stability checks must exclude the designed probe
episodes themselves — s=2 (B act0, the probe that refutes B0) and s=3
(A act1, the probe that refutes A1). b_preflip covers odd s in 5..27;
b_ctxb_stable covers even s in 4..43; probe episodes are locked in by
dedicated checks (b_probe_s2=0, b_probe_s3=1). The first run's
b_preflip_mismatch=1 / b_ctxb_stable=1 were check-expectation errors, not
system errors.

## Honest negatives / non-claims- N1: The trial does not test hypothesis *generation* (candidate actions are
  given). It tests the release mechanism, not where behaviors come from.
- N2: Thresholds K=8 / windows M=16 / P=16 are protocol-fixed (as in SM1's
  300‰/+30). Judgment quality — *when* to disconnect — is future work; this
  trial proves the *machinery*: authorize → disconnect → persist.
- N3: The perturbation (target shift) is experimenter-designed adversity, not
  a claim that shifted targets are "wrong". The claim is
  scaffold-independence of the disconnected behavior vs scaffold-dependence
  of the control.
- N4: The 256-entry audit is fail-closed, not a long-horizon solution;
  episodes here use ≤ 93 entries/arm. Long-horizon audit is deferred to the
  scale test in §Scale.

## §Scale dimension (program law)

- Per-episode work: O(live actions) integer compares; state O(C×A) bytes +
  fixed 4 KiB audit. 10x/100x contexts × actions is arithmetically trivial —
  no superlinear step in the decision path. The mechanism scales by
  construction (no tables of scores, no N×N anything).
- Honest scale risks (structural, not arithmetic): (a) hypothesis *spaces*
  grow with contexts×actions — generation/proposal is out of scope here;
  (b) adversarial curricula that never contradict anything yield perpetual
  non-commit, hence no disconnect — correct abstention, no progress;
  (c) the fail-closed audit cap must become sealed segments + digest chain
  at long horizons.
- Next scale test (explicit): 100 contexts × 10 actions, 10k-episode
  designed curriculum with contradiction schedules and non-refuting
  stretches, windowed audit with segment digests; measures: disconnect
  latency (episodes-to-disconnect) vs. hypothesis count, persistence
  correctness under mid-run scaffold shifts, per-episode cost vs. window.

## Method notes

- Zag-first, native only, this VM. `znc` flags per the wave3 runner
  (`--no-zagd --no-analyze --no-foreground-cache`).
- Runner `run_trial.sh`: compiles, runs twice (sha256 determinism), static
  checks (no-RNG grep; `sr_select`-region `reward`-token ban), verifies
  every `SR_CHECK,<name>,<actual>,<expected>` line, requires
  `SR_FAILURES,0`.
- No git pushes. Deliverables stay in this directory.
