# PREREG AMENDMENT 3: harness isolation refinements

Status: FROZEN 2026-10-02. Committed before the redesigned
implementation is run.

Two harness-side isolation refinements, both documented here
before use. Neither changes a kill bar's meaning.

1. I6 retires the training shortcut FACT (11,71,14) after training.
   Rationale: probe showed it acts as a spurious specialize
   alternative at j=0 (r=71 != 70), creating a rival 1-link [71]
   MAP that integ_explore observes first (lowest id), poisoning
   the (11,74) prediction basis with 14 before the intended [70,2]
   adaptation is observed. The FACT is training scaffolding, not
   part of the test world; removing it is the same class of
   harness management as withdrawing shortcuts in prior batteries.
   The Amendment 1 derivation for I6 stands, with exactly one
   [70,2] trial MAP per explore cycle in cycle 1 (later cycles may
   also create a benign 1-link [74] MAP from the prediction FACT;
   both execute to 99, so observations agree).

2. I5 retires the stale Q1 composite MAP_Z before its explore
   loop. Rationale: probe showed MAP_Z's contract fallback
   (un_satisfy) reanimates it via gathered live facts to terminal
   140, so Q3's native DFS selects it over the revised a2. The
   answer is correct either way, but I5's purpose is to test
   whether the KIND-DISPATCHED REVISION integrates with learner
   verification; the fallback shadow must be removed to isolate
   that path. The fallback-reanimation behavior itself is a
   genuine integration observation and is reported (REPORT
   section on integration breaks), not hidden.

3. p5 (explore FACT score) is relaxed from ==3 to >=3 in
   I1/I2/I6. Rationale: when explore observes multiple agreeing
   adapted MAPs per cycle (I6 cycles 2+), the score climbs faster
   than one point per cycle. The bar's meaning (reliable
   prediction basis established) is unchanged; the exact tick
   count was always an artifact of observation multiplicity.
