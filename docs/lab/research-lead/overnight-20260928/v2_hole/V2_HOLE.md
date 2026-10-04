# V2 Hole Probe

## Claim Under Test
Verification criterion analysis `c2a48bee6` (V2):
`t2_revise_graph` accepts a repair iff `out != -999999` (successful re-execution).
It never checks `out == new_o`, where `new_o` is the contradicting observation.
Prediction: a repair that runs but computes something unrelated to the observation
would still be accepted.

## Method
Unfrozen variant of frozen TNN-2 (SHA-256 verified verbatim copy; cognition untouched;
only main replaced with probe driver). Three probes, each on a fresh workspace:

- **Probe 1 (adversarial):** Hand-crafted legal 4-op ISA graph with a trailing SETREG
  after the provenance-carrying SETREG:
  `g0(guard reg0==100) -> st0(set reg0<-300, prov->f0) -> st1(set reg0<-999)`.
  Executes to 999. Contradict `f0=(100,200,300)` with `new_o=500`.
  Repaired graph: `g0 -> nst(set reg0<-500) -> st1(set reg0<-999)`. Executes to 999.
  999 != 500, 999 != -999999.

- **Probe 2 (realistic):** Count graph with the exact structure `t2_asm_count` builds.
  Facts `(100,200,300)`, `(300,200,400)`. Count = 2.
  Contradict `f1=(300,200,400)` with `new_o=500`.
  Repaired graph executes to 2 (the count, unchanged by the link-value edit).
  2 != 500.

- **Probe 3 (control):** Realistic 1-hop chain. `f0=(102,12,201)`, graph computes 201.
  Contradict with `new_o=999`. Repaired graph computes 999 == new_o.
  Must be accepted (validates the probe harness).

Production entry point `revise_on_contradict` called directly (the same dispatcher
`ev_observe` uses). Acceptance signal: MAP answer field (28) updated and new fact
taught via `ev_teach_in`.

## Results (3/3 byte-identical runs)

| Probe | exec_before | new_o | map_ans_after | exec_after | Verdict |
|-------|-------------|-------|---------------|------------|---------|
| 1 (adversarial) | 999 | 500 | 999 | 999 | CONFIRMED |
| 2 (count) | 2 | 500 | 2 | 2 | CONFIRMED (vacuous) |
| 3 (control) | 201 | 999 | 999 | 999 | PASS |

- **Probe 1 CONFIRMED:** The wrong repair (999) was accepted even though the
  observation was 500. The MAP now claims `(100,200)=999`; a fact `(100,200,999)`
  was taught. The observation (500) was silently discarded. **The hole is real.**
- **Probe 2 CONFIRMED:** The repair was accepted with `out=2 != new_o=500`.
  The acceptance check is vacuous here. (Semantically defensible: the count
  genuinely did not change when the link value changed from 400 to 500.
  The check cannot distinguish this from Probe 1's wrongness.)
- **Probe 3 PASS:** Correct repair accepted. The harness works.

## Honest Scope
- The hole EXISTS in the acceptance criterion: it does not verify `out == new_o`.
- Probe 1 uses a hand-crafted graph (trailing SETREG) that the trial assemblers
  would not build. It isolates the criterion, but the exploit requires a graph
  shape outside the trial's output distribution.
- Probe 2 shows the realistic boundary: with trial-built graphs, accepted values
  are either correct (chain, terminal) or the repair fails safe (interior guard
  failure). The count case is accepted-but-unverified, coincidentally correct.
- The criterion is therefore **deficient but not currently exploited** by the
  trial's own graphs. It would become exploitable if graphs with
  value-transforming steps after provenance-carrying SETREGs ever entered
  learner state (e.g., via composition memory or hand-built procedures).
- No SUF, L3, or architecture claims. This is a correctness finding about a
  verification criterion.

## Verdict
**V2-HOLE-COMPLETE: CONFIRMED.** `t2_revise_graph` accepts repairs with
`out != new_o`. The acceptance check (`out != -999999`) cannot distinguish
correct repairs from wrong-but-running ones.

## Standing Metric (variant delta)
- RESEARCHER-OWNED STRUCTURAL DECISIONS: 0 (no cognition changes; driver only)
- LEARNER-OWNED STRUCTURAL DECISIONS: 0
- SUF DECISIONS: 0
- New cognition lines: 0
- Modes/bridges/handlers/semantic cases: 0/0/0/0
