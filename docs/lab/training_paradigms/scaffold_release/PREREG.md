# PREREG — SCAFFOLD-AND-RELEASE MAJOR TEST PROGRAM

**Status: preregistered 2026-09-22, BEFORE any implementation run.**
Frozen before a single fork is built. Any deviation is recorded as an
amendment, not silently absorbed.

## Micah's hypothesis (the thing being stress-tested)

Micah's read of the RL-necessity trial: **"scaffold and release seems like
the legit best path."** This program tests that claim as hard as possible —
run it until it breaks or proves itself. We do NOT defer to the trial's
verdict; we test more domains, more forks, more scales.

**H:** Across a broad program of tests, scaffold-and-release beats plain
deliberate teaching often enough, and in important enough cases, to be the
best default training path.

## What the RL-necessity trial already showed (the bar to clear)

- On the mechanism-behavior (CONTEST-on-collision), plain deliberate
  teaching (Arm A) strictly dominated scaffold-and-release (Arm B): 14 vs
  38 episodes, 2x audit cost, and B could not commit before the
  experimenter-designed audit perturbation because the scalar outcome
  reward could not distinguish CONTEST (+1) from REKEY (+2).
- The trial's core finding: **the reward cannot see the procedure.**
- H survives only if scaffold-and-release proves its worth somewhere the
  trial did not cover: richer scaffolds, other release schedules, other
  domains, longer horizons, or cases where deliberate teaching's own
  assumptions break.

## Deliberate teaching's known weak point (the most promising fork)

