# Segmentation Architecture Review

Prereg: b89ec1477 (frozen before analysis).
Verdict: **REVIEW-COMPLETE.** All three kill bars pass.

## 1. Why the distributional lineage hits a ceiling

DEVANG2 (402e53d32 / 153e2af8e, bigram DP, 13/20), DEVANG3 (b2ceb6b38 /
e0d3a5e94, V3 TP plus lexicon-reuse, 16/20), and DEVANG4 (c73372286 /
d9ebbfe6d, merge pass plus negator-aware grounding, 16/20) are three
consecutive generations that repair adjacent edge cases while retaining
one representation: boundaries are decided in a single pass from corpus
string statistics, decoupled from consequence grounding. Each generation
added a researcher-authored repair (TP threshold, lexicon-reuse split,
merge pass, skip-grounding-after-"not") and each repair left NEG novel
at 0/3. This is the architecture-review trigger firing, not a tuning
problem.

The DEVANG4 diagnosis (d9ebbfe6d, K1 analysis) states the architectural
flaw plainly: grounding and negator learning are interdependent with
segmentation, but the pipeline runs segmentation first and grounding
second, so each pollutes the other. Five frozen failure facts:

1. "taknotgrn" segments as ["tak","not","g","r","n"]; "grn" never forms
   a lexicon entry (chicken-and-egg: fragments never recur as a unit
   because they are never segmented as a unit).
2. "not" neg_tot=13, neg_viol=4, is_negator=0; pair statistics need clean
   segments and do not get them.
3. "red" is mis-grounded by NEG episodes, which poisons the very pair
   statistics the negator detector needs.
4. Fragment counts are high ("r"=55), so no count or length filter
   separates fragments from words.
5. DEVANG4's own repairs are word-specific ("skip after not") and fail
   when "not" itself is fragmented ("takn","ot","red").

The deeper point: "not" is a semantic operator. It changes the mapping
from the words that follow it to consequences. No string statistic can
decide that "not" is special; only its effect on consequences can. A
boundary criterion that never consults meaning cannot discover a
meaning-driven unit, and every downstream statistic built on its output
inherits the blindness.

## 2. Hypotheses

### H1: Consequence-grounded segmentation

Mechanism. Boundaries are proposed from recurrence but kept or dropped
by consequence-prediction gain. Learner state: a set of candidate
units, each with a grounding record (which consequence features it
predicts, from past episodes only). Decision rule: a boundary between
A and B is kept iff treating A and B as separate units predicts episode
consequences better (lower prediction error on episodes seen so far)
than the merged unit; merged otherwise. No fixed TP threshold; the
criterion is prediction error, which is already the learner's objective.

How it addresses the failures. "not" survives as a unit because
treating it as a unit enables the negation mapping, which sharply
reduces prediction error on NEG episodes. "grn" merges from fragments
because the merged unit predicts the color feature while the fragments
do not. "red" mis-grounding is contained: a unit whose grounding
contradicts under negation scope gets its scope-specific record,
because the scope changes predictions.

Predicted residual failure. Consequences are sparse (one target per
utterance), so the boundary signal is weak early; wrong early
segmentations can lock in before enough episodes arrive. Credit
assignment for a single boundary among many is hard. H1 could also
over-merge units that jointly predict well but are semantically
distinct (e.g., "tak"+"not" if their conjunction is the best predictor
of flipped consequences).

### H2: Predictive boundary discovery

Mechanism. The learner maintains its own online next-character
predictor, trained causally on past observations only. A boundary is
placed at local maxima of prediction failure (surprise): the position
where the predictor's error is highest relative to its recent average.
Learner state: predictor parameters plus a short surprise history.

Difference from DEVANG3 TP, which this must not duplicate. TP is a
fixed corpus statistic with fixed Laplace smoothing and a frozen
threshold (-15). H2's surprise is relative to the learner's current
model, so the same string can be a boundary early and not a boundary
late; cold-start is handled naturally because an untrained predictor
is surprised everywhere, which degrades to single characters, the
same safe start the redesign used. Rare words get boundaries because
they surprise.

Predicted residual failure. H2 segments "not" correctly but still needs
a separate negator detector, so the interdependency problem is
untouched: pair statistics over H2 segments remain fragile under
fragmentation. H2 fixes segmentation adaptivity, not the semantic
operator problem. It is also still a surface criterion; a recurrent
meaningless trigram that is internally predictable gets no internal
boundaries and is effectively treated as a unit.

### H3: Recurrence/compression-based units

Mechanism. The lexicon is a compression codebook. Learner state: a chunk
inventory and the running code length of the corpus-so-far encoded with
it. Decision rule: a chunk is promoted when encoding it as one code
reduces total description length (codebook cost plus encoded corpus),
computed incrementally over past observations only. No frequency
threshold; a rare chunk promotes if its reuse pays for its code.

How it addresses the failures. "grn" promotes despite rarity because
each occurrence as one code is cheaper than three char codes; unlike
the TP threshold it needs no per-position statistic to cross a bar.
The chicken-and-egg is addressed by construction: the merged
hypothesis is evaluated as a hypothesis, not discovered by accident.

