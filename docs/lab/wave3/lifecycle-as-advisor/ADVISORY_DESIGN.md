# Advisory interface design — lifecycle estimator as advisor to deliberate memory agency

**Companion to:** `PREREG.md` (falsification criteria), `trial/` (native
implementation). This document is the interface contract: what the advisor
is, what it is not, and the structural reasons it cannot become the decider.

## 1. The problem it solves

MA3 (`wave2/memoryagency/TRIAL_RESULTS_MA3.md`) showed the two available
mechanisms have complementary strengths and complementary failure modes:

- **Deliberate agency** (protect-while-uncertain, declared values) never
  evicts blindly — 30 vs 0 on the standard curriculum — but with
  non-negative trust it cannot express negative evidence and seals shut
  under traps (11 admitted vs AUTO's 72 on adversarial).
- **Lifecycle estimator** (bounded-linear future-use, delayed credit) learns
  signed weights and keeps churning under traps — but its first evictions
  are blind, and in the AUTO arm the estimator *decides*: eviction is a
  direct function of predicted future-use with no deliberate check. That is
  the catastrophic failure the ANTI-RL clause rules out: a substrate
  deciding.

The advisory interface keeps the estimator's signed, learned signal and the
agency's deliberate protection, joined at a joint the estimator cannot
cross on its own.

## 2. The interface, precisely

### 2.1 The advisor (substrate side)

`adv_advisor.zag` — pure integer module, **zero imports**:

- State: `AdvState { w: []u8 (8×i32 LE), bias: i32 }` — the lifecycle-v1
  bounded-linear predictor, integer port (proven lineage: MA3's `auto_*`).
- `adv_score(as, feats, base) → 0..100`: `clamp01(50 + 25·z)`, `z` in 1/256
  units. A prediction, not a value judgment.
- `adv_suggest(as, feats, base) → signed i32`: `a = (score−50)·2`
  ∈ [−100,100]; `|a| < 10` → `0` (no opinion). **Signed is load-bearing**:
  negative advice means "this pattern predicts *unimportance*" — the exact
  expressive gap MA3 identified in the agency policy. The suggestion carries
  a direction and a strength, never an instruction.
- `adv_credit(as, feats, base, truth)`: delayed full-information delta
  credit, `w += lr·err·g·x` with saturation-aware gain (the v1 rule).
  Substrate learning from verified outcomes — the same legitimacy as the
  curiosity substrate's EMAs. No reward flows into the learner's
  declared-value path.

**What the advisor cannot do:** it receives feature bytes and returns a
number. It has no store pointer, no slot ids, no op handles, and names no
memory machinery. The runner's static check (`grep -E '@import|MaStore|ma_'`
on `adv_advisor.zag` must be empty) enforces this the way the R34 runner
enforces learner-core isolation. Eviction-by-estimator is impossible at the
type level: there is no expression in the advisor's language that denotes a
slot.

### 2.2 The advice record (the joint)

New audited op `MA_OP_ADVISE = 9`, recorded by `ma_advise_record`:

```
(slot, advice_signed, strength, accepted∈{0,1}, decision_code, w_before, w_after)
```

- **Non-mutating**: before/after snapshots are untouched (the replay check
  special-cases it like `MA_OP_SETSTAGE`; rollback skips it). It is a
  record of deliberation, not a state change.
- **Every accept/reject is one of these.** There is no other way for advice
  to enter the ledger. "Why did you kill this?" always has a complete
  answer: the advice value, whether it was followed, and the policy's
  declared weight at the time.
- Decision codes: `1` = KILL_ADMIT (pressure kill), `2` = ADMIT_REFUSED
  (incoming dropped at the gate), `3` = WCAL (advisory-weight calibration
  on delayed revelation).

### 2.3 The gated kill (op-implementation guarantee)

`ma_kill_advised(s, slot, tok)`:

- Runs the full `ma_kill` refusal ladder (stage, live, CORE, pinned).
- **Then** verifies `audit[tok]` is a successful `MA_OP_ADVISE` record
  naming `slot`; otherwise `MA_REFUSED_NOADVISE` (109), itself an audited
  refusal.
- The advice arm uses this op for **every** USER kill. Plain `ma_kill` is
  never called on USER slots in that arm (trial asserts
  `adv_no_plain_kills == 0`).

This is the REFUSED_CORE shape: the dangerous transition (eviction without
deliberation) is *impossible*, not discouraged. The estimator's output can
only reach a kill through: estimator → number → policy weighs it against
declared values → policy records ADVISE (accept or reject) → policy invokes
the gated kill. Remove any link and eviction stops.

### 2.4 The policy's deliberate rule (learner side)

At each pressure event (store full), the advice-arm policy:

1. Declares its own judgment: `v_in` for the incoming memory, `v_s` per
   candidate (signed trust × features — explicit declared values, the MA3
   recommendation for signed judgments).
2. Solicits advice: `a_in`, `a_s` per candidate (signed; 0 = no opinion).
3. Computes `c = v + w·a` with `w` the **policy-declared** advisory weight.
4. Kills `argmin c` (tie → lowest slot) iff `v_in + w·a_in` strictly beats
   `min c`; otherwise drops the incoming memory.
5. Records the ADVISE entry: `accepted = 1` iff the advisor's top kill-lean
   (argmin `a`, tie → lowest slot) coincides with the killed slot *and*
   its strength ≥ margin — i.e., the policy demonstrably followed the
   advice. Otherwise `accepted = 0`: a deliberate, audited rejection.

`w` is calibrated by verification, not sampling: on each delayed
revelation of an admitted memory, compare the recorded advice sign with
the revealed truth — agree: `w += 4`; disagree: `w -= 8`; clamp [0,100].
Deterministic, logic-driven trust calibration. A WCAL record audits each
change.

## 3. Why this cannot smuggle automaticity back in

Three independent barriers, each checkable:

| Barrier | Mechanism | Check |
|---|---|---|
| Type-level | Advisor cannot name slots (no imports, no store access) | runner grep: isolation |
| Op-level | `ma_kill_advised` refuses without a deliberate ADVISE token | `REFUSED_NOADVISE` path; `adv_kills_gated` |
| Audit-level | Every advice-driven kill has a ledgered accept/reject with the advice value | `adv_kills_gated`, acceptance-rate band |

And the tripwire: if acceptance ≥ 95% the trial reads NEGATIVE —
"the estimator decides in practice" — because an advisor that is never
rejected is a decider wearing an audit costume. The design *requires*
visible rejections to count as advisory.

## 4. What the interface does not do

- It does not give the advisor any say over CORE (CORE kills remain
  `REFUSED_CORE` through the same ladder inside `ma_kill_advised`).
- It does not let advice change declared values: `value` is still assigned
  by the learner at ADD and revised only by deliberate acts. Advice enters
  the *decision* (which slot to kill), never the *judgment* (what a memory
  is worth).
- It does not consult the advisor when there is no pressure: uncontended
  admissions are pure declared-value judgments. Advice is for hard
  trade-offs, which is where the MA3 adversarial loss actually bit.

## 5. Scale argument

Per pressure event the interface costs one advice scan: O(CAP) slots ×
O(feats) integer ops — the same order as the victim scan the policy
already performs. Advice is a per-slot signed scalar solicited on demand;
there are no pairwise or N×N structures, no global optimization, no
cross-slot state in the advisor. Time scales linearly in (slots ×
episodes); memory linearly in (slots × feats) plus the audit ledger, whose
cap must grow with horizon (4096 entries here; ~400k at 100x). The named
next test is a 320-slot / 5000-episode linearity check on variant v3.
