# CONSOLIDATED REPORT -- TNN overnight session

Lane `ownership`. Branch `lane/ownership`.
Covers PHASE 0 through PHASE 5, plus instrument hardening.
Phases 6-15 are listed at the end as not started, with reasons.

---

## 1. ARCHITECTURE CHANGES

**Nothing in TNN's implementation was changed.** This session produced
evidence and two static-analysis tools, not a patch to the canonical
learner. Stating that plainly because "architecture changes" is the
heading that invites overclaiming.

What was added:

```
tools/tnn_bars_lint.sh    enforces RULE R3 (recompute every bar)
tools/tnn_loop_lint.sh    enforces loop termination (from a real segfault)
```

`RULES.md` (R1-R10) is now standing policy, superseding ad-hoc
per-lane decisions.

## 2. STRONGEST SURVESTING RESULTS

**R-A. Applicability can be moved to learner state, and the router it
replaces was surface-bound pure loss.** (`REPORT_23.md`, C1541)

The audited router decides which cognition runs by parsing the *shape*
of the input. On a semantically identical input whose punctuation
carries no type information, it withholds and the capability is lost.
Deriving the same information from the fact table and from probing the
structures costs nothing and works on both encodings.

```
router/aligned = 12    router/neutral = FAIL
contract/aligned = 12  contract/neutral = 12
```

Permutation-invariant, facts-only-resistant, 9/10 bars pass.

**R-B. Selection among applicable structures is solvable by the learner
from consequences alone, and the solution transfers.** (`REPORT_45.md`)

C1541 produced a counterexample that contracts provably cannot fix. A
consequence-weighted selection fixes it in **one trial**, transfers to a
fresh query with no source change, and collapses to the counterexample
when support is erased.

```
first_correct = 1 wrong = 1 of 12
PHASE4 TRANSFER q=(20,111) -> 22, same chain, no source change
FO (support erased) -> 11 (the counterexample returns)
```

**R-C. Two structurally different invalidation mechanisms exist and
must never be conflated.** Gate invalidation (the structure stops being
eligible) is **immediate**. Consequence revision (it stays eligible and
becomes wrong) took **12 trials**. Reporting "revision works at trial 0"
because a fact change gated the chain out would have been false.

**R-D. Flat-gradient worlds cannot test proposal learning, for a
provable reason.** (`REPORT.md` in `noisy/`) Any wrong linear parity
over GF(2) disagrees with the true parity on exactly half the rows,
regardless of arity. Adding a second candidate class did not create a
gradient. On a genuinely graded family the entire win is `argmax`,
which is ranking already held at L2.

## 3. IMPORTANT KILLS

**KILL-1. Proposal ordering is not a route to L3.** Closed with a
mechanism, not a benchmark failure: the feedback geometry is flat, so
there is nothing to learn about proposal quality. Under noise an
*apparent* within-wrong gradient appears (spread 12-16) but it is
sampling variance -- facts-only reproduces it exactly. Gradient reversal
collapses the truth from 57 to 7 with the complement tying at top.

**KILL-2. Learned contracts are NOT sufficient for recruitment.**
The single most useful negative of the session. A legitimately learned
structure whose output is class-valid but wrong is recruited and
accepted. Its output really is subject-only, so *nothing available to
the mechanism could reject it*. Confirmed shared by both the router and
contract arms, so it is not a bridge-removal regression.

**KILL-3. Additive support over chain elements is unsound.** It rewards
self-composition: `(s,s)` scores `2*s` and outscores `(s)`, so the
system oscillates (18/28 stable). Any rule preventing score growth with
chain length restores stability to 27/28.

**KILL-4. Name-based bridge auditing is invalid for this codebase.**
Every `_TO_` and `_MODE` occurrence is a comment *asserting absence*.
All four real bridges are implicit. Retired as a method.

**KILL-5. Additive support is not self-composition-safe under revision**
-- see KILL-3; the two are the same defect seen from selection and from
revision.

## 4. BRIDGE AUDIT

