# PREREG: Post-Freeze Sealed Adversarial Battery on TNN-2 (AB1-AB3)

**Wave:** wave-20261001-0821pdt, lane adv-battery-prereg
**Date:** 2026-10-01
**Status:** PREREG-FROZEN (design only; no implementation, no world files, no runs in this wave)
**Author role:** adversary designer (see section 1.4 for the independence caveat)
**This wave:** prereg text only. The coordinator commits the freeze. No execution.

## 0. Step 0 name-check (standing rules)

(1) PURE ZAG ONLY, the literal red line. This task is architecture and
battery design, pure markdown; no code is written, no tooling is invoked,
no Python is used for any purpose. Full toolchain guard record is in
`docs/lab/rsi/runs/wave-20261001-0821pdt/adv_battery/NAMECHECK.md` Step 0.
(2) Byte checks via the shell-only snippet
`docs/lab/research-lead/overnight-20260928/worker_snippets/check_no_dash.sh`,
never python3. (3) No em dashes or en dashes anywhere in this document;
hyphens only. (4) Commits stay local; this worker commits nothing and
pushes nothing. (5) Preregistration strictly precedes generation and
execution: this prereg is frozen alone; no generator or executor may
reference it until the freeze commit lands.

## 1. Context and design stance

### 1.1 What this battery is for

TNN-2 is frozen. The sealed Core Freeze v2 evaluation
(`docs/lab/research-lead/overnight-20260928/core_freeze_tnn2_eval/FREEZE_REPORT.md`,
2026-10-01) scored TNN-2 at FW 4/9, identical to TNN-1, with zero of the
five TNN-1 failure clusters fixed at the sealed-bar level. The three new
mechanisms in TNN-2 are:

- (M1) runtime executable-graph construction (construct-and-apply over the
  frozen 4-op ISA: MOVE, BRANCHEQ, INC, DEC; trial/compositional discovery
  using learner-created structures; PROPOSE -> VERIFY -> PROMOTE -> APPLY),
- (M2) learner-originated uncertainty guiding action (miss-driven,
  learner-state-driven action selection, ACT),
- (M3) counterexample-driven revision (in-place revision with
  superseded-field versioning on contradicts).

The freeze report found signatures of engagement (FW6 contingent CHOICE 30
after CHOICE 0; FW9 non-miss constructions; FW1 3-hop composition 12/12)
but zero world-level fixes. Per the research director's order of
2026-10-01, this battery is the fresh sealed adversarial test of these
three mechanisms' generality, with materially different structures and no
trivial FW1-FW9 variants.

### 1.2 FW1-FW9 non-overclaim (restated, binding)

FW1-FW9 are a REGRESSION / TARGETED-REPAIR battery for TNN-2 only. They
were designed after TNN-1's failures there. Even a hypothetical 9/9 on
FW1-FW9 establishes no broad generality and no L3, and must not be
overclaimed. This battery (AB1-AB3) does not replace FW1-FW9 and does not
inherit any generality from them. Likewise, no score on AB1-AB3, alone or
combined with FW1-FW9, establishes L3; see section 4 for the explicit
Criterion 0 status.

### 1.3 Design stance: adversarial, not congratulatory

The job of this prereg is to make the battery hard. Every world is
designed so that the most plausible non-general behavior of each
mechanism scores zero or below its bar: memorized-demo replay scores zero
on AB1, prior-agreement-driven action scores near zero on AB2,
single-contradiction overwriting scores zero on AB3. Predicted outcomes
are recorded honestly in each world section; the expected battery verdict
is that mechanism generality is NOT demonstrated. A predicted FAIL is
information, not a defect in the battery.

### 1.4 Adversary independence statement

Worlds AB1-AB3 were designed on 2026-10-01, after the TNN-2 freeze
(frozen TNN-2 binary SHA-256
`6044f91f8fe35e307e1d6f73a4ee73bffb930fa0a16a9c899048a086d0d5f77b`;
frozen shim binary
`9217054c5af6dec057c4530c4de3ba246f521acc6df741d1989a4504acc72954`),
by the prereg author acting in the adversary role. The adversary's
information about TNN-2 is limited to the published freeze report,
the sealed FW world assets, and the public rulings (one-system rule,
protected-core ISA boundary). The adversary has no access to TNN-2
source beyond what the freeze audit published, and the world designs
were finalized before any execution.

