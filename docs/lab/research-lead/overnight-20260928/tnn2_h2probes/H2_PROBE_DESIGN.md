# H2 Masked Verification Probe Design

## NOT IMPLEMENTED

This document is a DESIGN ONLY. No probe code was written, no Zag source was
modified, no binary was built, and no probe was executed. Everything below
describes tests that COULD be run against the frozen TNN-2 binary
(commit `f4de7ff46`) using only driver-side inputs (world scripts and
`mp_run` flags). Nothing here changes the learner. The predicted outcomes
are derived by reading the frozen source (`t2_try_verify` lines 497-510,
`t2_trial` lines 586-666, `mp_run` lines 668-671); they are predictions to
be checked by a future executor, not measured results.

Roadmap context: this is Step 1 of the TNN-3 roadmap (commit `67a420cca`).
It must precede Step 4 (H1 widening) because widening the constructor while
the acceptance oracle remains would build a larger finite menu under the
same generous acceptance test, which is the treadmill Micah forbade.

---

## 1. What is a masked verification probe?

A masked verification probe is a sealed-world evaluation in which the
driver-supplied answer key (`expected`) is separated from the learner's
trial loop, so that candidate acceptance must be decided by the learner
itself from its own state. The external score is computed only AFTER the
learner has committed to an answer, a promotion, or a refusal.

Precise definition. A probe run is masked iff all of the following hold:

1. During the entire trial (every call to `t2_try_verify` for that query),
   no value derived from the sealed answer key reaches the verifier. The
   driver withholds `expected`, supplies a corrupted `expected`, or the
   verifier is required to ignore it.
2. The learner commits to an observable decision: an answer, a promoted
   graph, or an explicit refusal/uncertainty signal, before the key is
   revealed.
3. Scoring compares the committed decision against the sealed key offline.
   The score cannot leak back into the learner during the trial.
4. A paired unmasked control run (same world, `expected` supplied, flags=0)
   is executed to confirm the mechanism passes with the oracle. The
   discrimination signal is the GAP between unmasked and masked behavior,
   not the masked score alone.

The reason for condition 4: H2's prediction (roadmap section 2) is that
current mechanisms fail masked probes while passing unmasked ones. Without
the control, a masked failure could be blamed on the world being too hard
rather than on the oracle being the binding constraint.

## 2. How the `expected` is masked

The driver provides observations (teach/query events that build learner
state) but the answer key travels a separate path that the learner cannot
read during the trial. Concretely, against frozen TNN-2, three masking
modes, all driver-side, no learner source edits:

- **Withhold:** call `mp_run` with the masked flag set (flags bit 0 = 1).
  The existing masked branch of `t2_try_verify` ignores `expected` and
  accepts any candidate whose execution returns a clean value
  (v != -2 and v != -999999). The driver may pass any `expected` value,
  including a garbage sentinel, because the masked branch never reads it.
- **Lie:** call `mp_run` unmasked (flags=0) but supply a wrong `expected`
  (for example true_answer + delta, or a plausible wrong value drawn from
  the same range). The verifier behaves exactly as in production; only the
  key is corrupted.
- **Withhold plus held-back facts:** withhold `expected` AND reserve a
  subset of taught facts as a private consistency set the trial never sees.
  Acceptance quality is then scored two ways: against the sealed key, and
  against consistency with the held-back facts. This mode matters for
  Probe C, where the learner's own criterion has to come from somewhere
  the oracle does not reach.

Critical design point. The current masked branch is NOT learner-internal
verification. It is acceptance without verification: the first candidate
that executes cleanly is promoted. The probes exploit this. If the probe
worlds are easy, masked mode accidentally gives the intended answer (the
code comment at line 583 even notes masked `t_f2` still prefers the 2-hop
reading). Therefore every probe world must be a **search-order trap**: a
world where the first executable candidate in the researcher's fixed
search order (chains k=2..4, then sums, then counts, then single hops) is
WRONG, and the correct structure appears later in that order or requires
a discrimination the order cannot make. The probe discriminates oracle
dependence from genuine verification only on trap worlds.

## 3. What learner-internal verification would look like

Three candidate forms, ordered from weakest to strongest. Any of them
would count as learner-internal; all three require the acceptance
decision to read learner-created persistent state.

**Form 1: Prediction-based acceptance.** The learner generates a prediction
from a candidate structure about a not-yet-observed fact, observes the
actual outcome, and accepts or rejects the candidate based on the match.
The prediction, the comparison, and the resulting endorsement must live
in learner state (not in driver code), and a wrong prediction must be
able to retract the endorsement.

