# Segmentation Architecture Review 2: The Operator Representation

Commissioned by the treadmill-watch trigger after DEVANG-H1 BUILD-FAIL
(4c753a9db). This review makes no new empirical claims; it analyzes
committed results only. Review only; no implementation performed.

Prior review: `SEG_REVIEW.md` (prereg b89ec1477), which recommended H4
first with H1 as fallback, predicted H2/H3 would repeat the NEG
failure, and set falsification conditions for the lineage.

## 1. Frozen empirical record

| System | Commit | T1 NEG-novel | Test acc | "not" segments | is_negator |
|--------|--------|--------------|----------|----------------|------------|
| DEVANG2 | 402e53d32 | 1/3 (K3) | 13/20 | n/a | 0 |
| DEVANG3 | b2ceb6b38 | 0/3 | 16/20 | fragmented contexts | 0 |
| DEVANG4 | d9ebbfe6d | 0/3 | 16/20 | atomic, but pair stats polluted | 0 |
| DEVANG-H4 | 5c2f64857 | 0/3 | 14/20 | atomic (good) | 0 |
| DEVANG-H1 | 4c753a9db | 0/3 | 13/20 | atomic (good) | 0 |
| C2 control | (frozen) | n/a | 17/20 | n/a | n/a |

Five consecutive systems, three segmentation regimes (bigram DP, TP
plus lexicon-reuse, TP plus merge pass, H4 revisable chunks, H1
prediction-gain), one invariant: T1 0/3 everywhere after DEVANG2, and
is_negator("not") = 0 in every system that reports it. Scores decline
16/20 to 14/20 to 13/20 across the review lineage while the frozen
simple control C2 scores 17/20, beating every learner.

## 2. What H4 and H1 tested, and what each found

H4 tested bidirectional revisability: chunks split when fragments
develop independent grounding, merge when their conjunction predicts
better. Finding: the merge mechanism never fired (thrash 0, stable but
inert). Root cause was candidate generation, not the split/merge
criteria: candidates came only from runs of 3+ single-char fragments,
TP rarely emits clean fragment runs, so "grn" never entered the
lexicon and never got grounding. The bootstrap problem: the mechanism
needs the merged unit to have clean grounding to fire, but the unit
only gets grounding if segmented as a whole, which requires the merge
to have fired.

H1 tested consequence-prediction gain over candidates from ALL
adjacent pairs, fixing H4's bottleneck. Finding: merges fire (35 in
episodes 50-99) but the criterion is insufficient. Candidate explosion:
every adjacent pair becomes a lexicon entry, 96/96 full, dozens of
cnt=0 junk candidates crowd out real words. Myopic gain/loss on one
target per utterance cannot distinguish true predictive units from
noise ("grn" loss=1 rejected, "bal" loss=4 rejected). SIZE regressed
3/3 to 0/3. The H4 bootstrap is fixed and replaced by a worse failure.

The common finding, and the important one: in BOTH systems "not"
segments atomically, yet is_negator stays 0 and T1 stays 0/3. The H1
builder's diagnosis states it plainly: "Without is_negator=1, T1
cannot pass regardless of segmentation." The H1 builder also found
that [g] carries correct color-2 grounding, so the content side is
not the blocker either. The blocker is the negator detector.

## 3. Falsifier (b) fires: the root-cause claim must be revised

The prior review set this falsification condition for H4: "(b) T1/T3
fail despite correct segmentation of 'not', which would show the
semantic-operator problem is in the negator detector rather than the
segmenter."

Condition (b) has now fired twice, under two independent segmentation
regimes. Per the review's own logic, the semantic-operator problem is
in the negator detector rather than the segmenter.

This revises the prior review's section-1 root-cause claim. That
claim was: grounding and negator learning are interdependent with
segmentation, but the pipeline runs segmentation first and grounding
second, so each pollutes the other. The claim is not false, but it is
incomplete in the way that matters: it located the binding constraint
in the segmentation half of the interdependency. Two experiments have
now fixed the segmentation half (atomic "not") and T1 did not move.
The binding constraint is the operator half. A third segmentation
hypothesis cannot be the fix for a detector-side binding constraint.

## 4. Is the current representation itself wrong?

Answer: the operator/grounding representation is wrong; the
segmentation representation is not the binding constraint.

Evidence the segmentation representation is not binding: "not"
isolates as an atomic unit under TP+merge (H4), under
prediction-gain merging (H1), and was already atomic in DEVANG4's
test traces. Three regimes, same isolation. The residual
segmentation failures ("grn" fragments) are real but secondary: with
is_negator=0, T1 fails regardless of how "grn" segments.

The operator representation is wrong in three specific ways:

