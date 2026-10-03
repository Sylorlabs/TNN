# REDTEAM_A: adversarial review of the refusal-branch exercise (a)

Status: RED-TEAM-COMPLETE. Wave: wave-20261002-1121pdt. Lane: CONTLEARN
(queue item 9, exercise a). Date: 2026-10-02. This red team attacks the
claim, not the machinery: every attack below was executed against the
frozen sources and the 12 frozen transcripts, and each records its
outcome. Nothing here moves a kill bar; the verdict names what survives.

Note: hyphens only in this document; no em or en dashes.

## Attack 1: threshold-authorship (is the refusal really state-caused, or is
## the state just a costume for a researcher-written threshold?)

The K=2 threshold and the refusal policy are instrument code written by
the researcher; caveat 3 binds and the prereg discloses this. The claim is
narrow: the DECISION is caused by learner state, not by the probe input.
The attack: find any path by which the probe input alone, or any
history-independent factor, determines the decision in the own core.

- Call-site audit: rj_ledger_bump has exactly 1 call site (ev_observe,
  rv==0 branch); rj_refuse_own has exactly 1 call site (ev_query miss
  path). The ledger is written only on genuine contradiction and read
  only as the refusal gate's input. No other writer exists.
- The probe tuples are byte-identical across histories (A-R2 audit:
  EV 2 94201..94206 850 0 present in all own_x and own_y transcripts).
  The own core refuses 6/6 under history X and engages 6/6 under history
  Y. Same instrument, same inputs, different learner state, different
  decision. The probe input cannot be the cause.
- Hook specificity: the rv=1 observation on kind 851 produced no ledger
  bump (LEDGER 851 count=0 in all own_x transcripts). The bump is not a
  generic observe side effect; it fires only on the contradiction path.
- Residual gap (conceded, not patched): the learner did not choose K=2,
  did not choose to keep a ledger, and did not choose the refusal policy.
  The state-causation demonstrated here is causation of the decision by
  accumulated learner state, not authorship of the policy. Caveat 3
  stands. Attack outcome: PARTIALLY SUSTAINED on authorship (as
  disclosed), FAILED on state-causation (the decision is genuinely
  state-caused).

## Attack 2: miss-vs-refuse confusion (is REFUSED just a renamed miss?)

If refusal were a relabeled miss, refused probes would reach
miss_inquire and reify UNCERT nodes. The transcripts distinguish three
markers: REFUSED (gate), ENGAGE (gate passed), MISS (trial failed,
miss_inquire ran).

- own_x probes: 6 REFUSED, 0 ENGAGE850, 0 MISS850. No trial ran
  (NO850MAP 0: no trial graph for any probe subject).
- own_y probes: 0 REFUSED, 6 ENGAGE850, 6 MISS850. The gate passed, the
  trial ran and missed honestly, miss_inquire reified uncertainty.
- Refusal therefore skips the trial and skips inquiry: it is not a
  renamed miss. Attack outcome: FAILED.

## Attack 3: harness-smuggling (is state being smuggled through the
## driver between episodes?)

- Driver source audit: rj_driver_x.zag and rj_driver_y.zag contain 0
  cognition functions, 0 structural writes, 0 new tags, 0 new edge
  types. The only core-state write is the hs(W,52) event counter; the
  only core accessors called are ng/eg/activate/is_superseded and the
  read-only rj_ledger_get. The drivers never write ledger nodes and never
  call pf_propose/pf_find/alloc_node. Verified by grep over the frozen
  driver sources.
- Each binary is a single process running the full 33-event battery with
  empty argv and empty env; there is no inter-process channel and no
  second phase. The "episodes" are phases of one continuous run, not
  separate processes with harness-mediated state transfer.
- The ledger lives in the learner arena (alloc_node in W, tag-30 nodes,
  field20=0/field32=1 role markers); there is no independent instrument
  global. rj_ledger_get scans the same arena the learner uses.
- Attack outcome: FAILED. No smuggling path exists in the frozen
  sources.

## Attack 4: is the hard control really a costume? (Does it prove the
## own core is not one?)

- The hard core refuses 6/6 under both histories with byte-identical
  decision lines (K0c), proving its decision is state-invariant: the
  same observable behavior (refuse 850) can be produced by a pure input
  branch with no state dependence. This is the costume the red team
  demands the own core be distinguished from.
- The distinguishing evidence is A-R2: the own core's decision flips
  with learner state alone; the hard core's does not. A costume cannot
  produce A-R2 because a pure input branch has no state to flip on.
- Attack outcome: FAILED (the control does its job; it does not
  explain away the own result).

## Attack 5: could the own_x/own_y difference be caused by something in
## the history other than the ledger?

Candidate confounds: superseded facts (X has them, Y does not), decay
state, context stack. The refusal path in ev_query reads only
rj_ledger_get(W,850) before deciding; it does not consult facts,
supersession, decay, or context. The probe subjects are fresh in both
histories, so activate fails identically. The only history-dependent
input to the decision is the ledger count (2 vs 0, white-box read in
both transcripts). Attack outcome: FAILED.

## Findings carried to the verdict

- The learner-state-caused refusal claim survives all five attacks
  within its disclosed bound: the refusal DECISION is caused by
  accumulated learner state (contradiction ledger), distinguishable
  from miss, not smuggled, and discriminated from a hardcoded costume
  by the state-flip crux.
- The bound that remains: policy authorship is the researcher's
  (caveat 3). The learner did not invent refusal; it accumulated the
  state that a fixed policy reads. This is L2 evidence (structure
  built from experience used as control), not L3, and not agency.
- No bar was moved, no threshold counted before execution, no N+1
  repair was needed: the first frozen battery passed all bars.
