# REPORT -- P5-meta5a (repaired): STILL NOT INTERPRETABLE. Structural limitation named.

Branch `lane/ownership`. Prereg `p5meta5a/PREREG.md` + repair.
3/3 sha-identical. 18 fingerprint rows. No `*_ok` flags.

## CHRONOLOGY OF THIS PHASE

1. **Void #1** -- clone-only loop, no mutation operator. All arms 300.
2. **Repair** -- added one generic point-mutation operator. Arms now
   separate and acquisition succeeds (7-188 trials).
3. **Void #2** -- arms 1/2/3 (relevant / irrelevant / misleading) were
   *byte-identical*, and arm 4 (prior present, population reset) exactly
   equalled FRESH. The prior had **zero** effect.
4. **Repair attempt** -- removed `want()` from acquisition fitness,
   substituting an observed-pairs table. **Results did not change at all.**

## WHY REPAIR 4 CHANGED NOTHING

`OBS` is populated as a **complete copy** of the training-band answer
set, so scoring against `OBS` is arithmetically identical to scoring
against `want()`. The substitution was cosmetic. I am recording that
rather than claiming a fix that did not fix anything.

## THE STRUCTURAL LIMITATION (this is the finding)

The prior cannot help **by construction**, for a reason that no amount of
harness repair will fix:

* Acquisition begins with the **entire** training-band answer set
  available in `OBS` (or, before repair, handed `want()` directly).
* A learner that already possesses the full answer set for the target
  band **cannot be accelerated** by prior experience on anything.
* The prior's converged program occupies 1 of 24 population slots. The
  first acquisition fitness evaluation selects whichever program scores
  highest *right now*; if that is not the prior's program, the prior is
  discarded on trial 1.

So `RELEVANT == IRRELEVANT == MISLEADING` is the **correct output of
this harness**, and it is not a defect in the arms.

## WHAT WOULD MAKE THE QUESTION ASKABLE

Experience can only help if experience supplies something the learner
does **not** already have. Two structurally different ways:

* **Partial-observation acquisition**: the target family's answers are
  revealed **one per trial**, so a learner that has previously solved a
  *related* family arrives with machinery that fits faster. This is the
  honest version of "learning to learn".
* **Cross-family structural prior**: the prior is on family A and the
  target is family B, and the question is whether acquiring A's mapping
  machinery reduces B's acquisition cost. This is `p5meta5b`, running in
  parallel on branch `lane/p5meta5b`.

Both require that acquisition *not* start with full target information.
Neither is a tuning change.

## BARS THIS PHASE ESTABLISHED (about the harness, not learners)

* A clone-only loop cannot search, even when solutions provably exist
  (5/5, 5/5, 6/6 solutions generalise to unseen probes).
* A population seeded by a linear function of the slot index has ~4
  distinct members out of 24, and collapses to 1 under full cloning.
* Fitness compared against one target value across many inputs is a
  category error that silently pins acquisition at maximum.
* Providing a target function to the learner makes every prior arm
  identical, which is detectable only by comparing arms -- hence
  `tools/lab/arm_audit.py` and the `armBuild` class of defect.

The last point is the transferable lesson: **four of the five defects in
this phase were only visible because arms that should differ were
compared.** That check is now permanent infrastructure.

## STATUS

`P5-meta5a` **inconclusive by construction** -- not void (the harness
now functions) and not negative (the question is unaskable here).
Superseded by `p5meta5b` (parallel branch) and by a partial-observation
successor on this branch.

L3 = 0. No architecture changed. No bridges added or removed. No modes,
routers, domain names, or strategy menus.