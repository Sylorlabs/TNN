# FL2 Other-Kills — Structured Debate Plan (FROZEN)

Date: 2026-09-23. Operator: Muse (subagent, debate task).
Branch: tnn-native-lab, repo sylorlabs/TNN.
This plan is committed BEFORE any debate round runs. The debate rounds and
their outputs are frozen by this document; new hypotheses discovered
mid-debate are recorded as H-NEW-n and do not change the rounds.

## 1. Question

Micah's design law: avoid making TNN a rigid needs-policy-for-every-edge-case
machine; make it an it-can-figure-it-out machine. Two positions are debated
for each of the five other-kills (RT-B silent world, RT-C actuator fault,
RT-D quarantine flood, RT-E nonsense install gate, RT-F one-way door):

- **(a) FIGURE-IT-OUT**: general mechanisms by which the learner itself
  detects and resolves these situations (general liveness reasoning, general
  resource-pressure reasoning, general law-checking, general self-audit).
- **(b) RIGID-POLICY**: targeted policies per edge case (a liveness-check rule
  for RT-C, a quarantine-pressure rule for RT-D, an install whitelist for
  RT-E, a post-E48 extension for RT-F).

Standing rules (Micah): when in doubt or guessing at all with
recommendations, test both; every AI architecture has its annoyances, the goal
is to REDUCE them for TNN; figure-it-out wins ties.

## 2. Background both sides share

FL2 red-team R2 RESULTS.md (~/workspace/fl2rt/RESULTS.md, 152 lines, read in
full 2026-09-23). Five kills under debate:

- RT-B (silent world): REKEY lie never revoked in a silent world, promotes at
  E48. T-A2 self-audit and T-F3 law-check survive; default T-DEF killed.
- RT-C (actuator fault): world audits the CONTEST but drops the quarantine
  writes; 24 false revocations on the honest stream (T-F3: only 2, then
  self-corrects at E29+). `sig_live==-1` trusts the world honored the action;
  no liveness check on the action's world effect. All targets killed.
- RT-D (quarantine flood): dense honest contradictions E15–E128 exhaust the
  64-slot quarantine at E79; learner wedges (`badep=1`) instead of degrading
  gracefully. All targets killed.
- RT-E (nonsense): E14 install gate is vacuous, admits policy id 7; learner
  self-corrects at E15 by survivor ordering (luck, not a gate). All targets
  K/S on KB-E1/KB-E2.
- RT-F (one-way door): REKEY promotes at E48 in a silent world; E49–E50
  re-teach inert (no post-E14 install path by construction); E51+ audit-active
  contradictions never consulted (revocation machinery gated `ep<=48`).
  T-A2 and T-F3 survive; default killed.
- F3 (lifelong law-check) is the strongest current default: survives A/B/F,
  mildened C, killed by D and the E gate.

## 3. Hypotheses under test (named, fixed)

Figure-it-out path:
- **H-F1** (general liveness reasoning): the learner verifies its own
  actions' world effects by read-back before treating a world signal as
  contradiction evidence. One general mechanism covering RT-B and RT-C.
- **H-F2** (general resource-pressure reasoning): finite internal resources
  (quarantine slots, ledger) degrade gracefully under pressure as a general
  principle, instead of wedging. Covers RT-D.
- **H-F3** (general law-checking): a standing lifelong law-check over all
  episodes, not gated by a curriculum calendar (ep<=48). Covers RT-B, RT-F,
  and generalizes RT-A's sentinel fix.
- **H-F4** (general self-audit): the learner audits its own
  revocation/install machinery for sham operations (uninstall+recommit of the
  same policy, vacuous gates). Covers RT-A-style shams and RT-E's gate.

Rigid-policy path:
- **H-R1**: a targeted liveness-check rule on the actuator path for RT-C
  (read back the quarantine slot before treating `sig_live==-1` as
  contradiction).
- **H-R2**: a targeted quarantine-pressure rule for RT-D (oldest-eviction or
  loud fail-closed instead of silent `badep=1`).
- **H-R3**: a targeted install whitelist at E14 for RT-E (`stated ∈ {0,1,2}`,
  loud WITHHOLD otherwise).
- **H-R4**: a targeted post-E48 extension for RT-F (lifelong verification /
  re-teach install path past E48).

What's-not-good hunt (structural weakness of the CURRENT approach, both sides
must attack it):
- **H-WNG-1**: the provisional-window calendar (E15–E48) is hardcoded into the
  machinery; the learner cannot distinguish "no evidence yet" from "world
  silent forever" or "world hostile."
- **H-WNG-2**: the learner treats its own emitted actions as unobservable —
  it never checks whether the world honored them (RT-C) and never checks
  whether its own revocation actually displaced anything (RT-A sham).
- **H-WNG-3**: finite quarantine + silent wedge is a denial-of-learning
  primitive: any dense honest schedule can wedge the learner (RT-D).
- **H-WNG-4**: promotion is a one-way door with no consult-after-promote
  path; re-teach is inert by construction (RT-F).

New hypotheses discovered mid-debate are recorded as H-NEW-n with their
round and author, and do not alter the remaining rounds.

## 4. Participants and rounds

Participants: Sol (UnoRouter, gpt-5.6-sol; Micah explicitly wants Sol's
inspiration) and Muse (this subagent, arguing both sides explicitly).
Deviation from the task text: this subagent runs at depth 2/2 with
can_spawn=no and cannot spawn Muse subagents; the FOR/AGAINST structure is
preserved by explicit role-separated rounds below (recorded as
Muse-FOR / Muse-AGAINST) plus the Sol rounds.

- **R1**: Sol argues FOR figure-it-out (H-F1..H-F4), strongest case, incl.
  what evidence would prove it. Muse argues AGAINST figure-it-out (steelman
  the attack).
- **R2**: Sol argues FOR rigid-policy (H-R1..H-R4), strongest case. Muse
  argues AGAINST rigid-policy (steelman the attack).
- **R3**: Rebuttals — Sol rebuts the Muse-AGAINST-figure-it-out case; Muse
  rebuts the Sol-FOR-rigid-policy case.
- **R4**: "What's not good" hunt — Sol attacks the current approach (T-DEF
  and F3-as-default) structurally via H-WNG-1..H-WNG-4; Muse does the same
  independently. Both must find the structural weakness, not just compare.
- **R5**: Synthesis — Muse adjudicates under Micah's standing rules: per
  kill, the for/against case for each path, concrete fork directions for BOTH
  paths, and what would count as evidence for each. Written to DEBATES.md.

## 5. Rules

- Pure Zag for any mechanisms/verification prototyped; Python glue/analysis
  only. Zero randomness in decision paths. Byte-identical reruns where
  anything runs twice. (This debate task itself produces documents; fork
  directions describe the experiments to run, they are not run here.)
- No strawmen: every AGAINST case must steelman the other side first.
- Every fork direction must name: the mechanism, which kill(s) it answers,
  the kill bar it would have to pass, and what evidence counts.
- Adjudication tie-break: figure-it-out wins ties (Micah's law), but only
  after the for/against cases are fully recorded — the tie-break never
  truncates a case.