Full map in `BRIDGE_MAP.md`. Baseline: 105,673 files / 80,991,292 LOC /
987 experiments / 106 lanes.

```
explicit named bridges (_TO_ in code)     0
named cognitive modes in code             0
structural cognitive bridges              4
  in the CANONICAL learner               3
generic interface mechanisms              1
```

| id | location | what it is | class |
|---|---|---|---|
| BR-1 | `unified_learn.zag:734` `route_line` | syntactic router, 5 role-named routes (`PROC_LEARN`, `CAUS_LEARN`, `PROC_QUERY`, `CAUS_QUERY`, `WITHHOLD`) selected by input shape | **D** |
| BR-2 | `unified_learn.zag:423,445` `bridge_apply`/`bridge_learn` | conditional `(pos,val)` bridge, triggered by hardcoded policy: "PROC_LEARN failure automatically triggers bridge induction" | **D** |
| BR-3 | `unified_learn.zag:1008` | candidate-origin taxonomy `-1 none / -2 ambiguous / 0 proc / 1 bridge` | **D** |
| BR-4 | `xio_adapters/xio_core.zag:95-99` | for any numeric MAP, re-derives a **count** instead of executing the MAP; produced `count(103)=2` where `sum(103)=15` | **D** |
| BR-5 | `l3_bridge_impl/bridge.zag` | removed a signature enum + 3 recipe branches, added 4 generic operators | **B** (positive) |

**The cluster is the finding.** BR-1, BR-2, BR-3 are one missing
generic property in three disguises: *deciding which learned structure
applies, using that structure's own properties.* BR-1 substitutes
input syntax; BR-2 substitutes a fallback policy; BR-3 substitutes
mechanism provenance.

**BR-4 has a different root cause: representation lossiness.**
`promote_graph` persists `(relation, subject, graph root, index, answer)`
and DEP edges, but **not which aggregation produced the graph length**.
`SUM` and `COUNT` emit structurally identical INC chains differing only
in length. So a numeric MAP is lossy and cannot be re-instantiated for
a new input. A generic executor therefore *cannot* fix BR-4; learner
state must first retain provenance. This is why BR-4 is excluded from
the recruitment work.

## 5. BRIDGE DELETIONS

**Zero deletions from TNN.** No bridge was removed.

What was achieved instead is a **measured replacement for BR-1** in an
isolated experiment: the surface→type substitution is unnecessary and
surface-dependent. That is a prerequisite for deletion, not deletion.

Deletion queue, with the blocker for each stated:

```
BR-1  deletable once a replacement is committed to the canonical learner
      -- replacement now MEASURED (this session)
BR-2  BLOCKED on selection (KILL-2). Its (pos,val) condition is already
      learned by search; only the decision to induce is researcher policy,
      and that policy is a workaround for selection not existing.
BR-3  deletable with BR-1/BR-2
BR-4  NOT deletable. Requires MAP provenance retention (PHASE 10).
BR-5  keep. Already the right shape.
```

## 6. METHOD OWNERSHIP PROGRESS

Two researcher-owned decisions moved, one partially, and the remaining
gap is now narrow and named.

```
applicability   MOVED to learner state      (R-A)
selection       MOVED IN EFFECT             (R-B)
  but its scoring rule is researcher-owned  (KILL-3)
scoring rule    OPEN, and it is the smallest
                well-defined ownership gap found
```

The refined frontier statement:

> TNN learns inside cognitive spaces researchers create, and it can now
> learn *which of its own structures applies* and *which to prefer from
> consequences*. What it cannot yet learn is **how to credit itself** --
> the rule by which experience becomes preference.

## 7. SELF-ORGANIZATION PROGRESS

Emergent roles are demonstrated in the sense that role assignment is
never declared: value classes are **derived** from the fact table
(`bit0 = occurs as subject`, `bit1 = occurs as object`), signatures are
learned by **probing structures**, and role vocabulary is absent from
source (grep-clean). Two structures with no declared roles composed
because their learned contracts happened to connect.

What is *not* demonstrated: a structure recruited into a role it was not
learned for, across a role change. Composition is between structurally
different functions, but the functions are still arity- and
type-shaped in a way the researcher set up. Honest limit.

