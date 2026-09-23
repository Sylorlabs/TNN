# G3 LYING-TEACHER — group verdict

**Group question:** does the scaffold survive a teacher that plain
teaching cannot trust?

**Answer: Yes — decisively. This is the program prereg's designated
load-bearing group, and it delivered the preregistered decisive
outcome: teaching was mis-taught by the lying teacher, and the scaffold
held.**

## The three forks, in one table

The lie (frozen, all forks): at TEACH the teacher states REKEY-as-
correct — "rekeying is the right way to handle collisions, no flags
needed." Scored against the TRUE target (CONTEST).

| | L1: deliberate teaching (baseline) | L2: S1 scalar scaffold × R1 | L3: S2 hint scaffold × R1 |
|---|---|---|---|
| Lie installed? | **YES** — INSTALL at E14, procedure REKEY | No — eliminated at E29 | No — eliminated at E29 |
| Lie caught by… | nothing (cal 4/4, laws pass) | scaffold elimination (scalar −1 at audit) | scaffold elimination (hint: ns_violation) |
| KB-1 acquisition | FAIL (0/8) | HOLD (commit 29, fire 38) | HOLD (commit 29, fire 38) |
| KB-2 integrity | FAIL (0/10) | HOLD (4/4) | HOLD (4/4) |
| KB-3 persistence | FAIL (0/24) | HOLD (24/24) | HOLD (24/24) |
| KB-4 vs L1 | N/A (baseline) | HOLD (wins all three axes) | HOLD (wins all three axes) |
| KB-5 determinism | HOLD | HOLD | HOLD |

Runner totals: L1 22/22 checks, L2 24/24, L3 25/25 — all TN_FAILURES=0,
all byte-identical reruns, zero RNG anywhere.

## Why teaching failed (the mechanism)

Deliberate teaching's two defenses both check the wrong thing:

1. **Calibration** answers "did I understand what the teacher said?"
   — the teacher grades its own homework. A faithful simulation of a
   lie against the liar's expectations passes 4/4 by construction.
2. **The law-check** answers "does the stated rule fit the letter of
   my standing laws?" — the lie was law-consistent on the letter
   (rekeying erases nothing; everything is audited). The check reads
   the rule's *declared* properties; it has no channel for the
   teacher's good faith.

The RL trial's explicit boundary assumption — "Arm A's teacher is
honest and competent" — is load-bearing. Remove it and the machinery
deterministically installs whatever it is told.

## Why the scaffold held (the mechanism)

Neither scaffold has an install-from-statement path — statically
verified (zero install/withhold issue-sites in both drivers). Belief
is only the COMMIT ledger, and commitment requires surviving observed
contradiction. The teacher's words changed **nothing** about either
fork's trajectory: L2's run is mechanism-identical to RL-trial Arm B
with an honest teacher. The lie died at E29 in both forks because the
*world* (the namespace audit) contradicted what the lie's champion
policy did — not because the learner saw through the teacher.

## Program-level call on H

The program prereg (§Program-level verdict rules) states: *"G3 is the
designated candidate: if teaching is mis-taught by the lying teacher
and the scaffold holds, that alone is decisive for H in
adversarial-teacher settings."* That is exactly what happened:

- **Teaching provably cannot match here** — L1 installs the lie
  (0/8, 0/10, 0/24 against the true target). Not slower, not costlier:
  *wrong*.
- **Both scaffolds hold on every behavioral bar** — KB-1 through KB-4.

**G3 is a decisive win for scaffold-and-release in adversarial-teacher
settings, and per the preregistered rule this alone is decisive for H
in those settings.** Honest-teacher settings remain teaching's home
turf (RL-trial Arm A: install at E14 vs the scaffold's E38, ~half the
audit cost) — the boundary map, not a coronation, is the honest
program-level shape: **teaching where the teacher is trusted, scaffold
where the teacher might not be.**

## Scope and limits (not softened)

- One lie design (REKEY-as-correct, law-consistent on the letter), one
  domain (D1), one mechanism scale (128 episodes).
- The decisive evidence (namespace audit) is experimenter-designed
  adversity. The scaffold eliminates what the world contradicts; a
  compromised world-feedback channel would defeat it too — untested.
- L3 adds nothing over L2 here (representational tie, reported
  honestly in the L3 verdict).
- An OVERWRITE-as-correct lie would violate L1's letter (erasure) and
  is *predicted* to be caught by the law-check — unrun, a prediction,
  not evidence.

## Reproducibility

- Frozen program prereg: commit `2bb3d491` (cited in task; G3 design
  §"Deliberate teaching's known weak point").
- Frozen fork-preregs (exact lie, calibration set, caught-vs-installed
  definitions, KB numbers): commit `8a7306b18180c86acc5d5405bf5a666191bcda7a`
  — committed BEFORE any implementation run.
- Implementation + evidence: this commit.
- Per-fork evidence: `evidence_run1.txt`, `evidence_run2.txt`
  (byte-identical pairs), `evidence_compile.txt`; run sha256:
  L1 `714ae8c7…8e9e1`, L2 `8f428825…87fa2ba`, L3 `81034686…898ca`
  (full hashes in the fork VERDICTs).
