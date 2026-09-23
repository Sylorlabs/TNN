# TRIGGER_DESIGN — the EDUCATED-GUESS context switch (HT2)

Agent (Wave-3, learner-driven-switching), 2026-09-19.
Status: DESIGN — preregistered in PREREG_HT2.md before any run.

## 0. What HT1 left open (the exact gap)

HT1 proved the *mechanism*: `CTX_SWITCH` as a deliberate, verified,
refusable op with intrinsic corroboration, no score table anywhere.
But the *policy* driving it was protocol-fixed in the harness: probe the
active partition every episode; on one majority-negative batch, probe all
alternatives and switch in the same episode; propose the alternate label
(`1 - label`) if nothing verifies. The learner never decided *when* to
probe, *when* to doubt, or *what* to guess. Its probe/switch timing was a
fixed stimulus–response protocol — exactly what this investigation
replaces.

HT2 keeps the HT1 mechanism **byte-identical** (`ctx_core.zag` is copied
with a sha256 fidelity check in the runner; the corroboration rule,
refusal paths, and audit invariants are not re-proven, they are reused).
What is under test is the **trigger**: the learner's own decision logic
for doubt → verification → falsification → educated guess → switch.

## 1. The shape: hypothesis, contradiction, deliberate test, falsification

The learner holds an **explicit hypothesis** about the active partition:

> **H**: "Partition P (declared label L) explains current observations."
> Prediction content of H: observations agree with L — by majority.

A **reason to doubt** is a *recorded contradiction* of that prediction —
not a low reward, not a threshold crossing. The full trigger shape:

1. **Perception (world-driven, always on).** Each episode the world
   presents 8 passive observation bits: does the current regime match the
   active partition's declared label? (Adversarial noise: 15% flips on
   the randomized curriculum; designed lies on the adversarial
   curriculum.) The learner *records* them. Recording is perception, not
   a decision — the learner does not choose the episode rate.
2. **Contradiction (evidence-driven).** If the episode's 8 bits show
   majority-disagree (agree ≤ 3), the recorded evidence *contradicts* H's
   prediction. The learner raises **doubt** — an epistemic state, not an
   action. Nothing switches. Nothing is even re-probed yet.