(a) Single-primary grounding. Each word carries one primary
consequence feature, learned across affirmative and negated
episodes alike. Negated contexts contaminate the primary. The only
fix in the lineage is the researcher-authored "skip grounding after
not" rule: a dedicated semantic case keyed on a word identity. It
fails when "not" itself fragments, it cannot generalize to an
undiscovered operator, and it is exactly the kind of pre-training
semantic branch that the mandate's C0-A would kill on sight.

(b) Pair-statistic operator detection. "not" earns is_negator=1 only
when ("not", X) pairs show X's primary violated at a 70% rate, where
X must be a clean single segment with a correct primary. In NEG
episodes with novel words, X is fragmented and its primary is
polluted, so the detector's preconditions are unsatisfiable exactly
in the episodes where the operator is active. The detector tries to
learn a semantic operator from surface adjacency statistics.

(c) Operator as word flag. The ontology contains words, consequence
features, and adjacency. It contains no scope object and no
interpretation-function object. But "not" IS a function over
interpretation: it maps the consequence prediction of its scope
span. An ontology without scope cannot represent an operator as
what it is; it can only approximate it as a flagged word plus
statistics over neighbors. This is the representational gap, and no
segmentation hypothesis in H1-H4 touches it, because segmentation
hypotheses by construction only repartition the character stream.

## 5. Why H2 would be the treadmill

The prior review predicted H2 "segments 'not' correctly but still
needs a separate negator detector, so the interdependency problem is
untouched" and would repeat the NEG failure. H4 and H1 have now
empirically confirmed the mechanism behind that prediction, twice:
atomic "not", is_negator=0, T1 0/3. H2 addresses segmentation
adaptivity (relative surprise vs fixed TP threshold). Sections 2-4
show segmentation adaptivity is not the binding constraint. Building
H2 would be a third hypothesis in the same lineage aimed at a
non-binding constraint, teaching nothing the two failures have not
already taught. The treadmill watch forbids exactly this. Do not
build H2.

## 6. Path forward: the operator/scope representation

The next mechanism must represent what "not" is: a scope-taking
operator over interpretation. Design requirements for the eventual
builder (to be preregistered separately, not implemented here):

R1. Compositional interpretation over spans. The learner maintains
an interpretation function applied to spans, with a span combiner.
The combiner itself is generic machinery; what is learned is the
operator inventory, not the word flags.

R2. Operator discovery from systematic prediction residuals. When a
recurring word form's presence systematically inverts or shifts the
predicted consequence features of the following span relative to
that span's standalone record, the learner proposes an operator
hypothesis bound to that form. Discovered after experience, not a
researcher "skip after not" rule. The proposal must be falsifiable:
it is kept only if it reduces prediction error on episodes seen so
far.

R3. Scope-conditioned grounding. Each unit keeps per-context
grounding records (default context plus one record per active
operator hypothesis), learned from episodes. No researcher-authored
scope rules; the contexts are the discovered operators from R2.

R4. Frozen falsifiers for the builder's prereg: (F1) T1 NEG-novel
passes with a white-box operator record present in persistent
learner state, bound to the "not" form, created after experience;
(F2) T3 scope-shift passes, showing the operator role generalizes
to a novel word; (F3) source audit shows no word-specific branches
for negation (no "skip after not", no is_negator flag keyed on
identity); (F4) ablation: removing the operator record destroys
T1; (F5) score meets or beats the 16/20 baseline without
regressing K6 SIZE.

Honest scope and open risks. This is researcher-designed
operator-discovery machinery, a bounded L2 direction, not L3: the
discovery criterion, the span combiner, and the record structure
are researcher-authored. The consequence signal is sparse (one
target per utterance); whether it suffices for operator discovery
is an open empirical question this design must face, not assume.
If F1 fails while F3/F4 pass (operator found but T1 still fails),
the signal-sparsity hypothesis, not the representation, is the
next target.

## 7. Kill bar checklist

- K1 PASS: H4 and H1 failures analyzed against the frozen record
  (sections 1-2); the common finding (atomic "not", is_negator=0,
  T1 0/3) identified as the decisive evidence.
- K2 PASS: the representation question answered (section 4): the
  operator/grounding representation is wrong in three specified
  ways; the segmentation representation is not the binding
  constraint, with evidence.
- K3 PASS: path forward specified (section 6, R1-R4 with frozen
  falsifiers F1-F5); H2 explicitly excluded as the treadmill
  (section 5); no third segmentation hypothesis authorized.

## Files

- `SEG_REVIEW2.md`: this review.
- Prior: `SEG_REVIEW.md`, `PREREG_SEG_REVIEW.md` (unchanged).

No implementation performed. No DEVANG5 authorized by this review.
The operator/scope builder must preregister separately against R4.
