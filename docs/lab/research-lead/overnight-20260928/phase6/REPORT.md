# REPORT -- PHASE 6/7: TRANSFER AND REVISION OF GENERATIVE STATE

Branch `ownership`. Prereg `phase6/PREREG.md`. 3/3 sha256
`88c5fcb3dcfbd12a72d5...` (72 rows). `score67.py` recomputes all verdicts.

## PERMUTATION CLOSURE -- THE POSITIVE SURVIVES (added after initial report)

The earlier report flagged a missing permutation control. It is now
repaired, run, and **the positive holds**.

| regime | A experienced | H permuted | ratio | equivalent |
|---|---|---|---|---|
| primary(prior) | 8 | 6 | 1.33 | YES |
| related_transfer | -1 | -1 | -- | YES |
| unrelated | -1 | -1 | -- | YES |
| short_control | 2 | 1 | 2.00 | YES |

**Broken-permutation positive control: DETECTED.** An arm that relabels
the state but not the target scores -1 where A scores 8. So the test can
actually detect identity dependence -- it is not vacuous.

**Isomorphism verified.** `permute(x) = 3x mod 10`, `gcd(3,10)=1`, a
genuine bijection; targets relabel consistently (`1->3, 2->6, 7->1,
6->8`) and printed in the raw output.

**Verdict: learner-owned generative bias demonstrated, bounded L2. No
transfer, no revision, no method ownership.**

### The segfault root cause, and two more bugs

1. **`continue` is not valid Zag** (0 uses in 1,025 audited sources).
   My bounds guard used it, so the loop counter never advanced on that
   path and the permutation loop ran past the buffer -> SIGSEGV. That was
   the segfault. Repaired with `if/else`, not by disabling the arm.
2. **`armBuild` had no case for arms 6 and 7**, so both fell through to
   `return 0` (fresh state). The "shuffled" arm was literally running the
   fresh learner -- which is why it first reported -1 and looked like
   permutation had killed the result.
3. **The permutation relabelled only the column, not the row.** Verified
   analytically: after relabelling, the learner reads `row P(a)` where it
   needs `row a`, so the world is non-isomorphic. Fixed to relabel row,
   column, and the START row together.

Bug 2 is the same class as the Phase 4 defect where a "shuffled" arm was
silently a duplicate of A. **This is the second time an arm did not run
the state it claimed to.** Every arm-state mapping is now checked by
`armBuild` coverage rather than by reading the table.

## VERDICT

**The primary generation claim holds. Transfer fails. Revision is
untested.**

This is the strongest positive result in the lane *and* it is not
method ownership.

## HARNESS POSITIVE CONTROL -- PASSES

Regime 3 is a short (length-2) target that uniform sampling must reach.
Fresh sampler hit it at **cost 15** in all three budgets. The metric
detects success when success occurs, so the `-1` results below mean
"genuinely not found", not "broken instrument".

This control was added precisely because Phase 4's regime 1 leaked
success into fresh sampling at budget 225.

## CONDITION 1 -- holds BY CONSTRUCTION

Fresh sampling never found the long target in any regime at any budget
(200/1000/4000): `[-1, -1, -1]` throughout. With `OPS=10` and `LEN=6`,
one-proposal hit probability is `10^-6`. Unlike Phase 4, this is now a
design property rather than luck.

## CONDITION 2 -- HOLDS on the prior's own target

| regime | budget | A experienced | B fresh | F irrelevant | G misleading |
|---|---|---|---|---|---|
| primary | 200 | **8** | -1 | -1 | -1 |
| primary | 1000 | **8** | -1 | -1 | -1 |
| primary | 4000 | **8** | -1 | -1 | -1 |

Learner state makes the target **cheaply generatable** (8 proposals) where
a fresh sampler needs more than 4000. `F_irrelevant` and `G_misleading`
both fail, so the gain is specific to *relevant* experience.

Cost is **invariant across budget** (8/8/8), which is what an
independence fix should produce.

## CONDITION 3 -- DISTILLATION BEATS RE-DERIVATION

`C_facts_only` replays the same raw facts 40 times per episode and then
generates; it **never succeeded**, while `A` succeeded at 8. So the
distilled bigram state is strictly cheaper than re-deriving the same
information from the same facts.

**This is the Condition 3 result Phase 4 failed** (there, facts-only tied
the experienced arm at cost 1). The difference is that here the target is
unreachable without state, so facts-only cannot shortcut it.

## PHASE 6 -- TRANSFER FAILS

On the related-but-unseen regime, `A` **never succeeded** (all budgets).
The prior learned on regime 0 did not help generate regime 1's target.

Worse, the arms that *did* succeed there were the wrong ones:

| regime | who succeeded at budget 200 |
|---|---|
| primary | `A_experienced` |
| related_transfer | **`G_misleading`** |
| unrelated | **`F_irrelevant`** |

