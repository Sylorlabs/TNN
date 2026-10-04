# DEVINT-CLA2 Unimplemented-Elements Triage

**Date (UTC):** 2026-09-30
**Worker:** DEVINT-CLA2 Unimplemented-Elements Triage Worker
**Verdict target:** DEVINT-TRIAGE-COMPLETE

## Inputs

- Prereg: `devint_cla2_prereg/PREREG_DEVINT_CLA2.md` (commit `f24063bcb`)
- Red team: `devint_cla2_redteam/DEVINT_REDTEAM_REPORT.md` (commit `a5ccb100d`)
- Implementation: `devint_cla2_build/devint_cla2.zag` (commit `35f9500b2`)
- Report correction: commit `a003bd19b` (M2 claim retracted, F4 qualified)
- Method: read-only source audit. All definition/call-site claims below were
  verified with shell grep against the implementation. No code was written or
  executed. No Python invoked.

## The six elements

### E1. M2 bid-vs-survival metric

**Specified (prereg section 6, M2):** After S10 eviction, partition surviving
vs evicted nodes by signed evidence bid. Metric: fraction of nodes with
bid >= 2 surviving vs fraction with bid <= 0 surviving. Retention is
evidence-driven (not positional) iff the high-bid survival rate exceeds the
low-bid rate by >= 40 points. Also verify zero positional-attractor signature
(F1).

**Built (verified):** `m2_check` is defined at line 663 of `devint_cla2.zag`
and never called anywhere in the file. The BUILD_REPORT's "M2 holds" claim was
retracted by correction commit `a003bd19b`: the frozen metric was never
computed. GROUPs survived S10 via harness-authored PROTECT edges, not via bid.

**Scientific importance: HIGH.** M2 is the empirical test of the
"evidence-driven retention" claim, one of the four frozen claims under test
(workspace expressiveness, revision locality, retention policy, developmental
persistence). Falsifier F4 states: S10 eviction occurs but M2 shows no
bid-vs-survival correlation, then REJECT the implementation (core smuggling).
The red team additionally found genuine retention fragilities (evidence-cascade
eviction: unprotected bid-0 evidence nodes evict first, rule SUPPORTS edges
vanish, rule bids collapse to 0, and the positional tie-break in `evict_one`
then kills low-id rules). An honest M2 measurement may FAIL, which is itself
high-value: it would localize the retention pathology instead of leaving it
latent.

**Implementation difficulty: MODERATE** for the measurement itself (the
function is already written; it needs call-site wiring and honest reporting).
The follow-on risk is LARGE: if M2 fails, the retention routine needs
hardening (protect evidence nodes or make rule bids robust to evidence loss;
remove or justify the positional tie-break; make demotion propagate to
retention priority), per the red team's recommendation 2.

### E2. S10 post-eviction accuracy on 10 held-out episodes

**Specified (prereg section 5, S10 check):** "post-eviction next-concept
prediction accuracy on 10 held-out episodes measured," alongside eviction
occurring and high-bid structures surviving at a higher rate.

**Built (verified):** `stage_s10` checks only eviction count and GROUP
survival. No post-eviction prediction accuracy is measured on any held-out
episodes.

**Scientific importance: MODERATE-HIGH.** This is the functional-consequence
test of eviction: M2 measures which structures survive (the correlation); this
measures whether the surviving structure still works (capability preserved).
Without it, we know high-bid things survived but not whether the system can
still predict after pressure. It does not block a structural claim the way E1
does, but it blocks the functional claim that eviction preserves useful
knowledge.

**Implementation difficulty: LOW-MODERATE.** The prediction machinery exists
(it is exercised in S11 recognition). The work is measurement wiring: freeze
10 held-out episodes, run next-concept prediction before and after the S10
eviction, report both accuracies as exact integers.

### E3. S6 examples-to-criterion (and the M1 synergy metric)

**Specified (prereg section 5, S6 check):** "Record examples-to-criterion."
(Prereg section 6, M1): run S6 procedure induction twice in the same process,
once with GROUP-node concept vocabulary visible to the induction and once with
GROUP nodes masked (segments only, same examples, same ops). Metric:
examples-to-criterion n_visible vs n_masked. Synergy iff n_visible < n_masked.
This tests whether the GROUP-node representation carries the learning
advantage.

**Built (verified):** Neither recorded. There is no induction process to
measure (see E6). M1 is entirely unimplemented.

**Scientific importance: HIGH.** M1 is the "consolidation is a win" evidence:
it tests whether the unified GROUP-node representation actually helps learning
relative to raw segments. A negative or null M1 result would be reported
honestly as data (prereg: negative synergy deltas do not fail the build), but
the absence of any measurement leaves the consolidation benefit untested.
Fully blocked on E6: examples-to-criterion is undefined without an induction
process that reaches criterion at some example count.