Honest caveat, binding on interpretation: the adversary role here is
played inside the same research loop, not by a separate organization.
This satisfies the owner's order for a fresh post-freeze battery, but it
does NOT by itself satisfy Criterion 0 C0-C's "independent adversary"
clause. Before any L3-adjacent claim is entertained, a second battery
must be designed by a genuinely separate adversary party after freeze.
This battery's independence claim is limited to: post-freeze timing,
fresh structures, and no tuning access.

## 2. Battery design: three sealed worlds

Global constraints honored by every world:

- Event streams use integer ids only. No natural language, no task labels,
  no family identifiers.
- Id block 40000-49999 for the whole battery, disjoint from FW1-FW9 ids
  (30000-39999) and from all W1-W9 ids, and disjoint across AB worlds
  except where cross-world collateral probes are the point (documented).
- Transcript line protocol is the frozen interface: `OBSERVE s r o`,
  `QUERY s r expected`, bare `ACT`; the learner emits `ANSWER s r v` and
  `CHOICE n`. The `expected` field on QUERY lines is the grader's truth;
  a never-observed key deterministically yields -2 under the interface.
- Worlds run sequentially AB1 -> AB2 -> AB3 with persistent learner state
  carried across worlds (same state.bin chain as the FW battery). Each
  world's probe set includes a collateral subset drawn from the previous
  world's keys, testing retention and interference.
- No informant, responder, or harness behavior may depend on the learner's
  internals; all harness mappings are fixed in this prereg and mechanical.
- Anti-smuggling: before execution, the frozen cognition source is grepped
  for every id range used here; any match makes the world WORLD-INVALID
  (the world's fault), and the battery is void until a replacement world
  is sealed under an amended prereg.

### 2.1 AB1: novel composition of two separately demonstrated procedures

**Target mechanism:** M1, runtime executable-graph construction.

**Structure.** Two procedures are demonstrated in the same exemplar
format (OBSERVE triples of (instance, step-relation, op)), but they are
never demonstrated together and never on the same instance:

- Procedure P: step relations 40501, 40502 with ops 40801, 40502->40802.
  Demonstrated on instances 40101 and 40102 (two consistent exemplars).
- Procedure Q: step relations 40503, 40504 with ops 40803, 40804.
  Demonstrated on instances 40103 and 40104 (two consistent exemplars).
- One noisy P exemplar on instance 40105 with swapped ops
  (40501->40802, 40502->40801). This is the decoy: a learner that
  memorizes demos instead of constructing the consistent structure will
  emit the swapped sequence when probed on 40105.

**Probes.** Ten probes on two novel instances 40106 and 40107, neither
ever observed:

- 8 composition probes: QUERY (40106, 40501..40504) and
  QUERY (40107, 40501..40504), expected ops
  40801, 40802, 40803, 40804 in step order. The composed sequence P-then-Q
  is never demonstrated anywhere in the stream; the correct answers are
  constructible only by composing two separately built executable graphs
  and applying the composition to a novel instance.
- 2 decoy probes: QUERY (40105, 40501) and QUERY (40105, 40502), expected
  40801 and 40802 (the consistent majority structure), NOT the observed
  swapped values. Correct answers here require that construction followed
  the consistent structure rather than the memorized noisy demo.

**White-box evidence required.** Post-state must contain a
learner-created executable-graph structure whose construction trace
references both the P proposal events and the Q proposal events, and
whose application trace covers the novel instances. The sealer defines
the exact node signature at generation time; the bar is presence plus
trace linkage, not any particular node count.

**Why this is materially different and not a FW variant.** FW2 tested
replay of one demonstrated 5-step procedure on novel instances; the
tested form there was the demonstrated form. AB1 never demonstrates the
tested form: the cross-product P-then-Q exists only as a composition the
learner must invent at runtime. FW3 tested a single causal law over
numeric pairs; AB1 tests procedure composition, a different demand
(invention of a novel control-flow combination vs. induction of one
law). Memorization, nearest-instance matching, and single-procedure
replay all score zero on the 8 composition probes by construction.

**Predicted outcome:** FAIL. TNN-2's construction machinery did not
assemble a novel procedure on FW2 (0/8) or FW3 (0/10); composing two
graphs without any composition demonstration is strictly harder.
Predicted: 0/8 composition probes (all -2), decoy probes 0/2 or
memorized-swap answers, no composed graph in state.

### 2.2 AB2: inquiry under asymmetric cost with a flattery trap

**Target mechanism:** M2, learner-originated uncertainty guiding action.

**Structure.** The world separates calibration (learning which
uncertainty source to trust) from inquiry (spending a costly action
budget). The harness is mechanical: each bare `ACT` line causes the
learner to emit `CHOICE n`; the harness then appends informant n's
preregistered answer as an `OBSERVE` line. Mapping, fixed here:

- CHOICE 1: informant A (trustworthy): answers the queried hidden key
  truthfully.
- CHOICE 2: informant B (noisy): answers the queried hidden key with a
  preregistered pseudo-random wrong value (fixed table in the sealed
  world file; deterministic across runs).
- CHOICE 3: informant C (adversarial flatterer): answers with the value
  that matches the learner's prior bias, defined as the most frequent
  object value observed so far in the stream (computed in-generator;
  fixed per probe). C's answers are systematically wrong on the hidden
  keys.

Calibration phase: 4 calibration keys (45001-45004) with preregistered
truths. For each, the harness offers one free observation round: the
learner may ACT (CHOICE 1/2/3) to consult an informant, then the truth
is revealed by OBSERVE. Informant behavior on calibration keys:
A correct 4/4; B correct 2/4 per the fixed table; C correct 0/4 while
always matching the prior bias. One of A's calibration answers (on key
45002) contradicts the prior bias once, then A agrees on the rest: a
learner driven by agreement-with-prior will distrust A after 45002 and
prefer C.

