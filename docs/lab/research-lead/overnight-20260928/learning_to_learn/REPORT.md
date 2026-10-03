# Learning-to-Learn Report

**Verdict: LEARNING-TO-LEARN-COMPLETE.**

**Date:** 2026-10-01
**Worker:** Learning-to-Learn Worker (Constitution Section 16)
**Commit:** local only, nothing pushed.

## 1. Question

Constitution Section 16: does TNN improve not only what it knows but HOW
it learns? Strong target: earlier experience leads to later unfamiliar
problems requiring fewer examples, less search, less compute, with causal
ablation proving prior learning produced the improvement, and the
improvement coming from learned learning strategies rather than merely
more facts.

## 2. Mechanism under test

The learned learning strategy is the LINK-ordered two-pass rebind from
the persistent-connections work (`105e9ee8b`): every verified rebind
writes a type-14 LINK edge from the newly promoted MAP to the helper MAP
whose shape was reused. Later queries try linked MAPs (the learner's own
prior successful constructions, newest first) before the id-order scan.
The LINK contents and resulting search order are determined by which
rebinds actually verify. The write rule and pass structure are
researcher-authored; the strategy instance is learner-built.

## 3. Design

Two task families, five problems each. Every problem is a fresh subject
with a taught plen-5 true path plus plen-3 and plen-4 distractor paths,
followed by one query. Literal ranges are disjoint across problems
(stride 300 exceeds the max distractor offset 203; a stride-100 pilot
showed duplicate-FACT path inflation in t2_gather and was fixed before
measurement).

- **Treatment:** Family 1 (subjects 101-105), 20-event interference gap,
  Family 2 (subjects 201-205, fresh literals).
- **Fresh:** distractors then Family 2 only. Same binary, no Family 1.
- **Ablated:** Family 1, then `pc_del_links` (LINK14 6 to 0, MAP facts
  retained), then Family 2. New rebinds during Family 2 may write fresh
  links, which measures strategy re-learning.

Per-problem metrics from the transcript: `rb_tried`/`rb_rej` (rebind
search, stashed in unused header fields 56/60 by 2 lines of
behavior-neutral instrumentation), `trial` (1 if the blind trial ran,
detected by header-16/last-phase stats differing from rebind stats;
verified against raw RB-STAT lines, no coincidental equalities, zero
ACT-HITs), `total` (verifies = compute).

3/3 byte-identical runs per arm (SHA-256 verified), all exit 0, all
answers correct in all arms (accuracy 100% everywhere; the effect is
purely on learning cost).

## 4. Results

Per-problem total verifies:

| Problem | Treat F1 | Treat F2 | Fresh F2 | Abl F1 | Abl F2 |
|---|---|---|---|---|---|
| P0 | 16 (trial) | 1 | 16 (trial) | 16 (trial) | 11 |
| P1 | 11 | 1 | 11 | 11 | 1 |
| P2 | 1 | 1 | 1 | 1 | 1 |
| P3 | 1 | 1 | 1 | 1 | 1 |
| P4 | 1 | 1 | 1 | 1 | 1 |
| **Family total** | 30 | **5** | **30** | 30 | **15** |

LINK14 census: treat 2 to 6 to 11; fresh 2 to 6; abl 2 to 6 to 0 to 5.

### 4.1 Experience reduces later learning cost: 30 to 5

Family 2 costs 5 verifies with Family 1 experience versus 30 fresh, a 6x
reduction. The within-family learning curve (16 to 11 to 1) is identical
in treat-F1 and fresh-F2: the learner acquires the retrieval strategy at
the same rate. The difference is that treatment starts Family 2 with the
strategy already built.

### 4.2 Examples-to-criterion

Criterion: solve a new problem with at most 2 verifies and no trial.

- Treatment: criterion reached after 2 Family-1 examples (P0 16, P1 11,
  P2 onward 1). Family 2 needs **0 additional examples**.
- Fresh: 2 examples to reach criterion in Family 2 (starts over).
- Ablated: 1 example to re-reach criterion after link deletion
  (F2-P0 11, F2-P1 onward 1).

### 4.3 Ablation proves the strategy, not the facts, is causal

The ablation arm holds every Family-1 MAP fact but no LINKs. Its F2-P0
costs 11 verifies versus treatment's 1: identical facts, the only
difference is the recorded retrieval strategy. Family 2 total rises 5 to
15. MAP possession alone does not explain the speedup; the learned
search order does. The strategy then re-learns from one expensive
experience (11 to 1), and the fresh link census (0 to 5) shows the
rebuild.

## 5. Honest boundaries

1. The two families are structurally identical (plen-5 chains) and differ
   only in surface literals. This tests transfer of a learned retrieval
   strategy to new instances, not learning-to-learn across different
   problem shapes.
2. The "strategy" is simple: retry own prior successful constructions
   newest-first. It is not a learned abstract rule about learning.
3. The update rule (write LINK on verified rebind; Pass 1 before Pass 2)
   is researcher-authored. Learner-owned: which links exist, the
   resulting order, all cost reductions.
4. Scale is 5+5 problems. The 100-problem regime and sublinear retrieval
   are not tested here (see the rebind-hardening scale finding).
5. Verification still arbitrates every candidate; the strategy changes
   only search order, never correctness.

## 6. Standing metrics

- RESEARCHER-OWNED: LINK write rule, two-pass order, family/criterion
  definitions, instrumentation fields.
- LEARNER-OWNED: all LINK edges, search order per query, all
  examples-to-criterion values, re-learned links in ablation.
- COGNITION LINES added: 0 to the mechanism (verbatim from `105e9ee8b`);
  5 lines instrumentation + ~100 lines driver.
- MODES/BRIDGES/HANDLERS/SEMANTIC CASES: 0/0/0/0.

## 7. Deliverables

All in `docs/lab/research-lead/overnight-20260928/learning_to_learn/`:
NAMECHECK.md, REPORT.md, `l2l_base_trim.zag` (byte-identical to the
persistent-connections build input), `l2l_patch.zag`,
`l2l_driver_{treat,fresh,abl}.zag`, `l2l_full_{treat,fresh,abl}.zag`,
binaries, compile logs, 9 run transcripts (3/3 SHA-256 identical per
arm).