**Implementation difficulty: MODERATE once E6 exists** (measurement plus a
second masked run with identical examples and ops). Blocked on E6, which is
HIGH difficulty.

### E4. S9 SPLIT

**Specified (prereg section 5, S9):** "SPLIT attempted on the
boundary-violated concept (one GROUP replaced by two whose concatenation
equals it, both recurring afterward)." (Prereg section 6, M3): count SPLIT
refinements (one GROUP replaced by two, each recurring >= 2 afterward);
report refinement count and accuracy on contradictory contexts before vs
after S9.

**Built (verified):** `split_group` is defined at line 587 of
`devint_cla2.zag` and never called anywhere in the file. There is no
boundary-violated concept in the workspace to split (see E5).

**Scientific importance: MODERATE-HIGH.** SPLIT is the structural revision
mechanism for concepts: the workspace-native equivalent of revising a wrong
concept rather than merely demoting it. Without SPLIT, revision is state
change (demotion) only, not representational refinement, and M3
(contradiction -> representational refinement) is dead. Blocked on E5: SPLIT
needs a represented boundary violation as its target.

**Implementation difficulty: MODERATE.** The function is already defined; the
work is wiring (invoke it on the violated concept, verify both children recur
afterward, record the refinement count). The harder prerequisite is E5.

### E5. S7 boundary violations (workspace representation)

**Specified (prereg section 5, S7 check):** ">= 1 boundary-violation event
logged." The frozen edge vocabulary (prereg section 2) includes SURPRISE, and
the section 4 mapping expresses contradiction events as authored edges. The
prereg's spirit is workspace-native representation: developmental events live
in the workspace, not in harness locals.

**Built (verified):** The 2 "boundary violation" events are a harness-local
counter (`nviol=nviol+1` in the stage function). No SURPRISE edge, no
UNCERTAINTY node, no workspace structure of any kind is authored. The prereg's
"logged" is satisfied only in the weakest sense.

**Scientific importance: MODERATE-HIGH.** Representational honesty: the
workspace claims contradiction is representable as edges, but concept-boundary
violations (the concept-level contradiction event, and the trigger the
developmental story gives for SPLIT) live only in a harness counter. Also the
direct prerequisite for E4.

**Implementation difficulty: LOW-MODERATE.** The SURPRISE edge type already
exists in the frozen vocabulary. The work: when a boundary-violating episode
arrives, author a SURPRISE edge (or UNCERTAINTY node) on the violated GROUP,
and use that workspace structure as the SPLIT trigger for E4. The mechanism
pieces exist; this is wiring, not invention.

### E6. S6 pairing induction (the mechanism itself)

**Specified (prereg section 4 mapping):** "Procedure pairing table |
Executable graph (MAP/COPY ops) with SUPPORTS edges from training examples."
(Prereg section 5, S6): substitution procedure as executable graph; pairing
(frozen, hidden): M0<->M2, M1<->M3 (bik<->zol, gup<->tav). (Prereg section 10
localization): S6 failing means "Executable procedure graphs do not support
the pairing induction the table did."

**Built (verified):** `learn_procedure(W,g0,g2,g1,g3,ev)` is defined at line
481 and called once, at line 968, with explicit harness arguments
(`learn_procedure(W,gbik,gzol,ggup,gtav,ev)`) derived by byte-matching inside
`stage_s6`. `s6_train_out` (line 717) is defined and never called;
`s6_train_in` (line 710) is called at line 967 but only to feed episodes for
substring statistics (`feed_episode(W,s6_train_in(i))`), never to derive the
pairing. No code reads the training pairs to produce bik<->zol / gup<->tav.
The 5/5 held-out check verifies storage and retrieval of a harness-supplied
pairing. This is procedure storage, not procedure induction. The red team
calls this its strongest finding.

**Scientific importance: HIGHEST.** This is the learning-vs-storage
distinction on which the developmental claim stands or falls. The sequence
claims the learner ACQUIRES a substitution procedure; what was built stores a
supplied one. Every other S6 result (the 5/5 held-out check) tests retrieval.
It also unlocks E3 (examples-to-criterion and the M1 synergy metric), which
are undefined without an induction process. It directly tests the prereg's S6
localization row: implementing induction determines whether the executable
graph form supports induction or whether the old table was doing real work the
workspace cannot. It connects to the program's core frontier: procedure
induction from examples is L2 structural learning, complementary to the
MUL-1 construction-from-search result.

