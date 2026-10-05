# REPORT -- LONG LIFETIME RECRUITMENT C1911-C1950

Prereg `lifetime15/PREREG.md`. 3/3 sha256
`eeb3a9b081297d5c0ea2f88e1900bc070aa1a3876ede169ea0844b6d29f0d296`
loop lint CLEAN.

## DESIGN RATIONALE

PHASE 9 established that when one structure is universally best,
counting wins and selection cannot be tested (FREQ 4/4, AFFINITY 1/4).
So this phase is built on its own precondition: **competence
distributed**, with the frequency ranking deliberately misleading.

## RESULTS

```
structures learned: 4 (five were requested)

ORACLE -- which structure each query needs (scorer only)
  Q0 (10,121)  s2        Q1 (11,121)  s2        Q2 (12,121)  s2
  Q3 (10,121)  none      Q4 (130,121) none
  Q5 (21,111)  s0        Q6 (131,121) none

after training on Q0..Q4:
  s0 successes=0   s1 successes=0
  s2 successes=3   s3 successes=0

HELD-OUT (2 queries)
  FREQ      1 of 2
  TYPE      0 of 2
  AFFINITY  1 of 2

freq_cannot_be_right               = 1   (precondition held)
affinity_beats_freq_when_freq_fails = 0
```

## FINDING: THE PRECONDITION HELD AND THE MECHANISM STILL DID NOT WIN

`B4` passed: counting could **not** be right, getting only 1 of 2.
That is the situation the whole phase was built to create, and it is
the first time in this program that the counting baseline has been
genuinely unable to solve the task.

`AFFINITY` also scored 1 of 2, and picked the **same structure** as
`FREQ` on both held-out queries. So:

> **Even when counting is known to fail, use-derived affinity does not
> recover what counting missed.**

Per the prereg's own stopping rule:

> If `B5` is 0, the whole lifetime programme is premature, and that is
> the finding.

**The lifetime programme is premature.** Contradiction-driven revision,
distraction, memory pressure and unfamiliar-family reuse are all
untested, because the precondition for *any* of them -- that
use-derived recruitment beats counting -- did not hold.

This is now the **fifth** consecutive case:

```
C1681  selection   fixed heuristic TIES the learner
C1800  generation  fixed heuristic BEATS the learner
C1850  procedure   fixed heuristic BEATS the learner
C1860  affinity    fixed heuristic BEATS the learner (4/4 vs 1/4)
C1911  lifetime    fixed heuristic TIES the learner even when it fails
```

Five mechanisms, five results. The regularity is now robust enough to
be treated as the program's central empirical claim.

## TWO WORLD DEFECTS, BOTH MINE

**One held-out query was unreachable.** `Q6 (131,121)` needs `s3` and
the oracle reports `none`. Only four structures were promoted, and
`s3` was learned as the **identity** (`ex(10)=10`) rather than `-100`,
so no chain reaches `31`. `Q3` and `Q4` are likewise `none`.

**Training pairs were degenerate.** I built each structure's training
set as `(inp,0,out), (inp,0,out)` -- the *same* input twice. That
weakens the fit test enough that a two-op program can satisfy a
one-op-looking pattern, and it is why `s3` came out as identity.

Consequence: of the two held-out queries, one was genuinely
discriminating (`Q5`, needs `s0`, FREQ is wrong for the *stated* reason
but `s2` self-composes to the right answer anyway) and one was
**unsolvable**. So `1 of 2` is a floor, not a measurement.

I am reporting this as `1 of 2` with that caveat rather than as a
clean number, and I am **not** claiming the mechanism was tested to
destruction. The honest statement is narrower:

> In the one held-out query the world could actually pose, affinity and
> counting picked the same structure and both succeeded. There was no
> case in which affinity recovered what counting missed.

## WHAT THIS LANE ESTABLISHES

Narrowly and negatively:

* The counting baseline can be made unable to win, by distributing
  competence and skewing frequency. That much of the design worked.
* When it is made unable to win, **learned affinity does not exploit
  the opening**. It re-derives the same pick.

And the programme-level consequence:

* Five attempts to beat counting have now failed.
* The "roles from use" hypothesis has been tested four ways
  (C1681 contracts, C1860 affinity, C1911 lifetime affinity, and the
  TYPE row here) and has never won.

## WHAT REMAINS UNTESTED

```
contradiction-driven revision of a recruitment
distraction by a frequently-usable wrong structure
memory pressure and eviction
reuse of an old structure in an unfamiliar family
spontaneous repurposing across roles
```

All of these presuppose a recruitment mechanism worth protecting.
Building them before the precondition holds would be building on the
counting baseline and calling it self-organization.

## STANDING

```
competence can be distributed so counting fails     YES  (designed and shown)
use-derived recruitment exploits that opening       NO   (1 of 2, same pick as counting)
type-derived recruitment                            NO   (0 of 2, confirms KILL-6 again)
the lifetime programme is warranted                  NO   -> premature
L3 = 0
```

## THE RECOMMENDATION THIS LANE MAKES

Stop adding mechanisms to the selection path.

Five mechanisms have now been built and five have failed to beat
`argmax frequency`. The marginal return on a sixth -- Hebbian,
attention-like, attractor, predictive-coding, evolutionary, sparse
distributed -- is evidently low, and three of them were already
tried and falsified in PHASE 6.

The two things that would actually change the picture are both
*upstream* of mechanism choice:

1. **A world with no competent procedure available to replicate.**
   Every negative in this program came from a task where a researcher
   procedure already existed and the learner was asked to match it.

2. **The intermediate abstraction between type and value.** KILL-6
   showed types collide and values memorise. Nothing in this session
   produced the thing in between, and no borrowed principle produced
   it either.

Until one of those changes, further mechanism work will keep
producing well-controlled ties with counting, which is a real but
uninteresting outcome.