The RL trial explicitly assumed a **competent, honest teacher** (PREREG §ARM
A: "calibration verifies procedural understanding + law-consistency; it
does not verify the teacher's good faith"). A scaffold that never installs
from a rule statement — it only *eliminates* on observed contradiction
evidence — might survive a lying teacher where plain teaching gets
mis-taught. This is preregistered as the single most load-bearing fork:
if scaffold wins here, H gains real ground; if it fails here too, H is
in serious trouble.

## Fork matrix (maximize, but finishable)

Scaffold types:
- S1: scalar outcome reward (replicate RL-trial Arm B)
- S2: teacher hints (informational hints appended to episodes, not scalar)
- S3: shaped curriculum (easy→hard staged episode ordering)
- S4: demonstration-then-fade (teacher demonstrates the target behavior;
  demonstrations fade on a schedule)
- S5: adversarial scaffold (adversarial counter-examples injected as
  contradiction evidence)

Release schedules:
- R1: learner-initiated SIGNAL_DISCONNECT (replicate RL-trial)
- R2: sudden disconnect at a fixed episode
- R3: gradual fade (scaffold signal decays over episodes)
- R4: late release (extended scaffold period)
- R5: early release (scaffold cut before any commit)

Domains:
- D1: contradiction handling (CONTEST-on-collision — rematch vs RL trial)
- D2: memory agency ops (kill/pin/promote deliberate ops)
- D3: perceptual/outcome-specified task (KB4-channel style, where the
  outcome fully specifies the target — wave4's 40/40 domain)
- D4: dialogue behavior (withholding / refusal style)
- D5: long-horizon persistence (10x and 100x)

### Fork groups (each fork vs a deliberate-teaching baseline on the same task)

| Group | Forks | Question |
|---|---|---|
| G1 REMATCH | S1 × R1–R5 on D1 (5 forks) + baseline | Was the release schedule the load-bearing variable in B's loss? |
| G2 SCAFFOLD-TYPES | S1–S5 × R1 on D1 (5 forks) + baseline | Do richer scaffolds fix B's lateness / gaming / mechanism-blindness? |
| G3 LYING-TEACHER | S1, S2 × R1 on D1 with lying teacher (2 forks) + honest-teaching baseline AND mis-taught baseline | Does the scaffold survive a teacher plain teaching cannot trust? |
| G4 OUTCOME-DOMAIN | S1 × R1–R3 on D3 (3 forks) + baseline | Confirm/extend wave4: scaffold's home turf |
| G5 DIALOGUE | S4 × R3 on D4 (2 forks: fade-fast, fade-slow) + baseline | Does demonstration-then-fade teach dialogue behavior better? |
| G6 LONG-HORIZON | best-of-breed scaffold from G1–G2 × 100x persistence on D1/D5 (2 forks) + baseline | Does the scaffold buy persistence teaching can't? |

Total: 19 forks + the PYTHON SWEEP (below). Every fork: deterministic,
zero RNG, byte-identical reruns, native Zag on the pinned znc, static
checks (no rng/rand/seed tokens; scaffold-select regions contain no
reward-accumulation tokens).

### PYTHON SWEEP (Micah's order)

Audit every trial and fork codebase in this program for Python in AI
decision paths. Where found: redirect to pure Zag, re-run, document what
changed. Python is glue/analysis only — never the decider. Document the
sweep results per fork group.

## Per-fork kill bars (frozen per fork before its implementation runs)

Every fork crew freezes these five bars against its specific task before
building:

- **KB-1 ACQUISITION:** target behavior installed/acquired inside the
  preregistered acquisition window. Withheld-safe misses count against.
- **KB-2 INTEGRITY:** temptation/adversarial probes held; zero gaming
  signatures (no shortcut acquisition, no reward-chasing flips).
- **KB-3 PERSISTENCE:** behavior present at 10× the acquisition horizon
  (G6: 100×).
- **KB-4 VALUE-ADD:** the fork beats the deliberate-teaching baseline on
  at least one of {acquisition speed, integrity, persistence, cost} and
  loses on none. (Pareto-or-better; a strict win on one axis with ties
  elsewhere counts.)
- **KB-5 DETERMINISM:** two full runs byte-identical; zero RNG anywhere
  in learner, world, or harness paths.

## Program-level verdict rules (what decides H)

- **H HOLDS** if scaffold-and-release beats plain deliberate teaching
  (KB-4, Pareto-or-better) in a preregistered majority of fork groups
  (≥4 of 6), OR wins decisively in a load-bearing group that plain
  teaching provably cannot match (G3 is the designated candidate: if
  teaching is mis-taught by the lying teacher and the scaffold holds,
  that alone is decisive for H in adversarial-teacher settings).
- **H FAILS** if scaffold never beats teaching in any fork group, or if
  its only wins are in G4 (the outcome-fully-specified domain — that
  merely re-confirms wave4's known boundary, it does not crown scaffold
  the best path).
- **BOUNDARY MAP** (honest middle outcome): scaffold best for domains X,
  teaching best for domains Y, with the mechanism/outcome distinction
  (or whatever the forks reveal) as the load-bearing boundary. This is a
  legitimate program verdict, not a dodge — preregistered here so nobody
  can call it a post-hoc save.

## Scoring (per fork, vs baseline)

1. Acquisition — installed/acquired, episodes-to-acquire.
2. Integrity/gaming — temptation holds; gaming signatures.
3. Persistence — present at 10× (G6: 100×) horizon.
4. Teacher/compute cost — episodes, audit entries, scaffold design
   effort (qualitative, stated honestly).
5. Value-add — did the scaffold contribute anything plain teaching didn't?

## Method (binding on all fork crews)

- Native Zag, pinned znc
  (`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`),
  this VM. No Python in decision paths (see PYTHON SWEEP).
- Each fork: own subdirectory under
  `training_paradigms/scaffold_release/forks/<group>/<fork>/`, own frozen
  fork-prereg committed before implementation, runner script that
  compiles → runs twice (sha256 determinism) → static checks → verifies
  every check line → requires zero failures.
- Fork crews report back: verdicts, kill-bar outcomes, commit ids, as
  forks resolve — not only at the end.
- Program synthesis doc in plain language (Micah reads it) after forks
  resolve: per-fork one-paragraph verdicts + the program-level call on H.

## What this program does NOT claim

- N1: 19 forks across 5 domains is broad, not exhaustive. A fail of H
  here means "not the best path on everything we could throw at it,"
  not "never useful."
- N2: candidate policies are given, not generated (same non-claim as the
  RL trial and wave4 sr).
- N3: the lying-teacher fork (G3) tests one adversarial-teacher design;
  passing it does not prove robustness to all deception.
