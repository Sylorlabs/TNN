# JUDGE_BRIEF: LEARNER-MECH root-cause analysis

RENDER_SHA: be5c65a39
FIRST_RENDERED_WAVE: wave-20261001-2321pdt
COMPONENT_LINEAGE: CONTLEARN-OWNED MACHINERY-DEPENDENT (VERDICT_OWNED.md,
JUDGE_BRIEF.md)
NEW_KNOWLEDGE_CLAIM: In the frozen TNN-2 core no learner-created state
can initiate trial/promotion construction (the machinery is reachable
only from the researcher-invoked event interface, with control parameters
fed by event arguments), so learner-owned integration currently has no
control path to run on, not merely an unproven mechanism.

## Verdict

Root cause identified (analysis only; no verdict change, no design
proposed). The mechanism gap is gap (a) with reinforcing sub-gap (c):
(a) no learner-state structure can trigger construction initiation; (c)
the construction machinery's control parameters (masked/dc/di from
`flags`, the accept oracle `expected`) arrive via the event arguments and
bypass learner state entirely. The primitive construction operations
(`alloc_node`/`link_edge`, the 4-op `execute()` ISA) and the usability of
constructed products by standing mechanisms are present; initiation and
control from learner state are absent.

## The control-plane line

Four event entry points (`ev_teach`, `ev_query`, `ev_observe`, `ev_act`),
all researcher-invoked; every construction is initiated inside one of
them. `ev_query` on miss runs a hardcoded sequence: `activate` (reads
state, constructs nothing) -> `mp_run` -> `bootstrap_miss` ->
`miss_inquire`. Verified call-site inventory: `mp_run` one call site
(ev_query:827); `t2_trial` one (mp_run:670); `t2_try_verify` four
(t2_trial only); `promote_graph` four (t2_trial only); `bootstrap_miss`
one (ev_query:830). `mp_set`/`mp_get` are called only in test functions,
never in the cognition path; the "learner-set miss policy" comment at
line 828 does not describe the control flow. The learner's observed
TREAT response (UNCERTAINTY/guide accumulation, 6/12/18 across phases) is
construction, but reflexive on a researcher query event, with no
learner-state branch that can escalate to trial construction.

## Substrate properties needed (not a design)

1. Initiation-from-state: a learner-created structure must be able to
   cause the construction service to run, on the learner's schedule.
2. Control-from-state: gating and parameterization of construction must
   be readable from learner state, not only event arguments.
3. Trigger-from-state: the integrate-vs-reify-uncertainty decision must be
   expressible in learner state and honored by the control plane.
4. White-box initiation evidence: the structure that caused construction
   must be visible in persistent learner state.

Properties 1-3 are absent in the frozen core; property 4 already holds
(construction-provenance DEP edges). No mode, bridge, handler, or opcode
is proposed; initiation semantics are TNN-3 governance.

## Constitution scoring

Learner authority over integration is effectively zero on this
discrimination; human hand-holding is maximal (researcher fires the
query, sets flags/expected, machinery does the work; removing exactly
that machinery drops integration 6/6 to 0/6). The gap closes when a run
with event-triggered machinery disabled passes CO-1 (6/6 store, 12/12
reuse, 12/12 delayed) via a construction path reachable from learner
state, with white-box initiation evidence.

## What this does not claim

No learner agency in the causal sense (H2-v2/H3 stand); no procedure
execution at query time (Attack 6 carried forward: CONTROL reuse is
exact-hit retrieval of machinery-taught facts); no L3; no generality;
the battery was disclosed-in-prereg, not a sealed adversarial world.

## Evidence paths

- `docs/lab/rsi/runs/wave-20261001-2321pdt/LEARNER-MECH/LEARNER_MECH_ANALYSIS.md`
  (full root-cause analysis)
- `docs/lab/rsi/runs/wave-20261001-2321pdt/LEARNER-MECH/NAMECHECK.md`
  (Step 0 toolchain verification)
- Frozen core: `docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag`
  (commit f4de7ff46; blob `b226b223cb3ee0be742af673653fb8ea8605f281`
  re-verified this lane; SHA-256
  `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`)
- Consumed inputs (read-only):
  `docs/lab/rsi/runs/wave-20261001-2321pdt/CONTLEARN-OWNED/VERDICT_OWNED.md`,
  `.../JUDGE_BRIEF.md`, `.../PREREG_OWNED.md`
