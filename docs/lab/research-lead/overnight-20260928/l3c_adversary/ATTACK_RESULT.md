# L3C-ADVERSARY Phase 2: Attack Results

Date: 2026-09-30. Attack source: l3c_attack.zag (commit 7af24029e).
Protocol status: UNMODIFIED. Lines 1-311 of l3c_attack.zag are
byte-identical to lines 1-311 of the committed l3c_form.zag
(verified by diff before the prereg commit; only fn main() replaced).
Binary l3c_attack_bin built fresh from that source with the pinned znc.
Two runs: byte-identical (determinism 2/2).

## Results vs frozen predictions

### Family A (sig 501): conjunction needed. PREDICTED HONEST FAIL. CONFIRMED.
- Actual: events=2, built=0, unresolved=2, eval=2/4. Matches prediction
  exactly. disc() finds no single-feature separator; construct() returns
  -1 twice; clash evals fail. The protocol fails honestly here.

### Family B (sig 502): threshold needed. PREDICTION MISSED ON MECHANISM; ACTUAL FINDING STRONGER.
- Predicted: events=2, built=0, unresolved=2, eval=2/4 (assumed disc sees
  both clash vectors).
- Actual: events=2, built=1, unresolved=0, eval=3/4.
- Root cause (white-box, confirmed by trace): construct() fires on the
  FIRST clash observation, when only one clash vector is stashed (cc=1).
  disc() therefore finds (f1==9) from a single sample and builds the
  dispatch eagerly. The second clash vector (f1=10) then contradicts the
  built dispatch: observe() takes the DISP branch, interp() misses,
  events increments, return code 2, and no construction is possible.
- The eval pattern (the f1=9 clash passes via the labeled edge, the f1=10
  clash fails via the default) uniquely identifies the built separator
  as (f1==9), derived from the deterministic trace.
- Reading: EAGER OVERFIT THEN DEAD END. The protocol commits to a
  separator from n=1 clash observation (maximal overfitting) and then
  cannot revise or extend when the next observation contradicts it. This
  is a worse failure than the predicted honest fail: the monitor fires,
  a dispatch exists, and the contradiction is unresolvable.

### Family C (sig 503): nested dispatch. PREDICTED SILENT DEAD END. CONFIRMED
  (event count 3, not 4; substantive prediction holds).
- Actual: events=3, built=1, unresolved=0, rc_nested=2,2, eval=4/6.
  (The second clash1 vector is consistent post-construction, so no event;
  my predicted 4 double-counted it. The substantive bars all hold.)
- The two nested contradictions return code 2: counted as events, never
  constructed, never flagged unresolved, and their feature vectors are
  not even stashed (the DISP branch of observe() records nothing).
  The contradiction persists permanently and silently.

### Family D (sig 504): underdetermined separator. PREDICTED SILENT MISRESOLUTION. CONFIRMED
  (events=1, not 2; substantive prediction holds).
- Actual: events=1, built=1, rep=(1,1), held-out 2/4 with exactly the two
  predicted silent misresolutions:
  FAM_D HELDOUT_MIS f=(3,1,5,7) true=2 (protocol gives 0)
  FAM_D HELDOUT_MIS f=(3,0,9,7) true=0 (protocol gives 2)
- Both (f1==1) and (f3==9) were consistent with every observed vector;
  disc() returned the first scan-order hit. "Discovery" is first-hit
  luck; the protocol cannot represent underdetermination.

### Family E (sig 505): stash-window forgetting. PREDICTED SILENT MISRESOLUTION. CONFIRMED
  (events=1, not 2; substantive prediction holds).
- Actual: events=1, built=1, rep=(1,1), observed-eval 4/5 with exactly the
  predicted silent misresolution:
  FAM_E FORGOTTEN_MIS f=(3,1,0,7) true=2 (protocol gives 0)
- The third training vector is never stashed (stash keeps 2 per class),
  so disc() builds (f1==1), contradicting actually-observed training
  data. The discriminator reasons over a 2-vector window, not the history.

### Totals
Actual: events=9, built=4, unresolved=2. (Predicted 12/3/4; the delta is
entirely the post-construction consistency of repeated clash vectors,
plus Family B's eager-construction mechanism. No substantive prediction
about resolution behavior was wrong in the protocol's favor.)

## Verdict: L3C-ADVERSARY-PROTOCOL-SMUGGLING-PROVEN

The fixed protocol is a conditional constructor in disguise. The
conditional FORM (single-level dispatch: if feature==value then new else
old) is written by the researcher in construct()'s fixed six-op emission
and interp()'s fixed label matching; the learner selects no form and
varies none. What is data-driven is only the (feature, value) parameter
pair, i.e. parameter fitting of a supplied template. The breaking
exhibits:

1. Family C (principal structural exhibit): the protocol cannot
   represent nested dispatch. observe()'s DISP branch has no
   construction path and stashes nothing. Exact protocol change forced:
   stash contradicting vectors on the DISP branch and add recursive
   construction that re-points an EDGE target (construct() currently only
   re-points the rule slot).
2. Family A (expressiveness exhibit): conjunctions are inexpressible.
   Exact protocol change forced: conjunctive edge labels (schema change
   in op_label_edge plus AND-matching in interp()) or nested DISP
   emission in construct().
3. Family B (eagerness exhibit): the protocol commits to a separator from
   a single clash observation and then dead-ends on the next one. Exact
   protocol change forced: deferred/evidence-accumulating construction,
   plus a revision path for built dispatches.
4. Family D: first-hit scan order resolves underdetermination by fiat.
   A genuinely generic discriminator would need ambiguity representation.
5. Family E: the 2-vector stash window lets "discovery" contradict
   observed history. A generic learner would need unbounded (or
   principled) observation memory.

## Boundary map (what the fixed protocol genuinely handles)

Single-level, single-feature-equality contradictions where every clash
observation shares the first clash vector's separator, with at most two
training vectors per class. Within that class it genuinely discovers
(fi,fv) from data with no per-family source change (the builder's
families 1 and 2). Outside that class it fails honestly (A), overfits
then dead-ends (B), dead-ends silently (C), or misresolves silently
(D, E). The template never adapts.

## Honest-scope note

This kills the "emergent conditional form" reading, not the mechanism's
bounded utility: as a fixed-template conditional constructor with
data-driven parameter discovery it is a clean bounded-L2 mechanism, and
Phase 1 confirms the reported numbers reproduce byte-identically. The
builder's own honest scope (NOT L3, NOT Criterion 0) is sustained and
narrowed: the discriminator and construction protocol are the
researcher-supplied conditional constructor.

## Kill bars

- K1: Phase-1 reproduction report committed (7fae6a188) before any
  Phase-2 attack file existed. PASS.
- K2: all four required families (a)-(d) plus bonus (e) run against the
  UNMODIFIED protocol (verbatim verified by diff), outcomes vs frozen
  predictions reported above. PASS.
- K3: pure Zag, zero Python, no em dashes (shell-only check_no_dash.sh).
  PASS.

## Recommendation

Retire the "emergence" claim for this lineage and do not promote it as a
C0-A candidate. The productive next step is a protocol v2 in which the
DISPATCH FORM ITSELF is constructed: replace the fixed six-op construct()
with a recursive constructor that can emit nested dispatch (Family C is
the forcing exhibit), and replace the first-hit disc() with a
discriminator that searches a genuinely compositional predicate space
(conjunctions, then inequalities). The v2 prereg must include Families
A-E as frozen falsifiers: v2 passes only if it resolves C without a
per-family source change. Do not attempt v2 by widening the fixed
template (more label slots, more scan features); that repeats the
downgraded pattern.
