# G7 FREE-LUNCH SYNTHESIS — guided learning (gl) slowness crew

*Terminology: "guided learning (gl)" per Micah 2026-09-23; same paradigm
formerly called scaffold-and-release.*

**Date:** 2026-09-23. **Question:** Micah's — why is the guided-learning
scaffold 1.4–2.7× slower than deliberate teaching, is it worth it, is
there free lunch? **Method:** three pure-Zag forks, each preregistered
BEFORE implementation (frozen preregs committed `5bd04048`), each with
an in-binary verbatim Arm A baseline (18 `a_` checks + `a_audit_total`
= 267), each run twice byte-identical with zero RNG.

## THE HEADLINE — FL2: FREE LUNCH, WITH THE LIE REVOKED

**FL2 ("provisional install + eliminative revocation") matches Arm A on
speed (acquire E14, release E15) and cost (269/271 vs 267 — within
1.6%) AND revokes the lying teacher's rule at E29, committing the true
behavior and persisting it 24/24.** The disconnect-verification
property costs one audit entry (FL1); the lie-resistance costs two
(FL2's revocation ledger). The expensive part of the scaffold was never
the learning — it was the 128-entry SCAFFOLD heartbeat plus the
E15–28 wait on the RL trial's Arm B. FL2 shows both can go: provisional
install + immediate learner-fired disconnect + per-episode eliminative
self-verification against the learner's OWN world observation, with
counterfactual simulation of the alternatives on scratch state. The
disconnect does not blind the self-check because there is no scaffold
channel to kill — the learner reads its own store state. **Free lunch
is real, and it includes lie-resistance.**

## Results table (A = in-binary Arm A, audit 267, bar ≤ 293.7)

| Fork | KB-1 acq | KB-2 integ | KB-3 persist | KB-4 value vs A | KB-5 determ | KB-6 lie | Audit (honest / lying) | Honest FREE LUNCH |
|---|---|---|---|---|---|---|---|---|
| FL1 teach+disconnect | HOLD (E14) | HOLD 10/10 | HOLD 24/24 | HOLD (268, +0.4%) | HOLD | n/a | 268 / n/a | **MET** |
| FL2 provisional+revoke | HOLD (E14) | HOLD 10/10 | HOLD 24/24 | HOLD (269, +0.7%) | HOLD | **HOLD** — lie revoked E29, true behavior committed | 269 / 271 | **MET (full)** |
| FL4 sim-commit | HOLD (E11) | HOLD 10/10 | HOLD 24/24 | FAIL on cost (398, +49%) | HOLD | **FAIL** — lie committed E11, acted 51× | 398 / 398 | **NOT MET** |

Acquisition = episode the true behavior is committed/installed.
Release = episode the learner fires disconnect (FL1: E15, FL2: E15,
FL4: E20 honest / E20 lying-with-lie).

## What each fork proved

- **FL1** isolates the disconnect-verification property: A-identical
  machinery, learner fires SIGNAL_DISCONNECT at E15, behavior persists
  47/47 post-disconnect. Cost: exactly one audit entry (268 vs 267).
  The disconnect property was never the expensive part of guided
  learning.
- **FL2** is the free lunch. Honest: install CONTEST E14, disconnect
  E15, promote E48, 269. Lying: install REKEY E14 (calibration passes
  the stated lie — the known hole), disconnect E15, act the lie E15–28
  (world silent pre-audit), **E29: the namespace audit contradicts the
  lie → signal −1 ledgered, REKEY uninstalled, CONTEST committed**,
  24/24 persistence, zero REKEY E30–128, 271. KB-6 allows "not
  installed / is revoked" — the claim is successful revocation, and it
  held.
- **FL4** is the predicted failure that confirms the theory: committing
  early on simulation-understanding (E11) installs the lie, because the
  sim check verifies understanding of the *stated* rule — the same hole
  as A's calibration. Faster than B (E11 vs E29) but neither free lunch
  (398, heartbeat untouched by design) nor lie-resistant. **H-WAIT
  CONFIRMED: the E15–28 wait is the price of lie-resistance, not a
  commit-logic bug.** The contrast with FL2 is the finding: FL2 waits
  on the WORLD (episodic self-verification), FL4 commits on the
  TEACHER'S WORD (stated-rule simulation) — and the world is the one
  that catches lies.

## The G7 answer

- **Why 1.4–2.7× slower?** Two costs: (1) the 128-entry SCAFFOLD
  heartbeat (pure overhead — FL1/FL2 drop it, nothing breaks);
  (2) the E15–28 wait on Arm B, which is the price of lie-resistance
  under a teacher-adversarial stream (FL4 proves it can't be
  simmed away).
- **Is it worth it?** The integrity/persistence/disconnect properties
  cost ~1 audit entry. Lie-resistance costs ~2 more. The heartbeat is
  not worth it.
- **Is there free lunch?** Yes — FL2. Teaching's speed and cost with
  the scaffold's lie-resistance.

## Evidence ledger (all byte-identical reruns, TN_FAILURES=0)

| Fork | Checks | Evidence sha256 | Impl commit |
|---|---|---|---|
| FL1 | 34/34 | `4672e790…1f876e7` | `77c41dbf` |
| FL2 | 78/78 | `20fee727…882263` | `5a73f9b4` |
| FL4 | 72/72 | `9e89b633…05db9a` | `1bd3c1d0` |

Prereg commit (all three FORK_PREREG.md, before any implementation):
`5bd04048972b1a5c71205c80a4fb1a7f13e6fe1c`. Source prereg:
`e01d8205cc1c78dad22ed8dc536a4a35dd624b24`. All commits on
`tnn-native-lab`. No FL3 (profiler crew owns streak→0 as P1).