**Form 2: Consistency-based acceptance.** The candidate is accepted only if
its execution agrees with independently retained facts that were not used
to construct it (the held-back set in masking mode 3). Acceptance is a
cross-check: the structure is endorsed because it coheres with what the
learner already believes, not because an external key matched.

**Form 3: Consequence-based acceptance.** The candidate is accepted
provisionally and retained only if adopting it reduces subsequent misses
or improves subsequent predictions. This is the strongest form and it
requires the reuse path (promoted structures must actually execute at
query time), which the interaction analysis (`9009ff259`) showed is
currently absent: `ev_query` reads only tag-1 facts, never tag-20 MAPs.

None of these exist in frozen TNN-2. `t2_try_verify` reads exactly three
decision inputs: the execution value `v`, the driver-supplied `expected`,
and the researcher-set `masked` flag. No learner-state policy value
enters the decision. The DOF map (`d2af26581`) records zero pure-learner
decisions anywhere in the system, and acceptance is a researcher decision.

## 4. The three probes

### Probe A: Withhold the key. Can the system verify without `expected`?

**Setup.** Sealed trap worlds (see section 2). Driver teaches facts, issues
the query, calls `mp_run` with flags bit 0 = 1 (masked). The learner
commits to an answer/promotion. The evaluator scores the committed answer
against the sealed key offline. Paired control: identical world, flags=0,
true `expected` supplied.

**Recorded observables.** Committed answer; whether a graph was promoted;
the promoted graph's signature (`t2_sig`); trial stats from header
field 16 (tried/rejected counts); refusal events (there is no refusal
path, so the observable is its absence).

**Predicted outcome for frozen TNN-2 (from source reading).**
The masked branch accepts the FIRST candidate with v != -2 and
v != -999999. Search order is fixed: chains k=2..4 in `t2_gather` path
order, then sums (popcount-descending bitmask), then counts, then single
hops. On trap worlds the first executable candidate is the wrong
structure, so the system promotes the wrong structure with high tried
counts and near-zero rejected counts (it stops at the first executable
candidate; rejections only occur for guard failures or execution
failures). The system never refuses: there is no code path that declines
to promote when any candidate executes, so the observable refusal rate is
exactly zero. `promote_graph` then inserts an exact-match fact and a MAP
node that `ev_query` never reads, so the wrong promotion is causally
inert at query time and also unrepairable: the revision red team
(`687ba0219`) showed revision handles only one topology and is never
invoked on the promotion path. Net prediction: masked accuracy at or
below the search-order baseline, zero refusals, spurious MAPs accumulated
with no feedback loop to remove them, while the unmasked control passes.

**What makes this probe discriminating.** On non-trap worlds masked mode
looks fine, which is why the code comment says masked `t_f2` still works.
The probe is only informative on trap worlds. A future system that does
learner-internal verification would show masked accuracy ABOVE the
search-order baseline, or a nonzero refusal rate on worlds where nothing
meets its internal criterion.

### Probe B: Lie about the key. Can the system detect a wrong `expected`?

**Setup.** Sealed worlds where the driver supplies a corrupted `expected`
in unmasked mode (flags=0). Two lie classes: (B1) a wrong value that some
candidate structure executes to (the lie is "confirmable" by a wrong
structure); (B2) a wrong value that no candidate executes to (the lie is
unconfirmable). Paired control: true `expected`.

**Recorded observables.** Whether the lie-matching candidate is promoted
(B1); whether any uncertainty node, contradiction edge, or refusal is
produced; the content of learner state after the trial (does it now hold
a "verified" MAP encoding a false relation?); behavior on the NEXT query
in the same world (does the false promotion cause a downstream miss, and
is that miss attributed to the lie?).

**Predicted outcome for frozen TNN-2 (from source reading).**
In class B1, unmasked `t2_try_verify` promotes the first candidate with
v == wrong_expected. The learner now holds a promoted graph whose
"verified" label contradicts its own retained facts, and no alarm fires:
`miss_inquire` is triggered only by execution misses, never by oracle
inconsistency, and the inquiry red team (`4e329c772`) found no production
path that resolves UNCERTAINTY nodes or supersedes stale guides (L6
absent). `contradict_map` exists but has no production caller tied to
verification outcomes. In class B2, no candidate matches, ans stays -2,
nothing is promoted, and nothing is learned: the trial fails silently
with no record of WHY it failed (the tried/rejected stats are packed
into a header field and never read by any decision). On the next query,
a B1 false promotion causes downstream misses that the system attributes
to the world, not to the corrupted key, because the key is never
re-examined. Net prediction: the lie is either absorbed as false
knowledge (B1) or dropped without a trace (B2); in neither class does the
system produce any signal distinguishing "oracle disagrees with my
facts" from "no candidate worked."

