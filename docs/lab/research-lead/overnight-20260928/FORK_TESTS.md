# FORK TEST RECORD -- three forks, each tested rather than argued

Branch `ownership`. Tests the three options raised after PHASE 17's void
verdict, in the order recommended (cheap falsification before expensive
build). Each fork gets an explicit verdict and evidence.

---

## FORK 3 -- can the existing corpus substrate host the needed mechanism?

**Verdict: NO. Tested and falsified by reading `borrow/b24.zag`.**

The recommendation was to check whether the cross-step state already in
the corpus (`borrow/b24`..`b28`, which hold `sup[]`/`accum`) lets me
test the dilemma's premise cheaply, before funding a new build. That
check is decisive and negative.

**Evidence.** `sup[]` is per-structure accumulated consequence. In
`b24.zag`:

* All **11** reads of `sup[]` are `sc > bestScore` comparisons
  (lines 378, 401, ...). It is a **ranking** statistic, never a gate.
* **Zero** occurrences of support gating correctness
  (`sup.*FAIL` matches: 0). If prior state determined whether a
  structure could succeed, a support-threshold failure would appear.
* It is written as `sup[f0] += tok` (line ~514) — one scalar per
  structure, incremented by consequence tokens.

So `sup[]` is **accumulated counting**, not **compositional context**.
Correctness is fully determined by the current query (`con[]` class
filter + `exec` + class match); `sup[]` only ranks candidates that have
*already* been shown eligible.

This is the same mechanism as the `argmax frequency` arm, just with the
counts sourced from consequence tokens instead of outcomes. It is not
the "context established by prior steps" class the dilemma requires.

**What this closes.** The dilemma's escape route needs state that
**gates** behaviour — where what worked before determines what is
*possible* now. Nothing in the corpus does that. All 88 borrowed-phase
experiments route on eligibility-from-the-current-query and rank by
accumulated scalar.

**Consequence:** Fork 1 is not cheap. It needs new infrastructure
(a substrate where prior state changes the candidate set, not just its
ranking), which is a genuinely different experiment class.

---

## FORK 2 -- is the dilemma itself the finding?

**Verdict: YES, and it is already committed and verifiable.**

The dilemma is not a failure to find an answer; it is an answer about
what this candidate family can express. `dilemma17.py` verifies both
horns over 1,950 `(x,y)` pairs:

| family | N | pairs | ambiguous | verdict |
|---|---|---|---|---|
| `a in [1,2]` | 20 | 780 | **0** | search == oracle |
| `a in [1,2,3]` | 30 | 1170 | **0** | search == oracle |
| `a in [1,2,3,5]` | 40 | 1560 | **0** | search == oracle |
| `a in [1,2,3,5,7]` | 50 | 1950 | **0** | search == oracle |

* **Observable target** → any learner holding the trace table solves it
  in one observation. The world cannot distinguish *learned* from
  *searched*. (PHASE 16 took this horn and won 12/36 — a router, not
  learning.)
* **Hidden target** → the only signal channel is gone; every arm
  collapses to a tie-break. (PHASE 17 took this horn and produced
  `LEARNED` with an identically-zero metric.)

The two requirements in the brief — "a genuinely available conditional
signal" and "conditional competence must not be search" — are mutually
exclusive **within this family**. That is a clean, verified, negative
result, and it is stronger than either failed experiment.

**Standing caveat.** This is bounded: verified for affine-composition
candidates with a 2-step multiplicative structure. It does **not**
generalise to all candidate families, and I have not shown the
requirement pair is impossible in principle — only that this family
cannot express it.

---

## FORK 1 -- build the stateful-interaction experiment

**Verdict: NOT ATTEMPTED, and deliberately deferred.**

Requirements per the dilemma: candidates individually
indistinguishable under single-shot evaluation, separable only under
repeated interaction, correctness depending on context established by
prior steps.

Fork 3 established this needs new substrate infrastructure, since
nothing in the corpus gates behaviour on prior state. Building it means
inventing a state-bearing world and then testing one mechanism against
it — with me as the sole author of both, which is precisely the
independence problem `INDEPENDENCE_AUDIT.md` identifies.

I am not declining this because it is hard. I am declining to build it
**before** Fork 2's dilemma is accepted as a result, because if the
dilemma holds, the correct thing to change is the *question* (does
competence require gating state?) rather than the world. Otherwise I
risk authoring a world whose only virtue is that my mechanism wins in
it — the count16 failure mode, at a larger scale.

---

## CONSOLIDATED FORK VERDICT

| fork | verdict | basis |
|---|---|---|
| 3. reuse corpus state | **NO** | `sup[]` ranks, never gates; 11/11 reads are comparisons, 0 gates |
| 2. dilemma is the finding | **YES** | 1,950 pairs, 0 ambiguous, both horns verified |
| 1. build stateful experiment | **deferred** | needs new substrate; should follow acceptance of 2 |

**Recommended order: accept 2, then design 1 as a test of the gating
hypothesis rather than another attempt to beat counting.**

## C1634 STATUS: OPEN, with a sharper statement

Not "counting dominates, cause unknown." Instead:

> Within affine-composition candidate families, a query-blind arm is
> capped at `ceil(H/N)`, and **any** conditional arm either identifies
> the correct candidate in one observation (making it search, not
> learning) or has no signal to condition on. Counting's dominance is
> therefore not an artifact of candidate size that better selection can
> overcome — within this family it is the **only** outcome available.

The next experiment must test whether **gating state** (prior experience
changing which candidates are *possible*, not merely preferred) breaks
this. That is a different hypothesis than C1634 and should be
preregistered as C1635.

L3 = 0. No architecture changed. No bridges added or removed.