3. **Deliberate verification (learner-issued test).** Because of the
   contradiction — not because of a schedule — the learner issues a
   16-probe batch *as a test of H specifically* ("if H is true, this batch
   comes back majority-positive"). This is the step HT1's protocol
   skipped: HT1 never re-tested the active hypothesis; it went straight
   to the alternatives.
4. **Explanation or falsification (logic, not counting).**
   - Verification confirms H (majority-positive) → the contradiction is
     **explained** as noise; H stands, re-committed. The learner
     *withholds* commitment-change under doubt — the observable
     signature of non-reflex intelligence, and the thing tables cannot do
     (POST_TABLE.md §1a).
   - Verification contradicts H (majority-negative) → H is **falsified**
     by two *independent* contradicting observations. Only now does the
     learner consider switching.
   - Verification ties (8/16) → **inconclusive**: re-test once; a second
     tie is treated as explained (withhold falsification on inconclusive
     evidence — the conservative choice).
5. **Educated guess (hypothesis-driven, tested before commitment).** With
   H falsified, the learner tests *alternative hypotheses*, in a
   deliberate order:
   - First, every other live partition, each probed fresh as a test of
     "regime = label[Q]". The first that verifies is switch-candidate.
   - Only if none verifies: **propose a new partition** with the smallest
     non-negative label not currently live — the next *unfalsified*
     candidate. This is the educated guess: it is not random (it excludes
     live hypotheses, which were tested first) and it is not a schedule
     (it is issued because every known hypothesis failed its test).
   - Each guess is **probed and recorded before any switch is attempted**;
     a guess that does not verify is falsified by its own test and never
     commits (the corroboration rule refuses it structurally).
   - One novel guess per doubt episode. If it fails, the rational move is
     not blind enumeration but **re-examining the falsification**:
     re-verify the original hypothesis with a fresh probe. If it
     confirms → the falsification is **overturned** (the verification
     batch was the outlier); H re-committed, zero switches. If it
     contradicts again → back off until fresh passive evidence arrives
     (the investigation is world-driven, so it terminates; it never spins
     on its own).
6. **Switch (deliberate op, HT1's corroboration).** `CTX_SWITCH` commits
   only with target majority-positive AND old-active majority-negative
   recorded evidence — satisfied *by construction* of the falsification
   path, and re-checked by `ctx_switch_verified_scan`.

## 2. What "reason to doubt" is (the key question, answered)

> A reason to doubt is a **recorded observation that contradicts the
> active hypothesis's explicit prediction**, escalated to falsification
> only when a **deliberately issued verification probe — designed by the
> learner as a test of that specific hypothesis — independently
> contradicts it too.**

Why this is logic, not a reward threshold — stated precisely, because the
distinction is the whole investigation:

- **No scalar is accumulated, compared, or maximized anywhere.** There is
  no value, no score, no `+=`, no argmax, no reward signal in the
  learner's path (the probes report *agreement bits*, not rewards).
- The numbers that do appear (majority, 8 passive bits, 16 probe batch,
  two independent contradictions) express **the hypothesis's prediction
  content** ("explains observations" *means* observations mostly agree)
  and the **independence requirement** for falsification (one
  contradiction raises the question; a second, deliberately sought one
  answers it). They are not cutoffs on a value being optimized.
- The verification probe is **learner-issued as a test**, not passively
  received. A threshold *reacts* to a sample; a test *asks a question*.
  The observable difference: when the test confirms H, the learner
  **explains the contradiction as noise and stands by H**. A
  threshold/reflex system has no "explain away" move — it can only
  switch or count down.
- Falsification is **defeasible**: a falsified hypothesis can be
  re-tested and its falsification overturned when all alternatives fail.
  Thresholds don't overturn; they re-trigger.

Honest boundary: "two independent contradictions" contains the number 2.
What makes it logical rather than threshold-shaped is *what is being
counted* (contradictions of an explicit prediction, the second one
deliberately sought as a test) and *what happens on each count* (doubt
is an epistemic state that withholds action; only falsification licenses
investigation; only verification licenses commitment). The count is in
the *evidence structure*, not in a *value comparison*.

## 3. The perception/investigation split (why probe timing is learner-driven)

The ban covers timers and fixed schedules **as triggers**. The design
separates two things HT1 conflated:

- **Perception** — the world's 8-bit passive stream each episode. The
  learner records it (audited) but takes no investigative action on a
  schedule. The episode rate is the *world's* heartbeat (the curriculum
  advances in episodes); it is not the learner's trigger.
- **Investigation** — 16-probe batches, issued by the learner **only**
  to resolve a recorded contradiction (verification), to test a specific
  alternative hypothesis, to test a novel guess, or to re-examine a
  falsification. In steady state the learner issues **zero** probe
  batches: it perceives, it acts on its committed hypothesis, it does not
  experiment on a schedule.

Checkable properties (all enforced in the trial):
- The learner's decision functions take **(hypothesis state, recorded
  evidence)** only — no clock, no episode counter, no RNG. Static
  checks in `run_ht2.sh` grep `ht2_learner.zag` for
  `rng|episode|clock` and require zero hits.
- Every learner-issued probe and every switch attempt is audited in the
  learner's decision ledger **with its evidential reason**, and
  `ht2_causal_check` proves the causal chain: no DOUBT without a
  recorded contradiction, no FALSIFIED without a contradicting
  verification, no SWITCH without a falsification plus a verified
  alternative. A schedule-driven action would appear as a ledger entry
  with no evidential predecessor — the check fails the trial if one
  exists.

## 4. The educated guess, precisely

"Educated" is doing three specific pieces of work:

1. **Test the known before inventing the new.** Live partitions are
   existing, previously-corroborated hypotheses; each is *tested fresh*
   (not assumed from stale evidence) before any novel label is proposed.
2. **Guess from the unfalsified set.** The novel label is the smallest
   non-negative integer not currently live — deterministic, excluding
   hypotheses already under test. It is a genuine guess (no positive
   evidence for it), and that is why it is *tested before commitment*:
   probe → record → switch only if verified.
3. **A wrong guess is falsified by its own test.** It costs a probe
   batch, never a commitment — the corroboration rule refuses the
   switch structurally. The ledger then shows
   `DOUBT → FALSIFIED → TEST_ALT → GUESS → GUESS_FALSIFIED → OVERTURN`,
   the white-box trace of doubt that never became commitment.