**What makes this probe discriminating.** It separates systems that treat
the oracle as ground truth from systems that treat the oracle as one
evidence source among others. A learner-internal verifier would, in B1,
refuse to promote a candidate that contradicts retained facts even
though the oracle endorses it, or flag the contradiction; in B2 it would
record the failure as evidence ABOUT THE ORACLE, not just about the
candidates.

### Probe C: Generate the criterion. Can the system produce its own acceptance rule?

**Setup.** Withheld key (masked) on tie worlds: worlds where two or more
candidate structures from different families both execute cleanly but
imply different answers, and the learner's own retained facts support one
of them. Example structure: a 2-hop chain and a sum both execute; the
sum's components are each supported by multiple independent fact paths
while the chain rests on a single path. The researcher's search order
tries chains before sums, so the order-determined winner is the chain.
A consistency-based learner criterion (Form 2) would prefer the sum.
The driver withholds `expected`; the learner must choose on
learner-internal grounds.

**Recorded observables.** Which family the promoted graph comes from; a
white-box trace of every value read by the accept decision during the
trial (to check whether any learner-created persistent state value is
among them); an ablation variant where the supporting fact multiplicity
is equalized (both candidates equally supported) to test whether the
choice tracks the evidence or the order.

**Predicted outcome for frozen TNN-2 (from source reading).**
The accept decision reads v, expected (ignored in masked mode), and the
masked flag. It reads no learner-state policy value; the DOF map records
zero pure-learner decisions. The tie is therefore broken by search order
alone: the chain is promoted on every tie world regardless of fact
multiplicity, and the ablation variant changes nothing. The white-box
trace shows the decision is a pure function of (execution value,
researcher constants). Net prediction: 100 percent order-determined
choices, zero evidence-tracking, and the trace contains no
learner-created value anywhere in the causal chain of the decision.

**What makes this probe discriminating.** It is the direct behavioral
test of the DOF map's central claim ("indices and literals" only). Any
future mechanism that passes must show a learner-state value in the
causal chain of acceptance, verified by the ablation: equalize the
evidence and the choice must become order-independent or explicitly
arbitrary-with-refusal, not order-determined.

## 5. Predicted outcomes summary (frozen TNN-2)

| Probe | Predicted result | Mechanism (source-grounded) |
|-------|------------------|-----------------------------|
| A (withhold) | FAIL: promotes first executable candidate; wrong on trap worlds; zero refusals | Masked branch accepts v != -2, v != -999999; fixed search order; no refusal path |
| B1 (confirmable lie) | FAIL: promotes lie-matching wrong structure; no contradiction signal | Unmasked branch matches v == expected; no oracle-vs-facts comparison exists |
| B2 (unconfirmable lie) | FAIL: silent no-promotion; failure leaves no usable trace | ans = -2 path records nothing actionable; no inquiry into the key |
| C (own criterion) | FAIL: ties broken by researcher search order; no learner value in decision | Accept decision inputs are v, expected, masked only; DOF map: 0 learner decisions |

In all probes the unmasked control is predicted to PASS, which is exactly
the H2 discrimination signature from the roadmap: fail masked, pass
unmasked, therefore the oracle binds.

## 6. What a PASS looks like

A future system demonstrates learner-internal verification only if ALL of
the following are observed on sealed post-freeze worlds (worlds designed
after the mechanism freeze, by an independent adversary, per C0-C):

1. **Above-baseline masked accuracy.** On trap worlds with the key
   withheld, committed answers beat the frozen masked baseline
   (first-executable-in-search-order) by a preregistered margin, 3/3
   byte-identical runs. Beating the baseline proves the acceptance
   decision uses information the baseline does not.
2. **Refusal competence.** On adversarial worlds where no candidate meets
   the internal criterion, the system explicitly declines to promote
   (nonzero refusal rate), rather than promoting the first executable
   candidate. Refusal must be observable in behavior and in learner state.
3. **Lie resistance.** On B1 worlds the system does not promote an
   oracle-endorsed candidate that contradicts its retained facts: it
   refuses, flags a contradiction, or promotes the fact-consistent
   candidate instead. Zero promotions of fact-contradicting candidates is
   the bar. On B2 worlds the failure is recorded as evidence about the
   key, visible in learner state.
4. **Causal learner-state involvement.** A white-box trace shows a
   learner-created persistent value entering the accept/reject decision;
   ablating that value (and only that value) flips at least one
   acceptance decision while researcher constants are untouched. This is
   the anti-theater check: a criterion that cannot be ablated is a
   researcher constant with a new name.