## 8. FORMAL / META / BELIEF / SCALING

**Not attempted this session.** P5 meta-learning, P6 FL7 formal
induction, P7 inquiry, trial-graph leak closure, generation-stamp
integration and 20k→50k→100k scaling were left untouched. The session
was spent on PHASE 0-5 because the audit surfaced a
higher-information target than any of them.

One related finding worth carrying forward: the audit found that the
prior **four-pair generality claim is false**. `xdomain_causal_interv`
and `xdomain_grammar_construct` both cite "Arithmetic to planning: H1
PASS, H2 PASS", but `xdomain_arith_plan/NAMECHECK.md` records a
preregistration **supersession** -- the typed-contract run for that pair
was replaced by invention-mechanism ports, which were all KILLED. Two
colliding `H1`/`H2` naming schemes (contracts/composition vs
mutation/recombination/invention) caused it.

**Corrected generality: three real pairs, not four.** Recorded as
`PROCESS-FAIL (citation)`. No data is falsified; a claim was overstated
across a supersession boundary.

## 9. WHAT BECAME MORE LEARNER-OWNED

1. **Applicability.** Which stored structure may apply to a situation,
   from contracts derived by probing its own graph. Replaces a
   surface-form router. Survives identifier permutation; cannot be
   reproduced from facts alone.
2. **Preference.** Which applicable structure to use, from scalar
   consequence tokens. Converges in one trial, transfers, and is
   load-bearing (erasing it restores the failure).
3. **Structure assembly** (carried from prior lanes): structures are
   still assembled by verified search over generic primitives, never
   handwritten. Re-confirmed here in a fresh substrate.

## 10. WHAT REMAINS RESEARCHER-OWNED

1. **The scoring rule** turning consequence history into preference.
   Owner of the `SUM`/`MAX`/`NONSELF`/`DAMPED` choice. KILL-3 shows the
   choice is not cosmetic.
2. **Value classes themselves** are derived by a rule I wrote. Closer to
   plumbing than cognition, but it is a rule, not learned.
3. **The consequence oracle.** The world supplies a scalar reward. The
   mechanism cannot invert it to the answer, but in a 3-candidate world
   it is close to invertible. Declared limitation.
4. **Candidate enumeration** for recruitment (length-1 and length-2
   chains, `MAXQ=3`). Still a researcher-chosen search space.
5. **Everything in the canonical learner**: the procedure store, the
   trial templates, `route_line`, the bridge, the router, the fact
   format. None of it was touched.
6. **BR-4's aggregation semantics** -- absent from learner state, which
   is why it cannot be replaced.

## 11. L3 STANDING

**L3 = 0.** Unchanged.

Reasons, stated plainly:

* H16v3's core question is untouched. Nothing here was tested against
  it, and per RULE R4 passing it is not the objective.
* The substrate is a declared **minimal reproduction** of the audited
  architectural shape, not the frozen 4-op ISA. Bit-compatibility is not
  claimed.
* Selection is now partly learner-owned, but its scoring rule is not,
  and the mechanism demonstrably picks a wrong applicable structure
  without consequence feedback.
* The audit found the canonical learner is *more* bridged than the
  program assumed, not less. Progress is measured on an isolated
  mechanism, not on TNN's actual cognition.

No promotion is claimed.

## 12. HIGHEST-VALUE NEXT FRONTIER

Ranked by information gain, not by effort.

**1. Discriminate the surviving scoring rules.** MAX, NONSELF and DAMPED
all produced identical results because every viable chain here has
length <= 2. The experiment that separates them is a world where the
correct answer **requires self-composition** -- the one case NONSELF
forbids. Cheap, and it converts a 3-way tie into a decision.

**2. `H-SC`: provenance-scoped credit.** Every rule tested shares one
global scalar per structure. Scoping credit to the regime that earned
it should make REV-A fast *and* stable, where these rules only make it
stable. This is the most promising untested idea and it attacks the
actual remaining ownership gap.