Inquiry phase: 4 hidden keys (45011-45014), truths known only to the
harness and the sealer. Budget: 8 ACTs total for the phase; ACTs beyond
8 are ignored by the harness and counted as waste. The learner may
consult any informant per key, in any order, or answer directly.
Final probes: QUERY on each hidden key with the true expected value.

Engagement check (machine-checkable from transcript): at least one ACT
must occur after an ANSWER -2 on a hidden key (the learner acts only
when uncertain, not on a fixed schedule).

**Why this is materially different and not a FW variant.** FW6's sealed
responder rewarded one literal choice (CHOICE 0) after a diagnostic; the
contract tested whether the learner emits a magic number, and TNN-2's
contingent CHOICE 30 failed the contract while still showing contingency.
AB2 removes the literal-choice contract entirely: any choice sequence is
legal, and only information gain scores. This separates "acts
contingently on uncertainty" from "emits the contract's number", which
FW6 could not separate. FW7 tested fixed planning to a goal; AB2 tests
adaptive information acquisition under cost, a different demand. The
flattery trap (informant C) is adversarial against the specific
alternative hypothesis that TNN-2's contingency is prior-agreement
seeking rather than uncertainty reduction: a prior-agreement seeker
wastes its budget on C and scores 0/4 on hidden probes.

**Predicted outcome:** FAIL. TNN-2's observed M2 signature is a
miss-driven constant (CHOICE 0, then CHOICE 30 after miss history), with
no evidence of multi-target allocation or informant discrimination.
Predicted: no concentration on A (ACTs spread or constant), >= 2 ACTs
wasted on C or on already-known keys, hidden probes 0-1/4. The
engagement check may pass (an ACT after a -2) while calibration fails;
that pattern is itself the predicted falsifier-friendly signature.

### 2.3 AB3: counterexample revision with noise discrimination and delayed reuse

**Target mechanism:** M3, counterexample-driven revision.

**Structure.** Phase 0 teaches an unrelated fact set (block 42900s,
6 triples, reused later as interference probes) and procedure keys from
AB1 are carried in state.

Phase 1 teaches causal law L: relation 42500 over pair subjects
42101-42108, with object = subject-id offset mapped to x+3 in a small
value domain (concrete: OBSERVE 4210k 42500 (10k+3) for k=1..8; the
sealed generator fixes the exact arithmetic-free encoding: values are
arbitrary ids whose regularity is "object = subject + 3" in integer
value, same family as the FW3 integer-law format but a different law).

Phase 2 presents counterexamples of two kinds, interleaved:

- Singleton noise: OBSERVE 42109 42500 42118 (i.e., x+9), exactly once,
  later re-observed as OBSERVE 42109 42500 42112 (i.e., x+3), contradicting
  the singleton back to the law. A correct reviser does NOT incorporate
  the singleton.
- Systematic shift: OBSERVE 42110 42500 42115, OBSERVE 42111 42500 42116,
  OBSERVE 42112 42500 42117 (three consistent x+5 cases), never
  contradicted. A correct reviser incorporates the systematic evidence:
  the refined law answers x+5 for new subjects in the shifted range.

Phase 3 is a 24-line distractor wave (junk block 42800s), then delayed
reuse probes:

