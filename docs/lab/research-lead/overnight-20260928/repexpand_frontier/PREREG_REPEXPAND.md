# PREREG REPEXPAND-1: Representational expansion via coupled-count invention

Frozen: 2026-09-29. This prereg is committed alone before any implementation,
attack, or run for REPEXPAND-1. Pure Zag. No Python at any stage.

## 1. Objective

Test Micah's mandatory L3 Criterion 0: the learner must create or recruit a
representational primitive, operator, decomposition, procedure-building
construct, or internal structural form that was NOT already expressible as one
of the frozen researcher-enumerated solution families.

NOT L3 (frozen negative examples): researcher supplies ADD/SUB/K/N DSL and the
learner searches compositions; researcher supplies SPLIT/MERGE/FORM and the
learner chooses where to apply them.

Potential L3 (what this experiment tests): the current language cannot
represent a repeated observed transformation; the learner detects the
representational inadequacy, creates primitive P, P compresses and explains the
observations, P solves hidden cases, P is reused, P transfers to a changed
surface domain, and ablating P removes the advantage.

## 2. World

An episode presents an observed context and hides content the learner must
predict exactly.

Observed context: (spec_sym, n, head[2]).
- spec_sym: one byte, '#' (35) or '$' (36). A run of n copies is observed.
- n: positive integer, the specifier count.
- head[2]: two bytes naming the content alphabet, e.g. "ab" or "xy".

Hidden content: two runs (s1^l1, s2^l2). The learner must output
(s1, l1, s2, l2) exactly. Scoring is exact match on all four fields.

Some episodes carry an unscored trailing distractor run (z^m). Distractors
test that the created primitive couples selectively; they never affect scoring.

## 3. Frozen base language L

L is the bounded-template predictor family, frozen as follows.

- An L-expression is an ALT of 1 to 3 branches.
- A branch is a fixed triple (c0, c1, c2) with each ci in 1..8, plus fixed
  symbols (spec '#', content 'a', 'b').
- Prediction semantics: given observed (spec_sym, n): if spec_sym == '#'
  and a branch with c0 == n exists (first such branch in canonical order),
  predict content ('a'^c1, 'b'^c2). Otherwise predict nothing (failure).
- Canonical enumeration used by the learner and the impossibility check:
  512 singles (all (c0,c1,c2) with ci in 1..8) plus 92 diagonal ALTs
  (all 1-, 2-, 3-element subsets of diagonal triples (k,k,k), k in 1..8).
  Total 604. Off-diagonal ALT combinations are excluded by Lemma 2 below.
- Conceptual type tags: ATOM=1, SEQ=2, REPK=3, ALT=4. Every L predictor is a
  normal form over these. All counts in L are frozen constants. L has no
  production with a runtime-bound parameter slot.

L is intentionally the strongest L2 baseline for this task shape: memorized
templates with alternation. Section 4 proves its limitation is qualitative
(any finite template count fails on the infinite family), not a matter of the
frozen constant 3 or the frozen range 1..8.

## 4. Impossibility proof (frozen before learning)

Target family E_n = (spec='#', n, head="ab", content a^n b^n) for n >= 1.

Lemma 1. A branch (c0,c1,c2) predicts E_n correctly iff c0==n, c1==n, c2==n.
Proof. The branch is selected iff spec_sym=='#' and c0==n. Its prediction is
'a'^c1 followed by 'b'^c2, which equals a^n b^n iff c1==n and c2==n.

Lemma 2. A branch whose triple is not all-equal is never correct on any E_n.
Proof. Correctness on E_n requires c0==c1==c2==n by Lemma 1.

Theorem. No L-expression predicts all of E_1..E_12 correctly, hence no
L-expression solves the infinite target family.
Proof. By Lemma 2 only diagonal branches can be correct on any E_n. By
Lemma 1 each diagonal branch (k,k,k) is correct on exactly one E_n (n=k).
An L-expression has at most 3 branches, so it is correct on at most 3 of
E_1..E_12. 3 < 12.

Computational check (K-RX-1): the frozen program scores all 604 canonical
L-expressions on E_1..E_12 and reports the maximum. The bar requires max < 12.

## 5. Frozen episode lists (no randomness anywhere)

- TRAIN (LEARN phase, creation allowed): spec='#', head="ab",
  n in [2,3,5,7,4,6], content a^n b^n. 6 episodes.
- HIDDEN (FROZEN phase, no creation): spec='#', head="ab",
  n in [9,11,15,17], content a^n b^n. 4 episodes. Disjoint from TRAIN.
- EXTENDED (FROZEN phase, unboundedness probe): spec='#', head="ab",
  n in [13,20,30], content a^n b^n. 3 episodes.
- TRANSFER (FROZEN phase): 4 episodes.
  T1: spec='$', n=4, head="ab", content a^4 b^4.
  T2: spec='$', n=9, head="ab", content a^9 b^9.
  T3: spec='#', n=3, head="xy", content x^3 y^3, distractor z^2 (unscored).
  T4: spec='#', n=8, head="xy", content x^8 y^8, distractor z^5 (unscored).
- CONTRADICTION (REVISE phase, creation allowed as supersession):
  spec='#', head="ab", n in [3,6,4], content a^n b^(2n). 3 episodes.
- FOLLOWUP (REVISE phase): spec='#', head="ab", n in [5,7],
  content a^n b^(2n). 2 episodes.

## 6. Learner design

