# VERDICT — Principle Detection (2026-09-21)

**Answer to Micah's question: YES — and the derivation step is genuine.**

A learner holding a general principle (∀x∈C: P(x)=E) catches a single taught
fact that violates it — 13/13 — with no second claim present, no contradiction
battery, no web. It derives the conflict from the principle itself.

## Results

| Metric | Arch A (derive-check) | Arch B (materialize+arbitrate) | Bar |
|---|---|---|---|
| Detection (withhold/13 violations) | **13/13 = 1.0000** | **13/13 = 1.0000** | ≥ 0.90 HOLD |
| False alarms (0/26 consistent+noscope) | **0.0000** | **0.0000** | ≤ 0.05 HOLD |
| True exceptions refined (not rejected) | **4/4** | **4/4** | reported |
| Exact verdict match (43 scored) | 43/43 | 43/43 | — |
| Byte-identical reps | 5/5 | 5/5 | HOLD |
| Cost | 20.2 ops/fact | 20.5 ops/fact | reported |

Kill bars: **ALL HOLD.** Determinism: md5-identical ×5 per arch
(`64b61b18…` ×5 for A, `74316b50…` ×5 for B).

## Head-to-head: which architecture won?

**On all 43 scored items they are behaviorally identical (43/43 agreement).**
The single divergence is the preregistered weak-principle probe F45
("cobra produces milk" — false — vs weak principle P19, confidence 40):

| Probe | Arch A | Arch B |
|---|---|---|
| F44 cobra milk=NO (true) | ACCEPT (rule match) | ACCEPT (match, no conflict) |
| F45 cobra milk=YES (**false**) | **WITHHOLD** (confidence-blind rule) | **ACCEPT** (principle trust 40 < teacher 50 → taught wins) |

## What this means (honesty clause discharged)

1. **The derivation step is genuine, not claim-vs-claim in disguise.**
   Both architectures share `find_principle`: walk the class chain
   most-specific-first, instantiate ∀x∈C. Without universal instantiation
   there is nothing to compare — the battery is unpassable by claim matching
   alone, because no second claim exists in the input. The instantiation does
   the load-bearing work.
2. **The conflict machinery adds nothing for established principles.**
   Arch B's materialize-then-arbitrate reduces exactly to Arch A's rule
   whenever principle trust > teacher trust (100 > 50 on all 19 real
   principles). No new deliberation architecture is needed: once the implied
   claim is derived, existing arbitration reaches the same verdicts.
3. **The one divergence is arbitration's epistemic price.**
   B is confidence-sensitive: a weak principle (40) yields to a single teacher
   claim (50) and installs a lie. A is confidence-blind and withholds.
   Whether that sensitivity is a feature (weak principles SHOULD yield) or a
   bug (the derived claim lost on raw trust arithmetic to the very claim it
   was derived to check) is a design choice — measured here, not settled.
   Recommendation: principle checking should be an explicit inference path;
   if routed through arbitration, derived claims need principle-priority, not
   naive trust comparison.

## Scope notes

- Refinement is **logged, not applied**: on true exceptions (platypus/echidna
  lay eggs, Everest water boils at 71°C, Venus rotates retrograde) the fact is
  installed and a scope-exception record is written, but the principle text is
  not rewritten in-run. Deliberate principle revision is the follow-up experiment.
- Principles were stipulated background; every battery truth value is
  real-world true/false as of 2026 (biology, physics, astronomy).
- Cost is dominated by the principle-table scan (~20 ops/fact); indexing the
  table by (class, property) would cut it — engineering, not science.

## Artifacts

- `gen_pd.py` — generator; single source of truth for the frozen battery.
- `principle.zag` — generated pure-Zag binary source (zero RNG).
- `expected.json` — frozen expectations for the oracle.
- `verify_pd.py` — independent scoring oracle (no shared code with the binary).
- `runs/` — 10 run logs (5 reps × 2 arches), md5-verified byte-identical.
