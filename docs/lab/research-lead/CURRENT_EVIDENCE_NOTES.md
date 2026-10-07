# Current evidence notes and interpretation corrections

Date: 2026-10-06. Base: ownership 91b2acc29. Fast branch only; not merged.
This is a correction layer, NOT a rewrite of historical results or preregs.
See RESEARCH_GOALS_AND_TESTS.md for the operational goal and hypothesis matrix.

## Verified matcher correction

Fresh pure-Zag audit: overnight-20260928/fast_membership_order/REPORT.md.
The original p6struct fixture reproduces its 3/340 result. Its matcher is NOT a
qualified general exact-membership scorer: locally successful alternatives return
one endpoint and do not backtrack in a parent's suffix. Equivalent rule orders
change acceptance. Root semantics and any-nonterminal union must be separated.
Do not infer learner induction failures from this scorer on general grammars.

The fixture A2->A0->A1 is acyclic. Nested recursive function calls are required by
its implementation, but it does not demonstrate a recursive language, dependency
cycle, or depth generalization. Context-free grammar membership is decidable; the
report's reference to undecidable unrestricted grammars does not describe this
particular bounded context-free representation.

The statistical-versus-structural claim is too broad. A finite-state probabilistic
model with declared support can both generate and decide positive-support membership.
Whether its learned support is useful is empirical. Exact consistency does not alone
require a production grammar, and neither representation class establishes ownership.

p6struct PREREG S4 predicts accept-everything after deleting productions. Actual
unchanged parser behavior is reject-everything. Test positive acceptance loss and
negative rejection separately. All-reject is not evidence learned negative knowledge.
Consult count alone (S5) cannot exclude always-consult-everything; require matched
rival behavior. Different right/wrong updates (S6) alone do not prove an acquired
policy. Constant coincidence (S7) is not leakage: audit information flow and whether
complete final solutions were supplied instead.

## Architecture compression: scope correction

composition_synthesis/COMPOSITION_SYNTHESIS.md claims a unified module inherited the
full GEN envelope. contract_unify/REPORT.md explicitly says GEN trial-round machinery
was NOT re-run; only the chosen drift and grammar scenarios were tested. Treat full
subsumption as a hypothesis requiring regressions, not established integration.
The same report discloses a fixed 11-feature library and a tie-break direction chosen
to satisfy frozen targets. Zero scenario branches is useful, not proof no handholding.

learned_contracts reports six singleton kinds learned from behavior. This is bounded
behavior-based refinement. Require the flat probe-table rival before crediting kinds
with representational necessity, type abstraction, or novel method ownership.

## Hypothesis language: prospective, not measured

l2_ess_hypothesis/HYPOTHESIS.md explicitly records no builds or runs. Its PASS by
construction statements are proposed properties. Learned schedulers can also retire,
retry, and recover; behavioral evidence and rival predictions decide utility, not the
word distrust. Generic fixed update thresholds are an architectural bias, not by
themselves task-specific handholding. Task-specific thresholds/labels remain a concern.

## Control versus prediction

A learned applicability contract may legitimately widen after new success. That is
not automatically a human safety invariant. Separate immutable authorized limits,
revisable predictive beliefs, and per-contract episode/revision state. Ask whether
updates can erase previous rejects or affect unrelated contracts before claiming
reliable control. Preregistered small probes are now executed:
[fast_goals_20261006/REPORT.md](overnight-20260928/fast_goals_20261006/REPORT.md).
Growth admitted a stored reject, shared A failures triggered B revision, and the
flat probe-table rival matched singleton-kind selection exactly. Both original
positive scenarios also reproduced byte-for-byte after an output-only host shim.
These findings are narrow; no actual TNN safety violation or broad impossibility
of contract learning is established.

## Subsequent executed fast-loop evidence

See [FAST_RESEARCH_LOOP.md](FAST_RESEARCH_LOOP.md). The endpoint-set scorer fork
matches independent oracles over8160 bounded queries, but is not a production repair.
Known-reject growth and isolated-history forks are generic engineering controls,
not learner-created policy; the growth guard fails on an unseen forbidden intermediate.
Method, action and protocol positives tie simpler same-information rivals. They are
microlearners, not capabilities measured on current TNN.

The unchanged frozen TNN-2 reference was also executed directly:
[core information-flow audit](overnight-20260928/fast_core_20261006/REPORT.md).
Identical observations return31 or32 depending on expected input. The source comment
post-hoc-only must be read as supervised trial feedback, not post-return-only feedback.
With no expected answer the unmasked query abstains; masked mode accepts first route.
The query relation is deliberately underdetermined, so this is an information-flow
result, not a failure to infer knowable semantics. Latest production equivalence is
unestablished. Historical source/report comments remain intact; this is a dated correction.

## General evidence ceiling

Latest queue still lists measure-tnn and human external-red-team as blocked. Harness
reports are not proof the canonical persistent learner works; deterministic repeats
are not independent replication. No matched transformer control/autonomy experiment
has been qualified here. Do not infer comparative advantage from architecture labels.
