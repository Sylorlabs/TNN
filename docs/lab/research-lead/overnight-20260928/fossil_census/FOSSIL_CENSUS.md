# FOSSIL CENSUS

**Verdict: FOSSIL-CENSUS-COMPLETE.**
**Date:** 2026-10-01 UTC.

## Question

Bid semantics (`1538eeefe`) established that a MAP's bid is a birth
certificate: no production code adds bid-relevant edges to a MAP after
promotion, and zero MAPs execute at query time. The predicted consequence
is a fossil population: MAP shells that survive eviction (bid 2 outranks
the bid-0 sweep) while never being referenced again.

This experiment counts the fossils.

## Method

Unfrozen variant with three behavior-preserving instrumentation hooks
(see NAMECHECK.md): per-MAP reference counter (field 12, never read by
production code), birth clock tick (field 16), revision hook, and
post-promotion execution attribution hook. Behavioral equivalence
verified: base binary (no hooks) and full binary (hooks) produce
byte-identical battery output.

Battery: teach 4 chains, promote 4 MAPs (3 unmasked + 1 masked), re-query
(shadow FACT hits), contradict one licensing fact (revision of MAP_A),
then 1000 filler teaches for eviction pressure. Census at two points:
pre-filler (low pressure) and post-filler (high pressure).

Classification per live tag-20 MAP:
- LIVE: root and graph intact, referenced at least once post-promotion.
- FOSSIL: root and graph intact, never referenced post-promotion.
- ZOMBIE: graph root destroyed (dead slot / wrong tag).
- DEGRADED: root valid but graph walk hits dead cell.

3/3 byte-identical runs (SHA-256 `0c11b7b0...`).

## Results

### Pre-filler census (low pressure)

```
MAP 22 LIVE refs=2 bid=2 birth=12 ans=999
MAP 46 FOSSIL refs=0 bid=2 birth=13 ans=301
MAP 87 FOSSIL refs=0 bid=2 birth=14 ans=401
MAP 98 FOSSIL refs=0 bid=2 birth=17 ans=601
CENSUS live=1 fossil=3 zombie=0 degraded=0
```

Fossil fraction: 3/4 = 75%. The fossil population exists: three MAPs are
structurally intact, were never referenced after promotion (refs=0), and
carry the birth-certificate bid of 2. MAP 22 is LIVE because the battery
revised it (refs=2: one revision event + one re-execution during repair).

Note what the refs show: re-queries (phase 3) hit shadow FACTs and never
touched the MAPs. The only post-promotion reference in the entire battery
is the researcher-driven revision. Nothing in the learner's own operation
consults a MAP.

### Post-filler census (high pressure)

```
MAP 22 ZOMBIE root=15 refs=2 bid=2
MAP 46 ZOMBIE root=35 refs=0 bid=2
MAP 87 ZOMBIE root=72 refs=0 bid=2
MAP 98 ZOMBIE root=91 refs=0 bid=2
CENSUS live=0 fossil=0 zombie=4 degraded=0
```

Zombie fraction: 4/4 = 100%. Under eviction pressure every MAP's graph
root was destroyed. The fossil state is transient: fossils do not persist,
they zombify. The bid-2 "fossil mechanism" protects the MAP shell while
the graph cells (bid 0, evicted first) rot underneath it.

MAP 22 is the sharpest case: it was LIVE (referenced by revision), yet it
still zombified. Being used does not protect a MAP, because use leaves no
trace on the bid and the graph cells it depends on are bid-0 regardless.

## Bid distribution

Pre-filler: all 4 MAPs at bid 2 (birth certificate, unchanged since
promotion; revision does not touch MAP standing). Post-filler: all 4
zombie shells still at bid 2. The bid never reflected utility at any point
in the MAPs' lifetimes.

## Interpretation

1. The fossil prediction is confirmed: 75% of MAPs fossilize under low
   pressure (intact, never referenced, bid frozen at birth value).
2. Fossilization is a waystation, not an end-state: under pressure 100%
   zombify. The architecture produces dead structures by two routes
   (never-used and used-then-rotted) and retains neither usefully.
3. The refs counter is the more honest utility meter the bid was supposed
   to be: it shows exactly one reference event across four MAP lifetimes,
   and it was researcher-driven (contradiction), not learner-driven.
4. Combined with the zombie census (running): the dead-structure
   population has two compartments, fossils (intact, unreferenced) and
   zombies (shell intact, graph destroyed). Both are invisible to the
   learner: no machinery reads refs, no machinery checks root integrity
   before use, and the bid cannot distinguish any of these states from a
   healthy MAP.

## Standing metrics

- RESEARCHER-OWNED STRUCTURAL DECISIONS: 0
- LEARNER-OWNED STRUCTURAL DECISIONS: 0
- SOURCE-ENUMERABLE FORMS: all (tag-20 MAP, tag-101..104 graph cells)
- SUF DECISIONS: 0
- LEARNER-INTERNAL CRITERIA: 0
- REUSE EVENTS: 0
- REVISION EVENTS: 1 (MAP_A revised during battery, then zombified)
- COGNITION LINES: 0 added (instrumentation only, unfrozen variant)
- MODES: 0, BRIDGES: 0, HANDLERS: 0, SEMANTIC CASES: 0

## Constraints honored

UNFROZEN ONLY. Frozen source SHA-256 re-verified unmodified at end
(`a29972ca...`). Pure Zag, safebin, `which python3 python` empty.
Zero em dashes byte-verified. Paper untouched. Nothing pushed.
3/3 byte-identical runs.
