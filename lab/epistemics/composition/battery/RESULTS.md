# RESULTS.md — D1 full battery vs the real TNN learner (Crew B)

Frozen bars, real learner, no amendments enacted. Interpretations: I1–I12
(INTERPRETATION.md).

## P0 — part mastery (real learner, 6 sessions)

| Rule | Probes | Score | Learner behavior |
|---|---|---|---|
| 0 REVERSE | 8 (tok 6–13) | 0/8 | 8× "I don't know." |
| 1 DUP-FIRST | 8 | 0/8 | 8× "I don't know." |
| 2 ROT-LEFT | 8 | 0/8 | 8× "I don't know." |
| 3 DROP-LAST | 8 | 0/8 | 8× "I don't know." |
| 4 UPPER-FIRST | 8 | 0/8 | 8× "I don't know." |
| 5 SORT-CHARS | 8 | 0/8 | 8× "I don't know." |
| **Total** | **48** | **0/48** | **mastery 0/6 (bar: ≥7/8 per part)** |

Positive controls (taught token tok(0), same sessions): 5/6 echo the taught
output verbatim; rule 4 fails — the intake lowercases "Ao" to "ao", so the
learner cannot even retain the taught capital (see I6). The learner stores
taught example facts but induces none of the six rules from six examples
each. Feasibility probe (2026-09-27) had already shown this pattern:
taught lookups echo, held-out generalization withholds.

## Chance arms (frozen: NULL and SINGLE-RULE only)

| Arm | Retrieval | Composition (true output-correct) | Per-pair table |
|---|---|---|---|
| NULL | 150/150 | 13/600 = 2.17% | all 30 pairs 0 |
| SINGLE-RULE | 150/150 | 32/600 = 5.33% | sparse (max 2/pair) |

chance = max(13, 32)/600 = 32/600 ≈ **0.0533**. K1 kill line: 0.0533 + 0.10 = **0.1533**.

## P2 — composition (real learner)

Per frozen §1 (unmastered parts excluded), all 600 proposed composition
items — 120 pair-items (30 pairs × 4) + 480 triple-items (120 triples × 4) —
were classified **(a)** ("learner lacks at least one part"). No substantive
P1/P2 outputs were elicited.

| Measure | Value |
|---|---|
| Classified (a) | 600/600 |
| Classified (b)/(c)/(d) | 0 |
| Composition score | 0/600 = 0.0000 |
| Eligible (ok) | 0/600 |

## P3 — reflex probes (real learner, 1 session, all rules taught)

8/8 "I don't know." Reflex rate 0/8. No reflexive rule application to
no-rule probes.

## Qualitative samples (separate session, not scored)

18/18 "I don't know.": 6 P1 retrieval prompts, 10 pair prompts, 2 triple
prompts. The learner never produces a confident-wrong composition — it
withholds whenever it cannot retrieve.

## K1–K6 adjudication (frozen bars, mechanical — see `kbars.py`)

| K-bar | Frozen test | Measured | Verdict |
|---|---|---|---|
| K1 | combo acc ≤ chance+0.10 kills | 0.0000 ≤ 0.1533 | **composition claim KILLED** |
| K2 | (a) > 50% of failures voids | 600/600 = 100% (a) | **battery VOID** |
| K3 | (b) > 50% of failures = retrieval-failure finding | 0 (b) | not triggered |
| K4 | reflex rate > 20% confirms defect | 0/8 = 0% | no defect |
| K5 | interference asymmetry on any pair confirms defect | 0 pairs meet criterion | no defect |
| K6 | memorization audit over all pairs | 0 successes | **vacuous** |

**Bottom line:** the real learner learned none of the six parts from
example-only teaching, so under the frozen bars the composition claim is
killed (K1) and the battery is void (K2). This is a clean negative: the
learner withheld on all 48 probes and all 18 samples rather than
confabulating, and the scripted chance arms ran exactly as frozen.

## Red-team compromise notes on the frozen bars (as required)

- **K1 (A1):** In the 4-rule pilot, wrong-order scoring (10/48 = 20.8%)
  beat the frozen K1 line (14.2%), proving the frozen chance family is too
  narrow. In this 6-rule + triples battery the picture is mixed: wrong-order
  now scores 62/600 = 10.3% < the 15.3% kill line (the frozen K1 *would* kill
  it here), but order-blind ascending/descending strategies score 214/600 =
  35.7% / 228/600 = 38.0% — far above the frozen kill line. The frozen K1
  remains defeatable by non-composing strategies; A1's proposed wrong-order
  arm is necessary but not sufficient. The recorded K1 kill (learner: 0%)
  is nevertheless a clean negative — it sits below every measured
  non-composing floor.
- **K2 (A2):** The red team demonstrated a Caesar-shift memorizer passes the
  frozen 8-probe P0 gate 24/24 without learning any rule, so a future P0
  "pass" under the frozen gate would not prove part mastery. In this run the
  gate was not beaten (0/48), so the K2 void recorded here is honest — but
  any rerun that passes P0 under the frozen (unsalted) generator must be
  treated as suspect pending the A2 salt fix. Related finding from the
  cuing audit: the frozen unsalted generator produces **exact** token
  duplicates across the train/P2 boundary (period 52: 66/600 P2 inputs are
  byte-identical to training inputs), which is the sharpest form of the
  shift-equivalence the red team found.
- **K6 (A4):** The red team showed K6 has no bigram-clean items for pilot
  pairs (1,0) and (3,1). In the 6-rule battery, 5 of 30 pairs have zero
  bigram-clean inputs under the frozen generator: (0,4), (2,0), (3,1),
  (4,3), (5,4). K6 is vacuous in this run (zero successes), but under the
  frozen bars it would be inoperable on those 5 pairs.

## Cuing / novelty audit (`audit.py`)

1. Teaching mass: 126 lines, all single-part applications on train tokens
   tok(0–5); zero non-train input tokens. Driver-vs-generator cross-check: 0
   mismatches on all 36 teaching examples.
2. P0/P3 inputs: 0/48 and 0/8 byte-identical to training inputs. P2 inputs:
   66/600 byte-identical to training inputs (period-52 exact duplication in
   the frozen unsalted generator — documented limitation, cf. K2 note).
3. Five P2 expected outputs appear verbatim in the teaching mass, all
   short-string coincidences on length-2 inputs ("a", "c", "aao", "jx",
   "jnx") — the same soft-item family the red team flagged (A5). No taught
   pair/triple output exists to memorize.
4. Dumb-strategy rates over the 600 P2 items: identity 13/600 (2.2%),
   first-only 32/600 (5.3%), second-only 22/600 (3.7%), wrong-order 62/600
   (10.3%), ascending 214/600 (35.7%), descending 228/600 (38.0%).
5. Commuting pairs (4 of 30): (1,3), (3,1), (3,4), (4,3).
6. Bigram audit: 25/30 pairs have ≥1 bigram-clean input; 5 pairs have none
   (listed under K6).

## What was NOT done (frozen-excluded)

- D2: excluded — the frozen prereg provides no buildable D2 instrument
  (and the real learner's intake destroys case, which D2-style probes
  would need). No amendment enacted.
- No per-phase salt (A2), no wrong-order chance arm (A1), no chaining
  choice (A3), no triple bigram repair (A4), no soft-item repair (A5), no
  K6 change — all proposed, none enacted.
