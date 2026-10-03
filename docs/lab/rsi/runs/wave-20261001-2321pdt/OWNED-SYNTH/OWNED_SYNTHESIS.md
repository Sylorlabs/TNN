# OWNED-SYNTHESIS: learner-owned integration, five verdicts synthesized

Wave: wave-20261001-2321pdt. Lane: OWNED-SYNTH (synthesis only; read-only toward
the five source lanes; no experiments). For the debate group and TNN-3 governance.

Note: no em-dashes are used in this document.

## 1. The five inputs

| # | Lane | Result | Nature |
|---|------|--------|--------|
| 1 | CONTLEARN | BUILD-PASS, LEARNOWN-DEMONSTRATED | Frozen execution, K0-K6 all pass, with red-team QUALIFY carried in |
| 2 | CONTLEARN-OWNED | MACHINERY-DEPENDENT (0/6 vs 6/6) | Machinery-disabled discrimination, frozen prereg |
| 3 | CONTLEARN-OWNED2 | MACHINERY-DEPENDENT (0/6 vs 6/6) | Independent replication of #2, amended prereg, discarded pilot |
| 4 | LEARNER-MECH | Root-cause analysis | White-box: no learner-state initiation path |
| 5 | MECH-VERIFY | CONFIRMED x3 | Independent verification of #4's three claims |

## 2. The established fact, doubly confirmed

On a fixed disclosed battery of fresh 2-hop chains, the continuing learner
integrates 0/6 without the event-triggered trial/promotion/P-INV machinery
and 6/6 with it, on the identical battery. CONTLEARN-OWNED measured this
(STORE_OK 0/6 vs 6/6, REUSE 6/12 vs 12/12, DELAYED 6/12 vs 12/12, all probes
on the true miss path in TREAT, zero MAP nodes at every phase).
CONTLEARN-OWNED2 reproduced it independently (STORE_OK 0/6 vs 6/6, REUSE
6/12 vs 12/12, DELAYED 6/12 vs 12/12, MAPC=0 at all three censuses, DEPC
equal to GUIDEC at 6/12/18, proving the only learner-side edges ever
written were guide-to-UNCERTAINTY links). In both lanes standing retrieval
of taught 1-hop facts was intact in TREAT (6/6), proving the variant is
functional and the failure is a capability gap, not breakage. Both lanes
are 3/3 byte-identical, all bars except the discriminating CO-1 pass, and
both pass K0-K6 process bars.

"Learner-owned integration" in the strong sense (the learner decides or
authors the integration) is MACHINERY-DEPENDENT. That is the doubly
confirmed fact.

## 3. The supersession: how LEARNOWN-DEMONSTRATED is now bounded

CONTLEARN's BUILD-PASS stands on its own frozen bars: unsupervised store
13/13, masked reuse 20/20 across 3 task families, ablation-verified
dependence on stored structures (deletion drops original-value reuse
0/20), nostore control 0/20, byte-identical determinism. The verdict
document itself stated the scope explicitly: the workspace is owned in the
weak H10 sense (resident in the learner's arena, manipulated only through
the frozen event interface), and the strong sense was not claimed.

The two machinery-disabled lanes upgrade that scope statement. Per
CONTLEARN-OWNED's verdict: "the strong sense (the learner decides or
authors) is now measured absent, not merely unclaimed." The correct bounded
reading of the LEARNOWN-DEMONSTRATED label is now:

**LEARNOWN-DEMONSTRATED (machinery-enabled scope):** on the disclosed
battery, the store/reuse/reuse mechanics do not depend on per-query answer
keys (the 2021pdt red-team qualification), AND they do depend on the
researcher event-triggered construction machinery (the 2321pdt
discrimination). The learner's own mechanisms (standing retrieval, UNCERTAINTY
reification, guide construction) demonstrably respond to the new experience
(6/12/18 UNCERTAINTY+guide pairs accumulate), but that response never
recurses into integration: no mechanism reads the guides to build
anything, and zero MAPs are ever constructed.

This supersession is a refinement of the claim boundary, not a retraction
of the evidence. The 13/13 and 20/20 measurements remain true of the
machinery-enabled core; what changed is that the strong reading is
falsified, so citing LEARNOWN-DEMONSTRATED must always name the
machinery-enabled scope.

## 4. The mechanism gap (LEARNER-MECH, MECH-VERIFY CONFIRMED x3)

The frozen core (1591 lines, blob b226b223cb3ee0be742af673653fb8ea8605f281)
was analyzed for control-flow reachability into construction, and all three
claims were independently verified against the frozen bytes:

(a) Initiation is event-only. The construction machinery (mp_run, t2_trial,
t2_try_verify, promote_graph, bootstrap_miss) has no call path from any
learner-created node, edge type, frame state, or POLICY_ROOT-linked
structure. Every construction entry is reachable only from the four
researcher-invoked event handlers (ev_teach, ev_query, ev_observe, ev_act)
or self-tests. Learner state is read as DATA (t2_gather, activate, ev_act
bid selection) but never as CONTROL. Nothing in state can gate, enable,
defer, retry, or redirect the trial loop.

(b) Control parameters bypass learner state entirely. mp_run derives its
control bits and accept oracle from the event's flags/expected arguments.
The "learner-set miss policy" comment is inaccurate as a control-flow
description: mp_set/mp_get are called only in a self-test; mp_run never
reads the mp slot. The researcher, as event caller, sets whether trials
run and how they are verified.