What the guess is *not*: random (no RNG in the learner — attested §6),
scheduled (issued only when every known hypothesis failed its test), or
a reward-maximizing choice (there is no reward and no value function).

## 5. Scale dimension (program law: scaling is allowed; toy mechanisms are not)

The trial is small-scale (4 partitions, 2 regimes, 48+16 episodes — sized
for head-to-head comparability with HT1). The design's scaling argument:

- **Decision cost is O(partitions) per doubt episode**, O(1) per episode
  in steady state (zero probe batches when committed — investigative cost
  is driven by *world adversity*, not by time). Nothing is indexed by
  regime count; there are no N×N structures to blow up.
- **No accumulators, no drift.** Evidence windows are fixed-size records
  replaced wholesale; the bad-streak is a bounded mechanism counter the
  HT2 policy does not even read. Nothing grows with horizon except the
  audit ledgers.
- **Ledger growth is O(doubt episodes + episodes).** Per-episode
  observation records are the linear term. Fixed caps (256/256) are
  *engineering*, sized for the trial — the mechanism does not depend on
  them.
- **Deterministic given state** (§6): behavior at any scale is
  reproducible; scale tests are meaningful because reruns are identical.

What does *not* yet scale (honest): 4-slot pressure over long horizons
(partitions are never killed in HT1/HT2 — unification with MA slots and
the deliberate KILL op is the designed path, cf. CTX_DESIGN.md §6);
per-episode observation records make the learner ledger O(episodes)
(the designed path is a ring ledger for observations plus a commitment
ledger for decisions).

**Next scale test (explicit, named): HT2-SCALE** — 16 partitions,
4 regimes, 480-episode designed curriculum with slot-pressure events
(forced PROPOSE beyond cap → exercises KILL/backoff), ledger caps ×20,
plus the ring-ledger observation design. It is *not* run here; it is the
named next step if HT2 passes.

## 6. No randomness in the AI (program-law attestation)

- **The learner** (all of `ht2_learner.zag`): zero RNG. No random
  exploration, no random tie-breaks (alternative scan is lowest-slot
  order; guess labels are smallest-unfalsified), no stochastic policy,
  no seeded RNG. Deterministic function of (hypothesis state, recorded
  evidence). Attested by design (decision signatures carry no RNG),
  by static check (runner greps, must be empty), and by runtime proof
  (two full runs byte-identical).
- **The world** (harness, not the AI): two curricula.
  - **R (randomized):** seeded LCG flip sequence (identical to HT1's —
    same seed, same generator, so the 10 true flips land on the same
    episodes) and seeded 15% channel noise. Seeded RNG here is
    *scaffolding for Micah's acceptance test* ("randomized switching
    curriculum must not fail"), explicitly labeled as such — never part
    of the system.
  - **A (adversarial, preferred):** fully *designed* — explicit flip
    positions, explicit noise placement with named adversarial intents
    (isolated lies, pre-flip burst, post-flip masking, forced noisy
    verification). Zero RNG. This is the stronger test per program law:
    adversity as designed curriculum.
- **Verdict discipline:** the report distinguishes "the system is
  deterministic" (byte-identical reruns, no RNG in the learner) from
  "the test was adversarial" (curriculum A's designed attacks).

Prereg amendment record (2026-09-19, program-law update, *before any
run*): the HT2 learner design never contained RNG in its decision path
(HT1's CTX learner was already RNG-free); no removal was needed. The
change vs the original brief is on the *world* side: the primary test
is now the fully-designed adversarial curriculum A, with the seeded
randomized curriculum R retained as scaffolding for the acceptance test
and the HT1 head-to-head. No trial has run under the old plan; nothing
is silently rerun.

## 7. What HT2 does NOT show (honest boundaries)

- The learner does not choose *what the world presents* (the 8-bit
  passive rate is a curriculum parameter) — it chooses *what to
  investigate and when*.
- Alternative scan order is lowest-slot-first (deliberate simplification;
  evidence-ranked ordering is future work — correctness does not depend
  on order since every alternative is tested).
- Partitions are never killed (slot pressure untested here; the MA-KILL
  unification is the designed path — see §5).
- Two regimes in the trial (the mechanism is regime-count-agnostic;
  HT2-SCALE tests 4).
- BACKOFF (all-tests-fail incl. overturn) is implemented as the safety
  path but is unreachable at 15% noise; it is unit-tested with forced
  adversarial batches, not curriculum-tested.
