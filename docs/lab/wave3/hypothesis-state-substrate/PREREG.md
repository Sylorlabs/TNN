# PREREG — hypothesis-state-substrate trial

**Status: preregistered 2026-09-19, BEFORE any run.** No trial binary has been
compiled or executed at the time of writing. Any deviation will be recorded as
an amendment, not silently absorbed.

**Program-law amendments incorporated (Micah, 2026-09-19):**
- A1 (scale allowed): §7 states the scale dimension, the scaling argument, and
  the explicit next scale test.
- A2/A3 (no RNG in the system): the substrate, the world, and the harness
  contain no RNG — no LCG, no random tie-breaks, no stochastic policies, no
  seeded RNG in the harness either. The "world" is five explicitly-designed
  deterministic curricula. The verdict will distinguish "the system is
  deterministic" (byte-identical reruns + static no-RNG grep) from "the test
  was adversarial" (curricula E1–E5 are designed to contradict/refute).

## Hypothesis

H1: A system that holds multiple competing hypotheses explicitly, refutes
them by direct logical contradiction of their defining claims, and commits
iff exactly one survivor remains, behaves observably differently from
argmax-over-scores — specifically, it commits to a low-support survivor
over a high-support refuted hypothesis, and it holds (rather than commits)
under genuine non-uniqueness.

H0 (null): the eliminative machinery is argmax over scores with extra steps —
commit behavior is a pure function of the final confirmation-counter vector.

## Design

Substrate `hss.zag` (native Zag, Linux x86-64, `znc 2026.07.0-dev`):
- 8 hypothesis slots. Each: active flag (u8), defining-claim bitmask (u32,
  bit i = "observation i must be 1"), confirmation counter (u32, audit-only).
- `hss_observe(index, bit)`: per active slot — claim=1 & obs=0 → REFUTE
  (deactivate + audit); claim=1 & obs=1 → confirm (counter++, audit);
  claim=0 → consistent (audit). Refuting the committed slot → UNCOMMIT audit.
- `hss_activate(slot, sig)`: `sig == 0` → `HSS_VACUOUS` refusal + audit
  (unfalsifiable hypotheses are not hypotheses — logic gate, no threshold).
- `hss_commit()`: commit iff exactly one active slot; else HOLD with the
  active count in the audit entry. Revokes commitment if a rival appears.
- Audit: 64-entry op log (step, op, slot+1, aux); append fails closed with
  `HSS_AUDIT_FULL` — the op is not applied.
- Falsification control `hss_argmax` (harness-only, never substrate): lowest
  slot with the highest confirmation counter, ignoring refutation state.

Curricula (deterministic, designed — no RNG):
- **E1 discriminator.** A=slot0 sig1111, B=slot1 sig0001, C=slot2 sig1100.
  obs(0,1), obs(1,1), obs(0,1) [second reading], obs(2,0).
  Expected: A refuted (despite 3 confirmations, the most), C refuted, B
  survives with 2 → COMMIT B. Argmax control picks A (counter 3 > 2).
- **E2 non-uniqueness hold.** D=slot3, E=slot4, both sig1000. obs(3,1)
  confirms both. Expected: HOLD, active_count=2, no commit. Argmax would
  commit D. (Tests that the system does not commit on argmax, and that
  abstention comes from non-uniqueness, not a threshold.)
- **E3 total refutation.** F=slot5 sig0001, G=slot6 sig0010. obs(0,0) refutes
  F; obs(1,0) refutes G. Expected: HOLD, active_count=0, committed=-1, no crash.
- **E4 revocable commitment.** I=slot7 sig0010. obs(0,1) consistent → COMMIT I
  (sole active). obs(1,0) contradicts → REFUTE + UNCOMMIT. Expected: one
  COMMIT then one UNCOMMIT, final committed=-1. (Commitment is not a sticky
  threshold crossing.)
- **E5 vacuous refusal.** Activate slot0 sig=0 → expect `HSS_VACUOUS`
  (−350103), slot stays inactive, one REFUSE audit entry; a subsequent valid
  activation (sig=1) succeeds, proving the gate is specific.

## Positive predictions (all must hold for POSITIVE)

- P1: E1 ends with exactly one COMMIT audit entry, committed slot = 1 (B),
  and the argmax control returns 0 (A) → recorded DISAGREE=1.
- P2: E2 ends with zero COMMITs; final audit op is HOLD with aux=2;
  argmax returns 3 while the substrate holds → DISAGREE=1.