(c) The miss path hardcodes escalation. ev_query runs trial -> bootstrap ->
inquire on miss with no branch keyed on learner state. The observed 18
UNCERTAINTY+guide pairs are reflexive construction on a researcher
event; the path cannot escalate from "reify uncertainty" to "attempt trial
construction."

The substrate can build (alloc_node, link_edge reachable; 4-op ISA
execute() approved machinery) and can use what was built (promoted MAPs
serve later queries). What it cannot do is decide, from its own state,
to build.

Verification caveats (non-claim, recorded by MECH-VERIFY): the SHA-256
string printed in LEARNER_MECH_ANALYSIS.md is 79 characters and a
transcription error (correct: a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd);
the git blob hash is correct and pins the exact bytes analyzed, so no
claim is affected. Two line-number citations are off by one (ev_query is
813-835; the miss-policy comment is at 826).

## 5. What this means for the constitution's learner-authority metric

The constitution scores the desired trajectory as LEARNER AUTHORITY up
while HUMAN HAND-HOLDING down. On this discrimination, learner authority
over integration is effectively zero: the learner records facts
(ev_teach), reifies uncertainty (miss_inquire), and selects guides
(ev_act), but cannot initiate the one construction act that integrates new
experience. Human hand-holding is maximal on the integration path: the
researcher fires the query event, sets flags and expected, and the
machinery does the work. The 6/6 -> 0/6 drop when exactly that machinery
is removed is the measurement of the hand-holding share.

What would close the gap, in the constitution's terms: a run in which the
event-triggered machinery is disabled and the learner nevertheless
integrates, with white-box evidence that a learner-created structure
initiated the construction (the analog of how promote_graph leaves
construction-provenance DEP edges). The bar to pass would be CO-1 (6/6
store, 12/12 reuse, 12/12 delayed) via a construction path reachable from
learner state, not via the event path. Until such a run exists, any
integration result on TNN-2 remains MACHINERY-DEPENDENT in the strong sense:
the learner does not decide or author the integration.

Per the no-patch-treadmill rule, this result is followed by governance and
root-cause work, not by new handlers, modes, bridges, or opcodes.

## 6. The precise open question for TNN-3

What general substrate property would enable learner-initiated
construction, such that:

1. Initiation-from-state: a construction service is reachable from
   learner-created state, on the learner's schedule rather than on the
   arrival of a researcher event;
2. Control-from-state: gating and parameterization of construction are
   readable from learner-created state, not only from event arguments;
3. Trigger-from-state: the decision of when to attempt integration versus
   merely reify uncertainty is expressible in learner state and honored by
   the control plane;
4. White-box visibility of the initiation act: the structure that caused
   construction to start is inspectable in persistent learner state.

This is a question about the control plane, not a patch proposal. The
answer must live on the constitution's trajectory: LEARNER AUTHORITY up,
HUMAN HAND-HOLDING down, ARCHITECTURAL COMPRESSION, one continuing
learner, no new modes/bridges/routers. Per the governance standing rule,
proposing it is TNN-3 governance; this lane authorizes no design.

## 7. The debate question

Two readings are on the table:

- (A) MACHINERY-DEPENDENT overturns CONTLEARN's BUILD-PASS: the
  LEARNOWN-DEMONSTRATED label, having been measured to require researcher
  machinery for integration, no longer names any learner-owned capability,
  and the verdict should be retired or renamed to avoid implying it.
- (B) BUILD-PASS stands within the machinery-enabled scope: the frozen
  bars (store 13/13 unsupervised, reuse 20/20 masked, ablation, nostore
  control, determinism) measured exactly what the prereg froze, and the
  machinery-disabled lanes bound the interpretation rather than falsifying
  the measurements.

The evidence supports that the measurements in CONTLEARN are true of the
machinery-enabled core, and the discrimination in CONTLEARN-OWNED/OWNED2
falsifies only the strong reading, which CONTLEARN never claimed. The
debate is therefore about naming and citation discipline going forward:
whether LEARNOWN-DEMONSTRATED may still be cited as evidence of any
learner-owned property (position: it evidences learner-owned
responsiveness and storage within the frozen interface, i.e. the weak
H10 sense) or whether continued citation is a category error that will
be misread as learner-authored integration. Recommended citation form if
the label survives: "LEARNOWN-DEMONSTRATED (machinery-enabled scope;
strong sense measured absent, CONTLEARN-OWNED/OWNED2)."

## 8. Non-claims carried forward

No statement about learner agency in the causal sense (H2-v2/H3 stand);
no procedure execution at query time (reuse is exact-hit retrieval of
machinery-taught facts via activate, Attack 6); no L3 and no generality;
the machinery-disabled variants are measurement instruments, not proposed
architectures; all batteries were disclosed in prereg with fresh
ids/relations, not sealed adversarial worlds.

## 9. Recommended follow-ups for the coordinator

- Bind the supersession into the record: wherever LEARNOWN-DEMONSTRATED is
  cited (DEBATE briefs, TNN-3 governance docs, the H10 standing question),
  append the bounded form "machinery-enabled scope; strong sense measured
  absent".
- Correct the SHA-256 typo in LEARNER_MECH_ANALYSIS.md section 1 (the
  79-character string; correct value in MECH-VERIFY report) so the
  document is citeable.
- The TNN-3 open question in section 6 is the one genuine new work item;
  it belongs to substrate design governance, not to another measurement
  lane. No further machinery-disabled replications are needed: the fact
  is doubly confirmed.
