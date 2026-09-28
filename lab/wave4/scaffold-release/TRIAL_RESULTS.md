# TRIAL_RESULTS — scaffold-release (SIGNAL_DISCONNECT)

**Date:** 2026-09-19. **Verdict: POSITIVE.** All preregistered positive
predictions P1–P7 hold; no falsification criterion F1–F6 triggered.
One preregistered amendment (A1) was recorded before the passing run.

## What was built

Native Zag on this VM (`sr.zag` substrate + `sr_trial.zag` harness, same
`znc` flags as wave3). A learner holds per-context candidate actions as
eliminative hypotheses; the ±1 scaffold signal is legal **only** as the
contradiction bit (never accumulated, never consulted by action selection —
structurally enforced: `sr_select` takes no signal parameter, verified by
static token scan). `SIGNAL_DISCONNECT` is a deliberate audited op,
authorized iff: channel live + every context committed + 8 consecutive
verified episodes with no contradiction. The learner's own step rule fires
it; the harness never does. Refusals (`SR_UNVERIFIED` pre-stability,
`SR_ALREADY` post-disconnect) are audited with no state change.

## Evidence (all from `evidence_run1.txt`, byte-identical rerun)

**Arm (a) DISCONNECT — the learner weaned itself:**
- Exactly one `DISCONNECT` entry, fired by the learner's own rule at s=12,
  with `streak_at_fire == 8` (P1 ✓). Final COMMIT was s=3 — disconnect
  came only after verified stability (F2 not triggered).
- Refusal path: s=5 probe → `SR_UNVERIFIED` (−360103); s=13 probe →
  `SR_ALREADY` (−360104); exactly 2 REFUSE entries, channel transitioned
  only at s=12 (P2 ✓).
- Persistence: all 32 post-disconnect actions (s=12..43) equal the original
  scaffold-phase targets, **through** the s=28 target shift — zero
  mismatches (P3 ✓). LEARNED = persisted after disconnect.
- Zero ELIMINATE/COMMIT events after s=3; scaffold reads post-disconnect
  all returned the −99 sentinel (P4 ✓).

**Arm (b) NEVER-DISCONNECT control — the chasing signature:**
- Zero DISCONNECT entries, channel live at end; `legal_at_12 == 1`
  (authorization held — the trainer pin was the *only* difference) (P5 ✓).
- s=29: scaffold contradicts the committed A0 → ELIMINATE + UNCOMMIT
  (total refutation reopens the question); s=31: re-probe → ELIMINATE +
  COMMIT A→1; odd-s A-actions: 0 through s=29, 1 from s=33 — the control
  re-tracked the shifted scaffold, driven by new ledger events (P6 ✓).
- B-actions stable at 1 throughout (chase was specific, not collapse).

**Program law:** replay reconstructs (live, committed, probe cursor,
connected) exactly in both arms (P7 ✓); two runs byte-identical
(sha256 `f1238db1…`); no rng/rand/seed token in any source; the
`sr_select` region contains no signal token. 40/40 checks, `SR_FAILURES,0`.

## The amendment (honest record)

The first compiled run exposed a real design gap, recorded as PREREG
Amendment A1 rather than absorbed: the prereg's hand-computation forgot
that s=3's probe eliminates A1, so the control could not re-commit to A→1
at s=29 (no live candidates). Fix: total refutation of the committed
hypothesis → audited UNCOMMIT that revives candidates and restarts the
probe schedule (the HSS-E4 analogue). The first run's two other mismatches
were check-expectation errors (probe episodes s=2/s=3 counted in stability
windows), corrected in the checks. Arm (a) was green before and after A1;
A1 changed only the control's predicted chase sequence, which then passed
as amended.

## Honest boundaries

- K=8/M=16/P=16 are protocol-fixed; the trial proves the release
  *machinery*, not that 8 is the right stability standard. Judgment
  quality (when to disconnect) is future work.
- Candidate actions are given, not generated — hypothesis generation is
  out of scope (same non-claim as HSS N2).
- The perturbation is experimenter-designed adversity; the claim is
  scaffold-independence of the disconnected behavior, not that shifted
  targets are "wrong".
- The 256-entry audit is fail-closed (≤ 96 entries/arm used), not a
  long-horizon solution; scale test specified in PREREG §Scale (100
  contexts × 10 actions, 10k designed episodes, segment digests,
  disconnect-latency vs. hypothesis-count).
- The reopen (UNCOMMIT+revive) rule was validated only via the control
  arm's chase; its interaction with *repeated* refutations (oscillation
  risk: world flapping A 0→1→0→…) is untested — a designed flapping
  curriculum is the obvious next probe.

## Verdict rationale

POSITIVE because every preregistered prediction held on a byte-identical
native build: the learner disconnected on its own under its own
authorization rule, refused prematurely, persisted through perturbation,
and the pinned control chased the scaffold with scaffold-driven ledger
events. The mechanism — reward as contradiction-evidence, disconnect as a
deliberate audited op, learned = persists after disconnect — works as
specified.
