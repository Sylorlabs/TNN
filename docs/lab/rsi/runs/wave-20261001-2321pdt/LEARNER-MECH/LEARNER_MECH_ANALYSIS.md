# LEARNER-MECH root-cause analysis: why the continuing learner cannot own integration

Wave: wave-20261001-2321pdt. Lane: LEARNER-MECH (analysis only).
Replaces no verdict; consumes CONTLEARN-OWNED MACHINERY-DEPENDENT
(VERDICT_OWNED.md, JUDGE_BRIEF.md). Read-only toward the CONTLEARN-OWNED
lane dir and the frozen TNN-2 sources. No patch, handler, mode, or opcode
is proposed here (TNN-3 governance decides designs).

Frozen core under analysis: `docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag`,
commit f4de7ff46, 1591 lines, SHA-256
`a29972ca8183b2857c0c7b262d004fce6e4547c12ff8c05f9ebd9152dddca9efeb2a3b44064ec9d`
(reverified this lane: `git hash-object` ->
`b226b223cb3ee0be742af673653fb8ea8605f281`, equals the f4de7ff46 freeze
blob; `sha256sum` ->
`a29972ca8183b2857c0c7b262d004fce6e4547c12ff8c05f9ebd9152dddca9efeb2a3b44064ec9d`).

Note: no em-dashes are used in this document.

## 1. The discrimination being explained

With the event-triggered trial/promotion/P-INV machinery removed from the
query path, the continuing learner integrates 0/6 fresh 2-hop chains (all
18 family-D probes take the true miss path; zero MAP nodes; only
UNCERTAINTY/guide accumulation), while the unmodified frozen core
integrates 6/6 with 6 MAPs and 24 machinery-written DEP edges. Taught
1-hop facts are served 6/6 by standing retrieval in both conditions. The
question this analysis answers: what, exactly, in the frozen architecture
makes learner-owned initiation of integration impossible?

## 2. Catalog of the control plane: who can initiate what

The frozen core has four event entry points, all invoked by the external
driver (the researcher), never by learner-created state:

- `ev_teach` (line 297): allocates a fact node, links ET_PRO/ET_INS edges.
- `ev_query` (lines 813-836): the only event on the integration path.
- `ev_observe` (line 836): contradiction/revision entry point.
- `ev_act` (line 859): selects over learner-constructed guides by bid.

Main (line 1357) only runs self-tests; the continuing-learner drivers call
the four events from outside.

Every structure construction in the cognitive path is initiated inside one
of these handlers, in a hardcoded sequence. In particular `ev_query` runs
an unconditional linear chain on miss:

1. `activate` (line 140): exact-hit retrieval over learner-created edges
   and standing. Reads state; constructs nothing.
2. `mp_run` (line 827): trial construction. Call-site inventory verified by
   grep: `mp_run` has exactly one call site (ev_query:827); `t2_trial` one
   (mp_run:670); `t2_try_verify` four (t2_trial only); `promote_graph` four
   (t2_trial only); `bootstrap_miss` one (ev_query:830).
3. `bootstrap_miss` (line 830): P-INV statistical bootstrap, constructs a
   MAP on >=k facts sharing a value.
4. `miss_inquire` (lines 795-812): allocates an UNCERTAINTY node (tag 30)
   and a guide fact (tag 1) linked to POLICY_ROOT.

Step 4 is the only learner-side construction the discrimination left
running, and it is itself initiated by the researcher event: a query event
must arrive for it to fire. The learner cannot trigger a query.

## 3. The exact mechanism gap

The gap is (a): no learner-state structure can initiate construction. The
fuller statement, with the two reinforcing sub-gaps:

(a) Initiation is event-only. There is no call path from any
learner-created node, edge type, frame state, or POLICY_ROOT-linked
structure back into `mp_run`, `t2_trial`, `promote_graph`, or
`bootstrap_miss`. Learner state is read as DATA by the machinery
(`t2_gather` reads facts for chain search; `activate` reads edges for
retrieval; `ev_act` reads guides for bid selection) but never as CONTROL.
Nothing in state can gate, enable, defer, retry, or redirect the trial
loop.