Researcher-supplied machinery (NOT the claimed invention; this is the generic
structural-growth substrate):

a. bestL: the highest-scoring canonical L-expression on training episodes seen
   so far (score = exact predictions; tie-break: fewer branches, then lowest
   canonical index). Recomputed per episode from the frozen 604. Diagonal
   candidates only (justified by Lemma 2).
b. Primary hypothesis: the newest active created node if one exists,
   otherwise bestL.
c. Failure monitor: counts consecutive primary-hypothesis failures and keeps
   a ring buffer of the last 8 failures with features
   (l0, l1, l2, h0, h1, s1, s2): observed spec length, true content lengths,
   head symbols, true content symbols.
d. Generic relation search: over the last F=3 failures (F frozen). For each
   content run j in {1,2}, with l0 the observed spec length:
   - EQ if lj == l0 on all 3 failures;
   - else MUL(q) if lj == q*l0 with integer q >= 1 constant on all 3;
   - else ADD(d) if lj - l0 == d constant on all 3;
   - else NONE. Checked in the fixed order EQ, MUL, ADD.
   Symbol rule: sj == h[j-1] on all 3 failures (binds content symbol slots
   to head positions, not to literal bytes).
e. Reification: if both runs yield a length relation and both symbol rules
   hold, allocate a new node of type COUPLED (tag 7, outside L's {1,2,3,4}):
   {src run 0, (dst1, rel1, const1), (dst2, rel2, const2), symbol slots bound
   to head positions, version, status active}. Emits TRACE-CREATE with the
   episode index, the discovered relation, and the evidence count (== F).
f. Revision: the same trigger firing on later failures creates a new version
   that supersedes the old; the old node is retired with TRACE-RETIRE
   naming the reason and the superseding version.
g. Phase permissions: LEARN: creation allowed. HIDDEN, EXTENDED, TRANSFER:
   frozen (no creation). REVISE: creation allowed (supersession only in
   practice). ABLATION: separate learner instance with growth disabled.

Prediction with a COUPLED node: given observed (spec_sym, n, head): emit
(head[0]^len1, head[1]^len2) where lenj = apply(relj, n). The node keys on
run positions (spec run = run 0), never on the literal spec byte.

## 7. What counts as learner-created (the L3 claim under test)

The COUPLED node type: a grammar production with runtime-bound parameter
slots (content lengths computed from the observed l0 at prediction time).
It is absent from L's frozen productions; by the Theorem no composition of
L's constant-count templates can cover the family. The specific relation
(EQ vs MUL vs ADD and its constant) is determined by residual data, not by
the researcher: the same code path must yield (EQ,EQ) on TRAIN residuals and
(EQ,MUL(2)) on CONTRADICTION residuals.

## 8. Kill bars (all evaluated by the frozen program; all must PASS)

- K-RX-1 impossibility: max over the 604 L-expressions on E_1..E_12 < 12.
- K-RX-2 creation: at least one node created with type tag outside {1,2,3,4};
  TRACE-CREATE present with episode index, discovered relation, evidence == 3.
- K-RX-3 hidden success: learner with the created node scores 4/4 on HIDDEN
  and 3/3 on EXTENDED.
- K-RX-4 ablation: growth-disabled learner scores <= 1/4 on HIDDEN.
- K-RX-5 reuse and transfer: 4/4 on TRANSFER; total node-assisted exact
  predictions across all phases >= 10.
- K-RX-6 revision: v1 retired (TRACE-RETIRE present) and v2 created with a
  different relation (MUL(2) on run 2); 2/2 on FOLLOWUP.
- K-RX-7 determinism: 3/3 byte-identical raw outputs (checked by the shell
  harness with cmp).
- K-RX-8 purity: pure Zag (no Python at any stage); documentation contains
  no em dash bytes (checked by byte scan).

BUILD-PASS iff K-RX-1 through K-RX-8 all PASS. The builder reports
BUILD-PASS or BUILD-FAIL only and does not promote to SURVIVES.

## 9. Pre-registered defense against the "disguised menu" objection

Objection: the EQ/MUL/ADD relation templates are a researcher-enumerated menu
of solutions, so creating COUPLED is L2 menu selection.

Response, frozen here for the independent adversary to attack:
(a) the templates are generic binary relations over observed features, not
solution structures; (b) the reified production (runtime parameter binding
across run positions) has no counterpart in L's frozen grammar; (c) the same
code path produces different node contents for different residuals
((EQ,EQ) vs (EQ,MUL(2))), so the node content is data-determined; (d) the
ablation (K-RX-4) shows the advantage comes from the created node, and the
memorization control (bestL, an ALT of templates) scores 0/4 on HIDDEN.

## 10. Honest limitations (frozen)

- The world is synthetic and small; L is the bounded-template family by
  design. The claim under test is representational expansion (a new
  production with runtime-bound parameters), not task difficulty.
- Transfer changes the specifier byte, the content alphabet, and adds
  distractors, but preserves the abstract shape (spec run + 2 content runs).
- The relation search is restricted to source = the observed run and the
  relation family {EQ, MUL, ADD}; a world needing another relation would not
  trigger creation. This is a documented boundary of the growth machinery,
  not a hidden solution menu: the search space is generic over feature
  pairs, and the discovered relation content is data-determined.
- Prediction operates at the run-structure level (symbol, length) pairs,
  which exactly determine the sequences; this is the level where the
  representational expansion occurs.
