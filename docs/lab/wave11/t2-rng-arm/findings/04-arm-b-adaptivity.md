# Arm B adaptivity metric — slice 04

## Slice
Adaptivity metric for Arm B (fenced RNG experimental arm): specify what honest loss looks like
numerically, and the bar for the surprising case where RNG appears adaptive.

## Falsifiable claim
Across N=400 paired trials (same input, lawful internal-state delta), Arm B's output
variation carries no information about the state delta: direction rate 0.50 ± 0.05 and
state↔choice normalized mutual information (NMI) < 0.03, with both 95% bootstrap CIs covering
the null. If Arm B's NMI ≥ 0.10 or its direction rate falls outside [0.40, 0.60] with
p < 0.01, the "RNG is non-adaptive" null is killed and a seed-leakage forensic is mandatory
before any adaptivity is credited.

## Design
Paired-state protocol. Fix input I; present under lawful states S_a, S_b differing on one
logged axis (e.g. context partition load, depth of prior deliberation in audit). For each
trial, Arm B draws from its prereg-enumerated RNG points (seeded, logged); Arm C runs its
deterministic state-dependent variation. Extract from output a discrete variation choice
V ∈ {candidate phrasing, path taken, elaboration depth bucket}.

Zag-flavored sketch (builder implements; no semantics invented beyond this):

```
fn adaptivity_run(trials: []Trial, arm: i32) -> (f64, f64) {
  let dir: i32 = 0; let n: i32 = 0;
  // choice_log: per-trial (state_bucket, choice) appended to audit words
  for t in trials {
    let (va, vb) = (arm_output(t.I, t.Sa), arm_output(t.I, t.Sb));
    n = n + 1;
    if varies(va, vb) and aligned_with(t.state_delta, variation_dir(va, vb)) { dir = dir + 1; }
    audit_append(t.id, t.Sa, t.Sb, va, vb);   // logged, replayable
  }
  let rate: f64 = dir / n;                    // direction rate, null = 0.50
  let nmi: f64 = nmi_state_choice(choice_log); // null ≈ 0.0
  return (rate, nmi);
}
```

NMI computed over state-bucket × choice contingency table; null CI via 10,000
permutation bootstraps (labels shuffled, seeds logged). Rate CI via binomial exact.
Verdict requires BOTH metrics from the same replayed log (amendment: reproducibility
from logged state is itself an Arm B test — a seeded log that does not replay
byte-identically fails Arm B on that axis independently of adaptivity).

## Kill bar
The null ("Arm B non-adaptive") is killed — NOT celebrated — if either fires:
(K1) NMI_ArmB ≥ 0.10 with 95% CI lower bound > 0.05; or
(K2) direction rate ∉ [0.40, 0.60] with exact-binomial p < 0.01 (two-sided).
Converse pre-commit: if Arm B lands inside rate ∈ [0.45, 0.55] and NMI < 0.03, the
adaptivity loss is recorded as CONCLUSIVE HONEST LOSS — no hand-waving, no "promising
trend" language. Arm C's measured adaptivity is the positive control and must show
rate ≥ 0.80, NMI ≥ 0.40 or the harness is broken (invalid run, not an Arm B win).

## Honesty notes
- **Candidate-set smuggling (lawful-looking but misattributed):** if Arm B's candidate
  pool is state-dependent, a uniform draw over a state-shaped set IS state-tracking with
  RNG on top. Any K1/K2 firing must first re-audit the candidate generator: the
  adaptivity belongs to the generator (Arm C's territory), not the draw. A win through
  this channel is an attribution error, not an RNG win.
- **Seed leakage:** the RNG must be seeded from the prereg-enumerated source only. If the
  seed chain touches state words (timestamps, state hashes, audit cursors), "adaptivity"
  is state-dependence laundered through a PRNG — a fence violation, instant Arm B retire.
- **Null NMI is not "no variation":** Arm B may vary MORE than Arm C (higher raw
  entropy) while being adaptive ZERO. Report raw choice-entropy alongside; do not let
  "more diverse" be read as "more adaptive."
- Not claiming: this says nothing about Arm B on integrity traps, judgment stability,
  or replay — those are other slices' metrics. Not claiming RNG is "bad"; the claim is
  precisely that it does not track state.
- Weakest point: the metric depends on the harness producing genuinely lawful,
  state-delta-only pairs. If S_a vs S_b leaks into the input channel, both arms look
  adaptive and the positive control check (Arm C) will not catch it.

## Next build step
Build the paired-state harness + Arm C positive control FIRST, with no Arm B code: verify
Arm C lands rate ≥ 0.80 / NMI ≥ 0.40 and the permutation-null on shuffled labels lands
NMI < 0.03. Only then wire Arm B's seeded draws into the same harness and run the
rate/NMI battery — so an Arm B anomaly is evidence about RNG, not about harness bugs.
