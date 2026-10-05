# PREREG -- LONG LIFETIME RECRUITMENT C1911-C1950

Lane `ownership`. Phase 15. Frozen before implementation.

## 0. WHY THIS WORLD IS BUILT DIFFERENTLY

PHASE 9 (C1861) established that when one structure is universally
best, **counting wins and selection cannot be tested**. FREQ scored
4/4 there, not because counting is clever but because there was
nothing to choose.

So this phase is built on its own precondition:

> **Competence is distributed.** Every query needs a different
> structure, and the frequency ranking is deliberately misleading --
> the structure with the most successes overall is wrong for the
> held-out queries.

That makes counting *unable* to be right, which is the only situation
in which "use-derived recruitment" is a meaningful claim.

## 1. WORLD

Five structures, each learned by verified search, all distinct:

```
s0 = +100    s1 = -98    s2 = +1    s3 = -100    s4 = +98 (distractor)
```

Facts give quantities as objects, so the derived classes separate
subjects from object-only values.

## 2. SEQUENCE (the phase spec's lifecycle)

```
learn A          -> s0, s1 established
unrelated B      -> s2 trained on unrelated queries
learn C          -> s3 trained on a rare query
later task       -> held-out query needing A (s0 then s1)
new role         -> held-out query needing C (s3), never seen
```

The frequency skew is deliberate: s2 succeeds on three training
queries, s0 and s3 on one each. So `argmax frequency` picks s2 and is
wrong on **both** held-out queries.

## 3. RULES

```
FREQ      most successful structure        (the heuristic that beat me 4 times)
TYPE      derived class only               (KILL-6's approach)
AFFINITY  overlap of learned success-features
```

Features, all facts-derived, no role names:

```
f0 class(arg0)   f1 class(arg1)   f2 arg0 in goal
f3 arg1 in goal  f4 arg0,arg1 co-occur as subjects   f5 (reserved)
```

`f2`/`f3`/`f4` are the finer features PHASE 8 identified as the
missing ingredient. They are declared here in advance; if they do the
work, the coarse-only `TYPE` row must be strictly worse, which is the
built-in discrimination.

## 4. BARS

```
B1  3/3 identical sha256
B2  oracle printed: which structure each query needs
B3  competence is distributed (the oracle is not one structure)
B4  freq_cannot_be_right  (FREQ < 2)  <- precondition of the whole phase
B5  affinity_beats_freq_when_freq_fails
B6  affinity > type (the fine features are what do the work)
B7  both held-out queries resolved without any role label in source
B8  L3 reported as a value
```

## 5. WHAT THIS LANE DELIBERATELY DOES NOT DO

The full lifecycle in the phase spec also asks for contradiction-driven
revision, distraction, memory pressure and an unfamiliar family. Those
require a lifetime substrate that does not exist yet. Rather than
simulate them badly, this lane measures **the single precondition
question** -- whether use-derived recruitment beats counting *at all*
when counting is known to fail -- and records the remaining lifecycle
items as untested.

If `B5` is 0, the whole lifetime programme is premature, and that is
the finding.

## 6. DISCIPLINE

Pure Zag. `_zag_print`. 3/3, watchdog 180s. R3 and loop lints pass.
No role vocabulary. The oracle is scorer-only and never consulted by
a decision rule. Every arm reported, including failures.