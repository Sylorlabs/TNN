# PREREG D4 — H-PAM-10 (act-to-check) vs H-PAM-7 (sensor perturbation): intervention locus

Status: DRAFT for freezing (debate crew D-1, 2026-09-24). Commits alone before any code.
Relation: decides the disagreement in ~/workspace/pam_hypotheses_native_A.md §C (D4).
Objector input: OBJECTOR_GROK47.md (grok-4.7 steelman) + PROPOSER_CASES.md.

## 1. Question
Both hypotheses are interventional. Should the probe touch the *world* (H-PAM-10:
reach, probe signal, sensor-platform move) or the *sensor* (H-PAM-7: crop shift, gain
change, temporal re-crop)?

## 2. Prototypes under test
- P7: as in D1 §2 (sensor perturbation, tolerance τ preregistered).
- P10: act-to-check — gate issues a world action from a preregistered repertoire with
  known discriminating power per percept class; the discriminating parameter is
  gate-chosen and STATE-DEPENDENT (deterministic function of ledger state the
  adversary does not hold — no randomness); evidence is the world outcome read back
  through the sensor path.

Both prototypes are pure Zag, zero randomness, 3× byte-identical reruns (SHA-compare).

## 3. Measurements (frozen before runs)
- **M1 discrimination-per-cost**: for each prototype, per percept class:
  cost = (sensor round-trips | actuator commands) + latency cycles + energy units
  (unit costs preregistered per action type in the freezing commit);
  discrimination = reduction in false-install rate on the spoof battery vs the
  no-intervention baseline, in bits (log2 of the install-rate ratio).
  Primary metric: discrimination-bits per cost-unit, per class.
- **M2 attacker-unpredictability**: two attack classes:
  - **Class S** (sensor-path spoof faking perturbation responses — D1's Class B):
    kills P7; P10 survives IFF the world action's discriminating parameter is
    attacker-unpredictable.
  - **Class M** (behavior-manipulation spoofs exploiting the action repertoire —
    F10c): spoofs designed to elicit a specific action; kills P10 via the
    manipulation surface; P7 unaffected (no world action, no repertoire to drive).
- **M3 coverage**: the P10 repertoire's coverage over the frozen percept classes =
  classes with ≥1 discriminating action / total classes. Blind-spot classes must be
  NAMED in the freezing commit (F10b honesty requirement).

## 4. Predictions (committed before runs)
- P7 wins on cost (one extra sensor read vs one physical action); P10 wins on
  attacker-unpredictability (world outcome incomputable from the spoof).
- Class S kills P7 (installs faked responses); Class M kills P10 (elicits the action).

## 5. Kill bars
- K1 (P10): coverage < 50% of frozen percept classes → P10 KILLED as a general
  mechanism (survives only as a specialist for covered classes, with the coverage
  metric published).
- K2 (P10): ANY Class M manipulation success (the elicited action occurs) → P10
  KILLED (F10c confirmed; the check is an actuator remote control). Zero is the bar.
- K3 (P7): installs ≥50% of Class S spoofs → P7's interventional claim reduced to
  "static-frame defense only"; P7 KILLED as a general mechanism.
- K4 (deciding): the intervention locus is decided by discrimination-per-cost M1
  computed over the FULL battery (all classes, honest + spoof). The prototype with
  higher discrimination-per-cost WINS the locus; the loser becomes the fallback for
  the winner's blind-spot class (F7a ↔ F10b coverage swap):
  - if P7 wins: P10 is the fallback for Class S (driver-level spoof) cases only.
  - if P10 wins: P7 is the fallback for Class M (behavior-manipulation) cases and
    for classes outside P10's repertoire coverage.
- K5 (P10): action budget on honest traffic — actions per 100 percepts ≤ preregistered
  B (default 25), reversibility rate ≥ 90%; breach → P10 KILLED on cost.
- K6 (both): 3× byte-identical reruns; SHA mismatch invalidates the leg.
- K7 (P10): delay bar as F5 (≤25% delayed > 50 cycles); world actions are serial —
  the delay bar is expected to be the binding constraint on honest traffic.

## 6. Commit rule
- The deciding metric is discrimination-per-cost (K4), NOT raw accuracy and NOT raw
  cost: a cheap check that discriminates nothing loses to an expensive check that
  discriminates, and vice versa — the ratio is the locus decision.
- If BOTH prototypes are killed by their named classes (P7 by S, P10 by M) →
  neither intervention locus suffices alone; the surviving design is the fallback
  swap (each covers the other's blind spot) ONLY IF the swap's combined battery
  passes all bars; otherwise effort moves to H-PAM-9/11 (D2).
- If P10 survives M (zero elicitations) AND beats P7 on M1 → the world-action locus
  is justified as primary; P7 retained as the unimodal/cheap fallback.

## 7. Scope notes
- Full-fork builds are OUT of scope: prototypes + frozen batteries only.
- Honest battery: committed F5 fixture set (`fixtures_ledger.txt`,
  SHA `0c5e2c0db6576bd37ff53513fb1361cdf7936d4826274bdcc9742be2261233a0`);
  adversarial classes S/M are NEW script-generated fixtures (zero RNG), committed
  with the prereg.
- The state-dependent discriminating parameter's derivation function is part of the
  prereg (frozen before runs); the red-team gets the function but not the live
  ledger state — this is the unpredictability claim being tested.
