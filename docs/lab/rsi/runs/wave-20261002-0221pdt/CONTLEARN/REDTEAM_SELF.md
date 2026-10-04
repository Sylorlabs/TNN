# REDTEAM_SELF: CONTLEARN3 mechanism-proposal-first (self-attack)

Wave: wave-20261002-0221pdt. Lane: CONTLEARN. The prereg (section 1)
requires the red team to attack exactly the points below. This review is
written by the implementing worker against its own instrument; nothing
here is softened.

## Attack 1: is the "proposal" just a supervised template?

Yes, in content. The mech=1 (TRY_CHAIN) code is a fixed researcher
template: pf_propose writes it unconditionally on the miss path, and no
learner process chose, computed, or could have altered it. In the strong
authorship sense (the learner decides or authors the integration), the
proposal is researcher-constructed content placed into learner state.
The experiment does not claim otherwise; the claim bound in the prereg
names this explicitly. What the experiment does measure is the control-
plane property: the machinery cannot engage without consulting that
learner-state structure first, and the promoted MAP cites it. That is a
gating/ordering property, not authorship. Anyone citing this lane for
learner-authored proposals would be misreading it.

## Attack 2: does per-query supervision sneak back in?

The masked queries carry expected=-2, flags=1 (the disclosed supervisor
disconnect used by every prior lane). The E-ruling holds: expected is
post-hoc feedback only; the accept oracle is the first-clean-candidate
rule, unchanged. No new supervision channel was added. However, the
honest qualification: the proposal is written on the query-miss path, so
the measured ordering is really "query-miss, then proposal, then
machinery". The researcher still fires the query event. A genuinely
learner-scheduled proposal (initiation from learner state on the
learner's own schedule, LEARNER-MECH axis (a)) is NOT tested here and is
not claimed.

## Attack 3: is the gate ever actually exercised?

The MACHINERY_SKIPPED branch fired 0 times in the battery: ev_query
always proposes before engaging, so the refusal path is untested at
runtime. The gate's reality rests on (a) the code path (the only trial
entry in TREAT is pf_mp_run, which checks pf_find first), (b) the
provenance DEP edges (6/6 MAPs cite their proposals), and (c) the trace
ordering (6/6 PROPOSAL before MACHINERY). A stronger adversarial test
would delete a proposal mid-run and attempt engagement; that test is not
in this prereg and is not claimed. The gate is structurally enforced but
its refusal behavior is unverified empirically.

## Attack 4: does the proposal channel add capability or just ceremony?

CONTROL integrates the identical 6 chains with zero proposals and the
same reuse/retention numbers. The gate adds ordering and provenance, not
capability. This is consistent with the honest scope: the lane measures
whether proposal-first ordering can be enforced while preserving
integration, not whether it improves it.

## Attack 5: one-system rule and no-patch-treadmill

The instrument adds no new modes, bridges, handlers, tags, edge types,
opcodes, or state formats; the proposal is a tag-1 node in POLICY_ROOT
space, the same format as learner guides. The lane adds one new function
family to a lane-dir instrument, not to the frozen architecture. Per the
no-patch-treadmill rule, no fresh-world failure occurred, so no repair
lineage was opened.

## Attack 6: battery freshness and scope

All ids and relations are fresh to the wave-20261001/20261002 .zag
sources (verified by grep before freezing). The 2-hop chain pattern is
the same family as prior batteries (disclosed, not adversarial); the
conflict, correction, and delayed-reuse episodes are the new structural
elements. No sealed adversarial worlds; the script is disclosed.

## Residual risks acknowledged

- Proposal content authorship: researcher-templated (Attack 1).
- Proposal initiation: event-triggered, not learner-scheduled (Attack 2).
- Gate refusal: structurally present, empirically unexercised (Attack 3).
- No generality, no L3, no learner agency claim; citation form stays
  machinery-enabled per the debate Q7 binding form.

None of the above invalidates the frozen bars; all are inside the claim
bound. The verdict stands or falls on CP-1..CP-6 and K0..K3 as frozen.
