# VERDICT_CLH2: longer-horizon delayed REBIND under sustained interference

Wave: wave-20261002-0521pdt. Lane: CONTLEARN (CLH2, backlog item 29).
Date: 2026-10-02.
Frozen prereg: PREREG_CLH.md (commit aa47999f7, alone). Implementation
commit ef9b80200; K0 merge-base ancestry verified before verdict.

## Per-bar results

All bars PASS. Evidence in SEALED_EVAL.md; adversarial review in
REDTEAM_SELF.md.

- CP-R0 (proposal-before-machinery, TREAT): 24/24 PROPOSAL before
  MACHINERY, 0 MACHINERY_SKIPPED, 12/12 rebind pairs ordered with
  matching prop node ids.
- CP-R1 (rebind success, TREAT): REBIND_OK 12/12. New subjects and new
  relations (97001+i/863 -> 96201+i; 97101+i/866 -> 96101+i), answers
  served by new MAPs with alive DEP edges to the never-re-taught
  phase-A chain facts and to the anchor facts. REBIND_PROP_CITE 12/12
  (TREAT), 0/12 (CONTROL, no proposals exist).
- CP-R2 (structure survival, TREAT): SURVIVE_OK 6/6; SURVIVE_ANSFACT 6/6.
- CP-R3 (retention, TREAT): RETAIN_OK 6/6.
- CP-R4 (interference integrity, TREAT): PRESSURE_OK 96/96; INT2_OK 1/1;
  STORE3_OK 6/6.
- CP-R5 (structure dependence, NOPHASE): NOPHASE_OK 12/12 (all rebind
  answers == 1, the frozen count-branch prediction); NOPHASE_NOA 1/1;
  integrity 6/6, 96/96, 1/1.
- CP-R6 (determinism): 3/3 byte-identical per binary
  (2f03c4af... / d53258f7... / 9e6b8681...); FNV equal; rc=0; 0 stderr.
- CP-R7 (control reproduces): REBIND_OK_C 12/12, SURVIVE_OK_C 6/6,
  RETAIN_OK_C 6/6, zero PROPOSAL lines. No anomaly.
- K0: prereg and NAMECHECK strict ancestors of impl. K1: 9 processes,
  3 pre-run builds logged (0 during runs), AUDIT_PASS 166/142, kinds
  {1,2,3}, empty argv/env. K2: frozen hashes hold; drivers 0/0/0/0
  (cognition fns / structural writes / switch-match / new
  tags-edges-opcodes-modes-bridges-handlers-formats); cores byte copies;
  pure Zag. K3: lo_driver 3x == 1ff527fa....

## Verdict

**REBIND-DEMONSTRATED. BUILD-PASS.**

On the fixed disclosed 166-event battery, the continuing learner
integrates 6/6 novel 2-hop chains, then after 118 unrelated interference
events (96 memory-pressure facts, one unrelated conflict-plus-
correction episode, a second 2-hop chain family with 6/6 novel
integrations) rebinds the phase-A structure for 12/12 new problems: new
subjects, new relations, new entry points into the old chains, correct
answers served by new MAPs DEP-citing the never-re-taught phase-A
facts, while the 6/6 phase-A MAPs stay live with intact citations and
6/6 retention probes hold. The 12/12 rebind answers are
structure-caused: the no-phase-A control on the identical machinery and
identical problems returns 1, not the chain answers. All 3/3
byte-identical, one process per run, no reset, no task label, no
recompilation.

## Claim bound (binding; CONTLEARN3 caveats carried over)

The following caveats from CONTLEARN3 still bind, explicitly:

1. Proposal CONTENT (mech=TRY_CHAIN) is a fixed researcher template.
   No claim of learner authorship of proposal content.
2. Proposal initiation is still event-triggered, not learner-scheduled.
3. No learner agency in the causal sense.
4. The gate's refusal branch is structurally enforced but empirically
   unexercised (0 MACHINERY_SKIPPED, third consecutive lane).
5. No L3, no generality. The battery is disclosed and prereg-frozen,
   not sealed adversarial.
6. Citation form stays machinery-enabled per the debate Q7 binding form.

New notes from this lane's red team:

- The rebind capability is frozen-core behavior: CONTROL reproduces
  TREAT on every rebind bar (CP-R7, no anomaly). The proposal gate
  contributes ordering provenance (CP-R0), not the rebind itself.
- Head-family value selection is allocation-order-determined among two
  valid compositions ([U,S,A] tried before [U,S,B] by node-id order);
  the DEP-citation oracle pins which composition was used (6/6). The
  tail family (unique path) carries the stronger rebind evidence.
- The rebind problems are new in surface but same in structural kind
  (2-hop chains); no cross-kind transfer tested or claimed.

## Build status

**BUILD-PASS.**

## Keep / discard

KEEP the NOPHASE discriminator protocol: it is the reusable instrument
for structure-dependence claims (same machinery, same problems,
structure absent -> different answers). KEEP the rebind battery shape
(capability -> volumetric pressure -> unrelated conflict -> second
family -> new-entry-point rebind) as the lane's standard longer-horizon
template. DISCARD nothing: no mechanism was proposed, none killed; the
single-propagation revision finding from CONTLEARN-LH stands
unmodified.

## Queued next (for the coordinator)

1. Adversarial exercise of the gate's refusal branch (open since
   CONTLEARN3; 0 MACHINERY_SKIPPED in three lanes).
2. Learner-scheduled proposal initiation (LEARNER-MECH axis (a)).
3. Correction-propagation hypothesis from CONTLEARN-LH (does a second
   downstream revision fire on correction of a contradicted node?).
4. Cross-kind rebind: new problems of a different structural kind than
   the capability session (not just 2-hop chains), the next rebind
   frontier.
