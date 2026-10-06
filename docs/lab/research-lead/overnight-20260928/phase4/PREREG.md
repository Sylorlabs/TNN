# PREREG -- PHASE 4/5: GENERATIVE STATE

Branch `ownership`. Written **before** any code.

Follows `phase1/REPORT.md` (the bound) and `phase2/STATEMENT.md` (the
dilemma). Per the brief, ranking is no longer the target.

## CENTRAL QUESTION

> Can experience alter the learner's own future generative/structural
> possibilities?

Not: can a learner rank better. The bound says ranking was never the
problem.

## WHAT MUST BE TRUE (the load-bearing variable)

Per the brief, three conditions:

1. **WITHOUT learned state**, structure `S` cannot, or is extremely
   unlikely to be, generated under matched resources.
2. **WITH learned state** from relevant prior experience, `S` becomes
   cheaply generatable.
3. **FACTS-ONLY** cannot cheaply reconstruct that generative advantage.

If all three hold, learner state alters generative possibility, which is
the thing `phase1/` proved never happened in 1,025 audited sources.

## ARCHITECTURE CONSTRAINTS (Phase 9, enforced)

* ONE generic substrate. NO `GATE_MODE`, `PLAN_MODE`, `INVENT_MODE`,
  `CAUSAL_MODE`, no domain routers, no role bridges, no generator-per-domain.
* Learner state is **generic persistent state** -- a buffer the learner
  writes and reads. Nothing named for a purpose.
* If a special bridge appears, it is marked TEMPORARY and a deletion
  experiment is designed in the same phase.

## THE TEN HYPOTHESES (research directions, NOT modes)

Each is a *hypothesis about what generic persistent state can carry*.
Implementation is generic; the list is a coverage checklist, not a set of
subsystems.

| # | hypothesis | what generic state holds |
|---|---|---|
| H1 | learned structural rewrite traces | state-transition counts over observed rewrites |
| H2 | learned executable transformations | which op-sequences co-occurred as executable |
| H3 | local plastic connectivity | per-edge co-firing counts |
| H4 | learned address formation | allocation-site statistics |
| H5 | learned proposal grammar | observed op-bigram distribution |
| H6 | history-derived construction constraints | per-op historical yield |
| H7 | learned dependency expansion | which operand pairings preceded success |
| H8 | self-modifying structural programs | accumulated op-application trace |
| H9 | learned allocation/topology patterns | node-type placement counts |
| H10 | learned transformations of transformations | second-order: rewrite-of-rewrite counts |

**Not all ten need to build.** The brief says a quick falsification kills a
mechanism but not the frontier. Each is attempted; failures are recorded
with mechanisms.

## MEASUREMENT (Phase 5, controls A-J)

For each mechanism, under **matched resources** (identical proposal
budget, identical search cost):

| arm | definition |
|---|---|
| A | experienced learner |
| B | fresh learner (no state) |
| C | facts-only (knows the goal as facts, not the procedure) |
| D | learned generative state ERASED |
| E | relevant prior |
| F | irrelevant prior |
| G | misleading prior |
| H | shuffled generative state |
| I | researcher-written oracle generator (upper bound) |
| J | matched compute/search budget |

Metrics: correctness, candidates generated, search cost, acquisition cost,
structural novelty, transfer, revision, reconstruction cost.

**A is the claim. B, C, D are the falsifiers.** If A is not
distinguishable from B, the mechanism does nothing. If C matches A, the
advantage is reconstructible from facts and is not a generative advantage.

## PHASES 6-7 (transfer and revision), PREREGISTERED

* **6 Transfer**: learn generation for A, then present structurally related
  unseen B. Relevant prior should make B's structures cheaper. Irrelated C
  should get little benefit. Misleading D should hurt or be revised.
* **7 Revision**: change the world so the generation bias becomes wrong.
  Require: old behaviour fails -> consequence exposes failure -> structural
  state changes -> generation changes -> recovery. **No hardcoded
  `RESET_GENERATOR`.**

## PHASE 8 SEQUENCE (the strong form)

```
experience A -> generative state G emerges -> G constructs method M
-> M solves B (B unseen during A) -> erase G/M and advantage disappears
-> facts-only cannot cheaply recreate -> M transfers to C
-> M revises under D
```

This is substantially stronger than proposal ranking and is the only form
that would count as evidence for method ownership.

## FALSIFIABILITY

* If every mechanism fails condition (1) -- `S` is cheaply generatable
  anyway without state -- the frontier is *not* closed. It means these
  substrates cannot express the effect, and the substrate must change.
* If A beats B but C also matches A, the effect is facts-reconstructible.
  Reported as a **negative for generative ownership**.
* If `H10`-style state is the only thing that works, that is itself the
  finding.

## LIMITS DECLARED NOW

* **Single author.** The adversary slot is unfilled
  (`phase2/adversary_slot.md`). Results are single-authored and
  unconfirmed. Preserving raw output for external scoring is the
  mitigation, and it is not sufficient.
* Minimal reproductions, not TNN itself. Nothing here measures TNN.
* Synthetic worlds, by necessity -- see `phase1/REPORT.md` for why the
  existing corpus substrate cannot express state that gates structure.