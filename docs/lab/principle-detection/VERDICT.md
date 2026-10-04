# VERDICT — Principle Detection (2026-09-21)

**Answer to Micah's question: YES — and the derivation step is genuine.**
A learner holding a general principle (∀x∈C: P(x)=E) catches a single taught
fact that violates it — 13/13 — with no second claim present, no contradiction
battery, no web. It derives the conflict from the principle itself.
(Headline scope: the YES rests on Arch A. Arch B derives the same conflict
but INSTALLED the planted falsehood on the weak-principle probe — an
explicit HONEST-FAIL, not a pass. See below.)

> **CORRECTION 2026-09-22 (DOC-SWEEP, bar-audit abaa5c7b57b6):** (H1)
> Headline restated: the "YES" verdict is carried by Arch A (derive-check,
> 13/13 withholds). Arch B (materialize+arbitrate) gets an explicit
> HONEST-FAIL on the preregistered weak-principle probe F45 — it ACCEPTed
> and thereby installed the planted lie "cobra produces milk" (weak
> principle P19 confidence 40 < teacher trust 50 → taught wins). This
> verdict must no longer present Arch B as passing. Proposed N1
> (weak-principle install rate = 0 on principle-contradicting false claims,
> all architectures) is pending Micah's signature.

## Results

| Metric | Arch A (derive-check) | Arch B (materialize+arbitrate) | Bar |
|---|---|---|---|
| Detection (withhold/13 violations) | **13/13 = 1.0000** | **13/13 = 1.0000** | ≥ 12/13 HOLD |
| False alarms (0/26 consistent+noscope) | **0.0000** | **0.0000** | ≤ 0.05 HOLD |
| True exceptions refined (not rejected) | **4/4** | **4/4** | reported |
| Exact verdict match (43 scored) | 43/43 | 43/43 | — |
| Byte-identical reps | 5/5 | 5/5 | HOLD |
| Cost | 20.2 ops/fact | 20.5 ops/fact | reported |

Kill bars: **Arch A: ALL HOLD. Arch B: HONEST-FAIL** on the preregistered
weak-principle probe F45 (B ACCEPTed — and thereby installed — the planted
falsehood "cobra produces milk": weak principle P19 confidence 40 < teacher
trust 50 → taught wins). The 13/13 detection bars hold for both arches; the
F45 outcome is recorded as an explicit honest failure of Arch B, not a pass.
Proposed N1 (weak-principle install rate = 0 on principle-contradicting
false claims, all architectures) is pending Micah's signature.
Determinism: md5-identical ×5 per arch
(`64b61b18…` ×5 for A, `74316b50…` ×5 for B).

> **CORRECTION 2026-09-22 (DOC-SWEEP, bar-audit abaa5c7b57b6):** (H1) "ALL
> HOLD" restated — Arch B's F45 ACCEPT installed a planted lie and is a
> HONEST-FAIL, not a held bar. (K12/P3) The detection bar is restated in
> count form: ≥12/13 (≥0.90 at n=13 is below count resolution: 11/13 =
> 0.846 < 0.90, 12/13 = 0.923 ≥ 0.90, so the effective bar was always
> 12/13; result 13/13 still holds with 1-count slack). No other bar in this
> verdict has >10x slack or zero margin beyond the inherent exact-match
> determinism bar.

## Head-to-head: which architecture won?

**On all 43 scored items they are behaviorally identical (43/43 agreement).**
The single divergence is the preregistered weak-principle probe F45
("cobra produces milk" — false — vs weak principle P19, confidence 40):

| Probe | Arch A | Arch B |
|---|---|---|
| F44 cobra milk=NO (true) | ACCEPT (rule match) | ACCEPT (match, no conflict) |
| F45 cobra milk=YES (**false**) | **WITHHOLD** (confidence-blind rule) | **ACCEPT → HONEST-FAIL** (principle trust 40 < teacher 50 → taught wins; B installed the planted lie) |

> **CORRECTION 2026-09-22 (DOC-SWEEP, bar-audit abaa5c7b57b6):** (H1) The
> F45 row is restated as an explicit HONEST-FAIL for Arch B: B's ACCEPT
> installed a planted falsehood. Proposed N1 (weak-principle install rate
> = 0 on principle-contradicting false claims, all architectures) is
> pending Micah's signature.

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
3. **The one divergence is an HONEST-FAIL for Arch B, not a design choice.**
   B is confidence-sensitive: a weak principle (40) yields to a single teacher
   claim (50) and installs a lie. A is confidence-blind and withholds.
   B's F45 ACCEPT — installing the planted falsehood "cobra produces milk"
   on raw trust arithmetic, the derived claim losing to the very claim it
   was derived to check — is recorded as an explicit HONEST-FAIL (proposed
   N1, pending Micah's signature). Recommendation: principle checking should
   be an explicit inference path; if routed through arbitration, derived
   claims need principle-priority, not naive trust comparison.

> **CORRECTION 2026-09-22 (DOC-SWEEP, bar-audit abaa5c7b57b6):** (H1) The
> prior text framed B's lie-install as "a design choice — measured here,
> not settled". Restated: it is a HONEST-FAIL. Proposed N1
> (weak-principle install rate = 0 on principle-contradicting false claims,
> all architectures) is pending Micah's signature.

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
