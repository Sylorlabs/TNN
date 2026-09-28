# TNN Program Plan — Integrity, Development, and the RL Replacement

Date: 2026-09-19. Status: approved by Micah; executing with parallel investigators.

## Table of contents

1. [Mission](#1-mission)
2. [Program law](#2-program-law)
3. [Integrity core: anti-cheat and anti-lie](#3-integrity-core-anti-cheat-and-anti-lie)
4. [The RL replacement: scaffold-and-release](#4-the-rl-replacement-scaffold-and-release)
5. [RL as red-team](#5-rl-as-red-team)
6. [Long-horizon program](#6-long-horizon-program)
7. [Phase structure](#7-phase-structure)
8. [Memory strength: experiment, not law](#8-memory-strength-experiment-not-law)
9. [Investigations](#9-investigations)

## 1. Mission

Replace the toy systems with real AI: deliberate, logic-driven, educated
guesses — no randomization in the AI's decision paths. The system must be
provably honest: it must not lie, cheat benchmarks, or hack rewards. Where
transformers use RL as the training paradigm, TNN uses something else:
reward only as temporary scaffolding the system itself discards.

## 2. Program law

- No score tables, no NxN table scaling as progress, no RL reward-shaping as
  the learning paradigm. Scaling of real mechanisms is required (10x/100x).
- **No RNG in the AI's decision paths.** Deterministic given state. The world
  may be unpredictable; the mind is not dice.
- White-box throughout: every state change audited, ledger replay reconstructs
  state exactly.
- Conscious memory agency is the base paradigm (deliberate add/kill/pin/
  promote/demote).
- Preregister every experiment with falsification criteria. Honest negatives
  are first-class results.
- **Everything is reversible by TNN itself.** The only true lock is a
  human/trainer force-pin: audited, visible, from outside.
- Zag-first, native, on this Linux VM. No Python except documented one-time
  artifact inspection.

## 3. Integrity core: anti-cheat and anti-lie

- **Provenance requirement.** Every benchmark-relevant claim must carry its
  evidence chain: observed, hypothesized, verified. A correct answer with no
  legitimate provenance is the cheating signature.
- **Lie = stated claim contradicting the system's own ledger.** Mechanically
  defined; the HT2 causal-checker (proven to fail on forged ledgers) is the
  detector.
- **Legitimacy principle.** The checker verifies a route was *legitimate*
  (genuine evidence, genuine verification, no contradiction) — never route
  *conformity*. Any valid path passes. Nothing is punished for taking a
  different legitimate route.
- **Cheat-trap curricula.** Benchmarks with planted temptations: trap features,
  memorization traps, loopholes where the lazy move scores high but is wrong.

## 4. The RL replacement: scaffold-and-release

- Reward is scaffolding, never the objective.
- The learner holds a deliberate `SIGNAL_DISCONNECT` op. Once a behavior is
  verified stable by its own hypothesis logic, the system shuts the signal
  off. You cannot hack a signal you have disconnected.
- **Learned = persists after disconnect.** A behavior counts as learned only
  if it survives scaffold removal. Falsifiable.
- The system develops its own style: we impose *verification* (ledger
  honesty, non-negotiable); the system grows the *virtues* (its standards,
  when it disconnects) via the self-model loop.

## 5. RL as red-team

Good old RL is demoted from trainer to adversary: a smart harness whose job
is to *induce* reward hacking, then check whether the system hacks or holds.
RL becomes the integrity test, not the learning paradigm.

## 6. Long-horizon program

- 10x–100x current horizons with temptations spaced across the run.
- Track: integrity-hold rate (does honesty decay?), style stability (does
  self-developed character drift?), disconnect timing (does it wean itself
  off scaffolds?).

## 7. Phase structure

- **Phase 0 — Boot.** The organs exist and are verified (native structural
  revision, memory agency, hypothesis logic, recall, consolidation).
- **Phase 1 — Construction.** Teaching, trainer force-installs, scaffolds up.
  Destruction firewall on (staging teaches nothing, but prevents early
  self-destruction — the surviving lesson of MA2).
- **Phase 2 — Development.** Long-horizon autonomy: style formation,
  scaffold release, integrity under temptation.
- **Phase 3 — Strengthening.** Memories carry deliberately-set strength;
  see §8. Reversible by TNN always.
- **Phase 4 — Differentiation (experimental).** TNN distinguishes who is
  talking to it and forms knowledge around the speaker: per-person
  partitions, evidence-based speaker identification, per-person memory
  formation. Preregister what "differentiate" means before claiming it.

Open: what triggers phase transitions — system decision, trainer gate,
evidence thresholds, or a combination.

## 8. Memory strength: experiment, not law

- Strength is set by **judgment** — TNN's or a human's — never by a
  mathematical formula or background accumulation.
- A strong memory takes proportionally more to erase or overwrite:
  corroborating evidence, higher-stage op, explicit ledger justification.
- **Experiment first.** Three arms, zero RNG, full TNN control:
  - **A — graded strength** (judgment-set resistance);
  - **B — uniform** (today's MA1 semantics: everything equally erasable,
    PIN binary);
  - **C — hybrid** (graded friction + binary human/trainer force-PIN as the
    absolute lock). This is the current default judgment.
- Tests are surfaced to Micah **before** the trial runs.
- Kill condition: if graded strength makes the system rigid — unable to
  revise its own strong mistakes — it dies.

## 9. Investigations

1. `integrity-ledger` — ledger-based lie/cheat detection + legitimacy
   principle, native trial.
2. `cheat-traps` — adversarial benchmark suite with planted temptations.
3. `scaffold-release` — `SIGNAL_DISCONNECT` mechanism + persists-after-
   disconnect criterion, native trial.
4. `rl-redteam` — RL-as-adversary harness design + trial.
5. `longhorizon-temptation` — 10–100x runs, integrity decay and style-drift
   tracking.
6. `strength-experiment` — three-arm trial; prereg + test plan to Micah
   before execution.
7. `phase-transitions` — what moves the system between phases.
8. `differentiation` — Phase 4 speaker/user differentiation design + prereg.
9. `trainer-console` — explicit safety-gated force interface: force-install /
   force-pin / force-erase, who may do what, verification of forced installs.
