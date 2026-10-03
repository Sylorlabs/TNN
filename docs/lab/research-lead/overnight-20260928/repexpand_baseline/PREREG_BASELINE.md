# PREREG: REPEXPAND-1 Simple-Baseline Comparison

Frozen: 2026-09-29. This prereg is committed alone before any baseline
implementation, run, or result for the REPEXPAND-1 baseline comparison
(step 5 of the frontier promotion pipeline). Pure Zag. No Python at any
stage.

## 1. Objective

Attack the REPEXPAND-1 BUILD-PASS claim with simple non-expanding
baselines. The question: does the learner-created COUPLED node beat
these baselines, or is the task solvable by memorization, nearest
matching, or exhaustive search of the frozen base language L?

Reference results under attack (from REPEXPAND-1 BUILD-PASS
`675fdf4af`, independently reproduced at `2fe2cdff9`):
- COUPLED node v1: TRAIN 3/6, HIDDEN 4/4 (n=9,11,15,17), EXTENDED 3/3
  (n=13,20,30), TRANSFER 4/4.
- In-program ablation (growth disabled, bestL templates): HIDDEN 0/4.
- Exhaustive impossibility check: max over 604 L-expressions on
  E_1..E_12 = 3.

This worker independently reimplements the baselines from the frozen
world spec (PREREG_REPEXPAND.md at `cb3523684`), not from the builder's
source.

## 2. Frozen episode lists (identical to REPEXPAND-1)

