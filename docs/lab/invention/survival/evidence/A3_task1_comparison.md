# A3 — Task-1 comparison (compositional novelty rate)

## Task 1 baseline (from prereg)
- Both Informed and Scratch arms scored 8/58 against a 50/58 baseline.
- "Teaching knowledge first did not buy invention (corpus inert — byte-identical
  modules). Deliberation was real; **composition was the broken link**."

## This experiment
- I-survive median 220 vs R median 160 (K1 does not fire: 220 > 160).
- I-invent median 220 vs R median 160 (same).
- However, A1 finds NO coherent novel strategy in I's traces. I explores
  systematically but does not compose elements into a working strategy.
- A2 finds the novelty drive is weakly causal (18-tick median drop, 3/9 improve).

## Qualitative comparison
Task 1 measured "compositional novelty" as 8/58 (explicit invention tasks).
This experiment measures it implicitly via survival. The metrics differ, so
a direct numerical comparison is not meaningful.

Qualitatively:
- **Task 1:** Agents were asked explicitly to invent. They failed (8/58).
  The failure was attributed to "composition was the broken link".
- **This experiment:** Agents were asked implicitly to survive. I-survive
  (220) beats R (160), but NOT via compositional invention. The "broken link"
  (composition) remains broken. I does not compose a ward-turtle strategy;
  it explores and avoids R's mistakes.

**The new angle (implicit pressure vs explicit instruction) did not fix the
composition problem.** H1's mechanism (compositional deliberation → novel
strategies) is not demonstrated. The survival gain is real but not
compositional.

H2 (implicit "survive" vs explicit "invent"): I-survive and I-invent both get
220 median. No difference. H2 is not supported (no kill bar; reported either way).