**3. PHASE 10: BR-4 by making MAPs retain provenance.** The audit
proved the information is absent, so the experiment is well-posed:
add the aggregation to `promote_graph`, show the count re-derivation
becomes unnecessary, and measure whether a generic executor can then
instantiate a numeric MAP. This is the only bridge in the list whose
blocker is *representation*, and representation is learner state.

**4. PHASE 11: H16v4 against the new mechanisms.** The consequence-
weighted selector and the contract learner are the first mechanisms in
this program that were built *after* H16v3 existed. They need adversarial
audit: can facts-only plus a cheap search reproduce selection? Can a
researcher-written scoring rule masquerade as a learned one? The
`DAMPED` rule in particular is three characters of researcher code, and
that is exactly the shape H16 exists to kill.

**5. PHASE 6: other-architecture principles.** Not started. Note the
audit already supplies the best single example of "steal the principle,
not the subsystem": BR-5 removed a signature enum and three recipe
branches and replaced them with four generic operators, with every
`setnode` call inside one of the four. That is the compression target
for BR-1/2/3.

**Explicitly not recommended:** more seed/ordering/proposal-selection
experiments in parity worlds. KILL-1 closed that direction with a
mechanism, and re-opening it would be re-running a settled negative.

---

## PROCESS FAILURES AND BUGS (preserved)

Eleven defects, all mine, all caught. Preserved because the governance
value is in the pattern, not the count.

**Evaluator/instrument defects**

1. `trA`/`trB` allocated 8 bytes, 24 written. No bounds checking, so
   the training data was silently corrupted and *nothing was learned*.
   Symptom: `promoted=0`.
2. Noise generator inverted: `z/modulus` is always 0, so `u<e` was always
   true and all 64 labels were corrupted at e=0.15. Caught only because
   the prereg forced printing **realized** corruption counts.
3. A bar `K7_random_ok=1` was hardcoded in a label string. It was
   written immediately after the prereg said no bar may be set from a
   printed constant. Fixing it exposed defect 4.
4. `is_target` credited `TERN(1,4,5)` as solving target `(1,4)`. RANDOM
   read 16 instead of 35; LEARNED read 17 instead of 28.
5. An M12 metric printed `1` ("immune to reversal") when it was a
   tie-break artifact against the complement.
6. `RANDOM` reported 18 against a closed form of 35 (biased LCG); a
   second bug hid a flat layout confound and an unimplemented prereg rule.

**Substrate/state defects**

7. Stale root: `learn` for B clobbered A's scratch before promotion.
8. Promotion collision: every structure wrote the same base node, so all
   promoted structures came out identical.
9. Exclusions written into persistent support and never restored,
   destroying learned state.
10. Two `while` loops missing `s=s+1`. Infinite loop grew the output
    cursor past the buffer; `_zag_print(ob[0..c])` then read out of
    bounds -> segfault with **zero output**. The segfault *moved* when
    unrelated code changed layout, so it masqueraded as memory
    corruption. Now statically linted.

**Invalid experiments of my own**

11. Two revision arms measured nothing. The first made its expected
    answer class-2 (unreachable). The second made the stale chain
    class-0, so "revision at trial 0" was gate invalidation, not
    consequence revision. A suspiciously perfect result is usually a
    rigged test.

**And one misprediction.** I hand-derived 24 trials for REV-A; measured
12. My model wrongly assumed `s2` decayed while unused. Corrected
derivation gives 12, matching exactly. Recorded because a prediction
that was never wrong was never a prediction.

## WHAT TO KEEP DOING

Theory predicted a number, measurement disagreed, and the disagreement
found a real bug -- **every single time** (defects 2, 4, 6, and the
RANDOM closed form). Meanwhile defects 1, 7, 8, 9 were found by
*reading the promoted structures against the training data by hand*,
because each produced a plausible-looking wrong answer rather than a
crash.

Both practices are now tooling or habit:

* closed forms and realized values before interpreting a number;
* `tnn_bars_lint.sh`, `tnn_loop_lint.sh`;
* inspect promoted structures against training data, not just bars.