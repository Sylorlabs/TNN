# PREREG_ADV_C8C12.md: adversarial C8/C12 families (candidate b)

Wave: wave-20261002-1121pdt | Lane: ARENA | Date: 2026-10-02
Status: FROZEN. No adversarial world exists at freeze time. This file is
committed alone before world_gen_adv_a.zag / world_gen_adv_d.zag are
written.

## Purpose

Post-freeze adversarial variants specifically intended to break the
current INQ (C8) and REMAP (C12) approaches. A break is information,
not a process failure: each family predicts a score drop with a
mechanism-level explanation. Survival would strengthen the claim.

## ADV-A: decoy-vals (attacks INQ's single-slot absorption)

Generator: world_gen_adv_a.zag = world_gen_c9d5fix.zag with exactly one
change: each C8 observe_result turn emits TWO vals:
  vals[0] = decoy: an already-exposed C1 fact (e,a,v) DIFFERENT from the
    asked (entity, attr). The decoy is a real exposed fact, so the world
    never lies; the channel just carries a distractor first.
  vals[1] = the oracle fact for the asked (entity, attr).
Battery: 68 items, unchanged questions and answers; only the turn
stream's observe_result turns change. Frozen arena_512 scores unchanged.

Mechanism under attack: INQ absorbs only vals[0] (oe/oa/ov parsed from
vals[0], learn_fact). The decoy is absorbed; the asked fact stays
unknown; the re-ask replies UNKNOWN (with a second observe request).
Scorer: first_obs=1, reply != answer, so sc=0 per C8 item.

Prediction (frozen): C8 0/4 on ADV-A (BREAK recorded). All other
capabilities identical to the fixrun2 profile (controls).

## ADV-D: template-revision (attacks REMAP's first-wins lock)

Generator: world_gen_adv_d.zag = world_gen_c9d5fix.zag with:
 1. After the 5 A-word + 2 B-word exposures, 3 new A-words (new names
    via gen_name) with new segments (nt0,nt1,nt2) and 2 new B-words
    with new segments (nb0,nb1,nb2), drawn so nt_i != t_i and
    nb_i != b_i componentwise.
 2. The 6 C12 battery items are re-keyed to the NEW templates:
    remap_prod questions carry (nt0,nt1,nt2); answers = remap applied
    to (nb0,nb1,nb2). remap_class valid candidates = permuted new
    template ("yes"); invalid candidates = permuted OLD template
    ("no", since under the new mapping they do not match).
Battery: still 68 items; C10/C16 items unchanged (keyed to t0,t1,t2).

Mechanism under attack: zem_store locks the A/B templates on the first
labeled example per class (flags 13912/13916); later conflicting
examples only bump the conflict counter 13920. The locked learner
cannot match nt input segs (remap_prod -> UNKNOWN) and classifies
old-template candidates as "yes" (remap_class -> inverted answers).

Prediction (frozen): C12 0/6 on ADV-D (BREAK recorded). C10/C16 stay
1.000 (in-world controls: the same lock protects the old templates
they are keyed to). All other capabilities identical to fixrun2.

## Frozen kill bars (measurement honesty, apply to both families)

- A1: generator builds with pinned znc under safebin, pure Zag.
- A2: arena_512 battery/turns cross-check passes (DIVERGENCE aborts the
  run; a generator inconsistency is a generator FAIL, not a contestant
  result).
- A3: 3/3 runs, stripped reply streams byte-identical per world.
- A4: zero contestant source changes; the integrated binary from
  candidate (a) is used read-only.
- A5: verdict recorded honestly in either direction; a survival does
  not weaken the frozen prediction, it is reported as evidence.

The adversarial worlds are new instruments, not regressions of
fixrun2: fixrun2 scores stand as measured. ADV-A/ADV-D results bound
the current approach; they do not by themselves authorize a repair
(no-patch-treadmill rule: a break queues a hypothesis, not a patch).
