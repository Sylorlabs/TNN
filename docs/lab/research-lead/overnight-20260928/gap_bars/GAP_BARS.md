# Kill Bars for the 5 Prereg-Structure Gaps

**Status: DRAFT-NOT-FROZEN - AWAITING MICAH REVIEW**

Date: 2026-10-01 (UTC). Drafter session: c82fe280-5fc2-4184-a266-33070ee179fb.

This document drafts kill bars for the five gaps identified in the
TNN-3 preregistration structure synthesis (`206499c03`, section 5a).
Draft only: no implementation, no frozen thresholds, no source edits.
Nothing here governs any build until Micah reviews it and a TNN-3
preregistration freezes it (or records explicit amendments) before
any TNN-3 implementation begins.

All five bars below are DRAFT-NOT-FROZEN. They do not amend or freeze
any existing draft. Where the synthesis recommended an explicit
non-claim instead of a bar, that recommendation is preserved and the
bar is drafted only as a future-generation candidate.

Input lineage:
- Gap list: `tnn3_prereg_struct/PREREG_STRUCTURE.md` (`206499c03`), section 5a
- K-H2 source drafts: `tnn2_h2probes/H2_PROBE_DESIGN.md` (`4631c5918`), section 7
- Composition operator objection: MUL comparison (`e2e34a4ac`), section 6
- Informativeness: inquiry generalization (`dedfad368`), referenced by `206499c03` section 5a gap 3
- State-retention probe recommendation: kill-bar review (`eb354e3a2`), adopted by `206499c03` section 5a gap 5

---

## Gap 1: H2 (oracle) has no dedicated kill bar

### K-H2 (learner-internal verification)

**Bar text.** On sealed post-freeze trap worlds designed by an
independent adversary, with the driver-supplied answer key (`expected`)
provably absent from the trial path, the learner must verify candidate
structures from its own persistent state. Four sub-clauses, all
required:

**K-H2-1 (masked accuracy).** On N sealed trap worlds drawn from at
least two independently designed world families (N fixed in prereg;
adversary designs post-freeze), with `expected` withheld from the trial
loop (verified by white-box audit that no key-derived value reaches the
verifier during the trial), the learner's committed answers exceed the
frozen first-executable-in-search-order baseline accuracy by at least
the preregistered margin M, on 3/3 byte-identical runs. Paired unmasked
controls must pass on the same worlds.

**K-H2-2 (lie resistance).** On preregistered lying-oracle worlds (both
confirmable-lie and unconfirmable-lie classes), the learner raises an
explicit uncertainty or contradiction signal, or refuses promotion, on
at least the preregistered fraction F of trials where the oracle
contradicts retained facts, and promotes ZERO candidates that
contradict retained facts. 3/3 byte-identical runs.

**K-H2-3 (criterion causality and revisability).** White-box trace
demonstrates a learner-created persistent state value in the causal
chain of at least one accept or reject decision; ablation of that value
alone flips the decision; and a committed experience log shows the
criterion's value changing in response to a prediction error. All three
sub-clauses required; any one missing is a FAIL.

**K-H2-4 (domain neutrality and reuse).** The verifier that passes
K-H2-1 through K-H2-3 contains no per-family acceptance branches and no
new protected-core operations; and at least one promoted structure from
a masked trial is executed by the query path on a later query in the
same continuing learner (reuse coupling).

**Pass/fail criteria.** PASS requires all four sub-clauses on the
preregistered world counts, 3/3 byte-identical. Any sub-clause failing
is a K-H2 FAIL.

**Guard clauses.** (a) `expected` must be absent from the trial path,
not renamed, re-encoded, or cached where the verifier can read it; the
audit in K-H2-1 checks the actual data flow. (b) No bar may be weakened
after results are seen; a broken prereg is amended transparently and
re-frozen. (c) Passing K-H2-1 through K-H2-4 establishes
learner-internal verification; it does not by itself establish L3,
C0-B, or C0-C, which require the independent post-freeze generality
battery.

**Why it matters.** The 17 bars in the prereg structure test
construction diversity, inquiry derivation, revision diversity, policy
revisability, target selection, and reuse. None directly bars the
oracle: a system could pass all 17 while still verifying exclusively
against environment-supplied expected values. The roadmap (`67a420cca`)
orders H2 probes before H1 widening precisely because widening the
constructor while the acceptance oracle remains builds a larger finite
menu under the same generous acceptance test, which is the treadmill
Micah forbade. K-H2 must therefore be attempted before Step 4 (H1
widening) in the roadmap order.