(c) Control parameters bypass learner state entirely. `mp_run` derives its
control bits (masked, dc, di) from the event's `flags` argument and its
accept oracle from the event's `expected` argument. The "learner-set miss
policy" comment at line 828 is inaccurate as a description of control
flow: `mp_set`/`mp_get` are called only in test functions (lines 1010+),
never in the cognition path, and `mp_run` never reads the mp slot. The
researcher, as event caller, sets whether trials run and how they are
verified. So even the one policy dial that looks learner-settable is
event-fed.

(b) variant, weak form: the trigger `mp_run` exists as a function, but it
is event-invoked, and the branch structure of `ev_query` gives learner
state no way to re-invoke it. When TREAT's 18 probes hit the miss path,
the sequence was mp_run(absent) -> bootstrap_miss(absent) ->
miss_inquire(fired, UNCERTAINTY/guide accumulation). The miss path has no
branch keyed on learner state that could escalate from "reify uncertainty"
to "attempt trial construction." The observed accumulation of 6/12/18
UNCERTAINTY+guide pairs is construction happening, but reflexively, on a
researcher-initiated event, and it cannot recurse into integration.

What is NOT the gap: the primitive construction operations themselves.
`alloc_node` and `link_edge` are already reachable from the cognitive
path (ev_teach, miss_inquire, promote_graph, revise machinery); the
4-op ISA `execute()` is approved protected machinery; and the products
of integration are already usable by standing mechanisms (promoted MAPs
serve later queries via exact-hit retrieval of the taught answer fact).
The substrate can build and can use what was built. What it cannot do is
decide, from its own state, to build.

## 4. General substrate properties that would enable learner-owned integration

Stated as properties of the control plane, not as a design:

1. Initiation-from-state. Some construction service (trial, promote, or a
   successor) must be reachable from learner-created state, not only from
   the event interface. Concretely: a structure the learner created must
   be able to cause the construction machinery to run, on the learner's
   schedule rather than on the arrival of a researcher event.

2. Control-from-state. The gating and parameterization of construction
   (whether to attempt, in what search order, under what accept rule)
   must be readable from learner-created state, not only from event
   arguments. A miss policy that is set by the event caller is
   researcher-set, whatever the comment says.

3. Trigger-from-state. The decision of when to attempt integration versus
   merely reify uncertainty must be expressible in learner state and
   honored by the control plane. The current miss path hardcodes the
   escalation order and gives state no vote in it.

4. White-box visibility of the initiation act. Any future claim of
   learner-owned integration must be able to show, in persistent learner
   state, the structure that caused construction to start (the analog of
   how `promote_graph` leaves construction-provenance DEP edges).

Property 4 already holds; properties 1-3 are absent. Note that property 1
does not require a new mode, bridge, or handler: the question is only
which invocations can start the existing construction service.

## 5. Scoring against the constitution's learner-authority metric

The constitution's desired trajectory: LEARNER AUTHORITY up while HUMAN
HAND-HOLDING down. On this discrimination, learner authority over
integration is effectively zero: the learner records facts (ev_teach),
reifies uncertainty (miss_inquire), and selects guides (ev_act), but
cannot initiate the one construction act that integrates new experience.
Human hand-holding is maximal on the integration path: the researcher
fires the query event, sets flags and expected, and the machinery does
the work. The 6/6 -> 0/6 drop when exactly that machinery is removed is
the measurement of the hand-holding share.

What would close the gap, in the constitution's terms: a run in which the
event-triggered machinery is disabled and the learner nevertheless
integrates, with white-box evidence that a learner-created structure
initiated the construction (property 4 above). The bar to pass would be
CO-1 (6/6 store, 12/12 reuse, 12/12 delayed) via a construction path
reachable from learner state, not via the event path. Until such a run
exists, any integration result on TNN-2 remains MACHINERY-DEPENDENT in the
strong sense: the learner does not decide or author the integration.

## 6. Boundaries and non-claims

- No learner agency in the causal sense is claimed or denied here
  (H2-v2/H3 stand); this analysis is about control-flow reachability in
  the frozen source, which is a prerequisite for any such claim.
- No procedure execution at query time is analyzed; the CONTROL reuse path
  is exact-hit retrieval of machinery-taught facts (Attack 6 carried
  forward).
- No L3 or generality claim. The battery is disclosed-in-prereg with fresh
  ids/relations, not a sealed adversarial world.
- This analysis proposes no patch, handler, mode, bridge, or opcode. Any
  change to the protected-core boundary or initiation semantics is
  TNN-3 governance.