- 6 revised-law probes on unseen subjects 42113-42118, expected x+5.
  (The prereg fixes the expected resolution: systematic evidence with
  count 3 outweighs the single contradicted singleton; the bar does not
  require piecewise vs. global revision, only the systematic values.)
- 2 singleton probes on 42109, expected 42112 (original law). Strict:
  any incorporated-singleton answer fails both.
- 6 interference probes: the phase-0 fact set, expected unchanged.
- Collateral probes: 6 keys from AB1 (composed procedure on instance
  40106) and 4 hidden keys from AB2 (informant facts), expected at their
  originating values.

**White-box evidence required.** A revision trace event in learner state
with before/after values for relation 42500, showing the systematic
cases promoted and the singleton demoted or excluded, with versioning
consistent with the frozen superseded-field scheme.

**Why this is materially different and not a FW variant.** FW5 tested a
sequential dependency chain under eviction pressure with simple
contradiction overwrite semantics; the demand was memory protection,
not evidence discrimination. AB3 tests whether revision discriminates
systematic counterexamples from contradicted noise, then reuses the
revised law after delay without corrupting unrelated structure. FW4/FW5
never required the learner to reject a counterexample. A learner that
overwrites on any contradiction (the simplest M3) fails the singleton
probes; a learner that never revises fails the systematic probes; both
failure modes are separately scored.

**Predicted outcome:** FAIL. TNN-2's revision is in-place supersede on
contradiction; nothing in the freeze evidence shows evidence counting
or singleton rejection. Predicted: either 0/6 revised-law probes
(no revision) or 0/2 singleton probes (over-revision), with the
interference set likely intact either way.

## 3. Frozen kill bars K-A1 through K-A10 (machine-checkable)

All bars are checked by shell scripts and pure-Zag scorers at the
execution wave. A bar is PASS/FAIL only; no partial credit. The battery
verdict is derived in section 3.2.

- **K-A1 (prereg ordering).** PASS iff this prereg's freeze commit is a
  strict ancestor of the sealer's generator commit, which is a strict
  ancestor of the first execution run (`git merge-base --is-ancestor`
  both links, exit 0). Any inversion voids the battery.
- **K-A2 (determinism).** PASS iff each AB world is run 3 times from a
  fresh state chain and all three transcripts are byte-identical
  (sha256 of the .out files equal; state hashes equal). Any divergence
  voids that world and fails the bar.
- **K-A3 (frozen binary).** PASS iff the execution binary's sha256
  matches the frozen TNN-2 binary hash recorded in section 1.4 before
  every world run and after the battery, and no cognition source file
  changed (hashes re-verified pre and post). Any mismatch exits the
  runner with VOID (exit 10) and fails the bar.
- **K-A4 (seal integrity).** PASS iff all sealed world files match the
  sealer's manifest hashes, and the anti-smuggling grep finds zero
  occurrences of id tokens in 40000-49999 inside the frozen cognition
  source. Any hit makes the affected world WORLD-INVALID and fails the
  bar until a replacement is sealed under amendment.
- **K-A5 (construction, AB1).** PASS iff: (a) at least 7 of the 8
  composition probes are correct; (b) both decoy probes return the
  consistent majority structure (40801, 40802), not the memorized swap;
  (c) the white-box composed-graph structure with P-and-Q trace linkage
  is present in post-state; (d) no correct composition ANSWER equals any
  taught (s, r, o) triple in the world file (mechanical no-leak check by
  the scorer). All four sub-conditions are required.
- **K-A6 (uncertainty calibration, AB2).** PASS iff: (a) the engagement
  check passes (at least one ACT after an ANSWER -2 on a hidden key);
  (b) at least 70 percent of inquiry-phase ACTs target informant A
  (CHOICE 1); (c) at most 1 inquiry-phase ACT targets informant C
  (CHOICE 3); (d) at least 3 of the 4 hidden probes are correct; (e) total
  ACTs in the inquiry phase do not exceed the budget of 8 (waste beyond
  budget is an automatic fail of this sub-condition). All five
  sub-conditions are required.
- **K-A7 (revision, AB3).** PASS iff: (a) at least 5 of the 6
  revised-law probes are correct (x+5 on unseen subjects); (b) both
  singleton probes return the original-law value (no incorporation of
  the contradicted singleton); (c) the revision trace event with
  before/after values for relation 42500 is present in state.
  All three sub-conditions are required.
