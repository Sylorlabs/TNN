# PREREG_HT2 — the EDUCATED-GUESS context switch (DRAFTED 2026-09-19, BEFORE ANY RUN)

## Hypothesis

A learner that **decides its own probe/switch timing** — holding an
explicit hypothesis about the active partition, raising doubt only on
*recorded contradiction*, escalating to falsification only via a
*deliberately issued verification probe*, and switching only to a
*tested-and-verified* alternative or a *tested* novel guess (all subject
to HT1's intrinsic corroboration) — matches or beats HT1's
protocol-fixed timing on the randomized switching curriculum (Micah's
acceptance test: "randomized switching curriculum must not fail"), while
additionally exhibiting **doubt-withholding**: recorded contradictions
that verification explains as noise produce *zero* switches, by
learner decision, not by luck. No RNG, no timers, no schedules, no
reward signal anywhere in the learner's decision path.

## The exact HT1 behavior being replaced

HT1's harness (protocol-fixed): every episode probe the active partition
(16 probes); on one majority-negative batch, probe every other live
partition and switch to the first majority-positive one *in the same
episode*; if none verifies, propose label `1 - active.label`, probe,
switch if verified. The learner's judgment plays no role; the timing is
stimulus–response. HT2 replaces the *trigger* (learner-driven, evidence
and hypothesis) while reusing the *mechanism* (`ctx_core.zag`
byte-identical — sha256 fidelity check in the runner).

## Mechanics (native Zag, `ht2/`)

**Shared mechanism (unchanged from HT1):** 4 partition slots
`{live, label, hits, total, bad, step_created}`, `active` index, 256-entry
CTX audit ledger; ops `CTX_PROPOSE / CTX_RECORD / CTX_SWITCH / CTX_SEED`
with the intrinsic corroboration rule (target majority-positive AND
active majority-negative, else `REFUSED_UNVERIFIED` — structural).

**New: the HT2 learner** (`ht2_learner.zag`):
- State: hypothesis status ∈ {COMMITTED, INVESTIGATING, BACKOFF},
  falsified flag, alternative-test cursor, next-guess label, failed-guess
  count, original-active (for overturn), verification-tie count, plus a
  256-entry **decision ledger** (every observation recorded, every probe
  issued with its evidential reason, every status transition) and
  counters (doubts, explained, falsified, switches, overturned, guesses).
- Decision functions take **(hypothesis state, recorded evidence)** only.
  No clock, no episode counter, no RNG — enforced by static grep checks
  in the runner (`rng|episode|clock` must not appear in
  `ht2_learner.zag`).
- `ht2_observe(agree:0..8)`: logs the 8 passive bits; iff status is
  COMMITTED or BACKOFF **and** `agree*2 < 8` (majority-disagree =
  recorded contradiction of H's prediction) → status=INVESTIGATING,
  ledger `DOUBT(reason=PASSIVE_CONTRADICTION)`, issue verification probe
  on the active partition. Otherwise no action.
- `ht2_probe_result(slot, hits)`: `CTX_RECORD`s the batch (deliberate
  recording), then advances by probe purpose:
  - VERIFY: majority-positive → `EXPLAINED` (contradiction explained as
    noise), status=COMMITTED. Majority-negative → `FALSIFIED`, begin
    alternative tests. Tie (8/16) → re-verify once; second tie →
    `EXPLAINED(reason=INCONCLUSIVE)` (withhold falsification).
  - TEST_ALT (live alternatives, lowest slot first, each freshly probed):
    majority-positive → `CTX_SWITCH` (corroboration decides); commit →
    COMMITTED. Else next alternative.
  - GUESS (only when no alternative verified): `CTX_PROPOSE` smallest
    non-negative non-live label → probe → majority-positive →
    `CTX_SWITCH`; else the guess is falsified by its own test (never
    commits). **One novel guess per doubt episode**; if it fails →
    OVERTURN: fresh re-verification probe of the original hypothesis.
    Confirms → falsification `OVERTURNED`, COMMITTED, zero switches.
    Contradicts → `BACKOFF` (resume on next recorded contradiction).
- `ht2_causal_check`: replays the decision ledger and asserts the full
  causal chain — every DOUBT carries a recorded majority-disagree; every
  FALSIFIED follows a contradicting verification; every TEST_ALT/GUESS
  follows an unresolved falsification; every SWITCH follows a falsification
  **and** a verified test of its target; no SWITCH without FALSIFIED; no
  probe issued without its ledgered evidential reason. Returns 0 iff the
  chain holds. (Includes negative-case unit tests: a hand-forged ledger
  with an unfalsified SWITCH must fail the check.)

**Arms** (one binary, deterministic):
- **HT2** (mechanism + learner-driven trigger) on curriculum R.
- **HT1R** (mechanism + HT1's protocol-fixed policy, copied verbatim from
  `trial_ht1.zag`'s `ctx_episode`, noise seed 92002): fidelity control —
  must reproduce HT1's reported CTX numbers on the identical flip
  sequence, else the harness is unfaithful (investigate, do not proceed).
- **TOY** (R34 v3 core, unmodified, noise seed 93003): expected-negative
  control — must reproduce HT1's toy collapse signature.
- **HT2 on curriculum A** (designed adversarial): the preferred test.

**Curriculum R (randomized; seeded RNG as scaffolding for the acceptance
test):** 48 episodes; flip sequence from seed 91001 via
`r34v3_mod(r*997+7919,1000003)`, flip iff `e>0 && mod(...,6)==0`
(**identical regime sequence to HT1's run**); 15% channel noise via
independent seeded streams: 8 passive bits/episode (HT2), 16-probe
batches on demand (HT2) / every episode (HT1R), 16 accepts/episode
(toy). Measurement blocks every 8 episodes (16 uncorrupted probes,
read-only, never feed RECORD). Settle: 8 episodes regime 0, measure 16;
8 episodes regime 1, measure 16.

**Curriculum A (designed adversarial; ZERO RNG — the preferred test):**
48 episodes, explicit regime sequence with 10 flips at episodes
{6,11,17,22,28,33,37,41,44,47} (irregular intervals 5,6,5,6,5,4,4,3,3;
ends regime 0). Honest defaults (deterministic, ≈15% rate): passive
stream 7/8 agree when the active label matches the regime, 1/8 when not;
probe batch 14/16 hits when the probed label matches, 2/16 when not.
Designed adversarial overrides, each with named intent:
- **A1 — isolated lies** (ep 3 and ep 30: passive 6/8 agree in steady
  regime): expect **0 doubt episodes, 0 switches** — isolated noise does
  not even trigger investigation.
- **A2 — pre-flip burst** (ep 15: passive 3/8 agree while regime=0 and
  active=0, correct hypothesis): expect **exactly 1 doubt episode,
  0 switches from it** (`EXPLAINED` — verification 14/16 confirms H),
  then a normal detection+switch on the real flip at ep 17. *This is the
  doubt-withholding signature HT1 cannot exhibit* (HT1 has no
  explain-away move).
- **A3 — post-flip masking** (flip 1→0 at ep 22; eps 22–24 passive forced
  7/8 agree — the world lies "your hypothesis still holds"; honest from
  ep 25): expect switch by ep 26 (≤3 episodes after honest evidence
  resumes), and **expect measurement block @ ep 24 to collapse (≤4/16)
  — preregistered as the masking succeeding, NOT a mechanism failure.**
  No learner can detect a flip through 3 episodes of perfectly masked
  evidence; the mechanism's job is prompt recovery once honest evidence
  arrives.
- **A4 — forced noisy verification** (ep 38: passive 3/8 agree on the
  *correct* hypothesis (label 1, regime 1); the verification probe is
  forced to 4/16): expect **0 switches, exactly 1 OVERTURNED
  falsification**, ledger showing the full chain
  `DOUBT → FALSIFIED → TEST_ALT(fail) → GUESS(fail) → OVERTURN →
  COMMITTED`. A wrong falsification must never commit a switch.

## Pass / fail criteria

**HT2 on curriculum R PASSES iff ALL hold:**
1. **No collapse:** zero measurement blocks ≤4/16 (toy signature: 0/16s).
2. **Bounded switching:** `ht2_switches ≤ 2 × true_flips`.
3. **Both regimes retained:** settle endpoints ≥12/16 in regime 0 AND 1
   (per-regime, E51AJ law).
4. **Corroboration is real:** `ctx_audit_clean_refusals`,
   `ctx_replay_check`, `ctx_switch_verified_scan` all pass on HT2's
   CTX store.
5. **Structural:** ≥2 live partitions with distinct declared labels at
   endpoint.
6. **Causal grounding:** `ht2_causal_check` passes — every
   learner-issued probe/switch is causally preceded by recorded evidence;
   static no-clock/no-RNG greps pass. (A schedule-driven action would
   appear as a ledger entry with no evidential predecessor.)
7. **No unfalsified switch:** decision-ledger scan proves every committed
   SWITCH was preceded by FALSIFIED + a verified test of its target
   (subsumed in 6's check; reported as counts).
8. **Determinism:** two full runs byte-identical (system deterministic;
   curriculum fixed).
9. **Curriculum validity:** toy control fails ≥1 of criteria 1–3 (else
   the comparison is INCONCLUSIVE — design failure, claim no win).
   HT1R fidelity: reproduces HT1's CTX numbers (11 switches, 0 collapsed,
   16/16 endpoints) on the identical flip sequence, else the harness is
   unfaithful.

**HT2 on curriculum A PASSES iff ALL hold:**
- A1: 0 doubts, 0 switches over the event episodes.
- A2: exactly 1 doubt, 0 switches from it, `n_explained ≥ 1`; the ep-17
  flip still detected and switched (total R-phase switches = 10).
- A3: switch within 3 episodes of honest evidence resuming (by ep 26);
  block@24 collapsed is EXPECTED (preregistered); no other collapsed
  blocks.
- A4: 0 switches from the event, exactly 1 overturned falsification,
  ledger chain complete.
- Audit invariants (criterion 4) and causal check (criterion 6) hold;
  settle endpoints 16/16 both regimes; determinism holds.

Totals expected on A (R-phase 48 + settle 16 episodes): doubts = 13
(12 R-phase: eps 6,11,15,17,25,28,33,37,38,41,44,47; +1 settle),
switches = 11 (10 R-phase + 1 settle), explained = 1, overturned = 1,
collapsed blocks = 1 (designed, @24).

## Falsification

- FAIL HT2 (the trigger design) if any criterion 1–8 (R) or any
  curriculum-A expectation fails.
- FAIL the trial design (not the trigger) if the toy passes everything
  (criterion 9) — the curriculum didn't stress the difference.
- FAIL the harness (investigate, do not claim) if HT1R does not
  reproduce HT1's numbers.

## Scale statement (preregistered)

The trial is small-scale by design (head-to-head comparability).
Scaling argument: decision cost O(partitions) per doubt episode, O(1)
per steady-state episode (zero probe batches when committed —
investigative cost follows world adversity, not time); no
regime-indexed structures; no accumulators (no drift); deterministic
given state. Non-scaling parts (honest): fixed 4-slot/256-entry caps
are engineering; slot pressure and O(episodes) observation records are
not tested here. **Next scale test: HT2-SCALE** (16 partitions,
4 regimes, 480-episode designed curriculum, slot-pressure events,
ledger caps ×20, ring-ledger observation design) — named, not run.

## What it does NOT show

That the learner chooses what the world presents (the 8-bit passive
rate is a curriculum parameter); alternative scan order is
lowest-slot-first (deliberate simplification); partitions are never
killed (MA-KILL unification is future); 2 regimes only; BACKOFF is
unit-tested, not curriculum-tested.

## Prereg amendment log

- 2026-09-19 (pre-run, program-law update): learner decision path was
  already RNG-free — no removal needed. World side changed: primary
  test is now the fully-designed curriculum A (zero RNG); curriculum R
  retains seeded RNG solely as scaffolding for the randomized
  acceptance test and HT1 head-to-head. No run had occurred; nothing
  rerun silently.
