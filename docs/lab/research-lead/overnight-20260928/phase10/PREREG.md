# PREREG -- PHASE 10: STRUCTURAL POSSIBILITY, NOT PROPOSAL WEIGHTS

Branch `ownership`. Frozen before code. Follows `phase6/REPORT.md`
(permutation closed, positive is bounded L2) and `FORK_TESTS.md`
(the corpus substrate cannot express state that GATES structure).

## THE CEILING BEING BROKEN

Every mechanism so far has been:

> fixed alphabet + fixed proposal FORM + state changing WEIGHTS

which returns learned ranking in different clothing. The success bar
here is deliberately stronger than "the proposal distribution changed":

> **Relevant experience must cause a STRUCTURAL POSSIBILITY to become
> cheaply constructible that fresh and facts-only learners cannot cheaply
> reconstruct under matched resources.**

"Structural possibility" means: the space of things that can be built is
itself larger after experience. Not that a fixed space is sampled more
often.

## SUBSTRATE CHANGE (the minimal generic move)

Phase 6's substrate: sequences of length 6 over 10 fixed ops. Learner
state = bigram counts. The *form* was fixed by the researcher.

Phase 10's substrate adds exactly one degree of freedom:

1. **Variable-length programs** (length 3..8). Length is itself a
   structural choice, not fixed.
2. **Learned rewrite operations.** The generator can apply
   *learned* transformations to a partial construction. The set of
   applicable transforms is **learner state**, not a source-defined
   table. This is the crucial difference from Phase 6: the *available
   moves* change, not just their frequency.

No modes. No `GATE_MODE`, `PLAN_MODE`, `INVENT_MODE`, `CAUSAL_MODE`, no
domain routers, no role bridges, no generator-per-domain. One generic
persistent structural state buffer.

## FIVE COMPETING PRINCIPLES (hypotheses, not subsystems)

Each is a candidate answer to "which generic primitive lets experience
alter structural organization". They are *modes of one generic state
buffer*, selected by a preregistered arm index -- not separate systems.

| arm | principle | what learner state holds |
|---|---|---|
| P1 | local plastic connectivity | per-edge co-firing counts; construction follows strong edges |
| P2 | learned structural rewrites | which (pattern -> replacement) transforms have worked |
| P3 | content-addressed interaction | addresses derived from prior successful outputs |
| P4 | attractor / settling | states that recur are revisited; construction settles into them |
| P5 | learned executable transforms | which op-subsequences execute successfully together |

All five read and write the SAME generic buffer type. The arm index
selects which fields are updated -- this is a research convenience and is
disclosed as such, since a per-arm update rule is the mildest form of the
mode pattern the brief forbids. **Mitigation: P1-P5 differ only in which
counters increment, and all five are exercised through the same
construction loop. No arm gets a different generator, a different search,
or a different success criterion.**

## SUCCESS BAR

Required, under matched proposal budget:

* **S1**: with learned state, target constructible at low cost.
* **S2**: fresh learner cannot construct it within budget.
* **S3**: facts-only (same raw facts, charged reconstruction) cannot
  cheaply match.
* **S4**: erased state loses the advantage.
* **S5**: irrelevant prior does not help; misleading prior hurts or is
  revised.
* **S6**: survives identifier permutation (with a broken-permutation
  positive control, as in Phase 6).
* **S7**: unseen related transfer -- the structural lesson must apply to
  a target never seen.
* **S8**: revision after invalidation recovers.
* **S9**: source-enumeration audit -- the learner state must not encode
  a source-defined answer key.

## CLASSIFICATION RULE

If a mechanism only learns weights over a source-defined alphabet or
form, it is **bounded L2** and I move on without further effort. Only a
mechanism that changes *what can be built* is worth escalating to
method-ownership testing.

## LIMITS DECLARED NOW

* Single author. Adversary slot (`phase2/adversary_slot.md`) unfilled.
* Synthetic. Nothing measures TNN.
* Phase 6 found transfer and revision both fail for bigram state; this
  phase asks whether *structural* state does better, which is the whole
  point, but a negative is a plausible outcome and must not be
  reframed.