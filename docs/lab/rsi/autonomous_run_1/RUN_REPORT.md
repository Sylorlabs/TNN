# Autonomous RSI Run 1 — run report (frozen record)

Prereg: RUN_PREREG.md. Baseline: BASELINE.md. Commits: Phase 0 `5c5056fc`,
Phase 0b `2eab7157`, driver fix `bb8a18ff`.

## Clock

Loop started 2026-09-22 (t+0 at first loop deliberation). TNN declared itself
done at t+97s via HALT(three-barren) — well under the 1-hour budget.
(The hour is a ceiling, not a quota: the deliberation converged.)

## Deliberation transcript (verbatim PROP_* lines, all 3/3 deterministic)

### Round 0 (kept=- tried=- retired=- barren=b0 web=web0)

```
PROP_CHAMP,proxy_acc=22,proxy_wrong=2,proxy_cost=424
PROP_SIM,cand=c1,dacc=2,dwrong=-2,dcost=32,improved=2,v2=1
PROP_SIM,cand=c2,dacc=2,dwrong=-2,dcost=128,improved=2,v2=1
PROP_SIM,cand=c3,dacc=-6,dwrong=0,dcost=0,improved=0,v2=1
PROP_SIM,cand=c4,dacc=0,dwrong=0,dcost=-64,improved=0,v2=1
PROP_SIM,cand=c5,dacc=-14,dwrong=-2,dcost=0,improved=0,v2=1
PROP_DECISION,decision=PROPOSE
PROP_CAND,cand=c1,track=improvement
PROP_PRED,dacc=2,dwrong=-2,cost=456
PROP_RUN,extra=c1
```

Execution: 5/5 byte-identical. Verifier:
`SCORES: acc=24/24 wrong=0/24 cost=456 consults=18 recall=10000 costq=200`
`PREDICTION-VERDICT: HIT` (predicted acc∈[23,25] wrong∈[-1,1] cost==456).
`NO-DEGRADATION: PASS`. → KEPT. Intuition 1/1.

### Round 1 (kept={c1})

Deliberation re-simulated all eligible candidates against the new champion.
C1 now kept (ineligible); C2's marginal improvement collapsed to dacc=0
(its two fixes were already taken by C1) at +96 marginal cost → rejected.
C3/C5 harmful → rejected.
`PROPOSE c4 (efficiency), pred(dacc=0,dwrong=0,cost=384)`.
Execution: `acc=24/24 wrong=0/24 cost=384` → HIT, no degradation → KEPT.
Intuition 2/2.

### Rounds 2–4

Round 2: BARREN (b0→b1). Round 3: BARREN (b1→b2). Round 4: HALT,
reason=three-barren. No candidate cleared the bars; TNN stopped itself.

## Result

- Kept: C1 (2-against-1 evidence override), C4 (redundant-consult skip).
- Champion: ask-first + C1 + C4 → **acc 24/24, wrong 0/24, cost 384**
  vs baseline ask-first 22/2/424.
- Intuition score: **2/2** (every published prediction verified).
- No web queries (the thin-win trigger never fired).
- No retirements, no constitution (V2) violations, RECALL=10000 and
  COST-quiet=200 unchanged in every test.
- Discarded by the bars without testing: C3 (majority-override, -6 acc),
  C5 (consult-always, -14 acc), C2 (marginally dominated by C1).

## Honesty notes (for the red teams)

1. The "native deliberation" is proposer.zag: deterministic Zag compiled from
   the native-deliberation agent's written analysis (CANDIDATES.md, SELF_MODEL.md).
   The candidate SHAPES were identified by that analysis, not invented live by
   a running TNN. Whether this counts as "TNN itself, no help" is the central
   question the red teams must press.
2. Predictions that "hit" were computed by exact simulation of the same
   decide() the subject runs — transfer was proxy→real battery, not
   prediction→measurement in the strong sense. The intuition score measures
   cross-battery generalization, nothing more.
3. Both batteries are 24 hand-made items from one generator family. C1's
   evidence-override rule is proven only on those shapes.
4. C4's skip rule is compositional: it keys off the CURRENT kept policy's
   verdicts. A future kept candidate that changes verdicts could silently
   change what C4 skips.