**Implementation difficulty: HIGH.** Requires genuine induction: reading
training (in, out) example pairs, aligning source and target segment
sequences, and deriving the pairing from the examples using the learner's own
vocabulary (segments, then GROUP nodes), without reading the frozen hidden
answer. Candidate approaches: positional correspondence across aligned pairs,
co-occurrence statistics over the training set, or unification over the GROUP
vocabulary. This is the hardest of the six and is a focused instance of the
procedure-induction frontier. Scoping note: the induction need not be fully
general; it must derive this pairing from the training examples through the
learner's vocabulary, with the derivation traceable in the workspace (SUPPORTS
edges from training examples, per the section 4 mapping).

## Prerequisite graph

- E5 -> E4: a represented boundary violation is the SPLIT target. E4 cannot
  be attempted honestly without E5.
- E6 -> E3: examples-to-criterion (and the M1 visible/masked comparison) are
  undefined without an induction process that reaches criterion.
- E1 is independent as a measurement, but an honest E1 may trigger retention
  hardening (evidence-node protection, tie-break removal, demotion-aware
  retention), which is follow-on implementation work.
- E2 is independent: it needs the S11 prediction routine, which exists.

```
E6 (pairing induction) ---> E3 (examples-to-criterion, M1)
E5 (violation representation) ---> E4 (SPLIT)
E1 (M2 metric) [independent; may trigger retention hardening]
E2 (post-eviction accuracy) [independent]
```

## Priority ranking for the next wave

1. **E6, pairing induction.** The red team's strongest finding; the
   learning-vs-storage distinction; unlocks E3/M1; tests the S6 localization
   directly. Highest scientific importance, highest difficulty.
2. **E1, M2 metric.** F4 falsifier (no correlation -> REJECT the
   implementation); the honesty test for evidence-driven retention; may surface
   a genuine pathology, which is high information value either way.
   Independent of E6, so it can run in parallel.
3. **E5, boundary-violation representation.** Prerequisite for E4;
   representational honesty for the contradiction claim. Low-moderate
   difficulty.
4. **E4, SPLIT.** Structural revision of concepts; M3. Depends on E5; the
   function is already defined, so this is wiring once E5 lands.
5. **E3, examples-to-criterion and M1.** The consolidation-benefit evidence.
   Depends on E6; moderate difficulty once E6 exists.
6. **E2, post-eviction accuracy.** Functional consequence of eviction.
   Independent and low-moderate difficulty, but lower diagnostic value than E1
   (E1 tests the retention claim; E2 tests its consequence).

## Recommendation: implement E6 first

The single most important element for the next wave is **E6, genuine S6
pairing induction**.

Justification:

- It is the difference between "the learner acquired a procedure" and "the
  learner stored a supplied pairing." A developmental integration experiment
  that cannot show induction at S6 has a storage result wearing a learning
  claim. All downstream S6 evidence (5/5 held-out, S11 procedure reuse 3/3)
  currently tests retrieval of harness-supplied structure.
- It is the red team's strongest finding, and the finding most likely to
  replicate across future developmental runs if left unaddressed: any
  procedure stage built the same way will have the same hole.
- It unlocks E3: without induction there is no examples-to-criterion and no
  M1, which means the "consolidation helps learning" claim (the point of
  DEVINT-CLA2 over DEVINT1) stays untested at the procedure stage.
- It is a direct experimental test of the prereg's own S6 localization row.
  If induction proves infeasible in the executable-graph form, that is a
  precise, falsifiable consolidation cost, exactly the "lose-informative"
  outcome the prereg was designed to produce.
- Suggested scoping: derive the pairing from the S6 training examples through
  the learner's segment/GROUP vocabulary (positional correspondence or
  co-occurrence), with the derivation recorded as SUPPORTS edges from training
  examples per the section 4 mapping. The frozen hidden pairing must not be
  read; the training examples are the only admissible input.

Parallelizable alongside E6: E1 (M2 wiring and honest reporting) and E2
(post-eviction accuracy), since neither depends on the induction mechanism.
E5 should precede E4 in a later wave, and E3 follows E6.

## Governance notes

- BUILD-PASS stands (B1-B5 literally hold); none of the six elements affects
  the frozen kill bars. These are prereg-specified elements implemented
  incompletely or not at all, plus the red team's fragility findings. The M2
  and F4 claims were already corrected by commit `a003bd19b`.
- Any next-wave implementation of these elements needs its own frozen prereg
  amendment (the original prereg is frozen at `f24063bcb`); the amendment must
  precede implementation per the prereg commit-order rule.
- No new modes, bridges, handlers, or semantic cases should be introduced to
  implement these elements; the standing One-System Rule applies. In
  particular, E6 induction must work through the existing executable-graph
  form and edge vocabulary, or its failure is the finding.
