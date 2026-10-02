# Generator notes — cmp_scale

## Determinism

`gen_probes.py` imports nothing random. Probe `i` of a family is
`pool[i % len(pool)]`: combinatorial cycling over (entity combos ×
phrasing templates). Re-running produces byte-identical batteries and
oracle.

## SUP3 winner-last ordering (documented design decision)

SUP3 (3-way superlative) probes always place the true extremum LAST in
the question ("which is the tallest of big ben, the statue of liberty,
and the eiffel tower?"). Rationale, preregistered in spirit: a genuine
n-way superlative must be order-invariant; winner-last defeats any
pairwise-leftmost strategy (compare first two, name a winner) and forces
the machinery to consider all three mentions. A pairwise engine gets
these wrong; a real comparison engine gets them right regardless of
order. This is a deliberate adversarial ordering, not a trick — it is
the minimal test that distinguishes "compared two" from "compared three".

## Oracle independence

Expected answers come from the entity/attribute table in the generator,
never from the Zag code. Response-format rules ("the "-prefix list,
marker verbs) mirror the documented behavior of the baseline engine, and
the decisive metric (name + direction class) does not depend on exact
wording.

## Scale chunking

The batch runner's `dacc` accumulator is 131072 bytes with no bounds
check (found in code review, preregistered). 100x = 8800 probes runs as
4 chunks of 2200 dialogues; dialogue IDs are globally unique across
chunks. Per-DIALOGUE state resets each DIALOGUE, and no probe reads
cross-DIALOGUE state except ANA turn 2, which always follows its own
turn 1 — so chunking changes no behavior.

## Coverage check (from a dry run)

- 1x: 88 dialogues / 96 questions (ANA adds a 2nd turn)
- 10x: 880 dialogues / 960 questions
- 100x: 8800 dialogues / 9600 questions