5. **Revisability of the criterion.** A documented experience trace shows
   the acceptance criterion itself changing in response to prediction
   errors (for example, a consistency threshold tightening after a false
   acceptance). A fixed criterion is H1-style enumeration moved one level
   up.
6. **Domain neutrality.** The same verifier handles chain, sum, and count
   worlds with no per-family acceptance branches. A new branch per family
   is the benchmark-specific-handler smell and fails this condition.
7. **Reuse coupling.** Promoted structures must be readable by the query
   path (the interaction-analysis H2: promoted graphs currently never
   execute at query time). Acceptance without reuse is causally inert and
   cannot satisfy C0-D, so a PASS on verification alone does not
   establish cognitive reuse.

Forms 1, 2, or 3 from section 3 are all acceptable realizations; the
seven conditions above are realization-independent.

## 7. Draft kill bar language for H2 (DRAFT, NOT FROZEN)

The following is draft language for preregistration. It is NOT frozen and
governs nothing until Micah freezes it in a prereg commit that strictly
precedes implementation.

**K-H2-1 (masked accuracy).** On N sealed trap worlds drawn from at least
two independently designed world families (N fixed in prereg; adversary
designs post-freeze), with `expected` withheld from the trial loop
(verified by white-box audit that no key-derived value reaches the
verifier during the trial), the learner's committed answers exceed the
frozen first-executable-in-search-order baseline accuracy by at least the
preregistered margin M, on 3/3 byte-identical runs. Paired unmasked
controls must pass on the same worlds.

**K-H2-2 (lie resistance).** On preregistered lying-oracle worlds (both
confirmable-lie and unconfirmable-lie classes), the learner raises an
explicit uncertainty/contradiction signal or refuses promotion on at
least the preregistered fraction F of trials where the oracle contradicts
retained facts, and promotes ZERO candidates that contradict retained
facts. 3/3 byte-identical runs.

**K-H2-3 (criterion causality and revisability).** White-box trace
demonstrates a learner-created persistent state value in the causal chain
of at least one accept/reject decision; ablation of that value alone
flips the decision; and a committed experience log shows the criterion's
value changing in response to a prediction error. All three sub-clauses
are required; any one missing is a FAIL.

**K-H2-4 (domain neutrality and reuse).** The verifier that passes K-H2-1
through K-H2-3 contains no per-family acceptance branches and no new
protected-core operations; and at least one promoted structure from a
masked trial is executed by the query path on a later query in the same
continuing learner (reuse coupling, closing the interaction-analysis H2).

**Guard clauses.** (a) `expected` must be absent from the trial path, not
renamed, re-encoded, or cached where the verifier can read it; the audit
in K-H2-1 checks the actual data flow. (b) No bar may be weakened after
results are seen; a broken prereg is amended transparently and re-frozen.
(c) Passing K-H2-1..K-H2-4 establishes learner-internal verification; it
does not by itself establish L3, C0-B, or C0-C, which require the
independent post-freeze generality battery.

## 8. Execution notes for the future executor

- No new machinery is needed to run Probes A, B, and C against frozen
  TNN-2: all three use existing `mp_run` entry points (masked flag,
  corrupted `expected`, structured world scripts). The "new" content is
  the sealed trap worlds and the scoring, which live in the evaluator,
  not the learner.
- Trap worlds are the load-bearing design element. Non-trap worlds
  cannot discriminate because the current masked branch was tuned so
  that easy cases still work. The adversary designing the worlds must be
  shown the search order (chains k=2..4 in gather order, then sums, then
  counts, then single hops) and instructed to make the order-determined
  winner wrong.
- Determinism: all probe runs must be 3/3 byte-identical, same as every
  other bar in this program.
- The paired unmasked control is not optional; without it a masked
  failure is uninterpretable.

## 9. Lineage

- H2 hypothesis statement: red-team synthesis `42b4dfa91`, section 5
  ("oracle verification; fix = learner-internal acceptance").
- Roadmap ordering (H2 probes before H1 widening; treadmill risk):
  `67a420cca`, sections 2, 5, and Risk 3.
- Source facts: `t2_try_verify` / `t2_trial` / `mp_run` in `tnn2.zag`
  (commit `f4de7ff46`); masked branch never engages in production per
  construction red team `340e94e3e`.
- DOF result ("indices and literals"; 0 pure-learner decisions):
  `d2af26581`.
- Reuse-path structural failure (promoted graphs never execute at query
  time): interaction analysis `9009ff259`, section 6.

## Verdict

H2-PROBE-DESIGN-COMPLETE. Design only; NOT IMPLEMENTED. No code written,
no source modified, no probes executed. Ready for independent review and,
if Micah approves, for a future executor to build the sealed trap worlds
and run the three probes against the frozen TNN-2 binary.
