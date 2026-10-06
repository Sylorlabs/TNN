# PHASE 2 -- FORMAL STATEMENT AND ITS LOAD-BEARING ASSUMPTION

Branch `ownership`. Companion to `phase1/REPORT.md` and `count17/dilemma17.py`.

## NOT DONE: the independent adversary

The brief asks for an independent adversary to construct a
counterexample. **I did not supply one, and cannot.** An adversary I
write shares my priors and my reading of the code; that is
`INDEPENDENCE_AUDIT.md`'s failure mode, and it is *worse* for a proof
adversary than for an experiment, because a counterexample I produce is
evidence only that I looked hard. **The adversary slot is unfilled by
design.** A counterexample here should come from someone who believes the
statement is false.

Everything below is therefore a *conditional* formalisation: it says
what must be violated for learning to be possible, and identifies which
assumption is load-bearing and currently untested.

## NOTATION

* `X` -- observations available to the learner at decision time
* `z` -- target variable: the correct candidate for a query, `z = k*`
* `C` -- candidate space, fixed at compile time, `k in C`, `|C| = N`
* `E` -- eligibility mechanism, maps `X -> 2^C`
* `M` -- learner state carried across steps
* `S` -- search access: ability to evaluate any `k in C` against `X`

## THE TWO PHASES, FORMALLY

**PHASE 16 horn (observable target).** `z` is a function of `X`:
`z = f(X)` for some `f`, and `f` is computable by evaluating candidates.

> If `z = f(X)` is computable by candidate evaluation, then for any learner
> holding the evaluation map, `S` yields `z` in one query. Therefore the
> maximum achievable score is attained by *search*, and any arm that scores
> at that maximum has demonstrated search, not learning.

`dilemma17.py` verifies the premise: 1,950 `(x,y)` pairs, **0 ambiguous**.
`z` is identifiable in one observation.

**PHASE 17 horn (hidden target).** `z` is not a function of `X`:

> If `z` is not determined by `X`, then for any learner state `M` computed
> from observations alone, `M` is independent of `z` given `X`, so no
> selection rule over `M` can beat a fixed tie-break.

`truth(c) = c % N` depends on the query *index*. Observed: `LEARNED`'s metric
was identically zero (spread 0.0 at every N); `SHUFFLED` beat `LEARNED` in
12 of 15 cells.

## THE DILemma

Let `A1` = *the observation channel is sufficient to identify `z` in one
shot*.

```
If A1 holds      -> PHASE 16: learning collapses into search.
If A1 fails      -> PHASE 17: nothing to condition on.
Therefore:  within candidate families where evaluation determines z,
            "conditional competence" is not distinct from search.
```

## WHICH ASSUMPTION MUST BE VIOLATED

Learning requires `A1` to fail **and** some other channel to carry the
signal. Enumerating what that channel could be:

| channel | candidate for the missing signal | status |
|---|---|---|
| `X` (current observation) | richer query content | tested: PHASE 17, void |
| `M` (prior experience) | state changes what is *possible*, not just *preferred* | **untested** |
| `S` (search) | exhaustive construction | tested: collapses to oracle (Phase 16) |
| `E` (eligibility) | state gates the candidate set | **untested** |

**The load-bearing assumption is `A1` itself, and it is currently
unfalsified by any experiment in this lane.**

This is the key observation, and it is *not* the same as the Phase 1 bound.
Phase 1 established mechanically that no existing mechanism varies
`C` or `E`. The dilemma says that even if one did, `A1` still forces the
outcome. **Neither Phase 1 nor the dilemma has been tested against a
mechanism that actually varies `C` or `E` in learner state.** Phases 6-9,
16, and 17 all left those fixed.

So the honest status of the dilemma is:

> Not proven. Its premises (`A1`) were never violated by anything actually
> built, so it has never been *tested*. It is a statement about the
> candidate families examined, not about learning in general.

## WHAT WOULD FALSIFY IT

A mechanism where `A1` fails, `M` carries signal, and a learner beats
query-blind selection **without** search and **without** a
researcher-authored router. If such a mechanism exists, the dilemma is
false and C1635 resolves positive.

If no such mechanism exists after Phase 4's ten hypotheses, the dilemma's
scope should be widened rather than the mechanisms retried.

## STANDING BAR (from the brief)

Should any mechanism win, it is **not** method ownership unless the method
itself moves into learner state. A conditional readout is a router.

L3 = 0. No architecture changed.