`F_irrelevant` learned regime 2's bigrams and hit **regime 2** (cost 11) --
correct behaviour for its own target, and confirmation the arms are wired
as intended. `G_misleading` learned regime 1's bigrams with a penalty on
the true transitions and hit regime 1 at cost 4 -- the anti-weighted state
still points at the target, because the penalty was smaller than the
accumulated weight.

**Transfer is the central question of Phase 6 and it failed.** Bigram
statistics capture *what followed what* in the prior world. They do not
capture a structural relationship that would let the learner generate a
*different* world's structures.

## PHASE 7 -- REVISION: RECOVERY FAILS

Tested. The world flips from regime 0 to regime 1 at episode 20. Cost to
generate the current world's target, per episode:

```
ep 0..19  world=0   hit=8,8,3,3,10,8,1,8,5,5,1,1,3,8,8,2,16,5,7,6   (all found)
ep 20..39 world=1   hit=-1 x20                                          (NONE found)
```

So two of the four required steps hold and two fail:

| requirement | result |
|---|---|
| old generative behaviour fails after the change | **HOLDS** -- 20/20 episodes at -1 |
| consequences expose the failure | **HOLDS** -- the per-episode decrement fires every episode |
| learner structural state changes | **HOLDS** -- targeted decrements applied, no RESET |
| **recovery** | **FAILS** -- 0 of 20 post-flip episodes ever succeed |

**Verdict: no recovery.** The learner detects the change, and the state
does change, but it cannot rebuild a generative bias for the new world.
This is consistent with Phase 6's transfer failure: the same mechanism
that cannot reach a *related unseen* target here also cannot rebuild one
after its prior is invalidated.

The state is also monotonically decaying -- decrements with no
replenishment path, since reinforcement only fires on success, which never
happens. So it is a one-way ratchet, not a revising belief.

### Two defects on the way to this verdict

**Per-proposal consequences annihilated the state.** The first version
applied a -1 penalty on every failed proposal. With 400 proposals per
episode against ~25 accumulated counts, the state was destroyed within a
single episode and *every* arm scored 0 -- including world 0, where the
same state reaches cost 8 in the main sweep. Fixed by applying one
consequence per episode, from the final proposal only, penalising just the
first wrong pair.

**Zag has no bare `{ }` block.** The first fix used one; `znc` rejected it
with `unexpected token at top level`. Converted to plain statements.

## DEFECTS FOUND AND FIXED

**Cross-budget state decay (the important one).** The first version of the
run had `A` succeeding at budget 200 (cost 8) and failing at 1000/4000. That
was not a budget effect: the revision penalty mutated `ST2` inside the
budget loop, so each larger budget started from a state already decayed by
the previous budget's failures. More budget meant more decay. Fixed by
snapshotting `ST2` and restoring it before each budget, so budgets are
independent. Costs became 8/8/8.

**`H_shuffled` arm removed, unresolved.** The permutation arm segfaulted.
Isolating per arm showed arms 0-4 and the oracle run clean and only
`H_shuffled` crashes. The index arithmetic was verified in Python to be
in-range, so the cause is unresolved and the arm is **disabled rather than
fixed**. Consequence: **this phase has no identifier-permutation control**,
which the brief required. Recorded as a gap, not quietly dropped.

**Arm-loop damage from debugging.** A `sed` edit left
`while(a<6){ if(a<5){ a=a+1; }`, silently running only arms 1, 3, 5. Caught
because the row count was 36 instead of 72. Earlier output was discarded.

## WHAT THIS DOES AND DOES NOT ESTABLISH

**Does:** learner state can make a structure cheaply generatable that is
otherwise unreachable, and that advantage is specific to relevant
experience and cheaper than re-deriving from the same facts.

**Does not:** transfer to related unseen structures. And it is **not method
ownership**:

* The state is bigram counts over a fixed alphabet -- an
  `n`-gram/proposal-grammar mechanism, architecturally a language model.
* Nothing here composes, abstracts, or constructs a *method*. `A` learned
  to reproduce one sequence it had already seen 25 times. That is
  memorisation distributed across a state buffer, not a learned procedure.
* Per the brief's standing bar: **a method counts as owned only if the
  method itself moves into learner state.** Here only frequency
  information did.

## PHASE 8 -- NOT ATTEMPTED

The Phase 8 sequence requires `G` to construct method `M` that solves an
unseen `B`. **Transfer to unseen `B` failed**, which is a precondition of
the sequence. Attempting Phase 8 now would test a sequence whose second
step is already known to fail.

## REMAINING PHASES 9-11

* **Phase 9 (one substrate, no bridges):** satisfied by construction. One
  generic substrate, one generic state buffer, no modes or routers.
* **Phase 10 (architecture-borrow):** not run. Would require new
  infrastructure per `FORK_TESTS.md`.
* **Phase 11 (parallel research):** not run.

## LIMITS

Single author; adversary slot unfilled; two defects found in my own code
this phase; **no permutation control**; 3 regimes, 1 alphabet size,
1 prior length; synthetic; nothing measures TNN.

L3 = 0. No architecture changed. No bridges added or removed.