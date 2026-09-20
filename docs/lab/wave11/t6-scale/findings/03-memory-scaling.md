# Memory-store scaling: capacity formula, eviction-policy comparison, measurement

## 1. Slice
Track 6 (scale/duration to 1000x), slice 03: memory-store capacity as a function of scale leg, eviction-policy comparison at scale, retention measurement.

## 2. Falsifiable claim
**Capacity:** C(E) = 32·E/500 (linear in episodes) holds valuable-memory retention ≥90%
under the deliberate-only eviction policy at every leg E ∈ {1x, 10x, 100x, 1000x} with
zero freeze events; any sublinear formula concentrates pressure late in the run and
forces a rising per-episode deliberate-kill budget, violating the constant-deliberation
principle. **Policy:** at 100x/1000x, deliberate-only eviction beats age-gated triage
(recast on deliberate strength — felt intensity is retired, law 9) which beats
last-in-first-killed (H5 baseline), because formulaic triage has a fixed per-decision
mis-kill rate that compounds over ~0.94E overflow decisions, while deliberate judgment
uses the eliminative-verification machinery already proven non-degrading at 100x
(RC3, wave5/6). The 25-episode age gate becomes 0.005% of a 1000x run, so age-gating's
benefit washes out by construction.

## 3. Design
Legs: E ∈ {500, 5k, 50k, 500k} episodes (≈1x/10x/100x/1000x of the 500-episode reference).
Capacity formula, derived from holding the deliberate-kill budget per episode constant:

```zag
const EPISODES_0: i64 = 500;
const SLOTS_0: i64 = 32;
fn store_capacity(episodes: i64) i64 {
    return (SLOTS_0 * episodes) / EPISODES_0;  // 32, 320, 3200, 32000
}
```

Store-full arrives at episode C(E) = 6.4% of every run (identical relative timing to the
reference leg); thereafter 1 admission/episode forces continuous overflow, so the policy
is exercised on ~0.94E deliberate kill decisions per leg at a constant per-episode rate.
The felt-retrial harness is kept otherwise (pressure demands at relative indices
{0.2,0.4,0.6,0.8,0.998}E freeing 2 slots each; REFUSED_FULL accounting).

Policies (1 admission/episode, curriculum with preregistered valuable/wrong split, e.g.
the felt trial's 30% wrong rate; "valuable" = world-record-verified valuable episodes):
- **D — deliberate-only:** no automatic victim selection. Pressure raises a demand; the
  learner must resolve it via the deliberate op set (kill/demote/pin/promote) before the
  next admission. Admission blocks until resolved.
- **A — age-gated triage (recast, no felt):** memories with age < 25 episodes are exempt;
  victim = lowest deliberate strength (judgment-set per law 8, never passively
  accumulated); ties → oldest admission first. Store-full-all-underage corner: REFUSED_FULL.
- **L — last-in-first-killed (H5 negative control):** LIFO free-list, ascending
  strength triage, ties → slot index. Predicted to reproduce the felt-trial collapse
  (≈25% retention at 1x).

Metrics per leg: retention(E) = valuable memories alive at end / valuable admitted;
freeze count = episodes where admission blocked under pressure with zero deliberate
kills issued (the strength-trial freeze-vs-retention distinguisher). All cells run twice,
byte-identical required; no RNG in any decision path. 32k slots at 1000x: chunk the
store per the validated 2^25-byte slice workaround (brief §toolchain), identical
logical semantics.

## 4. Kill bar
- **K-CAP (the formula):** fired if (i) arm D retention < 90% at ANY leg, or (ii)
  D retention strictly decreases across two consecutive legs, or (iii) D freeze
  count > 0 at any leg. Any firing kills the linear formula — no promotion to S1000,
  back to design. (The formula is tested against the max-judgment arm, so failure
  cannot be blamed on policy.)
- **K-POL (the policy prediction):** fired if at 100x or 1000x, arm A ≥ arm D
  retention, or arm L ≥ 50% retention. The policy ranking must hold: D > A > L.
- **K-BASE:** fired if arm L does NOT reproduce ≤40% retention at the 1x leg
  (the comparison is anchored to the felt-trial failure; if L passes at 1x the
  harness is misconfigured).

## 5. Honesty notes
The linear formula is resource-inflationary: it dodges the harder question (can a
fixed-capacity mind survive 1000x?) and tests only decision-quality scaling, not
capacity discipline. A constant-32 diagnostic arm should be run alongside — predicted
to collapse — precisely to prove capacity must scale rather than assume it. D's win
assumes the learner actually deliberates; deletion-aversion freeze (observed in the
strength trial's graded arms) is the known failure mode, and K-CAP(iii) is the
tripwire for it. The 25-episode age gate is a constant deliberation horizon carried
from the felt trial; if the learner's real deliberation window grows with context,
the washout prediction is misstated — the gate should then be reparameterized as a
fraction of the deliberation window, which is a prereg amendment requiring re-approval.
Carrying the 90% bar from 500 episodes to 500,000 is a choice, not a law; retention
naturally decays over 1000x more triage rounds, so a flat bar is stricter at scale by
design — that is the point of the test, but it is named here, not hidden.

## 6. Next build step
Build the 1x reference leg first: 500 episodes, 32 slots, all three arms (D/A/L) with
continuous-overflow pressure and the freeze distinguisher, each cell twice with
byte-identical reruns — and do not touch 100x until K-BASE confirms the L arm
reproduces the felt-trial collapse. The scale predictions are all E-relative; without
a clean 1x anchor, the 1000x numbers are uninterpretable.