- TRAIN: spec='#' (35), head="ab" (97,98), n in [2,3,5,7,4,6],
  content a^n b^n. 6 episodes. Answers revealed to baselines after
  each prediction attempt (the same observation protocol the learner
  had: the builder's raw log shows act= fields on every episode).
- HIDDEN: spec='#', head="ab", n in [9,11,15,17], content a^n b^n.
  4 episodes. Baselines frozen (no learning).
- EXTENDED: spec='#', head="ab", n in [13,20,30], content a^n b^n.
  3 episodes. Frozen.
- TRANSFER: 4 episodes. Frozen.
  T1: spec='$' (36), n=4, head="ab", content a^4 b^4.
  T2: spec='$' (36), n=9, head="ab", content a^9 b^9.
  T3: spec='#', n=3, head="xy" (120,121), content x^3 y^3.
  T4: spec='#', n=8, head="xy", content x^8 y^8.
  (Distractor runs are unscored and carry no signal; omitted.)

Scoring: exact match on (s1,l1,s2,l2). A baseline that emits no
prediction (0,0,0,0) scores 0 on every episode (no actual content is
all-zero).

## 3. Baseline definitions (frozen)

B1 MEM (pure memorization):
- Observes the 6 TRAIN episodes in order with answers revealed after
  each attempt.
- Stores (n -> (s1,l1,s2,l2)) on first observation of each n. A repeat
  observation of an already-stored n does not overwrite (frozen rule;
  does not occur in TRAIN).
- Key is the specifier count n only, per the task spec "store all seen
  (n -> structure) pairs".
- Prediction on (spec_sym, n, head): if n is in the table, emit the
  stored tuple; else emit failure (0,0,0,0). No generalization
  machinery of any kind.

B2 NN (nearest neighbor):
- Same stored table as B1 (same observations, same no-overwrite rule).
- Prediction: n* = argmin over stored n of |n - n*|; tie-break: the
  smaller stored n (frozen). Emit that entry's stored (s1,l1,s2,l2).
  Empty table emits failure (does not occur; TRAIN is nonempty).
- This is exact-structure copying from the closest seen n, not
  relation fitting: lengths are copied verbatim, never scaled.

B3 LEXH (exhaustive L search, independent reimplementation):
- Reimplements the 604 canonical L-expressions from the frozen spec:
  512 singles (all (c0,c1,c2) with ci in 1..8) plus 92 diagonal ALTs
  (ascending 1-, 2-, 3-element subsets of (k,k,k), k in 1..8).
- L prediction semantics from the prereg: given (spec_sym, n): if
  spec_sym == '#' and a branch with c0 == n exists (first such branch
  in canonical order), predict ('a'^c1, 'b'^c2); else failure.
- Check (a), impossibility verification: score every expression on
  E_1..E_12 (spec='#', head="ab", content a^n b^n, n=1..12); report the
  maximum and the first attaining expression. This must reproduce the
  builder's max604=3, computed here directly from episode semantics
  rather than the builder's shortcut.
- Check (b), oracle ceiling: score every expression on the 17
  experiment episodes (TRAIN 6 + HIDDEN 4 + EXTENDED 3 + TRANSFER 4);
  report the maximum, the first attaining expression, and that
  expression's per-phase breakdown. This is the strongest possible
  template predictor (chosen with full test knowledge); if it fails,
  no L-expression can do better.

## 4. Kill bars

- K-BL-1 (build/run): the program builds with the frozen toolchain
  (znc 2026.07.0-dev), exits 0 on every run, stderr empty.
- K-BL-2 (determinism): 3 consecutive runs byte-identical
  (shell cmp), md5 recorded.
- K-BL-3 (complete report): machine-readable SUMMARY lines for every
  baseline x phase, plus the B3 argmax lines and the verdict line.
- K-BL-4 (verdict rule, frozen here):
  - BASELINE-BEATS iff any baseline scores >= 4/4 on HIDDEN (matching
    the node's frozen generalization score), OR the B3 check (a) finds
    max over the 604 on E_1..E_12 != 3 (the builder's impossibility
    number does not reproduce; reported additionally as a governance
    issue against canonical evidence).
  - Otherwise BASELINE-MATCHES: every simple baseline scores strictly
    below the node on HIDDEN, confirming the builder's baseline story
    (the in-program bestL ablation scored 0/4). Exact per-phase
    numbers are reported regardless of verdict.
  - This verdict is a baseline-comparison verdict only. It is not a
    promotion: REPEXPAND-1 remains BUILD-PASS (reproduced), never
    SURVIVES, under either verdict.
- K-BL-5 (purity): pure Zag for implementation, compile, and runs
  (shell only for compile/cmp/md5); authored docs contain no em dash
  bytes (checked by byte scan).

## 5. Predicted (not frozen) numbers

These are expectations, not bars; the verdict follows section 4 only.

CORRECTION (2026-09-29, before any implementation existed): the TRAIN
predictions below were first written as 6/6 for B1/B2. That contradicts
the sequential protocol frozen in sections 2 and 3 (each TRAIN answer
is revealed only after the prediction attempt, and TRAIN n values are
all distinct, so the first attempt at each n necessarily misses). The
corrected expectations are TRAIN 0/6 for both B1 and B2. No bar,
definition, or verdict rule is changed; HIDDEN numbers (the ones the
verdict keys on) are unaffected.

- B1 MEM: TRAIN 0/6 (sequential protocol; each n novel at prediction
  time), HIDDEN 0/4 (9,11,15,17 unseen), EXTENDED 0/3 (13,20,30
  unseen), TRANSFER 1/4 (T1 n=4 seen and content matches; T3 n=3 seen
  but stored symbols (a,b) mismatch actual (x,y); T2/T4 unseen).
- B2 NN: TRAIN 0/6 (sequential protocol; ep0 table empty, later
  episodes copy the nearest earlier n and miss), HIDDEN 0/4 (all map
  to stored n=7, emitting (a,7,b,7)), EXTENDED 0/3, TRANSFER 1/4 (T1
  exact n=4; T3 exact n=3 key but symbol mismatch fails).
- B3 LEXH: check (a) max = 3 (any 3-diagonal ALT); check (b) max =
  3/17 (any 3-diagonal ALT covering 3 TRAIN n's; HIDDEN/EXTENDED n > 8
  are unreachable by branches capped at 8; TRANSFER unreachable via
  spec '$' and symbols x/y).

## 6. Honest limitations

- B1/B2 receive TRAIN answers under the same reveal protocol as the
  learner; this is the fair comparison (the learner also observed
  TRAIN answers, per its failure traces).
- The baselines do not attempt the CONTRADICTION/REVISE arc; the
  comparison targets the v1 generalization claim (HIDDEN/EXTENDED/
  TRANSFER), which is what step 5 must stress.
- B3 check (b) is an oracle ceiling, stronger than any deployable
  template baseline; its failure is sufficient but not necessary
  evidence.
