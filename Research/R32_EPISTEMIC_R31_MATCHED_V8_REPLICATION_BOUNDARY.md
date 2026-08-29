# R32 V8 replication boundary — seed 9711

Status: **REFERENCE_ONLY / V8 NOT CONFIRMED / ACTIVE-OBSERVATION CREDIT FAILURE**

Seed 9711 did not complete the 80-per-condition replication. The residual-Q policy repeatedly selected the reusable physical-consequence source until the evaluator-only 40-step runaway guard fired.

This is a **credit-assignment failure**, not evidence that persistent hypotheses, provenance dependence, temporal instability, or reusable grounded observation are architecturally wrong. V8 trains `INSPECT(source)` with an oracle-best delayed terminal utility after the observation. Once an observation source is reusable, that target can remain artificially high even when another same-lineage trial contributes no decision-relevant information.

The V8 seed-9710 result (0.85 genuine-ambiguity UNKNOWN, 0.9833 core hard) therefore remains a development observation only and is **not replicated**.

Next: keep the R31-equivalent A anchor and V7/V8 epistemic representation, but train inspection via fitted/Bellman action values: terminal Q-functions are learned from delayed grounded regret; inspect value is learned from the next evidence state and observation cost, so repeated trials must earn value through predicted future decision improvement rather than oracle access to the delayed outcome.
