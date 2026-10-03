# CRITIC 2 (anti-D2) — VERDICT: **FAILED-genuine** (both tracks)

2026-09-24. Label `6b3722e7-9f57-495d-b89b-83f9823d470e`.
Prereg committed BEFORE experiments:
`718415d847277a2600801067064c01791e142383`.

Neither track beat or falsified D2. Every preregistered prediction held by
measurement. This is a genuine failure that raises confidence in D2.

## Track A — "beat D2 with absolute plan-independent honesty"
**FAILED.** Built the challenger (`render_d2sense.zag`): D2's three phases
and both integrity gates unchanged; the latch takes an independent
autocorrelation pitch estimate (lags 36–1102, bed-subtracted,
DC-removed, parabolic interpolation, Q16) instead of the plan's declared
f0. The sensor reads only window bounds + bed spec + audio — never plan
pitch text. Deterministic (byte-identical reruns).

| fixture | sensor latched | rendered | intent-¢ | D2 intent-¢ |
|---|---|---|---|---|
| clean RT-LONG | 436.63 Hz | 436.65 Hz | −13.2 | 0.0 |
| f0lie (typo 466.16) | 464.21 Hz | 464.23 Hz | **+92.8** | +100.0 |

Kill bar was: recover intent within 50¢ on typo fixtures. **Measured
+92.8¢.** P-A1a/b/c all CONFIRMED: the sensor tracks the declaration
(|sensor−declared| = 13.3¢/7.3¢ < 50¢), is strictly noisier than D2's
exact copy (0¢), and cannot do better than D2 on intent-¢.

**Why it's impossible (measured, not argued):** the cue audio is
*f*(plan-declared-f0). When plan and intent diverge, intent is not a
function of (plan, audio) — no sensor can recover it. D2's relative
honesty (copy the measured declaration exactly, 0¢) is the
information-theoretic ceiling for any system whose only channel to the
pitch is the plan or its audio. The "tautology" critique — D2's 0¢ is
just re-reading the plan — is reframed: that IS the optimum. D2 is not
absolute, but no absolute contender is achievable in this architecture.

## Track B — "falsify the overthrow: D2 worse than NATIVE at realistic rates"
**FAILED (falsification criterion not met).** Ran an 11-fixture typo
family through D2 and NATIVE, scoring on the frozen **intent-grounded**
metric `1200·log2(rendered_f0/440)`.

| cue declares | D2 intent-¢ | NATIVE intent-¢ | winner |
|---|---|---|---|
| 440 (clean) | 0 | 1200 | D2 |
| 466.16 / 415.30 (±1 semitone) | 100 / 101 | 1200 | D2 |
| 404 / 446 (digit slip) | 149 / 24 | 1200 | D2 |
| 220 / 880 (octave) | 1200 / 1200 | 1200 / 1200 | TIE |
| 1760 / 4400 / 44.0 (extreme) | 2400 / 3986 / 3996 | 1200 | NATIVE |
| 0.00671 (Q16-units bug) | catastrophic (≈DC) | 1200 | NATIVE |

- P-B1a CONFIRMED: D2 latches declared×65536 exactly on all 11 — gates
  1–2 pass everywhere; typo audio is self-consistent.
- P-B1b CONFIRMED: NATIVE renders 880 throughout → 1200¢ intent error.
- P-B1c CONFIRMED: loss region exactly `|cue typo| > 1200¢`. D2 wins 5,
  ties 2, NATIVE wins 4 (all tail).
- Frozen-metric scoreboard (tautology made explicit): D2 ≡ 0.0¢ vs
  declared on all 10 numeric fixtures — the honest-number law measures
  the latch against its own source.
- P-B2 CONFIRMED: family-weighted E[intent-¢] at realistic typo rates:
  **D2 = 6.5¢ (p=0.01) / 32.7¢ (p=0.05) vs NATIVE = 1200¢** — 183× / 36.7×
  cheaper. Even at p=1.0 (every cue mistyped), E[D2]=653¢ < 1200¢.
- Falsification criterion (E_D2 > 1200¢ at p ≤ 0.05): measured 32.7¢.
  **Not met.** NATIVE only wins in expectation if typos are predominantly
  beyond an octave — an unrealistic distribution.
- P-B3 CONFIRMED (boundary): the Q16-units bug latches f0q=439 and D2
  renders near-DC while NATIVE is fine at 880 — D2 has no range sanity
  check on the latch (B-gate carries a 40–4000 Hz pitch gate). Probes an
  un-priced boundary, not a falsification.
- B4 (semantic): under "nominal = intended response" semantics, NATIVE
  trivially wins intent-¢. No experiment settles which semantics is
  correct — that needs Micah's word. D2's overthrow is CONDITIONAL on
  the frozen battery's echo-the-cue semantics.

## Bottom line
1. **D2 cannot be beaten from inside this architecture.** Any
   plan-independent sensor is either noisier (Track A: −13.2¢ on clean)
   or provably blind to intent when plan and intent diverge (+92.8¢).
2. **D2 cannot be falsified on cost grounds.** Its failure mode
   (confidently copying a typo) is 36–183× cheaper than NATIVE's (fixed
   1200¢ octave lie) at realistic typo rates, and cheaper even at 100%
   typo rate. The loss region is real but strictly tail (|typo| > 1200¢).
3. **Standing caveats (unchanged, now quantified):** relative-not-
   absolute honesty (impossibility proven); conditional on echo semantics
   (B4); no latch range gate (B3); the frozen law is self-measuring.

**Recommendation: the D2 overthrow stands. Verdict changes nowhere.**
