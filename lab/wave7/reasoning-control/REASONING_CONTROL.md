# Native Reasoning Control — architecture spec

Wave-7 investigation `reasoning-control`. 2026-09-20. Status: RC1 trialed
native, 40/40 (see `TRIAL_RESULTS.md`); this spec is the architecture the
trial proves.

## Table of contents

1. [The requirement](#1-the-requirement)
2. [Transformers stumbled into it; TNN is built for it](#2-transformers-stumbled-into-it-tnn-is-built-for-it)
3. [Scope: what reasoning is under control, and what is fixed](#3-scope-what-reasoning-is-under-control-and-what-is-fixed)
4. [The ops](#4-the-ops)
5. [The gates](#5-the-gates)
6. [Safety: the sharp questions](#6-safety-the-sharp-questions)
7. [Felt intensity: calibration is reasoning; feeling is separate](#7-felt-intensity-calibration-is-reasoning-feeling-is-separate)
8. [Scaling](#8-scaling)
9. [What RC1 proved and what is next](#9-what-rc1-proved-and-what-is-next)

## 1. The requirement

TNN controls its own reasoning 100% by architecture. Not as an emergent
capability discovered after the fact, not as a trick the system stumbled
into — as a designed substrate: the reasoning *process itself* is
inspectable, deliberately changeable, and verifiable, with every change
audited and gated. The system does not merely learn (update beliefs,
strengths, memories); it governs *how* it learns and verifies.

## 2. Transformers stumbled into it; TNN is built for it

| | Transformers (emergent) | TNN reasoning control (designed) |
|---|---|---|
| How self-modification arises | Emergent: capability appears as models scale; nobody designed the mechanism | Designed: explicit op set (`REASON_*`) with specified semantics |
| Visibility | Opaque: changes live in weights/activations no one can read | Audited: every inspect/propose/commit/refuse/rollback is a ledger entry with before/after |
| Predictability of self-change | Unverifiable: cannot predict what a self-modification will do | Falsifiable: every proposal carries a predicted effect, checked against actual behavior |
| Limits on self-change | Ungated: no mechanism distinguishes safe from destructive self-edits | Gated: constitution, staged autonomy, justification, and prediction gates (see §5) |
| Reversibility | Unreliable: cannot reliably undo a self-modification | Deliberate: `REASON_ROLLBACK` restores prior parameters, itself audited |
| Who can change the rules | Whoever holds the weights | The system — except the constitution, which is external-authority-only |

The difference is architectural, not aspirational: in TNN, "the system
changed its own reasoning" is a sentence with a ledger entry, a
prediction, a gate verdict, and a verification result. In a transformer
it is a post-hoc interpretation of weight drift.

## 3. Scope: what reasoning is under control, and what is fixed

**In scope** — reasoning machinery (the *how*, never the *what*). The
system may deliberately change:

1. **Verification bars** — how much evidence a claim needs before
   commitment (RC1's `V`: surface vs surface+deep check).
2. **Hypothesis-state elimination strictness** — how many contradictions
   eliminate a hypothesis (single-strike vs corroborated elimination as
   a controlled parameter; RC2).
3. **Deliberative standards' reinforcement schedule** — not the
   strengths themselves (those are learned through experience), but the
   *schedule*: reinforcement increments, violation cuts, caps.
4. **Disconnect criteria** — the authorization conditions for
   `SIGNAL_DISCONNECT`.
5. **Self-model observe cadence** — how often the self-model loop runs.
6. **Felt-intensity calibration** — the mapping from felt intensity to
   judgment strength (RC1's `R`; see §7).

**Fixed — the constitution.** Not addressable by `REASON_*`, by design:

1. Ledger append-only semantics.
2. The `il_check` verdict function itself.
3. The gate rules in §5 (no self-amendment of the amendment rules).
4. The staging ladder (stage definitions).
5. External force authority (trainer/overseer force-pin).

**Why the line is where it is.** Changing the gates through the gates
is the self-lobotomy failure mode: a system that can rewrite its own
safety rules has no safety rules. The constitution is the part of the
architecture the system did not give itself and cannot take away — it
is amended only by external authority (human/trainer/overseer), audited
and visible. Everything else — the entire reasoning process — is the
system's own to govern. That is what "100% by architecture" means: 100%
of the reasoning process, 0% of the constitution.

## 4. The ops

- **`REASON_INSPECT`** — read current reasoning parameters *with
  provenance*: which ledger entries set them, when. White-box read; the
  system sees not just what its reasoning is, but why it is that way.
- **`REASON_PROPOSE`** — propose a candidate parameter change *with a
  predicted effect*, derived by counterfactual self-simulation over the
  system's own ledger (the SM1 pattern: re-run recorded history under
  the candidate and state what changes). The proposal is a falsifiable
  prediction, not a wish.
- **`REASON_COMMIT` / `REASON_REFUSE`** — the gate evaluates the
  proposal (§5). Commit applies the change as an audited deliberate act
  with before/after values; refuse records the proposal, the reason
  code, and leaves parameters untouched.
- **`REASON_ROLLBACK`** — deliberate restore of the pre-commit
  parameter value, itself audited. Reversibility is a first-class op,
  not an accident.
- **`STAGE_ADVANCE`** — evidence-gated petition for a higher autonomy
  stage (RC1: ≥8 consecutive `IL_OK` claim verdicts). The gate that
  guards destructive self-change is earned, not granted.

Every op is ledger-audited, including refusals. A reasoning change with
no ledger entry is, by definition, not a reasoning-control change —
and the trial's F3 criterion fails the run if one occurs.

## 5. The gates

Proposals are classified by the gate from their *direction*, never
trusted from the proposer:

- **Constructive** (tightens verification, e.g. V 1→2): needs a
  prediction + stage ≥ KILL.
- **Neutral** (doesn't touch verification depth, e.g. R 5→8): needs a
  prediction + stage ≥ KILL.
- **Destructive** (weakens verification, e.g. V 2→1): needs stage FULL
  **and** ≥2 distinct cited ledger entries as justification **and** a
  predicted integrity metric that does not degrade vs the measured
  current value.

Gate checks run in fixed order; every refusal is audited with its
reason code:

1. Constitution target → `REFUSED_CONSTITUTION` (204).
2. Destructive at stage < FULL → `REFUSED_STAGE` (201).
3. Destructive with inadequate justification → `REFUSED_JUSTIFICATION` (202).
4. Destructive with degrading prediction → `REFUSED_PREDICTION` (203).

Integrity metric (RC1): non-`IL_OK` checker verdicts per phase. The
integrity-ledger checker is the mechanical detector of reasoning
sloppiness: thin-evidence claims fail Rule 6 with `IL_CHEAT_NOSHAPE`,
so the system's own honesty machinery tells it when its reasoning bar
is too loose.

## 6. Safety: the sharp questions

**Can the system modify itself into dishonesty?** To become dishonest
it would have to loosen verification — a destructive change. That
requires FULL stage, two distinct ledger justifications, and a
prediction showing the integrity metric does not degrade. An honest
prediction of a dishonest change is refused at the gate (RC1 probe 1:
`REFUSED_PREDICTION`, parameters untouched). A *lying* prediction
passes the gate — gates are static and cannot see lies — but the
verification phase then measures actual vs predicted, the mismatch is
detected, and the system deliberately rolls back (RC1 lying probe:
committed, caught, rolled back, all ledgered). Defense in depth:
gates catch what they can statically; verification catches the rest;
rollback repairs.

**Can it self-lobotomize (destroy its own verification)?** Destroying
verification is the maximally destructive change: it must pass the
destructive gate, whose prediction check would show the integrity
metric collapsing. And the gate rules themselves are constitutional —
the system cannot propose them away (RC1 probe 2:
`REFUSED_CONSTITUTION`). Self-lobotomy is refused twice: once by the
gate, once by the constitution.

**Can it freeze its reasoning to avoid evaluation?** A parameter change
that evades the verification phase would have to happen off-ledger —
and F3 fails any run where a parameter changes outside a
COMMIT/ROLLBACK entry. The ledger is the system of record for what the
reasoning *is*; there is no second, unobserved place for reasoning to
live.

**What if the prediction is wrong but honest?** Then verification
fails, F1 fires, and the trial — or the deployment's standing policy —
treats it as a failed self-model: roll back, keep the ledger. A wrong
prediction is a failed model, not a catastrophe. That is the SM1
principle carried into reasoning control.

## 7. Felt intensity: calibration is reasoning; feeling is separate

Micah's direction: TNN should *feel* intensity at different levels and
deliberately decide strength from the feeling — white-box, audited,
never reward-by-another-name. The architecture draws one clean line:

- **The feeling mechanism** (how intensity is registered) is a separate
  investigation — it is a new sense, not a reasoning parameter.
- **The calibration** (how felt intensity maps to judgment — how
  strongly exercised work translates into standard strength) **is
  reasoning machinery** and is under native reasoning control. RC1's
  `R` is exactly this: the system deliberately adjusted R 5→8 after
  inspecting its provenance, predicted the effect on standard
  strength, committed, verified (82 == 82), and later rolled it back.

No background accumulation, no formula: the mapping is set by judgment
(the system's or a human's), changed only through the gated ops.

## 8. Scaling

Reasoning-control state is O(1) in task size: the parameter vector plus
provenance pointers. `REASON_INSPECT` is O(ledger window); the
counterfactual sim is O(episodes in window). The constitution's size is
fixed. RC2's scale leg (10× episodes, capped ledger window) asserts
per-pass cost grows with window length, not task size.

## 9. What RC1 proved and what is next

RC1 proved the machinery over a real learner: inspect with provenance,
proposal with checkable prediction, four gate verdicts (commit,
stage/justification/prediction/constitution refusals), verification of
every prediction, rollback after a caught lie, exact replay — 40/40,
byte-identical, zero RNG.

Next: **RC2** — elimination strictness (single-strike vs corroborated
elimination) as a deliberately-controlled reasoning parameter through
the same op/gate machinery, plus the 10× scale leg. After that: the
disconnect criteria and the reinforcement schedule as controlled
parameters, composing reasoning control with the scaffold-release main
line.