- P3: E3 ends with zero COMMITs, committed=-1, no crash on the empty set.
- P4: E4 shows COMMIT then UNCOMMIT (one of each in the audit), final
  committed=-1.
- P5: E5 returns `HSS_VACUOUS`, leaves the slot inactive, logs REFUSE; the
  follow-up valid activation succeeds.
- P6: two consecutive binary runs are byte-identical (sha256); the sources
  contain no rng/rand/seed token (static grep); the commit region contains no
  reference to the confirmation counters (static token check) — the system is
  deterministic *and* the commit rule is structurally independent of scores.
- P7: every audit REFUTE/COMMIT entry carries (slot, observation index) —
  never a score delta or margin — verified by reading the E1 audit dump.

## Falsification criteria (any one triggers NEGATIVE or MIXED)

- F1: E1 commits to slot 0 (the highest-counter hypothesis) or fails to
  refute A → the eliminative rule is not operating. NEGATIVE.
- F2: any commit/deactivate decision in the run trace depends on comparing a
  counter/score against a researcher-chosen constant → threshold-based design.
  NEGATIVE. (Checked by the commit-region static token scan + audit review.)
- F3: the substrate's commit behavior is a pure function of the final
  counter vector — i.e., no discriminator episode can be constructed where it
  disagrees with argmax. E1/E2 are constructed to disagree; if the
  disagreement fails to materialize for a mechanistic reason (not a bug),
  the design is argmax-with-extra-steps. NEGATIVE.
- F4: the audit shows confirmation counters influencing any refutation
  (e.g. a weakest-link removal) → scores decide. NEGATIVE.

## What would show "just argmax with extra steps" (the key design question)

Three independent tripwires: (1) behavioral — E1/E2 disagreement with the
argmax control fails to appear; (2) structural — the commit region references
score/counter state (static check); (3) evidential — audit entries justify a
decision with a numeric comparison rather than a (slot, claim, observation)
contradiction triple. Passing all three is the positive bar.

## Honest negatives / non-claims (first-class)

- N1: If P6's static check fails (a counter leaks into the commit region),
  the verdict is NEGATIVE even if behavior looks right — structure first.
- N2: The trial does not test hypothesis *generation* (who proposes new
  slots). A committed-then-everything-refuted system has no recovery path
  except external re-activation; that is out of scope and stated, not hidden.
- N3: The audit cap (64) is fail-closed, not a long-horizon solution; the
  trial's episodes use ≤ 20 entries. Long-horizon audit behavior is deferred
  to the scale test in §7, not claimed here.
- N4: Confirmation counters are deliberately score-like in *appearance*.
  The claim is not "no numbers exist" but "numbers do not decide" — P6/F2
  are the teeth. If a reviewer finds a decision path through the counters,
  that is a NEGATIVE finding, not a wording dispute.

## §7 Scale dimension (program law A1)

- **Scaling argument.** Per-observation work is O(active slots) integer
  compares; per-commit work is one O(capacity) scan; state is 16 bytes/slot
  plus a fixed 1 KiB audit. 10x/100x slot counts (80/800) are arithmetically
  trivial — no superlinear step exists in the decision path. The binding
  constraints at scale are structural: (a) hypothesis generation (out of
  scope — proposed next step: wire slot proposals to the
  native-structural-revision workstream's PROMOTE proposals); (b)
  adversarial curricula that never contradict anything yield perpetual HOLD,
  which is the *correct* abstention but no progress; (c) the 64-entry audit
  fails closed on long horizons.
- **Next scale test (explicit).** 1000 slots, 100k-observation adversarial
  curricula (designed contradiction schedules + designed non-refuting
  stretches), audit with sealed segments + digest chain instead of
  fail-closed cap; measures: HOLD correctness under non-refuting stretches,
  commit latency (observations-to-commit) vs. slot count, audit segment
  integrity. Not run here — the current trial is the mechanism proof.
- **What scale would falsify.** If commit latency grows superlinearly with
  slot count, or if HOLD-under-ambiguity degrades into spurious commits as
  slots increase, the "scales" claim dies.

## Method notes

- Zag-first, native only, this VM. `znc` flags per ZAG_PLAYBOOK.md.
- `znc check` on the v1 source first (type-soundness evidence for the analysis).
- Runner `run_trial.sh`: compiles, runs twice (sha256 determinism), runs the
  static checks (no-RNG grep; commit-region token allowlist), verifies every
  `HSS_CHECK,<name>,<actual>,<expected>` line, requires `HSS_FAILURES,0`.
- No git pushes. Deliverables stay in this directory.