Predicted residual failure. Compression is still a surface criterion.
A recurrent meaningless filler promotes (it compresses), and "not"
promotes as a chunk but gains no negator semantics; the pair-statistic
problem persists unchanged. H3 also risks promoting long accidental
collocations ("taknot") if they recur, since they compress well.

### H4: Multi-level revisable chunks

Mechanism. Chunks live in a hierarchy and boundaries are revisable.
Split rule: a chunk splits when its fragments develop independent
grounding records (each fragment predicts distinct consequence
features across past episodes). Merge rule: adjacent segments merge
when their conjunction predicts a consequence feature better than
either alone, and neither has independent grounding. Learner state:
chunk tree plus per-chunk grounding records. Unlike H1-H3, a decision
made at episode 10 can be undone at episode 60.

How it addresses the failures. This is the only hypothesis where
segmentation and grounding are mutually causal in both directions.
"g","r","n" merge because their conjunction predicts color-2 while
the fragments predict nothing alone. "not" stays atomic because its
grounding (consequence-flip) is independent of its neighbors.
"tak"+"not" do not merge: "tak" grounds to the action, "not" to the
flip, so their groundings are independent and the merge rule blocks.
"red" mis-grounding is repaired by splitting the scope-specific
record rather than by a word-specific skip rule.

Predicted residual failure. The split/merge criteria can thrash if the
grounding records are noisy early; without a hysteresis or
evidence-count requirement, chunks could split and re-merge every few
episodes. It is also the most complex to implement in the memory
budget, and complexity is itself a failure mode (cf. DEVANG1 memory
corruption).

## 3. Discriminating battery

Frozen episode generator (seed 123456789), 100 train episodes, 20 test
utterances, strict one-pass online: no hypothesis may use future
episodes. DEVANG3/DEVANG4 is the frozen distributional control.

- T1 NEG-novel (frozen 3 items): predicted pass H1, H4; predicted fail
  H2, H3, control. Isolates the semantic-operator problem.
- T2 rare-word (grn/blu rare in train, in test): predicted pass H2,
  H3, H4; borderline H1; fail control. Isolates the rarity problem.
- T3 scope-shift: "not" applied to a novel word never seen under
  negation. Predicted pass H1, H4 (functional role generalizes);
  predicted fail H2, H3, control (pair statistics need the pair).
- T4 filler: a recurrent meaningless trigram injected across episodes
  with no consequence correlation. Predicted pass H1, H4 (no
  prediction gain, no shared grounding); predicted fail H3
  (compression promotes it); H2 acceptable (predictable, no internal
  boundary). Splits surface criteria from consequence criteria.
- T5 revision: mid-stream, a stable chunk's meaning splits (a new
  referent reuses an old form). Predicted pass only H4. Isolates
  revisability.
- T6 novel concatenation of known words (existing novel tests):
  predicted pass all; guards against regressions.

Prediction matrix:

| Test | H1 | H2 | H3 | H4 | Control |
|------|----|----|----|----|---------|
| T1 NEG-novel | pass | fail | fail | pass | fail |
| T2 rare-word | ? | pass | pass | pass | fail |
| T3 scope-shift | pass | fail | fail | pass | fail |
| T4 filler | pass | ok | fail | pass | ok |
| T5 revision | fail | fail | fail | pass | fail |
| T6 concat | pass | pass | pass | pass | pass |

T1 and T3 jointly discriminate {H1,H4} from the rest. T4
discriminates H3 from H1/H4. T5 isolates H4.

## 4. Recommendation

Implement **H4** first, with H1 as the fallback if H4's split/merge
thrashes in practice. Rationale: the frozen diagnosis is an
interdependency between segmentation and grounding, and H4 is the only
hypothesis that makes the dependency bidirectional and revisable.
H1 addresses the same root cause but retains the chicken-and-egg (it
needs segments to ground and grounding to segment) without a revision
mechanism. H2 and H3 are predicted by this review to repeat the NEG
failure, so building either as DEVANG5 would continue the repair
lineage under a new name.

Treadmill guard: H4's split/merge criteria must be stated as
prediction-gain comparisons, not as hand-tuned count or length
thresholds. Any constant that rescues a test item voids the run.

Falsification conditions for H4: (a) split/merge thrash rate exceeds
one revision per ten episodes after episode 50; (b) T1/T3 fail despite
correct segmentation of "not", which would show the semantic-operator
problem is in the negator detector rather than the segmenter; (c) H4
scores at or below the 16/20 control on the frozen 20. If (a) fires,
fall back to H1. If (b) fires, the review's root-cause claim is wrong
and the negator mechanism, not segmentation, is the next target.

## 5. Kill bar checklist

- K1 PASS: H1-H4 each specified with mechanism, decision rule, and
  learner state; each is implementable without new semantic cases.
- K2 PASS: Section 2 gives per-hypothesis failure analysis against the
  five frozen facts, each with at least one predicted residual
  failure.
- K3 PASS: Section 3 designs six tests; T1/T3, T4, and T5 make
  divergent predictions across hypotheses; the online constraint is
  enforced by construction.

## Files

- `PREREG_SEG_REVIEW.md`: frozen review plan (b89ec1477).
- `SEG_REVIEW.md`: this review.

No implementation was performed. No DEVANG5 is authorized by this
review; the implementer must preregister separately against the
discriminating battery in Section 3.
