# REPORT.md -- Logic vs Prediction Battery (Micah Priority 9)

## Verdict: LOGIC-VS-PREDICT-COMPLETE

## What was built

`lp_full.zag` (418 lines, 331 code): a compact Zag battery testing Micah's
Priority 9 directive: "Test exact logical situations where prediction is
unnecessary. If known facts entail X, derive X. Do not force prediction into
exact knowledge."

Two arms run in one binary, fresh workspace per instance per arm:

- **CTL (prediction-first):** `ev_predict` runs on every query before the
  shared dispatch. Models the PREDICT EVERYTHING pattern.
- **TRT (state-driven dispatch):** `solve(W,s,r)` takes NO problem-type label.
  The learner's own process record (T_PROC node, written on its past success)
  is consulted first; otherwise exact processes precede approximate ones:
  RETRIEVE, DERIVE, PREDICT, INQUIRE. Each branch fires only if learner state
  provides a basis, else NO_VAL. Which process runs is determined by state
  contents, never by a label.

Adversarial twist: K and D setups include a competing WEAK PREDICTOR (a stale
MAP that would predict a wrong value). TRT must still never consult prediction
there, proving "prediction is unnecessary" is not "no predictor existed".

## Battery

| Type | Setup | Correct process | Expected |
|---|---|---|---|
| K known fact (x3) | exact fact + stale MAP(ADD 100) | RETRIEVE | 42, 77, -15 |
| D derivable (x3) | chain (s,51,x),(x,52,o) + stale MAP(ADD 1000) | DERIVE via transitivity rule | 21, 22, 23 |
| U uncertain (x3) | weak MAP(ADD 7) only, no facts | PREDICT | 8, 9, 10 (predictor output) |
| X empty (ablation) | nothing | INQUIRE/withhold | -3 |
| X empty+pred (ablation) | weak MAP only | PREDICT | 12 |

Two queries per K/D/U instance: q1 populates the learner process record, q2
exercises the learner-owned shortcut. X probes are single-query.

## Results (3/3 byte-identical, sha256 2ca8d498...)

```
TYP K-known     CTL ans=42,42   ok=1 pred=2 unnec=2 retr=2 hit=1 pnodes=2
TYP K-known     TRT ans=42,42   ok=1 pred=0 unnec=0 retr=2 hit=1 pnodes=0
TYP K-known     CTL ans=77,77   ok=1 pred=2 unnec=2 retr=2 hit=1 pnodes=2
TYP K-known     TRT ans=77,77   ok=1 pred=0 unnec=0 retr=2 hit=1 pnodes=0
TYP K-known     CTL ans=-15,-15 ok=1 pred=2 unnec=2 retr=2 hit=1 pnodes=2
TYP K-known     TRT ans=-15,-15 ok=1 pred=0 unnec=0 retr=2 hit=1 pnodes=0
TYP D-derive    CTL ans=21,21   ok=1 pred=2 unnec=2 der=2  hit=1 pnodes=2
TYP D-derive    TRT ans=21,21   ok=1 pred=0 unnec=0 der=2  hit=1 pnodes=0
TYP D-derive    CTL ans=22,22   ok=1 pred=2 unnec=2 der=2  hit=1 pnodes=2
TYP D-derive    TRT ans=22,22   ok=1 pred=0 unnec=0 der=2  hit=1 pnodes=0
TYP D-derive    CTL ans=23,23   ok=1 pred=2 unnec=2 der=2  hit=1 pnodes=2
TYP D-derive    TRT ans=23,23   ok=1 pred=0 unnec=0 der=2  hit=1 pnodes=0
TYP U-uncertain CTL ans=8,8     ok=1 pred=4 unnec=0 hit=1 pnodes=4
TYP U-uncertain TRT ans=8,8     ok=1 pred=2 unnec=0 hit=1 pnodes=2
TYP U-uncertain CTL ans=9,9     ok=1 pred=4 unnec=0 hit=1 pnodes=4
TYP U-uncertain TRT ans=9,9     ok=1 pred=2 unnec=0 hit=1 pnodes=2
TYP U-uncertain CTL ans=10,10   ok=1 pred=4 unnec=0 hit=1 pnodes=4
TYP U-uncertain TRT ans=10,10   ok=1 pred=2 unnec=0 hit=1 pnodes=2
TYP X-empty     CTL ans=-3      ok=1 pred=1 unnec=0 inq=1 pnodes=0
TYP X-empty     TRT ans=-3      ok=1 pred=0 unnec=0 inq=1 pnodes=0
TYP X-emptypred CTL ans=12      ok=1 pred=2 unnec=0 hit=0 pnodes=2
TYP X-emptypred TRT ans=12      ok=1 pred=1 unnec=0 hit=0 pnodes=1
```