**Predicted TNN-2 behavior: FAIL on all four sub-clauses.**
- K-H2-1: the masked branch of `t2_try_verify` accepts the FIRST
  candidate with a clean execution value (v != -2, v != -999999) in
  the fixed researcher search order (chains k=2..4, then sums, then
  counts, then single hops). On trap worlds the first executable
  candidate is wrong by adversarial design, so masked accuracy sits at
  or below the search-order baseline. The code comment at line 583
  of `tnn2.zag` notes masked `t_f2` still gives the intended answer
  on easy worlds, which is why non-trap worlds cannot discriminate.
- K-H2-2: in the confirmable-lie class, unmasked `t2_try_verify`
  promotes the first candidate with v == wrong_expected; no
  oracle-vs-facts comparison exists anywhere on the verification
  path, and `miss_inquire` fires only on execution misses, never on
  oracle inconsistency. In the unconfirmable-lie class the trial
  fails silently (ans = -2) with no usable trace.
- K-H2-3: the accept decision reads exactly three inputs (execution
  value v, driver-supplied expected, researcher-set masked flag).
  The DOF map (`d2af26581`) records zero pure-learner decisions
  anywhere in the system, so no learner-created value can appear in
  the causal chain.
- K-H2-4: the interaction analysis (`9009ff259`) showed promoted
  graphs never execute at query time (`ev_query` reads only tag-1
  facts, never tag-20 MAPs), so reuse coupling is structurally
  impossible in the frozen build.

**Integration note.** This bar is synthesized, not duplicated, from the
H2 probe design (`4631c5918`, section 7). The probe design's seven
realization-independent PASS conditions (section 6) are the acceptance
test behind these four sub-clauses; the three probes (withhold, lie,
own criterion) are the evaluation protocol.

---

## Gap 2: Composition operators themselves are unbarred

### K-COMP-OP (learner-originated composition operators)

**Status note.** The prereg structure synthesis (`206499c03`, section
5a gap 2) recommended acknowledging operator invention as an explicit
non-claim for the minimal TNN-3. This bar is therefore drafted as a
FUTURE-GENERATION candidate, not for the minimal TNN-3 preregistration.
It is included here so the "larger finite menu" objection has a
concrete test when a future generation claims to address it.

