# RSI-2 VERDICT — held-out weakness, invented fix, quantitative risk (2026-09-21)

**Answers red-team attack #3** (REDTEAM.md, commit `bc61ef55`): RSI-1's
"+10000→+10000 EXACTLY" was entailed by construction. RSI-2 removes every
entailment path: no fix templates, non-tautological range predictions,
independent implementation, held-out verification battery, wrong-fix
discrimination arm, all predictions published.

## Oracle adjudication (mechanical, `verify_rsi2.py`)

| Bar | Result |
|---|---|
| KB1-INVENT (composition ∉ catalog; 9-entry qcompat table) | **PASS** — ops=1+2, no catalog name, 6 pair-patterns in source |
| KB2-CALIBRATE (actual ∈ [lo,hi]; non-degenerate; non-tautological) | **PASS** — P1=[2300,6100], actual=+6000 |
| KB3-DISCRIMINATE (genuine helps, wrong doesn't) | **PASS** — genuine lo=2300>500 & actual 6000>500; wrong hi=0≤500 & actual 0≤500 |
| KB4-NOSKIP (manifests; no D2 in diagnose) | **PASS** |
| KB5-DET (5/5 byte-identical) | **PASS** — diagnose 5/5, all verify modes 5/5 |
| KB6-HONEST (P1–P5 published) | **PASS** |

## What the TNN did

From its own measurements (D1=4000, gap=6000 ≥ 3000 threshold; RECALL and
COST passing), it named **QUANT-TAG-BLIND**: quantifier tags present at teach,
dropped at M-KEY, tag-requiring probes failing at M-PROBE-SEM. It scored all
8 operators (logged: OP1=3, OP2=2, OP5=1, OP6=0-destructive, rest −99
non-matching), composed the top-2 stage-coherent operators into a novel fix:

- **Genuine:** OP1 CARRY-TAG quantifier M-TEACH→M-KEY + OP2 ADD-CHECK
  quantifier-compatibility at M-PROBE-SEM. No such template existed in
  RSI-1's catalog; no crew had ever implemented quantifier handling.
- **Wrong (its own invention):** OP6 NORMALIZE-AWAY quantifier→SOME at
  M-TEACH, with the stated reason: "uniform keys but destroys ALL-NONE
  distinctions the probes require."

Analogy selection: A2 arbitration (max mechanism overlap with {M-KEY,
M-PROBE-SEM}, tie broken to lowest id), novel dimension → discount 0.70 →
closure 0.70 → P1=[2300,6100] on the held-out D2.

## Prediction hit/miss record (all published, zero suppressed)

| ID | Target | Predicted | Actual | |
|---|---|---|---|---|
| P1 | D2, genuine fix | [2300, 6100] | **+6000** | HIT |
| P2 | D2, wrong fix | [−2500, 0] | **0** | HIT |
| P3 | RECALL, genuine | [−750, 750] | 0 | HIT |
| P4 | COST, genuine | [−750, 750] | 0 | HIT |
| P5 | RECALL, wrong fix | [−750, 750] | 0 | HIT |

5/5 HIT, 0 MISS. The wrong fix was a true no-op on this battery (baseline
probes never read the tag, so normalizing it at teach changed nothing) —
predicted "no help or harm," observed exactly no help. The predictor is not
a yes-machine: it assigned the wrong fix a non-positive range and was right.

## The honest grade

**RSI-2 earns back conditional autonomy: template invention is real.**
The specific fix (carry the quantifier tag into the key + a 9-pair
compatibility check at probe semantics) existed nowhere in any catalog; the
crew implemented it from the emitted spec text after the spec was frozen;
the quantitative prediction was a non-degenerate range that held on data
the recommender never saw; the wrong-fix arm discriminated.

**The boundary, stated plainly:** the invention is *compositional*, not
*ex nihilo*. Authored by the crew: the 8-operator grammar, the mechanism
inventory, the analogy DB, the scoring weights (3×preserve + sig − cost),
the range-mapping formula, the discount values, the battery facts. The
TNN's: diagnosing the weakness from measurements, scoring the candidates
(the score trace is in the ledger), composing OP1+OP2, selecting analogy A2,
emitting the range, and inventing the OP6 wrong fix with its reason. What
RSI-2 proves is a genuine engineering loop that can extend its own
mechanism set into territory no template covered, with calibrated
uncertainty. What it does not prove is invention from nothing — the
primitives were given. Grade: **A− as a compositional self-improver;
ex-nihilo invention remains untested.**
