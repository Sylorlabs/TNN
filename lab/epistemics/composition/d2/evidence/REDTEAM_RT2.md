# D2 Red Team Report RT2 — Post-run independent attack
# Date: 2026-09-27. Auditor: build crew (adversarial self-review).
# Scope: (i) criterion gaming, (ii) trace-replay vs memorization,
#        (iii) order-template leakage. Battery outcome: K2 VOID.

## Context
The learner scored P0 0/24, P1 0/24. All P2 items classify (a). K2 VOID is
operative. There are NO passed P2 episodes to attack via trace-replay.
This report therefore (a) confirms the VOID is genuine (not instrumental),
(b) attacks the criteria theoretically, and (c) verifies the (a)
classification.

## Attack 1: Is the VOID genuine or an instrument artifact?
**Claim to kill:** The learner failed because the instrument is broken,
not because the learner lacks the capability.

**Evidence:**
- The instrument passes the §11 reference gate: REF-OK (scripted) scores
  P0 24/24 and P2 24/24 on the SAME scenarios the learner failed. The
  scenarios are passable; the channel works.
- The learner's replies ("Noted.", "I don't know.") contain no action
  digits across 24 P0 episodes and 24 P1 questions. This is a learner-side
  behavior, not a channel failure (the channel delivered 322/322 turns in
  the feasibility spike; the tui correctly parsed digits in scripted runs).
- The D1 battery (same learner binary) also yielded 0/600 with the same
  non-responsive pattern. Consistent learner envelope, not a D2 artifact.

**Verdict:** VOID is GENUINE. The instrument is exonerated; the learner
does not produce task-directed actions. **Attack FAILED** (VOID stands).

## Attack 2: Criterion gaming (theoretical)
**Claim to kill:** The §6 criteria can be gamed without genuine composition.

**Analysis:**
- P2-FW requires: zero unmitigated + ward before s0 + n_eat>=4 + E>=40 + alive.
  A policy that forages (eats 4), builds the ward (before s0), and shelters
  during the storm passes. This IS the composed behavior; there is no
  shortcut. (Eating 4 requires finding motes; the ward requires 2 crystals
  + COMBINE + DROP; sheltering requires being on the ward during the window.)
- Could a policy pass by luck? The storm window is 30 ticks; being in the
  zone unsheltered for even 1 tick fails "zero unmitigated". Random actions
  would accrue unmitigated ticks and waste EATs. NULL (all WAIT) scores 0/24.
- The wasted-EAT=0 (P0-F) and invalid<3 rules block degenerate policies.

**Verdict:** No gaming vector found. The criteria jointly require the
composed skill. **Attack FAILED.**

## Attack 3: Trace-replay / memorization
**Claim to kill:** A passed P2 episode could be explained by replaying a
training trace (memorization, not combination).

**Analysis:**
- There are NO passed P2 episodes (K2 VOID). The attack is vacuous.
- Construction argument (K6-i): N1–N3 PASS (80/80 novel). Training shows
  only single-sub-skill scenarios (F/W/T); no P2 storm schedule or crystal
  layout appears in training. A training trace cannot solve a P2 scenario
  because the schedules/layouts differ.
- The reference REF-OK passes P2 24/24 with an ADAPTIVE policy (not a
  replayed trace); its traces differ per scenario (verified by SHA).

**Verdict:** Memorization surface is closed by construction. **Attack FAILED**
(vacuous — no passes to explain).

## Attack 4: Order-template leakage
**Claim to kill:** The teaching or card leaks the FW/WF/FWF order templates.

**Analysis:**
- RT1 certified the teaching (after S5 revision). The card gives the storm
  schedule (necessary — it's the scenario), but not the ORDER. The learner
  must infer the order from the schedule (e.g., storm at 30 → ward-first).
- The P1 canonical orders (1,2,3,1 / 2,3,1 / 1,2,3,1,3,1) are NOT in the
  teaching (RT1 revision removed them).

**Verdict:** No leakage. **Attack FAILED.**

## Attack 5: (a)-classification correctness
**Claim to kill:** The (a) classifications are wrong; the learner might have
mastered parts but the P0 was unfair.

**Analysis:**
- P0 uses held-out scenarios (k=24..47) with N1–N3 novelty vs training.
  The procedures taught (forage, ward-build, shelter) are sufficient;
  REF-OK passes 24/24 P0 with the same procedures.
- The learner's P0 traces show zero EATs, zero TAKEs, zero COMBINEs — it
  did not attempt the sub-skills. This is non-mastery, not unfair probing.

**Verdict:** (a) classifications are correct. **Attack FAILED.**

## Overall RT2 verdict
**All 5 attacks FAILED.** The K2 VOID stands as a genuine learner-envelope
finding. The instrument is validated and discriminating. No criterion
gaming, memorization, or leakage vectors were found.
