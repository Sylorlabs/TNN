# REPORT -- PHASE 4/5: GENERATIVE STATE. NEGATIVE.

Branch `ownership`. Prereg `phase4/PREREG.md`, frozen before code.
3/3 sha256 `e300b7f0fa6752914f44...` (30 rows, one per regime x arm)
`score4.py` recomputes every verdict independently.

## VERDICT

**The generative-state hypothesis is not supported.** Of the three
prereg conditions, one holds cleanly, one fails, and one fails
decisively. The result that looked positive on the first two runs was an
output-contract bug (below), and fixing it removed the effect.

## RESULTS

Cost to generate the target (proposals needed; `-1` = never in 400):

```
 regime  A_exper  E_relat  B_fresh  C_facts  D_erasd  F_irrel  G_misle  H_shuff  I_oracl  J_match
   0        1        1       -1        1       -1       -1       -1       -1        1        1
   1       10       10      225       37      225       -1       -1       10        1       10
   2        3        3       -1        6       -1       -1       -1       -1        1        3
```

### Condition 1 -- without learned state, is S hard? -- **FAILS in 1 of 3**

Fresh learner (`B`) failed outright in regimes 0 and 2 (never in 400), so
the condition holds there. But in regime 1 the **fresh uniform sampler
succeeded at cost 225**. So in that regime the target was reachable by
luck, and any "learned state made it cheap" claim is confounded by a
budget large enough for random search.

The prereg says a quick falsification kills a mechanism but not the
frontier. This kills *this instantiation*.

### Condition 2 -- does learned state make S cheap? -- **holds, but weakly**

A beat B in 2 of 3 regimes (regime 0: 1 vs never; regime 2: 3 vs never).
In regime 1 there is no separation (10 vs 225 -- both succeeded, A is
20x cheaper, but Condition 1 already failed there).

So the honest statement is: **learned state helps where fresh sampling
fails, and does nothing where fresh sampling succeeds.** That is a real
effect but a narrow one.

### Condition 3 -- can facts-only reconstruct it? -- **FAILS DECISIVELY in regime 0**

In regime 0, `C_facts_only` scored **cost 1 -- identical to the
experienced learner**. A learner that was handed the target ops as bare
facts, with no procedure and no experience, generated the target on its
first proposal.

That is precisely the disqualifying condition in the prereg: *"If C
matches A, the effect is facts-reconstructible and is NOT a
generative-competence advantage."* In regimes 1 and 2 C was 4x and 2x
worse than A, so there the effect is *not* trivially reconstructible.

### Control integrity -- one control FAILED

* `I_oracle` = 1 everywhere. Correct, it is a bound.
* `F_irrelevant` = never, in all 3. Correct: wrong experience gives no
  benefit.
* `G_misleading` = never, in all 3. Correct: anti-weighted state does not
  help.
* **`H_shuffled` = 10 in regime 1 -- it SUCCEEDED.**

The shuffle control permutes op labels generically (`(x*5+2)%OPS`). In
regimes 0 and 2 it failed as expected. In regime 1 the permuted state
still hit the target. Given that the *fresh* uniform sampler also hit in
regime 1 (cost 225), regime 1 is simply a permissive world at budget 400:
almost any state finds the target. The shuffle control caught that.

`D_erased` correctly equals `B_fresh` in all regimes -- no residue.

## THE DEFECTS THAT PRODUCED A FALSE POSITIVE FIRST

Recorded because the first two runs looked positive and the effect was
entirely artifactual.

**Defect A -- correlated sampler.** The first sampler used
`pick = (tries*31 + pos*17 + rg*7) % total`. That single linear hash is
strongly correlated across positions. With the informed state weighting
two ops to 60/124, position 1 required `pick >= 120` -- about 3% of
draws. So even the perfectly-informed arm could not hit the target in
400 tries, and **every** arm reported `cost = -1`, which reads as a
striking "nobody can generate this" until you notice it includes the
informed arm. Replaced with a per-position mixing hash.

**Defect B -- duplicate rows silently overwritten by the scorer.** The
generator emitted one row per `(build, arm)`, so each `(regime, arm)`
appeared 3-6 times. `score4.py` keyed on `(rg, arm)` and kept the last,
so the **uniform fresh** row overwrote the informed one and every arm
scored `-1`. The first "positive" table I read -- A=1/10/3 beating B=never
-- was read from the raw file, not from the scorer, which is exactly why
the two disagreed. Fixed by restructuring the generator to emit exactly
one row per `(regime, arm)`; `armBuild()` and `buildState()` extracted as
functions.

**Defect C -- shuffle control was a duplicate of A.** Arm 7 fell through
to `bb = build`, so with `build = 1` it ran the *identical* state as A and
"matched" it perfectly. That looked like strong evidence for the
mechanism. It was the same buffer twice. Fixed by adding a real permuting
state variant; `H_shuffled` then behaved correctly (failed in 2 of 3).

**Defect D -- my own misreading.** I reported `A` winning when I had
truncated output with `head -12` and read an `arm=0` line that was below
the cutoff. I checked my own output rather than trusting the excerpt.

## ANSWERS TO THE BRIEF'S CENTRAL QUESTION

> Can experience alter the learner's own future generative/structural
> possibilities?

**In this instantiation: weakly, and not in the way that would matter.**

* Learner state does change the *proposal distribution* -- that part is
  real and it is not a ranker. It biases what gets generated, which is
  what `phase1/` proved never happened in 1,025 audited sources.
* But the gain is **facts-reconstructible** in the one regime where it
  was cleanest (C tied A at cost 1).
* And it is **not robust**: in regime 1 a fresh sampler and a shuffled
  state both succeeded, so the regime measures budget, not competence.

The per-requirement verdict:

* **Phase 4 (ten hypotheses)**: one mechanism built (learned proposal
  grammar, H5, at first order; H10 via the permuted-state variant). It
  fails Condition 3. The other nine not built -- a quick falsification
  of the shared mechanism shape does not distinguish them, and they all
  reduce to "state biases generation" which is what this tested.
* **Phase 5 (controls A-J)**: implemented and reported. Three controls
  (A-vs-B, C, H) are informative; I, F, G, D behaved as expected.
* **Phase 6 (transfer)**: not run. Preregistered; would need Condition 2
  to hold robustly first.
* **Phase 7 (revision)**: not run.
* **Phase 8 (method objects)**: not attempted. Nothing here qualifies.

## WHAT ACTUALLY CHANGED RELATIVE TO PHASE 1

This is the one positive thing, and it is about *my* prior, not the
architecture.

`phase1/REPORT.md` proved no audited mechanism alters the candidate
space. Phase 4 built one that **does** alter generation -- and then found
it insufficient. That is a different failure from Phases 6-9/16/17,
which all failed *inside* a fixed space. So the frontier moved: the
question is no longer "can state alter generation" (it can) but "can it
alter generation in a way facts cannot reconstruct" (not shown).

## LIMITS

* Single author. The adversary slot (`phase2/adversary_slot.md`) is
  unfilled. Three of the four defects above were found by me, in my own
  code, after reporting a false positive twice.
* 3 regimes, 1 budget (400), 1 alphabet size. Regime 1's permissiveness
  suggests the budget is the binding constraint and should be swept.
* Synthetic substrate; nothing here measures TNN.
* `I_oracle` is hardcoded to cost 1 rather than implemented as a
  generator, so it is a declared bound, not a measurement.

L3 = 0. No architecture changed. No bridges added or removed.