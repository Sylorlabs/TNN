# REPORT -- P5-meta5c: VOID. Clone-dominant dynamics erase the prior within one trial.

Branch `lane/ownership`. 3/3 sha-identical. 18 fingerprint rows.
No `*_ok` flags.

## RESULT

| family | FRESH | RELEVANT | IRRELEVANT | MISLEADING | POP_ABLATED | ORACLE_SEED |
|---|---|---|---|---|---|---|
| 0 | 111 | 119 | 119 | 119 | 111 | 119 |
| 1 | 57 | 7 | 7 | 7 | 57 | 7 |
| 2 | 188 | 111 | 111 | 111 | 188 | 111 |

**Byte-identical to p5meta5a-repaired** despite a real change: target answers
are now revealed one per trial (sentinel `-1` until revealed) and the prior
phase observes only half its family.

## ROOT CAUSE: NOT THE INFORMATION CONTENT OF THE PRIOR

`RELEVANT == IRRELEVANT == MISLEADING` in every family, and
`POP_ABLATED == FRESH` exactly. The prior's contribution is being erased
mechanically, not out-weighed:

* `POP = 24`; each trial clones the leader into the **12 even slots**.
* One mutation touches **one** slot per trial.
* Effective diversity after one trial: ~13 slots, **one lineage**.

The prior seeds the population, but trial 1's fitness evaluation selects a
leader on partial evidence and immediately clones it. If the prior's
program is not already the argmax, it is overwritten in the even slots,
and it survives in an odd slot only by chance -- which the next clone
erases.

So the observation scheme is irrelevant to the outcome. This is a
**dynamics** defect, and it explains why changing the information
available (`want()` -> full `OBS` -> partial `OBS`) produced literally
identical numbers three times.

## WHAT THIS ESTABLISHES (about the harness)

* Clone-dominant selection erases initial conditions within one
  generation. Any hypothesis of the form "prior experience changes
  acquisition" is **unfalsifiable** on this harness, because the
  intervention is removed before it can act.
* Corollary for instrumentation: **identical results across arms after a
  substantive code change is itself a red flag.** Three byte-identical
  tables should have been treated as "the change did not take effect"
  immediately, rather than investigated as a scientific finding.

## THE REPAIR THAT COULD WORK

Not another information change. The dynamics must admit persistence:

* Clone into a **minority** of slots (e.g. 4 of 24), leaving 20
  independent lineages; **or**
* Add **elitism without clonal domination**: keep all slots distinct,
  mutate several, select only for the *reported leader*.

Either way the prior program must survive at least until the evidence
justifies discarding it. This is a harness repair and must be labelled as
such -- repairing an instrument produces no evidence about learners.

## THE STANDING LESSON (four defects, one pattern)

p5meta5a and p5meta5c together produced **five** defects, and every one
had the same shape: **the intended intervention never reached the
mechanism under test.**

| defect | intended | what actually happened |
|---|---|---|
| no mutation op | search | clone-only loop cannot search |
| seeding linear in `i` | 24 diverse programs | 4 distinct |
| full-clone inheritance | inherit best | population becomes 1 program |
| fitness vs one target | fitness | category error, acquisition pinned |
| clone-dominant | prior persists | prior erased in 1 trial |

Four of five were visible by **comparing arms that should differ**. That
check is now permanent (`tools/lab/arm_audit.py`), and this phase is a
strong argument for a second permanent check: **a no-op-change
detector**, which fails a run when a substantive edit leaves every arm
byte-identical.

## STATUS

`P5-meta5a` and `P5-meta5c` are both **VOID on harness grounds**. No
claim about learners is made or unmade. `P5-meta5b` continues in
parallel on `lane/p5meta5b`.

`P5-meta` remains open. The blocker is now precisely specified: **the
experimental apparatus does not preserve interventions**, so no
learning-to-learn question can be answered on it.

L3 = 0. No architecture changed. No bridges added or removed.