# REPORT -- WHICH SUPPORT SCORING RULE? C1601-C1620

Follows `REPORT_45.md`, which named the scoring rule as the
researcher-owned part. 3/3 sha256
`450d43959b421ad9c1eb5ece9e88c2ea973248faf3bba048f2daf21d5368c99b`
bars lint CLEAN, loop lint CLEAN.

## SCENARIO

Identical for all four rules, so the comparison is controlled:

* consequences change, facts do **not** -- the stale recruitment stays
  class-eligible, so only the scoring rule can dislodge it
* initial support `s0=11 s1=11 s2=-1`
* expected answer 11 (the previously-penalised structure)
* 40 trials

## RULES

```
0 SUM      sup[a] + sup[b]                    (C1571, oscillates)
1 MAX      max(sup[a], sup[b])                no length inflation
2 NONSELF  SUM, but a structure may not appear twice in one chain
3 DAMPED   (sup[a] + sup[b]) / chain_len
```

## RESULTS

| rule | first_correct | wrong | correct_after_first | final | support |
|---|---|---|---|---|---|
| SUM | 12 | **21** | **18** / 28 | 11 | s0=-1 s1=-1 s2=0 |
| MAX | 12 | 12 | **27** / 28 | 11 | s0=-1 s1=-1 s2=27 |
| NONSELF | 12 | 12 | **27** / 28 | 11 | s0=-1 s1=-1 s2=27 |
| DAMPED | 12 | 12 | **27** / 28 | 11 | s0=-1 s1=-1 s2=27 |

## FINDINGS

**1. The oscillation is caused by length/self-composition inflation, and
it is not specific to `SUM`.** Any rule that stops a chain from scoring
more than its best member removes it. Wrong trials drop 21 -> 12, and
post-revision stability rises from 18/28 (64%) to 27/28 (96%).

**2. Revision SPEED is unchanged at 12 trials under every rule.** The
scoring rule's contribution is **stability, not revision latency**.
That is the opposite of what I expected when I built this lane, and it
is the more useful statement: a slow-but-stable reviser is a different
animal from an oscillating one, and only the second is broken.

**3. Three of four hypotheses survive. The test was not discriminative
enough between MAX, NONSELF and DAMPED.** Per the standing rule that at
least some hypotheses must die, this lane only kills `SUM-as-specified`
-- and `SUM` here is the rule that produced the C1571 failure, so this
is a partial kill, not a clean one.

The three survivors are all "stop the score from growing with the
chain". They coincide here because all three candidate chains in this
world are length 1 or 2. Distinguishing them needs a world where a chain
of length 3 or more is viable, or where the correct answer requires
reusing one structure twice -- which is precisely the case NONSELF
forbids and SUM/MAX/DAMPED allow.

## WHAT THIS DOES NOT ESTABLISH

* No claim that any rule is correct. Only that three of them are not
  the oscillation.
* No L3 movement. **L3 = 0.**
* Nothing about whether the *representation* of support is right. All
  four share it: one scalar per structure, global rather than
  provenance-scoped. `H-SC` (context-scoped credit) remains untested
  and remains the most promising of the remaining ideas, because
  scoping credit to the regime that earned it would make REV-A fast
  *and* stable, whereas these rules only make it stable.

## STANDING

The frontier statement is now sharper:

> Applicability is learner-owned (C1541).
> Selection is learner-owned *in effect* (C1571) but its scoring rule is
> researcher-owned, and the rule matters for stability, not speed (C1601).

Next discriminating experiment: a world where the correct answer
requires self-composition, to separate NONSELF from MAX and DAMPED, plus
an `H-SC` arm with provenance-scoped credit.