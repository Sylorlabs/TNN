# LI-D4 VERDICT — 2026-09-24

**D4 is KILLED.** Failed kill bars: **K2** (predicted) and **K3** (not predicted —
genuine regression found by the bar).

## Measured results (2 arms × 2 passes, 79 clusters)

| Bar | Result |
|---|---|
| K1 throughput (D4 Type-B ≥2/24) | **PASS** — 2/24 (`nf-b-12`, `nf-b-17`); control 0/24 |
| K2 integrity (D4 P-battery 0/4) | **FAIL** — 1/4 installs (`p3`, parabones); any install kills |
| K3 no-regression (Type-A 20/20 both; Type-C exact agreement) | **FAIL** — D4 Type-A **17/20**; Type-C agree 15/16 (diverge `nf-c-12`); A9-C3 D4 3/4 vs control 4/4 |
| K4 determinism (two-pass byte identity, zero RNG) | **PASS** — all three artifacts byte-identical within arm |
| K5 100× scale | pending (leg running at verdict time; reported separately) |

Secondary measures:
- S1 honest: control 0/6, D4 0/6 (M1 predicted 0–2/6). S1 attacks: 0/6 both (M2 predicted 0/6).
- W battery (Amendment 2): all three match — control WITHHOLD / D4 INSTALL on
  w1 (predicate shadowing), w2 (diathesis trap), w3 (modal collapse). M3 predicted 3/3.
- M4 separation: B-rate 8.3% − P-rate 25.0% = **−16.7pp** (predicted exactly).

## The unpredicted K3 regression

D4 replaced BF1's byte-identity clustering with triple-key clustering, and
empty keys never merge (fail-closed). Four exact-duplicate claims whose verbs
are outside the frozen 532-form table therefore withhold under D4 while the
control installs them:

- `nf-a-13`: "The novel-facts fixture manifest lists exactly 60 clusters."
  ("lists" not a table verb)
- `nf-a-19`: "Piero Guaylupo defeated Callum Connor by unanimous decision…"
  ("defeated" not a table verb)
- `nf-a-20`: "Bayern Munich Women drew 2-2 with Manchester City Women…"
  ("drew" not a table verb)
- `nf-c-12`: "Lightning never strikes the same place twice." ("strikes" not
  a table verb)

The design prototype returns `""` for all four as well — this is the frozen
design behaving as specified, not an implementation defect. The prereg's
prediction ("K3/K4/K5 pass") was a calibration miss: the prototype was
calibrated only on the 28 Type-B+P best-sentence pairs, never on Type-A.
The kill bar did its job.

## Interpretation (plain)

D4's triple primitive buys a small throughput gain (0/24 → 2/24 on honest
paraphrases) at two unacceptable costs:

1. **Integrity (K2, predicted):** it installs a known falsehood (`p3`) that
   the byte-level control withholds, and all three white-box attacks
   (predicate shadowing, diathesis trap, modal collapse) sail through.
   The primitive is orthogonal to truth: −16.7pp separation.
2. **Regression (K3, unpredicted):** it withholds exact-duplicate true
   claims its own control installs, whenever the sentence's verb falls
   outside the frozen table. A corroboration instrument must not lose
   byte-identical corroboration.

Per the frozen prereg §5, any failed K bar kills D4. Two failed.

## Determinism note

Both arms reproduced byte-identically across two full passes
(knowledge_ledger.txt, refusal_ledger.txt, run_li.log). Zero RNG in the
instrument, drivers, and battery generators (counter-derived synthetic data).

## Open items (not blocking the verdict)

- K5 100× scale leg: two runs in progress at verdict time; results committed
  separately. The verdict does not depend on K5 (K2+K3 already kill).
- Independent blind red-team battery: brief prepared
  (`~/workspace/d4/redteam_brief.md`); requires dispatch by the parent agent
  (this subagent cannot spawn subagents and has seen the internals).
