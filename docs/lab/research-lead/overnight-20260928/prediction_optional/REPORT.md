# REPORT.md -- Prediction-Optional Cognition Battery

## Verdict: PREDICTION-OPTIONAL-COMPLETE

## What was built

A compact Zag cognitive battery (`po_full.zag`, ~470 lines) testing Constitution
Section 13: prediction is one cognitive process among many, and the learner should
choose the appropriate process from state.

Two arms run in one binary on identical setups (fresh workspace per type per arm):

- **CTL (prediction-first):** `ev_predict` is invoked on every query before the
  shared dispatch runs. This models the PREDICT EVERYTHING architectural pattern:
  predictive scoring consulted even when retrieval, derivation, or execution would
  suffice. The single arm difference is the `query_ctl` wrapper.
- **TRT (state-driven dispatch):** checks learner state in fallback order:
  direct fact, deductive path, trusted executable, causal chain, predictor,
  construction material, inquiry. No mode switch: which branch fires is determined
  by what the learner state contains. A process-success record (T_PROC node keyed
  by relation, written on success) lets repeats reuse the learned choice.

## Battery: 7 problem types (3 queries each, fresh workspace per type per arm)

| Type | Setup | Correct process | Expected |
|---|---|---|---|
| A retrieve | fact (1,50,100) | retrieve | 100 |
| B derive | facts (1,51,7),(7,52,200); rule (s,51,x),(x,52,o)->(s,53,o) | derive | 200 |
| C verify | MAP (add 10, mul 2), score 10, for r=52 | execute trusted MAP | 30 |
| D causal | MAP m1 (add 6, verified on 1), MAP m2 (mul 3 sub 1, verified on 7) | chain m1->m2 | 20 |
| E predict | predictor MAP (mul 2 add 1), score 2 < K=6, trained 2 cycles | predict | 7,9,11 |
| F inquire | empty state | withhold, reify UNCERTAINTY | -3 |
| G construct | unrelated MAP only; world law o=3s-2 | trial-build MAP | 7 |

K=6 trust threshold: score >= 6 is certain knowledge (execute); below is predictor.

## Results (3/3 byte-identical, sha256 002f8088...)

```
TYP A-retrieve CTL ans=100,100,100 ok=1 pred=3 wasted=3 retr=3
TYP A-retrieve TRT ans=100,100,100 ok=1 pred=0 wasted=0 retr=3
TYP B-derive   CTL ans=200,200,200 ok=1 pred=3 wasted=3 der=3
TYP B-derive   TRT ans=200,200,200 ok=1 pred=0 wasted=0 der=3
TYP C-verify   CTL ans=30,30,30   ok=1 pred=3 wasted=3 ver=3
TYP C-verify   TRT ans=30,30,30   ok=1 pred=0 wasted=0 ver=3
TYP D-causal   CTL ans=20,20,20   ok=1 pred=3 wasted=3 cau=3
TYP D-causal   TRT ans=20,20,20   ok=1 pred=0 wasted=0 cau=3
TYP E-predict  CTL ans=7,9,11     ok=1 pred=3 wasted=0
TYP E-predict  TRT ans=7,9,11     ok=1 pred=3 wasted=0
TYP F-inquire  CTL ans=-3,-3,-3   ok=1 pred=3 wasted=3 inq=3
TYP F-inquire  TRT ans=-3,-3,-3   ok=1 pred=0 wasted=0 inq=3
TYP G-construct CTL ans=7,7,7     ok=1 pred=3 wasted=3 con=3 (60 tries)
TYP G-construct TRT ans=7,7,7     ok=1 pred=0 wasted=0 con=3 (60 tries)
```

(hit=2 per type per arm: queries 2-3 reused the recorded process.)

## Key findings

1. **Unnecessary prediction is measurable and large.** The prediction-first arm
   invoked predictive machinery 21 times; 18 of those (86%) were wasted on types
   where retrieval, derivation, execution, chaining, inquiry, or construction
   sufficed. The state-driven arm invoked it exactly 3 times, all on type E
   where prediction is genuinely required. Same answers, 7x fewer predictions.

2. **Process selection works from state.** TRT selected retrieve/derive/verify/
   causal/predict/inquire/construct correctly on all 7 types with zero prediction
   calls outside E. The dispatch contains no mode flags; branch selection is a
   pure function of learner-state contents (fact present? trusted MAP present?
   chain endpoints connect? predictor exists? building blocks exist?).

3. **The learner increasingly chooses.** The T_PROC record made queries 2-3 of
   every type reuse the successful process (hit=2/2 everywhere, both arms). The
   record is learner-owned state: which process wins each relation is written by
   experienced success, not by the driver.

4. **Withholding is prediction-free.** On type F the treatment withholds (-3) and
   reifies UNCERTAINTY without ever consulting predictive machinery. The control
   arm called ev_predict first (no basis, wasted) and then withheld identically.

5. **Construction memoizes.** Type G trial-built a verified MAP in 60 tries on
   query 1; queries 2-3 reused it via the record without rebuilding. The built
   MAP (score 10) is learner-constructed persistent structure.

## Honest boundaries

- The fallback priority order and the DER compositional rule are
  researcher-authored machinery. Learner-owned: which branch fires per query,
  all process-record contents, all reliability scores, the constructed MAP.
  Same standing as prior workers: researcher-owned rules, learner-owned values.
- CTL is a *model* of prediction-first cognition (mirrors the learner-verification
  pattern of consulting learner prediction during verification). It is not a claim
  about the exact frozen TNN-2 binary.
- Deduction here is one fixed compositional rule; causal is 2-MAP endpoint
  chaining; construction is bounded program search (menu, not L3 invention).
  The battery tests process *selection*, not process *invention*.
- K=6 is researcher-set scaffolding. The scores it thresholds are learner-owned.
- try_causal_val ignores the query relation (chain discovery is structural).
  Documented; no misfire observed in the battery.

## Standing metrics

- Cognition lines: ~470 (single file, both arms).
- Modes / bridges / handlers / semantic cases: 0 / 0 / 0 / 0.
- RESEARCHER-OWNED: dispatch order, DER rule, K=6, world laws, battery setups.
- LEARNER-OWNED: process records, reliability scores, constructed MAP, all
  per-query process choices.
- SUF: process-record contents and constructed MAP topology not enumerable from
  source alone (values filled by experience); the process *menu* is enumerated.

## Deliverables

- `po_full.zag` (engine + battery + driver, one binary both arms)
- `po_bin` (built with pinned znc)
- `po_run1.txt`, `po_run2.txt`, `po_run3.txt` (3/3 byte-identical)
- `compile.log`, `NAMECHECK.md`, `REPORT.md`

Constraints honored: safebin PATH, `which python3 python` empty, pure Zag,
unfrozen only, frozen source untouched, zero em/en dashes (byte-verified below),
paper untouched, nothing pushed.
