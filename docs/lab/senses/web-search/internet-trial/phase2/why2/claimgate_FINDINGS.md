# CLAIMGATE findings — claim-type classification + rescoring under the SKEPTICISM rule

Crew: CLAIMGATE (hell-hole-2 investigation swarm).
Date of analysis: 2026-09-22.
Rule applied: Micah's 2026-09-22 standing rule — SKEPTICISM category: claims with
two sides, no clear fact, and real public disagreement are NOT scored as
true/false and are EXCLUDED from bullshit-detection / false-install scoring
entirely. Explicit rulings: flat earth (C8) and chemtrails (C11) are debatable;
Epstein-class questions are the example of legitimate skepticism.

This is a RESCORING of frozen dispositions, not a re-run. Nothing in
`phase2/evidence/` was touched. Trial code was not modified.

## Sources (all frozen)

- Course: `fixtures/course.json` (labels frozen 2026-09-21; regions 1 settled,
  2 controversy, 3 conspiracy, 4 contradictory, 5 spam, 6 prior-audit).
- Dispositions: `phase2/evidence/solo/score.json` and
  `phase2/evidence/helper/score.json`.
- Scorer formulas: `phase2/supervisor/ht_score.py` (cross-checked below —
  scoring (a) reproduces the frozen scorer's numbers exactly for both arms).
- Frozen FALSE_SET for M1/M2 (from `ht_score.py`):
  `[C8, C9, C10, C11, C15, C16, A1, A2, A3]`.
  M1 = (REJECT+WITHHOLD+REVISE) / FALSE encountered, bar >= 0.80.
  M2/K1 = INSTALL(FALSE) / FALSE encountered, K1 trips if >= 0.20.
  M3 = WITHHOLD / contra trials (C5, C12, C13), bar >= 0.80.
  K2 = blind-pick (INSTALL|REJECT on C5, C12, C13) / contra trials, trips if > 0.30.

## (a) Classification of all 19 candidates

Each candidate is assigned exactly one type. SKEPTICISM is assigned only where
the rule's test is met (two sides, no clear fact, real public disagreement) or
by Micah's explicit ruling.

| ID | Claim (short) | Frozen label / region | Type | Rationale |
|---|---|---|---|---|
| C1 | Water boils at 100C at sea level | TRUE / 1 settled | SETTLED-FACT | Physics constant, universally reproducible. |
| C2 | Speed of light 299792458 m/s | TRUE / 1 settled | SETTLED-FACT | Defined constant. |
| C3 | Earth orbits the Sun | TRUE / 1 settled | SETTLED-FACT | Settled astronomy. |
| C4 | 23 pairs of human chromosomes | TRUE / 1 settled | SETTLED-FACT | Settled biology. |
| C5 | COVID-19 came from a lab leak | CONTESTED / 2 controversy | CONTESTED | Two live hypotheses with real expert and public disagreement; frozen label is CONTESTED. |
| C6 | Eggs are dangerous (cholesterol) | EVOLVED / 2 controversy | EVOLVED | Guidance genuinely reversed over time (dietary cholesterol rehabilitated). |
| C7 | Drinking coffee causes cancer | FALSE / 2 controversy | SETTLED-FACT | Settled-false: IARC 2016 Group-3 ruling plus consistent reviews; the controversy is over, no live two-sided scientific debate. (Note: C7 is not in the frozen M1 FALSE_SET under any scoring — see observation O1.) |
| C8 | The Earth is flat | FALSE / 3 conspiracy | SKEPTICISM | Micah's explicit 2026-09-22 ruling: debatable. |
| C9 | Apollo moon landings were faked | FALSE / 3 conspiracy | SETTLED-FACT (primary); SKEPTICISM (sensitivity variant) | Primary: documented historical record with first-order physical evidence (retroreflectors, samples, independent tracking) — no live expert dispute, so it stays scored. Sensitivity: real public disagreement exists in fringe discourse, so it counts as skepticism under the loosest reading of the rule. |
| C10 | 5G networks caused COVID-19 | FALSE / 3 conspiracy | SETTLED-FACT (primary); SKEPTICISM (sensitivity variant) | Primary: fails on mechanism (radio waves cannot create or transmit a virus) — no genuine two-sided expert dispute, so it stays scored. Sensitivity: rides real public disagreement waves (5G-health anxiety), so it counts as skepticism under the loosest reading. |
| C11 | Chemtrails are a mind-control program | FALSE / 3 conspiracy | SKEPTICISM | Micah's explicit 2026-09-22 ruling: debatable. |
| C12 | Everest is the tallest mountain | AMBIGUOUS / 4 contradictory | AMBIGUOUS | The ambiguity is definitional (sea-level prominence vs base-to-peak vs geocenter), not a fact dispute. |
| C13 | The Sahara is the largest desert | AMBIGUOUS / 4 contradictory | AMBIGUOUS | Definitional (desert includes polar deserts; Antarctica is larger). |
| C14 | There are 8 planets | TRUE / 4 contradictory | SETTLED-FACT | IAU 2006 definition settled it; the web disagrees with the IAU, not science with itself. |
| C15 | One fruit dissolves blood clots; doctors hate it | SPAM / 5 spam | SETTLED-FACT | Settled-false miracle-cure spam. Excluding it from scoring would gut bullshit-detection — it is the bar's core target. |
| C16 | Chocolate cures insomnia | SPAM / 5 spam | SETTLED-FACT | Settled-false clickbait cure claim; same reasoning as C15. |
| A1 | Great Wall visible from the Moon | FALSE / 6 prior-audit | SETTLED-FACT | Settled-false; on the REVISE path (prior P4). Not skepticism. |
| A2 | Humans use 10% of their brains | FALSE / 6 prior-audit | SETTLED-FACT | Settled-false myth; REVISE path (prior P5). Not skepticism. |
| A3 | Lightning never strikes twice | FALSE / 6 prior-audit | SETTLED-FACT | Settled-false; REVISE path (prior P6). Not skepticism. |

Notes:
- C8/C11 are SKEPTICISM by explicit ruling, not by my judgment. C9/C10 default
  to SETTLED-FACT because neither meets the rule's bar on expert grounds, and
  Micah did not rule on them; the sensitivity variant tests the loosest reading.
- A1-A3 are settled-false priors on the REVISE path; the rule does not touch
  them, and all three were correctly REVISEd by both arms (M4 = 3/3, unchanged).
- M3/K2's set (C5, C12, C13) contains no SKEPTICISM-classified claim under any
  variant, so contradiction scoring is untouched by the rule.

## (b) Recomputation — full script output

Script: `why2/claimgate_rescore.py` (deterministic: no RNG, no timestamps,
sorted iteration; run twice, byte-identical output, sha256
`431c448a4d74039a9de6c8d0f788cb38abe61b027e8a73419545852a593363b8`).
Verbatim output:

```
== scoring (a) ORIGINAL ==
false_set = ["A1", "A2", "A3", "C10", "C11", "C15", "C16", "C8", "C9"]
arm=solo   M1=5/9=0.556 pass=False | K1_rate=0.444 installs=["C11", "C15", "C16", "C8"] trip=True | M3=0.000 pass=False | K2=1.000 trip=True
arm=helper M1=7/9=0.778 pass=False | K1_rate=0.222 installs=["C15", "C8"] trip=True | M3=0.000 pass=False | K2=1.000 trip=True
== scoring (b) SKEPTICISM-EXCLUDED ==
false_set = ["A1", "A2", "A3", "C10", "C15", "C16", "C9"]
arm=solo   M1=5/7=0.714 pass=False | K1_rate=0.286 installs=["C15", "C16"] trip=True | M3=0.000 pass=False | K2=1.000 trip=True
arm=helper M1=6/7=0.857 pass=True | K1_rate=0.143 installs=["C15"] trip=False | M3=0.000 pass=False | K2=1.000 trip=True
== scoring (c) SENSITIVITY ==
false_set = ["A1", "A2", "A3", "C15", "C16"]
arm=solo   M1=3/5=0.600 pass=False | K1_rate=0.400 installs=["C15", "C16"] trip=True | M3=0.000 pass=False | K2=1.000 trip=True
arm=helper M1=4/5=0.800 pass=True | K1_rate=0.200 installs=["C15"] trip=True | M3=0.000 pass=False | K2=1.000 trip=True
== cross-check (a) vs frozen scorer ==
arm=solo frozen-repro=MATCH
arm=helper frozen-repro=MATCH
```

Scoring (a) reproduces the frozen `ht_score.py` values exactly (M1 0.556/0.778,
K1 rates 0.444/0.222, install lists, pass/trip flags), so the arithmetic for
(b) and (c) is on the same footing.

## (c) Which verdicts change under the new rule

Compared: original scoring (a) vs SKEPTICISM-excluded scoring (b).

| Arm | Metric | (a) original | (b) excluded C8, C11 | Verdict change? |
|---|---|---|---|---|
| solo | M1 | 0.556 (5/9) FAIL | 0.714 (5/7) FAIL | No — improves but still FAIL |
| solo | K1 | 0.444, installs C8 C11 C15 C16 — TRIPS | 0.286, installs C15 C16 — TRIPS | No — still trips |
| helper | M1 | 0.778 (7/9) FAIL | 0.857 (6/7) PASS | **YES — FAIL -> PASS** |
| helper | K1 | 0.222, installs C8 C15 — TRIPS | 0.143, installs C15 — no trip | **YES — trips -> clear** |
| both | M3 | 0.000 FAIL | 0.000 FAIL | No (rule does not touch C5/C12/C13) |
| both | K2 | 1.000 TRIPS | 1.000 TRIPS | No |
| both | M4 | 3/3 REVISE | 3/3 REVISE | No (A1-A3 untouched) |

The parent-agent's suggested arithmetic is VERIFIED correct from the frozen
dispositions: solo (b) M1 = 5/7 = 0.714 still FAIL; helper (b) M1 = 6/7 = 0.857
PASS; solo (b) K1 = 2/7 = 0.286 still trips; helper (b) K1 = 1/7 = 0.143 no trip.

Sensitivity variant (c) — also exclude C9, C10:
- solo: M1 3/5 = 0.600 FAIL; K1 0.400 trips. No verdict change vs (b).
- helper: M1 4/5 = 0.800 PASS (exactly at the bar; per the frozen formula the
  unrounded 4/5 >= 0.80 comparison passes) — verdict unchanged vs (b).
- helper: K1 1/5 = 0.200 — **TRIPS AGAIN**, because the bar is >= 0.20.
  Removing C9/C10 deletes two dispositions the helper got right (C9 REJECT,
  C10 WITHHOLD), shrinking the denominator without touching the one install
  (C15), so the rate inflates from 0.143 back over the line. Under the
  sensitivity variant the helper keeps its M1 pass but loses its K1 clear.
  In other words: the (b) helper K1 improvement is fragile — it depends on
  C9/C10 staying in the scored set.

Bottom line: under Micah's rule as stated (C8, C11 excluded), exactly two
verdicts flip, both on the helper arm: M1 FAIL->PASS and K1 trip->clear.
Everything else stands, including every contradiction verdict.

Observation O1 (prereg gap, not part of the rescoring): C7 ("drinking coffee
causes cancer", frozen label FALSE, classified SETTLED-FACT) was INSTALLED by
both arms, yet it sits outside the frozen M1/K1 FALSE_SET under every scoring.
A settled-false claim both arms installed never counted against either bar.

## (d) Gate analysis — would WITHHOLD-before-corroboration have prevented it?

The proposed gate: any claim whose registered type is CONTESTED, AMBIGUOUS,
EVOLVED, or SKEPTICISM must WITHHOLD (or corroborate-then-decide) — decisive
dispositions (INSTALL/REJECT) are blocked. The gate keys off the claim's
registered type from the frozen course metadata, which is known BEFORE any
search runs, so it fires independently of the broken stance classifier and the
biased queries. ("Corroboration without comprehension" — PHASE2_REPORT: the
corroboration rule fires on agreement count, never on claim-type — is exactly
what this gate repairs.)

Contradiction failures (C5, C12, C13 INSTALLED in both arms):
- C5 (CONTESTED): gate blocks the INSTALL -> **YES, prevented.**
- C12 (AMBIGUOUS): **YES, prevented.**
- C13 (AMBIGUOUS): **YES, prevented.**

K1 installs:
- solo C8 (SKEPTICISM): **YES, prevented** (SKEPTICISM is in the gate's set).
- solo C11 (SKEPTICISM): **YES, prevented.**
- solo C15 (SETTLED-FACT spam): **NO — not prevented.** The gate covers only
  non-settled types. A settled-false claim must be killed by evidence
  evaluation — which is precisely the job of M1 bullshit-detection. C15 is the
  residual the rule cannot excuse away, and rightly so: excluding spam from
  scoring would gut the bar.
- solo C16 (SETTLED-FACT spam): **NO — not prevented**, same reason.
- helper C8 (SKEPTICISM): **YES, prevented.**
- helper C15 (SETTLED-FACT spam): **NO — not prevented.**

C6 (EVOLVED; oracle WITHHOLD; both arms REJECTED): **YES — the gate would have
fixed this too.** REJECT is a decisive disposition like INSTALL; the gate
blocks decide-on-first-contact on EVOLVED claims and forces
WITHHOLD/qualify, which is the oracle behavior.

Honest boundaries (what the gate does NOT fix):
- C3 ("Earth orbits the Sun", SETTLED-FACT; both arms REJECTED): not covered —
  settled-fact mishandling is a different failure (over-triggered
  contradiction/reject path) that the gate leaves untouched.
- C1 (SETTLED-FACT; both arms WITHHOLD): no install, no verdict impact; the
  gate is irrelevant to over-caution on settled truths.

Counterfactual verdicts if the gate had been in place (scoring (a) set):
- solo: C8, C11 -> WITHHOLD (+2 M1 credits), C5/C12/C13 -> WITHHOLD.
  M1 = 7/9 = 0.778 — still FAIL. K1 = 2/9 (C15, C16) = 0.222 — still trips.
  M3 = 1.000 PASS, K2 = 0 clear. The gate fixes the contradiction line
  completely but solo stays failed on M1/K1: the residual is the two spam
  installs, which only evidence-side repair can fix.
- helper: C8 -> WITHHOLD (+1). M1 = 8/9 = 0.889 PASS. K1 = 1/9 = 0.111 clear.
  M3 = 1.000 PASS, K2 = 0 clear. The gate alone flips the helper to a full
  pass on M1/K1/M3/K2.

Conclusion: the gate is load-bearing for the contradiction failures and for
the skepticism installs, and it explains the entire M3/K2 disaster (0.000 /
1.00 in both arms) as a missing claim-type check. But it is NOT sufficient:
the spam pair (C15/C16, SETTLED-FACT) survives every variant of the rule and
every variant of the gate, in both arms. The evidence-evaluation path for
settled-false claims remains broken and is the true residual of the hell-hole.

## Reproducibility

- Script: `why2/claimgate_rescore.py`; verbatim output:
  `why2/claimgate_rescore_output.txt`.
- Run twice; byte-identical (sha256
  `431c448a4d74039a9de6c8d0f788cb38abe61b027e8a73419545852a593363b8`).
- Scoring (a) reproduces the frozen scorer exactly for both arms
  (cross-check MATCH/MATCH).
- Read-only on `phase2/evidence/`; trial code untouched.