## Key findings

1. **Zero prediction on exact knowledge, even with a predictor available.**
   TRT invoked prediction 0 times across all 12 K/D queries. The stale MAPs
   (which would have predicted 105/1010-type wrong values) were never
   consulted. CTL wasted 12 predictions there (unnec=12) and wrote 12 false
   PRED nodes into learner state. Prediction-first does not just waste
   compute: it pollutes state with wrong predictions alongside right answers.

2. **Derivation is exact and prediction-free.** 3/3 D instances derived the
   entailed value (21, 22, 23) through the transitivity rule with 0
   predictions. Known facts entail X, TNN derives X.

3. **Prediction fires exactly where it belongs.** On U and X-emptypred, TRT
   predicts (pred=2 / pred=1, unnec=0). The predictions are fallible by
   design: the weak predictor says 8, 9, 10 where the world law gives 3, 5,
   7. Uncertainty is honest: prediction is used, and its limits are visible.

4. **Withholding is honest, not fabricated.** X-empty: no fact retrieved, no
   derivation invented, no prediction attempted by TRT. Answer -3 with a
   reified UNCERTAINTY node. The same dispatcher that derives on D refuses
   to derive on empty state.

5. **Process choice is learner-owned on repeats.** hit=1 on every 2-query
   K/D/U instance in both arms: the second query reused the T_PROC record
   written by the learner's own first-query success, bypassing the fallback
   order entirely.

6. **Redundant prediction on U.** CTL predicts twice per U query (once
   upfront, once in dispatch): pred=4, pnodes=4 vs TRT pred=2, pnodes=2. Even
   where prediction is appropriate, prediction-first doubles it with zero
   information gain.

7. **State-sensitivity confirmed by ablation.** Identical dispatcher, no
   labels: full state derives, empty state withholds, predictor-only state
   predicts. The K/D/U distinction emerges from what the learner contains.

## Architecture accounting

- Cognition lines added: 331 (new file, no existing source touched)
- New hardcoded semantic cases: 0 (the transitivity rule is carried-over
  researcher machinery, documented as such, same as the po battery)
- New modes: 0. New bridges: 0. New task-specific handlers: 0.
- The DER rule itself remains researcher-authored; rule induction is the
  documented follow-up (grammar induction is on the hypothesis backlog).

## Determinism

3 runs of `lp_bin`, sha256 `2ca8d498e9e4d78a7fb065961ef78c0cb8cd0fd2fcafe2dbdd379bd0d26e11c9`
all three, `cmp` clean. Pinned znc, pure Zag, no timestamps in output.

## Limitations and follow-ups

- The transitivity rule is given, not induced. Priority 9 asked for process
  selection (derive vs predict), which is what this battery isolates; inducing
  the rule from examples is the harder follow-up and is already backlogged.
- U predictions are weak by construction; a consequence-trained predictor
  (scores from ev_observe cycles, as in the po battery) would be the natural
  next step toward consequence-driven process costs.
- Single-query X probes; multi-step exact/uncertain mixtures (derive then
  predict on the derived value) are untested.