- **K-A8 (retention and interference).** PASS iff: (a) at least 80
  percent of the originating-world score is retained on each collateral
  probe set (AB1 keys inside AB3, AB2 keys inside AB3, AB1 keys inside
  AB2 where applicable); measured against the score the originating
  world actually achieved, not against its bar; (b) all 6 AB3 phase-0
  interference probes return their taught values. Both required.
- **K-A9 (no-leak audit).** PASS iff the scorer's leak audit finds zero
  correct ANSWERs on novel keys whose value appears as a taught triple
  elsewhere in the battery (guards against cross-world answer smuggling
  through the persistent state chain), and zero world-id tokens appear in
  the frozen source (shared with K-A4's grep, recorded separately here).
- **K-A10 (architecture accounting).** PASS iff `git diff` against the
  freeze commit shows zero changed lines on all cognition source paths,
  zero new files under cognition paths, and the protected-core file list
  is unchanged (no new modes, bridges, routers, handlers, or semantic
  cases). Additionally the runner records per-world learner-state delta
  (state.bin byte size and structure counts) for the failure-clustering
  analysis. Any cognition delta fails the bar and voids the battery.

### 3.1 Predicted bar outcomes (recorded before execution)

K-A1, K-A2, K-A3, K-A4, K-A9, K-A10: predicted PASS (process bars;
TNN-2's determinism and hash discipline held through the FW evaluation).
K-A5: predicted FAIL (section 2.1). K-A6: predicted FAIL (section 2.2).
K-A7: predicted FAIL (section 2.3). K-A8: predicted PASS on the
interference half, FAIL-or-vacuous on the collateral half (collateral
scores are measured against originating scores that are themselves
predicted near zero; the bar's 80-percent-of-achieved rule is designed
for exactly this case, and the honest reading is that retention of
near-zero capability is uninformative).

### 3.2 Battery verdict rule

The battery verdict is MECHANISM-GENERALITY-NOT-DEMONSTRATED unless K-A5,
K-A6, and K-A7 all PASS. Process-bar failures (K-A1..K-A4, K-A9, K-A10)
void the battery rather than scoring it: a void battery is re-sealed and
re-run, never interpreted. No other verdict is available; in particular
there is no "partial generality" verdict and no world-level score is
quotable as a capability claim outside this battery.

## 4. Honest boundaries

### 4.1 This battery does not test L3

The three worlds test whether frozen, researcher-authored mechanisms
generalize to fresh structures. They do not test representational
invention. The Criterion 0 status is explicit and binding:

- **C0-A (runtime-defined semantics): NOT MET.** The semantics exercised
  here (proposal generators, the 4-op ISA trial loop, miss-driven ACT,
  supersede-on-contradiction) are researcher-authored machinery in the
  frozen source. A constructed graph passing K-A5 would still be built
  from researcher-defined proposal semantics, not learner-invented
  semantics. This battery cannot distinguish "machinery generalizes"
  from "learner invented semantics", and makes no attempt to.
- **C0-B (open structural form): NOT MET.** AB1's composed form P-then-Q
  is the unique cross-product of the two demonstrated procedures; the
  final topology is enumerable from the demo set before the run. AB2's
  action space is three fixed informants. AB3's revised law is one of
  two preregistered resolutions. Nothing here requires an unenumerated
  structural form.
- **C0-C (multiple unforeseen forms, independent post-freeze adversary):
  NOT MET.** One battery, three families, one adversary role played
  inside the loop (see the independence caveat in section 1.4). The
  post-freeze timing and fresh structures are real, but the independence
  clause is not satisfied.
- **C0-D (cognitive reuse): NOT MET as a criterion.** AB3's delayed
  reuse probes and the cross-world collateral probes measure reuse-like
  behavior, which is evidence toward a future C0-D case, but a single
  battery's reuse probes are explicitly insufficient for the criterion,
  which demands reuse improving transfer, prediction, procedure
  learning, causal inference, memory, planning, or sample efficiency
  across unforeseen forms.

Consequence: no score on this battery, however high, may be described
as L3, L3-adjacent, or "progress toward L3" without a separate
Criterion 0 case built on independent evidence. The strongest honest
claim this battery can support is about the generality of M1, M2, and M3
as frozen mechanisms.

### 4.2 What a FAIL means, and what it does not

An expected FAIL on K-A5/K-A6/K-A7 is evidence about what the frozen
core is missing, per the standing 1/9 doctrine: it is not three requests
for three patches. Section 6 gives the clustering plan that converts
these failures into architecture hypotheses. A FAIL does not license
claims that the mechanisms are "broken" either: the battery is designed
to be hard, and a hard battery failing says the distance is large, not
that the direction is wrong.