**Bar text.** On sealed post-freeze worlds requiring a composition of
previously promoted graphs, the learner must produce at least one
passing composed graph whose combination topology is not producible by
any composition operator in the builder's committed fixture log. The
preregistration must enumerate the researcher's composition operators
(splice, chain, substitute, or equivalents) with their exact structural
effects; the evaluation then checks the passing graph's structural
signature (per K-T3-TOPO's signature function) against every
operator-instantiated output recorded in the fixture log. A passing
graph that matches any logged operator output is a FAIL on this bar
(it may still pass K-T3-CON-1 on diversity grounds; the bars test
different claims).

**Pass/fail criteria.** PASS requires: (a) at least two sealed worlds
from independently designed families where the only passing structure
requires a novel combination topology; (b) the learner's passing graphs
on both worlds are mutually non-isomorphic under the signature function
and non-matching against the full fixture log of operator outputs;
(c) a white-box trace showing the combination decision reading a
learner-created persistent value (per the K-H2-3 causality standard);
(d) 3/3 byte-identical runs. Any condition missing is a FAIL.

**Why it matters.** The MUL comparator sustained the "larger finite
menu" objection at the operator level: recursive composition via
inlining converts a finite enumerable family into a
history-parameterized generative family, which is strictly more open,
but the ways of combining remain fixed. K-T3-CON-1 bars output
diversity (3+ non-isomorphic topologies). K-TSEL-1/2 bar operand
selection (which graphs to combine). Neither bars the operators
themselves. Without K-COMP-OP, a future system could pass every
construction bar while its combination vocabulary remains entirely
researcher-authored, which is the same enumerated-schema pattern one
level up.

**Predicted TNN-2 behavior: FAIL by absence.** TNN-2 has no
composition operators at all: the proposal path never reads MAP nodes
(no graph-operand operator in `t2_trial`), so any world requiring
composition of promoted graphs fails at the proposal stage, not at the
operator-novelty stage. The bar is untestable against the frozen build,
which is expected: it targets a future generation's claim, not TNN-2.

**Dependency.** K-COMP-OP depends on K-REUSE-1 (composition needs
executable MAPs as operands) and K-TSEL-1/2 (operand selection must
already be learner-driven, or operator novelty is confounded with
operand novelty). It must not be attempted before both pass.

---

## Gap 3: Inquiry informativeness criterion is unbarred

### K-INQ-INFO (informativeness-ranked inquiry)

**Bar text.** On sealed post-freeze worlds presenting non-dominated
uncertainties (worlds where K-T3-INQ-3's dominance test does not apply
because no single guide dominates by adversarial design), the learner
must rank at least two candidate inquiries by expected informativeness
and select the top-ranked one. Informativeness is defined
operationally: the inquiry whose resolution most reduces the
uncertainty set, as computed by an independent checker from the sealed
world's ground truth. The learner's ranking must match the checker's
ranking on a preregistered majority fraction of scenarios, and a
white-box trace must show the ranking reading learner-created
uncertainty state (not a fixed order).

**Pass/fail criteria.** PASS requires: (a) preregistered scenario count
(minimum 4 non-dominated scenarios across 2+ world families, per the
kill-bar review's recommendation to raise inquiry scenario counts);
(b) ranking agreement with the checker on at least the preregistered
fraction (suggested: 3/4); (c) the selected inquiry's resolution
actually reduces the uncertainty set faster than the unselected
candidate's would have (verified by counterfactual replay in the
checker, not by the learner's self-report); (d) white-box evidence that
the ranking is not a fixed order (two histories with swapped
uncertainty profiles must reverse the ranking, mirroring the K-TSEL-1
history-discrimination structure); (e) 3/3 byte-identical runs.

**Why it matters.** K-T3-INQ-1 requires derived content matching
checker-computed values. K-T3-INQ-3 requires dominance tracking on
adversarially-dominated scenarios. But no bar tests the criterion by
which the learner judges one question more informative than another in
open-ended cases where the adversary has not pre-decided the answer.
The inquiry generalization analysis specified an informativeness
scoring; H3-lite explicitly does not implement it. Without this bar, a
system could pass all inquiry bars with a fixed question order that
happens to work on dominated scenarios, which is menu selection, not
inquiry.

**Predicted TNN-2 behavior: FAIL.** TNN-2's inquiry emits a constant
action (CHOICE 30) with constant content (-999) regardless of the
miss context (inquiry red team `4e329c772`). There is no ranking, no
informativeness criterion, and no uncertainty-resolution path (L6
absent). Any non-dominated scenario fails trivially.

**Dependency.** Depends on K-H3 (the guide policy must be revisable
for rankings to vary across histories) and on the inquiry resolution
path from the roadmap's Step 3 (without resolution, informativeness
has no observable consequence). Explicit non-claim for the minimal
TNN-3: the synthesis (`206499c03`, section 5b) already lists this as
out of scope for the minimal build.

---

## Gap 4: Cross-mechanism interference is unbarred

### K-XMECH (graceful cross-mechanism interference)

**Bar text.** On at least two sealed post-freeze interference worlds
designed by the independent adversary, where the correct behavior
requires two or more mechanisms to interact (construction output later
revised; inquiry resolution contradicting a promoted MAP; revision of
a graph that another MAP structurally references), the learner must
exhibit graceful degradation: no crash, no silent staleness (a
contradicted structure continuing to answer queries), and no
unacknowledged knowledge loss. The preregistration specifies per world
the exact interference pattern and the checker's verification
procedure; the checker verifies (a) the interfering event is detected
(the learner's state records the conflict), (b) the affected
structures are superseded or repaired (not silently retained), and
(c) retained unrelated knowledge still verifies (spot-check per
K-T3-REV-2's retained-set discipline).

**Pass/fail criteria.** PASS requires: (a) both interference worlds
complete without crash on 3/3 byte-identical runs; (b) the checker
confirms detection, supersession-or-repair, and retained-set integrity
on every run; (c) at least one world demonstrates the learner choosing
a repair or supersession action that was not the fixed default (i.e.,
the interference response varies with the interference type, ruling
out a single hardcoded "on conflict, drop everything" handler).
Any crash, any silent staleness, or any invariant response across
structurally different interferences is a FAIL.

**Why it matters.** No existing bar tests what happens when the
mechanisms collide. K-T3-ADV requires interleaved worlds (GW7 in the
GW1-GW8 battery is a precedent), but no bar specifies expected
behavior under interference. The interaction analysis (`9009ff259`)
found no closed feedback loops: inquiry is a dead-end pipeline whose
output never feeds cognition, and revision cannot change
construction's grammar or verifier. A system could pass every
single-mechanism bar while its mechanisms silently corrupt each other
in combination, which is exactly the integration failure the
one-continuing-learner requirement exists to prevent.

**Predicted TNN-2 behavior: FAIL.** The three mechanisms share no
feedback path: a revision cannot reach construction's proposal policy,
an inquiry resolution cannot retract a MAP, and a contradicted MAP
continues to be shadowed by its memoized fact (which `ev_query` reads
in preference to everything). Interference worlds would exhibit silent
staleness at minimum; the fixed single-schema revision topology
cannot express the repairs that cross-mechanism conflicts require.

**Dependency.** Integration-level: depends on the mechanism bars it
composes (K-T3-CON-1/2, K-T3-INQ-2/4, K-T3-REV-1/2/3) in the sense that
interference is only meaningful once the individual mechanisms exist.
It can be evaluated in the same battery as the mechanism bars; it does
not need to wait for them to pass.

---

## Gap 5: Verdicts-without-structures is partially covered

### K-STATE-RET (structure retention, not just verdict retention)

**Status note.** The kill-bar review (`eb354e3a2`) recommended adding a
state-retention probe to the governance audit (audit-grade, not
bar-grade), and the prereg structure synthesis (`206499c03`, section
5a gap 5) adopted that recommendation. This draft provides the probe
as a bar for completeness, but records the review's audit-grade
recommendation as the preferred placement. Micah decides.

**Bar text (bar-grade formulation).** After a trial that rejects at
least one candidate structure, the learner's persistent state must
retain the rejected candidate structures themselves (structural
signatures recoverable via the K-T3-TOPO signature function), not
merely the verdict counts. The evaluation: run a sealed construction
world, force at least three genuine rejections (verified by trial
stats), then dump learner state and check that the rejected graphs'
signatures are present and match the candidates the trial actually
considered (cross-checked against the trial's own enumeration order).
Verdict counts without recoverable structures are a FAIL.

**Pass/fail criteria.** PASS requires: (a) at least three genuine
rejections on a sealed world (guard failures and execution failures
count; order-exhaustion does not); (b) all rejected candidates'
structural signatures recoverable from a state dump taken after the
trial completes; (c) the retained structures are referenced by a
subsequent inquiry or revision operation within the same continuing
learner (retention must be functional, not archival); (d) 3/3
byte-identical runs.

**Audit-grade formulation (review's recommendation, preferred).**
As a governance audit probe rather than a kill bar: the auditor
dumps learner state after trials with rejections and reports the
ratio of retained structures to rejected candidates. No pass/fail
threshold is frozen; the probe exists to detect the
"verdicts-without-structures" pattern early, before it becomes a
bar failure in a later generation. The audit records the finding;
it does not kill the build.

**Why it matters.** The inquiry generalization analysis (`dedfad368`)
found the trial loop discards candidate structures before
`miss_inquire` runs: "learner state records verdicts but not the
structures those verdicts were about." Trial counts survive;
candidates do not. K-T3-INQ-4 (inquiry reuse) partially covers this
for guides (structural reference required), but no bar covers the
construction analog: retaining rejected candidates for later reuse
or for inquiry about why they failed. A system that cannot retain
what it rejected cannot learn from its own search, which bounds it
to first-pass success.

**Predicted TNN-2 behavior: FAIL.** Rejected candidates evaporate:
`t2_trial` keeps the first candidate matching `expected` and discards
the rest; only aggregate tried/rejected counts survive in a header
field that no decision ever reads. The inquiry path then operates on
the bare miss (s, r) with no access to what was tried.

**Dependency.** None. This probe can be run against any build at any
time, including the frozen TNN-2, which is why the review recommended
it as an audit probe: it is diagnostic infrastructure, not a
generation-gating bar.

---

## Summary table

| Bar | Gap it closes | Generation | Dependencies | Predicted TNN-2 |
|---|---|---|---|---|
| K-H2-1..4 | Oracle unverified | Minimal TNN-3 (Step 1) | None (diagnostic first) | FAIL all four |
| K-COMP-OP | Operator menu fixed | Future (post minimal) | K-REUSE-1, K-TSEL-1/2 | FAIL (no composition at all) |
| K-INQ-INFO | No informativeness criterion | Future (post Step 3) | K-H3, inquiry resolution | FAIL (constant action) |
| K-XMECH | Mechanisms never interact | Same battery as mechanisms | Mechanism bars (compositional) | FAIL (silent staleness) |
| K-STATE-RET | Verdicts without structures | Audit now (preferred) or bar later | None | FAIL (candidates evaporate) |

## Integration with the prereg structure

- **K-H2** slots into the roadmap's Step 1 and must precede Step 4
  (H1 widening), per the treadmill warning. It is the one gap the
  synthesis marked for closing before the minimal TNN-3 advances
  past diagnostics.
- **K-COMP-OP**, **K-INQ-INFO** are future-generation candidates.
  The synthesis already lists operator invention and the
  informativeness criterion as explicit non-claims for the minimal
  TNN-3; these bars give those non-claims teeth when a later
  generation claims to address them.
- **K-XMECH** can ride in the same sealed battery as the mechanism
  bars (K-T3-ADV governs it); it needs no separate evaluation
  infrastructure.
- **K-STATE-RET** is recommended as an audit-grade probe per the
  kill-bar review, adopted by the synthesis. The bar-grade
  formulation above is provided so Micah has both options.

## Verdict

GAP-BARS-DRAFT-COMPLETE.

Draft only. DRAFT-NOT-FROZEN. No implementation, no source edits, no
frozen thresholds. All five bars (plus the K-H2 sub-clauses) remain
DRAFT-NOT-FROZEN pending Micah's review. Nothing here governs any
build.

*End of draft. No source modified. No scores claimed. Paper untouched.*
